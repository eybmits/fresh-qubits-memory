"""Numerical campaign for 'The Memory Limits of Noisy Quantum Reservoirs' (Sec. V A, Appendix F).
Memory depth W(eps) of standard reservoirs (all-to-all transverse-field Ising, Haar random) with
k reinitialized input qubits (Fujii-Nakajima encoding) under depolarizing noise of strength q.
Results are written to results_<tag>.json."""
import json, sys, time
import numpy as np
from qrc_sim import ising_unitary, haar_unitary, memory_curves, depth_from_curves

EPS = 1e-2

def run(tag, configs, n_real, seed, l_max, d_stop):
    rng = np.random.default_rng(seed)
    out = []
    t0 = time.time()
    for (model, n, k, q) in configs:
        Ws, curves_rand = [], []
        for rep in range(n_real):
            U = ising_unitary(n, rng) if model == "ising" else haar_unitary(n, rng)
            best = 0
            samplers = [None, None, (lambda: 0.0), (lambda: 0.5), (lambda: 1.0)]
            for si, samp in enumerate(samplers):
                cv = memory_curves(U, n, k, q, rng, n_branch=1, t_wash=60, gap=0, l_max=l_max,
                                   d_stop=d_stop, u_sampler=samp)
                best = max(best, depth_from_curves(cv, EPS))
                if si == 0:
                    curves_rand.append(cv[0].tolist())
            Ws.append(int(best))
        out.append(dict(model=model, n=n, k=k, q=q, W=Ws, curves=curves_rand))
        print(f"[{tag}] {model} n={n} k={k} q={q}: W={Ws}  ({time.time()-t0:.0f}s)", flush=True)
        json.dump(out, open(f"results_{tag}.json", "w"))

if __name__ == "__main__":
    which = sys.argv[1]
    if which == "main":
        cfg = []
        for model in ("ising", "haar"):
            for k in (1, 2):
                for n in range(k + 2, 10):
                    cfg.append((model, n, k, 0.9))
            for k in (3, 4):
                cfg.append((model, 8, k, 0.9))
        run("main", cfg, n_real=6, seed=2026, l_max=300, d_stop=3e-3)
    elif which == "qscan":
        cfg = []
        for q in (0.95, 0.98, 0.99):
            for model in ("ising", "haar"):
                for n in (4, 6, 8):
                    cfg.append((model, n, 1, q))
        run("qscan", cfg, n_real=3, seed=7, l_max=3000, d_stop=3e-3)
