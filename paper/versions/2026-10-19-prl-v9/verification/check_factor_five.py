#!/usr/bin/env python3
"""Reproduce the finite-range factor-five check using only the standard library.

Run from any directory. Writes factor-five.json beside this script. Exact rational
majority probabilities are followed by Decimal logarithms at 100-digit precision.
This checks a finite claim about one readout of the explicit repetition reservoir,
not a universal reservoir-memory theorem or an all-k inequality.
"""
from decimal import Decimal, ROUND_CEILING, ROUND_FLOOR, localcontext
from fractions import Fraction
from hashlib import sha256
import json
from math import comb
from pathlib import Path

PRECISION = 100
Q = Fraction(9, 10)
EPSILON = Fraction(1, 100)
KS = (5, 7, 9, 11, 13, 15)
HERE = Path(__file__).resolve().parent
REPO = HERE.parents[3]
DATA_PATH = REPO / "paper/prl-source/sim/exact_numbers.json"


def decimal(value):
    return Decimal(value.numerator) / Decimal(value.denominator)


def show(value):
    return format(value, ".30g")


def main():
    saved_bytes = DATA_PATH.read_bytes()
    saved = json.loads(saved_bytes)
    with localcontext() as ctx:
        ctx.prec = PRECISION
        q, epsilon = decimal(Q), decimal(EPSILON)
        p = (1 - Q) / 2
        rows, ratios, previous = [], [], None
        for k in KS:
            r = k - 2
            error = sum(
                (Fraction(comb(r, j)) * p**j * (1 - p)**(r - j)
                 for j in range((r + 1) // 2, r + 1)), Fraction(0)
            )
            lam = 1 - 2 * error
            decay = -decimal(lam).ln()
            depth = (q / epsilon).ln() / decay
            depth_integer = int(depth.to_integral_value(rounding=ROUND_CEILING))
            half = Decimal(2).ln() / decay
            half_integer = int(half.to_integral_value(rounding=ROUND_FLOOR))
            saved_depth = Decimal(str(saved["rep_depth_q09"][str(k)]))
            relative_difference = abs(depth - saved_depth) / depth
            if relative_difference >= Decimal("1e-9"):
                raise AssertionError("Saved curve differs from the independent calculation")
            rows.append({
                "k": k, "r": r, "n": 2 * r + 2,
                "majority_error_exact": {
                    "numerator": error.numerator, "denominator": error.denominator,
                    "decimal": str(decimal(error)),
                },
                "lambda_exact": {"numerator": lam.numerator, "denominator": lam.denominator},
                "continuous_single_qubit_depth": show(depth),
                "integer_single_qubit_depth_ceil": depth_integer,
                "continuous_half_life": show(half),
                "integer_half_life_floor": half_integer,
                "saved_continuous_depth": str(saved_depth),
                "saved_relative_difference": show(relative_difference),
            })
            if previous is not None:
                old_k, old_depth, old_integer, old_half, old_half_integer = previous
                ratio = depth / old_depth
                integer_ratio = Decimal(depth_integer) / Decimal(old_integer)
                if not (ratio > 5 and integer_ratio > 5):
                    raise AssertionError("Factor-five statement fails in the stated range")
                ratios.append({
                    "from_k": old_k, "to_k": k,
                    "continuous_depth_ratio": show(ratio),
                    "integer_depth_ratio": show(integer_ratio),
                    "continuous_half_life_ratio": show(half / old_half),
                    "integer_half_life_ratio": show(Decimal(half_integer) / Decimal(old_half_integer)),
                    "continuous_and_integer_depth_ratios_exceed_five": True,
                })
            previous = k, depth, depth_integer, half, half_integer
        if not (Decimal(rows[0]["continuous_single_qubit_depth"]) > 300
                and Decimal(rows[-1]["continuous_single_qubit_depth"]) > 2000000):
            raise AssertionError("Quoted endpoint depth thresholds fail")
        continuous_ratios = [Decimal(x["continuous_depth_ratio"]) for x in ratios]
        integer_ratios = [Decimal(x["integer_depth_ratio"]) for x in ratios]
        report = {
            "revision": "2026-10-19-prl-v9",
            "method": "Exact Fraction binomial probabilities; Decimal logarithms; no stochastic simulation",
            "decimal_working_precision_digits": PRECISION,
            "reported_transcendental_significant_digits": 30,
            "parameters": {"q": "0.9", "epsilon": "0.01", "bit_flip_probability": "0.05", "k_values": list(KS)},
            "formulas": {
                "r": "k - 2 (odd)", "n": "2*r + 2",
                "p_r": "sum(comb(r,j)*p**j*(1-p)**(r-j), j=(r+1)/2,...,r)",
                "lambda_r": "1 - 2*p_r",
                "response": "q*lambda_r**t",
                "continuous_depth": "ln(q/epsilon)/(-ln(lambda_r))",
                "integer_depth": "ceil(continuous_depth)",
                "continuous_half_life": "ln(2)/(-ln(lambda_r))",
                "integer_half_life": "floor(continuous_half_life)",
                "asymptotic_two_qubit_factor": "1/(1-q**2), from p_(r+2)/p_r -> 1-q**2",
            },
            "rows": rows,
            "successive_ratios": ratios,
            "finite_range_bounds": {
                "minimum_continuous_ratio": show(min(continuous_ratios)),
                "maximum_continuous_ratio": show(max(continuous_ratios)),
                "minimum_integer_ratio": show(min(integer_ratios)),
                "maximum_integer_ratio": show(max(integer_ratios)),
                "all_five_ratios_exceed": 5,
                "depth_at_k5_exceeds": 300,
                "depth_at_k15_exceeds": 2000000,
                "interpretation": "Computed finite-range extrema at stated precision, not rigorous interval-arithmetic certificates",
            },
            "asymptotic_two_qubit_factor": show(1 / (1 - q * q)),
            "scope": {
                "supported_claim": "At q=0.9 and epsilon=0.01, for odd k=5,...,15 in the explicit repetition reservoir, every two additional input qubits increase the single-qubit memory depth by more than a factor of five.",
                "quantity": "Exact single-qubit threshold depth, which lower-bounds the full-state memory depth; not a ratio statement about the optimum over all reservoirs",
                "not_established_by_this_check": [
                    "A universal claim for every reservoir, every k, or every noise strength",
                    "The same finite ratios for full-state distinguishability or optimized memory depth",
                    "A new numerical campaign, hardware result, or proof of the universal theorem",
                ],
                "citation": "Main Figure 4(b) and Supplemental Material, The error-correcting reservoir (exact response and lower-bound formula)",
                "table_S1_qualification": "Table S1 reports integer half-lives and only selected k values; it is not a table of memory depths at epsilon=0.01.",
            },
            "saved_dataset_check": {
                "path": str(DATA_PATH.relative_to(REPO)),
                "sha256": sha256(saved_bytes).hexdigest(),
                "relative_tolerance": "1e-9",
                "all_six_values_agree_within_tolerance": True,
            },
            "reproduce": "python3 paper/versions/2026-10-19-prl-v9/verification/check_factor_five.py",
        }
    (HERE / "factor-five.json").write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
    print("Six depths and five successive ratios verified; wrote factor-five.json")


if __name__ == "__main__":
    main()
