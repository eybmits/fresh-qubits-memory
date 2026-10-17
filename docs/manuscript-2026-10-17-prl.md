# Manuscript import: 17 October 2026, PRL revision

The current manuscript is **The Fundamental Memory Ceiling of Noisy Quantum Reservoirs** by Markus Baumann, Jonas Stein, and Claudia Linnhoff-Popien. It is a PRL-format Letter followed by Supplemental Material. Current artifacts are the [PDF](../paper/memory_limits_prl_2026-10-17.pdf), [editable source](../paper/prl-source/memory_limits_prl.tex), [provenance](../paper/versions/2026-10-17-prl-v1/provenance.json), and [prepared arXiv source package](../paper/submission/arxiv-2026-10-17/arxiv-source.zip).

This record distinguishes the received manuscript's scientific claims from checks performed during import. It does not establish proof correctness, novelty, journal eligibility, arXiv acceptance, or publication status.

## Received files and author integration

The user supplied `memory_limits_prl_source (1).zip`, `memory_limits_prl (4).tex`, `memory_limits_prl (16).pdf`, and `fig4.pdf`. The standalone TeX equals the ZIP's `memory_limits_prl.tex` byte for byte, with SHA-256 `6b2d3fb06c42463f4948018af81ea84ac97ce48ecf94296791a336057d7127d2`. Both copies of Figure 4 have SHA-256 `5f04d161888130327252cb5368987680d5f5d21ffaab1feaeb9c67314f3a9263`. The received PDF carries the new title and a single-author byline.

The user explicitly confirmed retaining the previously approved three authors and institutional metadata. The active edition therefore restores:

| Author | ORCID |
| --- | --- |
| Markus Baumann | [0009-0007-3575-1006](https://orcid.org/0009-0007-3575-1006) |
| Jonas Stein | [0000-0001-5727-9151](https://orcid.org/0000-0001-5727-9151) |
| Claudia Linnhoff-Popien | [0000-0001-6284-9286](https://orcid.org/0000-0001-6284-9286) |

All three have the two approved affiliations: Quantum Applications and Research Laboratory (QAR-Lab), and Chair of Mobile and Distributed Systems, Department of Computer Science, Ludwig-Maximilians-Universität München, Oettingenstraße 67, 80538 München, Germany. The contact remains `markus.baumann@campus.lmu.de`. PDF author metadata is consistent with the byline. The same three-author block, ORCID links, and two affiliations are restored in the separate Supplemental Material title block. The active date is fixed to October 17, 2026 for reproducible builds. The array package is pinned to its compatible historical interface for the installed REVTeX toolchain. In the AI-use acknowledgment, the two instances of “The author” become “Markus Baumann,” preserving the original author’s disclosure without attributing that AI use or those checks to the coauthors. The source README names all three authors and records these integration changes.

These integration changes are distinct from the immutable received files. Detailed hashes and final artifact checks belong to the linked provenance.

## Supplied scientific changes

This is a substantive revision of the supplied manuscript, not a conversion of revision 5's layout alone. The Letter uses `aps,prl,twocolumn,superscriptaddress,floatfix` in REVTeX 4.2, has four main figures, and is followed by Supplemental Material with seven additional figures. The new title and abstract are retained.

The upper bound now has the simplified form

\[
W(\varepsilon)\le\left\lceil2^{k/(1-q)^2}\ln(1/\varepsilon)\right\rceil
\quad(k\ge4),
\]

with a separate small-\(k\) form, and the underlying contraction constant is improved. The Supplemental Material reorganizes the proof and its supporting statements. The repetition construction retains the exponential lower scaling. The text explicitly distinguishes an upper bound for all admissible reservoirs from an existence construction attaining the scaling; more fresh qubits alone do not guarantee an improvement for an arbitrary reservoir.

The supplied numerical campaign also changes: six realizations per configuration, sizes up to nine qubits, one differing input and differing earlier histories, five common continuations, and washout from three initial states until their sampled residual is below \(10^{-6}\). Cold-input, noise, and evolution-time controls are included, together with an extended-history validation. The main campaign has 30 configurations and 180 realizations. These data are separate from revision 5 and from the independent repair simulations elsewhere in the repository.

## Import checks and bounded replay

The supplied scripts were inspected before execution in an extracted working copy. The following checks completed:

| Check | Observed result |
| --- | --- |
| Source consistency | Standalone TeX and Figure 4 match their ZIP versions exactly |
| References and inputs | All 38 citation keys have BBL entries; all eleven referenced figure PDFs are present |
| `checks/verify_simple_proof.py` | Sampled injection-norm and elementary inequality checks returned their expected signs; maximum sampled normalized 2-norm ratio was 0.6386 |
| `checks/verify_constants.py` | New direct/closed contraction constants differed by at most \(1.965\times10^{-31}\); sampled bound margins had expected signs |
| `sim/test_sim.py` | Asserted linearity check passed; printed depolarization and repetition-response comparisons agreed to displayed precision |
| `sim/quoted_numbers.py` | Quoted values agreed with the supplied JSON, including Ising means 16.2–18.2 for the size scan at \(k=1\); the saved extended-history validation gained at most one step in 24 realizations |
| Small independent campaign replay | Six Ising and six Haar realizations at \(n=3,k=1,q=0.9\) reproduced every saved depth, per-continuation depth, and washout step count exactly |

For these twelve replayed realizations, maximum forgetting-curve differences were \(8.372\times10^{-14}\) for Ising and \(1.555\times10^{-14}\) for Haar. Washout residual differences were below \(8.3\times10^{-16}\). The full large campaign was not rerun. Some supplied checks print diagnostic values rather than asserting every comparison; they are finite consistency checks, not a proof verifier.

The constants checker used mpmath from an existing archived environment through `PYTHONPATH`; the default Python lacked that dependency. Other scientific checks used NumPy/SciPy and `OPENBLAS_NUM_THREADS=1`. The supplied word counter reported approximately 3542 word equivalents and 594 approximate abstract characters; the supplied README says 590 characters. This is a local count, not an editorial determination.

Commands from an extracted source directory:

```bash
OPENBLAS_NUM_THREADS=1 python3 checks/verify_simple_proof.py
OPENBLAS_NUM_THREADS=1 python3 checks/verify_constants.py
python3 checks/wordcount.py memory_limits_prl.tex .
(cd sim && OPENBLAS_NUM_THREADS=1 python3 test_sim.py)
(cd sim && python3 quoted_numbers.py)
```

The small replay called `campaign.run_config(model, 3, 1, 0.9)` for `model` equal to `ising` and `haar`, retaining all six realizations. No new data were written into the supplied campaign outputs.

## Three interpretation qualifications

1. **Finite history sampling.** The reported numerical depth maximizes over finitely many history pairs and continuations. It is an estimator/lower witness of the supremum in the formal definition, not a certified maximization over all possible histories. The extended search is useful empirical evidence but does not change that distinction.
2. **Comparison across reset widths.** The campaign's unitary random seed depends on \(k\). A curve changing \(k\) therefore compares ensembles of different unitaries; it is not a paired intervention on one fixed reservoir unitary. Within a fixed `(model,n,k)`, the cold-input, noise, and evolution-time controls reuse the corresponding random streams.
3. **Continuous versus integer depths.** Figure 4(b) plots continuous threshold crossings, whereas the formal memory depth is integer-valued. At \(k=5,q=0.9,\varepsilon=0.01\), the single-qubit crossing is about 308.08, while the integer depth is 309; the full-state witness is 316. The continuous expression is a valid lower bound, but these conventions should not be treated as identical. This less-than-one-step difference does not alter the exponential scaling.

These qualifications are recorded without an unsolicited scientific rewrite. Historical audit notes also distinguish a size-independent uniform ceiling from the performance of an individual architecture below it, and the persistence of the upper bound under additional unital noise from attainability under arbitrary added noise. Finite numerical agreement does not establish the universal theorem or quantum advantage. No forecasting readout or hardware experiment was run for this import.

## Historical reproducibility and submission preparation

The active source is [paper/prl-source/](../paper/prl-source/). The older [paper/source/](../paper/source/) remains unchanged because independent historical experiments import its simulator. Earlier PDFs, received archives, datasets, and audit records are preserved; they are not silently replaced by this campaign.

The arXiv package is prepared separately from the received archive and the complete reproducibility source. The integrated manuscript builds to 22 pages: six pages of Letter/references and sixteen pages of Supplemental Material. BibTeX regeneration first reproduced the supplied BBL byte for byte. After replacing the publisher-URL placeholder in the supplement entry, the BBL was regenerated and verified again. The supplement contents use a smaller font to fit the expanded author block on S1. All 22 repository tests pass. These build and regression results are distinct from the finite scientific checks above. The final package/provenance record supplies package contents and fresh-package verification. Preparation does not assign an arXiv identifier, select a submission license on the user's behalf, establish endorsement, or constitute a final submission. Historical PRA/PRL portal drafts remain distinct from this arXiv preparation.
