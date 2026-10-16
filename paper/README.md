# Manuscript versions and source

## Current version: 16 October 2026, revision 4

**The Memory Limits of Noisy Quantum Reservoirs**

Markus Baumann, Jonas Stein, and Claudia Linnhoff-Popien (LMU Munich)

- [Current 17-page PDF](memory_limits_2026-10-16-v4.pdf)
- [Editable LaTeX](source/memory_limits.tex), [bibliography](source/refs.bib), [source reproduction instructions](source/README.txt)
- [Received ZIP/PDF and provenance](versions/2026-10-16-v4/provenance.json)
- [Revision scope and checks](../docs/manuscript-2026-10-16-v4.md), [official PRA template audit](../docs/pra-template-check-2026-10-16.md)

This imports the newly supplied `memory_limits (5).pdf` and `memory_limits_source (1).zip`. The earlier approved title, exact abstract and three-author order are retained. The update includes eight figures, five tables, and supplied Ising/Haar and repetition-code simulations with saved datasets. Those simulations are distinct from the repository's earlier independent empirical report.

The manuscript uses the official APS REVTeX 4.2 class with `aps,pra,reprint`. All fonts in the rebuilt PDF are embedded Type 1. Three table preambles were repaired for TeX Live 2025 without changing their contents. The mathematical body is otherwise retained from the supplied revision; see the checks and remaining interpretation notes above.

Build from the repository root (TeX Live with REVTeX 4.2, pdfLaTeX and BibTeX):

```bash
latexmk -cd -pdf -interaction=nonstopmode -halt-on-error \
  -outdir=../../work/manuscript-build-2026-10-16-v4 paper/source/memory_limits.tex
(cd work/manuscript-build-2026-10-16-v4 && BIBINPUTS=../../paper/source: bibtex memory_limits)
latexmk -cd -pdf -interaction=nonstopmode -halt-on-error \
  -outdir=../../work/manuscript-build-2026-10-16-v4 paper/source/memory_limits.tex
```

The supplied BBL is included and matches BibTeX regeneration. The source ZIP prepared for APS embeds that bibliography in its upload copy; the editable source keeps BibTeX. No shell escape is needed. The current simulation supplement needs Python 3 with NumPy, SciPy and mpmath; figure generation also needs matplotlib, LaTeX, TikZ, Helvetica and cm-super. Follow [source/README.txt](source/README.txt), including the final copy step for generated figure PDFs.

The current PDF, source ZIP and complete supplement are prepared locally for a PRA Regular Article. They have not been submitted. Original PDFs and input archives remain immutable; publication metadata is not fabricated.

## Previous revision 3: 16 October 2026

The [12-page PDF](memory_limits_2026-10-16.pdf), [final source snapshot](versions/2026-10-16/source-final-v3.zip), [original inputs/provenance](versions/2026-10-16/provenance.json), and [historical scope/checks](../docs/manuscript-2026-10-16.md) are preserved. It used the approved abstract and three-author order; its source has now been superseded in `source/` by revision 4.

## Original version: 15 October 2026

[`fresh_qubits_pra.pdf`](fresh_qubits_pra.pdf) is the unchanged 12-page manuscript **Fresh qubits set the memory: A sharp reset–memory law and classical learning of noisy quantum reservoirs**. Its receipt details and checksum remain in [provenance.json](provenance.json). Only a PDF was supplied for that version. Historical learning claims and equation anchors in the original research notes remain tied to it.

[manuscript.bib](manuscript.bib) records draft citations without inventing acceptance, a DOI or a publication date.
