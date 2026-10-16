# Repair added to Ising and Haar dynamics

Protocol fixed on 16 October 2026 before the main runs. The manuscript and
its figures remain untouched. Exploratory checks guide feasible architecture
choices; the final run uses eight predetermined unitary seeds per model and
retains all realizations and controls, including negative results.

## Fixed global reservoir

Use the supplied all-to-all transverse-field Ising builder (J=h=1, tau=10)
and Haar builder, each on the same five memory qubits. Draw one unitary per
model/seed and reuse it across r=1,3,5, repair variants and passive controls.
Seed = 2026101602 + 1000 * model_index + replicate, replicate=0,...,7.
Fix q=0.9 and epsilon=0.01. The total physical size is n=12: five core qubits,
r fresh repair ancillas, two write/input controls, and 5-r padding qubits.
Thus the reset budget is k=r+2=3,5,7.

R_r measures the majority of the first r computational-basis memory bits,
copies it into r fresh zero ancillas, and swaps them with the old bits. This
has a reversible fixed-unitary implementation; tracing old bits gives the
reduced channel. The other 5-r core bits are retained with their conditional
correlations. They are not replaced by independent marginals. Two fixed
control sectors select write or hold. All physical qubits undergo independent
depolarization after the ideal composite unitary. Noise on discarded wires
vanishes under their next partial trace, so evolving only the 32x32 core
density matrix is exact for this metric.

Test two hold cycles:

- Native: rho -> D[U R_r(rho) Udag]. The original global Ising/Haar unitary
  continues to act every cycle. The paired passive control omits R_r.
- Basis-aware: rho -> D[U R_r(Udag rho U) Udag]. This explicitly adds a
  known-U decoder and encoder. Its passive control is D[rho], because Udag/U
  cancel without repair. It is an encoded-memory architecture, not unchanged
  native reservoir evolution. The noisy interval remains between encoding
  and the following decoding; the physical noise is not undone.

For each channel, converge a common hold state from I/32 until successive
states differ by less than 1e-12 in Frobenius norm (maximum 10,000 steps), and
record convergence diagnostics. Branch by writing r copies of b=0 or b=1
while retaining the other core qubits, then apply U and noise. Evolve the
state difference under identical hold inputs. Record core trace distance
and a fixed linear observable: the sign of the initial core difference.
This observable is selected separately for each model/seed/k/variant/control
at the write pulse, then held fixed for the entire trajectory. It generally
acts jointly on all five core qubits, rather than being a local Z readout.
It has operator norm at most one. Define witness depth as 1 + largest delay above epsilon.
Continue until core trace distance is below epsilon, which also bounds all
later fixed-readout contrasts. No extrapolation is used.

This is a write/hold memory experiment. Core trace distance is a lower witness
for full-system memory, not a supremum over histories or a forecasting score.
Finite common-state convergence is a numerical check, not a proof of washout.
The two metrics are reported separately. Extra decoder/repair gates are
included in the architecture description. Elementary-gate errors and
implementation costs are not modelled; depolarization occurs after each
ideal composite cycle.

## Modular encoded alternative

Also test a distinct architecture: r=1,3,5 two-qubit modules, each using the
same native Ising/Haar U_2, with a joint majority recovery of the decoded
logical bits. Refresh complete modules and reencode. This uses k=2r+2=4,8,12
and fixed total n=22, with decoupled noisy padding. The quantum state carrying
the bit passes through U_2, physical noise, and U_2dag at every cycle. These
are modular Ising/Haar encoders; their tensor product is not a global
Haar-random unitary on the full core. The decoder is known and engineered.

The exact conditional product-state closure gives a two-state transition
matrix, including asymmetric errors; propagate it to actual threshold
crossings. Validate this closure against independently assembled dense
reduced-memory density matrices for r=1,3. Use a fixed linear encoded
two-qubit readout on one module. The passive control receives the same
initial encoded state and physical noise, with no recovery. Report resource
differences and do not equate its readout metric with global core trace
distance. This construction can test a positive mechanism even if repair
of the globally scrambled Haar register fails.

Module seeds are 621100 + replicate for Ising and 621200 + replicate for Haar,
replicate=0,...,7, fixed before the exploratory modular run. All eight seeds
are retained in the final run. The entire module memory is overwritten at
write, making the written state independent of the initial state. Stop both
variants only when the one-module trace distance is at most epsilon; this
bounds all later values of the chosen module readout even if it revives.

## Reproduction

Install NumPy, SciPy and Matplotlib. Scripts use float64/complex128 and save
seeds, source hashes, environment, per-run results and threshold curves.
Use one BLAS thread. Final commands and outcomes are in the results report.
The original paper and previous experimental evidence are preserved.
