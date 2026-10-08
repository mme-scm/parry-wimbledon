"""POST HOC (plan.md addendum 1, M4/M5): robustness of the thrift tests H4a / H4b, the verdict rule, and an H5 sensitivity.

* The pre-registered H4 statistics (p05_thrift.h4) with 100,000 permutations at three seeds; Monte Carlo SE of p.
* Variants (20,000 permutations each): without hypocoristic and epithet forms; surname and first name only; first reference per player per
  utterance; span-mode situational slot (classify(span) on the reference; column slot_sit_span); without the streams that carry hypocoristics.
* Leave-one-stream-out (20 runs, 5,000 permutations each).
* Holm under substitution: each variant's p replaces the primary p in the seven-test family (results/primary_tests.csv).
* Verdict rule (addendum 1, M5): 'rejected (robust)' if the pre-registered run is Holm-rejected and every variant (the three 100,000-permutation
  seeds and each listed variant; not leave-one-stream-out) is Holm-rejected under substitution; 'not robust / inconclusive' if the
  pre-registered run is rejected and some variant is not; 'not rejected' otherwise.
* H5 with the stored t_to_next_first_hit_s on all 20 streams (column t_next_stored_all; valid after the corpus frame-rate correction).
* Per-team H4b tests (results/thrift_tests_2b.csv): count with p < 0.05 against the number expected under H0.

Inputs: results/refexpr_pool_tokens.csv (p04), results/primary_tests.csv (p06), results/thrift_tests_2b.csv (p05).
Outputs (results/): h4_robust.csv, h4_robust_loso.csv, h4_verdicts.json, h5_sensitivity_post_hoc.csv
Run: python -I analysis/parry/p10_h4_robust.py
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import numpy as np
import lib2b as L
import p05_thrift as T
import p06_primary as P6

N_BIG, SEEDS_BIG = 100000, 3
N_VAR, N_LOSO = 20000, 5000
ALPHA = 0.05


def holm_sub(prim, test, p):
    ids = list(prim)
    ps = [p if k == test else float(prim[k]["p"]) for k in ids]
    return P6.holm(ps)[ids.index(test)]


def main():
    refs = T.load_refs()
    for r in refs:
        r["t_next_stored_all"] = T.fnum(r.get("t_next_stored_all"))
    comm = [r for r in refs if not r["umpire_pattern"] and r["player"] != "UNRESOLVED"]
    prim = {r["id"]: r for r in L.read_csv(L.RESULTS / "primary_tests.csv")}
    rows = []

    def add(variant, rs, res, seed, n_perm, kind, slot_key="slot_sit"):
        for k in ("H4a", "H4b"):
            d = res[k]
            p = d["p_one_sided_fewer"]
            hp = holm_sub(prim, k, p)
            rows.append({"test": k, "variant": variant, "kind": kind, "slot": slot_key, "tokens": d["tokens"],
                         "streams": len({r["stream"] for r in rs}), "D_obs": d["D_obs"], "null_mean": d["null_mean"], "null_lo": d["null_lo"],
                         "null_hi": d["null_hi"], "p_one_sided_fewer": p, "mc_se": float(np.sqrt(p * (1 - p) / n_perm)), "permutations": n_perm,
                         "seed": seed, "holm_p_substituted": hp, "holm_rejected": hp < ALPHA, "status": "post hoc (addendum 1, M5)"})
    # pre-registered run, as stored
    for k in ("H4a", "H4b"):
        pr = prim[k]
        rows.append({"test": k, "variant": "pre-registered run (p05, 10,000 permutations)", "kind": "pre-registered", "slot": "slot_sit",
                     "tokens": len(comm), "streams": len({r["stream"] for r in comm}), "D_obs": pr["estimate"], "p_one_sided_fewer": float(pr["p"]),
                     "permutations": 10000, "seed": "[SEED, 5] (p05 sequence)", "holm_p_substituted": float(pr["p_holm"]),
                     "holm_rejected": pr["reject_holm_0.05"] == "True", "status": "2b-primary"})
    for k in range(SEEDS_BIG):
        seed = [L.SEED, 113, k]
        add(f"100,000 permutations, seed {k}", comm, T.h4(comm, np.random.default_rng(seed), n_perm=N_BIG), str(seed), N_BIG, "seed")
        print("seed", k, rows[-1]["p_one_sided_fewer"], flush=True)
    hypo_streams = {r["stream"] for r in comm if r["category"] == "hypocoristic"}
    seen, first = set(), []
    for r in sorted(comm, key=lambda r: (r["utt_id"], int(r["word_k0"]))):
        if (r["utt_id"], r["player"]) not in seen:
            seen.add((r["utt_id"], r["player"]))
            first.append(r)
    variants = [
        ("without hypocoristic and epithet forms", [r for r in comm if r["category"] in ("surname", "first_name", "full_name", "title_surname")], "slot_sit"),
        ("surname and first name only", [r for r in comm if r["category"] in ("surname", "first_name")], "slot_sit"),
        ("first reference per player per utterance", first, "slot_sit"),
        ("span-mode slot (classify(span) on the reference)", comm, "slot_sit_span"),
        (f"without the {len(hypo_streams)} streams with hypocoristics", [r for r in comm if r["stream"] not in hypo_streams], "slot_sit"),
    ]
    for vi, (lab, rs, sk) in enumerate(variants):
        seed = [L.SEED, 114, vi]
        add(lab, rs, T.h4(rs, np.random.default_rng(seed), slot_key=sk, n_perm=N_VAR), str(seed), N_VAR, "variant", sk)
        print(lab, rows[-1]["p_one_sided_fewer"], flush=True)
    L.write_csv(L.RESULTS / "h4_robust.csv", rows)
    loso = []
    for si, s in enumerate(L.TV):
        rs = [r for r in comm if r["stream"] != s]
        res = T.h4(rs, np.random.default_rng([L.SEED, 114, 100 + si]), n_perm=N_LOSO)
        for k in ("H4a", "H4b"):
            d = res[k]
            loso.append({"test": k, "left_out": s, "label": L.short(s), "tokens": d["tokens"], "D_obs": d["D_obs"], "null_mean": d["null_mean"],
                         "p_one_sided_fewer": d["p_one_sided_fewer"], "holm_p_substituted": holm_sub(prim, k, d["p_one_sided_fewer"]),
                         "permutations": N_LOSO})
    L.write_csv(L.RESULTS / "h4_robust_loso.csv", loso)
    # ---- verdicts
    thr = L.read_csv(L.RESULTS / "thrift_tests_2b.csv")
    verdicts = {}
    for k in ("H4a", "H4b"):
        pre = next(r for r in rows if r["test"] == k and r["kind"] == "pre-registered")
        others = [r for r in rows if r["test"] == k and r["kind"] in ("seed", "variant")]
        failing = [r["variant"] for r in others if not r["holm_rejected"]]
        if pre["holm_rejected"] and not failing:
            v = "rejected (robust)"
        elif pre["holm_rejected"]:
            v = "not robust / inconclusive"
        else:
            v = "not rejected"
        lo = [r for r in loso if r["test"] == k]
        verdicts[k] = {"verdict": v, "pre_registered_holm_rejected": pre["holm_rejected"], "variants_checked": len(others),
                       "variants_not_rejected": failing, "p_range_variants": [min(r["p_one_sided_fewer"] for r in others),
                                                                                max(r["p_one_sided_fewer"] for r in others)],
                       "loso_p_range": [min(r["p_one_sided_fewer"] for r in lo), max(r["p_one_sided_fewer"] for r in lo)],
                       "loso_n_p_below_0.05": sum(r["p_one_sided_fewer"] < ALPHA for r in lo), "loso_runs": len(lo),
                       "rule": "rejected (robust) iff the pre-registered run and every seed/variant are Holm-rejected under substitution"}
    for sk in ("slot_sit", "slot_syn"):
        pt = [r for r in thr if r["test"] == "H4b per team" and r["slot_type"] == sk]
        verdicts[f"H4b_per_team_{sk}"] = {"tests": len(pt), "p_below_0.05": sum(float(r["p_one_sided_fewer"]) < ALPHA for r in pt),
                                          "expected_under_H0": ALPHA * len(pt)}
    verdicts["hypocoristic_streams"] = sorted(hypo_streams)
    verdicts["category_counts_commentary_only"] = {c: sum(r["category"] == c for r in comm) for c in sorted({r["category"] for r in comm})}
    L.write_json(L.RESULTS / "h4_verdicts.json", verdicts)
    # ---- H5 with the stored time field on all 20 streams
    h, _ = T.h5(comm, np.random.default_rng([L.SEED, 117]), xkey="t_next_stored_all")
    L.write_csv(L.RESULTS / "h5_sensitivity_post_hoc.csv",
                [{"analysis": "H5 sensitivity (post hoc)", "references": "commentary_only",
                  "time": "t_to_next_first_hit_s (stored; all 20 streams after the corpus frame-rate correction)", **h,
                  "status": "post hoc (addendum 1)"}],
                ["analysis", "references", "time", "tokens", "streams", "rho_weighted", "boot_lo", "boot_hi", "null_lo", "null_hi", "null_sd", "p_two",
                 "mde_rho_approx", "permutations", "status"])
    print(verdicts)


if __name__ == "__main__":
    main()
