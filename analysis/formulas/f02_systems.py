"""(b) Formulaic systems (frames with exactly one open slot) in the 2019 final; plan section 3.

Outputs: results/systems_2019.tsv, results/systems_by_type.csv, results/systems_summary.json
Run: python -I analysis/formulas/f02_systems.py
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import csv
from collections import Counter, defaultdict
import numpy as np
import common as C

N_EXCERPTS = 40
EX_WIDTH = 12


def main():
    recs = C.load_stream(C.MAIN)
    utts = [r["toks"] for r in recs]
    T = sum(len(u) for u in utts)
    names = C.player_name_lexicon()
    S = C.system_set(utts, names)
    Sfast = C.system_set_fast(utts, names)
    assert set(S) == Sfast, (len(S), len(Sfast))
    F = C.formula_set(utts, m=2)
    # pool attestation of each frame (with any filler of the right type)
    pool_att = Counter()
    for s in C.pool_streams():
        seen = set()
        for r in C.load_stream(s):
            toks = r["toks"]
            L = len(toks)
            for n in range(2, min(6, L) + 1):
                for i in range(L - n + 1):
                    for key, _ in C.frame_keys(toks, i, n, names):
                        if key in S:
                            seen.add(key)
        for k in seen:
            pool_att[k] += 1
    # per-frame coverage and beyond-(a) coverage; occurrences for excerpts
    cov_tok = Counter()
    beyond = Counter()
    occs = defaultdict(list)
    a_cov = [C.cover_a(t, F) > 0 for t in utts]
    for ui, toks in enumerate(utts):
        L = len(toks)
        masks = defaultdict(lambda: np.zeros(L, bool))
        for n in range(2, min(6, L) + 1):
            for i in range(L - n + 1):
                for key, _ in C.frame_keys(toks, i, n, names):
                    if key in S:
                        masks[key][i:i + n] = True
                        occs[key].append((ui, i, n))
        for key, m in masks.items():
            cov_tok[key] += int(m.sum())
            beyond[key] += int((m & ~a_cov[ui]).sum())
    order = sorted(S, key=lambda k: (-S[k]["utts"], -S[k]["occ"], -k[0], C.frame_str(k)))
    used = defaultdict(list)
    ex_words = 0
    with open(C.RESULTS / "systems_2019.tsv", "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh, delimiter="\t")
        w.writerow(["rank", "frame", "n", "slot_position", "slot_type", "occurrences", "utterances", "distinct_fillers",
                    "top_fillers", "coverage_share", "coverage_beyond_a_share", "pool_streams_attested",
                    "example_excerpt_max12w"])
        for k, key in enumerate(order, 1):
            st = S[key]
            ex = ""
            if k <= N_EXCERPTS:
                for ui, i, n in occs[key]:
                    toks = utts[ui]
                    extra = max(0, EX_WIDTH - n)
                    a = max(0, i - extra // 2)
                    b = min(len(toks), a + EX_WIDTH)
                    a = max(0, b - EX_WIDTH)
                    if any(not (b <= x or a >= y) for x, y in used[ui]):
                        continue
                    used[ui].append((a, b))
                    ex = " ".join(toks[a:b])
                    break
                ex_words += len(ex.split())
            fil = "; ".join(f"{f}:{c}" for f, c in st["fillers"].most_common(8))
            w.writerow([k, C.frame_str(key), key[0], key[1], key[2], st["occ"], st["utts"], len(st["fillers"]), fil,
                        f"{cov_tok[key] / T:.5f}", f"{beyond[key] / T:.5f}", pool_att.get(key, 0), ex])
    by = Counter((key[0], key[2]) for key in S)
    with open(C.RESULTS / "systems_by_type.csv", "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["n", "slot_type", "systems"])
        for (n, st), c in sorted(by.items()):
            w.writerow([n, st, c])
    C.write_json(C.RESULTS / "systems_summary.json", {
        "stream": C.MAIN, "tokens": T, "systems": len(S),
        "systems_by_slot_type": dict(Counter(k[2] for k in S)),
        "excerpt_words_written": ex_words,
    })
    print("systems", len(S), dict(Counter(k[2] for k in S)))


if __name__ == "__main__":
    main()
