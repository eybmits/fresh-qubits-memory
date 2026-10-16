# Manuscript revision 5: 16 October 2026

Current full manuscript: **The Memory Limits of Noisy Quantum Reservoirs**, by Markus Baumann, Jonas Stein, and Claudia Linnhoff-Popien.

[PDF](../paper/memory_limits_2026-10-16-v5.pdf) | [LaTeX](../paper/source/memory_limits.tex) | [Provenance](../paper/versions/2026-10-16-v5/provenance.json) | [PRA format check](pra-template-check-2026-10-16-v5.md)

## Supplied revision and scope

The new inputs are `memory_limits (9).pdf` and `memory_limits_source (2).zip`. The supplied PDF has 21 pages. The new source retains the approved title and abstract but was supplied with only Markus Baumann in its byline. The integration retains the previously requested three authors, all three ORCID identifiers, and the two QAR-Lab/chair affiliations for each author. Earlier v4 sources, PDFs and submission bundles remain historical records.

Relative to v4, the new manuscript develops the proof framework and its physical interpretation in considerably more detail:

- A dedicated appendix defines normalized Schatten quantities, distinguishability, purity and the input budget through the operator inequality `E(I) <= 2^b I`.
- Expanded arguments relate the purity recursion and contraction to unique echo states, driven memory, finite-time runs and initialization washout.
- A new glossary table records proof constants and their origin.
- The noise discussion explicitly treats extra unital channels around the independent depolarizing layer, non-unital channels with bounded budgets, and a decomposition of full-rank unital qubit channels with a depolarizing component. The baseline matching construction does not imply that every additional unital channel preserves its attainable lifetime.
- The repetition-code appendix discusses anisotropic unital noise using the best-preserved Bloch direction. The accuracy condition for its readout-based lower bound remains relevant.
- The numerical-methods appendix is expanded. The robustness figure's evolution-time label changes from `J tau` to `J Delta t`, separating physical evolution time from the normalized-trace symbol.

The integration also makes six narrowly scoped wording clarifications without changing equations: three references to `k_q` now call it a sufficient threshold, `P_*` is described as an upper bound on maintainable purity, `C` as the prefactor in the interpolated 2-norm bound, and the unital-channel subsection title is restricted to full-rank Choi matrices. Apart from these recorded clarifications, table-format compatibility and the existing acknowledgment's attribution to Markus, the supplied scientific body is retained.

All supplied simulator scripts and five JSON datasets match their v4 versions byte-for-byte. The numerical study remains distinct from `results/empirical-2026-10-16/`, which is not silently incorporated into either submission supplement. This revision's expanded proofs are author-supplied content; integrating them is not an independent mathematical certification.

## Formatting and validation

The integrated manuscript compiles to 21 pages in REVTeX 4.2 with `aps,pra,reprint,superscriptaddress,floatfix`, plus `orcidlink` for author identifiers. Four paragraph-column table preambles received the same REVTeX/array compatibility repair used previously; formatting preserves cell contents except for the recorded glossary wording clarifications. There are eight figures and six tables in the new source.

The integrating agent rendered and inspected all 21 pages, including the first-page author block, the new proof-constant glossary and the revised robustness figure. All eight figures and six tables are present. All three exact ORCID URL annotations were verified. There are no overfull boxes or unresolved references; nonfatal nameref and REVTeX deferred-float warnings remain. All 12 repository tests pass. The PDF SHA256 is `69a83d1a0c0f4bab16b29e879efd2226f0f16fc6a0b2c8701a5e7544b315ea76`. The final upload-source copy embeds the generated BBL; the editable source continues to use BibTeX. The supplied simulator code and JSON datasets are unchanged, so full campaigns were not rerun. Earlier diagnostic evidence remains tied to its recorded source hashes. Fresh package compilation is recorded in the package manifest.

## Submission status and scientific limits

The PRA portal draft `es2026oct16_686` remains unsubmitted, with no uploaded files and no author fields entered. The browser upload permission was declined; this preparation does not retry the upload. ORCID identifiers are known but APS authentication remains separate. The profile name and unaffiliated state require verification/correction; an academic title for Markus is not verified.

A separate unsubmitted PRL draft, `es2026oct16_693`, exists, also with no uploaded files or author fields. The full v5 manuscript is a source/reference for PRL planning, not a finished Letter. No short PRL manuscript has been authorized or created, and no joint submission is declared. The incoming v5 core contains 6,218 ordinary TeXcount words (5,264 body, 165 headings, 789 captions). Including the audited equation, figure and table contributions gives a conservative estimate of at least 7,733 PRL word-equivalents, versus the 3,750-word core limit. These are local estimates, not an official APS count; the final integration makes only minor wording edits, and a condensed Letter needs its own count.

As before, Ising/Haar depths maximize over five sampled continuations per realization. These are lower witnesses for the worst-case memory depth, not its certified supremum. The studies do not train a forecasting readout or establish quantum computational advantage. The main-text interpretation, author declarations and the existing assistance/human-verification statements remain matters for author review before submission.
