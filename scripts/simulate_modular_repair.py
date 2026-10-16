#!/usr/bin/env python3
"""Exact encoded Ising/Haar module memory with fresh-ancilla majority repair.

This is a modular engineered hybrid, not an unchanged global Ising/Haar
reservoir. Each of r two-qubit modules stores U|b,0>. A hold cycle decodes,
computes the majority into fresh modules, swaps out the old modules, encodes,
and then independently depolarizes every physical qubit. At fixed n=22,
k=2r+2 includes two write/input controls. Spectators are decoupled and noisy.
The two conditional product states close exactly under this channel; their
signed weights are propagated one cycle at a time to the measured crossing.
Requires NumPy and SciPy. No manuscript files are modified.
"""

import argparse
import csv
import hashlib
import json
import math
from pathlib import Path
import platform
import sys
import time

import numpy as np
import scipy
from scipy.stats import unitary_group

N, Q, EPSILON = 22, 0.9, 0.01
COPIES = (1, 3, 5)
SEED_BASES = {"ising": 621100, "haar": 621200}
I = np.eye(2, dtype=complex)
X = np.array([[0, 1], [1, 0]], dtype=complex)
Y = np.array([[0, -1j], [1j, 0]], dtype=complex)
Z = np.diag([1, -1]).astype(complex)


def kron_power(matrix, copies):
    result = np.ones((1, 1), dtype=complex)
    for _ in range(copies):
        result = np.kron(result, matrix)
    return result


def make_unitary(model, seed):
    """Same two-qubit Ising convention/Haar generator as supplied qrc_sim.py."""
    rng = np.random.default_rng(seed)
    if model == "ising":
        coupling = rng.uniform(-0.5, 0.5)
        hamiltonian = coupling * np.kron(X, X) + np.kron(Z, I) + np.kron(I, Z)
        values, vectors = np.linalg.eigh(hamiltonian)
        return (vectors * np.exp(-10j * values)) @ vectors.conj().T
    if model == "haar":
        return unitary_group.rvs(4, random_state=rng)
    raise ValueError("model must be 'ising' or 'haar'")


def depolarize(state, q, qubits=2):
    """Partial-trace form of independent local depolarization; linear on deltas."""
    result = state.copy()
    dimension = 1 << qubits
    if state.shape != (dimension, dimension) or not 0 <= q <= 1:
        raise ValueError("incompatible state or noise")
    for site in range(qubits):
        before, after = 1 << site, 1 << (qubits - site - 1)
        tensor = result.reshape(before, 2, after, before, 2, after)
        partial = tensor[:, 0, :, :, 0, :] + tensor[:, 1, :, :, 1, :]
        tensor = q * tensor
        tensor[:, 0, :, :, 0, :] += (1 - q) * partial / 2
        tensor[:, 1, :, :, 1, :] += (1 - q) * partial / 2
        result = tensor.reshape(dimension, dimension)
    return result


def independent_pauli_noise(state, q, qubits):
    """Independent reference implementation using a Kraus/Pauli sum per site."""
    result = state.copy()
    for site in range(qubits):
        updated = np.zeros_like(result)
        for weight, pauli in zip(((1 + 3 * q) / 4,) + ((1 - q) / 4,) * 3,
                                 (I, X, Y, Z)):
            operator = np.kron(np.eye(1 << site),
                               np.kron(pauli, np.eye(1 << (qubits - site - 1))))
            updated += weight * operator @ result @ operator.conj().T
        result = updated
    return result


def encoded_branches(unitary, q):
    states = []
    for index in (0, 2):
        vector = unitary[:, index]  # |b,0> in big-endian qubit order.
        states.append(depolarize(np.outer(vector, vector.conj()), q))
    return np.asarray(states)


def majority_probability(probability, copies):
    if copies < 1 or copies % 2 != 1:
        raise ValueError("copies must be a positive odd integer")
    return sum(math.comb(copies, count) * probability**count
               * (1 - probability)**(copies - count)
               for count in range(copies // 2 + 1, copies + 1))


def majority_transition(unitary, q, copies):
    """Columns are the new logical bit conditioned on the previous bit."""
    states = encoded_branches(unitary, q)
    probabilities = []
    for state in states:
        decoded = unitary.conj().T @ state @ unitary
        probability = float(np.trace(decoded[2:, 2:]).real)
        if not -1e-12 <= probability <= 1 + 1e-12:
            raise ArithmeticError("invalid decoded probability")
        probabilities.append(float(np.clip(probability, 0, 1)))
    votes = [majority_probability(value, copies) for value in probabilities]
    transition = np.array([[1 - votes[0], 1 - votes[1]], votes])
    return states, np.asarray(probabilities), transition


def dense_repair(state, unitary, q, copies):
    """Reduced-memory reference: decode dense state, enumerate vote, reset/encode.

    Tracing the old memory after reversible majority-compute and swap gives
    precisely this measure-and-prepare map. No independence of the input is
    assumed here. Noise is applied using an independent Pauli implementation.
    """
    decoder = kron_power(unitary.conj().T, copies)
    decoded = decoder @ state @ decoder.conj().T
    weights = np.zeros(2, dtype=complex)
    for label, value in enumerate(np.diag(decoded)):
        ones = sum((label >> (2 * index + 1)) & 1 for index in range(copies))
        weights[int(ones > copies // 2)] += value
    result = np.zeros_like(state)
    for bit, weight in enumerate(weights):
        vector = unitary[:, 2 * bit]
        pure = np.outer(vector, vector.conj())
        result += weight * kron_power(pure, copies)
    return independent_pauli_noise(result, q, 2 * copies)


def simulate_case(unitary, copies, *, q=Q, epsilon=EPSILON, repair=True,
                  max_cycles=100_000):
    """Return per-cycle linear contrast and actual integer crossing depth."""
    if not 0 < q < 1 or not 0 < epsilon < 1:
        raise ValueError("simulation needs q and epsilon strictly between zero and one")
    states, probabilities, transition = majority_transition(unitary, q, copies)
    observable = unitary @ np.kron(Z, I) @ unitary.conj().T
    delta = states[0] - states[1]
    weights = np.array([1.0, -1.0])
    curves, depth = [], 0
    previous_distance = 1.0
    for delay in range(max_cycles):
        if repair:
            delta = sum(weight * state for weight, state in zip(weights, states))
        contrast = float(abs(np.trace(observable @ delta)) / 2)
        distance = float(np.abs(np.linalg.eigvalsh((delta + delta.conj().T) / 2)).sum() / 2)
        if contrast > distance + 2e-12 or distance > previous_distance + 2e-12:
            raise AssertionError("readout bound or module trace contraction failed")
        previous_distance = distance
        curves.append({"delay": delay, "contrast": contrast,
                       "module_trace_distance": distance})
        if contrast > epsilon:
            depth = delay + 1
        # A fixed observable could dip and revive. The contracting module
        # trace-distance bound certifies that no future revival can exceed eps.
        # For repaired trajectories the exact two-state closure also guarantees
        # contraction of this marginal (the logical difference is one scalar).
        if distance <= epsilon:
            break
        if repair:
            weights = transition @ weights
        else:
            # Same encoded write state. During hold U and Udag cancel, fresh
            # ancillas are unused; each physical memory qubit still sees noise.
            delta = depolarize(delta, q)
    else:
        raise RuntimeError("Threshold was not crossed; no extrapolation is permitted")
    if depth and not (curves[depth - 1]["contrast"] > epsilon >= curves[depth]["contrast"]):
        raise AssertionError("invalid threshold crossing")
    if any(point["contrast"] > epsilon for point in curves[depth:]):
        raise AssertionError("a later above-threshold readout was missed")
    return curves, {"depth": depth, "decoded_p1_given_0": probabilities[0],
                    "decoded_p1_given_1": probabilities[1],
                    "logical_eigenvalue": transition[1, 1] - transition[1, 0],
                    "initial_contrast": curves[0]["contrast"],
                    "last_above": curves[depth - 1]["contrast"] if depth else None,
                    "first_not_above": curves[depth]["contrast"],
                    "terminal_module_trace_distance": curves[-1]["module_trace_distance"],
                    "cycles_simulated": len(curves)}


def check_channel(unitary, copies, q=Q):
    states, probabilities, transition = majority_transition(unitary, q, copies)
    product_states = [kron_power(state, copies) for state in states]
    errors = []
    for weights in (np.array([.37, .63]), np.array([1., -1.])):
        dense_input = sum(weight * state for weight, state in zip(weights, product_states))
        got = dense_repair(dense_input, unitary, q, copies)
        expected = sum(weight * state for weight, state in
                       zip(transition @ weights, product_states))
        errors.append(float(np.max(np.abs(got - expected))))
    residual = float(np.max(np.abs(unitary.conj().T @ unitary - np.eye(4))))
    if max(errors) > 2e-12 or residual > 2e-12:
        raise AssertionError("dense reference channel or unitarity check failed")
    if min(np.linalg.eigvalsh(state).min() for state in states) < -1e-12:
        raise AssertionError("nonpositive conditional state")
    if not np.allclose(transition.sum(axis=0), 1, atol=1e-13):
        raise AssertionError("nonstochastic transition")
    if not np.all((0 <= transition) & (transition <= 1)):
        raise AssertionError("invalid transition probability")
    return {"copies": copies, "dense_channel_max_entry_error": max(errors),
            "unitary_max_entry_residual": residual,
            "probability_min": float(probabilities.min()),
            "probability_max": float(probabilities.max())}


def save_csv(path, rows):
    with path.open("w", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def run(output, replicates=8):
    output = Path(output).resolve()
    output.mkdir(parents=True, exist_ok=True)
    start = time.perf_counter()
    depth_rows, curve_rows, checks, unitaries = [], [], [], []
    for model in ("ising", "haar"):
        for replicate in range(replicates):
            seed = SEED_BASES[model] + replicate
            unitary = make_unitary(model, seed)
            unitaries.append({"model": model, "replicate": replicate, "seed": seed,
                              "real": unitary.real.tolist(), "imag": unitary.imag.tolist(),
                              "sha256_complex128_le": hashlib.sha256(
                                  unitary.astype("<c16").tobytes()).hexdigest()})
            for copies in COPIES:
                if copies <= 3:
                    checks.append({"model": model, "replicate": replicate, "seed": seed,
                                   **check_channel(unitary, copies)})
                for repair in (False, True):
                    curves, result = simulate_case(unitary, copies, repair=repair)
                    prefix = {"model": model, "replicate": replicate, "seed": seed,
                              "n": N, "module_qubits": 2, "r": copies,
                              "k": 2 * copies + 2, "repair": repair,
                              "q": Q, "epsilon": EPSILON}
                    depth_rows.append({**prefix, **result})
                    curve_rows.extend({**prefix, **row} for row in curves)
            print(f"{model} seed={seed}: repaired depths " +
                  str([row["depth"] for row in depth_rows[-6:] if row["repair"]]), flush=True)
    save_csv(output / "depths.csv", depth_rows)
    save_csv(output / "curves.csv", curve_rows)
    save_csv(output / "channel_checks.csv", checks)
    (output / "unitaries.json").write_text(json.dumps(unitaries, indent=2) + "\n")
    names = ("depths.csv", "curves.csv", "channel_checks.csv", "unitaries.json")
    metadata = {
        "method": "Exact conditional product-state channel; signed weights propagated per cycle",
        "architecture": "Two-qubit Ising/Haar encoders embedded in a modular majority-repaired hybrid",
        "not_claimed": "Not an unchanged or global Ising/Haar reservoir; no trained forecasting task or hardware",
        "resources": {"n": N, "copies": COPIES, "k": [2 * r + 2 for r in COPIES],
                      "fresh_per_copy": 2, "control_qubits": 2,
                      "active_qubits": [4 * r + 2 for r in COPIES],
                      "spectator_qubits": [N - 4 * r - 2 for r in COPIES]},
        "input": "One write input b=0 or 1 followed by identical hold inputs",
        "initial_state": "Writing swaps out the entire prior memory, so written state is independent of initialization",
        "unitaries": "Same U for every module and every r for a replicate; full fixed repair circuit depends on r",
        "ising_parameters": {"module_qubits": 2, "J": 1, "h": 1, "tau": 10,
                             "Hamiltonian": "J12 X1 X2 + Z1 + Z2; J12 uniform [-0.5,0.5]"},
        "seed_bases": SEED_BASES, "replicates": replicates,
        "noise": "Independent local depolarization on all physical qubits after each ideal cycle",
        "q": Q, "epsilon": EPSILON,
        "readout": "Fixed linear observable U(Z tensor I)Udag on the first two-qubit module",
        "depth": "1 + largest delay with half absolute readout difference > epsilon; write delay is zero",
        "stopping_rule": "Continue until one-module trace distance <= epsilon, bounding all later readout revivals; depth records last above-threshold contrast",
        "passive_control": "Same encoded writes/resources/noise; during holds decode and encode cancel without repair",
        "dense_reference": "Independent dense 2r-qubit reduced-memory channel, explicit vote enumeration and Pauli noise; r=1,3",
        "precision": "complex128/float64", "python": sys.version, "numpy": np.__version__,
        "scipy": scipy.__version__, "platform": platform.platform(),
        "seconds": time.perf_counter() - start, "argv": sys.argv,
        "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "outputs": {name: hashlib.sha256((output / name).read_bytes()).hexdigest() for name in names},
    }
    (output / "metadata.json").write_text(json.dumps(metadata, indent=2) + "\n")
    return depth_rows, curve_rows, metadata


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path, default=Path("modular-repair-results"))
    parser.add_argument("--replicates", type=int, default=8)
    args = parser.parse_args()
    if not 1 <= args.replicates <= 100:
        parser.error("replicates must be from 1 to 100")
    run(args.output_dir, args.replicates)


if __name__ == "__main__":
    main()
