"""POST HOC (plan.md addendum 2, N1): how much more often does TV commentary use its TV-only n >= 3 strings than the baselines do?

Strings: every n >= 3 string that p08 classes as TV-only in a majority of a target's 5 samples, pooled over the 20 targets
(results/largeI_tvonly_types_pooled_all.csv), weighted by its occurrences in those targets (primary) or one per type; the 300 commonest
(the critic's set) as a check; yardstick: the strings p08 classes as shared with a baseline sample (largeI_shared_types_pooled_all.csv).
Matched-size rates: R = 100 replicates; in each, one 100,000-token sample (whole utterances, common.subsample) of the 20 TV streams pooled,
of the Cornell text and of the press answers (seed [SEED, 118, r], drawn in that order; 2b normalisation). Per string and source:
occurrences per 100,000 tokens in each sample, averaged over the R samples (the matched-size rate), and the share of samples in which the
string is a formula of the sample (>= 2 utterances). Whole-text rates as a check.
Statistics per string set, weighting and baseline (Cornell, press, the larger of the two): among strings with a positive baseline rate,
TV rate / baseline rate (weighted median and quartiles; weighted quantile = smallest value whose cumulative weight reaches q of the total);
share (weighted) with baseline rate below 1 and below 0.5 per 100,000; share of all strings (weighted) with zero rate in both baselines.
Uncertainty (implementation note of addendum 2: the planned bootstrap over replicates was dropped because resampling replicates with
replacement leaves fewer distinct samples, so rare strings lose their attestation and its intervals excluded their own estimates):
(i) Monte Carlo stability: the statistics from the two halves of the replicates (r < 50, r >= 50); (ii) heterogeneity of the stock:
percentile bootstrap over strings (B = 2,000, seed [SEED, 119]; the strings are a selected set, so this is descriptive).
Also the rate of the bigram `<name> <name>` (full names) per 100,000 tokens of each whole text (minor 10).

Outputs (results/): rate_ratio_summary.csv, rate_ratio_strings.csv (TV-only strings), rate_ratio_meta.json
Run: python -I analysis/parry/p13_rate_ratio.py
"""
import sys
import time
from collections import Counter
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from multiprocessing import Pool
import numpy as np
import lib2b as L

I_SIZE, R_RATE, B = 100000, 100, 2000
OUT = L.RESULTS
SOURCES = ("tv_all20", "cornell", "press_pooled")
NMAX = 12
UTTS = {}
CAND = {}          # tuple -> column index
CAND_FIRST = set()
LENS = ()


def scan(utts):
    """Occurrence counts and utterance counts (distinct utterances containing the string) of every candidate string."""
    occ, utt = Counter(), Counter()
    for u in utts:
        Lu = len(u)
        seen = set()
        for i in range(Lu):
            if u[i] not in CAND_FIRST:
                continue
            for n in LENS:
                if i + n > Lu:
                    break
                g = tuple(u[i:i + n])
                k = CAND.get(g)
                if k is not None:
                    occ[k] += 1
                    seen.add(k)
        utt.update(seen)
    return occ, utt


def job(r):
    rng = np.random.default_rng([L.SEED, 118, r])
    out = {}
    for src in SOURCES:
        U = UTTS[src]
        idx = L.subsample(U, I_SIZE, rng)
        sub = [U[i] for i in idx]
        occ, utt = scan(sub)
        out[src] = (sum(len(u) for u in sub), occ, utt)
    return r, out


def scan_whole(k):
    src, a, b = k
    return src, scan(UTTS[src][a:b])


def wquant(x, w, q):
    """Weighted quantile: smallest x whose cumulative weight reaches q of the total weight."""
    o = np.argsort(x, kind="stable")
    xs, cw = x[o], np.cumsum(w[o])
    return float(xs[np.searchsorted(cw, q * cw[-1] - 1e-9)])


def ratio_stats(tv, base, w):
    att = base > 0
    out = {"strings": int(len(w)), "strings_attested": int(att.sum()), "weight_share_attested": float(w[att].sum() / w.sum())}
    if att.sum() == 0:
        return out
    ratio = tv[att] / base[att]
    wa = w[att]
    out.update({"median_ratio": wquant(ratio, wa, 0.5), "q1_ratio": wquant(ratio, wa, 0.25), "q3_ratio": wquant(ratio, wa, 0.75),
                "min_ratio": float(ratio.min()), "share_ratio_ge_10": float(wa[ratio >= 10].sum() / wa.sum()),
                "share_base_rate_lt_1": float(wa[base[att] < 1].sum() / wa.sum()),
                "share_base_rate_lt_0.5": float(wa[base[att] < 0.5].sum() / wa.sum()),
                "median_base_rate": wquant(base[att], wa, 0.5)})
    return out


def main():
    global UTTS, CAND, CAND_FIRST, LENS
    t0 = time.time()
    UTTS["tv_all20"] = [u for s in L.TV for u in L.load_tv(s).norm]
    UTTS["cornell"] = L.load_cornell().norm
    UTTS["press_pooled"] = L.load_press(None).norm
    sets = {"tv_only_all": L.read_csv(OUT / "largeI_tvonly_types_pooled_all.csv"), "shared_all": L.read_csv(OUT / "largeI_shared_types_pooled_all.csv")}
    sets["tv_only_top300"] = sets["tv_only_all"][:300]
    for nm in ("tv_only_all", "shared_all"):
        for row in sets[nm]:
            g = tuple(row["ngram"].split(" "))
            if g not in CAND:
                CAND[g] = len(CAND)
    CAND_FIRST = {g[0] for g in CAND}
    LENS = tuple(range(3, NMAX + 1))
    ncand = len(CAND)
    print("strings", ncand, "loaded", round(time.time() - t0, 1), "s", flush=True)
    with Pool(4) as pool:
        res = pool.map(job, range(R_RATE), chunksize=1)
        chunks = []
        for src in SOURCES:
            n = len(UTTS[src])
            k = (n + 7) // 8
            chunks += [(src, a, min(n, a + k)) for a in range(0, n, k)]
        whole_parts = pool.map(scan_whole, chunks)
    t_jobs = time.time() - t0
    res.sort(key=lambda x: x[0])
    occ = {src: np.zeros((R_RATE, ncand)) for src in SOURCES}
    form = {src: np.zeros((R_RATE, ncand)) for src in SOURCES}
    ntok = {src: np.zeros(R_RATE) for src in SOURCES}
    for r, out in res:
        for src in SOURCES:
            nt, oc, ut = out[src]
            ntok[src][r] = nt
            for k, v in oc.items():
                occ[src][r, k] = v
            for k, v in ut.items():
                form[src][r, k] = float(v >= 2)
    whole_occ = {src: np.zeros(ncand) for src in SOURCES}
    for src, (oc, _) in whole_parts:
        for k, v in oc.items():
            whole_occ[src][k] += v
    whole_tok = {src: sum(len(u) for u in UTTS[src]) for src in SOURCES}
    rate_whole = {src: 1e5 * whole_occ[src] / whole_tok[src] for src in SOURCES}
    per = {src: 1e5 * occ[src] / ntok[src][:, None] for src in SOURCES}       # (R, ncand) rates per sample

    def rates_from(sel):
        """matched-size rates: mean over the selected replicates of the per-sample rates."""
        return {src: per[src][sel].mean(0) for src in SOURCES}

    rate_m = rates_from(np.arange(R_RATE))
    halves = (rates_from(np.arange(R_RATE // 2)), rates_from(np.arange(R_RATE // 2, R_RATE)))
    form_m = {src: form[src].mean(0) for src in SOURCES}
    brng = np.random.default_rng([L.SEED, 119])
    BOOT_COLS = ("median_ratio", "q1_ratio", "q3_ratio", "share_base_rate_lt_1", "share_unattested_both_baselines")

    summ, extra = [], {}
    for set_name, rows in sets.items():
        ix = np.array([CAND[tuple(r["ngram"].split(" "))] for r in rows])
        occw = np.array([float(r["occurrences_in_targets"]) for r in rows])
        for wname, w in (("occurrences", occw), ("types", np.ones(len(rows)))):
            for rname in ("matched", "whole"):
                rt = rate_m if rname == "matched" else rate_whole
                tv = rt["tv_all20"][ix]
                for bname in ("cornell", "press_pooled", "max"):
                    base = (np.maximum(rt["cornell"], rt["press_pooled"]) if bname == "max" else rt[bname])[ix]
                    st = ratio_stats(tv, base, w)
                    row = {"string_set": set_name, "weighting": wname, "rates": rname, "baseline": bname, **st,
                           "share_unattested_both_baselines": float(w[(rt["cornell"][ix] == 0) & (rt["press_pooled"][ix] == 0)].sum() / w.sum()),
                           "share_max_base_rate_lt_1_all": float(w[np.maximum(rt["cornell"], rt["press_pooled"])[ix] < 1].sum() / w.sum())}
                    if rname == "matched":
                        for h, hr in enumerate(halves):
                            bh = (np.maximum(hr["cornell"], hr["press_pooled"]) if bname == "max" else hr[bname])[ix]
                            sh = ratio_stats(hr["tv_all20"][ix], bh, w)
                            row[f"half{h + 1}_median_ratio"] = sh.get("median_ratio", np.nan)
                            row[f"half{h + 1}_share_base_rate_lt_1"] = sh.get("share_base_rate_lt_1", np.nan)
                        cz, pz = rt["cornell"][ix] == 0, rt["press_pooled"][ix] == 0
                        bs = []
                        for b in range(B):
                            jx = brng.integers(0, len(ix), len(ix))
                            s_ = ratio_stats(tv[jx], base[jx], w[jx])
                            bs.append([s_.get(c_, np.nan) for c_ in BOOT_COLS[:4]] + [float(w[jx][cz[jx] & pz[jx]].sum() / w[jx].sum())])
                        bs = np.array(bs)
                        for k_, col in enumerate(BOOT_COLS):
                            row[col + "_lo"] = float(np.nanpercentile(bs[:, k_], 2.5))
                            row[col + "_hi"] = float(np.nanpercentile(bs[:, k_], 97.5))
                        row["interval"] = "percentile bootstrap over strings (descriptive; the strings are a selected set)"
                    summ.append(row)
            extra[f"{set_name}_{wname}"] = {f"formula_share_{src}": float((w * form_m[src][ix]).sum() / w.sum()) for src in SOURCES}
    fields = []
    for row in summ:
        fields += [k for k in row if k not in fields]
    L.write_csv(OUT / "rate_ratio_summary.csv", summ, fields=fields)
    srows = []
    for r in sets["tv_only_all"]:
        k = CAND[tuple(r["ngram"].split(" "))]
        srows.append({"ngram": r["ngram"], "n": r["n"], "targets_tv_only": r["targets_tv_only"], "occurrences_in_targets": r["occurrences_in_targets"],
                      "modal_slot": r["modal_slot"], **{f"per_100k_{src}_matched": rate_m[src][k] for src in SOURCES},
                      **{f"formula_share_{src}": form_m[src][k] for src in SOURCES},
                      **{f"per_100k_{src}_whole": rate_whole[src][k] for src in SOURCES}})
    L.write_csv(OUT / "rate_ratio_strings.csv", srows)
    # minor 10: full names
    nn = {}
    for src in SOURCES:
        c = sum(1 for u in UTTS[src] for i in range(len(u) - 1) if u[i].startswith(L.NAME_TOKEN) and u[i + 1].startswith(L.NAME_TOKEN))
        nn[src] = {"bigrams": c, "per_100k_tokens": 1e5 * c / whole_tok[src]}
    meta = {"I_size": I_SIZE, "R": R_RATE, "B": B, "sources": SOURCES, "strings_scanned": ncand,
            "set_sizes": {k: len(v) for k, v in sets.items()}, "whole_tokens": whole_tok,
            "sample_tokens_mean": {src: float(ntok[src].mean()) for src in SOURCES},
            "sample_share_of_pool": {src: float(ntok[src].mean() / whole_tok[src]) for src in SOURCES},
            "formula_share_in_samples": extra, "name_name_bigram": nn,
            "seeds": {"samples": "[SEED, 118, r]", "bootstrap over strings": "[SEED, 119]"},
            "runtime_s": round(time.time() - t0, 1), "runtime_scans_s": round(t_jobs, 1)}
    L.write_json(OUT / "rate_ratio_meta.json", meta)
    for row in summ:
        if row["weighting"] == "occurrences" and row["string_set"] in ("tv_only_all", "tv_only_top300", "shared_all"):
            print(row["string_set"], row["rates"], row["baseline"], round(row.get("median_ratio", float("nan")), 2),
                  round(row.get("q1_ratio", float("nan")), 2), round(row.get("q3_ratio", float("nan")), 2),
                  round(row.get("share_base_rate_lt_1", float("nan")), 3), round(row["share_unattested_both_baselines"], 3))
    print("done", meta["runtime_s"], "s")


if __name__ == "__main__":
    main()
