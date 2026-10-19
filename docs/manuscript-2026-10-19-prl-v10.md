# PRL revision 10 - explicit quantifiers and the three-class conclusion

Revision 10 implements the user's requested Figure 1 update on top of
[revision 9](manuscript-2026-10-19-prl-v9.md).

## Figure 1

- Panel (a) states the upper bound for **every individual system** in the
  admissible noisy-dynamics class N, using the universal quantifier.
- Panel (b) states the lower bound for **one explicit construction** in the
  intersection of quantum reservoirs Q and measurement-free error correction E,
  using the existential quantifier and the star identifying that construction.
- Panel (c) restores the earlier scaling graph alongside the inference for
  all three classes. Because Q and E are
  subsets of N, and the construction belongs to both, the largest memory in
  each of the three classes has exponential scaling in k.

The caption explicitly gives this inheritance argument, refers to **all three
maxima**, and retains fixed noise strength and accuracy. The system symbol S is
distinguished from the class symbol calligraphic S. The schematic curve in
panel (c) illustrates the maximum for a chosen class. The conclusion concerns the optimum over each
class, not a lower bound on every system or attainability at every fixed size.

The manuscript change is confined to this caption; the body text, abstract,
theorems, proofs, numerical statements, author metadata, and AI disclosure are
unchanged. All other figures, simulation code, and supplied data are retained.
The approved cover letter and 100-word justification are preserved byte for byte.
Earlier versions and packages remain unchanged.

## Artifacts and verification

- [Combined PDF](../paper/memory_limits_prl_2026-10-19-v10.pdf).
- [PRL package and upload instructions](../paper/submission/prl-2026-10-19-v10/README.md).
- [arXiv source ZIP](../paper/submission/arxiv-2026-10-19-v10/arxiv-source.zip).
- [Zenodo preparation](../paper/submission/zenodo-2026-10-19-v10/README.md).
- [Source snapshot](../paper/versions/2026-10-19-prl-v10/source-final-prl-v10.zip),
  [provenance](../paper/versions/2026-10-19-prl-v10/provenance.json), and
  [verification](../paper/versions/2026-10-19-prl-v10/verification.json).

Build, local APS-style length accounting, visual inspection, package integrity,
preserved correspondence, and a fresh arXiv extraction/build are recorded with
the revision. The combined PDF has **25 pages (6 Letter + 19 supplement)**;
the local length estimate is **3747 word equivalents**, and the unchanged
plain-text abstract contains **595 characters**. All 22 repository tests pass.
No new scientific simulation campaign
is needed for this figure/caption change. The figure expresses the existing
proof's scope and does not establish a new theorem or a sharper exponent.

Revision 10 is prepared locally. No submission portal, final submission, public
release, DOI, or license is changed.
