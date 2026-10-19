# Public reproduction tools — 19 October 2026

This update improves access and reproduction of the submitted manuscript. It changes repository documentation, dependencies, execution wrappers, tests, and CI, not scientific results or manuscript content.

## Checks performed

- A fresh Python 3.14.3 virtual environment installed `.[paper]`; `pip check` reported no broken requirements. It resolved NumPy 2.5.4, SciPy 1.18.1, Matplotlib 3.11.2, and mpmath 1.4.1.
- All **36 unit tests passed**, including process-failure, partial-result, stale-output, and figure-input checks.
- The current-paper `check` command completed all four diagnostic steps.
- A fresh smoke campaign reran six seeded Ising and six seeded Haar realizations at `n=3`, `k=1`, `q=0.9`, `epsilon=0.01`. Memory depths, partition depths, and washout-step counts matched the supplied reference exactly. Maximum absolute curve differences were below `5.5e-14` (Ising) and `1.1e-14` (Haar), within the `1e-10` comparison tolerance.
- A complete figure and manuscript build completed all 12 commands, regenerating all 11 figures. The LaTeX recorder confirmed that the rebuilt manuscript loaded the new copies. This build used NumPy 2.3.3, SciPy 1.16.2, and Matplotlib 3.11.2.
- The rebuilt PDF has 25 pages. Extracted text matches the submitted PDF on every page. At 90 dpi, 24 pages render identically; the remaining page differs in 54 antialiasing pixels in figure text, checked visually.
- SHA256 comparisons confirmed that all **540 tracked scientific/archive files** in the pre-update baseline were unchanged, including manuscript sources, PDFs, datasets, and ZIP archives.
- Local documentation links resolve; an independent code review found no blocking issue in the new wrappers.

The new build explicitly excludes Matplotlib 3.11.0, whose [confirmed TeX/PDF bug](https://github.com/matplotlib/matplotlib/issues/31925) dropped a minus sign in Figure 3. Rebuilding with 3.11.2 restored that sign; the rebuilt Figure 3 is pixel-identical to the supplied figure at 140 dpi. The supplied figure was never changed.

## Scope

The expensive full simulation campaign was **not** rerun in this update. Its supplied output files satisfy the new structural completeness contract. Small simulations and diagnostics establish bounded numerical reproduction, not proof of the universal theorem, novelty, or journal acceptance. Submitted files remain the reference artifacts.

The [reproduction guide](reproduction.md) gives the commands and locations of the logs and manifests created on each run. Generated local environments and bulk outputs are excluded from Git. GitHub CI now additionally runs the current-paper diagnostics, small campaign, and full figure/manuscript build.

## Tool fingerprints

- `scripts/run_prl_campaign.py`: `4cf7c2c2311bd392939080bfd6367b69477c2c11cd5c81d93804c3d902b7d28e`
- `scripts/reproduce_paper.py`: `72b4f8b6672121a1fb9e981dfe7a2048c1786cdff74d4987b57c47f10c977770`
