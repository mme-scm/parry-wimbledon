#!/usr/bin/env python3
"""Provenance verdicts for the frozen final poem (composition/final/poem.jsonl; text = composition/drafts/v4.txt).

    source .venv/bin/activate
    python -I review/provenance_check.py composition/final/poem.jsonl review/provenance_final_evidence.json
    python -I review/poem_density.py composition/final/poem.jsonl review/poem_density_final.json
    python -I review/provenance_v4_extra.py composition/final/poem.jsonl review/provenance_final_evidence.json \
        review/provenance_final_extra.json
    python -I review/provenance_report_final.py        # -> review/provenance_final.md

The v4 report script (review/provenance_report_v4.py) pointed at the final records: the same classes, the same verdict
criteria (its module docstring) and the same classification order, with its reviewer judgments J carried over. The four
J entries that carried a QUERY the final records answer (24/1, 29/6, 62/0: the slot is now shown by the cited model line;
33/1: the citation order corrected) are dropped, so those entries are classed from the evidence alone (slot_class /
auto_class) like any entry without a judgment; CIT_EXPLAINED is emptied, so every cited line must contain the claimed
string or be a hit of the recorded query on its own. Nothing else is judged here.
"""
import json
import re
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "review"))
sys.path.insert(0, str(ROOT / "homer"))
import greek as G  # noqa: E402
import provenance_report as R  # noqa: E402
import provenance_report_v4 as V4  # noqa: E402
import poem_density as PD  # noqa: E402

EV = ROOT / "review/provenance_final_evidence.json"
DENS = ROOT / "review/poem_density_final.json"
DENS_V4 = ROOT / "review/poem_density_v4.json"
EXTRA = ROOT / "review/provenance_final_extra.json"
JSONL = ROOT / "composition/final/poem.jsonl"
JSONL_V4 = ROOT / "composition/drafts/v4.jsonl"
OUT = ROOT / "review/provenance_final.md"

J = dict(V4.J)
for key in ((24, 1), (29, 6), (62, 0), (33, 1)):
    J.pop(key)   # decided from the evidence (slot_class / auto_class) like any other entry, not by the carried-over judgment
CIT_EXPLAINED = {}


def main():
    V4.FUNC = PD.FUNC
    c1, c2 = len(PD.P.C.ngram("βοὴν ἀγαθὸς Διομήδης")), len(PD.P.C.ngram("βοὴν ἀγαθὸς Μενέλαος"))
    V4.NAME_PAR = (f"Homer alternates names in one slot: βοὴν ἀγαθὸς Διομήδης {c1}x / βοὴν ἀγαθὸς Μενέλαος {c2}x (6-12); "
                   "the model line itself shows the slot (name_slots in review/provenance_final_extra.json)")
    ev = json.load(open(EV, encoding="utf-8"))
    dens = json.load(open(DENS, encoding="utf-8"))
    dens4 = json.load(open(DENS_V4, encoding="utf-8"))
    extra = json.load(open(EXTRA, encoding="utf-8"))
    recs = {json.loads(l)["n"]: json.loads(l) for l in open(JSONL, encoding="utf-8") if l.strip()}
    v4 = {json.loads(l)["n"]: json.loads(l) for l in open(JSONL_V4, encoding="utf-8") if l.strip()}
    assert [recs[n]["text"] for n in sorted(recs)] == [v4[n]["text"] for n in sorted(v4)], "final text != v4 text"
    slots = {}
    for x in extra["name_slots"]:
        slots.setdefault(x["verse"], []).append(x)
    zero = {(z["n"], z["loose"]): z for z in extra["forms_with_0_homeric_hits"]}

    rows, detail = [], []
    tallies, agree = Counter(), Counter()
    fails, queries = {}, {}
    unclaimed_all, cit_notes = [], []
    exact2_lines, exact2_content = set(), set()
    for r in ev:
        n = r["n"]
        rec = recs[n]
        f_reasons, q_reasons, ent = [], [], []
        for k, s in enumerate(r["sources"]):
            par, qr = "-", None
            if (n, k) in J:
                cls, kind, par, qr = J[(n, k)]
            else:
                cls, kind = R.auto_class(s, r)
                if cls == "M" and kind.startswith("mobility"):
                    f0 = s["fragments"][0]
                    kind += (f": verse {', '.join(f0['poem_positions']) or '-'}; Homer "
                             + ", ".join(f"{p} ({c})" for p, c in f0["homer_positions"].items()))
                if cls is None and s["status"] == "COINAGE":
                    sc = V4.slot_class(n, s, slots)
                    if sc is None:
                        raise SystemExit(f"no slot evidence for line {n} entry {k}: {s['text']}")
                    cls, kind, par, qr = sc
                elif cls is None:
                    cited_ok = all(c["contains_any_fragment"] or c["in_query_hits"] for c in s["cited_check"]) and s["cited_check"]
                    if not cited_ok:
                        raise SystemExit(f"no judgment for line {n} entry {k}: {s['text']}")
                    cls, kind = "M", V4.generic_modified(s, r, rec)
                    if r["parallels"]:
                        par = (f"record's quoted parallels for this line: {sum(p['verified'] for p in r['parallels'])}/"
                               f"{len(r['parallels'])} verified")
            hw = s["fragments"][0]["H_loose"].split() if s["fragments"] else []
            if cls == "E" and len(hw) >= 2:
                exact2_lines.add(n)
                if any(w not in PD.FUNC for w in hw):
                    exact2_content.add(n)
            tallies[R.CLASSNAME[cls]] += 1
            comp = s["status"]
            agree[(comp, R.CLASSNAME[cls])] += 1
            for cit, ok_nu in R.cited_problem(s):
                rng = re.search(r"\d+\.\d+-\d+", s["citation"] or "")
                expl = CIT_EXPLAINED.get((n, k, cit))
                cit_notes.append(f"line {n} entry {k} {cit}: " + ("movable nu" if ok_nu else f"explained: {expl}" if expl
                                                                  else "inside the cited range" if rng else "MISSING"))
                if not ok_nu and not rng and not expl:
                    f_reasons.append(f"entry {k}: cited {cit} does not contain '{s['fragments'][0]['H']}'")
            if comp == "ATTESTED-EXACT" and cls != "E":
                if len(hw) >= 2:
                    f_reasons.append(f"entry {k}: '{s['fragments'][0]['H']}' labelled ATTESTED-EXACT but is {R.CLASSNAME[cls]} ({kind})")
                else:
                    q_reasons.append(f"entry {k}: single word '{s['fragments'][0]['H']}' labelled exact: {kind}")
            if comp == "ATTESTED-MODIFIED" and cls == "E":
                q_reasons.append(f"entry {k}: labelled modified but exact")
            if s["claimed_count"] is not None and s["query_total"] is not None and s["claimed_count"] != s["query_total"]:
                q_reasons.append(f"entry {k}: count {s['claimed_count']} not reproduced (query `{s['query']}` gives {s['query_total']})")
            if qr:
                q_reasons.append(f"entry {k}: {qr}")
            f0 = s["fragments"][0] if s["fragments"] else {}
            hpos = ", ".join(f"{p} ({c})" for p, c in list(f0.get("homer_positions", {}).items())[:4]) or "-"
            ppos = ", ".join(f0.get("poem_positions") or []) or "-"
            cc = s["cited_check"]
            cit_ok = sum(1 for c in cc if c["contains_any_fragment"] or c["in_query_hits"])
            detail.append(f"| {n} | {k} | {R.esc(s['text'])} | {comp} | {R.esc(s['citation'])} | {cit_ok}/{len(cc)} | "
                          f"{s['claimed_count']} / {s['query_total']} / {f0.get('homer_total', '-')} | {R.esc(hpos)} | {ppos} | "
                          f"**{R.CLASSNAME[cls]}**{(': ' + R.esc(kind)) if kind else ''} | {R.esc(par)} |")
            ent.append(f"{k}:{cls}")
        for w in r["words"]:
            z = zero.get((n, w))
            if z and not z["in_coinages"] and not z["in_coinage_entry"]:
                if z["named_in_modified_entry"] or z["named_in_modifications"]:
                    q_reasons.append(f"{z['form']} (0 hits) is disclosed in the record but not listed in `coinages`")
                else:
                    f_reasons.append(f"form {z['form']} (0 hits) not marked")
        allw = r["windows"]

        def contained(w):
            return any(x is not w and x["i"] <= w["i"] and x["i"] + x["n"] >= w["i"] + w["n"] and x["n"] > w["n"]
                       for x in allw if not x["claimed"])
        unc = [w for w in allw if not w["claimed"] and not contained(w)]
        unclaimed_all += [(n, w) for w in unc]
        verdict = "FAIL" if f_reasons else ("QUERY" if q_reasons else "PASS")
        if f_reasons:
            fails[n] = f_reasons
        if q_reasons:
            queries[n] = q_reasons
        par_ok = sum(p["verified"] for p in r["parallels"])
        unc_s = "; ".join(f"{w['ngram']} ({w['count']}x, {w['poem_position']}{'' if w['position_attested'] else ', position not Homeric'})"
                          for w in unc) or "-"
        reasons = " / ".join(f_reasons + q_reasons) or "-"
        rows.append(f"| {n} | {R.esc(rec['text'])} | **{verdict}** | {' '.join(ent)} | {par_ok}/{len(r['parallels'])} | {R.esc(unc_s)} | {R.esc(reasons)} |")

    verdicts = Counter("FAIL" if n in fails else "QUERY" if n in queries else "PASS" for n in recs)
    n_cited = sum(len(s["cited_check"]) for r in ev for s in r["sources"])
    n_par = sum(len(r["parallels"]) for r in ev)
    n_par_ok = sum(p["verified"] for r in ev for p in r["parallels"])
    par_bad = [(r["n"], p["quoted"], p["citation"]) for r in ev for p in r["parallels"] if not p["verified"]]
    cc = ev[0].get("cli_crosscheck") or {}
    n_entries = sum(len(r["sources"]) for r in ev)
    n_entries_v4 = sum(len(v4[n]["sources"]) for n in v4)
    label_changes = [(n, k, v4[n]["sources"][k]["status"], recs[n]["sources"][k]["status"]) for n in recs
                     for k in range(len(v4[n]["sources"])) if v4[n]["sources"][k]["status"] != recs[n]["sources"][k]["status"]]
    new_entries = [(n, k, recs[n]["sources"][k]["text"]) for n in recs for k in range(len(v4[n]["sources"]), len(recs[n]["sources"]))]
    D, D4 = dens["coverage"], dens4["coverage"]
    ref = dens["homeric_reference_verse_vs_rest_of_homer"]
    slot_bad = []
    for s_ in [x for x in extra["name_slots"] if not x["same_position"]]:
        ents = [e for e in recs[s_["verse"]]["sources"] if e["status"] == "COINAGE"]
        words = set(G.loose(w) for e in ents for w in V4.toks(e["text"] + " " + (e.get("query") or "") + " " + (e.get("citation") or "")))
        if G.loose(s_["model"]) in words:
            slot_bad.append(s_)
    zero_undisclosed = [z for z in extra["forms_with_0_homeric_hits"] if not (z["in_coinages"] or z["in_coinage_entry"])]
    claims_bad = [c for c in extra["claims"] if any(v == "NOT A HIT" for v in c["cited"].values())]
    posf = extra["position_field_mismatches"]
    cl = extra["check_line"]

    out = []
    A = out.append
    A("# Provenance verdicts: composition/final/poem.jsonl (the frozen final poem; text = composition/drafts/v4.txt)")
    A("")
    A("Generated by `review/provenance_report_final.py` from `review/provenance_final_evidence.json` (`review/provenance_check.py`), "
      "`review/provenance_final_extra.json` (`review/provenance_v4_extra.py`) and `review/poem_density_final.json` (`review/poem_density.py`); "
      "rerun: the commands in the script's docstring. Criteria, classes and judgments: review/provenance_report_v4.py (its docstring), carried over; "
      "the record corrections themselves are listed in composition/final/record_edits.md.")
    A("")
    A("## Summary")
    A("")
    A(f"* Lines: **PASS {verdicts['PASS']}, QUERY {verdicts['QUERY']}, FAIL {verdicts['FAIL']}** (of {len(recs)}). v4 (review/provenance_v4.md): PASS 55, QUERY 8, FAIL 1.")
    A(f"* Verse text: identical to v4 in all {len(recs)} records (asserted). `homer/check_line.py` on the final text: {cl['n_verses']} verses, {cl['n_flagged']} flagged, {cl['n_unmetrical']} unmetrical.")
    A(f"* Source entries: {n_entries} (v4: {n_entries_v4}; {len(new_entries)} added); reviewer's classes: " + ", ".join(f"{k} {v}" for k, v in sorted(tallies.items())) + ".")
    A(f"* Labels changed since v4: {len(label_changes)} (" + "; ".join(f"{n}/{k} {a} → {b}" for n, k, a, b in label_changes) + ").")
    A(f"* Recorded queries: {cc.get('distinct_queries')} distinct, each rerun with `python homer/concordance.py … --count`; mismatches with the in-process rerun: {len(cc.get('mismatches', {}))}.")
    A(f"* Entries whose `count` the recorded query does not reproduce: {sum(1 for r in ev for s in r['sources'] if s['claimed_count'] is not None and s['query_total'] is not None and s['claimed_count'] != s['query_total'])}.")
    A(f"* Cited lines checked: {n_cited}; lines that neither contain the claimed string nor are hits of the recorded query: {sum(1 for c in cit_notes if c.endswith('MISSING'))}"
      + (" (" + "; ".join(c for c in cit_notes if c.endswith('MISSING')) + ")" if any(c.endswith('MISSING') for c in cit_notes) else "")
      + f"; movable-nu / in-range notes: {sum(1 for c in cit_notes if not c.endswith('MISSING'))}.")
    A(f"* Homeric parallels quoted in the records' `modifications`: {n_par}; found in the cited line by the concordance: {n_par_ok}" + (f"; not found: {par_bad}" if par_bad else "") + ".")
    A(f"* Coined-name slots (review/provenance_final_extra.json name_slots): {len(extra['name_slots'])} rows; the records' cited model lines that do not show the slot: "
      + (", ".join(f"{s['verse']} {s['coined']} v. {s['model']} ({s['model_citation']}: {s['condition']})" for s in slot_bad) or "none")
      + f". Rows marked 'no' in the table: {sum(1 for x in extra['name_slots'] if not x['same_position'])} (models the final COINAGE entries no longer name: the v4 entries' former models and the name-formation model Ἕκτωρ Πριαμίδης of the `coinages` field, kept for the audit trail).")
    A(f"* Forms with 0 Homeric hits not listed in `coinages` or a COINAGE entry: {len(zero_undisclosed)}" + (f" ({[(z['n'], z['form']) for z in zero_undisclosed]})" if zero_undisclosed else "") + ".")
    A(f"* Free-text claims rerun (review/provenance_v4_extra.py CLAIMS, {len(extra['claims'])}): with a cited line that is not a hit: {len(claims_bad)}.")
    A(f"* `position` fields that differ from the string's position in the verse: {len(posf)}" + (f" ({[(p['n'], p['k'], p['position_field'], p['verse_position']) for p in posf]})" if posf else "") + ".")
    A(f"* Lines with an ATTESTED-EXACT formula of ≥ 2 words (reviewer's classes): {len(exact2_lines)}/{len(recs)}; not function words only: {len(exact2_content)}/{len(recs)}. "
      f"poem_density.py: {dens['lines_with_claimed_exact_formula_ge2_words_pct']}% / {dens['lines_with_claimed_exact_formula_ge2_words_not_function_only_pct']}%.")
    A(f"* Density (review/poem_density.py, unchanged text): n2_all_min1 {D['n2_all_min1']['coverage']:.1f}% [{D['n2_all_min1']['ci95'][0]:.1f}, {D['n2_all_min1']['ci95'][1]:.1f}] "
      f"(v4 {D4['n2_all_min1']['coverage']:.1f}%); n3_all_min1 {D['n3_all_min1']['coverage']:.1f}%; n2_base_min2 {D['n2_base_min2']['coverage']:.1f}%; "
      f"verbatim Homeric verses {dens['verses_identical_to_a_homeric_verse']} of {dens['verses']}; Homeric reference n2_all_min1 {ref['n2_all_min1']:.1f}%.")
    A("")
    A("## Composer's labels v. reviewer's classes")
    A("")
    A("| composer | reviewer | entries |")
    A("|---|---|---|")
    for (a, b), c in sorted(agree.items()):
        A(f"| {a} | {b} | {c} |")
    A("")
    A("## Entries added in the final records")
    A("")
    for n, k, t in new_entries:
        A(f"* {n}/{k}: {R.esc(t)}")
    A("")
    A("## Per-line table")
    A("")
    A("Entries: `k:E/M/N` = entry k, reviewer's class. Parallels = the record's quoted Homeric parallels found in the cited line / quoted. "
      "Unclaimed = maximal attested windows not contained in any entry.")
    A("")
    A("| n | verse | verdict | entries | parallels | unclaimed attested windows | reasons |")
    A("|---|---|---|---|---|---|---|")
    out += rows
    A("")
    A("## Unclaimed attested windows")
    A("")
    for n, w in unclaimed_all:
        A(f"* {n}: {w['ngram']} ({w['count']}x, {w['poem_position']}{'' if w['position_attested'] else ', position not Homeric'})")
    A("")
    A("## Source entries in detail")
    A("")
    A("| n | k | entry | label | citation | cited ok | count / query / Homer | Homer positions | verse position | class | parallel |")
    A("|---|---|---|---|---|---|---|---|---|---|---|")
    out += detail
    OUT.write_text("\n".join(out) + "\n", encoding="utf-8")
    print(f"verdicts: {dict(verdicts)}; entries {n_entries}; classes {dict(tallies)}; label changes {len(label_changes)}; new entries {len(new_entries)}")
    print(f"CLI cross-check mismatches: {len(cc.get('mismatches', {}))}; MISSING cited lines: {sum(1 for c in cit_notes if c.endswith('MISSING'))}; parallels {n_par_ok}/{n_par}; slots not shown: {len(slot_bad)}; check_line flagged {cl['n_flagged']}")
    if fails or queries:
        print("FAIL:", fails)
        print("QUERY:", queries)


if __name__ == "__main__":
    main()
