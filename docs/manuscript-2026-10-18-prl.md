# Manuscript revision: 18 October 2026, PRL revision 2

**The Fundamental Memory Ceiling of Noisy Quantum Reservoirs**, by Markus Baumann, Jonas Stein, and Claudia Linnhoff-Popien.

Current artifacts are the [PDF](../paper/memory_limits_prl_2026-10-18.pdf), [editable source](../paper/prl-source/memory_limits_prl.tex), [provenance](../paper/versions/2026-10-18-prl-v2/provenance.json), [arXiv source ZIP](../paper/submission/arxiv-2026-10-18/arxiv-source.zip), and [canonical author record](../paper/author_information.json). The [17 October scientific import record](manuscript-2026-10-17-prl.md) remains historical and unchanged.

## Requested corrections

The three confirmed authors and their ORCIDs remain in the same order:

| Author | ORCID |
| --- | --- |
| Markus Baumann | [0009-0007-3575-1006](https://orcid.org/0009-0007-3575-1006) |
| Jonas Stein | [0000-0001-5727-9151](https://orcid.org/0000-0001-5727-9151) |
| Claudia Linnhoff-Popien | [0000-0001-6284-9286](https://orcid.org/0000-0001-6284-9286) |

Their affiliation is combined into one block preserving Quantum Applications and Research Laboratory (QAR-Lab), Chair of Mobile and Distributed Systems, Department of Computer Science, and Ludwig-Maximilians-Universität München. The shared address, Oettingenstraße 67, 80538 München, Germany, appears once per byline, both in the Letter and in the Supplemental Material. The contact remains `markus.baumann@campus.lmu.de`.

The existing Supplemental Material citation is reference **[28]**. This revision adds the actual [GitHub repository URL](https://github.com/eybmits/fresh-qubits-memory) to that entry and the manuscript's code/data information without creating a new bibliography item. There are still 38 cited entries. The manuscript date is fixed to October 18, 2026.

The title, abstract, scientific results, figures, simulator, and datasets remain those imported on 17 October. This is an affiliation and code-access correction, not a new numerical campaign or a proof revision. The received originals and the 17 October PDF, package, manifests, and provenance are preserved unchanged.

## Code access and release status

The user explicitly requested the GitHub link while retaining a **private repository** and will make it public separately. The link can work for authorized collaborators while failing for other readers. Public access to that URL must therefore be established before relying on it as the public code destination; no visibility change is performed in this revision.

The prepared arXiv source ZIP also contains the reproducibility code and data as ancillary material and preserves the figure construction sources. The included instructions reconstruct the full source layout. These files become externally accessible through arXiv only after the corresponding submission is released; local packaging is not publication.

Nothing has been uploaded or submitted. No arXiv identifier, journal acceptance, submission license, or completed account/category endorsement is claimed. The remaining submission workflow includes the user's license choice, any required account/category steps, review of the arXiv-generated PDF, and explicit final submission.

## Verification status

The [17 October import record](manuscript-2026-10-17-prl.md) documents historical finite checks of the unchanged scientific code/data: the supplied diagnostic scripts passed, a replay of six Ising and six Haar realizations at `n=3`, `k=1`, `q=0.9` reproduced the saved depths and washout counts, and the largest forgetting-curve difference was below `8.4e-14`. The full large campaign was not rerun. That edition also passed 22 repository tests and fresh-package compilation.

**Current artifact checks passed.** The [verification record](../paper/submission/arxiv-2026-10-18/verification.json) confirms a fresh arXiv-source extraction and compilation to 22 pages (six Letter/reference pages and sixteen supplement pages), matching BibTeX regeneration, all 38 bibliography entries with `SM` still number 28, and the actual GitHub PDF hyperlinks on pages 6 and 22. The shared street address appears once on each title page. All fonts are embedded; no unresolved references/citations or overfull boxes were found. Rendered title pages, references and the code section were visually checked. All 51 source files reconstruct byte for byte, and ZIP regeneration is deterministic. The scientific code, datasets and figure PDFs are unchanged; no new scientific simulation was run for this formatting/link revision.

## Scientific interpretation qualifications retained

1. **Finite history sampling:** maximizing over the sampled history pairs and continuations gives an estimator/lower witness of the formal memory-depth supremum, not a certified maximization over every possible history.
2. **Comparison across reset widths:** the sampled unitary seed depends on `k`. Changing `k` compares ensembles of different unitaries, rather than intervening on one fixed unitary while holding it unchanged.
3. **Continuous and integer depths:** Figure 4(b) uses continuous threshold crossings; the formal depth is integer-valued. At `k=5`, `q=0.9`, and `epsilon=0.01`, the single-qubit crossing is about 308.08, the integer depth is 309, and the full-state witness is 316. The convention differs by less than one step for the single-qubit comparison and does not alter its exponential scaling.

These presentation and interpretation qualifications remain visible from the prior review. They are not evidence that the universal theorem is false, but successful compilation and finite numerical agreement do not certify that theorem, establish novelty, or demonstrate quantum advantage. No forecasting readout or hardware experiment was added. Technical upload readiness is conditional on the current artifact checks and the remaining submission steps, independently of scientific review.
