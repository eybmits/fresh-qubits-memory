# Manuscript versions and source

## Current version: 16 October 2026, revision 5

**The Memory Limits of Noisy Quantum Reservoirs**

Markus Baumann, Jonas Stein, and Claudia Linnhoff-Popien, each affiliated with QAR-Lab and the Chair of Mobile and Distributed Systems, Department of Computer Science, LMU Munich. The PDF includes all three ORCID links.

- [Current 21-page PDF](memory_limits_2026-10-16-v5.pdf)
- [Editable LaTeX](source/memory_limits.tex), [bibliography](source/refs.bib), [build instructions](source/README.txt)
- [Received ZIP/PDF and provenance](versions/2026-10-16-v5/provenance.json)
- [Revision scope and checks](../docs/manuscript-2026-10-16-v5.md), [PRA format and PRL length audit](../docs/pra-template-check-2026-10-16-v5.md)

Imported from `memory_limits (9).pdf` and `memory_limits_source (2).zip`. The title and approved abstract are unchanged. The main changes are expanded proof explanations, a constants glossary, and consistent evolution-time notation. The simulator, saved datasets and bibliography are unchanged from revision 4. Four local wording distinctions were clarified without changing equations; all transformations are recorded in the provenance.

This is the full manuscript in official APS REVTeX 4.2 with `aps,pra,reprint`. It has eight figures and six tables. Four paragraph-column table preambles were normalized for the installed REVTeX/array incompatibility without changing cell content, apart from the separately documented wording clarifications.

Build from the repository root (TeX Live with REVTeX 4.2, pdfLaTeX, BibTeX and orcidlink):

```bash
latexmk -cd -pdf -interaction=nonstopmode -halt-on-error \
  -outdir=../../work/manuscript-build-2026-10-16-v5 paper/source/memory_limits.tex
(cd work/manuscript-build-2026-10-16-v5 && BIBINPUTS=../../paper/source: bibtex memory_limits)
latexmk -cd -pdf -interaction=nonstopmode -halt-on-error \
  -outdir=../../work/manuscript-build-2026-10-16-v5 paper/source/memory_limits.tex
```

The supplied BBL matches BibTeX regeneration. The separately prepared APS source ZIP embeds that bibliography; editable source keeps BibTeX. No shell escape is needed. The simulation supplement uses NumPy and SciPy; figure generation additionally needs matplotlib, LaTeX, TikZ, Helvetica and cm-super. Follow the final figure-copy step in [source/README.txt](source/README.txt).

An unsubmitted PRL Letter draft has been started, but the current full manuscript exceeds PRL's 3750-word-equivalent core limit. A separate short Letter is still required. [PRL administrative drafts](submission/prl-2026-10-16/README.TXT) record its status and the 100-word justification. The earlier PRA draft is also unsubmitted. No manuscript has been uploaded, no fees or agreements accepted, and no journal acceptance is implied.

## Previous revision 4: 16 October 2026

The [17-page PDF](memory_limits_2026-10-16-v4.pdf), [final source snapshot](versions/2026-10-16-v4/source-final-v4.zip), [original inputs/provenance](versions/2026-10-16-v4/provenance.json), and [historical check record](../docs/manuscript-2026-10-16-v4.md) are preserved. Its received source introduced the supplied numerical campaigns, datasets and eight-figure layout.

## Previous revision 3: 16 October 2026

The [12-page PDF](memory_limits_2026-10-16.pdf), [final source snapshot](versions/2026-10-16/source-final-v3.zip), [original inputs/provenance](versions/2026-10-16/provenance.json), and [historical scope/checks](../docs/manuscript-2026-10-16.md) are preserved. It used the approved abstract and three-author order; its source has now been superseded in `source/` by revision 5.

## Original version: 15 October 2026

[`fresh_qubits_pra.pdf`](fresh_qubits_pra.pdf) is the unchanged 12-page manuscript **Fresh qubits set the memory: A sharp reset–memory law and classical learning of noisy quantum reservoirs**. Its receipt details and checksum remain in [provenance.json](provenance.json). Only a PDF was supplied for that version. Historical learning claims and equation anchors in the original research notes remain tied to it.

[manuscript.bib](manuscript.bib) records draft citations without inventing acceptance, a DOI or a publication date.
