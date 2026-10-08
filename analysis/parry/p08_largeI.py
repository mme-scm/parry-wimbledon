"""POST HOC (plan.md addendum 1, A1): cross-corpus comparison with a large identification set, and the TV-only n >= 3 stock.

Targets: each of the 20 TV streams (whole text). Sources, each subsampled to I = 100,000 tokens (whole utterances): the other 19 TV streams
pooled, Cornell live text, press answers pooled; R = 5 subsamples per source x target. Inventory = n-grams 2..12 in >= 2 utterances of the
subsample (not stop-only). Coverage of the target at n >= 2 / n >= 3, observed and unigram-shuffled (target and source shuffled once per
replicate), all tokens and commentary-only (tokens inside common.official_mask_v2 patterns dropped; observed only). 2b normalisation
(primary) and raw tokens.
TV-only n >= 3 stock (2b normalisation): target tokens covered by an n >= 3 n-gram of the TV inventory that is in neither the Cornell nor
the press inventory of the same replicate; stricter readings: 'strict' (the n-gram is also not a formula of the whole Cornell text or of
the whole press corpus) and 'cross-broadcast' (the n-gram occurs in >= 2 of the other 19 TV streams). Slot composition by
SlotClassifier.classify(span) on the longest covering occurrence.

Outputs (results/): largeI_coverage.csv, largeI_summary.csv, largeI_tvonly_by_target.csv, largeI_tvonly_slots.csv,
largeI_tvonly_types_finals.csv, largeI_tvonly_types_pooled.csv, largeI_meta.json
Run: python -I analysis/parry/p08_largeI.py
"""
import sys
import time
from collections import Counter, defaultdict
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from multiprocessing import Pool
import numpy as np
import lib2b as L

I_SIZE, R, B = 100000, 5, 10000
OUT = L.RESULTS
SOURCES = ("tv_other19", "cornell", "press_pooled")
BASELINES = ("cornell", "press_pooled")
TOKVARS = ("norm", "raw")
NMAX = 12
TEAMS = {}
KEEP = {}          # stream -> list of bool arrays (True = outside umpire/score-call patterns)
PRESS_CHUNKS = []
CAND = set()
CAND_FIRST = set()


def cov_stats(utts, F, keep=None):
    n = c2 = c3 = 0
    nk = k2 = k3 = 0
    for ui, u in enumerate(utts):
        mx = L.C.cover_a(u, F)
        n += len(u)
        c2 += int((mx >= 2).sum())
        c3 += int((mx >= 3).sum())
        if keep is not None:
            kp = keep[ui]
            nk += int(kp.sum())
            k2 += int(((mx >= 2) & kp).sum())
            k3 += int(((mx >= 3) & kp).sum())
    out = {"n2": c2 / n, "n3": c3 / n, "tokens": n}
    if keep is not None:
        out.update({"n2_comm": k2 / nk if nk else float("nan"), "n3_comm": k3 / nk if nk else float("nan"), "tokens_comm": nk})
    return out


def job(args):
    j, r, tok = args
    tgt = L.TV[j]
    rng = np.random.default_rng([L.SEED, 108, j, r, TOKVARS.index(tok)])
    get = (lambda t: t.norm) if tok == "norm" else (lambda t: t.raw)
    M = get(TEAMS[tgt])
    Ms = L.shuffle_utts(M, rng)
    rows, invs = [], {}
    for src in SOURCES:
        I = [u for s in L.TV if s != tgt for u in get(TEAMS[s])] if src == "tv_other19" else get(TEAMS[src])
        idx = L.subsample(I, I_SIZE, rng)
        Iu = [I[i] for i in idx]
        F = L.C.formula_set_fast(Iu, m=2)
        Fs = L.C.formula_set_fast(L.shuffle_utts(Iu, rng), m=2)
        o = cov_stats(M, F, KEEP[tgt])
        s = cov_stats(Ms, Fs)
        rows.append({"tokens": tok, "source": src, "target": tgt, "r": r, "I_tokens": sum(len(u) for u in Iu), "F_types": len(F),
                     "F_types_n3": sum(1 for g in F if len(g) >= 3), "Fs_types": len(Fs), "M_tokens": o["tokens"], "M_tokens_comm": o["tokens_comm"],
                     "obs_n2": o["n2"], "obs_n3": o["n3"], "shuf_n2": s["n2"], "shuf_n3": s["n3"], "obs_n2_comm": o["n2_comm"],
                     "obs_n3_comm": o["n3_comm"]})
        invs[src] = F
    occ = []
    if tok == "norm":
        Ft, Fc, Fp = invs["tv_other19"], invs["cornell"], invs["press_pooled"]
        for ui, u in enumerate(M):
            Lu = len(u)
            for n in range(3, min(NMAX, Lu) + 1):
                for i in range(Lu - n + 1):
                    g = tuple(u[i:i + n])
                    if g in Ft:
                        occ.append((ui, i, n, g, g in Fc, g in Fp))
    return j, r, tok, rows, occ


def _scan(utts, cand, first, lens):
    """(utterance counts, occurrence counts): g -> number of distinct utterances of utts containing g, and of occurrences (g in cand)."""
    cnt, occ = Counter(), Counter()
    for u in utts:
        Lu = len(u)
        seen = set()
        for i in range(Lu):
            if u[i] not in first:
                continue
            for n in lens:
                if i + n > Lu:
                    break
                g = tuple(u[i:i + n])
                if g in cand:
                    seen.add(g)
                    occ[g] += 1
        cnt.update(seen)
    return cnt, occ


def _scan_chunk(k):
    return _scan(PRESS_CHUNKS[k], CAND, CAND_FIRST, range(3, NMAX + 1))


def boot_mean(v, rng, B_=B):
    v = np.asarray(v, float)
    d = np.array([v[rng.integers(0, len(v), len(v))].mean() for _ in range(B_)])
    return float(v.mean()), float(np.percentile(d, 2.5)), float(np.percentile(d, 97.5))


def main():
    global TEAMS, KEEP, PRESS_CHUNKS, CAND, CAND_FIRST
    t0 = time.time()
    for s in L.TV:
        TEAMS[s] = L.load_tv(s)
        KEEP[s] = [L.C.official_mask_v2(u, L.NAMES) for u in TEAMS[s].raw]
    TEAMS["cornell"] = L.load_cornell()
    TEAMS["press_pooled"] = L.load_press(None)
    print("loaded", round(time.time() - t0, 1), "s", flush=True)
    jobs = [(j, r, tok) for tok in TOKVARS for j in range(len(L.TV)) for r in range(R)]
    with Pool(4) as pool:
        res = pool.map(job, jobs, chunksize=1)
    t_jobs = time.time() - t0
    print("jobs done", round(t_jobs, 1), "s", flush=True)
    cov_rows = [row for _, _, _, rows, _ in res for row in rows]
    L.write_csv(OUT / "largeI_coverage.csv", cov_rows)

    # ---------------------------------------------------------------- summary: sources and TV-minus-baseline differences
    rng = np.random.default_rng([L.SEED, 109])
    per = defaultdict(lambda: defaultdict(list))   # (tok, src, target) -> measure -> values over r
    for row in cov_rows:
        for m in ("obs_n2", "obs_n3", "shuf_n2", "shuf_n3", "obs_n2_comm", "obs_n3_comm", "F_types", "F_types_n3"):
            per[(row["tokens"], row["source"], row["target"])][m].append(float(row[m]))
    tmean = {k: {m: float(np.mean(v)) for m, v in d.items()} for k, d in per.items()}
    for k, d in tmean.items():
        d["exc_n2"] = d["obs_n2"] - d["shuf_n2"]
        d["exc_n3"] = d["obs_n3"] - d["shuf_n3"]
    summ = []
    MEAS = ("obs_n2", "obs_n3", "shuf_n2", "shuf_n3", "exc_n2", "exc_n3", "obs_n2_comm", "obs_n3_comm")
    for tok in TOKVARS:
        for src in SOURCES:
            for m in MEAS + ("F_types", "F_types_n3"):
                v = [tmean[(tok, src, t)][m] for t in L.TV]
                est, lo, hi = boot_mean(v, rng, 2000)
                summ.append({"tokens": tok, "statistic": f"{src} -> TV", "measure": m, "estimate": est, "ci_lo": lo, "ci_hi": hi,
                             "targets_positive": "", "n_targets": len(v), "min_over_targets": min(v), "max_over_targets": max(v),
                             "uncertainty": "percentile bootstrap over the 20 targets, B = 2000"})
        for b in BASELINES:
            for m in MEAS:
                d = [tmean[(tok, "tv_other19", t)][m] - tmean[(tok, b, t)][m] for t in L.TV]
                est, lo, hi = boot_mean(d, rng)
                summ.append({"tokens": tok, "statistic": f"TV minus {b}", "measure": m, "estimate": est, "ci_lo": lo, "ci_hi": hi,
                             "targets_positive": int(sum(x > 0 for x in d)), "n_targets": len(d), "min_over_targets": min(d),
                             "max_over_targets": max(d), "uncertainty": f"percentile bootstrap over the 20 targets, B = {B}"})
    L.write_csv(OUT / "largeI_summary.csv", summ)

    # ---------------------------------------------------------------- TV-only stock: candidates and their attestation elsewhere
    occ_by = defaultdict(dict)   # target -> r -> occ list
    for j, r, tok, _, occ in res:
        if tok == "norm":
            occ_by[L.TV[j]][r] = occ
    CAND = {o[3] for t in occ_by for r in occ_by[t] for o in occ_by[t][r] if not (o[4] or o[5])}
    CAND_FIRST = {g[0] for g in CAND}
    t1 = time.time()
    corn_utts, corn_occ = _scan(TEAMS["cornell"].norm, CAND, CAND_FIRST, range(3, NMAX + 1))
    pn = TEAMS["press_pooled"].norm
    k = (len(pn) + 7) // 8
    PRESS_CHUNKS = [pn[a:a + k] for a in range(0, len(pn), k)]
    with Pool(4) as pool:
        parts = pool.map(_scan_chunk, range(len(PRESS_CHUNKS)))
    press_utts, press_occ = Counter(), Counter()
    for pu, po in parts:
        press_utts.update(pu)
        press_occ.update(po)
    tv_streams_with = defaultdict(set)
    tv_occ = {}
    for s in L.TV:
        su, so = _scan(TEAMS[s].norm, CAND, CAND_FIRST, range(3, NMAX + 1))
        tv_occ[s] = so
        for g in su:
            tv_streams_with[g].add(s)
    tv_tok = {s: TEAMS[s].ntok for s in L.TV}
    rate_c = lambda g: 1e5 * corn_occ.get(g, 0) / TEAMS["cornell"].ntok
    rate_p = lambda g: 1e5 * press_occ.get(g, 0) / TEAMS["press_pooled"].ntok

    def rate_tv(g, excl=None):
        ss = [s for s in L.TV if s != excl]
        return 1e5 * sum(tv_occ[s].get(g, 0) for s in ss) / sum(tv_tok[s] for s in ss)
    t_scan = time.time() - t1
    strict = {g for g in CAND if corn_utts.get(g, 0) < 2 and press_utts.get(g, 0) < 2}

    # ---------------------------------------------------------------- token classes, slot composition, type lists
    by_target, slot_rows = [], []
    slot_pool = {cls: Counter() for cls in ("tv_only", "shared", "tv_only_strict", "tv_only_cross")}
    types_final = []
    types_pool = defaultdict(lambda: {"targets": 0, "occurrences": 0, "slots": Counter()})
    for t in L.TV:
        raw = TEAMS[t].raw
        keep = KEEP[t]
        ntok = sum(len(u) for u in raw)
        nkeep = int(sum(k_.sum() for k_ in keep))
        cls_cache, span_cache = {}, {}

        def slot_of(ui, a, b):
            key = (ui, a, b)
            v = span_cache.get(key)
            if v is None:
                c = cls_cache.get(ui)
                if c is None:
                    c = cls_cache[ui] = L.SlotClassifier(raw[ui])
                v = span_cache[key] = c.classify(a, b)
            return v
        acc = defaultdict(list)
        slots_t = {cls: Counter() for cls in slot_pool}
        only_reps = Counter()
        for r in range(R):
            occ = occ_by[t][r]
            cov_any = [np.zeros(len(u), bool) for u in raw]
            cov_sh = [np.zeros(len(u), bool) for u in raw]
            cov_noC = [np.ones(len(u), bool) for u in raw]      # no covering occurrence is in the Cornell inventory
            cov_noP = [np.ones(len(u), bool) for u in raw]
            nonstrict = [np.zeros(len(u), bool) for u in raw]  # covered by a TV-only n-gram that is not strict
            noncross = [np.zeros(len(u), bool) for u in raw]   # covered by a TV-only n-gram attested in < 2 other TV streams
            best_only = [dict() for _ in raw]                  # token -> (n, -i) of the longest leftmost TV-only occurrence
            best_sh = [dict() for _ in raw]
            seen_only = set()
            for ui, i, n, g, inC, inP in occ:
                sl = slice(i, i + n)
                cov_any[ui][sl] = True
                if inC:
                    cov_noC[ui][sl] = False
                if inP:
                    cov_noP[ui][sl] = False
                if inC or inP:
                    cov_sh[ui][sl] = True
                    bd = best_sh[ui]
                else:
                    seen_only.add(g)
                    if g not in strict:
                        nonstrict[ui][sl] = True
                    if len(tv_streams_with[g] - {t}) < 2:
                        noncross[ui][sl] = True
                    bd = best_only[ui]
                for q in range(i, i + n):
                    if q not in bd or (n, -i) > bd[q][0]:
                        bd[q] = ((n, -i), (i, i + n))
            for g in seen_only:
                only_reps[g] += 1
            tot = {k_: 0 for k_ in ("any", "shared", "only", "strict", "cross", "notC", "notP")}
            totk = dict(tot)
            for ui, u in enumerate(raw):
                anyv, sh = cov_any[ui], cov_sh[ui]
                only = anyv & ~sh
                stv = only & ~nonstrict[ui]
                crv = only & ~noncross[ui]
                notC = anyv & cov_noC[ui]
                notP = anyv & cov_noP[ui]
                kp = keep[ui]
                for k_, v in (("any", anyv), ("shared", sh), ("only", only), ("strict", stv), ("cross", crv), ("notC", notC), ("notP", notP)):
                    tot[k_] += int(v.sum())
                    totk[k_] += int((v & kp).sum())
                for q in np.where(only)[0]:
                    sp = best_only[ui][int(q)][1]
                    s_ = slot_of(ui, *sp)
                    slots_t["tv_only"][s_] += 1
                    slots_t["tv_only"]["_umpire_mask"] += int(not kp[q])
                    if stv[q]:
                        slots_t["tv_only_strict"][s_] += 1
                        slots_t["tv_only_strict"]["_umpire_mask"] += int(not kp[q])
                    if crv[q]:
                        slots_t["tv_only_cross"][s_] += 1
                        slots_t["tv_only_cross"]["_umpire_mask"] += int(not kp[q])
                for q in np.where(sh)[0]:
                    sp = best_sh[ui][int(q)][1]
                    slots_t["shared"][slot_of(ui, *sp)] += 1
                    slots_t["shared"]["_umpire_mask"] += int(not kp[q])
            for k_ in tot:
                acc[k_].append(tot[k_] / ntok)
                acc[k_ + "_comm"].append(totk[k_] / nkeep)
        row = {"target": t, "label": L.short(t), "tokens": ntok, "tokens_comm": nkeep, "R": R}
        for k_, v in acc.items():
            row[f"share_{k_}"] = float(np.mean(v))
        by_target.append(row)
        for cls, c in slots_t.items():
            tot_c = sum(v for kk, v in c.items() if not kk.startswith("_"))
            for sl in list(L.SLOTS) + ["_umpire_mask"]:
                slot_rows.append({"target": t, "label": L.short(t), "class": cls, "slot": sl, "tokens_summed_over_R": c.get(sl, 0),
                                  "share_of_class": c.get(sl, 0) / tot_c if tot_c else float("nan")})
            slot_pool[cls].update(c)
        # type lists: n-grams TV-only in a majority of the R replicates (>= 3 of 5)
        occ_cnt = Counter()
        occ_slot = defaultdict(Counter)
        allocc = {}
        for r in range(R):
            for ui, i, n, g, inC, inP in occ_by[t][r]:
                allocc[(ui, i, n)] = g
        for (ui, i, n), g in allocc.items():
            occ_cnt[g] += 1
            occ_slot[g][slot_of(ui, i, i + n)] += 1
        maj = [g for g, k_ in only_reps.items() if 2 * k_ > R]   # TV-only in a majority of the R replicates
        for g in maj:
            tp = types_pool[g]
            tp["targets"] += 1
            tp["occurrences"] += occ_cnt[g]
            tp["slots"].update(occ_slot[g])
            if t in (L.MAIN, L.HELDOUT):
                ms, mc = occ_slot[g].most_common(1)[0]
                types_final.append({"target": t, "label": L.short(t), "ngram": " ".join(g), "n": len(g), "occurrences_in_target": occ_cnt[g],
                                    "replicates_tv_only": only_reps[g], "modal_slot": ms, "modal_slot_share": mc / sum(occ_slot[g].values()),
                                    "other_tv_streams_attesting": len(tv_streams_with[g] - {t}), "cornell_utterances_full": corn_utts.get(g, 0),
                                    "press_utterances_full": press_utts.get(g, 0), "strict": g in strict,
                                    "per_100k_tv_other19": rate_tv(g, t), "per_100k_cornell": rate_c(g), "per_100k_press": rate_p(g)})
    L.write_csv(OUT / "largeI_tvonly_by_target.csv", by_target)
    for cls, c in slot_pool.items():
        tot_c = sum(v for kk, v in c.items() if not kk.startswith("_"))
        for sl in list(L.SLOTS) + ["_umpire_mask"]:
            slot_rows.append({"target": "ALL_TV", "label": "20 TV targets pooled", "class": cls, "slot": sl, "tokens_summed_over_R": c.get(sl, 0),
                              "share_of_class": c.get(sl, 0) / tot_c if tot_c else float("nan")})
    L.write_csv(OUT / "largeI_tvonly_slots.csv", slot_rows)
    types_final.sort(key=lambda x: (x["target"], -x["occurrences_in_target"], x["ngram"]))
    keep_final = []
    for t in (L.MAIN, L.HELDOUT):
        keep_final += [x for x in types_final if x["target"] == t][:200]
    L.write_csv(OUT / "largeI_tvonly_types_finals.csv", keep_final)
    pooled = []
    for g, d in types_pool.items():
        ms, mc = d["slots"].most_common(1)[0]
        pooled.append({"ngram": " ".join(g), "n": len(g), "targets_tv_only": d["targets"], "occurrences_in_targets": d["occurrences"],
                       "modal_slot": ms, "modal_slot_share": mc / sum(d["slots"].values()), "tv_streams_attesting": len(tv_streams_with[g]),
                       "cornell_utterances_full": corn_utts.get(g, 0), "press_utterances_full": press_utts.get(g, 0), "strict": g in strict,
                       "per_100k_tv_all20": rate_tv(g), "per_100k_cornell": rate_c(g), "per_100k_press": rate_p(g)})
    pooled.sort(key=lambda x: (-x["occurrences_in_targets"], x["ngram"]))
    L.write_csv(OUT / "largeI_tvonly_types_pooled.csv", pooled[:300])
    meta = {"I_size": I_SIZE, "R": R, "B": B, "sources": SOURCES, "token_variants": TOKVARS, "targets": len(L.TV),
            "candidates_tv_only_types": len(CAND), "strict_types": len(strict), "pooled_majority_types": len(pooled),
            "cornell_tokens_full": TEAMS["cornell"].ntok, "press_tokens_full": TEAMS["press_pooled"].ntok,
            "runtime_jobs_s": round(t_jobs, 1), "runtime_scan_s": round(t_scan, 1), "runtime_total_s": round(time.time() - t0, 1),
            "seeds": {"jobs": "[SEED, 108, target index, r, token variant index]", "bootstrap": "[SEED, 109]"}}
    L.write_json(OUT / "largeI_meta.json", meta)
    print("done", meta["runtime_total_s"], "s")


if __name__ == "__main__":
    if len(sys.argv) > 2 and sys.argv[1] == "--quick":   # test only: small I, R = 2, B = 200, outputs to the given directory
        I_SIZE, R, B, OUT = 20000, 3, 200, Path(sys.argv[2])
        OUT.mkdir(parents=True, exist_ok=True)
    main()
