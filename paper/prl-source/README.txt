The Fundamental Memory Ceiling of Noisy Quantum Reservoirs -- Physical Review Letters version, source files
Markus Baumann, Jonas Stein, and Claudia Linnhoff-Popien, LMU Munich

Repository edition: 18 October 2026, revision 3. The three confirmed authors, ORCIDs
and one shared QAR-Lab/chair/LMU address are retained. The date is fixed and the
array package is pinned to the arXiv-documented REVTeX-compatible release.
Numerical prose/captions explicitly distinguish sampled estimates, unitary
ensembles across k, and continuous crossings from integer depths.
Reference [28] and the code section link to the GitHub repository; the author
will make the currently private repository public separately.

Manuscript (REVTeX 4.2, prl option): one file with the Letter followed by the Supplemental Material
  pdflatex memory_limits_prl && bibtex memory_limits_prl && pdflatex memory_limits_prl && pdflatex memory_limits_prl
  memory_limits_prl.bbl is included for submission systems that do not run BibTeX.
  The Letter ends with the reference list; the Supplemental Material starts on a new page (pages S1-S16,
  equations, figures, tables and lemmas numbered S1, S2, ...) and cites the reference list of the Letter.
  For submission, the Letter alone (the file up to \bibliography{refs}) is the manuscript, and the Supplemental
  Material is uploaded as its own PDF (pages S1-S16 of the combined PDF). References cited only in the Supplemental
  Material appear in the reference list of the Letter, through the note "which includes Refs. [36-38]" of the
  Supplemental-Material reference. This archive (code and data) is the source archive named in the Data
  availability statement and in Sec. IX of the Supplemental Material; upload it with the Supplemental Material.

Length of the Letter (APS length guide, journals.aps.org/authors/length-guide; limit 3750 words)
  Text (2398), captions (260), data-availability statement (25)       2683 words
  Displayed equations: 7 rows x 16 words                             112 words
  Fig. 1 (one-column, aspect 1.43): 150/1.43 + 20                    125 words
  Fig. 2 (two-column, aspect 2.88): 300/(0.5 x 2.88) + 40            249 words
  Fig. 3 (two-column, aspect 3.81)                                   197 words
  Fig. 4 (two-column, aspect 3.44)                                   214 words
  Total                                                            ~3580 words
  Abstract: 590 characters (limit of the PRL instructions: 600 characters; not counted in the 3750 words).
  Recount after every edit:  python3 checks/wordcount.py memory_limits_prl.tex .

Figures (final PDFs in this folder; sources in figures/)
  Every figure is produced at its printed size (7.05 in or 3.40 in wide) and included without scaling, so all
  text in all figures is set in 8 pt. One palette throughout: purple = input, blue = memory and the reservoir
  that attains the limit, red = noise and the limit, greys = standard reservoirs and references.
  Fig. 1   fig1.pdf  <- figures/fig1.tex (TikZ; scope of the theorem as nested classes)
  Fig. 2   fig2.pdf  <- figures/fig2.tex (TikZ; panel b, the reservoir, and the bottom row of boxes)
                       + fig2a.pdf <- figures/fig2a.py (panel a, square axes)
  Fig. 3   fig3.pdf  <- figures/fig3.py (the memory limit, schematic)
  Fig. 4   fig4.pdf  <- figures/fig4.tex (TikZ; panel a) + fig4bc.pdf <- figures/fig4bc.py, which also prints the
                       exact memory depth of the copies without repair quoted in the text
  Fig. S1-S7  figS1.pdf ... figS7.pdf <- figures/figS.py
  Shared style: figures/figstyle.py (matplotlib with usetex: Helvetica text, Computer Modern math; needs
  LaTeX with helvet and cm-super) and figures/tikzstyle.tex (same colours and size).
  Build, from inside figures/:
    pdflatex fig1.tex
    python3 fig2a.py && pdflatex fig2.tex
    python3 fig3.py
    python3 fig4bc.py && pdflatex fig4.tex
    python3 figS.py
  The scripts read the data in ../sim and write the PDFs into figures/.

Simulations and exact numbers (Python 3 with numpy, scipy, mpmath)
  sim/qrc_sim.py         density-matrix simulator of reservoirs with input injection by reinitialization, and the
                         memory-depth estimator: two kinds of history pairs (one differing input; all earlier inputs
                         differing), five continuations, echo states prepared by a washout that runs until three
                         initial states agree within 1e-6
  sim/campaign.py        all simulation runs:  python3 campaign.py main|cold|noise [ising|haar]
                                               python3 campaign.py tau
                         The reservoir unitaries depend only on (model, n, k), so the cold runs, the noise scan and
                         the evolution-time scan use the same six reservoirs as the main runs.
  sim/run_all.sh         runs the whole campaign on two cores (about 30 minutes), merges the results (merge.py),
                         and validates the estimator (validate_pairs.py, about 15 minutes)
  sim/test_sim.py        validation of the simulator (linearity, exact response of the error-correcting reservoir)
  sim/validate_pairs.py  validation of the memory-depth estimator against a much larger set of history pairs
  sim/quoted_numbers.py  prints every simulation number quoted in the Letter and the Supplemental Material
  sim/rep_curve.py       full-state trace distance of the error-correcting reservoir (k = 5) and its memory depth
                         (316 time steps; 309 for the single-qubit readout)
  sim/exact_numbers.py   constants, half-lives, washout, cooling reservoir (exact arithmetic)
  JSON files: results_main, results_cold, results_noise, results_tau (simulation runs; the per-model files
  results_<mode>_ising/haar are the raw outputs that merge.py combines), validate_pairs, rep_curve, exact_numbers. Notation: in the code, the transverse field g of the Ising reservoir is called h,
  and the evolution time per step Delta t is called tau.

Checks
  checks/verify_constants.py  independent numerical check of the contraction rate
                              delta^-1 = 2^(beta_q k + (1+4q)/(1-q)), of the conditions (a+1) delta <= 1 and
                              delta <= 1 - 2^-bartheta (bartheta = 1 - theta) used in Proposition S4, and of the
                              simple forms 2^(k/(1-q)^2) (k >= 4) and 2^((k+1)/(1-q)^2) (k >= 1)
  checks/verify_simple_proof.py  checks of the elementary steps of the Supplemental proof (2-norm bound for the
                              injection step on random instances, the single inequality behind Proposition S4,
                              and the concentration of the examples)
  checks/wordcount.py         length of the Letter according to the APS length guide

Justification for the editors (PRL asks for about 100 words at submission)
  We prove a fundamental resource limitation for an entire class of open quantum systems. With k fresh qubits
  per time step, no noisy quantum dynamics retains information for longer than exp[O(k)] time steps, however
  large it is: a universal no-go result that covers every architecture within a well-defined noise model,
  including ones not yet conceived, and whose exponential scaling an explicit reservoir attains. The result
  identifies entropy removal, not size, as the resource that limits memory, and it reaches beyond quantum
  reservoir computing to the stabilization of information in noisy quantum systems in general, including
  measurement-free error correction.
