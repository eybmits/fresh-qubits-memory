"""Numerical campaign of the Letter and the Supplemental Material (Sec. VII): memory depth W(eps) of standard
reservoirs (all-to-all transverse-field Ising, Haar random) with k reinitialized input qubits under depolarizing
noise of strength q, eps = 0.01.

Usage:  python3 campaign.py main  [ising|haar]   n = 3..9 for k = 1, 2 and n = 8 for k = 3, 4; q = 0.9
        python3 campaign.py cold  [ising|haar]   n = 8, k = 2..4, additional input qubits reinitialized in |0>
        python3 campaign.py noise [ising|haar]   n = 6, k = 1, q = 0.95 ... 1 (weak-noise and noiseless limit)
        python3 campaign.py tau                  Ising, n = 6, k = 1, q = 0.9, evolution time J*dt = 0.3..30
Reservoir unitaries are drawn from a random stream that depends only on (model, n, k), so all modes use the same
six reservoirs for given n and k: the cold runs, the noise scan, and the evolution-time scan (same couplings)
differ from the main runs only in the parameter that is varied. Results are written to
results_<mode>[_<model>].json; merge.py combines them into results_main/cold/noise/tau.json."""
import json, sys, time
import numpy as np
from qrc_sim import ising_unitary, haar_unitary, memory_depth, fn_state, cold_state

EPS = 1e-2
SEED = 2026
MODEL_ID = {"ising": 1, "haar": 2}


def streams(model, n, k):
    """Random streams for the reservoir unitaries and for the inputs of reservoirs (model, n, k)."""
    return (np.random.default_rng([SEED, MODEL_ID[model], n, k, 0]),
            np.random.default_rng([SEED, MODEL_ID[model], n, k, 1]))


def run_config(model, n, k, q, n_real=6, l_max=300, encode=fn_state, tau=10.0):
    rngU, rngI = streams(model, n, k)
    entry = dict(model=model, n=n, k=k, q=q, tau=tau, encoding="cold" if encode is cold_state else "input",
                 W=[], parts=[], curves=[], washout=[])
    for rep in range(n_real):
        U = ising_unitary(n, rngU, tau=tau) if model == "ising" else haar_unitary(n, rngU)
        r = memory_depth(U, n, k, q, rngI, encode=encode, eps=EPS, l_max=l_max)
        entry["W"].append(r["W"]); entry["parts"].append(r["parts"])
        entry["curves"].append(r["curve"]); entry["washout"].append(r["washout"])
    return entry


def configs(mode, model):
    if mode == "main":
        return ([dict(model=model, n=n, k=k, q=0.9) for k in (1, 2) for n in range(k + 2, 10)]
                + [dict(model=model, n=8, k=k, q=0.9) for k in (3, 4)])
    if mode == "cold":
        return [dict(model=model, n=8, k=k, q=0.9, encode=cold_state) for k in (2, 3, 4)]
    if mode == "noise":
        return [dict(model=model, n=6, k=1, q=q, l_max=6000) for q in (0.95, 0.98, 0.99, 0.995, 0.999, 1.0)]
    if mode == "tau":
        return [dict(model="ising", n=6, k=1, q=0.9, tau=tau, l_max=400) for tau in (0.3, 1.0, 3.0, 10.0, 30.0)]
    raise ValueError(mode)


def main():
    mode = sys.argv[1]
    models = ["ising"] if mode == "tau" else ([sys.argv[2]] if len(sys.argv) > 2 else ["ising", "haar"])
    tag = mode if mode == "tau" or len(models) > 1 else f"{mode}_{models[0]}"
    out, t0 = [], time.time()
    for model in models:
        for c in configs(mode, model):
            e = run_config(**c)
            out.append(e)
            res = max(w["residual"] for w in e["washout"])
            steps = max(max(w["steps"]) for w in e["washout"])
            print(f"[{tag}] {e['model']} n={e['n']} k={e['k']} q={e['q']} tau={e['tau']} {e['encoding']}: W={e['W']}  "
                  f"(washout <= {steps} steps, residual {res:.1e}; {time.time() - t0:.0f}s)", flush=True)
            json.dump(out, open(f"results_{tag}.json", "w"))


if __name__ == "__main__":
    main()
