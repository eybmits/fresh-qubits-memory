The Fundamental Memory Ceiling of Noisy Quantum Reservoirs -- Physical Review Letters version, source files
Markus Baumann, Jonas Stein, and Claudia Linnhoff-Popien
Quantum Applications and Research Laboratory (QAR-Lab), Ludwig-Maximilians-Universität München
Revision 9, October 19, 2026; 25 pages (6-page Letter and 19-page Supplemental Material).
Project repository: https://github.com/eybmits/fresh-qubits-memory (currently private).

Manuscript (REVTeX 4.2, prl option): one file with the Letter followed by the Supplemental Material
  pdflatex memory_limits_prl && bibtex memory_limits_prl && pdflatex memory_limits_prl && pdflatex memory_limits_prl
  memory_limits_prl.bbl is included for submission systems that do not run BibTeX.
  Fonts: Latin Modern (Type 1) with ToUnicode maps, so that the text layer of the PDF is searchable and copies
  correctly (ligatures, accented names).
  The Letter ends with the reference list; the Supplemental Material starts on a new page (pages S1-S19,
  equations, figures, tables and lemmas numbered S1, S2, ...) and cites the reference list of the Letter.
  For submission, the Letter alone (the file up to \bibliography{refs}) is the manuscript, and the Supplemental
  Material is uploaded as its own PDF (pages S1-S19 of the combined PDF). References cited only in the Supplemental
  Material appear in the reference list of the Letter, through the inclusive citation note in the
  Supplemental-Material reference. This archive (code and data) is the source archive named in the Data
  availability statement and in Sec. IX of the Supplemental Material; upload it with the Supplemental Material.

Length of the Letter (APS length guide, journals.aps.org/authors/length-guide; limit 3750 words)
  Counted with the method the guide recommends: the Letter is typeset with REVTeX after removing \maketitle
  (title, byline, abstract), the displayed equations, the acknowledgments, and the bibliography, and the words of
  the typeset text are counted with wordcount.tex from CTAN (hyphenated compounds and each part of a citation
  list count separately); equations and figures are added with the formulas of the guide.
  Typeset text: body, captions, data-availability statement           2792 words
  Displayed equations: 6 rows x 16 words                                96 words
  Fig. 1 (one-column, aspect 2.02): 150/2.02 + 20                       94 words
  Fig. 2 (two-column, aspect 2.88): 300/(0.5 x 2.88) + 40              249 words
  Fig. 3 (two-column, aspect 2.73)                                     259 words
  Fig. 4 (two-column, aspect 3.44)                                     214 words
  Total                                                               3705 words
  This is a local length estimate, not an APS editorial eligibility decision.
  Abstract: 595 plain-Unicode characters (PRL style-guide limit: 600; not counted above).
  Recount after every edit:  python3 checks/aps_wordcount.py memory_limits_prl.tex . /tmp/memory-limits-wordcount

Figures (final PDFs in this folder; sources in figures/)
  Every figure is produced at its printed size (7.05 in or 3.40 in wide) and included without scaling, so all
  text in all figures is set in 8 pt. One palette throughout: purple = input, blue = memory and the reservoir
  that attains the limit, red = noise and the limit, greys = standard reservoirs and references.
  Fig. 1   fig1.pdf  <- figures/fig1.tex (TikZ; two-panel scope of the theorem as nested classes)
  Fig. 2   fig2.pdf  <- figures/fig2.tex (TikZ; panel b, the reservoir, and the bottom row of boxes)
                       + fig2a.pdf <- figures/fig2a.py (panel a, square axes)
  Fig. 3   fig3.pdf  <- figures/fig3.tex (TikZ; panel b, the reservoirs A, B, C and their memory windows; the
                       qubit lattices in isometric view use the TikZ library shadows.blur, TeX Live package
                       pgf-blur)
                       + fig3a.pdf <- figures/fig3a.py (panel a, the limit versus k)
  Fig. 4   fig4.pdf  <- figures/fig4.tex (TikZ; panel a) + fig4bc.pdf <- figures/fig4bc.py, which also prints the
                       exact memory depth of the copies without repair quoted in the text (grey in panel b: the
                       region at or below these memory depths)
  Fig. S1-S7  figS1.pdf ... figS7.pdf <- figures/figS.py
  Shared style: figures/figstyle.py (matplotlib with usetex: Helvetica text, Computer Modern math; needs
  LaTeX with helvet and cm-super) and figures/tikzstyle.tex (same colours and size).
  Build, from inside figures/:
    pdflatex fig1.tex
    python3 fig2a.py && pdflatex fig2.tex
    python3 fig3a.py && pdflatex fig3.tex
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
  checks/aps_wordcount.py     length of the Letter with the method of the APS length guide (wordcount.tex)
  checks/wordcount.py         simpler length estimate from the LaTeX source

Justification for the editors (preserved exactly from the approved previous version)
How long can a noisy quantum system remember past inputs? We establish a universal memory ceiling under local Markovian depolarizing noise: with \(k\) qubits refreshed per step, the optimal memory depth scales as \(\exp[\Theta(k)]\) at fixed noise strength and accuracy. Our size-independent upper bound covers all admissible dynamics and input encodings. A measurement-free error-correction scheme achieves the same exponential scaling, establishing an optimal resource law. This is a limit on an entire class of quantum dynamics, not on one computing architecture. By identifying entropy removal as the resource governing memory, our result connects quantum information, nonequilibrium physics, and physical computing.

The approved cover letter and 100-word justification are unchanged in this revision.
The editorial framing and Figure 1 were updated; the exact theorem, abstract, code and data remain unchanged.
This archive does not submit
or publish them. Numerical campaign data are preserved; current verification is bounded to
repository/simulator tests and numerical checks of stated proof steps.
