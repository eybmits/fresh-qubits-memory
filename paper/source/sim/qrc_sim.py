"""Density-matrix simulation of noisy quantum reservoirs with input injection by reinitialization.

Model (one time step):  X -> D_q^{(x)n} ( U [ sigma(u) (x) Tr_in X ] U^dagger ),
where the first k qubits form the input register. The same linear map acts on states and on
differences of states, which we use to compute trace distances between echo states.
"""
import numpy as np
from scipy.stats import unitary_group

# ----------------------------------------------------------------------------- basic maps
def ptrace_in(X, n, k):
    a, b = 2 ** k, 2 ** (n - k)
    return np.einsum("aiaj->ij", X.reshape(a, b, a, b))

def depolarize_all(X, n, q):
    d = 2 ** n
    for i in range(n):
        A, B = 2 ** i, 2 ** (n - i - 1)
        R = X.reshape(A, 2, B, A, 2, B)
        red = R[:, 0, :, :, 0, :] + R[:, 1, :, :, 1, :]
        R = q * R
        R[:, 0, :, :, 0, :] += 0.5 * (1 - q) * red
        R[:, 1, :, :, 1, :] += 0.5 * (1 - q) * red
        X = R.reshape(d, d)
    return X

def step(X, sigma, U, n, k, q):
    M = np.kron(sigma, ptrace_in(X, n, k))
    M = U @ M @ U.conj().T
    return depolarize_all(M, n, q)

def trace_distance(X):
    X = 0.5 * (X + X.conj().T)
    return 0.5 * np.abs(np.linalg.eigvalsh(X)).sum()

# ----------------------------------------------------------------------------- input encodings
def fn_state(u, k):
    """Fujii-Nakajima encoding |psi(u)> = sqrt(1-u)|0> + sqrt(u)|1> on each of the k input qubits."""
    psi = np.array([np.sqrt(1 - u), np.sqrt(u)], dtype=complex)
    s1 = np.outer(psi, psi.conj())
    s = s1
    for _ in range(k - 1):
        s = np.kron(s, s1)
    return s

# ----------------------------------------------------------------------------- reservoir unitaries
PX = np.array([[0, 1], [1, 0]], dtype=complex)
PZ = np.array([[1, 0], [0, -1]], dtype=complex)

def op_on(P, i, n):
    out = np.array([[1.0 + 0j]])
    for j in range(n):
        out = np.kron(out, P if j == i else np.eye(2))
    return out

def ising_unitary(n, rng, J=1.0, h=1.0, tau=10.0):
    """All-to-all transverse-field Ising reservoir H = sum_{i<j} J_ij X_i X_j + h sum_i Z_i,
    J_ij uniform in [-J/2, J/2], evolved for a time tau per time step."""
    d = 2 ** n
    H = np.zeros((d, d), dtype=complex)
    Xs = [op_on(PX, i, n) for i in range(n)]
    for i in range(n):
        for j in range(i + 1, n):
            H += rng.uniform(-J / 2, J / 2) * (Xs[i] @ Xs[j])
        H += h * op_on(PZ, i, n)
    E, V = np.linalg.eigh(H)
    return (V * np.exp(-1j * E * tau)) @ V.conj().T

def haar_unitary(n, rng):
    return unitary_group.rvs(2 ** n, random_state=rng)

# ----------------------------------------------------------------------------- memory depth
def memory_curves(U, n, k, q, rng, n_branch=3, t_wash=80, gap=10, l_max=200, d_stop=1e-4,
                  encode=fn_state, u_pair=(0.0, 1.0), u_sampler=None):
    """Trace distance D(l) between echo states whose input sequences differ only in the input
    injected l+1 time steps before the end (u_pair), with common random inputs elsewhere.
    Returns a list of arrays D[0..l_end] (one per branch)."""
    if u_sampler is None:
        u_sampler = lambda: rng.uniform(0, 1)
    d = 2 ** n
    rho = np.eye(d, dtype=complex) / d
    for _ in range(t_wash):
        rho = step(rho, encode(u_sampler(), k), U, n, k, q)
    curves = []
    for b in range(n_branch):
        # branch: inject the two different inputs into the current echo state
        X = step(rho, encode(u_pair[1], k), U, n, k, q) - step(rho, encode(u_pair[0], k), U, n, k, q)
        D = [trace_distance(X)]
        for l in range(1, l_max + 1):
            X = step(X, encode(u_sampler(), k), U, n, k, q)
            D.append(trace_distance(X))
            if D[-1] < d_stop:
                break
        curves.append(np.array(D))
        # advance the common trajectory before the next branch
        for _ in range(gap):
            rho = step(rho, encode(u_sampler(), k), U, n, k, q)
    return curves

def depth_from_curves(curves, eps):
    """Memory depth estimate: 1 + largest l with D(l) > eps, maximized over branches."""
    best = 0
    for D in curves:
        idx = np.nonzero(D > eps)[0]
        if len(idx):
            best = max(best, idx[-1] + 1)
    return best
