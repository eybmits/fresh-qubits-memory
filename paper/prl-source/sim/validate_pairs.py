"""Validation of the memory-depth estimator of qrc_sim.memory_depth (Supplemental Material, Sec. VII C).
For reservoirs of the campaign (same seeds, hence the same unitaries), compare the memory depth W of the
estimator, which uses the history pairs 'single' and 'history' with five continuations, with the largest
memory depth found over a much larger set of history pairs and continuations:
  - blocks of j = 2, 3, 5, 10, 30 consecutive differing inputs (0 versus 1),
  - all sign patterns of six consecutive differing inputs (0/1 versus 1/0),
  - three pairs of independent random histories,
  - constant histories with the input pairs (0, 1/2), (1/2, 1), (1/4, 3/4),
  - greedy continuations that maximize the trace distance at every time step (inputs 0, 1/4, 1/2, 3/4, 1),
each (except the greedy ones) followed by the five continuations of the estimator.
Usage: python3 validate_pairs.py  -> prints the largest difference and writes validate_pairs.json"""
import itertools, json, time
import numpy as np
from qrc_sim import (ising_unitary, haar_unitary, memory_depth, washout, forgetting_curve, depth, step,
                     trace_distance, fn_state)
from campaign import streams

EPS = 1e-2


def greedy_curve(X, U, n, k, q, l_max=300, d_stop=3e-3, grid=(0.0, 0.25, 0.5, 0.75, 1.0)):
    D = [trace_distance(X)]
    for l in range(1, l_max + 1):
        cand = [step(X, fn_state(u, k), U, n, k, q) for u in grid]
        dist = [trace_distance(Y) for Y in cand]
        i = int(np.argmax(dist))
        X = cand[i]; D.append(dist[i])
        if D[-1] < d_stop:
            break
    return np.array(D)


def extended_depth(U, n, k, q, rng, l_max=300):
    seqA, seqB = rng.uniform(size=l_max + 1), rng.uniform(size=l_max + 1)
    conts = [lambda l: seqA[l], lambda l: seqB[l], lambda l: 0.0, lambda l: 0.5, lambda l: 1.0]
    best = {}

    def score(name, X, greedy=False):
        W = max(depth(forgetting_curve(X, U, n, k, q, c, l_max=l_max), EPS) for c in conts)
        if greedy:
            W = max(W, depth(greedy_curve(X, U, n, k, q, l_max=l_max), EPS))
        best[name] = max(best.get(name, 0), W)

    rho, _, _ = washout(U, n, k, q, lambda t: rng.uniform())
    # blocks of constant differing inputs, and the single-input pair with a greedy continuation
    for j in (1, 2, 3, 5, 10, 30):
        A, B = rho, rho
        for _ in range(j):
            A = step(A, fn_state(0.0, k), U, n, k, q); B = step(B, fn_state(1.0, k), U, n, k, q)
        score(f"block{j}", B - A, greedy=(j == 1))
    # sign patterns of six differing inputs
    for pat in itertools.product((0, 1), repeat=5):
        A, B = rho, rho
        for s in (0,) + pat:
            A = step(A, fn_state(float(s), k), U, n, k, q); B = step(B, fn_state(float(1 - s), k), U, n, k, q)
        score("patterns", B - A)
    # constant histories with several input pairs, and the (0, 1) pair with a greedy continuation
    fp = {u: washout(U, n, k, q, lambda t, u=u: u)[0] for u in (0.0, 0.25, 0.5, 0.75, 1.0)}
    score("history01", fp[1.0] - fp[0.0], greedy=True)
    for a, b in ((0.0, 0.5), (0.5, 1.0), (0.25, 0.75)):
        score("history_other", fp[b] - fp[a])
    # independent random histories
    for _ in range(3):
        ra = washout(U, n, k, q, lambda t: rng.uniform())[0]
        rb = washout(U, n, k, q, lambda t: rng.uniform())[0]
        score("random", ra - rb)
    return max(best.values()), best


if __name__ == "__main__":
    out, t0, worst = [], time.time(), 0
    for model in ("ising", "haar"):
        for n, k in ((6, 1), (6, 2), (8, 1), (8, 2)):
            q = 0.9
            rngU, rngI = streams(model, n, k)       # the same reservoirs and inputs as campaign.py main
            rng2 = np.random.default_rng([12345, 1 if model == "ising" else 2, n, k])
            for rep in range(3):  # the first three realizations of the campaign
                U = ising_unitary(n, rngU) if model == "ising" else haar_unitary(n, rngU)
                W = memory_depth(U, n, k, q, rngI, eps=EPS)["W"]
                Wx, parts = extended_depth(U, n, k, q, rng2)
                worst = max(worst, Wx - W)
                out.append(dict(model=model, n=n, k=k, rep=rep, W=W, W_extended=Wx, parts=parts))
                print(f"{model} n={n} k={k} rep={rep}: W={W}  extended={Wx}  {parts}  ({time.time()-t0:.0f}s)",
                      flush=True)
                json.dump(out, open("validate_pairs.json", "w"))
    print("largest gain of the extended set over the estimator:", worst, "time steps")
