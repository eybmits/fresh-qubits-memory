"""Supplemental figures S1-S7. Same style and palette as the main-text figures:
red = upper bounds and noise, blue = the construction and lower bounds, purple = input, greys = standard
reservoirs and references.
  S1  noise caps the purity (Step 1 of the proof)         S2  how tight are the bounds (exact numbers)
  S3  washout of a redundant initial state                S4  exact response of the error-correcting reservoir
  S5  entropy budget at work                              S6  simulations: forgetting curves and robustness
  S7  standard reservoirs versus input qubits"""
import sys, json; sys.path.insert(0, ".")
from figstyle import *
import numpy as np
from math import log, comb, floor
from fractions import Fraction
setup()
E = json.load(open("../sim/exact_numbers.json"))
R = json.load(open("../sim/results_main.json"))
N = json.load(open("../sim/results_noise.json"))
TAU = json.load(open("../sim/results_tau.json"))
COLD = json.load(open("../sim/results_cold.json"))
rep = json.load(open("../sim/rep_curve.json"))
STY = {"ising": dict(color=ISING, mk="D", ms=4.3, name="Ising"),
       "haar": dict(color=HAAR, mk="^", ms=4.8, name="Haar")}
IDLE = dict(color=INK, lw=1.0, ls=(0, (4, 2.5)))


def get(model, n, k):
    for e in R:
        if e["model"] == model and e["n"] == n and e["k"] == k:
            return e


# ============================================================== Fig. S1: noise caps the purity (Step 1)
# The purity bound of Eq. (S-purityrec), iterated with equality, for reservoirs that start in a pure state:
# log2 P_t^2 = theta^t n + (1 - theta^t) * cap, with the cap 2 k q^2 / (1 - q^2) of every echo state.
q1, k1 = 0.9, 2
theta1 = 2 * q1 ** 2 / (1 + q1 ** 2)
cap1 = 2 * k1 * q1 ** 2 / (1 - q1 ** 2)
SOFT_BOX = dict(boxstyle="round,pad=0.2,rounding_size=0.16", fc="white", ec="none", alpha=0.6)
fig = figure(COLUMNWIDTH, 2.05)
ax = add_axes(fig, 0.47, 0.40, COLUMNWIDTH - 0.47 - 0.15, 2.05 - 0.40 - 0.20)  # room for the tick label 100
tt = np.arange(0, 101)
ns1 = [100, 1000, 10000]
for n_, col in zip(ns1, blues(4)[1:]):
    ax.plot(tt, theta1 ** tt * n_ + (1 - theta1 ** tt) * cap1, color=col, lw=1.5, zorder=3,
            label={100: r"$10^2$", 1000: r"$10^3$", 10000: r"$10^4$"}[n_])
    t0 = int(np.ceil(np.log(n_) / -np.log(theta1)))      # washout time t_0 of Sec. III F
    ax.plot(t0, theta1 ** t0 * n_ + (1 - theta1 ** t0) * cap1, "o", ms=4.8, color=col, mec=INK, mew=0.7, zorder=5)
ax.axhline(cap1, color=RED, lw=1.3, ls=(0, (4, 2.5)), zorder=2)
label(ax, 2.0, 8.0, r"cap $2kq^2/(1-q^2)\approx17$, for any $n$", color=RED_DARK, ha="left", va="center",
      bbox=SOFT_BOX, zorder=6)
label(ax, 98.0, 3.6, r"dots: washout, grows as $\log n$", ha="right", va="center", bbox=SOFT_BOX, zorder=6)
ax.set_yscale("log"); ax.set_xlim(0, 100); ax.set_ylim(2.2, 4e4)
ax.set_yticks([10, 1e2, 1e3, 1e4])
legend(ax, loc="upper right", title=r"reservoir size $n$", ncol=3, handlelength=1.2, columnspacing=0.8)
xlabel(ax, "Time step", "t")
ylabel(ax, "Purity bound", r"\log_2P_t^2")
ax.set_title(r"Noise caps the purity", loc="left", fontsize=FS, pad=4)
ax.set_title(r"$q=0.9$, $k=2$", loc="right", fontsize=FS, pad=4)
save(fig, "figS1.pdf")
print("Fig. S1: cap %.2f, washout t0" % cap1, [int(np.ceil(np.log(n_) / -np.log(theta1))) for n_ in ns1])

# ============================================================== Fig. S2: how tight are the bounds?
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
c.plot(kk, 10 ** np.array(d["upper_log10"]), color=RED, lw=1.5, label="upper bound (Thm.~1)")
c.plot(d["rep_k"], d["rep_depth"], "o", ms=4.0, color=BLUE, mec=BLUE_DARK, mew=0.6, label="error-correcting reservoir")
c.set_yscale("log"); c.set_xlim(0, 31); c.set_ylim(1, 1e21)
c.set_yticks([1, 1e5, 1e10, 1e15, 1e20])
legend(c, loc="upper left", handlelength=1.3, borderaxespad=0.4)
xlabel(c, "Input qubits", "k")
ylabel(c, "Memory depth", r"W(\varepsilon)")
panel(c, "c", "Bounds", r"$q=0.5$, $\varepsilon=0.01$")
save(fig, "figS2.pdf")

# ============================================================== Fig. S3: washout of a redundant initial state
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
save(fig, "figS3.pdf")

# ============================================================== Fig. S4: exact response of the error-correcting reservoir
q = Fraction(9, 10); p = (1 - q) / 2


def p_r(r):
    return sum(Fraction(comb(r, j)) * p ** j * (1 - p) ** (r - j) for j in range(r // 2 + 1, r + 1))


lam = {r: 1 - 2 * float(p_r(r)) for r in range(1, 20, 2)}
alpha = -0.5 * log(1 - 0.81)
ks = np.arange(3, 18, 2)
ramp = dict(zip(ks.tolist(), blues(len(ks))))       # one shade per k, light (k = 3) to dark (k = 17)
fig = figure(TEXTWIDTH, 2.05)
a, b = even_row(fig, 2, left=0.47, right=0.06, gap=0.66)
t = np.logspace(0, 8.7, 800)
a.axhline(0.5, color=GREY, lw=0.8, ls=(0, (1.5, 1.5)), zorder=1)
for k in (3, 7, 11, 15):
    r = k - 2; col = ramp[k]
    a.plot(t, lam[r] ** t, color=col, lw=1.5, zorder=3, label=r"$%d$" % k)
    th = log(2) / -log(lam[r])
    a.plot(th, 0.5, "o", ms=4.5, color=col, mec=darker(col, 0.6), mew=0.7, zorder=4)
a.set_xscale("log"); a.set_xlim(1, 4e8); a.set_ylim(-0.03, 1.1)
a.set_xticks([1, 1e2, 1e4, 1e6, 1e8])
xlabel(a, "Time since storage", "t")
ylabel(a, "Signal", r"\langle Z\rangle_t/q")
panel(a, "a", "Exact decay of a stored bit", r"$q=0.9$")
legend(a, loc="center right", title=r"$k$", handlelength=1.2, borderaxespad=0.4)
T = [floor(log(2) / -log(lam[k - 2])) for k in ks]
kk = np.linspace(3, 17.5, 200)
b.plot(kk, np.exp(alpha * (kk - 2)) / 4, color=BLUE, lw=1.1, ls=(0, (4, 2.5)), zorder=2,
       label=r"bound $e^{\alpha_q r}/4$")
b.plot(ks, T, color=GREY_LIGHT, lw=0.9, zorder=3)
for kv, Tv in zip(ks, T):
    b.plot(kv, Tv, "o", ms=4.8, color=ramp[kv], mec=darker(ramp[kv], 0.6), mew=0.7, zorder=4)
b.plot([], [], "o", ms=4.8, color=BLUE, mec=darker(BLUE, 0.6), mew=0.7, label="exact")
b.set_yscale("log"); b.set_ylim(0.5, 3e7); b.set_xlim(2, 18.2)
b.set_xticks([3, 5, 7, 9, 11, 13, 15, 17]); b.set_yticks([1, 1e2, 1e4, 1e6])
b.annotate(r"$1.9\times10^{6}$", xy=(17, T[-1]), xytext=(14.6, 5.5e6), fontsize=FS, ha="center", va="center",
           arrowprops=dict(arrowstyle="-", lw=0.6, color=INK, shrinkA=1, shrinkB=3))
label(b, 2.6, 1.6e5, r"$\times 5.6$ per two" + "\n" + "input qubits", color=BLUE_DARK, ha="left", va="center",
      linespacing=1.1)
xlabel(b, "Input qubits", r"k=r+2")
ylabel(b, "Half-life")
panel(b, "b", "Half-life", r"$q=0.9$")
legend(b, loc="lower right", handlelength=1.6, borderaxespad=0.4)
save(fig, "figS4.pdf")
print("half-lives q=0.9:", dict(zip(ks.tolist(), T)))

# ============================================================== Fig. S5: entropy budget
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
save(fig, "figS5.pdf")

# ============================================================== Fig. S6: simulations
qf, eps = 0.9, 1e-2
fig = figure(TEXTWIDTH, 2.05)
a, b, c = even_row(fig, 3, left=0.47, right=0.06, gap=0.62)
# a: forgetting curves (all n = 8)
L = np.arange(0, 700)
a.plot(L + 1, qf ** (L + 1), zorder=2, **IDLE)
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
label(a, 1.4, 1.12, r"\textbf{error-correcting reservoir}", color=BLUE_DARK, ha="left", va="bottom")
a.set_xscale("log"); a.set_yscale("log")
a.set_xlim(1, 700); a.set_ylim(1e-3, 2.4)
a.set_xticks([1, 10, 100]); a.set_xticklabels(["1", "10", r"$10^2$"])
xlabel(a, "Time steps", "L+1")
ylabel(a, "Trace distance", r"D(L)")
panel(a, "a", "Forgetting", r"$n=8$")


def collect(model, n):
    """Memory depth versus q for the same six reservoirs (q = 0.9 from the main runs)."""
    pts = {}
    for e in R + N:
        if e["model"] == model and e["n"] == n and e["k"] == 1:
            pts[e["q"]] = e["W"]
    return pts


qq = np.linspace(0.85, 0.9995, 400)
b.plot(1 - qq, np.log(1 / eps) / -np.log(qq), zorder=1, **IDLE)
label(b, 4.2e-3, 3.4e2, "idle qubit", ha="left", va="center")
summary = {}
for model in ("ising", "haar"):
    st = STY[model]
    pts = collect(model, 6)
    qs = sorted(qv for qv in pts if qv < 1)
    x = [1 - qv for qv in qs]; mu = [np.mean(pts[qv]) for qv in qs]; sd = [np.std(pts[qv]) for qv in qs]
    b.plot(x, mu, color=st["color"], lw=0.9, zorder=2)
    b.errorbar(x, mu, yerr=sd, fmt=st["mk"], ms=st["ms"], color=st["color"], mec=darker(st["color"], 0.6), mew=0.8,
               ecolor=darker(st["color"], 0.7), elinewidth=0.8, label=r"%s, $n=6$" % st["name"], zorder=3)
    W1 = np.mean(pts[1.0])
    b.axhline(W1, color=st["color"], lw=0.9, ls=(0, (1, 1.5)), zorder=1)
    summary[model] = dict(W1=W1, W1_range=(min(pts[1.0]), max(pts[1.0])))
b.set_xscale("log"); b.set_yscale("log")
b.set_xlim(0.16, 8e-4); b.set_ylim(2, 6e3)
b.set_xticks([0.1, 0.01, 0.001]); b.set_xticklabels([r"$10^{-1}$", r"$10^{-2}$", r"$10^{-3}$"])
b.plot([], [], color=INK, lw=0.9, ls=(0, (1, 1.5)), label="noiseless limit")
legend(b, loc="upper left", handlelength=1.4, borderaxespad=0.4)
xlabel(b, "Noise per time step", "1-q")
ylabel(b, "Memory depth", r"W(\varepsilon)")
panel(b, "b", "Weak noise", r"$k=1$")
taus = [e["tau"] for e in TAU]
mu = [np.mean(e["W"]) for e in TAU]; sd = [np.std(e["W"]) for e in TAU]
st = STY["ising"]
c.plot(taus, mu, color=st["color"], lw=0.9)
c.errorbar(taus, mu, yerr=sd, fmt=st["mk"], ms=st["ms"], color=st["color"], mec=darker(st["color"], 0.6), mew=0.8,
           ecolor=darker(st["color"], 0.7), elinewidth=0.8, zorder=3, label=r"Ising, $n=6$")
c.axhline(log(1 / eps) / -log(0.9) // 1, **IDLE)
label(c, 0.25, 41.2, "idle qubit", ha="left", va="top")
c.set_xscale("log"); c.set_xlim(0.2, 45); c.set_ylim(0, 48)
c.set_xticks([0.3, 1, 3, 10, 30]); c.set_xticklabels(["0.3", "1", "3", "10", "30"])
legend(c, loc="center right", handlelength=1.0, borderaxespad=0.4)
xlabel(c, "Evolution time per step", r"J\Delta t")
ylabel(c, "Memory depth", r"W(\varepsilon)")
panel(c, "c", "Ising dynamics", r"$q=0.9$, $k=1$")
save(fig, "figS6.pdf")
print("noiseless limit n=6:", summary)
print("rep k=5 full-state depth:", 1 + max(i for i, v in enumerate(D) if v > eps))

# ============================================================== Fig. S7: standard reservoirs versus input qubits
def get_cold(model, n, k):
    for e in COLD:
        if e["model"] == model and e["n"] == n and e["k"] == k:
            return e


fig = figure(COLUMNWIDTH, 2.05)
ax = add_axes(fig, 0.47, 0.40, COLUMNWIDTH - 0.47 - 0.06, 2.05 - 0.40 - 0.20)
ax.axhline(log(1 / eps) / -log(0.9) // 1, zorder=1, **IDLE)
label(ax, 0.68, 41.2, "idle qubit", ha="left", va="top")
ks = [1, 2, 3, 4]
for model in ("ising", "haar"):
    st = STY[model]
    mu = [np.mean(get(model, 8, k)["W"]) for k in ks]
    sd = [np.std(get(model, 8, k)["W"]) for k in ks]
    muc = [mu[0]] + [np.mean(get_cold(model, 8, k)["W"]) for k in ks[1:]]
    sdc = [sd[0]] + [np.std(get_cold(model, 8, k)["W"]) for k in ks[1:]]
    x = np.array(ks)
    ax.plot(x - 0.06, mu, color=st["color"], lw=0.9, zorder=2)
    ax.errorbar(x - 0.06, mu, yerr=sd, fmt=st["mk"], ms=st["ms"], color=st["color"], mec=darker(st["color"], 0.6),
                mew=0.8, ecolor=darker(st["color"], 0.7), elinewidth=0.8, zorder=3,
                label=r"%s, input on all $k$ qubits" % st["name"])
    ax.plot(x + 0.06, muc, color=st["color"], lw=0.9, ls=(0, (3, 2)), zorder=2)
    ax.errorbar(x + 0.06, muc, yerr=sdc, fmt=st["mk"], ms=st["ms"], color=st["color"], mfc="white",
                mec=darker(st["color"], 0.6), mew=0.8, ecolor=darker(st["color"], 0.7), elinewidth=0.8, zorder=3,
                label=r"%s, extra qubits in $|0\rangle$" % st["name"])
ax.set_xlim(0.6, 4.4); ax.set_ylim(0, 50); ax.set_xticks(ks)
legend(ax, loc="upper right", handlelength=1.0, borderaxespad=0.4, bbox_to_anchor=(1.0, 0.80))
xlabel(ax, "Input qubits", "k")
ylabel(ax, "Memory depth", r"W(\varepsilon)")
ax.set_title(r"No gain from input qubits", loc="left", fontsize=FS, pad=4)
ax.set_title(r"$n=8$, $q=0.9$", loc="right", fontsize=FS, pad=4)
save(fig, "figS7.pdf")
print("Fig. S7: input", [(m, [round(np.mean(get(m, 8, k)["W"]), 1) for k in ks]) for m in ("ising", "haar")],
      "cold", [(m, [round(np.mean(get_cold(m, 8, k)["W"]), 1) for k in ks[1:]]) for m in ("ising", "haar")])
