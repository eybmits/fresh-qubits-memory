# Physical Review A format check: revision 5

The newly supplied manuscript is a full PRA-style article. The integration target is the official APS REVTeX class:

```latex
\documentclass[aps,pra,reprint,superscriptaddress,floatfix]{revtex4-2}
```

The original `twocolumn` option was supported; `reprint` explicitly requests the journal-style layout. The figures and data are retained. Six explicit wording clarifications in the scientific text are recorded in the version provenance; equations are unchanged. This record is separate from the historical v4 check.

| Item | Current preparation |
| --- | --- |
| Authors | Markus Baumann, Jonas Stein, Claudia Linnhoff-Popien, in the previously approved order. |
| Identifiers | ORCID `0009-0007-3575-1006`, `0000-0001-5727-9151`, `0000-0001-6284-9286`, respectively. |
| Affiliations | All three: QAR-Lab and Chair of Mobile and Distributed Systems, Department of Computer Science, LMU Munich, Oettingenstraße 67, 80538 München. |
| Contact | `markus.baumann@campus.lmu.de`; contact-author prefix retained. |
| Dependencies | REVTeX 4.2, pdfLaTeX, BibTeX/apsrev4-2, `orcidlink` and its TikZ dependencies. |
| Abstract | Previously approved one-paragraph abstract retained; no new abstract drafted. |
| Bibliography | Working source uses BibTeX; upload-only source embeds the final BBL. |
| Figures/tables | Eight figures and six tables in the supplied source; all present in the final rendered PDF. |
| Length | Supplied PDF: 21 pages. PRA Regular Articles have no length limit. Final integrated PDF: 21 pages. |
| Data availability | Separate section after acknowledgments and before appendices. |
| Upload | Initial submission uses a single PDF containing article text and figures; supplement is separate. No upload performed. |

The format choices follow [PRA author guidance](https://journals.aps.org/pra/authors), the [REVTeX FAQ](https://journals.aps.org/revtex/revtex-faq), and [APS submission guidance](https://journals.aps.org/authors/web-submission-guidelines-physical-review). They do not imply that the paper meets PRL length or editorial criteria. The incoming v5 core contains 6,218 ordinary TeXcount words (5,264 body, 165 headings, 789 captions); the conservative local estimate including audited equations, figures and tables is at least 7,733 PRL word-equivalents, versus a 3,750-word core limit. This is not an official APS count, and the final wording clarifications make only minor changes. A short Letter would need a separate length and layout check.

## Final checks

The integrating agent compiled the final v5 manuscript and rendered all 21 pages. The byline, three ORCID links, six tables and eight figures were checked; the new constant glossary and revised robustness figure received closer inspection. There are no overfull boxes or unresolved references. Nonfatal nameref and deferred-float warnings remain, with all floats present. All 12 repository tests pass. This is a fresh v5 build check; previous numerical diagnostics are reused only where the underlying simulator/data hashes are unchanged.

Final PDF: 873584 bytes, SHA256 `69a83d1a0c0f4bab16b29e879efd2226f0f16fc6a0b2c8701a5e7544b315ea76`. A separate fresh compilation of the upload-only source with embedded bibliography is checked against this PDF and documented in the package manifest.

## Portal state

PRA draft `es2026oct16_686`: authenticated campus account, Regular Article, Quantum information science; unsubmitted, with no files uploaded or author fields entered. Browser upload permission was explicitly declined and is not retried. The next file-information step needs the manuscript PDF and figure count.

PRL draft `es2026oct16_693`: separate unsubmitted Letter preparation, Quantum Information, Science, and Technology / Quantum Algorithms and Computation; no uploaded files, no author fields entered and no short manuscript prepared. The original instruction to stop before final submission still applies.

ORCID authentication, author declarations, and profile-name/affiliation verification remain pending. No fee, licence, copyright agreement or final submission has been accepted. Formatting and file checks do not validate proofs, novelty, significance or author approval.
