"""Fig. 1, panels a, c, d (matplotlib). Panel b is drawn in TikZ; fig1.tex assembles all four panels.

Geometry (inches): row 1 is 2.25 high (panel a: 2.05 wide), row 2 is 1.95 high (panels c, d: 3.48 wide).
Every panel has a top margin of 0.20 in, so all titles sit 0.20 in - 4 pt below the top of their row."""
import sys; sys.path.insert(0, ".")
from figstyle import *
import numpy as np
from matplotlib.patches import Rectangle
from matplotlib.transforms import blended_transform_factory
setup()

# =============================================================================== a: temporal task
def mackey_glass(T, tau=17, beta=0.2, gamma=0.1, n=10, dt=0.05, x0=1.2, burn=600):
    steps_per = int(round(1 / dt)); lag = int(round(tau / dt))
    total = (T + burn) * steps_per
    x = np.full(total + lag + 1, x0)
    for i in range(lag, total + lag):
        xl = x[i - lag]
        x[i + 1] = x[i] + dt * (beta * xl / (1 + xl ** n) - gamma * x[i])
    return x[lag::steps_per][burn:burn + T]

mg = mackey_glass(160)
u = (mg - mg.min()) / (mg.max() - mg.min())
t = np.arange(len(u))
tnow, lagT = 145, 100
fig = figure(2.05, 2.25)
ax = add_axes(fig, 0.28, 0.40, 2.05 - 0.28 - 0.06, 2.25 - 0.40 - 0.20)
ax.plot(t[:tnow + 1], u[:tnow + 1], color=INK, lw=0.8, zorder=2)
ax.plot(t[:tnow + 1], u[:tnow + 1], "o", ms=1.5, color=INK, mew=0, zorder=3)
ya = 1.27                                   # height of the dimension arrow
for tt in (tnow - lagT, tnow):              # dimension lines from the two inputs up to the arrow
    ax.plot([tt, tt], [u[tt] + 0.06, ya + 0.07], ls=(0, (2, 1.6)), lw=0.75, color=PURPLE, zorder=1)
    ax.plot(tt, u[tt], "o", ms=5, color=PURPLE, mec="white", mew=0.8, zorder=5)
label(ax, tnow - lagT - 4, u[tnow - lagT] + 0.04, r"$u_{t-100}$", color=PURPLE_DARK, ha="right", va="bottom")
label(ax, tnow - 4, u[tnow] + 0.04, r"$u_{t}$", color=PURPLE_DARK, ha="right", va="bottom")
ax.annotate("", xy=(tnow - lagT, ya), xytext=(tnow, ya),
            arrowprops=dict(arrowstyle="<|-|>", lw=0.8, color=INK, shrinkA=0, shrinkB=0, mutation_scale=6))
label(ax, (2 * tnow - lagT) / 2, ya + 0.05, "100 time steps", ha="center", va="bottom")
label(ax, 75, -0.31, r"$y_{t+1}=0.7\,u_t+0.3\,u_{t-100}$", ha="center", va="center",
      bbox=dict(boxstyle="round,pad=0.32,rounding_size=0.22", fc=GREY_FILL, ec=INK, lw=0.7))
ax.set_xlim(-5, 153); ax.set_ylim(-0.53, 1.5)
ax.set_xticks([0, 50, 100, 145]); ax.set_xticklabels(["0", "50", "100", r"$t$"])
ax.set_yticks([0, 0.5, 1])
xlabel(ax, "Time step")
ax.set_ylabel(r"$u_t$", rotation=0, labelpad=0)
ax.yaxis.set_label_coords(-0.115, 0.935)
panel(ax, "a", "Temporal task")
save(fig, "fig1a.pdf")

# =============================================================================== c, d: common geometry
CW, CH = 3.48, 1.95
AX = dict(left=0.28, bottom=0.40, width=CW - 0.28 - 0.34, height=CH - 0.40 - 0.20)

def right_label(ax, y, s, color):
    tr = blended_transform_factory(ax.transAxes, ax.transData)
    label(ax, 1.02, y, s, color=color, transform=tr, ha="left", va="center", clip_on=False)

# =============================================================================== c: same input qubits, same limit
fig = figure(CW, CH)
ax = add_axes(fig, **AX)
xl, top = (8, 2600), 10 ** 5.6
ax.set_xscale("log"); ax.set_yscale("log")
ax.set_xlim(*xl); ax.set_ylim(1, top)
W2, W4, W6 = 10 ** 2.35, 10 ** 3.5, 10 ** 4.65
ax.fill_between(xl, W2, top, color=RED_FILL, lw=0, zorder=0)
ax.axhline(W2, color=BLUE_DARK, lw=1.6, zorder=3)
for W in (W4, W6):
    ax.axhline(W, color=BLUE, lw=1.0, ls=(0, (4, 2.5)), zorder=2)
right_label(ax, W2, r"$W_{q,2}$", BLUE_DARK)
right_label(ax, W4, r"$W_{q,4}$", BLUE)
right_label(ax, W6, r"$W_{q,6}$", BLUE)
label(ax, 2350, 10 ** 5.12, r"unreachable with $\bm{k=2}$, for any $\bm n$", color=RED_DARK, bold=True,
      ha="right", va="center")
nA, nB, h = 20, 200, 10 ** 1.0          # equal bars: more qubits do not lengthen the memory
for n0, lab in ((nA, "A"), (nB, "B")):
    w = 0.08
    ax.add_patch(Rectangle((n0 * 10 ** -w, 1.0), n0 * (10 ** w - 10 ** -w), h - 1, fc=BLUE_FILL, ec=BLUE_DARK,
                           lw=0.8, zorder=4))
    ax.plot([n0, n0], [h, W2], ls=(0, (1, 1.5)), lw=0.8, color=GREY, zorder=3)
    label(ax, n0 * 10 ** 0.13, 10 ** 0.5, r"\textbf{%s}\enspace$n=%d$" % (lab, n0), ha="left", va="center")
    ax.plot(n0, W2, "o", ms=4.6, mfc="white", mec=INK, mew=0.9, zorder=6)
ax.annotate("", xy=(nB * 0.86, W2), xytext=(nA * 1.16, W2),
            arrowprops=dict(arrowstyle="-|>", lw=1.2, color=INK, shrinkA=0, shrinkB=0, mutation_scale=8), zorder=5)
label(ax, np.sqrt(nA * nB), 10 ** 2.17, r"$10\times$ more qubits:" + "\n" + "same limit", ha="center", va="top",
      linespacing=1.15)
ax.annotate("", xy=(nA, W4 / 1.13), xytext=(nA, W2 * 1.13),
            arrowprops=dict(arrowstyle="-|>", lw=1.3, color=PURPLE, shrinkA=0, shrinkB=0, mutation_scale=8), zorder=5)
label(ax, nA * 1.2, np.sqrt(W2 * W4), r"$+2$ input qubits: higher limit", color=PURPLE_DARK, ha="left",
      va="center")
ax.set_yticks([]); ax.minorticks_off(); ax.grid(False)
ax.set_xticks([10, 100, 1000]); ax.set_xticklabels([r"$10$", r"$10^2$", r"$10^3$"])
xlabel(ax, "Reservoir size", "n")
ylabel(ax, "Memory depth")
panel(ax, "c", "Same input qubits, same limit", r"$k=2$")
save(fig, "fig1c.pdf")

# =============================================================================== d: memory limit versus k
fig = figure(CW, CH)
ax = add_axes(fig, **AX)
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
label(ax, 11.0, np.exp(c2 * 11.0) * 1.9, r"upper bound $e^{c_2k}$", color=RED_DARK, ha="right", va="bottom")
label(ax, 19.6, 10 ** 1.15, r"lower bound $e^{c_1k}$", color=BLUE_DARK, ha="right", va="bottom")
ax.set_yticks([]); ax.minorticks_off(); ax.grid(False)
ax.set_xticks([0, 2, 4, 6, 10, 15, 20])
xlabel(ax, "Input qubits per time step", "k")
ylabel(ax, "Memory depth")
panel(ax, "d", "More input qubits, higher limit", r"any $n$")
save(fig, "fig1d.pdf")
print("panels a, c, d done")
