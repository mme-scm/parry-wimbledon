"""2b.1 genre core and idiolect share, by situational slot (plan section 4).

K(g) = number of the 20 TV streams whose inventory contains g. Core_k = {g : K(g) >= k}. For each stream, its formula tokens (covered
by its own inventory) are split by a(t) = max K over the own formulas covering t: idiolect (a = 1) vs core-k (a >= k). Slot of a formula
token = slot of the longest own-inventory occurrence covering it (classifier, plan section 5).

Outputs: results/core_sizes.csv, results/core_top.csv, results/idiolect_shares.csv, results/core_baselines.csv, results/core_meta.json
Run: python -I analysis/parry/p02_core.py
"""
import sys
import time
from collections import Counter, defaultdict
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from multiprocessing import Pool
import numpy as np
from scipy.stats import spearmanr
import lib2b as L

S, R_MATCHED, R_BASE = 1500, 200, 20
KS_SHARE = (2, 5, 10, 15, 20)
TVT = []
CLS = {}


def classifier(team_k, ui):
    key = (team_k, ui)
    c = CLS.get(key)
    if c is None:
        c = L.SlotClassifier(TVT[team_k].raw[ui])
        CLS[key] = c
    return c


def token_attest(team_k, uis, utts, F, K):
    """For the utterances uis of team team_k (token lists utts aligned with uis): per formula token (a, slot).
    Returns list of (a, slot) for covered tokens and the number of tokens."""
    out = []
    ntok = 0
    for ui, u in zip(uis, utts):
        Lu = len(u)
        ntok += Lu
        amax = [0] * Lu
        span = [None] * Lu
        for n in range(min(12, Lu), 1, -1):
            for i in range(Lu - n + 1):
                g = tuple(u[i:i + n])
                if g in F:
                    k = K.get(g, 1)
                    for t in range(i, i + n):
                        if k > amax[t]:
                            amax[t] = k
                        if span[t] is None:
                            span[t] = (i, i + n)
        cl = None
        cache = {}
        for t in range(Lu):
            if span[t] is None:
                continue
            if cl is None:
                cl = classifier(team_k, ui)
            sp = span[t]
            if sp not in cache:
                cache[sp] = cl.classify(*sp)
            out.append((amax[t], cache[sp]))
    return out, ntok


def shares(rows):
    """rows: list of (a, slot). Returns dict slot -> (n formula tokens, idiolect share, core-k shares)."""
    by = defaultdict(list)
    for a, s in rows:
        by[s].append(a)
        by["ALL"].append(a)
    res = {}
    for s, v in by.items():
        v = np.array(v)
        res[s] = [len(v), float(np.mean(v == 1))] + [float(np.mean(v >= k)) for k in KS_SHARE]
    return res


def core_sizes(invs, n_streams):
    K = Counter()
    for F in invs:
        K.update(F)
    out = {}
    for k in range(2, n_streams + 1):
        core = [g for g, c in K.items() if c >= k]
        out[k] = (len(core), sum(1 for g in core if len(g) >= 3), sum(1 for g in core if not L.is_content_free(g)))
    return K, out


def _matched(r):
    rng = np.random.default_rng([L.SEED, 2, r])
    subs = []
    invs = []
    for k, t in enumerate(TVT):
        idx = L.subsample(t.raw, S, rng)
        u = [t.norm[i] for i in idx]
        _, F, _ = L.index_inventory(u)
        subs.append((idx, u))
        invs.append(F)
    K, cs = core_sizes(invs, len(TVT))
    per = []
    for k, t in enumerate(TVT):
        rows, _ = token_attest(k, subs[k][0], subs[k][1], invs[k], K)
        per.append(shares(rows))
    return cs, per


def main():
    global TVT
    t0 = time.time()
    TVT = [L.load_tv(s) for s in L.TV]
    names = [t.name for t in TVT]
    size_rows, share_rows, top_rows, base_rows = [], [], [], []
    meta = {}
    # ---------------- full size
    full_K = {}
    for tokvar in ("norm", "raw"):
        invs = []
        for t in TVT:
            _, F, _ = L.index_inventory(t.norm if tokvar == "norm" else t.raw)
            invs.append(F)
        K, cs = core_sizes(invs, len(TVT))
        for k, (a, b, c) in cs.items():
            size_rows.append({"size": "full", "tokens": tokvar, "k": k, "types_base": a, "types_n3": b, "types_content": c})
        if tokvar == "norm":
            full_K = K
            full_invs = invs
            for k, t in enumerate(TVT):
                rows, ntok = token_attest(k, list(range(len(t.norm))), t.norm, invs[k], K)
                sh = shares(rows)
                for slot, v in sh.items():
                    share_rows.append({"size": "full", "stream": names[k], "slot": slot, "stream_tokens": ntok, "formula_tokens": v[0],
                                       "share_idiolect": v[1], **{f"share_core{kk}": v[2 + i] for i, kk in enumerate(KS_SHARE)}})
    # top core list with modal slot over occurrences in all streams
    slot_cnt = defaultdict(Counter)
    utt_cnt = Counter()
    for k, t in enumerate(TVT):
        for ui, u in enumerate(t.norm):
            seen = set()
            for n in range(2, min(12, len(u)) + 1):
                for i in range(len(u) - n + 1):
                    g = tuple(u[i:i + n])
                    if full_K.get(g, 0) >= 10 and g in full_invs[k]:
                        slot_cnt[g][classifier(k, ui).classify(i, i + n)] += 1
                        seen.add(g)
            utt_cnt.update(seen)
    top = sorted(full_K.items(), key=lambda kv: (-kv[1], -utt_cnt[kv[0]], kv[0]))[:60]
    for g, kk in top:
        sc = slot_cnt[g]
        modal, mc = sc.most_common(1)[0] if sc else ("", 0)
        top_rows.append({"formula": " ".join(g), "n": len(g), "streams_K": kk, "utterances_all_streams": utt_cnt[g], "modal_slot": modal,
                         "modal_slot_share": mc / sum(sc.values()) if sc else float("nan")})
    # ---------------- matched size
    t1 = time.time()
    with Pool(4) as pool:
        reps = pool.map(_matched, range(R_MATCHED), chunksize=5)
    meta["matched_runtime_s"] = round(time.time() - t1, 1)
    for k in range(2, len(TVT) + 1):
        arr = np.array([rp[0][k] for rp in reps], float)
        size_rows.append({"size": f"matched S={S}", "tokens": "norm", "k": k, "types_base": arr[:, 0].mean(), "types_n3": arr[:, 1].mean(),
                          "types_content": arr[:, 2].mean(), "types_base_lo": np.percentile(arr[:, 0], 2.5),
                          "types_base_hi": np.percentile(arr[:, 0], 97.5), "R": R_MATCHED})
    for k, nm in enumerate(names):
        slots = set()
        for rp in reps:
            slots |= set(rp[1][k].keys())
        for slot in sorted(slots):
            vals = np.array([rp[1][k][slot] for rp in reps if slot in rp[1][k]], float)
            row = {"size": f"matched S={S}", "stream": nm, "slot": slot, "stream_tokens": S, "formula_tokens": vals[:, 0].mean(),
                   "share_idiolect": vals[:, 1].mean(), "share_idiolect_lo": np.percentile(vals[:, 1], 2.5),
                   "share_idiolect_hi": np.percentile(vals[:, 1], 97.5), "replicates_with_slot": len(vals)}
            for i, kk in enumerate(KS_SHARE):
                row[f"share_core{kk}"] = vals[:, 2 + i].mean()
            share_rows.append(row)
    # ---------------- correlation of idiolect share with stream size
    full_all = {r["stream"]: r for r in share_rows if r["size"] == "full" and r["slot"] == "ALL"}
    mat_all = {r["stream"]: r for r in share_rows if r["size"].startswith("matched") and r["slot"] == "ALL"}
    ntoks = [t.ntok for t in TVT]
    rho_f = spearmanr(ntoks, [full_all[n]["share_idiolect"] for n in names])
    rho_m = spearmanr(ntoks, [mat_all[n]["share_idiolect"] for n in names])
    meta["spearman_idiolect_vs_stream_tokens"] = {"full": [float(rho_f[0]), float(rho_f[1])], "matched": [float(rho_m[0]), float(rho_m[1])]}
    # ---------------- baselines: share of full-size core_k types in Cornell / press inventories at total-TV size
    tot = sum(ntoks)
    teams_b = {"cornell": L.load_cornell(), "press_pooled": L.load_press(None)}
    cores = {k: {g for g, c in full_K.items() if c >= k} for k in KS_SHARE}
    for bname, team in teams_b.items():
        vals = defaultdict(list)
        for r in range(R_BASE):
            rng = np.random.default_rng([L.SEED, 3, r, len(bname)])
            idx = L.subsample(team.raw, tot, rng)
            _, F, _ = L.index_inventory([team.norm[i] for i in idx])
            for k in KS_SHARE:
                vals[k].append(len(cores[k] & F) / len(cores[k]) if cores[k] else np.nan)
                vals[(k, 3)].append(len({g for g in cores[k] if len(g) >= 3} & F) / max(1, len({g for g in cores[k] if len(g) >= 3})))
        for k in KS_SHARE:
            v = np.array(vals[k])
            v3 = np.array(vals[(k, 3)])
            base_rows.append({"baseline": bname, "k": k, "core_types": len(cores[k]), "core_types_n3": len({g for g in cores[k] if len(g) >= 3}),
                              "share_in_baseline_inventory": v.mean(), "lo": np.percentile(v, 2.5), "hi": np.percentile(v, 97.5),
                              "share_n3_in_baseline_inventory": v3.mean(), "subsample_tokens": tot, "R": R_BASE})
    L.write_csv(L.RESULTS / "core_sizes.csv", size_rows,
                ["size", "tokens", "k", "types_base", "types_base_lo", "types_base_hi", "types_n3", "types_content", "R"])
    L.write_csv(L.RESULTS / "core_top.csv", top_rows)
    L.write_csv(L.RESULTS / "idiolect_shares.csv", share_rows,
                ["size", "stream", "slot", "stream_tokens", "formula_tokens", "share_idiolect", "share_idiolect_lo", "share_idiolect_hi"]
                + [f"share_core{k}" for k in KS_SHARE] + ["replicates_with_slot"])
    L.write_csv(L.RESULTS / "core_baselines.csv", base_rows)
    meta["total_s"] = round(time.time() - t0, 1)
    meta["S"], meta["R_matched"], meta["R_baseline"] = S, R_MATCHED, R_BASE
    L.write_json(L.RESULTS / "core_meta.json", meta)
    print("done", meta)


if __name__ == "__main__":
    main()
