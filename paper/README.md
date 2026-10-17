# Manuscript versions and source

## Current version: 17 October 2026, PRL revision

**The Fundamental Memory Ceiling of Noisy Quantum Reservoirs**

Markus Baumann, Jonas Stein, and Claudia Linnhoff-Popien, each affiliated with QAR-Lab and the Chair of Mobile and Distributed Systems, Department of Computer Science, LMU Munich. The working manuscript retains all three approved ORCID links and the campus.lmu.de contact address.

- [Current 22-page PDF](memory_limits_prl_2026-10-17.pdf)
- [Editable LaTeX](prl-source/memory_limits_prl.tex), [bibliography](prl-source/refs.bib), [supplied build instructions](prl-source/README.txt)
- [Received inputs and provenance](versions/2026-10-17-prl-v1/provenance.json)
- [Revision scope and checks](../docs/manuscript-2026-10-17-prl.md)
- [Prepared arXiv source ZIP](submission/arxiv-2026-10-17/arxiv-source.zip)

Imported from `memory_limits_prl_source (1).zip`, `memory_limits_prl (4).tex`, `memory_limits_prl (16).pdf`, and `fig4.pdf`. The standalone TeX and Figure 4 are byte-identical to their ZIP counterparts. The original inputs are preserved; the active edition integrates the author metadata confirmed by the user. It uses the new supplied title and abstract.

This version is a PRL Letter followed by Supplemental Material in one file, using official APS REVTeX 4.2 with `aps,prl,twocolumn`. It has four main figures and seven supplemental figures. It changes the upper-bound constants, proof exposition, and numerical campaigns. The import record separates these supplied scientific changes from local metadata and build adjustments; finite checks do not certify the theorem.

Build from the repository root (TeX Live with REVTeX 4.2, pdfLaTeX, BibTeX, and orcidlink):

```bash
latexmk -cd -pdf -interaction=nonstopmode -halt-on-error \
  -outdir=../../work/manuscript-build-2026-10-17-prl paper/prl-source/memory_limits_prl.tex
```

The matching BBL is included and matches BibTeX regeneration byte for byte. Its supplemental-material entry points to the included supplement/source archive, replacing the received publisher-URL placeholder. The integrated PDF has six pages of Letter/references and sixteen pages of Supplemental Material. No shell escape is needed to compile the manuscript from its bundled figure PDFs. Rerunning simulations needs NumPy and SciPy, and the constants checker additionally needs mpmath. Rebuilding figures also needs matplotlib, LaTeX, TikZ, Helvetica, and cm-super; follow [prl-source/README.txt](prl-source/README.txt), then copy the generated figure PDFs to the manuscript directory before compiling.

The arXiv package is prepared for review and upload. No arXiv identifier, acceptance, or completed submission is implied. Historical [PRL administrative drafts](submission/prl-2026-10-16/README.TXT) and PRA drafts are preserved; their manuscript details and earlier length audit are historical. The supplied PRL counter reports about 3542 word equivalents for this Letter, not a journal eligibility decision.

## Previous revision 5: 16 October 2026

The [21-page PDF](memory_limits_2026-10-16-v5.pdf), [source tree](source/memory_limits.tex), [received inputs/provenance](versions/2026-10-16-v5/provenance.json), [revision record](../docs/manuscript-2026-10-16-v5.md), and [PRA template audit](../docs/pra-template-check-2026-10-16-v5.md) are preserved. The historical title is **The Memory Limits of Noisy Quantum Reservoirs**. Its full PRA-style manuscript expanded proof explanations and retained revision 4's simulator and datasets. `paper/source/` remains unchanged because independent historical experiments import its simulator; current manuscript development uses `paper/prl-source/`.

## Previous revision 4: 16 October 2026

The [17-page PDF](memory_limits_2026-10-16-v4.pdf), [final source snapshot](versions/2026-10-16-v4/source-final-v4.zip), [original inputs/provenance](versions/2026-10-16-v4/provenance.json), and [historical check record](../docs/manuscript-2026-10-16-v4.md) are preserved. Its received source introduced the supplied numerical campaigns, datasets and eight-figure layout.

## Previous revision 3: 16 October 2026

The [12-page PDF](memory_limits_2026-10-16.pdf), [final source snapshot](versions/2026-10-16/source-final-v3.zip), [original inputs/provenance](versions/2026-10-16/provenance.json), and [historical scope/checks](../docs/manuscript-2026-10-16.md) are preserved. It used the approved abstract and three-author order; its source was superseded in `source/` by revision 5, whose tree is now preserved for reproducibility.

## Original version: 15 October 2026

[`fresh_qubits_pra.pdf`](fresh_qubits_pra.pdf) is the unchanged 12-page manuscript **Fresh qubits set the memory: A sharp reset–memory law and classical learning of noisy quantum reservoirs**. Its receipt details and checksum remain in [provenance.json](provenance.json). Only a PDF was supplied for that version. Historical learning claims and equation anchors in the original research notes remain tied to it.

[manuscript.bib](manuscript.bib) records draft citations without inventing acceptance, a DOI or a publication date.
