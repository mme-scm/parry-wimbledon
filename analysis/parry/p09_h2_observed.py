"""POST HOC (plan.md addendum 1, M1/M2): H2 on observed coverage, why the Cornell shuffled null is large, and H1 as a check.

(1) The H2-type statistic (mean over TV targets of [mean TV-source coverage - baseline coverage]) on observed, shuffled and excess
    coverage, S = 1,500 and 3,000, base / n3 / content, normalised and raw tokens, from results/sharing_pairs.csv; vertex bootstrap
    over TV streams (B = 10,000; the same resampling as lib2b.vertex_boot_vs_baseline, vectorised and checked against it).
(2) Unigram concentration per corpus (2b normalisation): <name>, <num> token shares, Simpson index, share of the 10 commonest types;
    and over 50 unigram-shuffled 1,500-token subsamples per team, the shuffled inventory size and the share of its types containing a
    placeholder (and the same for the unshuffled subsamples).
(3) H1 as a check: share of the TV -> TV excess reached by press -> TV and Cornell -> TV; press-speaker yardstick.

Outputs (results/): h2_observed.csv, unigram_concentration.csv, shuffled_inventory_composition.csv, h1_check.json
Run: python -I analysis/parry/p09_h2_observed.py
"""
import sys
from collections import Counter
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import numpy as np
import lib2b as L

B = 10000
R_SHUF, S_SHUF = 50, 1500
HYPO = ("rafa", "nole", "rog", "carlitos")


def vboot_fast(M, base, B_, rng):
    """Same draws and statistic as lib2b.vertex_boot_vs_baseline, vectorised over targets."""
    n = M.shape[0]
    out = np.empty(B_)
    for b in range(B_):
        idx = rng.integers(0, n, n)
        sub = M[np.ix_(idx, idx)]
        mask = idx[:, None] != idx[None, :]
        cnt = mask.sum(0)
        ok = cnt > 0
        colmean = np.where(ok, (np.where(mask, sub, 0.0)).sum(0) / np.maximum(cnt, 1), np.nan)
        out[b] = np.mean(colmean[ok] - base[idx][ok])
    return out


def matrices(rows, S, tok, meas):
    tv = [s for s in L.TV if any(r["source"] == s for r in rows if r["S"] == S and r["tokens"] == tok and r["measure"] == meas)]
    ix = {s: k for k, s in enumerate(tv)}
    n = len(tv)
    O, N, E = (np.full((n, n), np.nan) for _ in range(3))
    base = {b: np.full((3, n), np.nan) for b in ("cornell", "press_pooled")}
    for r in rows:
        if r["S"] != S or r["tokens"] != tok or r["measure"] != meas:
            continue
        a, t = r["source"], r["target"]
        vals = (float(r["obs_mean"]), float(r["null_mean"]), float(r["excess"]))
        if a in ix and t in ix:
            O[ix[a], ix[t]], N[ix[a], ix[t]], E[ix[a], ix[t]] = vals
        elif a in base and t in ix:
            base[a][:, ix[t]] = vals
    return tv, (O, N, E), base


def main():
    rows = L.read_csv(L.RESULTS / "sharing_pairs.csv")
    rng = np.random.default_rng([L.SEED, 110])
    # check the vectorised bootstrap against lib2b on one configuration
    tv, (O, N, E), base = matrices(rows, "1500", "norm", "cov_base")
    d1 = L.vertex_boot_vs_baseline(E, base["cornell"][2], 50, np.random.default_rng(1))
    d2 = vboot_fast(E, base["cornell"][2], 50, np.random.default_rng(1))
    assert np.allclose(d1, d2), "vectorised vertex bootstrap differs from lib2b"
    out = []
    for S in ("1500", "3000"):
        for tok in ("norm", "raw"):
            for meas in ("cov_base", "cov_n3", "cov_content"):
                tv, mats, base = matrices(rows, S, tok, meas)
                if not tv:
                    continue
                n = len(tv)
                for b in ("cornell", "press_pooled"):
                    for k, what in enumerate(("observed", "shuffled", "excess")):
                        M, bv = mats[k], base[b][k]
                        per_t = np.array([np.mean(M[[i for i in range(n) if i != j], j]) - bv[j] for j in range(n)])
                        draws = vboot_fast(M, bv, B, rng)
                        out.append({"S": S, "tokens": tok, "measure": meas, "baseline": b, "coverage": what, "estimate": float(per_t.mean()),
                                    "ci_lo": float(np.percentile(draws, 2.5)), "ci_hi": float(np.percentile(draws, 97.5)),
                                    "p_two": L.boot_p_two(draws), "targets_positive": int(np.sum(per_t > 0)), "n_targets": n,
                                    "tv_tv_mean": float(np.nanmean(M[~np.eye(n, dtype=bool)])), "baseline_to_tv_mean": float(np.mean(bv)),
                                    "B": B, "uncertainty": "vertex bootstrap over TV streams (lib2b.vertex_boot_vs_baseline draws)"})
    L.write_csv(L.RESULTS / "h2_observed.csv", out)

    # ---------------------------------------------------------------- (2) unigram concentration and shuffled inventories
    tv_teams = [L.load_tv(s) for s in L.TV]
    corn, press = L.load_cornell(), L.load_press(None)
    conc = []

    def conc_row(name, utts, raw_utts=None):
        c = Counter(t for u in utts for t in u)
        n = sum(c.values())
        p = np.array(sorted(c.values(), reverse=True), float) / n
        nm = sum(v for k, v in c.items() if k.startswith(L.NAME_TOKEN))
        row = {"corpus": name, "tokens": n, "types": len(c), "share_name": nm / n, "share_num": c.get(L.NUM_TOKEN, 0) / n,
               "simpson_sum_p2": float(np.sum(p ** 2)), "share_top10_types": float(p[:10].sum())}
        if raw_utts is not None:
            rc = Counter(t for u in raw_utts for t in u)
            row["hypocoristic_tokens_raw"] = int(sum(rc.get(h, 0) for h in HYPO))
            row["hypocoristic_per_1000"] = 1000 * row["hypocoristic_tokens_raw"] / n
        return row
    conc.append(conc_row("TV, 20 streams pooled", [u for t in tv_teams for u in t.norm], [u for t in tv_teams for u in t.raw]))
    tvr = [conc_row(t.name, t.norm, t.raw) for t in tv_teams]
    mean_row = {"corpus": "TV, mean over the 20 streams"}
    for k in ("share_name", "share_num", "simpson_sum_p2", "share_top10_types", "hypocoristic_per_1000"):
        mean_row[k] = float(np.mean([r[k] for r in tvr]))
    conc.append(mean_row)
    conc.append(conc_row("cornell", corn.norm, corn.raw))
    conc.append(conc_row("press_pooled", press.norm, press.raw))
    L.write_csv(L.RESULTS / "unigram_concentration.csv", conc,
                ["corpus", "tokens", "types", "share_name", "share_num", "simpson_sum_p2", "share_top10_types", "hypocoristic_tokens_raw",
                 "hypocoristic_per_1000"])
    comp = []
    teams = tv_teams + [corn, press]
    for ti, t in enumerate(teams):
        r_ = np.random.default_rng([L.SEED, 111, ti])
        sizes, ph, sizes_o, ph_o = [], [], [], []
        for _ in range(R_SHUF):
            idx = L.subsample(t.raw, S_SHUF, r_)
            u = [t.norm[i] for i in idx]
            for utts, sz, pp in ((L.shuffle_utts(u, r_), sizes, ph), (u, sizes_o, ph_o)):
                F = L.C.formula_set_fast(utts, m=2)
                sz.append(len(F))
                pp.append(np.mean([any(x == L.NUM_TOKEN or x.startswith(L.NAME_TOKEN) for x in g) for g in F]) if F else np.nan)
        comp.append({"team": t.name, "medium": t.medium, "S": S_SHUF, "R": R_SHUF, "shuffled_types": float(np.mean(sizes)),
                     "shuffled_share_with_placeholder": float(np.nanmean(ph)), "observed_types": float(np.mean(sizes_o)),
                     "observed_share_with_placeholder": float(np.nanmean(ph_o))})
    L.write_csv(L.RESULTS / "shuffled_inventory_composition.csv", comp)

    # ---------------------------------------------------------------- (3) H1 as a check
    agg = {(r["S"], r["tokens"], r["measure"], r["statistic"]): r for r in L.read_csv(L.RESULTS / "sharing_aggregates.csv")}
    chk = {}
    for S in ("1500", "3000"):
        for meas in ("cov_base", "cov_n3"):
            tvx = float(agg[(S, "norm", meas, "TV->TV mean excess")]["estimate"])
            d = {"tv_tv_excess": tvx}
            for b in ("cornell", "press_pooled"):
                bx = float(agg[(S, "norm", meas, f"{b}->TV mean excess")]["estimate"])
                d[f"{b}_to_tv_excess"] = bx
                d[f"{b}_share_of_tv_tv_excess"] = bx / tvx if tvx else float("nan")
            chk[f"S{S}_{meas}"] = d
    sp = ["press_federer", "press_djokovic", "press_murray", "press_nadal"]
    chk["press_speakers_mean_excess_S1500_base"] = float(np.mean([float(agg[("1500", "norm", "cov_base", f"{x}->{y} excess")]["estimate"])
                                                                   for x in sp for y in sp if x != y]))
    L.write_json(L.RESULTS / "h1_check.json", chk)
    print("done")


if __name__ == "__main__":
    main()
