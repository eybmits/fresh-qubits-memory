#!/usr/bin/env python3
"""Reproduce manuscript Table I using Eqs. (2), (3)/(28), and (4)."""

import argparse
import csv
import json
from pathlib import Path
import platform
import sys

from fresh_qubits_memory import analyze_majority


def main() -> int:
    parser = argparse.ArgumentParser(
        description=__doc__,
        epilog="q supports at most 100 decimal places. Integer floors use adaptive precision up to 4096 working digits; more extreme cases raise an error.",
    )
    parser.add_argument("--q", default="0.9", help="depolarizing retention in (0,1); default: 0.9")
    parser.add_argument("--copies", nargs="+", type=int, default=list(range(1, 16, 2)), help="odd copy counts, 1..255; default: 1 3 5 7 9 11 13 15")
    parser.add_argument("--precision", type=int, default=80, help="output significant decimal digits, 30..512; default: 80")
    parser.add_argument("--output-dir", type=Path, default=Path("results/table1"))
    args = parser.parse_args()
    try:
        rows = [analyze_majority(args.q, r, precision=args.precision).as_dict() for r in args.copies]
    except (ValueError, ArithmeticError) as exc:
        parser.error(str(exc))
    args.output_dir.mkdir(parents=True, exist_ok=True)
    csv_path = args.output_dir / "table1.csv"
    with csv_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    metadata = {
        "source": "Supplied fresh_qubits_pra (1).pdf, Table I; Eqs. (2), (3)/(28), (4)",
        "scope": "Exact binomial-tail scalar model; does not verify the general theorem or simulate the quantum unitary.",
        "time_convention": "T is the largest integer with lambda**T >= 1/2; t=0 is the write and t counts subsequent hold cycles.",
        "method": "Exact rational binomial sum; outward-rounded Decimal logarithm and square-root bounds certify integer floors.",
        "parameters": {"q": args.q, "copies": args.copies, "decimal_precision": args.precision},
        "python_version": platform.python_version(),
        "command": ["python", "scripts/reproduce_table1.py", *sys.argv[1:]],
        "rows": rows,
    }
    metadata_path = args.output_dir / "metadata.json"
    metadata_path.write_text(json.dumps(metadata, indent=2) + "\n", encoding="utf-8")
    print(csv_path)
    print(metadata_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
