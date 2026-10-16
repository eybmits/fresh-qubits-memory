"""Fig. 3, panels b, c: exact response of the repetition-code reservoir (q = 0.9). Panel a is in fig3.tex."""
import sys; sys.path.insert(0, ".")
from figstyle import *
import numpy as np
from fractions import Fraction
from math import comb, log, floor
setup()
q = Fraction(9, 10); p = (1 - q) / 2
def p_r(r):
    return sum(Fraction(comb(r, j)) * p ** j * (1 - p) ** (r - j) for j in range(r // 2 + 1, r + 1))
lam = {r: 1 - 2 * float(p_r(r)) for r in range(1, 20, 2)}
alpha = -0.5 * log(1 - 0.81)
ks = np.arange(3, 18, 2)
ramp = dict(zip(ks.tolist(), blues(len(ks))))       # one shade per k, light (k = 3) to dark (k = 17)

fig = figure(4.40, 2.05)
b, c = even_row(fig, 2, left=0.45, right=0.06, gap=0.60)
# ------------------------------------------------------------------ b: exact decay of the stored signal
t = np.logspace(0, 8.7, 800)
b.axhline(0.5, color=GREY, lw=0.8, ls=(0, (1.5, 1.5)), zorder=1)
for k in (3, 7, 11, 15):
    r = k - 2; col = ramp[k]
    b.plot(t, lam[r] ** t, color=col, lw=1.5, zorder=3, label=r"$%d$" % k)
    th = log(2) / -log(lam[r])
    b.plot(th, 0.5, "o", ms=4.5, color=col, mec=darker(col, 0.6), mew=0.7, zorder=4)
b.set_xscale("log"); b.set_xlim(1, 4e8); b.set_ylim(-0.03, 1.1)
b.set_xticks([1, 1e2, 1e4, 1e6, 1e8])
xlabel(b, "Time since storage", "t")
ylabel(b, "Signal", r"\langle Z\rangle_t/q")
panel(b, "b", "Exact decay", r"$q=0.9$")
legend(b, loc="center right", title=r"$k$", handlelength=1.2, borderaxespad=0.4)
# ------------------------------------------------------------------ c: half-life versus input qubits
T = [floor(log(2) / -log(lam[k - 2])) for k in ks]
kk = np.linspace(3, 17.5, 200)
c.plot(kk, np.exp(alpha * (kk - 2)) / 4, color=BLUE, lw=1.1, ls=(0, (4, 2.5)), zorder=2,
       label=r"bound $e^{\alpha_q r}/4$")
c.plot(ks, T, color=GREY_LIGHT, lw=0.9, zorder=3)
for kv, Tv in zip(ks, T):
    c.plot(kv, Tv, "o", ms=4.8, color=ramp[kv], mec=darker(ramp[kv], 0.6), mew=0.7, zorder=4)
c.plot([], [], "o", ms=4.8, color=BLUE, mec=darker(BLUE, 0.6), mew=0.7, label="exact")
c.set_yscale("log"); c.set_ylim(0.5, 3e7); c.set_xlim(2, 18.2)
c.set_xticks([3, 7, 11, 15]); c.set_yticks([1, 1e2, 1e4, 1e6])
c.annotate(r"$1.9\times10^{6}$", xy=(17, T[-1]), xytext=(12.6, 5.5e6), fontsize=FS, ha="center", va="center",
           arrowprops=dict(arrowstyle="-", lw=0.6, color=INK, shrinkA=1, shrinkB=3))
label(c, 2.6, 1.6e5, r"$\times 5.6$ per two" + "\n" + "input qubits", color=BLUE_DARK, ha="left", va="center",
      linespacing=1.1)
xlabel(c, "Input qubits", "k")
ylabel(c, "Half-life")
panel(c, "c", "Half-life", r"$q=0.9$")
legend(c, loc="lower right", handlelength=1.6, borderaxespad=0.4)
save(fig, "fig3bc.pdf")
print(dict(zip(ks.tolist(), T)))
