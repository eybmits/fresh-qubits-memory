# Manuscript versions and source

## Current version: 16 October 2026

**Input Reinitialization Sets the Memory of Noisy Quantum Reservoirs**

Markus Baumann, Ludwig-Maximilians-Universität München

- [Current PDF](memory_limits_2026-10-16.pdf)
- [Editable LaTeX](source/memory_limits.tex), [bibliography](source/refs.bib), and figure assets/sources in [source/](source/)
- [Version provenance](versions/2026-10-16/provenance.json)
- [Version scope and checks](../docs/manuscript-2026-10-16.md)

This revision starts from the user-supplied `memory_limits_source.zip` and `memory_limits (1).pdf`, received on 16 October 2026. The supplied PDF and source archive are preserved byte-for-byte in [versions/2026-10-16/](versions/2026-10-16/). The working source incorporates the user's replacement abstract verbatim, a matching new title, PDF metadata, and a table-formatting compatibility repair. Its mathematical body and figure assets are otherwise retained from the supplied source.

Build from the repository root with a TeX distribution containing REVTeX 4.2, pdfLaTeX, BibTeX, and latexmk:

```bash
mkdir -p work
latexmk -cd -pdf -interaction=nonstopmode -halt-on-error \
  -outdir=../../work/manuscript-build-2026-10-16 paper/source/memory_limits.tex
```

The result is `work/manuscript-build-2026-10-16/memory_limits.pdf`. The supplied `.bbl` is committed for build systems that do not run BibTeX. To regenerate it, run BibTeX in the build directory with the source directory on `BIBINPUTS`, then rerun latexmk:

```bash
(cd work/manuscript-build-2026-10-16 && BIBINPUTS=../../paper/source: bibtex memory_limits)
latexmk -cd -pdf -interaction=nonstopmode -halt-on-error \
  -outdir=../../work/manuscript-build-2026-10-16 paper/source/memory_limits.tex
```

The tables use native paragraph columns with cell-local alignment. This avoids the `Extra \or` error caused by the supplied `array` table preambles with REVTeX 4.2f on TeX Live 2025; table contents are unchanged. No shell escape is needed. Figure PDFs are supplied; rebuilding the two plotted figures requires matplotlib, and rebuilding the schematic figure sources requires TikZ and standalone.

The supplied [numerical supplement](source/supplemental_numbers.py) requires `mpmath` (checked with version 1.3.0). This is optional and separate from the dependency-free numerical package in `src/`:

```bash
python3 -m venv work/supplement-env
work/supplement-env/bin/python -m pip install mpmath==1.3.0
work/supplement-env/bin/python paper/source/supplemental_numbers.py
```

## Original version: 15 October 2026

[`fresh_qubits_pra.pdf`](fresh_qubits_pra.pdf) remains an unchanged copy of the supplied 12-page manuscript, **Fresh qubits set the memory: A sharp reset–memory law and classical learning of noisy quantum reservoirs**. Its original checksum and receipt details remain in [`provenance.json`](provenance.json).

Only a PDF was supplied for that original version. The 16 October source package belongs to the later revision, not a recovered LaTeX source of the old PDF. Historical equation/table anchors and learning claims in the original summary and research plan remain tied to this baseline.

Neither version establishes journal acceptance, a DOI, or a confirmed publication date. The Supplemental Material bibliography entry still contains the supplied publisher-URL placeholder. [`manuscript.bib`](manuscript.bib) provides separate draft citation records for the two versions.
