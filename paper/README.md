# Manuscript versions and source

## Current version: 18 October 2026, PRL revision 4

**The Fundamental Memory Ceiling of Noisy Quantum Reservoirs**

Markus Baumann, Jonas Stein, and Claudia Linnhoff-Popien share one combined affiliation: Quantum Applications and Research Laboratory (QAR-Lab), Chair of Mobile and Distributed Systems, Department of Computer Science, Ludwig-Maximilians-Universität München, Oettingenstraße 67, 80538 München, Germany. The shared address appears once in each of the Letter and Supplemental Material bylines. All three approved ORCID links and the campus.lmu.de contact address are retained in the [canonical author record](author_information.json).

- [Combined PDF](memory_limits_prl_2026-10-18-v4.pdf), [six-page Letter](submission/prl-2026-10-18-v4/memory_limits_prl_letter.pdf), [sixteen-page Supplemental Material](submission/prl-2026-10-18-v4/2_supplemental_material/memory_limits_prl_SM.pdf)
- [Editable LaTeX](prl-source/memory_limits_prl.tex), [bibliography](prl-source/refs.bib), [build instructions](prl-source/README.txt)
- [Received originals and receipt](versions/2026-10-18-prl-v4/receipt.json), [provenance](versions/2026-10-18-prl-v4/provenance.json), [final source snapshot](versions/2026-10-18-prl-v4/source-final-prl-v4.zip)
- [Revision scope and checks](../docs/manuscript-2026-10-18-prl-v4.md)
- [PRL handoff ZIP](submission/prl-2026-10-18-v4/prl-submission.zip) and [upload instructions](submission/prl-2026-10-18-v4/README.md)
- [Prepared arXiv source ZIP](submission/arxiv-2026-10-18-v4/arxiv-source.zip)
- [Upload guide: separate PRL PDFs and combined arXiv version](submission/README.md)

This edition imports `memory_limits_prl_submission (1).zip`, `memory_limits_prl_source (3).zip`, `memory_limits_prl (6).tex`, `fig3 (1).pdf`, and `memory_limits_prl (28).pdf`, preserving all five supplied originals. The two full-source archives have the same 53 files; the standalone TeX and Figure 3 match their archived counterparts byte for byte. It incorporates the new abstract, Figures 1, 3, and S2, and the singular-value clarification of normalized Schatten norms. The abstract and Figure 3 are qualified to describe the optimal memory ceiling. The three confirmed authors, ORCIDs, one shared affiliation, and GitHub URL in reference [28] are retained, as are the finite-history, independent-ensemble, and continuous-crossing clarifications.

The [PRL justification TXT](submission/prl-2026-10-18-v4/justification.txt) preserves the user's exact new 100-word text. Its immutable received copy is [justification-user.txt](versions/2026-10-18-prl-v4/justification-user.txt).

The canonical source combines the Letter and supplement using APS REVTeX 4.2 with `aps,prl,twocolumn`, four main figures, and seven supplemental figures. The combined PDF has 22 pages. The PRL handoff provides a separately compiled six-page Letter and a sixteen-page supplement, with matching text documented in the [PRL build verification](submission/prl-2026-10-18-v4/build_verification.json). Its source archive includes the full reproduction code and data. The final Letter has a local estimate of 3654 equivalent words against the 3750-word PRL limit; its abstract has 575 rendered characters. Neither the estimate nor compilation is an editorial eligibility decision.

Build the combined manuscript from the repository root (TeX Live with REVTeX 4.2, pdfLaTeX, BibTeX, and orcidlink):

```bash
latexmk -cd -pdf -interaction=nonstopmode -halt-on-error \
  -outdir=../../work/manuscript-build-2026-10-18-prl-v4 paper/prl-source/memory_limits_prl.tex
```

A matching BBL is included. Reference [28] identifies the supplement/source archive, the GitHub repository, and the references cited only in the supplement. No shell escape is needed to compile from the bundled figure PDFs. Rerunning simulations needs NumPy and SciPy, and the constants checker additionally needs mpmath. Rebuilding figures also needs matplotlib, LaTeX, TikZ, Helvetica, and cm-super; follow [prl-source/README.txt](prl-source/README.txt).

The simulator and all 13 supplied JSON datasets are unchanged from revision 3. Its isolated repetition-curve replay reproduced full-state depth 316 and single-qubit depth 309, with full-state agreement exact and single-qubit agreement within `1.11e-16`. These remain historical checks; the large campaign was not rerun for revision 4. The canonical combined PDF compiles without unresolved citations or references, multiply defined labels, or overfull boxes, and all 22 repository tests pass. The separate PRL Letter and SM text match the combined PDF, and a fresh arXiv source extraction compiles to the same text. Source reconstruction and deterministic package checks pass. All 22 combined-document pages pass visual review, and the separate PDFs retain the corresponding text and layouts. See the [revision note](../docs/manuscript-2026-10-18-prl-v4.md) for the checks and their scope. Finite checks and sampled proof diagnostics do not certify the universal theorem.

The user confirmed the disclosed model name Claude Opus 5.5 on 18 October 2026. The manuscript's supplied verification statements remain attributed to Markus Baumann; automated checks do not independently establish those human attestations.

The repository remains **private**, as explicitly requested; the user will make it public separately. Nothing has been uploaded or submitted. PRL author attestations and portal preview, arXiv license choice and preview, and any publication options remain for the actual submission. The prepared code/data archives do not depend on public GitHub access. Historical PRL and PRA administrative drafts remain preserved and are not the current upload package.

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
