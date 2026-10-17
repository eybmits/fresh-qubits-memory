"""Print every simulation number quoted in the Letter and the Supplemental Material, from the result files."""
import json, os
import numpy as np

R = json.load(open("results_main.json"))
C = json.load(open("results_cold.json"))
N = json.load(open("results_noise.json"))
T = json.load(open("results_tau.json"))


def get(L, **kw):
    out = [e for e in L if all(e.get(k) == v for k, v in kw.items())]
    assert len(out) == 1, (kw, len(out))
    return out[0]


def m(e):
    return float(np.mean(e["W"]))


print("== size scan (q = 0.9): mean W per n")
for model in ("ising", "haar"):
    for k in (1, 2):
        ns = sorted(e["n"] for e in R if e["model"] == model and e["k"] == k)
        means = {n: round(m(get(R, model=model, n=n, k=k)), 1) for n in ns}
        print(f"  {model} k={k}: {means}   range of means {min(means.values())}-{max(means.values())}")
print("== n = 8 versus k (q = 0.9): mean W; 'input' = all input qubits carry the input, 'cold' = extra qubits in |0>")
for model in ("ising", "haar"):
    print(f"  {model} input:", {k: round(m(get(R, model=model, n=8, k=k)), 1) for k in (1, 2, 3, 4)})
    print(f"  {model} cold :", {k: round(m(get(C, model=model, n=8, k=k)), 1) for k in (2, 3, 4)})
print("== weak noise (n = 6, k = 1, the same six reservoirs at every q)")
for model in ("ising", "haar"):
    pts = {0.9: get(R, model=model, n=6, k=1)["W"]}
    for e in N:
        if e["model"] == model:
            pts[e["q"]] = e["W"]
    for q, w in sorted(pts.items()):
        print(f"  {model} q={q}: W={w}  mean {np.mean(w):.1f}")
print("== evolution time (Ising, n = 6, k = 1, q = 0.9; the same couplings at every J*dt)")
for e in T:
    print(f"   J*dt={e['tau']}: W={e['W']}  mean {m(e):.1f}")
print("== washout: largest number of steps and largest residual")
for name, L in (("q = 0.9", R + C + T), ("q > 0.9", N)):
    steps = max(max(w["steps"]) for e in L for w in e["washout"])
    res = max(w["residual"] for e in L for w in e["washout"])
    print(f"   {name}: up to {steps} steps, residual <= {res:.1e}")
print("== which history pair sets W in the main runs")
cnt = {"history": 0, "single": 0, "tie": 0}
for e in R:
    for p in e["parts"]:
        h = max(v for k_, v in p.items() if k_.startswith("history"))
        s = max(v for k_, v in p.items() if k_.startswith("single"))
        cnt["history" if h > s else "single" if s > h else "tie"] += 1
print("  ", cnt)
if os.path.exists("validate_pairs.json"):
    V = json.load(open("validate_pairs.json"))
    gain = [v["W_extended"] - v["W"] for v in V]
    print(f"== validation: largest gain of the extended set of history pairs: {max(gain)} time steps "
          f"over {len(V)} realizations (gains: {sorted(set(gain))})")
