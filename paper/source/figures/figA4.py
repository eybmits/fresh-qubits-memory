"""Appendix Fig. 8: robustness of the simulations (noise strength, evolution time).
Same colours as Fig. 4: Ising dark grey, Haar light grey, idle qubit as dashed reference line."""
import sys, json; sys.path.insert(0, ".")
from figstyle import *
import numpy as np
from math import log
setup()
R = json.load(open("../sim/results_main.json"))
Q = json.load(open("../sim/results_qscan.json"))
X = json.load(open("../sim/results_extra.json"))
eps = 1e-2
STY = {"ising": dict(color=ISING, mk="D", ms=4.3, name="Ising"),
       "haar": dict(color=HAAR, mk="^", ms=4.8, name="Haar")}
IDLE = dict(color=INK, lw=1.0, ls=(0, (4, 2.5)))
def collect(model, n):
    pts = {}
    for e in R:
        if e["model"] == model and e["n"] == n and e["k"] == 1:
            pts[e["q"]] = e["W"]
    for e in Q:
        if e["model"] == model and e["n"] == n:
            pts[e["q"]] = e["W"]
    for e in X["qsat"]:
        if e["model"] == model and e["n"] == n:
            pts[e["q"]] = e["W"]
    return pts
fig = figure(TEXTWIDTH, 2.05)
a, b = even_row(fig, 2, left=0.47, right=0.06, gap=0.66)
qq = np.linspace(0.85, 0.9995, 400)
a.plot(1 - qq, np.log(1 / eps) / -np.log(qq), zorder=1, **IDLE)
label(a, 2.4e-3, 1.4e3, "idle qubit", ha="left", va="center")
summary = {}
for model in ("ising", "haar"):
    st = STY[model]
    pts = collect(model, 6)
    qs = sorted(q for q in pts if q < 1)
    x = [1 - q for q in qs]; mu = [np.mean(pts[q]) for q in qs]; sd = [np.std(pts[q]) for q in qs]
    a.plot(x, mu, color=st["color"], lw=0.9, zorder=2)
    a.errorbar(x, mu, yerr=sd, fmt=st["mk"], ms=st["ms"], color=st["color"], mec=darker(st["color"], 0.6), mew=0.8,
               ecolor=darker(st["color"], 0.7), elinewidth=0.8, label=r"%s, $n=6$" % st["name"], zorder=3)
    W1 = np.mean(pts[1.0])
    a.axhline(W1, color=st["color"], lw=0.9, ls=(0, (1, 1.5)), zorder=1)
    summary[model] = dict(q=qs, mu=mu, W1=W1)
a.set_xscale("log"); a.set_yscale("log")
a.set_xlim(0.16, 8e-4); a.set_ylim(2, 6e3)
a.set_xticks([0.1, 0.01, 0.001]); a.set_xticklabels([r"$10^{-1}$", r"$10^{-2}$", r"$10^{-3}$"])
a.plot([], [], color=INK, lw=0.9, ls=(0, (1, 1.5)), label="noiseless limit")
legend(a, loc="upper left", handlelength=1.4, borderaxespad=0.4)
xlabel(a, "Noise per time step", "1-q")
ylabel(a, "Memory depth", r"W(\varepsilon)")
panel(a, "a", "Weak noise", r"$k=1$, $\varepsilon=0.01$")
taus = [e["tau"] for e in X["tau"]]
mu = [np.mean(e["W"]) for e in X["tau"]]; sd = [np.std(e["W"]) for e in X["tau"]]
st = STY["ising"]
b.plot(taus, mu, color=st["color"], lw=0.9)
b.errorbar(taus, mu, yerr=sd, fmt=st["mk"], ms=st["ms"], color=st["color"], mec=darker(st["color"], 0.6), mew=0.8,
           ecolor=darker(st["color"], 0.7), elinewidth=0.8, zorder=3, label=r"Ising, $n=6$")
b.axhline(log(1 / eps) / -log(0.9) // 1, **IDLE)
label(b, 0.25, 41.2, "idle qubit", ha="left", va="top")
b.set_xscale("log"); b.set_xlim(0.2, 45); b.set_ylim(0, 48)
b.set_xticks([0.3, 1, 3, 10, 30]); b.set_xticklabels(["0.3", "1", "3", "10", "30"])
legend(b, loc="center right", handlelength=1.0, borderaxespad=0.4)
xlabel(b, "Evolution time per step", r"J\Delta t")
ylabel(b, "Memory depth", r"W(\varepsilon)")
panel(b, "b", "Ising dynamics", r"$q=0.9$, $k=1$")
save(fig, "figA4.pdf")
print(summary)
