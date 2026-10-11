"""Figure 5: coverage of the poem's tokens by Homeric word n-grams under the six definitions of
review/poem_density.py, with bootstrap 95% CIs over verses, for all 64 verses and for the 45 verses
that are not verbatim Homeric lines, beside the Homeric-verse reference (each Homeric verse against the
rest of Homer, token-weighted) and the shuffled-word baseline (mean and 2.5-97.5%). Reads
paper/figures/results/poem_stats.json and review/poem_density_v4.json only."""
import json
import sys as _sys
from pathlib import Path as _Path

import numpy as np
from matplotlib.lines import Line2D
from matplotlib.patches import Patch

_sys.path.insert(0, str(_Path(__file__).resolve().parent))  # python -I does not add the script dir
from common import AQUA, BLUE, INK, INK2, ORANGE, RES_P, REVIEW, plt, save  # noqa: E402

stats = json.loads((RES_P / "poem_stats.json").read_text(encoding="utf-8"))
dens = json.loads((REVIEW / "poem_density_v4.json").read_text(encoding="utf-8"))
D = stats["density"]
defs = list(D["definitions"].items())
# the statistics file must restate the density file exactly
for key, d in defs:
    c = dens["coverage"][key]
    assert d["coverage_pct"] == c["coverage"] and d["ci95"] == c["ci95"], key
    assert d["excluding_verbatim_pct"] == c["excluding_verbatim_verses"]["coverage"], key
    assert d["homeric_reference_pct"] == dens["homeric_reference_verse_vs_rest_of_homer"][key], key
    assert d["shuffled_mean_pct"] == c["shuffled_mean"], key

n_all, n_verb = D["verses"], D["verbatim_verses"]
SERIES = [
    ("coverage_pct", "ci95", f"all {n_all} verses", BLUE),
    ("excluding_verbatim_pct", "excluding_verbatim_ci95",
     f"excluding the {n_verb} verbatim Homeric verses ({n_all - n_verb} verses)", AQUA),
]

fig, ax = plt.subplots(figsize=(7.8, 3.6))
nd, ns = len(defs), len(SERIES)
width = 0.33
x0 = np.arange(nd)
for j, (vkey, ckey, label, color) in enumerate(SERIES):
    xs = x0 + (j - (ns - 1) / 2) * width
    vals = np.array([d[vkey] for _, d in defs], dtype=float)
    lo = vals - np.array([d[ckey][0] for _, d in defs], dtype=float)
    hi = np.array([d[ckey][1] for _, d in defs], dtype=float) - vals
    ax.bar(xs, vals, width=width * 0.92, color=color, label=label, linewidth=0)
    ax.errorbar(xs, vals, yerr=[lo, hi], fmt="none", ecolor=INK, elinewidth=0.8, capsize=0)

half = width * ns / 2 + 0.06
for i, (_, d) in enumerate(defs):
    # Homeric-verse reference: each Homeric verse measured against the rest of Homer
    ref = d["homeric_reference_pct"]
    ax.plot([i - half, i + half], [ref, ref], color=ORANGE, lw=1.8, solid_capstyle="butt", zorder=4)
    # shuffled-word baseline: mean as a dash, 2.5-97.5% as a whisker
    sm, (slo, shi) = d["shuffled_mean_pct"], d["shuffled_2.5_97.5"]
    ax.plot([i - half, i + half], [sm, sm], color=INK, lw=1.4, solid_capstyle="butt", zorder=4)
    ax.plot([i, i], [slo, shi], color=INK, lw=0.8, zorder=4)

ax.set_xticks(x0)
ax.set_xticklabels([d["short_label"] for _, d in defs], fontsize=7.5)
ax.set_ylabel("tokens covered (%)")
ax.set_ylim(0, 100)
ax.set_xlim(-0.6, nd - 0.4)
ax.grid(axis="x", visible=False)
handles = [Patch(color=c, label=lab) for _, _, lab, c in SERIES]
handles.append(Line2D([0], [0], color=ORANGE, lw=1.8, label="Homeric verse vs the rest of Homer (reference)"))
handles.append(Line2D([0], [0], color=INK, lw=1.4, label="shuffled-word baseline (mean; whisker 2.5–97.5%)"))
ax.legend(handles=handles, loc="upper right", ncol=1, handlelength=1.6)
ax.set_title(f"Coverage of the poem ({n_all} verses, {D['tokens']} tokens) by Homeric n-grams (bootstrap 95% CI)",
             loc="left", color=INK)
ax.annotate(f"min: n-gram attested ≥ 1× or ≥ 2× in Homer; 'not function-only' excludes n-grams made of the "
            f"{D['function_words']} function words alone", (0, -0.30), xycoords="axes fraction", fontsize=7, color=INK2)
save(fig, "fig5_poem")
