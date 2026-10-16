# Manuscript revision: 16 October 2026

The current draft is **Input Reinitialization Sets the Memory of Noisy Quantum Reservoirs** ([PDF](../paper/memory_limits_2026-10-16.pdf), [source](../paper/source/memory_limits.tex)).

## Changes in this update

The user supplied a new 12-page manuscript and its complete LaTeX package, including bibliography, figure assets and sources, and a numerical supplement. This update imports that revision, replaces its abstract with the user's exact text, changes its title and PDF metadata, and repairs the two table preambles for the installed REVTeX/LaTeX combination. The mathematical prose, equations, bibliography entries, and figure assets from the supplied revision are retained. Original inputs and checksums are archived in [the provenance record](../paper/versions/2026-10-16/provenance.json).

The 15 October source PDF and numerical baseline are preserved. The newly supplied revision already differs substantially from it:

- Memory depth is defined by trace distance between echo states with matching recent input histories, uniformly over the earlier history. This differs from the original readout-based definition.
- The main theorem fixes `0 < q < 1` and `0 < epsilon < q`, with upper bound `ceil(A_q 2^(beta_q k) ln(1/epsilon))` and a matching exponential order in `k`.
- The focus is memory limits, input reinitialization, and noise. The former classical-learning theorem is absent.
- Majority-refresh lifetimes now appear in Figure 4; Table I is notation. The existing `results/table1/` remains a reproduction of the original manuscript's Table I.
- The source now includes prior QRC work on partial measurements and resets, including Hu et al. (2024), as supplied by the user. The bibliography has not been independently audited in this update.

The noise interpretation remains conditional: a fixed independent depolarizing layer is assumed per time step. Additional unital layers preserve the upper bound; they need not preserve the particular construction's achievable lifetime. No gate-level fault-tolerance statement follows from the ideal-unitary/noise-cycle model.

## Validation

- The replacement abstract is checked byte-for-byte against the requested LaTeX text.
- The scientific body is compared with the supplied source, allowing only the two table-formatting changes.
- The current PDF compiles to 12 pages with resolved citations and cross-references; no overfull boxes are reported. Nonfatal REVTeX/nameref and paragraph-spacing warnings remain. BibTeX reports the inherited missing year for the Supplemental Material placeholder and a style-control warning.
- All 12 pages are rendered and inspected, with detailed inspection of the first page and both tables.
- `PYTHONPATH=src python3 -m unittest discover -s tests -v`: all six existing tests pass.
- The supplied supplement runs with `mpmath==1.3.0`; its eight majority lifetimes match the independent committed baseline. Its other reported constants are recorded as supplied calculations, not as independently certified results.

These are source, build, layout, and numerical checks. They do not constitute an independent proof review or novelty audit.
