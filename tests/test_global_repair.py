"""Independent full-ancilla checks for the reduced repaired-reservoir map."""

import importlib.util
from pathlib import Path
import sys
import unittest
from unittest.mock import patch

AVAILABLE = all(importlib.util.find_spec(name) is not None for name in ("numpy", "scipy"))
if AVAILABLE:
    import numpy as np
    sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
    import simulate_global_repair as target


def independent_noise(matrix, n, q):
    paulis = (np.array([[0, 1], [1, 0]], complex),
              np.array([[0, -1j], [1j, 0]], complex), np.diag([1, -1]))
    output = matrix.copy()
    for site in range(n):
        updated = (1 + 3 * q) / 4 * output
        for pauli in paulis:
            operator = np.array([[1]], complex)
            for index in range(n):
                operator = np.kron(operator, pauli if index == site else np.eye(2))
            updated += (1 - q) / 4 * operator @ output @ operator.conj().T
        output = updated
    return output


@unittest.skipUnless(AVAILABLE, "optional NumPy/SciPy dependencies not installed")
class GlobalRepairTests(unittest.TestCase):
    def test_actual_channel_against_full_physical_dilation(self):
        rng = np.random.default_rng(2026101609)
        m, d = 3, 8
        with patch.object(target, "M", m):
            for r in (1, 3):
                fresh, remainder = 1 << r, 1 << (m - r)
                permutation = []
                for ancilla in range(fresh):
                    for memory in range(fresh):
                        for rest in range(remainder):
                            vote = int(memory.bit_count() > r // 2)
                            repaired = ancilla ^ (fresh - 1 if vote else 0)
                            permutation.append(memory * d + repaired * remainder + rest)
                self.assertEqual(len(set(permutation)), fresh * d)
                for builder in (target.sim.ising_unitary, target.sim.haar_unitary):
                    unitary = builder(m, rng)
                    full_unitary = np.kron(np.eye(fresh), unitary)
                    for variant in ("native", "decoded"):
                        for difference in (False, True):
                            a = rng.normal(size=(d, d)) + 1j * rng.normal(size=(d, d))
                            state = a @ a.conj().T
                            state /= np.trace(state)
                            if difference:
                                state -= np.eye(d) / d
                            before = unitary.conj().T @ state @ unitary if variant == "decoded" else state
                            injected = np.zeros((fresh * d, fresh * d), complex)
                            injected[:d, :d] = before
                            repaired = np.empty_like(injected)
                            repaired[np.ix_(permutation, permutation)] = injected
                            physical = independent_noise(full_unitary @ repaired @
                                                         full_unitary.conj().T, m + r, target.Q)
                            reduced = np.array([[sum(physical[a * d + i, a * d + j]
                                                     for a in range(fresh))
                                                 for j in range(d)] for i in range(d)])
                            actual = target.hold(state, r, unitary, variant, True)
                            np.testing.assert_allclose(actual, reduced, atol=2e-14, rtol=0)

    def test_repair_keeps_conditional_remainder_coherence(self):
        plus = np.array([[.5, .5], [.5, .5]])
        minus = np.array([[.5, -.5], [-.5, .5]])
        state = np.zeros((4, 4), complex)
        state[:2, :2], state[2:, 2:] = .3 * plus, .7 * minus
        with patch.object(target, "M", 2):
            np.testing.assert_allclose(target.refresh(state, 1), state, atol=1e-15)
            # Both write branches retain the SAME coherent remainder mixture.
            expected_remainder = .3 * plus + .7 * minus
            for bit in (0, 1):
                written = target.write(state, 1, bit)
                np.testing.assert_allclose(written[2 * bit:2 * bit + 2,
                                                  2 * bit:2 * bit + 2],
                                           expected_remainder, atol=1e-15)
                self.assertAlmostEqual(float(np.trace(written).real), 1.)

    def test_no_noise_preserves_repetition_code_with_decoding(self):
        unitary = target.sim.haar_unitary(3, np.random.default_rng(18))
        delta = np.zeros((8, 8), complex)
        delta[0, 0], delta[-1, -1] = 1., -1.
        encoded = unitary @ delta @ unitary.conj().T
        with patch.object(target, "M", 3), patch.object(target, "Q", 1.):
            np.testing.assert_allclose(target.hold(encoded, 3, unitary, "decoded", True),
                                       encoded, atol=2e-14, rtol=0)


if __name__ == "__main__":
    unittest.main()
