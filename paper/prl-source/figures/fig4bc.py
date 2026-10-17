"""Fig. 4, panels b, c: memory depth of the error-correcting reservoir (b) and of standard reservoirs (c)
(q = 0.9, eps = 0.01). Panel a (circuit) is drawn in fig4.tex.
Panel b also shows the same reservoir without repair: its r = k - 2 memory copies are written once and then only
decay, and even the best readout of all r copies (exact trace distance) keeps the bit for only 43 to 53 time steps.
Colours: error-correcting reservoir and the lower bound of Theorem 1 in blue (attain the limit), standard reservoirs
in greys (Ising dark, Haar light), the idle qubit as a dashed reference line."""
import sys, json; sys.path.insert(0, ".")
from figstyle import *
import numpy as np
from math import log, comb
from fractions import Fraction
setup()
R = json.load(open("../sim/results_main.json"))
q, eps = 0.9, 1e-2
alpha = -0.5 * log(1 - q * q)
W_idle = 43  # = 1 + max{l : q^(l+1) > eps}: a single qubit that holds the input without repair


def get(model, n, k):
    for e in R:
        if e["model"] == model and e["n"] == n and e["k"] == k:
            return e


def td_copies(r, s):
    """Trace distance between r copies of (I + sZ)/2 and r copies of (I - sZ)/2: the best readout of r unrepaired
    copies whose bias has decayed to s."""
    a, b = (1 + s) / 2, (1 - s) / 2
    return 0.5 * sum(comb(r, j) * abs(a ** j * b ** (r - j) - b ** j * a ** (r - j)) for j in range(r + 1))


def W_norepair(r):
    """Memory depth of r unrepaired copies, with the convention of the error-correcting reservoir (exact, continuous
    in t): td_copies(r, q^(t+1)) = eps. For r = 1 this is ln(q/eps)/(-ln q), the value of both reservoirs at k = 3."""
    lo, hi = 0.0, 500.0
    for _ in range(200):
        mid = (lo + hi) / 2
        lo, hi = (mid, hi) if td_copies(r, q ** (mid + 1)) > eps else (lo, mid)
    return lo


def p_r(r):
    p = Fraction(1, 20)
    return sum(Fraction(comb(r, j)) * p ** j * (1 - p) ** (r - j) for j in range(r // 2 + 1, r + 1))


STY = {"ising": dict(color=ISING, mk="D", ms=4.3, name="Ising"),
       "haar": dict(color=HAAR, mk="^", ms=4.8, name="Haar")}
IDLE = dict(color=INK, lw=1.0, ls=(0, (4, 2.5)))

fig = figure(4.40, 2.05)
b, c = even_row(fig, 2, left=0.45, right=0.06, gap=0.60)

# ---------------------------------------------------------------- b: memory depth versus input qubits
kr = np.arange(3, 16, 2)
Wrep = [log(q / eps) / -log(1 - 2 * float(p_r(k - 2))) for k in kr]      # exact, single-qubit readout
k0 = 3 + log(4) / alpha                                                   # Theorem 1(ii) applies for k >= k0
kk = np.linspace(k0, 15.6, 100)
b.plot(kk, np.exp(alpha * (kk - 3)) / 4 * log(q / eps), color=BLUE, lw=1.1, ls=(0, (4, 2.2)), zorder=2,
       label=r"lower bound (Thm.~1)")
Wnr = [W_norepair(k - 2) for k in kr]                                    # the same copies, without repair
b.plot(kr, Wnr, color=GREY, lw=1.0, zorder=2)
b.plot(kr, Wnr, "o", ms=4.0, mfc="white", mec=GREY_DARK, mew=0.8, zorder=3)
b.plot(kr, Wrep, color=BLUE_LIGHT, lw=1.0, zorder=2)
b.plot(kr, Wrep, "o", ms=4.6, color=BLUE, mec=BLUE_DARK, mew=0.7, zorder=4, label="error-correcting reservoir")
b.set_yscale("log"); b.set_xlim(2, 16); b.set_ylim(2, 2e7)
b.set_xticks([3, 5, 7, 9, 11, 13, 15]); b.set_yticks([1e1, 1e3, 1e5])
# direct labels instead of a legend: each label sits next to its own line; the label of the lower bound runs
# parallel to it, above the line
label(b, 2.45, 10 ** 6.25, "error-correcting reservoir", color=BLUE_DARK, ha="left", va="center")
label(b, 15.6, 10 ** 1.13, "without repair", color=GREY_DARK, ha="right", va="center")
kc = 11.4
lb = lambda x: np.exp(alpha * (x - 3)) / 4 * log(q / eps)
p0, p1 = b.transData.transform([(kc - 1, lb(kc - 1)), (kc + 1, lb(kc + 1))])
ang = np.degrees(np.arctan2(p1[1] - p0[1], p1[0] - p0[0]))
label(b, kc, lb(kc) * 10 ** 0.50, r"lower bound (Thm.~1)", color=BLUE, ha="center", va="center", rotation=ang,
      rotation_mode="anchor")
xlabel(b, "Input qubits", "k")
ylabel(b, "Memory depth", r"W(\varepsilon)")
panel(b, "b", "Gain from input qubits", r"$q=0.9$")

# ---------------------------------------------------------------- c: memory depth versus reservoir size
c.axhline(W_idle, zorder=1, **IDLE)
label(c, 2.7, W_idle - 1.6, "idle qubit", ha="left", va="top")
for model, k, filled in (("ising", 1, True), ("ising", 2, False), ("haar", 1, True), ("haar", 2, False)):
    st = STY[model]
    ns = [n for n in sorted(e["n"] for e in R if e["model"] == model and e["k"] == k) if n >= k + 2]
    mu = np.array([np.mean(get(model, n, k)["W"]) for n in ns])
    sd = np.array([np.std(get(model, n, k)["W"]) for n in ns])
    x = np.array(ns) + (-0.1 if k == 1 else 0.1)
    c.fill_between(x, mu - sd, mu + sd, color=st["color"], alpha=0.2, lw=0)
    c.errorbar(x, mu, yerr=sd, fmt=st["mk"], ms=st["ms"], color=st["color"],
               mfc=st["color"] if filled else "white", mec=darker(st["color"], 0.6), mew=0.8,
               ecolor=darker(st["color"], 0.7), elinewidth=0.8, label=r"%s, $k{=}%d$" % (st["name"], k), zorder=3)
c.set_xlim(2.5, 9.5); c.set_ylim(0, 50)
c.set_xticks(range(3, 10))
# legend centred in the free band between the data (W <= 20) and the idle-qubit label (W >= 38)
legc = legend(c, loc="center", bbox_to_anchor=(0.5, 0.585), ncol=2, handlelength=0.9, handletextpad=0.3,
              columnspacing=0.7, borderpad=0.35, markerscale=0.9)
xlabel(c, "Reservoir size", "n")
ylabel(c, "Memory depth", r"W(\varepsilon)")
panel(c, "c", "No gain from size", r"$\varepsilon=0.01$")
fig.draw_without_rendering()
_L = legc.get_window_extent(); _A = c.get_window_extent()
_pt = 72.0 / fig.dpi
print("legend c margins (pt): left %.1f right %.1f top-of-axes %.1f, bottom at W = %.1f, top at W = %.1f" % (
    (_L.x0 - _A.x0) * _pt, (_A.x1 - _L.x1) * _pt, (_A.y1 - _L.y1) * _pt,
    c.transData.inverted().transform((0, _L.y0))[1], c.transData.inverted().transform((0, _L.y1))[1]))
save(fig, "fig4bc.pdf")
print("Wrep:", dict(zip(kr.tolist(), [round(w, 1) for w in Wrep])), "k0 = %.2f" % k0)
print("without repair:", dict(zip(kr.tolist(), [round(w, 1) for w in Wnr])))
W_int = lambda r: 1 + max(l for l in range(400) if td_copies(r, q ** (l + 1)) > eps)   # integer convention, as W_idle
print("without repair, integer memory depth (quoted in the text):", {k: W_int(k - 2) for k in kr.tolist()})
