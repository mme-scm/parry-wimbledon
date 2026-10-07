"""Top-10 commentary formulae or systems of the 2019 final for the Phase 3 composition brief (plan section 9).

Revision 1 (plan.md addendum 2; critic C2/C9): `official_call` is computed with common.official_mask_v2 (the S5 patterns plus
point-score calls, bare `thank you`, `mr <name>`, `advantage <name>`, game-set calls and challenge announcements), so it now
fires on score calls, which the umpire says as often as the commentators; the `commentary_only` list therefore excludes them.
Column schema unchanged.

Outputs: results/top10_for_brief.csv (pre-specified ranking), results/top10_for_brief_n3.csv (exploratory: n >= 3 formulas
and systems with >= 2 fixed tokens)
Run: python -I analysis/formulas/f08_top10.py
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import csv
from collections import Counter
import numpy as np
import common as C


def contained(a: str, b: str) -> bool:
    return f" {a} " in f" {b} "


def main():
    recs = C.load_stream(C.MAIN)
    C.add_contexts(recs, C.MAIN)
    names = C.player_name_lexicon()
    masks = [C.official_mask_v2(r["toks"], names) for r in recs]
    with open(C.RESULTS / "formulas_2019.tsv") as fh:
        F = [dict(r, kind="formula", item=r["formula"]) for r in csv.DictReader(fh, delimiter="\t")]
    with open(C.RESULTS / "systems_2019.tsv") as fh:
        S = [dict(r, kind="system", item=r["frame"]) for r in csv.DictReader(fh, delimiter="\t")]
    Sset = C.system_set([r["toks"] for r in recs], names)
    keymap = {C.frame_str(k): k for k in Sset}
    items = []
    for r in F + S:
        items.append({"kind": r["kind"], "item": r["item"], "n": int(r["n"]), "utterances": int(r["utterances"]),
                      "occurrences": int(r["occurrences"]),
                      "fixed_tokens": int(r["n"]) - (1 if r["kind"] == "system" else 0),
                      "pool_streams_attested": int(r["pool_streams_attested"]),
                      "fillers": r.get("top_fillers", "")})
    # drop items contained in a longer item of the same kind with the same utterance count
    keep = []
    for it in items:
        dom = any(o is not it and o["kind"] == it["kind"] and o["n"] > it["n"] and o["utterances"] == it["utterances"]
                  and contained(it["item"], o["item"]) for o in items)
        if not dom:
            keep.append(it)

    def occurrences(it):
        hits = []
        for ui, r in enumerate(recs):
            toks = r["toks"]
            L = len(toks)
            n = it["n"]
            for i in range(L - n + 1):
                if it["kind"] == "formula":
                    ok = " ".join(toks[i:i + n]) == it["item"]
                else:
                    key = keymap[it["item"]]
                    ok = any(k == key for k, _ in C.frame_keys(toks, i, n, names))
                if ok:
                    hits.append((ui, i, n))
        return hits

    def situate(it):
        hits = occurrences(it)
        uis = sorted({h[0] for h in hits})
        off = np.mean([not masks[ui][i:i + n].any() for ui, i, n in hits]) if hits else 0.0
        role = Counter(recs[u]["ctx_role"] for u in uis).most_common(1)[0][0]
        score = Counter(recs[u]["ctx_score"] for u in uis).most_common(1)[0][0]
        nonother = Counter(recs[u]["ctx_score"] for u in uis if recs[u]["ctx_score"] not in ("other", "NA"))
        phase = Counter(recs[u]["ctx_phase"] for u in uis).most_common(1)[0][0]
        ta = [recs[u]["ctx_time_after"] for u in uis if recs[u]["ctx_time_after"] is not None]
        tb = [recs[u]["ctx_dt_before"] for u in uis if recs[u]["ctx_dt_before"] is not None]
        return {"official_call": bool(off >= 0.5), "share_occurrences_in_official_patterns": float(off),
                "modal_clip_role": role, "modal_score_situation": score,
                "pressure_points_share": float(sum(nonother.values()) / len(uis)) if uis else 0.0,
                "modal_phase": phase, "median_time_after_s": float(np.median(ta)) if ta else None,
                "median_dead_time_before_s": float(np.median(tb)) if tb else None}

    def write(name, pool_items):
        ranked = sorted(pool_items, key=lambda x: (-x["utterances"], -x["occurrences"], -x["n"], x["item"]))
        out = []
        for it in ranked:
            out.append({**it, **situate(it)})
            if sum(1 for o in out if not o["official_call"]) >= 10 and len(out) >= 10:
                break
        rows = []
        for lst_name, lst in (("with_official", out[:10]), ("commentary_only", [o for o in out if not o["official_call"]][:10])):
            for rank, o in enumerate(lst, 1):
                rows.append({"list": lst_name, "rank": rank, **o})
        with open(C.RESULTS / name, "w", newline="") as fh:
            w = csv.DictWriter(fh, fieldnames=list(rows[0]))
            w.writeheader()
            for x in rows:
                w.writerow({k: (f"{v:.3f}" if isinstance(v, float) else v) for k, v in x.items()})
        return rows

    rows = write("top10_for_brief.csv", keep)
    write("top10_for_brief_n3.csv", [it for it in keep if (it["kind"] == "formula" and it["n"] >= 3) or
                                     (it["kind"] == "system" and it["fixed_tokens"] >= 2)])
    for r in rows:
        print(r["list"], r["rank"], r["kind"], r["item"], r["utterances"], r["official_call"], r["modal_clip_role"])


if __name__ == "__main__":
    main()
