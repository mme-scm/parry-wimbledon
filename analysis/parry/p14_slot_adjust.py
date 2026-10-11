"""POST HOC (plan.md addendum 2, N2 and minor 3): the slot composition of the TV-only stock corrected for the slot classifier's confusions.

q = composition of a class's tokens by the span-mode classifier (Table 2.E; per-target counts in results/largeI_tvonly_slots.csv).
Confusion: SlotClassifier.classify(span) (the mode that produced q) on every coder span of the calibration sample (all confidence levels,
as in Table 3.4) against the coder's slot, per coder; recomputed here and asserted equal to calibration_slot_context_confusion.csv.
Estimators: (i) 'calibration' (primary): p_k = sum_j q_j P(coder slot k | classifier slot j); a classifier slot with no coder span keeps its
own share; (ii) 'inversion' (sensitivity): p >= 0 with sum 1 minimising || q - p P(classifier slot | coder slot) ||^2 (NNLS with the sum
constraint as a heavily weighted extra row). Spans weighted equally (primary) or by token length (sensitivity).
Uncertainty: percentile bootstrap (B = 2,000, seed [SEED, 120]) resampling the calibration utterances (with all their spans, both coders)
and, independently, the 20 targets (the finals: utterances only).
Minor 3: kappa of the context mode (and span mode) on the commentary references inside a coder span, with a percentile bootstrap over
references (B = 2,000, seed [SEED, 121]; references treated as independent although they cluster in utterances).

Inputs: corpus/transcripts/samples/parry_sample_300.jsonl (gitignored), coding_A.jsonl, coding_B.jsonl, results/largeI_tvonly_slots.csv,
results/calibration_slot_context_confusion.csv. Outputs (results/): slot_adjusted_composition.csv, slot_adjust_meta.json
Run: python -I analysis/parry/p14_slot_adjust.py
"""
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import numpy as np
from scipy.optimize import nnls
import lib2b as L
import calibrate as CAL

SAMPLE = L.ROOT / "corpus" / "transcripts" / "samples" / "parry_sample_300.jsonl"
B = 2000
S = list(L.SLOTS)
K = len(S)
CLASSES = ("tv_only", "tv_only_cross", "tv_only_strict", "shared")
GROUPS = {"SCORE+STAT+OFFICIAL": ("SCORE", "STAT", "OFFICIAL"), "SHOT+JUDGE": ("SHOT", "JUDGE")}


def per_utt_confusion(spans, weight="spans"):
    """spans: list per utterance of (coder slot index, classifier slot index, length); returns array (utterances, true k, classified j)."""
    C = np.zeros((len(spans), K, K))
    for u, sp in enumerate(spans):
        for k, j, ln in sp:
            C[u, k, j] += 1.0 if weight == "spans" else ln
    return C


def est_calibration(q, C):
    col = C.sum(0)
    P = np.where(col > 0, C / np.where(col > 0, col, 1), np.eye(K))   # P[k, j] = P(true k | classified j)
    return P @ q


def est_inversion(q, C):
    row = C.sum(1, keepdims=True)
    M = np.where(row > 0, C / np.where(row > 0, row, 1), np.eye(K))   # M[k, j] = P(classified j | true k)
    lam = 1e3
    A = np.vstack([M.T, lam * np.ones((1, K))])
    b = np.concatenate([q, [lam]])
    p, _ = nnls(A, b)
    return p / p.sum()


def main():
    sample = [json.loads(l) for l in open(SAMPLE, encoding="utf-8") if l.strip()]
    coders = {}
    coders["A"], _ = CAL.load_coding(L.HERE / "coding_A.jsonl", sample)
    coders["B"], _ = CAL.load_coding(L.HERE / "coding_B.jsonl", sample)
    both = [r for r in sample if r["utt_id"] in coders["A"] and r["utt_id"] in coders["B"]]
    spans = {"A": [], "B": []}
    for r in both:
        toks = [t for t, _, _ in CAL.tokens_with_offsets(r["text"])]
        sc = L.SlotClassifier(toks)
        for who in ("A", "B"):
            spans[who].append([(S.index(sp["slot"]), S.index(sc.classify(sp["s"], sp["e"])), sp["e"] - sp["s"]) for sp in coders[who][r["utt_id"]]])
    # check against the confusion counts of calibrate_chance.py (Table 3.4)
    ref = Counter()
    for row in L.read_csv(L.RESULTS / "calibration_slot_context_confusion.csv"):
        if row["unit"] == "coder span" and row["mode"] == "span":
            ref[(row["coder"], row["coder_slot"], row["classifier_slot"])] += int(row["n"])
    mine = Counter()
    for who in ("A", "B"):
        for u in spans[who]:
            for k, j, _ in u:
                mine[(who, S[k], S[j])] += 1
    assert mine == ref, "span-mode confusion differs from calibration_slot_context_confusion.csv"
    # classifier compositions
    cnt = defaultdict(lambda: np.zeros(K))
    for row in L.read_csv(L.RESULTS / "largeI_tvonly_slots.csv"):
        if row["slot"] in S and row["class"] in CLASSES:
            cnt[(row["target"], row["class"])][S.index(row["slot"])] = float(row["tokens_summed_over_R"])
    scopes = [("ALL_TV", c) for c in CLASSES] + [(L.MAIN, "tv_only"), (L.HELDOUT, "tv_only")]

    def q_of(scope, cls, tidx=None):
        if scope != "ALL_TV":
            v = cnt[(scope, cls)]
        else:
            v = sum(cnt[(L.TV[i], cls)] for i in (range(len(L.TV)) if tidx is None else tidx))
        return v / v.sum()
    rng = np.random.default_rng([L.SEED, 120])
    nU, nT = len(both), len(L.TV)
    draws = [(rng.integers(0, nU, nU), rng.integers(0, nT, nT)) for _ in range(B)]
    CU = {(who, wt): per_utt_confusion(spans[who], wt) for who in ("A", "B") for wt in ("spans", "tokens")}
    CB = {key: [CU[key][ui].sum(0) for ui, _ in draws] for key in CU}
    rows = []
    items = [(sl, [S.index(sl)]) for sl in S] + [(g, [S.index(x) for x in m]) for g, m in GROUPS.items()]
    for scope, cls in scopes:
        q0 = q_of(scope, cls)
        qs = np.array([q_of(scope, cls, ti) if scope == "ALL_TV" else q0 for _, ti in draws])
        for who in ("A", "B"):
            for weight in ("spans", "tokens"):
                C0 = CU[(who, weight)].sum(0)
                for ename, fn in (("calibration", est_calibration), ("inversion", est_inversion)):
                    p0 = fn(q0, C0)
                    bs = np.array([fn(qs[b], CB[(who, weight)][b]) for b in range(B)])
                    for name, cols in items:
                        rows.append({"target": scope, "label": "20 TV targets pooled" if scope == "ALL_TV" else L.short(scope), "class": cls,
                                     "coder": who, "estimator": ename, "weighting": weight, "slot": name,
                                     "classifier_share": float(q0[cols].sum()),
                                     "classifier_ci_lo": float(np.percentile(qs[:, cols].sum(1), 2.5)),
                                     "classifier_ci_hi": float(np.percentile(qs[:, cols].sum(1), 97.5)),
                                     "adjusted_share": float(p0[cols].sum()), "ci_lo": float(np.percentile(bs[:, cols].sum(1), 2.5)),
                                     "ci_hi": float(np.percentile(bs[:, cols].sum(1), 97.5)), "B": B,
                                     "uncertainty": "percentile bootstrap: calibration utterances" + (" and the 20 targets" if scope == "ALL_TV" else "")})
    L.write_csv(L.RESULTS / "slot_adjusted_composition.csv", rows)
    # ---- minor 3: reference-level kappa with bootstrap CI
    pairs = defaultdict(list)
    for row in L.read_csv(L.RESULTS / "calibration_slot_context_confusion.csv"):
        if row["unit"] == "reference (commentary_only)":
            pairs[(row["coder"], row["mode"])] += [(row["coder_slot"], row["classifier_slot"])] * int(row["n"])
    krng = np.random.default_rng([L.SEED, 121])
    kap = {}
    for (who, mode), pr in sorted(pairs.items()):
        xs = np.array([a for a, _ in pr])
        ys = np.array([b for _, b in pr])
        kd = []
        for _ in range(B):
            ix = krng.integers(0, len(pr), len(pr))
            kd.append(CAL.kappa(xs[ix], ys[ix]))
        kap[f"references_{who}_commentary_only_{mode}"] = {"n": len(pr), "kappa": CAL.kappa(xs, ys), "ci_lo": float(np.nanpercentile(kd, 2.5)),
                                                           "ci_hi": float(np.nanpercentile(kd, 97.5))}
    meta = {"utterances": nU, "spans": {w: int(sum(len(u) for u in spans[w])) for w in spans}, "confusion_check": "equal to calibration_slot_context_confusion.csv",
            "B": B, "seeds": {"composition bootstrap": "[SEED, 120]", "reference kappa bootstrap": "[SEED, 121]"}, "reference_kappa": kap}
    L.write_json(L.RESULTS / "slot_adjust_meta.json", meta)
    for r in rows:
        if r["target"] == "ALL_TV" and r["class"] == "tv_only" and r["weighting"] == "spans" and r["slot"] in ("SCORE+STAT+OFFICIAL", "OTHER", "SHOT+JUDGE"):
            print(r["coder"], r["estimator"], r["slot"], round(r["classifier_share"], 3), round(r["adjusted_share"], 3), round(r["ci_lo"], 3), round(r["ci_hi"], 3))
    print(json.dumps(kap, indent=1))


if __name__ == "__main__":
    main()
