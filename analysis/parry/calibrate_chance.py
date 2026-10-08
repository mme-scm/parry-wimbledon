"""POST HOC (plan.md addendum 1, M3/M4): the calibration against the coders at chance level, and the slot classifier in the mode used.

(1) Every automatic measure x reference set (A, B, A and B, A or B; HIGH + MEDIUM spans): auto share a, coder share c, precision and its
    chance level c and ceiling min(1, c / a), recall and its chance level a, Cohen's kappa (automatic vs coder) with a percentile bootstrap
    over utterances (B = 2,000). The same by sample group (2019 / other) with the groups' utterance lengths.
(2) Span level: share of each coder's HIGH spans fully inside / touching the automatic positive set, against 200 random circular shifts of
    the automatic labels within each utterance.
(3) Slot classifier: classify_context (the mode that assigns a reference's situational slot in H4) and classify(span) on every coder span vs
    the coder's slot; and, for the referring expressions of the 300 sampled utterances (p04's extraction) that lie inside a coder span, both
    modes vs that span's slot (longest overlapping span).

Inputs: the sample (gitignored), coding_A.jsonl, coding_B.jsonl, results/calibration_auto_labels.json (written by calibrate.py; recomputed
if absent). Outputs (results/): calibration_chance.csv, calibration_chance_groups.csv, calibration_span_recall.csv,
calibration_slot_context.json, calibration_slot_context_confusion.csv
Run: python -I analysis/parry/calibrate_chance.py
"""
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import numpy as np
import lib2b as L
import calibrate as CAL

SAMPLE = L.ROOT / "corpus" / "transcripts" / "samples" / "parry_sample_300.jsonl"
B, N_SHIFT = 2000, 200
REFS = ("A", "B", "A_and_B", "A_or_B")


def kappa_counts(n11, n10, n01, n00):
    N = n11 + n10 + n01 + n00
    a = (n11 + n10) / N
    c = (n11 + n01) / N
    po = (n11 + n00) / N
    pe = a * c + (1 - a) * (1 - c)
    return (po - pe) / (1 - pe) if pe < 1 else float("nan")


def stats_counts(n11, n10, n01, n00):
    N = n11 + n10 + n01 + n00
    a, c = (n11 + n10) / N, (n11 + n01) / N
    prec = n11 / (n11 + n10) if n11 + n10 else float("nan")
    rec = n11 / (n11 + n01) if n11 + n01 else float("nan")
    return {"auto_share": a, "coder_share": c, "precision": prec, "chance_precision": c, "precision_minus_chance": prec - c,
            "precision_ceiling": min(1.0, c / a) if a else float("nan"), "recall": rec, "chance_recall": a, "recall_minus_chance": rec - a,
            "kappa": kappa_counts(n11, n10, n01, n00), "tokens": N}


def main():
    sample = [json.loads(l) for l in open(SAMPLE, encoding="utf-8") if l.strip()]
    A, _ = CAL.load_coding(L.HERE / "coding_A.jsonl", sample)
    Bc, _ = CAL.load_coding(L.HERE / "coding_B.jsonl", sample)
    both = [r for r in sample if r["utt_id"] in A and r["utt_id"] in Bc]
    ap = L.RESULTS / "calibration_auto_labels.json"
    if ap.exists():
        auto = {k: {m: np.array(v, bool) for m, v in d.items()} for k, d in json.loads(ap.read_text()).items()}
    else:
        auto = CAL.automatic_labels(both)
    units = []
    for r in both:
        toks = CAL.tokens_with_offsets(r["text"])
        n = len(toks)
        pa, pb = CAL.positive(A[r["utt_id"]], n, CAL.PRIMARY_CONF), CAL.positive(Bc[r["utt_id"]], n, CAL.PRIMARY_CONF)
        units.append({"r": r, "n": n, "toks": [t for t, _, _ in toks], "group": "2019" if r["stream"] == L.MAIN else "other",
                      "ref": {"A": pa, "B": pb, "A_and_B": pa & pb, "A_or_B": pa | pb}, "auto": auto[r["utt_id"]]})
    measures = [m for m in CAL.MEASURES if all(m in u["auto"] for u in units)]
    # per-utterance 2x2 counts: (measure, ref) -> array (n_utts, 4)
    cnt = {}
    for m in measures:
        for ref in REFS:
            arr = np.zeros((len(units), 4))
            for k, u in enumerate(units):
                x, y = np.asarray(u["auto"][m], bool), u["ref"][ref]
                arr[k] = [np.sum(x & y), np.sum(x & ~y), np.sum(~x & y), np.sum(~x & ~y)]
            cnt[(m, ref)] = arr
    rng = np.random.default_rng([L.SEED, 112])
    draws = [rng.integers(0, len(units), len(units)) for _ in range(B)]
    rows = []
    for (m, ref), arr in cnt.items():
        st = stats_counts(*arr.sum(0))
        kd, pd, rd = [], [], []
        for idx in draws:
            s_ = stats_counts(*arr[idx].sum(0))
            kd.append(s_["kappa"])
            pd.append(s_["precision_minus_chance"])
            rd.append(s_["recall_minus_chance"])
        rows.append({"measure": m, "label": CAL.MEASURE_LABEL[m], "reference": ref, **st,
                     "kappa_lo": np.percentile(kd, 2.5), "kappa_hi": np.percentile(kd, 97.5),
                     "precision_minus_chance_lo": np.percentile(pd, 2.5), "precision_minus_chance_hi": np.percentile(pd, 97.5),
                     "recall_minus_chance_lo": np.percentile(rd, 2.5), "recall_minus_chance_hi": np.percentile(rd, 97.5),
                     "status": "post hoc (addendum 1, M3)"})
    a_ab = np.concatenate([u["ref"]["A"] for u in units])
    b_ab = np.concatenate([u["ref"]["B"] for u in units])
    coder_kappa = CAL.kappa(a_ab, b_ab)
    L.write_csv(L.RESULTS / "calibration_chance.csv", rows)
    # ---- groups
    grows = []
    for g in ("2019", "other"):
        ix = [k for k, u in enumerate(units) if u["group"] == g]
        lens = [units[k]["n"] for k in ix]
        for m in measures:
            for ref in ("A", "B", "A_or_B"):
                st = stats_counts(*cnt[(m, ref)][ix].sum(0))
                grows.append({"group": g, "utterances": len(ix), "tokens": int(sum(lens)), "median_tokens_per_utterance": float(np.median(lens)),
                              "mean_tokens_per_utterance": float(np.mean(lens)), "measure": m, "reference": ref, **st})
    L.write_csv(L.RESULTS / "calibration_chance_groups.csv", grows)
    # ---- span level, HIGH spans
    srng = np.random.default_rng([L.SEED, 112, 1])
    shifts = [[int(srng.integers(0, max(u["n"], 1))) for u in units] for _ in range(N_SHIFT)]
    coders = {"A": A, "B": Bc}
    srows = []
    for m in measures:
        for who in ("A", "B"):
            def shares(shift=None):
                full = part = tot = 0
                for k, u in enumerate(units):
                    x = np.asarray(u["auto"][m], bool)
                    if shift is not None:
                        x = np.roll(x, shift[k])
                    for sp in coders[who][u["r"]["utt_id"]]:
                        if sp["conf"] != "HIGH":
                            continue
                        seg = x[sp["s"]:sp["e"]]
                        tot += 1
                        full += bool(seg.all())
                        part += bool(seg.any())
                return full / tot, part / tot, tot
            f0, p0, tot = shares()
            ch = np.array([shares(sh)[:2] for sh in shifts])
            srows.append({"measure": m, "coder": who, "high_spans": tot, "fully_inside": f0, "fully_inside_chance_mean": ch[:, 0].mean(),
                          "fully_inside_chance_hi": np.percentile(ch[:, 0], 97.5), "touching": p0, "touching_chance_mean": ch[:, 1].mean(),
                          "touching_chance_hi": np.percentile(ch[:, 1], 97.5), "shifts": N_SHIFT})
    L.write_csv(L.RESULTS / "calibration_span_recall.csv", srows)
    # ---- slot classifier: context mode and span mode on coder spans
    out = {"coder_kappa_token_level": coder_kappa}
    conf_rows = []
    for who in ("A", "B"):
        xs, yc, ys = [], [], []
        for u in units:
            sc = L.SlotClassifier(u["toks"])
            for sp in coders[who][u["r"]["utt_id"]]:
                xs.append(sp["slot"])
                yc.append(sc.classify_context(sp["s"], sp["e"]))
                ys.append(sc.classify(sp["s"], sp["e"]))
        for mode, ys_ in (("context", yc), ("span", ys)):
            out[f"coder_spans_{who}_{mode}"] = {"n": len(xs), "agreement": float(np.mean(np.array(xs) == np.array(ys_))), "kappa": CAL.kappa(xs, ys_)}
            for (c, k), n in sorted(Counter(zip(xs, ys_)).items()):
                conf_rows.append({"unit": "coder span", "coder": who, "mode": mode, "coder_slot": c, "classifier_slot": k, "n": n})
    # ---- slot classifier on the referring expressions of the sample (p04's extraction)
    import spacy
    import p04_refexpr_pool as P4
    import refexpr as RX
    nlp = spacy.load("en_core_web_sm")
    ptab = P4.players_table()
    raw_spans = {}
    for who, path in (("A", L.HERE / "coding_A.jsonl"), ("B", L.HERE / "coding_B.jsonl")):
        d = {}
        for line in open(path, encoding="utf-8"):
            if line.strip():
                o = json.loads(line)
                d[o["utt_id"]] = [(s_["start_char"], s_["end_char"], (s_.get("slot") or "OTHER").upper()) for s_ in o.get("spans") or []]
        raw_spans[who] = d
    pats_cache = {}
    ref_pairs = defaultdict(list)   # (who, refset, mode) -> list of (coder slot, classifier slot)
    n_refs = Counter()
    for u in units:
        r = u["r"]
        s = r["stream"]
        if s not in pats_cache:
            pats_cache[s] = P4.patterns_for(s, ptab)
        pats, _, _ = pats_cache[s]
        doc = nlp(r["text"])
        words, idx = RX.word_seq(doc)
        found = P4.find(words, pats)
        if not found:
            continue
        sc = L.SlotClassifier(words)
        for k0, k1, expr, cat, ref in found:
            c0 = doc[idx[k0]].idx
            last = doc[idx[k1 - 1]]
            c1 = last.idx + len(last.text)
            comm = not P4.umpire(words, k0, k1, cat)
            ctx, spn = sc.classify_context(k0, k1), sc.classify(k0, k1)
            n_refs["all"] += 1
            n_refs["commentary_only"] += int(comm)
            for who in ("A", "B"):
                cov = [(e - a, sl) for a, e, sl in raw_spans[who].get(r["utt_id"], []) if a < c1 and e > c0]
                if not cov:
                    continue
                csl = max(cov)[1]
                for refset in ("all", "commentary_only"):
                    if refset == "commentary_only" and not comm:
                        continue
                    ref_pairs[(who, refset, "context")].append((csl, ctx))
                    ref_pairs[(who, refset, "span")].append((csl, spn))
    out["sample_references"] = dict(n_refs)
    for (who, refset, mode), pr in sorted(ref_pairs.items()):
        xs = [a for a, _ in pr]
        ys = [b for _, b in pr]
        out[f"references_{who}_{refset}_{mode}"] = {"n": len(pr), "agreement": float(np.mean(np.array(xs) == np.array(ys))), "kappa": CAL.kappa(xs, ys)}
        for (c, k), n in sorted(Counter(pr).items()):
            conf_rows.append({"unit": f"reference ({refset})", "coder": who, "mode": mode, "coder_slot": c, "classifier_slot": k, "n": n})
    L.write_json(L.RESULTS / "calibration_slot_context.json", out)
    L.write_csv(L.RESULTS / "calibration_slot_context_confusion.csv", conf_rows)
    print(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
