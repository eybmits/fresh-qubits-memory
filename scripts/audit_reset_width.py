#!/usr/bin/env python3
"""Paired reset-width and independent-channel audit; see the dated protocol."""

import argparse
import csv
import hashlib
import json
import math
from pathlib import Path
import platform
import shlex
import sys
import time

import numpy as np
import scipy

SCRIPT = Path(__file__).resolve()
STANDALONE = (SCRIPT.parent / "qrc_sim.py").is_file()
ROOT = SCRIPT.parents[1]
SIM_DIRECTORY = SCRIPT.parent if STANDALONE else ROOT / "paper/source/sim"
PROTOCOL = (SCRIPT.parent / "reset-width-audit-2026-10-16.md" if STANDALONE
            else ROOT / "experiments/reset-width-audit-2026-10-16.md")
DEFAULT_OUTPUT = (ROOT / "audit-results" if STANDALONE
                  else ROOT / "results/reset-width-audit-2026-10-16")
sys.path.insert(0, str(SIM_DIRECTORY))
import qrc_sim as supplied

SEED = 2026101601
Q, EPSILON = .9, .01


def write_csv(directory, name, rows):
    with (directory / name).open("w", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def independent_trace(matrix, n, k):
    """Direct index sum, with no reshape/einsum implementation shared."""
    rest = 1 << (n-k)
    return np.array([[sum(matrix[a*rest+i, a*rest+j] for a in range(1 << k))
                      for j in range(rest)] for i in range(rest)])


def independent_noise(matrix, n, q):
    """Compose full Pauli matrices; separate from supplied trace/reinsert map."""
    paulis = [np.array([[0, 1], [1, 0]], complex),
              np.array([[0, -1j], [1j, 0]], complex),
              np.diag([1., -1.]).astype(complex)]
    out = matrix.copy()
    for site in range(n):
        updated = (1+3*q)/4 * out
        for pauli in paulis:
            operator = np.array([[1.]], complex)
            for index in range(n):
                operator = np.kron(operator, pauli if index == site else np.eye(2))
            updated += (1-q)/4 * operator @ out @ operator.conj().T
        out = updated
    return out


def audit_channels():
    rng = np.random.default_rng(SEED)
    rows = []
    for n in range(1, 5):
        d = 1 << n
        samples = []
        for _ in range(2):
            a = rng.normal(size=(d,d)) + 1j*rng.normal(size=(d,d))
            state = a @ a.conj().T
            samples.append(state / np.trace(state))
        unitary = supplied.haar_unitary(n, rng)
        for k in range(1, n+1):
            encoding = supplied.fn_state(.31, k)
            for q in (.1, .9, 1.):
                errors = []
                for matrix in (samples[0], samples[0]-samples[1]):
                    reduced = independent_trace(matrix, n, k)
                    errors.append(float(np.max(np.abs(reduced-supplied.ptrace_in(matrix,n,k)))))
                    injected = np.kron(encoding, reduced)
                    expected = independent_noise(unitary@injected@unitary.conj().T,n,q)
                    observed = supplied.step(matrix,encoding,unitary,n,k,q)
                    errors.append(float(np.max(np.abs(expected-observed))))
                assert max(errors) < 2e-13, (n,k,q,errors)
                rows.append(dict(n=n,k=k,q=q,max_absolute_error=max(errors)))
    return rows


def paired_sweep():
    rows, curves, summaries = [], [], []
    for n in (4, 6):
        for model_index, model in enumerate(("ising", "haar")):
            for replicate in range(4):
                seed = SEED + 10000*n + 100*model_index + replicate
                unitary_rng = np.random.default_rng(seed)
                builder = supplied.ising_unitary if model == "ising" else supplied.haar_unitary
                unitary = builder(n, unitary_rng)
                # Independent stream, cached before varying reset width.
                input_seed = seed + 1_000_000
                input_rng = np.random.default_rng(input_seed)
                sequences = [input_rng.uniform(size=140) for _ in range(2)]
                sequences += [np.full(140, value) for value in (0., .5, 1.)]
                for k in range(1, n+1):
                    depths = []
                    for sequence_index, sequence in enumerate(sequences):
                        state = np.eye(1 << n, dtype=complex)/(1 << n)
                        for value in sequence[:60]:
                            state = supplied.step(state, supplied.fn_state(value,k),unitary,n,k,Q)
                        delta = (supplied.step(state,supplied.fn_state(1.,k),unitary,n,k,Q)
                                 - supplied.step(state,supplied.fn_state(0.,k),unitary,n,k,Q))
                        distance = supplied.trace_distance(delta)
                        depth = int(distance > EPSILON)
                        max_upward_drift = 0.
                        for delay in range(81):
                            if delay:
                                delta = supplied.step(delta,supplied.fn_state(sequence[59+delay],k),unitary,n,k,Q)
                                new_distance = supplied.trace_distance(delta)
                                max_upward_drift = max(max_upward_drift,new_distance-distance)
                                distance = new_distance
                            if distance > EPSILON:
                                depth = delay+1
                            if replicate == 0:
                                curves.append(dict(model=model,n=n,k=k,replicate=replicate,
                                                   continuation=sequence_index,delay=delay,trace_distance=distance))
                            # CPTP contraction proves no later recrossing is possible.
                            if delay and distance < .003:
                                break
                        assert max_upward_drift < 1e-12
                        if k == n:
                            assert depth == 1 and distance < 1e-12
                        rows.append(dict(model=model,n=n,k=k,replicate=replicate,
                                         unitary_seed=seed,input_seed=input_seed,
                                         continuation=sequence_index,witness_depth=depth,
                                         stopped_delay=delay,last_distance=distance,
                                         maximum_upward_drift=max_upward_drift))
                        depths.append(depth)
                    summaries.append(dict(model=model,n=n,k=k,replicate=replicate,
                                          unitary_seed=seed,input_seed=input_seed,
                                          witness_depth=max(depths)))
            print(f"paired {model} n={n} complete",flush=True)
    return rows, curves, summaries


def full_permutation(r, n):
    """Enumerate physical gates independently for all 2**n basis strings."""
    result = []
    for label in range(1 << n):
        bits = [(label >> (n-1-index)) & 1 for index in range(n)]
        a, c, b = bits[:r], bits[r], bits[r+1]
        x, spectators = bits[r+2:2*r+2], bits[2*r+2:]
        vote = b if c else int(sum(x)>r//2)
        output = x + [c,b] + [bit ^ vote for bit in a] + spectators
        result.append(sum(bit << (n-1-index) for index,bit in enumerate(output)))
    result = np.asarray(result, dtype=np.int64)
    assert np.unique(result).size == 1 << n
    return result


def diagonal_noise(values, n):
    p = (1-Q)/2
    result = values.copy()
    for index in range(n):
        blocks = result.reshape(-1, 2, 1 << (n-1-index))
        zero, one = blocks[:,0].copy(), blocks[:,1].copy()
        blocks[:,0] = (1-p)*zero + p*one
        blocks[:,1] = p*zero + (1-p)*one
    return result


def diagonal_step(values, r, n, control, bit, permutation, repair=True):
    """The passive control uses one fixed unitary: write on c=1, identity on c=0.

    These orthogonal control sectors are invariant, so their direct sum is
    reversible. The branch below exploits the freshly fixed classical c value;
    it is not a changed unitary or an external intervention during a trajectory.
    """
    # Physical input register is first r+2 qubits; spectators follow memory.
    marginal = values.reshape(1 << (r+2), -1).sum(axis=0)
    injected = np.zeros_like(values)
    injected.reshape(1 << (r+2), -1)[2*control+bit] = marginal
    if repair or control:
        evolved = np.empty_like(injected)
        evolved[permutation] = injected
    else:
        evolved = injected
    return diagonal_noise(evolved, n)


def fixed_size_repair():
    n = 12
    records, summaries = [], []
    labels = np.arange(1 << n)
    for r in (1,3,5):
        permutation = full_permutation(r,n)
        initial = np.full(1 << n, 1/(1 << n))
        written = [diagonal_step(initial,r,n,1,b,permutation) for b in (0,1)]
        start = written[0]-written[1]
        observable = 1-2*((labels >> (n-2*r-2)) & 1)
        p = (1-Q)/2
        error = sum(math.comb(r,j)*p**j*(1-p)**(r-j) for j in range(r//2+1,r+1))
        log_lambda = math.log1p(-2*error)
        for repair in (False,True):
            delta = start.copy()
            depth_z = depth_trace = 0
            maximum_error = 0.
            trace_leakage = 0.
            for delay in range(10_000):
                z = float(abs(observable @ delta)/2)
                distance = float(np.abs(delta).sum()/2)
                expected = Q*math.exp(delay*log_lambda) if repair else Q**(delay+1)
                maximum_error = max(maximum_error,abs(z-expected))
                trace_leakage = max(trace_leakage,float(abs(delta.sum())))
                if z > EPSILON:
                    depth_z = delay+1
                if distance > EPSILON:
                    depth_trace = delay+1
                records.append(dict(n=n,r=r,k=r+2,repair=repair,delay=delay,
                                    single_qubit_gap_over_two=z,trace_distance=distance,
                                    predicted_single_qubit_gap=expected))
                if distance < EPSILON and z < EPSILON:
                    break
                delta = diagonal_step(delta,r,n,0,0,permutation,repair=repair)
            assert delay < 9999 and maximum_error < 2e-11 and trace_leakage < 2e-11
            summaries.append(dict(n=n,r=r,k=r+2,repair=repair,
                                  single_qubit_witness_depth=depth_z,
                                  trace_distance_witness_depth=depth_trace,
                                  last_delay=delay,max_readout_error=maximum_error,
                                  maximum_trace_leakage=trace_leakage))
        print(f"fixed n={n}, r={r} complete",flush=True)
    return records,summaries


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir",type=Path,default=DEFAULT_OUTPUT,
                        help=f"Output directory (default: {DEFAULT_OUTPUT})")
    args = parser.parse_args()
    required_sources = [SCRIPT, PROTOCOL, SIM_DIRECTORY / "qrc_sim.py"]
    optional_sources = [SIM_DIRECTORY / "campaign.py", SIM_DIRECTORY / "results_main.json"]
    missing_required = [str(path) for path in required_sources if not path.is_file()]
    if missing_required:
        parser.error("Required provenance input is missing: " + ", ".join(missing_required))
    args.output_dir.mkdir(parents=True,exist_ok=True)
    start = time.perf_counter()
    checks = audit_channels()
    continuation_rows,curve_rows,paired_rows = paired_sweep()
    repetition_rows,repetition_summary = fixed_size_repair()
    for name,rows in (("channel_checks.csv",checks),
                      ("paired_continuations.csv",continuation_rows),
                      ("paired_curves_replicate0.csv",curve_rows),
                      ("paired_depths.csv",paired_rows),
                      ("fixed_size_repair_curves.csv",repetition_rows),
                      ("fixed_size_repair_depths.csv",repetition_summary)):
        write_csv(args.output_dir,name,rows)
    sources = required_sources + [path for path in optional_sources if path.is_file()]
    metadata = dict(seed=SEED,q=Q,epsilon=EPSILON,precision="complex128 / float64",
                    command=shlex.join([sys.executable,*sys.argv]),
                    python=sys.version,numpy=np.__version__,scipy=scipy.__version__,
                    platform=platform.platform(),seconds=time.perf_counter()-start,
                    channel_checks=len(checks),paired_configurations=len(paired_rows),
                    unitary_realizations=len({(row["n"],row["model"],row["replicate"]) for row in paired_rows}),
                    maximum_channel_error=max(row["max_absolute_error"] for row in checks),
                    layout="standalone_source_package" if STANDALONE else "research_repository",
                    sources={str(path.relative_to(ROOT)):hashlib.sha256(path.read_bytes()).hexdigest()
                             for path in sources},
                    missing_optional_provenance=[str(path.relative_to(ROOT)) for path in optional_sources
                                                 if not path.is_file()],
                    outputs={path.name:hashlib.sha256(path.read_bytes()).hexdigest()
                             for path in args.output_dir.glob("*.csv")})
    (args.output_dir/"metadata.json").write_text(json.dumps(metadata,indent=2)+"\n")
    report = ["# Reset-width numerical audit", "", "Independent channel checks passed; no reset, partial-trace, or noise implementation discrepancy was found in these cases.",
              "",f"Maximum channel discrepancy: {metadata['maximum_channel_error']:.3g}. Runtime: {metadata['seconds']:.2f} s.",
              "", "Paired standard-reservoir witness depths (four fixed unitaries; same five continuations at every k):", "",
              "| Model | n | k | Four paired witness depths |", "|---|---:|---:|---|"]
    for n in (4,6):
        for model in ("ising","haar"):
            for k in range(1,n+1):
                values = [row["witness_depth"] for row in paired_rows if row["n"]==n and row["model"]==model and row["k"]==k]
                report.append(f"| {model} | {n} | {k} | {values} |")
    report += ["", "Fixed total size, full diagonal channel with and without repair:", "",
               "| n | r | k | Repair | Single-qubit witness depth | Trace-distance witness depth |", "|---:|---:|---:|---|---:|---:|"]
    for row in repetition_summary:
        report.append(f"| {row['n']} | {row['r']} | {row['k']} | {row['repair']} | {row['single_qubit_witness_depth']} | {row['trace_distance_witness_depth']} |")
    report += ["", "Interpretation: a larger reset budget allows better constructions, but enlarging a reset register in an unchanged architecture can erase more information. The paired controls test that this tradeoff is not solely caused by using different random realizations across k. At k=n, one common next input erases the past exactly. Repair, rather than the reset count alone, produces the large gain in the fixed-n construction.",
               "", "Limitations: finite small-system diagnostics do not prove the universal theorem or monotonicity for all architectures. The five continuations give lower witnesses, not the supremum over histories. The exact diagonal construction is a classical reversible write/hold memory and is not a trained streaming forecasting model, a hardware result, or a demonstration of quantum advantage. Passive and repair controls share size, noise, number of stored copies, and reset width, while their hold unitaries intentionally differ. Spectators are present and noisy but do not interact with the memory.", ""]
    (args.output_dir/"REPORT.md").write_text("\n".join(report))
    print(json.dumps({"seconds":metadata["seconds"],"channel_error":metadata["maximum_channel_error"],"repair_summary":repetition_summary},indent=2))


if __name__ == "__main__":
    main()
