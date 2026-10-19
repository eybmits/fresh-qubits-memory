# Manuscript versions and source

## Current version: 19 October 2026, PRL revision 10

**The Fundamental Memory Ceiling of Noisy Quantum Reservoirs**

Markus Baumann, Jonas Stein, and Claudia Linnhoff-Popien share one affiliation: Quantum Applications and Research Laboratory (QAR-Lab), Ludwig-Maximilians-Universität München, Oettingenstraße 67, 80538 München, Germany. The address appears once in each of the Letter and Supplemental Material bylines. The three approved ORCID links and campus.lmu.de contact address are retained in the [canonical author record](author_information.json).

- [Combined PDF, 25 pages](memory_limits_prl_2026-10-19-v10.pdf), [Letter, 6 pages](submission/prl-2026-10-19-v10/memory_limits_prl_letter.pdf), [Supplemental Material, 19 pages](submission/prl-2026-10-19-v10/2_supplemental_material/memory_limits_prl_SM.pdf)
- [Editable LaTeX](prl-source/memory_limits_prl.tex), [bibliography](prl-source/refs.bib), [build instructions](prl-source/README.txt)
- [Received originals and receipt](versions/2026-10-19-prl-v10/receipt.json), [provenance](versions/2026-10-19-prl-v10/provenance.json), [final source snapshot](versions/2026-10-19-prl-v10/source-final-prl-v10.zip)
- [Revision scope and verification](../docs/manuscript-2026-10-19-prl-v10.md)
- [PRL handoff ZIP](submission/prl-2026-10-19-v10/prl-submission.zip) and [upload instructions](submission/prl-2026-10-19-v10/README.md)
- [Prepared arXiv source ZIP](submission/arxiv-2026-10-19-v10/arxiv-source.zip)
- [Local Zenodo handoff](submission/zenodo-2026-10-19-v10/README.md)
- [Upload guide: separate PRL PDFs, combined arXiv version, and Zenodo draft](submission/README.md)

Revision 10 clarifies Figure 1's quantifiers and restores the earlier panel (c) scaling graph alongside the logical inference. Panel (a) states the bound for every admissible system in $\mathcal N$. Panel (b) identifies one construction in the overlap of quantum reservoirs $\mathcal Q$ and measurement-free error correction $\mathcal E$. Since both subclasses lie in $\mathcal N$, panel (c) gives exponential scaling for the optimal memory in each of the three classes at fixed noise and accuracy. Equal scaling classes do not imply equal exact maxima, and the lower bound is not claimed for every fixed system size.

The strengthened converse, the numerical gap in Supplemental Material Sec. III G, and the full prior-work comparison in Sec. VIII B remain as in revision 9. The main scientific argument is unchanged.

The factor-five example is explicitly restricted to the single-qubit readout of the repetition reservoir at $q=0.9$, $\varepsilon=0.01$, and odd $k=5,\ldots,15$. The [quantitative report](versions/2026-10-19-prl-v9/verification/factor-five.json) and [reproduction script](versions/2026-10-19-prl-v9/verification/check_factor_five.py) verify all five successive ratios. Table S1 continues to report half-lives; it is not relabeled as a memory-depth table.

The theorem, proofs, abstract, simulation code, and all supplied datasets are unchanged from revision 9. The two exponents still differ; the revision does not claim the exact optimal rate. Confirmed authorship, affiliation, disclosure, the GitHub code link, and the qualifications on sampled histories, independently sampled unitaries, integer depths, and finite-precision capacity are retained. See the [revision note](../docs/manuscript-2026-10-19-prl-v10.md) for the precise scope and verification.

The [cover letter PDF](submission/prl-2026-10-19-v10/cover_letter.pdf) and [TXT](submission/prl-2026-10-19-v10/cover_letter.txt) preserve the approved cover revision 2, including its original 18 October date. Referee suggestions remain separate. The [PRL justification TXT](submission/prl-2026-10-19-v10/justification.txt) retains the approved 100-word text byte for byte, including the supplied LaTeX delimiters; its frozen input is [justification-user.txt](versions/2026-10-18-prl-v5/justification-user.txt). The Figure 1 update does not replace those approved submission texts.

The canonical source combines the Letter and supplement using APS REVTeX 4.2 with `aps,prl,twocolumn`, four main figures, and seven supplemental figures. The combined manuscript has 25 pages (6 Letter + 19 supplement). The unchanged plain-text abstract has 595 characters, and the local APS-method length estimate is 3747 word equivalents (2804 text + 96 equations + 847.4076 figure equivalents before rounding). Page counts and build/package checks are recorded in the [revision note](../docs/manuscript-2026-10-19-prl-v10.md) and [PRL build verification](submission/prl-2026-10-19-v10/build_verification.json). Local length estimates are not an APS editorial eligibility decision.

Build the combined manuscript from the repository root (TeX Live with REVTeX 4.2, pdfLaTeX, BibTeX, and orcidlink):

```bash
latexmk -cd -pdf -interaction=nonstopmode -halt-on-error \
  -outdir=../../work/manuscript-build-2026-10-19-prl-v10 paper/prl-source/memory_limits_prl.tex
```

A matching BBL is included. Reference [28] identifies the source archive, the GitHub repository, and references cited only in the supplement. No shell escape is needed to compile from bundled figure PDFs. Rerunning simulations needs NumPy and SciPy; the constants checker additionally needs mpmath. Rebuilding figures also needs matplotlib, LaTeX, TikZ, and the fonts listed in [prl-source/README.txt](prl-source/README.txt).

All eight simulator Python files and all 13 supplied JSON datasets are unchanged from the preceding edition. The revision-3 repetition-curve replay remains historical evidence: full-state depth 316 and single-qubit depth 309, with full-state agreement exact and single-qubit agreement within `1.11e-16`. The large campaign was not rerun for this update. Current verification is recorded separately; finite checks and sampled proof diagnostics do not certify the universal theorem.

The AI disclosure names Claude Opus 5.5 and attributes review and responsibility to Markus Baumann. Automated checks do not independently establish those human attestations.

Revision 10 is a **local preparation**, not an upload or submission. GitHub remains **private**. No new PRL, arXiv, or Zenodo portal action accompanies this update. The local Zenodo draft leaves license, access right, publication date, and DOI unset; the supplied CC BY 4.0/open-access proposal remains unselected. The earlier arXiv draft is described below as a historical observation.

## Previous PRL revision 9: 19 October 2026

The [25-page PDF](memory_limits_prl_2026-10-19-v9.pdf), [provenance](versions/2026-10-19-prl-v9/provenance.json), [source snapshot](versions/2026-10-19-prl-v9/source-final-prl-v9.zip), [PRL package](submission/prl-2026-10-19-v9/README.md), [arXiv source ZIP](submission/arxiv-2026-10-19-v9/arxiv-source.zip), [Zenodo draft](submission/zenodo-2026-10-19-v9/README.md), and [revision record](../docs/manuscript-2026-10-19-prl-v9.md) remain unchanged. Revision 9 restructured the main-text explanation, moved the numerical bound gap to the supplement, and reduced Figure 1 to two panels. Its finite-range factor-five calculation remains available as a [report](versions/2026-10-19-prl-v9/verification/factor-five.json) and [reproduction script](versions/2026-10-19-prl-v9/verification/check_factor_five.py). Its 6-page Letter, 19-page supplement, and 3705-word-equivalent estimate belong to that edition. Its packages were prepared locally, without replacing the previously uploaded revision-7 arXiv draft.

## Previous PRL revision 8: 19 October 2026

The [25-page PDF](memory_limits_prl_2026-10-19-v8.pdf), [received inputs and receipt](versions/2026-10-19-prl-v8/receipt.json), [provenance](versions/2026-10-19-prl-v8/provenance.json), [source snapshot](versions/2026-10-19-prl-v8/source-final-prl-v8.zip), [PRL package](submission/prl-2026-10-19-v8/README.md), [arXiv source ZIP](submission/arxiv-2026-10-19-v8/arxiv-source.zip), [Zenodo draft](submission/zenodo-2026-10-19-v8/README.md), and [revision record](../docs/manuscript-2026-10-19-prl-v8.md) remain unchanged. Revision 8 incorporated the new supplied manuscript and figures, expanded the discussion of prior work, and retained the approved cover letter and justification. Its 6-page Letter, 19-page supplement, 595-character abstract, and 3732-word-equivalent estimate belong to that edition. Its packages were prepared locally, without replacing the previously uploaded revision-7 arXiv draft.

## Previous PRL revision 7: 18 October 2026

The [24-page PDF](memory_limits_prl_2026-10-18-v7.pdf), [provenance](versions/2026-10-18-prl-v7/provenance.json), [source snapshot](versions/2026-10-18-prl-v7/source-final-prl-v7.zip), [PRL package with cover revision 2](submission/prl-2026-10-18-v7-cover-v2/README.md), [arXiv source ZIP](submission/arxiv-2026-10-18-v7/arxiv-source.zip), [Zenodo draft](submission/zenodo-2026-10-18-v7/README.md), and [revision record](../docs/manuscript-2026-10-18-prl-v7.md) remain preserved. Revision 7 shortened the shared affiliation to QAR-Lab and LMU while retaining the address. Scientific content and the AI disclosure were unchanged from revision 6.

On 18 October 2026, revision 7 was last observed in arXiv draft **8248308** with saved metadata and a **SUCCEEDED** 24-page portal compilation. The user selected arXiv's non-exclusive distribution license; the final **Submit** action was left open. The [upload record and portal-generated PDF](submission-records/arxiv-2026-10-18-v7/README.md) preserve that historical state, which does not establish the portal's current status. The draft number is not a public arXiv identifier. Revision 8 has not replaced that uploaded source in the portal. Historical packages and administrative drafts remain unchanged.

## Previous PRL revision 6: 18 October 2026

The [24-page PDF](memory_limits_prl_2026-10-18-v6.pdf), [provenance](versions/2026-10-18-prl-v6/provenance.json), [source snapshot](versions/2026-10-18-prl-v6/source-final-prl-v6.zip), [PRL package](submission/prl-2026-10-18-v6/README.md), [arXiv source ZIP](submission/arxiv-2026-10-18-v6/arxiv-source.zip), [Zenodo draft](submission/zenodo-2026-10-18-v6/README.md), and [revision record](../docs/manuscript-2026-10-18-prl-v6.md) remain preserved. Revision 6 changed only the manuscript's two AI-disclosure paragraphs following the author's clarification that GPT assistance was limited to language and formatting. Scientific content, figures, simulation code, and data remained unchanged from revision 5. Its build and package checks remain evidence for that edition; revision 7 changes only affiliation information.

## Previous PRL revision 5: 18 October 2026

The [24-page PDF](memory_limits_prl_2026-10-18-v5.pdf), [received originals and receipt](versions/2026-10-18-prl-v5/receipt.json), [provenance](versions/2026-10-18-prl-v5/provenance.json), [source snapshot](versions/2026-10-18-prl-v5/source-final-prl-v5.zip), [PRL package](submission/prl-2026-10-18-v5/README.md), [arXiv source ZIP](submission/arxiv-2026-10-18-v5/arxiv-source.zip), [Zenodo draft](submission/zenodo-2026-10-18-v5/README.md), and [revision record](../docs/manuscript-2026-10-18-prl-v5.md) remain preserved. This edition imported the five supplied source, PDF, submission, and Zenodo files; it introduced Latin Modern typography, revised figures, and expanded memory-capacity and finite-precision discussions. Its 22-test pass, 3688-word-equivalent local estimate, 588-character abstract, and 24-page visual review remain historical checks of revision 5. Revision 6 changes only the two disclosure paragraphs in its manuscript source.

## Previous PRL revision 4: 18 October 2026

The [22-page PDF](memory_limits_prl_2026-10-18-v4.pdf), [provenance](versions/2026-10-18-prl-v4/provenance.json), [PRL package](submission/prl-2026-10-18-v4/README.md), [arXiv source ZIP](submission/arxiv-2026-10-18-v4/arxiv-source.zip), and [revision record](../docs/manuscript-2026-10-18-prl-v4.md) remain preserved. The [second justification update](versions/2026-10-18-prl-v4/justification-update-v2.json), its [exact input](versions/2026-10-18-prl-v4/justification-user-v2.txt), and [frozen source snapshot](versions/2026-10-18-prl-v4/source-final-prl-v4-justification-v2.zip) remain part of that edition. Its 22-test pass, 3654-word local estimate, 575-character abstract, and 22-page visual review are historical checks of revision 4.

## Previous PRL revision 3: 18 October 2026

The [22-page PDF](memory_limits_prl_2026-10-18-v3.pdf), [provenance](versions/2026-10-18-prl-v3/provenance.json), [PRL package](submission/prl-2026-10-18-v3/README.md), [arXiv source ZIP](submission/arxiv-2026-10-18-v3/arxiv-source.zip), and [revision record](../docs/manuscript-2026-10-18-prl-v3.md) are preserved unchanged. This edition imported proof and precision corrections, updated references and figures, and the 309-step single-qubit depth. It introduced the finite-history estimator, independent unitary sampling across `k`, and continuous-versus-integer threshold clarifications retained in revision 4. Its recorded 22-test pass, isolated repetition replay, 3580-word estimate, and 590-character abstract belong to that edition.

## Previous PRL revision 2: 18 October 2026

The [22-page PDF](memory_limits_prl_2026-10-18.pdf), [provenance](versions/2026-10-18-prl-v2/provenance.json), [arXiv source ZIP](submission/arxiv-2026-10-18/arxiv-source.zip), and [revision record](../docs/manuscript-2026-10-18-prl.md) are preserved unchanged. This edition combined the repeated affiliation address and added the GitHub URL to reference [28] and the code/data information. It preserved the scientific content and datasets imported on 17 October. Its three recorded numerical presentation qualifications are addressed in revision 3; its archived notes still describe the checks and limitations of that earlier edition.

## Previous PRL revision 1: 17 October 2026

The [22-page PDF](memory_limits_prl_2026-10-17.pdf), [received inputs and provenance](versions/2026-10-17-prl-v1/provenance.json), [arXiv source ZIP](submission/arxiv-2026-10-17/arxiv-source.zip), and [import/check record](../docs/manuscript-2026-10-17-prl.md) are preserved unchanged. That edition imported `memory_limits_prl_source (1).zip`, `memory_limits_prl (4).tex`, `memory_limits_prl (16).pdf`, and `fig4.pdf`; the standalone TeX and Figure 4 matched their ZIP counterparts byte for byte. It restored the confirmed three authors and ORCIDs, with two affiliation blocks sharing the same street address.

The supplied scientific revision introduced the current title and abstract, improved upper-bound constants, reorganized proofs, and new numerical campaigns. Its import record reports the checks performed on 17 October, including the bounded twelve-realization replay, 22 repository tests, and a fresh-package build. These remain historical evidence for the unchanged scientific sources; they are not relabeled as new checks for revision 2. The archived edition and its package were not uploaded or submitted.

## Previous revision 5: 16 October 2026

The [21-page PDF](memory_limits_2026-10-16-v5.pdf), [source tree](source/memory_limits.tex), [received inputs/provenance](versions/2026-10-16-v5/provenance.json), [revision record](../docs/manuscript-2026-10-16-v5.md), and [PRA template audit](../docs/pra-template-check-2026-10-16-v5.md) are preserved. The historical title is **The Memory Limits of Noisy Quantum Reservoirs**. Its full PRA-style manuscript expanded proof explanations and retained revision 4's simulator and datasets. `paper/source/` remains unchanged because independent historical experiments import its simulator; current manuscript development uses `paper/prl-source/`.

## Previous revision 4: 16 October 2026

The [17-page PDF](memory_limits_2026-10-16-v4.pdf), [final source snapshot](versions/2026-10-16-v4/source-final-v4.zip), [original inputs/provenance](versions/2026-10-16-v4/provenance.json), and [historical check record](../docs/manuscript-2026-10-16-v4.md) are preserved. Its received source introduced the supplied numerical campaigns, datasets and eight-figure layout.

## Previous revision 3: 16 October 2026

The [12-page PDF](memory_limits_2026-10-16.pdf), [final source snapshot](versions/2026-10-16/source-final-v3.zip), [original inputs/provenance](versions/2026-10-16/provenance.json), and [historical scope/checks](../docs/manuscript-2026-10-16.md) are preserved. It used the approved abstract and three-author order; its source was superseded in `source/` by revision 5, whose tree is now preserved for reproducibility.

## Original version: 15 October 2026

[`fresh_qubits_pra.pdf`](fresh_qubits_pra.pdf) is the unchanged 12-page manuscript **Fresh qubits set the memory: A sharp reset–memory law and classical learning of noisy quantum reservoirs**. Its receipt details and checksum remain in [provenance.json](provenance.json). Only a PDF was supplied for that version. Historical learning claims and equation anchors in the original research notes remain tied to it.

[manuscript.bib](manuscript.bib) records draft citations without inventing acceptance, a DOI or a publication date.
