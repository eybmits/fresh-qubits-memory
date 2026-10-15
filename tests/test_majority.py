"""Independent checks of the manuscript's scalar majority-refresh example."""

from decimal import Decimal, ROUND_HALF_UP, localcontext
from fractions import Fraction
from itertools import product
import unittest

from fresh_qubits_memory import analyze_majority, majority_error, readable_lifetime


class MajorityTests(unittest.TestCase):
    def test_exact_error_against_enumerated_outcomes(self):
        # Enumerate individual noisy strings, independently of binomial coefficients.
        p = Fraction(1, 20)
        for r in (1, 3, 5, 7):
            expected = Fraction(0)
            for bits in product((0, 1), repeat=r):
                flips = sum(bits)
                if flips > r // 2:
                    expected += p**flips * (1 - p) ** (r - flips)
            self.assertEqual(majority_error("0.9", r), expected)

    def test_table_one_entries(self):
        lifetimes = [6, 47, 298, 1790, 10431, 59739, 337940, 1894286]
        guarantees = [0, 3, 15, 83, 440, 2316, 12191, 64163]
        errors = ["5.0e-2", "7.3e-3", "1.2e-3", "1.9e-4", "3.3e-5", "5.8e-6", "1.0e-6", "1.8e-7"]
        for r, lifetime, guarantee, error in zip(range(1, 16, 2), lifetimes, guarantees, errors):
            with self.subTest(r=r), localcontext() as context:
                context.prec = 100
                result = analyze_majority("0.9", r)
                self.assertEqual(result.lifetime_cycles, lifetime)
                self.assertEqual(result.guaranteed_cycles, guarantee)
                self.assertEqual(result.fresh_qubits, r + 2)
                self.assertEqual(result.total_qubits, 2 * r + 2)
                # The manuscript uses half-up rounding: exact p_3=0.00725
                # appears as 7.3e-3 (Decimal's default half-even gives 7.2e-3).
                self.assertEqual(result.logical_error.quantize(Decimal(error), rounding=ROUND_HALF_UP), Decimal(error))
                # Independent high-precision power checks catch off-by-one errors.
                self.assertGreaterEqual(result.decay_factor**lifetime, Decimal("0.5"))
                self.assertLess(result.decay_factor ** (lifetime + 1), Decimal("0.5"))
                self.assertLessEqual(guarantee, lifetime)

    def test_single_copy_and_exact_threshold(self):
        self.assertEqual(majority_error("0.9", 1), Fraction(1, 20))
        self.assertEqual(analyze_majority("0.9", 1).decay_factor, Decimal("0.9"))
        self.assertEqual(analyze_majority("0.5", 1).lifetime_cycles, 1)
        self.assertEqual(analyze_majority("0.499999999999999999999999999999", 1).lifetime_cycles, 0)
        self.assertEqual(analyze_majority("0.500000000000000000000000000001", 1).lifetime_cycles, 1)

    def test_markov_recurrence_and_error_bound(self):
        for q, r in (("0.3", 3), ("0.7", 5), ("0.9", 7)):
            error = majority_error(q, r)
            decay = 1 - 2 * error
            probability_zero = Fraction(1)
            for t in range(11):
                self.assertEqual(2 * probability_zero - 1, decay**t)
                probability_zero = probability_zero * (1 - error) + (1 - probability_zero) * error
            # Square both nonnegative sides to avoid a numerical square root.
            self.assertLessEqual(error**2, (1 - Fraction(q) ** 2) ** r)

    def test_tiny_errors_do_not_round_lifetime_to_infinity(self):
        error = majority_error("0.999999", 31)
        result = analyze_majority("0.999999", 31, precision=40)
        self.assertLess(error, Fraction(1, 10**80))
        self.assertEqual(result.lifetime_cycles, readable_lifetime(error, precision=90))
        with localcontext() as context:
            context.prec = 250
            decay = Decimal((1 - 2 * error).numerator) / Decimal((1 - 2 * error).denominator)
            self.assertGreaterEqual(decay**result.lifetime_cycles, Decimal("0.5"))
            self.assertLess(decay ** (result.lifetime_cycles + 1), Decimal("0.5"))

    def test_input_validation(self):
        for q in ("0", "1", "-0.1", "1.1", "NaN", "Infinity", "bad", True, None, "1e-101"):
            with self.subTest(q=q), self.assertRaises(ValueError):
                majority_error(q, 3)
        for r in (0, -1, 2, 4, 257, 3.0, True):
            with self.subTest(r=r), self.assertRaises(ValueError):
                majority_error("0.9", r)
        for precision in (0, 29, 513, 80.0, True):
            with self.subTest(precision=precision), self.assertRaises(ValueError):
                analyze_majority("0.9", 3, precision=precision)
        for error in (Fraction(0), Fraction(1, 2), Fraction(-1), 0.1):
            with self.subTest(error=error), self.assertRaises(ValueError):
                readable_lifetime(error)


if __name__ == "__main__":
    unittest.main()
