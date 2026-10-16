"""Supplemental Material: reproduces every numerical value quoted in
'Input Reinitialization Sets the Memory of Noisy Quantum Reservoirs'.
Requires: Python >= 3.9, mpmath. Run: python3 supplemental_numbers.py"""
from fractions import Fraction
from math import comb, ceil, log
import mpmath as mp

mp.mp.dps = 50

def majority_error(r, p):
    """p_r = Pr[Bin(r, p) > r/2], exact rational."""
    return sum(Fraction(comb(r, j)) * p**j * (1 - p)**(r - j) for j in range(r // 2 + 1, r + 1))

def half_life(r, q):
    """Largest T with lambda_r^T >= 1/2 for the repetition-code reservoir (Fig. 4c)."""
    lam = 1 - 2 * majority_error(r, (1 - q) / 2)
    return int(mp.floor(mp.log(2) / -mp.log(mp.mpf(lam.numerator) / lam.denominator)))

def constants(q):
    a = 2 * q / (1 - q)
    theta = 2 * q**2 / (1 + q**2)
    beta = a / (2 * (1 - theta))
    log2A = 1 / (1 - q) + a * (2 + 1 / (1 - theta))
    alpha = -0.5 * log(1 - q**2)
    return alpha, beta, log2A, theta

q = Fraction(9, 10)
print("== Sec. IV / Fig. 4: repetition-code reservoir at q = 0.9 ==")
print("single qubit: q^6 = %.3f, q^7 = %.3f  -> signal halves within seven time steps" % (0.9**6, 0.9**7))
prev = None
for r in range(1, 16, 2):
    T = half_life(r, q)
    ratio = "" if prev is None else "  (x%.2f)" % (T / prev)
    print("k = %2d (r = %2d, n = %2d): half-life = %8d time steps%s" % (r + 2, r, 2 * r + 2, T, ratio))
    prev = T
print("p_r for r = 15 (k = 17, n = 32): %.2e" % float(majority_error(15, (1 - q) / 2)))

alpha, beta, log2A, theta = constants(0.9)
print("\n== Theorem 1 constants at q = 0.9 ==")
print("alpha_q = %.4f, beta_q = %.4f, log2 A_q = %.4f" % (alpha, beta, log2A))
print("delta^-1 = 2^(%.1f + %.1f k)" % (log2A, beta))
print("k_q = 3 + ceil(ln4/alpha_q) = %d" % (3 + ceil(log(4) / alpha)))
for n in (100, 1000):
    print("washout t0(n = %d) = %d time steps" % (n, ceil(log(n) / -log(theta))))
a5, b5, l5, _ = constants(0.5)
print("q = 1/2, k = 1: log2 delta^-1 = %.2f" % (l5 + b5))

print("\n== Sec. V B / Appendix C: amplitude damping, q = 0.9, gamma = 0.3 ==")
qf, g = 0.9, 0.3
a_ = (1 - qf) / 2
d = qf * (1 - g)
ps = a_ / (1 - d)
s_min = next(s for s in range(1, 100) if d**s <= (0.5 - ps) / 2)
c = d**2 * (0.5 - ps)**2 / 2
print("a = %.3f, d = %.3f, p* = %.4f, c = %.4f, least admissible s = %d" % (a_, d, ps, c, s_min))

def tail_ge(r, p, x):
    return mp.fsum(mp.binomial(r, j) * mp.mpf(p)**j * (1 - mp.mpf(p))**(r - j)
                   for j in range(int(mp.ceil(x)), r + 1))

s, n = 8, 1100
r = (n - 2) // (s + 1)
thr = (a_ + d / 2) * r
pi1 = (ps + d**s * (a_ + d - ps)) / (1 + d**(s + 1))   # stationary bit probability while F = 1
w0, w1 = ps, a_ + d * (1 - pi1)
err0 = float(tail_ge(r, w0, thr))
err1 = float(1 - tail_ge(r, w1, thr))
print("pipeline s = %d, n = %d (r = %d): probability of losing the stored bit per time step: %.1e (F=0), %.1e (F=1)"
      % (s, n, r, err0, err1))
