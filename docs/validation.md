# Initial validation record

**Follow-up:** the [16 October independent numerical validation](../results/empirical-2026-10-16/REPORT.md) extends this scalar baseline to the full diagonal construction, physical sampling, small quantum channels, and cooling. The historical record below describes the original six tests only. With the optional validation dependencies installed, the current suite has 12 passing test methods.

Validated on 15 October 2026 with Python 3.14.7 in an isolated virtual environment. The package installed successfully with `python -m pip install -e .`.

```bash
python -m unittest discover -s tests -v
python scripts/reproduce_table1.py --output-dir results/table1
```

All **six test methods passed**, including their parameterized subcases. The committed CSV and JSON contain all eight default rows.

| Check | Evidence |
| --- | --- |
| Source preservation | The repository PDF matches the supplied file byte-for-byte and its recorded SHA-256 checksum. |
| Exact binomial probabilities | Rational binomial-tail sums agree with explicit enumeration of noisy bit strings for `r = 1, 3, 5, 7`. |
| Table I | All eight readable lifetimes and all eight conservative integer guarantees match the manuscript at `q = 0.9`. Logical-error probabilities match its displayed rounding. |
| Lifetime boundaries | High-precision direct powers satisfy `λ^T ≥ 1/2` and `λ^(T+1) < 1/2` for every Table I row. |
| Equality convention | `λ = 1/2` gives `T = 1`; nearby values are checked on either side. |
| Recurrence | A two-state Markov update agrees with the scalar decay on several small examples; the stated majority-error bound also holds in those cases. |
| Rare-error stability | An error below `10^-80` gives the same finite integer lifetime at two output precisions, with independent boundary checks. |
| Input validation | Invalid `q`, copy counts, precisions and error probabilities are rejected. |

For `r = 3`, the exact probability is `0.00725`. Table I displays `7.3 × 10^-3`, corresponding to half-up rounding at that tie. Python Decimal's default half-even display would give `7.2 × 10^-3`. The test explicitly uses half-up **only for comparison with the manuscript's printed probability**; the exact calculation is unchanged.

The GitHub workflow runs installation, these tests and the reproduction script on Python 3.11 and 3.13. Its live run status is recorded by GitHub Actions separately from this local validation record.

This evidence validates the scalar numerical example within the tested scope. It does not validate the full reversible circuit, prove the contraction or learning theorems, establish novelty, or reproduce the cooling construction. Those tasks remain in [the research plan](research-plan.md).
