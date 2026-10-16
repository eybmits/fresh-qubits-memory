# Manuscript revision 4: 16 October 2026

Current manuscript: **The Memory Limits of Noisy Quantum Reservoirs**, by Markus Baumann, Jonas Stein, and Claudia Linnhoff-Popien.

[PDF](../paper/memory_limits_2026-10-16-v4.pdf) | [LaTeX](../paper/source/memory_limits.tex) | [Input/output provenance](../paper/versions/2026-10-16-v4/provenance.json) | [PRA template audit](pra-template-check-2026-10-16.md)

## Source and changes

This version imports `memory_limits (5).pdf` and `memory_limits_source (1).zip`, received on 16 October 2026. Both inputs are archived byte-for-byte. The supplied PDF has 17 pages, eight figures, five tables and a single-author byline. The approved three-author order is restored; the supplied title and the latest approved abstract are retained exactly. The preceding 12-page PDF and its source snapshot remain in the version history.

The new revision adds a numerical section and Appendix F, Ising and Haar reservoir simulations, saved JSON datasets, eight redesigned figure PDFs, and expanded figure-generation code. These are supplied research results, distinct from the independent validation under `results/empirical-2026-10-16/`. That earlier report is preserved with its original scope and source hashes.

The template is REVTeX 4.2f with `aps,pra,reprint,superscriptaddress,floatfix`. Switching `twocolumn` to `reprint` expresses the standard journal layout; the former option was supported too. Three table preambles were repaired for the installed REVTeX/array incompatibility without changing cell contents. PDF metadata and the contact-author prefix were added; the date is fixed at 16 October 2026. The assistance acknowledgment names Markus explicitly, preserving the existing attribution without assigning the asserted checks to coauthors.

A normalization comparison confirms the mathematical body is identical to the new supplied source apart from table formatting and that attribution. All 36 other supplied files, including the figures, bibliography and simulation data/code, are byte-identical. The source README adds explicit figure assembly/copy instructions.

## Validation

- Rebuild: 17 US Letter pages with resolved citations and cross-references, no overfull boxes, embedded Type 1 fonts. All 17 pages rendered and visually reviewed; all eight figures and five tables are present.
- BibTeX regeneration with `apsrev4-2` matches the supplied BBL exactly. The publisher-assigned Supplemental Material URL placeholder is retained as expected by APS.
- Nonfatal warnings remain: nameref label compatibility, underfull paragraphs, REVTeX deferred-float processing at the bibliography, and BibTeX style control / missing year in the Supplemental Material entry. All deferred figures and tables appear in the PDF.
- In an isolated source copy, `sim/test_sim.py`, `sim/check_washout.py`, `sim/exact_numbers.py`, and `sim/rep_curve.py` exit successfully. Repetition readout error is at most 2.45e-15. The largest checked post-washout trace distance is 5.805e-7.
- Regenerated numerical constants have identical integer values and a maximum floating-point difference of 5.72e-14; all agree at absolute/relative tolerance 1e-12. The 700 repetition-curve points reproduce exactly; the sampled full-state depth is 316, compared with the readout value 308.0763.
- The large Ising/Haar campaigns were not rerun. Their supplied main/noise/evolution-time/weak-noise datasets contain 180/54/30/18 realizations, respectively.

## Interpretation and remaining author review

The empirical memory depths maximize over five sampled input continuations per realization. As Appendix F states, they are lower witnesses for the worst-case memory depth, not a certified supremum over all histories. The main-text language about exact memory depth and independence from size is stronger than these finite samples establish. This update preserves the supplied scientific prose and records the distinction here and in the submission cover letter.

The streaming-input simulations do not train a linear readout or evaluate forecasting accuracy. The Mackey–Glass series in Fig. 1a is illustrative. Build checks, finite simulation agreement and the correct journal template do not establish theorem validity, novelty or journal acceptance.

The local PRA submission package includes this revision's simulator, saved data and figure sources. No manuscript has been submitted; APS account/login, corresponding-author ORCID authentication and final author declarations remain separate steps. The existing disclosure of AI assistance and claimed human verification must be confirmed by the authors before submission.
