#!/usr/bin/env python3
"""Write review/provenance_v2.md from the machine evidence and the reviewer's recorded judgments (draft v2).

    source .venv/bin/activate
    python -I review/provenance_check.py composition/drafts/v2.jsonl review/provenance_v2_evidence.json
    python -I review/poem_density.py composition/drafts/v2.jsonl review/poem_density_v2.json
    python -I review/provenance_v2_extra.py composition/drafts/v2.jsonl review/provenance_v2_evidence.json \
        review/provenance_v2_extra.json
    python -I review/provenance_report_v2.py

Same classes and verdict criteria as review/provenance_report.py (v1); the helpers are imported from it.
Classification order for every `sources` entry:
  1. JUDGMENTS below (reviewer's decision with reason and Homeric parallel);
  2. provenance_report.auto_class (exact / mobility / movable nu, from the evidence);
  3. COINAGE entries: ATTESTED-MODIFIED (substitution of the coined name into an attested slot) if every Homeric
     model word named in the entry stands in the cited model line at the position the coined name has in the
     verse (review/provenance_v2_extra.json, name_slots); otherwise no decision (the script stops);
  4. other entries whose cited lines contain the string but whose string is not in the verse word for word:
     ATTESTED-MODIFIED, the kind stated from the words kept and changed plus the record's own modification
     kinds; 'structural model' when no content word is shared.
Verdicts (as v1): FAIL if a cited line lacks the claimed string, or an entry labelled ATTESTED-EXACT (string of
>= 2 words) is not exact, or a form unattested in Homer is not disclosed at all; QUERY if the classification is
debatable (single words labelled exact at a position Homer never gives them; counts in `count` fields that the
recorded query does not reproduce; name slots that the model line does not show; a citation field that cites no
line; a form unattested in Homer disclosed in an entry but not listed in `coinages`); PASS otherwise.
Bookkeeping errors that do not change a class (a wrong `position` field for an exact string whose actual position
is attested; counts inside free-text notes; a `mobility` label where nothing moves) are listed as jsonl
corrections and do not affect the verdict.
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
import provenance_report as R  # noqa: E402  (v1 helpers: auto_class, cited_problem, esc ...)

NAME_PAR = "-"
FUNC = None  # filled from review/poem_density.py (frozen list) in main()

EV = ROOT / "review/provenance_v2_evidence.json"
DENS = ROOT / "review/poem_density_v2.json"
DENS1 = ROOT / "review/poem_density_v1.json"
EXTRA = ROOT / "review/provenance_v2_extra.json"
JSONL = ROOT / "composition/drafts/v2.jsonl"
OUT = ROOT / "review/provenance_v2.md"

ATR = ("ATTESTED-MODIFIED", "shape model for the LSSL name slot: Ἀτρεΐδ- (the records' query `--loose ατρειδ`, a "
       "substring) 210x, 64 at 3-5 (reproduced; the v1 count error is fixed); cited Il. 1.102 ἥρως Ἀτρεΐδης has it at 3-5",
       "Ἀτρεΐδης (nom.) 34x at 3-5 (`--ngram`)", None)
ATR = ("M",) + ATR[1:]
J = {
 (1, 0): ("M", "inflection ἄνδρα → dual ἄνδρε; 1-5.5 kept", "ἄνδρε line-initial in ἄνδρε δύω (Il. 23.659 = 23.802)", None),
 (1, 3): ("M", "truncation: ἄνδρε δύω → ἄνδρε (δύω dropped); ἄνδρε keeps 1-1.5 (6 of 9)", "-", None),
 (1, 4): ("M", "inflection δαΐφρονα → dual δαΐφρονε (0x in Homer; now listed in `coinages`); slot 6-8 kept",
          "-ονε duals of the same declension: κρατερόφρονε (Od. 11.299), δαήμονε (Od. 16.253), both verified", None),
 (4, 0): ("M", "structural model: two subjects of διαστήτην joined by τε … καί (only τε, καί shared)", "-", None),
 (4, 1): ("M", "substitution of both names in the frame name τε καί epithet + name; τε (5.5) and καί (6) at the same positions as in Il. 14.29",
          "Il. 14.29 = 14.380 Τυδεΐδης Ὀδυσεύς τε καὶ Ἀτρεΐδης Ἀγαμέμνων", None),
 (4, 3): ("M", "substitution of 1-5.5 and of the name at 9.5-12; τε καὶ ἀντίθεος kept at 5.5-9", "τε καὶ ἀντίθεος + SSLX name 3x (Il. 20.232, Od. 3.414, 8.119)", None),
 (7, 3): ("M", "inflection δεύτερος → δεύτερον and mobility (Homer 9-12, verse 1-3.5)", "adverbial δεύτερον αὖ at 1-3 5x (Il. 3.332)", None),
 (19, 2): ("M", "inflection δεύτερος → δεύτερον; 9-12 kept", "δεύτερον αὖ (Il. 3.332)", None),
 (19, 4): ATR, (24, 3): ATR, (54, 2): ATR, (56, 3): ATR,
 (20, 1): ("M", "substitution μέν → δέ (τρὶς δέ μιν 0x); the δέ-limb of the counting pair", "τρὶς μέν … τρὶς δέ: Il. 18.155 / 18.157, 21.176 / 21.177", None),
 (20, 2): ("M", "structural: only αὖτʼ shared (at 3 in both)", "-", None),
 (22, 6): ("M", "syntactic parallel only (dual subject τώ with a plural verb); no word of the verse", "-", None),
 (22, 7): ("M", "syntactic parallel only (as entry 6)", "-", None),
 (24, 1): ("M", "the same formula with αὖτʼ for αὖθʼ (aspiration before the rough breathing of Ἑλβέτιος)",
           "τὸν δʼ αὖθʼ Ἱππολόχοιο (Il. 6.144) beside τὸν δʼ αὖτʼ 28x", None),
 (24, 4): ("M", "inflection: movable ν added, δάμασε → δάμασεν (the ν-form is 0x in Homer), same slot 5.5-7",
           "the same formula with and without movable ν: περὶ στήθεσσιν ἔδυνε (Il. 11.19) / ἔδυνεν (Il. 3.332)", None),
 (24, 5): ("M", "parallel only (the σσ-variant δάμασσε, not in the verse)", "-", None),
 (29, 1): ("M", "substitution: coined name + δʼ αὖτʼ at 1-3; the cited Il. 8.55 (Τρῶες δʼ αὖθʼ ἑτέρωθεν) is a hit of the recorded query",
           "closer: Ἕκτωρ δʼ αὖτʼ Αἴαντος (Il. 17.304, 1-3), Αἴας δʼ αὖτʼ (Il. 14.469, 1-3)", None),
 (58, 1): ("M", "substitution: coined name + δʼ αὖτʼ at 1-3 (as 29)", "Ἕκτωρ δʼ αὖτʼ (Il. 17.304, 1-3), Αἴας δʼ αὖτʼ (Il. 14.469)", None),
 (38, 4): ("M", "structural parallel: the relative clause that follows λέων ὣς in Il. 20.165 (the verse continues with the Il. 5.137 clause in 39)", "-", None),
 (39, 1): ("M", "structural: the opening (Il. 5.136) of the simile whose relative clause 39 keeps", "-", None),
 (43, 5): ("M", "separation: ἀνῆκε (4-5.5) … θυμός (9-10), verb before subject", "verb before θυμὸς ἀγήνωρ: πάλιν αὖτις ἀνήσει θυμὸς ἀγήνωρ (Il. 2.276)", None),
 (44, 1): ("M", "unelided ἔκφερε for ἔκφερʼ (0x; listed in `coinages`)", "unelided imperfects of the same verb: ἐξέφερον (Il. 23.377), ἔφερεν (Il. 24.232)", None),
 (44, 2): ("M", "parallel only (unelided compound imperfect, not in the verse)", "-", None),
 (44, 3): ("M", "parallel only (unelided simplex, not in the verse)", "-", None),
 (44, 6): ("E", "δʼ αὖ at 3 (28 of 110 at 3-3, the recorded query)", "e.g. Il. 3.200 οὗτος δʼ αὖ Λαερτιάδης (δʼ αὖ at 3 before a name)",
           "citation field 'Il. 1.?-…' cites no line (the string itself is verified by the recorded query)"),
 (51, 2): ("M", "substitution of the name Ὀδυσῆος → Ζοκοβῆος at 9.5-12 (ἀντιθέου kept at 7-9)", "ἀντιθέου Ὀδυσῆος at 7-12 (Od. 20.369)", None),
 (51, 3): ("M", "structural (shape) model for the SSLX genitive at 9.5-12: no word shared", "-", None),
}

MOVE_NONE = {15, 43}   # records whose 'mobility' modification says that nothing moves


def toks(s):
    return [t.core for t in G.tokenize(G.nfc(s))]


def generic_modified(s, rec_ev, rec):
    f0 = s["fragments"][0]
    vw = set(rec_ev["words"])
    H = f0["H"]
    tk = toks(H)
    kept = [t for t in tk if G.loose(t) in vw]
    gone = [t for t in tk if G.loose(t) not in vw]
    content_kept = [t for t in kept if G.loose(t) not in FUNC]
    if not content_kept:
        return "structural model (no content word shared" + (f"; shared: {' '.join(kept)}" if kept else "") + ")"
    return f"kept {' '.join(kept)}; replaced or dropped: {' '.join(gone) or '-'}"


def slot_class(n, s, slots):
    words = set(G.loose(w) for w in toks(s["text"] + " " + (s.get("query") or "") + " " + (s.get("citation") or "")))
    cand = [x for x in slots.get(n, []) if G.loose(x["model"]) in words]
    if not cand:
        return None
    ok = all(x["same_position"] and x["model_in_line"] for x in cand)
    desc = "; ".join(f"{x['coined']} at {x['verse_position']} = {x['model']} at {x['model_position']} in {x['model_citation']}"
                     for x in cand)
    if ok:
        return ("M", "substitution of the coined name into the model's slot (" + desc + ")", NAME_PAR, None)
    return ("N", "the model line does not show the slot (" + desc + ")", "-", "name slot not shown by the model line")


def main():
    global FUNC
    import poem_density as PD
    FUNC = PD.FUNC
    global NAME_PAR
    c1, c2 = len(PD.P.C.ngram("βοὴν ἀγαθὸς Διομήδης")), len(PD.P.C.ngram("βοὴν ἀγαθὸς Μενέλαος"))
    NAME_PAR = (f"Homer alternates names in one slot: βοὴν ἀγαθὸς Διομήδης {c1}x / βοὴν ἀγαθὸς Μενέλαος {c2}x "
                "(6-12); the model line itself shows the slot (section 6)")
    ev = json.load(open(EV, encoding="utf-8"))
    dens = json.load(open(DENS, encoding="utf-8"))
    dens1 = json.load(open(DENS1, encoding="utf-8"))
    extra = json.load(open(EXTRA, encoding="utf-8"))
    recs = {json.loads(l)["n"]: json.loads(l) for l in open(JSONL, encoding="utf-8") if l.strip()}
    slots = {}
    for x in extra["name_slots"]:
        slots.setdefault(x["verse"], []).append(x)
    zero = {(z["n"], z["loose"]): z for z in extra["forms_with_0_homeric_hits"]}

    rows, detail = [], []
    tallies, agree = Counter(), Counter()
    fails, queries = {}, {}
    unclaimed_all, cit_notes = [], []
    cls_of = {}
    exact2_lines = set()
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
                    sc = slot_class(n, s, slots)
                    if sc is None:
                        raise SystemExit(f"no slot evidence for line {n} entry {k}: {s['text']}")
                    cls, kind, par, qr = sc
                elif cls is None:
                    cited_ok = all(c["contains_any_fragment"] or c["in_query_hits"] for c in s["cited_check"]) and s["cited_check"]
                    if not cited_ok:
                        raise SystemExit(f"no judgment for line {n} entry {k}: {s['text']}")
                    cls, kind = "M", generic_modified(s, r, rec)
                    if r["parallels"]:
                        par = (f"record's quoted parallels for this line: {sum(p['verified'] for p in r['parallels'])}/"
                               f"{len(r['parallels'])} verified (section 7)")
            cls_of[(n, k)] = cls
            hw = s["fragments"][0]["H_loose"].split() if s["fragments"] else []
            if cls == "E" and len(hw) >= 2:
                exact2_lines.add(n)
            tallies[R.CLASSNAME[cls]] += 1
            comp = s["status"]
            agree[(comp, R.CLASSNAME[cls])] += 1
            for cit, ok_nu in R.cited_problem(s):
                rng = re.search(r"\d+\.\d+-\d+", s["citation"] or "")
                cit_notes.append(f"line {n} entry {k} {cit}: " + ("movable nu" if ok_nu else "inside the cited range" if rng else "MISSING"))
                if not ok_nu and not rng:
                    f_reasons.append(f"entry {k}: cited {cit} does not contain '{s['fragments'][0]['H']}'")
            if comp == "ATTESTED-EXACT" and cls != "E":
                if len(hw) >= 2:
                    f_reasons.append(f"entry {k}: '{s['fragments'][0]['H']}' labelled ATTESTED-EXACT but is {R.CLASSNAME[cls]} ({kind})")
                elif qr is None:
                    q_reasons.append(f"entry {k}: single word '{s['fragments'][0]['H']}' labelled exact: {kind}")
            if comp == "ATTESTED-MODIFIED" and cls == "E":
                q_reasons.append(f"entry {k}: labelled modified but exact")
            if s["claimed_count"] is not None and s["query_total"] is not None and s["claimed_count"] != s["query_total"]:
                q_reasons.append(f"entry {k}: count {s['claimed_count']} not reproduced (query gives {s['query_total']})")
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
        # unattested forms
        for w in r["words"]:
            z = zero.get((n, w))
            if z and not z["in_coinages"] and not z["in_coinage_entry"]:
                if z["named_in_modified_entry"]:
                    q_reasons.append(f"{z['form']} (0 hits) is disclosed as a modified form in an entry but not listed in `coinages` (as R8 required for δαΐφρονε, ἔκφερε)")
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
    cc = ev[0].get("cli_crosscheck") or {}
    text = "\n".join(recs[n]["text"] for n in sorted(recs))
    L_ = [G.loose(t.core) for t in G.tokenize(G.nfc(text))]

    def cnt(pfx):
        return sum(1 for w in L_ if w.startswith(pfx))
    D, D1 = dens["coverage"], dens1["coverage"]
    ref = dens["homeric_reference_verse_vs_rest_of_homer"]

    out = []
    A = out.append
    A("# Provenance review: composition/drafts/v2 (provenance-verifier)")
    A("")
    A("Generated by `review/provenance_report_v2.py` from `review/provenance_v2_evidence.json` (`review/provenance_check.py`), "
      "`review/provenance_v2_extra.json` (`review/provenance_v2_extra.py`) and `review/poem_density_v2.json` "
      "(`review/poem_density.py`); rerun:")
    A("")
    A("```")
    A("source .venv/bin/activate")
    A("python -I review/provenance_check.py composition/drafts/v2.jsonl review/provenance_v2_evidence.json")
    A("python -I review/poem_density.py composition/drafts/v2.jsonl review/poem_density_v2.json")
    A("python -I review/provenance_v2_extra.py composition/drafts/v2.jsonl review/provenance_v2_evidence.json review/provenance_v2_extra.json")
    A("python -I review/provenance_report_v2.py")
    A("```")
    A("")
    A("## 1. Method")
    A("")
    A(f"* As for v1 (review/provenance_v1.md section 1): every `sources` entry of the {len(recs)} records was rerun with its recorded "
      "query through the `Concordance` methods behind `homer/concordance.py`'s CLI, and every distinct query once more through the "
      "CLI itself (`--count`); the Homeric string of the entry was run with `ngram`, each cited line checked for it, and its "
      "position in the verse (`homer/scan.py --json`) compared with its Homeric positions. Every 2-word and longer window of every verse "
      "was run through `ngram` for unclaimed attested phrases. The Greek-plus-citation pairs quoted in the records' "
      "`modifications` were checked the same way.")
    A("* New in v2 (`review/provenance_v2_extra.py`): forms with 0 Homeric hits and where they are marked; the coined stems as "
      "loose substrings; the -είδης model of Ζοκοβείδης by NFC regex (the loose form drops the diaeresis, so Πηλείδη and "
      "Πηλεΐδη can only be told apart on the NFC text); the Ionic-η model of Νοβήκος; every coined name's slot against the "
      "position of the Homeric model word in the cited model line; the counts asserted in the notes; the records' `position` fields.")
    A("* Classes and verdicts: as v1. **ATTESTED-EXACT** = in the verse word for word (accent-insensitive; movable ν ignored and "
      "noted), in the cited lines, at a position Homer gives it; **ATTESTED-MODIFIED** = in the cited lines, changed in the verse "
      "(kind stated, with a Homeric parallel for that kind where one is offered or found); **NOT-ATTESTED** = not in the cited "
      "lines, or the configuration asserted does not occur. COINAGE entries are classified by their model: a substitution "
      "(ATTESTED-MODIFIED) when the model word stands in the cited line at the position the coined name takes in the verse. "
      "**FAIL** / **QUERY** / **PASS** criteria are those of v1 (header of `review/provenance_report_v2.py`); bookkeeping errors "
      "that change no class are listed in section 8 as jsonl corrections and do not affect the verdict.")
    A("")
    A("## 2. Summary")
    A("")
    A(f"* Lines: **PASS {verdicts['PASS']}, QUERY {verdicts['QUERY']}, FAIL {verdicts['FAIL']}** (of {len(recs)}). "
      + (lambda m: f"v1 (review/provenance_v1.md): PASS {m.group(1)}, QUERY {m.group(2)}, FAIL {m.group(3)} (of {m.group(4)})."
         if m else "")(re.search(r"PASS (\d+), QUERY (\d+), FAIL (\d+)\*\* \(of (\d+)\)",
                                 (ROOT / "review/provenance_v1.md").read_text(encoding="utf-8"))))
    A(f"* Source entries: {sum(tallies.values())}; reviewer's classes: ATTESTED-EXACT {tallies['ATTESTED-EXACT']}, "
      f"ATTESTED-MODIFIED {tallies['ATTESTED-MODIFIED']}, NOT-ATTESTED {tallies['NOT-ATTESTED']}.")
    A(f"* Recorded queries: {cc.get('distinct_queries')} distinct, each rerun with `python homer/concordance.py … --count`; mismatches "
      f"with the in-process rerun: {len(cc.get('mismatches', {}))}. Entries whose `count` or `query_hits` differ from the rerun "
      f"total: {sum(1 for r in ev for k, x in enumerate(r['sources']) if x['claimed_count'] != x['query_total'] or recs[r['n']]['sources'][k].get('query_hits') != x['query_total'])}.")
    A(f"* Cited lines checked: {n_cited}; lines that neither contain the claimed string nor are hits of the recorded query: "
      + ("; ".join(cit_notes) if cit_notes else "none") + ". One entry cites no line at all (44, entry 6: 'Il. 1.?-…').")
    A(f"* Homeric parallels quoted in the records' `modifications`: {n_par}; found in the cited line by the concordance: {n_par_ok}.")
    sc_bad = [r["n"] for r in ev if (r["scan"]["word_positions"] != recs[r["n"]]["scansion"]["word_positions"].split()
                                     or r["scan"]["pattern"] != recs[r["n"]]["scansion"]["pattern"])]
    A(f"* The records' `scansion.word_positions` and `pattern` agree with `homer/scan.py --json` in {len(recs) - len(sc_bad)} of "
      f"{len(recs)} lines" + (f" (differ: {', '.join(map(str, sc_bad))})" if sc_bad else "") + "; all positions above are scan.py's.")
    A("* FAIL lines: " + ("; ".join(f"**{n}** ({' / '.join(v)})" for n, v in sorted(fails.items())) or "none") + ".")
    A("* QUERY lines: " + ("; ".join(f"**{n}** ({' / '.join(v)})" for n, v in sorted(queries.items()) if n not in fails) or "none") + ".")
    A("")
    A("## 3. Composer's labels v. reviewer's classes (source entries)")
    A("")
    A("| composer | reviewer | entries |")
    A("|---|---|---|")
    for (c, m), v in sorted(agree.items()):
        A(f"| {c} | {m} | {v} |")
    A("")
    A("Every ATTESTED-EXACT label of a string of two or more words is exact (word for word, in the cited lines, at an attested "
      "position). The one composer-EXACT entry the automatic rule could not confirm is 44/6 (δʼ αὖ), whose citation field is a "
      "placeholder; the string is verified at the verse's position by the recorded query. Every single word labelled exact stands at a "
      "position Homer gives it. Every COINAGE entry's model shows the slot (section 6). The one composer-MODIFIED entry that is "
      "exact apart from a movable ν (24/4, δάμασε → δάμασεν) is classed as modified (the ν-form itself is 0x in Homer).")
    A("")
    A("## 4. Round-1 rulings (review/round_1.md) and brief Addendum A1")
    A("")
    A("| ruling | v1 item | v2 | check | result |")
    A("|---|---|---|---|---|")

    def lab(n, k):
        s = recs[n]["sources"][k]
        return f"{n}/{k} {s['status']} → reviewer {R.CLASSNAME[cls_of[(n, k)]]}"
    R8 = [
        ("R8", "5 δὲ πρῶτος (exact → modified)", "5", "verse rebuilt on δʼ ἑτέρωθεν; " + lab(5, 2)),
        ("R8", "15 ἀλλʼ ἐσσυμένως λάβʼ ἄεθλον", "23", lab(23, 3) + "; " + lab(23, 4)),
        ("R8", "20 Il. 5.151 'model'", "20", "Il. 5.151 cited in v2 line 20: " + str(any("5.151" in (s["citation"] or "") for s in recs[20]["sources"]))),
        ("R8", "23 πάλιν αὖτις", "23", "πάλιν αὖτις claimed in v2 line 23: " + str(any("πάλιν" in s["text"] for s in recs[23]["sources"]))),
        ("R8", "24 τὸν δʼ αὖτʼ", "24", lab(24, 0) + "; " + lab(24, 1)),
        ("R8", "29 βοὴν ἀγαθὸν Μενέλαον (count 5)", "29", lab(29, 3) + f", count {recs[29]['sources'][3]['count']}"),
        ("R8", "31 φίλα γυῖα λέλυνται", "31", lab(31, 1)),
        ("R8", "46 ἀντιθέου Ὀδυσῆος / Πηληϊάδεω Ἀχιλῆος", "51", lab(51, 2) + "; " + lab(51, 3)),
        ("R8", "51 καὶ βάλε", "56", lab(56, 5) + " (βάλε δʼ at 7.5-9, as Il. 15.541)"),
        ("R8", "52 shape model ἀντιθέου Ὀδυσῆος", "57", "verse rebuilt on Il. 16.466; " + lab(57, 2)),
        ("R8", "22 σφαῖραν, βάλλον (single words)", "22", lab(22, 0) + "; " + lab(22, 2)),
        ("R8", "24, 33, 49 δίς; 50 αὖτε at 9-9.5", "24, 33, 54, 55", f"δίς in v2: {L_.count('δισ')}; αὖτε at 9-9.5: rebuilt"),
        ("R8", "28 ἔλαβεν", "28", lab(28, 3)),
        ("R8", "49 ἀμύνετο at 2-4", "54", lab(54, 5) + " (6-8, its only Homeric slot)"),
        ("R8", "55 τέλος", "60", lab(60, 1)),
        ("R8", "12 Il. 16.284 uncited", "12", lab(12, 0)),
        ("R8", "1 δαΐφρονε, 41 ἔκφερε", "1, 44", lab(1, 4) + "; " + lab(44, 1) + "; both in `coinages`: "
         + str(zero[(1, 'δαιφρονε')]["in_coinages"] and zero[(44, 'εκφερε')]["in_coinages"])),
        ("R8", "19, 33 ἀτρειδ- query and count", "19, 24, 54, 56", lab(19, 4) + f"; count {recs[19]['sources'][4]['count']} = query"),
        ("R8", "'mobility' labels that are substitutions", "all", "relabelled in 2, 5, 10, 12, 21, 32, 38; still 'mobility' where nothing moves: "
         + ", ".join(map(str, sorted(MOVE_NONE))) + " (new lines; section 8)", "applied; 2 new mislabels"),
        ("R8", "unclaimed 47 ἕλκε δὲ μέσσα λαβών· ῥέπε δʼ", "52", lab(52, 0)),
        ("R8", "unclaimed 34 κεν ἐξενάριξε", "34", "verse rebuilt (no ἐξενάριξε)"),
        ("R8", "unclaimed 1 ἄνδρε δύω", "1", lab(1, 3)),
        ("R2", "Ῥογῆρος ἰσόθεος φώς (27, 49)", "27, 54", f"ἰσόθεος in v2: {cnt('ισοθε')}; Ῥογῆρος now before κέρδεα / δεύτερον (consonant-initial)"),
        ("R3/A1.2", "Ζοκοβίδης, Νοβάκος", "4, 36, 53, 56; 55", f"Ζοκοβίδ- in v2: {cnt('ζοκοβιδ')}; Νοβάκ- in v2: {cnt('νοβακ')}; Ζοκοβείδης / Νοβήκος: section 5"),
        ("R4/A1.3", "δίς + verb", "-", f"δίς in v2: {L_.count('δισ')}"),
        ("R5/A1.3", "ἐξενάριξε ≤ 2, aristeia only", "-", f"ἐξενάριξ- in v2: {cnt('εξεναριξ')} (victory verbs now ἐδάμασσε, δάμασεν, ἐνίκα, ἤρατο κῦδος)"),
        ("R6/A1.3", "πάλιν only 'back'", "22", f"πάλιν in v2: {L_.count('παλιν')} (line 22, glossed 'back' by the record, at 7.5-8, an attested slot; the sense is for the philology review)"),
        ("A1.1", "name slots recorded", "all", "every coined name's slot checked against its model line: section 6"),
    ]
    for t in R8:
        a, b, c, d = t[:4]
        A(f"| {a} | {R.esc(b)} | {c} | {R.esc(d)} | {t[4] if len(t) > 4 else 'applied'} |")
    A("")
    A("## 5. The new Djokovic forms")
    A("")
    P = extra["patronymic"]
    st = extra["coined_stems_substring_hits"]
    A(f"* **0 Homeric hits**: `--loose` substrings ζοκοβ {st['ζοκοβ']}, νοβηκ {st['νοβηκ']}, νοβακ {st['νοβακ']} (and φεδερ {st['φεδερ']}, "
      f"ρογηρ {st['ρογηρ']}, ελβετ {st['ελβετ']}, σερβ {st['σερβ']}); no claimed coinage exists in Homer. Ζοκοβείδης (4, 36, 53, 56) "
      "and Νοβήκος (55) are listed in `coinages` with their analogical models in every record that uses them.")
    pe, pi = P["Πηλείδ (diphthong ει)"], P["Πηλεΐδ (ε-ϊ)"]
    A(f"* **The -είδης model** (records: 'as Πηλείδη from Πηλεύς with the diphthong ει as one long syllable (Il. 1.277 μήτε σὺ "
      f"Πηλείδη, LLL) beside Πηλεΐδης with short ι (38x, LSSL); cf. Πηλείωνα (Il. 22.7) beside Πηλεΐων- (48x)'). Verified: "
      f"Πηλείδ- with the diphthong {pe['total']}x, `{pe['hits'][0]}` (positions {pe['positions']}: Πη 3, λει 4, δη 5, i.e. LLL with "
      f"ει one long syllable); Πηλεΐδ- {pi['total']}x in all forms, of which nominative Πηλεΐδης "
      f"{P['Πηλεΐδης (nom.)']['total']}x; Πηλείων- {P['Πηλείων (diphthong)']['total']}x (`{P['Πηλείων (diphthong)']['hits'][0]}`), "
      f"Πηλεΐων- {P['Πηλεΐων (ε-ϊ)']['total']}x. The model holds; the figure '38x' is not reproduced by any query tried "
      f"(Πηλεΐδης {P['Πηλεΐδης (nom.)']['total']}, Πηλεΐδ- {pi['total']}): correct it in the four records (section 8).")
    am = P["Ἀμαρυγκ- (Ἀμαρυγκεύς and patronymics)"]
    at = P["Ἀτρείδ (diphthong)"]
    A(f"* **Closer parallels the records do not cite** (found by the same regex): the -εύς name Ἀμαρυγκεύς (`{am['hits'][2]}`) has "
      f"both patronymics, `{am['hits'][1]}` with the diphthong and `{am['hits'][0]}` with -εΐ-: the exact derivation Ζοκοβεύς → "
      f"Ζοκοβείδης, and outside the Πηλεύς family. A nominative -είδης with the diphthong: `{at['hits'][0]}`. Suggest citing "
      "Il. 4.517 and Od. 15.52 beside Il. 1.277.")
    ie = extra["ionic_eta"]
    A(f"* **Νοβήκος** (SLL at 6-8, η for the ᾱ of the name): the Ionic-epic η model Ἀθήνη is {ie['αθηνη --word']}x (`--loose αθηνη --word`), "
      f"Ἀθάνα {ie['αθανα --word']}x, as the record states; the slot model Μελανθὼ δεύτερον αὖτις (Od. 19.65) is verified "
      "(section 6). The dialect statement is marked [unverified] in the record, correctly (it is scholarship, not concordance output).")
    A("")
    A("## 6. Name slots: coined name v. Homeric model word (review/provenance_v2_extra.json)")
    A("")
    A("| verse | coined | position in the verse | word before / after | model | model line | model's position | before / after in the model | same | model word's positions in Homer |")
    A("|---|---|---|---|---|---|---|---|---|---|")
    for x in extra["name_slots"]:
        A(f"| {x['verse']} | {x['coined']} | {x['verse_position']} | {x['verse_prev'] or '^'} / {x['verse_next'] or '$'} | {x['model']} | "
          f"{x['model_citation']} | {x['model_position']} | {x['model_prev'] or '^'} / {x['model_next'] or '$'} | "
          f"{'yes' if x['same_position'] else '**no**'} | {R.esc(', '.join(f'{p} ({c})' for p, c in list(x['model_form_positions_in_homer'].items())[:4]))} |")
    rho = extra["rho_initial_at_6_after_vowel_final_word_at_5.5"]
    A("")
    allsame = all(x["same_position"] and x["model_in_line"] for x in extra["name_slots"])
    dio = [h for h in PD.P.C.ngram("Διομήδης") if h.pos_start == "9.5"]
    prevw = Counter(G.loose(h.text.split()[h.tok_start - 1]) for h in dio if h.tok_start > 0)
    n_kai = prevw.get("και", 0)
    A(("Every coined name stands where its model word stands in the cited line." if allsame else
       "**Some coined names do not stand where their model word stands (see 'same').**") + f" The slots that depend on a neighbour hold: "
      "Σέρβος at 9-9.5 and Σέρβον at 3-3.5 precede a vowel-initial word as Τεῦκρος does in Il. 8.273 and 12.350; Ῥογῆρος and Νοβήκος "
      "at 6-8 follow a vowel-final word as Μελανθώ does in Od. 19.65. Ῥογῆρος differs from its model in its initial ρ after a short "
      f"vowel at 5.5 (ἀφάμαρτε, 27, 33); Homer has a ρ-initial word at 6 after a vowel-final word ending at 5.5 {rho['count']} times "
      f"(e.g. {rho['examples'][1].split(' | ')[0]}; {rho['examples'][3].split(' | ')[0]}), so the short final vowel is Homeric there "
      f"(a scansion point; check_line.py gives no flag). Bare Ζοκοβείδης after ἂψ (56): of the {len(dio)} Διομήδης at 9.5-12, "
      f"{len(dio) - n_kai} follow an epithet ({', '.join(f'{w} {c}' for w, c in prevw.most_common() if w != 'και')}) and {n_kai} "
      "follows καί, so the bare name after a non-epithet is a small extension of the model, not a new slot.")
    A("")
    A("## 7. Per-line table")
    A("")
    A("Entries: `k:E/M/N` = entry k, reviewer's class (details in section 10). Parallels = the record's quoted Homeric parallels found "
      "in the cited line / quoted. Unclaimed = maximal attested windows not contained in any entry.")
    A("")
    A("| n | verse | verdict | entries | parallels | unclaimed attested windows | reasons |")
    A("|---|---|---|---|---|---|---|")
    out.extend(rows)
    A("")
    A("## 8. Unclaimed phrases, coinages, jsonl corrections")
    A("")
    A("* Unclaimed attested windows (all listed in the table): " + "; ".join(
        f"{n}: {w['ngram']} ({w['count']}x, {w['poem_position']}{'' if w['position_attested'] else ', not a Homeric position'})"
        for n, w in unclaimed_all) + ". None is a formula the records should add: each only extends a claimed formula by a "
      "particle (δʼ αὖθʼ ἑτέρωθεν, δʼ αὖτʼ, δέ μιν, αὖτʼ ἐπί) or is a fragment of a disclosed mobility (δὴ περὶ in 48, δʼ ἂψ in 56).")
    zl = extra["forms_with_0_homeric_hits"]
    notlisted = sorted({(z["n"], z["form"]) for z in zl if not z["in_coinages"]})
    undisclosed = sorted({(z["n"], z["form"]) for z in zl if not (z["in_coinages"] or z["in_coinage_entry"] or z["named_in_modified_entry"])})
    A("* Forms with 0 Homeric hits (`--loose … --word`): " + ", ".join(dens["unattested_forms"]) + ". Undisclosed: "
      + (", ".join(f"{f} ({n})" for n, f in undisclosed) or "none") + ". Disclosed but not listed in `coinages`: "
      + (", ".join(f"{f} ({n})" for n, f in notlisted) or "none") + " (QUERY, jsonl only).")
    pf = extra["position_field_mismatches"]
    exact_pf = [p for p in pf if cls_of[(p["n"], p["k"])] == "E"]
    A("* jsonl corrections (no verdict effect):")
    for p in exact_pf:
        A(f"  * {p['n']}/{p['k']} '{p['text']}': `position` {p['position_field']}, but the string stands at {', '.join(p['verse_position'])} "
          f"in the verse (attested there: {p['homer_positions'].get(p['verse_position'][0], 0)}x)")
    A("  * " + ", ".join(map(str, sorted(MOVE_NONE))) + ": a `modifications` entry of kind 'mobility' that states that no word moves; "
      "drop it or relabel ('position kept')")
    A("  * 44/6: citation 'Il. 1.?-…' (a placeholder); cite a line, e.g. Il. 3.200 (δʼ αὖ at 3)")
    A("  * 4, 36, 53, 56 (`coinages`, Ζοκοβείδης): 'Πηλεΐδης … 38x' → Πηλεΐδης 24x (nominative), Πηλεΐδ- 51x; add Il. 4.517 "
      "Ἀμαρυγκείδην / Il. 2.622 Ἀμαρυγκεΐδης (from Ἀμαρυγκεύς, Il. 23.630) and Od. 15.52 Ἀτρείδης")
    ncs = extra["note_counts"]
    A(f"  * 27, 33 (Ῥογῆρος slot note): 'Ἀχαιῶν 95x' at 6-8 → {ncs['Ἀχαιῶν'].get('6-8')}x")
    A("  * 29, 58: the model of Σέρβος δʼ αὖτʼ is better cited as Ἕκτωρ δʼ αὖτʼ (Il. 17.304, 1-3) than Il. 8.55 (δʼ αὖθʼ ἑτέρωθεν)")
    A("  * 30, 54: the apposition parallel αὐτὰρ ὅ γʼ ἥρως (7x) is at 9-12 in all seven lines, not line-initial; the parallel "
      "holds for the apposition, not for the position")
    A("")
    A("## 9. Formulaic density (review/poem_density.py)")
    A("")
    A(f"Method as v1 (section 6 there): I = Homer, M = the poem ({dens['verses']} verses, {dens['tokens']} tokens); n-grams within one "
      "verse, compared as `concordance.py --ngram`; coverage = share of tokens inside at least one attested word n-gram; `base` drops "
      f"n-grams made only of function words ({dens['func_words']} frozen loose forms); `min2` = at least 2 Homeric occurrences; 95% CI "
      f"bootstrap over verses, B = {dens['B']}; shuffled = poem tokens permuted over positions, R = {dens['R']}; Homeric reference = "
      "each Homeric verse against the rest of Homer, token-weighted.")
    A("")
    A("| definition | coverage % [95% CI] | without the verbatim Homeric verses | without tokens unattested in Homer | shuffled % | excess (pp) | Homeric verse v. rest of Homer % | reference v. the 'without verbatim' interval | v1 coverage % |")
    A("|---|---|---|---|---|---|---|---|---|")
    for k in ["n2_all_min1", "n2_base_min1", "n3_all_min1", "n3_base_min1", "n2_base_min2", "n3_base_min2"]:
        d = D[k]
        x = d["excluding_verbatim_verses"]
        rel = "inside" if x["ci95"][0] <= ref[k] <= x["ci95"][1] else ("below" if ref[k] < x["ci95"][0] else "above")
        A(f"| {k} | {d['coverage']} [{d['ci95'][0]}, {d['ci95'][1]}] | {x['coverage']} [{x['ci95'][0]}, {x['ci95'][1]}] | "
          f"{d['excluding_tokens_unattested_in_homer']} | {d['shuffled_mean']} [{d['shuffled_2.5_97.5'][0]}, {d['shuffled_2.5_97.5'][1]}] | "
          f"{d['excess_pp']} | {ref[k]} | {rel} | {D1[k]['coverage']} |")
    x0 = D["n2_all_min1"]["excluding_verbatim_verses"]
    A("")
    A(f"* **Verbatim Homeric verses: {dens['verses_identical_to_a_homeric_verse']} of {dens['verses']}** "
      f"({', '.join(map(str, dens['verbatim_verse_numbers']))}); v1: {dens1['verses_identical_to_a_homeric_verse']} of {dens1['verses']}. "
      f"The 'without' column drops them ({x0['verses']} verses, {x0['tokens']} tokens). {dens['tokens_unattested_in_homer']} tokens "
      "are forms unattested in Homer (section 8) and can never be covered.")
    A(f"* **Lines with at least one ATTESTED-EXACT formula of 2 or more words**: {dens['lines_with_claimed_exact_formula_ge2_words']} of "
      f"{dens['verses']} = **{dens['lines_with_claimed_exact_formula_ge2_words_pct']}%** (claimed strings found verbatim at a Homeric "
      f"position, poem_density.py; v1 {dens1['lines_with_claimed_exact_formula_ge2_words_pct']}%); by the reviewer's classes (entries "
      f"classed E with 2 or more words): {len(exact2_lines)} of {len(recs)}. Counting only formulas not made of function words alone: "
      f"{dens['lines_with_claimed_exact_formula_ge2_words_not_function_only_pct']}% (none in "
      f"{', '.join(map(str, dens['lines_without_claimed_exact_formula_ge2_words_not_function_only'])) or '-'}). Unclaimed included, any "
      f"attested non-function-word n-gram at a Homeric position: {dens['lines_with_any_attested_ngram_at_homeric_position_pct']}% (none "
      f"in {', '.join(map(str, dens['lines_without_any_attested_ngram_at_homeric_position'])) or '-'}).")
    below = [k for k in D if ref[k] < D[k]["excluding_verbatim_verses"]["ci95"][0]]
    inside = [k for k in D if D[k]["excluding_verbatim_verses"]["ci95"][0] <= ref[k] <= D[k]["excluding_verbatim_verses"]["ci95"][1]]
    A(f"* Reading (exploratory; {dens['verses']} verses): with every verse counted the poem's coverage is above the Homeric reference on "
      f"every definition. Without the copied verses the reference lies inside the poem's 95% interval for {', '.join(inside) or 'none'} and "
      f"below it for {', '.join(below) or 'none'}. As in v1, this measures reuse of attested wording by a composer working from the "
      "concordance, not oral composition; Homer's own figure includes his repeated verses, as the poem's includes its copied ones.")
    A("")
    A("## 10. Source entries in detail")
    A("")
    A("Columns as v1: composer's status; cited lines containing the string or hits of the recorded query / cited lines; count claimed / "
      "recorded query's hits / hits of the claimed string (`ngram`); the string's Homeric positions (top 4); its position in the verse "
      "if there word for word; reviewer's class and modification; Homeric parallel for that kind of modification ('-' = none needed "
      "or none offered; the record's own parallels are counted in section 7).")
    A("")
    A("| n | k | entry text | composer | citation | cited ok | count c/q/H | Homeric positions | verse position | reviewer | Homeric parallel |")
    A("|---|---|---|---|---|---|---|---|---|---|---|")
    out.extend(detail)
    A("")
    OUT.write_text("\n".join(out) + "\n", encoding="utf-8")
    print(dict(verdicts), dict(tallies))
    print("FAIL:", {n: v for n, v in sorted(fails.items())})
    print("QUERY:", {n: v for n, v in sorted(queries.items()) if n not in fails})
    print("agree:", dict(agree))


if __name__ == "__main__":
    main()
