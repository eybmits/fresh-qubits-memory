# PRL revision 9 - structural framing and compact scope figure

This revision implements the user's [editorial suggestions](../paper/versions/2026-10-19-prl-v9/editorial-request-original.txt)
on top of revision 8. The input is preserved byte-for-byte with a
[receipt](../paper/versions/2026-10-19-prl-v9/receipt.json). No new scientific
manuscript export was supplied. Revision 8 and all earlier release artifacts
remain unchanged.

## Editorial changes

- The paragraph after Theorem 1 now emphasizes the exponential scaling class,
  the upper bound uniform in system size, and the difference between a universal
  upper bound and an explicit attaining construction. It still states that the
  two bounds do not determine the optimal exponent.
- The numerical comparison above 2^470 versus 316 is moved to SM III G, "How
  tight are the bounds?" The exact values 85.7, 2^470, and 316 no longer appear
  in the main text. The SM distinguishes full-state memory 316 from single-qubit
  memory 309 and retains the noise and accuracy parameters.
- Repeated statements about conservative constants are consolidated in SM III G.
  The temporal-task discussion refers there for quantitative limitations;
  closing the exponent gap remains an explicit open problem in the Conclusion.
- Figure 1 now contains only its two scope panels. The duplicate scaling graph
  is removed; Figure 3 retains that visualization. Width is unchanged and the
  figure is 29.3% shorter. The caption describes the optimum over reservoirs,
  rather than claiming that the lower scaling is attainable at every fixed n.
- The main-text Fawzi/Nelson comparison is shortened and points to the complete,
  already qualified discussion in SM VIII B. The fresh-qubit converse is stated
  more directly, with its noise-model scope retained.
- The construction paragraph now gives a verified factor-five example, and
  the Conclusion emphasizes the fresh-qubit ceiling and error removal without
  claiming that the memory of an individual reservoir is independent of size.
- Supplemental equation links now have separate PDF destinations. This fixes
  a pre-existing collision with main-text equations 1-6 without changing the
  displayed equations or their numbering.

The [change record](../paper/versions/2026-10-19-prl-v9/integration-changes.json)
contains exact before/after text. The mathematical theorem, proof environments,
abstract, simulator, saved datasets, author metadata, AI disclosure, approved
cover letter and 100-word justification are unchanged. Rounded numerical
constants in SM prose now use approximate equality explicitly.

## Quantitative statement and claim boundaries

At q = 0.9 and epsilon = 0.01, the exact single-qubit memory depths for the
plotted odd k = 5, 7, ..., 15 increase by factors between 5.6569 and 6.2986 for
each additional pair of input qubits. The integer depths also satisfy the
factor-five statement. The claim is expressly restricted to those plotted
instances of the repetition reservoir; it is not a universal improvement for
arbitrary reservoirs or noise strengths.

Table S1 reports half-lives, not the epsilon = 0.01 memory depths. The new
sentence therefore cites Figure 4(b), with the derivation in SM V. The
[exact-probability verification](../paper/versions/2026-10-19-prl-v9/verification/factor-five.json)
and [reproduction script](../paper/versions/2026-10-19-prl-v9/verification/check_factor_five.py)
record the formula, precision, ratios, integer conventions, and comparison with
saved data. This bounded check does not prove a statement for every odd k.

An upper/lower exponent gap does not alone prove that no other construction can
attain the upper exponent. Accordingly, the main text says that the bounds do
not determine the rate, rather than adding an unproved non-tightness claim.

## Current artifacts and checks

- [Combined PDF: 25 pages](../paper/memory_limits_prl_2026-10-19-v9.pdf).
- [PRL handoff: 6-page Letter and 19-page supplement](../paper/submission/prl-2026-10-19-v9/README.md).
- [arXiv source ZIP](../paper/submission/arxiv-2026-10-19-v9/arxiv-source.zip).
- [Zenodo preparation](../paper/submission/zenodo-2026-10-19-v9/README.md).
- [Final source snapshot](../paper/versions/2026-10-19-prl-v9/source-final-prl-v9.zip),
  [provenance](../paper/versions/2026-10-19-prl-v9/provenance.json), and
  [verification](../paper/versions/2026-10-19-prl-v9/verification.json).

The local APS-style estimate is **3705 word equivalents**, including figures
and displayed equations; the unchanged abstract contains **595 plain-Unicode
characters**. Length accounting is a local check, not an editorial decision.
The document compiles without unresolved references/citations, multiply defined
labels, or overfull boxes. All 22 repository tests pass. Figure and manuscript
render checks, package integrity, correspondence byte equality, and a fresh
arXiv extraction/build are recorded in the verification files. The independent
numeric checks of revision 8 remain historical evidence for the unchanged
scientific code; no new large simulation campaign was run.

Revision 9 is a local preparation. No submission portal was changed, no final
submission was made, and no publication, DOI, license change, or public GitHub
release is implied. The October 18 arXiv revision-7 upload record remains
historical and does not describe the live status of that draft today.
