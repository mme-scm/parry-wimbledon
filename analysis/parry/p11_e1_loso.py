"""POST HOC (plan.md addendum 1, minor items): E1 with a leave-one-stream-out inventory; E2 nulls summed per slot.

E1 (p05_thrift.e1) identifies the genre inventory on the 20 TV streams pooled, so an n-gram repeated inside one stream only enters the
inventory and all its occurrences belong to that stream: 'fewer distinct types per team than chance' is then guaranteed. Here each stream is
segmented (greedy longest-first, the p05 rule) with the formulas (2b-normalised, n >= 2 in >= 2 utterances, not stop-only) and OPEN-slot
systems (Phase 2 criteria) identified on the OTHER 19 streams pooled, and the same across-team null is applied (team labels permuted among
the slot's occurrences, 10,000 permutations).
E2: per slot, D summed over the slot's classes (those with >= 2 attested TV forms); null = sum of independent within-class permutations
of team labels (10,000), as plan section 9 promised.

Outputs (results/): e1_loso_tests.csv, e1_loso_meta.json, e2_slot_sums.csv
Run: python -I analysis/parry/p11_e1_loso.py
"""
import sys
import time
from collections import Counter, defaultdict
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from multiprocessing import Pool
import numpy as np
import lib2b as L
import p05_thrift as T

N_PERM = 10000
TEAMS = []


def segment(k):
    """Occurrences (type string, slot) in stream k with the inventory of the other 19 streams (p05 segmentation rule)."""
    pooled = [u for j, t in enumerate(TEAMS) if j != k for u in t.norm]
    F = L.C.formula_set_fast(pooled, m=2)
    Sys = {x for x in L.C.system_set_fast(pooled, frozenset()) if x[2] == "OPEN"}
    t = TEAMS[k]
    occ = []
    for u, ur in zip(t.norm, t.raw):
        cl = None
        i, Lu = 0, len(u)
        while i < Lu:
            found = None
            for n in range(min(12, Lu - i), 1, -1):
                g = tuple(u[i:i + n])
                if g in F:
                    found = (n, " ".join(g))
                    break
                if n <= 6:
                    for j in range(1, n - 1):
                        key = (n, j, "OPEN", g[:j] + g[j + 1:])
                        if key in Sys:
                            found = (n, L.C.frame_str(key))
                            break
                    if found:
                        break
            if found:
                if cl is None:
                    cl = L.SlotClassifier(ur)
                occ.append((found[1], cl.classify(i, i + found[0])))
                i += found[0]
            else:
                i += 1
    return k, occ, len(F), len(Sys)


def main():
    global TEAMS
    t0 = time.time()
    TEAMS = [L.load_tv(s) for s in L.TV]
    with Pool(4) as pool:
        res = pool.map(segment, range(len(TEAMS)), chunksize=1)
    occ = [(k, typ, sl) for k, oc, _, _ in res for typ, sl in oc]
    team_idx = np.array([o[0] for o in occ])
    typ, _ = T.enc([o[1] for o in occ])
    slot = np.array([o[2] for o in occ])
    rng = np.random.default_rng([L.SEED, 115])
    tests = []
    for sl in L.SLOTS:
        ix = np.where(slot == sl)[0]
        if len(ix) == 0:
            continue
        D, ms = T.econ_stats(team_idx[ix], typ[ix])
        nd, nm = np.empty(N_PERM), np.empty(N_PERM)
        for p in range(N_PERM):
            perm = team_idx[ix][rng.permutation(len(ix))]
            nd[p], nm[p] = T.econ_stats(perm, typ[ix])
        tests.append({"analysis": "E1 formula expressions, leave-one-stream-out inventory", "slot": sl, "occurrences": len(ix), "D_obs": D,
                      "null_mean": nd.mean(), "null_lo": np.percentile(nd, 2.5), "null_hi": np.percentile(nd, 97.5),
                      "p_one_sided_fewer": (1 + np.sum(nd <= D)) / (N_PERM + 1), "modal_share_obs": ms, "modal_share_null_mean": nm.mean(),
                      "p_one_sided_modal_higher": (1 + np.sum(nm >= ms)) / (N_PERM + 1), "permutations": N_PERM,
                      "null": "team labels permuted among occurrences within slot", "status": "post hoc (addendum 1), exploratory"})
    L.write_csv(L.RESULTS / "e1_loso_tests.csv", tests)
    L.write_json(L.RESULTS / "e1_loso_meta.json", {"occurrences": len(occ), "per_stream": {L.TV[k]: {"occurrences": len(oc), "formulas_other19": nf,
                                                   "open_systems_other19": ns} for k, oc, nf, ns in res}, "runtime_s": round(time.time() - t0, 1)})
    # ---- E2 summed per slot
    occ2 = defaultdict(list)   # class -> list of (team index, form)
    for ti, t in enumerate(TEAMS):
        for u in t.raw:
            for a, cname, fname, txt in T.e2_find(T.unify(u)):
                occ2[cname].append((ti, fname))
    rng2 = np.random.default_rng([L.SEED, 116])
    by_slot = defaultdict(list)
    for cname, slot_, forms in T.E2:
        oc = occ2.get(cname, [])
        if len({f for _, f in oc}) < 2:
            continue
        ti_, _ = T.enc([o[0] for o in oc])
        ty_, _ = T.enc([o[1] for o in oc])
        by_slot[slot_].append((cname, ti_, ty_))
    rows = []
    for slot_, cl in by_slot.items():
        D = sum(T.econ_stats(ti_, ty_)[0] for _, ti_, ty_ in cl)
        null = np.zeros(N_PERM)
        for p in range(N_PERM):
            null[p] = sum(T.econ_stats(ti_[rng2.permutation(len(ti_))], ty_)[0] for _, ti_, ty_ in cl)
        rows.append({"slot": slot_, "classes": ", ".join(c for c, _, _ in cl), "n_classes": len(cl), "occurrences": sum(len(t_) for _, t_, _ in cl),
                     "D_obs": D, "null_mean": null.mean(), "null_lo": np.percentile(null, 2.5), "null_hi": np.percentile(null, 97.5),
                     "p_one_sided_fewer": (1 + np.sum(null <= D)) / (N_PERM + 1), "permutations": N_PERM, "status": "post hoc (addendum 1), exploratory"})
    L.write_csv(L.RESULTS / "e2_slot_sums.csv", rows)
    print("done", round(time.time() - t0, 1), "s")
    for r in tests + rows:
        print(r)


if __name__ == "__main__":
    main()
