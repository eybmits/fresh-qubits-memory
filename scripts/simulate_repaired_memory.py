#!/usr/bin/env python3
"""Simulate the majority-refresh memory at fixed n=12; no manuscript changes.

Requirements: numpy, matplotlib. Run with --output-dir PATH.
The channel is evolved explicitly; the formula is only an independent check.
"""

import argparse
import csv
import hashlib
import json
import math
import os
from pathlib import Path
import platform
import sys
import time

import numpy as np

N, Q, EPSILON = 12, 0.9, 0.01
COPIES = (1, 3, 5)


def majority_permutation(r):
    """Bijective gate on [fresh ancillas, control, bit, memory, spectators]."""
    permutation = []
    for label in range(1 << N):
        bits = [(label >> (N - 1 - i)) & 1 for i in range(N)]
        ancillas, control, bit = bits[:r], bits[r], bits[r + 1]
        memory, spectators = bits[r + 2:2 * r + 2], bits[2 * r + 2:]
        vote = bit if control else int(sum(memory) > r // 2)
        # Compute vote into fresh ancillas, then swap with the old memory.
        output = memory + [control, bit] + [a ^ vote for a in ancillas] + spectators
        permutation.append(sum(b << (N - 1 - i) for i, b in enumerate(output)))
    permutation = np.asarray(permutation, dtype=np.int64)
    assert np.unique(permutation).size == 1 << N
    return permutation


def noise(state):
    """Independent depolarization, restricted exactly to diagonal states."""
    p = (1 - Q) / 2
    output = state.copy()
    for site in range(N):
        blocks = output.reshape(-1, 2, 1 << (N - 1 - site))
        zero, one = blocks[:, 0].copy(), blocks[:, 1].copy()
        blocks[:, 0] = (1 - p) * zero + p * one
        blocks[:, 1] = p * zero + (1 - p) * one
    return output


def step(state, r, control, bit, permutation, repair):
    """Reset -> fixed reversible gate -> noise, also valid for differences."""
    retained = state.reshape(1 << (r + 2), -1).sum(axis=0)
    injected = np.zeros_like(state)
    injected.reshape(1 << (r + 2), -1)[2 * control + bit] = retained
    # The passive comparator's fixed gate writes in the c=1 sector and is
    # identity in the c=0 sector. These sectors are invariant and orthogonal.
    if repair or control:
        evolved = np.empty_like(injected)
        evolved[permutation] = injected
    else:
        evolved = injected
    return noise(evolved)


def simulate():
    curves, depths = [], []
    labels = np.arange(1 << N)
    for r in COPIES:
        permutation = majority_permutation(r)
        initial = np.full(1 << N, 1 / (1 << N))
        written = [step(initial, r, 1, b, permutation, True) for b in (0, 1)]
        for state in written:
            assert state.min() >= 0 and abs(state.sum() - 1) < 1e-12
        # Last memory qubit; its Z expectation is a linear readout.
        observable = 1 - 2 * ((labels >> (N - 2 * r - 2)) & 1)
        p = (1 - Q) / 2
        vote_error = sum(math.comb(r, j) * p**j * (1 - p)**(r - j)
                         for j in range(r // 2 + 1, r + 1))
        log_lambda = math.log1p(-2 * vote_error)
        for repair in (False, True):
            delta = written[0] - written[1]
            z_depth = trace_depth = 0
            max_error = max_trace_leakage = 0.0
            previous_trace = 1.0
            for delay in range(10_000):
                contrast = float(abs(observable @ delta) / 2)
                trace_distance = float(np.abs(delta).sum() / 2)
                expected = Q * math.exp(delay * log_lambda) if repair else Q**(delay + 1)
                max_error = max(max_error, abs(contrast - expected))
                max_trace_leakage = max(max_trace_leakage, float(abs(delta.sum())))
                assert contrast <= trace_distance + 1e-12
                assert trace_distance <= previous_trace + 1e-12
                previous_trace = trace_distance
                if contrast > EPSILON:
                    z_depth = delay + 1
                if trace_distance > EPSILON:
                    trace_depth = delay + 1
                curves.append(dict(n=N, r=r, k=r + 2, repair=repair,
                                   delay=delay, single_qubit_contrast=contrast,
                                   trace_distance=trace_distance))
                if contrast < EPSILON and trace_distance < EPSILON:
                    break
                delta = step(delta, r, 0, 0, permutation, repair)
            else:
                raise RuntimeError("Threshold not crossed; no extrapolation permitted")
            assert max_error < 2e-11 and max_trace_leakage < 2e-11
            # Strict > threshold: equality is already forgotten. This formula
            # checks the integer count; it is never used to evolve the state.
            analytic_depth = math.ceil(math.log(EPSILON / Q) /
                                       (log_lambda if repair else math.log(Q)))
            assert z_depth == analytic_depth
            depths.append(dict(n=N, r=r, k=r + 2, repair=repair,
                               single_qubit_depth=z_depth,
                               trace_distance_depth=trace_depth,
                               max_formula_error=max_error,
                               max_trace_leakage=max_trace_leakage))
        print(f"n={N}, k={r + 2}: repair {depths[-1]['single_qubit_depth']}, "
              f"passive {depths[-2]['single_qubit_depth']}", flush=True)
    return curves, depths


def save_csv(path, records):
    with path.open("w", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(records[0]))
        writer.writeheader()
        writer.writerows(records)


def plot(output, curves, depths):
    os.environ.setdefault("MPLCONFIGDIR", str(output / ".matplotlib"))
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    plt.rcParams.update({"font.size": 11, "axes.spines.top": False,
                         "axes.spines.right": False, "pdf.fonttype": 42})
    colors = ("#86b6e7", "#347dcc", "#123f87")
    fig, (left, right) = plt.subplots(1, 2, figsize=(10.2, 4.2),
                                    gridspec_kw={"width_ratios": [1.35, 1]})
    for r, color in zip(COPIES, colors):
        data = [row for row in curves if row["r"] == r and row["repair"]]
        # Include the write cycle: delay=0 is displayed at cycle 1.
        left.semilogx([row["delay"] + 1 for row in data],
                      [row["single_qubit_contrast"] for row in data],
                      color=color, lw=2.5, label=f"k = {r + 2}")
    left.axhline(EPSILON, color="#777777", lw=1, ls="--")
    left.text(1.3, EPSILON + .03, "threshold = 0.01", color="#666666", fontsize=9)
    left.set(xlabel="Cycles including the write cycle", ylabel="Single-qubit contrast",
             ylim=(0, 1), title="Newly simulated memory traces")
    left.legend(frameon=False, loc="upper right")
    repaired = [row for row in depths if row["repair"]]
    right.semilogy([row["k"] for row in repaired],
                   [row["single_qubit_depth"] for row in repaired],
                   "o-", color=colors[-1], lw=2, ms=7)
    for row in repaired:
        right.annotate(str(row["single_qubit_depth"]),
                       (row["k"], row["single_qubit_depth"]),
                       xytext=(0, 10), textcoords="offset points", ha="center")
    right.set(xlabel="Fresh qubits per cycle k", ylabel="Readout witness depth",
              xticks=[3, 5, 7], xlim=(2.6, 7.4), ylim=(25, 4000),
              title="Gain from majority repair")
    for ax in (left, right):
        ax.grid(alpha=.18, which="major")
    fig.suptitle("Fixed total size n = 12  |  Depolarizing noise q = 0.9", y=1.01, fontsize=13)
    fig.tight_layout()
    fig.savefig(output / "repaired_memory.png", dpi=200, bbox_inches="tight")
    fig.savefig(output / "repaired_memory.pdf", bbox_inches="tight")
    plt.close(fig)
    return matplotlib.__version__


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path, default=Path("repaired-memory-results"))
    args = parser.parse_args()
    output = args.output_dir.resolve()
    output.mkdir(parents=True, exist_ok=True)
    start = time.perf_counter()
    curves, depths = simulate()
    save_csv(output / "curves.csv", curves)
    save_csv(output / "depths.csv", depths)
    matplotlib_version = plot(output, curves, depths)
    files = ("curves.csv", "depths.csv", "repaired_memory.png", "repaired_memory.pdf")
    metadata = dict(n=N, q=Q, epsilon=EPSILON, copies=COPIES,
                    k=[r + 2 for r in COPIES], precision="float64",
                    method="Explicit complete diagonal channel, 4096 entries; no extrapolation",
                    input="One write input b=0 or b=1, followed by identical hold inputs",
                    depth_definition="1 + largest delay with contrast > epsilon; write is delay 0",
                    unitary="Fixed within each trajectory; corresponding majority circuit for each k",
                    noise="Independent depolarization on every physical qubit after each ideal gate cycle",
                    seed=None, randomness="None: exact probability propagation",
                    python=sys.version, numpy=np.__version__, matplotlib=matplotlib_version,
                    platform=platform.platform(), seconds=time.perf_counter() - start,
                    argv=sys.argv, script_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                    outputs={name: hashlib.sha256((output / name).read_bytes()).hexdigest() for name in files})
    (output / "metadata.json").write_text(json.dumps(metadata, indent=2) + "\n")
    print(f"Saved simulation, data and plots to {output}")


if __name__ == "__main__":
    main()
