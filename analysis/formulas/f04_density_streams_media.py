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
R_MATCHED = 200        # D5(i), 2019-size
R_HELDOUT = 50         # D5(ii)
R_LARGE = 20           # D5(iii)
S_STREAM = 1500
NAMES = C.player_name_lexicon()
CORPORA = {}


def ident(utts):
    return C.formula_set_fast(utts, m=2), C.system_set_fast(utts, NAMES)


def insample_and_split(utts):
    F, S = ident(utts)
    n, ca, cab = C.densities(utts, F, S, NAMES)
    half = np.arange(len(utts)) % 2
    U0 = [u for u, h in zip(utts, half) if h == 0]
    U1 = [u for u, h in zip(utts, half) if h == 1]
    F0, S0 = ident(U0)
    F1, S1 = ident(U1)
    x = C.densities(U1, F0, S0, NAMES)
    y = C.densities(U0, F1, S1, NAMES)
    pn = x[0].sum() + y[0].sum()
    return [C.ratio(ca, n), C.ratio(cab, n), (x[1].sum() + y[1].sum()) / pn, (x[2].sum() + y[2].sum()) / pn]


def _job_sub(args):
    corpus, target, seed = args
    utts = CORPORA[corpus]["utts"]
    rng = np.random.default_rng(seed)
    idx = C.subsample(utts, target, rng)
    return [corpus, target, seed] + insample_and_split([utts[i] for i in idx])


def _job_heldout(args):
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
    n, ca, cab = C.densities([utts[i] for i in midx], F, S, NAMES)
    return [corpus, m_target, seed, C.ratio(ca, n), C.ratio(cab, n), int(n.sum()), tot, len(mgroups)]


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
    T19 = sum(map(len, CORPORA[C.MAIN]["utts"]))
    TPOOL = sum(map(len, CORPORA["tv_pool_all"]["utts"]))
    print("targets", T19, TPOOL, flush=True)

    with Pool(4) as pool:
        # D4(i) leave-one-stream-out
        loo = pool.map(_job_loo, [(s, pool_names) for s in streams])
        rows = [x for lst in loo for x in lst]
        print("D4i done", flush=True)
        # D4(ii) per stream at 1,500 tokens, also text and press
        jobs = []
        for k, s in enumerate(streams + [C.TEXT, "press_answers"]):
            for r in range(R_SMALL_STREAM):
                jobs.append((s, S_STREAM, C.MASTER_SEED + 10000 * (k + 1) + r))
        small = pool.map(_job_sub, jobs, chunksize=20)
        print("D4ii done", flush=True)
        # D5(i) matched to 2019 size
        jobs = []
        for k, s in enumerate(["tv_pool_all", C.TEXT, "press_answers"]):
            for r in range(R_MATCHED):
                jobs.append((s, T19, C.MASTER_SEED + 500000 + 1000 * k + r))
        matched = pool.map(_job_sub, jobs, chunksize=5)
        print("D5i done", flush=True)
        # D5(iii) in-sample at pool size
        jobs = []
        for k, s in enumerate(["tv_pool_all", C.TEXT, "press_answers"]):
            for r in range(R_LARGE):
                jobs.append((s, TPOOL, C.MASTER_SEED + 600000 + 1000 * k + r))
        large = pool.map(_job_sub, jobs, chunksize=1)
        print("D5iii done", flush=True)
        # D5(ii) held-out, disjoint groups
        jobs = []
        for k, s in enumerate([C.TEXT, "press_answers"]):
            for r in range(R_HELDOUT):
                jobs.append((s, TPOOL, T19, C.MASTER_SEED + 700000 + 1000 * k + r))
        held = pool.map(_job_heldout, jobs, chunksize=1)
        print("D5ii done", flush=True)

    # per-stream summary
    def summ(vals):
        v = np.array(vals, float)
        return float(v.mean()), float(np.percentile(v, 2.5)), float(np.percentile(v, 97.5))
    by = {}
    for rec in small:
        by.setdefault(rec[0], []).append(rec[3:])
    for s, vals in by.items():
        v = np.array(vals)
        for j, (design, lab) in enumerate((("D4ii_insample_1500", "a"), ("D4ii_insample_1500", "a+b"),
                                           ("D4ii_splithalf_1500", "a"), ("D4ii_splithalf_1500", "a+b"))):
            m, lo, hi = summ(v[:, j])
            rows.append({"stream": s, "design": design, "measure": lab, "density": m, "ci_lo": lo, "ci_hi": hi,
                         "tokens_measured": S_STREAM, "tokens_identification": S_STREAM})
    with open(C.RESULTS / "density_streams.csv", "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0]))
        w.writeheader()
        for x in rows:
            w.writerow({k: (f"{v:.6f}" if isinstance(v, float) else v) for k, v in x.items()})
    with open(C.RESULTS / "medium_replicates.csv", "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["design", "corpus", "target_tokens", "seed", "insample_a", "insample_ab", "splithalf_a", "splithalf_ab",
                    "heldout_a", "heldout_ab", "tokens_measured", "tokens_identification", "groups_in_measurement"])
        for rec in matched:
            w.writerow(["D5i_matched_2019_size"] + rec[:3] + [f"{x:.6f}" for x in rec[3:]] + ["", "", "", "", ""])
        for rec in large:
            w.writerow(["D5iii_insample_pool_size"] + rec[:3] + [f"{x:.6f}" for x in rec[3:]] + ["", "", "", "", ""])
        for rec in held:
            w.writerow(["D5ii_heldout_disjoint_groups", rec[0], rec[1], rec[2], "", "", "", "", f"{rec[3]:.6f}", f"{rec[4]:.6f}",
                        rec[5], rec[6], rec[7]])
    med = []
    for design, recs_, cols in (("D5i_matched_2019_size", matched, [("insample", 3, 4), ("splithalf", 5, 6)]),
                                ("D5iii_insample_pool_size", large, [("insample", 3, 4)])):
        for corpus in ["tv_pool_all", C.TEXT, "press_answers"]:
            sel = [r for r in recs_ if r[0] == corpus]
            for name, ja, jab in cols:
                for lab, j in (("a", ja), ("a+b", jab)):
                    m, lo, hi = summ([r[j] for r in sel])
                    med.append({"design": design, "corpus": corpus, "estimate": name, "measure": lab, "mean": m,
                                "p2_5": lo, "p97_5": hi, "replicates": len(sel)})
    for corpus in [C.TEXT, "press_answers"]:
        sel = [r for r in held if r[0] == corpus]
        for lab, j in (("a", 3), ("a+b", 4)):
            m, lo, hi = summ([r[j] for r in sel])
            med.append({"design": "D5ii_heldout_disjoint_groups", "corpus": corpus, "estimate": "heldout", "measure": lab,
                        "mean": m, "p2_5": lo, "p97_5": hi, "replicates": len(sel)})
    with open(C.RESULTS / "density_medium.csv", "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(med[0]))
        w.writeheader()
        for x in med:
            w.writerow({k: (f"{v:.6f}" if isinstance(v, float) else v) for k, v in x.items()})
    C.write_json(C.RESULTS / "density_medium_meta.json", {
        "target_matched_tokens": T19, "target_pool_tokens": TPOOL, "S_stream": S_STREAM,
        "R_small_stream": R_SMALL_STREAM, "R_matched": R_MATCHED, "R_heldout": R_HELDOUT, "R_large": R_LARGE,
        "press_answers": len(CORPORA["press_answers"]["utts"]),
        "press_tokens": sum(map(len, CORPORA["press_answers"]["utts"])),
        "press_interviewees": len(set(CORPORA["press_answers"]["groups"])),
        "cornell_updates": len(CORPORA[C.TEXT]["utts"]), "cornell_tokens": sum(map(len, CORPORA[C.TEXT]["utts"])),
        "cornell_player_pair_groups": len(set(CORPORA[C.TEXT]["groups"])),
        "mean_tokens_per_utterance": {k: float(np.mean([len(u) for u in CORPORA[k]["utts"]]))
                                      for k in ["tv_pool_all", C.MAIN, C.HELDOUT, C.TEXT, "press_answers"]},
    })
    print("done")


if __name__ == "__main__":
    main()
