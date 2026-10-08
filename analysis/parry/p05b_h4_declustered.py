"""POST HOC sensitivity (written after the H4b result was seen; exploratory): H4a and H4b with references de-clustered.

The plan's H4 permutations are token-level, but references in one utterance share a context window (hence often a slot) and often repeat
the same form, which can make cells look more homogeneous than independent tokens would. Here only the first reference to each player in each
utterance is kept, and the same tests are rerun. Also reported: the contribution of each situational slot to D_b (observed distinct forms minus
the null mean, from the same permutations).

Inputs: results/refexpr_pool_tokens.csv. Outputs: results/h4_declustered.csv, results/h4b_by_slot.csv
Run: python -I analysis/parry/p05b_h4_declustered.py
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import numpy as np
import lib2b as L
import p05_thrift as T

N_PERM = 10000


def main():
    rng = np.random.default_rng([L.SEED, 55])
    refs = T.load_refs()
    comm = [r for r in refs if not r["umpire_pattern"] and r["player"] != "UNRESOLVED"]
    seen, first = set(), []
    for r in sorted(comm, key=lambda r: (r["utt_id"], int(r["word_k0"]))):
        k = (r["utt_id"], r["player"])
        if k not in seen:
            seen.add(k)
            first.append(r)
    rows = []
    for lab, rs in (("all commentary-only references (as in H4)", comm), ("first reference per player per utterance", first)):
        res = T.h4(rs, rng, n_perm=N_PERM)
        for k in ("H4a", "H4b"):
            rows.append({"test": k, "token_set": lab, **res[k], "status": "post hoc sensitivity (exploratory)"})
    L.write_csv(L.RESULTS / "h4_declustered.csv", rows)
    # per-slot contribution to D_b (all commentary-only references)
    tp, _ = T.enc([(r["stream"], r["player"]) for r in comm])
    slot, skeys = T.enc([r["slot_sit"] for r in comm])
    form, _ = T.enc([(r["stream"], r["player"], r["expression"]) for r in comm])

    def per_slot(sl_arr):
        out = np.zeros(len(skeys))
        code = (tp * (len(skeys)) + sl_arr) * (int(form.max()) + 1) + form
        u = np.unique(code)
        s_of = (u // (int(form.max()) + 1)) % len(skeys)
        for s in s_of:
            out[s] += 1
        return out
    obs = per_slot(slot)
    null = np.array([per_slot(T.permute_within(slot, tp, rng)) for _ in range(N_PERM)])
    srows = []
    for i, s in enumerate(skeys):
        srows.append({"slot": s, "references": int(np.sum(slot == i)), "distinct_obs": obs[i], "null_mean": null[:, i].mean(),
                      "obs_minus_null": obs[i] - null[:, i].mean(), "null_lo": np.percentile(null[:, i], 2.5), "null_hi": np.percentile(null[:, i], 97.5)})
    L.write_csv(L.RESULTS / "h4b_by_slot.csv", srows)
    for r in rows:
        print(r["test"], r["token_set"], r["tokens"], r["D_obs"], round(r["null_mean"], 1), r["p_one_sided_fewer"])
    for r in srows:
        print(r)


if __name__ == "__main__":
    main()
