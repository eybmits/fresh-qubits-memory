# Physical Review A template check — 16 October 2026

The updated manuscript uses the official APS REVTeX 4.2 class with the Physical Review A journal option:

```latex
\documentclass[aps,pra,reprint,superscriptaddress,floatfix]{revtex4-2}
```

The supplied source already used the correct class with `twocolumn`. Replacing that option with `reprint` makes the intended journal-style layout explicit; it does **not** imply that the earlier two-column version was invalid. APS documents `reprint` for journal-style output and `preprint` for a one-column, double-spaced, 12-point manuscript. [APS REVTeX FAQ](https://journals.aps.org/revtex/revtex-faq)

## Source and submission checks

| Item | Checked state |
| --- | --- |
| Journal and class | `paper/source/memory_limits.tex` uses `revtex4-2`, `aps`, `pra`, and `reprint`. |
| Bibliography | The working source retains `\bibliography{refs}`; BibTeX uses the class-selected `apsrev4-2` style, including article titles. The upload-source variant embeds the generated `.bbl` so it does not require a BibTeX run. |
| Authors | The latest supplied source contained only Markus Baumann. The previous explicit author instruction has been preserved: Markus Baumann, Jonas Stein, Claudia Linnhoff-Popien, in that order. |
| ORCID | All three author identifiers are linked in the byline using `orcidlink`: Markus `0009-0007-3575-1006`, Jonas `0000-0001-5727-9151`, Claudia `0000-0001-6284-9286`. This is separate from APS authentication. |
| Affiliations | All three authors carry both superscripts: QAR-Lab and the Chair of Mobile and Distributed Systems, Department of Computer Science, LMU Munich, Oettingenstraße 67, 80538 München. |
| Contact author | The byline now uses `\email[Contact author: ]{markus.baumann@campus.lmu.de}`. |
| Page layout | REVTeX controls margins, text fonts, and type size. No arbitrary margin, font-size, or line-spacing replacements were introduced. The existing `\raggedbottom` remains a layout preference. |
| Abstract | One paragraph, 231 whitespace-separated words; below the APS limit of 500 words. |
| Data availability | A separate section follows the acknowledgments and precedes the appendices. |
| Article type | The rebuilt manuscript has 17 pages. PRA Regular Articles have no length limit. |
| Initial upload | A single manuscript PDF includes text, figures, tables, references, and appendices. Supplemental files are separate. APS requests production source files upon acceptance; they are prepared here in advance. |

PRA points authors to the APS REVTeX templates and encourages reference titles. Its current guidelines specify no length limit for Regular Articles. [PRA author guidelines](https://journals.aps.org/pra/authors)

The current APS style guide is dated February 2026. It supports the contact-author prefix and superscript affiliations, specifies the abstract limit, and places data availability after acknowledgments and before appendices. [APS Journals Style Guide](https://res.cloudinary.com/apsphysics/image/upload/APS_Journals_Style_Guide_Authors022326_guzwhx.pdf)

Initial submission requires a PDF; source files are requested upon acceptance. APS controls the final production typography, so a REVTeX draft is not an exact prediction of the eventual published pagination. [APS web submission guidelines](https://journals.aps.org/authors/web-submission-guidelines-physical-review)

## Build and visual verification

The integrating agent reported the following checks on the rebuilt submission version:

- Compilation completed with 17 pages, no unresolved references, and no overfull boxes.
- All fonts are embedded Type 1 fonts.
- All eight figures and five tables are visible in the rendered PDF.
- Nonfatal `nameref` and deferred-float warnings remain; they did not prevent the verified figures and tables from appearing.

This records formatting and build evidence. It does not certify the mathematical claims, novelty, author approval, or the manuscript's assertion about human verification of AI-assisted work. No manuscript has been submitted as part of this check.

## Author-metadata follow-up and portal status

After the ORCID and affiliation correction, the integrating agent rendered all 17 pages again, inspected the first-page byline and both affiliation markers, and verified all three exact ORCID URL annotations. The abstract and mathematical body are unchanged. The new PDF SHA256 is `e0d8176e9f3ba77a8ab3c5c7a0e4c4bde36b492422a2703dc1999a471b9bdff6`.

APS account login is authenticated and unsubmitted draft `es2026oct16_686` exists for PRA Regular Article / Quantum Information Science. No files have been uploaded and no author fields entered. Browser upload permission was explicitly declined; the current file-information step needs the PDF and figure count, and upload must not be retried. ORCID authentication, verification/correction of the portal's “Dr. Markus” name and unaffiliated state (academic title not verified), and final author declarations remain pending. Nothing has been submitted.
