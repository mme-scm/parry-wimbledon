"""Confirmatory tests T1-T4, secondary OLS slope, descriptive T5, robustness R1-R6 (plan sections 4-7).

Outputs (results/): confirmatory_<tag>.csv, robustness_<tag>.csv, t5_<tag>.json, details_<tag>.json, nulls_<tag>.npz,
verdict.json.
"""
import json
import sys
import warnings
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import rankdata

sys.path.insert(0, str(Path(__file__).resolve().parent))
from metre_lib import (RES, SEED, TAGS, block_bootstrap_indices, holm, pearson_rows, spearman_rows,  # noqa: E402
                       timing_sequence, two_sided_p)

B = 10_000
L_BLOCK = 10
K_MIN = 10
CAT = {"within_game": 0, "changeover": 1, "other_game_end": 2}
warnings.filterwarnings("ignore", category=RuntimeWarning)


# ---------------------------------------------------------------- statistics (vectorised over rows = shifts / resamples)
def stat_T1(words, A2):
    return spearman_rows(np.broadcast_to(words, A2.shape), A2)


def stat_ols(words, A2):
    W = np.broadcast_to(words, A2.shape)
    Ac = A2 - A2.mean(1, keepdims=True)
    Wc = W - W.mean(1, keepdims=True)
    return (Ac * Wc).sum(1) / (Ac ** 2).sum(1)


def tercile_masks(A2):
    q1 = np.quantile(A2, 1 / 3, axis=1, keepdims=True)
    q2 = np.quantile(A2, 2 / 3, axis=1, keepdims=True)
    return A2 <= q1, A2 > q2


def shares_T2(tok, cov, A2):
    tok = np.broadcast_to(tok, A2.shape)
    cov = np.broadcast_to(cov, A2.shape)
    s, l = tercile_masks(A2)
    sh_s = (cov * s).sum(1) / (tok * s).sum(1)
    sh_l = (cov * l).sum(1) / (tok * l).sum(1)
    return sh_s, sh_l


def stat_T2(tok, cov, A2):
    a, b = shares_T2(tok, cov, A2)
    return a - b


def shares_T4(tok, cov, C2):
    tok = np.broadcast_to(tok, C2.shape)
    cov = np.broadcast_to(cov, C2.shape)
    w, c = C2 == 0, C2 == 1
    return (cov * w).sum(1) / (tok * w).sum(1), (cov * c).sum(1) / (tok * c).sum(1)


def stat_T4(tok, cov, C2):
    a, b = shares_T4(tok, cov, C2)
    return a - b


def stat_T3(syll, s_unit, A2, chunk=1500):
    out = np.empty(A2.shape[0])
    rs = rankdata(syll)
    for i in range(0, A2.shape[0], chunk):
        Astr = A2[i:i + chunk][:, s_unit]
        out[i:i + chunk] = pearson_rows(np.broadcast_to(rs, Astr.shape), rankdata(Astr, axis=1))
    return out


def partial_spearman_rows(syll, s_unit, ntok_unit, A2, chunk=1500):
    """R4: Spearman of syllables and A, both rank-residualised on the unit token count."""
    rs = rankdata(syll)
    rt = rankdata(ntok_unit[s_unit])
    X = np.column_stack([np.ones_like(rt), rt])
    beta = np.linalg.lstsq(X, rs, rcond=None)[0]
    es = rs - X @ beta
    out = np.empty(A2.shape[0])
    proj = np.linalg.pinv(X)
    for i in range(0, A2.shape[0], chunk):
        ra = rankdata(A2[i:i + chunk][:, s_unit], axis=1)
        ea = ra - (ra @ proj.T) @ X.T
        out[i:i + chunk] = pearson_rows(np.broadcast_to(es, ea.shape), ea)
    return out


# ---------------------------------------------------------------- nulls
def index_shift_matrix(cycles, M, kmin=K_MIN):
    ks = np.arange(kmin, M - kmin + 1)
    return (cycles[None, :] + ks[:, None]) % M


def time_shift_matrix(t_units, t_seq, t_end, smin=300):
    t0 = t_seq[0]
    T = t_end - t0
    ss = np.arange(smin, int(np.floor(T)) - smin + 1)
    tau = t0 + np.mod(t_units[None, :] - t0 + ss[:, None], T)
    return np.searchsorted(t_seq, tau, side="right") - 1


def boot_T3(syll, s_unit, n_units, idx, A, ntok=None):
    """Bootstrap T3 (and R4 if ntok given): resample units, carry their strings."""
    order = np.argsort(s_unit, kind="stable")
    syll_o, unit_o = syll[order], s_unit[order]
    starts = np.searchsorted(unit_o, np.arange(n_units), "left")
    ends = np.searchsorted(unit_o, np.arange(n_units), "right")
    out = np.empty(idx.shape[0])
    for b in range(idx.shape[0]):
        parts = [np.arange(starts[u], ends[u]) for u in idx[b]]
        sel = np.concatenate(parts) if parts else np.array([], int)
        sel_units = np.repeat(idx[b], ends[idx[b]] - starts[idx[b]])
        if len(sel) < 3:
            out[b] = np.nan
            continue
        sy = syll_o[sel]
        a = A[sel_units]
        if ntok is None:
            out[b] = np.corrcoef(rankdata(sy), rankdata(a))[0, 1]
        else:
            rt = rankdata(ntok[sel_units])
            X = np.column_stack([np.ones_like(rt), rt])
            es = rankdata(sy) - X @ np.linalg.lstsq(X, rankdata(sy), rcond=None)[0]
            ra = rankdata(a)
            ea = ra - X @ np.linalg.lstsq(X, ra, rcond=None)[0]
            out[b] = np.corrcoef(es, ea)[0, 1]
    return out


def ci(x):
    x = np.asarray(x)
    x = x[~np.isnan(x)]
    return [float(np.quantile(x, 0.025)), float(np.quantile(x, 0.975))]


def rnd(x, k=4):
    return None if x is None or (isinstance(x, float) and np.isnan(x)) else round(float(x), k)


# ---------------------------------------------------------------- per match
def run_match(tag):
    U = pd.read_csv(RES / f"units_{tag}.csv").sort_values("point_idx").reset_index(drop=True)
    S = pd.read_csv(RES / f"strings_{tag}.csv")
    C, t_end = timing_sequence(tag)
    A_seq = C.A.to_numpy(float)
    cat_seq = C.category.map(CAT).to_numpy()
    t_seq = C.elapsed_s.to_numpy(float)
    M = len(C)
    pos = {p: i for i, p in enumerate(U.point_idx)}
    n = len(U)

    def unit_arrays(Usub, variant):
        return (Usub[f"n_tok_{variant}"].to_numpy(float), Usub[f"n_cov_{variant}"].to_numpy(float))

    def strings_of(Usub, variant):
        loc = {p: i for i, p in enumerate(Usub.point_idx)}
        s = S[(S.variant == variant) & S.point_idx.isin(loc)]
        return s.syll.to_numpy(float), s.point_idx.map(loc).to_numpy()

    def evaluate(Usub, variant="base", predictor="A", null="index", tests=("T1", "T2", "T3", "T4"), seed=SEED):
        """Observed statistic, block-bootstrap CI and shift-null p for the requested tests on a unit subset."""
        nn = len(Usub)
        cyc = Usub.cyc.to_numpy()
        if predictor == "A":
            A_obs = Usub.A.to_numpy(float)
            C_obs = Usub.category.map(CAT).to_numpy()
            if null == "index":
                Ish = index_shift_matrix(cyc, M)
            else:
                Ish = time_shift_matrix(Usub.elapsed_s.to_numpy(float), t_seq, t_end)
            A_null, C_null = A_seq[Ish], cat_seq[Ish]
        else:  # R3: D, shifted within the unit sequence
            A_obs = Usub.D.to_numpy(float)
            C_obs = Usub.category.map(CAT).to_numpy()
            Ish = index_shift_matrix(np.arange(nn), nn)
            A_null, C_null = A_obs[Ish], C_obs[Ish]
        words = Usub.words.to_numpy(float)
        tok, cov = unit_arrays(Usub, variant)
        syll, s_unit = strings_of(Usub, variant)
        idx = block_bootstrap_indices(nn, B, L_BLOCK, seed)
        res = {}
        for t in tests:
            if t == "T1":
                obs = stat_T1(words, A_obs[None, :])[0]
                nul = stat_T1(words, A_null)
                bt = spearman_rows(words[idx], A_obs[idx])
                extra = {}
            elif t == "OLS":
                obs = stat_ols(words, A_obs[None, :])[0]
                nul = stat_ols(words, A_null)
                Ab, Wb = A_obs[idx], words[idx]
                Ac = Ab - Ab.mean(1, keepdims=True)
                bt = (Ac * (Wb - Wb.mean(1, keepdims=True))).sum(1) / (Ac ** 2).sum(1)
                extra = {}
            elif t == "T2":
                obs = stat_T2(tok, cov, A_obs[None, :])[0]
                nul = stat_T2(tok, cov, A_null)
                sh_s, sh_l = shares_T2(tok[idx], cov[idx], A_obs[idx])
                bt = sh_s - sh_l
                o_s, o_l = shares_T2(tok, cov, A_obs[None, :])
                s_m, l_m = tercile_masks(A_obs[None, :])
                extra = {"share_short": rnd(o_s[0]), "share_short_ci": [rnd(v) for v in ci(sh_s)],
                         "share_long": rnd(o_l[0]), "share_long_ci": [rnd(v) for v in ci(sh_l)],
                         "n_units_short": int(s_m.sum()), "n_units_long": int(l_m.sum()),
                         "tokens_short": int(tok[s_m[0]].sum()), "tokens_long": int(tok[l_m[0]].sum()),
                         "A_cut_1_3": rnd(np.quantile(A_obs, 1 / 3), 2), "A_cut_2_3": rnd(np.quantile(A_obs, 2 / 3), 2)}
            elif t == "T3":
                if len(syll) < 3:
                    continue
                obs = stat_T3(syll, s_unit, A_obs[None, :])[0]
                nul = stat_T3(syll, s_unit, A_null)
                bt = boot_T3(syll, s_unit, nn, idx, A_obs)
                extra = {"n_strings": int(len(syll)), "mean_syll": rnd(syll.mean(), 3),
                         "median_syll": rnd(np.median(syll), 2)}
            elif t == "R4":
                ntok_u = tok
                obs = partial_spearman_rows(syll, s_unit, ntok_u, A_obs[None, :])[0]
                nul = partial_spearman_rows(syll, s_unit, ntok_u, A_null)
                bt = boot_T3(syll, s_unit, nn, idx, A_obs, ntok=ntok_u)
                extra = {"n_strings": int(len(syll))}
            elif t == "T4":
                n_chg = int((C_obs == 1).sum())
                if n_chg < 15:
                    res[t] = {"testable": False, "n_changeover_units": n_chg}
                    continue
                obs = stat_T4(tok, cov, C_obs[None, :])[0]
                nul = stat_T4(tok, cov, C_null)
                w_b, c_b = shares_T4(tok[idx], cov[idx], C_obs[idx])
                bt = w_b - c_b
                o_w, o_c = shares_T4(tok, cov, C_obs[None, :])
                extra = {"share_within_game": rnd(o_w[0]), "share_within_ci": [rnd(v) for v in ci(w_b)],
                         "share_changeover": rnd(o_c[0]), "share_changeover_ci": [rnd(v) for v in ci(c_b)],
                         "n_units_within": int((C_obs == 0).sum()), "n_units_changeover": n_chg,
                         "tokens_within": int(tok[C_obs == 0].sum()), "tokens_changeover": int(tok[C_obs == 1].sum())}
            p, K = two_sided_p(obs, nul)
            lo, hi = ci(bt)
            res[t] = {"testable": True, "estimate": rnd(obs), "ci_lo": rnd(lo), "ci_hi": rnd(hi), "p_shift": rnd(p, 5),
                      "n_shifts": int(K), "null_mean": rnd(np.nanmean(nul)), "null_sd": rnd(np.nanstd(nul)),
                      "n_units": int(nn), **extra, "_null": nul}
        return res

    # ---- primary
    prim = evaluate(U, tests=("T1", "OLS", "T2", "T3", "T4"))
    fam = [t for t in ("T1", "T2", "T3", "T4") if prim.get(t, {}).get("testable")]
    padj = holm([prim[t]["p_shift"] for t in fam])
    rows = []
    preds = {"T1": "P1 words increase with A", "T2": "P2 share(short A) - share(long A) > 0",
             "T3": "P3 formula syllables increase with A", "T4": "P4 share(within game) - share(changeover) > 0"}
    stats = {"T1": "Spearman rho(words, A)", "T2": "difference in formula share (short - long tercile)",
             "T3": "Spearman rho(string syllables, A)", "T4": "difference in formula share (within - changeover)"}
    for t in ("T1", "T2", "T3", "T4"):
        r = prim.get(t, {"testable": False})
        if not r.get("testable"):
            rows.append({"test": t, "prediction": preds[t], "statistic": stats[t], "testable": False,
                         "note": f"not testable: {r.get('n_changeover_units', 'n/a')} changeover units after exclusions (< 15)"})
            continue
        j = fam.index(t)
        rows.append({"test": t, "prediction": preds[t], "statistic": stats[t], "testable": True,
                     "n_units": r["n_units"], "n_strings": r.get("n_strings"), "estimate": r["estimate"],
                     "ci_lo": r["ci_lo"], "ci_hi": r["ci_hi"], "p_shift": r["p_shift"], "n_shifts": r["n_shifts"],
                     "p_holm": rnd(padj[j], 5), "significant_holm": bool(padj[j] < 0.05),
                     "direction_as_H1": bool(r["estimate"] > 0), "note": ""})
    pd.DataFrame(rows).to_csv(RES / f"confirmatory_{tag}.csv", index=False)

    # ---- robustness
    rob = []

    def add(check, res, note=""):
        for t, r in res.items():
            if not r.get("testable", True):
                rob.append({"check": check, "test": t, "testable": False, "note": f"{r.get('n_changeover_units')} changeover units"})
                continue
            rob.append({"check": check, "test": t, "testable": True, "n_units": r["n_units"],
                        "n_strings": r.get("n_strings"), "estimate": r["estimate"], "ci_lo": r["ci_lo"],
                        "ci_hi": r["ci_hi"], "p_shift": r["p_shift"], "n_shifts": r["n_shifts"],
                        "ci_excludes_0": bool(r["ci_lo"] > 0 or r["ci_hi"] < 0), "note": note})
    r1 = evaluate(U, variant="R1", tests=("T2", "T3", "T4"))
    add("R1 score-call tokens removed", r1)
    add("R2 strict formulas (n>=3, count>=5, streams>=3)", evaluate(U, variant="R2", tests=("T2", "T3", "T4")))
    UD = U[U.D > 0].reset_index(drop=True)
    add("R3 predictor D (last hit to next serve), unit-sequence shift", evaluate(UD, predictor="D", tests=("T1", "T2", "T3")))
    add("R4 T3 partial Spearman controlling unit token count", {"T3": evaluate(U, tests=("R4",))["R4"]})
    U5 = U[~U.repeat_involved].reset_index(drop=True)
    add("R5 units in cross-point exact repeats excluded", evaluate(U5, tests=("T1", "T2", "T3", "T4")))
    r6 = evaluate(U, null="time", tests=("T1", "T2", "T3", "T4"))
    add("R6 continuous time-shift null (1-s steps)", r6)
    pd.DataFrame(rob).to_csv(RES / f"robustness_{tag}.csv", index=False)

    # ---- T5 descriptive: rate ceiling
    A = U.A.to_numpy(float)
    words = U.words.to_numpy(float)
    rate = words / A
    idx = block_bootstrap_indices(n, B, L_BLOCK, SEED)

    def q90_ratio(A2, R2):
        s, l = tercile_masks(A2)
        qs = np.array([np.quantile(R2[i][s[i]], 0.9) for i in range(A2.shape[0])])
        ql = np.array([np.quantile(R2[i][l[i]], 0.9) for i in range(A2.shape[0])])
        return qs, ql
    qs, ql = q90_ratio(A[None, :], rate[None, :])
    bqs, bql = q90_ratio(A[idx], rate[idx])
    logratio_b = np.log(bql / bqs)
    lr_ci = ci(logratio_b)
    bound = np.log(1.5)
    if lr_ci[0] > -bound and lr_ci[1] < bound:
        decision = "flat ceiling (CI inside +-log 1.5)"
    elif lr_ci[1] < 0:
        decision = "ceiling falls with available time"
    else:
        decision = "inconclusive"
    import statsmodels.api as sm
    X = sm.add_constant(A)
    qr = sm.QuantReg(words, X).fit(q=0.9, max_iter=5000)
    bcoef = []
    n_warn = 0
    for b in range(B):
        ii = idx[b]
        with warnings.catch_warnings(record=True) as wlist:
            warnings.simplefilter("always")
            try:
                fb = sm.QuantReg(words[ii], X[ii]).fit(q=0.9, max_iter=2000)
                bcoef.append(fb.params)
            except Exception:
                bcoef.append([np.nan, np.nan])
            n_warn += int(len(wlist) > 0)
    bcoef = np.array(bcoef)
    t5 = {"n_units": n, "rate_words_per_s": {"median": rnd(np.median(rate)), "q90": rnd(np.quantile(rate, 0.9)),
                                             "max": rnd(rate.max()), "mean": rnd(rate.mean())},
          "q90_rate_short_tercile": rnd(qs[0]), "q90_rate_short_ci": [rnd(v) for v in ci(bqs)],
          "q90_rate_long_tercile": rnd(ql[0]), "q90_rate_long_ci": [rnd(v) for v in ci(bql)],
          "log_ratio_long_over_short": rnd(np.log(ql[0] / qs[0])), "log_ratio_ci": [rnd(v) for v in lr_ci],
          "ratio_long_over_short": rnd(ql[0] / qs[0]), "ratio_ci": [rnd(np.exp(v)) for v in lr_ci],
          "equivalence_bounds_log": [rnd(-bound), rnd(bound)], "decision": decision,
          "quantreg_0.9": {"intercept": rnd(qr.params[0]), "intercept_ci": [rnd(v) for v in ci(bcoef[:, 0])],
                           "slope_words_per_s": rnd(qr.params[1]), "slope_ci": [rnd(v) for v in ci(bcoef[:, 1])]},
          "bootstrap": f"circular block, L={L_BLOCK}, B={B}",
          "quantreg_bootstrap_fits_with_warning": n_warn,
          "quantreg_bootstrap_fits_failed": int(np.isnan(bcoef[:, 0]).sum())}
    json.dump(t5, open(RES / f"t5_{tag}.json", "w"), indent=1)

    # ---- details (without null arrays) and nulls for figures
    det = {t: {k: v for k, v in r.items() if k != "_null"} for t, r in prim.items()}
    det["descriptives"] = {"n_units": n, "tokens": int(words.sum()), "zero_word_units": int((words == 0).sum()),
                           "words_median": rnd(np.median(words)), "words_mean": rnd(words.mean()),
                           "A_median": rnd(np.median(A)), "A_q25": rnd(np.quantile(A, .25)), "A_q75": rnd(np.quantile(A, .75)),
                           "A_max": rnd(A.max()), "M_cycles": M, "category_counts": U.category.value_counts().to_dict(),
                           "share_base_all": rnd(U.n_cov_base.sum() / U.n_tok_base.sum()),
                           "share_R1_all": rnd(U.n_cov_R1.sum() / U.n_tok_R1.sum()),
                           "share_R2_all": rnd(U.n_cov_R2.sum() / U.n_tok_R2.sum())}
    det["robustness_R1_raw"] = {t: {k: v for k, v in r.items() if k != "_null"} for t, r in r1.items()}
    json.dump(det, open(RES / f"details_{tag}.json", "w"), indent=1, default=lambda o: o if not isinstance(o, np.generic) else o.item())
    np.savez_compressed(RES / f"nulls_{tag}.npz", **{f"{t}_null": prim[t]["_null"] for t in prim if prim[t].get("testable")},
                        **{f"{t}_obs": np.array([prim[t]["estimate"]]) for t in prim if prim[t].get("testable")})
    return pd.DataFrame(rows), pd.DataFrame(rob)


def verdict(conf, rob):
    """Interpretation rules of plan section 7."""
    c19, c23 = conf["2019wimF"].set_index("test"), conf["2023wimF"].set_index("test")
    r19 = rob["2019wimF"]
    out = {}
    for t in ("T2", "T3", "T4"):
        row = c19.loc[t]
        sig = bool(row.get("significant_holm", False)) and bool(row.get("direction_as_H1", False))
        r1 = r19[(r19.check.str.startswith("R1")) & (r19.test == t)]
        r1_ok = bool(len(r1) and r1.iloc[0].testable and r1.iloc[0].estimate > 0 and r1.iloc[0].ci_excludes_0)
        rep = None
        if t in c23.index and bool(c23.loc[t].get("testable", False)):
            rep = bool(c23.loc[t].significant_holm and c23.loc[t].direction_as_H1)
        out[t] = {"holm_sig_in_H1_direction_2019": sig, "R1_same_sign_ci_excl_0": r1_ok,
                  "supports_H1_2019": bool(sig and r1_ok), "replicated_2023": rep,
                  "opposite_direction_sig_2019": bool(row.get("significant_holm", False)) and not bool(row.get("direction_as_H1", True))}
    t1 = c19.loc["T1"]
    out["T1_precondition_2019"] = {"significant_holm": bool(t1.significant_holm), "positive": bool(t1.direction_as_H1)}
    out["H1_supported_2019"] = any(v["supports_H1_2019"] for k, v in out.items() if k in ("T2", "T3", "T4"))
    out["H1_supported_and_replicated"] = any(v["supports_H1_2019"] and v["replicated_2023"] for k, v in out.items()
                                             if k in ("T2", "T3", "T4"))
    return out


if __name__ == "__main__":
    conf, rob = {}, {}
    for tag in TAGS:
        conf[tag], rob[tag] = run_match(tag)
        print(tag)
        print(conf[tag].drop(columns=["prediction", "statistic"]).to_string())
        print(rob[tag].to_string())
    v = verdict(conf, rob)
    json.dump(v, open(RES / "verdict.json", "w"), indent=1)
    print(json.dumps(v, indent=1))
