# Research plan

This plan turns the supplied manuscript into an auditable scientific project. It separates reproduction of reported results from mathematical review and new research. A completed numerical check must be recorded with its command, parameters, output, tolerance, and software version; passing it does not certify a theorem.

## Priority 0 — Establish a reliable baseline

| Work item | Source anchor | Completion criterion |
| --- | --- | --- |
| Preserve the exact supplied PDF and provenance. | Source manuscript | Record the original filename and a cryptographic hash; distinguish the supplied manuscript from later versions. Do not invent DOI, publication date, or license. |
| Reproduce the majority probabilities, decay factors, lifetimes, and analytical guarantees in Table I. | Eqs. (2)–(4), (28); Table I | Independently evaluate the binomial tail at `q = 0.9` for all eight odd `r` values, reproduce the printed rounding, and verify both defining lifetime inequalities. |
| Confirm conventions and small cases. | Eqs. (5)–(7), (26)–(28) | Document that `q` is retention, `p = (1 − q)/2`, the write is `t = 0`, `k = r + 2`, and `n = 2r + 2`; recover `λ_1 = q` and `f_b(0) = (−1)^b q`. |
| Audit numerical stability. | Eq. (28), Table I | Evaluate lifetimes with stable logarithms; test near half-signal integer boundaries and rare binomial tails; report the supported parameter range. Avoid interpreting floating-point `λ_r = 1` as infinite physical memory. |
| Recover the original supplemental script if available. | Reference [6] | Obtain a separately identified source version and compare its output with the independent implementation. Until then, label repository code as a new reproduction, not the author's supplied supplement. |

Use deterministic calculations for exact table reproduction. Monte Carlo is a secondary cross-check with explicit seeds and uncertainty; it is unsuitable for directly resolving million-cycle rare-error lifetimes with a small sample budget.

## Priority 1 — Validate the physical construction and constants

1. **Check the full reversible map on small registers.** Enumerate every computational-basis input for `r = 1` and `r = 3` and verify that Eq. (27) is a permutation. Separately propagate the resulting classical probability distribution through product depolarization. Compare write/hold sequences against Eq. (28), including mixed initial data. This checks the reset accounting and update order, not just the scalar recurrence.
2. **Reproduce the upper-bound examples.** Implement `θ = 2q²/(1+q²)` [Lemma 2], the washout time from Sec. IV E, and the constants in Eqs. (18)–(21). Check `δ⁻¹ = 2^11` for `q = 1/2, k = 1`, the printed approximation at `q = 0.9`, and washout times 42 and 63. Compute large constants in logarithmic form.
3. **Audit theorem dependencies.** Check the hypotheses and normalization in the cited forward and reverse hypercontractive inequalities, Lemma 3, the two branches of the common-norm contraction, and the driven-state limit. Record any gap as an open issue with an exact equation anchor. Mathematical review must use the original cited sources, not only this manuscript's summaries.
4. **Check the finite-window quantifiers.** Verify the suffix indexing in Eqs. (9), (24), and (30); distinguish an arbitrary finite initialization from a driven history and an expectation gap from an individual measurement success probability. Check ceilings, floors, and the sufficiently-large-`k` condition separately.

Acceptance requires a transparent validation record and resolution of any discrepancy, with manuscript claims kept distinct from independently established facts.

## Priority 2 — Extend reproduction to the other noise regimes

| Work item | Source anchor | Validation target |
| --- | --- | --- |
| Anisotropic unital product channels | Sec. VII B, Eqs. (43)–(44) | For explicit Pauli channels, verify the Choi normalization, `q_M = 1 − 2 λ_min(J_M)`, and the largest Bloch singular value `s_M`; reproduce both numerical examples and their differing constants. |
| Cooling constants and pipeline | Theorem 9; Appendix D | Derive `a`, `d`, `p_*`, `s`, and `c`; implement the reversible rotation/XOR map and test conditional-error bounds on small registers. Independently reconstruct the stationary estimate near 1,100 qubits at `q = 0.9, γ = 0.3`, documenting block size and estimator. |
| Pure-dephasing boundary case | Proposition 10(i) | Verify exact preservation of computational-basis write states and explain why the full-rank Choi/depolarizing-core hypothesis fails. |
| Temporally correlated Pauli errors | Proposition 10(ii) | Draw an error once and reuse it, then compare with independent errors redrawn each cycle. Confirm two-cycle revival while matching the one-cycle averaged depolarizing channel. |

Noise ordering must remain explicit: the cooling theorem uses `D_q ◦ AD_γ`. Swapping layers or adding gate-level noise defines a different experiment and needs a fresh analysis.

## Priority 3 — Reproduce the learning statement on bounded examples

Use small tractable reservoirs and known encodings first. For a single-qubit `R_y(u)` encoding, the active coordinates are `1`, `sin(u)`, and `cos(u)` [Sec. VI B].

- Construct recent-input product features with a declared coordinate order and window order. Check them against a direct small-system window computation.
- Fit the **unclipped** squared-loss objective with coefficients constrained to `[-1,1]`, then clip predictions after training, as in Eqs. (39)–(40). Track the empirical objective tolerance `ν`.
- Generate independently sampled histories and bounded **task labels**, state the task-generating rule, and evaluate on an independent test set. If a separate diagnostic uses reservoir-generated labels, identify it as output approximation rather than the task-label learning experiment.
- Report feature count, wall time, memory use, window approximation error, empirical objective gap, and test risk separately. Compare with the one-scalar majority baseline to avoid equating large window requirements with general classical hardness.
- Evaluate the numerical size of Eq. (41) and disclose when its worst-case guarantee is vacuous. A successful small experiment is not empirical proof of the full uniform theorem.

Dependent time-series windows and closed-loop forecasting are separate proposed studies; their statistical guarantees cannot be borrowed from the iid theorem without further work.

## Proposed extensions — Not manuscript results

1. **Tighter constants:** reduce the gap between the constructive lifetime and the universal upper bound, especially for weak or anisotropic noise. Compare candidate improvements analytically before treating numerical fits as asymptotic evidence.
2. **Physical circuit restrictions:** compile majority refresh into a declared gate set and geometry, count depth and resets, and introduce noise after elementary gates. Determine which memory claims survive this changed model.
3. **Practical learning:** investigate sparse or structured input-product models and compare their finite-data behavior with the full worst-case library. Any improvement is task dependent unless supported by a separate theorem.
4. **Resource tradeoffs:** map finite-size lifetime versus reset rate, damping, register size, and observable choice. Keep the cost of measurement repetitions separate from the expectation-value memory definition.

## Publication readiness

Before describing the repository as a complete reproducibility package, obtain or clearly mark the missing supplemental material, verify bibliographic metadata against primary sources, state code and manuscript reuse permissions separately, and archive the exact manuscript/code version used for each reported result. Release notes should list reproduced claims, unresolved discrepancies, and experiments still proposed.
