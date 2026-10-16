"""Shared figure style for all figures of the paper.

Design rules (reverse-engineered from Freiheit & Campaioli, arXiv:2608.25511, and unified):
  * one text size, 8 pt, for every label, tick, legend entry, annotation and panel title;
    Helvetica for text, Computer Modern for math, bold words in axis labels and panel letters;
  * every figure is produced at its printed size and included without scaling;
  * three hues with a fixed meaning, plus greys:
      blue   = memory: the reservoir that reaches the limit, lower bounds, attainable regions
      red    = noise and the limit: noise, upper bounds, unreachable regions
      purple = input: input injection, reinitialized input qubits
      greys  = standard reservoirs, references and neutral elements.
"""
import matplotlib as mpl
mpl.use("pdf")
import matplotlib.pyplot as plt
from matplotlib.colors import to_rgb, to_hex
import numpy as np

PREAMBLE = (r"\usepackage[T1]{fontenc}\usepackage{helvet}\renewcommand{\familydefault}{\sfdefault}"
            r"\usepackage{amsmath,amssymb,bm}\renewcommand{\mathdefault}[1]{\mathsf{#1}}")
FS = 8.0                      # the single text size of all figures (pt)
TEXTWIDTH = 7.05              # in; REVTeX \textwidth = 510 pt = 7.057 in
COLUMNWIDTH = 3.40            # in; REVTeX \columnwidth = 246 pt = 3.404 in
PT = 1 / 72.0                 # matplotlib point in inches

# ----------------------------------------------------------------------------------------------- palette
INK = "#1A1A1A"
BLUE, BLUE_DARK, BLUE_LIGHT, BLUE_FILL = "#3C7FE0", "#1D4C9C", "#8DB8F0", "#DDE9F9"
RED, RED_DARK, RED_FILL = "#EF4B3B", "#B8301F", "#FCE3DE"
PURPLE, PURPLE_DARK, PURPLE_FILL = "#9B4FE0", "#6B2CAB", "#EFE2FB"
GREY_DARK, GREY, GREY_LIGHT, GREY_FILL = "#4A4A4A", "#8C8C8C", "#B4B4B4", "#EDEDED"
ISING, HAAR = GREY_DARK, "#A3A3A3"           # standard reservoirs
GRID = "#E4E4E4"


def mix(c1, c2, t):
    a, b = np.array(to_rgb(c1)), np.array(to_rgb(c2))
    return to_hex((1 - t) * a + t * b)


def blues(m):
    """m shades of the blue ramp, light to dark (for parameter families of the construction)."""
    stops = ["#8DB8F0", BLUE, "#14347A"]
    out = []
    for i in range(m):
        t = i / max(m - 1, 1)
        out.append(mix(stops[0], stops[1], 2 * t) if t <= 0.5 else mix(stops[1], stops[2], 2 * t - 1))
    return out


def darker(c, f=0.7):
    r, g, b = to_rgb(c)
    return (r * f, g * f, b * f)


# ----------------------------------------------------------------------------------------------- rcParams
def setup():
    plt.rcParams.update({
        "text.usetex": True, "text.latex.preamble": PREAMBLE, "font.family": "sans-serif",
        "font.size": FS, "axes.labelsize": FS, "axes.titlesize": FS,
        "xtick.labelsize": FS, "ytick.labelsize": FS, "legend.fontsize": FS, "legend.title_fontsize": FS,
        "axes.linewidth": 0.8, "axes.edgecolor": INK, "axes.labelcolor": INK,
        "xtick.color": INK, "ytick.color": INK,
        "xtick.major.width": 0.8, "ytick.major.width": 0.8, "xtick.minor.width": 0.6, "ytick.minor.width": 0.6,
        "xtick.major.size": 3.0, "ytick.major.size": 3.0, "xtick.minor.size": 1.7, "ytick.minor.size": 1.7,
        "xtick.direction": "out", "ytick.direction": "out", "xtick.major.pad": 2.2, "ytick.major.pad": 2.2,
        "axes.grid": True, "grid.color": GRID, "grid.linewidth": 0.55, "axes.axisbelow": True,
        "axes.labelpad": 2.5, "axes.titlepad": 4.0,
        "legend.frameon": True, "legend.fancybox": True, "legend.edgecolor": INK, "legend.framealpha": 1.0,
        "legend.borderpad": 0.4, "legend.handletextpad": 0.5, "legend.borderaxespad": 0.5,
        "legend.handlelength": 1.5, "legend.labelspacing": 0.28, "legend.columnspacing": 1.0,
        "lines.linewidth": 1.3, "lines.markersize": 4.5, "lines.markeredgewidth": 0.7,
        "errorbar.capsize": 1.6,
        "pdf.fonttype": 42, "savefig.dpi": 300,
    })


# ----------------------------------------------------------------------------------------------- layout
def figure(width, height):
    """A figure of exactly the printed size (inches)."""
    return plt.figure(figsize=(width, height))


def add_axes(fig, left, bottom, width, height):
    """Axes placed in absolute inches, so that margins are identical across figures."""
    W, H = fig.get_size_inches()
    return fig.add_axes([left / W, bottom / H, width / W, height / H])


def row(fig, lefts, widths, bottom=0.40, top=0.20):
    """A row of axes with common bottom and top margins (inches)."""
    W, H = fig.get_size_inches()
    h = H - bottom - top
    return [add_axes(fig, l, bottom, w, h) for l, w in zip(lefts, widths)]


def even_row(fig, n, left=0.47, right=0.06, gap=0.62, bottom=0.40, top=0.20):
    """n axes of equal width; `left` and `gap` leave room for y tick labels and y labels."""
    W, _ = fig.get_size_inches()
    w = (W - left - right - (n - 1) * gap) / n
    return row(fig, [left + i * (w + gap) for i in range(n)], [w] * n, bottom, top)


# ----------------------------------------------------------------------------------------------- text helpers
def panel(ax, letter, title="", right=""):
    """Panel header: bold letter, regular title, optional right-aligned note (all 8 pt)."""
    ax.set_title(r"\textbf{%s}\enspace %s" % (letter, title), loc="left", fontsize=FS, pad=4)
    if right:
        ax.set_title(right, loc="right", fontsize=FS, pad=4)


def xlabel(ax, words, sym=""):
    ax.set_xlabel(r"\textbf{%s}" % words + (r"\quad $%s$" % sym if sym else ""))


def ylabel(ax, words, sym=""):
    ax.set_ylabel(r"\textbf{%s}" % words + (r"\quad $%s$" % sym if sym else ""))


def legend(ax, **kw):
    kw.setdefault("shadow", {"ox": 1.2, "oy": -1.2, "color": "#B5B5B5", "alpha": 1.0})
    kw.setdefault("fontsize", FS)
    leg = ax.legend(**kw)
    leg.get_frame().set_linewidth(0.8)
    return leg


def label(ax, x, y, s, color=INK, bold=False, **kw):
    kw.setdefault("fontsize", FS)
    if bold:  # matplotlib typesets each line separately, so bold each line on its own
        s = "\n".join(r"\textbf{%s}" % line for line in s.split("\n"))
    return ax.text(x, y, s, color=color, **kw)


def save(fig, name):
    fig.savefig(name)  # no tight bbox: the printed size is the figure size
    plt.close(fig)
