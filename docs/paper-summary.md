# Manuscript summary

**Historical scope:** this page describes the immutable 15 October 2026 manuscript. For the current 18 October PRL revision 5, see [the current version note](manuscript-2026-10-18-prl-v5.md); its state-based memory definition and supplied scientific changes are documented in the [17 October import record](manuscript-2026-10-17-prl.md). Equation/table anchors and the classical-learning result below belong to the earlier version.

## Source and evidence status

**Title:** *Fresh qubits set the memory: A sharp reset–memory law and classical learning of noisy quantum reservoirs*

**Author:** Markus Baumann

**Affiliation printed in the manuscript:** Ludwig-Maximilians-Universität München

**Supplied file:** `fresh_qubits_pra (1).pdf` (12 pages).

The source does not establish a publication date, accepted journal version, DOI, or public preprint identifier. The filename does not establish publication in *Physical Review A*. Reference [6] contains a publisher-URL placeholder for a numerical supplement; that script was not part of the supplied PDF.

The statements below are **claims and derivations reported by the manuscript**. Numerical checks in this repository can test particular formulas and examples; they do not independently prove the theorems or establish novelty. Proposed research is identified separately in [the research plan](research-plan.md).

## Model and memory definition

Each cycle resets a register of at most `k` qubits to a known input state, applies the same arbitrary `n`-qubit unitary, and then independently depolarizes every qubit [Sec. III, Eqs. (5)–(7)]:

$$
\rho_t=\mathcal D_q^{\otimes n}\!\left(U[\sigma_A(u_t)\otimes\operatorname{Tr}_A\rho_{t-1}]U^\dagger\right),
\qquad 0<q<1.
$$

Here `q` is the retained Bloch-vector fraction, not the probability of a classical bit flip. On computational-basis states the flip probability is `p = (1 − q)/2`. The readout is an expectation `f_t = Tr(O ρ_t)` with `||O||∞ ≤ 1`; a persistent noiseless external record is outside the model.

The general upper-bound assumption is a CPTP update `E_u` with `E_u(I) ≤ J I` uniformly in the input [Eq. (8)]. Resetting `k` qubits gives `J ≤ 2^k`. This is a per-cycle fresh-state budget.

For the unique driven state of a left-infinite input history, `W_f(ε)` is the smallest suffix length for which **some unrestricted function** of the recent inputs approximates the output uniformly within `ε` [Eq. (9)]. `W_{q,k}` takes the worst case over register size, encodings, unitary, and bounded readout. It does not measure the computational complexity of an arbitrary classical predictor.

## Principal claims and anchors

| Claim in the manuscript | Precise scope | Source |
| --- | --- | --- |
| Driven memory scales as `exp[Θ_q(k)]`. | Fixed `0 < q < 1`, fixed admissible accuracy, sufficiently large `k`; uniform upper bound independent of `n`. The two exponential constants differ. | Theorem 1, Eqs. (10)–(11) |
| A common norm contracts every allowed update. | Traceless Hermitian differences; the norm combines normalized Schatten 1- and 2-norms, with constants depending on `q` and `J`. | Theorem 4, Eqs. (18)–(21) |
| Arbitrary initial states wash out before the dimension-independent driven bound applies. | An additional `O_q(log n)` transient is sufficient and necessary in order; no dimension-independent bound from time zero is claimed. | Sec. IV E, Eqs. (22)–(25); Appendix B |
| A reversible majority-refresh reservoir attains the exponential order. | Odd `r` copies, `k = r + 2` fresh qubits per cycle, `n = 2r + 2`, one-qubit `Z` readout. The write erases dependence on the old data state. | Sec. V, Eqs. (26)–(31) |
| Maintaining a readout gap at least `q` for `T` cycles costs `Θ_q(log T)` fresh qubits per cycle. | Optimization over permitted reservoirs in driven operation; fixed noise strength. | Corollary 5 |
| A known input-product library supports classical learning from task labels. | Known classically evaluable encoding coordinates, bounded labels, iid examples, box-constrained least squares. | Sec. VI, Eqs. (34)–(41); Theorem 6; Appendix C |
| Unital noise around a depolarizing core preserves the upper law. | A fixed-strength independent depolarizing layer acts each cycle; surrounding maps can be spatially correlated or time varying. The general nonunital formulation has input-independence conditions. | Theorem 7, Eq. (42) |
| Product noise from any nontrivial unital qubit channel with full-rank Choi matrix has the same exponential order in `k`. | The upper constant uses its depolarizing core; the lower constant uses its best-preserved Bloch direction. | Corollary 8, Eqs. (43)–(44) |
| Amplitude damping can supply an extensive fresh-state resource. | Noise `(D_q ◦ AD_γ)^{⊗n}`, fixed `0 < q,γ < 1`: a construction with `k = 2` attains `exp[Ω_{q,γ}(n)]`; the upper bound matches the order in `n`. | Theorem 9, Eqs. (45)–(46); Appendix D |
| A depolarizing single-cycle marginal alone is insufficient. | Pure dephasing preserves a classical bit; fixed temporally correlated Pauli errors can revive it every second cycle. | Proposition 10, Sec. VII D |

Theorem 1 defines

$$
\alpha_q=-\tfrac12\log(1-q^2),\qquad
\beta_q=\frac{q(1+q^2)}{(1-q)(1-q^2)},
$$

and reports

$$
\tfrac14 e^{\alpha_q(k-3)}\log(q/\varepsilon)
\le W_{q,k}(\varepsilon)
\le \left\lceil A_q2^{\beta_q k}\log(2/\varepsilon)\right\rceil,
\qquad 0<\varepsilon<q/2.
$$

`A_q` is explicit in Eq. (21). These constants are loose: the manuscript gives `δ⁻¹ ≈ 2^(217.5 + 85.7 k)` at `q = 0.9` [Sec. IV D]. This is an asymptotic obstruction, not a practical lifetime estimate.

## Numerical reproduction targets

For odd `r`, the majority mechanism has [Eqs. (2)–(4), (28)]

$$
p_r=\Pr[\operatorname{Bin}(r,(1-q)/2)>r/2],\quad
\lambda_r=1-2p_r,\quad
f_b(t)=(-1)^bq\lambda_r^t.
$$

The write is `t = 0`; `t` counts subsequent hold cycles. The Table I lifetime is the largest integer `T` with `λ_r^T ≥ 1/2`, so the gap between the two write histories remains at least `q`. At `q = 0.9`, Table I lists:

| Copies `r` | Fresh qubits `k` | Lifetime `T` (cycles) |
| ---: | ---: | ---: |
| 1 | 3 | 6 |
| 3 | 5 | 47 |
| 5 | 7 | 298 |
| 7 | 9 | 1,790 |
| 9 | 11 | 10,431 |
| 11 | 13 | 59,739 |
| 13 | 15 | 337,940 |
| 15 | 17 | 1,894,286 |

The analytical guarantee `floor(exp(α_q r)/4)` is weaker than this exact recurrence lifetime. Sec. IV E also gives initialization times 42 and 63 cycles for `n = 100` and `n = 1000` at `q = 0.9`. The cooling estimate near 1,100 qubits in Sec. VII C needs a separate derivation and reproduction; it is not a Table I result.

## Interpretation limits

- The lower construction is reversible classical logic embedded in a quantum unitary. One scalar tracks its expected output exactly [Sec. V, after Corollary 5]. Exponentially long memory does not imply classical computational hardness.
- The unitary can be nonlocal and arbitrarily deep, with noise applied only after the complete update. No gate-level noise threshold or hardware implementation is established [Sec. VIII B].
- The input-product library has `K = (4^k)^L` features before exploiting redundant encoding coordinates [Eq. (38)]. Independence from `n` at fixed `q,k,ε` does not imply a small or practical feature library.
- Theorem 6 bounds risk relative to the reservoir predictor, using the original task labels. It does not simulate the quantum state, sample its full measurement distribution, or recover a circuit's behavior without training data [Secs. VI, VIII B].
- Generalization for overlapping dependent windows, closed-loop forecasting, and arbitrarily drifting noise is not supplied by the iid learning statement. The stated noise extension for learning requires fixed unital maps or randomness independent across cycles and from the inputs [Sec. VII A].
- Fresh-state accounting is an upper-bound resource measure, not a guarantee that every channel with a large budget has long memory. A complete replacement channel can erase everything [Sec. VIII B].
- Publication status and the accuracy of the bibliography require external verification before public scholarly release. The PDF's acknowledgments report language-model assistance; this project does not treat that disclosure as proof verification.
