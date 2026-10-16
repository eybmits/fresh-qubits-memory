# Reset-width numerical audit

Independent channel checks passed; no reset, partial-trace, or noise implementation discrepancy was found in these cases.

Maximum channel discrepancy: 1.11e-16. Runtime: 4.66 s.

Paired standard-reservoir witness depths (four fixed unitaries; same five continuations at every k):

| Model | n | k | Four paired witness depths |
|---|---:|---:|---|
| ising | 4 | 1 | [11, 13, 12, 12] |
| ising | 4 | 2 | [14, 15, 8, 14] |
| ising | 4 | 3 | [9, 5, 8, 9] |
| ising | 4 | 4 | [1, 1, 1, 1] |
| haar | 4 | 1 | [7, 7, 8, 7] |
| haar | 4 | 2 | [5, 5, 5, 5] |
| haar | 4 | 3 | [3, 5, 4, 4] |
| haar | 4 | 4 | [1, 1, 1, 1] |
| ising | 6 | 1 | [11, 11, 10, 12] |
| ising | 6 | 2 | [9, 9, 10, 9] |
| ising | 6 | 3 | [10, 8, 7, 7] |
| ising | 6 | 4 | [5, 8, 6, 5] |
| ising | 6 | 5 | [4, 5, 4, 4] |
| ising | 6 | 6 | [1, 1, 1, 1] |
| haar | 6 | 1 | [6, 6, 6, 6] |
| haar | 6 | 2 | [4, 4, 4, 4] |
| haar | 6 | 3 | [4, 4, 4, 4] |
| haar | 6 | 4 | [3, 3, 3, 3] |
| haar | 6 | 5 | [3, 3, 3, 3] |
| haar | 6 | 6 | [1, 1, 1, 1] |

Fixed total size, full diagonal channel with and without repair:

| n | r | k | Repair | Single-qubit witness depth | Trace-distance witness depth |
|---:|---:|---:|---|---:|---:|
| 12 | 1 | 3 | False | 43 | 43 |
| 12 | 1 | 3 | True | 43 | 43 |
| 12 | 3 | 5 | False | 43 | 47 |
| 12 | 3 | 5 | True | 309 | 316 |
| 12 | 5 | 7 | False | 43 | 49 |
| 12 | 5 | 7 | True | 1941 | 1986 |

Interpretation: a larger reset budget allows better constructions, but enlarging a reset register in an unchanged architecture can erase more information. The paired controls test that this tradeoff is not solely caused by using different random realizations across k. At k=n, one common next input erases the past exactly. Repair, rather than the reset count alone, produces the large gain in the fixed-n construction.

Limitations: finite small-system diagnostics do not prove the universal theorem or monotonicity for all architectures. The five continuations give lower witnesses, not the supremum over histories. The exact diagonal construction is a classical reversible write/hold memory and is not a trained streaming forecasting model, a hardware result, or a demonstration of quantum advantage. Passive and repair controls share size, noise, number of stored copies, and reset width, while their hold unitaries intentionally differ. Spectators are present and noisy but do not interact with the memory.
