The Memory Limits of Noisy Quantum Reservoirs -- source files

Manuscript (REVTeX 4.2, aps,pra,reprint; Physical Review A style; orcidlink)
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
  Copy the eight final PDFs to the manuscript folder after generation:
    cp fig1.pdf fig2.pdf fig3.pdf fig4.pdf figA1.pdf figA2.pdf figA3.pdf figA4.pdf ..

Simulations and exact numbers (Supplemental Material; Python 3 with numpy, scipy; matplotlib for figures)
  sim/qrc_sim.py         density-matrix simulator of reservoirs with input injection by reinitialization
  sim/test_sim.py        validation (linearity, exact repetition-code response)
  sim/check_washout.py   convergence of the washout
  sim/campaign.py        main runs (python3 campaign.py main) and noise scan (python3 campaign.py qscan)
  sim/campaign_extra.py  evolution-time scan and weak-noise limit
  sim/rep_curve.py       full-state trace distance of the repetition-code reservoir (k = 5)
  sim/exact_numbers.py   rational majority tails and floating-point constants, half-lives, washout and cooling
  The JSON files contain the results used in the figures.
  Notation: in the code, the transverse field g of the Ising reservoir is called h, and the
  evolution time per step Delta t is called tau.

Repository integration (16 October 2026, revision 5)
  Supplied title, abstract and scientific revisions retained. Restored author order:
  Markus Baumann, Jonas Stein, Claudia Linnhoff-Popien, with verified ORCID IDs
  and both QAR-Lab and Chair of Mobile and Distributed Systems affiliations at LMU.
  Four table preambles use native paragraph columns for REVTeX compatibility.
  Date fixed to 16 October 2026; PDF metadata and contact-author prefix supplied.
  New AI-assistance wording retained, with its singular verification attribution
  explicitly naming Markus Baumann. This assertion still requires author review.
  Original ZIP/PDF and the preceding final sources are archived separately.

Venue status
  This is the expanded full manuscript in PRA format, not a PRL-length Letter.
  The PRL portal draft is unsubmitted; no PRL-ready manuscript has been uploaded.

Numerical scope
  Simulator and saved datasets are unchanged from revision 4. Sampled history
  depths are lower witnesses, not certified maximization over every history.
  No forecasting readout is trained. Build checks are not proof verification.
