"""Combine the per-model result files of campaign.py (results_<mode>_ising.json, results_<mode>_haar.json) into
results_main.json, results_cold.json and results_noise.json; results_tau.json is written directly by campaign.py.
A merged file is only rewritten when both per-model files exist."""
import json, os
for mode in ("main", "cold", "noise"):
    parts = [f"results_{mode}_{model}.json" for model in ("ising", "haar")]
    if all(os.path.exists(p) for p in parts):
        json.dump(sum((json.load(open(p)) for p in parts), []), open(f"results_{mode}.json", "w"))
        print("merged", mode)
