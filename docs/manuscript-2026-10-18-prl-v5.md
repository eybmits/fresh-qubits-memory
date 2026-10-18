# PRL revision 5 — 18 October 2026

The current manuscript is **The Fundamental Memory Ceiling of Noisy Quantum Reservoirs**, by Markus Baumann, Jonas Stein, and Claudia Linnhoff-Popien. This edition imports the latest source, submission, and Zenodo handoffs, retains the confirmed metadata and numerical interpretation qualifications, and prepares separate PRL PDFs and a combined arXiv document. The Zenodo handoff is a local draft. No external upload, submission, DOI reservation, license selection, or visibility change was performed.

## Received material and preservation

The five supplied files are archived byte-for-byte in [paper/versions/2026-10-18-prl-v5](../paper/versions/2026-10-18-prl-v5/):

| Received filename | Archived filename |
| --- | --- |
| `memory_limits_prl_zenodo.zip` | `zenodo-original.zip` |
| `memory_limits_prl_source (4).zip` | `source-original.zip` |
| `memory_limits_prl (7).tex` | `manuscript-supplied.tex` |
| `memory_limits_prl (37).pdf` | `manuscript-supplied.pdf` |
| `memory_limits_prl_submission (2).zip` | `submission-original.zip` |

The [receipt](../paper/versions/2026-10-18-prl-v5/receipt.json) records original names, byte sizes, and SHA-256 hashes. The nested source archives in the received Zenodo and PRL submission bundles are byte-identical (SHA-256 `41a5e024b0431cfe32db0452d969b6f8340fe6b121dd2ee3fe230c791f815fdb`). The received source package includes 54 files. Final input comparisons and source changes are recorded in the [provenance](../paper/versions/2026-10-18-prl-v5/provenance.json).

The latest user-approved PRL justification is retained verbatim in [justification-user.txt](../paper/versions/2026-10-18-prl-v5/justification-user.txt) and [the prepared TXT](../paper/submission/prl-2026-10-18-v5/justification.txt). It has 100 whitespace-delimited words and includes the supplied LaTeX delimiters. It states fixed noise strength and accuracy and separates the universal upper bound from the achieving construction. Both earlier justification paragraphs and their provenance remain in [revision 4](manuscript-2026-10-18-prl-v4.md).

The [final source snapshot](../paper/versions/2026-10-18-prl-v5/source-final-prl-v5.zip) preserves this edition. Earlier manuscripts, packages, and experimental evidence remain unchanged. Current sources are in [paper/prl-source](../paper/prl-source/); `paper/source/` remains the historical 16 October revision 5 tree imported by older reproductions. Instructions inside the received Zenodo documentation were treated as content, not authorization to publish or select a license.

## Manuscript changes

The received revision changes document typography to Latin Modern with Unicode text mappings, revises Figure 3's panels and the Figure 4 baseline, and expands the Supplemental Material treatment of memory capacity and finite-precision readout. The new Figure 3(a) plotting source replaces the prior panel source; earlier files remain in the version archives and Git history. The bibliography and code/supplement citation have been reorganized: the code link is now in reference **[27]**, not [28].

The integration preserves the distinction between an optimal memory ceiling and the achieved memory of an individual reservoir. The abstract opening describes the fundamental ceiling, Figure 3 describes a higher attainable ceiling, and the initialization-washout condition remains separate from driven memory. The Supplemental Material now explicitly requires finite positive input variance, `0 < Var(u) < infinity`, when defining normalized linear memory capacity, and states the intended finite readout-resolution range `0 < sigma <= 2B`. These are explicit assumptions for the expanded discussion, not a new simulation campaign. Table S2 now states that additional unital noise does not raise the memory upper bound; this does not assert that achievable memory is unchanged by additional noise.

The existing numerical interpretation qualifications remain: finite history pairs estimate the supremum defining memory depth; size comparisons apply to sampled ensembles; different `k` values use independently sampled unitaries; and Figure 4(b)'s continuous threshold crossings are rounded up to define integer memory depth. All eight simulator Python files and all 13 supplied simulation JSON datasets are unchanged from the preceding edition.

The three confirmed authors and ORCIDs remain in their approved order. QAR-Lab, the chair, department, and LMU share one address per byline. The GitHub link remains in the code/supplement reference and code/data section. Claude Opus 5.5 remains the user-confirmed model name; verification statements remain attributed to Markus Baumann. Automated checks do not independently establish those human attestations.

## Length accounting

The received `checks/aps_wordcount.py` adds a PDF-text-based local APS-style word-equivalent estimate alongside the older source-text heuristic. Its integration makes failures explicit and handles bibliography suppression through the local TeX build environment instead of assuming the BBL is absent. The counters use different text extraction methods and are local estimates; neither is an APS editorial eligibility determination. On the final source, the APS-style counter reports **3688 word equivalents**: 2729 text words, 112 displayed-equation equivalents, and 847 figure equivalents. This is about 62 below the 3750-word PRL limit under that local method. The older source-text heuristic reports **3524** and is retained as a secondary estimate rather than substituted for the more conservative result. The rendered abstract contains **588 characters**, including spaces.

## Verification and its limits

The canonical combined PDF compiles to **24 pages**, comprising the six-page Letter and eighteen-page Supplemental Material, without unresolved citations or references, multiply defined labels, or overfull boxes. All **22 repository tests pass**. The [verification directory](../paper/versions/2026-10-18-prl-v5/verification/) preserves this revision's evidence.

The local Zenodo handoff has been generated twice with identical bytes. All manifest hashes, all 54 archived source files, the outer archive contents, three-author ORCID order, and revision-5 citation metadata pass verification. License, access, publication date, and DOI remain unset in the draft. The final PRL and Zenodo source ZIPs are byte-identical (SHA-256 `b7d2636a1c32f21011c917cf6364a30fda481ed8b255afb1737acf46ea20c08f`).

The independently checked PRL package contains a separately compiled six-page Letter and an eighteen-page SM; their text matches the corresponding ranges of the final combined PDF. All managed-file hashes and archive contents pass, all 54 source mappings match the canonical source, SM page labels are S1–S18, the latest 100-word justification matches byte for byte, and the final Table S2 wording is present. Author metadata, all three Letter ORCID links, and GitHub URLs are preserved. Repeated full PRL builds are byte-identical. See the [PRL build verification](../paper/submission/prl-2026-10-18-v5/build_verification.json) and this edition's [verification directory](../paper/versions/2026-10-18-prl-v5/verification/).

A fresh arXiv extraction compiles without shell escape to the same 24-page text, with no unresolved citations/references or overfull boxes. Its regenerated BBL is byte-identical to the bundled bibliography. Reconstruction restores all 54 canonical source files, the archive has 57 entries, and regeneration is deterministic. The [arXiv verification record](../paper/submission/arxiv-2026-10-18-v5/verification.json) records these checks. The final combined PDF SHA-256 is `90f0e19e58f22fcdac6fc5c01ce5864adc6b4f87641498bcb53924884c956a62`.

All 24 final combined-document pages pass visual review, including the author bylines, new Figure 3, Figure 4, reference [27], the memory-capacity paragraph, Table S2, and the final code/data section. All eighteen standalone SM pages are pixel-identical to the corresponding combined pages. Standalone Letter pages 1–5 are pixel-identical; its reference-only final page balances cleanly into two columns, with identical extracted text. All fonts are embedded Type 1 fonts. The main Latin Modern prose fonts have Unicode maps; some imported figure fonts do not, so no claim is made that every embedded font has a Unicode map. The [visual-review record](../paper/versions/2026-10-18-prl-v5/verification/visual-review.json) records these checks.

The revision 3 repetition replay remains historical evidence for unchanged numerical source/data: full-state depth 316 and single-qubit depth 309 at `k=5`, `q=0.9`, and `epsilon=0.01`, with curve agreement exact and within `1.11e-16`, respectively. The twelve-realization small-reservoir replay recorded on [17 October](manuscript-2026-10-17-prl.md) also remains historical. The full large campaign is not rerun for a document/package update. Finite checks cannot certify the universal theorem, asymptotic optimality, novelty, or hardware feasibility.

## Prepared artifacts

| Artifact | Purpose |
| --- | --- |
| [Combined 24-page PDF](../paper/memory_limits_prl_2026-10-18-v5.pdf) | Letter, references, and full Supplemental Material together |
| [Six-page Letter PDF](../paper/submission/prl-2026-10-18-v5/memory_limits_prl_letter.pdf) | PRL main manuscript upload |
| [Eighteen-page supplement PDF](../paper/submission/prl-2026-10-18-v5/2_supplemental_material/memory_limits_prl_SM.pdf) | Separate PRL Supplemental Material upload |
| [PRL justification TXT](../paper/submission/prl-2026-10-18-v5/justification.txt) | Exact latest user-supplied 100-word paragraph for the portal |
| [PRL handoff ZIP](../paper/submission/prl-2026-10-18-v5/prl-submission.zip) | PDFs, production sources, code/data, and administrative drafts; unpack before upload |
| [PRL instructions](../paper/submission/prl-2026-10-18-v5/README.md) | File roles and remaining portal steps |
| [arXiv source ZIP](../paper/submission/arxiv-2026-10-18-v5/arxiv-source.zip) | Combined manuscript sources and reproducibility material |
| [Zenodo draft handoff](../paper/submission/zenodo-2026-10-18-v5/README.md) | Code/data source ZIP, draft metadata, author details, citation, and hashes |

The source layout has 54 canonical files. The arXiv archive adds three packaging helpers, making 57 entries; its sole main TeX file is `memory_limits_prl.tex`. Five auxiliary TeX files are figure/style sources rather than additional manuscript targets. The combined PDF preview remains outside the source ZIP. For PRL, the Letter PDF and supplemental PDF are separate upload files; the code/data ZIP accompanies the supplement. The [upload guide](../paper/submission/README.md) links the current files.

## Local Zenodo preparation

The received `.zenodo.json` named only Markus Baumann and suggested CC BY 4.0 and open access. The current manual-entry draft restores all three confirmed authors, their ORCIDs, and the shared affiliation. It identifies the source edition as `2026-10-18-prl-v5`, uses the received Dataset resource-type proposal, and describes the supplied numerical diagnostics without claiming that they prove the theorem.

License, access right, publication date, and DOI are intentionally absent from `zenodo_metadata_draft.json`. The received proposal is preserved in the immutable input and provenance. The draft is not an automatic `.zenodo.json` integration or a complete API request: Zenodo's documented defaults must not be confused with an author's decision. The source ZIP is the same canonical code/data material prepared for PRL. Creator/ORCID and metadata field names were checked against the [official Zenodo documentation](https://developers.zenodo.org/#deposit-metadata); no live portal validation or deposition was performed.

## Cover-letter update

The cover letter was subsequently replaced with the user's detailed 18 October
draft, adapted to the three-author manuscript and the shared QAR-Lab/LMU address.
The [two-page PDF](../paper/submission/prl-2026-10-18-v5/cover_letter.pdf) and
[TXT](../paper/submission/prl-2026-10-18-v5/cover_letter.txt) include five suggested
referees and four alternates with professional contact details checked against
institutional sources. The [contact record](../paper/submission/prl-2026-10-18-v5/referees.json)
preserves those sources. The user's submission-history and exclusivity statements
are retained as author declarations. The user subsequently confirmed absence of
competing interests and conflicts with the proposed referees for all three
authors; the letter now includes that declaration. The preparation notes also record
Zambrini's listed 2020–2026 PRL editorial role for eligibility review.

`scripts/prepare_prl_cover.py` reproducibly renders the administrative source in
`paper/submission-admin/prl-2026-10-18/`; `scripts/prepare_prl.py` incorporates it
into the PRL handoff. At the user's request the letter was shortened by about
one third and given three headings and a compact letterhead; the referee list
remains on page 2. Both cover pages were visually inspected, no placeholders
remain, and repeated rendering is byte-identical. This administrative update
does not change the manuscript, its simulations, the 100-word justification,
or the arXiv and Zenodo packages.

## Submission status

The repository remains private at the user's request. Code and data are included in the handoff archives independently of public GitHub access. No upload, final submission, DOI registration/reservation, license selection, or repository visibility change occurred. Portal previews, author attestations, funding and publication choices remain for the corresponding author's review. Zenodo licensing, arXiv licensing, and any repository software license are separate decisions; none is selected by creating these local packages.
