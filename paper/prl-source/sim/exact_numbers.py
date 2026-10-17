"""Exact (non-sampled) numbers for the appendix figures and tables. Writes exact_numbers.json."""
import json
from fractions import Fraction
from math import comb, log, ceil, floor, sqrt, exp, log2
import numpy as np
from scipy.stats import binom

out = {}

# ---------------------------------------------------------------- constants of Theorem 1
def consts(q):
    a = 2 * q / (1 - q)
    th = 2 * q * q / (1 + q * q)
    beta = a / (2 * (1 - th))
    log2A = (1 + 4 * q) / (1 - q)       # k-independent part of log2(1/delta), contraction with R = 2 P_*
    alpha = -0.5 * log(1 - q * q)
    pstar = q * q / (1 - q * q)          # log2 P_* per input qubit
    return dict(q=q, theta=th, alpha=alpha, alpha_bits=alpha / log(2), beta=beta, log2A=log2A, pstar=pstar,
                beta_closed=q * (1 + q * q) / ((1 - q) * (1 - q * q)))
qs = np.linspace(0.02, 0.99, 200)
out["const_curve"] = [consts(float(q)) for q in qs]
out["const_table"] = []
for q in (0.5, 0.8, 0.9, 0.95, 0.99):
    c = consts(q)
    c["t0_100"] = ceil(log(100) / -log(c["theta"]))
    c["t0_1000"] = ceil(log(1000) / -log(c["theta"]))
    c["kq"] = 3 + ceil(log(4) / c["alpha"])      # smallest k with exp(alpha (k-3)) >= 4
    out["const_table"].append(c)

# ---------------------------------------------------------------- error-correcting reservoir (repetition code)
def p_r(r, q):
    p = Fraction(1, 1) * (1 - Fraction(q).limit_denominator(10 ** 6)) / 2
    return sum(Fraction(comb(r, j)) * p ** j * (1 - p) ** (r - j) for j in range(r // 2 + 1, r + 1))
def half_life(r, q):
    lam = 1 - 2 * float(p_r(r, q))
    return floor(log(2) / -log(lam)) if lam < 1 else float("inf")
def depth_rep(r, q, eps):
    lam = 1 - 2 * float(p_r(r, q))
    return log(q / eps) / -log(lam)
out["rep_pr"] = {}
for q in (0.8, 0.9, 0.95):
    rs = list(range(1, 42, 2))
    out["rep_pr"][str(q)] = dict(r=rs, exact=[float(p_r(r, q)) for r in rs],
                                 chernoff=[(1 - q * q) ** (r / 2) for r in rs])
out["rep_halflife_table"] = {}
for q in (0.8, 0.9, 0.95, 0.99):
    out["rep_halflife_table"][str(q)] = {str(k): half_life(k - 2, q) for k in (3, 5, 9, 13, 17)}
out["rep_depth_q09"] = {str(k): depth_rep(k - 2, 0.9, 1e-2) for k in range(3, 20, 2)}
# bounds versus k at q = 0.5 (eps = 0.01)
q = 0.5; c = consts(q)
ks = list(range(1, 31))
out["bounds_q05"] = dict(k=ks,
    upper_log10=[(c["log2A"] + c["beta"] * k) * log10_2 + np.log10(log(1 / 1e-2)) for k in ks] if (log10_2 := np.log10(2)) else None,
    rep_k=[k for k in ks if k >= 3 and (k - 2) % 2 == 1],
    rep_depth=[depth_rep(k - 2, q, 1e-2) for k in ks if k >= 3 and (k - 2) % 2 == 1])

# ---------------------------------------------------------------- washout of an initial state (U = I)
def tv_copies(m, L, q):
    a = (1 + q ** L) / 2                         # probability that a copy still reads its initial value
    j = np.arange(m + 1)
    return 0.5 * np.abs(binom.pmf(j, m, a) - binom.pmf(j, m, 1 - a)).sum()
q = 0.9
Ls = list(range(0, 121))
out["washout"] = {}
for m in (1, 10, 100, 1000, 10000):
    out["washout"][str(m)] = [float(tv_copies(m, L, q)) for L in Ls]
ms = np.unique(np.round(np.logspace(0, 4.5, 40)).astype(int))
tw = []
for m in ms:
    L = 0
    while tv_copies(int(m), L, q) > 1e-2:
        L += 1
    tw.append(L)
out["washout_time"] = dict(m=[int(x) for x in ms], t=tw,
    upper=[ceil(log(sqrt(m) / 1e-2) / -log(q)) for m in ms],
    lower=[(log(m) - log(4 / (1e-2 * 2))) / (-2 * log(q)) for m in ms])  # placeholder, recomputed below
# Chebyshev lower bound: trace distance >= 2(1 - 2/(m q^{2L})) in total variation units -> TV >= 1 - 2/(m q^{2L})
# TV > eps as long as 2/(m q^{2L}) < 1 - eps  <=>  L < ln(m (1-eps)/2) / (2 ln(1/q))
out["washout_time"]["lower"] = [max(0.0, log(m * (1 - 1e-2) / 2) / (-2 * log(q))) for m in ms]

# ---------------------------------------------------------------- cooling reservoir (amplitude damping), k = 2
def cooling_error(n, q, g):
    a = (1 - q) / 2; d = q * (1 - g); ps = a / (1 - d); th = a + d / 2
    best = (1.0, None, None)
    for s in range(1, 60):
        us = ps + d ** s * (1 - ps)
        if us >= 0.5:
            continue
        r = (n - 2) // (s + 1)
        if r < 1:
            break
        thr = ceil(th * r - 1e-12)                       # decide 1 iff count >= th*r
        e0 = binom.sf(thr - 1, r, a + d * us)            # P[Bin >= thr]
        e1 = binom.cdf(thr - 1, r, a + d * (1 - us))     # P[Bin < thr]
        e = max(e0, e1)
        if e < best[0]:
            best = (float(e), s, r)
    return best
out["cooling"] = {}
for g in (0.1, 0.3, 0.5):
    ns = list(range(10, 1601, 10))
    res = [cooling_error(n, 0.9, g) for n in ns]
    out["cooling"][str(g)] = dict(n=ns, err=[x[0] for x in res], s=[x[1] for x in res], r=[x[2] for x in res])
# smallest n with error <= 1e-6 at gamma = 0.3
for g in (0.1, 0.3, 0.5):
    n = 4
    while cooling_error(n, 0.9, g)[0] > 1e-6:
        n += 1
    out.setdefault("cooling_n_1e6", {})[str(g)] = (n, cooling_error(n, 0.9, g))
out["rep_p15"] = float(p_r(15, 0.9))

json.dump(out, open("exact_numbers.json", "w"))
print("constants:", [(c["q"], round(c["alpha"], 4), round(c["beta"], 3), round(c["log2A"], 2), round(c["pstar"], 3), c["t0_100"], c["kq"]) for c in out["const_table"]])
print("half-lives:", out["rep_halflife_table"])
print("rep depth q=0.9 eps=0.01:", {k: round(v, 1) for k, v in out["rep_depth_q09"].items()})
print("washout times:", list(zip(out["washout_time"]["m"], out["washout_time"]["t"]))[::6])
print("cooling n for 1e-6:", out["cooling_n_1e6"])
print("p_15 =", out["rep_p15"])
