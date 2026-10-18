# Manuscript versions and source

## Current version: 18 October 2026, PRL revision 3

**The Fundamental Memory Ceiling of Noisy Quantum Reservoirs**

Markus Baumann, Jonas Stein, and Claudia Linnhoff-Popien share one combined affiliation: Quantum Applications and Research Laboratory (QAR-Lab), Chair of Mobile and Distributed Systems, Department of Computer Science, Ludwig-Maximilians-Universität München, Oettingenstraße 67, 80538 München, Germany. The shared address appears once in each of the Letter and Supplemental Material bylines. All three approved ORCID links and the campus.lmu.de contact address are retained in the [canonical author record](author_information.json).

- [Combined PDF](memory_limits_prl_2026-10-18-v3.pdf), [six-page Letter](submission/prl-2026-10-18-v3/memory_limits_prl_letter.pdf), [sixteen-page Supplemental Material](submission/prl-2026-10-18-v3/2_supplemental_material/memory_limits_prl_SM.pdf)
- [Editable LaTeX](prl-source/memory_limits_prl.tex), [bibliography](prl-source/refs.bib), [build instructions](prl-source/README.txt)
- [Received originals and receipt](versions/2026-10-18-prl-v3/receipt.json), [provenance](versions/2026-10-18-prl-v3/provenance.json), [final source snapshot](versions/2026-10-18-prl-v3/source-final-prl-v3.zip)
- [Revision scope and checks](../docs/manuscript-2026-10-18-prl-v3.md)
- [PRL handoff ZIP](submission/prl-2026-10-18-v3/prl-submission.zip) and [upload instructions](submission/prl-2026-10-18-v3/README.md)
- [Prepared arXiv source ZIP](submission/arxiv-2026-10-18-v3/arxiv-source.zip)

This edition imports `memory_limits_prl_submission.zip`, `memory_limits_prl_letter.pdf`, `memory_limits_prl_SM.pdf`, and `submission_notes.txt`, preserving the supplied originals. It incorporates the supplied proof and precision corrections, updated references and figures, and the 309-step single-qubit depth. The three confirmed authors, ORCIDs, one shared affiliation, and GitHub URL in reference [28] are retained. The manuscript also now explains the finite-history estimate, independent unitary sampling across `k`, and the continuous thresholds in Figure 4(b).

The canonical source combines the Letter and supplement using APS REVTeX 4.2 with `aps,prl,twocolumn`, four main figures, and seven supplemental figures. The combined PDF has 22 pages. The PRL handoff provides a separately compiled six-page Letter and a sixteen-page supplement, with matching text documented in the [PRL build verification](submission/prl-2026-10-18-v3/build_verification.json). Its source archive includes the full reproduction code and data. The final Letter has a local estimate of 3580 equivalent words against the 3750-word PRL limit; its abstract has 590 rendered characters. Neither the estimate nor compilation is an editorial eligibility decision.

Build the combined manuscript from the repository root (TeX Live with REVTeX 4.2, pdfLaTeX, BibTeX, and orcidlink):

```bash
latexmk -cd -pdf -interaction=nonstopmode -halt-on-error \
  -outdir=../../work/manuscript-build-2026-10-18-prl-v3 paper/prl-source/memory_limits_prl.tex
```

A matching BBL is included. Reference [28] identifies the supplement/source archive, the GitHub repository, and the references cited only in the supplement. No shell escape is needed to compile from the bundled figure PDFs. Rerunning simulations needs NumPy and SciPy, and the constants checker additionally needs mpmath. Rebuilding figures also needs matplotlib, LaTeX, TikZ, Helvetica, and cm-super; follow [prl-source/README.txt](prl-source/README.txt).

All 13 supplied JSON datasets remain unchanged. The 22 repository tests pass, and an isolated replay of the repetition reservoir reproduces full-state depth 316 and single-qubit depth 309. The full-state curve matches exactly and the single-qubit curve agrees within `1.11e-16`. These finite checks and the sampled proof diagnostics do not certify the universal theorem. The large campaign was not rerun for this import.

The user confirmed the disclosed model name Claude Opus 5.5 on 18 October 2026. The manuscript's supplied verification statements remain attributed to Markus Baumann; automated checks do not independently establish those human attestations.

The repository remains **private**, as explicitly requested; the user will make it public separately. Nothing has been uploaded or submitted. PRL author attestations and portal preview, arXiv license choice and preview, and any publication options remain for the actual submission. The prepared code/data archives do not depend on public GitHub access. Historical PRL and PRA administrative drafts remain preserved and are not the current upload package.

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
