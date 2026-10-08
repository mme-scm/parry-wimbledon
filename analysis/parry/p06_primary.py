"""The seven 2b-primary tests (plan section 7) with Holm-Bonferroni at alpha = 0.05.

Inputs: results/primary_H1H2.json (p01), results/primary_H4H5.json (p05). Output: results/primary_tests.csv
Run: python -I analysis/parry/p06_primary.py
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import lib2b as L

ALPHA = 0.05
CLAIMS = {
    "H1a": "TV teams share multiword stock beyond lexicon (n >= 2)",
    "H1b": "TV teams share multiword stock beyond lexicon (n >= 3)",
    "H2a": "TV sources share more with TV targets than Cornell live text does",
    "H2b": "TV sources share more with TV targets than press answers do",
    "H4a": "naming habits (reference categories) are team-specific",
    "H4b": "form choice is bound to the situational slot within team x player",
    "H5": "longer referring expressions where more time is available",
}


def holm(ps):
    order = sorted(range(len(ps)), key=lambda i: ps[i])
    m = len(ps)
    adj = [0.0] * m
    run = 0.0
    for rank, i in enumerate(order):
        run = max(run, min(1.0, (m - rank) * ps[i]))
        adj[i] = run
    return adj


def main():
    a = L.read_json(L.RESULTS / "primary_H1H2.json")
    b = L.read_json(L.RESULTS / "primary_H4H5.json")
    rows = []
    for k in ("H1a", "H1b", "H2a", "H2b"):
        d = a[k]
        rows.append({"id": k, "claim": CLAIMS[k], "statistic": d["statistic"], "estimate": d["estimate"],
                     "interval": f"[{d['ci_lo']:.4f}, {d['ci_hi']:.4f}] (vertex bootstrap 95% CI)", "p": d["p_two"],
                     "p_kind": f"two-sided percentile-bootstrap, floor {d['p_floor']:.5f}", "p_at_floor": d["p_two"] <= d["p_floor"] + 1e-12,
                     "detail": f"{d['n_targets_positive']} of {d['n_targets']} TV targets positive"})
    for k in ("H4a", "H4b"):
        d = b[k]
        rows.append({"id": k, "claim": CLAIMS[k], "statistic": d["statistic"], "estimate": d["D_obs"],
                     "interval": f"null mean {d['null_mean']:.1f}, 95% [{d['null_lo']:.0f}, {d['null_hi']:.0f}]", "p": d["p_one_sided_fewer"],
                     "p_kind": f"one-sided permutation (fewer than chance), {d['permutations']} permutations",
                     "p_at_floor": d["p_one_sided_fewer"] <= 1 / (d["permutations"] + 1) + 1e-12,
                     "detail": f"{d['tokens']} commentary-only references" + (f"; MDE theta at 80% power {d['mde_theta_80pct_power']:.3f}"
                                                                              if k == "H4b" and d.get("mde_theta_80pct_power") is not None else "")})
    d = b["H5"]
    rows.append({"id": "H5", "claim": CLAIMS["H5"], "statistic": d["statistic"], "estimate": d["rho_weighted"],
                 "interval": f"stream-bootstrap 95% CI [{d['boot_lo']:.3f}, {d['boot_hi']:.3f}]; null 95% [{d['null_lo']:.3f}, {d['null_hi']:.3f}]",
                 "p": d["p_two"], "p_kind": f"two-sided permutation, {d['permutations']} permutations", "p_at_floor": d["p_two"] <= 1 / (d["permutations"] + 1) + 1e-12,
                 "detail": f"{d['tokens']} references in {d['streams']} streams; MDE rho about {d['mde_rho_approx']:.3f}"})
    adj = holm([r["p"] for r in rows])
    for r, p in zip(rows, adj):
        r["p_holm"] = p
        r["reject_holm_0.05"] = p < ALPHA
        r["status"] = "2b-primary (exploratory relative to Phase 2)"
    L.write_csv(L.RESULTS / "primary_tests.csv", rows)
    for r in rows:
        print(r["id"], r["estimate"], r["p"], r["p_holm"], r["reject_holm_0.05"])


if __name__ == "__main__":
    main()
