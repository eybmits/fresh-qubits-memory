"""Independent channel simulators for optional numerical validation.

Requires NumPy. The package's original exact-arithmetic API does not import
this module. Basis order is most significant qubit first throughout.
"""

import numpy as np


def repetition_permutation(r):
    """Full reversible map on (a, c, b, x), manuscript Eq. (12)."""
    labels = np.arange(1 << (2 * r + 2), dtype=np.int64)
    mask = (1 << r) - 1
    x = labels & mask
    b = (labels >> r) & 1
    c = (labels >> (r + 1)) & 1
    a = labels >> (r + 2)
    weights = np.array([i.bit_count() for i in range(1 << r)])
    vote = np.where(c, b, weights[x] > r // 2)
    return (x << (r + 2)) | (c << (r + 1)) | (b << r) | (a ^ (vote * mask))


def bit_channel(probabilities, n, p01, p11):
    """Product classical channel, independently on every physical qubit.

    This is the complete quantum channel on diagonal density matrices.
    p01=P(output 1 | input 0); p11=P(output 1 | input 1).
    """
    out = np.asarray(probabilities, dtype=float).copy()
    for site in range(n):
        stride = 1 << (n - site - 1)
        blocks = out.reshape(-1, 2, stride)
        zero, one = blocks[:, 0].copy(), blocks[:, 1].copy()
        blocks[:, 0] = (1 - p01) * zero + (1 - p11) * one
        blocks[:, 1] = p01 * zero + p11 * one
    return out


def repetition_step(probabilities, r, q, c, b, permutation=None):
    """Discard input, prepare fresh ancillas/control, permute, then noise."""
    memdim = 1 << r
    marginal = probabilities.reshape(-1, memdim).sum(axis=0)
    reset = np.zeros_like(probabilities)
    reset.reshape(-1, memdim)[2 * c + b] = marginal
    perm = repetition_permutation(r) if permutation is None else permutation
    out = np.empty_like(reset)
    out[perm] = reset
    return bit_channel(out, 2 * r + 2, (1 - q) / 2, (1 + q) / 2)


def reset_density(rho, eta, k):
    """Partial trace of the first k qubits, followed by tensor preparation."""
    a = 1 << k
    b = rho.shape[0] // a
    reduced = np.trace(rho.reshape(a, b, a, b), axis1=0, axis2=2)
    return np.kron(eta, reduced)


def depolarize_density(rho, q, n):
    """Independent Pauli-mixture implementation of product depolarization."""
    out = rho.copy()
    dim = 1 << n
    labels = np.arange(dim)
    for site in range(n):
        mask = 1 << (n - site - 1)
        flipped = out[np.ix_(labels ^ mask, labels ^ mask)]
        signs = 1 - 2 * ((labels & mask) != 0).astype(int)
        zz = signs[:, None] * signs[None, :]
        out = (1 + 3 * q) / 4 * out + (1 - q) / 4 * (flipped + zz * flipped + zz * out)
    return out


def quantum_step(rho, eta, k, unitary, q, n):
    reset = reset_density(rho, eta, k)
    return depolarize_density(unitary @ reset @ unitary.conj().T, q, n)


def trace_norm(matrix):
    return float(np.abs(np.linalg.eigvalsh((matrix + matrix.conj().T) / 2)).sum())


def trace_distance(a, b):
    return trace_norm(a - b) / 2


def normalized_purity(rho):
    return float(np.sqrt(rho.shape[0] * np.vdot(rho, rho).real))


def bound_constants(q, k):
    theta = 2 * q * q / (1 + q * q)
    a = 2 * q / (1 - q)
    log2_r = (1 + theta * k / 2) / (1 - theta)
    log2_inverse_delta = 1 / (1 - q) + a * (2 + k / 2 + log2_r)
    return theta, log2_r, log2_inverse_delta


def common_norm(matrix, log2_r):
    """V(d*matrix), with normalized Schatten norms as in Appendix A."""
    return max(trace_norm(matrix), np.sqrt(matrix.shape[0]) * np.linalg.norm(matrix) * 2.0 ** (-log2_r))


def cooling_step(counts, r, q, gamma, rng, write=None):
    """Exact lumped dynamics of all cooling blocks, without decorrelation.

    Each row is one trajectory and each column is a block in queue order.
    Count sufficiency follows from homogeneous independent bit channels;
    correlations between blocks are retained trajectory by trajectory.
    """
    a, d = (1 - q) / 2, q * (1 - gamma)
    vote = counts[:, 0] >= (a + d / 2) * r if write is None else np.full(len(counts), bool(write))
    old_tail = counts[:, -1]
    fresh = np.where(vote, r - old_tail, old_tail)
    before = np.concatenate((fresh[:, None], counts[:, :-1]), axis=1)
    return rng.binomial(r - before, a) + rng.binomial(before, a + d)
