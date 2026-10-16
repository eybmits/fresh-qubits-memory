"""Extra runs for Appendix F: dependence on the Ising evolution time and the weak-noise limit."""
import json, time
import numpy as np
from qrc_sim import ising_unitary, haar_unitary, memory_curves, depth_from_curves
EPS = 1e-2
rng = np.random.default_rng(99)
out = dict(tau=[], qsat=[])
t0 = time.time()
def depth(U, n, k, q, l_max):
    best = 0
    for samp in (None, None, (lambda: 0.0), (lambda: 0.5), (lambda: 1.0)):
        cv = memory_curves(U, n, k, q, rng, n_branch=1, t_wash=80, gap=0, l_max=l_max, d_stop=3e-3, u_sampler=samp)
        best = max(best, depth_from_curves(cv, EPS))
    return int(best)
for tau in (0.3, 1.0, 3.0, 10.0, 30.0):
    Ws = [depth(ising_unitary(6, rng, tau=tau), 6, 1, 0.9, 400) for _ in range(6)]
    out["tau"].append(dict(tau=tau, W=Ws))
    print(f"tau={tau}: {Ws} ({time.time()-t0:.0f}s)", flush=True)
    json.dump(out, open("results_extra.json", "w"))
for q in (0.995, 0.999, 1.0):
    for model in ("ising", "haar"):
        Ws = [depth(ising_unitary(6, rng) if model == "ising" else haar_unitary(6, rng), 6, 1, q, 6000) for _ in range(3)]
        out["qsat"].append(dict(model=model, q=q, n=6, W=Ws))
        print(f"q={q} {model}: {Ws} ({time.time()-t0:.0f}s)", flush=True)
        json.dump(out, open("results_extra.json", "w"))
