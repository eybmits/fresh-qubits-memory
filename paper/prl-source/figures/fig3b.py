"""Fig. 3, panel b (matplotlib): the memory limit versus the number k of input qubits (schematic).
The limit lies between the two bounds of Theorem 1, two exponentials in k, for every size n. Above the upper bound no
reservoir remembers (red); below the lower bound every memory depth is attainable (blue); the limit W_{q,k} (dashed)
lies in the hatched band. The reservoirs of panel a sit on the limit: A and B (n = 20 and 200, k = 2) at the same
point, C (k = 4) higher. The axes carry no numbers: the curves show the form of the bounds, not their constants.

Geometry (inches): the panel is 2.680 wide (from 11.10 cm to the right edge of the 7.05 in figure) and 2.60 high.
The x axis sits at the height of the time axis of panel a (1.27 cm), and the title and the axis label share their
baselines with panel a; fig3.tex places this PDF at the top right of the figure."""
import sys; sys.path.insert(0, ".")
from figstyle import *
import numpy as np
import matplotlib.patheffects as pe
setup()

W, H = 2.680, 6.604 / 2.54
X0, Y0 = 0.30, 1.27 / 2.54                 # axes origin (in): left margin for the y label, x axis as in panel a
AW, AH = 2.02, H - 0.22 - Y0               # axes size: right margin for W_{q,k}, top margin for the title
fig = figure(W, H)
ax = add_axes(fig, X0, Y0, AW, AH)

kmax = 12.0
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


along(hi, 7.3, "upper bound", RED_DARK, side=+1)
along(lo, 5.6, "lower bound", BLUE_DARK, side=-1)

# region names, in the corners of the two regions
label(ax, 0.30, top / 1.8, "no reservoir remembers this long", color=RED_DARK, bold=True, ha="left", va="top",
      zorder=5)
label(ax, kmax - 0.25, bot * 1.5, r"attainable with $\bm k$ input qubits", color=BLUE_DARK, bold=True,
      ha="right", va="bottom", zorder=5)


def box(s, xy, xytext, color, conn):
    """Formula in a white box with a drop shadow and an arrow to the curve (style of the legend boxes)."""
    t = ax.annotate(s, xy=xy, xytext=xytext, color=color, fontsize=FS, ha="center", va="center", zorder=7,
                    bbox=dict(boxstyle="round,pad=0.32,rounding_size=0.18", fc="white", ec=INK, lw=0.8),
                    arrowprops=dict(arrowstyle="-|>", color=INK, lw=0.75, shrinkA=0, shrinkB=1.2, mutation_scale=6.5,
                                    connectionstyle=conn))
    t.get_bbox_patch().set_path_effects([pe.SimplePatchShadow(offset=(1.2, -1.2), shadow_rgbFace="#B5B5B5",
                                                              alpha=1.0), pe.Normal()])
    return t


box(r"$2^{k/(1-q)^2}$", (4.2, hi(4.2)), (2.0, 10 ** 4.15), RED_DARK, "angle,angleA=0,angleB=90,rad=0")
box(r"$e^{\alpha_q k}$", (9.9, lo(9.9)), (9.9, 10 ** 0.52), BLUE_DARK, "arc3,rad=0")

# the reservoirs of panel a on the limit: A and B (k = 2) at the same point, C (k = 4) higher
ax.plot(2, Wk(2), "o", ms=8.2, mfc="white", mec=INK, mew=0.9, zorder=8)
ax.plot(2, Wk(2), "o", ms=3.4, mfc=INK, mec=INK, mew=0.6, zorder=9)
ax.plot(4, Wk(4), "o", ms=4.6, mfc=PURPLE, mec="white", mew=0.7, zorder=9)
label(ax, 2.45, Wk(2) / 1.9, r"\textbf{A}, \textbf{B}", ha="left", va="center", zorder=9)
label(ax, 4.35, Wk(4) / 1.9, r"\textbf{C}", color=PURPLE_DARK, ha="left", va="center", zorder=9)
tr = mpl.transforms.blended_transform_factory(ax.transAxes, ax.transData)
label(ax, 1.03, Wk(kmax), r"$W_{q,k}$", transform=tr, ha="left", va="center", clip_on=False)

ax.set_yticks([]); ax.minorticks_off(); ax.grid(False)
ax.set_xticks([0, 2, 4, 6, 8, 10, 12])
ax.set_ylabel(r"\textbf{Memory depth}", labelpad=4)
# x label and title share their baselines with panel a (0.25 cm above the bottom, 10.4 bp below the top)
fig.text((X0 + AW / 2) / W, (0.25 / 2.54) / H, r"\textbf{Input qubits per time step}\quad $k$", fontsize=FS,
         ha="center", va="baseline")
fig.text(X0 / W, (H - 10.4 / 72) / H, r"\textbf{b}\enspace Exponential in input qubits", fontsize=FS, ha="left",
         va="baseline")
fig.text((X0 + AW) / W, (H - 10.4 / 72) / H, r"any $n$", fontsize=FS, ha="right", va="baseline")
save(fig, "fig3b.pdf")
print("panel b done")
