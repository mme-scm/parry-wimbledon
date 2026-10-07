"""REVISION 1 (plan.md addendum 2; post hoc, exploratory): power and minimum detectable effects (MDE) of the timing tests
C3a/C3b (R3a/R3b), C4 (R4) and C5 (R5), and circular-shift nulls that respect serial correlation for C3 and C5.

MDE = the smallest simulated effect that the test, as run in f03/f06 (same statistic, same permutation scheme, same N),
rejects with probability >= 0.80; linear interpolation between grid points. Simulations start from the observed data with the
real association destroyed (labels permuted or values re-drawn), then inject an effect of known size:
  C3 (coverage, shortest vs longest tercile): T1/T3 labels are randomly reassigned (sizes kept); each uncovered token of a T1
     utterance becomes covered with probability q = delta / (1 - d_T1), so the expected T1-minus-T3 difference is delta (pp).
     Two-sided label-permutation test (999 permutations).
  C4 (thrift D): within each player x slot stratum, each reference takes, with probability theta, a context-specific
     "designated" expression (the stratum's k-th most frequent type for tercile k, k mod the number of types, at most 3),
     otherwise a draw from the stratum's observed expression distribution. theta = share of references whose form is fixed
     by the time context. One-sided within-stratum permutation test (499 permutations). Mean Cramer's V (context x
     expression, within strata, token-weighted) of the simulated data is reported to translate theta.
  C5 (Spearman rho, syllables vs dead time): within each player, the observed syllable values are reassigned in the order
     of a latent z = r * standardised rank(time) + sqrt(1 - r^2) * N(0, 1) (marginals and ties kept). The MDE is stated as the
     mean achieved Spearman rho at 80% power (ties attenuate it below r). Two-sided within-player permutation test (999).
alpha = 0.05 (unadjusted) and the Bonferroni level alpha/m (m = 6 for 2019, 5 for 2023), the most stringent Holm step.
C4/C5 use the commentary-only token set (umpire-pattern references excluded; f06), as the revised confirmatory tests.

Outputs: results/power_curves.csv, results/mde_summary.json, results/circular_shift_tests.json
Run: python -I analysis/formulas/f09_power.py
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import csv
import json
import time
from multiprocessing import Pool
import numpy as np
from scipy.stats import rankdata
import common as C

ALPHA = 0.05
M_FAMILY = {C.MAIN: 6, C.HELDOUT: 5}
NSIM = 400
P_C3, P_C4, P_C5 = 999, 499, 999
GRID_C3 = [0.0, 0.01, 0.02, 0.03, 0.04, 0.05, 0.06, 0.07, 0.08, 0.09, 0.10, 0.12, 0.14, 0.16]
GRID_C4 = [0.0, 0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.4, 0.5, 0.6, 0.8, 1.0]
GRID_C5 = [0.0, 0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.5, 0.6]
SHIFT_MIN = 10  # circular shifts closer than this many utterances to 0 are excluded


# ---------------------------------------------------------------- C3
def c3_data(stream):
    recs = C.load_stream(stream)
    C.add_contexts(recs, stream)
    name = "pool_to_2019" if stream == C.MAIN else "pool_to_2023"
    with open(C.RESULTS / f"utt_coverage_{name}.csv") as fh:
        cov = {r["utt_id"]: (int(r["tokens"]), int(r["covered_a"])) for r in csv.DictReader(fh)}
    n = np.array([cov[r["utt_id"]][0] for r in recs])
    c = np.array([cov[r["utt_id"]][1] for r in recs])
    return recs, n, c


def diff13(c, n, is1):
    return c[is1].sum() / n[is1].sum() - c[~is1].sum() / n[~is1].sum()


def perm_p_two(c, n, is1, rng, P):
    L = rng.permuted(np.tile(is1, (P, 1)), axis=1)
    c1, n1 = L @ c, L @ n
    null = c1 / n1 - (c.sum() - c1) / (n.sum() - n1)
    obs = diff13(c, n, is1)
    return (1 + np.sum(np.abs(null) >= abs(obs) - 1e-12)) / (1 + P), null


def _c3_job(args):
    stream, field, delta, seed = args
    recs, n_all, c_all = c3_data(stream)
    lab = np.array([r[field] for r in recs])
    sel = np.where((lab == "T1") | (lab == "T3"))[0]
    n, c0 = n_all[sel].astype(float), c_all[sel].astype(np.int64)
    is1_obs = lab[sel] == "T1"
    rng = np.random.default_rng(seed)
    rej, rej_b, effs = 0, 0, []
    for _ in range(NSIM):
        is1 = rng.permutation(is1_obs)
        d1 = c0[is1].sum() / n[is1].sum()
        q = min(1.0, delta / (1 - d1)) if delta > 0 else 0.0
        c = c0.copy()
        if q > 0:
            c[is1] = c0[is1] + rng.binomial((n[is1] - c0[is1]).astype(np.int64), q)
        p, _ = perm_p_two(c.astype(float), n, is1, rng, P_C3)
        rej += p <= ALPHA
        rej_b += p <= ALPHA / M_FAMILY[stream]
        effs.append(diff13(c, n, is1))
    return {"test": "C3", "stream": stream, "context": field, "effect_param": delta, "power": rej / NSIM,
            "power_bonferroni": rej_b / NSIM, "mean_achieved_effect": float(np.mean(effs)), "nsim": NSIM, "nperm": P_C3}


def c3_circular(stream, field):
    recs, n, c = c3_data(stream)
    lab = np.array([r[field] for r in recs])
    N = len(lab)

    def stat(lb):
        s1, s3 = lb == "T1", lb == "T3"
        return c[s1].sum() / n[s1].sum() - c[s3].sum() / n[s3].sum()
    obs = stat(lab)
    null = np.array([stat(np.roll(lab, k)) for k in range(SHIFT_MIN, N - SHIFT_MIN + 1)])
    p = (1 + np.sum(np.abs(null) >= abs(obs) - 1e-12)) / (1 + len(null))
    rng = np.random.default_rng(C.MASTER_SEED + 9)
    s13 = np.where((lab == "T1") | (lab == "T3"))[0]
    pl, null_perm = perm_p_two(c[s13].astype(float), n[s13].astype(float), lab[s13] == "T1", rng, 9999)
    return {"stream": stream, "context": field, "observed_diff_T1_minus_T3": float(obs), "n_shifts": int(len(null)),
            "shift_null_lo": float(np.percentile(null, 2.5)), "shift_null_hi": float(np.percentile(null, 97.5)),
            "p_two_sided_circular_shift": float(p), "p_two_sided_label_permutation_9999": float(pl),
            "label_permutation_null_sd": float(null_perm.std()), "shift_null_sd": float(null.std())}


# ---------------------------------------------------------------- C4 / C5 data (commentary-only reference tokens)
def ref_tokens(stream):
    with open(C.RESULTS / f"refexpr_tokens_{stream}.csv") as fh:
        rows = [r for r in csv.DictReader(fh) if not r.get("umpire_pattern")]
    for r in rows:
        r["syllables"] = int(r["syllables"])
        for k in ("dead_time_before_s",):
            r[k] = float(r[k]) if r[k] not in ("", "None") else None
    return rows


def c4_arrays(stream):
    rows = [r for r in ref_tokens(stream) if r["dtb_terc"] != "NA"]
    st_ids = {s: i for i, s in enumerate(sorted({(r["player"], r["slot"]) for r in rows}))}
    ex_ids = {e: i for i, e in enumerate(sorted({r["expression"] for r in rows}))}
    cx_ids = {"T1": 0, "T2": 1, "T3": 2}
    strata = np.array([st_ids[(r["player"], r["slot"])] for r in rows])
    expr = np.array([ex_ids[r["expression"]] for r in rows])
    ctx = np.array([cx_ids[r["dtb_terc"]] for r in rows])
    return strata, expr, ctx


def D_rows(strata, exprM, ctxM):
    key = (strata[None, :].astype(np.int64) * 1000 + ctxM) * 1000 + exprM
    sk = np.sort(key, axis=1)
    return 1 + (np.diff(sk, axis=1) != 0).sum(1)


def within_strata_perm(strata, x, rng, P):
    """P copies of x, each permuted within strata."""
    N = len(x)
    order0 = np.argsort(strata, kind="stable")
    keys = strata[None, :] + rng.random((P, N))
    idx = np.argsort(keys, axis=1)
    out = np.empty((P, N), dtype=x.dtype)
    out[:, order0] = x[idx]
    return out


def cramers_v_within(strata, expr, ctx):
    num, den = 0.0, 0
    for s in np.unique(strata):
        g = strata == s
        e, c = expr[g], ctx[g]
        ue, uc = np.unique(e), np.unique(c)
        if len(ue) < 2 or len(uc) < 2:
            continue
        tab = np.zeros((len(ue), len(uc)))
        for a, b in zip(np.searchsorted(ue, e), np.searchsorted(uc, c)):
            tab[a, b] += 1
        n = tab.sum()
        expct = tab.sum(1, keepdims=True) * tab.sum(0, keepdims=True) / n
        chi2 = ((tab - expct) ** 2 / expct).sum()
        v = np.sqrt(chi2 / (n * (min(tab.shape) - 1)))
        num += v * n
        den += n
    return num / den if den else float("nan")


def _c4_job(args):
    stream, theta, seed = args
    strata, expr_obs, ctx = c4_arrays(stream)
    rng = np.random.default_rng(seed)
    designated = {}
    pools = {}
    for s in np.unique(strata):
        e = expr_obs[strata == s]
        vals, cnt = np.unique(e, return_counts=True)
        order = vals[np.lexsort((vals, -cnt))]
        K = min(3, len(order))
        for k in range(3):
            designated[(s, k)] = order[k % K]
        pools[s] = e
    rej, rej_b, vs, red = 0, 0, [], []
    for _ in range(NSIM):
        expr = np.empty_like(expr_obs)
        for s in np.unique(strata):
            g = np.where(strata == s)[0]
            expr[g] = pools[s][rng.integers(0, len(pools[s]), len(g))]
        if theta > 0:
            hit = rng.random(len(expr)) < theta
            for i in np.where(hit)[0]:
                expr[i] = designated[(strata[i], ctx[i])]
        Dobs = D_rows(strata, expr[None, :], ctx[None, :])[0]
        ctxP = within_strata_perm(strata, ctx, rng, P_C4)
        null = D_rows(strata, np.broadcast_to(expr, ctxP.shape), ctxP)
        p = (1 + np.sum(null <= Dobs)) / (1 + P_C4)
        rej += p <= ALPHA
        rej_b += p <= ALPHA / M_FAMILY[stream]
        vs.append(cramers_v_within(strata, expr, ctx))
        red.append(null.mean() - Dobs)
    return {"test": "C4", "stream": stream, "context": "dtb_terc", "effect_param": theta, "power": rej / NSIM,
            "power_bonferroni": rej_b / NSIM, "mean_achieved_effect": float(np.mean(vs)),
            "mean_D_reduction_vs_null": float(np.mean(red)), "nsim": NSIM, "nperm": P_C4}


def c5_arrays(stream):
    rows = [r for r in ref_tokens(stream) if r["dead_time_before_s"] is not None]
    syl = np.array([r["syllables"] for r in rows], float)
    tv = np.array([r["dead_time_before_s"] for r in rows], float)
    pl = np.array([r["player"] for r in rows])
    utt = [r["utt_id"] for r in rows]
    return syl, tv, pl, utt


def rho_perm_null(rs, rt, groups, rng, P):
    rs_c = rs - rs.mean()
    rt_c = rt - rt.mean()
    den = np.sqrt((rs_c ** 2).sum() * (rt_c ** 2).sum())
    M = within_strata_perm(groups, rt_c, rng, P)
    return (M @ rs_c) / den, float(rs_c @ rt_c / den)


def _c5_job(args):
    stream, r, seed = args
    syl, tv, pl, _ = c5_arrays(stream)
    gid = np.unique(pl, return_inverse=True)[1]
    rt = rankdata(tv)
    rng = np.random.default_rng(seed)
    rej, rej_b, rhos = 0, 0, []
    for _ in range(NSIM):
        s2 = np.empty_like(syl)
        for g in np.unique(gid):
            ix = np.where(gid == g)[0]
            zt = rankdata(tv[ix])
            zt = (zt - zt.mean()) / zt.std()
            z = r * zt + np.sqrt(1 - r * r) * rng.standard_normal(len(ix))
            s2[ix[np.argsort(z)]] = np.sort(syl[ix])
        rs = rankdata(s2)
        null, obs = rho_perm_null(rs, rt, gid, rng, P_C5)
        p = (1 + np.sum(np.abs(null) >= abs(obs) - 1e-12)) / (1 + P_C5)
        rej += p <= ALPHA
        rej_b += p <= ALPHA / M_FAMILY[stream]
        rhos.append(obs)
    return {"test": "C5", "stream": stream, "context": "dead_time_before_s", "effect_param": r, "power": rej / NSIM,
            "power_bonferroni": rej_b / NSIM, "mean_achieved_effect": float(np.mean(rhos)), "nsim": NSIM, "nperm": P_C5}


def c5_circular(stream):
    rows = [r for r in ref_tokens(stream)]
    recs = C.load_stream(stream)
    C.add_contexts(recs, stream)
    uorder = [r["utt_id"] for r in recs]
    utime = np.array([np.nan if r["ctx_dt_before"] is None else r["ctx_dt_before"] for r in recs])
    upos = {u: i for i, u in enumerate(uorder)}
    tpos = np.array([upos[r["utt_id"]] for r in rows])
    syl = np.array([r["syllables"] for r in rows], float)

    def stat(ut):
        t = ut[tpos]
        ok = ~np.isnan(t)
        a, b = rankdata(syl[ok]), rankdata(t[ok])
        return float(np.corrcoef(a, b)[0, 1])
    obs = stat(utime)
    N = len(uorder)
    null = np.array([stat(np.roll(utime, k)) for k in range(SHIFT_MIN, N - SHIFT_MIN + 1)])
    p = (1 + np.sum(np.abs(null) >= abs(obs) - 1e-12)) / (1 + len(null))
    return {"stream": stream, "observed_rho": obs, "n_shifts": int(len(null)), "shift_null_lo": float(np.percentile(null, 2.5)),
            "shift_null_hi": float(np.percentile(null, 97.5)), "p_two_sided_circular_shift": float(p)}


def mde(curve, key="power"):
    """Linear interpolation of the effect parameter (and achieved effect) at power 0.80; None if never reached."""
    pts = sorted(curve, key=lambda x: x["effect_param"])
    for a, b in zip(pts, pts[1:]):
        if a[key] < 0.8 <= b[key]:
            w = (0.8 - a[key]) / (b[key] - a[key])
            return (a["effect_param"] + w * (b["effect_param"] - a["effect_param"]),
                    a["mean_achieved_effect"] + w * (b["mean_achieved_effect"] - a["mean_achieved_effect"]))
    if pts and pts[0][key] >= 0.8:
        return pts[0]["effect_param"], pts[0]["mean_achieved_effect"]
    return None, None


def main():
    t0 = time.time()
    jobs3, jobs4, jobs5 = [], [], []
    for si, stream in enumerate((C.MAIN, C.HELDOUT)):
        for fi, field in enumerate(("ctx_dtb_terc", "ctx_ta_terc")):
            for k, d in enumerate(GRID_C3):
                jobs3.append((stream, field, d, C.MASTER_SEED + 3_000_000 + 100_000 * si + 10_000 * fi + k))
        for k, th in enumerate(GRID_C4):
            jobs4.append((stream, th, C.MASTER_SEED + 4_000_000 + 100_000 * si + k))
        for k, r in enumerate(GRID_C5):
            jobs5.append((stream, r, C.MASTER_SEED + 5_000_000 + 100_000 * si + k))
    with Pool(4) as pool:
        res = pool.map(_c3_job, jobs3, chunksize=1) + pool.map(_c4_job, jobs4, chunksize=1) + pool.map(_c5_job, jobs5, chunksize=1)
    fields = ["test", "stream", "context", "effect_param", "power", "power_bonferroni", "mean_achieved_effect",
              "mean_D_reduction_vs_null", "nsim", "nperm"]
    with open(C.RESULTS / "power_curves.csv", "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=fields)
        w.writeheader()
        for r in res:
            w.writerow({k: (f"{r[k]:.6f}" if isinstance(r.get(k), float) else r.get(k, "")) for k in fields})
    summ = {}
    names = {(C.MAIN, "C3", "ctx_dtb_terc"): "C3a", (C.MAIN, "C3", "ctx_ta_terc"): "C3b", (C.HELDOUT, "C3", "ctx_dtb_terc"): "R3a",
             (C.HELDOUT, "C3", "ctx_ta_terc"): "R3b", (C.MAIN, "C4", "dtb_terc"): "C4", (C.HELDOUT, "C4", "dtb_terc"): "R4",
             (C.MAIN, "C5", "dead_time_before_s"): "C5", (C.HELDOUT, "C5", "dead_time_before_s"): "R5"}
    for (stream, test, ctx), tid in names.items():
        curve = [r for r in res if r["stream"] == stream and r["test"] == test and r["context"] == ctx]
        p0 = next(r for r in curve if r["effect_param"] == 0.0)
        e, a = mde(curve)
        eb, ab = mde(curve, "power_bonferroni")
        dred = None
        if test == "C4" and e is not None:
            lo_ = max([r for r in curve if r["effect_param"] <= e], key=lambda r: r["effect_param"])
            hi_ = min([r for r in curve if r["effect_param"] >= e], key=lambda r: r["effect_param"])
            w_ = 0.0 if hi_["effect_param"] == lo_["effect_param"] else (e - lo_["effect_param"]) / (hi_["effect_param"] - lo_["effect_param"])
            dred = lo_["mean_D_reduction_vs_null"] + w_ * (hi_["mean_D_reduction_vs_null"] - lo_["mean_D_reduction_vs_null"])
        summ[tid] = {"stream": stream, "context": ctx, "type_I_error_at_zero_effect": p0["power"],
                     "achieved_effect_at_zero": p0["mean_achieved_effect"], "mde_D_reduction_vs_null_alpha05": dred,
                     "mde_param_alpha05": e, "mde_achieved_alpha05": a,
                     "mde_param_bonferroni": eb, "mde_achieved_bonferroni": ab, "alpha_bonferroni": ALPHA / M_FAMILY[stream],
                     "effect_scale": {"C3": "difference in coverage share, shortest minus longest tercile (pp/100)",
                                      "C4": "theta = share of references whose form is fixed by the tercile; achieved = mean Cramer's V",
                                      "C5": "latent r; achieved = mean Spearman rho"}[test]}
    circ = {"shift_min": SHIFT_MIN}
    for stream in (C.MAIN, C.HELDOUT):
        for field in ("ctx_dtb_terc", "ctx_ta_terc"):
            circ[f"{stream}:{field}"] = c3_circular(stream, field)
        circ[f"{stream}:C5_dead_time_before_s"] = c5_circular(stream)
    # observed effect-size translations (real data, commentary-only tokens)
    for stream, tid in ((C.MAIN, "C4"), (C.HELDOUT, "R4")):
        s, e, c = c4_arrays(stream)
        summ[tid]["observed_cramers_v_within_strata"] = cramers_v_within(s, e, c)
    summ["runtime_seconds"] = time.time() - t0
    summ["nsim"] = NSIM
    summ["nperm"] = {"C3": P_C3, "C4": P_C4, "C5": P_C5}
    C.write_json(C.RESULTS / "mde_summary.json", summ)
    C.write_json(C.RESULTS / "circular_shift_tests.json", circ)
    for k, v in summ.items():
        print(k, v)
    for k, v in circ.items():
        print(k, v)


if __name__ == "__main__":
    main()
