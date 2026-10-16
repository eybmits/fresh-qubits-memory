"""Figures 2 and 4(b,c) for 'The Memory Limits of Noisy Quantum Reservoirs'.
Fig. 2 is a schematic (no numerical axes); Fig. 4(b,c) are exact values for the repetition-code reservoir."""
from fractions import Fraction
from math import comb, log, floor
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

BLUE, PINK, GREEN, GOLD, GRAY, INK = "#3D6FB5", "#E35D6A", "#2E9B57", "#D9A82B", "#8C8C8C", "#222222"
plt.rcParams.update({
    "font.family": "DejaVu Sans", "mathtext.fontset": "dejavusans",
    "font.size": 7.2, "axes.labelsize": 7.6, "xtick.labelsize": 6.8, "ytick.labelsize": 6.8,
    "legend.fontsize": 6.6, "axes.linewidth": 0.6, "xtick.major.width": 0.6, "ytick.major.width": 0.6,
    "xtick.minor.width": 0.4, "ytick.minor.width": 0.4, "xtick.direction": "out", "ytick.direction": "out",
    "pdf.fonttype": 42, "axes.edgecolor": "#333333",
})

def panel_label(ax, s):
    ax.text(0.97, 0.95, s, transform=ax.transAxes, ha="right", va="top", fontsize=8.5, fontweight="bold")

def grid(ax):
    ax.grid(True, which="major", color="#d9d9d9", lw=0.5, ls=(0, (2, 2)), zorder=0)

# ---------------------------------------------------------------- Fig. 2 (schematic)
fig, (a, b) = plt.subplots(1, 2, figsize=(7.0, 2.35), gridspec_kw={"wspace": 0.28})
k = np.linspace(0, 20, 400)
c1, c2 = 0.30, 0.62
lo, hi = np.exp(c1 * k), np.exp(c2 * k)
top = 6e5
a.set_yscale("log"); a.set_xlim(0, 20); a.set_ylim(1, top)
a.fill_between(k, hi, top, color=PINK, alpha=0.13, lw=0, zorder=1)
a.fill_between(k, 1, lo, color=BLUE, alpha=0.13, lw=0, zorder=1)
a.fill_between(k, lo, hi, facecolor="none", edgecolor="#bdbdbd", hatch="////", lw=0, zorder=1)
a.plot(k, hi, color=PINK, lw=1.6, zorder=3)
a.plot(k, lo, color=BLUE, lw=1.6, zorder=3)
a.text(1.0, 1.6e5, "no reservoir can remember\nthis long (Sec. III)", color="#a3303b", fontsize=7, va="top")
a.text(9.2, 1.6, "reached by the repetition-\ncode reservoir (Sec. IV)", color="#24508a", fontsize=7, va="bottom")
a.text(9.6, np.exp(c2 * 9.6) * 4.0, r"upper bound $e^{c_2k}$", color="#c0404c", fontsize=7, ha="right", va="bottom")
a.text(16.2, np.exp(c1 * 16.2) / 4.0, r"lower bound $e^{c_1k}$", color="#24508a", fontsize=7, ha="left", va="top",
       bbox=dict(boxstyle="square,pad=0.1", fc="#e3ebf6", ec="none"))
a.annotate("", xy=(7.0, np.exp(c2 * 7.0)), xytext=(7.0, np.exp(c1 * 7.0)),
           arrowprops=dict(arrowstyle="<->", lw=0.7, color="#555555"))
a.text(7.35, np.exp(0.5 * (c1 + c2) * 7.0), "gap in\nconstants", fontsize=6.5, color="#555555", va="center",
       bbox=dict(boxstyle="square,pad=0.15", fc="white", ec="none"))
a.set_xlabel(r"input qubits reinitialized per time step, $k$")
a.set_ylabel(r"memory depth $W_{q,k}(\varepsilon)$ (log scale)")
a.set_yticks([]); a.minorticks_off(); a.set_xticks([0, 5, 10, 15, 20])
panel_label(a, "a)")
for s in ("top", "right"):
    a.spines[s].set_visible(False)

n = np.logspace(1, np.log10(2.4e4), 300)
ceil = 2.0e3
b.set_xscale("log"); b.set_yscale("log"); b.set_xlim(10, 2.4e4); b.set_ylim(3, 6e4)
b.fill_between(n, ceil, 6e4, color=PINK, alpha=0.13, lw=0)
floor_ = 2.2e2
b.fill_between(n, floor_, ceil, facecolor="none", edgecolor="#bdbdbd", hatch="////", lw=0)
b.plot(n, np.full_like(n, ceil), color=PINK, lw=1.6)
b.plot(n, np.full_like(n, floor_), color=BLUE, lw=1.6)
b.text(13, 2.8e3, r"upper bound for fixed $k$: the same for every $n$", color="#a3303b", fontsize=7, va="bottom")
b.text(13, 1.75e2, r"lower bound, reached with $n\leq 2k$ qubits", color="#24508a", fontsize=7, va="top")
wash = 12 * np.log(n)
b.plot(n, wash, color=GOLD, lw=1.4, ls=(0, (4, 2)))
b.text(1.1e3, 46, r"washout of the initial state $\propto\log n$", color="#8a6a12", fontsize=6.8, ha="center", va="top")
for nn in (100, 1e4):
    b.plot([nn, nn], [3, 6e4], color="#9a9a9a", lw=0.6, ls=":")
for xa, lab in ((100, "A: 100 qubits"), (1e4, "B: 10 000 qubits")):
    b.plot([xa], [np.sqrt(ceil * floor_)], marker="o", ms=4.5, color=INK, mec="white", mew=0.7, zorder=5)
    b.text(xa * (1.18 if xa == 100 else 0.85), np.sqrt(ceil * floor_), lab, color=INK, fontsize=6.6,
           ha="left" if xa == 100 else "right", va="center",
           bbox=dict(boxstyle="square,pad=0.12", fc="white", ec="none"))
b.set_xlabel(r"total number of qubits, $n$")
b.set_ylabel(r"memory depth $W(\varepsilon)$ (log scale)")
b.set_yticks([]); b.minorticks_off()
b.set_xticks([10, 100, 1000, 10000]); b.set_xticklabels(["10", r"$10^2$", r"$10^3$", r"$10^4$"])
panel_label(b, "b)")
for s in ("top", "right"):
    b.spines[s].set_visible(False)
fig.subplots_adjust(left=0.06, right=0.99, bottom=0.17, top=0.97)
fig.savefig("fig_limit.pdf"); fig.savefig("fig_limit_preview.png", dpi=200)

# ---------------------------------------------------------------- Fig. 4 (b,c): exact data
q = Fraction(9, 10); p = (1 - q) / 2
alpha = -0.5 * log(1 - float(q) ** 2)
def p_r(r):
    return sum(Fraction(comb(r, j)) * p**j * (1 - p)**(r - j) for j in range(r // 2 + 1, r + 1))
rs = list(range(1, 16, 2)); ks = [r + 2 for r in rs]
lam = {r: 1 - 2 * float(p_r(r)) for r in rs}
T = [floor(log(2) / -log(lam[r])) for r in rs]
print("half-lives:", list(zip(ks, T)))

fig, (b, c) = plt.subplots(1, 2, figsize=(4.55, 2.15), gridspec_kw={"wspace": 0.42})
t = np.logspace(0, 7.3, 600)
for r, col in ((1, GOLD), (5, GREEN), (9, PINK), (13, BLUE)):
    b.plot(t, lam[r] ** t, color=col, lw=1.4, zorder=3)
    th = log(2) / -log(lam[r])
    b.plot([th], [0.5], "o", ms=3.6, color=col, mec="white", mew=0.6, zorder=4)
    t85 = log(0.86) / log(lam[r])
    b.text(t85 * 1.55, 0.86, rf"$k={r+2}$", color=col, fontsize=6.8, ha="left", va="center", fontweight="bold")
b.axhline(0.5, color="#9a9a9a", lw=0.6, ls=":", zorder=1)
b.set_xscale("log"); b.set_xlim(1, 2e7); b.set_ylim(0, 1.05)
b.set_xticks([1, 1e2, 1e4, 1e6])
b.set_xlabel(r"time steps since storage, $t$")
b.set_ylabel(r"signal $\langle Z\rangle_t\,/\,q=\lambda_r^{\,t}$")
grid(b); panel_label(b, "b)")
for s in ("top", "right"):
    b.spines[s].set_visible(False)

kk = np.linspace(3, 17.5, 200)
c.plot(kk, np.exp(alpha * (kk - 2)) / 4, color=GRAY, lw=1.1, ls=(0, (4, 2.5)), zorder=2, label="Chernoff bound")
c.plot(ks, T, color=BLUE, lw=1.3, zorder=3)
c.plot(ks, T, "o", ms=4.0, color=BLUE, mec="white", mew=0.7, zorder=4, label="exact")
c.set_yscale("log"); c.set_ylim(0.7, 2e7); c.set_xlim(2.2, 18)
c.set_xticks([3, 7, 11, 15]); c.set_yticks([1, 1e2, 1e4, 1e6])
c.set_xlabel(r"input qubits per time step, $k$")
c.set_ylabel("half-life (time steps)")
c.legend(loc="upper left", frameon=False, handlelength=1.6, borderaxespad=0.2)
c.annotate(r"$1.9\times10^{6}$", xy=(17, T[-1]), xytext=(13.3, 6.0e5), fontsize=6.6, ha="center",
           arrowprops=dict(arrowstyle="-", lw=0.5, color=INK))
grid(c); panel_label(c, "c)")
for s in ("top", "right"):
    c.spines[s].set_visible(False)
fig.subplots_adjust(left=0.12, right=0.99, bottom=0.2, top=0.97)
fig.savefig("fig_repetition.pdf"); fig.savefig("fig_repetition_preview.png", dpi=220)
