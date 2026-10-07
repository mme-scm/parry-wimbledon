"""Confirmatory tests C1-C5 (2019) and replication R1-R5 (2023) with Holm-Bonferroni; exploratory corpus contrasts
(plan section 7). Reads results written by f03-f06 and f09.

Revision 1 (plan.md addendum 2), deviations from the pre-registered plan, each labelled in the outputs:
* A1: C1/R1 are reported as "indeterminate pending a WER estimate" whatever their interval or p: the TV-vs-press contrast
  confounds commentary with ASR noise (unknown word error rate), transcription convention and held-out design.
* B1: for C1/R1/C2 the inferential statistic is the 95% interval of the replicate differences. The pre-registered "p"
  (2 x the share of replicate pairs on the minority side) is not a calibrated null test; when no pair falls on the other
  side it equals its floor 2/(R+1) and the Holm value is resolution-limited. C2 now uses R = 1000 matched replicates.
* B6: C4/C5/R4/R5 are run on the commentary-only references (umpire-pattern references excluded, f06); the
  pre-registered all-token results are kept as sensitivity rows (family *_sensitivity, Holm in the original family).
* B7: C2 and the medium rows are corpus contrasts (matches, outlet, period, ASR vs edited prose, segmentation differ).

Outputs: results/confirmatory.csv, results/medium_contrasts.csv
Run: python -I analysis/formulas/f07_confirmatory.py
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import csv
import json
import numpy as np
import common as C

NPAIRS = 10000
FAMS = {"2019": ("C1", "C2", "C3a", "C3b", "C4", "C5"), "2023_replication": ("R1", "R3a", "R3b", "R4", "R5")}


def holm(ps):
    ps = np.asarray(ps, float)
    order = np.argsort(ps)
    m = len(ps)
    adj = np.empty(m)
    running = 0.0
    for rank, i in enumerate(order):
        running = max(running, min(1.0, (m - rank) * ps[i]))
        adj[i] = running
    return adj


def p_two(diff):
    n = len(diff)
    lo = (1 + np.sum(diff <= 0)) / (1 + n)
    hi = (1 + np.sum(diff >= 0)) / (1 + n)
    return float(min(1.0, 2 * min(lo, hi)))


def utt_cov(name):
    with open(C.RESULTS / f"utt_coverage_{name}.csv") as fh:
        rows = list(csv.DictReader(fh))
    return np.array([int(r["tokens"]) for r in rows]), np.array([int(r["covered_a"]) for r in rows]), \
        np.array([int(r["covered_ab"]) for r in rows])


def reps(design, corpus, col):
    with open(C.RESULTS / "medium_replicates.csv") as fh:
        return np.array([float(r[col]) for r in csv.DictReader(fh) if r["design"] == design and r["corpus"] == corpus
                         and r[col] != ""])


def pair_diff(x_draws, y_draws, seed):
    rng = np.random.default_rng(seed)
    d = x_draws[rng.integers(0, len(x_draws), NPAIRS)] - y_draws[rng.integers(0, len(y_draws), NPAIRS)]
    return d


def summarise(name, hyp, est_x, est_y, d, family, status="confirmatory", extra="", n_pairs=None):
    p = p_two(d)
    floor = 2 / (1 + len(d))
    return {"id": name, "family": family, "status": status, "hypothesis": hyp, "estimate_x": float(est_x),
            "estimate_y": float(est_y), "difference": float(est_x - est_y), "diff_lo": float(np.percentile(d, 2.5)),
            "diff_hi": float(np.percentile(d, 97.5)), "p": p, "p_floor": floor, "p_at_floor": bool(abs(p - floor) < 1e-12),
            "replicate_pairs": len(d), "test": extra}


def main():
    rows = []
    med = []
    mmeta = json.loads((C.RESULTS / "density_medium_meta.json").read_text())
    mde = json.loads((C.RESULTS / "mde_summary.json").read_text())
    circ = json.loads((C.RESULTS / "circular_shift_tests.json").read_text())
    i_cornell = mmeta["D5ii_identification_size"][C.TEXT]["tokens_identification_median"]
    press_ho = reps("D5ii_heldout_disjoint_groups", "press_answers", "heldout_a")
    text_ho = reps("D5ii_heldout_disjoint_groups", C.TEXT, "heldout_a")
    # C1 / R1
    for cid, name, fam, seed in (("C1", "pool_to_2019", "2019", 31), ("R1", "pool_to_2023", "2023_replication", 33)):
        n, ca, _ = utt_cov(name)
        est, lo, hi, draws = C.boot_ratio(ca, n, B=2000, seed=seed)
        d = pair_diff(draws, press_ho, C.MASTER_SEED + (1 if cid == "C1" else 2))
        rows.append(summarise(cid, f"(a) repeated-n-gram coverage, pool -> {name[-4:]} final, minus press answers "
                                   f"(I ~100k -> M 9.7k, disjoint interviewees)",
                              est, press_ho.mean(), d, fam,
                              extra=f"{NPAIRS} random pairs: bootstrap draw of the TV value x press replicate (R={len(press_ho)}); "
                                    "inferential statistic = 95% interval of the differences"))
        d2 = pair_diff(draws, text_ho, C.MASTER_SEED + 10 + (1 if cid == "C1" else 2))
        med.append(summarise(f"E-{cid}-text", f"(a) coverage, pool -> {name[-4:]} final, minus Cornell text held-out "
                                              f"(disjoint player pairs; I median {i_cornell:,.0f} tokens, not 100k)",
                             est, text_ho.mean(), d2, fam, status="exploratory"))
        # D5(ii-b): M concentrated in few groups (press: usually one interviewee), I reaches ~100k for both corpora
        for corpus, lab in (("press_answers", "press"), (C.TEXT, "text")):
            g = reps("D5iib_heldout_grouped_M", corpus, "heldout_a")
            d3 = pair_diff(draws, g, C.MASTER_SEED + 20 + (1 if cid == "C1" else 2) + (5 if lab == "text" else 0))
            med.append(summarise(f"E-{cid}-{lab}-groupedM", f"(a) coverage, pool -> {name[-4:]} final, minus {lab} held-out with M "
                                                            "concentrated in few groups, I ~100k (D5ii-b, post hoc)",
                                 est, g.mean(), d3, fam, status="exploratory (post hoc)"))
    # C2 (R = 1000 matched replicates, paired by replicate index; the pairing is arbitrary because the subsamples are independent)
    tv = reps("D5i_matched_2019_size", "tv_pool_all", "splithalf_a")
    tx = reps("D5i_matched_2019_size", C.TEXT, "splithalf_a")
    pr = reps("D5i_matched_2019_size", "press_answers", "splithalf_a")
    k = min(len(tv), len(tx))
    rows.append(summarise("C2", "corpus contrast, split-half (a) repeated-n-gram coverage at 2019 size: TV pool subsamples minus "
                                "Cornell live-text subsamples",
                          tv.mean(), tx.mean(), tv[:k] - tx[:k], "2019",
                          extra=f"{k} independent subsample pairs; inferential statistic = 95% interval of the differences"))
    for a_name, a, b_name, b in (("tv_pool", tv, "press", pr), ("cornell_text", tx, "press", pr)):
        kk = min(len(a), len(b))
        med.append(summarise(f"E-split-{a_name}-vs-{b_name}", f"split-half (a) coverage at 2019 size: {a_name} minus {b_name}",
                             a.mean(), b.mean(), a[:kk] - b[:kk], "corpus", status="exploratory"))
    for col in ("insample_a", "insample_ab", "splithalf_ab", "insample_n3", "splithalf_n3", "splithalf_n4", "splithalf_content",
                "splithalf_content_n3", "insample_content_n3"):
        a = reps("D5i_matched_2019_size", "tv_pool_all", col)
        b = reps("D5i_matched_2019_size", C.TEXT, col)
        c = reps("D5i_matched_2019_size", "press_answers", col)
        kk = min(len(a), len(b), len(c))
        med.append(summarise(f"E-{col}-tv-vs-text", f"{col} at 2019 size: TV pool minus Cornell text", a.mean(), b.mean(),
                             a[:kk] - b[:kk], "corpus", status="exploratory"))
        med.append(summarise(f"E-{col}-tv-vs-press", f"{col} at 2019 size: TV pool minus press answers", a.mean(), c.mean(),
                             a[:kk] - c[:kk], "corpus", status="exploratory"))
    # C3 / R3
    t3 = json.loads((C.RESULTS / "c3_time_tests.json").read_text())
    for cid, key, fam, ckey in (("C3a", f"{C.MAIN}:dead_time_before:pool_a", "2019", f"{C.MAIN}:ctx_dtb_terc"),
                                ("C3b", f"{C.MAIN}:time_after:pool_a", "2019", f"{C.MAIN}:ctx_ta_terc"),
                                ("R3a", f"{C.HELDOUT}:dead_time_before:pool_a", "2023_replication", f"{C.HELDOUT}:ctx_dtb_terc"),
                                ("R3b", f"{C.HELDOUT}:time_after:pool_a", "2023_replication", f"{C.HELDOUT}:ctx_ta_terc")):
        t = t3[key]
        rows.append({"id": cid, "family": fam, "status": "confirmatory",
                     "hypothesis": f"(a) coverage (pool-identified), shortest minus longest tercile of {key.split(':')[1]}",
                     "estimate_x": t["T1_density"], "estimate_y": t["T3_density"], "difference": t["diff_T1_minus_T3"],
                     "diff_lo": t["diff_ci_lo"], "diff_hi": t["diff_ci_hi"], "p": t["p_two_sided"],
                     "test": f"{t['n_perm']} label permutations; CI by bootstrap within terciles",
                     "mde_80_alpha05": mde[cid]["mde_achieved_alpha05"], "mde_80_bonferroni": mde[cid]["mde_achieved_bonferroni"],
                     "p_circular_shift_exploratory": circ[ckey]["p_two_sided_circular_shift"]})
    # C4 / R4 (revised token set) and the pre-registered all-token rows (sensitivity)
    with open(C.RESULTS / "thrift_tests.csv") as fh:
        th = list(csv.DictReader(fh))
    with open(C.RESULTS / "length_time_tests.csv") as fh:
        lt = list(csv.DictReader(fh))
    for tset, suffix in (("commentary_only", ""), ("all_tokens", "_all_tokens")):
        for cid, stream, fam in (("C4", C.MAIN, "2019"), ("R4", C.HELDOUT, "2023_replication")):
            t = next(r for r in th if r["token_set"] == tset and r["stream"] == stream and r["context"] == "dtb_terc"
                     and r["players"] == "both" and r["permutation"] == "token_within_player_slot")
            rows.append({"id": cid + suffix, "family": fam + ("" if not suffix else "_sensitivity"),
                         "status": "confirmatory" if not suffix else "sensitivity (pre-registered token set, incl. umpire patterns)",
                         "hypothesis": f"thrift: distinct expressions per player x slot x dead-time tercile below permutation null ({tset})",
                         "estimate_x": float(t["D_observed"]), "estimate_y": float(t["null_mean"]),
                         "difference": float(t["D_observed"]) - float(t["null_mean"]),
                         "diff_lo": float(t["null_lo"]) - float(t["null_mean"]), "diff_hi": float(t["null_hi"]) - float(t["null_mean"]),
                         "p": float(t["p_one_sided_fewer"]), "replicate_pairs": int(t["tokens"]),
                         "test": f"one-sided, {t['n_perm']} permutations within player x slot; diff_lo/hi = null 95% interval minus null mean; "
                                 f"{t['tokens']} reference tokens",
                         "mde_80_alpha05": mde[cid]["mde_param_alpha05"] if not suffix else "",
                         "mde_80_bonferroni": mde[cid]["mde_param_bonferroni"] if not suffix else ""})
        for cid, stream, fam in (("C5", C.MAIN, "2019"), ("R5", C.HELDOUT, "2023_replication")):
            t = next(r for r in lt if r["token_set"] == tset and r["stream"] == stream and r["time"] == "dead_time_before_s"
                     and r["permutation"] == "token_within_player")
            rows.append({"id": cid + suffix, "family": fam + ("" if not suffix else "_sensitivity"),
                         "status": "confirmatory" if not suffix else "sensitivity (pre-registered token set, incl. umpire patterns)",
                         "hypothesis": f"extension: Spearman rho of expression length (syllables) with dead_time_before_s ({tset})",
                         "estimate_x": float(t["rho"]), "estimate_y": float(t["null_mean"]), "difference": float(t["rho"]),
                         "diff_lo": float(t["null_lo"]), "diff_hi": float(t["null_hi"]), "p": float(t["p_two_sided"]),
                         "replicate_pairs": int(t["tokens"]),
                         "test": f"two-sided, {t['n_perm']} permutations within player; diff_lo/hi = null 95% interval of rho; "
                                 f"{t['tokens']} reference tokens",
                         "mde_80_alpha05": mde[cid]["mde_achieved_alpha05"] if not suffix else "",
                         "mde_80_bonferroni": mde[cid]["mde_achieved_bonferroni"] if not suffix else "",
                         "p_circular_shift_exploratory": circ[f"{stream}:C5_dead_time_before_s"]["p_two_sided_circular_shift"]
                         if not suffix else ""})
    # Holm within the pre-registered families (revised rows), and for the sensitivity rows within the original composition
    byid = {r["id"]: r for r in rows}
    for fam, ids in FAMS.items():
        adj = holm([byid[i]["p"] for i in ids])
        for i, a in zip(ids, adj):
            byid[i]["p_holm"] = float(a)
        orig = [i + "_all_tokens" if i[:2] in ("C4", "C5", "R4", "R5") else i for i in ids]
        adj_o = holm([byid[i]["p"] for i in orig])
        for i, a in zip(orig, adj_o):
            if i.endswith("_all_tokens"):
                byid[i]["p_holm"] = float(a)
    for r in rows:
        cid = r["id"].split("_")[0]
        r["reject_at_0.05"] = bool(r["p_holm"] < 0.05)
        if cid in ("C1", "R1"):
            r["verdict"] = "indeterminate pending a WER estimate"
            r["inferential_statistic"] = "95% interval of differences; p is a replicate-overlap share" + \
                                         (" at its floor" if r.get("p_at_floor") else "")
        elif cid == "C2":
            excl = r["diff_lo"] > 0 or r["diff_hi"] < 0
            r["verdict"] = ("corpus difference: 95% interval of differences excludes 0 (not a medium effect)" if excl else
                            "no corpus difference detected: 95% interval of differences includes 0")
            r["inferential_statistic"] = "95% interval of differences; p is a replicate-overlap share" + \
                                         (" at its floor 2/(R+1), not a calibrated test" if r.get("p_at_floor") else "")
        else:
            r["verdict"] = "rejected" if r["reject_at_0.05"] else "not rejected"
            if cid in ("C3a", "C3b", "R3a", "R3b"):
                r["verdict"] += ("" if r["reject_at_0.05"] else
                                 f"; MDE (80% power, alpha 0.05) = {100 * r['mde_80_alpha05']:.1f} pp")
            elif cid in ("C4", "R4") and r["mde_80_alpha05"] != "":
                r["verdict"] += ("" if r["reject_at_0.05"] else
                                 f"; MDE (80% power, alpha 0.05): theta = {r['mde_80_alpha05']:.2f}")
            elif cid in ("C5", "R5") and r["mde_80_alpha05"] != "":
                r["verdict"] += ("" if r["reject_at_0.05"] else
                                 f"; MDE (80% power, alpha 0.05): rho = {r['mde_80_alpha05']:.2f}")
            r["inferential_statistic"] = "permutation p (Holm within family)"
    fields = ["id", "family", "status", "hypothesis", "estimate_x", "estimate_y", "difference", "diff_lo", "diff_hi", "p", "p_floor",
              "p_at_floor", "replicate_pairs", "p_holm", "reject_at_0.05", "verdict", "inferential_statistic", "mde_80_alpha05",
              "mde_80_bonferroni", "p_circular_shift_exploratory", "test"]
    order = ["C1", "R1", "C2", "C3a", "C3b", "R3a", "R3b", "C4", "R4", "C5", "R5",
             "C4_all_tokens", "R4_all_tokens", "C5_all_tokens", "R5_all_tokens"]
    with open(C.RESULTS / "confirmatory.csv", "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=fields)
        w.writeheader()
        for i in order:
            x = byid[i]
            w.writerow({k: (f"{x[k]:.6f}" if isinstance(x.get(k), float) else x.get(k, "")) for k in fields})
    mfields = ["id", "family", "status", "hypothesis", "estimate_x", "estimate_y", "difference", "diff_lo", "diff_hi", "p", "p_floor",
               "p_at_floor", "replicate_pairs", "test"]
    with open(C.RESULTS / "medium_contrasts.csv", "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=mfields)
        w.writeheader()
        for x in med:
            w.writerow({k: (f"{x[k]:.6f}" if isinstance(x.get(k), float) else x.get(k, "")) for k in mfields})
    for i in order:
        r = byid[i]
        print(r["id"], round(r["estimate_x"], 4), round(r["estimate_y"], 4), round(r["difference"], 4), r["p"], r["p_holm"], r["verdict"])


if __name__ == "__main__":
    main()
