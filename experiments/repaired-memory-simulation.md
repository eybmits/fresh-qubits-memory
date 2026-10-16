# Majority-refresh memory simulation

This standalone simulation reproduces the constructive memory mechanism. It
does not modify the paper, its figures, abstract or scientific framing.

```bash
python3 -m pip install numpy matplotlib
OPENBLAS_NUM_THREADS=1 python3 scripts/simulate_repaired_memory.py \
  --output-dir results/local/repaired-memory
```

In the downloadable ZIP, the script is at the top level: run
`python3 simulate_repaired_memory.py --output-dir new-results`.

The experiment fixes `n=12`, depolarization `q=0.9`, and readout threshold
`epsilon=0.01`. It compares the majority constructions with `r=1,3,5` memory
copies and `k=r+2=3,5,7` fresh qubits. The fresh register includes `r` repair
ancillas and two input/control qubits. Unused qubits remain present, decoupled,
maximally mixed and noisy. The unitary is fixed during each run; each `k` has
its corresponding majority circuit.

Two input histories write bit 0 or bit 1 once, then use identical hold inputs.
The script evolves their complete diagonal state difference (4096 entries)
through reset, a bijective majority permutation, and independent depolarizing
noise on every qubit. The plotted contrast is half the difference of the two
single-qubit Z expectations. This is a linear readout. The diagonal restriction
is exact for this construction. The theoretical recurrence is used only to
check the simulation, never to update it or extrapolate the crossing time.

Depth is `1 + max{delay: contrast > epsilon}`, with the write cycle at delay
zero. The observed readout depths are **43, 309, 1941** for `k=3,5,7`.
The complete trace-distance depths are **43, 316, 1986**. Both are in the CSV.
The plotted curves and depths contain only the new repaired-memory runs.

The CSV also retains passive controls with the same size, reset width, copies,
noise, initial state and write operation. During hold, their fixed unitary is
identity, giving readout depths **43, 43, 43**. This comparison checks that the
gain comes from the repair mechanism. No negative result is overwritten.

This is a write/hold memory experiment with ideal unitary cycles and noise
after each cycle. It does not train a forecasting model or simulate errors on
individual elementary gates. Numerical checks cover permutation reversibility,
normalization after writing, trace-distance contraction, readout bounded by
trace distance, integer threshold crossings, and agreement with the independent
formula. Source hashes, library versions, commands and output hashes are saved
in `metadata.json`. NumPy and Matplotlib are the only external requirements;
there is no random sampling and no seed is needed.
