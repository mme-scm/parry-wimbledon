"""Confirmatory tests C1-C5 (2019) and replication R1-R5 (2023) with Holm-Bonferroni; exploratory medium contrasts
(plan section 7). Reads results written by f03-f06.

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
        return np.array([float(r[col]) for r in csv.DictReader(fh) if r["design"] == design and r["corpus"] == corpus])


def pair_diff(x_draws, y_draws, seed):
    rng = np.random.default_rng(seed)
    d = x_draws[rng.integers(0, len(x_draws), NPAIRS)] - y_draws[rng.integers(0, len(y_draws), NPAIRS)]
    return d


def summarise(name, hyp, est_x, est_y, d, family, status="confirmatory", extra=""):
    return {"id": name, "family": family, "status": status, "hypothesis": hyp, "estimate_x": float(est_x),
            "estimate_y": float(est_y), "difference": float(est_x - est_y), "diff_lo": float(np.percentile(d, 2.5)),
            "diff_hi": float(np.percentile(d, 97.5)), "p": p_two(d), "test": extra}


def main():
    rows = []
    med = []
    press_ho = reps("D5ii_heldout_disjoint_groups", "press_answers", "heldout_a")
    text_ho = reps("D5ii_heldout_disjoint_groups", C.TEXT, "heldout_a")
    # C1 / R1
    for cid, name, fam, seed in (("C1", "pool_to_2019", "2019", 31), ("R1", "pool_to_2023", "2023_replication", 33)):
        n, ca, _ = utt_cov(name)
        est, lo, hi, draws = C.boot_ratio(ca, n, B=2000, seed=seed)
        d = pair_diff(draws, press_ho, C.MASTER_SEED + (1 if cid == "C1" else 2))
        rows.append(summarise(cid, f"(a) density, pool -> {name[-4:]} final, minus press answers (100k -> 9.7k, disjoint interviewees)",
                              est, press_ho.mean(), d, fam,
                              extra=f"{NPAIRS} pairs: bootstrap draw of TV value x press replicate (R={len(press_ho)})"))
        d2 = pair_diff(draws, text_ho, C.MASTER_SEED + 10 + (1 if cid == "C1" else 2))
        med.append(summarise(f"E-{cid}-text", f"(a) density, pool -> {name[-4:]} final, minus Cornell text held-out (disjoint player pairs)",
                             est, text_ho.mean(), d2, fam, status="exploratory"))
    # C2
    tv = reps("D5i_matched_2019_size", "tv_pool_all", "splithalf_a")
    tx = reps("D5i_matched_2019_size", C.TEXT, "splithalf_a")
    pr = reps("D5i_matched_2019_size", "press_answers", "splithalf_a")
    k = min(len(tv), len(tx))
    rows.append(summarise("C2", "split-half (a) density at 2019 size: TV pool subsamples minus Cornell live text",
                          tv.mean(), tx.mean(), tv[:k] - tx[:k], "2019", extra=f"{k} paired replicates"))
    for a_name, a, b_name, b in (("tv_pool", tv, "press", pr), ("cornell_text", tx, "press", pr)):
        kk = min(len(a), len(b))
        med.append(summarise(f"E-split-{a_name}-vs-{b_name}", f"split-half (a) density at 2019 size: {a_name} minus {b_name}",
                             a.mean(), b.mean(), a[:kk] - b[:kk], "medium", status="exploratory"))
    for col in ("insample_a", "insample_ab", "splithalf_ab"):
        a = reps("D5i_matched_2019_size", "tv_pool_all", col)
        b = reps("D5i_matched_2019_size", C.TEXT, col)
        c = reps("D5i_matched_2019_size", "press_answers", col)
        kk = min(len(a), len(b), len(c))
        med.append(summarise(f"E-{col}-tv-vs-text", f"{col} at 2019 size: TV pool minus Cornell text", a.mean(), b.mean(),
                             a[:kk] - b[:kk], "medium", status="exploratory"))
        med.append(summarise(f"E-{col}-tv-vs-press", f"{col} at 2019 size: TV pool minus press answers", a.mean(), c.mean(),
                             a[:kk] - c[:kk], "medium", status="exploratory"))
    # C3 / R3
    t3 = json.loads((C.RESULTS / "c3_time_tests.json").read_text())
    for cid, key, fam in (("C3a", f"{C.MAIN}:dead_time_before:pool_a", "2019"), ("C3b", f"{C.MAIN}:time_after:pool_a", "2019"),
                          ("R3a", f"{C.HELDOUT}:dead_time_before:pool_a", "2023_replication"),
                          ("R3b", f"{C.HELDOUT}:time_after:pool_a", "2023_replication")):
        t = t3[key]
        rows.append({"id": cid, "family": fam, "status": "confirmatory",
                     "hypothesis": f"(a) density (pool-identified), shortest minus longest tercile of {key.split(':')[1]}",
                     "estimate_x": t["T1_density"], "estimate_y": t["T3_density"], "difference": t["diff_T1_minus_T3"],
                     "diff_lo": t["diff_ci_lo"], "diff_hi": t["diff_ci_hi"], "p": t["p_two_sided"],
                     "test": f"{t['n_perm']} label permutations; CI by bootstrap within terciles"})
    # C4 / R4
    with open(C.RESULTS / "thrift_tests.csv") as fh:
        th = list(csv.DictReader(fh))
    for cid, stream, fam in (("C4", C.MAIN, "2019"), ("R4", C.HELDOUT, "2023_replication")):
        t = next(r for r in th if r["stream"] == stream and r["context"] == "dtb_terc" and r["players"] == "both"
                 and r["permutation"] == "token_within_player_slot")
        rows.append({"id": cid, "family": fam, "status": "confirmatory",
                     "hypothesis": "thrift: distinct expressions per player x slot x dead-time tercile below permutation null",
                     "estimate_x": float(t["D_observed"]), "estimate_y": float(t["null_mean"]),
                     "difference": float(t["D_observed"]) - float(t["null_mean"]),
                     "diff_lo": float(t["null_lo"]) - float(t["null_mean"]), "diff_hi": float(t["null_hi"]) - float(t["null_mean"]),
                     "p": float(t["p_one_sided_fewer"]), "test": f"one-sided, {t['n_perm']} permutations within player x slot; diff_lo/hi = null 95% interval minus null mean"})
    # C5 / R5
    with open(C.RESULTS / "length_time_tests.csv") as fh:
        lt = list(csv.DictReader(fh))
    for cid, stream, fam in (("C5", C.MAIN, "2019"), ("R5", C.HELDOUT, "2023_replication")):
        t = next(r for r in lt if r["stream"] == stream and r["time"] == "dead_time_before_s" and r["status"] == "confirmatory")
        rows.append({"id": cid, "family": fam, "status": "confirmatory",
                     "hypothesis": "extension: Spearman rho of expression length (syllables) with dead_time_before_s",
                     "estimate_x": float(t["rho"]), "estimate_y": float(t["null_mean"]), "difference": float(t["rho"]),
                     "diff_lo": float(t["null_lo"]), "diff_hi": float(t["null_hi"]), "p": float(t["p_two_sided"]),
                     "test": f"two-sided, {t['n_perm']} permutations within player; diff_lo/hi = null 95% interval of rho"})
    # expected sign of the effect under the oral-formulaic hypothesis (plan section 7); C2 is non-directional
    expected = {"C1": 1, "R1": 1, "C2": 0, "C3a": 1, "C3b": 1, "R3a": 1, "R3b": 1, "C4": -1, "R4": -1, "C5": 1, "R5": 1}
    for fam in ("2019", "2023_replication"):
        sel = [r for r in rows if r["family"] == fam]
        adj = holm([r["p"] for r in sel])
        for r, a in zip(sel, adj):
            r["p_holm"] = float(a)
            r["reject_at_0.05"] = bool(a < 0.05)
            e = expected[r["id"]]
            sign = 1 if r["difference"] > 0 else (-1 if r["difference"] < 0 else 0)
            r["expected_sign"] = e
            if not r["reject_at_0.05"]:
                r["verdict"] = "not rejected"
            elif e == 0:
                r["verdict"] = "rejected (non-directional)"
            elif sign == e:
                r["verdict"] = "rejected, in the predicted direction"
            else:
                r["verdict"] = "rejected, OPPOSITE to the predicted direction"
    with open(C.RESULTS / "confirmatory.csv", "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0]))
        w.writeheader()
        for x in rows:
            w.writerow({k: (f"{v:.6f}" if isinstance(v, float) else v) for k, v in x.items()})
    with open(C.RESULTS / "medium_contrasts.csv", "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(med[0]))
        w.writeheader()
        for x in med:
            w.writerow({k: (f"{v:.6f}" if isinstance(v, float) else v) for k, v in x.items()})
    for r in rows:
        print(r["id"], round(r["estimate_x"], 4), round(r["estimate_y"], 4), round(r["difference"], 4), r["p"], r["p_holm"])


if __name__ == "__main__":
    main()
