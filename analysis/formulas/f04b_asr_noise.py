"""POST HOC EXPLORATORY (added after C1/C2 were seen; see plan.md addendum): can ASR noise explain why TV commentary is
less formulaic than press answers and written live text? Inject substitution noise into the comparison corpora (and extra
noise into the TV corpora) and recompute split-half and held-out (a) density.

Noise model: each token is replaced, independently with probability e, by a token drawn from the unigram distribution of
the 18-match TV pool (substitutions only; no insertions or deletions). Noise is applied to both I and M.
Outputs: results/asr_noise_sensitivity.csv
Run: python -I analysis/formulas/f04b_asr_noise.py
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import csv
import json
from collections import Counter
from multiprocessing import Pool
import numpy as np
import common as C

R_SPLIT = 50
R_HELD = 10
CORP = {}
UNI = {}


def noisy(utts, e, rng):
    if e <= 0:
        return utts
    words, probs = UNI["w"], UNI["p"]
    out = []
    for u in utts:
        m = rng.random(len(u)) < e
        if m.any():
            repl = rng.choice(len(words), size=int(m.sum()), p=probs)
            v = list(u)
            for k, i in enumerate(np.where(m)[0]):
                v[i] = words[repl[k]]
            out.append(v)
        else:
            out.append(u)
    return out


def dens_a(I, M):
    F = C.formula_set_fast(I, m=2)
    n = sum(len(u) for u in M)
    cov = sum(int((C.cover_a(u, F) > 0).sum()) for u in M)
    return cov / n


def _split(args):
    corpus, e, seed, target = args
    rng = np.random.default_rng(seed)
    utts = CORP[corpus]["utts"]
    idx = C.subsample(utts, target, rng)
    U = noisy([utts[i] for i in idx], e, rng)
    U0, U1 = U[0::2], U[1::2]
    F0 = C.formula_set_fast(U0, m=2)
    F1 = C.formula_set_fast(U1, m=2)
    n = sum(map(len, U))
    cov = sum(int((C.cover_a(u, F0) > 0).sum()) for u in U1) + sum(int((C.cover_a(u, F1) > 0).sum()) for u in U0)
    return ["splithalf_matched", corpus, e, seed, cov / n]


def _held(args):
    corpus, e, seed, i_target, m_target = args
    rng = np.random.default_rng(seed)
    if corpus == "tv_pool_to_2019":
        I = noisy(CORP["tv_pool_all"]["utts"], e, rng)
        M = noisy(CORP[C.MAIN]["utts"], e, rng)
        return ["heldout", corpus, e, seed, dens_a(I, M)]
    utts = CORP[corpus]["utts"]
    groups = CORP[corpus]["groups"]
    midx = C.subsample(utts, m_target, rng)
    mg = {groups[i] for i in midx}
    elig = [i for i in range(len(utts)) if groups[i] not in mg]
    order = rng.permutation(len(elig))
    iidx, tot = [], 0
    for k in order:
        iidx.append(elig[k])
        tot += len(utts[elig[k]])
        if tot >= i_target:
            break
    I = noisy([utts[i] for i in iidx], e, rng)
    M = noisy([utts[i] for i in midx], e, rng)
    return ["heldout", corpus, e, seed, dens_a(I, M)]


def main():
    asr = json.loads((C.ROOT / "corpus" / "reports" / "asr_proxy.json").read_text())
    e_lb = asr["hand_sample"]["total_per_1000_words"] / 1000.0
    levels = [0.0, round(e_lb, 4), 0.05, 0.10, 0.15]
    pool_recs = [r for s in C.pool_streams() for r in C.load_stream(s)]
    CORP["tv_pool_all"] = {"utts": [r["toks"] for r in pool_recs], "groups": [r["match_id"] for r in pool_recs]}
    CORP[C.MAIN] = {"utts": [r["toks"] for r in C.load_stream(C.MAIN)], "groups": None}
    tr = C.load_stream(C.TEXT)
    CORP[C.TEXT] = {"utts": [r["toks"] for r in tr], "groups": [C.cornell_group(r) for r in tr]}
    pr = C.load_press_answers()
    CORP["press_answers"] = {"utts": [r["toks"] for r in pr], "groups": [r["group"] for r in pr]}
    cnt = Counter(t for u in CORP["tv_pool_all"]["utts"] for t in u)
    UNI["w"] = list(cnt)
    tot = sum(cnt.values())
    UNI["p"] = np.array([cnt[w] / tot for w in UNI["w"]])
    T19 = sum(map(len, CORP[C.MAIN]["utts"]))
    TP = sum(map(len, CORP["tv_pool_all"]["utts"]))
    jobs_s, jobs_h = [], []
    for ci_, corpus in enumerate(["tv_pool_all", C.TEXT, "press_answers"]):
        for li, e in enumerate(levels):
            for r in range(R_SPLIT):
                jobs_s.append((corpus, e, C.MASTER_SEED + 800000 + 10000 * ci_ + 100 * li + r, T19))
    for ci_, corpus in enumerate(["tv_pool_to_2019", C.TEXT, "press_answers"]):
        for li, e in enumerate(levels[1:], 1):
            for r in range(R_HELD):
                jobs_h.append((corpus, e, C.MASTER_SEED + 900000 + 10000 * ci_ + 100 * li + r, TP, T19))
    with Pool(4) as pool:
        res = pool.map(_split, jobs_s, chunksize=5) + pool.map(_held, jobs_h, chunksize=1)
    with open(C.RESULTS / "asr_noise_sensitivity.csv", "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["design", "corpus", "added_substitution_rate", "seed", "density_a"])
        for r in res:
            w.writerow(r[:4] + [f"{r[4]:.6f}"])
    summ = {}
    for design, corpus, e in sorted({(r[0], r[1], r[2]) for r in res}):
        v = np.array([r[4] for r in res if r[0] == design and r[1] == corpus and r[2] == e])
        summ[f"{design}|{corpus}|{e}"] = {"mean": float(v.mean()), "p2_5": float(np.percentile(v, 2.5)),
                                          "p97_5": float(np.percentile(v, 97.5)), "replicates": len(v)}
    C.write_json(C.RESULTS / "asr_noise_summary.json", {"levels": levels, "hand_read_lower_bound_rate": e_lb,
                                                         "R_split": R_SPLIT, "R_held": R_HELD, "cells": summ})
    for k, v in summ.items():
        print(k, round(v["mean"], 4))


if __name__ == "__main__":
    main()
