#!/usr/bin/env python3
"""Exact fixed-five-qubit Ising/Haar core with native or decoded repair."""

import argparse
import csv
import hashlib
import json
from pathlib import Path
import platform
import sys
import time

import numpy as np
import scipy

HERE = Path(__file__).resolve().parent
SIM = HERE if (HERE / "qrc_sim.py").exists() else HERE.parent / "paper/source/sim"
sys.path.insert(0, str(SIM))
import qrc_sim as sim

M, N, Q, EPSILON = 5, 12, .9, .01
BASE_SEED = 2026101602


def refresh(matrix, r):
    """Majority reset of r sites, preserving conditional remainder blocks."""
    a, b = 1 << r, 1 << (M - r)
    blocks = matrix.reshape(a, b, a, b)
    result = np.zeros_like(blocks)
    for label in range(a):
        target = a - 1 if label.bit_count() > r // 2 else 0
        result[target, :, target, :] += blocks[label, :, label, :]
    return result.reshape(1 << M, 1 << M)


def write(matrix, r, bit):
    a, b = 1 << r, 1 << (M - r)
    rest = np.einsum("aiaj->ij", matrix.reshape(a, b, a, b))
    result = np.zeros_like(matrix).reshape(a, b, a, b)
    target = a - 1 if bit else 0
    result[target, :, target, :] = rest
    return result.reshape(1 << M, 1 << M)


def hold(matrix, r, unitary, variant, repair):
    if variant == "native":
        state = refresh(matrix, r) if repair else matrix
        state = unitary @ state @ unitary.conj().T
    elif variant == "decoded":
        if repair:
            decoded = unitary.conj().T @ matrix @ unitary
            state = unitary @ refresh(decoded, r) @ unitary.conj().T
        else:
            state = matrix
    else:
        raise ValueError(variant)
    return sim.depolarize_all(state, M, Q)


def common_state(r, unitary, variant, repair):
    state = np.eye(1 << M, dtype=complex) / (1 << M)
    for iteration in range(1, 10_001):
        next_state = hold(state, r, unitary, variant, repair)
        # Roundoff correction only; check trace drift independently below.
        residual = float(np.linalg.norm(next_state - state))
        state = next_state
        if residual < 1e-12:
            break
    else:
        raise RuntimeError("Common hold state did not converge")
    assert abs(np.trace(state) - 1) < 2e-10
    assert np.linalg.eigvalsh(state).min() > -2e-12
    return state, iteration, residual


def trajectory(r, unitary, variant, repair):
    state, iterations, residual = common_state(r, unitary, variant, repair)
    # In the decoded variant the fixed c=1 write sector also decodes before
    # writing, so the retained remainder uses the same logical coordinates.
    before_write = unitary.conj().T @ state @ unitary if variant == "decoded" else state
    branches = [sim.depolarize_all(unitary @ write(before_write, r, bit) @
                                  unitary.conj().T, M, Q) for bit in (0, 1)]
    delta = branches[0] - branches[1]
    values, vectors = np.linalg.eigh(delta)
    observable = (vectors * np.sign(values)) @ vectors.conj().T
    trace_depth = readout_depth = 0
    maximum_drift = maximum_trace_leakage = 0.
    previous = 1.
    curve = []
    for delay in range(10_000):
        distance = float(sim.trace_distance(delta))
        contrast = float(abs(np.trace(observable @ delta)) / 2)
        maximum_drift = max(maximum_drift, distance - previous)
        maximum_trace_leakage = max(maximum_trace_leakage, float(abs(np.trace(delta))))
        assert contrast <= distance + 1e-11
        assert np.max(np.abs(delta - delta.conj().T)) < 2e-11
        if distance > EPSILON:
            trace_depth = delay + 1
        if contrast > EPSILON:
            readout_depth = delay + 1
        curve.append(dict(delay=delay, core_trace_distance=distance,
                          fixed_readout_contrast=contrast))
        if distance < EPSILON:
            break
        previous = distance
        delta = hold(delta, r, unitary, variant, repair)
    else:
        raise RuntimeError("No threshold crossing; no extrapolation permitted")
    assert maximum_drift < 2e-11 and maximum_trace_leakage < 2e-10
    summary = dict(core_trace_depth=trace_depth, fixed_readout_depth=readout_depth,
                   common_state_iterations=iterations, common_state_residual=residual,
                   maximum_upward_drift=maximum_drift,
                   maximum_trace_leakage=maximum_trace_leakage)
    return summary, curve


def save_csv(path, rows):
    with path.open("w", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path, default=Path("global-repair-results"))
    parser.add_argument("--replicates", type=int, default=8)
    args = parser.parse_args()
    if not 1 <= args.replicates <= 100:
        parser.error("replicates must be between 1 and 100")
    args.output_dir.mkdir(parents=True, exist_ok=True)
    start = time.perf_counter()
    rows, curves, unitaries = [], [], []
    for model_index, model in enumerate(("ising", "haar")):
        builder = sim.ising_unitary if model == "ising" else sim.haar_unitary
        for replicate in range(args.replicates):
            seed = BASE_SEED + 1000 * model_index + replicate
            unitary = builder(M, np.random.default_rng(seed))
            assert np.max(np.abs(unitary.conj().T @ unitary - np.eye(1 << M))) < 1e-12
            unitaries.append(dict(model=model, replicate=replicate, seed=seed,
                                  sha256=hashlib.sha256(unitary.tobytes()).hexdigest()))
            for variant in ("native", "decoded"):
                for r in (1, 3, 5):
                    for repair in (False, True):
                        identity = dict(model=model, replicate=replicate, seed=seed,
                                        variant=variant, repair=repair, n=N, core_qubits=M,
                                        r=r, k=r + 2, q=Q, epsilon=EPSILON)
                        summary, curve = trajectory(r, unitary, variant, repair)
                        rows.append(dict(**identity, **summary))
                        curves.extend(dict(**identity, **point) for point in curve)
            print(f"{model} replicate {replicate + 1}/{args.replicates} complete", flush=True)
    save_csv(args.output_dir / "depths.csv", rows)
    save_csv(args.output_dir / "curves.csv", curves)
    source_files = (Path(__file__).resolve(), SIM / "qrc_sim.py")
    metadata = dict(n=N, core_qubits=M, q=Q, epsilon=EPSILON, replicates=args.replicates,
                    base_seed=BASE_SEED, unitaries=unitaries, precision="complex128",
                    python=sys.version, numpy=np.__version__, scipy=scipy.__version__,
                    platform=platform.platform(), argv=sys.argv,
                    seconds=time.perf_counter() - start,
                    method="Exact 32x32 reduced-core CPTP channels; conditional correlations retained",
                    metrics="Core trace witness and fixed initial-Helstrom linear-readout witness",
                    source_hashes={p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in source_files},
                    outputs={name: hashlib.sha256((args.output_dir / name).read_bytes()).hexdigest()
                             for name in ("depths.csv", "curves.csv")})
    (args.output_dir / "metadata.json").write_text(json.dumps(metadata, indent=2) + "\n")
    print(f"Saved {len(rows)} runs, {len(curves)} curve points; {metadata['seconds']:.2f}s")


if __name__ == "__main__":
    main()
