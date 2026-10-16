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

The local PRA submission package includes this revision's simulator, saved data and figure sources. APS login is authenticated with the campus account, and an unsubmitted portal draft exists: `es2026oct16_686` (PRA Regular Article, Quantum Information Science). No files have been uploaded or author fields filled. Browser upload permission was explicitly declined; the upload must not be retried. The current portal step requires the manuscript PDF and figure count (eight). No manuscript has been submitted, and no declarations, fees or copyright terms have been accepted. ORCID authentication and final author declarations remain pending. The existing disclosure of AI assistance and claimed human verification must be confirmed by the authors before submission.

## Author metadata correction

The current front matter adds ORCID identifiers for Markus Baumann (`0009-0007-3575-1006`), Jonas Stein (`0000-0001-5727-9151`), and Claudia Linnhoff-Popien (`0000-0001-6284-9286`). All three have both affiliations: the Quantum Applications and Research Laboratory (QAR-Lab) and the Chair of Mobile and Distributed Systems, Department of Computer Science, Ludwig-Maximilians-Universität München, Oettingenstraße 67, 80538 München, Germany. Prior manuscripts and institutional sources are documented in [author_metadata_sources.txt](../paper/submission/2026-10-16-v4/author_metadata_sources.txt).

The approved abstract and the entire source after `\begin{abstract}` remain byte-identical to commit `701742a`. The rebuilt PDF remains 17 pages; all three ORCID links and both affiliation markers were inspected. Its SHA256 is `e0d8176e9f3ba77a8ab3c5c7a0e4c4bde36b492422a2703dc1999a471b9bdff6`. ORCID identifiers in a manuscript do not authenticate them through APS. The portal profile currently displays “Dr. Markus” and an unaffiliated state. Verify/correct the displayed name to Markus Baumann and the affiliations; the academic title is not verified. The manuscript uses Markus Baumann without an academic title.
