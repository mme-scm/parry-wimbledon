"""Figure 4: the serve-to-serve cycle A as a frame. (a) tokens per point vs A by dead-ball category;
(b) pool-repeated n-gram share by A tercile and by category with block-bootstrap CIs; (c, d) the
confirmatory statistics T1-T4 against their circular-shift null (2.5-97.5% band) and bootstrap CIs.
Reads analysis/metre/results/units_2019wimF.csv, details_2019wimF.json, confirmatory_2019wimF.csv and
nulls_2019wimF.npz only."""
import json
import sys as _sys
from pathlib import Path as _Path

_sys.path.insert(0, str(_Path(__file__).resolve().parent))  # python -I does not add the script dir
import numpy as np
import pandas as pd
from matplotlib.ticker import NullFormatter

from common import AQUA, BLUE, INK, INK2, MUTED, ORANGE, RES_M, plt, save

units = pd.read_csv(RES_M / "units_2019wimF.csv")
det = json.load(open(RES_M / "details_2019wimF.json"))
conf = pd.read_csv(RES_M / "confirmatory_2019wimF.csv").set_index("test")
nulls = np.load(RES_M / "nulls_2019wimF.npz")

fig, axes = plt.subplots(2, 2, figsize=(6.6, 5.6))
(ax_a, ax_b), (ax_c, ax_d) = axes

# (a) tokens vs A
CATS = [("within_game", "within game", BLUE), ("other_game_end", "other game end", AQUA), ("changeover", "changeover / set break", ORANGE)]
for key, label, col in CATS:
    s = units[units.category == key]
    ax_a.scatter(s.A, s.n_tok_base, s=22, color=col, alpha=0.75, edgecolor="white", linewidth=0.8, label=f"{label} (n = {len(s)})")
ax_a.set_xscale("log")
ax_a.set_xticks([15, 20, 30, 50, 100, 200, 300])
ax_a.set_xticklabels(["15", "20", "30", "50", "100", "200", "300"])
ax_a.xaxis.set_minor_formatter(NullFormatter())
ax_a.set_xlabel("available time A = serve-to-serve cycle (s, log scale)")
ax_a.set_ylabel("tokens attached to the point")
t1 = conf.loc["T1"]
ax_a.set_title(f"(a) tokens vs A; T1 ρ = {t1.estimate:.3f} [{t1.ci_lo:.3f}, {t1.ci_hi:.3f}]", loc="left", color=INK)
ax_a.legend(loc="upper left")

# (b) group shares
T2, T4 = det["T2"], det["T4"]
groups = [
    (f"short A\n(≤ {T2['A_cut_1_3']:.0f} s)", T2["share_short"], T2["share_short_ci"]),
    (f"long A\n(> {T2['A_cut_2_3']:.0f} s)", T2["share_long"], T2["share_long_ci"]),
    ("within\ngame", T4["share_within_game"], T4["share_within_ci"]),
    ("changeover /\nset break", T4["share_changeover"], T4["share_changeover_ci"]),
]
xs = [0, 1, 2.4, 3.4]
for x, (lab, v, c_) in zip(xs, groups):
    ax_b.errorbar(x, 100 * v, yerr=[[100 * (v - c_[0])], [100 * (c_[1] - v)]], fmt="o", color=BLUE, ms=6, mec="white", mew=1, ecolor=INK, elinewidth=1, capsize=3)
ax_b.set_xticks(xs)
ax_b.set_xticklabels([g[0] for g in groups], fontsize=7.5)
ax_b.set_ylabel("pool-repeated n-gram share (%)")
ax_b.set_title("(b) shares behind T2 and T4 (block-bootstrap 95% CI)", loc="left", color=INK)
ax_b.grid(axis="x", visible=False)
ax_b.annotate("T2: short − long", (0.5, 100 * T2["share_long"] + 2.6), ha="center", fontsize=7.5, color=INK2)
ax_b.annotate("T4: within − changeover", (2.9, 100 * T4["share_within_game"] + 2.6), ha="center", fontsize=7.5, color=INK2)
ax_b.set_ylim(55, 72)

LABELS = {"T1": "T1\nρ(tokens, A)", "T3": "T3\nρ(syllables, A)", "T2": "T2\nshort − long A", "T4": "T4\nwithin − changeover"}


def null_panel(ax, tests, scale, ylabel, title):
    for i, t in enumerate(tests):
        nd = nulls[f"{t}_null"] * scale
        lo, hi = np.percentile(nd, [2.5, 97.5])
        ax.bar(i, hi - lo, bottom=lo, width=0.5, color=MUTED, alpha=0.35, linewidth=0, label="circular-shift null, 2.5–97.5%" if i == 0 else None)
        r = conf.loc[t]
        ax.errorbar(i, r.estimate * scale, yerr=[[(r.estimate - r.ci_lo) * scale], [(r.ci_hi - r.estimate) * scale]], fmt="o", color=BLUE, ms=6, mec="white", mew=1, ecolor=INK, elinewidth=1, capsize=3,
                    label="observed, block-bootstrap 95% CI" if i == 0 else None)
        ax.annotate(f"p = {r.p_shift:.3f}\nHolm {r.p_holm:.3f}", (i, max(hi, r.ci_hi * scale)), xytext=(0, 5), textcoords="offset points", ha="center", fontsize=7, color=INK2)
    ax.axhline(0, color=INK2, lw=0.6)
    ax.set_xticks(range(len(tests)))
    ax.set_xticklabels([LABELS[t] for t in tests], fontsize=7.5)
    ax.set_ylabel(ylabel)
    ax.set_title(title, loc="left", color=INK)
    ax.grid(axis="x", visible=False)
    ax.set_xlim(-0.6, len(tests) - 0.4)


null_panel(ax_c, ["T1", "T3"], 1.0, "Spearman ρ", "(c) rank correlations vs shift null (402 shifts)")
ax_c.set_ylim(-0.2, 0.5)
ax_c.legend(loc="lower right")
null_panel(ax_d, ["T2", "T4"], 100.0, "difference in share (pp)", "(d) share differences vs shift null (402 shifts)")
ax_d.set_ylim(-9, 9)
fig.tight_layout()
save(fig, "fig4_metre")
