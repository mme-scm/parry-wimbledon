#!/usr/bin/env python3
"""Scan the whole of Homer and build the derived tables.

    python homer/build_tables.py

Pass 1 scans every line of homer/lines.tsv with all α/ι/υ free (resolved only
by fitting the hexameter, plus the accent rules).  From the lines with a
unique scansion it collects the dichrona whose quantity is fixed
(homer/dichrona.tsv).  Pass 2 rescans every line, now preferring the attested
quantity of each dichronon (a contrary quantity costs the tier-1 licence
`dichronon_contra`).  Pass 2 is the reference scansion (homer/scansion.tsv);
the tables below are built from it:

    homer/dichrona.tsv          quantities of α/ι/υ per word form (from pass 1)
    homer/scansion.tsv          one row per line (pass 2)
    homer/licences.tsv          every licence attested per word form
    homer/positions.tsv         word-end frequency at each metrical position
    homer/validation_stats.json figures for homer/validation.md
"""
import collections
import csv
import json
import pathlib
import sys
import time

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import greek as G  # noqa: E402
import scan as S  # noqa: E402

POSITIONS = ["1", "1.5", "2", "3", "3.5", "4", "5", "5.5", "6", "7", "7.5", "8",
             "9", "9.5", "10", "11", "12"]
ELEMENT = {}
for f in range(1, 7):
    ELEMENT[str(2 * f - 1)] = (f, "longum")
    if f < 6:
        ELEMENT[f"{2 * f - 1}.5"] = (f, "biceps, first short")
        ELEMENT[str(2 * f)] = (f, "biceps (contracted, or second short)")
ELEMENT["12"] = (6, "final anceps")
MAX_CIT = 10


def cit(r):
    return f"{r['work']}. {r['book']}.{r['line']}"


def write_tsv(path, header, rows):
    with open(path, "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f, delimiter="\t", lineterminator="\n", quoting=csv.QUOTE_NONE, escapechar="\\")
        w.writerow(header)
        for r in rows:
            w.writerow(r)


def status_counts(records):
    c = collections.Counter(r["status"] for r in records)
    n = len(records)
    out = {"lines": n}
    for k in ("unique", "multiple", "fail", "error"):
        out[k] = c.get(k, 0)
        out[k + "_pct"] = round(100 * c.get(k, 0) / n, 3) if n else 0
    out["tiers"] = dict(collections.Counter(str(r.get("tier")) for r in records if r["status"] != "fail"))
    for w in ("Il", "Od"):
        sub = [r for r in records if r["work"] == w]
        cw = collections.Counter(r["status"] for r in sub)
        out[w] = {"lines": len(sub), **{k: cw.get(k, 0) for k in ("unique", "multiple", "fail")}}
    return out


def build_dichrona(records):
    att = collections.defaultdict(lambda: {"L": [], "S": [], "env": collections.Counter(), "vowel": ""})
    for r in records:
        for form, idx, vowel, q, env, place in r.get("attest", []):
            d = att[(form, idx)]
            d[q].append(cit(r))
            d["env"][env] += 1
            d["vowel"] = vowel
    rows = []
    for (form, idx), d in sorted(att.items(), key=lambda x: (G.loose(x[0][0]), x[0][0], x[0][1])):
        nl, ns = len(d["L"]), len(d["S"])
        q = "L" if ns == 0 else ("S" if nl == 0 else "conflict")
        rows.append([form, G.loose(form), idx, d["vowel"], q, nl, ns,
                     ",".join(f"{k}:{v}" for k, v in d["env"].most_common()),
                     "; ".join(d["L"][:MAX_CIT]), "; ".join(d["S"][:MAX_CIT])])
    write_tsv(HERE / "dichrona.tsv",
              ["form", "loose", "vowel_no", "vowel", "quantity", "n_long", "n_short", "contexts",
               "citations_long", "citations_short"], rows)
    q = collections.Counter(r[4] for r in rows)
    return {"forms_vowels": len(rows), "L": q["L"], "S": q["S"], "conflict": q["conflict"],
            "attestations": sum(r[5] + r[6] for r in rows),
            "conflict_attestations_minority": sum(min(r[5], r[6]) for r in rows if r[4] == "conflict")}


def build_analogy(dichrona_rows_path=HERE / "dichrona.tsv"):
    """Quantity of a word-internal α/ι/υ predicted from other forms that share
    the same beginning (letters up to the next vowel): key -> counts of
    forms whose (majority) attested quantity is L / S."""
    learned = S.load_learned(dichrona_rows_path)
    cnt = collections.defaultdict(lambda: collections.Counter())
    examples = collections.defaultdict(list)
    for (form, vn), q in learned.items():
        key = S.analogy_key(form, vn)
        if key is None or len(key) < S.ANALOGY_MIN_KEY:
            continue
        cnt[key][q] += 1
        if len(examples[key]) < 8:
            examples[key].append(f"{form}:{vn}{q}")
    rows = []
    for key, c in sorted(cnt.items()):
        n = c["L"] + c["S"]
        q = max(("L", "S"), key=lambda x: c[x])
        ok = n >= S.ANALOGY_MIN_FORMS and c[q] / n >= S.ANALOGY_MIN_SHARE
        rows.append([key, q if ok else "undetermined", c["L"], c["S"], ", ".join(examples[key])])
    write_tsv(HERE / "dichrona_analogy.tsv", ["key", "quantity", "forms_long", "forms_short", "examples"], rows)
    return {"keys": len(rows), "determined": sum(1 for r in rows if r[1] in ("L", "S"))}


def evaluate_analogy(dichrona_path=HERE / "dichrona.tsv"):
    """Leave-one-form-out accuracy of the analogy predictor for several key
    lengths (used to choose scan.ANALOGY_EXTRA)."""
    learned = S.load_learned(dichrona_path)
    out = {}
    for extra in (0, 1, 2):
        cnt = collections.defaultdict(collections.Counter)
        items = []
        for (form, vn), q in learned.items():
            k = S.analogy_key(form, vn, extra)
            if k is None or len(k) < S.ANALOGY_MIN_KEY:
                continue
            cnt[k][q] += 1
            items.append((k, q))
        cov = cor = 0
        for k, q in items:
            c = cnt[k].copy()
            c[q] -= 1
            n = c["L"] + c["S"]
            if n >= S.ANALOGY_MIN_FORMS:
                p = max("LS", key=lambda x: c[x])
                if c[p] / n >= S.ANALOGY_MIN_SHARE:
                    cov += 1
                    cor += p == q
        out[f"extra={extra}"] = {"forms": len(items), "predicted": cov,
                                 "coverage_pct": round(100 * cov / len(items), 2),
                                 "accuracy_pct": round(100 * cor / max(cov, 1), 2)}
    return out


def build_licences(records):
    lic = collections.defaultdict(list)
    for r in records:
        if r["status"] != "unique":
            continue
        for nm, form, pos in r.get("licences", []):
            lic[(nm, form)].append(f"{cit(r)}@{pos}")
    rows = []
    for (nm, form), cits in sorted(lic.items(), key=lambda x: (x[0][0], -len(x[1]), x[0][1])):
        rows.append([nm, form, G.loose(form), len(cits), "; ".join(cits[:MAX_CIT])])
    write_tsv(HERE / "licences.tsv", ["licence", "form", "loose", "count", "citations"], rows)
    totals = collections.Counter()
    for (nm, form), cits in lic.items():
        totals[nm] += len(cits)
    return dict(totals)


def build_positions(records):
    rows = []
    stats = {}
    for subset_name, subset in (("all", None), ("Il", "Il"), ("Od", "Od")):
        recs = [r for r in records if r["status"] == "unique" and (subset is None or r["work"] == subset)]
        occ = collections.Counter()
        eo = collections.Counter()
        el = collections.Counter()
        for r in recs:
            for p in set(r["positions"]):
                occ[p] += 1
            for p in r["wordend_orth"]:
                eo[p] += 1
            for p in r["wordend_lex"]:
                el[p] += 1
        stats[subset_name] = (len(recs), occ, eo, el)
    n_all, occ, eo, el = stats["all"]
    for p in POSITIONS:
        foot, elem = ELEMENT[p]
        if p == "12":
            row = [p, foot, elem, occ[p], occ[p], 1.0, occ[p], 1.0, 1.0, 1.0, 1.0]
        else:
            fo = eo[p] / occ[p] if occ[p] else 0.0
            fl = el[p] / occ[p] if occ[p] else 0.0
            il = stats["Il"]
            od = stats["Od"]
            fil = il[2][p] / il[1][p] if il[1][p] else 0.0
            fod = od[2][p] / od[1][p] if od[1][p] else 0.0
            row = [p, foot, elem, occ[p], eo[p], round(fo, 5), el[p], round(fl, 5),
                   round(eo[p] / n_all, 5), round(fil, 5), round(fod, 5)]
        rows.append(row)
    write_tsv(HERE / "positions.tsv",
              ["position", "foot", "element", "lines_with_position", "wordend_orth", "freq_orth",
               "wordend_lex", "freq_lex", "freq_orth_per_line", "freq_orth_Il", "freq_orth_Od"], rows)
    return {"lines_used": n_all}


def main():
    t0 = time.time()
    rec1 = S.scan_corpus_records(learned=None)
    st1 = status_counts(rec1)
    print("pass 1:", {k: st1[k] for k in ("lines", "unique", "multiple", "fail")}, f"{time.time() - t0:.0f}s")
    dstats = build_dichrona(rec1)
    print("dichrona:", dstats)
    astats = build_analogy()
    astats["leave_one_out"] = evaluate_analogy()
    print("analogy:", astats)
    learned = S.load_learned(HERE / "dichrona.tsv")
    analogy = S.load_analogy(HERE / "dichrona_analogy.tsv")
    t1 = time.time()
    rec2 = S.scan_corpus_records(learned=learned, analogy=analogy)
    st2 = status_counts(rec2)
    print("pass 2:", {k: st2[k] for k in ("lines", "unique", "multiple", "fail")}, f"{time.time() - t1:.0f}s")
    S.write_scansion(rec2, HERE / "scansion.tsv")
    lstats = build_licences(rec2)
    pstats = build_positions(rec2)
    # changes between passes
    changed = sum(1 for a, b in zip(rec1, rec2) if a.get("pattern") != b.get("pattern"))
    fails = [[r["work"], r["book"], r["line"]] for r in rec2 if r["status"] == "fail"]
    anomalies = collections.Counter()
    for r in rec2:
        for a in r["row"][S.COLUMNS.index("anomalies")].split(","):
            if a:
                anomalies[a] += 1
    patterns = collections.Counter(r.get("pattern") for r in rec2 if r["status"] != "fail")
    out = {"pass1": st1, "pass2": st2, "dichrona": dstats, "analogy": astats, "licence_counts_unique_lines": lstats,
           "positions": pstats, "pattern_changed_pass1_to_pass2": changed, "failures": fails,
           "anomalies": dict(anomalies), "top_patterns": patterns.most_common(32),
           "runtime_s": round(time.time() - t0, 1)}
    (HERE / "validation_stats.json").write_text(json.dumps(out, indent=1, ensure_ascii=False) + "\n")
    print(json.dumps({k: out[k] for k in ("pattern_changed_pass1_to_pass2", "failures", "runtime_s")},
                     ensure_ascii=False))


if __name__ == "__main__":
    main()
