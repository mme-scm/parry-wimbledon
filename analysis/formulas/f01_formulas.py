"""(a) Exact repeated n-grams in the 2019 final: inventory, per-n table, maximal match, cross-stream sharing.

Outputs: results/formulas_2019.tsv, results/formulas_by_n.csv, results/maximal_match_2019.csv,
results/formulas_cross_stream.csv, results/formulas_summary.json
Run: python -I analysis/formulas/f01_formulas.py
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import csv
from collections import Counter, defaultdict
import numpy as np
import common as C

N_EXCERPTS = 80
EX_WIDTH = 12  # words per excerpt (<= 15); windows never overlap a window already written


def pick_excerpt(utts, occ_list, n, used, width=EX_WIDTH):
    """First occurrence whose excerpt window does not overlap a window already written; '' if none."""
    for ui, i in occ_list:
        toks = utts[ui]
        extra = max(0, width - n)
        a = max(0, i - extra // 2)
        b = min(len(toks), a + width)
        a = max(0, b - width)
        if any(not (b <= x or a >= y) for x, y in used[ui]):
            continue
        used[ui].append((a, b))
        return " ".join(toks[a:b])
    return ""


def main():
    recs = C.load_stream(C.MAIN)
    utts = [r["toks"] for r in recs]
    T = sum(len(u) for u in utts)
    uttc, occ = C.ngram_utt_counts(utts, nmax=12)
    F = C.formula_set(utts, m=2, nmax=12, stop_filter=True)
    Fraw = C.formula_set(utts, m=2, nmax=12, stop_filter=False)

    # pool sharing
    pool = C.pool_streams()
    in_stream = defaultdict(int)
    pool_tokens = 0
    for s in pool:
        pu = [r["toks"] for r in C.load_stream(s)]
        pool_tokens += sum(len(u) for u in pu)
        seen = set()
        for toks in pu:
            L = len(toks)
            for n in range(2, min(12, L) + 1):
                for i in range(L - n + 1):
                    g = tuple(toks[i:i + n])
                    if g in Fraw:
                        seen.add(g)
        for g in seen:
            in_stream[g] += 1
    held = set()
    hu = [r["toks"] for r in C.load_stream(C.HELDOUT)]
    for toks in hu:
        L = len(toks)
        for n in range(2, min(12, L) + 1):
            for i in range(L - n + 1):
                g = tuple(toks[i:i + n])
                if g in Fraw:
                    held.add(g)

    # per-formula coverage share and first occurrence
    cover_tok = Counter()
    first = {}
    occs = defaultdict(list)
    for ui, toks in enumerate(utts):
        L = len(toks)
        for n in range(2, min(12, L) + 1):
            for i in range(L - n + 1):
                g = tuple(toks[i:i + n])
                if g in F:
                    occs[g].append((ui, i))
    for g in F:
        cov = 0
        n = len(g)
        for toks in utts:
            L = len(toks)
            mask = np.zeros(L, bool)
            for i in range(L - n + 1):
                if tuple(toks[i:i + n]) == g:
                    mask[i:i + n] = True
            cov += int(mask.sum())
        cover_tok[g] = cov
    order = sorted(F, key=lambda g: (-uttc[g], -len(g), " ".join(g)))
    used = defaultdict(list)
    C.RESULTS.mkdir(exist_ok=True)
    ex_words = 0
    with open(C.RESULTS / "formulas_2019.tsv", "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh, delimiter="\t")
        w.writerow(["rank", "formula", "n", "utterances", "occurrences", "coverage_share", "pool_streams_attested",
                    "in_2023", "example_excerpt_max12w"])
        for k, g in enumerate(order, 1):
            ex = ""
            if k <= N_EXCERPTS:
                ex = pick_excerpt(utts, occs[g], len(g), used)
                ex_words += len(ex.split())
            w.writerow([k, " ".join(g), len(g), uttc[g], occ[g], f"{cover_tok[g] / T:.5f}", in_stream.get(g, 0),
                        int(g in held), ex])

    # per-n table
    rows = []
    for n in range(2, 8):
        for label, FF in (("stop_filtered", F), ("unfiltered", Fraw)):
            Fn = {g for g in FF if len(g) == n}
            cov = sum(int((C.cover_a(t, Fn, exact_n=n) > 0).sum()) for t in utts)
            rows.append({"n": n, "filter": label, "formula_types": len(Fn),
                         "occurrences": sum(occ[g] for g in Fn),
                         "coverage_tokens": cov, "coverage_share": cov / T,
                         "types_in_ge1_pool_streams": sum(1 for g in Fn if in_stream.get(g, 0) >= 1),
                         "types_in_ge3_pool_streams": sum(1 for g in Fn if in_stream.get(g, 0) >= 3),
                         "types_in_ge9_pool_streams": sum(1 for g in Fn if in_stream.get(g, 0) >= 9),
                         "types_in_2023": sum(1 for g in Fn if g in held)})
    with open(C.RESULTS / "formulas_by_n.csv", "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)

    # maximal match: longest formula covering each token
    maxlen = Counter()
    for t in utts:
        cv = C.cover_a(t, F, n_min=2, n_max=12)
        maxlen.update(int(x) for x in cv)
    with open(C.RESULTS / "maximal_match_2019.csv", "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["longest_formula_len", "tokens", "share"])
        for L in sorted(maxlen):
            w.writerow([L, maxlen[L], f"{maxlen[L] / T:.5f}"])

    # cross-stream summary by number of pool streams
    cs = Counter(min(in_stream.get(g, 0), 18) for g in F)
    with open(C.RESULTS / "formulas_cross_stream.csv", "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["pool_streams_attested", "formula_types_2019"])
        for k in range(0, 19):
            w.writerow([k, cs.get(k, 0)])

    covered = sum(int((C.cover_a(t, F) > 0).sum()) for t in utts)
    C.write_json(C.RESULTS / "formulas_summary.json", {
        "stream": C.MAIN, "utterances": len(utts), "tokens": T, "pool_tokens": pool_tokens,
        "formula_types_stop_filtered": len(F), "formula_types_unfiltered": len(Fraw),
        "insample_density_a_nmin2": covered / T,
        "types_shared_with_any_pool_stream": sum(1 for g in F if in_stream.get(g, 0) >= 1),
        "types_in_2023": sum(1 for g in F if g in held),
        "excerpt_words_written": ex_words,
    })
    print("formulas:", len(F), "density", covered / T, "excerpt words", ex_words)


if __name__ == "__main__":
    main()
