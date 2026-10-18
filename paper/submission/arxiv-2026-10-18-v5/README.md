# arXiv upload preparation — 18 October 2026, revision 5

This directory is a local preparation package. Nothing has been uploaded or
submitted; no license or submission agreement has been accepted.

## Upload and metadata

- Upload **arxiv-source.zip** as a TeX source submission. The single compilation
  target is `memory_limits_prl.tex`, using **pdfLaTeX / TeX Live 2025**.
- The manuscript contains the Letter and Supplemental Material in one document.
- `title.txt`, `authors.txt`, and `abstract.txt` are ready to paste into metadata
  fields. `abstract.txt` uses ASCII plus standard TeX mathematics.
- `author_information.json` retains the confirmed author order, affiliations,
  ORCIDs, and contact data from the earlier author record, with names and ORCIDs
  checked against this manuscript. Local historical source paths are omitted.
- Recommended primary category: **quant-ph**. No cross-list is proposed.
- `submission_metadata.json` records pending choices. Journal reference, DOI,
  and institutional report number are blank because none was established.
- The Comments field describes 24 pages and 11 figures. Final local build checks
  are recorded in `verification.json`; inspect the arXiv preview before submitting.

The user still needs to select a license, complete any account/category
endorsement required by the portal, inspect the arXiv-generated PDF, accept the
submission terms, and explicitly finalize the submission. These actions have
not been performed here. License grants for an announced version are irrevocable.

## Code link

The Supplemental Material bibliography entry and the supplemental code section link to
https://github.com/eybmits/fresh-qubits-memory. At the user's request, the repository
remains PRIVATE. Readers can use this GitHub link only after the author makes
the repository public. Code/data are also included in this arXiv source ZIP.

## Author review

The [revision review](../../../docs/manuscript-2026-10-18-prl-v5.md) records the
new source import and the applied clarifications: numerical depths are sampled
estimates, k comparisons use independently sampled unitary ensembles, and the
continuous crossings in Figure 4 differ from integer depths. The revised
manuscript now states these distinctions. Finite checks and packaging do not
certify the universal theorem. The author's supplied verification statements
remain the author's responsibility.

## What is in the ZIP

The root contains the manuscript, matched `.bbl`, `refs.bib`, and 11 final figure
PDFs. It excludes the compiled manuscript PDF, logs, caches and unrelated files.
`00README.json` specifies the sole top-level file and explicitly ignores
5 figure-construction TeX sources in `figure_sources/`. All other reproducibility
code, data and original build instructions are in `anc/reproducibility/`.
The source bytes are copied unchanged from `paper/prl-source/`.

After unpacking the COMPLETE source archive, restore the original full layout:

```sh
python3 anc/reconstruct_source.py /path/to/new-reproduction-directory
```

The destination must be new. The helper verifies every original file's SHA-256
before writing. It restores the main TeX, bibliography, final PDFs, README and
the original `figures/`, `sim/`, and `checks/` directories. Read the restored
README for figure and simulation commands. This avoids TeX files inside `anc/`
while preserving all reproducibility sources promised by the manuscript.

## Rebuild this package

From the repository root:

```sh
python3 scripts/prepare_arxiv.py
```

The generator only uses the Python standard library. ZIP entry order,
timestamps, permissions and compression level are fixed. Identical source bytes
and generator/runtime yield an identical ZIP. `package-manifest.json` records
the archive hash, every entry hash, original-to-upload paths and generator hash;
the manifest is external and does not hash itself. Fresh-unzip compilation and
scientific validation are separate checks, not implied by packaging success.

## Official guidance checked 17 October 2026

- [TeX submissions](https://info.arxiv.org/help/submit_tex.html): include figures,
  avoid build leftovers, supply a matching `.bbl` when preserving the prepared
  bibliography. Current arXiv also supports BibTeX processing. A fixed date avoids
  `\today` changing upon later rebuilds.
- [TeX Live and compilers](https://info.arxiv.org/help/faq/texlive.html): TL2025 is
  the default and TL2023 remains available. The source uses the documented older
  `array` package pin because the REVTeX/array combination failed under TL2025.
- [Source configuration](https://info.arxiv.org/help/00README.html): the documented
  JSON format supports `toplevel`, `include` and `ignore`. An explicit configuration
  is needed here to preserve figure-construction documents without compiling them.
- [Ancillary material](https://info.arxiv.org/help/ancillary_files.html): code/data
  live under root `anc/`; TeX files are kept outside it. Ancillary files accompany
  the downloadable complete article source.
- [Metadata](https://info.arxiv.org/help/prep.html): author order, ASCII/TeX fields,
  abstract limit of 1920 characters, page/figure comments, and journal/DOI fields.
- [Categories](https://arxiv.org/category_taxonomy): `quant-ph` exists; its fit is
  our recommendation based on this manuscript, not an arXiv acceptance decision.
- [Licenses](https://info.arxiv.org/help/license/index.html) and
  [endorsement](https://info.arxiv.org/help/endorsement.html): license choice and
  account/category status remain for the actual submission workflow.

Local compilation does not establish that arXiv has processed or accepted the
files. Verify the file list, single top-level target and resulting PDF in arXiv
before final submission.
