"""Fig. 3, panel a (matplotlib): the memory limit versus the number k of input qubits (schematic).
The limit W_{q,k} (dashed) lies between the two bounds of Theorem 1, two exponentials in k, for every size n. Above the
upper bound no reservoir remembers (red); below the lower bound every memory depth is attainable (blue). The reservoirs
of panel b sit on the limit: A and B (n = 10 and 100, k = 2) at the same point W_{q,2}, C (k = 4) at W_{q,4}; the two
levels are the ones marked on the time axis of panel b. The axes carry no other numbers: the curves show the form of
the bounds, not their constants.

Geometry (inches): the panel is 2.756 wide (the left 7.00 cm of the 7.05 in figure) and 2.579 high (6.55 cm). The
x axis sits at the height of the time axis of panel b (1.27 cm), and the title and the axis label share their
baselines with panel b; fig3.tex places this PDF at the top left of the figure."""
import sys; sys.path.insert(0, ".")
from figstyle import *
import numpy as np
import matplotlib.patheffects as pe
setup()

W, H = 7.00 / 2.54, 6.55 / 2.54
X0, Y0 = 0.60, 1.27 / 2.54                 # axes origin (in): room for the y label and the two level labels
AW, AH = W - X0 - 0.27, H - 0.22 - Y0      # right margin for W_{q,k}, top margin for the title
fig = figure(W, H)
ax = add_axes(fig, X0, Y0, AW, AH)

kmax = 10.0
k = np.linspace(0, kmax, 400)
c1, c2 = 0.40, 0.95                         # schematic rates of the lower and upper bound (slopes on the log scale)
lo = lambda x: 0.8 * np.exp(c1 * x)
hi = lambda x: 5.0 * np.exp(c2 * x)
Wk = lambda x: 2.0 * np.exp(0.5 * (c1 + c2) * x + 0.20 * np.sin(0.55 * x))
bot, top = 0.30, hi(kmax) * 8
ax.set_yscale("log"); ax.set_xlim(0, kmax); ax.set_ylim(bot, top)

# regions: unreachable (red), attainable (blue), the band of the limit (hatched)
ax.fill_between(k, hi(k), top, color=RED_FILL, lw=0, zorder=0)
ax.fill_between(k, bot, lo(k), color=BLUE_FILL, lw=0, zorder=0)
ax.fill_between(k, lo(k), hi(k), facecolor="none", edgecolor="#C8C8C8", hatch="/////", lw=0, zorder=0)
ax.plot(k, hi(k), color=RED, lw=1.6, zorder=3, solid_capstyle="butt")
ax.plot(k, lo(k), color=BLUE, lw=1.6, zorder=3, solid_capstyle="butt")
ax.plot(k, Wk(k), color=INK, lw=0.9, ls=(0, (3, 2)), zorder=3)


def along(f, x, s, color, side=+1, gap=4.6):
    """Label s set along the curve y = f(x), centred at x, on one side of the curve (side = +1 above, -1 below);
    gap is the distance (pt) from the curve to the centre line of the text."""
    p1, p0, p2 = ax.transData.transform([(x - 0.4, f(x - 0.4)), (x, f(x)), (x + 0.4, f(x + 0.4))])
    a = np.arctan2(p2[1] - p1[1], p2[0] - p1[0])
    d = side * gap * fig.dpi / 72
    q = p0 + d * np.array([-np.sin(a), np.cos(a)])
    xq, yq = ax.transData.inverted().transform(q)
    return label(ax, xq, yq, s, color=color, rotation=np.degrees(a), rotation_mode="anchor", ha="center",
                 va="center_baseline", zorder=5)


along(hi, 6.4, "upper bound", RED_DARK, side=+1)
along(lo, 3.1, "lower bound", BLUE_DARK, side=-1)

# region names, in the corners of the two regions
label(ax, 0.25, top / 1.7, "no reservoir remembers\nthis long", color=RED_DARK, bold=True, ha="left", va="top",
      zorder=5, linespacing=1.15)
label(ax, kmax - 0.2, bot * 1.25, "attainable with\n" + r"$\bm k$ input qubits", color=BLUE_DARK, bold=True,
      ha="right", va="bottom", zorder=5, linespacing=1.15)


def box(s, xy, xytext, color, conn):
    """Formula in a white box with a drop shadow and an arrow to the curve (style of the legend boxes)."""
    t = ax.annotate(s, xy=xy, xytext=xytext, color=color, fontsize=FS, ha="center", va="center", zorder=7,
                    bbox=dict(boxstyle="round,pad=0.32,rounding_size=0.18", fc="white", ec=INK, lw=0.8),
                    arrowprops=dict(arrowstyle="-|>", color=INK, lw=0.75, shrinkA=0, shrinkB=1.2, mutation_scale=6.5,
                                    connectionstyle=conn))
    t.get_bbox_patch().set_path_effects([pe.SimplePatchShadow(offset=(1.2, -1.2), shadow_rgbFace="#B5B5B5",
                                                              alpha=1.0), pe.Normal()])
    return t


box(r"$e^{k\ln 2/(1-q)^2}$", (4.6, hi(4.6)), (2.75, 10 ** 3.55), RED_DARK, "angle,angleA=0,angleB=90,rad=0")
box(r"$e^{\alpha_q k}$", (8.4, lo(8.4)), (8.4, 10 ** 2.12), BLUE_DARK, "arc3,rad=0")

# the reservoirs of panel b on the limit: A and B (k = 2) at the same point, C (k = 4) higher; dotted guides to the
# levels W_{q,2} and W_{q,4}, which panel b marks on its time axis
for kk in (2, 4):
    ax.plot([0, kk], [Wk(kk), Wk(kk)], ls=(0, (1, 1.6)), lw=0.8, color=GREY, zorder=4)
ax.plot(2, Wk(2), "o", ms=8.2, mfc="white", mec=INK, mew=0.9, zorder=8)
ax.plot(2, Wk(2), "o", ms=3.4, mfc=INK, mec=INK, mew=0.6, zorder=9)
ax.plot(4, Wk(4), "o", ms=4.6, mfc=PURPLE, mec="white", mew=0.7, zorder=9)
label(ax, 2.45, Wk(2) / 1.9, r"\textbf{A}, \textbf{B}", ha="left", va="center", zorder=9)
label(ax, 4.35, Wk(4) / 1.9, r"\textbf{C}", color=PURPLE_DARK, ha="left", va="center", zorder=9)
label(ax, 9.75, Wk(9.75) * 1.9, r"$W_{q,k}$", ha="right", va="bottom", zorder=9)

ax.minorticks_off(); ax.grid(False)
ax.set_yticks([Wk(2), Wk(4)]); ax.set_yticklabels([r"$W_{q,2}$", r"$W_{q,4}$"])
ax.set_xticks([0, 2, 4, 6, 8, 10])
ax.set_ylabel(r"\textbf{Memory depth}", labelpad=3)
# x label and title share their baselines with panel b (0.25 cm above the bottom, 10.4 bp below the top)
fig.text((X0 + AW / 2) / W, (0.25 / 2.54) / H, r"\textbf{Input qubits per time step}\quad $k$", fontsize=FS,
         ha="center", va="baseline")
fig.text(0.0, (H - 10.4 / 72) / H, r"\textbf{a}\enspace Exponential in input qubits", fontsize=FS, ha="left",
         va="baseline")
fig.text((X0 + AW) / W, (H - 10.4 / 72) / H, r"any $n$", fontsize=FS, ha="right", va="baseline")
save(fig, "fig3a.pdf")
print("panel a done")
