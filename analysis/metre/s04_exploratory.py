"""EXPLORATORY analyses (plan section 8 and later additions). Nothing here is confirmatory.

X1 medium contrast (lengths only), X2 phase-tag contrast (circular), X3 per-clip versions, X4 name-masked formulas,
X5 words vs rally duration / shots / D, X6 T4 on 2023 without E5, X7 T1 within single-clip units and with n_clips control
(added after seeing the R3 result for 2023: points with a first-serve-fault clip have both a longer cycle A and a second
transcript window).
Output: results/exploratory.json, results/exploratory_lengths.csv
"""
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import rankdata, spearmanr

sys.path.insert(0, str(Path(__file__).resolve().parent))
from metre_lib import (RES, SEED, TAGS, TR, POINT_PROPER, block_bootstrap_indices, cut_intervals, load_points,  # noqa: E402
                       read_jsonl, spearman_rows, timing_sequence, tokenize, two_sided_p)
from s03_confirmatory import (CAT, ci, index_shift_matrix, rnd, shares_T2, shares_T4, stat_T1, stat_T2,  # noqa: E402
                              stat_T4)

B = 10_000
out = {"_label": "EXPLORATORY: not in plan.md confirmatory family; no multiplicity correction; read as descriptive."}


def iid_ci_diff(x, y, fn, B=B, seed=SEED):
    rng = np.random.default_rng(seed)
    bx = rng.integers(0, len(x), (B, len(x)))
    by = rng.integers(0, len(y), (B, len(y)))
    return ci(np.array([fn(x[i]) - fn(y[j]) for i, j in zip(bx, by)]))


def partial_spearman(x, y, z):
    """Spearman of x and y with ranks residualised on the columns of z (ranks)."""
    rx, ry = rankdata(x), rankdata(y)
    Z = np.column_stack([np.ones(len(x))] + [rankdata(c) for c in np.atleast_2d(z)])
    ex = rx - Z @ np.linalg.lstsq(Z, rx, rcond=None)[0]
    ey = ry - Z @ np.linalg.lstsq(Z, ry, rcond=None)[0]
    return float(np.corrcoef(ex, ey)[0, 1])


def block_ci(fn, n, seed=SEED):
    idx = block_bootstrap_indices(n, 2000, 10, seed)
    return ci(np.array([fn(i) for i in idx]))


# ---------------------------------------------------------------- X1 lengths: written live text vs TV clips
corn = [len(tokenize(r.get("text_corrected") or r.get("text_raw"))) for r in read_jsonl(TR / "text_cornell.jsonl")]
corn = np.array(corn, float)
U19 = pd.read_csv(RES / "units_2019wimF.csv")
C19 = pd.read_csv(RES / "clips_2019wimF.csv")
clip_len = C19.loc[C19.n_tok > 0, "n_tok"].to_numpy(float)
unit_len = U19.loc[U19.words > 0, "words"].to_numpy(float)
qs = [0.1, 0.25, 0.5, 0.75, 0.9]
rows = []
for name, arr in [("cornell_update", corn), ("tv2019_clip_nonempty", clip_len), ("tv2019_unit_nonempty", unit_len)]:
    rows.append({"distribution": name, "n": len(arr), "mean": round(arr.mean(), 2), **{f"q{int(q*100)}": round(float(np.quantile(arr, q)), 2) for q in qs},
                 "max": float(arr.max())})
pd.DataFrame(rows).to_csv(RES / "exploratory_lengths.csv", index=False)
out["X1_lengths"] = {
    "note": "Cornell live text: other matches, written medium, no timing. Only length distributions compared.",
    "table": rows,
    "median_diff_cornell_minus_clip": float(np.median(corn) - np.median(clip_len)),
    "median_diff_ci_iid": [float(v) for v in iid_ci_diff(corn, clip_len, np.median, B=2000)],
    "median_diff_cornell_minus_unit": float(np.median(corn) - np.median(unit_len)),
    "median_diff_unit_ci_iid": [float(v) for v in iid_ci_diff(corn, unit_len, np.median, B=2000)],
}

for tag in TAGS:
    U = pd.read_csv(RES / f"units_{tag}.csv").sort_values("point_idx").reset_index(drop=True)
    Cl = pd.read_csv(RES / f"clips_{tag}.csv")
    C, t_end = timing_sequence(tag)
    A_seq = C.A.to_numpy(float)
    cat_seq = C.category.map(CAT).to_numpy()
    M = len(C)
    res = {}
    n = len(U)

    # ---- X2 phase-tag contrast (clip level, all clips with text)
    Ct = Cl[Cl.n_tok > 0]
    tagged = Ct[(Ct.phase == "between_points") | Ct.score_call_only]
    other = Ct[~((Ct.phase == "between_points") | Ct.score_call_only)]
    sh = lambda d: d.n_cov.sum() / d.n_tok.sum()  # noqa: E731
    rng = np.random.default_rng(SEED)
    bt = []
    for _ in range(B):
        a = tagged.iloc[rng.integers(0, len(tagged), len(tagged))]
        b = other.iloc[rng.integers(0, len(other), len(other))]
        bt.append(sh(a) - sh(b))
    res["X2_phase_tag"] = {"note": "CIRCULAR: between_points tag = text that is a score call; score calls are pool formulas.",
                           "n_clips_tagged": len(tagged), "n_clips_other": len(other),
                           "share_tagged": rnd(sh(tagged)), "share_other": rnd(sh(other)),
                           "diff": rnd(sh(tagged) - sh(other)), "diff_ci_iid_clips": [rnd(v) for v in ci(bt)]}

    # ---- X3 per-clip: point-proper clip text only (no fault clip text) vs A
    pp = Cl[Cl.clip_role.isin(POINT_PROPER)].groupby("point_idx")[["n_tok", "n_cov"]].sum()
    Ux = U.join(pp, on="point_idx", rsuffix="_pp")
    w_pp = Ux.n_tok.fillna(0).to_numpy(float)
    c_pp = Ux.n_cov.fillna(0).to_numpy(float)
    A = U.A.to_numpy(float)
    Ish = index_shift_matrix(U.cyc.to_numpy(), M)
    idx = block_bootstrap_indices(n, B, 10, SEED)
    t1 = stat_T1(w_pp, A[None, :])[0]
    p1, K = two_sided_p(t1, stat_T1(w_pp, A_seq[Ish]))
    t2 = stat_T2(w_pp, c_pp, A[None, :])[0]
    p2, _ = two_sided_p(t2, stat_T2(w_pp, c_pp, A_seq[Ish]))
    a_, b_ = shares_T2(w_pp[idx], c_pp[idx], A[idx])
    res["X3_point_proper_clip_only"] = {"T1_rho": rnd(t1), "T1_ci": [rnd(v) for v in ci(spearman_rows(w_pp[idx], A[idx]))],
                                        "T1_p_shift": rnd(p1, 5), "T2_diff": rnd(t2), "T2_ci": [rnd(v) for v in ci(a_ - b_)],
                                        "T2_p_shift": rnd(p2, 5), "n_shifts": K}

    # ---- X4 name-masked formulas (T2, T4)
    tok, cov = U.n_tok_X4.to_numpy(float), U.n_cov_X4.to_numpy(float)
    x4 = {"share_all": rnd(cov.sum() / tok.sum())}
    t2 = stat_T2(tok, cov, A[None, :])[0]
    p2, _ = two_sided_p(t2, stat_T2(tok, cov, A_seq[Ish]))
    a_, b_ = shares_T2(tok[idx], cov[idx], A[idx])
    x4.update({"T2_diff": rnd(t2), "T2_ci": [rnd(v) for v in ci(a_ - b_)], "T2_p_shift": rnd(p2, 5)})
    Cat = U.category.map(CAT).to_numpy()
    if (Cat == 1).sum() >= 15:
        t4 = stat_T4(tok, cov, Cat[None, :])[0]
        p4, _ = two_sided_p(t4, stat_T4(tok, cov, cat_seq[Ish]))
        w_, c_ = shares_T4(tok[idx], cov[idx], Cat[idx])
        x4.update({"T4_diff": rnd(t4), "T4_ci": [rnd(v) for v in ci(w_ - c_)], "T4_p_shift": rnd(p4, 5)})
    res["X4_name_masked"] = x4

    # ---- X5 words vs rally duration, shots, D (unit level)
    words = U.words.to_numpy(float)
    x5 = {}
    for col in ["tv_rally_duration_s", "tv_n_shots", "D", "n_clips"]:
        v = U[col].to_numpy(float)
        ok = ~np.isnan(v)
        rho = spearmanr(words[ok], v[ok])[0]
        x5[col] = {"rho": rnd(rho), "n": int(ok.sum())}
    ok = ~np.isnan(U.D.to_numpy(float)) & ~np.isnan(U.tv_rally_duration_s.to_numpy(float))
    Uo = U[ok].reset_index(drop=True)
    pr = partial_spearman(Uo.words, Uo.D, np.vstack([Uo.tv_rally_duration_s, Uo.n_clips]))
    pr_ci = block_ci(lambda i: partial_spearman(Uo.words.to_numpy()[i], Uo.D.to_numpy()[i],
                                                np.vstack([Uo.tv_rally_duration_s.to_numpy()[i], Uo.n_clips.to_numpy()[i]])), len(Uo))
    x5["partial_rho_words_D_given_rally_duration_and_n_clips"] = {"rho": rnd(pr), "ci_block_B2000": [rnd(v) for v in pr_ci],
                                                                 "n": len(Uo)}
    res["X5_words_vs_components"] = x5

    # ---- X7 T1 controlling the number of clips (fault clip = second transcript window)
    single = U[U.n_clips == 1].reset_index(drop=True)
    Ish1 = index_shift_matrix(single.cyc.to_numpy(), M)
    ws, As = single.words.to_numpy(float), single.A.to_numpy(float)
    rho_s = stat_T1(ws, As[None, :])[0]
    p_s, K1 = two_sided_p(rho_s, stat_T1(ws, A_seq[Ish1]))
    idx1 = block_bootstrap_indices(len(single), B, 10, SEED)
    pr_n = partial_spearman(words, A, U.n_clips.to_numpy(float))
    pr_n_ci = block_ci(lambda i: partial_spearman(words[i], A[i], U.n_clips.to_numpy(float)[i]), n)
    res["X7_clip_count_control"] = {
        "n_units_single_clip": len(single), "share_units_with_2plus_clips": rnd((U.n_clips > 1).mean()),
        "median_A_single": rnd(np.median(As)), "median_A_multi": rnd(np.median(U.A[U.n_clips > 1])),
        "median_words_single": rnd(np.median(ws)), "median_words_multi": rnd(np.median(U.words[U.n_clips > 1])),
        "T1_rho_single_clip_units": rnd(rho_s), "T1_single_ci": [rnd(v) for v in ci(spearman_rows(ws[idx1], As[idx1]))],
        "T1_single_p_shift": rnd(p_s, 5), "n_shifts": K1,
        "partial_rho_words_A_given_n_clips": rnd(pr_n), "partial_ci_block_B2000": [rnd(v) for v in pr_n_ci]}

    # ---- X6 T4 on 2023 without E5 (units E1-E4; changeover text is cut from the video)
    if tag == "2023wimF":
        P = load_points(tag).set_index("point_idx")
        last = P.index.max()
        agg = Cl[Cl.point_idx.notna()].groupby("point_idx")
        roles = agg.clip_role.apply(lambda s: bool(set(s) & POINT_PROPER))
        sums = agg[["n_tok", "n_cov"]].sum()
        Cseq = C.set_index("point_idx")
        keep = []
        for p in sums.index.astype(int):
            if not roles.loc[p] or p >= last:
                continue
            row = P.loc[p]
            r = row.resid_s
            ok_qc = pd.notna(r) and (abs(r) <= 3 or (r > 3 and row.pbp_serve_number == 2 and pd.isna(row.tv_clip_fault)))
            if ok_qc and Cseq.loc[p, "A"] <= 600:
                keep.append(p)
        V = pd.DataFrame({"point_idx": keep}).join(sums, on="point_idx").join(Cseq[["A", "category", "cyc"]], on="point_idx")
        V = V.sort_values("point_idx").reset_index(drop=True)
        tk, cv = V.n_tok.to_numpy(float), V.n_cov.to_numpy(float)
        Cv = V.category.map(CAT).to_numpy()
        IshV = index_shift_matrix(V.cyc.to_numpy(), M)
        t4 = stat_T4(tk, cv, Cv[None, :])[0]
        p4, K4 = two_sided_p(t4, stat_T4(tk, cv, cat_seq[IshV]))
        idxV = block_bootstrap_indices(len(V), B, 10, SEED)
        w_, c_ = shares_T4(tk[idxV], cv[idxV], Cv[idxV])
        res["X6_T4_2023_without_E5"] = {"n_units": len(V), "n_changeover": int((Cv == 1).sum()),
                                        "share_within": rnd(shares_T4(tk, cv, Cv[None, :])[0][0]),
                                        "share_changeover": rnd(shares_T4(tk, cv, Cv[None, :])[1][0]),
                                        "diff": rnd(t4), "ci": [rnd(v) for v in ci(w_ - c_)], "p_shift": rnd(p4, 5),
                                        "n_shifts": K4,
                                        "note": "changeover periods are cut from the 2023 video: talk after game-ending points is truncated"}
    out[tag] = res

json.dump(out, open(RES / "exploratory.json", "w"), indent=1)
print(json.dumps(out, indent=1)[:6000])
