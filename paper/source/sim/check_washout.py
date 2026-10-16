import numpy as np
from qrc_sim import *
rng = np.random.default_rng(5)
for model in ("ising", "haar"):
    for n in (4, 8):
        U = ising_unitary(n, rng) if model == "ising" else haar_unitary(n, rng)
        d = 2 ** n; k = 1; q = 0.9
        r1 = np.eye(d, dtype=complex) / d
        r2 = np.zeros((d, d), dtype=complex); r2[0, 0] = 1
        r3 = np.zeros((d, d), dtype=complex); r3[-1, -1] = 1
        for t in range(60):
            s = fn_state(rng.uniform(), k)
            r1, r2, r3 = (step(r, s, U, n, k, q) for r in (r1, r2, r3))
        print(model, n, "max trace distance between runs after 60 steps:",
              max(trace_distance(r1 - r2), trace_distance(r1 - r3), trace_distance(r2 - r3)))
