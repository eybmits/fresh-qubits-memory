#!/usr/bin/env python3
"""Replay the supplied PRL campaign safely, without overwriting published data.

The full mode runs the original campaign and estimator-validation scripts in two
lanes. Smoke mode replays only their n=3, k=1 main configurations (six realizations
per model). Neither mode changes the simulator, its seeds, or its estimator.
"""
from __future__ import annotations

import argparse
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
import hashlib
from importlib.metadata import PackageNotFoundError, version
import json
import math
import os
from pathlib import Path
import platform
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
SIM = ROOT / "paper/prl-source/sim"
MODELS = ("ising", "haar")
THREAD_ENV = {name: "1" for name in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS")}
PARTS = {f"{p}/{c}" for p in ("single", "history")
         for c in ("randomA", "randomB", "const0", "const05", "const1")}
EXTENDED_PARTS = {"block1", "block2", "block3", "block5", "block10", "block30",
                  "patterns", "history01", "history_other", "random"}


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_json(path, data):
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(data, indent=2, allow_nan=False) + "\n")
    temporary.replace(path)


def expected_configs(mode, model, smoke=False):
    """Completeness contract for the supplied campaign, not new simulation settings."""
    base = {"model": model, "q": 0.9, "tau": 10.0, "encoding": "input"}
    if smoke:
        return [dict(base, n=3, k=1)]
    if mode == "main":
        return [dict(base, n=n, k=k) for k in (1, 2) for n in range(k + 2, 10)] + [
            dict(base, n=8, k=k) for k in (3, 4)]
    if mode == "cold":
        return [dict(base, n=8, k=k, encoding="cold") for k in (2, 3, 4)]
    if mode == "noise":
        return [dict(base, n=6, k=1, q=q) for q in (0.95, 0.98, 0.99, 0.995, 0.999, 1.0)]
    if mode == "tau":
        return [dict(base, n=6, k=1, tau=t) for t in (0.3, 1.0, 3.0, 10.0, 30.0)]
    raise ValueError(f"Unknown mode: {mode}")


def result_contract(smoke):
    contract = {}
    for mode in (("main",) if smoke else ("main", "cold", "noise")):
        for model in MODELS:
            contract[f"results_{mode}_{model}.json"] = expected_configs(mode, model, smoke)
    if not smoke:
        contract["results_tau.json"] = expected_configs("tau", "ising")
    return contract


def require(condition, message):
    if not condition:
        raise ValueError(message)


def finite_number(value):
    return type(value) in (int, float) and math.isfinite(value)


def integer(value):
    return type(value) is int and value >= 0


def load_list(path):
    require(path.is_file() and not path.is_symlink(), f"Missing or unsafe result: {path.name}")
    data = json.loads(path.read_text())
    require(isinstance(data, list), f"Expected result list: {path.name}")
    return data


def validate_results(directory, smoke=False):
    """Reject partial/duplicate configurations and truncated realization records."""
    loaded = {}
    for filename, expected in result_contract(smoke).items():
        data = load_list(directory / filename)
        require(len(data) == len(expected), f"{filename}: expected {len(expected)} configurations, got {len(data)}")
        for index, (entry, config) in enumerate(zip(data, expected)):
            label = f"{filename}[{index}]"
            require(isinstance(entry, dict), f"{label}: expected an object")
            require(all(entry.get(key) == value for key, value in config.items()),
                    f"{label}: configuration mismatch; expected {config}")
            for field in ("W", "parts", "curves", "washout"):
                require(isinstance(entry.get(field), list) and len(entry[field]) == 6,
                        f"{label}: {field} must contain all six realizations")
            for w, parts, curve, washout in zip(entry["W"], entry["parts"], entry["curves"], entry["washout"]):
                require(isinstance(parts, dict) and set(parts) == PARTS
                        and all(integer(v) for v in parts.values()), f"{label}: incomplete history-pair depths")
                require(integer(w) and w == max(parts.values()), f"{label}: invalid memory depth")
                require(isinstance(curve, list) and curve and all(finite_number(v) and v >= 0 for v in curve),
                        f"{label}: missing or nonfinite forgetting curve")
                require(isinstance(washout, dict) and isinstance(washout.get("steps"), list)
                        and len(washout["steps"]) == 3 and all(integer(s) and s > 0 for s in washout["steps"])
                        and finite_number(washout.get("residual")) and washout["residual"] >= 0,
                        f"{label}: incomplete washout record")
        loaded[filename] = data
    if not smoke:
        data = load_list(directory / "validate_pairs.json")
        expected = [(model, n, k, rep) for model in MODELS
                    for n, k in ((6, 1), (6, 2), (8, 1), (8, 2)) for rep in range(3)]
        require(len(data) == len(expected), "validate_pairs.json: expected all 24 validation records")
        for entry, config in zip(data, expected):
            require(isinstance(entry, dict) and tuple(entry.get(key) for key in ("model", "n", "k", "rep")) == config,
                    "validate_pairs.json: incomplete or duplicate configurations")
            parts = entry.get("parts")
            require(integer(entry.get("W")) and isinstance(parts, dict) and set(parts) == EXTENDED_PARTS
                    and all(integer(v) for v in parts.values()) and entry.get("W_extended") == max(parts.values()),
                    "validate_pairs.json: incomplete extended-history record")
        loaded["validate_pairs.json"] = data
    return loaded


def compare_smoke(loaded):
    """Compare the two bounded replays with the preserved numerical reference."""
    report = {}
    for model in MODELS:
        filename = f"results_main_{model}.json"
        actual = loaded[filename][0]
        baseline_path = SIM / filename
        expected = load_list(baseline_path)[0]
        require(actual["W"] == expected["W"] and actual["parts"] == expected["parts"],
                f"{model}: smoke replay differs from the supplied memory depths")
        require([w["steps"] for w in actual["washout"]] == [w["steps"] for w in expected["washout"]],
                f"{model}: smoke replay differs from the supplied washout steps")
        require([len(c) for c in actual["curves"]] == [len(c) for c in expected["curves"]],
                f"{model}: smoke replay differs from the supplied curve lengths")
        error = max(abs(x - y) for a, b in zip(actual["curves"], expected["curves"]) for x, y in zip(a, b))
        require(error <= 1e-10, f"{model}: smoke curve error {error} exceeds 1e-10")
        report[model] = {"reference_sha256": sha256(baseline_path), "memory_depths_match": True,
                         "washout_steps_match": True, "maximum_curve_absolute_error": error,
                         "curve_absolute_tolerance": 1e-10}
    return report


def merge_verified(directory, loaded, smoke):
    # Called only after all lanes and all files have passed, never on saved data.
    for mode in (("main",) if smoke else ("main", "cold", "noise")):
        write_json(directory / f"results_{mode}.json",
                   loaded[f"results_{mode}_ising.json"] + loaded[f"results_{mode}_haar.json"])


def commands(smoke):
    if smoke:
        return {model: [[sys.executable, str(Path(__file__).resolve()), "--smoke-worker", model]]
                for model in MODELS}
    return {
        "ising": [[sys.executable, str(SIM / "campaign.py"), mode, "ising"]
                  for mode in ("main", "cold", "noise")] + [[sys.executable, str(SIM / "campaign.py"), "tau"]],
        "haar": [[sys.executable, str(SIM / "campaign.py"), mode, "haar"]
                 for mode in ("main", "cold", "noise")] + [[sys.executable, str(SIM / "validate_pairs.py")]],
    }


def run_lane(name, lane_commands, directory, env, smoke):
    records = []
    with (directory / f"log_{name}.txt").open("w") as log:
        for command in lane_commands:
            log.write("Command: " + json.dumps(command) + "\n")
            log.flush()
            try:
                completed = subprocess.run(command, cwd=directory, env=env, stdout=log, stderr=subprocess.STDOUT,
                                           timeout=300 if smoke else None, check=False)
                record = {"command": command, "returncode": completed.returncode}
            except (OSError, subprocess.TimeoutExpired) as error:
                record = {"command": command, "returncode": None, "error": str(error)}
            records.append(record)
            if record["returncode"] != 0:
                break
    return records


def package_versions():
    result = {}
    for package in ("numpy", "scipy"):
        try:
            result[package] = version(package)
        except PackageNotFoundError:
            result[package] = None
    return result


def run(output_dir, smoke=False):
    directory = Path(output_dir).resolve()
    # exist_ok=False also rejects an empty preexisting directory. No resume means
    # old or partially written JSON can never satisfy a new campaign invocation.
    directory.mkdir(parents=True, exist_ok=False)
    source_files = [SIM / filename for filename in ("qrc_sim.py", "campaign.py", "validate_pairs.py")]
    source_files.append(Path(__file__).resolve())
    sources = {str(path.relative_to(ROOT)): sha256(path) for path in source_files}
    env = dict(os.environ, **THREAD_ENV, PYTHONDONTWRITEBYTECODE="1")
    plan = commands(smoke)
    manifest = {
        "status": "running", "mode": "smoke" if smoke else "full", "started_utc": datetime.now(timezone.utc).isoformat(),
        "output_directory": str(directory), "python": sys.version, "platform": platform.platform(),
        "packages": package_versions(), "source_sha256": sources, "thread_environment": THREAD_ENV,
        "precision": "NumPy float64/complex128; unchanged supplied simulator",
        "equation": "Letter Eq. (3); Supplemental Material Sec. VII (sampled memory-depth estimator)",
        "seeds": {"campaign": 2026, "extended_history_validation": 12345,
                  "campaign_streams": "[2026, model_id (Ising=1, Haar=2), n, k, 0 for unitaries / 1 for inputs]",
                  "extended_history_streams": "[12345, model_id, n, k]"},
        "epsilon": 0.01, "realizations_per_configuration": 6,
        "expected_configurations": result_contract(smoke), "commands": plan,
        "note": "Smoke covers two small configurations only; neither mode proves the universal theorem.",
    }
    manifest_path = directory / "run_manifest.json"
    write_json(manifest_path, manifest)
    try:
        with ThreadPoolExecutor(max_workers=2) as pool:
            futures = {name: pool.submit(run_lane, name, lane, directory, env, smoke) for name, lane in plan.items()}
            manifest["lanes"] = {name: future.result() for name, future in futures.items()}
        failed = [name for name, records in manifest["lanes"].items()
                  if len(records) != len(plan[name]) or any(record["returncode"] != 0 for record in records)]
        require(not failed, "Failed simulation lane(s): " + ", ".join(failed) + "; see per-lane logs")
        require(all(sha256(ROOT / path) == digest for path, digest in sources.items()),
                "Source files changed during this run")
        loaded = validate_results(directory, smoke)
        if smoke:
            manifest["reference_comparison"] = compare_smoke(loaded)
        merge_verified(directory, loaded, smoke)
        manifest["result_sha256"] = {path.name: sha256(path) for path in sorted(directory.glob("*.json"))
                                     if path.name != "run_manifest.json"}
        manifest["status"] = "complete"
    except Exception as error:
        manifest["status"] = "failed"
        manifest["error"] = str(error)
        raise
    finally:
        manifest["finished_utc"] = datetime.now(timezone.utc).isoformat()
        write_json(manifest_path, manifest)
    return manifest


def smoke_worker(model):
    sys.path.insert(0, str(SIM))
    from campaign import run_config
    result = run_config(model=model, n=3, k=1, q=0.9)
    write_json(Path(f"results_main_{model}.json"), [result])
    print(f"{model}, n=3, k=1, q=0.9: W={result['W']}", flush=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path, help="New, nonexistent directory for results and provenance (required)")
    parser.add_argument("--smoke", action="store_true", help="Only n=3,k=1 Ising/Haar, six seeded realizations each; 5-minute limit per lane")
    parser.add_argument("--smoke-worker", choices=MODELS, help=argparse.SUPPRESS)
    args = parser.parse_args()
    if args.smoke_worker:
        smoke_worker(args.smoke_worker)
        return 0
    if args.output_dir is None:
        parser.error("--output-dir is required and must not already exist")
    try:
        run(args.output_dir, args.smoke)
    except (ValueError, OSError) as error:
        parser.exit(1, f"Campaign failed: {error}\n")
    print(f"Campaign complete: {args.output_dir.resolve()} (see run_manifest.json)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
