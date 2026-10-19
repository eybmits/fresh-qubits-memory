# Reproducing the current paper

This guide targets **The Fundamental Memory Ceiling of Noisy Quantum Reservoirs**, submitted to PRL on 19 October 2026. Start from the repository root. The submitted manuscript and archived packages are preserved; reproduction commands work in separate output directories.

## Installation

Use Python 3.11 or newer:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -e ".[paper]"
```

The `paper` extra installs NumPy, SciPy, Matplotlib, and mpmath. Matplotlib 3.11.0 is excluded because of its [confirmed TeX/PDF rendering bug](https://github.com/matplotlib/matplotlib/issues/31925), which can drop minus signs. LaTeX is only required to regenerate figures or build the paper. The historical validation-report tools have separate dependencies in `.[validation]`.

## Check numbers and simulator behavior

```bash
python scripts/reproduce_paper.py check --output-dir results/local/paper-check
```

This runs the current numerical/proof diagnostics, small simulator checks, and quoted-number extraction in an isolated source copy. Inspect `results/local/paper-check/manifest.json` and the command logs. Quoted-number extraction reads the supplied datasets; it does not rerun their campaign.

For a small actual simulation:

```bash
python scripts/run_prl_campaign.py --smoke --output-dir results/local/paper-smoke
```

The smoke run uses the original seeded Ising and Haar configurations at `n=3`, `k=1`, `q=0.9`, with six realizations each. It writes `results_main_ising.json`, `results_main_haar.json`, their merged `results_main.json`, and `run_manifest.json` with logs and provenance. A successful smoke run establishes this bounded reproduction, not completion of the full campaign or proof of the universal bound.

## Figures and manuscript

Install a TeX distribution providing `latex`, `pdflatex`, and `bibtex`, with REVTeX 4.2, standalone, TikZ/PGF, pgf-blur, Latin Modern, Helvetica (`helvet`), and cm-super. Matplotlib's TeX rendering also requires the appropriate font and rendering tools from that distribution. The build command reports missing commands or failed steps in its logs.

```bash
python scripts/reproduce_paper.py figures --output-dir results/local/paper-figures
python scripts/reproduce_paper.py build --output-dir results/local/paper-build
```

- `figures` regenerates four main figures and seven supplemental figures from the supplied data.
- `build` regenerates all eleven figures, copies them into the staged manuscript directory, and compiles the paper there.
- Figure outputs: `<output>/source/figures/fig1.pdf` through `fig4.pdf`, plus `figS1.pdf` through `figS7.pdf`.
- Complete rebuilt paper: `<output>/source/memory_limits_prl.pdf`.
- Provenance and commands: `<output>/manifest.json`.

The manuscript build uses the figures from that run. It must not silently fall back to the original root-level PDFs if figure generation fails. The [submitted PDF](../paper/memory_limits_prl_2026-10-19-concise.pdf) remains the archival reference; rebuilt PDFs may differ in metadata or font rendering across software environments.

The README image is a rendering of the preserved `paper/prl-source/fig4.pdf`, produced with:

```bash
pdftoppm -singlefile -scale-to 1800 -png paper/prl-source/fig4.pdf docs/assets/memory-scaling
```

## Full simulation campaign

```bash
python scripts/run_prl_campaign.py --output-dir results/local/paper-campaign
```

This runs the original main, cold-input, noise, and evolution-time scans and the extended history-pair validation. It retains the simulator, parameters, and random-seed scheme. The full campaign includes substantially larger density matrices and long weak-noise trajectories; runtime depends on hardware and can be much longer than the smoke run.

Use a new output path. The runner creates a fresh workspace without old result JSONs, checks each lane's exit status, validates the required configurations and realization counts, and merges only complete results. On failure, inspect the logs and rerun into a new directory. Partial outputs are not successful results.

The legacy `paper/prl-source/sim/run_all.sh` entry point delegates to the safe repository runner. Frozen source ZIPs retain the scripts that were supplied with those historical packages; use the current repository command above for new runs.

## Tests

```bash
python -m unittest discover -s tests -v
```

The tests cover reference numerical cases and reproduction-tool failure paths. The GitHub workflow also runs the current-paper checks and small campaign. Figure rebuilding and manuscript compilation are verified separately from these numerical tests.

## Historical Table-I reproduction

The dependency-free majority-refresh example was developed for the original 15 October manuscript. Its half-lives are discussed in the current Supplemental Material, but it is not the full current QRC simulation campaign.

```bash
python scripts/reproduce_table1.py --output-dir results/local/table1-replay
```

For the independent historical empirical-validation campaign and its optional dependencies, see the [archived overview](repository-history.md#historical-independent-numerical-validation). Keep generated outputs separate from the committed `results/` baselines.
