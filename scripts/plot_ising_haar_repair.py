#!/usr/bin/env python3
"""Plot only the new global and modular Ising/Haar repair experiments."""

import argparse
import csv
import os
from pathlib import Path

import numpy as np


def read(path):
    with path.open() as stream:
        return list(csv.DictReader(stream))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input-dir", type=Path,
                        default=Path("results/ising-haar-repair-2026-10-16"))
    parser.add_argument("--output-dir", type=Path)
    args = parser.parse_args()
    output = args.output_dir or args.input_dir
    output.mkdir(parents=True, exist_ok=True)
    os.environ.setdefault("MPLCONFIGDIR", str(Path("work/repair-plot-cache").resolve()))
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    plt.rcParams.update({"font.size": 11, "pdf.fonttype": 42,
                         "axes.spines.top": False, "axes.spines.right": False})
    global_rows = read(args.input_dir / "global/depths.csv")
    modular_rows = read(args.input_dir / "modular/depths.csv")
    selections = [
        ("global_native", global_rows, "native", "core_trace_depth", [3, 5, 7],
         "Direct repair of global reservoirs", "Core trace-distance witness depth", 12),
        ("global_decoded", global_rows, "decoded", "core_trace_depth", [3, 5, 7],
         "Global reservoirs with decoder and repair", "Core trace-distance witness depth", 12),
        ("global_fixed_readout", global_rows, "native", "fixed_readout_depth", [3, 5, 7],
         "Direct repair: fixed linear readout", "Fixed-readout witness depth", 12),
        ("modular_repair", modular_rows, None, "depth", [4, 8, 12],
         "Redundant two-qubit modules with decoder and repair", "Fixed two-qubit readout depth", 22),
    ]
    for name, rows, variant, metric, ks, title, ylabel, n in selections:
        fig, axes = plt.subplots(1, 2, figsize=(10, 4.7), sharey=True)
        for ax, model in zip(axes, ("ising", "haar")):
            for repair, color, marker, label in (
                    (True, "#2265b1", "o", "With majority repair"),
                    (False, "#777777", "s", "Without repair")):
                series = []
                for replicate in range(8):
                    values = []
                    for k in ks:
                        selected = [row for row in rows if row["model"] == model
                                    and row["repair"] == str(repair)
                                    and int(row["replicate"]) == replicate and int(row["k"]) == k
                                    and (variant is None or row["variant"] == variant)]
                        if len(selected) != 1:
                            raise ValueError(f"Expected one saved run: {model}, {replicate}, {k}")
                        values.append(float(selected[0][metric]))
                    series.append(values)
                data = np.asarray(series)
                median = np.median(data, axis=0)
                ax.fill_between(ks, data.min(axis=0), data.max(axis=0), color=color, alpha=.12)
                ax.semilogy(ks, median, color=color, marker=marker, lw=2,
                            ls="-" if repair else "--", label=label)
                if repair:
                    for k, value in zip(ks, median):
                        ax.annotate(f"{value:g}", (k, value), xytext=(0, 10),
                                    textcoords="offset points", ha="center", color=color)
            ax.set(title="Ising" if model == "ising" else "Haar", xticks=ks,
                   xlabel="Fresh qubits per cycle k")
            ax.grid(alpha=.18)
            ax.margins(x=.15, y=.25)
        axes[0].set_ylabel(ylabel)
        handles, labels = axes[0].get_legend_handles_labels()
        fig.legend(handles, labels, loc="lower center", ncol=2, frameon=False,
                   bbox_to_anchor=(.5, .035))
        fig.suptitle(title, fontsize=14, y=.99)
        fig.text(.5, .91, f"Fixed total n = {n}; q = 0.9; threshold = 0.01", ha="center")
        fig.text(.5, .015, "Medians of 8 fixed realizations; shading shows min–max, not confidence intervals.",
                 ha="center", fontsize=9, color="#555555")
        fig.tight_layout(rect=(0, .12, 1, .88))
        for extension in ("png", "pdf"):
            fig.savefig(output / f"{name}.{extension}", dpi=180, bbox_inches="tight")
        plt.close(fig)


if __name__ == "__main__":
    main()
