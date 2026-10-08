"""Figures for report.md, drawn from results/ only (matplotlib, Agg). Output: figures/*.png
Run: python -I analysis/parry/p07_figures.py
"""
import sys
from collections import defaultdict
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import lib2b as L

R = L.RESULTS
FIG = L.FIGURES
FIG.mkdir(parents=True, exist_ok=True)


def f(x):
    try:
        return float(x)
    except (TypeError, ValueError):
        return np.nan


def label(t):
    return {"cornell": "Cornell live text", "press_pooled": "press, pooled", "press_federer": "press: Federer",
            "press_djokovic": "press: Djokovic", "press_murray": "press: Murray", "press_nadal": "press: Nadal"}.get(t, L.short(t))


def fig_heatmap():
    rows = [r for r in L.read_csv(R / "sharing_pairs.csv") if r["S"] == "1500" and r["tokens"] == "norm" and r["measure"] == "cov_base"]
    teams = L.TV + ["cornell", "press_pooled", "press_federer", "press_djokovic", "press_murray", "press_nadal"]
    ix = {t: k for k, t in enumerate(teams)}
    M = np.full((len(teams), len(teams)), np.nan)
    for r in rows:
        M[ix[r["source"]], ix[r["target"]]] = 100 * f(r["excess"])
    fig, ax = plt.subplots(figsize=(11, 9.5))
    im = ax.imshow(M, cmap="viridis")
    ax.set_xticks(range(len(teams)))
    ax.set_yticks(range(len(teams)))
    ax.set_xticklabels([label(t) for t in teams], rotation=90, fontsize=7)
    ax.set_yticklabels([label(t) for t in teams], fontsize=7)
    ax.set_xlabel("target j (text measured)")
    ax.set_ylabel("source i (inventory)")
    ax.axhline(19.5, color="w", lw=1)
    ax.axvline(19.5, color="w", lw=1)
    fig.colorbar(im, ax=ax, label="excess coverage, percentage points (observed - shuffled)")
    ax.set_title("Pairwise sharing at 1,500 tokens (n >= 2, 2b normalisation; mean of 500 replicates)")
    fig.tight_layout()
    fig.savefig(FIG / "fig1_sharing_heatmap.png", dpi=150)
    plt.close(fig)


def fig_summary():
    agg = L.read_csv(R / "sharing_aggregates.csv")
    get = {(r["S"], r["tokens"], r["measure"], r["statistic"]): r for r in agg}
    fig, axes = plt.subplots(1, 4, figsize=(14, 4), sharey=False)
    srcs = [("TV", "TV->TV mean"), ("Cornell", "cornell->TV mean"), ("press", "press_pooled->TV mean")]
    for ax, (S, m) in zip(axes, [("1500", "cov_base"), ("1500", "cov_n3"), ("3000", "cov_base"), ("3000", "cov_n3")]):
        for k, (lab, st) in enumerate(srcs):
            o = get[(S, "norm", m, st + " obs")]
            n = get[(S, "norm", m, st + " null")]
            ax.bar(k, 100 * f(o["estimate"]), color="C0", alpha=0.8, label="observed" if k == 0 else None)
            ax.errorbar(k, 100 * f(o["estimate"]), yerr=[[100 * (f(o["estimate"]) - f(o["ci_lo"]))], [100 * (f(o["ci_hi"]) - f(o["estimate"]))]],
                        color="k", capsize=3)
            ax.bar(k, 100 * f(n["estimate"]), color="C3", alpha=0.8, width=0.5, label="shuffled null" if k == 0 else None)
        ax.set_xticks(range(3))
        ax.set_xticklabels([s for s, _ in srcs])
        ax.set_title(f"S = {S}, {'n >= 2' if m == 'cov_base' else 'n >= 3'}")
        ax.set_ylabel("coverage of a TV stream, %")
    axes[0].legend(fontsize=8)
    fig.suptitle("Source -> TV target coverage at matched size (95% CI: bootstrap over TV streams)")
    fig.tight_layout()
    fig.savefig(FIG / "fig2_sharing_summary.png", dpi=150)
    plt.close(fig)


def fig_core():
    rows = L.read_csv(R / "core_sizes.csv")
    fig, ax = plt.subplots(figsize=(7, 4.5))
    for size, tok, col, lab in (("full", "norm", "types_base", "full streams, n >= 2"), ("full", "norm", "types_n3", "full streams, n >= 3"),
                                ("matched S=1500", "norm", "types_base", "1,500-token subsamples, n >= 2")):
        rs = [r for r in rows if r["size"] == size and r["tokens"] == tok]
        ax.plot([int(r["k"]) for r in rs], [max(f(r[col]), 0.1) for r in rs], marker="o", label=lab)
    ax.set_yscale("log")
    ax.set_xlabel("k (number of the 20 TV streams whose inventory contains the n-gram)")
    ax.set_ylabel("core size (types), log scale")
    ax.set_title("Genre core: n-grams used as formulas by at least k teams")
    ax.legend()
    fig.tight_layout()
    fig.savefig(FIG / "fig3_core_curve.png", dpi=150)
    plt.close(fig)


def fig_idiolect():
    rows = [r for r in L.read_csv(R / "idiolect_shares.csv") if r["size"].startswith("matched")]
    slots = ["SCORE", "OFFICIAL", "SHOT", "JUDGE", "STAT", "CROWD", "OTHER", "ALL"]
    fig, ax = plt.subplots(figsize=(9, 4.5))
    for k, s in enumerate(slots):
        v = [f(r["share_idiolect"]) for r in rows if r["slot"] == s]
        c = [f(r["share_core10"]) for r in rows if r["slot"] == s]
        ax.scatter(np.full(len(v), k - 0.12) + np.random.default_rng(k).uniform(-0.05, 0.05, len(v)), v, s=10, color="C1", alpha=0.6)
        ax.scatter(np.full(len(c), k + 0.12) + np.random.default_rng(k + 9).uniform(-0.05, 0.05, len(c)), c, s=10, color="C0", alpha=0.6)
        ax.plot([k - 0.25, k], [np.mean(v)] * 2, color="C1", lw=2)
        ax.plot([k, k + 0.25], [np.mean(c)] * 2, color="C0", lw=2)
    ax.plot([], [], color="C1", lw=2, label="idiolect share (formula in no other stream)")
    ax.plot([], [], color="C0", lw=2, label="core share (formula in >= 10 streams)")
    ax.set_xticks(range(len(slots)))
    ax.set_xticklabels(slots)
    ax.set_ylabel("share of the stream's formula tokens")
    ax.set_title("Idiolect vs genre core by situational slot (1,500-token subsamples, mean of 200; dots = streams)")
    ax.legend(fontsize=8)
    fig.tight_layout()
    fig.savefig(FIG / "fig4_idiolect_by_slot.png", dpi=150)
    plt.close(fig)


def fig_targets():
    rows = L.read_csv(R / "pool_to_target.csv")
    loo = {r["target"]: r for r in rows if r["mode"] == "loo19" and r["tokens"] == "raw"}
    mat = {r["target"]: r for r in rows if r["mode"].startswith("matched")}
    order = sorted(loo, key=lambda t: f(loo[t]["base"]))
    fig, ax = plt.subplots(figsize=(8, 7))
    for k, t in enumerate(order):
        r = loo[t]
        col = "C3" if t == L.MAIN else ("C1" if t == L.HELDOUT else "C0")
        ax.errorbar(100 * f(r["base"]), k, xerr=[[100 * (f(r["base"]) - f(r["base_lo"]))], [100 * (f(r["base_hi"]) - f(r["base"]))]],
                    fmt="o", color=col, capsize=2)
        if t in mat:
            ax.plot(100 * f(mat[t]["base"]), k, marker="x", color="grey")
    ax.set_yticks(range(len(order)))
    ax.set_yticklabels([L.short(t) for t in order], fontsize=7)
    ax.set_xlabel("coverage by the other 19 streams' repeated n-grams (n >= 2, raw tokens), %")
    ax.set_title("Pool -> target coverage for every TV stream (o: 95% bootstrap CI; x: I subsampled to 100,000 tokens)")
    fig.tight_layout()
    fig.savefig(FIG / "fig5_pool_to_target.png", dpi=150)
    plt.close(fig)


def fig_refexpr():
    rows = [r for r in L.read_csv(R / "refexpr_category_shares.csv") if r["references"] == "commentary_only" and r["team"] != "ALL_TV"]
    cats = ["surname", "first_name", "full_name", "hypocoristic", "epithet", "title_surname"]
    rows.sort(key=lambda r: -f(r["share_surname"]))
    fig, ax = plt.subplots(figsize=(10, 4.8))
    bottom = np.zeros(len(rows))
    for c in cats:
        v = np.array([f(r[f"share_{c}"]) for r in rows])
        v = np.nan_to_num(v)
        ax.bar(range(len(rows)), v, bottom=bottom, label=c.replace("_", " "))
        bottom += v
    ax.set_xticks(range(len(rows)))
    ax.set_xticklabels([r["label"] for r in rows], rotation=90, fontsize=7)
    ax.set_ylabel("share of commentary-only references")
    ax.set_title("How each team names the two players (resolved references; umpire patterns excluded)")
    ax.legend(fontsize=7, ncol=3)
    fig.tight_layout()
    fig.savefig(FIG / "fig6_refexpr_categories.png", dpi=150)
    plt.close(fig)


def fig_extension():
    rows = L.read_csv(R / "extension_per_stream.csv")
    ext = {r["analysis"]: r for r in L.read_csv(R / "extension_2b.csv")}
    h = ext["H5"]
    rows = [r for r in rows if r["rho"] not in ("", "nan")]
    rows.sort(key=lambda r: f(r["rho"]))
    fig, ax = plt.subplots(figsize=(7, 6))
    ax.scatter([f(r["rho"]) for r in rows], range(len(rows)), s=[3 * f(r["tokens"]) ** 0.8 for r in rows], color="C0", alpha=0.7)
    ax.axvline(0, color="k", lw=0.8)
    ax.axvspan(f(h["boot_lo"]), f(h["boot_hi"]), color="C3", alpha=0.2, label="weighted mean rho, stream-bootstrap 95% CI")
    ax.axvline(f(h["rho_weighted"]), color="C3")
    ax.set_yticks(range(len(rows)))
    ax.set_yticklabels([r["label"] for r in rows], fontsize=7)
    ax.set_xlabel("Spearman rho, syllables of a reference vs time after its clip (A_after)")
    ax.set_title("Extension test H5 per stream (dot size = references)")
    ax.legend(fontsize=8)
    fig.tight_layout()
    fig.savefig(FIG / "fig7_extension.png", dpi=150)
    plt.close(fig)


def fig_calibration():
    p = R / "calibration_prf.csv"
    if not p.exists():
        return
    rows = [r for r in L.read_csv(p) if r["coder_confidence"] == "HIGH+MEDIUM"]
    ms = list(dict.fromkeys(r["measure"] for r in rows))
    refs = ["A", "B", "A_and_B", "A_or_B"]
    fig, axes = plt.subplots(1, 2, figsize=(12, 4.5), sharey=True)
    for ax, what in zip(axes, ("precision", "recall")):
        w = 0.2
        for k, ref in enumerate(refs):
            v = [f(next(r[what] for r in rows if r["measure"] == m and r["reference"] == ref)) for m in ms]
            lo = [f(next(r[what + "_lo"] for r in rows if r["measure"] == m and r["reference"] == ref)) for m in ms]
            hi = [f(next(r[what + "_hi"] for r in rows if r["measure"] == m and r["reference"] == ref)) for m in ms]
            x = np.arange(len(ms)) + (k - 1.5) * w
            ax.bar(x, v, width=w, label=ref.replace("_", " "))
            ax.errorbar(x, v, yerr=[np.array(v) - np.array(lo), np.array(hi) - np.array(v)], fmt="none", color="k", capsize=1.5, lw=0.7)
        ax.set_xticks(range(len(ms)))
        ax.set_xticklabels(ms, rotation=45, ha="right", fontsize=7)
        ax.set_title(f"token-level {what} vs LLM coders (HIGH+MEDIUM spans)")
    axes[0].legend(fontsize=7)
    fig.tight_layout()
    fig.savefig(FIG / "fig8_calibration.png", dpi=150)
    plt.close(fig)


def fig_largeI():
    """POST HOC (addendum 1, A1): per-target coverage of TV targets by 100,000-token sources (observed, 2b normalisation)."""
    rows = [r for r in L.read_csv(R / "largeI_coverage.csv") if r["tokens"] == "norm"]
    srcs = [("tv_other19", "other 19 TV streams"), ("cornell", "Cornell live text"), ("press_pooled", "press answers")]
    fig, axes = plt.subplots(1, 2, figsize=(11, 4.5), sharey=False)
    for ax, (m, lab_) in zip(axes, (("obs_n2", "n >= 2"), ("obs_n3", "n >= 3"))):
        for k, (src, sl) in enumerate(srcs):
            v = defaultdict(list)
            for r in rows:
                if r["source"] == src:
                    v[r["target"]].append(f(r[m]))
            y = [100 * np.mean(v[t]) for t in L.TV]
            ax.scatter(np.full(len(y), k) + np.linspace(-0.15, 0.15, len(y)), y, s=14, label=sl)
            ax.hlines(np.mean(y), k - 0.3, k + 0.3, color="k", lw=1.2)
        for t in L.TV:
            ys = [100 * np.mean([f(r[m]) for r in rows if r["source"] == src and r["target"] == t]) for src, _ in srcs]
            ax.plot(range(3), ys, color="0.8", lw=0.5, zorder=0)
        ax.set_xticks(range(3))
        ax.set_xticklabels([sl for _, sl in srcs])
        ax.set_ylabel("% of the TV target's tokens covered")
        ax.set_title(f"{lab_} (I = 100,000 tokens; mean of 5 samples)")
    fig.suptitle("Coverage of each of the 20 TV streams (whole text) by sources of equal size; lines join one target")
    fig.tight_layout()
    fig.savefig(FIG / "fig9_largeI_coverage.png", dpi=150)
    plt.close(fig)


def fig_tvonly_slots():
    """POST HOC (addendum 1, A1): slot composition of the TV-only and the shared n >= 3 tokens."""
    rows = L.read_csv(R / "largeI_tvonly_slots.csv")
    groups = [("ALL_TV", "tv_only", "20 targets: TV-only"), ("ALL_TV", "shared", "20 targets: shared"),
              ("ALL_TV", "tv_only_strict", "20 targets: TV-only, strict"), (L.MAIN, "tv_only", "2019 final: TV-only"),
              (L.HELDOUT, "tv_only", "2023 final: TV-only")]
    fig, ax = plt.subplots(figsize=(10, 4.2))
    left = np.zeros(len(groups))
    for sl in L.SLOTS:
        v = np.array([100 * f(next(r["share_of_class"] for r in rows if r["target"] == t and r["class"] == c and r["slot"] == sl)) for t, c, _ in groups])
        ax.barh(range(len(groups)), v, left=left, label=sl)
        left += v
    ax.set_yticks(range(len(groups)))
    ax.set_yticklabels([g[2] for g in groups])
    ax.invert_yaxis()
    ax.set_xlabel("% of the class's tokens (slot of the longest covering n >= 3 occurrence, classify(span))")
    ax.legend(ncol=7, fontsize=7, loc="lower center", bbox_to_anchor=(0.5, 1.0))
    fig.tight_layout()
    fig.savefig(FIG / "fig10_tvonly_slots.png", dpi=150)
    plt.close(fig)


def main():
    for fn in (fig_heatmap, fig_summary, fig_core, fig_idiolect, fig_targets, fig_refexpr, fig_extension, fig_calibration,
               fig_largeI, fig_tvonly_slots):
        fn()
        print("ok", fn.__name__)


if __name__ == "__main__":
    main()
