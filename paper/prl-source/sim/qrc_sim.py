"""Density-matrix simulation of noisy quantum reservoirs with input injection by reinitialization.

Model (one time step):  X -> D_q^{(x)n} ( U [ sigma(u) (x) Tr_in X ] U^dagger ),
where the first k qubits form the input register. The same linear map acts on states and on differences
of states, which we use to compute trace distances between echo states.

Memory depth (Eq. 3 of the main text): the smallest L such that any two input histories that agree on
their last L inputs lead to echo states within trace distance eps. memory_depth() evaluates it over two
kinds of history pairs,
  'single'  : the histories differ in one input, 0 versus 1, injected into a common echo state,
  'history' : the histories differ in all earlier inputs, constant 0 versus constant 1,
each followed by five common continuations (two random input sequences and the constant inputs 0, 1/2, 1).
Every echo state is prepared by a washout that runs until three different initial states agree within tol.
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


def cold_state(u, k):
    """Only the first input qubit carries the input; the other k-1 input qubits are reinitialized in |0>."""
    s = fn_state(u, 1)
    z = np.array([[1, 0], [0, 0]], dtype=complex)
    for _ in range(k - 1):
        s = np.kron(s, z)
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


# ----------------------------------------------------------------------------- echo states and memory depth
def washout(U, n, k, q, inputs, encode=fn_state, tol=1e-6, t_min=60, t_max=20000, every=10):
    """Drive three initial states (completely mixed, |0...0>, |1...1>) with the same inputs inputs(t) until
    they agree within trace distance tol (checked every `every` steps after t_min). Returns the state that
    started completely mixed, the number of steps, and the largest pairwise trace distance at the end."""
    d = 2 ** n
    r1 = np.eye(d, dtype=complex) / d
    r2 = np.zeros((d, d), dtype=complex); r2[0, 0] = 1
    r3 = np.zeros((d, d), dtype=complex); r3[-1, -1] = 1
    t = 0
    while True:
        s = encode(inputs(t), k)
        r1, r2, r3 = (step(r, s, U, n, k, q) for r in (r1, r2, r3))
        t += 1
        if t >= t_min and t % every == 0:
            res = max(trace_distance(r1 - r2), trace_distance(r1 - r3), trace_distance(r2 - r3))
            if res < tol or t >= t_max:
                return r1, t, float(res)


def forgetting_curve(X, U, n, k, q, cont, encode=fn_state, l_max=300, d_stop=3e-3):
    """D(l) = trace distance after l common time steps with inputs cont(1), cont(2), ...; D(0) is the trace
    distance of the difference X itself. Stops once D(l) < d_stop."""
    D = [trace_distance(X)]
    for l in range(1, l_max + 1):
        X = step(X, encode(cont(l), k), U, n, k, q)
        D.append(trace_distance(X))
        if D[-1] < d_stop:
            break
    return np.array(D)


def depth(D, eps):
    """Memory depth of one forgetting curve: 1 + the largest l with D(l) > eps."""
    idx = np.nonzero(D > eps)[0]
    return int(idx[-1] + 1) if len(idx) else 0


def memory_depth(U, n, k, q, rng, encode=fn_state, eps=1e-2, l_max=300, d_stop=3e-3, tol=1e-6, t_max=20000):
    """Memory depth of one reservoir, maximized over the history pairs 'single' and 'history' and over five
    continuations. Returns a dict with W, the depth of every pair and continuation, the washout data, and the
    forgetting curve of the 'history' pair with the first random continuation."""
    rho, t_r, res_r = washout(U, n, k, q, lambda t: rng.uniform(), encode, tol, t_max=t_max)
    rho0, t_0, res_0 = washout(U, n, k, q, lambda t: 0.0, encode, tol, t_max=t_max)
    rho1, t_1, res_1 = washout(U, n, k, q, lambda t: 1.0, encode, tol, t_max=t_max)
    pairs = {"single": step(rho, encode(1.0, k), U, n, k, q) - step(rho, encode(0.0, k), U, n, k, q),
             "history": rho1 - rho0}
    seqA, seqB = rng.uniform(size=l_max + 1), rng.uniform(size=l_max + 1)
    conts = {"randomA": lambda l: seqA[l], "randomB": lambda l: seqB[l],
             "const0": lambda l: 0.0, "const05": lambda l: 0.5, "const1": lambda l: 1.0}
    parts, curve = {}, None
    for pname, X in pairs.items():
        for cname, cont in conts.items():
            D = forgetting_curve(X, U, n, k, q, cont, encode, l_max, d_stop)
            parts[f"{pname}/{cname}"] = depth(D, eps)
            if pname == "history" and cname == "randomA":
                curve = D.tolist()
    return dict(W=max(parts.values()), parts=parts, curve=curve,
                washout=dict(steps=[t_r, t_0, t_1], residual=max(res_r, res_0, res_1)))
