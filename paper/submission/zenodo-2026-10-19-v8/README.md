# Lokaler Zenodo-Entwurf: PRL revision 8

Für **Code and data for "The Fundamental Memory Ceiling of Noisy Quantum Reservoirs"** liegen die aktuellen Dateien lokal bereit.
Es wurde kein Zenodo-Datensatz angelegt, nichts hochgeladen oder veröffentlicht
und keine DOI reserviert. GitHub bleibt davon unabhängig privat.

## Dateien und Formularangaben

- `memory_limits_prl_source.zip`: alle 54 aktuellen kanonischen Quelldateien,
  einschließlich Letter, Supplemental Material, Abbildungen, Programme,
  gespeicherte numerische Daten und README.txt mit Reproduktionsbefehlen.
  Dieses Archiv entspricht dem Code-/Datenarchiv im PRL-Paket.
- `zenodo_metadata_draft.json`: Titel, Beschreibung, Schlagworte, drei Autoren
  und ORCIDs für die manuelle Übernahme. Resource type: **Dataset**, passend
  zum erhaltenen Vorschlag; Versionsbezeichnung: **2026-10-19-prl-v8**.
- `author_information.json` und `CITATION.cff`: bestätigte Autorenangaben und
  aktuelle Zitiermetadaten. Die Kontaktdaten dienen der lokalen Vorbereitung.
- `manifest.json`: SHA-256-Prüfsummen und Herkunft der Dateien.
- `zenodo-handoff.zip`: gesamter lokaler Handoff, kein zusätzlich erforderlicher
  Zenodo-Upload.

Autorenreihenfolge:

- Baumann, Markus — ORCID 0009-0007-3575-1006
- Stein, Jonas — ORCID 0000-0001-5727-9151
- Linnhoff-Popien, Claudia — ORCID 0000-0001-6284-9286

Gemeinsame Zugehörigkeit: Quantum Applications and Research Laboratory (QAR-Lab), Ludwig-Maximilians-Universität München, Oettingenstraße 67, 80538 München, Germany

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
[Zenodo-Metadatendokumentation](https://developers.zenodo.org/#deposit-metadata) geprüft.

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
