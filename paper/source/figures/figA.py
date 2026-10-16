"""Appendix figures 5-7 from exact (non-sampled) numbers. Same style and palette as the main-text figures:
red = upper bounds and noise, blue = the construction and lower bounds, greys = neutral."""
import sys, json; sys.path.insert(0, ".")
from figstyle import *
import numpy as np
from math import log, comb
from fractions import Fraction
setup()
E = json.load(open("../sim/exact_numbers.json"))

# ============================================================== Fig. 5: how tight are the bounds?
fig = figure(TEXTWIDTH, 2.05)
a, b, c = even_row(fig, 3, left=0.47, right=0.06, gap=0.62)
cc = E["const_curve"]
qq = np.array([x["q"] for x in cc])
a.plot(qq, [x["beta"] for x in cc], color=RED, lw=1.5, label=r"upper bound, $\beta_q$")
a.plot(qq, [x["alpha_bits"] for x in cc], color=BLUE, lw=1.5, label=r"construction, $\alpha_q/\ln 2$")
for x in E["const_table"]:
    if x["q"] == 0.9:
        a.plot(0.9, x["beta"], "o", ms=4.5, color=RED, mec=darker(RED, 0.65), zorder=5)
        a.plot(0.9, x["alpha_bits"], "o", ms=4.5, color=BLUE, mec=darker(BLUE, 0.65), zorder=5)
        label(a, 0.86, x["beta"], r"$85.7$", color=RED_DARK, ha="right", va="center")
        label(a, 0.86, x["alpha_bits"] * 1.6, r"$1.20$", color=BLUE_DARK, ha="right", va="bottom")
a.set_yscale("log"); a.set_xlim(0, 1); a.set_ylim(1e-3, 3e4)
a.set_yticks([1e-2, 1, 1e2, 1e4])
legend(a, loc="upper left", handlelength=1.4, borderaxespad=0.4)
xlabel(a, "Noise strength", "q")
ylabel(a, "Bits per input qubit")
panel(a, "a", "Exponents")

cols = dict(zip(["0.8", "0.9", "0.95"], blues(3)))
for qs, col in cols.items():
    d = E["rep_pr"][qs]
    b.plot(d["r"], d["chernoff"], color=col, lw=1.0, ls=(0, (4, 2.2)))
    b.plot(d["r"], d["exact"], "o", ms=3.8, color=col, mec=darker(col, 0.6), mew=0.6, label=r"$%s$" % qs)
b.set_yscale("log"); b.set_xlim(0, 42); b.set_ylim(1e-40, 1)
b.set_yticks([1e-40, 1e-30, 1e-20, 1e-10, 1])
label(b, 41, 3e-39, "dashed: Chernoff\n" + r"bound $(1-q^2)^{r/2}$", ha="right", va="bottom", linespacing=1.1)
legend(b, loc="lower left", title=r"$q$", handlelength=1.0, borderaxespad=0.4)
xlabel(b, "Copies", "r")
ylabel(b, "Majority error", "p_r")
panel(b, "b", "Majority error")

d = E["bounds_q05"]
kk = np.array(d["k"])
c.fill_between(kk, 10 ** np.array(d["upper_log10"]), 1e22, color=RED_FILL, lw=0, zorder=0)
c.plot(kk, 10 ** np.array(d["upper_log10"]), color=RED, lw=1.5, label="upper bound (Thm. 1)")
c.plot(d["rep_k"], d["rep_depth"], "o", ms=4.0, color=BLUE, mec=BLUE_DARK, mew=0.6, label="repetition code")
c.set_yscale("log"); c.set_xlim(0, 31); c.set_ylim(1, 1e21)
c.set_yticks([1, 1e5, 1e10, 1e15, 1e20])
legend(c, loc="upper left", handlelength=1.3, borderaxespad=0.4)
xlabel(c, "Input qubits", "k")
ylabel(c, "Memory depth", r"W(\varepsilon)")
panel(c, "c", "Bounds", r"$q=0.5$, $\varepsilon=0.01$")
save(fig, "figA1.pdf")

# ============================================================== Fig. 6: washout of a redundant initial state
fig = figure(TEXTWIDTH, 2.05)
a, b = even_row(fig, 2, left=0.47, right=0.06, gap=0.66)
L = np.arange(0, 121)
ms = ["1", "10", "100", "1000", "10000"]
labs = {"1": r"$1$", "10": r"$10$", "100": r"$10^2$", "1000": r"$10^3$", "10000": r"$10^4$"}
for m, col in zip(ms, blues(5)):
    a.plot(L, np.maximum(E["washout"][m], 1e-12), color=col, lw=1.4, label=labs[m])
a.axhline(1e-2, color=GREY, lw=0.8, ls=(0, (1, 1.6)))
label(a, 118, 1.3e-2, r"$\varepsilon$", ha="right", va="bottom")
a.set_yscale("log"); a.set_xlim(0, 120); a.set_ylim(2e-6, 3)
a.set_yticks([1e-5, 1e-3, 1e-1])
legend(a, loc="lower left", title=r"copies $m$", ncol=5, columnspacing=0.7, handlelength=1.0, borderaxespad=0.4)
xlabel(a, "Time steps", "L")
ylabel(a, "Trace distance")
panel(a, "a", "Washout of a redundant initial state", r"$q=0.9$")
wt = E["washout_time"]
b.plot(wt["m"], wt["upper"], color=RED, lw=1.2, ls=(0, (4, 2.2)), label="upper bound")
b.plot(wt["m"], wt["lower"], color=BLUE, lw=1.2, ls=(0, (4, 2.2)), label="lower bound")
b.plot(wt["m"], wt["t"], "o", ms=3.8, color=INK, mec="white", mew=0.5, label="exact", zorder=4)
b.set_xscale("log"); b.set_xlim(0.8, 4e4); b.set_ylim(0, 110)
legend(b, loc="upper left", handlelength=1.4, borderaxespad=0.4)
xlabel(b, "Redundant copies", "m")
ylabel(b, "Washout time")
panel(b, "b", r"Washout grows as $\log m$", r"$\varepsilon=0.01$")
save(fig, "figA2.pdf")

# ============================================================== Fig. 7: entropy budget
fig = figure(TEXTWIDTH, 2.05)
a, b = even_row(fig, 2, left=0.47, right=0.06, gap=0.66)
for g, col in zip(["0.1", "0.3", "0.5"], blues(3)):
    dd = E["cooling"][g]
    n = np.array(dd["n"]); e = np.array(dd["err"])
    W = np.floor(1 / (4 * e))
    msk = W >= 1
    a.plot(n[msk], W[msk], color=col, lw=1.5, label=r"$%s$" % g)
a.set_yscale("log"); a.set_xlim(0, 1600); a.set_ylim(1, 1e9)
a.set_yticks([1, 1e3, 1e6, 1e9])
legend(a, loc="upper left", title=r"$k=2$, damping $\gamma$", handlelength=1.4, borderaxespad=0.4)
xlabel(a, "Reservoir size", "n")
ylabel(a, "Memory depth", r"W")
panel(a, "a", "Cooling noise adds memory", r"$q=0.9$")
t = np.arange(0, 21)
qv = 0.9
b.plot(t, np.ones_like(t, dtype=float), "s", ms=4.0, color=BLUE_DARK, mec=darker(BLUE_DARK, 0.6), mew=0.6,
       label=r"pure dephasing", zorder=4)
frozen = np.where(t % 2 == 0, 1.0, qv)
b.plot(t, frozen, "o-", ms=4.0, lw=0.8, color=BLUE_LIGHT, mec=darker(BLUE_LIGHT, 0.6), mew=0.6,
       label=r"frozen Pauli error", zorder=3)
b.plot(t, qv ** t, "D-", ms=3.6, lw=0.8, color=RED, mec=darker(RED, 0.65), mew=0.6, label=r"depolarizing, $q^t$",
       zorder=3)
b.set_xlim(-0.5, 20.5); b.set_ylim(0, 1.12); b.set_xticks([0, 5, 10, 15, 20])
legend(b, loc="lower left", handlelength=1.6, borderaxespad=0.4)
xlabel(b, "Time steps since storage", "t")
ylabel(b, "Readout", r"\langle Z\rangle_t")
panel(b, "b", "Where the limit ends", r"$q=0.9$")
save(fig, "figA3.pdf")
print("ok")
