"""Fig. 3: the memory limit (schematic).
a  Same number k of input qubits, ten times the size: the same limit. Two more input qubits raise it.
b  The limit lies between two exponentials in k, for every size n (Theorem 1).
Both panels are schematic: the axes carry no numbers, and the curves show the form of the bounds."""
import sys; sys.path.insert(0, ".")
from figstyle import *
import numpy as np
from matplotlib.patches import Rectangle
from matplotlib.transforms import blended_transform_factory
setup()

# =============================================================================== common geometry
CW, CH = 3.525, 1.85                     # width of each half and height of the figure (in)
AXW, AXH = CW - 0.28 - 0.34, CH - 0.40 - 0.20
fig = figure(2 * CW, CH)

def right_label(ax, y, s, color):
    tr = blended_transform_factory(ax.transAxes, ax.transData)
    label(ax, 1.02, y, s, color=color, transform=tr, ha="left", va="center", clip_on=False)

# =============================================================================== a: same input qubits, same limit
ax = add_axes(fig, 0.28, 0.40, AXW, AXH)
xl, top = (8, 2600), 10 ** 5.45
ax.set_xscale("log"); ax.set_yscale("log")
ax.set_xlim(*xl); ax.set_ylim(1, top)
W2, W4, W6 = 10 ** 2.45, 10 ** 3.4, 10 ** 4.35
ax.fill_between(xl, W2, top, color=RED_FILL, lw=0, zorder=0)
ax.axhline(W2, color=BLUE_DARK, lw=1.6, zorder=3)
for W in (W4, W6):
    ax.axhline(W, color=BLUE, lw=1.0, ls=(0, (4, 2.5)), zorder=2)
right_label(ax, W2, r"$W_{q,2}$", BLUE_DARK)
right_label(ax, W4, r"$W_{q,4}$", BLUE)
right_label(ax, W6, r"$W_{q,6}$", BLUE)
label(ax, 2350, 10 ** 4.93, r"unreachable with $\bm{k=2}$, for any $\bm n$", color=RED_DARK, bold=True,
      ha="right", va="center")
nA, nB, h = 20, 200, 10 ** 0.85         # equal bars: more qubits do not lengthen the memory
for n0, lab in ((nA, "A"), (nB, "B")):
    w = 0.08
    ax.add_patch(Rectangle((n0 * 10 ** -w, 1.0), n0 * (10 ** w - 10 ** -w), h - 1, fc=BLUE_FILL, ec=BLUE_DARK,
                           lw=0.8, zorder=4))
    ax.plot([n0, n0], [h, W2], ls=(0, (1, 1.5)), lw=0.8, color=GREY, zorder=3)
    label(ax, n0 * 10 ** 0.13, 10 ** 0.42, r"\textbf{%s}\enspace$n=%d$" % (lab, n0), ha="left", va="center")
    ax.plot(n0, W2, "o", ms=4.6, mfc="white", mec=INK, mew=0.9, zorder=6)
# the size arrow sits well below the limit line: more qubits move the reservoir, not the limit
ya = 10 ** 1.55
ax.annotate("", xy=(nB * 0.85, ya), xytext=(nA * 1.18, ya),
            arrowprops=dict(arrowstyle="-|>", lw=1.2, color=INK, shrinkA=0, shrinkB=0, mutation_scale=8), zorder=5)
label(ax, np.sqrt(nA * nB), ya * 10 ** 0.08, r"$10\times$ more qubits", ha="center", va="bottom")
ax.annotate("", xy=(nA, W4 / 1.13), xytext=(nA, W2 * 1.13),
            arrowprops=dict(arrowstyle="-|>", lw=1.3, color=PURPLE, shrinkA=0, shrinkB=0, mutation_scale=8), zorder=5)
label(ax, nA * 1.2, np.sqrt(W2 * W4), r"$+2$ input qubits: higher limit", color=PURPLE_DARK, ha="left",
      va="center")
ax.set_yticks([]); ax.minorticks_off(); ax.grid(False)
ax.set_xticks([10, 100, 1000]); ax.set_xticklabels([r"$10$", r"$10^2$", r"$10^3$"])
xlabel(ax, "Reservoir size", "n")
ylabel(ax, "Memory depth")
panel(ax, "a", "Same input qubits, same limit", r"$k=2$")

# =============================================================================== b: memory limit versus k
ax = add_axes(fig, CW + 0.28, 0.40, AXW, AXH)
k = np.linspace(0, 20, 400)
c1, c2 = 0.34, 0.62
lo, hi = np.exp(c1 * k), np.exp(c2 * k)
top, bot = np.exp(c2 * 20) * 3, 10 ** -0.25
ax.set_yscale("log"); ax.set_xlim(0, 20); ax.set_ylim(bot, top)
ax.fill_between(k, hi, top, color=RED_FILL, lw=0, zorder=0)
ax.fill_between(k, bot, lo, color=BLUE_FILL, lw=0, zorder=0)
ax.fill_between(k, lo, hi, facecolor="none", edgecolor="#C8C8C8", hatch="/////", lw=0, zorder=0)
ax.fill_between([0, 20], bot, 1, color=BLUE_FILL, lw=0, zorder=0)
ax.plot(k, hi, color=RED, lw=1.6, zorder=3)
ax.plot(k, lo, color=BLUE, lw=1.6, zorder=3)
Wk = lambda x: np.exp(0.5 * (c1 + c2) * x + 0.25 * np.sin(x / 3))
ax.plot(k, Wk(k), color=INK, lw=0.9, ls=(0, (3, 2)), zorder=3)
for kk in (2, 4, 6):
    ax.plot(kk, Wk(kk), "o", ms=4.0, mfc="white", mec=INK, mew=0.9, zorder=6)
right_label(ax, Wk(20), r"$W_{q,k}$", INK)
label(ax, 0.5, top / 2.6, "no reservoir remembers this long", color=RED_DARK, bold=True, ha="left", va="top")
label(ax, 19.6, bot * 1.9, r"attainable with $\bm k$ input qubits", color=BLUE_DARK, bold=True, ha="right",
      va="bottom")
label(ax, 11.0, np.exp(c2 * 11.0) * 1.9, r"upper bound $2^{k/(1-q)^2}$", color=RED_DARK, ha="right", va="bottom")
label(ax, 19.6, 10 ** 1.15, r"lower bound $e^{\alpha_qk}$", color=BLUE_DARK, ha="right", va="bottom")
ax.set_yticks([]); ax.minorticks_off(); ax.grid(False)
ax.set_xticks([0, 2, 4, 6, 10, 15, 20])
xlabel(ax, "Input qubits per time step", "k")
ylabel(ax, "Memory depth")
panel(ax, "b", "More input qubits, higher limit", r"any $n$")
save(fig, "fig3.pdf")
print("Fig. 3 done")

