# Reset-width audit, 16 October 2026

## Question and fixed protocol

The decreasing Ising/Haar curves in the supplied plot could reflect a channel
implementation error, different random realizations across reset widths, or a
real architectural tradeoff: resetting additional input qubits also discards
their old information. The theorem concerns the best attainable architecture
over size, unitary and encoding. It does not predict increasing memory for every
fixed unitary when its reset register is enlarged.

This protocol is written before the diagnostic is run. No old result is replaced
and no parameter is selected to obtain a positive trend.

1. Independently verify explicit-index partial traces and product Pauli-mixture
   noise against the supplied simulator for `n=1,2,3,4`, every `k=1,...,n`, and
   `q=0.1,0.9,1`. Check complete one-step channels on random states and traceless
   differences. Check the exact boundary `k=n`: a common next input erases every
   difference, so the witness depth cannot exceed one.
2. Run paired Ising and Haar controls at `n=4,6`, every `k=1,...,n`, four unitary
   realizations each, `q=0.9`, `epsilon=0.01`, 60 washout steps and at most 80
   common future steps. For each fixed unitary reuse precisely the same input
   sequences across all `k`: two uniform-random continuations and constants
   `0,0.5,1`. Use the maximum of these five sampled witness depths, as in the
   supplied campaign. `D(l)` is the full density-matrix trace distance after an
   input difference `(0,1)` followed by `l` common inputs; witness depth is
   `1 + max{l: D(l)>epsilon}`. All randomness uses recorded NumPy seeds. This
   finite sample cannot certify a supremum over all input histories.
3. Hold total size at `n=12` and explicitly propagate the complete diagonal
   channel for majority-refresh constructions with `r=1,3,5`, hence
   `k=3,5,7`. Spectator qubits are maximally mixed and undergo the same noise.
   Use the reversible map on `(ancilla,control,bit,memory,spectators)`, reset,
   permutation, and independent physical bit flips `p=(1-q)/2`, without using
   the analytical recurrence to update the state. Write once then hold with
   blank inputs. Record both trace distance and the single-memory-qubit readout,
   propagate until both fall below `epsilon`, and compare the latter with
   `q(1-2p_r)^l`. At identical `n,k,r,q`, use a passive-copy control whose
   memory receives no refresh. This isolates active repair from fresh qubits
   alone. These write/hold inputs are witnesses, not a streaming forecasting
   benchmark and not proof of simultaneous storage of many past inputs.

Precision is complex128 for density matrices and float64 for diagonal states.
The fixed seed is `2026101601`; derived seeds are recorded per realization.
Use one BLAS thread for reproducible, modest runtime:

```bash
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python3 scripts/audit_reset_width.py \
  --output-dir results/reset-width-audit-2026-10-16
```

Requirements: NumPy and SciPy, already optional validation dependencies. The
result metadata records versions, command, input/source hashes and runtime.
Interpretation and numerical outcomes are recorded in the generated report.

## Standalone manuscript source package

The identical script can also be placed at `sim/audit_reset_width.py` beside
`qrc_sim.py`, with this protocol at `sim/reset-width-audit-2026-10-16.md`.
From the source package root, run:

```bash
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python3 sim/audit_reset_width.py
```

The default output is then `audit-results/` in the package root. `--output-dir`
can override it. In the research repository the default is the dated `results/`
directory above. Both layouts require and hash the script, simulator and
protocol; missing required provenance is an error. The original campaign script
and historical dataset are also hashed when present, with missing optional
files explicitly recorded in metadata. The diagnostic itself does not depend
on those historical results to evolve or score new states.
