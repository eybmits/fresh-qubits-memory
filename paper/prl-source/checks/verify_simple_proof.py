"""Checks of the elementary steps used in the simplified Supplemental proof.
(1) Lemma S1: |E_u X|_2 <= 2^{k/2} |X|_2 for the injection map, on random Hermitian X, unitaries, input states.
(2) Proposition S4: with s = 1/(1-q), delta <= c_q 4^{-a} = 2^{4-5s}, a + 1 <= 2s, bartheta >= 1-q,
    1 - 2^{-bartheta} >= bartheta/2, and 2s 2^{4-5s} <= 1, which give (a+1) delta <= 1 and delta <= 1 - 2^{-bartheta}.
(3) Concentration of the examples: m redundant copies -> 2^{(m-1)/2}."""
import numpy as np
rng = np.random.default_rng(1)

def rand_herm(d):
    A = rng.normal(size=(d, d)) + 1j * rng.normal(size=(d, d))
    return (A + A.conj().T) / 2

def rand_unitary(d):
    Q, R = np.linalg.qr(rng.normal(size=(d, d)) + 1j * rng.normal(size=(d, d)))
    return Q * (np.diag(R) / abs(np.diag(R)))

def rand_state(d):
    A = rng.normal(size=(d, d)) + 1j * rng.normal(size=(d, d))
    r = A @ A.conj().T
    return r / np.trace(r)

def norm_p(X, p):
    ev = np.abs(np.linalg.eigvalsh(X))
    return np.mean(ev ** p) ** (1 / p)

worst = 0
for n, k in [(3, 1), (4, 1), (4, 2), (5, 2), (5, 3)]:
    d, din = 2 ** n, 2 ** k
    for _ in range(200):
        X = rand_herm(d)
        U = rand_unitary(d)
        sig = rand_state(din)
        Xr = X.reshape(din, d // din, din, d // din)
        trin = np.einsum("iaib->ab", Xr)                    # partial trace over the input register
        EX = U @ np.kron(sig, trin) @ U.conj().T
        ratio = norm_p(EX, 2) / (2 ** (k / 2) * norm_p(X, 2))
        worst = max(worst, ratio)
        assert norm_p(EX, 1) <= norm_p(X, 1) + 1e-9
print("Lemma S1: max |E X|_2 / (2^{k/2}|X|_2) =", round(worst, 4), "(must be <= 1)")

q = np.linspace(1e-6, 1 - 1e-6, 400001)
s = 1 / (1 - q); a = 2 * q / (1 - q); cq = 2 ** (-s); bth = (1 - q ** 2) / (1 + q ** 2)
print("c_q 4^-a == 2^(4-5s):", np.allclose(cq * 4.0 ** (-a), 2.0 ** (4 - 5 * s)))
print("a+1 <= 2s:", np.all(a + 1 <= 2 * s), "| bartheta >= 1-q:", np.all(bth >= 1 - q - 1e-15),
      "| 1-2^-bartheta >= bartheta/2:", np.all(1 - 2.0 ** (-bth) >= bth / 2 - 1e-15))
print("max 2s 2^(4-5s) =", (2 * s * 2.0 ** (4 - 5 * s)).max(), "(must be <= 1)")
for m in [1, 2, 3, 5]:
    n = 6; d = 2 ** n
    z = np.zeros(2 ** m); z[0] = 1; o = np.zeros(2 ** m); o[-1] = 1
    rho = np.kron(np.outer(z, z), np.eye(2 ** (n - m)) / 2 ** (n - m))
    rho2 = np.kron(np.outer(o, o), np.eye(2 ** (n - m)) / 2 ** (n - m))
    X = d * (rho - rho2)
    print("m=%d copies: concentration %.4f, predicted %.4f" % (m, norm_p(X, 2) / norm_p(X, 1), 2 ** ((m - 1) / 2)))
