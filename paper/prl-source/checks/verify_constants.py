"""Independent check of the improved contraction constants (all logs base 2 unless noted)."""
import numpy as np
from mpmath import mp, mpf, log, power
mp.dps = 40

def consts(q, b):
    q = mpf(q); b = mpf(b)
    theta = 2*q**2/(1+q**2); bth = 1-theta
    a = 2*q/(1-q); cq = power(2, -1/(1-q))
    log2C = b*theta/2
    log2Pstar = log2C/bth                      # P* = C^{1/bartheta}
    # improved weight R = 2 P*
    log2R = 1 + log2Pstar
    # delta = c_q (2 * 2^{b/2} R)^{-a}
    log2_delta_inv = 1/(1-q) + a*(1 + b/2 + log2R)
    beta = q*(1+q**2)/((1-q)*(1-q**2))
    closed = beta*b + (1+4*q)/(1-q)
    # original paper: R = (2C)^{1/bartheta}, delta = c_q (4 2^{b/2} R)^{-a}
    log2R_old = (1 + log2C)/bth
    log2_delta_inv_old = 1/(1-q) + a*(2 + b/2 + log2R_old)
    closed_old = beta*(b+2) + (1+4*q)/(1-q)
    return dict(theta=theta, bth=bth, a=a, cq=cq, log2C=log2C, log2Pstar=log2Pstar, log2R=log2R,
                d_inv=log2_delta_inv, closed=closed, d_inv_old=log2_delta_inv_old, closed_old=closed_old, beta=beta)

worst = dict(closed=0, old=0, two_norm=1e9, mono=-1e9, simp4=1e9, simp1=1e9)
for q in np.concatenate([np.linspace(1e-4, 0.999, 4000), [0.5, 0.8, 0.9, 0.95, 0.99, 0.999]]):
    for b in [0, 1, 2, 3, 4, 5, 8, 17, 50]:
        c = consts(q, b)
        worst["closed"] = max(worst["closed"], abs(c["d_inv"] - c["closed"]))
        worst["old"] = max(worst["old"], abs(c["d_inv_old"] - c["closed_old"]))
        delta = power(2, -c["d_inv"])
        # 2-norm part: C R^theta / R = 2^{-bartheta}; need 2^{-bartheta} <= 1 - delta
        two_part = power(2, c["log2C"] + c["theta"]*c["log2R"] - c["log2R"])
        assert abs(two_part - power(2, -c["bth"])) < mpf(10)**-30
        worst["two_norm"] = min(worst["two_norm"], float((1 - delta) - two_part))
        # monotonicity of x - delta x^{a+1} on [0,1]: (a+1) delta <= 1
        worst["mono"] = max(worst["mono"], float((c["a"]+1)*delta))
        if b >= 4:
            worst["simp4"] = min(worst["simp4"], float(b/(1-mpf(q))**2 - c["d_inv"]))
        if b >= 1:
            worst["simp1"] = min(worst["simp1"], float((b+1)/(1-mpf(q))**2 - c["d_inv"]))
print("max |direct - closed form| (new):", float(worst["closed"]))
print("max |direct - closed form| (old):", float(worst["old"]))
print("min (1-delta) - 2^{-bartheta}  (must be >= 0):", worst["two_norm"])
print("max (a+1) delta  (must be <= 1):", worst["mono"])
print("min k/(1-q)^2 - log2 delta^-1 for k>=4 (>=0):", worst["simp4"])
print("min (k+1)/(1-q)^2 - log2 delta^-1 for k>=1 (>=0):", worst["simp1"])
# counterexamples near the thresholds
for q in [0.74, 0.8, 0.9, 0.99]:
    c3 = consts(q, 3); c0 = consts(q, 0)
    print(f"q={q}: k=3 simple k/(1-q)^2 margin = {float(3/(1-mpf(q))**2 - c3['d_inv']):.3f} | k=0 (k+1) margin = {float(1/(1-mpf(q))**2 - c0['d_inv']):.3f}")
# the two elementary inequalities used in the proof
qs = np.linspace(1e-6, 0.999999, 200001)
g1 = (1+qs)/(1-qs) * 2.0**(-5*qs/(1-qs))
g2 = (1-qs**2)/(1+qs**2) - 2.0**(-5*qs/(1-qs))
g3 = 1 - 2.0**(-(1-qs**2)/(1+qs**2)) - (1-qs**2)/(2*(1+qs**2))
print("max (1+q)/(1-q) 2^{-5q/(1-q)} (<=1):", g1.max(), "| min bartheta - 2^{-5q/(1-q)} (>=0):", g2.min(), "| min 1-2^{-bartheta} - bartheta/2 (>=0):", g3.min())
# values at q = 0.9
c = consts(0.9, 1)
print("q=0.9: theta=%.4f bartheta=%.4f a=%.1f beta=%.3f (1+4q)/(1-q)=%.1f log2P*/b=%.4f" % (c["theta"], c["bth"], c["a"], c["beta"], (1+4*0.9)/0.1, c["log2Pstar"]))
for k in [2, 4, 5, 10, 17]:
    n_ = consts(0.9, k); print(f"  k={k}: log2 delta^-1 new={float(n_['d_inv']):.1f} old={float(n_['d_inv_old']):.1f} simple={k*100}")
