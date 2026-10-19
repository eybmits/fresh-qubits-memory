#!/usr/bin/env python3
"""Check or rebuild the current PRL paper in an isolated, newly created directory.

Examples (run from the repository root):
  python scripts/reproduce_paper.py check --output-dir results/local/paper-check
  python scripts/reproduce_paper.py figures --output-dir results/local/paper-figures
  python scripts/reproduce_paper.py build --output-dir results/local/paper-build

Install Python dependencies with ``pip install -e '.[paper]'``. Figures also
require a TeX installation; build requires BibTeX and REVTeX 4.2. All commands,
logs, input hashes, and output hashes are recorded in manifest.json. The check
command runs bounded numerical diagnostics, not the complete simulation campaign
and not a proof of the universal theorem. Supplied data and manuscript files are
never modified. Choose a new output directory for each run.
"""

import argparse
from datetime import datetime, timezone
import hashlib
import importlib.metadata
import importlib.util
import json
import os
from pathlib import Path
import platform
import re
import shutil
import subprocess
import sys
import time


REPO = Path(__file__).resolve().parents[1]
SOURCE = REPO / "paper" / "prl-source"
FIGURES = [f"fig{i}.pdf" for i in range(1, 5)] + [f"figS{i}.pdf" for i in range(1, 8)]
MAIN = "memory_limits_prl"


def file_hash(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def hashes(directory):
    return {p.relative_to(directory).as_posix(): file_hash(p)
            for p in sorted(directory.rglob("*"))
            if p.is_file() and "__pycache__" not in p.parts}


def prepare_output(source, output):
    """Copy the inputs once; never reuse outputs left by a previous run."""
    source, output = source.resolve(), output.resolve()
    if output == source or source in output.parents or output in source.parents:
        raise ValueError("Output must be separate from the canonical source tree.")
    if output.exists() and (not output.is_dir() or any(output.iterdir())):
        raise ValueError("Output directory is not empty; choose a new directory.")
    if any(p.is_symlink() for p in source.rglob("*")):
        raise ValueError("Canonical source contains a symlink; review it before copying.")
    output.mkdir(parents=True, exist_ok=True)
    staged = output / "source"
    shutil.copytree(source, staged, ignore=shutil.ignore_patterns(
        "__pycache__", "*.pyc", "*.aux", "*.log", "*.out", "*.blg", "*.fls",
        "*.fdb_latexmk", "*.synctex.gz", ".DS_Store"))
    return staged


class Runner:
    """Run a command and require newly produced, nonempty outputs."""

    def __init__(self, output, manifest):
        self.output, self.manifest = output, manifest
        self.log_dir = output / "logs"
        self.log_dir.mkdir()
        self.env = dict(os.environ, MPLCONFIGDIR=str(output / "matplotlib-cache"),
                        PYTHONDONTWRITEBYTECODE="1", OPENBLAS_NUM_THREADS="1",
                        OMP_NUM_THREADS="1", MKL_NUM_THREADS="1",
                        VECLIB_MAXIMUM_THREADS="1", NUMEXPR_NUM_THREADS="1")
        # Existing checks use assert; do not silently disable them via the environment.
        self.env.pop("PYTHONOPTIMIZE", None)
        manifest["thread_environment"] = {name: self.env[name] for name in (
            "OPENBLAS_NUM_THREADS", "OMP_NUM_THREADS", "MKL_NUM_THREADS",
            "VECLIB_MAXIMUM_THREADS", "NUMEXPR_NUM_THREADS")}

    def run(self, command, cwd, expected=()):
        expected = [cwd / name for name in expected]
        for path in expected:
            path.unlink(missing_ok=True)
        number = len(self.manifest["commands"]) + 1
        log = self.log_dir / f"{number:02d}.log"
        record = {"argv": list(command), "cwd": str(cwd.relative_to(self.output)),
                  "log": str(log.relative_to(self.output)), "status": "running"}
        self.manifest["commands"].append(record)
        print(f"[{number}] {' '.join(command[:2])} ({record['cwd']})", flush=True)
        started = time.monotonic()
        try:
            with log.open("w") as stream:
                result = subprocess.run(command, cwd=cwd, env=self.env,
                                        stdout=stream, stderr=subprocess.STDOUT, check=False)
            record["returncode"] = result.returncode
            if result.returncode:
                raise RuntimeError(f"Command failed with exit {result.returncode}; see {log}")
            for path in expected:
                if not path.is_file() or path.stat().st_size == 0:
                    raise RuntimeError(f"Command did not produce a nonempty {path}; see {log}")
                if path.suffix == ".pdf" and not path.read_bytes().startswith(b"%PDF-"):
                    raise RuntimeError(f"Invalid PDF output: {path}")
            record["status"] = "success"
            record["outputs"] = {str(p.relative_to(self.output)): file_hash(p) for p in expected}
        except Exception as error:
            record["status"], record["error"] = "failed", str(error)
            raise
        finally:
            record["seconds"] = round(time.monotonic() - started, 3)
            if log.exists():
                record["log_sha256"] = file_hash(log)


def check_numbers(runner, source):
    # Several supplied diagnostics print predicates. Check their computed values
    # explicitly as well, so a false predicate cannot result in a green command.
    diagnostics = [
        ("checks", "verify_constants.py", '''
w = d["worst"]
assert w["closed"] < 1e-25 and w["old"] < 1e-25, w
assert w["two_norm"] >= -1e-12 and w["mono"] <= 1 + 1e-12, w
assert w["simp4"] >= -1e-12 and w["simp1"] >= -1e-12, w
assert d["g1"].max() <= 1 + 1e-12
assert d["g2"].min() >= -1e-12 and d["g3"].min() >= -1e-12
'''),
        ("checks", "verify_simple_proof.py", '''
import numpy as np
assert d["worst"] <= 1 + 1e-12
q, s, a, cq, bth = (d[n] for n in ("q", "s", "a", "cq", "bth"))
np.testing.assert_allclose(cq * 4.0 ** (-a), 2.0 ** (4 - 5 * s), atol=1e-14)
assert np.all(a + 1 <= 2 * s + 1e-12)
assert np.all(bth >= 1 - q - 1e-12)
assert np.all(1 - 2.0 ** (-bth) >= bth / 2 - 1e-12)
assert (2 * s * 2.0 ** (4 - 5 * s)).max() <= 1 + 1e-12
'''),
        ("sim", "test_sim.py", '''
import numpy as np
for r in (1, 3):
    U, n = d["rep_unitary"](r)
    k, q = r + 2, 0.9
    rho = np.eye(2 ** n, dtype=complex) / 2 ** n
    X = (d["step"](rho, d["rep_input"](1, r), U, n, k, q)
         - d["step"](rho, d["rep_input"](0, r), U, n, k, q))
    p = sum(d["comb"](r, j) * .05 ** j * .95 ** (r - j)
            for j in range(r // 2 + 1, r + 1))
    signs = np.array([1 if i % 2 == 0 else -1 for i in range(2 ** n)])
    for lag in range(8):
        actual = abs(np.dot(signs, X.diagonal()).real) / 2
        np.testing.assert_allclose(actual, q * (1 - 2 * p) ** lag, atol=2e-13, rtol=0)
        X = d["step"](X, d["rep_input"]("blank", r), U, n, k, q)
np.testing.assert_allclose(d["depolarize_all"](np.diag([1., 0.]), 1, .9),
                           np.diag([.95, .05]), atol=1e-14)
'''),
    ]
    for directory, script, assertions in diagnostics:
        code = f"import runpy\nd = runpy.run_path({script!r})\n" + assertions
        runner.run([sys.executable, "-c", code], source / directory)
    runner.run([sys.executable, "quoted_numbers.py"], source / "sim")


def make_figures(runner, source):
    figures = source / "figures"
    manuscript = (source / f"{MAIN}.tex").read_text()
    included = set(re.findall(r"\\includegraphics(?:\[[^\]]*\])?\{([^}]+)\}", manuscript))
    if included != set(FIGURES):
        raise RuntimeError("The manuscript figure list changed; update the regeneration plan first.")
    # The manuscript includes PDFs in its own directory, not in figures/. Remove
    # those old copies first, and only repopulate them after every build succeeds.
    for name in FIGURES:
        (source / name).unlink(missing_ok=True)
        (figures / name).unlink(missing_ok=True)
    latex = ["pdflatex", "-interaction=nonstopmode", "-halt-on-error", "-no-shell-escape"]
    runner.run([*latex, "fig1.tex"], figures, ["fig1.pdf"])
    for number, panel in ((2, "fig2a"), (3, "fig3a"), (4, "fig4bc")):
        runner.run([sys.executable, f"{panel}.py"], figures, [f"{panel}.pdf"])
        runner.run([*latex, f"fig{number}.tex"], figures, [f"fig{number}.pdf"])
    runner.run([sys.executable, "figS.py"], figures, FIGURES[4:])
    copied = {}
    for name in FIGURES:
        produced = figures / name
        if not produced.is_file() or produced.stat().st_size == 0:
            raise RuntimeError(f"Missing regenerated figure: {produced}")
        shutil.copy2(produced, source / name)
        if file_hash(source / name) != file_hash(produced):
            raise RuntimeError(f"Figure copy verification failed: {name}")
        copied[name] = file_hash(produced)
    runner.manifest["manuscript_figure_sha256"] = copied


def build_manuscript(runner, source):
    latex = ["pdflatex", "-interaction=nonstopmode", "-halt-on-error", "-no-shell-escape",
             "-recorder", f"{MAIN}.tex"]
    runner.run(latex, source, [f"{MAIN}.pdf"])
    runner.run(["bibtex", MAIN], source, [f"{MAIN}.bbl"])
    for _ in range(2):
        runner.run(latex, source, [f"{MAIN}.pdf"])
    log = (source / f"{MAIN}.log").read_text(errors="replace")
    if re.search(r"(?:Reference|Citation) .+ undefined|There were undefined references|"
                 r"Label\(s\) may have changed", log):
        raise RuntimeError("Unresolved references remain in the final LaTeX log.")
    # Confirm the recorder names the copies that were regenerated, rather than
    # an alternative file found through a TeX search path.
    inputs = set()
    for line in (source / f"{MAIN}.fls").read_text(errors="replace").splitlines():
        if line.startswith("INPUT "):
            inputs.add((source / line[6:]).resolve())
    for name in FIGURES:
        if (source / name).resolve() not in inputs:
            raise RuntimeError(f"LaTeX did not record the freshly copied figure: {name}")
    runner.manifest["latex_figure_inputs_verified"] = True


def prerequisites(mode):
    modules = ("numpy", "scipy", "mpmath") if mode == "check" else ("numpy", "scipy", "matplotlib")
    missing = [name for name in modules if importlib.util.find_spec(name) is None]
    if missing:
        raise ValueError(f"Missing Python modules: {', '.join(missing)}; install .[paper].")
    tools = [] if mode == "check" else ["latex", "pdflatex"]
    if mode == "build":
        tools.append("bibtex")
    for tool in tools:
        if not shutil.which(tool):
            raise ValueError(f"Missing TeX tool {tool}; install a full TeX Live or MacTeX distribution.")
    versions = {name: importlib.metadata.version(name) for name in modules}
    # https://github.com/matplotlib/matplotlib/issues/31925: silent loss of
    # minus signs in usetex PDF output. It affects the Fig. 3 exponent here.
    if versions.get("matplotlib", "").split("+")[0] == "3.11.0":
        raise ValueError("Matplotlib 3.11.0 drops minus signs in TeX PDF output; "
                         "install .[paper] to select a compatible version (3.11.1 or newer, or 3.10.x).")
    return versions


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("mode", choices=("check", "figures", "build"))
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args(argv)
    manifest = {"mode": args.mode, "status": "running", "commands": [],
                "started_utc": datetime.now(timezone.utc).isoformat(),
                "python": sys.version, "platform": platform.platform(),
                "wrapper_sha256": file_hash(Path(__file__)),
                "scope": "Bounded diagnostics or figure regeneration from supplied data; no full campaign.",
                "diagnostic_random_seed": 1 if args.mode == "check" else None,
                "numeric_precision": ("mpmath 40 decimal digits; NumPy float64/complex128"
                                      if args.mode == "check" else "Supplied data; NumPy float64")}
    output = args.output_dir.resolve()
    try:
        manifest["dependencies"] = prerequisites(args.mode)
        source = prepare_output(SOURCE, output)
    except (OSError, ValueError) as error:
        parser.error(str(error))
    manifest["input_sha256"] = hashes(source)
    manifest["git_commit"] = None
    if shutil.which("git"):
        git = subprocess.run(["git", "rev-parse", "HEAD"], cwd=REPO, capture_output=True, text=True)
        if git.returncode == 0:
            manifest["git_commit"] = git.stdout.strip()
    runner = Runner(output, manifest)
    try:
        if args.mode == "check":
            check_numbers(runner, source)
        else:
            make_figures(runner, source)
            if args.mode == "build":
                build_manuscript(runner, source)
        manifest["status"] = "success"
    except Exception as error:
        manifest["status"], manifest["error"] = "failed", str(error)
        print(f"ERROR: {error}", file=sys.stderr)
    finally:
        after = hashes(source)
        manifest["changed_or_new_outputs_sha256"] = {
            key: value for key, value in after.items() if manifest["input_sha256"].get(key) != value}
        manifest["finished_utc"] = datetime.now(timezone.utc).isoformat()
        (output / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    print(f"{manifest['status']}: {output / 'manifest.json'}")
    return 0 if manifest["status"] == "success" else 1


if __name__ == "__main__":
    raise SystemExit(main())
