"""Figure 1: repeated-n-gram coverage of the 2019 final by design and definition, with bootstrap
95% CIs and the shuffled-word baseline. Reads analysis/formulas/results/coverage_family.csv only."""
import numpy as np
import pandas as pd
from matplotlib.lines import Line2D
from matplotlib.patches import Patch

import sys as _sys
from pathlib import Path as _Path

_sys.path.insert(0, str(_Path(__file__).resolve().parent))  # python -I does not add the script dir
from common import INK, MUTED, RAMP5, RES_F, pct, plt, save

df = pd.read_csv(RES_F / "coverage_family.csv")

DESIGNS = [
    ("D1_in_sample", "tv_2019wimF", "tv_2019wimF", "in-sample\n2019 → 2019"),
    ("D2_split_half", "2019 halves", "2019 other half (pooled)", "split-half\n2019 halves"),
    ("D3_held_out", "pool (18 matches)", "tv_2019wimF", "cross-match held-out\npool (18) → 2019"),
    ("D3_held_out", "tv_2019wimF", "tv_2023wimF", "held-out final\n2019 → 2023"),
]
DEFS = [
    ("base", "n ≥ 2, not stop-only (pre-registered)"),
    ("content", "n ≥ 2, not function-word/numeral-only"),
    ("n3", "n ≥ 3"),
    ("content_n3", "n ≥ 3, not function-word/numeral-only"),
    ("n4", "n ≥ 4"),
]

fig, ax = plt.subplots(figsize=(7.8, 3.4))
nd, nf = len(DESIGNS), len(DEFS)
width = 0.15
x0 = np.arange(nd)
for j, (key, label) in enumerate(DEFS):
    xs = x0 + (j - (nf - 1) / 2) * width
    vals, lo, hi, shuf = [], [], [], []
    for d, i_on, m_on, _ in DESIGNS:
        r = df[(df.design == d) & (df.identified_on == i_on) & (df.measured_on == m_on) & (df.definition == key)]
        assert len(r) == 1, (d, i_on, m_on, key, len(r))
        r = r.iloc[0]
        vals.append(pct(r.coverage))
        lo.append(pct(r.coverage) - pct(r.ci_lo))
        hi.append(pct(r.ci_hi) - pct(r.coverage))
        shuf.append(pct(r.shuffled_mean) if pd.notna(r.shuffled_mean) else np.nan)
    ax.bar(xs, vals, width=width * 0.92, color=RAMP5[j], label=label, linewidth=0)
    ax.errorbar(xs, vals, yerr=[lo, hi], fmt="none", ecolor=INK, elinewidth=0.8, capsize=0)
    # shuffled-word baseline: short dash on each bar
    for xx, s in zip(xs, shuf):
        if np.isfinite(s):
            ax.plot([xx - width * 0.46, xx + width * 0.46], [s, s], color=INK, lw=1.4, solid_capstyle="butt")

ax.set_xticks(x0)
ax.set_xticklabels([d[3] for d in DESIGNS])
ax.set_ylabel("tokens covered (%)")
ax.set_ylim(0, 62)
ax.set_xlim(-0.55, nd - 0.45)
handles = [Patch(color=RAMP5[j], label=lab) for j, (_, lab) in enumerate(DEFS)]
handles.append(Line2D([0], [0], color=INK, lw=1.4, label="shuffled-word baseline (mean)"))
ax.legend(handles=handles, loc="upper left", bbox_to_anchor=(1.01, 1.0), ncol=1, handlelength=1.6)
ax.set_title("Repeated-n-gram coverage of the 2019 final (bootstrap 95% CI)", loc="left", color=INK)
ax.grid(axis="x", visible=False)
save(fig, "fig1_coverage")
