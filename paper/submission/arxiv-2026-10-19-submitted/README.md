# arXiv preparation — full manuscript

Edition identifier: `2026-10-19-submitted`. The full PDF contains the Letter and Supplemental
Material together (25 pages, 11 figures). The uploaded source has compiled successfully in arXiv draft **8251813**;
metadata are saved, and the final Submit action remains open. See the
[portal record](../../submission-records/arxiv-2026-10-19/README.md).

Upload `arxiv-source.zip` as a TeX source submission. The only top-level TeX compilation target is
`memory_limits_prl.tex`, with pdfLaTeX / TeX Live 2025. Paste the exact title,
authors and abstract from the matching text files. The primary category is
`quant-ph`; DOI and journal-reference fields remain blank until assigned.
`submission_metadata.json` records the saved form values and the current portal
record. The preview confirms the user-selected non-exclusive distribution license.

The scientific sources, bibliography, figure PDFs, simulator and datasets are
copied byte for byte from `paper/prl-source/`. The public reproducibility README
uses the same cleaned instructions as the PRL supplemental archive; editor-only
correspondence and submission administration are excluded. The main text,
abstract, authors, affiliation and AI disclosure are unchanged.

The ZIP contains root-level TeX, bibliography and 11 final figures. The
`00README.json` configuration ignores 5 figure-construction TeX sources in
`figure_sources/`. Code and data are under `anc/reproducibility/`. After extracting
the complete ZIP, reconstruct the source layout with:

```sh
python3 anc/reconstruct_source.py /path/to/new-reproduction-directory
```

The destination must not exist; every file is SHA-256 checked before writing.
Follow the restored README for simulation and figure reproduction instructions.
No figure-building code runs during arXiv compilation.

Rebuild from the repository root:

```sh
python3 scripts/prepare_arxiv.py --edition 2026-10-19-submitted --output-dir paper/submission/arxiv-2026-10-19-submitted --readme-file paper/submission/arxiv-2026-10-19-submitted/reproduction-readme.txt
```

`package-manifest.json` records every entry and the deterministic archive hash.
`verification.json` records the fresh extraction, compilation and comparison to
the submitted full manuscript. This package check does not certify the scientific
theorem or imply arXiv acceptance. Inspect the arXiv-generated preview separately.
