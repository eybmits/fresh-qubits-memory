# Experiment protocols

Implemented follow-up: [16 October numerical validation protocol](empirical-2026-10-16.md), with [results and limitations](../results/empirical-2026-10-16/REPORT.md). It includes an explicitly labeled rare-event follow-up declared after the initial direct-sampling run.

The implemented baseline is `python scripts/reproduce_table1.py --output-dir results/table1` (run from the repository root after installation). It computes the exact binomial majority error and the corresponding readable lifetime from Eqs. (2), (3), (4) and (28). No Monte Carlo data or hardware runs are involved.

For each future experiment, add a protocol containing its research question, source equations, parameter grid, expected controls, runtime budget, random seeds if applicable, and acceptance criteria before a large run. Save small configuration files here and interpreted results under `results/`. See `docs/research-plan.md` for proposed work; those proposals are not implemented experiments.
