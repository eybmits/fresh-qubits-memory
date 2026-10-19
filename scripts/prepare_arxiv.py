#!/usr/bin/env python3
"""Build a deterministic arXiv source package without changing the manuscript.

Run from any directory. Only Python's standard library is required. This creates
local files; it does not log in, upload, select a license, or submit to arXiv.
"""

import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath
import re
import zipfile


REPO = Path(__file__).resolve().parents[1]
MAIN = "memory_limits_prl.tex"
EDITION = "2026-10-19-prl-v8"
EDITION_DATE = "2026-10-19"
EXPECTED_COMBINED_PAGES = 25
ZIP_DATE = (2026, 10, 19, 0, 0, 0)
FINAL_FIGURES = [f"fig{i}.pdf" for i in range(1, 5)] + [
    f"figS{i}.pdf" for i in range(1, 8)
]
ROOT_FILES = [MAIN, "memory_limits_prl.bbl", "refs.bib", *FINAL_FIGURES]
OFFICIAL_SOURCES = {
    "tex_submission": "https://info.arxiv.org/help/submit_tex.html",
    "texlive": "https://info.arxiv.org/help/faq/texlive.html",
    "source_configuration": "https://info.arxiv.org/help/00README.html",
    "ancillary_files": "https://info.arxiv.org/help/ancillary_files.html",
    "metadata": "https://info.arxiv.org/help/prep.html",
    "categories": "https://arxiv.org/category_taxonomy",
    "licenses": "https://info.arxiv.org/help/license/index.html",
    "endorsement": "https://info.arxiv.org/help/endorsement.html",
}


def digest(data):
    return hashlib.sha256(data).hexdigest()


def json_bytes(value):
    return (json.dumps(value, indent=2, ensure_ascii=False, sort_keys=True) + "\n").encode()


def braced_arguments(text, command):
    """Read balanced arguments, including nested ORCID commands in author names."""
    result = []
    for match in re.finditer(r"\\" + re.escape(command) + r"\s*\{", text):
        start = match.end()
        depth = 1
        position = start
        while depth and position < len(text):
            char = text[position]
            if char in "{}" and (position == 0 or text[position - 1] != "\\"):
                depth += 1 if char == "{" else -1
            position += 1
        if depth:
            raise ValueError(f"Unbalanced {command} argument")
        result.append(text[start:position - 1])
    return result


def source_files(source):
    selected = {name: source / name for name in ROOT_FILES}
    selected["README.txt"] = source / "README.txt"
    allowed = {
        "sim": {".py", ".json", ".sh"},
        "checks": {".py"},
        "figures": {".py", ".pdf", ".tex"},
    }
    for directory, extensions in allowed.items():
        for path in sorted((source / directory).rglob("*")):
            if not path.is_file() or path.suffix not in extensions:
                continue
            if any(part.startswith(".") or part == "__pycache__" for part in path.parts):
                continue
            selected[path.relative_to(source).as_posix()] = path
    for name, path in selected.items():
        if not path.is_file() or path.is_symlink():
            raise ValueError(f"Required regular source file missing: {name}")
    return {name: path.read_bytes() for name, path in sorted(selected.items())}


def payload_path(original):
    if original in ROOT_FILES:
        return original
    if original.startswith("figures/") and original.endswith(".tex"):
        return "figure_sources/" + PurePosixPath(original).name
    return "anc/reproducibility/" + original


def reconstruction_script(mapping):
    header = '''#!/usr/bin/env python3
"""Restore the original complete source layout from the unpacked arXiv archive.

Usage: python3 anc/reconstruct_source.py /path/to/NEW-output-directory
The destination must not exist. All source hashes are checked before writing.
"""
import argparse
import hashlib
import json
from pathlib import Path

FILES = json.loads(r''' + "'''" + json.dumps(mapping, sort_keys=True) + "''')\n"
    body = '''

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output_directory", type=Path)
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    destination = args.output_directory.resolve()
    if destination.exists():
        parser.error("The output directory already exists; choose a new directory.")
    verified = {}
    for original, record in FILES.items():
        path = root / record["archive_path"]
        if not path.is_file():
            parser.error("Download and unpack the complete article source first: missing "
                         + record["archive_path"])
        data = path.read_bytes()
        if hashlib.sha256(data).hexdigest() != record["sha256"]:
            parser.error("Source checksum mismatch: " + record["archive_path"])
        verified[original] = data
    destination.mkdir(parents=True)
    for original, data in verified.items():
        output = destination / original
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_bytes(data)
        output.chmod(0o755 if output.suffix == ".sh" else 0o644)
    print(f"Restored and hash-verified {len(verified)} source files to {destination}")


if __name__ == "__main__":
    main()
'''
    return (header + body).encode()


def validate_package(files, config, original_files):
    """Validate the used subset of arXiv's documented source configuration."""
    if config["spec_version"] != 1 or config["texlive_version"] not in (2023, 2025):
        raise ValueError("Unsupported arXiv specification or TeX Live version")
    if config["process"] != {"compiler": "pdflatex"}:
        raise ValueError("This package requires pdfLaTeX")
    top_levels = []
    ignored = set()
    for record in config["sources"]:
        if set(record) != {"filename", "usage"}:
            raise ValueError("Unsupported source configuration fields")
        if record["usage"] not in ("toplevel", "include", "ignore"):
            raise ValueError("Unsupported source usage")
        if record["filename"] not in files:
            raise ValueError("Source configuration refers to a missing file")
        if record["usage"] == "toplevel":
            top_levels.append(record["filename"])
        if record["usage"] == "ignore":
            ignored.add(record["filename"])
    if top_levels != [MAIN]:
        raise ValueError("Exactly the main manuscript must be compiled")
    for name, data in files.items():
        path = PurePosixPath(name)
        if path.is_absolute() or ".." in path.parts or any(p.startswith(".") for p in path.parts):
            raise ValueError(f"Unsafe archive path: {name}")
        if name.startswith("anc/") and path.suffix == ".tex":
            raise ValueError("TeX files must remain outside the ancillary directory")
        if path.suffix == ".tex" and name != MAIN and name not in ignored:
            raise ValueError(f"Auxiliary TeX source is not explicitly ignored: {name}")
        if path.suffix == ".pdf" and not data.startswith(b"%PDF-"):
            raise ValueError(f"Invalid PDF header: {name}")
    manuscript = original_files[MAIN].decode()
    included = re.findall(r"\\includegraphics(?:\[[^\]]*\])?\{([^}]+)\}", manuscript)
    if set(included) != set(FINAL_FIGURES):
        raise ValueError("The final figure list changed; review packaging selection")
    for name in included:
        if name not in files:
            raise ValueError(f"Missing final figure: {name}")
    if "\\begin{thebibliography}" not in original_files["memory_limits_prl.bbl"].decode():
        raise ValueError("The matching BibTeX bibliography is missing or invalid")


def author_metadata(source_text, author_path):
    previous = json.loads(author_path.read_text())
    authors = []
    manuscript_names = []
    manuscript_orcids = []
    for argument in braced_arguments(source_text, "author"):
        identifiers = braced_arguments(argument, "orcidlink")
        manuscript_orcids.extend(identifiers)
        name = re.sub(r"\\orcidlink\{[^}]+\}", "", argument).replace(r"\,", "").strip()
        manuscript_names.append(name)
    for record in previous["authors"]:
        author = {key: record[key] for key in ("given", "family", "orcid", "affiliation_ids")}
        author["corresponding"] = record.get("corresponding", False)
        author["email"] = record.get("email", record.get("email_from_manuscript"))
        author["orcid_authenticated_in_arxiv"] = None
        authors.append(author)
    if manuscript_names != [a["given"] + " " + a["family"] for a in authors]:
        raise ValueError("Manuscript authors do not match the confirmed author metadata")
    if manuscript_orcids != [a["orcid"] for a in authors]:
        raise ValueError("Manuscript ORCIDs do not match the confirmed author metadata")
    return {
        "authors": authors,
        "affiliations": previous["affiliations"],
        "metadata_source": "paper/author_information.json",
        "verification": "Names and ORCID order matched to the current manuscript; portal authentication was not performed.",
    }


def build(source, output, author_path):
    originals = source_files(source)
    manuscript = originals[MAIN].decode()
    title = braced_arguments(manuscript, "title")[0]
    abstract = re.search(r"\\begin\{abstract\}(.*?)\\end\{abstract\}", manuscript, re.S).group(1)
    abstract = " ".join(abstract.split())
    if not title.isascii() or not abstract.isascii() or len(abstract) > 1920:
        raise ValueError("Title/abstract violate the selected arXiv metadata format")
    authors = author_metadata(manuscript, author_path)
    files = {payload_path(name): data for name, data in originals.items()}
    mapping = {
        name: {"archive_path": payload_path(name), "sha256": digest(data), "bytes": len(data)}
        for name, data in originals.items()
    }
    config = {
        "spec_version": 1,
        "texlive_version": 2025,
        "process": {"compiler": "pdflatex"},
        "sources": [{"filename": MAIN, "usage": "toplevel"}] + [
            {"filename": name, "usage": "ignore"}
            for name in sorted(files) if name.startswith("figure_sources/")
        ],
    }
    files["00README.json"] = json_bytes(config)
    files["anc/reconstruct_source.py"] = reconstruction_script(mapping)
    figure_tex_count = sum(name.startswith("figure_sources/") and name.endswith(".tex")
                           for name in files)
    files["anc/README.txt"] = (
        "Reproducibility material for " + title + "\n\n"
        "Download and unpack the COMPLETE arXiv source archive, then run:\n"
        "  python3 anc/reconstruct_source.py /path/to/new-reproduction-directory\n\n"
        "The destination must not exist. The helper verifies SHA-256 hashes and\n"
        "restores the original complete layout: manuscript, bibliography, final\n"
        "figure PDFs, README, figures/, sim/, and checks/. No scientific source\n"
        "or data bytes are changed. Follow README.txt in the restored directory.\n\n"
        f"The {figure_tex_count} figure-construction .tex sources are in figure_sources/ outside anc/, because\n"
        "arXiv recommends excluding TeX files from ancillary directories. They\n"
        "are explicitly ignored during manuscript compilation in 00README.json.\n"
        "Only memory_limits_prl.tex is a top-level compilation target; it uses\n"
        "the final root-level figure PDFs and includes the Supplemental Material.\n\n"
        "Reproduction dependencies: Python 3, numpy, scipy, mpmath, matplotlib;\n"
        "pdfLaTeX/BibTeX and the figure font packages stated in the original README.\n"
        "No code is run by arXiv to recreate the figures.\n"
    ).encode()
    validate_package(files, config, originals)
    output.mkdir(parents=True, exist_ok=True)
    zip_path = output / "arxiv-source.zip"
    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for name, data in sorted(files.items()):
            info = zipfile.ZipInfo(name, ZIP_DATE)
            info.compress_type = zipfile.ZIP_DEFLATED
            info.create_system = 3
            info.external_attr = (0o100755 if name.endswith(".sh") else 0o100644) << 16
            archive.writestr(info, data, compress_type=zipfile.ZIP_DEFLATED, compresslevel=9)
    with zipfile.ZipFile(zip_path) as archive:
        if archive.testzip() is not None or set(archive.namelist()) != set(files):
            raise ValueError("ZIP integrity verification failed")
        if any(archive.read(name) != data for name, data in files.items()):
            raise ValueError("ZIP content verification failed")
    metadata = {
        "status": "prepared_locally_not_uploaded_or_submitted",
        "edition": EDITION,
        "edition_date": EDITION_DATE,
        "title": title,
        "authors": ", ".join(a["given"] + " " + a["family"] for a in authors["authors"]),
        "abstract": abstract,
        "abstract_characters": len(abstract),
        "primary_category": "quant-ph",
        "category_status": "Retained from the user's prior revision-7 draft; not entered or rechecked for this revision.",
        "cross_lists": [],
        "comments": f"{EXPECTED_COMBINED_PAGES} pages, 11 figures, including Supplemental Material. Reproducibility code and data included.",
        "comments_page_count_status": f"{EXPECTED_COMBINED_PAGES} pages expected; final local build confirmation is recorded in verification.json; inspect the arXiv preview",
        "journal_reference": None,
        "doi": None,
        "report_number": None,
        "license": "http://arxiv.org/licenses/nonexclusive-distrib/1.0/",
        "license_status": "Retains the user's selection for draft 8248308 on 18 October 2026; this revision has not been uploaded or rechecked in the portal.",
        "account_endorsement_status": "Prior revision-7 draft reached preview; current portal state has not been checked.",
        "submission_terms_accepted": None,
        "submission_terms_scope": "The user accepted the agreement for the prior draft; no portal action was performed for this revision.",
        "prior_portal_record": "paper/submission-records/arxiv-2026-10-18-v7/upload-verification.json",
        "prior_portal_draft_id": "8248308",
        "compiler": "pdflatex",
        "texlive_version": 2025,
        "main_file": MAIN,
        "official_requirements_checked": "2026-10-17",
        "code_repository_url": "https://github.com/eybmits/fresh-qubits-memory",
        "code_repository_visibility_at_preparation": "private",
        "code_repository_access_note": "User will make the repository public separately; no visibility change authorized.",
        "official_sources": OFFICIAL_SOURCES,
    }
    manifest = {
        "format": 1,
        "edition": EDITION,
        "edition_date": EDITION_DATE,
        "archive": zip_path.name,
        "archive_sha256": digest(zip_path.read_bytes()),
        "archive_bytes": zip_path.stat().st_size,
        "original_source_file_count": len(originals),
        "archive_entry_count": len(files),
        "source_root": "paper/prl-source",
        "archive_entries": {
            name: {"bytes": len(data), "sha256": digest(data)}
            for name, data in sorted(files.items())
        },
        "source_to_archive": mapping,
        "generator_sha256": digest(Path(__file__).read_bytes()),
        "manifest_scope": "External manifest, not included in or self-hashed by the archive.",
        "validation": "Documented arXiv configuration subset, safe paths, single top-level, no ancillary TeX, figure completeness, BBL header, ZIP CRC and byte equality.",
    }
    for name, value in (("submission_metadata.json", metadata), ("author_information.json", authors), ("package-manifest.json", manifest)):
        (output / name).write_bytes(json_bytes(value))
    (output / "title.txt").write_text(title + "\n")
    (output / "abstract.txt").write_text(abstract + "\n")
    (output / "authors.txt").write_text(metadata["authors"] + "\n")
    (output / "README.md").write_text(instructions(figure_tex_count))
    print(json.dumps({"archive": str(zip_path), "sha256": manifest["archive_sha256"],
                      "source_files": len(originals), "archive_entries": len(files)}, indent=2))


def instructions(figure_tex_count):
    return f"""# arXiv upload preparation — 19 October 2026, revision 8

This directory is a new local preparation package. Revision 8 has not been
uploaded or submitted. The earlier revision-7 upload to draft 8248308 is
documented in the [historical portal record](../../submission-records/arxiv-2026-10-18-v7/README.md).
That record reports successful compilation and saved metadata, with the final
Submit action left open. It is not a public arXiv identifier or a live status check.

## Upload and metadata

- Upload **arxiv-source.zip** as a TeX source submission. The single compilation
  target is `memory_limits_prl.tex`, using **pdfLaTeX / TeX Live 2025**.
- The manuscript contains the Letter and Supplemental Material in one document.
- `title.txt`, `authors.txt`, and `abstract.txt` are ready to paste into metadata
  fields. `abstract.txt` uses ASCII plus standard TeX mathematics.
- `author_information.json` retains the confirmed author order, affiliations,
  ORCIDs, and contact data from the earlier author record, with names and ORCIDs
  checked against this manuscript. Local historical source paths are omitted.
- Primary category: **quant-ph**, retaining the prior draft's selection.
  No cross-list is proposed.
- `submission_metadata.json` distinguishes current preparation from the prior
  portal record and retains the user's prior license choice. Journal reference, DOI,
  and institutional report number are blank because none was established.
- The Comments field describes {EXPECTED_COMBINED_PAGES} pages and 11 figures. Final local build checks
  are recorded in `verification.json`; inspect the arXiv preview before submitting.

The user previously selected arXiv's perpetual, non-exclusive distribution
license and accepted the submission agreement in draft 8248308. Those are
recorded historical choices; the current portal state has not been checked.
Replace the older draft files and metadata with this revision, verify the
retained license and any portal requirements, inspect the new arXiv-generated
PDF, and explicitly finalize submission when ready. No portal action has been
performed for this revision. License grants for an announced version are irrevocable.

## Code link

The Supplemental Material bibliography entry and the supplemental code section link to
https://github.com/eybmits/fresh-qubits-memory. At the user's request, the repository
remains PRIVATE. Readers can use this GitHub link only after the author makes
the repository public. Code/data are also included in this arXiv source ZIP.

## Author review

The [revision review](../../../docs/manuscript-2026-10-19-prl-v8.md) records the
new source import and the retained three-author metadata, shared QAR-Lab/LMU
affiliation, and approved AI disclosure. Finite checks and packaging do not
certify the universal theorem. The author's statement about reviewing AI
outputs remains the author's responsibility.

## What is in the ZIP

The root contains the manuscript, matched `.bbl`, `refs.bib`, and 11 final figure
PDFs. It excludes the compiled manuscript PDF, logs, caches and unrelated files.
`00README.json` specifies the sole top-level file and explicitly ignores
{figure_tex_count} figure-construction TeX sources in `figure_sources/`. All other reproducibility
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
  `\\today` changing upon later rebuilds.
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
"""


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-dir", type=Path, default=REPO / "paper/prl-source")
    parser.add_argument("--output-dir", type=Path, default=REPO / "paper/submission/arxiv-2026-10-19-v8")
    parser.add_argument("--author-file", type=Path, default=REPO / "paper/author_information.json")
    args = parser.parse_args()
    build(args.source_dir.resolve(), args.output_dir.resolve(), args.author_file.resolve())


if __name__ == "__main__":
    main()
