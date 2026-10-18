# PRL revision 7 - shortened shared affiliation

At the user's request on 18 October 2026, the shared author affiliation is now:

> Quantum Applications and Research Laboratory (QAR-Lab),
> Ludwig-Maximilians-Universität München,
> Oettingenstraße 67, 80538 München, Germany.

The chair and department lines were removed from both the Letter and the
Supplemental Material. The cover letter, author record, citation metadata, and
PRL/arXiv/Zenodo packages use the same shortened affiliation. The three authors,
their order, ORCIDs, and corresponding-author contact remain unchanged.

## Scope and preservation

The immediate predecessor is commit `9b8ea0d01b8eac49c1650781c0abaaceae6b3ec4`.
All earlier PDFs, source snapshots, packages, and received originals remain
preserved. The [original receipt](../paper/versions/2026-10-18-prl-v5/receipt.json)
and exact user-approved 100-word justification remain the frozen inputs.

The canonical TeX change consists of deleting two affiliation lines. All 53
other canonical source files are byte-identical to revision 6. Scientific claims,
proofs, figures, simulation code, numerical data, and the AI disclosure are
unchanged. The short cover letter retains its content and headings; only its
affiliation header changed.

Current files:

- [Combined PDF, 24 pages](../paper/memory_limits_prl_2026-10-18-v7.pdf)
- [PRL package, separate 6-page Letter and 18-page supplement](../paper/submission/prl-2026-10-18-v7/README.md)
- [arXiv source package](../paper/submission/arxiv-2026-10-18-v7/arxiv-source.zip)
- [Local Zenodo handoff](../paper/submission/zenodo-2026-10-18-v7/README.md)
- [Version provenance](../paper/versions/2026-10-18-prl-v7/provenance.json)
- [Source snapshot](../paper/versions/2026-10-18-prl-v7/source-final-prl-v7.zip)

## Verification

The combined PDF compiles without shell escape to 24 pages with no unresolved
references or citations, multiply defined labels, or overfull boxes. BibTeX
regenerates a byte-identical bibliography. The shortened affiliation causes
layout changes on pages 1-7; all seven pages and the cover's first page were
visually inspected. Pages 8-24 retain identical extracted text. The Letter and
supplement PDFs together match the combined PDF's text.

All 22 repository tests pass. Package manifests, ZIP integrity, reconstructed
source equality, shared affiliations, and the unchanged 100-word justification
and referee contacts were checked. The [verification record](../paper/versions/2026-10-18-prl-v7/verification.json)
records the checks. Numerical campaigns and a full proof review were not rerun
for this affiliation edit. The arXiv package was checked against the canonical
build; a separate fresh-extraction compilation was not repeated.

The manuscript body counted for the PRL limit is unchanged; the prior estimate
of 3688 word equivalents remains historical evidence for that identical body.
It is not an APS editorial eligibility determination. The abstract and the
100-word justification are unchanged.

At preparation time all packages were local, with no manuscript submission,
publication, DOI reservation, license choice, or repository-visibility change.
The later [arXiv upload record](../paper/submission-records/arxiv-2026-10-18-v7/README.md)
documents draft 8248308, the user's license choice, and successful arXiv PDF
processing. Final submission was left open; the original preparation snapshots
remain unchanged.
