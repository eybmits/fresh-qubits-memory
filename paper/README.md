# Manuscript versions and source

## Current version: 18 October 2026, PRL revision 6

**The Fundamental Memory Ceiling of Noisy Quantum Reservoirs**

Markus Baumann, Jonas Stein, and Claudia Linnhoff-Popien share one combined affiliation: Quantum Applications and Research Laboratory (QAR-Lab), Chair of Mobile and Distributed Systems, Department of Computer Science, Ludwig-Maximilians-Universität München, Oettingenstraße 67, 80538 München, Germany. The shared address appears once in each of the Letter and Supplemental Material bylines. All three approved ORCID links and the campus.lmu.de contact address are retained in the [canonical author record](author_information.json).

- [Combined PDF](memory_limits_prl_2026-10-18-v6.pdf), [Letter](submission/prl-2026-10-18-v6/memory_limits_prl_letter.pdf), [Supplemental Material](submission/prl-2026-10-18-v6/2_supplemental_material/memory_limits_prl_SM.pdf)
- [Editable LaTeX](prl-source/memory_limits_prl.tex), [bibliography](prl-source/refs.bib), [build instructions](prl-source/README.txt)
- [Received originals and receipt](versions/2026-10-18-prl-v5/receipt.json), [provenance](versions/2026-10-18-prl-v6/provenance.json), [final source snapshot](versions/2026-10-18-prl-v6/source-final-prl-v6.zip)
- [Revision scope and verification](../docs/manuscript-2026-10-18-prl-v6.md)
- [PRL handoff ZIP](submission/prl-2026-10-18-v6/prl-submission.zip) and [upload instructions](submission/prl-2026-10-18-v6/README.md)
- [Prepared arXiv source ZIP](submission/arxiv-2026-10-18-v6/arxiv-source.zip)
- [Local Zenodo handoff](submission/zenodo-2026-10-18-v6/README.md)
- [Upload guide: separate PRL PDFs, combined arXiv version, and Zenodo draft](submission/README.md)

This edition revises only the two AI-disclosure paragraphs in the manuscript after the author clarified that GPT assistance was limited to language and formatting. The revised disclosure names Claude Opus 5.5 and uses the author-approved wording about reviewing outputs. Scientific arguments, figures, simulation code, and data are unchanged from PRL revision 5. The five originals received for that edition remain preserved in its archive; revision 6 is a local revision and has no separate receipt. The retained three-author metadata, shared affiliation, and GitHub code link remain synchronized throughout. The code/supplement reference is [27].

The integration retains the numerical interpretation qualifications: sampled histories estimate the memory supremum, unitary ensembles are sampled separately across `k`, and continuous threshold crossings are rounded up for integer depths. The abstract and Figure 3 describe the optimal attainable ceiling rather than automatic memory improvement in every reservoir. The memory-capacity discussion explicitly assumes finite positive input variance; its readout-resolution range and initialization-washout statement are qualified in the source. See the [revision note](../docs/manuscript-2026-10-18-prl-v6.md) for exact scope and evidence.

The [PRL justification TXT](submission/prl-2026-10-18-v6/justification.txt) retains the latest user-approved 100-word text byte for byte, including the supplied LaTeX delimiters. Its current frozen input is [justification-user.txt](versions/2026-10-18-prl-v5/justification-user.txt); the previous two paragraphs remain in the revision 4 archive.

The canonical source combines the Letter and supplement using APS REVTeX 4.2 with `aps,prl,twocolumn`, four main figures, and seven supplemental figures. Current page counts, local length accounting, and build/package checks are recorded in the [revision note](../docs/manuscript-2026-10-18-prl-v6.md) and [PRL build verification](submission/prl-2026-10-18-v6/build_verification.json). The abstract is unchanged. Local length estimates do not constitute an APS editorial eligibility decision.

Build the combined manuscript from the repository root (TeX Live with REVTeX 4.2, pdfLaTeX, BibTeX, and orcidlink):

```bash
latexmk -cd -pdf -interaction=nonstopmode -halt-on-error \
  -outdir=../../work/manuscript-build-2026-10-18-prl-v6 paper/prl-source/memory_limits_prl.tex
```

A matching BBL is included. Reference [27] identifies the supplement/source archive, the GitHub repository, and the references cited only in the supplement. No shell escape is needed to compile from the bundled figure PDFs. Rerunning simulations needs NumPy and SciPy, and the constants checker additionally needs mpmath. Rebuilding figures also needs matplotlib, LaTeX, TikZ, and the fonts listed in [prl-source/README.txt](prl-source/README.txt).

All eight simulator Python files and all 13 supplied JSON datasets are unchanged from the preceding edition. The revision 3 repetition-curve replay remains historical evidence: full-state depth 316 and single-qubit depth 309, with full-state agreement exact and single-qubit agreement within `1.11e-16`. The large campaign was not rerun for revision 6. Finite numerical checks and sampled proof diagnostics do not certify the universal theorem.

The user confirmed the disclosed model name Claude Opus 5.5 and clarified GPT's editorial-only role on 18 October 2026. The revised disclosure statements remain attributed to Markus Baumann; automated checks do not independently establish those human attestations.

The repository remains **private**, as explicitly requested; the user will make it public separately. Nothing has been uploaded or submitted. PRL author attestations and portal preview, arXiv license choice and preview, and publication options remain for the actual submission. The local Zenodo draft has the three authors and ORCIDs but deliberately leaves license, access, publication date, and DOI unset; the supplied CC BY 4.0/open-access proposal is preserved as unselected input content. Historical PRL and PRA administrative drafts are preserved and are not the current upload package.

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
