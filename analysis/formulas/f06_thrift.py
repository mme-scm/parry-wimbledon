"""Economy (thrift) and extension of the referring-expression systems (plan section 6); tests C4, C5 (2019) and R4, R5 (2023).

Input: results/refexpr_tokens_<stream>.csv (from f05_refexpr.py).
Outputs: results/thrift_tests.csv, results/thrift_cells.csv, results/extension.csv, results/length_time_tests.csv
Run: python -I analysis/formulas/f06_thrift.py
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import csv
from collections import Counter, defaultdict
import numpy as np
from scipy.stats import spearmanr
import common as C

NPERM = 10000
CONTEXTS = ("dtb_terc", "ta_terc", "phase", "score", "role")


def load(stream):
    with open(C.RESULTS / f"refexpr_tokens_{stream}.csv") as fh:
        rows = list(csv.DictReader(fh))
    for r in rows:
        r["syllables"] = int(r["syllables"])
        for k in ("dead_time_before_s", "time_after_s"):
            r[k] = float(r[k]) if r[k] not in ("", "None") else None
    return rows


def D_stat(expr, ctx, strata):
    """Sum over cells (stratum x context) of distinct expression types."""
    key = (strata.astype(np.int64) * 1000 + ctx) * 1000 + expr
    return len(np.unique(key))


def thrift_test(rows, context, seed, players=None, level="token"):
    rows = [r for r in rows if r[context] != "NA" and (players is None or r["player"] in players)]
    ex_ids = {e: i for i, e in enumerate(sorted({r["expression"] for r in rows}))}
    cx_ids = {c: i for i, c in enumerate(sorted({r[context] for r in rows}))}
    st_ids = {s: i for i, s in enumerate(sorted({(r["player"], r["slot"]) for r in rows}))}
    expr = np.array([ex_ids[r["expression"]] for r in rows])
    ctx = np.array([cx_ids[r[context]] for r in rows])
    strata = np.array([st_ids[(r["player"], r["slot"])] for r in rows])
    obs = D_stat(expr, ctx, strata)
    rng = np.random.default_rng(seed)
    null = np.empty(NPERM, dtype=np.int64)
    if level == "token":
        groups = [np.where(strata == s)[0] for s in np.unique(strata)]
        for b in range(NPERM):
            c2 = ctx.copy()
            for g in groups:
                c2[g] = ctx[g][rng.permutation(len(g))]
            null[b] = D_stat(expr, c2, strata)
    else:  # utterance level: permute the context labels of utterances (exploratory robustness)
        utts = sorted({r["utt_id"] for r in rows})
        u_id = {u: i for i, u in enumerate(utts)}
        uix = np.array([u_id[r["utt_id"]] for r in rows])
        uctx = np.empty(len(utts), dtype=int)
        for i, r in enumerate(rows):
            uctx[uix[i]] = ctx[i]
        for b in range(NPERM):
            null[b] = D_stat(expr, uctx[rng.permutation(len(utts))][uix], strata)
    mean = null.mean()
    p_one = (1 + np.sum(null <= obs)) / (1 + NPERM)
    p_two = (1 + np.sum(np.abs(null - mean) >= abs(obs - mean))) / (1 + NPERM)
    cells = Counter((r["player"], r["slot"], r[context]) for r in rows)
    types = defaultdict(set)
    for r in rows:
        types[(r["player"], r["slot"], r[context])].add(r["expression"])
    single = sum(1 for k in cells if len(types[k]) == 1)
    return {"tokens": len(rows), "cells_occupied": len(cells), "D_observed": int(obs), "null_mean": float(mean),
            "null_lo": float(np.percentile(null, 2.5)), "null_hi": float(np.percentile(null, 97.5)),
            "p_one_sided_fewer": float(p_one), "p_two_sided": float(p_two), "n_perm": NPERM,
            "thrift_index_single_type_cells": single / len(cells)}, types, cells


def length_time(rows, tkey, seed, level="token"):
    rows = [r for r in rows if r[tkey] is not None]
    syl = np.array([r["syllables"] for r in rows], float)
    tv = np.array([r[tkey] for r in rows], float)
    rho = spearmanr(syl, tv).statistic
    rng = np.random.default_rng(seed)
    null = np.empty(NPERM)
    if level == "token":
        players = np.array([r["player"] for r in rows])
        groups = [np.where(players == p)[0] for p in np.unique(players)]
        for b in range(NPERM):
            t2 = tv.copy()
            for g in groups:
                t2[g] = tv[g][rng.permutation(len(g))]
            null[b] = spearmanr(syl, t2).statistic
    else:
        utts = sorted({r["utt_id"] for r in rows})
        u_id = {u: i for i, u in enumerate(utts)}
        uix = np.array([u_id[r["utt_id"]] for r in rows])
        ut = np.empty(len(utts))
        for i in range(len(rows)):
            ut[uix[i]] = tv[i]
        for b in range(NPERM):
            null[b] = spearmanr(syl, ut[rng.permutation(len(utts))][uix]).statistic
    p_two = (1 + np.sum(np.abs(null) >= abs(rho))) / (1 + NPERM)
    return {"tokens": len(rows), "rho": float(rho), "null_mean": float(null.mean()), "null_lo": float(np.percentile(null, 2.5)),
            "null_hi": float(np.percentile(null, 97.5)), "p_two_sided": float(p_two), "n_perm": NPERM,
            "mean_syll": float(syl.mean())}


def main():
    tests, lt, cell_rows, ext_rows = [], [], [], []
    for si, stream in enumerate((C.MAIN, C.HELDOUT)):
        rows = load(stream)
        players = sorted({r["player"] for r in rows})
        for ci, ctxname in enumerate(CONTEXTS):
            status = "confirmatory" if ctxname == "dtb_terc" else "exploratory"
            res, types, cells = thrift_test(rows, ctxname, C.MASTER_SEED + 100 * si + ci)
            tests.append({"stream": stream, "context": ctxname, "players": "both", "permutation": "token_within_player_slot",
                          "status": status, **res})
            for k in sorted(cells):
                cell_rows.append({"stream": stream, "context": ctxname, "player": k[0], "slot": k[1], "group": k[2],
                                  "tokens": cells[k], "distinct_expressions": len(types[k]),
                                  "expressions": "; ".join(sorted(types[k]))})
            if ctxname == "dtb_terc":
                res_u, _, _ = thrift_test(rows, ctxname, C.MASTER_SEED + 100 * si + 50, level="utterance")
                tests.append({"stream": stream, "context": ctxname, "players": "both", "permutation": "utterance",
                              "status": "exploratory", **res_u})
                for p in players:
                    res_p, _, _ = thrift_test(rows, ctxname, C.MASTER_SEED + 100 * si + 60 + players.index(p), players={p})
                    tests.append({"stream": stream, "context": ctxname, "players": p, "permutation": "token_within_player_slot",
                                  "status": "exploratory", **res_p})
        for ti, tkey in enumerate(("dead_time_before_s", "time_after_s")):
            for level in ("token", "utterance"):
                status = "confirmatory" if (tkey == "dead_time_before_s" and level == "token") else "exploratory"
                res = length_time(rows, tkey, C.MASTER_SEED + 1000 + 10 * si + 2 * ti + (level == "utterance"), level=level)
                lt.append({"stream": stream, "time": tkey, "permutation": level + ("_within_player" if level == "token" else ""),
                           "status": status, **res})
        # extension descriptives
        for p in players:
            pr = [r for r in rows if r["player"] == p]
            syl_class = lambda s: "1-2" if s <= 2 else ("3" if s == 3 else ("4-5" if s <= 5 else "6+"))
            occ_cells = {(r["slot"], r["dtb_terc"], syl_class(r["syllables"])) for r in pr}
            ext_rows.append({"stream": stream, "player": p, "tokens": len(pr),
                             "distinct_expressions": len({r["expression"] for r in pr}),
                             "distinct_categories": len({r["category"] for r in pr}),
                             "syllable_min": min(r["syllables"] for r in pr), "syllable_max": max(r["syllables"] for r in pr),
                             "distinct_syllable_lengths": len({r["syllables"] for r in pr}),
                             "occupied_cells_slot_x_dtb_x_sylclass": len(occ_cells),
                             "share_surname": float(np.mean([r["category"] == "surname" for r in pr])),
                             "share_epithet": float(np.mean([r["category"] == "epithet" for r in pr]))})
    for name, rr in (("thrift_tests.csv", tests), ("thrift_cells.csv", cell_rows), ("extension.csv", ext_rows),
                     ("length_time_tests.csv", lt)):
        with open(C.RESULTS / name, "w", newline="") as fh:
            w = csv.DictWriter(fh, fieldnames=list(rr[0]))
            w.writeheader()
            for x in rr:
                w.writerow({k: (f"{v:.6f}" if isinstance(v, float) else v) for k, v in x.items()})
    for t in tests:
        print(t["stream"], t["context"], t["players"], t["permutation"], t["D_observed"], round(t["null_mean"], 2),
              round(t["p_one_sided_fewer"], 4))
    for t in lt:
        print(t["stream"], t["time"], t["permutation"], round(t["rho"], 3), round(t["p_two_sided"], 4))


if __name__ == "__main__":
    main()
