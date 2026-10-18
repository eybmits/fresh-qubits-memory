"""Fig. 2, panel a (matplotlib): a temporal task that needs a memory of 100 time steps. Panel b (the reservoir)
is drawn in TikZ, and fig2.tex assembles both panels and draws the formula of the task in the bottom row of boxes.

Geometry (inches): the row is 2.45 high. The axes are square (1.20 x 1.20), so that panel b, the reservoir, carries
the figure. The title sits 10.4 bp below the top of the row, as in panel b; the axes sit centred in the band between
the title and the bottom 0.36 in of the row, where fig2.tex places the box with the formula y_{t+1}, next to the
legend boxes of panel b."""
import sys; sys.path.insert(0, ".")
from figstyle import *
import numpy as np
setup()
S, HROW = 1.20, 2.45             # side of the square axes, height of the row
WA = 0.28 + S + 0.06               # width of panel a: 1.54 in = 3.912 cm
AB = 0.95                          # bottom of the axes: centred between the title and the box row

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
fig = figure(WA, HROW)
ax = add_axes(fig, 0.28, AB, S, S)
ax.plot(t[:tnow + 1], u[:tnow + 1], color=INK, lw=1.6, zorder=2, solid_capstyle="round")
ya = 1.27                                   # height of the dimension arrow
for tt in (tnow - lagT, tnow):              # dimension lines from the two inputs up to the arrow
    ax.plot([tt, tt], [u[tt] + 0.06, ya + 0.07], ls=(0, (2, 1.6)), lw=0.75, color=PURPLE, zorder=1)
    ax.plot(tt, u[tt], "o", ms=5, color=PURPLE, mec="white", mew=0.8, zorder=5)
label(ax, tnow - lagT - 4, u[tnow - lagT] + 0.04, r"$u_{t-100}$", color=PURPLE_DARK, ha="right", va="bottom")
label(ax, tnow - 4, u[tnow] + 0.04, r"$u_{t}$", color=PURPLE_DARK, ha="right", va="bottom")
ax.annotate("", xy=(tnow - lagT, ya), xytext=(tnow, ya),
            arrowprops=dict(arrowstyle="<|-|>", lw=0.8, color=INK, shrinkA=0, shrinkB=0, mutation_scale=6))
label(ax, (2 * tnow - lagT) / 2, ya + 0.05, "100 time steps", ha="center", va="bottom")
ax.set_xlim(-5, 153); ax.set_ylim(-0.12, 1.58)
ax.set_xticks([0, 50, 100, 145]); ax.set_xticklabels(["0", "50", "100", r"$t$"])
ax.set_yticks([0, 0.5, 1])
xlabel(ax, "Time step")
ax.set_ylabel(r"$u_t$", rotation=0, labelpad=0)
ax.yaxis.set_label_coords(-0.115, 0.935)
# title at the height of the title of panel b (10.4 bp below the top), independent of the axes position
fig.text(0.28 / WA, (HROW - 10.4 / 72) / HROW, r"\textbf{a}\enspace Temporal task", fontsize=FS, ha="left",
         va="baseline")
save(fig, "fig2a.pdf")
print("panel a done")
