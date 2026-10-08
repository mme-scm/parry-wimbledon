"""2b.1 pairwise sharing at matched size (plan sections 2, 3, 7: H1a, H1b, H2a, H2b).

For every replicate, each team (20 TV streams, cornell, press_pooled, 4 press speakers) is subsampled to S tokens (whole utterances);
its inventory (n-grams in >= 2 utterances, not stop-only) is identified; for each ordered pair (i, j) the coverage of j by i's inventory
(base, n3, content) and the Jaccard of the inventories (base, n3) are computed, on the observed texts and on unigram-shuffled copies.

Outputs: results/sharing_pairs.csv, results/sharing_aggregates.csv, results/sharing_per_team.csv, results/inventory_sizes_matched.csv,
results/primary_H1H2.json, results/sharing_meta.json
Run: python -I analysis/parry/p01_sharing.py
"""
import sys
import time
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from multiprocessing import Pool
import numpy as np
import lib2b as L

CONFIGS = [(1500, 500, ("norm", "raw")), (3000, 200, ("norm",))]   # (S, R, token variants)
MEASURES = ("cov_base", "cov_n3", "cov_content", "jac_base", "jac_n3")
B_CI, B_P = 2000, 10000
TEAMS = []


def _rep(args):
    S, r, inc, tokvars = args
    rng = np.random.default_rng([L.SEED, S, r])
    n = len(inc)
    idxs = [L.subsample(TEAMS[t].raw, S, rng) for t in inc]
    out = {}
    for tv in tokvars:
        obs, nul = [], []
        sizes = []
        for k, t in enumerate(inc):
            src = TEAMS[t].norm if tv == "norm" else TEAMS[t].raw
            u = [src[i] for i in idxs[k]]
            us = L.shuffle_utts(u, rng)
            o = L.index_inventory(u)
            s_ = L.index_inventory(us)
            obs.append((o[0], L.variants(o[1]), o[2]))
            nul.append((s_[0], L.variants(s_[1]), s_[2]))
            sizes.append([len(o[1]), len({g for g in o[1] if len(g) >= 3}), len(L.variants(o[1])["content"]),
                          len(s_[1]), len({g for g in s_[1] if len(g) >= 3}), o[2]])
        res = {m: np.full((2, n, n), np.nan) for m in MEASURES}
        for a in range(n):
            for b in range(n):
                if a == b:
                    continue
                for w, data in ((0, obs), (1, nul)):
                    Fi = data[a][1]
                    occ_j, _, nt_j = data[b]
                    res["cov_base"][w, a, b] = L.coverage(occ_j, nt_j, Fi["base"], 2)
                    res["cov_n3"][w, a, b] = L.coverage(occ_j, nt_j, Fi["n3"], 3)
                    res["cov_content"][w, a, b] = L.coverage(occ_j, nt_j, Fi["content"], 2)
                    if a < b:
                        Fj = data[b][1]
                        for m, key in (("jac_base", "base"), ("jac_n3", "n3")):
                            A, Bs = Fi[key], Fj[key]
                            u_ = len(A | Bs)
                            val = len(A & Bs) / u_ if u_ else np.nan
                            res[m][w, a, b] = res[m][w, b, a] = val
        out[tv] = (res, np.array(sizes, float))
    return S, r, out


def main():
    global TEAMS
    t0 = time.time()
    TEAMS = L.load_all_teams()
    names = [t.name for t in TEAMS]
    n_tv = len(L.TV)
    meta = {"teams": {t.name: {"tokens": t.ntok, "utterances": len(t.raw), "medium": t.medium} for t in TEAMS},
            "load_s": round(time.time() - t0, 1), "configs": []}
    pair_rows, agg_rows, team_rows, size_rows = [], [], [], []
    primary = {}
    for S, R, tokvars in CONFIGS:
        inc = [k for k, t in enumerate(TEAMS) if t.ntok >= S]
        inc_names = [names[k] for k in inc]
        tv_pos = [p for p, k in enumerate(inc) if k < n_tv]
        t1 = time.time()
        with Pool(4) as pool:
            reps = pool.map(_rep, [(S, r, inc, tokvars) for r in range(R)], chunksize=4)
        meta["configs"].append({"S": S, "R": R, "token_variants": list(tokvars), "teams": inc_names,
                                "tv_streams_included": len(tv_pos), "runtime_s": round(time.time() - t1, 1)})
        for tv in tokvars:
            arr = {m: np.stack([rp[2][tv][0][m] for rp in reps]) for m in MEASURES}   # R x 2 x n x n
            sizes = np.stack([rp[2][tv][1] for rp in reps])                           # R x n x 6
            for p, nm in enumerate(inc_names):
                sz = sizes[:, p, :].mean(0)
                size_rows.append({"S": S, "tokens": tv, "team": nm, "types_base": sz[0], "types_n3": sz[1], "types_content": sz[2],
                                  "types_base_shuffled": sz[3], "types_n3_shuffled": sz[4], "subsample_tokens": sz[5], "R": R})
            for m in MEASURES:
                ob = arr[m][:, 0]
                nu = arr[m][:, 1]
                ex = ob - nu
                mo, mn, me = ob.mean(0), nu.mean(0), ex.mean(0)
                lo, hi = np.nanpercentile(ex, 2.5, axis=0), np.nanpercentile(ex, 97.5, axis=0)
                olo, ohi = np.nanpercentile(ob, 2.5, axis=0), np.nanpercentile(ob, 97.5, axis=0)
                for a, sa in enumerate(inc_names):
                    for b, sb in enumerate(inc_names):
                        if a == b or (m.startswith("jac") and a > b):
                            continue
                        pair_rows.append({"S": S, "tokens": tv, "measure": m, "source": sa, "target": sb, "obs_mean": mo[a, b],
                                          "obs_lo": olo[a, b], "obs_hi": ohi[a, b], "null_mean": mn[a, b], "excess": me[a, b],
                                          "excess_rep_lo": lo[a, b], "excess_rep_hi": hi[a, b], "R": R})
                # ---- aggregates (vertex bootstrap over TV streams)
                tvp = np.array(tv_pos)
                rng = np.random.default_rng([L.SEED, S, 77, MEASURES.index(m), tokvars.index(tv)])
                for what, M in (("obs", mo), ("null", mn), ("excess", me)):
                    Mtv = M[np.ix_(tvp, tvp)]
                    draws = L.vertex_boot_pairs(Mtv, B_CI, rng)
                    est = float(np.nanmean(Mtv[~np.eye(len(tvp), dtype=bool)]))
                    agg_rows.append({"S": S, "tokens": tv, "measure": m, "statistic": f"TV->TV mean {what}", "estimate": est,
                                     "ci_lo": np.percentile(draws, 2.5), "ci_hi": np.percentile(draws, 97.5),
                                     "n_pairs": len(tvp) * (len(tvp) - 1), "uncertainty": "vertex bootstrap over TV streams, B = 2000"})
                    for bp, bname in [(p, nm) for p, nm in enumerate(inc_names) if p not in tv_pos]:
                        row_to = M[bp, tvp]          # baseline -> TV targets
                        row_from = M[tvp, bp]        # TV sources -> baseline
                        for lab, vec in ((f"{bname}->TV mean {what}", row_to), (f"TV->{bname} mean {what}", row_from)):
                            if m.startswith("jac") and lab.startswith("TV->"):
                                continue
                            bd = np.array([vec[rng.integers(0, len(vec), len(vec))].mean() for _ in range(B_CI)])
                            agg_rows.append({"S": S, "tokens": tv, "measure": m, "statistic": lab, "estimate": float(vec.mean()),
                                             "ci_lo": np.percentile(bd, 2.5), "ci_hi": np.percentile(bd, 97.5), "n_pairs": len(vec),
                                             "uncertainty": "bootstrap over TV streams, B = 2000"})
                    # baseline <-> baseline (descriptive)
                    bps = [p for p in range(len(inc_names)) if p not in tv_pos]
                    for a in bps:
                        for b in bps:
                            if a != b and not (m.startswith("jac") and a > b):
                                agg_rows.append({"S": S, "tokens": tv, "measure": m, "statistic": f"{inc_names[a]}->{inc_names[b]} {what}",
                                                 "estimate": float(M[a, b]), "ci_lo": "", "ci_hi": "", "n_pairs": 1,
                                                 "uncertainty": "replicate mean (no CI)"})
                # ---- per team means (rows: as source and as target among TV)
                for p, nm in enumerate(inc_names):
                    others = [q for q in tv_pos if q != p]
                    team_rows.append({"S": S, "tokens": tv, "measure": m, "team": nm,
                                      "as_target_from_TV_obs": float(mo[others, p].mean()), "as_target_from_TV_excess": float(me[others, p].mean()),
                                      "as_source_to_TV_obs": float(mo[p, others].mean()), "as_source_to_TV_excess": float(me[p, others].mean())})
                # ---- H2-type differences: TV->TV excess minus baseline->TV excess, per target, vertex bootstrap
                for bname in ("cornell", "press_pooled"):
                    if bname not in inc_names or m.startswith("jac"):
                        continue
                    bp = inc_names.index(bname)
                    Mtv = me[np.ix_(tvp, tvp)]
                    base_row = me[bp, tvp]
                    B_here = B_P if (S == 1500 and tv == "norm" and m == "cov_base") else B_CI
                    draws = L.vertex_boot_vs_baseline(Mtv, base_row, B_here, rng)
                    est = float(np.mean([np.mean(Mtv[[i for i in range(len(tvp)) if i != j], j]) - base_row[j] for j in range(len(tvp))]))
                    agg_rows.append({"S": S, "tokens": tv, "measure": m, "statistic": f"TV->TV minus {bname}->TV excess",
                                     "estimate": est, "ci_lo": np.percentile(draws, 2.5), "ci_hi": np.percentile(draws, 97.5),
                                     "n_pairs": len(tvp), "uncertainty": f"vertex bootstrap over TV streams, B = {B_here}"})
                    if S == 1500 and tv == "norm" and m == "cov_base":
                        hid = {"cornell": "H2a", "press_pooled": "H2b"}[bname]
                        primary[hid] = {"statistic": f"mean over TV targets of [mean TV-source excess - {bname} excess], base coverage, S = 1500",
                                        "estimate": est, "ci_lo": float(np.percentile(draws, 2.5)), "ci_hi": float(np.percentile(draws, 97.5)),
                                        "p_two": L.boot_p_two(draws), "p_floor": 2 / (B_P + 1), "B": B_P,
                                        "n_targets_positive": int(sum(np.mean(Mtv[[i for i in range(len(tvp)) if i != j], j]) - base_row[j] > 0
                                                                      for j in range(len(tvp)))), "n_targets": len(tvp)}
                # ---- H1 (excess > 0), B = 10,000
                if S == 1500 and tv == "norm" and m in ("cov_base", "cov_n3"):
                    Mtv = me[np.ix_(tvp, tvp)]
                    draws = L.vertex_boot_pairs(Mtv, B_P, rng)
                    est = float(np.mean(Mtv[~np.eye(len(tvp), dtype=bool)]))
                    per_t = [np.mean(Mtv[[i for i in range(len(tvp)) if i != j], j]) for j in range(len(tvp))]
                    hid = {"cov_base": "H1a", "cov_n3": "H1b"}[m]
                    primary[hid] = {"statistic": f"mean over ordered TV pairs of excess coverage ({m[4:]}), S = 1500", "estimate": est,
                                    "ci_lo": float(np.percentile(draws, 2.5)), "ci_hi": float(np.percentile(draws, 97.5)),
                                    "p_two": L.boot_p_two(draws), "p_floor": 2 / (B_P + 1), "B": B_P,
                                    "n_targets_positive": int(sum(x > 0 for x in per_t)), "n_targets": len(tvp),
                                    "obs_mean": float(np.mean(mo[np.ix_(tvp, tvp)][~np.eye(len(tvp), dtype=bool)])),
                                    "null_mean": float(np.mean(mn[np.ix_(tvp, tvp)][~np.eye(len(tvp), dtype=bool)]))}
        print(f"S={S}: R={R}, {len(inc)} teams, {meta['configs'][-1]['runtime_s']} s", flush=True)
    L.write_csv(L.RESULTS / "sharing_pairs.csv", pair_rows)
    L.write_csv(L.RESULTS / "sharing_aggregates.csv", agg_rows)
    L.write_csv(L.RESULTS / "sharing_per_team.csv", team_rows)
    L.write_csv(L.RESULTS / "inventory_sizes_matched.csv", size_rows)
    L.write_json(L.RESULTS / "primary_H1H2.json", primary)
    meta["total_s"] = round(time.time() - t0, 1)
    L.write_json(L.RESULTS / "sharing_meta.json", meta)
    print("done", meta["total_s"], "s")


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--time-one":
        TEAMS = L.load_all_teams()
        inc = list(range(len(TEAMS)))
        t = time.time()
        _rep((1500, 0, inc, ("norm", "raw")))
        print("one replicate (norm+raw):", round(time.time() - t, 2), "s")
    else:
        main()
