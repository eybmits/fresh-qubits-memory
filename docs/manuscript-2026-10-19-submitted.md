# Submitted manuscript and full arXiv companion — 19 October 2026

The user requested that the exact final manuscript be synchronized to GitHub and prepared as a complete arXiv document. No manuscript changes were made during this synchronization. The final canonical source retains the abstract, introduction, entropy-budget terminology, simulations, conclusion, section-specific Supplemental Material citations, Figure 4 caption, and shortening edits previously authorized after revision 10. All intermediate dated PDFs and provenance directories remain preserved.

## Artifacts

- [Complete PDF](../paper/memory_limits_prl_2026-10-19-concise.pdf): 25 pages, six-page Letter plus nineteen-page supplement.
- [PRL handoff](../paper/submission/prl-2026-10-19-submitted/README.md), including the unchanged approved cover and local significance statement.
- [Canonical source snapshot](../paper/versions/2026-10-19-submitted/canonical-source.zip) and [provenance](../paper/versions/2026-10-19-submitted/provenance.json).
- [arXiv source ZIP](../paper/submission/arxiv-2026-10-19-submitted/arxiv-source.zip) and [fresh-build verification](../paper/submission/arxiv-2026-10-19-submitted/verification.json).

The complete PDF SHA256 is `f450ca6f27b70e5e10a8464532ab43dd6a593ffaf4ab6171365b777befabd3a9`; canonical TeX SHA256 is `77df6be9120b0d5cdde39dd62dfb6d63fab8e07ce4c3de3cc4d7f4c8d0a4fd02`. The local APS-method length estimate is 3743.4076 word equivalents; this does not establish editorial eligibility.

## Verification

The [local artifact report](../paper/versions/2026-10-19-submitted/local-artifact-verification.json) records 22 passing tests using `PYTHONPATH=src python -m unittest discover -s tests -v`. Desktop and workspace handoff artifacts match byte-for-byte. The standalone Letter contains exactly the first six pages' text; its final reference-page column balancing differs from the combined layout. The remaining nineteen pages match the supplement text exactly.

All 53 scientific members of the public code/data archive match the canonical source. Its README alone contains administrative cleanup. The arXiv build uses that clean README, retains all source material through the ancillary reconstruction layout, and excludes editor-only documents. Fresh extraction, compilation, bibliography regeneration, archive reconstruction, and deterministic regeneration passed. The resulting PDF is byte-identical to the preserved complete manuscript. All 25 rendered pages were reviewed in a contact sheet, with detailed checks of the first Letter page, first supplement page, and final page. No unresolved references, overfull boxes, or duplicate destinations were reported.

The packaging script now accepts explicit `--edition` and `--readme-file` options. Scientific simulation code, data, figures, and historical experiments were not changed or rerun as a new campaign. These checks establish artifact consistency, not theorem correctness, novelty, or acceptance.

## Portal records

The [author-provided APS screenshot](../paper/submission-records/prl-2026-10-19/README.md) shows **Submitted 19Oct2026-07:43 EDT**, temporary ID **es2026oct16_693**. The user submitted the manuscript. APS-hosted file bytes and final justification/referee fields were not independently retrieved.

The [arXiv record](../paper/submission-records/arxiv-2026-10-19/README.md) records the full source upload, successful 25-page portal compilation, and saved metadata in draft **8251813**. The [downloaded portal PDF comparison](../paper/submission-records/arxiv-2026-10-19/portal-pdf-verification.json) confirms identical scientific text on all 25 pages and identical rendering except the arXiv stamp on page 1. Final submission remains open. The earlier draft was no longer listed in the account; no cause is inferred. A draft ID is not a public arXiv identifier. At the author's request, GitHub was made public on 19 October 2026. The older Zenodo preparation is historical.
