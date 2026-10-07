"""Figure 2: injected substitution noise (post hoc) and the corpus contrasts. Two panels: split-half at
matched size (TV pool, Cornell live text, press answers) and the held-out design (pool -> 2019 vs Cornell,
press). Reads analysis/formulas/results/asr_noise_sensitivity.csv and density_main.csv only."""
import sys as _sys
from pathlib import Path as _Path

_sys.path.insert(0, str(_Path(__file__).resolve().parent))  # python -I does not add the script dir
import numpy as np
import pandas as pd

from common import AQUA, BLUE, INK, INK2, MUTED, ORANGE, RES_F, pct, plt, save

raw = pd.read_csv(RES_F / "asr_noise_sensitivity.csv")
agg = (
    raw.groupby(["design", "corpus", "added_substitution_rate"])["density_a"]
    .agg(mean="mean", lo=lambda s: np.percentile(s, 2.5), hi=lambda s: np.percentile(s, 97.5), n="size")
    .reset_index()
)
dm = pd.read_csv(RES_F / "density_main.csv")
tv_heldout_ref = pct(
    dm[(dm.design == "D3_held_out") & (dm.identified_on == "pool (18 matches)") & (dm.measured_on == "tv_2019wimF") & (dm.measure == "a")].density.iloc[0]
)
tv_split_ref = pct(agg[(agg.design == "splithalf_matched") & (agg.corpus == "tv_pool_all") & (agg.added_substitution_rate == 0.0)]["mean"].iloc[0])
HAND_READ_LOWER_BOUND = 0.022  # grid level equal to the corpus's hand-read lower bound (asr_noise_summary.json)

SERIES = {
    "tv_pool_all": ("TV commentary, pool subsample", BLUE),
    "tv_pool_to_2019": ("TV commentary, pool → 2019 final", BLUE),
    "text_cornell": ("Cornell written live text", ORANGE),
    "press_answers": ("press-conference answers", AQUA),
}


def crossing(sub, ref):
    """e* where the linearly interpolated mean first reaches ref (None if it does not)."""
    sub = sub.sort_values("added_substitution_rate")
    e, m = sub.added_substitution_rate.to_numpy(), pct(sub["mean"].to_numpy())
    for k in range(len(e) - 1):
        if (m[k] - ref) * (m[k + 1] - ref) <= 0 and m[k] != m[k + 1]:
            return e[k] + (ref - m[k]) * (e[k + 1] - e[k]) / (m[k + 1] - m[k])
    return None


fig, axes = plt.subplots(1, 2, figsize=(6.6, 3.2), sharex=True)
panels = [
    ("splithalf_matched", ["tv_pool_all", "text_cornell", "press_answers"], tv_split_ref, "split-half at matched size (9,791 tokens)", (0, 45)),
    ("heldout", ["tv_pool_to_2019", "text_cornell", "press_answers"], tv_heldout_ref, "held-out (I ≈ 65k–104k tokens → M 9,791)", (35, 80)),
]
for ax, (design, corpora, ref, title, ylim) in zip(axes, panels):
    ax.set_ylim(*ylim)
    for c in corpora:
        sub = agg[(agg.design == design) & (agg.corpus == c)].sort_values("added_substitution_rate")
        label, col = SERIES[c]
        e = sub.added_substitution_rate.to_numpy()
        ax.fill_between(e, pct(sub.lo.to_numpy()), pct(sub.hi.to_numpy()), color=col, alpha=0.16, linewidth=0)
        ax.plot(e, pct(sub["mean"].to_numpy()), color=col, lw=2, marker="o", ms=4, mec="white", mew=1, label=label)
        if c != corpora[0]:
            es = crossing(sub, ref)
            if es is not None:
                ax.axvline(es, color=col, lw=0.8, ls=":")
                ax.annotate(f"e* = {es:.3f}", (es, ylim[0]), xytext=(3, 4), textcoords="offset points", fontsize=7, color=col)
                print(f"{design} {c}: mean reaches TV reference {ref:.1f}% at e* = {es:.4f}")
            else:
                print(f"{design} {c}: mean stays above TV reference {ref:.1f}% over the grid")
    ax.axhline(ref, color=BLUE, lw=0.8, ls="--")
    ax.annotate(f"TV at e = 0: {ref:.1f}%", (0.0, ref), xytext=(2, 3), textcoords="offset points", fontsize=7, color=BLUE)
    ax.axvline(HAND_READ_LOWER_BOUND, color=MUTED, lw=0.7, ls=(0, (2, 2)))
    ax.annotate("hand-read\nlower bound", (HAND_READ_LOWER_BOUND, ylim[1]), xytext=(2, -2), textcoords="offset points", va="top", fontsize=6.5, color=MUTED)
    ax.set_title(title, loc="left", color=INK)
    ax.set_xlabel("injected substitution rate e")
    ax.set_xlim(-0.005, 0.165)
    ax.set_xticks([0, 0.05, 0.10, 0.15])
    ax.set_xticklabels(["0", "0.05", "0.10", "0.15"])
    ax.legend(loc="upper right")
axes[0].set_ylabel("repeated-n-gram coverage, n ≥ 2 (%)")
fig.suptitle("Injected substitution noise (post hoc): mean and 2.5–97.5% over 50 replicates", x=0.01, ha="left", fontsize=9.5, color=INK)
fig.tight_layout(rect=(0, 0, 1, 0.95))
save(fig, "fig2_noise")
