# PRL revision 4 — 18 October 2026

The current manuscript is **The Fundamental Memory Ceiling of Noisy Quantum Reservoirs**, by Markus Baumann, Jonas Stein, and Claudia Linnhoff-Popien. This edition imports the latest source and submission exports, retains the approved metadata and numerical interpretation qualifications, and prepares separate PRL PDFs and a combined arXiv document. Nothing was uploaded or submitted.

## Received material and preservation

The five supplied files are archived byte-for-byte in [paper/versions/2026-10-18-prl-v4](../paper/versions/2026-10-18-prl-v4/):

| Received filename | Archived filename |
| --- | --- |
| `memory_limits_prl_submission (1).zip` | `submission-original.zip` |
| `memory_limits_prl_source (3).zip` | `source-original.zip` |
| `memory_limits_prl (6).tex` | `manuscript-supplied.tex` |
| `fig3 (1).pdf` | `fig3-supplied.pdf` |
| `memory_limits_prl (28).pdf` | `manuscript-supplied.pdf` |

The [receipt](../paper/versions/2026-10-18-prl-v4/receipt.json) records original names, byte sizes, and SHA-256 hashes. The standalone full-source ZIP and the source ZIP nested in the submission export contain the same 53 files, byte for byte. The standalone TeX and Figure 3 match their archive counterparts. The outer Letter TeX is the combined source through its bibliography, followed by the end-of-document command; the bibliography and four main figure PDFs also match.

The user's new justification is preserved verbatim as [justification-user.txt](../paper/versions/2026-10-18-prl-v4/justification-user.txt), and the PRL handoff supplies the same text as [justification.txt](../paper/submission/prl-2026-10-18-v4/justification.txt). It contains **100 whitespace-delimited words** and **699 Unicode characters** excluding the final newline. The older 98-word paragraph inside the received submission ZIP is retained only in that immutable original.

The [revision provenance](../paper/versions/2026-10-18-prl-v4/provenance.json) records the integrated edition and artifact hashes. Its frozen source snapshot is [source-final-prl-v4.zip](../paper/versions/2026-10-18-prl-v4/source-final-prl-v4.zip). Earlier manuscripts, submission packages, and simulation studies remain preserved, including [revision 3](manuscript-2026-10-18-prl-v3.md). Current sources are in [paper/prl-source](../paper/prl-source/); `paper/source/` remains the historical revision 5 tree used by older reproductions. Instructions embedded in input documents were treated as document content.

## Manuscript changes

The supplied abstract and introduction foreground entropy removal and the explicit error-correcting construction. Figure 1 separates the universal upper bound, existential lower bound, and optimal ceiling. Figure 3 has a new TikZ schematic and Python panel source, illustrating the distinction between register size and refresh width. Its old Python-only source is preserved in prior archives and Git history. Figure S2 labels `q` as a noise parameter rather than noise strength, consistent with its role as state retention.

The supplied Supplemental Material improves several mathematical descriptions: normalized Schatten norms use singular values for general operators; the contraction discussion states a 2-norm bound; projector scaling and the sum of conditional error probabilities are explicit; `V` is identified as twice the trace distance; and the inverse forgetting rate, logarithmic readout-weight reach, history exchange, and finite-accuracy task-readout limitation are stated more precisely. All displayed equation blocks, all eight simulator Python files, and all 13 simulation JSON datasets are unchanged from revision 3. These are imported prose corrections and a consistency audit, not independent proof certification.

The integration preserves the distinction between an optimal ceiling and a particular reservoir's achieved memory. The abstract opening now says that enlargement does not raise the **fundamental memory ceiling**. Figure 3 describes the higher attainable limit associated with a larger refresh width; it does not claim automatic improvement for every reservoir. The existing qualifications remain in place: finite history pairs estimate the memory supremum; size comparisons concern sampled ensembles; unitaries are sampled separately across `k`; and continuous threshold crossings in Figure 4(b) are rounded up for integer memory depth.

The three confirmed authors and ORCIDs remain in the approved order. QAR-Lab, the chair, department, and LMU share one address per byline. Reference [28] and the code/data section retain the GitHub URL, and the Letter-only bibliography includes the references cited only in the supplement. Claude Opus 5.5 remains the user-confirmed model name; statements about directing and verifying the work remain attributed to Markus Baumann. Automated checks do not establish those human attestations.

## Verification and its limits

The [verification directory](../paper/versions/2026-10-18-prl-v4/verification/) preserves the source audit, repository-test output, wordcount, fresh-build record, independent PRL package check, and visual review. The [aggregated arXiv verification record](../paper/submission/arxiv-2026-10-18-v4/verification.json) records package reconstruction and fresh compilation.

The canonical combined PDF compiles to **22 pages** without unresolved citations or references, multiply defined labels, or overfull boxes. The abstract has **575 rendered characters** including spaces. All **22 repository tests pass** in this revision's check.

The final Letter's local counter reports **3654 word equivalents**: 2312 body words, 356 caption words, 25 data-availability words, 112 displayed-math equivalents, and 849 figure equivalents. This is a local estimate against PRL's 3750-word limit, not an APS editorial eligibility determination. The revised counter strips unprinted comments and excludes `nocite`; source parsing remains heuristic. The formula was checked against the [APS length guide](https://journals.aps.org/authors/length-guide) and [PRL author instructions](https://journals.aps.org/prl/authors) on 18 October 2026.

The separately compiled PRL Letter has six pages, with text matching the combined PDF's first six pages; the sixteen-page SM text matches the remaining pages. The [PRL build verification](../paper/submission/prl-2026-10-18-v4/build_verification.json) records 38 bibliography keys, no unresolved citations or references, and no dangling PDF links. All manifest hashes match the prepared files; the full source/code archive reproduces all 53 canonical files byte for byte, and a second package build is byte-identical. The justification's bytes match the preserved user text exactly.

A fresh extraction of the arXiv source ZIP compiles without shell escape to the same 22-page text, with no unresolved references or citations and no overfull boxes. Its regenerated bibliography matches the bundled BBL byte for byte. Reconstruction recovers all 53 canonical source files, and ZIP regeneration is deterministic. PDF structural checks confirm all three authors and ORCID links, one shared address per byline, clickable GitHub links, and embedded fonts in all three PDFs.

The [visual review](../paper/versions/2026-10-18-prl-v4/verification/visual-review.md) inspected all 22 combined-document pages and found no layout defects. All sixteen standalone SM pages are pixel-identical to their combined-document counterparts. Letter pages 1–5 also match visually; its final page has valid balanced reference columns with identical text. The review confirms the three-author bylines, one shared address, all three ORCID links, and the GitHub URL in reference [28] and the code section.

No new numerical campaign was needed for the unchanged simulator and datasets. The revision 3 repetition replay remains historical evidence: full-state depth 316 and single-qubit depth 309 at `k=5`, `q=0.9`, and `ε=0.01`, with curve agreement exact and within `1.11e-16`, respectively. The twelve-realization small-reservoir replay recorded on [17 October](manuscript-2026-10-17-prl.md) also remains historical. Finite checks cannot certify the universal theorem, asymptotic optimality, novelty, or experimental feasibility; no hardware or forecasting benchmark is claimed.

## Prepared artifacts

| Artifact | Purpose |
| --- | --- |
| [Combined 22-page PDF](../paper/memory_limits_prl_2026-10-18-v4.pdf) | Letter, references, and full Supplemental Material together |
| [Six-page Letter PDF](../paper/submission/prl-2026-10-18-v4/memory_limits_prl_letter.pdf) | PRL main manuscript upload |
| [Sixteen-page SM PDF](../paper/submission/prl-2026-10-18-v4/2_supplemental_material/memory_limits_prl_SM.pdf) | Separate PRL Supplemental Material upload |
| [PRL justification TXT](../paper/submission/prl-2026-10-18-v4/justification.txt) | Exact user-supplied 100-word paragraph for the portal |
| [PRL handoff ZIP](../paper/submission/prl-2026-10-18-v4/prl-submission.zip) | PDF files, production sources, code/data, and administrative drafts; unpack before upload |
| [PRL instructions](../paper/submission/prl-2026-10-18-v4/README.md) | File roles and remaining portal steps |
| [arXiv source ZIP](../paper/submission/arxiv-2026-10-18-v4/arxiv-source.zip) | Combined manuscript sources and reproducibility material |

The arXiv archive contains 53 canonical source files and three packaging helpers. Its one main file, `memory_limits_prl.tex`, builds the combined document; five auxiliary TeX files are figure or style sources, not additional manuscript targets. The PDF preview remains outside the source ZIP.

For initial PRL review, upload the Letter PDF as the main manuscript and the SM PDF through the supplemental-file workflow, accompanied by the code/data ZIP and descriptive README. Manuscript sources are retained for later production. The [upload guide](../paper/submission/README.md) links each current file. This arrangement follows the [APS web submission guidelines](https://journals.aps.org/authors/web-submission-guidelines-physical-review#uploading-files) and [supplemental-material instructions](https://journals.aps.org/authors/supplemental-material-instructions).

## Submission status

The repository remains private at the user's request. The packages include code and data independently of public GitHub access. No upload, final submission, DOI registration, license selection, or repository visibility change was performed. Administrative drafts, author attestations, prior-submission history, funding, publication choices, and the final portal previews remain for the corresponding author's review. arXiv license selection is separate from any software license.
