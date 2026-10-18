# PRL revision 5 import audit

Scope: bounded comparison of received inputs with HEAD `5a511adca5b240f63a3aaf2ca4c89c704336ae97`, source/package consistency, selected new statements, and the APS length calculation. This is not a full independent proof review or a new simulation campaign.

## Input consistency

- Standalone source ZIP, source ZIP inside the submission ZIP, and source ZIP inside the Zenodo ZIP contain identical 54 regular files.
- The standalone TeX exactly matches the source archive main TeX.
- Received combined PDF has 24 pages; Letter has 6 and Supplemental Material has 18. SM page text matches exactly after normalized whitespace. Letter text matches after removing whitespace; extraction-only spacing differences around caption titles/formulas and bibliography journal-volume boundaries explain the first normalized-text mismatch.
- All 13 JSON datasets and every `sim/` source file are byte-identical to HEAD. Both proof diagnostic scripts are byte-identical. No full numerical campaign needs rerunning for the manuscript import alone.
- New source adds `checks/aps_wordcount.py` and `figures/fig3a.py`/PDF, replaces the old fig3b panel, restyles figures, changes Fig.4(b) gray shading, and adds font/ToUnicode and unique SM figure/table hyperref anchors. Fig.4 numerical formulas and inputs are unchanged.

## Scientific and presentation changes

- Main Theorem upper-bound accuracy range is explicitly separated as 0<epsilon<1; lower bound retains 0<epsilon<q. The upper proof already supported this range.
- New SM memory-capacity paragraph derives a correlation-capacity upper bound under bounded readout norm, iid inputs, and conditional zero-mean readout noise with a positive lower variance bound. The covariance estimate and geometric-tail summation are consistent with these assumptions. This is a conditional statement, not a general noise-free bound on correlation capacity. Root made positive finite input variance and positive noise scale/finite unconditional noise variance explicit.
- The majority-refresh construction, contraction formula, core constants, and saved numerical results are unchanged. Most SM changes expand inline derivations into displayed equations, increasing the supplement from 16 to 18 pages.
- Main realization example changes 124 to 120 qubits, and Dao2026 moves to SM-only citations. This import audit did not re-review that cited hardware paper.
- Received files remove three-author metadata, ORCIDs, shared QAR-Lab/LMU affiliation, project URL, and the earlier finite-estimator / independent-k / continuous-threshold qualifications. Root restored the accepted metadata and qualifications.
- Fig.3 caption again claimed C reaches further back; root restored the distinction between a higher attainable ceiling and a guarantee for a given architecture. Root likewise clarified abstract and washout wording.
- Supplied AI acknowledgment now mentions GPT-6 Astra as well as the already user-confirmed Claude Opus 5.5. No tool-version truth claim independently certified by this audit.
- SM reference moves from [28] to [27] because a citation moved out of the introduction. All 38 references remain. Retain code URL in the SM entry with its new actual number, rather than forcing old numbering.
- Supplied 93-word justification differs from last explicitly approved 100-word justification. Root retains the explicit user wording.

## APS count

Primary guidance checked 18 October 2026: https://journals.aps.org/authors/length-guide and https://journals.aps.org/prl/authors . APS specifies 3750 word equivalents, excluding title/byline/abstract/acknowledgments/references, and provides equation/figure equivalents and a REVTeX/CTAN wordcount.tex procedure.

- Received counter reproduced 3670, but ignored failed subprocesses and omitted nofootinbib. During counting, REVTeX automatically loaded the bibliography and produced undefined-control errors. Nofootinbib alone did not cure the automatic bibliography.
- Assigned canonical `checks/aps_wordcount.py` now uses argument-list subprocesses (no shell), checks all return codes, disallows shell escape, verifies references and TeX errors, uses nofootinbib, and disables the counting-copy auto-bibliography. It keeps full-source references resolved in a precursor and never edits the manuscript. Unsupported tables/wide/display-math variants are rejected instead of silently miscounted. Machine-readable count.json is saved.
- Fixed received-input result: 2711 text +112 equation equivalents +847.4076189453992 figure equivalents =3670.407618945399; rounded3670. No TeX errors.
- Integrated-source result: 2729 text +112 +847.4076189453992 =3688.407618945399; rounded3688. The restored qualifications add 18 typeset words. Final count/source SHA256 is recorded in `final-count.json`; the main-text count is unchanged by the final SM-only Table S2 clarification. No TeX errors or unresolved references. This is a local estimate, not an APS editorial decision.

## Zenodo boundary

Received `.zenodo.json` proposes open access and CC BY 4.0; the instructions propose publishing and obtaining a DOI. These are document contents, not user authorization. Preserve originals; prepare updated draft metadata and source archive only, without selecting a license, publishing, or inventing a DOI.

Supporting records: source-comparison.json, supplied-pdf-consistency.json, integrated-wordcount/count.json, received-fixed-wordcount/count.json, and bounded source diffs in this directory.

## Final visual and split-PDF verification

- Reviewed all 24 combined-PDF pages through rendered contact sheets, plus detailed byline/abstract, SM byline/TOC, Figures 3/4, reference [27], memory-capacity derivation, and final code section.
- The final Table S2 wording now states that unital noise does not raise the memory upper bound. Only combined page18/S12 changed pixels after this clarification; visually rechecked and clean. Other23 pages are pixel-identical to the reviewed set.
- Final combined PDF SHA256 `90f0e19e58f22fcdac6fc5c01ce5864adc6b4f87641498bcb53924884c956a62` has 24pages. Standalone Letter6pages and SM18pages have identical extracted characters to the corresponding combined pages. Every SM page is pixel-identical. Letter pages1-5 are pixel-identical; its reference-only final page rebalances into two columns and was visually checked, with no content difference.
- All140 font records are embedded Type1; the main LatinModern prose fonts have ToUnicode maps. 76 imported figure-font records do not have explicit ToUnicode maps, so this is not a claim that every font has such maps.
- Three approved ORCID links are present on each main/SM byline. One shared address is printed per byline. GitHub URL is linked in reference[27] (across pages5-6) and the final code section. Metadata lists all three authors. No clipping, overlaps, missing glyphs, or broken layout were observed.
