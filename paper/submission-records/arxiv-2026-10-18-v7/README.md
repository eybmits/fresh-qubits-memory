# arXiv upload record - 18 October 2026

Revision 7 was uploaded to arXiv draft **8248308**. The portal successfully
compiled the sole main file, `memory_limits_prl.tex`, with pdfLaTeX / TeX Live
2025. Title, three authors, abstract, comments, and primary category `quant-ph`
were saved. The user accepted the submission agreement and selected arXiv's
perpetual, non-exclusive license in the browser.

**Last observed state: uploaded and prepared, not finally submitted.** The Submit
button was left unclicked. This temporary draft number is not a public arXiv
identifier, and no publication or moderation decision is claimed. The
[private portal preview](https://arxiv.org/submit/8248308/preview) requires the
submitter's account and may later expire or change.

## Evidence and checks

- [arXiv-generated PDF](arxiv-generated-8248308.pdf), 24 pages including the supplement.
- [Saved portal preview](preview-before-submit.jpg), showing metadata, license,
  category, successful PDF/HTML generation, and the still-open Submit button.
- [Upload verification](upload-verification.json), including source and PDF hashes.
- [Artifact manifest](artifact-manifest.json), hashes of the preserved handoff files.

The uploaded [source ZIP](../../submission/arxiv-2026-10-18-v7/arxiv-source.zip)
is the package prepared from commit `3a13086be2df5dce05899c736832c4e4b8700436`.
It is preserved unchanged. The downloaded PDF's extracted text on pages 2-24
is byte-identical to the canonical local PDF. Page 1 matches after removing the
arXiv draft watermark and normalizing whitespace. Pages 1, 7, and 24 were
visually checked without observed clipping, overlaps, or missing glyphs.

The file scanner reported seven missing dependencies in retained figure-source
documents that are not compilation targets. The actual main document compiled
successfully. All uploaded files, including the matched bibliography and code/data,
were retained. Poppler reported a font-type mismatch after arXiv added its
watermark; the inspected pages showed no visible defect. HTML generation was
reported successful by the portal, but HTML content was not independently checked.

The versioned preparation packages and their original `not_uploaded` metadata
remain historical snapshots from before the upload. This record documents the
later portal action without rewriting those artifacts. No manuscript, proof,
figure, simulator, numerical dataset, PRL package, or repository visibility was
changed during the upload. No further numerical campaign was run.
