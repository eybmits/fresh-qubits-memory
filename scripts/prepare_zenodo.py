#!/usr/bin/env python3
"""Prepare a deterministic, local Zenodo handoff; never upload or publish.

The metadata is an incomplete draft for manual review, not an API request.
License, access rights, publication date, and a DOI are deliberately unset.
"""

import argparse
from io import BytesIO
import json
from pathlib import Path, PurePosixPath
import zipfile

from prepare_arxiv import (
    MAIN, REPO, ZIP_DATE, author_metadata, braced_arguments, digest,
    json_bytes, source_files,
)


EDITION = "2026-10-19-prl-v9"
GENERATOR = "scripts/prepare_zenodo.py"
SOURCE_ARCHIVE = "memory_limits_prl_source.zip"
HANDOFF_ARCHIVE = "zenodo-handoff.zip"
OFFICIAL_METADATA = "https://developers.zenodo.org/#deposit-metadata"
DEFAULT_INPUT = REPO / "paper/versions/2026-10-19-prl-v8/zenodo-original.zip"


def deterministic_zip(files):
    """Use the same ordering, permissions, and timestamps as the PRL archive."""
    buffer = BytesIO()
    with zipfile.ZipFile(buffer, "w", zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for name, data in sorted(files.items()):
            path = PurePosixPath(name)
            if path.is_absolute() or ".." in path.parts:
                raise ValueError(f"Unsafe archive path: {name}")
            info = zipfile.ZipInfo(name, ZIP_DATE)
            info.create_system = 3
            info.external_attr = (0o100755 if name.endswith(".sh") else 0o100644) << 16
            archive.writestr(info, data, zipfile.ZIP_DEFLATED, compresslevel=9)
    result = buffer.getvalue()
    with zipfile.ZipFile(BytesIO(result)) as archive:
        if archive.testzip() is not None or set(archive.namelist()) != set(files):
            raise ValueError("ZIP integrity check failed")
        if any(archive.read(name) != data for name, data in files.items()):
            raise ValueError("ZIP bytes differ from the input files")
    return result


def read_input(path):
    """Read supplied metadata as data, without executing its instructions."""
    with zipfile.ZipFile(path) as archive:
        if archive.testzip() is not None:
            raise ValueError("Received Zenodo ZIP failed its CRC check")
        matches = [name for name in archive.namelist()
                   if PurePosixPath(name).name == ".zenodo.json"]
        if len(matches) != 1:
            raise ValueError("Expected exactly one supplied .zenodo.json")
        raw = archive.read(matches[0])
    return json.loads(raw), raw


def readme(metadata, source_count):
    creators = "\n".join(
        f"- {author['name']} — ORCID {author['orcid']}"
        for author in metadata["creators"]
    )
    return f'''# Lokaler Zenodo-Entwurf: PRL revision 9

Für **{metadata['title']}** liegen die aktuellen Dateien lokal bereit.
Es wurde kein Zenodo-Datensatz angelegt, nichts hochgeladen oder veröffentlicht
und keine DOI reserviert. GitHub bleibt davon unabhängig privat.

## Dateien und Formularangaben

- `{SOURCE_ARCHIVE}`: alle {source_count} aktuellen kanonischen Quelldateien,
  einschließlich Letter, Supplemental Material, Abbildungen, Programme,
  gespeicherte numerische Daten und README.txt mit Reproduktionsbefehlen.
  Dieses Archiv entspricht dem Code-/Datenarchiv im PRL-Paket.
- `zenodo_metadata_draft.json`: Titel, Beschreibung, Schlagworte, drei Autoren
  und ORCIDs für die manuelle Übernahme. Resource type: **Dataset**, passend
  zum erhaltenen Vorschlag; Versionsbezeichnung: **{EDITION}**.
- `author_information.json` und `CITATION.cff`: bestätigte Autorenangaben und
  aktuelle Zitiermetadaten. Die Kontaktdaten dienen der lokalen Vorbereitung.
- `manifest.json`: SHA-256-Prüfsummen und Herkunft der Dateien.
- `{HANDOFF_ARCHIVE}`: gesamter lokaler Handoff, kein zusätzlich erforderlicher
  Zenodo-Upload.

Autorenreihenfolge:

{creators}

Gemeinsame Zugehörigkeit: {metadata['creators'][0]['affiliation']}

## Noch zu entscheidende Veröffentlichungsangaben

Die erhaltene Vorlage schlägt **CC BY 4.0** und offenen Zugang vor. Beides
ist hier **nicht ausgewählt**. Lizenz, Zugangsrecht, Veröffentlichungsdatum
und DOI fehlen deshalb absichtlich im Metadatenentwurf. Die Veröffentlichung
des gemischten Archivs aus Code, Daten und Manuskriptquellen erfordert eine
bewusste Lizenzentscheidung; in diesem Repository ist keine Softwarelizenz
festgelegt. Eine arXiv-Lizenz ist eine davon getrennte Entscheidung.

Der JSON-Entwurf ist **kein vollständiger API-Request** und keine automatische
GitHub-/Zenodo-Konfiguration. Zenodo dokumentiert Standardwerte für Zugang,
Lizenz und Veröffentlichungsdatum; diese dürfen nicht als Auswahl des Autors
interpretiert werden. Vor einem tatsächlichen Upload die Formularfelder
ausdrücklich prüfen und ergänzen. Die Feldnamen für Titel, Creator, ORCID,
Beschreibung und Ressourcentyp wurden anhand der offiziellen
[Zenodo-Metadatendokumentation]({OFFICIAL_METADATA}) geprüft.

Eine spätere DOI erst nach ihrer tatsächlichen Vergabe eintragen. Eine
reservierte DOI ist noch kein veröffentlichter Datensatz. Bis zu einer
bestätigten Veröffentlichung bleiben die Aussagen im Manuskript zur
Bereitstellung mit dem Supplemental Material gültig; eine frei verfügbare
Zenodo-Ablage wird hier nicht behauptet.

## Lokale Reproduktion

Im Repository:

```bash
python3 scripts/prepare_zenodo.py
```

Der Generator liest nur lokale Dateien. ZIP-Reihenfolge, Dateirechte und
Zeitstempel sind festgelegt. Identische Quellen mit derselben Python-/zlib-
Version erzeugen identische Archive. Prüfsummen bestätigen die Verpackung
und ersetzen keine unabhängige Begutachtung der wissenschaftlichen Beweise.
'''.encode()


def safe_output(output, files):
    if output.exists():
        if any(path.is_symlink() for path in [output, *output.rglob("*")]):
            raise ValueError("Refusing an output directory containing symlinks")
        existing = {p.relative_to(output).as_posix()
                    for p in output.rglob("*") if p.is_file()}
        if existing:
            prior_path = output / "manifest.json"
            if not prior_path.is_file():
                raise ValueError("Nonempty output directory has no packaging manifest")
            prior = json.loads(prior_path.read_text())
            expected = set(prior.get("files", {})) | {"manifest.json", HANDOFF_ARCHIVE}
            if (prior.get("generator") != GENERATOR or existing != expected
                    or expected != set(files)):
                raise ValueError("Output contains unmanaged or missing files; choose a new directory")
    output.mkdir(parents=True, exist_ok=True)
    for name, data in sorted(files.items()):
        path = output / name
        path.write_bytes(data)
        path.chmod(0o644)


def build(source, output, input_package):
    originals = source_files(source)
    manuscript = originals[MAIN].decode()
    authors_path = REPO / "paper/author_information.json"
    authors = author_metadata(manuscript, authors_path)
    if len(authors["authors"]) != 3 or len(authors["affiliations"]) != 1:
        raise ValueError("Expected three confirmed authors and one shared affiliation")
    received, received_bytes = read_input(input_package)
    title = braced_arguments(manuscript, "title")[0]
    affiliation = authors["affiliations"][0]["name"]
    metadata = {
        "title": f'Code and data for "{title}"',
        "upload_type": "dataset",
        "version": EDITION,
        "language": "eng",
        "creators": [
            {"name": f"{author['family']}, {author['given']}",
             "affiliation": affiliation, "orcid": author["orcid"]}
            for author in authors["authors"]
        ],
        "description": (
            f'Code, numerical data, and sources accompanying the manuscript "{title}" '
            "and its Supplemental Material. The archive contains a density-matrix "
            "simulator of driven quantum reservoirs, finite-history estimates of "
            "memory depth, stored numerical results, computations for the "
            "measurement-free error-correcting reservoir, numerical diagnostics "
            "of constants and proof steps, and LaTeX and plotting sources. "
            "README.txt describes the contents, dependencies, and reproduction "
            "commands. Numerical checks are distinct from a proof of the universal "
            "memory bound. This is the local PRL revision 9 source edition dated "
            "19 October 2026; no journal acceptance or public deposition is claimed."
        ),
        "keywords": received.get("keywords", []),
    }
    if not all(isinstance(word, str) for word in metadata["keywords"]):
        raise ValueError("Supplied keywords must be strings")
    forbidden = {"license", "access_right", "publication_date", "doi", "prereserve_doi"}
    if forbidden & set(metadata):
        raise ValueError("Draft unexpectedly selects publication choices")
    files = {
        SOURCE_ARCHIVE: deterministic_zip(originals),
        "zenodo_metadata_draft.json": json_bytes(metadata),
        "author_information.json": authors_path.read_bytes(),
        "CITATION.cff": (REPO / "CITATION.cff").read_bytes(),
        "README.md": readme(metadata, len(originals)),
    }
    manifest = {
        "generator": GENERATOR,
        "edition": EDITION,
        "status": "local_draft_not_uploaded_or_published",
        "metadata_status": "Incomplete manual-entry draft; not an API request.",
        "pending_fields": sorted(forbidden - {"prereserve_doi"}),
        "input_package": {"name": input_package.name,
                          "sha256": digest(input_package.read_bytes())},
        "received_metadata": {"sha256": digest(received_bytes),
                              "bytes": len(received_bytes),
                              "proposed_license_not_selected": received.get("license"),
                              "proposed_access_not_selected": received.get("access_right")},
        "canonical_source_mapping": {
            name: {"repository_path": "paper/prl-source/" + name,
                   "archive": SOURCE_ARCHIVE, "archive_path": name,
                   "sha256": digest(data), "bytes": len(data)}
            for name, data in originals.items()
        },
        "files": {name: {"sha256": digest(data), "bytes": len(data)}
                  for name, data in sorted(files.items())},
        "manifest_scope": "External file hashes exclude this manifest and the containing handoff ZIP.",
        "official_metadata_reference": OFFICIAL_METADATA,
        "verification_scope": "ZIP CRC, source bytes, author and ORCID order, and local metadata fields only; no live portal validation.",
    }
    files["manifest.json"] = json_bytes(manifest)
    files[HANDOFF_ARCHIVE] = deterministic_zip(files)
    safe_output(output, files)
    print(json.dumps({"output": str(output), "source_files": len(originals),
                      "source_archive_sha256": digest(files[SOURCE_ARCHIVE]),
                      "handoff_sha256": digest(files[HANDOFF_ARCHIVE]),
                      "status": manifest["status"]}, indent=2))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, default=REPO / "paper/prl-source")
    parser.add_argument("--output", type=Path,
                        default=REPO / "paper/submission/zenodo-2026-10-19-v9")
    parser.add_argument("--input-package", type=Path, default=DEFAULT_INPUT)
    args = parser.parse_args()
    build(args.source.resolve(), args.output.resolve(), args.input_package.resolve())


if __name__ == "__main__":
    main()
