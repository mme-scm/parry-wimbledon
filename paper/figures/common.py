"""Shared paths, palette and matplotlib style for the paper figures.

Every figure script reads only from analysis/formulas/results/ and analysis/metre/results/
and writes PNG + SVG into paper/figures/. Palette: the dataviz reference palette (categorical
slots 1-3 validated for light mode; blue ordinal ramp validated as an ordinal scale).
"""
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
RES_F = ROOT / "analysis" / "formulas" / "results"
RES_M = ROOT / "analysis" / "metre" / "results"
OUT = Path(__file__).resolve().parent
TABLES = OUT / "tables"

# categorical slots (fixed order, never cycled)
BLUE = "#2a78d6"
ORANGE = "#eb6834"
AQUA = "#1baf7a"
# blue ordinal ramp, light -> dark (steps 250, 350, 450, 550, 650)
RAMP5 = ["#86b6ef", "#5598e7", "#2a78d6", "#1c5cab", "#104281"]
# chrome and ink
INK = "#0b0b0b"
INK2 = "#52514e"
MUTED = "#898781"
GRID = "#e1e0d9"
AXIS = "#c3c2b7"
SURFACE = "#ffffff"

plt.rcParams.update(
    {
        "font.family": "sans-serif",
        "font.size": 8.5,
        "axes.titlesize": 9.5,
        "axes.labelsize": 8.5,
        "axes.edgecolor": AXIS,
        "axes.labelcolor": INK2,
        "axes.spines.top": False,
        "axes.spines.right": False,
        "axes.grid": True,
        "axes.axisbelow": True,
        "grid.color": GRID,
        "grid.linewidth": 0.6,
        "xtick.color": INK2,
        "ytick.color": INK2,
        "xtick.labelsize": 8,
        "ytick.labelsize": 8,
        "legend.fontsize": 7.5,
        "legend.frameon": False,
        "figure.facecolor": SURFACE,
        "axes.facecolor": SURFACE,
        "savefig.facecolor": SURFACE,
        "text.color": INK,
    }
)


def save(fig, stem):
    """Write <stem>.png (200 dpi) and <stem>.svg into paper/figures/."""
    fig.savefig(OUT / f"{stem}.png", dpi=200, bbox_inches="tight")
    fig.savefig(OUT / f"{stem}.svg", bbox_inches="tight")
    print(f"wrote {stem}.png / .svg")


def pct(x):
    """Fraction -> percent; works on scalars and numpy arrays."""
    import numpy as np

    return 100.0 * np.asarray(x, dtype=float) if np.ndim(x) else 100.0 * float(x)
