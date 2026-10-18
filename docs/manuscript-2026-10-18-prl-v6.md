# PRL revision 6 - AI disclosure clarification

This edition changes only the AI disclosure in the Acknowledgments and the
Supplemental Material's code-and-data paragraph. The user clarified on
18 October 2026 that GPT was used only for language and formatting. The current
disclosure therefore names Claude Opus 5.5 (Anthropic) for the substantive roles
already described in the manuscript. This is an author-provided account of tool
use, not an independently established complete usage history.

The acknowledgment now reads:

> Claude Opus 5.5 (Anthropic) assisted with manuscript preparation, checks of
> derivations and references, and simulation and plotting code. Markus Baumann
> reviewed the outputs and takes responsibility for the final content.

The former blanket phrase "verified all results" is replaced by the narrower
review statement. The supplement names Claude as a code-development aid and
retains the actual validation and exact-result cross-references. It does not
recast the reported substantive assistance as language polishing.

The [APS AI policy](https://journals.aps.org/authors/appropriate-use-ai-tools),
checked 18 October 2026, distinguishes substantive assistance from light editing
and asks for tools/versions, roles, and author oversight. The GPT omission follows
the user's clarification about its editorial-only role. The cover letter still
correctly points to the manuscript's AI disclosure and is unchanged.

## Scope and preservation

The immediate predecessor is commit `17ff77b5dc2b14a6650246959beb1aa6c5064fc3`.
All revision-5 PDFs, received originals, source snapshots, and packages remain
preserved. The [original receipt](../paper/versions/2026-10-18-prl-v5/receipt.json)
and exact user-approved 100-word justification remain the frozen inputs.

Only two lines of the canonical TeX source changed. All other source files,
including the eight simulator scripts, thirteen numerical datasets, bibliography,
and figure files, are byte-identical to the predecessor. No scientific claim,
proof, figure, simulation, author identifier, or affiliation was changed.

Current files:

- [Combined PDF, 24 pages](../paper/memory_limits_prl_2026-10-18-v6.pdf)
- [PRL package, separate 6-page Letter and 18-page supplement](../paper/submission/prl-2026-10-18-v6/README.md)
- [arXiv source package](../paper/submission/arxiv-2026-10-18-v6/arxiv-source.zip)
- [Local Zenodo handoff](../paper/submission/zenodo-2026-10-18-v6/README.md)
- [Version provenance](../paper/versions/2026-10-18-prl-v6/provenance.json)
- [Source snapshot](../paper/versions/2026-10-18-prl-v6/source-final-prl-v6.zip)

## Verification

The combined PDF compiles without shell escape to 24 pages with no unresolved
references or citations, multiply defined labels, or overfull boxes. BibTeX
regenerates a byte-identical bibliography. Extracted page text differs from
revision 5 only on pages 5 and 24; both changed pages were visually inspected.
All 22 repository tests pass. The [verification record](../paper/versions/2026-10-18-prl-v6/verification.json)
records the scoped build and consistency checks. Numerical campaigns and a full
proof review were not rerun for this disclosure edit.

The manuscript body counted for the PRL limit is unchanged; the prior estimate
of 3688 word equivalents remains historical evidence for that identical body.
It is not an APS editorial eligibility determination. The rendered abstract and
the 100-word justification are unchanged.

All packages are local preparations. No manuscript submission, publication,
DOI reservation, license choice, or repository-visibility change was performed.
