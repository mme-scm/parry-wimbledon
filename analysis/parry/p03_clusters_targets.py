"""2b.1 exploratory: sharing by commentator-hint cluster, slam, year, gender and shared players; pool -> target coverage for every
TV stream (plan section 8).

Inputs: results/sharing_pairs.csv (p01). Outputs: results/cluster_tests.csv, results/qap_regression.csv, results/pair_2019_2023.json,
results/pool_to_target.csv, results/pool_to_target_meta.json
Run: python -I analysis/parry/p03_clusters_targets.py
"""
import sys
import time
from itertools import combinations
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from multiprocessing import Pool
import numpy as np
import lib2b as L

N_PERM = 10000
B = 2000
I_MATCHED, R_I = 100000, 20
TVT = []


def sim_matrices():
    rows = [r for r in L.read_csv(L.RESULTS / "sharing_pairs.csv") if r["S"] == "1500" and r["tokens"] == "norm"]
    idx = {s: k for k, s in enumerate(L.TV)}
    n = len(L.TV)
    E = np.full((n, n), np.nan)
    J = np.full((n, n), np.nan)
    for r in rows:
        if r["source"] in idx and r["target"] in idx:
            a, b = idx[r["source"]], idx[r["target"]]
            if r["measure"] == "cov_base":
                E[a, b] = float(r["excess"])
            elif r["measure"] == "jac_base":
                J[a, b] = J[b, a] = float(r["obs_mean"])
    Sym = (E + E.T) / 2
    return {"excess_cov_sym": Sym, "jaccard_obs": J}


def within_between(M, lab):
    n = len(lab)
    w, bt = [], []
    for a, b in combinations(range(n), 2):
        (w if lab[a] == lab[b] else bt).append(M[a, b])
    return (np.mean(w) - np.mean(bt)) if w and bt else np.nan, len(w)


def main():
    global TVT
    t0 = time.time()
    metas = [L.stream_meta(s) for s in L.TV]
    n = len(metas)
    mats = sim_matrices()
    rng = np.random.default_rng([L.SEED, 8])
    cl_rows, qap_rows = [], []
    labels = {"slam": [m["slam"] for m in metas], "year": [m["year"] for m in metas], "gender": [m["gender"] for m in metas]}
    hint = [L.HINT_CLUSTER.get(s, f"none:{k}") for k, s in enumerate(L.TV)]
    players = [set(m["players"]) for m in metas]
    shared = np.array([[len(players[a] & players[b]) for b in range(n)] for a in range(n)], float)
    dyear = np.array([[abs(metas[a]["year"] - metas[b]["year"]) for b in range(n)] for a in range(n)], float)
    iu = np.triu_indices(n, 1)
    for mname, M in mats.items():
        for lname, lab in labels.items():
            obs, nw = within_between(M, lab)
            null = np.empty(N_PERM)
            for p in range(N_PERM):
                null[p] = within_between(M, list(rng.permutation(lab)))[0]
            cl_rows.append({"similarity": mname, "label": lname, "within_pairs": nw, "within_minus_between": obs,
                            "null_mean": null.mean(), "null_lo": np.percentile(null, 2.5), "null_hi": np.percentile(null, 97.5),
                            "p_one_sided_higher_within": (1 + np.sum(null >= obs)) / (N_PERM + 1), "permutations": N_PERM,
                            "status": "exploratory"})
        # hint cluster: exact enumeration (any 2 of 20 streams)
        a0, b0 = L.TV.index(L.MAIN), L.TV.index(L.HELDOUT)
        vals = M[iu]
        v0 = M[a0, b0]
        rank = int(np.sum(vals >= v0))
        cl_rows.append({"similarity": mname, "label": "hint ('Tim' = 2019 and 2023 finals; other hints single streams)", "within_pairs": 1,
                        "within_minus_between": v0 - np.mean([v for (a, b), v in zip(zip(*iu), vals) if not (a == a0 and b == b0)]),
                        "null_mean": "", "null_lo": "", "null_hi": "", "p_one_sided_higher_within": rank / len(vals),
                        "permutations": f"exact, {len(vals)} pairs", "status": "exploratory"})
        # Mantel-type correlations
        for vname, D, sign in (("shared players", shared, 1), ("|year difference|", dyear, -1)):
            x, y = D[iu], M[iu]
            r_obs = np.corrcoef(x, y)[0, 1]
            null = np.empty(N_PERM)
            for p in range(N_PERM):
                pi = rng.permutation(n)
                null[p] = np.corrcoef(x, M[np.ix_(pi, pi)][iu])[0, 1]
            p_one = (1 + np.sum(sign * null >= sign * r_obs)) / (N_PERM + 1)
            cl_rows.append({"similarity": mname, "label": f"Mantel r with {vname}", "within_pairs": "", "within_minus_between": r_obs,
                            "null_mean": null.mean(), "null_lo": np.percentile(null, 2.5), "null_hi": np.percentile(null, 97.5),
                            "p_one_sided_higher_within": p_one, "permutations": N_PERM,
                            "status": "exploratory (one-sided: more sharing with more shared players / closer years)"})
        # QAP regression
        same_slam = np.array([[metas[a]["slam"] == metas[b]["slam"] for b in range(n)] for a in range(n)], float)
        same_gender = np.array([[metas[a]["gender"] == metas[b]["gender"] for b in range(n)] for a in range(n)], float)
        same_hint = np.array([[hint[a] == hint[b] for b in range(n)] for a in range(n)], float)
        X = np.column_stack([np.ones(len(iu[0])), same_slam[iu], same_gender[iu], shared[iu], dyear[iu], same_hint[iu]])
        names = ["intercept", "same slam", "same gender", "shared players", "|year difference|", "same hint (2019-2023 only)"]
        beta = np.linalg.lstsq(X, M[iu], rcond=None)[0]
        nullb = np.empty((N_PERM, len(beta)))
        for p in range(N_PERM):
            pi = rng.permutation(n)
            nullb[p] = np.linalg.lstsq(X, M[np.ix_(pi, pi)][iu], rcond=None)[0]
        for k, nm in enumerate(names):
            qap_rows.append({"similarity": mname, "term": nm, "beta": beta[k],
                             "p_two_sided_node_permutation": (1 + np.sum(np.abs(nullb[:, k] - nullb[:, k].mean()) >= abs(beta[k] - nullb[:, k].mean()))) / (N_PERM + 1),
                             "permutations": N_PERM, "status": "exploratory"})
    a0, b0 = L.TV.index(L.MAIN), L.TV.index(L.HELDOUT)
    pair = {}
    for mname, M in mats.items():
        vals = M[iu]
        pair[mname] = {"value": float(M[a0, b0]), "rank_among_190_pairs": int(np.sum(vals > M[a0, b0]) + 1), "n_pairs": int(len(vals)),
                       "mean_all_pairs": float(vals.mean()), "median_all_pairs": float(np.median(vals))}
        order = np.argsort(-vals)[:5]
        pair[mname]["top5_pairs"] = [[L.short(L.TV[iu[0][k]]), L.short(L.TV[iu[1][k]]), float(vals[k])] for k in order]
    L.write_csv(L.RESULTS / "cluster_tests.csv", cl_rows)
    L.write_csv(L.RESULTS / "qap_regression.csv", qap_rows)
    L.write_json(L.RESULTS / "pair_2019_2023.json", pair)
    print("clusters done", round(time.time() - t0, 1), "s", flush=True)
    pool_to_target()
    print("all done", round(time.time() - t0, 1), "s")


# ---------------------------------------------------------------- pool -> target (plan section 8)
def _cov_arrays(utts, F):
    k = len(utts)
    n = np.zeros(k)
    c2 = np.zeros(k)
    c3 = np.zeros(k)
    for j, u in enumerate(utts):
        mx = L.C.cover_a(u, F)
        n[j] = len(u)
        c2[j] = (mx >= 2).sum()
        c3[j] = (mx >= 3).sum()
    return n, c2, c3


def _target_job(args):
    j, tokvar, mode, r = args
    others = [k for k in range(len(TVT)) if k != j and (mode != "pool18" or TVT[k].name.startswith("tv_pool_"))]
    get = (lambda t: t.norm) if tokvar == "norm" else (lambda t: t.raw)
    I = [u for k in others for u in get(TVT[k])]
    if mode == "matched":
        rng = np.random.default_rng([L.SEED, 9, j, r])
        idx = L.subsample(I, I_MATCHED, rng)
        I = [I[i] for i in idx]
    F = L.C.formula_set_fast(I, m=2)
    n, c2, c3 = _cov_arrays(get(TVT[j]), F)
    out = {"target": TVT[j].name, "tokens": tokvar, "mode": mode, "r": r, "I_tokens": sum(len(u) for u in I),
           "M_tokens": int(n.sum()), "base": c2.sum() / n.sum(), "n3": c3.sum() / n.sum()}
    if mode != "matched":
        for key, c in (("base", c2), ("n3", c3)):
            est, lo, hi, _ = L.C.boot_ratio(c, n, B=B, seed=L.SEED + 31 * j + (key == "n3"))
            out[key + "_lo"], out[key + "_hi"] = lo, hi
    return out


def pool_to_target():
    global TVT
    TVT = [L.load_tv(s) for s in L.TV]
    t0 = time.time()
    jobs = [(j, tv, "loo19", 0) for j in range(len(TVT)) for tv in ("raw", "norm")]
    jobs += [(L.TV.index(s), "raw", "pool18", 0) for s in (L.MAIN, L.HELDOUT)]
    jobs += [(j, "raw", "matched", r) for j in range(len(TVT)) for r in range(R_I)]
    with Pool(4) as pool:
        res = pool.map(_target_job, jobs, chunksize=2)
    rows = [r for r in res if r["mode"] != "matched"]
    for j in range(len(TVT)):
        m = [r for r in res if r["mode"] == "matched" and r["target"] == TVT[j].name]
        for key in ("base", "n3"):
            v = np.array([r[key] for r in m])
            rows.append({"target": TVT[j].name, "tokens": "raw", "mode": f"matched I = {I_MATCHED}", "r": len(m),
                         "I_tokens": int(np.mean([r["I_tokens"] for r in m])), "M_tokens": m[0]["M_tokens"], key: v.mean(),
                         key + "_lo": np.percentile(v, 2.5), key + "_hi": np.percentile(v, 97.5)})
    # merge the two matched rows per target
    merged = {}
    out = []
    for r in rows:
        if r["mode"].startswith("matched"):
            k = r["target"]
            merged.setdefault(k, {}).update(r)
        else:
            out.append(r)
    out += list(merged.values())
    for r in out:
        r["label"] = L.short(r["target"])
    L.write_csv(L.RESULTS / "pool_to_target.csv", out,
                ["target", "label", "tokens", "mode", "r", "I_tokens", "M_tokens", "base", "base_lo", "base_hi", "n3", "n3_lo", "n3_hi"])
    loo = {r["target"]: r for r in out if r["mode"] == "loo19" and r["tokens"] == "raw"}
    vals = sorted(((r["base"], t) for t, r in loo.items()), reverse=True)
    rank = [t for _, t in vals].index(L.MAIN) + 1
    mat = {r["target"]: r for r in out if r["mode"].startswith("matched")}
    mvals = sorted(((r["base"], t) for t, r in mat.items()), reverse=True)
    meta = {"rank_2019_loo19_raw_base": rank, "n_targets": len(loo),
            "median_loo19_raw_base": float(np.median([r["base"] for r in loo.values()])),
            "range_loo19_raw_base": [float(min(r["base"] for r in loo.values())), float(max(r["base"] for r in loo.values()))],
            "rank_2019_matched_raw_base": [t for _, t in mvals].index(L.MAIN) + 1,
            "median_matched_raw_base": float(np.median([r["base"] for r in mat.values()])),
            "check_phase2_pool18_2019_raw_base": [r["base"] for r in out if r["mode"] == "pool18" and r["target"] == L.MAIN][0],
            "runtime_s": round(time.time() - t0, 1), "B": B, "R_matched": R_I}
    L.write_json(L.RESULTS / "pool_to_target_meta.json", meta)


if __name__ == "__main__":
    main()
