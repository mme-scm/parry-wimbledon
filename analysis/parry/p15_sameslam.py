"""POST HOC (plan.md addendum 2, minor 7): how much of the TV-source advantage is same-slam and same-player sharing?

Targets: the 20 TV streams (whole text, 2b normalisation). Sources at a common size I = 30,000 tokens (whole utterances, common.subsample),
R = 5 per target, seed [SEED, 122, target index, r], drawn in this order: (a) the other 19 TV streams; (b) the other streams of a different
slam; (c) the other streams sharing no player with the target; (d) both restrictions; (e) control: the other 19 streams minus k streams
drawn at random, k = the number of streams that (d) removes; (f) Cornell; (g) press. Inventory = common.formula_set_fast(sample, m = 2);
observed coverage of the target at n >= 2 and n >= 3. The two finals also at I = 54,000 (seed [SEED, 123, target index, r]).
Statistics: per target, mean over R; mean over targets with a percentile bootstrap over targets (B = 10,000, seed [SEED, 124]) of each
coverage, of (d) minus each baseline, and of the share of the TV-minus-baseline gap removed by a restriction, (a - x) / (a - baseline),
as a ratio of means over targets; the control (e) gives the share removed by dropping as many streams at random.

Outputs (results/): sameslam_coverage.csv, sameslam_summary.csv, sameslam_meta.json
Run: python -I analysis/parry/p15_sameslam.py
"""
import sys
import time
from collections import defaultdict
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from multiprocessing import Pool
import numpy as np
import lib2b as L

I_SMALL, I_FINALS, R, B = 30000, 54000, 5, 10000
OUT = L.RESULTS
SRC = ("a_other19", "b_other_slam", "c_no_shared_player", "d_both", "e_random_control", "f_cornell", "g_press")
BASE = ("f_cornell", "g_press")
NORM = {}
META = {}


def pools(t):
    o = [s for s in L.TV if s != t]
    m = META[t]
    b = [s for s in o if META[s]["slam"] != m["slam"]]
    c = [s for s in o if not set(META[s]["players"]) & set(m["players"])]
    d = [s for s in b if s in c]
    return o, b, c, d


def cov(utts, F):
    n = c2 = c3 = 0
    for u in utts:
        mx = L.C.cover_a(u, F)
        n += len(u)
        c2 += int((mx >= 2).sum())
        c3 += int((mx >= 3).sum())
    return c2 / n, c3 / n


def job(args):
    j, r, size, tag = args
    t = L.TV[j]
    rng = np.random.default_rng([L.SEED, 122 if tag == "all20" else 123, j, r])
    o, b, c, d = pools(t)
    k = len(o) - len(d)
    rows = []
    for src in SRC:
        if src == "e_random_control":
            drop = set(rng.choice(len(o), size=k, replace=False).tolist())
            streams = [s for i, s in enumerate(o) if i not in drop]
        else:
            streams = {"a_other19": o, "b_other_slam": b, "c_no_shared_player": c, "d_both": d}.get(src)
        I = [u for s in streams for u in NORM[s]] if streams is not None else NORM[src]
        idx = L.subsample(I, size, rng)
        Iu = [I[i] for i in idx]
        F = L.C.formula_set_fast(Iu, m=2)
        c2, c3 = cov(NORM[t], F)
        rows.append({"design": tag, "I": size, "target": t, "label": L.short(t), "r": r, "source": src,
                     "streams_in_pool": len(streams) if streams is not None else "", "pool_tokens": sum(len(u) for u in I),
                     "sample_tokens": sum(len(u) for u in Iu), "obs_n2": c2, "obs_n3": c3})
    return rows


def boot(fn, n, rng, B_=B):
    est = fn(np.arange(n))
    d = np.array([fn(rng.integers(0, n, n)) for _ in range(B_)])
    return float(est), float(np.percentile(d, 2.5)), float(np.percentile(d, 97.5))


def main():
    t0 = time.time()
    for s in L.TV:
        NORM[s] = L.load_tv(s).norm
        META[s] = L.stream_meta(s)
    NORM["f_cornell"] = L.load_cornell().norm
    NORM["g_press"] = L.load_press(None).norm
    jobs = [(j, r, I_SMALL, "all20") for j in range(len(L.TV)) for r in range(R)]
    jobs += [(L.TV.index(t), r, I_FINALS, "finals") for t in (L.MAIN, L.HELDOUT) for r in range(R)]
    with Pool(4) as pool:
        res = pool.map(job, jobs, chunksize=1)
    rows = [x for rr in res for x in rr]
    L.write_csv(OUT / "sameslam_coverage.csv", rows)
    per = defaultdict(lambda: defaultdict(list))
    for x in rows:
        for m in ("obs_n2", "obs_n3"):
            per[(x["design"], x["target"], x["source"])][m].append(float(x[m]))
    rng = np.random.default_rng([L.SEED, 124])
    summ = []
    for design, targets in (("all20", list(L.TV)), ("finals", [L.MAIN, L.HELDOUT])):
        for m in ("obs_n2", "obs_n3"):
            V = {s: np.array([np.mean(per[(design, t, s)][m]) for t in targets]) for s in SRC}
            n = len(targets)

            def add(stat, fn, kind):
                if design == "all20":
                    est, lo, hi = boot(fn, n, rng)
                else:
                    est, lo, hi = float(fn(np.arange(n))), float("nan"), float("nan")
                summ.append({"design": design, "I": I_SMALL if design == "all20" else I_FINALS, "measure": m, "statistic": stat, "kind": kind,
                             "estimate": est, "ci_lo": lo, "ci_hi": hi, "n_targets": n})
            for s in SRC:
                add(f"coverage: {s}", lambda ix, s=s: V[s][ix].mean(), "coverage")
            for s in ("a_other19", "d_both", "e_random_control"):
                for b in BASE:
                    add(f"{s} minus {b}", lambda ix, s=s, b=b: (V[s][ix] - V[b][ix]).mean(), "difference")
                    summ[-1]["targets_positive"] = int(np.sum(V[s] - V[b] > 0))
            for s in ("b_other_slam", "c_no_shared_player", "d_both", "e_random_control"):
                for b in BASE:
                    add(f"share of the a - {b} gap removed by {s}",
                        lambda ix, s=s, b=b: (V["a_other19"][ix] - V[s][ix]).mean() / (V["a_other19"][ix] - V[b][ix]).mean(), "share")
            for b in BASE:
                add(f"share of the a - {b} gap removed by d beyond the random control",
                    lambda ix, b=b: (V["e_random_control"][ix] - V["d_both"][ix]).mean() / (V["a_other19"][ix] - V[b][ix]).mean(), "share")
            if design == "finals":
                for t in targets:
                    for s in SRC:
                        summ.append({"design": design, "I": I_FINALS, "measure": m, "statistic": f"coverage: {s}", "kind": "per final",
                                     "estimate": float(np.mean(per[(design, t, s)][m])), "ci_lo": float("nan"), "ci_hi": float("nan"),
                                     "n_targets": 1, "target": L.short(t)})
    L.write_csv(OUT / "sameslam_summary.csv", summ, fields=["design", "I", "measure", "statistic", "kind", "target", "estimate", "ci_lo", "ci_hi",
                                                            "n_targets", "targets_positive"])
    meta = {"I_small": I_SMALL, "I_finals": I_FINALS, "R": R, "B": B, "sources": SRC,
            "pools": {L.short(t): {"streams": [len(p) for p in pools(t)], "tokens": [sum(len(u) for s in p for u in NORM[s]) for p in pools(t)]}
                      for t in L.TV},
            "pools_order": ["other 19", "different slam", "no shared player", "both"],
            "seeds": {"all20": "[SEED, 122, target index, r]", "finals": "[SEED, 123, target index, r]", "bootstrap": "[SEED, 124]"},
            "runtime_s": round(time.time() - t0, 1)}
    L.write_json(OUT / "sameslam_meta.json", meta)
    for x in summ:
        if x["measure"] == "obs_n3" and x["kind"] in ("share", "difference") or x["kind"] == "coverage" and x["measure"] == "obs_n3":
            print(x["design"], x["statistic"], round(x["estimate"], 4), round(x["ci_lo"], 4), round(x["ci_hi"], 4))
    print("done", meta["runtime_s"], "s")


if __name__ == "__main__":
    main()
