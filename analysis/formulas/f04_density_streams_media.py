"""Per-stream (D4) and per-medium size-matched (D5) densities, with the press-conference baseline (plan section 4).

Outputs: results/density_streams.csv, results/medium_replicates.csv, results/density_medium.csv
Run: python -I analysis/formulas/f04_density_streams_media.py
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import csv
from multiprocessing import Pool
import numpy as np
import common as C

B = 2000
R_SMALL_STREAM = 200   # D4(ii), 1,500 tokens
R_MATCHED = 1000       # D5(i), 2019-size; revision 1: raised from 200 for the (a) family (C2), see plan.md addendum 2
R_MATCHED_SYSTEMS = 200  # D5(i) replicates that also identify systems ((a)+(b)); = the pre-registered R, same seeds
R_HELDOUT = 50         # D5(ii)
R_HELDOUT_GROUPED = 50  # D5(ii-b), revision 1 (post hoc)
R_LARGE = 20           # D5(iii)
S_STREAM = 1500
NAMES = C.player_name_lexicon()
CORPORA = {}
FAM = C.FAMILY[1:]  # n3, n4, content, content_n3 ('base' = the (a) columns)


def ident(utts):
    return C.formula_set_fast(utts, m=2), C.system_set_fast(utts, NAMES)


def insample_and_split(utts, with_systems=True):
    """[insample_a, insample_ab, splithalf_a, splithalf_ab] + in-sample family (FAM) + split-half family (FAM).
    Without systems the (a)+(b) values are NaN; the (a) values are identical either way."""
    F = C.formula_set_fast(utts, m=2)
    fin = C.family_arrays(utts, F)
    half = np.arange(len(utts)) % 2
    U0 = [u for u, h in zip(utts, half) if h == 0]
    U1 = [u for u, h in zip(utts, half) if h == 1]
    F0 = C.formula_set_fast(U0, m=2)
    F1 = C.formula_set_fast(U1, m=2)
    x = C.family_arrays(U1, F0)
    y = C.family_arrays(U0, F1)
    pn = x["tokens"].sum() + y["tokens"].sum()
    sp = {k: (x[k].sum() + y[k].sum()) / pn for k in C.FAMILY}
    ins = {k: C.ratio(fin[k], fin["tokens"]) for k in C.FAMILY}
    if with_systems:
        S = C.system_set_fast(utts, NAMES)
        n, ca, cab = C.densities(utts, F, S, NAMES)
        S0 = C.system_set_fast(U0, NAMES)
        S1 = C.system_set_fast(U1, NAMES)
        xb = C.densities(U1, F0, S0, NAMES)
        yb = C.densities(U0, F1, S1, NAMES)
        ab_in = C.ratio(cab, n)
        ab_sp = (xb[2].sum() + yb[2].sum()) / pn
    else:
        ab_in = ab_sp = float("nan")
    return [ins["base"], ab_in, sp["base"], ab_sp] + [ins[k] for k in FAM] + [sp[k] for k in FAM]


def _job_sub(args):
    corpus, target, seed = args[:3]
    with_systems = args[3] if len(args) > 3 else True
    utts = CORPORA[corpus]["utts"]
    rng = np.random.default_rng(seed)
    idx = C.subsample(utts, target, rng)
    return [corpus, target, seed] + insample_and_split([utts[i] for i in idx], with_systems)


def _job_heldout(args):
    """D5(ii) as pre-registered: M = random whole utterances (>= m_target tokens); I = random utterances of groups not touched
    by M, until >= i_target tokens or the eligible set is exhausted (revision 1: for Cornell it is exhausted at ~65k)."""
    corpus, i_target, m_target, seed = args
    utts = CORPORA[corpus]["utts"]
    groups = CORPORA[corpus]["groups"]
    rng = np.random.default_rng(seed)
    midx = C.subsample(utts, m_target, rng)
    mgroups = {groups[i] for i in midx}
    eligible = [i for i in range(len(utts)) if groups[i] not in mgroups]
    order = rng.permutation(len(eligible))
    iidx, tot = [], 0
    for k in order:
        iidx.append(eligible[k])
        tot += len(utts[eligible[k]])
        if tot >= i_target:
            break
    F, S = ident([utts[i] for i in iidx])
    M = [utts[i] for i in midx]
    n, ca, cab = C.densities(M, F, S, NAMES)
    fam = C.family_arrays(M, F)
    return [corpus, m_target, seed, C.ratio(ca, n), C.ratio(cab, n), int(n.sum()), tot, len(mgroups),
            sum(len(utts[i]) for i in eligible)] + [C.ratio(fam[k], fam["tokens"]) for k in FAM]


def _job_heldout_grouped(args):
    """D5(ii-b), revision 1 (post hoc): M concentrated in as few groups as possible (groups in random order, each group's
    utterances in random order, until >= m_target tokens), so that I (random utterances of all other groups) reaches
    i_target for Cornell too. For press answers M is then usually one interviewee, the analogue of TV's one-match M.
    (a) family only (no systems)."""
    corpus, i_target, m_target, seed = args
    utts = CORPORA[corpus]["utts"]
    groups = CORPORA[corpus]["groups"]
    rng = np.random.default_rng(seed)
    by_g = {}
    for i, g in enumerate(groups):
        by_g.setdefault(g, []).append(i)
    glist = sorted(by_g)
    midx, tot_m, mgroups = [], 0, set()
    for gi in rng.permutation(len(glist)):
        g = glist[gi]
        mgroups.add(g)
        members = by_g[g]
        for k in rng.permutation(len(members)):
            midx.append(members[k])
            tot_m += len(utts[members[k]])
            if tot_m >= m_target:
                break
        if tot_m >= m_target:
            break
    eligible = [i for i in range(len(utts)) if groups[i] not in mgroups]
    order = rng.permutation(len(eligible))
    iidx, tot = [], 0
    for k in order:
        iidx.append(eligible[k])
        tot += len(utts[eligible[k]])
        if tot >= i_target:
            break
    F = C.formula_set_fast([utts[i] for i in iidx], m=2)
    M = [utts[i] for i in midx]
    fam = C.family_arrays(M, F)
    return [corpus, m_target, seed, C.ratio(fam["base"], fam["tokens"]), int(fam["tokens"].sum()), tot, len(mgroups),
            sum(len(utts[i]) for i in eligible)] + [C.ratio(fam[k], fam["tokens"]) for k in FAM]


def _job_loo(args):
    stream, pool_names = args
    I = [r["toks"] for s in pool_names if s != stream for r in C.load_stream(s)]
    M = [r["toks"] for r in C.load_stream(stream)]
    F, S = ident(I)
    n, ca, cab = C.densities(M, F, S, NAMES)
    out = []
    for lab, num, sd in (("a", ca, 401), ("a+b", cab, 402)):
        est, lo, hi, _ = C.boot_ratio(num, n, B=B, seed=sd)
        out.append({"stream": stream, "design": "D4i_leave_one_stream_out", "measure": lab, "density": est, "ci_lo": lo,
                    "ci_hi": hi, "tokens_measured": int(n.sum()), "tokens_identification": sum(map(len, I))})
    return out


def main():
    import time
    rt = {}
    t_start = time.time()
    streams = C.tv_streams()
    pool_names = C.pool_streams()
    for s in streams:
        CORPORA[s] = {"utts": [r["toks"] for r in C.load_stream(s)], "groups": None}
    pool_recs = [r for s in pool_names for r in C.load_stream(s)]
    CORPORA["tv_pool_all"] = {"utts": [r["toks"] for r in pool_recs], "groups": [r["match_id"] for r in pool_recs]}
    trecs = C.load_stream(C.TEXT)
    CORPORA[C.TEXT] = {"utts": [r["toks"] for r in trecs], "groups": [C.cornell_group(r) for r in trecs]}
    press = C.load_press_answers()
    CORPORA["press_answers"] = {"utts": [r["toks"] for r in press], "groups": [r["group"] for r in press]}
    press_years = sorted({r["date"][:4] for r in press if r["date"][:4].isdigit()})
    tv_years = sorted({r["match_id"][:4] for r in pool_recs} | {C.load_stream(s)[0]["match_id"][:4] for s in (C.MAIN, C.HELDOUT)})
    T19 = sum(map(len, CORPORA[C.MAIN]["utts"]))
    TPOOL = sum(map(len, CORPORA["tv_pool_all"]["utts"]))
    print("targets", T19, TPOOL, flush=True)

    def tick(name, t0):
        rt[name] = round(time.time() - t0, 1)
        print(name, "done", rt[name], "s", flush=True)

    with Pool(4) as pool:
        # D4(i) leave-one-stream-out
        t0 = time.time()
        loo = pool.map(_job_loo, [(s, pool_names) for s in streams])
        rows = [x for lst in loo for x in lst]
        tick("D4i", t0)
        # D4(ii) per stream at 1,500 tokens, also text and press
        t0 = time.time()
        jobs = []
        for k, s in enumerate(streams + [C.TEXT, "press_answers"]):
            for r in range(R_SMALL_STREAM):
                jobs.append((s, S_STREAM, C.MASTER_SEED + 10000 * (k + 1) + r))
        small = pool.map(_job_sub, jobs, chunksize=20)
        tick("D4ii", t0)
        # D5(i) matched to 2019 size; systems only for the first R_MATCHED_SYSTEMS replicates (identical seeds to the original run)
        t0 = time.time()
        jobs = []
        for k, s in enumerate(["tv_pool_all", C.TEXT, "press_answers"]):
            for r in range(R_MATCHED):
                jobs.append((s, T19, C.MASTER_SEED + 500000 + 1000 * k + r, r < R_MATCHED_SYSTEMS))
        matched = pool.map(_job_sub, jobs, chunksize=5)
        tick("D5i", t0)
        # D5(iii) in-sample at pool size
        t0 = time.time()
        jobs = []
        for k, s in enumerate(["tv_pool_all", C.TEXT, "press_answers"]):
            for r in range(R_LARGE):
                jobs.append((s, TPOOL, C.MASTER_SEED + 600000 + 1000 * k + r))
        large = pool.map(_job_sub, jobs, chunksize=1)
        tick("D5iii", t0)
        # D5(ii) held-out, disjoint groups
        t0 = time.time()
        jobs = []
        for k, s in enumerate([C.TEXT, "press_answers"]):
            for r in range(R_HELDOUT):
                jobs.append((s, TPOOL, T19, C.MASTER_SEED + 700000 + 1000 * k + r))
        held = pool.map(_job_heldout, jobs, chunksize=1)
        tick("D5ii", t0)
        # D5(ii-b) held-out, M concentrated in few groups (revision 1, post hoc)
        t0 = time.time()
        jobs = []
        for k, s in enumerate([C.TEXT, "press_answers"]):
            for r in range(R_HELDOUT_GROUPED):
                jobs.append((s, TPOOL, T19, C.MASTER_SEED + 750000 + 1000 * k + r))
        heldg = pool.map(_job_heldout_grouped, jobs, chunksize=1)
        tick("D5ii_b", t0)

    # per-stream summary
    def summ(vals):
        v = np.array([x for x in vals if not np.isnan(x)], float)
        return float(v.mean()), float(np.percentile(v, 2.5)), float(np.percentile(v, 97.5)), len(v)
    by = {}
    for rec in small:
        by.setdefault(rec[0], []).append(rec[3:7])
    for s, vals in by.items():
        v = np.array(vals)
        for j, (design, lab) in enumerate((("D4ii_insample_1500", "a"), ("D4ii_insample_1500", "a+b"),
                                           ("D4ii_splithalf_1500", "a"), ("D4ii_splithalf_1500", "a+b"))):
            m, lo, hi, _ = summ(v[:, j])
            rows.append({"stream": s, "design": design, "measure": lab, "density": m, "ci_lo": lo, "ci_hi": hi,
                         "tokens_measured": S_STREAM, "tokens_identification": S_STREAM})
    with open(C.RESULTS / "density_streams.csv", "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0]))
        w.writeheader()
        for x in rows:
            w.writerow({k: (f"{v:.6f}" if isinstance(v, float) else v) for k, v in x.items()})

    fam_in = [f"insample_{k}" for k in FAM]
    fam_sp = [f"splithalf_{k}" for k in FAM]
    fam_ho = [f"heldout_{k}" for k in FAM]
    fields = ["design", "corpus", "target_tokens", "seed", "insample_a", "insample_ab", "splithalf_a", "splithalf_ab"] + fam_in + fam_sp + \
             ["heldout_a", "heldout_ab"] + fam_ho + ["tokens_measured", "tokens_identification", "groups_in_measurement",
                                                     "tokens_eligible_for_identification"]

    def fmt(x):
        if isinstance(x, float):
            return "" if np.isnan(x) else f"{x:.6f}"
        return x
    with open(C.RESULTS / "medium_replicates.csv", "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=fields)
        w.writeheader()
        for design, recs_ in (("D5i_matched_2019_size", matched), ("D5iii_insample_pool_size", large)):
            for rec in recs_:
                d = dict(zip(["corpus", "target_tokens", "seed", "insample_a", "insample_ab", "splithalf_a", "splithalf_ab"] + fam_in + fam_sp, rec))
                w.writerow({k: fmt(v) for k, v in {"design": design, **d}.items()})
        for rec in held:
            d = dict(zip(["corpus", "target_tokens", "seed", "heldout_a", "heldout_ab", "tokens_measured", "tokens_identification",
                          "groups_in_measurement", "tokens_eligible_for_identification"] + fam_ho, rec))
            w.writerow({k: fmt(v) for k, v in {"design": "D5ii_heldout_disjoint_groups", **d}.items()})
        for rec in heldg:
            d = dict(zip(["corpus", "target_tokens", "seed", "heldout_a", "tokens_measured", "tokens_identification",
                          "groups_in_measurement", "tokens_eligible_for_identification"] + fam_ho, rec))
            w.writerow({k: fmt(v) for k, v in {"design": "D5iib_heldout_grouped_M", **d}.items()})
    med = []
    nf = len(FAM)
    for design, recs_, cols in (("D5i_matched_2019_size", matched, [("insample", 3, 4, 7), ("splithalf", 5, 6, 7 + nf)]),
                                ("D5iii_insample_pool_size", large, [("insample", 3, 4, 7)])):
        for corpus in ["tv_pool_all", C.TEXT, "press_answers"]:
            sel = [r for r in recs_ if r[0] == corpus]
            for name, ja, jab, jf in cols:
                for lab, j in [("a", ja), ("a+b", jab)] + [(k, jf + i) for i, k in enumerate(FAM)]:
                    m, lo, hi, nrep = summ([r[j] for r in sel])
                    med.append({"design": design, "corpus": corpus, "estimate": name, "measure": lab, "mean": m,
                                "p2_5": lo, "p97_5": hi, "replicates": nrep})
    for design, recs_, idx in (("D5ii_heldout_disjoint_groups", held, [("a", 3), ("a+b", 4)] + [(k, 9 + i) for i, k in enumerate(FAM)]),
                               ("D5iib_heldout_grouped_M", heldg, [("a", 3)] + [(k, 8 + i) for i, k in enumerate(FAM)])):
        for corpus in [C.TEXT, "press_answers"]:
            sel = [r for r in recs_ if r[0] == corpus]
            for lab, j in idx:
                m, lo, hi, nrep = summ([r[j] for r in sel])
                med.append({"design": design, "corpus": corpus, "estimate": "heldout", "measure": lab,
                            "mean": m, "p2_5": lo, "p97_5": hi, "replicates": nrep})
    with open(C.RESULTS / "density_medium.csv", "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(med[0]))
        w.writeheader()
        for x in med:
            w.writerow({k: (f"{v:.6f}" if isinstance(v, float) else v) for k, v in x.items()})

    def size_stats(recs_, j_ident, j_groups, j_elig):
        out = {}
        for corpus in [C.TEXT, "press_answers"]:
            sel = [r for r in recs_ if r[0] == corpus]
            ti = np.array([r[j_ident] for r in sel])
            gm = np.array([r[j_groups] for r in sel])
            el = np.array([r[j_elig] for r in sel])
            out[corpus] = {"tokens_identification_min": int(ti.min()), "tokens_identification_median": float(np.median(ti)),
                           "tokens_identification_max": int(ti.max()), "groups_in_measurement_median": float(np.median(gm)),
                           "groups_in_measurement_min": int(gm.min()), "groups_in_measurement_max": int(gm.max()),
                           "tokens_eligible_median": float(np.median(el)), "replicates": len(sel)}
        return out
    rt["total"] = round(time.time() - t_start, 1)
    C.write_json(C.RESULTS / "density_medium_meta.json", {
        "target_matched_tokens": T19, "target_pool_tokens": TPOOL, "S_stream": S_STREAM,
        "R_small_stream": R_SMALL_STREAM, "R_matched": R_MATCHED, "R_matched_systems": R_MATCHED_SYSTEMS,
        "R_heldout": R_HELDOUT, "R_heldout_grouped": R_HELDOUT_GROUPED, "R_large": R_LARGE,
        "press_answers": len(CORPORA["press_answers"]["utts"]),
        "press_tokens": sum(map(len, CORPORA["press_answers"]["utts"])),
        "press_interviewees": len(set(CORPORA["press_answers"]["groups"])),
        "press_years": [press_years[0], press_years[-1]] if press_years else None,
        "tv_years": [tv_years[0], tv_years[-1]],
        "cornell_updates": len(CORPORA[C.TEXT]["utts"]), "cornell_tokens": sum(map(len, CORPORA[C.TEXT]["utts"])),
        "cornell_player_pair_groups": len(set(CORPORA[C.TEXT]["groups"])),
        "mean_tokens_per_utterance": {k: float(np.mean([len(u) for u in CORPORA[k]["utts"]]))
                                      for k in ["tv_pool_all", C.MAIN, C.HELDOUT, C.TEXT, "press_answers"]},
        "D5ii_identification_size": size_stats(held, 6, 7, 8),
        "D5iib_identification_size": size_stats(heldg, 5, 6, 7),
        "runtime_seconds": rt, "cpus": 4,
    })
    print("done", rt)


if __name__ == "__main__":
    main()
