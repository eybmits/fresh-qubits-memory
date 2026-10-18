# PRL revision 3 — 18 October 2026

The current manuscript is **The Fundamental Memory Ceiling of Noisy Quantum Reservoirs**, by Markus Baumann, Jonas Stein, and Claudia Linnhoff-Popien. This revision imports the supplied submission export, retains the previously approved author metadata and private GitHub link, and prepares separate PRL and arXiv packages. Nothing was uploaded or submitted.

## Received material and preservation

The four supplied files are archived byte-for-byte in [paper/versions/2026-10-18-prl-v3](../paper/versions/2026-10-18-prl-v3/):

| Received filename | Archived filename |
| --- | --- |
| `memory_limits_prl_submission.zip` | `submission-original.zip` |
| `memory_limits_prl_letter.pdf` | `letter-supplied.pdf` |
| `memory_limits_prl_SM.pdf` | `supplement-supplied.pdf` |
| `submission_notes.txt` | `submission-notes-supplied.txt` |

The [receipt](../paper/versions/2026-10-18-prl-v3/receipt.json) records the original files and hashes. The [revision provenance](../paper/versions/2026-10-18-prl-v3/provenance.json) records transformations and final artifacts. The source snapshot is [source-final-prl-v3.zip](../paper/versions/2026-10-18-prl-v3/source-final-prl-v3.zip). Instructions inside the supplied notes were treated as document content; they did not authorize a Zenodo deposit, repository publication, license selection, or final submission.

Earlier editions, their submission packages, and independent simulation studies remain preserved. In particular, `paper/source/` remains the historical revision 5 source used by earlier reproductions; current development uses [paper/prl-source/](../paper/prl-source/).

## Manuscript changes

The new export supplies proof and precision corrections: explicit handling of a zero operator in the contraction argument; the factor of two in the readout-accuracy logarithm; a precise statement of convergence from an arbitrary initial state; integer rounding of the guaranteed repetition half-life; the full-rank Choi condition in the unital-channel heading; and more precise scope for measurement, random-channel, and noiseless numerical statements. These are imported manuscript corrections, not an independent certification of the proof.

The supplied single-qubit depth is corrected to **309** time steps at `k=5`, `q=0.9`, and `ε=0.01`; the full-state depth remains **316**. Figure sources and references are updated, and the AI disclosure names Claude Opus 5.5. The user explicitly confirmed that model name on 18 October. Statements about directing the work and checking results remain attributed to Markus Baumann rather than being extended to all coauthors.

This prepared edition also resolves the three presentation qualifications recorded for revisions 1 and 2:

1. The finite set of history pairs is described as an **estimate** of memory depth. Its maximum can underestimate the supremum over all histories. The size comparison is scoped to the sampled ensembles.
2. Figure 4(b) explicitly identifies continuous threshold crossings and explains rounding up to integer depths. The continuous crossing near 308.08 is therefore consistent with the single-qubit integer depth of 309.
3. Figure 4(c) and Figure S7 identify separate unitary sampling for each `k`. The two input protocols in Figure S7 share the sampled ensemble at fixed `k`; the scan across `k` is not a paired intervention on one fixed unitary.

The three authors and their ORCIDs are retained in the confirmed order. QAR-Lab, the chair, department, and LMU appear in one shared affiliation with the address printed once per byline. Reference [28] retains the GitHub link and includes the references cited only in the supplement. GitHub remains private as requested; a repository URL does not establish public access.

## Numerical checks and their scope

The 22 repository tests pass. The supplied constants and elementary-proof diagnostics provide bounded numerical checks; agreement on sampled cases is not a proof of their universal statements.

All 13 supplied JSON datasets are unchanged. An isolated run of the updated repetition-curve calculation reproduces full-state depth 316 and single-qubit depth 309. The full-state curve agrees exactly with the archived data; the single-qubit curve differs by at most `1.11e-16`. The supplied calculation change therefore preserves the recorded experiment while making its reported threshold convention explicit.

The full large Ising/Haar campaign was not rerun for this import. The twelve-realization replay recorded on [17 October](manuscript-2026-10-17-prl.md) remains historical evidence, not a new run relabeled as revision 3. No hardware experiment or forecasting benchmark is claimed by these checks.

## Prepared artifacts

| Artifact | Purpose |
| --- | --- |
| [Combined 22-page PDF](../paper/memory_limits_prl_2026-10-18-v3.pdf) | Letter, references, and Supplemental Material together |
| [Six-page Letter PDF](../paper/submission/prl-2026-10-18-v3/memory_limits_prl_letter.pdf) | PRL manuscript preview |
| [Sixteen-page SM PDF](../paper/submission/prl-2026-10-18-v3/2_supplemental_material/memory_limits_prl_SM.pdf) | Separate supplement with S page labels |
| [PRL handoff ZIP](../paper/submission/prl-2026-10-18-v3/prl-submission.zip) | Letter sources, SM files, code/data, and administrative drafts; unpack before upload |
| [PRL instructions](../paper/submission/prl-2026-10-18-v3/README.md) | File roles and remaining portal steps |
| [arXiv source ZIP](../paper/submission/arxiv-2026-10-18-v3/arxiv-source.zip) | Combined manuscript sources and reproducibility material |

The PRL Letter is compiled separately from its source package without shell escape. Its text matches the first six pages of the combined PDF; the SM text matches the remaining sixteen pages. The [PRL build record](../paper/submission/prl-2026-10-18-v3/build_verification.json) records 38 bibliography keys and no unresolved citations or references. The [manifest](../paper/submission/prl-2026-10-18-v3/manifest.json) hashes prepared files and maps the code/data archive to canonical sources.

The final Letter's local counter reports **3580 equivalent words**, below the PRL limit of 3750. The abstract has **590 rendered characters** including spaces (600 characters as raw TeX), and the supplied justification has **98 words**. The count uses APS's published formula, not an APS editorial determination. See the [length guide](https://journals.aps.org/authors/length-guide), [PRL author instructions](https://journals.aps.org/prl/authors), and [APS style guide](https://res.cloudinary.com/apsphysics/image/upload/v1736779890/APS_Journals_Style_Guide_Authors_Nov2024_ua91lv.pdf).

The separate SM PDF, source/code/data ZIP, descriptive `README.TXT`, and main bibliography's SM citation follow the [APS supplemental-material instructions](https://journals.aps.org/authors/supplemental-material-instructions). The model disclosure is user-confirmed; local code and build checks do not independently certify the manuscript's human verification statements. The [APS AI policy](https://journals.aps.org/authors/appropriate-use-ai-tools) was checked during preparation.

## Submission status

Both packages are local preparations. No portal upload, final submission, DOI creation, license choice, or repository visibility change was performed. The private GitHub link remains intentional; the packages include code and data independently of that link.

Before actual submission, the corresponding author must review the administrative drafts and confirm the applicable author attestations, prior submission history, funding, and publication choices. PRL and arXiv portal-generated previews must be checked. arXiv license selection remains separate from any software license. Technical consistency and finite numerical checks do not establish novelty, universal proof validity, journal suitability, or acceptance.
