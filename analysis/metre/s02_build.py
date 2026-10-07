"""Pool formulas and per-unit / per-clip / per-string derived tables (plan sections 2-3; robustness R1, R2; exploratory X4).

Outputs (results/): pool_formulas_summary.json, pool_formulas_top.tsv, sample_flow_<tag>.csv, units_<tag>.csv,
strings_<tag>.csv, clips_<tag>.csv, top_strings_<tag>.tsv. No source text is written except formula n-grams and the most
frequent formulaic strings (each at most 12 words).
"""
import json
import sys
from collections import Counter
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
import syllables  # noqa: E402
from metre_lib import (RES, TAGS, build_units, formula_set, full_names, mask_names, match_segment,  # noqa: E402
                       pool_ngram_table, read_jsonl, score_call_mask, split_unmasked, surnames, tokenize, TR,
                       pool_paths)

RES.mkdir(parents=True, exist_ok=True)

# ---------------------------------------------------------------- formulas from the pool only
table = pool_ngram_table()
F_base = formula_set(table, nmin=2, min_count=3, min_streams=2)
F_strict = formula_set(table, nmin=3, min_count=5, min_streams=3)
table_m = pool_ngram_table(mask_player_names=True)
F_masked = formula_set(table_m, nmin=2, min_count=3, min_streams=2)
pool_tokens = sum(len(tokenize(r.get("text_corrected"))) for p in pool_paths() for r in read_jsonl(p))
by_n = Counter(g.count(" ") + 1 for g in F_base)
summary = {"pool_streams": len(pool_paths()), "pool_tokens": pool_tokens,
           "distinct_ngrams_n2_12": len(table),
           "formulas_base(n>=2,count>=3,streams>=2)": len(F_base),
           "formulas_strict(n>=3,count>=5,streams>=3)": len(F_strict),
           "formulas_name_masked_base": len(F_masked),
           "formulas_base_by_n": {str(k): by_n[k] for k in sorted(by_n)}}
json.dump(summary, open(RES / "pool_formulas_summary.json", "w"), indent=1)
top = sorted(((table[g][0], table[g][1], g) for g in F_base), key=lambda x: (-x[0], x[2]))
with open(RES / "pool_formulas_top.tsv", "w") as f:
    f.write("n\tcount_pool\tn_pool_streams\tngram\n")
    for n in range(2, 7):
        for c, s, g in [t for t in top if t[2].count(" ") + 1 == n][:40]:
            f.write(f"{n}\t{c}\t{s}\t{g}\n")
print(json.dumps(summary))

VARIANTS = ["base", "R1", "R2", "X4"]


def segments_for(tokens, variant, sn, names):
    if variant == "R1":
        return split_unmasked(tokens, score_call_mask(tokens, sn))
    if variant == "X4":
        return [mask_names(tokens, names)] if tokens else []
    return [tokens] if tokens else []


def analyse_clip(tokens, variant, sn, names):
    F = {"base": F_base, "R1": F_base, "R2": F_strict, "X4": F_masked}[variant]
    nmin = 3 if variant == "R2" else 2
    n_tok, n_cov, strings, texts = 0, 0, [], []
    for seg in segments_for(tokens, variant, sn, names):
        occ, cov, maximal = match_segment(seg, F, nmin=nmin)
        n_tok += len(seg)
        n_cov += int(cov.sum())
        for a, b in maximal:
            strings.append((syllables.count_tokens(seg[a:b]), b - a))
            texts.append(" ".join(seg[a:b]))
    return n_tok, n_cov, strings, texts


for tag in TAGS:
    U, flow, clips_by_point = build_units(tag)
    sn, names = surnames(tag), full_names(tag)
    pd.DataFrame(flow, columns=["step", "n_units"]).to_csv(RES / f"sample_flow_{tag}.csv", index=False)
    unit_set = set(U.point_idx)
    srows, crows = [], []
    top_strings = Counter()
    add = {f"{k}_{v}": [] for v in VARIANTS for k in ("n_tok", "n_cov")}
    add["n_syll"] = []
    for p in U.point_idx:
        acc = {v: [0, 0] for v in VARIANTS}
        syl = 0
        for c in clips_by_point[p]:
            toks = tokenize(c["text_corrected"])
            syl += syllables.count_tokens(toks)
            for v in VARIANTS:
                nt, nc, strings, texts = analyse_clip(toks, v, sn, names)
                acc[v][0] += nt
                acc[v][1] += nc
                for (sy, nt_s) in strings:
                    srows.append({"point_idx": p, "variant": v, "syll": sy, "ntok": nt_s})
                if v == "base":
                    top_strings.update(texts)
        for v in VARIANTS:
            add[f"n_tok_{v}"].append(acc[v][0])
            add[f"n_cov_{v}"].append(acc[v][1])
        add["n_syll"].append(syl)
    for k, vals in add.items():
        U[k] = vals
    U["words"] = U["n_tok_base"]
    U.to_csv(RES / f"units_{tag}.csv", index=False)
    pd.DataFrame(srows).to_csv(RES / f"strings_{tag}.csv", index=False)
    with open(RES / f"top_strings_{tag}.tsv", "w") as f:
        f.write("count\tn_tokens\tstring\n")
        for s, c in top_strings.most_common(30):
            f.write(f"{c}\t{s.count(' ') + 1}\t{s}\n")
    # clip-level table (all clips of the stream; used by exploratory X2, X3)
    for r in read_jsonl(TR / f"tv_{tag}.jsonl"):
        toks = tokenize(r["text_corrected"])
        nt, nc, _, _ = analyse_clip(toks, "base", sn, names)
        nt1, nc1, _, _ = analyse_clip(toks, "R1", sn, names)
        crows.append({"utt_id": r["utt_id"], "clip_i": r["clip_i"], "point_idx": r["point_idx_pbp"],
                      "clip_role": r["clip_role"], "phase": r["phase"],
                      "score_call_only": "score_call_only" in (r.get("phase_tags") or []),
                      "contains_score_call": "contains_score_call" in (r.get("phase_tags") or []),
                      "dedup_action": r["dedup_action"], "clip_start_s": r["clip_start_s"], "clip_end_s": r["clip_end_s"],
                      "first_hit_s": r["first_hit_s"], "last_hit_s": r["last_hit_s"], "n_tok": nt, "n_cov": nc,
                      "n_tok_R1": nt1, "n_cov_R1": nc1, "in_units": r["point_idx_pbp"] in unit_set})
    pd.DataFrame(crows).to_csv(RES / f"clips_{tag}.csv", index=False)
    print(tag, dict(flow), "units", len(U), "tokens", int(U.words.sum()), "share_base",
          round(U.n_cov_base.sum() / max(1, U.n_tok_base.sum()), 3))
