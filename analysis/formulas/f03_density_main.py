"""Formulaic density for the finals: D1 in-sample, D2 split-half, D3 held-out across matches, D6 per context,
D7 shuffled-word baseline, sensitivity analyses S1-S8, and the C3/R3 time tests (plan sections 4, 7, 8).

Outputs: results/density_main.csv, results/density_context.csv, results/density_sensitivity.csv,
results/density_shuffled.csv, results/split_random.csv, results/c3_time_tests.json,
results/utt_coverage_<design>.csv (per-utterance token counts; no text)
Run: python -I analysis/formulas/f03_density_main.py
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import csv
import json
from multiprocessing import Pool
import numpy as np
import common as C

B = 2000
R_SHUFFLE = 200
R_RANDSPLIT = 200
N_PERM = 5000
NAMES = C.player_name_lexicon()


def ident(utts, m=2, stop=True):
    F = C.formula_set_fast(utts, m=m, stop_filter=stop)
    S = C.system_set_fast(utts, NAMES, stop_filter=stop)
    return F, S


def measure(utts, F, S, n_min=2, masks=None):
    return C.densities(utts, F, S, NAMES, n_min=n_min, masks=masks)


def row(design, ident_on, meas_on, variant, arrs, seed, strata=None):
    n, ca, cab = arrs
    out = []
    for lab, num in (("a", ca), ("a+b", cab)):
        est, lo, hi, _ = C.boot_ratio(num, n, B=B, seed=seed, strata=strata)
        out.append({"design": design, "identified_on": ident_on, "measured_on": meas_on, "variant": variant,
                    "measure": lab, "density": est, "ci_lo": lo, "ci_hi": hi,
                    "tokens_measured": int(np.sum(n)), "utterances_measured": int(len(n))})
    return out


def split_half(utts, half, F_S_by_half=None, n_min=2, masks=None):
    """half: array of 0/1. Identify on each half, measure on the other. Returns pooled arrays and strata."""
    half = np.asarray(half)
    idx0 = np.where(half == 0)[0]
    idx1 = np.where(half == 1)[0]
    U0 = [utts[i] for i in idx0]
    U1 = [utts[i] for i in idx1]
    F0, S0 = ident(U0)
    F1, S1 = ident(U1)
    m0 = [masks[i] for i in idx0] if masks is not None else None
    m1 = [masks[i] for i in idx1] if masks is not None else None
    a1 = measure(U1, F0, S0, n_min=n_min, masks=m1)  # identified on 0, measured on 1
    a0 = measure(U0, F1, S1, n_min=n_min, masks=m0)
    pooled = tuple(np.concatenate([x, y]) for x, y in zip(a0, a1))
    strata = np.concatenate([np.zeros(len(a0[0]), int), np.ones(len(a1[0]), int)])
    return a0, a1, pooled, strata


def _shuffle_job(args):
    seed, utts, parity = args
    rng = np.random.default_rng(seed)
    flat = [t for u in utts for t in u]
    perm = rng.permutation(len(flat))
    flat = [flat[i] for i in perm]
    out = []
    k = 0
    for u in utts:
        out.append(flat[k:k + len(u)])
        k += len(u)
    F, S = ident(out)
    n, ca, cab = measure(out, F, S)
    _, _, (pn, pa, pab), _ = split_half(out, parity)
    return [C.ratio(ca, n), C.ratio(cab, n), C.ratio(pa, pn), C.ratio(pab, pn)]


def _randsplit_job(args):
    seed, utts = args
    rng = np.random.default_rng(seed)
    half = rng.integers(0, 2, size=len(utts))
    _, _, (pn, pa, pab), _ = split_half(utts, half)
    return [C.ratio(pa, pn), C.ratio(pab, pn)]


def mask_utts(utts):
    """S5: replace official-call tokens by unique placeholders; return (utts, keep masks)."""
    out, masks = [], []
    k = 0
    for u in utts:
        keep = C.official_mask(u, NAMES)
        v = []
        for t, kp in zip(u, keep):
            if kp:
                v.append(t)
            else:
                v.append(f"<masked{k}>")
                k += 1
        out.append(v)
        masks.append(keep)
    return out, masks


def perm_test_terciles(n, ca, lab, seed, nperm=N_PERM):
    """Token-weighted density T1 minus T3; permutation of labels among T1+T3 utterances; two-sided p."""
    lab = np.asarray(lab)
    sel = np.where((lab == "T1") | (lab == "T3"))[0]
    n_s, c_s, l_s = n[sel], ca[sel], lab[sel]
    is1 = l_s == "T1"
    obs = c_s[is1].sum() / n_s[is1].sum() - c_s[~is1].sum() / n_s[~is1].sum()
    rng = np.random.default_rng(seed)
    null = np.empty(nperm)
    for b in range(nperm):
        p = rng.permutation(is1)
        null[b] = c_s[p].sum() / n_s[p].sum() - c_s[~p].sum() / n_s[~p].sum()
    p_two = (1 + np.sum(np.abs(null) >= abs(obs))) / (1 + nperm)
    # bootstrap CI of the difference (resample within each tercile)
    rngb = np.random.default_rng(seed + 1)
    i1 = np.where(is1)[0]
    i3 = np.where(~is1)[0]
    d = np.empty(B)
    for b in range(B):
        x = i1[rngb.integers(0, len(i1), len(i1))]
        y = i3[rngb.integers(0, len(i3), len(i3))]
        d[b] = c_s[x].sum() / n_s[x].sum() - c_s[y].sum() / n_s[y].sum()
    return {"T1_density": float(c_s[is1].sum() / n_s[is1].sum()), "T3_density": float(c_s[~is1].sum() / n_s[~is1].sum()),
            "diff_T1_minus_T3": float(obs), "diff_ci_lo": float(np.percentile(d, 2.5)), "diff_ci_hi": float(np.percentile(d, 97.5)),
            "perm_null_mean": float(null.mean()), "perm_null_lo": float(np.percentile(null, 2.5)),
            "perm_null_hi": float(np.percentile(null, 97.5)), "p_two_sided": float(p_two), "n_perm": nperm,
            "utterances_T1": int(is1.sum()), "utterances_T3": int((~is1).sum()),
            "tokens_T1": int(n_s[is1].sum()), "tokens_T3": int(n_s[~is1].sum())}


def save_utt_cov(name, recs, arrs):
    n, ca, cab = arrs
    with open(C.RESULTS / f"utt_coverage_{name}.csv", "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["utt_id", "tokens", "covered_a", "covered_ab"])
        for r, x, y, z in zip(recs, n, ca, cab):
            w.writerow([r["utt_id"], int(x), int(y), int(z)])


def main():
    rows, ctx_rows, sens_rows = [], [], []
    r19 = C.load_stream(C.MAIN)
    cuts19 = C.add_contexts(r19, C.MAIN)
    r23 = C.load_stream(C.HELDOUT)
    cuts23 = C.add_contexts(r23, C.HELDOUT)
    u19 = [r["toks"] for r in r19]
    u23 = [r["toks"] for r in r23]
    pool_recs = [r for s in C.pool_streams() for r in C.load_stream(s)]
    upool = [r["toks"] for r in pool_recs]
    print("tokens 2019/2023/pool", sum(map(len, u19)), sum(map(len, u23)), sum(map(len, upool)), flush=True)

    F19, S19 = ident(u19)
    Fpool, Spool = ident(upool)
    F23, S23 = ident(u23)
    # D1
    a19_in = measure(u19, F19, S19)
    rows += row("D1_in_sample", C.MAIN, C.MAIN, "primary", a19_in, 11)
    a23_in = measure(u23, F23, S23)
    rows += row("D1_in_sample", C.HELDOUT, C.HELDOUT, "primary", a23_in, 12)
    # D2 split-half by clip parity
    par19 = np.array([r["clip_i"] % 2 for r in r19])
    a0, a1, pooled, strata = split_half(u19, par19)
    rows += row("D2_split_half", "2019 odd clips", "2019 even clips", "primary", a0, 21)
    rows += row("D2_split_half", "2019 even clips", "2019 odd clips", "primary", a1, 22)
    rows += row("D2_split_half", "2019 halves", "2019 other half (pooled)", "primary", pooled, 23, strata)
    par23 = np.array([r["clip_i"] % 2 for r in r23])
    _, _, pooled23, strata23 = split_half(u23, par23)
    rows += row("D2_split_half", "2023 halves", "2023 other half (pooled)", "primary", pooled23, 24, strata23)
    # D3 held-out
    a19_pool = measure(u19, Fpool, Spool)
    rows += row("D3_held_out", "pool (18 matches)", C.MAIN, "primary", a19_pool, 31)
    a23_19 = measure(u23, F19, S19)
    rows += row("D3_held_out", C.MAIN, C.HELDOUT, "primary", a23_19, 32)
    a23_pool = measure(u23, Fpool, Spool)
    rows += row("D3_held_out", "pool (18 matches)", C.HELDOUT, "primary", a23_pool, 33)
    save_utt_cov("pool_to_2019", r19, a19_pool)
    save_utt_cov("pool_to_2023", r23, a23_pool)
    save_utt_cov("insample_2019", r19, a19_in)
    save_utt_cov("insample_2023", r23, a23_in)

    # D6 per context
    for stream, recs, arr_in, arr_ho, cuts in ((C.MAIN, r19, a19_in, a19_pool, cuts19), (C.HELDOUT, r23, a23_in, a23_pool, cuts23)):
        for field in ("ctx_phase", "ctx_dtb_terc", "ctx_ta_terc", "ctx_role", "ctx_score"):
            labs = np.array([r[field] for r in recs])
            for g in sorted(set(labs)):
                sel = np.where(labs == g)[0]
                for ident_lab, arr, seed in (("in_sample", arr_in, 61), ("pool", arr_ho, 62)):
                    n, ca, cab = (x[sel] for x in arr)
                    for lab, num in (("a", ca), ("a+b", cab)):
                        est, lo, hi, _ = C.boot_ratio(num, n, B=B, seed=seed)
                        ctx_rows.append({"stream": stream, "context": field[4:], "group": g, "identified_on": ident_lab,
                                         "measure": lab, "density": est, "ci_lo": lo, "ci_hi": hi,
                                         "tokens": int(n.sum()), "utterances": int(len(sel))})
    # C3 / R3 time tests (pool-identified (a))
    tests = {"cuts_2019": cuts19, "cuts_2023": cuts23}
    for stream, recs, arr, sd in ((C.MAIN, r19, a19_pool, 71), (C.HELDOUT, r23, a23_pool, 73)):
        n, ca, _ = arr
        for field, key in (("ctx_dtb_terc", "dead_time_before"), ("ctx_ta_terc", "time_after")):
            lab = [r[field] for r in recs]
            tests[f"{stream}:{key}:pool_a"] = perm_test_terciles(n, ca, lab, sd)
            sd += 1
        # exploratory: in-sample identification
    for stream, recs, arr, sd in ((C.MAIN, r19, a19_in, 81), (C.HELDOUT, r23, a23_in, 83)):
        n, ca, _ = arr
        for field, key in (("ctx_dtb_terc", "dead_time_before"), ("ctx_ta_terc", "time_after")):
            lab = [r[field] for r in recs]
            tests[f"{stream}:{key}:insample_a:exploratory"] = perm_test_terciles(n, ca, lab, sd)
            sd += 1
    C.write_json(C.RESULTS / "c3_time_tests.json", tests)
    print("C3 done", flush=True)

    # ---------------- sensitivity analyses
    # S1 text_dedup
    d19 = C.load_stream(C.MAIN, "text_dedup")
    d23 = C.load_stream(C.HELDOUT, "text_dedup")
    dpool = [r["toks"] for s in C.pool_streams() for r in C.load_stream(s, "text_dedup")]
    ud19 = [r["toks"] for r in d19]
    ud23 = [r["toks"] for r in d23]
    Fd, Sd = ident(ud19)
    sens_rows += row("D1_in_sample", C.MAIN, C.MAIN, "S1_text_dedup", measure(ud19, Fd, Sd), 101)
    _, _, pooled_d, st_d = split_half(ud19, np.array([r["clip_i"] % 2 for r in d19]))
    sens_rows += row("D2_split_half", "2019 halves", "2019 other half (pooled)", "S1_text_dedup", pooled_d, 102, st_d)
    Fdp, Sdp = ident(dpool)
    sens_rows += row("D3_held_out", "pool (18 matches)", C.MAIN, "S1_text_dedup", measure(ud19, Fdp, Sdp), 103)
    sens_rows += row("D3_held_out", C.MAIN, C.HELDOUT, "S1_text_dedup", measure(ud23, Fd, Sd), 104)
    # S2 no stop filter
    F2, S2 = ident(u19, stop=False)
    sens_rows += row("D1_in_sample", C.MAIN, C.MAIN, "S2_no_stop_filter", measure(u19, F2, S2), 111)
    F2p, S2p = ident(upool, stop=False)
    sens_rows += row("D3_held_out", "pool (18 matches)", C.MAIN, "S2_no_stop_filter", measure(u19, F2p, S2p), 112)
    sens_rows += row("D3_held_out", C.MAIN, C.HELDOUT, "S2_no_stop_filter", measure(u23, F2, S2), 113)
    # S3 m = 3
    F3 = C.formula_set_fast(u19, m=3)
    sens_rows += row("D1_in_sample", C.MAIN, C.MAIN, "S3_m3", measure(u19, F3, S19), 121)
    F3p = C.formula_set_fast(upool, m=3)
    sens_rows += row("D3_held_out", "pool (18 matches)", C.MAIN, "S3_m3", measure(u19, F3p, Spool), 122)
    sens_rows += row("D3_held_out", C.MAIN, C.HELDOUT, "S3_m3", measure(u23, F3, S19), 123)
    # S4 far repeats only (in-sample)
    F4 = C.formula_set(u19, m=2, min_gap=4, clip_idx=[r["clip_i"] for r in r19])
    sens_rows += row("D1_in_sample", C.MAIN, C.MAIN, "S4_repeats_ge4_clips_apart", measure(u19, F4, S19), 131)
    # S5 official calls masked
    mu19, mk19 = mask_utts(u19)
    mu23, mk23 = mask_utts(u23)
    mpool, _ = mask_utts(upool)
    F5, S5 = ident(mu19)
    sens_rows += row("D1_in_sample", C.MAIN, C.MAIN, "S5_official_calls_masked", measure(mu19, F5, S5, masks=mk19), 141)
    _, _, pooled5, st5 = split_half(mu19, par19, masks=mk19)
    sens_rows += row("D2_split_half", "2019 halves", "2019 other half (pooled)", "S5_official_calls_masked", pooled5, 142, st5)
    F5p, S5p = ident(mpool)
    sens_rows += row("D3_held_out", "pool (18 matches)", C.MAIN, "S5_official_calls_masked", measure(mu19, F5p, S5p, masks=mk19), 143)
    sens_rows += row("D3_held_out", C.MAIN, C.HELDOUT, "S5_official_calls_masked", measure(mu23, F5, S5, masks=mk23), 144)
    masked_share = 1 - sum(int(m.sum()) for m in mk19) / sum(map(len, u19))
    # S6 n_min = 3
    sens_rows += row("D1_in_sample", C.MAIN, C.MAIN, "S6_nmin3", measure(u19, F19, S19, n_min=3), 151)
    sens_rows += row("D3_held_out", "pool (18 matches)", C.MAIN, "S6_nmin3", measure(u19, Fpool, Spool, n_min=3), 152)
    sens_rows += row("D3_held_out", C.MAIN, C.HELDOUT, "S6_nmin3", measure(u23, F19, S19, n_min=3), 153)
    _, _, pooled6, st6 = split_half(u19, par19, n_min=3)
    sens_rows += row("D2_split_half", "2019 halves", "2019 other half (pooled)", "S6_nmin3", pooled6, 154, st6)
    # S7 block split
    blk = np.array([(r["clip_i"] // 20) % 2 for r in r19])
    _, _, pooled7, st7 = split_half(u19, blk)
    sens_rows += row("D2_split_half", "2019 halves", "2019 other half (pooled)", "S7_blocks_of_20_clips", pooled7, 161, st7)
    print("sensitivity done", flush=True)

    # S8 random half-splits, D7 shuffled baseline (parallel)
    with Pool(4) as pool:
        rs = pool.map(_randsplit_job, [(C.MASTER_SEED + 1000 + k, u19) for k in range(R_RANDSPLIT)])
        sh = pool.map(_shuffle_job, [(C.MASTER_SEED + 2000 + k, u19, par19) for k in range(R_SHUFFLE)])
    rs = np.array(rs)
    sh = np.array(sh)
    with open(C.RESULTS / "split_random.csv", "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["replicate", "density_a", "density_ab"])
        for k, (x, y) in enumerate(rs):
            w.writerow([k, f"{x:.6f}", f"{y:.6f}"])
    with open(C.RESULTS / "density_shuffled.csv", "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["replicate", "insample_a", "insample_ab", "splithalf_a", "splithalf_ab"])
        for k, v in enumerate(sh):
            w.writerow([k] + [f"{x:.6f}" for x in v])
    for j, (design, lab) in enumerate((("D1_in_sample", "a"), ("D1_in_sample", "a+b"), ("D2_split_half", "a"), ("D2_split_half", "a+b"))):
        v = sh[:, j]
        sens_rows.append({"design": design, "identified_on": "2019 shuffled words", "measured_on": "2019 shuffled words",
                          "variant": f"D7_shuffled_word_baseline_R{R_SHUFFLE}", "measure": lab, "density": float(v.mean()),
                          "ci_lo": float(np.percentile(v, 2.5)), "ci_hi": float(np.percentile(v, 97.5)),
                          "tokens_measured": sum(map(len, u19)), "utterances_measured": len(u19)})
    for j, lab in enumerate(("a", "a+b")):
        v = rs[:, j]
        sens_rows.append({"design": "D2_split_half", "identified_on": "2019 random halves", "measured_on": "2019 other half (pooled)",
                          "variant": f"S8_random_half_splits_R{R_RANDSPLIT}", "measure": lab, "density": float(v.mean()),
                          "ci_lo": float(np.percentile(v, 2.5)), "ci_hi": float(np.percentile(v, 97.5)),
                          "tokens_measured": sum(map(len, u19)), "utterances_measured": len(u19)})

    for name, rr in (("density_main.csv", rows), ("density_context.csv", ctx_rows), ("density_sensitivity.csv", sens_rows)):
        with open(C.RESULTS / name, "w", newline="") as fh:
            w = csv.DictWriter(fh, fieldnames=list(rr[0]))
            w.writeheader()
            for x in rr:
                w.writerow({k: (f"{v:.6f}" if isinstance(v, float) else v) for k, v in x.items()})
    C.write_json(C.RESULTS / "density_main_meta.json", {
        "tokens_2019": sum(map(len, u19)), "tokens_2023": sum(map(len, u23)), "tokens_pool": sum(map(len, upool)),
        "utterances_2019": len(u19), "utterances_2023": len(u23), "utterances_pool": len(upool),
        "formula_types_2019": len(F19), "system_frames_2019": len(S19), "formula_types_pool": len(Fpool), "system_frames_pool": len(Spool),
        "formula_types_2023": len(F23), "system_frames_2023": len(S23),
        "S5_masked_token_share_2019": masked_share, "B": B, "R_shuffle": R_SHUFFLE, "R_randsplit": R_RANDSPLIT, "n_perm_C3": N_PERM,
    })
    print("done")


if __name__ == "__main__":
    main()
