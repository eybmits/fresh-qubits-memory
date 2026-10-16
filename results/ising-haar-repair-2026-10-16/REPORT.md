# Adding repair to Ising and Haar dynamics

16 October 2026. Simulation-only experiment; no manuscript changes.

**Result:** direct majority repair improves the measured memory with increasing
reset width in the tested global Ising cores. The same intervention fails in
the tested global Haar cores. A separate modular architecture with known
encoders/decoders and majority recovery improves with reset width for both
models. The modular architecture is not a global Haar-random reservoir.

All figures contain new simulations. Every predetermined realization and all
controls are retained. No curves were selected for a favorable trend.

## 1. Repair in a fixed global five-qubit core

At fixed total **n=12**, q=0.9 and epsilon=0.01, reuse the same five-qubit
unitary across k=3,5,7. The first r=k-2 core qubits receive reversible majority
refresh using r fresh ancillas; two extra fresh controls choose write/hold.
The remaining core qubits retain their conditional correlations. Padding is
decoupled and noisy. The full physical cycle admits a fixed unitary; its
32x32 reduced core channel is simulated exactly.

For each channel a common hold state is numerically converged before the
write pulse. The two histories write opposite bits once and then receive
identical hold inputs. Core trace distance is a distinguishability witness,
not a maximum over all histories. Values below are **medians over eight
realizations**, so half-integer medians do not denote fractional cycles.

| Core trace-distance depth | k=3 | k=5 | k=7 |
|---|---:|---:|---:|
| Ising, direct repair | 24 | 38.5 | 100.5 |
| Ising, native passive control | 31 | 41 | 45 |
| Haar, direct repair | 6 | 4 | 2 |
| Haar, native passive control | 11 | 12 | 13 |
| Ising, decoder + repair + encoder | 29 | 55 | 127 |
| Ising, decoded passive control | 33 | 43 | 48 |
| Haar, decoder + repair + encoder | 13 | 12 | 12 |
| Haar, decoded passive control | 21 | 28 | 35 |

Direct repaired Ising increases at both k increments in all eight realizations.
At k=3 its median is worse than the passive control; at k=7 it is substantially
better. Direct repaired Haar decreases at both increments in all eight.
Adding a decoder to a global Haar core also fails to produce an overall gain
with k in this experiment. These finite tests do not establish a universal
impossibility theorem for repaired Haar systems.

The decoded cycle is Udag -> recovery -> U -> noise. With recovery removed,
the Udag/U pair cancels, so its passive control is noise-only storage of an
encoded state. The direct cycle instead keeps native U evolution every step.
Passive and repaired runs share physical parameters and the write rule; their
converged pre-write states can differ because their hold channels differ.

A second metric uses the sign of the initial core state difference as a
fixed linear observable. It is chosen per run at write, then held fixed; it
generally acts on all five core qubits. Native repaired Ising's median depths
are **19,38,100.5**, while native repaired Haar's are **2,2,2**. These results
are also saved and plotted separately. They are not standard local-Z readouts.

## 2. Modular encoded repair

At fixed total **n=22**, each redundant module contains two qubits and the
same Ising/Haar U2. The bit is stored in U2|b,0>, experiences independent
physical noise, and is decoded before majority recovery. Each recovery
refreshes complete modules, reencodes, and subjects all physical qubits to
noise again. The module carrying information genuinely participates in this
noisy Ising/Haar encoding interval; it is not a separate untouched register.

r=1,3,5 modules require **k=2r+2=4,8,12** fresh qubits including two controls.
Thus the active count is 4r+2 and noisy padding keeps total n=22. The U2 for
each realization is unchanged across r. The complete composite unitary changes
with the recovery architecture, while remaining fixed within each trajectory.
The readout is the fixed two-qubit observable U2(Z tensor I)U2dag on the first
module. It is a linear observable, generally not one physical qubit's Z.

| Fixed two-qubit readout depth | k=4 | k=8 | k=12 |
|---|---:|---:|---:|
| Ising modules, repair | 36.5 | 222 | 1195 |
| Ising modules, passive | 41 | 41 | 41 |
| Haar modules, repair | 27 | 126 | 511.5 |
| Haar modules, passive | 34.5 | 34.5 | 34.5 |

Every one of the eight fixed realizations per model improves at both k
increments. The shaded figures show the min-max range, not confidence bands.
Single-module repair is often worse than passive storage; these outcomes are
retained. The redundant recovery is responsible for the large gains.

The exact channel closes on two conditional product states. We propagate
their signed weights cycle by cycle with the full, potentially asymmetric
2x2 logical transition matrix. No symmetric-error assumption is imposed on
Haar. All reported thresholds are actually crossed; none is extrapolated.
The closure is independently checked against dense reduced-memory evolution
for one and three modules. This is an engineered modular memory, not an
unchanged global Haar reservoir or evidence for a universal improvement law.

## Validation and scope

- 192 global runs and 96 modular runs; seeds and all curves are saved.
- 16 independent full-ancilla physical dilation cases validate the global
  reduced channel, including generic correlated states and differences.
- 32 dense modular channel comparisons: maximum matrix-entry discrepancy
  about 2.22e-15.
- Identity encoding recovers the known 43,309,1941 repetition depths.
- Noiseless recovery, physical-noise implementation, conditional coherences,
  exact threshold equality and original two-qubit builder agreement checked.
- Both simulations terminate using contractive trace-distance bounds, allowing
  the chosen readout to revive before its final crossing.
- 22 repository tests pass. Maximum global common-state residual is below
  1e-12; convergence is a numerical check, not a proof of washout.

This is a write/hold memory study, not a trained forecasting benchmark.
Elementary-gate errors, gate depth, hardware and implementation cost are not
simulated: depolarization follows each ideal composite cycle. Three redundancy
levels and eight realizations do not prove asymptotic exponential scaling or
quantum advantage. The global and modular figures use different metrics and
resource budgets; their values should not be directly compared as a fair
performance contest.

## Reproduce

Install NumPy, SciPy and Matplotlib, then run from the repository or ZIP root:

```bash
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python3 scripts/simulate_global_repair.py --output-dir new-results/global
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python3 scripts/simulate_modular_repair.py --output-dir new-results/modular
python3 scripts/plot_ising_haar_repair.py --input-dir new-results --output-dir new-results
PYTHONPATH=src OPENBLAS_NUM_THREADS=1 python3 -m unittest discover -s tests -v
```

The ZIP contains the two new test modules (10 tests); the full repository
suite contains 22. Frozen reference results are in `reference-results/` in
the ZIP. Run into a different output directory to preserve the reference.
Each campaign saves source hashes, unitary seeds, commands, versions and
output hashes. `summary.json` contains every median, range and underlying
eight values. `manifest.json` hashes the sources and archived artifacts.
The original manuscript tree remains byte-for-byte unchanged.
