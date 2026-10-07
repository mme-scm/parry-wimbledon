"""POST HOC analyses after the critic review v1 (plan.md, Addendum 1, items PH2-PH6). Nothing here is confirmatory.

PH2 minimum detectable effects (MDE) for T2-T4 by simulation on shifted timing with planted effects, incl. illustrative
    misattribution (attenuation) scenarios; PH3 T1 within within-game units; PH4 ranges of A and 2019 restricted to the 2023
    range; PH5 serial-correlation check of the shift null (shift-null SD vs iid permutation-null SD); PH6 umpire-pattern
    sensitivity (variants U and R1U built in s02_build.py).
Outputs (results/): posthoc_mde.csv, posthoc_power_curves.csv, posthoc_sensitivity.csv, posthoc.json
"""
import json
import sys
import warnings
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import norm, rankdata

sys.path.insert(0, str(Path(__file__).resolve().parent))
from metre_lib import RES, SEED, TAGS, block_bootstrap_indices, spearman_rows, timing_sequence, two_sided_p  # noqa: E402
from s03_confirmatory import (B, CAT, K_MIN, L_BLOCK, boot_T3, ci, index_shift_matrix, rnd, shares_T2,  # noqa: E402
                              shares_T4, stat_T1, stat_T2, stat_T3, stat_T4, tercile_masks)

warnings.filterwarnings("ignore", category=RuntimeWarning)
ALPHA = 0.05
POWER = 0.80
FAMILY_M = {"2019wimF": 4, "2023wimF": 3}
D_GRID = np.round(np.arange(0, 0.2001, 0.005), 4)
W_GRID = np.round(np.arange(0, 0.6001, 0.02), 4)
MIX = [0.0, 0.25, 0.5]
N_PERM = 2000
LABEL = "POST HOC (plan.md Addendum 1): not pre-registered, outside every Holm family, for interpretation only."


# ---------------------------------------------------------------- helpers
def load(tag):
    U = pd.read_csv(RES / f"units_{tag}.csv").sort_values("point_idx").reset_index(drop=True)
    S = pd.read_csv(RES / f"strings_{tag}.csv")
    C, t_end = timing_sequence(tag)
    return U, S, C


def strings_of(U, S, variant):
    loc = {p: i for i, p in enumerate(U.point_idx)}
    s = S[(S.variant == variant) & S.point_idx.isin(loc)]
    return s.syll.to_numpy(float), s.point_idx.map(loc).to_numpy()


def eval_tests(U, S, C, variant="base", tests=("T2", "T3", "T4"), with_ci=True):
    """Same computation as s03_confirmatory.evaluate (index-shift null, block bootstrap) for a unit subset and variant."""
    A_seq = C.A.to_numpy(float)
    cat_seq = C.category.map(CAT).to_numpy()
    M = len(C)
    nn = len(U)
    Ish = index_shift_matrix(U.cyc.to_numpy(), M)
    A_obs, C_obs = U.A.to_numpy(float), U.category.map(CAT).to_numpy()
    A_null, C_null = A_seq[Ish], cat_seq[Ish]
    tok, cov = U[f"n_tok_{variant}"].to_numpy(float), U[f"n_cov_{variant}"].to_numpy(float)
    syll, s_unit = strings_of(U, S, variant)
    idx = block_bootstrap_indices(nn, B, L_BLOCK, SEED) if with_ci else None
    out = {}
    for t in tests:
        extra = {}
        if t == "T1":
            w = U.words.to_numpy(float)
            obs, nul = stat_T1(w, A_obs[None, :])[0], stat_T1(w, A_null)
            bt = spearman_rows(w[idx], A_obs[idx]) if with_ci else None
        elif t == "T2":
            obs, nul = stat_T2(tok, cov, A_obs[None, :])[0], stat_T2(tok, cov, A_null)
            if with_ci:
                a, b = shares_T2(tok[idx], cov[idx], A_obs[idx])
                bt = a - b
        elif t == "T3":
            obs, nul = stat_T3(syll, s_unit, A_obs[None, :])[0], stat_T3(syll, s_unit, A_null)
            bt = boot_T3(syll, s_unit, nn, idx, A_obs) if with_ci else None
            extra = {"n_strings": int(len(syll))}
        elif t == "T4":
            n_chg = int((C_obs == 1).sum())
            if n_chg < 15:
                out[t] = {"testable": False, "n_changeover_units": n_chg}
                continue
            obs, nul = stat_T4(tok, cov, C_obs[None, :])[0], stat_T4(tok, cov, C_null)
            if with_ci:
                a, b = shares_T4(tok[idx], cov[idx], C_obs[idx])
                bt = a - b
        p, K = two_sided_p(obs, nul)
        lo, hi = ci(bt) if with_ci else (np.nan, np.nan)
        out[t] = {"testable": True, "estimate": rnd(obs), "ci_lo": rnd(lo), "ci_hi": rnd(hi), "p_shift": rnd(p, 5),
                  "n_shifts": int(K), "n_units": int(nn), "null_sd": rnd(np.nanstd(nul), 5), **extra, "_null": nul}
    return out


def strip(d):
    return {k: v for k, v in d.items() if k != "_null"}


# ---------------------------------------------------------------- PH2: power / MDE
def shift_setup(U, C):
    M = len(C)
    ks = np.arange(K_MIN, M - K_MIN + 1)
    I = (U.cyc.to_numpy()[None, :] + ks[:, None]) % M
    A_all = C.A.to_numpy(float)[I]
    C_all = C.category.map(CAT).to_numpy()[I]
    dist = np.abs(ks[:, None] - ks[None, :]) % M
    dist = np.minimum(dist, M - dist)
    nullmask = dist >= K_MIN            # [k (test shift), k0 (base)]
    return ks, A_all, C_all, nullmask


def p_from_matrix(Sm, nullmask):
    """Two-sided shift-null p for every base k0 (column): observed = diagonal, null = admissible rows of the column."""
    obs = np.diag(Sm)
    valid = nullmask & ~np.isnan(Sm)
    Kn = valid.sum(0)
    up = (1 + ((Sm >= obs[None, :]) & valid).sum(0)) / (1 + Kn)
    dn = (1 + ((Sm <= obs[None, :]) & valid).sum(0)) / (1 + Kn)
    return np.minimum(1.0, 2 * np.minimum(up, dn)), obs


def neighbours(n):
    prev = np.r_[0, np.arange(n - 1)]
    nxt = np.r_[np.arange(1, n), n - 1]
    return prev, nxt


def power_share(tok, cov, G1, G2, nullmask, alphas, label):
    """T2/T4: plant +d/2 (group 1) and -d/2 (group 2) in each unit's formula share under the base shift k0."""
    G1f, G2f = G1.astype(float), G2.astype(float)
    with np.errstate(invalid="ignore", divide="ignore"):
        den1, den2 = G1f @ tok, G2f @ tok
    n = len(tok)
    prev, nxt = neighbours(n)
    base = 0.5 * (G1f - G2f)          # rows = base k0
    rows = []
    for m in MIX:
        mixed = (1 - m) * base + m / 2 * (base[:, prev] + base[:, nxt])
        true0 = meas0 = None
        for d in D_GRID:
            covp = np.clip(cov[None, :] + d * mixed * tok[None, :], 0, tok[None, :])
            with np.errstate(invalid="ignore", divide="ignore"):
                Sm = (G1f @ covp.T) / den1[:, None] - (G2f @ covp.T) / den2[:, None]
            p, obs = p_from_matrix(Sm, nullmask)
            # true effect: the same plant without misattribution, evaluated at the base shift k0
            cov_true = np.clip(cov[None, :] + d * base * tok[None, :], 0, tok[None, :])
            with np.errstate(invalid="ignore", divide="ignore"):
                tr = (np.einsum("kn,kn->k", G1f, cov_true) / den1 - np.einsum("kn,kn->k", G2f, cov_true) / den2)
            if d == 0:
                true0, meas0 = tr.copy(), obs.copy()
            ok = ~np.isnan(obs)
            row = {"test": label, "mix": m, "param": float(d),
                   "true_effect": float(np.nanmean(tr - true0)), "measured_effect": float(np.nanmean(obs - meas0)),
                   "n_bases": int(ok.sum())}
            for name, a in alphas.items():
                row[f"power_{name}"] = float(np.mean((p[ok] < a) & (obs[ok] > 0)))
            rows.append(row)
    return rows


def power_T3(syll, s_unit, A_all, nullmask, alphas):
    """T3: Gaussian-copula plant between string syllables and the A of the string's (source) unit."""
    K, n = A_all.shape
    Ns = len(syll)
    RA = rankdata(A_all[:, s_unit], axis=1)
    RA -= RA.mean(1, keepdims=True)
    RA /= np.linalg.norm(RA, axis=1, keepdims=True)
    zA = norm.ppf((rankdata(A_all, axis=1) - 0.5) / n)
    sorted_syll = np.sort(syll)
    prev, nxt = neighbours(n)
    rows = []
    for m in MIX:
        rng = np.random.default_rng(SEED)
        tieb = rng.random((K, Ns))
        zs = norm.ppf((rankdata(syll[None, :] + 0.5 * tieb, axis=1) - 0.5) / Ns)
        u = rng.random((K, Ns))
        src = np.where(u < 1 - m, s_unit[None, :], np.where(u < 1 - m / 2, prev[s_unit][None, :], nxt[s_unit][None, :]))
        zA_src = np.take_along_axis(zA, src, axis=1)
        RAsrc = rankdata(np.take_along_axis(A_all, src, axis=1), axis=1)
        RAsrc -= RAsrc.mean(1, keepdims=True)
        RAsrc /= np.linalg.norm(RAsrc, axis=1, keepdims=True)
        for w in W_GRID:
            lat = np.sqrt(1 - w ** 2) * zs + w * zA_src
            r = np.argsort(np.argsort(lat, axis=1, kind="stable"), axis=1, kind="stable")
            sp = sorted_syll[r]
            Rp = rankdata(sp, axis=1)
            Rp -= Rp.mean(1, keepdims=True)
            Rp /= np.linalg.norm(Rp, axis=1, keepdims=True)
            Sm = RA @ Rp.T
            p, obs = p_from_matrix(Sm, nullmask)
            tr = np.einsum("kn,kn->k", Rp, RAsrc)
            row = {"test": "T3", "mix": m, "param": float(w), "true_effect": float(tr.mean()),
                   "measured_effect": float(obs.mean()), "n_bases": int(K)}
            for name, a in alphas.items():
                row[f"power_{name}"] = float(np.mean((p < a) & (obs > 0)))
            rows.append(row)
    return rows


def mde(curve, col, eff):
    """Smallest effect with power >= POWER (linear interpolation on the first crossing)."""
    c = curve.sort_values("param").reset_index(drop=True)
    hit = np.where(c[col].to_numpy() >= POWER)[0]
    if len(hit) == 0:
        return None
    i = int(hit[0])
    if i == 0:
        return float(c.loc[0, eff])
    p0, p1 = c.loc[i - 1, col], c.loc[i, col]
    e0, e1 = c.loc[i - 1, eff], c.loc[i, eff]
    return float(e0 + (POWER - p0) / (p1 - p0) * (e1 - e0)) if p1 > p0 else float(e1)


# ---------------------------------------------------------------- main
out = {"_label": LABEL}
curves, mde_rows, sens_rows = [], [], []
U_all, S_all, C_all_ = {}, {}, {}
for tag in TAGS:
    U, S, C = load(tag)
    U_all[tag], S_all[tag], C_all_[tag] = U, S, C
    res = {}
    conf = pd.read_csv(RES / f"confirmatory_{tag}.csv").set_index("test")

    # ---- consistency check: re-implementation reproduces the confirmatory T2-T4 (base) exactly
    chk = eval_tests(U, S, C, "base", tests=("T2", "T4"), with_ci=True)
    for t, r in chk.items():
        if r["testable"]:
            c = conf.loc[t]
            assert abs(r["estimate"] - c.estimate) < 1e-9 and abs(r["p_shift"] - c.p_shift) < 1e-9, (tag, t)
            assert abs(r["ci_lo"] - c.ci_lo) < 1e-9 and abs(r["ci_hi"] - c.ci_hi) < 1e-9, (tag, t)
    res["reimplementation_check"] = "T2/T4 base estimates, CIs and p equal confirmatory_<tag>.csv"

    # ---- PH2 MDE
    ks, A_all, Cat_all, nullmask = shift_setup(U, C)
    alphas = {"alpha05": ALPHA, "alpha_holm1": ALPHA / FAMILY_M[tag]}
    tok, cov = U.n_tok_base.to_numpy(float), U.n_cov_base.to_numpy(float)
    s_m, l_m = tercile_masks(A_all)
    rows = power_share(tok, cov, s_m, l_m, nullmask, alphas, "T2")
    if (U.category == "changeover").sum() >= 15:
        rows += power_share(tok, cov, Cat_all == 0, Cat_all == 1, nullmask, alphas, "T4")
    syll, s_unit = strings_of(U, S, "base")
    rows += power_T3(syll, s_unit, A_all, nullmask, alphas)
    cv = pd.DataFrame(rows)
    cv.insert(0, "match", tag)
    curves.append(cv)
    for (t, m), g in cv.groupby(["test", "mix"]):
        for an, a in alphas.items():
            col = f"power_{an}"
            z = g[g.param == 0].iloc[0]
            mde_rows.append({"match": tag, "test": t, "mix": m, "alpha": round(a, 5), "alpha_label": an,
                             "mde_true": rnd(mde(g, col, "true_effect"), 4), "mde_measured": rnd(mde(g, col, "measured_effect"), 4),
                             "size_at_zero_effect": rnd(z[col], 4), "max_power_in_grid": rnd(g[col].max(), 3),
                             "grid_max_true_effect": rnd(g.true_effect.max(), 4), "n_bases": int(g.n_bases.min())})
    res["mde_setup"] = {"n_base_shifts": int(len(ks)), "null_shifts_per_base_min": int(nullmask.sum(0).min()),
                        "alphas": {k: round(v, 5) for k, v in alphas.items()}, "power_target": POWER,
                        "mix_scenarios": MIX, "d_grid_max": float(D_GRID.max()), "w_grid_max": float(W_GRID.max()),
                        "n_strings_T3": int(len(syll))}

    # ---- PH3 T1 within categories
    wg = U[U.category == "within_game"].reset_index(drop=True)
    r_wg = eval_tests(wg, S, C, "base", tests=("T1",))["T1"]
    nz = U[U.words > 0].reset_index(drop=True)
    r_nz = eval_tests(nz, S, C, "base", tests=("T1",))["T1"]
    res["PH3_T1_within_category"] = {
        "T1_all_units": {"rho": rnd(conf.loc["T1"].estimate), "ci": [rnd(conf.loc["T1"].ci_lo), rnd(conf.loc["T1"].ci_hi)],
                         "n": int(conf.loc["T1"].n_units)},
        "T1_within_game_units": strip(r_wg), "T1_units_with_text": strip(r_nz),
        "median_tokens_by_category": {k: rnd(v, 1) for k, v in U.groupby("category").words.median().items()},
        "n_by_category": {k: int(v) for k, v in U.category.value_counts().items()},
        "median_A_by_category": {k: rnd(v, 1) for k, v in U.groupby("category").A.median().items()},
        "median_A_zero_token_units": rnd(U.A[U.words == 0].median(), 1),
        "median_A_units_with_text": rnd(U.A[U.words > 0].median(), 1),
        "n_zero_token_units": int((U.words == 0).sum())}

    # ---- PH4 ranges of A
    A = U.A.to_numpy(float)
    res["PH4_A_range"] = {"min": rnd(A.min(), 1), "q10": rnd(np.quantile(A, .1), 1), "median": rnd(np.median(A), 1),
                          "q90": rnd(np.quantile(A, .9), 1), "max": rnd(A.max(), 1), "n_units": int(len(A)),
                          "n_units_A_over_100s": int((A > 100).sum()),
                          "n_changeover_units": int((U.category == "changeover").sum())}

    # ---- PH5 serial correlation
    def lag1(x):
        x = np.asarray(x, float)
        return rnd(np.corrcoef(rankdata(x[:-1]), rankdata(x[1:]))[0, 1], 3)
    share_u = (U.n_cov_base / U.n_tok_base)[U.n_tok_base > 0]
    rng = np.random.default_rng(SEED)
    perms = np.array([rng.permutation(len(U)) for _ in range(N_PERM)])
    A_obs, C_obs = U.A.to_numpy(float), U.category.map(CAT).to_numpy()
    words = U.words.to_numpy(float)
    prim = eval_tests(U, S, C, "base", tests=("T1", "T2", "T3", "T4"), with_ci=False)
    ph5 = {"lag1_spearman_unit_order": {"tokens": lag1(words), "formula_share_units_with_text": lag1(share_u),
                                        "A": lag1(A_obs), "A_full_cycle_sequence": lag1(C.A.to_numpy(float))},
           "n_permutations": N_PERM, "tests": {}}
    for t in ("T1", "T2", "T3", "T4"):
        r = prim[t]
        if not r["testable"]:
            continue
        Ap, Cp = A_obs[perms], C_obs[perms]
        if t == "T1":
            nul = stat_T1(words, Ap)
        elif t == "T2":
            nul = stat_T2(tok, cov, Ap)
        elif t == "T3":
            nul = stat_T3(syll, s_unit, Ap)
        else:
            nul = stat_T4(tok, cov, Cp)
        pp_, _ = two_sided_p(r["estimate"], nul)
        ph5["tests"][t] = {"sd_shift_null": rnd(np.nanstd(r["_null"]), 5), "sd_perm_null": rnd(np.nanstd(nul), 5),
                           "ratio_shift_over_perm": rnd(np.nanstd(r["_null"]) / np.nanstd(nul), 3),
                           "p_shift": r["p_shift"], "p_perm": rnd(pp_, 5)}
    res["PH5_serial_correlation"] = ph5

    # ---- PH6 umpire-pattern sensitivity
    for v in ("U", "R1U"):
        rr = eval_tests(U, S, C, v, tests=("T2", "T3", "T4"))
        for t, r in rr.items():
            if not r["testable"]:
                sens_rows.append({"match": tag, "check": f"PH6 variant {v}", "variant": v, "test": t,
                                  "testable": False, "n_changeover_units": r["n_changeover_units"]})
                continue
            sens_rows.append({"match": tag, "check": f"PH6 variant {v}", "variant": v, "test": t, **strip(r),
                              "share_all": rnd(U[f"n_cov_{v}"].sum() / U[f"n_tok_{v}"].sum()),
                              "tokens": int(U[f"n_tok_{v}"].sum())})
    out[tag] = res

# ---- PH4 (2019 restricted to the A range of the 2023 units)
U19, S19, C19 = U_all["2019wimF"], S_all["2019wimF"], C_all_["2019wimF"]
amax23 = float(U_all["2023wimF"].A.max())
U19r = U19[U19.A <= amax23].reset_index(drop=True)
rr = eval_tests(U19r, S19, C19, "base", tests=("T2", "T3"))
for t, r in rr.items():
    sens_rows.append({"match": "2019wimF", "check": "PH4 2019 units with A <= max A of 2023 units", "variant": "base",
                      "test": t, **strip(r), "share_all": rnd(U19r.n_cov_base.sum() / U19r.n_tok_base.sum()),
                      "tokens": int(U19r.n_tok_base.sum())})
out["PH4_2019_restricted"] = {"A_max_2023": amax23, "n_units_2019_restricted": int(len(U19r)),
                              "n_units_2019_dropped": int(len(U19) - len(U19r))}

umpire = json.load(open(RES / "posthoc_umpire_check.json"))
out["PH6_umpire_check"] = umpire

pd.concat(curves).to_csv(RES / "posthoc_power_curves.csv", index=False)
pd.DataFrame(mde_rows).to_csv(RES / "posthoc_mde.csv", index=False)
S_df = pd.DataFrame(sens_rows)
S_df["ci_excludes_0"] = ((S_df.ci_lo > 0) | (S_df.ci_hi < 0)) & S_df.testable
S_df.to_csv(RES / "posthoc_sensitivity.csv", index=False)
json.dump(out, open(RES / "posthoc.json", "w"), indent=1, default=lambda o: o.item() if isinstance(o, np.generic) else str(o))
print(pd.DataFrame(mde_rows).to_string())
print(S_df.drop(columns=["_null"], errors="ignore").to_string())
print(json.dumps({t: {k: v for k, v in out[t].items() if k.startswith("PH")} for t in TAGS}, indent=1,
                 default=lambda o: o.item() if isinstance(o, np.generic) else str(o))[:5000])
