# PRL revision 8 - new manuscript with retained submission correspondence

The five files supplied on 19 October 2026 are the basis of this revision.
The [receipt](../paper/versions/2026-10-19-prl-v8/receipt.json) preserves their
names and SHA-256 hashes; the received PDFs, TeX and ZIPs are archived unchanged.
The three source archives agree byte-for-byte. The standalone TeX differs from
the source-archive TeX only by a local `../figs/` graphics search path; the
portable archive source is the integration baseline.

## Requested merge

| Material | Treatment |
| --- | --- |
| Theorem 1(i) | Retains the new explicit rate `delta^-1 = 2^((1+4q)/(1-q)) 2^(beta_q k)`, valid also for small k; the simpler bound for k >= 4 remains its corollary. |
| Novelty framing | Retains the new historical repetition/majority construction, emphasis on the fresh-qubit-rate converse, Fawzi/Nelson comparisons, and SM section VIII B. This is the manuscript's positioning, not independent certification of global novelty. |
| Constants and open questions | Retains the main-text comparison above 2^470 versus 316 and the quantum-code exponent question. The comparison now explicitly gives epsilon = 0.01, identifies 316 as full-state memory, and marks 85.7 as a rounded exponent. |
| GitHub links | Retains the project URL in the Supplemental Material bibliography entry and SM IX. Automatic citation numbering places the entry at [28] in this build; it was [27] in revision 7. |
| Figure 4 | Retains continuous threshold crossings, rounding upward to integer depth, sampled-ensemble scope, and independent unitary sampling across k. |
| Figure S7 | Retains independent ensembles across k and the shared ensemble between input protocols at fixed k. Its simulated integer depths are not relabelled as continuous crossings. |
| Memory capacity | Restores positive finite input variance, a strictly positive readout-noise floor, and finite unconditional variance; explicitly states finite positive variance of y_t. |
| Table S2 | Says additional unital noise does not raise the memory upper bound; it does not claim unchanged attainable memory. |
| Authors and disclosure | Preserves the three authors, ORCIDs, shared QAR-Lab/LMU affiliation, Contact author label, and the previously confirmed Claude-only disclosure. |
| Cover and justification | Preserves the approved cover revision 2 PDF/TXT, its October 18 date, referee files, and exact approved 100-word justification byte-for-byte. Incoming replacement templates remain only in archived originals. |

The manuscript's newer abstract, figures, prose, and additional bibliography
entries are retained. The phrase "Within these ensembles" is restored, and the
washout discussion again distinguishes a size-independent ceiling from the
memory of an individual reservoir. Three redundant passages were shortened to
fit the PRL length budget without removing scientific statements or requested
qualifications. The [integration record](../paper/versions/2026-10-19-prl-v8/integration-changes.json)
records these edits.

## Source checks and build compatibility

The new prior-work discussion was checked against primary papers. Fawzi et al.'s
extension allowing free perfect classical computation is now expressly limited
to unital noise, including depolarizing noise; the SM also states the fixed
sufficiently small simulation-error condition. The total-width versus fresh-rate
comparison remains. See [Fawzi et al., Theorems 1-2](https://drops.dagstuhl.de/storage/00lipics/lipics-vol215-itcs2022/LIPIcs.ITCS.2022.68/LIPIcs.ITCS.2022.68.pdf).

The Nelson comparison explicitly excludes intermediate measurements and
noiseless classical processing, consistent with
[Nelson et al., Theorem 1 and section 1.1](https://drops.dagstuhl.de/storage/00lipics/lipics-vol383-ccc2026/LIPIcs.CCC.2026.38/LIPIcs.CCC.2026.38.pdf).
The text says that pure dephasing can preserve a classical bit rather than
claiming it erases nothing. The historical majority-restoration principle is
supported by [von Neumann, sections 8-10](https://www.smri.it/Publications/vonNeumannNew.pdf);
the present SM supplies the explicit fresh-qubit accounting.

The existing REVTeX-compatible `array` package pin and the validated local APS
word-count helper are retained. The latter fails on unresolved references and
unsupported layouts, disables automatic bibliography inclusion in the counting
pass, and produces structured accounting. The bibliography is regenerated from
the new `refs.bib`, with the restored GitHub URL. No numerical data were altered.

## Files and verification

- [Combined PDF: 25 pages](../paper/memory_limits_prl_2026-10-19-v8.pdf).
- [PRL handoff: 6-page Letter and 19-page supplement](../paper/submission/prl-2026-10-19-v8/README.md).
- [arXiv source ZIP](../paper/submission/arxiv-2026-10-19-v8/arxiv-source.zip).
- [Zenodo preparation](../paper/submission/zenodo-2026-10-19-v8/README.md).
- [Final source snapshot](../paper/versions/2026-10-19-prl-v8/source-final-prl-v8.zip).
- [Provenance](../paper/versions/2026-10-19-prl-v8/provenance.json) and
  [verification](../paper/versions/2026-10-19-prl-v8/verification.json).

The local APS-style length estimate is **3732 word equivalents**: 2789 typeset
words, 96 for six displayed-equation rows, and about 847 for figures. The full
new abstract contains **595 plain-Unicode characters**. These checks do not
constitute an APS editorial eligibility decision.

The combined document and separately compiled Letter have no unresolved
references/citations, multiply defined labels, or overfull boxes. PRL PDF splits
match the combined text. A fresh extraction of the arXiv package compiles to
25 pages with matching text and bibliography; its reconstruction script restores
all 54 canonical source files exactly. Package manifests and ZIP members were
checked, including exact equality of the retained correspondence.

All 22 repository tests and the supplied simulator, constant, and elementary
proof-step diagnostics pass. The simulator Python files and 13 JSON datasets
are byte-identical to the previous version. Finite numeric diagnostics and
sampled matrix checks do not verify a universal theorem; no new large simulation
campaign or forecasting benchmark was run. See the
[numerical report](../paper/versions/2026-10-19-prl-v8/verification/numerical-checks.json).

Revision 8 is prepared locally. No submission portal was changed, no final
submission was made, and no DOI or repository-visibility change is implied.
The last recorded observation of arXiv draft 8248308 is the
[revision-7 upload record from October 18](../paper/submission-records/arxiv-2026-10-18-v7/README.md);
it is historical evidence, not a live check of that draft's current status.
