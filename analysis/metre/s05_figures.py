"""Figures for report.md (figures/). Values plotted are read from results/ or recomputed from results/ tables.

fig1 words vs available time; fig2 formula share by A tercile (base, R1) and by dead-ball category; fig3 formula string
syllables by A tercile; fig4 index-shift null distributions; fig5 (exploratory) lengths of written updates vs TV transcripts.
Error bars in fig2 are block-bootstrap 95% CIs recomputed here with B = 2,000 (display only; reported CIs are in results/).
"""
import json
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

sys.path.insert(0, str(Path(__file__).resolve().parent))
from metre_lib import FIG, RES, SEED, TAGS, TR, block_bootstrap_indices, read_jsonl, tokenize  # noqa: E402

FIG.mkdir(parents=True, exist_ok=True)
LABEL = {"2019wimF": "2019 final (in-sample)", "2023wimF": "2023 final (held-out)"}


def terciles(A):
    q1, q2 = np.quantile(A, [1 / 3, 2 / 3])
    return np.where(A <= q1, 0, np.where(A > q2, 2, 1))


# ---- fig1
fig, axes = plt.subplots(1, 2, figsize=(11, 4.4), sharey=True)
for ax, tag in zip(axes, TAGS):
    U = pd.read_csv(RES / f"units_{tag}.csv")
    t5 = json.load(open(RES / f"t5_{tag}.json"))
    one = U.n_clips == 1
    ax.scatter(U.A[one], U.words[one], s=12, alpha=.6, label="1 clip")
    ax.scatter(U.A[~one], U.words[~one], s=12, alpha=.6, marker="^", label="2+ clips (fault clip)")
    xs = np.linspace(U.A.min(), U.A.max(), 200)
    qr = t5["quantreg_0.9"]
    ax.plot(xs, qr["intercept"] + qr["slope_words_per_s"] * xs, "k--", lw=1, label="0.9 quantile regression")
    ax.set_xscale("log")
    ax.set_xticks([15, 20, 30, 50, 100, 200, 300], ["15", "20", "30", "50", "100", "200", "300"])
    ax.minorticks_off()
    ax.set_xlabel("available time A = serve-to-serve cycle (s, log scale)")
    ax.set_title(LABEL[tag], fontsize=10)
    ax.legend(fontsize=8)
axes[0].set_ylabel("tokens attached to the point")
fig.tight_layout()
fig.savefig(FIG / "fig1_words_vs_available_time.png", dpi=150)
plt.close(fig)

# ---- fig2
fig, axes = plt.subplots(1, 3, figsize=(13, 4.2))
for k, tag in enumerate(TAGS):
    U = pd.read_csv(RES / f"units_{tag}.csv").sort_values("point_idx").reset_index(drop=True)
    A = U.A.to_numpy(float)
    idx = block_bootstrap_indices(len(U), 2000, 10, SEED)
    for j, (v, mk) in enumerate([("base", "o"), ("R1", "s")]):
        tok, cov = U[f"n_tok_{v}"].to_numpy(float), U[f"n_cov_{v}"].to_numpy(float)
        T = terciles(A)
        est = [cov[T == g].sum() / tok[T == g].sum() for g in range(3)]
        bs = np.array([[cov[i][terciles(A[i]) == g].sum() / tok[i][terciles(A[i]) == g].sum() for g in range(3)] for i in idx])
        lo, hi = np.quantile(bs, .025, 0), np.quantile(bs, .975, 0)
        x = np.arange(3) + (j - .5) * .15
        axes[k].errorbar(x, est, yerr=[np.array(est) - lo, hi - np.array(est)], fmt=mk, capsize=3,
                         label={"base": "all tokens", "R1": "score-call tokens removed (R1)"}[v])
    axes[k].set_xticks(range(3), ["short A", "middle A", "long A"])
    axes[k].set_title(LABEL[tag], fontsize=10)
    axes[k].set_ylabel("formula share (token-pooled)")
    axes[k].legend(fontsize=8)
U = pd.read_csv(RES / "units_2019wimF.csv").sort_values("point_idx").reset_index(drop=True)
idx = block_bootstrap_indices(len(U), 2000, 10, SEED)
cats = ["within_game", "other_game_end", "changeover"]
tok, cov, cat = U.n_tok_base.to_numpy(float), U.n_cov_base.to_numpy(float), U.category.to_numpy()
est = [cov[cat == c].sum() / tok[cat == c].sum() for c in cats]
bs = np.array([[cov[i][cat[i] == c].sum() / max(1, tok[i][cat[i] == c].sum()) for c in cats] for i in idx])
lo, hi = np.quantile(bs, .025, 0), np.quantile(bs, .975, 0)
axes[2].errorbar(range(3), est, yerr=[np.array(est) - lo, hi - np.array(est)], fmt="o", capsize=3)
axes[2].set_xticks(range(3), ["within game", "other game end", "changeover/\nset break"])
axes[2].set_title("2019: dead-ball category (T4)", fontsize=10)
axes[2].set_ylabel("formula share (token-pooled)")
fig.tight_layout()
fig.savefig(FIG / "fig2_formula_share.png", dpi=150)
plt.close(fig)

# ---- fig3
fig, axes = plt.subplots(1, 2, figsize=(10, 4), sharey=True)
for ax, tag in zip(axes, TAGS):
    U = pd.read_csv(RES / f"units_{tag}.csv")
    S = pd.read_csv(RES / f"strings_{tag}.csv")
    S = S[S.variant == "base"].merge(U[["point_idx", "A"]], on="point_idx")
    q1, q2 = np.quantile(U.A, [1 / 3, 2 / 3])
    groups = [S.syll[S.A <= q1], S.syll[(S.A > q1) & (S.A <= q2)], S.syll[S.A > q2]]
    ax.boxplot(groups, showfliers=False)
    ax.set_xticks([1, 2, 3], [f"short A\n(n={len(groups[0])})", f"middle A\n(n={len(groups[1])})", f"long A\n(n={len(groups[2])})"])
    ax.set_title(LABEL[tag], fontsize=10)
axes[0].set_ylabel("syllables per formulaic string")
fig.tight_layout()
fig.savefig(FIG / "fig3_formula_syllables.png", dpi=150)
plt.close(fig)

# ---- fig4
names = {"T1": "T1 Spearman(words, A)", "T2": "T2 share short - long", "T3": "T3 Spearman(syllables, A)",
         "T4": "T4 share within - changeover"}
fig, axes = plt.subplots(2, 4, figsize=(14, 5.5))
for r, tag in enumerate(TAGS):
    Z = np.load(RES / f"nulls_{tag}.npz")
    for c, t in enumerate(["T1", "T2", "T3", "T4"]):
        ax = axes[r, c]
        if f"{t}_null" not in Z:
            ax.text(.5, .5, "not testable", ha="center", va="center")
            ax.set_axis_off()
            continue
        ax.hist(Z[f"{t}_null"], bins=30, color="0.7")
        ax.axvline(Z[f"{t}_obs"][0], color="r")
        ax.set_title(f"{tag}: {names[t]}", fontsize=8)
fig.suptitle("Index-shift nulls (grey) and observed statistics (red)", fontsize=10)
fig.tight_layout()
fig.savefig(FIG / "fig4_shift_nulls.png", dpi=150)
plt.close(fig)

# ---- fig5 (exploratory)
corn = np.array([len(tokenize(r.get("text_corrected") or r.get("text_raw"))) for r in read_jsonl(TR / "text_cornell.jsonl")])
C19 = pd.read_csv(RES / "clips_2019wimF.csv")
U19 = pd.read_csv(RES / "units_2019wimF.csv")
fig, ax = plt.subplots(figsize=(6, 4))
for arr, lab in [(corn, "Cornell written update"), (C19.n_tok[C19.n_tok > 0].to_numpy(), "2019 TV clip (non-empty)"),
                 (U19.words[U19.words > 0].to_numpy(), "2019 TV unit (non-empty)")]:
    x = np.sort(arr)
    ax.step(x, np.arange(1, len(x) + 1) / len(x), where="post", label=f"{lab}, n={len(x)}")
ax.set_xscale("log")
ax.set_xlabel("tokens")
ax.set_ylabel("cumulative proportion")
ax.set_title("EXPLORATORY: length distributions by medium", fontsize=10)
ax.legend(fontsize=8)
fig.tight_layout()
fig.savefig(FIG / "fig5_lengths_by_medium_exploratory.png", dpi=150)
plt.close(fig)
print("figures written:", sorted(p.name for p in FIG.glob("*.png")))
