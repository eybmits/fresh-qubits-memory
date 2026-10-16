The Memory Limits of Noisy Quantum Reservoirs -- source files

Manuscript (REVTeX 4.2, aps,pra,reprint; Physical Review A style)
  pdflatex memory_limits && bibtex memory_limits && pdflatex memory_limits && pdflatex memory_limits
  memory_limits.bbl is included for submission systems that do not run BibTeX.

Figures (final PDFs are in this folder; sources in figures/)
  Every figure is produced at its printed size (7.05 in wide) and included without scaling, so all
  text in all figures is set in 8 pt. One palette is used throughout: purple = input, blue = reservoir
  dynamics and attainable memory, red = noise and the limit, greys = standard reservoirs and references.

  Fig. 1  fig1.pdf   <- figures/fig1.tex (TikZ; draws panel b and includes fig1a/c/d.pdf)
                        fig1a.pdf, fig1c.pdf, fig1d.pdf <- figures/fig1_panels.py
  Fig. 2  fig2.pdf   <- figures/fig2.py
  Fig. 3  fig3.pdf   <- figures/fig3.tex (TikZ; draws panel a and includes fig3bc.pdf)
                        fig3bc.pdf <- figures/fig3bc.py
  Fig. 4  fig4.pdf   <- figures/fig4.py   (data: sim/results_main.json, sim/rep_curve.json)
  Fig. 5-7 figA1.pdf, figA2.pdf, figA3.pdf <- figures/figA.py (data: sim/exact_numbers.json)
  Fig. 8  figA4.pdf  <- figures/figA4.py  (data: sim/results_*.json)

  Shared style: figures/figstyle.py (matplotlib with usetex: Helvetica text, Computer Modern math;
  needs LaTeX with the helvet and cm-super packages) and figures/tikzstyle.tex (same colours and size).
  Build, from inside figures/:
    python3 fig1_panels.py && pdflatex fig1.tex
    python3 fig2.py
    python3 fig3bc.py && pdflatex fig3.tex
    python3 fig4.py && python3 figA.py && python3 figA4.py
  The scripts read the data in ../sim and write the PDFs into figures/.
  After generating them, copy the eight completed figures to the manuscript folder:
    cp fig1.pdf fig2.pdf fig3.pdf fig4.pdf figA1.pdf figA2.pdf figA3.pdf figA4.pdf ..
  The intermediate fig1a.pdf, fig1c.pdf, fig1d.pdf and fig3bc.pdf stay in figures/.

Simulations and exact numbers (Supplemental Material; Python 3 with numpy, scipy, mpmath)
  sim/qrc_sim.py         density-matrix simulator of reservoirs with input injection by reinitialization
  sim/test_sim.py        validation (linearity, exact repetition-code response)
  sim/check_washout.py   convergence of the washout
  sim/campaign.py        main runs (python3 campaign.py main) and noise scan (python3 campaign.py qscan)
  sim/campaign_extra.py  evolution-time scan and weak-noise limit
  sim/rep_curve.py       full-state trace distance of the repetition-code reservoir (k = 5)
  sim/exact_numbers.py   rational majority tails, floating-point constants, half-lives, washout and cooling
  The JSON files contain the results used in the figures.

Repository integration (16 October 2026, revision 4)
  Approved title and abstract retained. Author order: Markus Baumann, Jonas Stein,
  Claudia Linnhoff-Popien. Contact: markus.baumann@campus.lmu.de.
  Three table preambles use native paragraph columns to avoid the array/REVTeX
  Extra \or error on TeX Live 2025. Cell contents are unchanged.
  The document date is fixed to 16 October 2026 for reproducible rebuilds.
  The original received ZIP/PDF and the previous source are archived separately.
  APS source upload ZIP embeds the final bibliography; this editable version uses BibTeX.

Interpretation of numerical material
  The simulations probe input-history retention under IID and constant continuations.
  Their depths are sampled lower witnesses, not exact maximization over all histories.
  No trained forecasting readout is evaluated. Fig. 1a uses illustrative Mackey-Glass data.
  Checks and source/PDF build validation do not establish proofs, novelty or acceptance.
