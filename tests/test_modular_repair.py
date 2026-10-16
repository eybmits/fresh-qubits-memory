"""Independent small-channel and crossing checks for the optional hybrid study."""

import importlib.util
import math
from pathlib import Path
import unittest

AVAILABLE = all(importlib.util.find_spec(name) is not None for name in ("numpy", "scipy"))
if AVAILABLE:
    import numpy as np
    spec = importlib.util.spec_from_file_location(
        "modular_repair", Path(__file__).resolve().parents[1] / "scripts/simulate_modular_repair.py")
    simulation = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(simulation)


@unittest.skipUnless(AVAILABLE, "optional NumPy/SciPy dependencies not installed")
class ModularRepairTests(unittest.TestCase):
    def test_module_unitaries_match_supplied_reservoir_builders(self):
        original_spec = importlib.util.spec_from_file_location(
            "original_qrc_sim", Path(__file__).resolve().parents[1] / "paper/source/sim/qrc_sim.py")
        original = importlib.util.module_from_spec(original_spec)
        original_spec.loader.exec_module(original)
        for model in ("ising", "haar"):
            builder = getattr(original, model + "_unitary")
            for seed in (37, 621200):
                np.testing.assert_allclose(simulation.make_unitary(model, seed),
                                           builder(2, np.random.default_rng(seed)),
                                           rtol=0, atol=3e-15)

    def test_dense_channels_match_factorized_signed_and_positive_states(self):
        for model, seed in (("ising", 193), ("haar", 293)):
            unitary = simulation.make_unitary(model, seed)
            for copies in (1, 3):
                with self.subTest(model=model, copies=copies):
                    result = simulation.check_channel(unitary, copies, q=.73)
                    self.assertLess(result["dense_channel_max_entry_error"], 2e-12)

    def test_noiseless_repair_preserves_both_logical_values(self):
        for model in ("ising", "haar"):
            unitary = simulation.make_unitary(model, 37)
            for copies in (1, 3, 5):
                states, probabilities, transition = simulation.majority_transition(unitary, 1, copies)
                np.testing.assert_allclose(probabilities, [0, 1], atol=2e-15)
                np.testing.assert_allclose(transition, np.eye(2), atol=2e-15)
                self.assertAlmostEqual(float(np.trace(states[0] @ states[1]).real), 0, places=13)

    def test_identity_encoder_recovers_known_majority_crossings(self):
        # Extra module qubits carry no logical information for U=I. This must
        # reproduce the original repetition simulation despite different k.
        for copies, expected in ((1, 43), (3, 309), (5, 1941)):
            curves, result = simulation.simulate_case(np.eye(4), copies)
            self.assertEqual(result["depth"], expected)
            self.assertGreater(curves[expected - 1]["contrast"], .01)
            self.assertLessEqual(curves[expected]["contrast"], .01)
            passive, baseline = simulation.simulate_case(np.eye(4), copies, repair=False)
            self.assertEqual(baseline["depth"], 43)

    def test_exact_threshold_is_not_counted_as_remembered(self):
        curves, result = simulation.simulate_case(np.eye(4), 1, q=.5, epsilon=.25)
        self.assertEqual(result["depth"], 1)
        self.assertEqual(curves[1]["contrast"], .25)

    def test_stopping_rule_bounds_later_readout_revivals(self):
        unitary = simulation.make_unitary("haar", 621200)
        for repair in (False, True):
            curves, result = simulation.simulate_case(unitary, 3, repair=repair)
            depth = result["depth"]
            self.assertLessEqual(curves[-1]["module_trace_distance"], .01)
            self.assertEqual(result["first_not_above"], curves[depth]["contrast"])
            self.assertTrue(all(row["contrast"] <= .01 for row in curves[depth:]))
            self.assertTrue(all(row["contrast"] <= row["module_trace_distance"] + 1e-13
                                for row in curves))
            self.assertTrue(all(after["module_trace_distance"] <= before["module_trace_distance"] + 1e-13
                                for before, after in zip(curves, curves[1:])))
        # This passive example needs extra cycles after the readout crosses;
        # those trailing cycles are necessary for the certified stopping rule.
        curves, result = simulation.simulate_case(unitary, 3, repair=False)
        self.assertGreater(len(curves), result["depth"] + 1)

    def test_noise_implementation_on_entangled_state(self):
        state = np.array([1, 0, 0, 1j]) / math.sqrt(2)
        density = np.outer(state, state.conj())
        for q in (0, .63, 1):
            np.testing.assert_allclose(simulation.depolarize(density, q),
                                       simulation.independent_pauli_noise(density, q, 2),
                                       atol=1e-14)


if __name__ == "__main__":
    unittest.main()
