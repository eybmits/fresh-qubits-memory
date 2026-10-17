import numpy as np, time
from qrc_sim import *
rng = np.random.default_rng(1)

# 1) linearity check: difference evolution equals evolution of difference
n, k, q = 4, 1, 0.9
U = haar_unitary(n, rng)
r1 = np.eye(2**n, dtype=complex) / 2**n
r2 = r1.copy(); r2[0, 0] += 0.1; r2[1, 1] -= 0.1
for t in range(5):
    s = fn_state(rng.uniform(), k)
    r1n, r2n = step(r1, s, U, n, k, q), step(r2, s, U, n, k, q)
    X = step(r1 - r2, s, U, n, k, q)
    assert np.allclose(X, r1n - r2n)
    r1, r2 = r1n, r2n
print("linearity ok; trace preserved:", np.trace(r1).real)

# 2) single-qubit depolarizing: <Z> shrinks by q
n = 1
rho = np.array([[1, 0], [0, 0]], dtype=complex)
print("depolarize single qubit:", depolarize_all(rho, 1, 0.9).real.diagonal(), "expected", [0.95, 0.05])

# 3) error-correcting (repetition-code) reservoir as permutation unitary, r = 1 and r = 3: compare with q*lambda_r^l
from fractions import Fraction
from math import comb
def rep_unitary(r):
    # qubit order: ancillas a (r), c, b, memory x (r); input register = a, c, b  (k = r + 2)
    n = 2 * r + 2
    d = 2 ** n
    P = np.zeros((d, d))
    for idx in range(d):
        bits = [(idx >> (n - 1 - j)) & 1 for j in range(n)]
        a, c, b, x = bits[:r], bits[r], bits[r + 1], bits[r + 2:]
        F = b if c == 1 else int(sum(x) > r / 2)
        new = x + [c, b] + [ai ^ F for ai in a]
        out = sum(bit << (n - 1 - j) for j, bit in enumerate(new))
        P[out, idx] = 1
    return P.astype(complex), n
def rep_input(sym, r):
    # sym in {0,1,'blank'}; ancillas |0>, (c,b) = (1,b) or (0,0)
    c, b = (0, 0) if sym == "blank" else (1, sym)
    v = np.zeros(2 ** (r + 2)); v[(0 << 2) | (c << 1) | b] = 1  # ancillas all zero -> high bits 0
    return np.outer(v, v).astype(complex)
for r in (1, 3):
    U, n = rep_unitary(r)
    k = r + 2; q = 0.9; p = (1 - q) / 2
    pr = float(sum(Fraction(comb(r, j)) * Fraction(1, 20) ** j * Fraction(19, 20) ** (r - j) for j in range(r // 2 + 1, r + 1)))
    lam = 1 - 2 * pr
    d = 2 ** n
    rho = np.eye(d, dtype=complex) / d
    for _ in range(30):
        rho = step(rho, rep_input([0, 1, "blank"][rng.integers(3)], r), U, n, k, q)
    X = step(rho, rep_input(1, r), U, n, k, q) - step(rho, rep_input(0, r), U, n, k, q)
    Zlast = np.diag([1 if (i & 1) == 0 else -1 for i in range(d)]).astype(complex)  # Z on last memory qubit
    out = []
    for l in range(0, 8):
        if l > 0:
            X = step(X, rep_input("blank", r), U, n, k, q)
        out.append((l, trace_distance(X), abs(np.trace(Zlast @ X).real) / 2, q * lam ** l))
    print("r=%d:" % r, ["l=%d D=%.5f Zgap/2=%.5f q*lam^l=%.5f" % o for o in out[:4]])
