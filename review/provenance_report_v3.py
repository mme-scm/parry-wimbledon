#!/usr/bin/env python3
"""Write review/provenance_v3.md from the machine evidence and the reviewer's recorded judgments (draft v3).

    source .venv/bin/activate
    python -I review/provenance_check.py composition/drafts/v3.jsonl review/provenance_v3_evidence.json
    python -I review/poem_density.py composition/drafts/v3.jsonl review/poem_density_v3.json
    python -I review/provenance_v3_extra.py composition/drafts/v3.jsonl review/provenance_v3_evidence.json \
        review/provenance_v3_extra.json
    python -I review/provenance_report_v3.py

Adapted from review/provenance_report_v2.py (same classes, same verdict criteria, same classification order; the
judgments J re-keyed to the v3 entries and extended to the rebuilt verses 23, 33, 36, 44, 51, 55, 56).
Same classes and verdict criteria as review/provenance_report.py (v1); the helpers are imported from it.
Classification order for every `sources` entry:
  1. JUDGMENTS below (reviewer's decision with reason and Homeric parallel);
  2. provenance_report.auto_class (exact / mobility / movable nu, from the evidence);
  3. COINAGE entries: ATTESTED-MODIFIED (substitution of the coined name into an attested slot) if every Homeric
     model word named in the entry stands in the cited model line at the position the coined name has in the
     verse (review/provenance_v3_extra.json, name_slots); otherwise no decision (the script stops);
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

EV = ROOT / "review/provenance_v3_evidence.json"
DENS = ROOT / "review/poem_density_v3.json"
DENS1 = ROOT / "review/poem_density_v2.json"   # previous round, for comparison
EXTRA = ROOT / "review/provenance_v3_extra.json"
JSONL = ROOT / "composition/drafts/v3.jsonl"
JSONL_PREV = ROOT / "composition/drafts/v2.jsonl"
OUT = ROOT / "review/provenance_v3.md"

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
 (19, 4): ATR, (24, 3): ATR, (54, 2): ATR, (56, 5): ATR,
 (20, 1): ("M", "substitution μέν → δέ (τρὶς δέ μιν 0x); the δέ-limb of the counting pair", "τρὶς μέν … τρὶς δέ: Il. 18.155 / 18.157, 21.176 / 21.177", None),
 (20, 2): ("M", "structural: only αὖτʼ shared (at 3 in both)", "-", None),
 (22, 6): ("M", "syntactic parallel only (dual subject τώ with a plural verb); no word of the verse", "-", None),
 (22, 7): ("M", "syntactic parallel only (as entry 6)", "-", None),
 (24, 1): ("M", "the same formula with αὖτʼ for αὖθʼ (aspiration before the rough breathing of Ἑλβέτιος)",
           "τὸν δʼ αὖθʼ Ἱππολόχοιο (Il. 6.144) beside τὸν δʼ αὖτʼ 28x", None),
 (24, 4): ("M", "inflection: movable ν added, δάμασε → δάμασεν (the ν-form is 0x in Homer), same slot 5.5-7",
           "the same formula with and without movable ν: περὶ στήθεσσιν ἔδυνε (Il. 11.19) / ἔδυνεν (Il. 3.332)", None),
 (24, 5): ("M", "parallel only (the σσ-variant δάμασσε, not in the verse)", "-", None),
 (29, 1): ("M", "substitution of the name in Ἕκτωρ δʼ αὖτʼ + verb (Il. 17.304, 1-3) → Σέρβος δʼ αὖτʼ + verb (Σέρβος δʼ αὖτʼ itself 0x); the model is now the round-2 one",
           "Αἴας δʼ αὖτʼ (Il. 14.469, 1-3); Ἕκτωρ δʼ αὖτʼ also Il. 3.76 (3-5)", None),
 (58, 1): ("M", "substitution of the name in Ἕκτωρ δʼ αὖτʼ + verb (Il. 17.304, 1-3), as 29", "Αἴας δʼ αὖτʼ (Il. 14.469, 1-3)", None),
 (38, 4): ("M", "structural parallel: the relative clause that follows λέων ὣς in Il. 20.165 (the verse continues with the Il. 5.137 clause in 39)", "-", None),
 (39, 1): ("M", "structural: the opening (Il. 5.136) of the simile whose relative clause 39 keeps", "-", None),
 (43, 5): ("M", "separation: ἀνῆκε (4-5.5) … θυμός (9-10), verb before subject", "verb before θυμὸς ἀγήνωρ: πάλιν αὖτις ἀνήσει θυμὸς ἀγήνωρ (Il. 2.276)", None),
 (23, 1): ("M", "expansion: δεύτερον αὖ (1-3) kept, the rest of the line replaced (the prize verb follows, as the verb of the second exploit follows in Il. 6.184)", "δεύτερον αὖ + verb: Il. 6.184", None),
 (23, 6): ("M", "substitution: μίγη (6-7) → ἄφαρ (6-7) before κρατερὸς + name at 7.5-12; Διομήδης → Ζοκοβείδης", "κρατερὸς Διομήδης after a word ending at 7: Il. 5.143", None),
 (33, 3): ("M", "mobility: the second καὶ βάλεν stands at 9-10 (Homer 1-2 only, 11x; the first καὶ βάλεν of the verse, at 1-2, is entry 0)",
           "the same kind: οὐδʼ ἀφάμαρτε at 3-5.5 (Il. 11.350, 13.160) and at 9-12 (Il. 14.403, 22.290)", None),
 (33, 5): ("M", "structural parallel: a repeated action given its own verb + verse-final αὖτις (no content word of the verse)",
           "καί + verb + αὖτις verse-final: καὶ ἀνήγαγον αὖτις (Il. 15.29, 7.5-12); verb + αὖτις: ἵξομαι αὖτις (Il. 6.367), ὑποδέξομαι αὖτις (Il. 18.59)", None),
 (36, 1): ("M", "substitution of the name-epithet formula at 6-12: ποδάρκης δῖος Ἀχιλλεύς → βοὴν ἀγαθὸς Φεδερῆρος (τρὶς μὲν ἔπειτʼ ἐπόρουσε kept at 1-5.5)",
           "the count line takes three different 6-12 completions (Il. 5.436, 16.784, 20.445); ἐπόρουσε βοὴν ἀγαθὸς Διομήδης at 3.5-12 (Il. 5.432, unclaimed)", None),
 (44, 0): ("M", "frame of the race-position line: ἔκφερʼ (unelided, entry 1) + the leader at 1-5.5, the follower's clause at 6-12 (ἐπὶ δʼ ὄρνυτο δῖος Ὀδυσσεύς → ὃ δʼ ἕσπετο κέρδεα εἰδώς)",
           "follower clause pronoun + δʼ + verb of following: ἡ δʼ ἕσπετο Παλλὰς Ἀθήνη (Od. 1.125), ὃ δʼ ἅμʼ ἕσπετο ἰσόθεος φώς (Il. 11.472)", None),
 (44, 1): ("M", "unelided ἔκφερε for ἔκφερʼ (0x; listed in `coinages`), line-initial as ἔκφερʼ in Il. 23.759 (1-1.5)",
           "the unelided imperfect line-initial: ἔκφερεν (Od. 15.470, 1-2)", None),
 (44, 2): ("M", "parallel only (the unelided imperfect with movable ν; not in the verse)", "-", None),
 (44, 4): ("M", "slot model: δʼ αὖτε at 3-3.5 + an SLS word at 4-5.5 before a vowel (γυναῖκας → Νοβῆκος); only δʼ αὖτε shared", "-", None),
 (44, 7): ("M", "substitution: ἡ → ὃ (the masculine pronoun) and Παλλὰς Ἀθήνη → κέρδεα εἰδώς; δʼ ἕσπετο kept at 7-8 (ὃ δʼ ἕσπετο itself 0x)",
           "ὃ δʼ + verb at 6-8 marking the change of subject: ὃ δʼ ἅμʼ ἕσπετο (Il. 11.472 = 15.559 = 16.632), ὃ δʼ ἐπέσσυτο (Il. 21.234, 21.601)", None),
 (51, 0): ("M", "structural model: τὴν μέν + genitive of the first owner, τὴν δʼ + genitive + epithet in -οιο of the second; both names replaced, ἄρʼ and αὖ added (shared: τὴν μέν, τὴν δʼ)", "-", None),
 (51, 4): ("M", "structural: pronoun + δʼ αὖ at 6-7 + the name phrase to the verse end; only δʼ αὖ shared", "-", None),
 (55, 3): ("M", "mobility: the second καὶ βάλεν at 9-10 (Homer 1-2 only, 11x), as 33",
           "οὐδʼ ἀφάμαρτε at 3-5.5 (Il. 11.350) and at 9-12 (Il. 22.290)", None),
 (55, 5): ("M", "structural parallel: a repeated action with its own verb + verse-final αὖτις, as 33", "καὶ ἀνήγαγον αὖτις (Il. 15.29)", None),
 (56, 0): ("M", "orthography of the elision: ἔνθʼ αὖτʼ (12x, 1-2) written ἔνθʼ αὖθʼ before the rough breathing of Ἑλβέτιος (ἔνθʼ αὖθʼ 0x, because ἔνθʼ αὖτʼ never precedes an aspirated word)",
           "αὖθʼ before a rough breathing 33x, αὖτʼ before a rough breathing 0x (NFC text): τὸν δʼ αὖθʼ Ἱππολόχοιο (Il. 6.144), Χρύσης δʼ αὖθʼ ἱερεύς (Il. 1.370)", None),
 (56, 1): ("M", "parallel only (αὖθʼ before a rough breathing; αὖθʼ itself is in the verse at 2)", "-", None),
 (56, 2): ("M", "parallel only (as entry 1)", "-", None),
 (56, 3): ("M", "structural: ἔνθʼ αὖτʼ + the subject name at 1-5 (Αἰνείας → Ἑλβέτιος at 3-5, αὖτʼ → αὖθʼ as entry 0)", "-", None),
}

MOVE_NONE = set()   # records whose 'mobility' modification says that nothing moves (v2: 15, 43; relabelled in v3)


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
    prev = {json.loads(l)["n"]: json.loads(l) for l in open(JSONL_PREV, encoding="utf-8") if l.strip()}
    text_changed = [n for n in sorted(recs) if recs[n]["text"] != prev[n]["text"]]
    rec_changed = [n for n in sorted(recs) if n not in text_changed and any(
        recs[n].get(k) != prev[n].get(k) for k in ("sources", "modifications", "coinages", "notes", "gloss", "facts"))]
    CL = {(c["n"], c["label"]): c for c in extra["claims"]}

    def cl(n, label):
        return CL[(n, label)]

    def pos(c, k=4):
        return ", ".join(f"{p} {v}x" for p, v in list(c["positions"].items())[:k]) or "-"

    def cited_ok(c):
        return all(v != "NOT A HIT" for v in c["cited"].values())

    A("# Provenance review: composition/drafts/v3 (provenance-verifier)")
    A("")
    A("Generated by `review/provenance_report_v3.py` from `review/provenance_v3_evidence.json` (`review/provenance_check.py`), "
      "`review/provenance_v3_extra.json` (`review/provenance_v3_extra.py`) and `review/poem_density_v3.json` "
      "(`review/poem_density.py`); rerun:")
    A("")
    A("```")
    A("source .venv/bin/activate")
    A("python -I review/provenance_check.py composition/drafts/v3.jsonl review/provenance_v3_evidence.json")
    A("python -I review/poem_density.py composition/drafts/v3.jsonl review/poem_density_v3.json")
    A("python -I review/provenance_v3_extra.py composition/drafts/v3.jsonl review/provenance_v3_evidence.json review/provenance_v3_extra.json")
    A("python -I review/provenance_report_v3.py")
    A("```")
    A("")
    A("## 1. Method")
    A("")
    A(f"* As for v1 and v2 (review/provenance_v1.md section 1, review/provenance_v2.md section 1): every `sources` entry of the {len(recs)} "
      "records was rerun with its recorded query through the `Concordance` methods behind `homer/concordance.py`'s CLI, and every distinct "
      "query once more through the CLI itself (`--count`); the Homeric string of the entry was run with `ngram`, each cited line checked "
      "for it, and its position in the verse (`homer/scan.py --json`) compared with its Homeric positions. Every 2-word and longer window "
      "of every verse was run through `ngram` for unclaimed attested phrases. The Greek-plus-citation pairs quoted in the records' "
      "`modifications` were checked the same way. All 60 records were rerun, not only the changed ones.")
    A(f"* Changed since v2: verse text in {', '.join(map(str, text_changed))}; record fields only in {', '.join(map(str, rec_changed))} "
      "(computed from the two jsonl files).")
    A("* `review/provenance_v3_extra.py` (adapted from the v2 script): forms with 0 Homeric hits and where they are marked; the coined "
      "stems as loose substrings; the -είδης models by NFC regex; every coined name's slot against the position of the Homeric model word "
      "in the cited model line; the records' `position` fields; and, new in v3, every count, position and cited line asserted in the "
      f"changed records and in the round-2 corrections ({len(extra['claims'])} claims, section 5), the accent of Νοβῆκος (Homeric words "
      "in -η + one consonant + -ος) and αὖθʼ / αὖτʼ before a rough breathing (NFC text).")
    A("* Classes and verdicts: as v1 and v2. **ATTESTED-EXACT** = in the verse word for word (accent-insensitive; movable ν ignored and "
      "noted), in the cited lines, at a position Homer gives it; **ATTESTED-MODIFIED** = in the cited lines, changed in the verse "
      "(kind stated, with a Homeric parallel for that kind where one is offered or found); **NOT-ATTESTED** = not in the cited "
      "lines, or the configuration asserted does not occur. COINAGE entries are classified by their model: a substitution "
      "(ATTESTED-MODIFIED) when the model word stands in the cited line at the position the coined name takes in the verse. "
      "**FAIL** / **QUERY** / **PASS** criteria are those of v1 (header of `review/provenance_report_v2.py`); bookkeeping errors "
      "that change no class are listed in section 8 as jsonl corrections and do not affect the verdict.")
    A("")
    A("## 2. Summary")
    A("")
    m2 = re.search(r"PASS (\d+), QUERY (\d+), FAIL (\d+)\*\* \(of (\d+)\)", (ROOT / "review/provenance_v2.md").read_text(encoding="utf-8"))
    A(f"* Lines: **PASS {verdicts['PASS']}, QUERY {verdicts['QUERY']}, FAIL {verdicts['FAIL']}** (of {len(recs)}). "
      + (f"v2 (review/provenance_v2.md): PASS {m2.group(1)}, QUERY {m2.group(2)}, FAIL {m2.group(3)} (of {m2.group(4)})." if m2 else ""))
    A(f"* Source entries: {sum(tallies.values())}; reviewer's classes: ATTESTED-EXACT {tallies['ATTESTED-EXACT']}, "
      f"ATTESTED-MODIFIED {tallies['ATTESTED-MODIFIED']}, NOT-ATTESTED {tallies['NOT-ATTESTED']}.")
    n_cnt_bad = sum(1 for r in ev for k, x in enumerate(r['sources'])
                    if x['claimed_count'] != x['query_total'] or recs[r['n']]['sources'][k].get('query_hits') != x['query_total'])
    A(f"* Recorded queries: {cc.get('distinct_queries')} distinct, each rerun with `python homer/concordance.py … --count`; mismatches "
      f"with the in-process rerun: {len(cc.get('mismatches', {}))}. Entries whose `count` or `query_hits` differ from the rerun "
      f"total: {n_cnt_bad}.")
    no_cit = [f"{r['n']}/{k}" for r in ev for k, x in enumerate(r["sources"]) if not x["cited_lines"]]
    A(f"* Cited lines checked: {n_cited}; lines that neither contain the claimed string nor are hits of the recorded query: "
      + ("; ".join(cit_notes) if cit_notes else "none") + ". Entries that cite no line: " + (", ".join(no_cit) or "none")
      + " (v2: 44/6, 'Il. 1.?-…', now gone).")
    A(f"* Homeric parallels quoted in the records' `modifications`: {n_par}; found in the cited line by the concordance: {n_par_ok}.")
    ncl_ok = sum(1 for c in extra["claims"] if cited_ok(c))
    A(f"* v3 claims recomputed (section 5): {len(extra['claims'])}; with every cited line a hit of the query: {ncl_ok}; counts or "
      "positions asserted in the records that the concordance does not reproduce: listed in section 8 (no class changes).")
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
    lab_bad = [(n, k) for (n, k), c in cls_of.items()
               if recs[n]["sources"][k]["status"] == "ATTESTED-EXACT" and c != "E"]
    lab_bad2 = [(n, k) for (n, k), c in cls_of.items()
                if recs[n]["sources"][k]["status"] == "ATTESTED-MODIFIED" and c == "E"]
    A("Every ATTESTED-EXACT label is exact (word for word, in the cited lines, at an attested position)"
      + (": exceptions " + ", ".join(f"{n}/{k}" for n, k in lab_bad) if lab_bad else "") + "; every ATTESTED-MODIFIED label is a "
      "modification" + (": exceptions " + ", ".join(f"{n}/{k}" for n, k in lab_bad2) if lab_bad2 else "") + ". Every COINAGE "
      "entry's model shows the slot (section 6). Two composer-MODIFIED entries contain a string that also stands in the verse at an "
      "attested position (33/3 and 55/3, καὶ βάλεν): the entry is for the second καὶ βάλεν at 9-10, a position Homer never gives it "
      "(11x, all 1-2); the first, at 1-2, is entry 0. They are classed as modified (mobility), as labelled.")
    A("")
    A("## 4. Round-2 rulings (review/round_2.md) and the provenance_v2 record corrections")
    A("")
    A("| ruling / item | lines | check (v3) | result |")
    A("|---|---|---|---|")

    def lab(n, k):
        s = recs[n]["sources"][k]
        return f"{n}/{k} {s['status']} → reviewer {R.CLASSNAME[cls_of[(n, k)]]}"
    acc = extra["accent_eta_C_os"]
    asp = extra["aspiration"]
    zero_l = extra["forms_with_0_homeric_hits"]
    in_coin = {(z["n"], z["loose"]): z["in_coinages"] for z in zero_l}
    pf = extra["position_field_mismatches"]
    pf_keys = {(p["n"], p["k"]) for p in pf}
    srcs = lambda n: recs[n]["sources"]  # noqa: E731

    def mods(n):
        return " ".join(m["homeric_parallel"] for m in recs[n]["modifications"])

    def coin(n):
        return " ".join(c["analogical_model"] for c in recs[n].get("coinages") or [])
    rows4 = [
        ("R9 Νοβῆκος (circumflex)", "44, 55",
         f"Νοβήκ- (acute) in v3: {sum(1 for n in recs for t in toks(recs[n]['text']) if t.startswith('Νοβήκ'))}; Νοβῆκ-: "
         f"{', '.join(str(n) for n in sorted(recs) if 'Νοβῆκ' in recs[n]['text'])}. Homeric words in η + one consonant + -ος: "
         f"{acc['circumflex_types']} types / {acc['circumflex_tokens']} tokens with the circumflex, {acc['acute_types']} with the acute "
         f"(e.g. {', '.join(w for w, _ in acc['circumflex_examples'][:5])})", "applied"),
        ("R10 Ζοκοβεύς / Ζοκοβῆος for Novak", "23, 44, 51",
         f"Ζοκοβεύ- / Ζοκοβῆ- in v3: {cnt('ζοκοβευ') + cnt('ζοκοβη')}; Djokovic is now κρατερὸς Ζοκοβείδης (23, 7.5-12), Νοβῆκος (44, "
         "4-5.5), Σέρβου κρατεροῖο (51, 8-12); slots in section 6; the decision is in FOR_HUMAN.md ('Ζοκοβεύς vs Ζοκοβείδης'). "
         f"Rejected genitives: Ζοκοβείδαο / -είδεω (not in v3); their Homeric models Πηλεΐδαο {cl(51, 'Πηλεΐδαο')['total']}x "
         f"({pos(cl(51, 'Πηλεΐδαο'))}), Πηληϊάδεω {cl(51, 'Πηληϊάδεω')['total']}x, Πηληϊάδεω Ἀχιλῆος "
         f"{cl(51, 'Πηληϊάδεω Ἀχιλῆος')['total']}x, as the record of 51 states", "applied"),
        ("R11 two aces / two winners", "33, 55",
         f"δεύτερον αὖτις in 33, 55: none (left only in 24, which R11 does not touch); each stroke has its own clause καὶ βάλεν … καὶ "
         f"βάλεν αὖτις; points recorded in `facts` (33: 357, 358; 55: 420, 421): "
         f"{'357' in recs[33]['facts'] and '358' in recs[33]['facts'] and '420' in recs[55]['facts'] and '421' in recs[55]['facts']}; "
         f"δίς in v3: {L_.count('δισ')}; καὶ βάλεν αὖτις {cl(33, 'καὶ βάλεν αὖτις')['total']}x in Homer (not claimed as attested)",
         "applied"),
        ("R12 attacker of 'the fourth time'", "36-37",
         "36 is the τρὶς μέν count naming Federer (τρὶς μὲν ἔπειτʼ ἐπόρουσε + βοὴν ἀγαθὸς Φεδερῆρος); the Homeric sequence τρὶς μὲν "
         "ἔπειτʼ ἐπόρουσε … ἀλλʼ ὅτε δὴ τὸ τέταρτον ἐπέσσυτο δαίμονι ἶσος is verified in Il. 5.436/438, 16.784/786, 20.445/447 "
         "(in all three a τρὶς δέ line intervenes: 5.437, 16.785, 20.446; the poem goes from 36 to 37 directly: section 8)", "applied"),
        ("24 δάμασεν in `coinages`", "24",
         f"listed: {in_coin.get((24, 'δαμασεν'))}; parallel περὶ στήθεσσιν ἔδυνεν {cl(24, 'περὶ στήθεσσιν ἔδυνεν')['total']}x "
         f"(Il. 3.332, 19.371) / ἔδυνε {cl(24, 'περὶ στήθεσσιν ἔδυνε')['total']}x (Il. 11.19, 16.133) verified; "
         + lab(24, 4), "applied"),
        ("positions 12/2, 22/1, 22/5, 31/2", "12, 22, 31",
         "; ".join(f"{n}/{k} `position` {srcs(n)[k]['position']}" + (" (still differs)" if (n, k) in pf_keys else " = verse")
                   for n, k in [(12, 2), (22, 1), (22, 5), (31, 2)]), "applied"),
        ("'mobility' where nothing moves", "15, 43",
         f"15: {[m['kind'] for m in recs[15]['modifications']]}; 43: {[m['kind'] for m in recs[43]['modifications']]}", "applied"),
        ("model of Σέρβος δʼ αὖτʼ", "29, 58",
         f"cited: {srcs(29)[1]['citation']} / {srcs(58)[1]['citation']}; Ἕκτωρ δʼ αὖτʼ {cl(29, 'Ἕκτωρ δʼ αὖτʼ')['total']}x "
         f"({cl(29, 'Ἕκτωρ δʼ αὖτʼ')['cited']}); " + lab(29, 1) + "; " + lab(58, 1), "applied"),
        ("Ἀχαιῶν at 6-8", "27, 33",
         f"records say 96x: {'96x' in srcs(27)[3]['citation'] and '96x' in srcs(33)[1]['citation']}; concordance "
         f"{cl(33, 'Ἀχαιῶν')['positions'].get('6-8')}x", "applied"),
        ("αὐτὰρ ὅ γʼ ἥρως verse-final", "30, 54",
         f"stated in 30: {'verse-final' in mods(30)}, in 54: {'verse-final' in mods(54)}; concordance {cl(30, 'αὐτὰρ ὅ γʼ ἥρως')['total']}x, "
         f"{pos(cl(30, 'αὐτὰρ ὅ γʼ ἥρως'))}; new model αὐτὰρ ὃ … ἄναξ ἀνδρῶν Ἀγαμέμνων (Il. 2.402, 3.81, 19.51): "
         f"{cited_ok(cl(30, 'ἄναξ ἀνδρῶν Ἀγαμέμνων')) and cited_ok(cl(30, 'αὐτὰρ ὃ (line-initial)'))}", "applied"),
        ("Πηλεΐδης counts", "4, 23, 53, 56",
         f"'24x nominative, Πηλεΐδ- 51x' in all four records: {all('24x nominative' in coin(n) and '51x' in coin(n) for n in (4, 23, 53, 56))}; "
         f"concordance Πηλεΐδης {cl(4, 'Πηλεΐδης (nom.)')['total']}x, Πηλεΐδ- {cl(4, 'Πηλεΐδ- (all)')['total']}x; '38x' left: "
         f"{any('38x' in coin(n) for n in recs)}", "applied"),
        ("-είδης models Il. 4.517 / Od. 15.52", "4, 23, 53, 56",
         f"cited in all four: {all('4.517' in coin(n) and '15.52' in coin(n) for n in (4, 23, 53, 56))}; verified: "
         + "; ".join(f"{c['label']} {list(c['cited'].items())[0][0]}@{list(c['cited'].items())[0][1]}"
                     for c in extra["claims"] if c["n"] == 4 and c["cited"]), "applied"),
        ("44 citation δʼ αὖ (Il. 3.200)", "44",
         f"placeholder 'Il. 1.?' in v3: {any('1.?' in (s.get('citation') or '') for n in recs for s in srcs(n))}; δʼ αὖ replaced by δʼ αὖτε "
         f"(entry 3, {pos(cl(44, 'δʼ αὖτε'))}); Il. 3.200 cited in the modifications for the v2 particle: {'3.200' in mods(44)} "
         f"(οὗτος δʼ αὖ Λαερτιάδης verified: {cited_ok(cl(44, 'οὗτος δʼ αὖ Λαερτιάδης'))})", "applied"),
        ("56 αὖθʼ before Ἑλβέτιος", "56",
         f"ἔνθʼ αὖθʼ in the verse; αὖθʼ + rough breathing {asp['αὖθʼ + rough (count)']}x, αὖτʼ + rough breathing "
         f"{asp['αὖτʼ + rough (count)']}x (NFC text), as the record states; ἔνθʼ αὖτʼ {asp['ἔνθʼ αὖτʼ']}x, ἔνθʼ αὖθʼ {asp['ἔνθʼ αὖθʼ']}x", "applied"),
    ]
    for a, b, c, d in rows4:
        A(f"| {R.esc(a)} | {b} | {R.esc(c)} | {d} |")
    A("")
    A("## 5. The rebuilt verses: claims recomputed (review/provenance_v3_extra.json, `claims`)")
    A("")
    A("Every count, position and parallel the changed records assert, and the round-2 corrections, rerun with the concordance. "
      "'cited' = the cited line is a hit of the query (its position there).")
    A("")
    A("| line | string | query | Homer: total, positions | record asserts | cited lines (position) | ok |")
    A("|---|---|---|---|---|---|---|")
    for c in extra["claims"]:
        cit = "; ".join(f"{k}@{v}" for k, v in c["cited"].items()) or "-"
        A(f"| {c['n']} | {R.esc(c['label'])} | `{R.esc(c['query'])}` | {c['total']}: {R.esc(pos(c, 5))} | {R.esc(c['asserted'])} | "
          f"{R.esc(cit)} | {'yes' if cited_ok(c) else '**no**'} |")
    A("")
    A("## 6. Name slots: coined name v. Homeric model word (review/provenance_v3_extra.json)")
    A("")
    A("| verse | coined | position in the verse | word before / after | model | model line | model's position | before / after in the model | same | model word's positions in Homer |")
    A("|---|---|---|---|---|---|---|---|---|---|")
    for x in extra["name_slots"]:
        A(f"| {x['verse']} | {x['coined']} | {x['verse_position']} | {x['verse_prev'] or '^'} / {x['verse_next'] or '$'} | {x['model']} | "
          f"{x['model_citation']} | {x['model_position']} | {x['model_prev'] or '^'} / {x['model_next'] or '$'} | "
          f"{'yes' if x['same_position'] else '**no**'} | {R.esc(', '.join(f'{p} ({c})' for p, c in list(x['model_form_positions_in_homer'].items())[:4]))} |")
    A("")
    allsame = all(x["same_position"] and x["model_in_line"] for x in extra["name_slots"])
    A(("Every coined name stands where its model word stands in the cited line." if allsame else
       "**Some coined names do not stand where their model word stands (see 'same').**")
      + " The new slots: **Ζοκοβείδης** in 23 at 9.5-12 after κρατερός (7.5-9) and a word ending at 7 (ἄφαρ, 6-7), exactly the "
      "configuration of μίγη κρατερὸς Διομήδης (Il. 5.143, 6-12); **Νοβῆκος** in 44 at 4-5.5 (S L S, the final -ος short before ὃ) "
      "after δʼ αὖτε, as γυναῖκας in Od. 24.278 (before ἀμύμονα) and ἄριστος in Il. 1.91 (before Ἀχαιῶν), both before a vowel; "
      "**Νοβῆκος** in 55 at 6-8 between a vowel-final ἀφάμαρτε and καί, the Ῥογῆρος slot of 27 and 33 (Μελανθώ, Od. 19.65; "
      "Ὀδυσσεύς, Il. 2.272), its final syllable long by position before καί; **Σέρβου** in 51 at 8-9 (LL) before the SSLX "
      f"κρατεροῖο, as κνίσῃ before ἐκάλυψαν ({cl(51, 'κνίσῃ ἐκάλυψαν')['total']}x at 8-12) and ἀνδρῶν before Ἀγαμέμνων "
      f"({cl(51, 'ἀνδρῶν Ἀγαμέμνων')['total']}x at 8-12); the function model τὴν δʼ Ἕκτορος ἱπποδάμοιο (Il. 22.211) is a frame, not a "
      "slot model (Ἕκτορος stands at "
      f"{cl(51, 'Ἕκτορος (in the frame model)')['cited']['Il. 22.211']} there, Σέρβου at 8-9), and is classed as such (51/0). **Ἑλβετίου** (51, 3-5) keeps its v2 slot.")
    A("")
    A("## 7. Per-line table")
    A("")
    A("Entries: `k:E/M/N` = entry k, reviewer's class (details in section 10). Parallels = the record's quoted Homeric parallels found "
      "in the cited line / quoted. Unclaimed = maximal attested windows not contained in any entry. Δ = changed since v2 (T = verse text, "
      "r = record only).")
    A("")
    A("| n | Δ | verse | verdict | entries | parallels | unclaimed attested windows | reasons |")
    A("|---|---|---|---|---|---|---|---|")
    for row in rows:
        n = int(row.split("|")[1])
        d = "T" if n in text_changed else ("r" if n in rec_changed else "")
        A(row.replace(f"| {n} | ", f"| {n} | {d} | ", 1))
    A("")
    A("## 8. Unclaimed phrases, coinages, jsonl corrections")
    A("")
    A("* Unclaimed attested windows (all listed in the table): " + "; ".join(
        f"{n}: {w['ngram']} ({w['count']}x, {w['poem_position']}{'' if w['position_attested'] else ', not a Homeric position'})"
        for n, w in unclaimed_all) + ".")
    A("  * New in v3 and worth claiming: **36 ἐπόρουσε βοὴν ἀγαθὸς** (3.5-9, the position of Il. 5.432 `Αἰνείᾳ δʼ ἐπόρουσε βοὴν "
      "ἀγαθὸς Διομήδης`): the verse is the first half of the count line Il. 5.436 joined to the second half of Il. 5.432 on the shared "
      "ἐπόρουσε (3.5-5.5 in both), with Φεδερῆρος for Διομήδης. ἐπόρουσε βοὴν ἀγαθὸς Διομήδης (3.5-12) is the closer model for 6-12 "
      "than the Il. 20.445 substitution the record cites; it strengthens the line and changes no verdict.")
    A("  * **44 ὃ δʼ** (6-7, function words only): the pronoun-plus-particle the record cites only through its parallels "
      f"(ὃ δʼ ἅμʼ ἕσπετο, ὃ δʼ ἐπέσσυτο); ὃ δʼ ἕσπετο itself is {cl(44, 'ὃ δʼ ἕσπετο')['total']}x in Homer and is not claimed as "
      "attested (entry 7 is a modification of ἡ δʼ ἕσπετο, Od. 1.125), correctly.")
    rest = sorted({n for n, w in unclaimed_all if n not in (36, 44)})
    A(f"  * The rest ({', '.join(map(str, rest))}) are as in v2: a particle extending a claimed formula, or a fragment of a disclosed "
      "mobility where the position is not Homeric (48 δὴ περί, 56 δʼ ἄψ). 29 and 58 no longer show δʼ αὖτʼ as unclaimed: the "
      "string is now inside the claimed Σέρβος δʼ αὖτʼ.")
    zl = extra["forms_with_0_homeric_hits"]
    notlisted = sorted({(z["n"], z["form"]) for z in zl if not z["in_coinages"]})
    undisclosed = sorted({(z["n"], z["form"]) for z in zl if not (z["in_coinages"] or z["in_coinage_entry"] or z["named_in_modified_entry"])})
    st = extra["coined_stems_substring_hits"]
    A("* Forms with 0 Homeric hits (`--loose … --word`): " + ", ".join(dens["unattested_forms"]) + ". Undisclosed: "
      + (", ".join(f"{f} ({n})" for n, f in undisclosed) or "none") + ". Disclosed but not listed in `coinages`: "
      + (", ".join(f"{f} ({n})" for n, f in notlisted) or "none") + ".")
    A("* Claimed coinages that exist in Homer: none. `--loose` substrings: " + ", ".join(f"{k} {v}" for k, v in st.items())
      + f". Strings of the rebuilt verses that are 0x in Homer and not claimed as attested: καὶ βάλεν αὖτις "
      f"({cl(33, 'καὶ βάλεν αὖτις')['total']}x; 33, 55), ὃ δʼ ἕσπετο ({cl(44, 'ὃ δʼ ἕσπετο')['total']}x; 44), ἔνθʼ αὖθʼ "
      f"({asp['ἔνθʼ αὖθʼ']}x; 56), Σέρβος δʼ αὖτʼ (0x; 29, 58): each is disclosed as a modification of an attested string.")
    exact_pf = [p for p in pf if cls_of[(p["n"], p["k"])] == "E"]
    A("* jsonl corrections (no verdict effect):")
    for p in exact_pf:
        A(f"  * {p['n']}/{p['k']} '{p['text']}': `position` {p['position_field']}, but the string stands at {', '.join(p['verse_position'])} "
          f"in the verse (attested there: {p['homer_positions'].get(p['verse_position'][0], 0)}x)")
    td, td2 = cl(20, "τρὶς δέ"), cl(20, "τρὶς δʼ")
    A(f"  * 20 (`notes`): '--ngram \"τρὶς δέ\" 7x, --ngram \"τρὶς δ᾽\" 7x' → τρὶς δέ {td['total']}x ({pos(td)}; entry 0 of the same "
      f"record already says 8x), τρὶς δʼ {td2['total']}x ({pos(td2)}); the cited Od. 4.277, Il. 24.16, 24.273 are hits")
    kr = cl(51, "κρατεροῖο")
    A(f"  * 51/5 κρατεροῖο: '7x: 5 at 9.5-12' → {kr['total']}x: {pos(kr)} (the class is unaffected: 9.5-12 is attested)")
    pd = cl(51, "* δʼ αὖ (pronoun at 6)")["positions"]
    da7 = cl(51, "δʼ αὖ")["positions"].get("7-7")
    A(f"  * 51 (`modifications`, mobility): 'pronoun + δʼ αὖ 6x' → δʼ αὖ at 7 is {da7}x, but a one-syllable word (pronoun) at 6 "
      f"precedes it only {pd.get('6-7')}x (Il. 6.462 σοί, 8.324 τόν, 23.724 τά, 24.732 σύ); in {pd.get('5.5-7')} (Il. 10.108, 21.105) "
      "a preposition (ποτί, περί) stands at 5.5-6")
    pk = cl(51, "Πολυποίταο κρατεροῖο")
    A(f"  * 51/6 Πολυποίταο κρατεροῖο: `position` 8-12 is the span of the analogue in the verse; in Homer the phrase stands at "
      f"{list(pk['positions'])[0]} (Il. 23.848), so only κρατεροῖο (9.5-12) shares the slot")
    A("  * 56/1 αὖθʼ ἱερεύς: `position` 2-3 matches neither the verse (αὖθʼ at 2) nor Homer (Il. 1.370, 3-5); harmless in a "
      "parallel-only entry")
    A("  * 36 / 37 (`notes`): 'exactly as Diomedes is the subject of Il. 5.438 after 5.436' – in Homer the τρὶς μέν line and ἀλλʼ ὅτε "
      "δὴ τὸ τέταρτον are always separated by a τρὶς δέ line (Il. 5.437, 16.785, 20.446); the poem's two-line sequence is a "
      "contraction (the subject is still fixed); also add Il. 5.432 to 36 (above)")
    A("")
    A("## 9. Formulaic density (review/poem_density.py)")
    A("")
    A(f"Method as v1 and v2 (review/provenance_v1.md section 6): I = Homer, M = the poem ({dens['verses']} verses, {dens['tokens']} tokens); "
      "n-grams within one verse, compared as `concordance.py --ngram`; coverage = share of tokens inside at least one attested word "
      f"n-gram; `base` drops n-grams made only of function words ({dens['func_words']} frozen loose forms); `min2` = at least 2 Homeric "
      f"occurrences; 95% CI bootstrap over verses, B = {dens['B']}; shuffled = poem tokens permuted over positions, R = {dens['R']}; "
      "Homeric reference = each Homeric verse against the rest of Homer, token-weighted. This is the n-gram coverage method of "
      "analysis/formulas (report.md section 1: common.cover_a / boot_ratio / shuffle_tokens) applied to Greek.")
    A("")
    A("| definition | coverage % [95% CI] | without the verbatim Homeric verses | without tokens unattested in Homer | shuffled % | excess (pp) | Homeric verse v. rest of Homer % | reference v. the 'without verbatim' interval | v2 coverage % |")
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
      f"({', '.join(map(str, dens['verbatim_verse_numbers']))}); v2: {dens1['verses_identical_to_a_homeric_verse']} of {dens1['verses']}. "
      f"The 'without' column drops them ({x0['verses']} verses, {x0['tokens']} tokens). {dens['tokens_unattested_in_homer']} tokens "
      "are forms unattested in Homer (section 8) and can never be covered.")
    A(f"* **Lines with at least one ATTESTED-EXACT formula of 2 or more words**: {dens['lines_with_claimed_exact_formula_ge2_words']} of "
      f"{dens['verses']} = **{dens['lines_with_claimed_exact_formula_ge2_words_pct']}%** (claimed strings found verbatim at a Homeric "
      f"position, poem_density.py; v2 {dens1['lines_with_claimed_exact_formula_ge2_words_pct']}%); by the reviewer's classes (entries "
      f"classed E with 2 or more words): {len(exact2_lines)} of {len(recs)}. Counting only formulas not made of function words alone: "
      f"**{dens['lines_with_claimed_exact_formula_ge2_words_not_function_only_pct']}%** (none in "
      f"{', '.join(map(str, dens['lines_without_claimed_exact_formula_ge2_words_not_function_only'])) or '-'}; v2 "
      f"{dens1['lines_with_claimed_exact_formula_ge2_words_not_function_only_pct']}%). Unclaimed included, any "
      f"attested non-function-word n-gram at a Homeric position: {dens['lines_with_any_attested_ngram_at_homeric_position_pct']}% (none "
      f"in {', '.join(map(str, dens['lines_without_any_attested_ngram_at_homeric_position'])) or '-'}).")
    below = [k for k in D if ref[k] < D[k]["excluding_verbatim_verses"]["ci95"][0]]
    inside = [k for k in D if D[k]["excluding_verbatim_verses"]["ci95"][0] <= ref[k] <= D[k]["excluding_verbatim_verses"]["ci95"][1]]
    A(f"* Reading (exploratory; {dens['verses']} verses): with every verse counted the poem's coverage is above the Homeric reference on "
      f"every definition. Without the copied verses the reference lies inside the poem's 95% interval for {', '.join(inside) or 'none'} and "
      f"below it for {', '.join(below) or 'none'}. As in v1 and v2, this measures reuse of attested wording by a composer working from the "
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
    print("lab_bad:", lab_bad, lab_bad2)


if __name__ == "__main__":
    main()
