"""Fig. 4: memory of standard reservoirs versus the limit (q = 0.9, eps = 0.01).
Colours: repetition-code reservoir in blue (reaches the limit), standard reservoirs in greys
(Ising dark, Haar light), the idle qubit as a dashed reference line."""
import sys, json; sys.path.insert(0, ".")
from figstyle import *
import numpy as np
from math import log, comb
from fractions import Fraction
setup()
R = json.load(open("../sim/results_main.json"))
rep = json.load(open("../sim/rep_curve.json"))
q, eps = 0.9, 1e-2
def get(model, n, k):
    for e in R:
        if e["model"] == model and e["n"] == n and e["k"] == k:
            return e
STY = {"ising": dict(color=ISING, mk="D", ms=4.3, name="Ising"),
       "haar": dict(color=HAAR, mk="^", ms=4.8, name="Haar")}
IDLE = dict(color=INK, lw=1.0, ls=(0, (4, 2.5)))
W_idle = 43  # = 1 + max{l : q^(l+1) > eps}: a single qubit that holds the input without repair

fig = figure(TEXTWIDTH, 2.05)
a, b, c = even_row(fig, 3, left=0.47, right=0.06, gap=0.62)
# ---------------------------------------------------------------- a: forgetting curves (all n = 8)
L = np.arange(0, 700)
a.plot(L + 1, q ** (L + 1), zorder=2, **IDLE)
D = np.array(rep["D"])
a.plot(np.arange(len(D)) + 1, D, color=BLUE, lw=1.6, zorder=4)
for model in ("haar", "ising"):
    st = STY[model]
    cv = get(model, 8, 1)["curves"]
    m = min(len(x) for x in cv)
    arr = np.array([x[:m] for x in cv])
    l = np.arange(m) + 1
    a.fill_between(l, arr.min(0), arr.max(0), color=st["color"], alpha=0.3, lw=0)
    a.plot(l, np.median(arr, 0), color=st["color"], lw=1.5, zorder=3)
a.axhline(eps, color=GREY, lw=0.8, ls=(0, (1, 1.6)))
label(a, 1.15, eps * 1.2, r"$\varepsilon$", ha="left", va="bottom")
label(a, 1.12, 1.3e-3, "Haar", color=darker(HAAR, 0.75), bold=True, ha="left", va="bottom")
label(a, 15.5, 1.3e-3, "Ising", color=ISING, bold=True, ha="left", va="bottom")
label(a, 32, 0.1, "idle\nqubit", color=INK, bold=True, ha="left", va="center", linespacing=1.05)
label(a, 1.4, 1.12, r"\textbf{repetition code}, $k=5$", color=BLUE_DARK, ha="left", va="bottom")
a.set_xscale("log"); a.set_yscale("log")
a.set_xlim(1, 700); a.set_ylim(1e-3, 2.4)
a.set_xticks([1, 10, 100]); a.set_xticklabels(["1", "10", r"$10^2$"])
xlabel(a, "Time steps", "l")
ylabel(a, "Trace distance", r"D(l)")
panel(a, "a", "Forgetting", r"$n=8$")
# ---------------------------------------------------------------- b: memory depth versus reservoir size
b.axhline(W_idle, zorder=1, **IDLE)
label(b, 2.7, W_idle - 1.6, "idle qubit", ha="left", va="top")
for model, k, filled in (("ising", 1, True), ("ising", 2, False), ("haar", 1, True), ("haar", 2, False)):
    st = STY[model]
    ns = [n for n in sorted(e["n"] for e in R if e["model"] == model and e["k"] == k) if n >= k + 2]
    mu = np.array([np.mean(get(model, n, k)["W"]) for n in ns])
    sd = np.array([np.std(get(model, n, k)["W"]) for n in ns])
    x = np.array(ns) + (-0.1 if k == 1 else 0.1)
    b.fill_between(x, mu - sd, mu + sd, color=st["color"], alpha=0.2, lw=0)
    b.errorbar(x, mu, yerr=sd, fmt=st["mk"], ms=st["ms"], color=st["color"],
               mfc=st["color"] if filled else "white", mec=darker(st["color"], 0.6), mew=0.8,
               ecolor=darker(st["color"], 0.7), elinewidth=0.8, label=r"%s, $k=%d$" % (st["name"], k), zorder=3)
b.set_xlim(2.5, 9.5); b.set_ylim(0, 50)
b.set_xticks(range(3, 10))
legend(b, loc="center right", handlelength=1.0, borderaxespad=0.4, bbox_to_anchor=(1.0, 0.56))
xlabel(b, "Reservoir size", "n")
ylabel(b, "Memory depth", r"W(\varepsilon)")
panel(b, "b", "No gain from size", r"$\varepsilon=0.01$")
# ---------------------------------------------------------------- c: memory depth versus input qubits
def p_r(r):
    p = Fraction(1, 20)
    return sum(Fraction(comb(r, j)) * p ** j * (1 - p) ** (r - j) for j in range(r // 2 + 1, r + 1))
kr = np.arange(3, 16, 2)
Wrep = [log(q / eps) / -log(1 - 2 * float(p_r(k - 2))) for k in kr]
c.axhline(W_idle, zorder=1, **IDLE)
label(c, 15.6, W_idle / 1.5, "idle qubit", ha="right", va="top")
c.plot(kr, Wrep, color=BLUE_LIGHT, lw=1.0, zorder=2)
c.plot(kr, Wrep, "o", ms=4.6, color=BLUE, mec=BLUE_DARK, mew=0.7, zorder=4, label="repetition code")
for model in ("ising", "haar"):
    st = STY[model]
    ks = [1, 2, 3, 4]
    mu = [np.mean(get(model, 8, k)["W"]) for k in ks]
    sd = [np.std(get(model, 8, k)["W"]) for k in ks]
    c.plot(ks, mu, color=st["color"], lw=0.9, zorder=2)
    c.errorbar(ks, mu, yerr=sd, fmt=st["mk"], ms=st["ms"], color=st["color"], mec=darker(st["color"], 0.6),
               mew=0.8, ecolor=darker(st["color"], 0.7), elinewidth=0.8, label=r"%s, $n=8$" % st["name"], zorder=3)
c.set_yscale("log"); c.set_xlim(0.3, 16); c.set_ylim(1.5, 3e6)
c.set_xticks([1, 3, 5, 7, 9, 11, 13, 15]); c.set_yticks([1e1, 1e3, 1e5])
legend(c, loc="upper left", handlelength=1.0, borderaxespad=0.4)
xlabel(c, "Input qubits", "k")
ylabel(c, "Memory depth", r"W(\varepsilon)")
panel(c, "c", "Gain from input qubits")
save(fig, "fig4.pdf")
print("n=8 vs k:", [(m, k, np.mean(get(m, 8, k)["W"])) for m in ("ising", "haar") for k in (1, 2, 3, 4)])
print("Wrep:", [round(w, 1) for w in Wrep], "W_idle", W_idle)
