"""2b.2 calibration of the automatic formula inventory against two blind coders (plan section 6).

The coders are LLM agents, not humans: Cohen's kappa measures their mutual reliability, not the validity of either coder's
judgement against Parry's concept or against human specialists.

Inputs (defaults): analysis/parry/coding_A.jsonl, analysis/parry/coding_B.jsonl (format: analysis/parry/manual.md),
corpus/transcripts/samples/parry_sample_300.jsonl (gitignored; utt_id, stream, text = text_corrected).
Outputs (results/): calibration_agreement.json, calibration_prf.csv, calibration_strata.csv, calibration_slot_classifier.csv,
calibration_meta.json; if a coding file is missing: calibration_status.json only.
Run: python -I analysis/parry/calibrate.py [--sample P] [--coding-a P] [--coding-b P] [--out DIR] [--auto JSON]
`--auto` (tests only) supplies precomputed automatic token labels {utt_id: {measure: [0/1,...]}} instead of computing them from the corpus.
"""
from __future__ import annotations

import argparse
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import numpy as np
import lib2b as L

C = L.C
B = 2000
PRIMARY_CONF = ("HIGH", "MEDIUM")
ALL_CONF = ("HIGH", "MEDIUM", "LOW")
MEASURES = ["pool_n2", "pool_n3", "pool_systems", "pool_n2_or_systems", "insample_n2", "insample_n3",
            "pool_n2_normalised", "pool_content_n2", "core_K5_loo"]
MEASURE_LABEL = {
    "pool_n2": "pool exact n >= 2 (Phase 2 (a))", "pool_n3": "pool exact n >= 3", "pool_systems": "pool systems only ((b))",
    "pool_n2_or_systems": "pool (a) or (b)", "insample_n2": "in-sample exact n >= 2", "insample_n3": "in-sample exact n >= 3",
    "pool_n2_normalised": "pool exact n >= 2, 2b normalisation (exploratory)", "pool_content_n2": "pool content n >= 2 (exploratory)",
    "core_K5_loo": "genre core: in >= 5 other streams' inventories (exploratory)"}
CONFIRM_MEASURES = MEASURES[:6]


# ---------------------------------------------------------------- tokens with character offsets
def tokens_with_offsets(text: str):
    """Phase 2 tokens of `text` with (start, end) character offsets into `text`. The Phase 2 normaliser (NFKC, quotes, dashes,
    lower-case) preserves length for this corpus; if it does not, offsets are mapped through a character alignment."""
    norm = C.normalise(text)
    if len(norm) != len(text):
        # fall back: normalise character by character (keeps a 1:1 map where possible)
        chars, cmap = [], []
        for i, ch in enumerate(text):
            n = C.normalise(ch)
            for c in n:
                chars.append(c)
                cmap.append(i)
        norm = "".join(chars)
    else:
        cmap = list(range(len(text)))
    out = []
    for m in C._TOKEN.finditer(norm):
        a, b = m.start(), m.end()
        out.append((m.group(0), cmap[a], cmap[b - 1] + 1))
    return out


# ---------------------------------------------------------------- coder files
def load_coding(path, sample):
    """dict utt_id -> list of span dicts with token interval (s, e); plus stats."""
    texts = {r["utt_id"]: r["text"] for r in sample}
    offs = {r["utt_id"]: tokens_with_offsets(r["text"]) for r in sample}
    stats = Counter()
    out = {}
    with open(path, encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            try:
                obj = json.loads(line)
            except json.JSONDecodeError:
                stats["bad_json_lines"] += 1
                continue
            uid = obj.get("utt_id")
            if uid not in texts:
                stats["unknown_utt_id"] += 1
                continue
            text = texts[uid]
            spans = []
            for sp in obj.get("spans") or []:
                stats["spans_in_file"] += 1
                a, b, t = sp.get("start_char"), sp.get("end_char"), sp.get("text") or ""
                ok = isinstance(a, int) and isinstance(b, int) and 0 <= a < b <= len(text) and text[a:b] == t
                if not ok:
                    pos = []
                    if t:
                        k = text.find(t)
                        while k >= 0:
                            pos.append(k)
                            k = text.find(t, k + 1)
                    if pos:
                        a = min(pos, key=lambda p: abs(p - (a if isinstance(a, int) else 0)))
                        b = a + len(t)
                        stats["relocated"] += 1
                    else:
                        stats["dropped_not_found"] += 1
                        continue
                toks = [k for k, (_, ts, te) in enumerate(offs[uid]) if ts < b and te > a]
                if not toks:
                    stats["dropped_no_token"] += 1
                    continue
                conf = (sp.get("confidence") or "").upper()
                if conf not in ALL_CONF:
                    stats["unknown_confidence"] += 1
                spans.append({"s": toks[0], "e": toks[-1] + 1, "slot": (sp.get("slot") or "OTHER").upper(),
                              "type": (sp.get("type") or "").upper(), "conf": conf})
            if uid in out:
                stats["duplicate_utt_id"] += 1
            out[uid] = spans
    stats["utterances"] = len(out)
    return out, dict(stats)


def positive(spans, ntok, confs):
    v = np.zeros(ntok, dtype=bool)
    for sp in spans:
        if sp["conf"] in confs:
            v[sp["s"]:sp["e"]] = True
    return v


def token_attr(spans, ntok, confs, attr):
    """Per token the attribute of the longest covering span with confidence in confs (None if uncovered)."""
    out = [None] * ntok
    best = [0] * ntok
    for sp in spans:
        if sp["conf"] not in confs:
            continue
        ln = sp["e"] - sp["s"]
        for t in range(sp["s"], sp["e"]):
            if ln > best[t]:
                best[t], out[t] = ln, sp[attr]
    return out


def conf_level(spans, ntok):
    rank = {"HIGH": 3, "MEDIUM": 2, "LOW": 1}
    out = [None] * ntok
    for sp in spans:
        for t in range(sp["s"], sp["e"]):
            if out[t] is None or rank.get(sp["conf"], 0) > rank.get(out[t], 0):
                out[t] = sp["conf"]
    return out


# ---------------------------------------------------------------- statistics
def kappa(a, b):
    a = np.asarray(a)
    b = np.asarray(b)
    if len(a) == 0:
        return float("nan")
    cats = sorted(set(a.tolist()) | set(b.tolist()), key=str)
    po = float(np.mean(a == b))
    pe = sum(float(np.mean(a == c)) * float(np.mean(b == c)) for c in cats)
    return (po - pe) / (1 - pe) if pe < 1 else float("nan")


def match_spans(A, Bs):
    """Exact matches (identical token interval) and one-to-one overlap matches (greedy by token Jaccard)."""
    exact = len({(x["s"], x["e"]) for x in A} & {(y["s"], y["e"]) for y in Bs})
    pairs = []
    for i, x in enumerate(A):
        for j, y in enumerate(Bs):
            inter = min(x["e"], y["e"]) - max(x["s"], y["s"])
            if inter > 0:
                union = max(x["e"], y["e"]) - min(x["s"], y["s"])
                pairs.append((inter / union, i, j))
    pairs.sort(reverse=True)
    ua, ub, matched = set(), set(), []
    for _, i, j in pairs:
        if i in ua or j in ub:
            continue
        ua.add(i)
        ub.add(j)
        matched.append((A[i], Bs[j]))
    return exact, matched


def prf(auto, ref):
    tp = float(np.sum(auto & ref))
    pa, pr = float(np.sum(auto)), float(np.sum(ref))
    p = tp / pa if pa else float("nan")
    r = tp / pr if pr else float("nan")
    f = 2 * p * r / (p + r) if (p == p and r == r and p + r > 0) else float("nan")
    return p, r, f


def boot(fn, units, rng, B_=B):
    """Percentile bootstrap over utterances: fn(list of units) -> float or tuple."""
    draws = []
    n = len(units)
    for _ in range(B_):
        idx = rng.integers(0, n, n)
        draws.append(fn([units[i] for i in idx]))
    d = np.array(draws, float)
    return np.nanpercentile(d, 2.5, axis=0), np.nanpercentile(d, 97.5, axis=0)


# ---------------------------------------------------------------- automatic labels from the corpus
def automatic_labels(sample):
    """{utt_id: {measure: bool array over the utterance's Phase 2 tokens}} (plan section 6)."""
    teams = {s: L.load_tv(s) for s in L.TV}
    pool = [s for s in L.TV if s.startswith("tv_pool_")]
    full_inv = {s: L.index_inventory(teams[s].norm)[1] for s in L.TV}
    cache = {}
    out = {}
    for r in sample:
        s = r["stream"]
        if s not in cache:
            I = [s2 for s2 in pool if s2 != s]
            raw_I = [u for s2 in I for u in teams[s2].raw]
            norm_I = [u for s2 in I for u in teams[s2].norm]
            F = C.formula_set_fast(raw_I, m=2)
            Sy = C.system_set_fast(raw_I, L.NAMES)
            Fn = C.formula_set_fast(norm_I, m=2)
            Fi = C.formula_set_fast(teams[s].raw, m=2)
            K = Counter()
            for s2 in L.TV:
                if s2 != s:
                    K.update(full_inv[s2])
            core = {g for g, c in K.items() if c >= 5}
            cache[s] = (F, Sy, Fn, Fi, C.content_formulas(F), core)
        F, Sy, Fn, Fi, Fc, core = cache[s]
        toks = [t for t, _, _ in tokens_with_offsets(r["text"])]
        ntoks = L.norm_tokens(toks)
        mx = C.cover_a(toks, F)
        sysb = C.cover_b_set(toks, Sy, L.NAMES)
        mi = C.cover_a(toks, Fi)
        out[r["utt_id"]] = {
            "pool_n2": mx >= 2, "pool_n3": mx >= 3, "pool_systems": sysb, "pool_n2_or_systems": (mx >= 2) | sysb,
            "insample_n2": mi >= 2, "insample_n3": mi >= 3, "pool_n2_normalised": C.cover_a(ntoks, Fn) >= 2,
            "pool_content_n2": C.cover_a(toks, Fc) >= 2, "core_K5_loo": C.cover_a(ntoks, core) >= 2}
    return out


# ---------------------------------------------------------------- main analysis
def run(sample_path, a_path, b_path, out_dir, auto=None, B_=B, seed=L.SEED + 22):
    out_dir = Path(out_dir)
    sample = [json.loads(l) for l in open(sample_path, encoding="utf-8") if l.strip()]
    if not (Path(a_path).exists() and Path(b_path).exists()):
        L.write_json(out_dir / "calibration_status.json", {"status": "coding files absent; calibration not run",
                                                           "coding_A": str(a_path), "coding_B": str(b_path),
                                                           "A_exists": Path(a_path).exists(), "B_exists": Path(b_path).exists()})
        print("coding files absent; calibration not run")
        return None
    rng = np.random.default_rng(seed)
    A, sa = load_coding(a_path, sample)
    Bc, sb = load_coding(b_path, sample)
    both = [r for r in sample if r["utt_id"] in A and r["utt_id"] in Bc]
    if auto is None:
        auto = automatic_labels(both)
        # POST HOC (plan addendum 1, M3): keep the automatic token labels for calibrate_chance.py (new file; no other output changes)
        L.write_json(out_dir / "calibration_auto_labels.json", {u: {m: np.asarray(v, int).tolist() for m, v in d.items()} for u, d in auto.items()})
    units = []
    for r in both:
        toks = tokens_with_offsets(r["text"])
        n = len(toks)
        sc = L.SlotClassifier([t for t, _, _ in toks])
        units.append({"utt_id": r["utt_id"], "group": "2019" if r["stream"] == L.MAIN else "other", "n": n,
                      "A": A[r["utt_id"]], "B": Bc[r["utt_id"]],
                      "auto": {m: np.asarray(auto[r["utt_id"]][m], bool) for m in auto[r["utt_id"]]},
                      "cls_slot": sc.token_slots(), "sc": sc})
    measures = [m for m in MEASURES if all(m in u["auto"] for u in units)]

    def posv(u, who, confs):
        if who == "A":
            return positive(u["A"], u["n"], confs)
        if who == "B":
            return positive(u["B"], u["n"], confs)
        a, b = positive(u["A"], u["n"], confs), positive(u["B"], u["n"], confs)
        return a & b if who == "A_and_B" else a | b

    # ---- inter-coder agreement
    def tok_kappa(us, confs=PRIMARY_CONF):
        a = np.concatenate([positive(u["A"], u["n"], confs) for u in us]) if us else np.array([])
        b = np.concatenate([positive(u["B"], u["n"], confs) for u in us]) if us else np.array([])
        return kappa(a, b)

    def span_f1(us, confs=PRIMARY_CONF):
        nA = nB = ex = ov = 0
        for u in us:
            Aa = [x for x in u["A"] if x["conf"] in confs]
            Bb = [x for x in u["B"] if x["conf"] in confs]
            e, mt = match_spans(Aa, Bb)
            nA += len(Aa)
            nB += len(Bb)
            ex += e
            ov += len(mt)
        d = nA + nB
        return (2 * ex / d if d else float("nan"), 2 * ov / d if d else float("nan"))

    def attr_agree(us, attr, confs=PRIMARY_CONF):
        xa, xb = [], []
        for u in us:
            _, mt = match_spans([x for x in u["A"] if x["conf"] in confs], [x for x in u["B"] if x["conf"] in confs])
            for x, y in mt:
                xa.append(x[attr])
                xb.append(y[attr])
        if not xa:
            return float("nan"), float("nan"), 0
        return float(np.mean(np.array(xa) == np.array(xb))), kappa(xa, xb), len(xa)

    agr = {"coders": "two LLM agents (not humans), blind to the automatic inventory; kappa = their mutual reliability, not validity",
           "utterances_both": len(units), "tokens": int(sum(u["n"] for u in units)),
           "file_stats": {"A": sa, "B": sb}}
    for lab, confs in (("primary_HIGH_MEDIUM", PRIMARY_CONF), ("all_confidences", ALL_CONF)):
        k = tok_kappa(units, confs)
        klo, khi = boot(lambda us: tok_kappa(us, confs), units, rng, B_)
        f_ex, f_ov = span_f1(units, confs)
        (elo, olo), (ehi, ohi) = boot(lambda us: span_f1(us, confs), units, rng, B_)
        sl = attr_agree(units, "slot", confs)
        ty = attr_agree(units, "type", confs)
        agr[lab] = {"token_kappa": k, "token_kappa_ci": [float(klo), float(khi)],
                    "positive_token_share_A": float(np.mean(np.concatenate([positive(u["A"], u["n"], confs) for u in units]))),
                    "positive_token_share_B": float(np.mean(np.concatenate([positive(u["B"], u["n"], confs) for u in units]))),
                    "span_F1_exact": f_ex, "span_F1_exact_ci": [float(elo), float(ehi)],
                    "span_F1_overlap": f_ov, "span_F1_overlap_ci": [float(olo), float(ohi)],
                    "spans_A": sum(1 for u in units for x in u["A"] if x["conf"] in confs),
                    "spans_B": sum(1 for u in units for x in u["B"] if x["conf"] in confs),
                    "matched_spans": sl[2], "slot_agreement": sl[0], "slot_kappa": sl[1], "type_agreement": ty[0], "type_kappa": ty[1]}
    agr["span_counts"] = {who: {"by_confidence": dict(Counter(x["conf"] for u in units for x in u[who])),
                                "by_slot": dict(Counter(x["slot"] for u in units for x in u[who])),
                                "by_type": dict(Counter(x["type"] for u in units for x in u[who]))} for who in ("A", "B")}
    L.write_json(out_dir / "calibration_agreement.json", agr)

    # ---- precision / recall of automatic measures
    prf_rows, strata_rows = [], []
    for m in measures:
        for who in ("A", "B", "A_and_B", "A_or_B"):
            for lab, confs in (("HIGH+MEDIUM", PRIMARY_CONF), ("all", ALL_CONF)):
                def f(us, m=m, who=who, confs=confs):
                    if not us:
                        return (np.nan, np.nan, np.nan)
                    a = np.concatenate([u["auto"][m] for u in us])
                    r = np.concatenate([posv(u, who, confs) for u in us])
                    return prf(a, r)
                p, r, f1 = f(units)
                lo, hi = boot(f, units, rng, B_ if lab == "HIGH+MEDIUM" else 500)
                prf_rows.append({"measure": m, "label": MEASURE_LABEL[m], "reference": who, "coder_confidence": lab,
                                 "precision": p, "precision_lo": lo[0], "precision_hi": hi[0], "recall": r, "recall_lo": lo[1],
                                 "recall_hi": hi[1], "F1": f1, "F1_lo": lo[2], "F1_hi": hi[2],
                                 "auto_positive_share": float(np.mean(np.concatenate([u["auto"][m] for u in units]))),
                                 "status": "descriptive" if m in CONFIRM_MEASURES else "exploratory"})
        # strata: recall by coder slot and by confidence; precision by classifier slot; split 2019 vs other
        for who in ("A", "B"):
            rec_slot = defaultdict(lambda: [0, 0])
            rec_conf = defaultdict(lambda: [0, 0])
            prec_slot = defaultdict(lambda: [0, 0])
            for u in units:
                a = u["auto"][m]
                ref = posv(u, who, PRIMARY_CONF)
                ts = token_attr(u[who], u["n"], PRIMARY_CONF, "slot")
                cl = conf_level(u[who], u["n"])
                for t in range(u["n"]):
                    if ts[t] is not None:
                        rec_slot[ts[t]][0] += int(a[t])
                        rec_slot[ts[t]][1] += 1
                    if cl[t] is not None:
                        rec_conf[cl[t]][0] += int(a[t])
                        rec_conf[cl[t]][1] += 1
                    if a[t]:
                        prec_slot[u["cls_slot"][t]][0] += int(ref[t])
                        prec_slot[u["cls_slot"][t]][1] += 1
            for kind, d in (("recall by coder slot", rec_slot), ("share of coder tokens covered, by confidence", rec_conf),
                            ("precision by classifier slot", prec_slot)):
                for k, (num, den) in sorted(d.items()):
                    strata_rows.append({"measure": m, "reference": who, "stratum_kind": kind, "stratum": k, "numerator": num,
                                        "denominator": den, "value": num / den if den else float("nan")})
            for grp in ("2019", "other"):
                us = [u for u in units if u["group"] == grp]
                if us:
                    p, r, f1 = prf(np.concatenate([u["auto"][m] for u in us]), np.concatenate([posv(u, who, PRIMARY_CONF) for u in us]))
                    strata_rows.append({"measure": m, "reference": who, "stratum_kind": "precision / recall / F1 by sample group",
                                        "stratum": grp, "numerator": "", "denominator": len(us), "value": f"{p:.4f} / {r:.4f} / {f1:.4f}"})
    L.write_csv(out_dir / "calibration_prf.csv", prf_rows)
    L.write_csv(out_dir / "calibration_strata.csv", strata_rows)

    # ---- slot classifier vs coders
    cls_rows = []
    summary = {}
    for who in ("A", "B"):
        xs, ys = [], []
        for u in units:
            for sp in u[who]:
                xs.append(sp["slot"])
                ys.append(u["sc"].classify(sp["s"], sp["e"]))
        conf = Counter(zip(xs, ys))
        for (c, k), n in sorted(conf.items()):
            cls_rows.append({"coder": who, "coder_slot": c, "classifier_slot": k, "spans": n})
        summary[who] = {"spans": len(xs), "agreement": float(np.mean(np.array(xs) == np.array(ys))) if xs else float("nan"),
                        "kappa": kappa(xs, ys) if xs else float("nan")}
    L.write_csv(out_dir / "calibration_slot_classifier.csv", cls_rows)
    meta = {"classifier_vs_coder": summary, "measures": measures, "B": B_, "utterances_both": len(units),
            "groups": dict(Counter(u["group"] for u in units))}
    L.write_json(out_dir / "calibration_meta.json", meta)
    print(json.dumps({"agreement": {k: agr[k] for k in ("primary_HIGH_MEDIUM",)}, "classifier": summary}, indent=1, default=str))
    return agr, prf_rows, strata_rows, meta


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--sample", default=str(L.ROOT / "corpus" / "transcripts" / "samples" / "parry_sample_300.jsonl"))
    ap.add_argument("--coding-a", default=str(L.HERE / "coding_A.jsonl"))
    ap.add_argument("--coding-b", default=str(L.HERE / "coding_B.jsonl"))
    ap.add_argument("--out", default=str(L.RESULTS))
    ap.add_argument("--auto", default=None)
    ap.add_argument("--B", type=int, default=B)
    a = ap.parse_args()
    auto = None
    if a.auto:
        auto = {k: {m: np.array(v, bool) for m, v in d.items()} for k, d in json.loads(Path(a.auto).read_text()).items()}
    run(a.sample, a.coding_a, a.coding_b, a.out, auto=auto, B_=a.B)


if __name__ == "__main__":
    main()
