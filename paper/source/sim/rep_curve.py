"""Full-state trace distance D(l) of the repetition-code reservoir (k = 5, n = 8, q = 0.9), blank inputs after the
stored bit. Saved to rep_curve.json together with the single-qubit readout bound q*lambda^l."""
import json, numpy as np
from fractions import Fraction
from math import comb
from qrc_sim import step, trace_distance
r = 3; n = 2 * r + 2; k = r + 2; q = 0.9; d = 2 ** n
P = np.zeros((d, d))
for idx in range(d):
    bits = [(idx >> (n - 1 - j)) & 1 for j in range(n)]
    a, c, b, x = bits[:r], bits[r], bits[r + 1], bits[r + 2:]
    F = b if c == 1 else int(sum(x) > r / 2)
    new = x + [c, b] + [ai ^ F for ai in a]
    P[sum(bit << (n - 1 - j) for j, bit in enumerate(new)), idx] = 1
U = P.astype(complex)
def inp(sym):
    c, b = (0, 0) if sym == "blank" else (1, sym)
    v = np.zeros(2 ** k); v[(c << 1) | b] = 1
    return np.outer(v, v).astype(complex)
rng = np.random.default_rng(3)
rho = np.eye(d, dtype=complex) / d
for _ in range(50):
    rho = step(rho, inp([0, 1, "blank"][rng.integers(3)]), U, n, k, q)
X = step(rho, inp(1), U, n, k, q) - step(rho, inp(0), U, n, k, q)
D = [trace_distance(X)]
for l in range(1, 700):
    X = step(X, inp("blank"), U, n, k, q)
    D.append(trace_distance(X))
pr = float(sum(Fraction(comb(r, j)) * Fraction(1, 20) ** j * Fraction(19, 20) ** (r - j) for j in range(2, 4)))
lam = 1 - 2 * pr
json.dump(dict(D=D, readout=[q * lam ** l for l in range(700)], lam=lam), open("rep_curve.json", "w"))
W = 1 + max(i for i, v in enumerate(D) if v > 1e-2)
print("W(0.01) full state:", W, " readout bound:", np.log(q / 1e-2) / -np.log(lam))
