"""Fig. 2: why every reservoir forgets.
a  Step 1, computed: the purity bound of Eq. (purity) for reservoirs that start in a pure state.
b  Steps 2 and 3, schematic: one time step maps the box V <= 1 into the shaded region inside V <= 1 - delta."""
import sys; sys.path.insert(0, ".")
from figstyle import *
import numpy as np
from matplotlib.patches import Rectangle
setup()

q, k = 0.9, 2
theta = 2 * q ** 2 / (1 + q ** 2)
cap = 2 * k * q ** 2 / (1 - q ** 2)            # pure qubits' worth of purity of every echo state

fig = figure(TEXTWIDTH, 2.05)
a, b = even_row(fig, 2, left=0.47, right=0.06, gap=0.66)

# =============================================================================== a: noise caps the purity
t = np.arange(0, 101)
ns = [100, 1000, 10000]
cols = blues(4)[1:]
for n, col in zip(ns, cols):
    y = theta ** t * n + (1 - theta ** t) * cap
    lab = {100: r"$10^2$", 1000: r"$10^3$", 10000: r"$10^4$"}[n]
    a.plot(t, y, color=col, lw=1.4, zorder=3, label=lab)
    tw = np.log(n - cap) / -np.log(theta)       # bound reaches cap + 1 bit, i.e. P <= sqrt(2) P_*
    a.plot(tw, cap + 1, "o", ms=4.5, color=col, mec=darker(col, 0.6), mew=0.7, zorder=5)
a.axhline(cap, color=RED, lw=1.2, ls=(0, (4, 2.5)), zorder=2)
label(a, 1.5, cap / 1.2, r"cap $2kq^2/(1-q^2)\approx17$, any $n$", color=RED_DARK, ha="left", va="top")
label(a, 99, cap / 1.2, r"dots: washout $\propto\log n$", ha="right", va="top")
a.set_yscale("log"); a.set_xlim(0, 100); a.set_ylim(5, 4e4)
legend(a, loc="upper right", title=r"reservoir size $n$", ncol=3, handlelength=1.2, columnspacing=0.8)
a.set_yticks([10, 1e2, 1e3, 1e4])
xlabel(a, "Time step", "t")
ylabel(a, "Purity bound", r"\log_2P_t^2")
panel(a, "a", "Step 1: noise caps the purity", r"$q=0.9$, $k=2$")

# =============================================================================== b: one distance contracts
d = 0.22                                         # exaggerated contraction rate 1 - delta = 0.78
b.grid(False)
b.set_xlim(0, 1.86); b.set_ylim(0, 1.17)
b.add_patch(Rectangle((0, 0), 1 - d, 0.5, fc=BLUE_FILL, ec="none", zorder=0))
b.plot([0, 1 - d, 1 - d], [0.5, 0.5, 0], color=BLUE, lw=0.9, zorder=1)
b.plot([0, 1, 1], [1, 1, 0], color=INK, lw=1.4, zorder=2)                       # V = 1
b.plot([0, 1 - d, 1 - d], [1 - d, 1 - d, 0], color=BLUE_DARK, lw=1.1, ls=(0, (4, 2.5)), zorder=2)  # V = 1-delta
label(b, 0.03, 0.975, r"$V\le1$", ha="left", va="top")
label(b, 0.03, 1 - d - 0.025, r"$V\le1-\delta$", color=BLUE_DARK, ha="left", va="top")
label(b, (1 - d) / 2 - 0.08, 0.25, "after one\ntime step", color=BLUE_DARK, bold=True, ha="center", va="center",
      linespacing=1.15)
x0, y0, y1, x1 = 0.92, 0.92, 0.40, 0.60          # one difference X and its image after one time step
arw = dict(arrowstyle="-|>", lw=1.3, color=RED, shrinkA=3.2, shrinkB=3.2, mutation_scale=8)
b.annotate("", xy=(x0, y1), xytext=(x0, y0), arrowprops=arw, zorder=4)
b.annotate("", xy=(x1, y1), xytext=(x0, y1), arrowprops=arw, zorder=4)
b.plot(x0, y0, "o", ms=4.8, color=INK, mec=INK, zorder=5)
b.plot(x0, y1, "o", ms=2.6, color=RED, mec=RED, zorder=5)
b.plot(x1, y1, "o", ms=4.8, mfc="white", mec=BLUE_DARK, mew=1.0, zorder=5)
label(b, x0 - 0.035, y0, r"$X$", ha="right", va="center")
label(b, x1 - 0.04, y1, r"$X'$", color=BLUE_DARK, ha="right", va="center")
label(b, 1.05, (y0 + y1) / 2, r"\textbf{Step 1}" + "\n" + "noise caps the 2-norm", color=RED_DARK, ha="left",
      va="center", linespacing=1.15)
label(b, 1.05, y1 + 0.075, r"\textbf{Step 2}" + "\n" + "spread-out differences" + "\n" + "lose distinguishability",
      color=RED_DARK, ha="left", va="top", linespacing=1.15)
b.set_xticks([0, 1 - d, 1]); b.set_xticklabels([r"$0$", r"$1-\delta$", r"$1$"])
b.set_yticks([0, 0.5, 1 - d, 1]); b.set_yticklabels([r"$0$", r"$\tfrac12$", r"$1-\delta$", r"$1$"])
xlabel(b, "Distinguishability", r"\lvert X\rvert_1")
ylabel(b, "2-norm", r"\lvert X\rvert_2/R")
panel(b, "b", "Steps 2 and 3: one distance contracts", r"any $U$, $u$, $n$")
save(fig, "fig2.pdf")
print("cap", cap, "theta", theta, "washout", [round(np.log(n - cap) / -np.log(theta), 1) for n in ns])
