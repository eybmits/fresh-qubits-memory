# Revision 4: supplied-content audit

Audit date: 18 October 2026. Comparison base: `942bbd4031d1f50ef5a5403b897b63372a9b1af8` (revision 3). This is a version and consistency audit, not a new mathematical peer review.

## Input agreement

- The standalone full-source ZIP and full source nested in the submission ZIP contain 53 byte-identical files.
- Standalone TeX and Figure 3 match the archive copies exactly.
- The outer Letter TeX is exactly the combined-source prefix through the bibliography, followed by end-of-document. All six other outer manuscript files (BBL, bibliography, figures 1–4) match the combined source.
- Supplied PDFs have 6 Letter, 16 Supplemental Material, and 22 combined pages. SM text is identical to combined pages 7–22. Letter text from the date onward is identical after whitespace normalization to combined pages 1–6; default extraction moves only the affiliation superscript and a blank line in the byline/reference area.
- All 13 simulation JSON files, all eight simulation Python files, and all displayed equation blocks are unchanged. No numerical campaign rerun was needed for this revision audit.

## Actual changes

- Revised abstract and introduction: removes the leaking-boat analogy and foregrounds entropy removal and the explicit error-correcting construction.
- Figure 1 now draws the overlap of QRC and measurement-free error correction and separates universal upper bound, existential lower bound, and the interval containing the optimal ceiling.
- Figure 3 is redesigned using `fig3.tex` plus `fig3b.py`/`fig3b.pdf`; its old Python-only source is removed. The schematic now depicts sizes 20/200 and refresh widths 2/4.
- Figure S2 relabels q from “Noise strength” to “Noise parameter”, consistent with q being state-retention probability.
- Supplemental prose fixes: singular values rather than eigenvalue magnitudes for general operators; a 2-norm bound rather than an unsupported concentration-ratio statement; scaled projectors; sum of two conditional error probabilities rather than total prior-weighted error; V equals twice trace distance; inverse forgetting rate; logarithmic readout-weight reach; six-bit patterns considered up to history exchange; task-readout limitation stated at finite accuracy rather than absolute unrecoverability.
- Explicit `nocite` includes three SM-only references in a Letter-only BibTeX build. Bibliography scientific entries otherwise match v3; the received source reverts repository links and submission metadata.
- Wordcounter removes unprinted comments before parsing and excludes `nocite`, preventing the new build note from inflating the count.

## Integration corrections recommended

1. Restore the already approved three authors, ORCIDs, shared affiliation, fixed date, arXiv array workaround, SM contents sizing, Markus-specific AI accountability, and GitHub links. The received version reverts these to a single author/old address/no repository URL.
2. Restore v3 qualifiers for sampled numerical estimates, separately sampled unitaries across k, and continuous plotted threshold crossings versus integer memory depths. The v4 input removes these clarifications despite unchanged data.
3. The new abstract opening “enlarging a noisy quantum reservoir does not extend its memory” is broader than the theorem. An individual reservoir may improve below the ceiling. State that enlargement does not raise the fundamental ceiling instead.
4. Figure 3’s caption “C reaches further back” and markers placed on the optimum can suggest automatic attainment. Describe the higher possible ceiling associated with C, clarify that the diagram shows ceilings, and do not imply every depicted reservoir attains it. This is a schematic, not a simulated fixed-size comparison; the displayed exponential expressions omit constants and have theorem validity ranges.
5. Preserve the exact 100-word justification supplied in the current message. The archive still contains the older 98-word paragraph.

## Length and justification

The exact new user paragraph is **100 whitespace-delimited words**, **699 Unicode characters** excluding its trailing newline. APS requests a 100-word justification. The supplied Letter's approximate count is **3620 words**: 2309 body, 325 captions, 25 data availability, 112 displayed-math equivalents, and approximately 849 figure equivalents. Its abstract is 556 rendered characters (the counter's rough TeX-string result is 560).

The counter's single-column equation and figure-equivalent formulas match the current official APS length guide. There are seven counted equation rows and no main-text tables. Text parsing remains heuristic (for example, inline math is one token and some TeX environment/label tokens can affect counts). Recount the integrated version and label it a local estimate rather than an APS-certified measurement.

Primary sources verified 18 October 2026:
- https://journals.aps.org/authors/length-guide
- https://journals.aps.org/prl/authors

See `content-audit.json` for checks and exact file-change inventory, and `received-wordcount.txt` for the executable count output. Nothing was uploaded or submitted by this audit.
