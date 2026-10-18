#!/usr/bin/env python3
"""Prepare local PRL upload files from the canonical combined Letter and SM.

Requires pypdf, pdfLaTeX and BibTeX. The supplied combined PDF must be freshly
built from paper/prl-source; its Letter text is checked against an independent
build before any output is written. All TeX build files stay in a temporary
directory. This script does not access a submission portal or change GitHub.
"""

import argparse
from collections import Counter
from datetime import datetime, timezone
from io import BytesIO
import json
import logging
import os
from pathlib import Path
import re
import shutil
import subprocess
import tempfile
import unicodedata
import zipfile

from pypdf import PdfReader, PdfWriter
from pypdf.constants import PageLabelStyle

from prepare_arxiv import (
    EXPECTED_COMBINED_PAGES, MAIN, REPO, ZIP_DATE, author_metadata, braced_arguments, digest,
    json_bytes, source_files,
)


EDITION = "2026-10-18-v5"
GENERATOR = "scripts/prepare_prl.py"
DEFAULT_JUSTIFICATION = REPO / "paper/versions/2026-10-18-prl-v5/justification-user.txt"
MANUSCRIPT_FILES = [MAIN, "refs.bib", "memory_limits_prl.bbl"] + [
    f"fig{i}.pdf" for i in range(1, 5)
]
EXPECTED_PAGES = (6, EXPECTED_COMBINED_PAGES - 6)
OFFICIAL_SOURCES = {
    "web_submission": "https://journals.aps.org/authors/web-submission-guidelines-physical-review",
    "prl_author_instructions": "https://journals.aps.org/prl/authors",
    "supplemental_material": "https://journals.aps.org/authors/supplemental-material-instructions",
    "length_guide": "https://journals.aps.org/authors/length-guide",
}


def deterministic_zip(files):
    """Stable order, timestamps and modes; no machine-specific ZIP metadata."""
    buffer = BytesIO()
    with zipfile.ZipFile(buffer, "w", zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for name, data in sorted(files.items()):
            info = zipfile.ZipInfo(name, ZIP_DATE)
            info.create_system = 3
            info.external_attr = (0o100755 if name.endswith(".sh") else 0o100644) << 16
            archive.writestr(info, data, zipfile.ZIP_DEFLATED, compresslevel=9)
    return buffer.getvalue()


def letter_source(combined):
    marker = re.search(r"(?m)^% SUPPLEMENTAL MATERIAL\s*$", combined)
    if marker is None or len(re.findall(r"(?m)^% SUPPLEMENTAL MATERIAL\s*$", combined)) != 1:
        raise ValueError("Expected one Supplemental Material boundary in the source")
    letter = combined[:marker.start()]
    # The separator before the marker is harmless, but omit it in the derived file.
    letter = re.sub(r"\n%={5,}\s*$", "", letter).rstrip()
    if r"\bibliography{refs}" not in letter or r"\end{document}" in letter:
        raise ValueError("Unexpected Letter bibliography or document boundary")
    return (letter + "\n\n\\end{document}\n").encode()


def portal_abstract(combined):
    """Convert only this manuscript's known abstract math to portal-ready text."""
    matches = re.findall(r"\\begin\{abstract\}(.*?)\\end\{abstract\}", combined, re.S)
    if len(matches) != 1:
        raise ValueError("Expected exactly one manuscript abstract")
    abstract = " ".join(matches[0].split())
    for before, after in ((r"$k$", "k"), (r"$\exp[\Theta(k)]$", "exp[Θ(k)]")):
        abstract = abstract.replace(before, after)
    if any(character in abstract for character in "\\${}%~"):
        raise ValueError("Unconverted abstract TeX; review the plain-text conversion")
    if not abstract or len(abstract) > 600:
        raise ValueError(f"Portal abstract has {len(abstract)} characters; review the 600-character limit")
    return (abstract + "\n").encode("utf-8")


def bibitems(bbl):
    return re.findall(r"\\bibitem\s*(?:\[[\s\S]*?\])?\s*\{([^}]+)\}", bbl.decode())


def normalized_text(reader, start=0, end=None):
    text = "".join(page.extract_text() or "" for page in reader.pages[start:end])
    return re.sub(r"\s+", "", unicodedata.normalize("NFKC", text))


def link_inventory(reader, start=0):
    """Check all links and describe those whose targets survive the page split."""
    links = Counter()
    removed = 0
    destinations = reader.named_destinations
    for index, page in enumerate(reader.pages[start:]):
        for reference in page.get("/Annots", []):
            annotation = reference.get_object()
            if annotation.get("/Subtype") != "/Link":
                continue
            action = annotation.get("/A", {})
            if action.get("/S") == "/URI":
                links[(index, "URI", str(action["/URI"]))] += 1
                continue
            destination = action.get("/D", annotation.get("/Dest"))
            if not isinstance(destination, str) or destination not in destinations:
                raise ValueError("Unexpected or unresolved internal PDF link; inspect before packaging")
            target = reader.get_destination_page_number(destinations[destination])
            if target is None or target < 0 or target >= len(reader.pages):
                raise ValueError("PDF link points outside the document")
            if target < start:
                removed += 1
            else:
                links[(index, "GoTo", destination, target - start)] += 1
    return links, removed


def compile_letter(files):
    """Build independently, including a second BibTeX pass for nested SM cites."""
    for program in ("pdflatex", "bibtex"):
        if not shutil.which(program):
            raise ValueError(f"Required TeX program not found: {program}")
    environment = os.environ.copy()
    environment["SOURCE_DATE_EPOCH"] = str(int(datetime(
        *ZIP_DATE, tzinfo=timezone.utc).timestamp()))
    environment["FORCE_SOURCE_DATE"] = "1"
    environment["TZ"] = "UTC"
    tex_command = [
        "pdflatex", "-no-shell-escape", "-interaction=nonstopmode", "-halt-on-error",
        "-jobname=memory_limits_prl",
        r"\pdfinfoomitdate=1\pdftrailerid{}\pdfsuppressptexinfo=15\input{memory_limits_prl.tex}",
    ]
    commands = [tex_command, ["bibtex", "memory_limits_prl"], tex_command,
                ["bibtex", "memory_limits_prl"], tex_command, tex_command]
    with tempfile.TemporaryDirectory(prefix="fresh-qubits-prl-") as temporary:
        directory = Path(temporary)
        for name, data in files.items():
            (directory / name).write_bytes(data)
        for command in commands:
            completed = subprocess.run(command, cwd=directory, env=environment,
                                       stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                                       text=True, timeout=120, check=False)
            if completed.returncode:
                raise ValueError("Letter compilation failed:\n" + completed.stdout[-10000:])
        log = (directory / "memory_limits_prl.log").read_text(errors="replace")
        bad = re.findall(
            r"^.*(?:undefined|Rerun to get|Label\(s\) may have changed|multiply defined|^!).*$",
            log, re.M | re.I,
        )
        if bad:
            raise ValueError("Unresolved final Letter build diagnostics:\n" + "\n".join(bad))
        bibliography = (directory / "memory_limits_prl.bbl").read_bytes()
        if bibitems(bibliography) != bibitems(files["memory_limits_prl.bbl"]):
            raise ValueError("Fresh Letter references differ from the combined manuscript")
        pdf = (directory / "memory_limits_prl.pdf").read_bytes()
        evidence = {
            "commands": commands,
            "shell_escape": False,
            "source_date_epoch": environment["SOURCE_DATE_EPOCH"],
            "final_log_sha256": digest(log.encode()),
            "unresolved_references_or_citations": False,
            "bibliography_keys": bibitems(bibliography),
            "tool_versions": {
                tool: subprocess.run([tool, "--version"], stdout=subprocess.PIPE,
                                     text=True, check=True).stdout.splitlines()[0]
                for tool in ("pdflatex", "bibtex")
            },
        }
        return pdf, bibliography, evidence


def split_supplement(combined_pdf, title, author_names):
    reader = PdfReader(BytesIO(combined_pdf))
    letter_pages, supplemental_pages = EXPECTED_PAGES
    if len(reader.pages) != sum(EXPECTED_PAGES):
        raise ValueError(f"Expected {sum(EXPECTED_PAGES)} combined pages, found {len(reader.pages)}; review the split")
    if "Supplemental Material:" not in (reader.pages[letter_pages].extract_text() or ""):
        raise ValueError(f"Page {letter_pages + 1} is not the expected Supplemental Material title page")
    writer = PdfWriter()
    # append() translates surviving named destinations and internal page links.
    # Links to the removed Letter cannot remain local links in the separate SM.
    expected_links, links_to_letter = link_inventory(reader, letter_pages)

    class LinkDiagnostics(logging.Filter):
        # pypdf 6.10 reports intermediate annotation counts during append even
        # when surviving links are subsequently reconstructed. Replace only
        # that noisy diagnostic with the exhaustive before/after check below.
        def filter(self, record):
            return not record.getMessage().startswith("Annotation sizes differ:")

    logger = logging.getLogger("pypdf.generic._link")
    diagnostic_filter = LinkDiagnostics()
    logger.addFilter(diagnostic_filter)
    try:
        writer.append(reader, pages=(letter_pages, len(reader.pages)), import_outline=True)
    finally:
        logger.removeFilter(diagnostic_filter)
    writer.add_metadata({
        "/Title": "Supplemental Material: " + title,
        "/Author": ", ".join(author_names),
        "/Subject": "Proofs, derivations, simulation methods, and reproduction guide",
    })
    writer.set_page_label(0, supplemental_pages - 1, style=PageLabelStyle.DECIMAL,
                          prefix="S", start=1)
    result = BytesIO()
    writer.write(result)
    data = result.getvalue()
    split = PdfReader(BytesIO(data))
    if normalized_text(split) != normalized_text(reader, letter_pages):
        raise ValueError("Supplemental text changed during PDF splitting")
    actual_links, _ = link_inventory(split)
    if actual_links != expected_links:
        raise ValueError("A surviving supplemental hyperlink changed or was lost during splitting")
    return reader, data, {
        "preserved_internal_links": sum(n for key, n in actual_links.items() if key[1] == "GoTo"),
        "preserved_uri_links": sum(n for key, n in actual_links.items() if key[1] == "URI"),
        "removed_links_to_separate_letter": links_to_letter,
        "dangling_links": 0,
    }


def prepare_cover(template, author_names):
    replacements = {
        "I submit the manuscript": "We submit the manuscript",
        "The Letter proves that it does not:": (
            "The Letter proves that adding qubits cannot raise the uniform memory ceiling:"
        ),
        "Sincerely,\nMarkus Baumann\n": (
            "Sincerely,\nMarkus Baumann\nOn behalf of "
            + ", ".join(author_names[:-1]) + ", and " + author_names[-1] + "\n"
        ),
    }
    for before, after in replacements.items():
        if template.count(before) != 1:
            raise ValueError(f"Cover-letter template changed; review replacement: {before!r}")
        template = template.replace(before, after)
    return ("DRAFT — author review required before sending\n\n" + template.strip() + "\n").encode()


def readme(title, author_names):
    return f"""# PRL submission preparation — {EDITION}

{title}
{', '.join(author_names)}

This is a local, unsubmitted preparation package. Nothing was uploaded or sent.
The outer `prl-submission.zip` is a convenient handoff; unpack it first. It is
not a single manuscript file to upload indiscriminately to the APS portal.

1. Upload `memory_limits_prl_letter.pdf` as the manuscript: six pages including
   figures and references. PDF is sufficient for initial submission.
2. Use **Upload supplemental files** for the three files in
   `2_supplemental_material/`: the separate {EXPECTED_PAGES[1]}-page `memory_limits_prl_SM.pdf`,
   complete source/code/data ZIP, and descriptive `README.TXT`. The source ZIP
   is the reproducibility deposit cited by the paper; it includes the combined
   manuscript, bibliography, figures, simulator, saved data, and checks.
3. Review `cover_letter.txt` and `justification.txt` before using their text.
   `abstract.txt` contains the manuscript abstract as plain Unicode text, with
   its character count checked against the portal's 600-character limit.
   `justification.txt` contains the exact text supplied by the user for this
   revision, with no heading; it is ready to paste into the justification field.
   The cover letter is a draft: its exclusive-submission statement needs final
   confirmation by the authors. Coauthor approval and any prior submission
   history have not been verified by this preparation workflow.
4. Enter the confirmed author order, contact address, ORCIDs and one shared
   affiliation from `author_information.json`. The identifiers are copied from
   the approved author record; authentication in the portal remains separate.
5. Complete funding, data availability, any referee suggestions/conflicts,
   publication options and rights/terms according to the authors' decisions.
   Check the PDF generated by APS before making the final submission.

The Letter and Supplemental Material belong to the same submission but use
separate PDF uploads. The {sum(EXPECTED_PAGES)}-page combined PDF is prepared for arXiv and reading.
The seven Letter source files in `manuscript-source.zip` and `1_manuscript/`
are retained for production: APS requests manuscript sources after acceptance.
They are not required for initial peer review. If requested later, the main TeX
file is `memory_limits_prl.tex`.

The code link in the Supplemental Material bibliography entry and SM code section is
https://github.com/eybmits/fresh-qubits-memory . The repository remains PRIVATE
at the user's request; the user will open access separately. Do not describe
this link as public until access has been verified. The complete code/data
archive is included with the proposed Supplemental Material deposit.

The user confirmed on 18 October 2026 that the disclosed model name
“Claude Opus 5.5” is correct. The workflow does not independently certify the
manuscript's author statements about checking every derivation and numerical
result, AI-tool rights, coauthor consent, originality, or exclusive submission.
Build, consistency and numerical checks are evidence of their specific scope;
they are not a complete independent proof review or a prediction of acceptance.

`manifest.json` hashes every prepared file except itself and the outer ZIP,
records the original input-package hash, and maps each reproducibility file
to the canonical source. `build_verification.json` records the fresh Letter
build and its text agreement with the first six pages of the combined PDF.
The SM preserves text and surviving internal links; references to removed
Letter pages are read alongside the Letter rather than as local SM links.
Build logs and intermediate TeX files are not included in upload packages.

Rebuild with Python containing pypdf, plus pdfLaTeX/BibTeX on PATH:

```sh
python scripts/prepare_prl.py --combined-pdf /absolute/path/to/fresh-combined.pdf
```

An existing generated output directory can be refreshed only if it contains
exactly the files managed by its prior manifest; unrelated files are protected.

Official APS guidance checked 18 October 2026:

- File upload requirements: {OFFICIAL_SOURCES['web_submission']}
- PRL author instructions: {OFFICIAL_SOURCES['prl_author_instructions']}
- Supplemental Material: {OFFICIAL_SOURCES['supplemental_material']}
- Length guide: {OFFICIAL_SOURCES['length_guide']}

These files do not create a DOI, select a publication license, change repository
visibility, accept an agreement, or submit the manuscript.
""".encode()


def supplemental_readme(title, authors):
    affiliation = authors["affiliations"][0]["name"]
    names = ", ".join(a["given"] + " " + a["family"] for a in authors["authors"])
    return f"""Title: {title}
Authors: {names}
Affiliation: {affiliation}
Contact: markus.baumann@campus.lmu.de

Description: Supplemental Material containing the proofs, exact analysis of
the error-correcting reservoir, entropy budget for general noise, simulation
methods, and complete source, code and data for the article.

Files:
memory_limits_prl_SM.pdf — Supplemental Material, pages S1–S{EXPECTED_PAGES[1]}. Equations,
figures and tables carry an S prefix; unprefixed references refer to the Letter.
memory_limits_prl_source.zip — combined Letter and Supplemental Material in
LaTeX; bibliography; figure PDFs and generation sources; simulation programs,
saved datasets and independent calculation checks. Unpack and follow README.txt.

Minimum requirements: a PDF reader for the supplement; Python 3 with numpy,
scipy, mpmath and matplotlib for the numerical/plotting programs; pdfLaTeX and
BibTeX with REVTeX 4.2 and the packages listed in README.txt for the documents.
The plotting sources additionally use the fonts and TeX packages stated there.

The code repository is https://github.com/eybmits/fresh-qubits-memory .
All reproduction files are also included in this Supplemental Material deposit.
""".encode()


def safe_output(output, files):
    if output.exists():
        previous_manifest = output / "manifest.json"
        existing = {p.relative_to(output).as_posix() for p in output.rglob("*") if p.is_file()}
        if existing:
            if not previous_manifest.is_file():
                raise ValueError("Nonempty output directory lacks a packaging manifest; choose a new one")
            previous = json.loads(previous_manifest.read_text())
            expected = set(previous.get("files", {})) | {"manifest.json", "prl-submission.zip"}
            if previous.get("generator") != GENERATOR or existing != expected:
                raise ValueError("Output contains unmanaged or missing files; choose a new directory")
            if expected != set(files):
                raise ValueError("Output file layout changed; choose a new directory for this package")
        if any(p.is_symlink() for p in [output, *output.rglob("*")]):
            raise ValueError("Refusing to write through symlinks in the output directory")
    output.mkdir(parents=True, exist_ok=True)
    for name, data in files.items():
        path = output / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data)
        path.chmod(0o644)


def build(combined_pdf, output, input_package, justification_file=DEFAULT_JUSTIFICATION):
    source = REPO / "paper/prl-source"
    originals = source_files(source)
    combined_text = originals[MAIN].decode()
    abstract = portal_abstract(combined_text)
    authors_path = REPO / "paper/author_information.json"
    authors = author_metadata(combined_text, authors_path)
    names = [a["given"] + " " + a["family"] for a in authors["authors"]]
    title = braced_arguments(combined_text, "title")[0]
    if len(names) != 3 or len(authors["affiliations"]) != 1:
        raise ValueError("Expected the confirmed three authors and one shared affiliation")
    combined_data = combined_pdf.read_bytes()
    combined, supplemental_pdf, supplemental_links = split_supplement(combined_data, title, names)
    letter_files = {name: originals[name] for name in MANUSCRIPT_FILES}
    letter_files[MAIN] = letter_source(combined_text)
    letter_pdf, letter_bbl, verification = compile_letter(letter_files)
    letter = PdfReader(BytesIO(letter_pdf))
    if len(letter.pages) != EXPECTED_PAGES[0]:
        raise ValueError(f"Fresh Letter is not {EXPECTED_PAGES[0]} pages; review page split and length")
    if normalized_text(letter) != normalized_text(combined, 0, EXPECTED_PAGES[0]):
        raise ValueError("Fresh Letter text differs from the combined PDF; rebuild the combined PDF first")
    letter_links, _ = link_inventory(letter)
    letter_files["memory_limits_prl.bbl"] = letter_bbl
    verification.update({
        "letter_pages": len(letter.pages),
        "supplemental_pages": EXPECTED_PAGES[1],
        "combined_pages": len(combined.pages),
        "portal_abstract_characters": len(abstract.decode("utf-8").rstrip("\n")),
        "portal_abstract_max_characters": 600,
        "letter_text_matches_combined": True,
        "letter_combined_page_range": [1, EXPECTED_PAGES[0]],
        "supplemental_text_matches_combined": True,
        "supplemental_combined_page_range": [EXPECTED_PAGES[0] + 1, sum(EXPECTED_PAGES)],
        "combined_pdf_sha256": digest(combined_data),
        "letter_pdf_sha256": digest(letter_pdf),
        "supplemental_pdf_sha256": digest(supplemental_pdf),
        "supplemental_link_validation": supplemental_links,
        "letter_link_validation": {
            "internal_links": sum(n for key, n in letter_links.items() if key[1] == "GoTo"),
            "uri_links": sum(n for key, n in letter_links.items() if key[1] == "URI"),
            "dangling_links": 0,
        },
        "scope": "Technical packaging checks only; no independent certification of all proofs.",
    })
    with zipfile.ZipFile(input_package) as archive:
        templates = {name: archive.read(name) for name in
                     ("cover_letter.txt", "justification.txt", "submission_notes.txt")}
    justification = justification_file.read_bytes()
    if not justification.decode("utf-8").strip():
        raise ValueError("The user-supplied justification is empty")
    files = {"1_manuscript/" + name: data for name, data in letter_files.items()}
    files.update({
        "memory_limits_prl_letter.pdf": letter_pdf,
        "manuscript-source.zip": deterministic_zip(letter_files),
        "2_supplemental_material/memory_limits_prl_SM.pdf": supplemental_pdf,
        "2_supplemental_material/memory_limits_prl_source.zip": deterministic_zip(originals),
        "2_supplemental_material/README.TXT": supplemental_readme(title, authors),
        "author_information.json": authors_path.read_bytes(),
        "cover_letter.txt": prepare_cover(templates["cover_letter.txt"].decode(), names),
        "justification.txt": justification,
        "abstract.txt": abstract,
        "README.md": readme(title, names),
        "build_verification.json": json_bytes(verification),
    })
    manifest = {
        "generator": GENERATOR,
        "edition": EDITION,
        "status": "Prepared locally; not uploaded or submitted; author attestations pending.",
        "input_package": {"name": input_package.name, "sha256": digest(input_package.read_bytes())},
        "combined_pdf": {"name": combined_pdf.name, "sha256": digest(combined_data)},
        "template_inputs": {name: {"sha256": digest(data), "bytes": len(data)}
                            for name, data in templates.items()},
        "user_justification": {
            "name": justification_file.name,
            "sha256": digest(justification),
            "bytes": len(justification),
            "handling": "Copied byte-for-byte without a heading; replaces the archived ZIP justification.",
        },
        "canonical_source_mapping": {
            name: {"repository_path": "paper/prl-source/" + name,
                   "archive": "2_supplemental_material/memory_limits_prl_source.zip",
                   "archive_path": name, "sha256": digest(data), "bytes": len(data)}
            for name, data in originals.items()
        },
        "files": {name: {"sha256": digest(data), "bytes": len(data)}
                  for name, data in sorted(files.items())},
        "official_sources": OFFICIAL_SOURCES,
        "changes_from_received_package": [
            "Derived Letter-only sources from the current canonical combined manuscript.",
            "Compiled the Letter independently without shell escape and refreshed its bibliography.",
            "Split the SM from the supplied fresh combined PDF and set title, authors and S page labels.",
            "Retained the three confirmed authors, their ORCIDs, and one shared affiliation.",
            "Packed every selected canonical reproduction source with deterministic ZIP metadata.",
            "Adapted the cover letter to three authors and a uniform memory ceiling claim.",
            "Retained the supplied exclusivity sentence in the draft cover letter; README records pending author attestations.",
            "Used the user's exact replacement justification without a heading; retained the original ZIP text in input provenance.",
            "Prepared plain Unicode abstract text with a checked 600-character maximum.",
            "Replaced stale submission notes with the current README.",
        ],
    }
    files["manifest.json"] = json_bytes(manifest)
    files["prl-submission.zip"] = deterministic_zip(files)
    # Verify the canonical input was not changed by another process while building.
    if source_files(source) != originals:
        raise ValueError("Canonical source changed during packaging; rerun after it is frozen")
    safe_output(output, files)
    return {"output": str(output), "letter_pages": EXPECTED_PAGES[0],
            "supplemental_pages": EXPECTED_PAGES[1],
            "source_files": len(originals), "outer_zip_sha256": digest(files["prl-submission.zip"])}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--combined-pdf", type=Path, required=True,
                        help=f"Freshly compiled {sum(EXPECTED_PAGES)}-page combined Letter and Supplemental Material")
    parser.add_argument("--output-dir", type=Path,
                        default=REPO / "paper/submission/prl-2026-10-18-v5")
    parser.add_argument("--input-package", type=Path,
                        default=REPO / "paper/versions/2026-10-18-prl-v5/submission-original.zip")
    parser.add_argument("--justification-file", type=Path, default=DEFAULT_JUSTIFICATION,
                        help="User-approved plain UTF-8 text copied byte-for-byte to justification.txt")
    args = parser.parse_args()
    try:
        result = build(args.combined_pdf.resolve(), args.output_dir.resolve(),
                       args.input_package.resolve(), args.justification_file.resolve())
    except (ValueError, OSError, subprocess.SubprocessError, zipfile.BadZipFile) as error:
        parser.exit(1, f"PRL package not written: {error}\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
