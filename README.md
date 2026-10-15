# Fresh Qubits Set the Memory

Scientific project for **“Fresh qubits set the memory: A sharp reset–memory law and classical learning of noisy quantum reservoirs”** by Markus Baumann (LMU Munich).

The supplied manuscript studies how the number of freshly prepared qubits per cycle limits the memory of a noisy quantum reservoir. This repository preserves the manuscript, records a research and validation plan, and provides an independent numerical reproduction of its majority-refresh example.

**Status:** initial research workspace, created 15 October 2026. The supplied PDF is the source of the theoretical claims. The numerical starter reproduces Table I; it does not verify the proofs or implement the complete quantum reservoir or learning algorithm. Publication and peer-review status are not established by the supplied material.

## Scientific scope

Each cycle overwrites a register of at most $k$ qubits, applies a fixed unitary, and independently depolarizes every qubit with fixed $0<q<1$. For the driven state after the initial transient, the manuscript claims a worst-case finite-window memory of $\exp[\Theta_q(k)]$ at fixed accuracy, independent of the total register size $n$ (Theorem 1).

The matching construction uses an odd number $r$ of repetition copies, $k=r+2$ fresh qubits, and $n=2r+2$ total qubits. With $p=(1-q)/2$:

$$
p_r=\sum_{j=(r+1)/2}^{r}\binom{r}{j}p^j(1-p)^{r-j},\qquad
\lambda_r=1-2p_r,\qquad f_b(t)=(-1)^b q\lambda_r^t.
$$

Table I reports the largest integer $T_r$ with $\lambda_r^{T_r}\geq 1/2$. At $q=0.9$, $r=15$ ($k=17$) gives **1,894,286 hold cycles**. These are ideal-unitary/noise cycles, not elementary gate cycles.

The exponential upper and lower bounds match in order, not in constants. A long finite-window requirement does not establish classical computational hardness: the example above has a one-scalar recurrence. Learning guarantees have additional assumptions, including independent training examples and classically evaluable input-encoding coordinates. See the [paper summary](docs/paper-summary.md) for these distinctions.

## Quick start

Python 3.11 or newer is required. The calculation and tests use only the Python standard library.

```bash
git clone https://github.com/eybmits/fresh-qubits-memory.git
cd fresh-qubits-memory
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -e .
python -m unittest discover -s tests -v
python scripts/reproduce_table1.py --output-dir results/table1
```

The script writes CSV values and JSON metadata. The committed [baseline output](results/table1/) is generated from the equations, with the lifetime and conservative-guarantee rows checked against Table I. No stochastic sampling is used. Package installation uses setuptools as its build tool; runtime calculations need no third-party packages.

Optional flags are `--q`, `--copies`, and `--precision`; see `--help`. The implementation accepts odd `r` from 1 to 255 and finite-decimal `q` in `(0,1)` with at most 100 decimal places. Output precision is 30–512 digits; adaptive working precision is capped at 4096 digits and extreme cases that exceed the bound are rejected. See the [validation record](docs/validation.md) for the tested scope and the manuscript's display-rounding convention.

## Repository map

| Path | Purpose |
| --- | --- |
| [paper/](paper/) | Original PDF, provenance and draft citation |
| [docs/paper-summary.md](docs/paper-summary.md) | Source-grounded model, claims and limitations |
| [docs/research-plan.md](docs/research-plan.md) | Prioritized scientific work and acceptance criteria |
| [src/fresh_qubits_memory/](src/fresh_qubits_memory/) | Majority-error and readable-lifetime calculations |
| [scripts/reproduce_table1.py](scripts/reproduce_table1.py) | Reproducible Table I entry point |
| [tests/](tests/) | Reference values and numerical boundary checks |
| [experiments/](experiments/) | Protocols for future experiments |
| [data/](data/) | Data provenance and storage conventions |
| [results/](results/) | Small reproducible outputs and interpretation |

Start with the [research plan](docs/research-plan.md). The first completed check is numerical reproduction of Table I; proof review, small-system circuit validation, cooling-noise experiments and the classical learner remain research tasks. The original LaTeX source and the supplement's scripts were not supplied.

## Citation and reuse

[CITATION.cff](CITATION.cff) describes this research repository; [paper/manuscript.bib](paper/manuscript.bib) records the supplied manuscript without inventing a DOI or journal acceptance. The PDF is preserved byte-for-byte, with its checksum in [paper/provenance.json](paper/provenance.json).

No open-source license has been selected. Public release and licensing are separate project decisions.
