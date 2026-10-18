# Manuscript versions and source

## Current version: 18 October 2026, PRL revision 2

**The Fundamental Memory Ceiling of Noisy Quantum Reservoirs**

Markus Baumann, Jonas Stein, and Claudia Linnhoff-Popien share one combined affiliation: Quantum Applications and Research Laboratory (QAR-Lab), Chair of Mobile and Distributed Systems, Department of Computer Science, Ludwig-Maximilians-Universität München, Oettingenstraße 67, 80538 München, Germany. The shared address appears once in each of the Letter and Supplemental Material bylines. All three approved ORCID links and the campus.lmu.de contact address are retained in the [canonical author record](author_information.json).

- [Current PDF](memory_limits_prl_2026-10-18.pdf)
- [Editable LaTeX](prl-source/memory_limits_prl.tex), [bibliography](prl-source/refs.bib), [supplied build instructions](prl-source/README.txt)
- [Revision provenance](versions/2026-10-18-prl-v2/provenance.json)
- [Revision scope and checks](../docs/manuscript-2026-10-18-prl.md)
- [Prepared arXiv source ZIP](submission/arxiv-2026-10-18/arxiv-source.zip)

This edition corrects the repeated affiliation address and adds the GitHub URL to the existing Supplemental Material reference [28] and the code/data information. It keeps all 38 bibliography entries and the existing title, abstract, scientific text, figures, simulation code, and datasets. The date is fixed to October 18, 2026. The [17 October import record](../docs/manuscript-2026-10-17-prl.md) documents the supplied files and earlier scientific changes.

The manuscript is a PRL Letter followed by Supplemental Material in one file, using APS REVTeX 4.2 with `aps,prl,twocolumn`. It has four main figures and seven supplemental figures. The rebuilt edition has 22 pages (six Letter/reference pages and sixteen supplement pages); the current [verification record](submission/arxiv-2026-10-18/verification.json) records fresh build and package results. Compilation and finite numerical checks do not certify the theorem.

Build from the repository root (TeX Live with REVTeX 4.2, pdfLaTeX, BibTeX, and orcidlink):

```bash
latexmk -cd -pdf -interaction=nonstopmode -halt-on-error \
  -outdir=../../work/manuscript-build-2026-10-18-prl paper/prl-source/memory_limits_prl.tex
```

A matching BBL is included. Reference [28] identifies the included supplement/source archive and the GitHub repository. No shell escape is needed to compile the manuscript from its bundled figure PDFs. Rerunning simulations needs NumPy and SciPy, and the constants checker additionally needs mpmath. Rebuilding figures also needs matplotlib, LaTeX, TikZ, Helvetica, and cm-super; follow [prl-source/README.txt](prl-source/README.txt), then copy the generated figure PDFs to the manuscript directory before compiling.

The repository remains **private**, as explicitly requested; the user will make it public separately. The URL therefore does not yet provide public code access. The arXiv source ZIP includes code/data as ancillary material, but it has not been uploaded or submitted. License choice, account/category checks, and inspection of the arXiv-generated preview remain pending. The [current note](../docs/manuscript-2026-10-18-prl.md) retains the three scientific interpretation qualifications; technical readiness is distinct from scientific certification.

Historical [PRL administrative drafts](submission/prl-2026-10-16/README.TXT) and PRA drafts are preserved; their manuscript details and earlier length audit are historical. The supplied PRL counter reported about 3542 word equivalents during the 17 October import, not a journal eligibility decision.

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
