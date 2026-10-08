#!/usr/bin/env python3
"""Write review/provenance_v4.md from the machine evidence and the reviewer's recorded judgments (draft v4).

    source .venv/bin/activate
    python -I review/provenance_check.py composition/drafts/v4.jsonl review/provenance_v4_evidence.json
    python -I review/poem_density.py composition/drafts/v4.jsonl review/poem_density_v4.json
    python -I review/provenance_v4_extra.py composition/drafts/v4.jsonl review/provenance_v4_evidence.json \
        review/provenance_v4_extra.json
    python -I review/provenance_report_v4.py

Adapted from review/provenance_report_v3.py: same classes, same verdict criteria, same classification order. The
judgments J are re-keyed to the v4 numbering (records' `v3_line`; an old judgment is carried over only where the v4
entry text is the v3 entry text) and extended to the verses changed or added in v4.
Classification order for every `sources` entry:
  1. J below (reviewer's decision with reason and Homeric parallel; an optional QUERY reason);
  2. provenance_report.auto_class (exact / mobility / movable nu, from the evidence);
  3. COINAGE entries: ATTESTED-MODIFIED if every Homeric model word named in the entry stands in the cited model line
     at the position the coined name has in the verse (review/provenance_v4_extra.json, name_slots); otherwise
     NOT-ATTESTED with a QUERY (unless J decides);
  4. other entries whose cited lines contain the string but whose string is not in the verse word for word:
     ATTESTED-MODIFIED, the kind stated from the words kept and changed; 'structural model' when no content word is
     shared.
Verdicts (as v1-v3): FAIL if a cited line lacks the claimed string (and the miss is not a movable nu, a line range,
or one of the CIT_EXPLAINED cases below), or an entry labelled ATTESTED-EXACT (string of >= 2 words) is not exact,
or a form unattested in Homer is not disclosed at all; QUERY if the classification is debatable (single words
labelled exact that are not exact; counts in `count` fields that the recorded query does not reproduce; name slots
that the cited model line does not show; a citation field that, read by the Il./Od. convention, cites the wrong
lines; a form unattested in Homer disclosed but not listed in `coinages`); PASS otherwise. Bookkeeping errors in
free text (counts and examples inside `text`, `modifications`, `notes`, `coinages`) are listed in section 9 as
jsonl corrections and do not affect the verdict.
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

EV = ROOT / "review/provenance_v4_evidence.json"
DENS = ROOT / "review/poem_density_v4.json"
DENS1 = ROOT / "review/poem_density_v3.json"   # previous round, for comparison
EXTRA = ROOT / "review/provenance_v4_extra.json"
JSONL = ROOT / "composition/drafts/v4.jsonl"
JSONL_PREV = ROOT / "composition/drafts/v3.jsonl"
OUT = ROOT / "review/provenance_v4.md"
PREV_MD = ROOT / "review/provenance_v3.md"

ATR = ("M", "shape model for the LSSL name slot: Ἀτρεΐδ- (the records' query `--loose ατρειδ`, a substring) 210x, 64 at "
       "3-5; cited Il. 1.102 ἥρως Ἀτρεΐδης has it at 3-5", "Ἀτρεΐδης (nom.) 34x at 3-5 (`--ngram`)", None)
KB = ("M", "mobility: the second καὶ βάλεν stands at 9-10 (Homer 1-2 only, 11x; the first καὶ βάλεν of the verse, at 1-2, "
      "is entry 0); recorded in the record as a departure from Homer's localisation (critic M8)",
      "the same kind of shift for other line-initial pairs: καὶ σάκος 1-2 (Il. 10.257, Od. 14.277) and 9-10 (Il. 15.125, "
      "15.474); ἔνθα δέ 1-2 and 9-10 (Il. 6.245, 6.249, 18.497); αἶψα δʼ 1-2 and 9-10 (Il. 1.387, 6.514, 18.532): verified, "
      "section 5", None)
KB5 = ("M", "structural parallel: a repeated action given its own verb + verse-final αὖτις (no content word of the verse)",
       "καί + verb + αὖτις verse-final: καὶ ἀνήγαγον αὖτις (Il. 15.29); αὖτις of a second cast: Od. 22.272", None)
J = {
 # carried over from v3 (entry text unchanged)
 (1, 0): ("M", "inflection ἄνδρα → dual ἄνδρε; 1-5.5 kept", "ἄνδρε line-initial in ἄνδρε δύω (Il. 23.659 = 23.802)", None),
 (1, 3): ("M", "truncation: ἄνδρε δύω → ἄνδρε (δύω dropped); ἄνδρε keeps 1-1.5 (6 of 9)", "-", None),
 (1, 4): ("M", "inflection δαΐφρονα → dual δαΐφρονε (0x in Homer; listed in `coinages`); slot 6-8 kept",
          "-ονε duals of the same declension: κρατερόφρονε (Od. 11.299), δαήμονε (Od. 16.253)", None),
 (4, 0): ("M", "structural model: two subjects of διαστήτην joined by τε … καί (only τε, καί shared)", "-", None),
 (4, 1): ("M", "substitution of both names in the frame name τε καί epithet + name; τε (5.5) and καί (6) at the same positions as in Il. 14.29",
          "Il. 14.29 = 14.380 Τυδεΐδης Ὀδυσεύς τε καὶ Ἀτρεΐδης Ἀγαμέμνων", None),
 (4, 3): ("M", "substitution of 1-5.5 and of the name at 9.5-12; τε καὶ ἀντίθεος kept at 5.5-9", "τε καὶ ἀντίθεος + SSLX name 3x (Il. 20.232, Od. 3.414, 8.119)", None),
 (7, 3): ("M", "inflection δεύτερος → δεύτερον and mobility (Homer 9-12, verse 1-3.5)", "adverbial δεύτερον αὖ at 1-3 5x (Il. 3.332)", None),
 (25, 3): ATR, (60, 5): ATR, (19, 5): ATR,
 (20, 1): ("M", "substitution μέν → δέ (τρὶς δέ μιν 0x); the δέ-limb of the counting pair", "τρὶς μέν … τρὶς δέ: Il. 18.155 / 18.157, 21.176 / 21.177", None),
 (20, 2): ("M", "structural: only αὖτʼ shared (at 3 in both)", "-", None),
 (22, 6): ("M", "syntactic parallel only (dual subject τώ with a plural verb); no word of the verse", "-", None),
 (22, 7): ("M", "syntactic parallel only (as entry 6)", "-", None),
 (25, 1): ("M", "the same formula with αὖτʼ for αὖθʼ (aspiration before the rough breathing of Ἑλβέτιος)",
           "τὸν δʼ αὖθʼ Ἱππολόχοιο (Il. 6.144) beside τὸν δʼ αὖτʼ 28x", None),
 (25, 4): ("M", "inflection: movable ν added, δάμασε → δάμασεν (the ν-form is 0x in Homer; listed in `coinages`), same slot 5.5-7",
           "the same formula with and without movable ν: περὶ στήθεσσιν ἔδυνε (Il. 11.19) / ἔδυνεν (Il. 3.332)", None),
 (25, 5): ("M", "parallel only (the σσ-variant δάμασσε, not in the verse)", "-", None),
 (31, 1): ("M", "substitution of the name in Ἕκτωρ δʼ αὖτʼ + verb (Il. 17.304, 1-3) → Σέρβος δʼ αὖτʼ + verb (Σέρβος δʼ αὖτʼ itself 0x)",
           "Αἴας δʼ αὖτʼ (Il. 14.469, 1-3); Ἕκτωρ δʼ αὖτʼ also Il. 3.76 (3-5)", None),
 (43, 4): ("M", "structural parallel: the relative clause that follows λέων ὣς in Il. 20.165 (the verse continues with the Il. 5.137 clause in 44)", "-", None),
 (44, 1): ("M", "structural: the opening (Il. 5.136) of the simile whose relative clause 44 keeps", "-", None),
 (48, 5): ("M", "separation: ἀνῆκε (4-5.5) … θυμός (9-10), verb before subject", "verb before θυμὸς ἀγήνωρ: πάλιν αὖτις ἀνήσει θυμὸς ἀγήνωρ (Il. 2.276)", None),
 (37, 3): KB, (59, 3): KB, (37, 5): KB5, (59, 5): KB5,
 (41, 1): ("M", "substitution of the name-epithet formula at 6-12: ποδάρκης δῖος Ἀχιλλεύς → βοὴν ἀγαθὸς Φεδερῆρος (τρὶς μὲν ἔπειτʼ ἐπόρουσε kept at 1-5.5)",
           "the count line takes three different 6-12 completions (Il. 5.436, 16.784, 20.445); ἐπόρουσε βοὴν ἀγαθὸς Διομήδης at 3.5-12 (Il. 5.432, now entry 4)", None),
 (55, 0): ("M", "structural model: τὴν μέν + genitive of the first owner, τὴν δʼ + genitive + epithet in -οιο of the second; both names replaced, ἄρʼ and αὖ added (shared: τὴν μέν, τὴν δʼ)", "-", None),
 (55, 4): ("M", "structural: pronoun + δʼ αὖ at 6-7 + the name phrase to the verse end; only δʼ αὖ shared", "-", None),
 (60, 0): ("M", "orthography of the elision: ἔνθʼ αὖτʼ (12x, 1-2) written ἔνθʼ αὖθʼ before the rough breathing of Ἑλβέτιος (ἔνθʼ αὖθʼ 0x)",
           "αὖθʼ before a rough breathing (NFC text, section 4): τὸν δʼ αὖθʼ Ἱππολόχοιο (Il. 6.144), Χρύσης δʼ αὖθʼ ἱερεύς (Il. 1.370)", None),
 (60, 1): ("M", "parallel only (αὖθʼ before a rough breathing; αὖθʼ itself is in the verse at 2)", "-", None),
 (60, 2): ("M", "parallel only (as entry 1)", "-", None),
 (60, 3): ("M", "structural: ἔνθʼ αὖτʼ + the subject name at 1-5 (Αἰνείας → Ἑλβέτιος at 3-5, αὖτʼ → αὖθʼ as entry 0)", "-", None),
 # v4: verses changed or added
 (19, 2): ("M", "substitution of 1-5.5 (ὣς εἰπὼν Τρώεσσιν → ὣς ἄρʼ ὅ γʼ Ἑλβέτιος τότʼ) before the unchanged 6-12 formula",
           "ἐπέσσυτο δαίμονι ἶσος after seven different first halves (Il. 5.438, 5.459, 5.884, 16.705, 16.786, 20.447, 21.227)", None),
 (20, 4): ("M", "slot parallel: ἐδάμασσε at 3.5-5.5 after a long monosyllable; only ἐδάμασσε shared", "κὴρ ἐδάμασσε (Od. 11.171 = 11.398), μοῖρʼ ἐδάμασσε (Od. 22.413)", None),
 (20, 8): ("M", "structural: καί at 6 joining a second verb formula at 7-12 (only καί shared)", "εἴρυσσέν τε καὶ ἄσπετον ἤρατο κῦδος (Il. 3.373 = 18.165)", None),
 (24, 1): ("M", "substitution of the ethnic into an A1 slot (3-3.5 before a vowel; check_line clean, section 7); the cited Il. 6.45 has the bare name before δʼ ἄρʼ ἔπειτα at 1-3, not at 3-3.5",
           "LS name at 3-3.5 before a vowel: Τεῦκρος (Il. 12.350 = 12.363), the model already used for Σέρβον in 48",
           "name slot not shown by the cited model line (Ἄδρηστος at 1-3 in Il. 6.45); cite Il. 12.350"),
 (24, 3): ("M", "semantic model re-inflected: πύματον … δρόμον (the last lap, 3.5-8) → μάχῃ πυμάτῃ (the last fight, 6-9); only the stem shared; πυματ- moved to 7.5-9 (πύματον 3.5-5 6x, 5.5-7 2x)",
           "the feminine πυμάτη at 3.5-5 (Il. 6.118, nom.) and πυμάτην (Il. 18.608)", None),
 (24, 4): ("M", "inflection πυμάτην → dative πυμάτῃ and mobility (3.5-5 → 7.5-9); the dative with iota subscript is 0x, but the nominative πυμάτη, identical in the loose form, is in Il. 6.118 (3.5-5)",
           "πυμάτῳ (Od. 7.138) for the dative", None),
 (24, 6): ("M", "frame: ἀλλʼ ὅ γʼ (1-2) … ἐνίκα (10-12) kept; the middle replaced by name + ἔπειτα + the contest in the dative + μιν",
           "ἐνίκα with the contest in the dative: πόδεσσι δὲ πάντας ἐνίκα (Il. 20.410), κάλλει ἐνίκα (Il. 23.742); the man beaten in the accusative: πάντας ἐνίκα (Il. 23.680)", None),
 (29, 1): ("M", "structural: ἀλλὰ καὶ ὧς (1-3) kept, the rest replaced (the chariot race of Il. 23.516)", "-", None),
 (29, 2): ("M", "substitution and mobility: ἐδάμη ὑπὸ χερσί (Il. 2.860, 1.5-5.5) moved to 3.5-9.5 with κρατεροῦ between; the agent genitive ποδώκεος Αἰακίδαο → κρατεροῦ … Νοβήκου, split around ὑπὸ χερσί",
           "agent genitive before ὑπὸ χερσί: Ἀτρεΐδεω ὑπὸ χερσί (Il. 11.180), Πατρόκλου ὑπὸ χερσί (Il. 16.699); ὑπὸ χερσί at 7.5-9.5 (Il. 3.352, 23.675); the split epithet … ὑπὸ χερσί … name is not among the 11 Homeric ὑπὸ χερσί lines (section 5)", None),
 (29, 6): ("M", "substitution of the coined genitive into an A1 slot (SLL at 10-12; check_line clean); the cited models do not show it (Ἀχιλῆος at 9.5-12 in Il. 21.553, Αἰακίδαο at 9-12 in Il. 2.860)",
           "SLL name genitive in -ου at 10-12: Λυκούργου in ὑπʼ ἀνδροφόνοιο Λυκούργου (Il. 6.134, ὑπό + epithet + name), Σκαμάνδρου (Il. 5.77)",
           "name slot not shown by the cited model lines (Il. 21.553: Ἀχιλῆος at 9.5-12; Il. 2.860: Αἰακίδαο at 9-12); cite Il. 6.134"),
 (33, 0): ("E", "", "-", None),
 (33, 1): ("E", "", "-", "citation field 'Il. 13.66, Od. 18.34 (line-initial), 11.110, 23.336' reads, by the Il./Od. convention, as Od. 11.110 and Od. 23.336, which lack τοῖιν; the lines are Il. 11.110 and Il. 23.336 (as the entry's own text says)"),
 (33, 3): ("M", "parallel only: the present λέλυνται (Od. 8.233, 18.242); the verse keeps the pluperfect λέλυντο of Il. 13.85", "-", None),
 (34, 1): ("M", "the verse has the unelided παρέλασσε (0x in Homer: written out before the consonant of βοήν); Homer has only the elided παρέλασσʼ (Il. 23.382, 23.527, 3.5-5), both in a κεν-clause (would have driven past)",
           "-", None),
 (40, 2): ("M", "structural: ὃ δέ μιν (5.5-7) kept, the hit verb follows (βάλεν at 7.5-8 for φθάμενος βάλε)", "-", None),
 (40, 3): ("E", "", "-", None),
 (49, 2): ("M", "parallel only: the elided ἔκφερʼ at 3-3.5 (Il. 23.259); the verse has the unelided ἔκφερεν at 3-4 (entry 1)", "-", None),
 (49, 3): ("M", "frame of the race-position line (Il. 23.759): the leader + ἔκφερ- in the first half, the follower's clause at 6-12 (ἐπὶ δʼ ὄρνυτο δῖος Ὀδυσσεύς → ὃ δʼ ἐπέσσυτο τυτθὸν ὀπίσσω); only δʼ shared",
           "the follower by pronoun: ὃ δʼ ἐπέσσυτο ποσσὶ διώκειν (Il. 21.601)", None),
 (55, 9): ("M", "the string τὴν δʼ Ἕκτορος ἱπποδάμοιο is not in the verse: only τὴν δʼ is (6-7, as in Il. 22.211); Ἕκτορος ἱπποδάμοιο → αὖ Σέρβου κρατεροῖο",
           "τὴν δʼ at 6-7: Il. 22.211, 14.168, Od. 3.11, 5.58, 16.357 (5x)", None),
 (56, 5): ("M", "parallel: a hero's ἐέλδωρ with his name in the genitive (Il. 15.74); only ἐέλδωρ shared", "-", None),
 (58, 1): ("M", "ἕτερος after the article at 1.5-3 (Od. 8.374 τὴν ἕτερος) kept; the rest replaced", "-", None),
 (61, 2): ("M", "slot model for the coined vocative Φεδερεῦ (SSL at 5.5-7, as Ἀχιλεῦ in the three cited lines: section 7); not in the verse", "-", None),
 (61, 3): ("M", "structural: the narrator's second-person apostrophe (Il. 16.787); no word shared", "-", None),
 (62, 0): ("M", "substitution of the ethnic in the dative into an A1 slot (LL at 1-2 before δʼ; check_line clean); the cited τῷ δʼ (Il. 1.250) has τῷ at 1 only",
           "LL dative name at 1-2 before δʼ: Γλαύκῳ δʼ (Il. 16.508); Σέρβος at 1-2 as Ἕκτωρ (Il. 8.216)",
           "name slot not shown by the cited model line (τῷ at 1-1 in Il. 1.250); cite Il. 16.508 (Γλαύκῳ δʼ)"),
}

# cited lines that the claimed string does not contain, with the reviewer's explanation (no FAIL)
CIT_EXPLAINED = {
    (33, 0, "Od. 18.34"): "elision variant: the line has τοῖϊν δέ unelided, as the citation itself says (the count 2 counts it; the recorded query gives 1)",
    (33, 1, "Od. 11.110"): "citation order (see the QUERY): Il. 11.110 has τοῖιν at 5-5.5",
    (33, 1, "Od. 23.336"): "citation order (see the QUERY): Il. 23.336 has τοῖιν at 5-5.5",
    (56, 7, "Od. 20.369"): "cited for the entry's second model, ἀντιθέου (7-9 there, the slot of Ἑλβετίου: section 7), not for Ἀτρεΐδης",
    (40, 3, "Il. 5.5"): "parser artefact: '3-5.5' in the citation text read as a line number by provenance_check.parse_citations; no such citation is intended",
}


def toks(s):
    return [t.core for t in G.tokenize(G.nfc(s))]


def generic_modified(s, rec_ev, rec):
    f0 = s["fragments"][0]
    vw = set(rec_ev["words"])
    tk = toks(f0["H"])
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
    global FUNC, NAME_PAR
    import poem_density as PD
    FUNC = PD.FUNC
    c1, c2 = len(PD.P.C.ngram("βοὴν ἀγαθὸς Διομήδης")), len(PD.P.C.ngram("βοὴν ἀγαθὸς Μενέλαος"))
    NAME_PAR = (f"Homer alternates names in one slot: βοὴν ἀγαθὸς Διομήδης {c1}x / βοὴν ἀγαθὸς Μενέλαος {c2}x "
                "(6-12); the model line itself shows the slot (section 7)")
    ev = json.load(open(EV, encoding="utf-8"))
    dens = json.load(open(DENS, encoding="utf-8"))
    dens1 = json.load(open(DENS1, encoding="utf-8"))
    extra = json.load(open(EXTRA, encoding="utf-8"))
    recs = {json.loads(l)["n"]: json.loads(l) for l in open(JSONL, encoding="utf-8") if l.strip()}
    prev = {json.loads(l)["n"]: json.loads(l) for l in open(JSONL_PREV, encoding="utf-8") if l.strip()}
    slots = {}
    for x in extra["name_slots"]:
        slots.setdefault(x["verse"], []).append(x)
    zero = {(z["n"], z["loose"]): z for z in extra["forms_with_0_homeric_hits"]}

    rows, detail = [], []
    tallies, agree = Counter(), Counter()
    fails, queries = {}, {}
    unclaimed_all, cit_notes = [], []
    cls_of, kind_of = {}, {}
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
                               f"{len(r['parallels'])} verified (section 8)")
            cls_of[(n, k)] = cls
            kind_of[(n, k)] = kind
            hw = s["fragments"][0]["H_loose"].split() if s["fragments"] else []
            if cls == "E" and len(hw) >= 2:
                exact2_lines.add(n)
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
        rows.append((n, f"| {R.esc(rec['text'])} | **{verdict}** | {' '.join(ent)} | {par_ok}/{len(r['parallels'])} | {R.esc(unc_s)} | {R.esc(reasons)} |"))

    verdicts = Counter("FAIL" if n in fails else "QUERY" if n in queries else "PASS" for n in recs)
    n_cited = sum(len(s["cited_check"]) for r in ev for s in r["sources"])
    n_par = sum(len(r["parallels"]) for r in ev)
    n_par_ok = sum(p["verified"] for r in ev for p in r["parallels"])
    par_bad = [(r["n"], p["quoted"], p["citation"]) for r in ev for p in r["parallels"] if not p["verified"]]
    cc = ev[0].get("cli_crosscheck") or {}
    D, D1 = dens["coverage"], dens1["coverage"]
    ref = dens["homeric_reference_verse_vs_rest_of_homer"]
    CL = {(c["n"], c["label"]): c for c in extra["claims"]}

    def cl(n, label):
        return CL[(n, label)]

    def pos(c, k=4):
        return ", ".join(f"{p} {v}x" for p, v in list(c["positions"].items())[:k]) or "-"

    def cited_ok(c):
        return all(v != "NOT A HIT" for v in c["cited"].values())

    # changes since v3
    new_lines = [n for n in sorted(recs) if recs[n].get("v3_line") is None]
    text_changed = [n for n in sorted(recs) if n not in new_lines and recs[n]["text"] != prev[recs[n]["v3_line"]]["text"]]
    rec_changed = [n for n in sorted(recs) if n not in new_lines and n not in text_changed and any(
        recs[n].get(k) != prev[recs[n]["v3_line"]].get(k) for k in ("sources", "modifications", "coinages", "notes", "gloss", "facts"))]
    dropped_v3 = sorted(set(prev) - {recs[n]["v3_line"] for n in recs if recs[n].get("v3_line")})

    out = []
    A = out.append
    A("# Provenance review: composition/drafts/v4 (provenance-verifier, final round)")
    A("")
    A("Generated by `review/provenance_report_v4.py` from `review/provenance_v4_evidence.json` (`review/provenance_check.py`), "
      "`review/provenance_v4_extra.json` (`review/provenance_v4_extra.py`) and `review/poem_density_v4.json` "
      "(`review/poem_density.py`); rerun:")
    A("")
    A("```")
    A("source .venv/bin/activate")
    A("python -I review/provenance_check.py composition/drafts/v4.jsonl review/provenance_v4_evidence.json")
    A("python -I review/poem_density.py composition/drafts/v4.jsonl review/poem_density_v4.json")
    A("python -I review/provenance_v4_extra.py composition/drafts/v4.jsonl review/provenance_v4_evidence.json review/provenance_v4_extra.json")
    A("python -I review/provenance_report_v4.py")
    A("```")
    A("")
    A("## 1. Method")
    A("")
    A(f"* As for v1-v3 (review/provenance_v1.md section 1, review/provenance_v3.md section 1): every `sources` entry of the {len(recs)} "
      "records was rerun with its recorded query through the `Concordance` methods behind `homer/concordance.py`'s CLI, and every distinct "
      "query once more through the CLI itself (`--count`); the Homeric string of each entry was run with `ngram`, each cited line checked "
      "for it, and its position in the verse (`homer/scan.py --json`) compared with its Homeric positions. Every 2-word and longer window "
      "of every verse was run through `ngram` for unclaimed attested phrases. The Greek-plus-citation pairs quoted in the records' "
      f"`modifications` were checked the same way. All {len(recs)} records were rerun, not only the changed ones.")
    A(f"* Changes since v3 (from the records' `v3_line` and the two jsonl files): **new verses** {', '.join(map(str, new_lines))}; "
      f"**verse text changed** {', '.join(map(str, text_changed))}; record fields only {', '.join(map(str, rec_changed))}; v3 verses "
      f"withdrawn: {', '.join(map(str, dropped_v3)) or 'none'} (v3 numbering). v3 had {len(prev)} verses, v4 has {len(recs)}.")
    A(f"* `review/provenance_v4_extra.py` (adapted from the v3 script): forms with 0 Homeric hits and where each record discloses them "
      "(now including `modifications`); every form listed in `coinages` looked up in Homer; the coined stems as loose substrings; every "
      "coined name's slot against the position of the Homeric model word in the cited model line (and, marked 'reviewer', a model line "
      "that shows the slot where the cited one does not); `homer/check_line.py` on every verse (Addendum A1: a name slot is allowed where "
      f"check_line passes with no flags); the accents of Νοβῆκος / Νοβήκου; and {len(extra['claims'])} counts, positions and cited lines "
      "asserted in free text of the changed records, in the round-3 corrections and in the critic's M8 parallels (section 5).")
    A("* Classes and verdicts: as v1-v3. **ATTESTED-EXACT** = in the verse word for word (accent-insensitive; movable ν ignored and "
      "noted), in the cited lines, at a position Homer gives it; **ATTESTED-MODIFIED** = in the cited lines, changed in the verse "
      "(kind stated, with a Homeric parallel for that kind where one is offered or found); **NOT-ATTESTED** = not in the cited "
      "lines, or the configuration asserted does not occur. COINAGE entries are classed by their model (a substitution when the model "
      "word stands in the cited line at the coined name's position). **FAIL** / **QUERY** / **PASS**: header of "
      "`review/provenance_report_v4.py` (the v1 criteria). Free-text bookkeeping errors that change no class are listed in section 9.")
    A("")
    A("## 2. Summary")
    A("")
    m3 = re.search(r"PASS (\d+), QUERY (\d+), FAIL (\d+)\*\* \(of (\d+)\)", PREV_MD.read_text(encoding="utf-8"))
    A(f"* Lines: **PASS {verdicts['PASS']}, QUERY {verdicts['QUERY']}, FAIL {verdicts['FAIL']}** (of {len(recs)}). "
      + (f"v3 (review/provenance_v3.md): PASS {m3.group(1)}, QUERY {m3.group(2)}, FAIL {m3.group(3)} (of {m3.group(4)})." if m3 else ""))
    A(f"* Source entries: {sum(tallies.values())}; reviewer's classes: ATTESTED-EXACT {tallies['ATTESTED-EXACT']}, "
      f"ATTESTED-MODIFIED {tallies['ATTESTED-MODIFIED']}, NOT-ATTESTED {tallies['NOT-ATTESTED']}.")
    cnt_bad = [f"{r['n']}/{k}" for r in ev for k, x in enumerate(r['sources'])
               if x['claimed_count'] != x['query_total'] or recs[r['n']]['sources'][k].get('query_hits') != x['query_total']]
    A(f"* Recorded queries: {cc.get('distinct_queries')} distinct, each rerun with `python homer/concordance.py … --count`; mismatches "
      f"with the in-process rerun: {len(cc.get('mismatches', {}))}. Entries whose `count` or `query_hits` differ from the rerun "
      f"total: {len(cnt_bad)} ({', '.join(cnt_bad) or '-'}).")
    no_cit = [f"{r['n']}/{k}" for r in ev for k, x in enumerate(r["sources"]) if not x["cited_lines"]]
    A(f"* Cited lines checked: {n_cited}; lines that neither contain the claimed string nor are hits of the recorded query: "
      + ("; ".join(cit_notes) if cit_notes else "none") + ". Entries that cite no line: " + (", ".join(no_cit) or "none") + ".")
    A(f"* Homeric parallels quoted in the records' `modifications`: {n_par}; found in the cited line by the concordance: {n_par_ok}"
      + (f" (not found: {'; '.join(f'{a}: {b} {c}' for a, b, c in par_bad)})" if par_bad else "") + ".")
    ncl_ok = sum(1 for c in extra["claims"] if cited_ok(c))
    A(f"* Free-text claims recomputed (section 5): {len(extra['claims'])}; with every cited line a hit of the query: {ncl_ok}; "
      "counts, positions or descriptions that the concordance does not reproduce: section 9 (no class changes).")
    sc_bad = [r["n"] for r in ev if (r["scan"]["word_positions"] != recs[r["n"]]["scansion"]["word_positions"].split()
                                     or r["scan"]["pattern"] != recs[r["n"]]["scansion"]["pattern"])]
    A(f"* The records' `scansion.word_positions` and `pattern` agree with `homer/scan.py --json` in {len(recs) - len(sc_bad)} of "
      f"{len(recs)} lines" + (f" (differ: {', '.join(map(str, sc_bad))})" if sc_bad else "") + "; all positions in this review are "
      f"scan.py's. `homer/check_line.py`: {extra['check_line']['n_flagged']} verses flagged, {extra['check_line']['n_unmetrical']} "
      f"unmetrical (of {extra['check_line']['n_verses']}).")
    A("* FAIL lines: " + ("; ".join(f"**{n}** ({' / '.join(v)})" for n, v in sorted(fails.items())) or "none") + ".")
    A("* QUERY lines: " + ("; ".join(f"**{n}** ({' / '.join(v)})" for n, v in sorted(queries.items()) if n not in fails) or "none") + ".")
    A(f"* Density (section 10): n ≥ 2 coverage {D['n2_all_min1']['coverage']}% [{D['n2_all_min1']['ci95'][0]}, {D['n2_all_min1']['ci95'][1]}] "
      f"(v3 {D1['n2_all_min1']['coverage']}%); verbatim Homeric lines {dens['verses_identical_to_a_homeric_verse']} of {dens['verses']} "
      f"(v3 {dens1['verses_identical_to_a_homeric_verse']} of {dens1['verses']}); lines with an ATTESTED-EXACT formula of ≥ 2 words "
      f"{dens['lines_with_claimed_exact_formula_ge2_words']}/{dens['verses']} = {dens['lines_with_claimed_exact_formula_ge2_words_pct']}%, "
      f"not function words only {dens['lines_with_claimed_exact_formula_ge2_words_not_function_only_pct']}%.")
    A("")
    A("## 3. Composer's labels v. reviewer's classes (source entries)")
    A("")
    A("| composer | reviewer | entries |")
    A("|---|---|---|")
    for (c, m), v in sorted(agree.items()):
        A(f"| {c} | {m} | {v} |")
    A("")
    lab_bad = [(n, k) for (n, k), c in cls_of.items() if recs[n]["sources"][k]["status"] == "ATTESTED-EXACT" and c != "E"]
    lab_bad2 = [(n, k) for (n, k), c in cls_of.items() if recs[n]["sources"][k]["status"] == "ATTESTED-MODIFIED" and c == "E"]
    coin_n = [(n, k) for (n, k), c in cls_of.items() if recs[n]["sources"][k]["status"] == "COINAGE" and c == "N"]
    A("* Labelled ATTESTED-EXACT but not exact: " + ("; ".join(f"{n}/{k} '{recs[n]['sources'][k]['text'][:60]}' ({R.esc(kind_of[(n, k)][:160])})"
                                                          for n, k in lab_bad) or "none") + ".")
    A("* Labelled ATTESTED-MODIFIED but exact: " + (", ".join(f"{n}/{k}" for n, k in lab_bad2) or "none")
      + ". 25/4 (δάμασεν, exact apart from the movable ν, as in v3 24/4) is classed modified by judgment, as labelled; 37/3 and 59/3 "
      "contain καὶ βάλεν, which also stands in the verse at 1-2 (entry 0): the entries are for the second καὶ βάλεν at 9-10, and are "
      "classed modified (mobility), as labelled.")
    A("* COINAGE entries classed NOT-ATTESTED: " + (", ".join(f"{n}/{k}" for n, k in coin_n) or "none")
      + "; by judgment (section 7) 24/1, 29/6 and 62/0 are substitutions into slots allowed by A1 (check_line clean), but their cited "
      "model lines do not show the slot: QUERY, with a model line that does.")
    A("")

    # ------------------------------------------------------------------ section 4
    A("## 4. Round-3 record corrections (review/round_3.md, provenance_v3 section 8) and the critic's M8 parallels")
    A("")
    A("| item | v4 line(s) | check | result |")
    A("|---|---|---|---|")

    def mods(n):
        return " ".join(m["homeric_parallel"] for m in recs[n]["modifications"])

    def notes(n):
        return recs[n].get("notes") or ""

    def coin(n):
        return " ".join(c["analogical_model"] for c in recs[n].get("coinages") or [])

    def alltext(n):
        r = recs[n]
        return " ".join([r.get("notes") or "", mods(n), coin(n)] + [s["text"] + " " + s["citation"] for s in r["sources"]])
    td, td2 = cl(20, "τρὶς δέ"), cl(20, "τρὶς δʼ")
    kr, pk = cl(55, "κρατεροῖο"), cl(55, "Πολυποίταο κρατεροῖο")
    pd6 = cl(55, "* δʼ αὖ (pronoun at 6)")["positions"].get("6-7")
    da7 = cl(55, "δʼ αὖ")["positions"].get("7-7")
    COMMA = re.compile(r"καὶ βάλεν, οὐδ. ἀφάμαρτε, \w+, καὶ βάλεν αὖτις")
    rows4 = [
        ("20 notes: τρὶς δέ 8x, τρὶς δʼ 9x", "20",
         f"notes say '8x' and '9x': {'τρὶς δέ 8x' in notes(20) and '9x' in notes(20)}; concordance τρὶς δέ {td['total']}x ({pos(td)}), τρὶς δʼ {td2['total']}x", "applied"),
        ("51 κρατεροῖο 4 at 9.5-12, 3 at 7.5-9.5", "55",
         f"entry 5: '{recs[55]['sources'][5]['text']}'; concordance {kr['total']}x: {pos(kr)}", "applied"),
        ("51 Πολυποίταο κρατεροῖο at 5.5-12", "55", f"entry 6 `position` {recs[55]['sources'][6]['position']}; concordance {list(pk['positions'])[0]}", "applied"),
        ("51 pronoun + δʼ αὖ at 6-7: 4x (not 6x)", "55",
         f"modifications still say 'pronoun + δʼ αὖ at 6-7 is Homeric 6x': {'Homeric 6x' in mods(55)}; concordance: δʼ αὖ at 7 {da7}x, "
         f"a one-syllable word + δʼ αὖ at 6-7 {pd6}x", "**not applied** (section 9)"),
        ("51 note on Ζοκοβείδαο before a double consonant", "55", f"in notes: {'double consonant' in notes(55)}", "applied"),
        ("56/1 position field (αὖθʼ ἱερεύς at 3-5)", "60", f"60/1 `position` {recs[60]['sources'][1]['position']}; concordance {pos(cl(60, 'αὖθʼ ἱερεὺς'))}", "applied"),
        ("36 cite Il. 5.432 and Il. 13.20", "41",
         f"41/4 cites {recs[41]['sources'][4]['citation']} ({pos(cl(41, 'ἐπόρουσε βοὴν ἀγαθὸς Διομήδης'))}); 41/5 cites {recs[41]['sources'][5]['citation']} "
         f"({pos(cl(41, 'τρὶς μὲν ὀρέξατʼ ἰών'))}); the contraction stated in notes: {'contraction' in notes(41)}; the intervening τρὶς δʼ lines "
         f"Il. 5.437, 16.785, 20.446 verified: {cited_ok(cl(41, 'τρὶς δʼ (the intervening line)'))}", "applied"),
        ("44 Νοβῆκος SLS at 4-5.5, parallels Il. 21.256, 23.376-377, Od. 2.203", "49",
         "v3 44 is rebuilt as 49 with Σέρβος at 1-2; the note says the correction no longer applies: "
         f"{'no longer applies' in notes(49)}; Νοβῆκ- in 49: {'Νοβῆκ' in recs[49]['text']}", "moot"),
        ("33/55 cite Od. 22.272 for αὖτις 'again'; comma after ἀφάμαρτε", "37, 59",
         f"Od. 22.272 cited in 37: {any('22.272' in s['citation'] for s in recs[37]['sources'])}, 59: {any('22.272' in s['citation'] for s in recs[59]['sources'])} "
         f"(verified {pos(cl(37, 'αὖτις δὲ μνηστῆρες ἀκόντισαν'))}); 37 and 59 both read 'καὶ βάλεν, οὐδʼ ἀφάμαρτε, NAME, καὶ βάλεν αὖτις': "
         f"{all(COMMA.match(recs[n]['text']) is not None for n in (37, 59))}", "applied"),
        ("23 cite Il. 23.511 (λάβʼ ἄεθλον)", "20",
         f"v3 23 withdrawn; λάβʼ ἄεθλον now in 20 at {', '.join(e['fragments'][0]['poem_positions'][0] for e in [ev[19]['sources'][6]])}, "
         f"its only Homeric slot ({pos(cl(20, 'λάβʼ ἄεθλον'))}, Il. 23.511 cited)", "applied (and M8 restored)"),
        ("provenance_v3 36: add Il. 5.432 (ἐπόρουσε βοὴν ἀγαθός unclaimed)", "41", f"41/4: {recs[41]['sources'][4]['text'][:70]}", "applied"),
        ("provenance_v3 36/37: the τρὶς μέν → τὸ τέταρτον sequence is a contraction", "41-42", f"stated in 41 notes: {'contraction' in notes(41)}", "applied"),
        ("M8 καὶ βάλεν at 9-10 (Homer 1-2 only)", "37, 59",
         f"καὶ βάλεν {cl(37, 'καὶ βάλεν')['total']}x, {pos(cl(37, 'καὶ βάλεν'))}; parallels of the same shift in 37 and 59: καὶ σάκος "
         f"({pos(cl(37, 'καὶ σάκος'))}; cited lines verified: {cited_ok(cl(37, 'καὶ σάκος'))}), ἔνθα δέ ({pos(cl(37, 'ἔνθα δὲ'))}; "
         f"{cited_ok(cl(37, 'ἔνθα δὲ'))}), αἶψα δʼ ({pos(cl(37, 'αἶψα δʼ'))}; {cited_ok(cl(37, 'αἶψα δʼ'))}); the record calls it 'a departure "
         f"from Homer's localisation': {'departure' in mods(37) and 'departure' in mods(59)}", "present (counts at 1-2 corrected in section 9)"),
        ("M8 τὴν δʼ αὖ at 6-7 (Homer 1-2 only)", "55",
         f"τὴν δʼ αὖ {cl(55, 'τὴν δʼ αὖ')['total']}x, {pos(cl(55, 'τὴν δʼ αὖ'))}; parallels: τὴν δʼ at 6-7 {cl(55, 'τὴν δʼ (at 6-7)')['positions'].get('6-7')}x "
         f"(Il. 22.211 verified: {cited_ok(cl(55, 'τὴν δʼ (at 6-7)'))}), τὸν δʼ at 6-7 {cl(55, 'τὸν δʼ (at 6-7)')['positions'].get('6-7')}x "
         f"(Il. 2.396, 2.701 verified: {cited_ok(cl(55, 'τὸν δʼ (at 6-7)'))})", "present (entry 9 mislabelled: FAIL)"),
        ("M8 λάβʼ ἄεθλον out of slot (v3 23, 3.5-5.5)", "20", f"now at its slot 9.5-12 inside ἐσσυμένως λάβʼ ἄεθλον ({pos(cl(20, 'ἐσσυμένως λάβʼ ἄεθλον'))}, Il. 23.511)", "restored"),
        ("M8 single-word mobility (σφαῖραν, βάλλον 22; ἔλαβεν 28 → 30; πολλάκι 48 → 52; τέλος 60 → 64)", "22, 30, 38, 52, 64",
         "mobility modifications in v4: " + ", ".join(f"{n}" for n in sorted(recs) if any(m["kind"] == "mobility" for m in recs[n]["modifications"]))
         + f" (v3: {', '.join(str(n) for n in sorted(prev) if any(m['kind'] == 'mobility' for m in prev[n]['modifications']))})", "disclosed, unchanged"),
    ]
    for a, b, c, d in rows4:
        A(f"| {R.esc(a)} | {b} | {R.esc(c)} | {d} |")
    A("")

    # ------------------------------------------------------------------ section 5 new material
    A("## 5. The new and rebuilt material (critic_poem_v1 issues): what the concordance shows")
    A("")
    cfh = {(c["n"], c["form"]): c for c in extra["coinage_forms_in_homer"]}
    pum = cfh.get((24, "πυμάτῃ"))
    acc_os, acc_ou = extra["accent_eta_C_os"], extra["accent_eta_C_ou"]
    gen = extra["slot_gen_ou_10_12_capitalised"]
    dat = extra["slot_dat_omega_1_2_before_de"]
    items = [
        ("24 tie-break, ἐνίκα (M2, M4)",
         f"ἐνίκα {cl(24, 'ἐνίκα')['total']}x ({pos(cl(24, 'ἐνίκα'))}), at 10-12 as in the verse; the frame ἀλλʼ ὅ γʼ … ἐνίκα is Il. 4.389 "
         f"(verified); ἀλλʼ ὅ γε {pos(cl(24, 'ἀλλʼ ὅ γε'))}. The contest in the dative with ἐνίκα is Homeric (πόδεσσι δὲ πάντας ἐνίκα Il. 20.410, "
         f"κάλλει ἐνίκα Il. 23.742: verified). μάχῃ {cl(24, 'μάχῃ')['total']}x ({pos(cl(24, 'μάχῃ'))}), not 26 as the entry's count. "
         f"πυμάτῃ: the record says '0 hits'; exact (with iota subscript) {cl(24, 'πυμάτῃ (exact NFC)')['total']}, but the loose form "
         f"(the concordance's and the density's comparison) has {pum['loose_hits'] if pum else '?'} hit, the nominative "
         f"{(pum['loose_examples'][0] if pum and pum['loose_examples'] else '-')}: a closer model than the cited πυμάτην (Il. 18.608) and "
         f"not a coinage in the loose sense. πύματον {cl(24, 'πύματον')['total']}x ({pos(cl(24, 'πύματον'))}). Σέρβος at 3-3.5: the cited "
         "Il. 6.45 has Ἄδρηστος at 1-3; the slot is shown by Τεῦκρος (Il. 12.350, 3-3.5 before a vowel)."),
        ("29 the 2:49:12 break (M3)",
         f"ἀλλὰ καὶ ὧς {pos(cl(29, 'ἀλλὰ καὶ ὧς'))}; ἐδάμη {cl(29, 'ἐδάμη')['total']}x, {pos(cl(29, 'ἐδάμη'))} only (verse 3.5-5, labelled exact); "
         f"ὑπὸ χερσί {cl(29, 'ὑπὸ χερσὶ')['total']}x ({pos(cl(29, 'ὑπὸ χερσὶ'))}), at 7.5-9.5 as in the verse; κρατεροῦ {cl(29, 'κρατεροῦ')['total']}x "
         f"({pos(cl(29, 'κρατεροῦ'))}; verse 5.5-7, labelled exact). The modification says 'the epithet before ὑπό as ὑπὸ κρατεροῦ Ἀχιλῆος "
         "(Il. 21.553)'; in Il. 21.553 ὑπό precedes κρατεροῦ (ὑπὸ κρατεροῦ Ἀχιλῆος, 6-12), so the line is no parallel for the verse's order "
         "κρατεροῦ ὑπὸ χερσὶ Νοβήκου; Homer puts an agent genitive before ὑπὸ χερσί (Ἀτρεΐδεω / Πατρόκλου / Τηλεμάχου / Αἰγίσθου ὑπὸ χερσί, "
         "1-5.5) or after it (Il. 2.860, 16.438), never an epithet before and its noun after among the 11 lines. Νοβήκου at 10-12: the "
         f"cited models do not show the slot; SLL name genitives in -ου at 10-12 do ({', '.join(f'{w} {c}x' for w, c in gen['by_type'])}; "
         "ὑπʼ ἀνδροφόνοιο Λυκούργου, Il. 6.134). Accent: Homeric words in η + one consonant + -ου: "
         f"{acc_ou['acute_types']} types / {acc_ou['acute_tokens']} tokens with the acute, {acc_ou['circumflex_types']} with the circumflex "
         f"(e.g. {', '.join(w for w, _ in acc_ou['acute_examples'][:4])}), so Νοβήκου beside Νοβῆκος is right. Register: ἀλλʼ ἐδάμη ὑπὸ χερσὶ "
         "ποδώκεος Αἰακίδαο (Il. 2.860 = 2.874) is a death in both uses (the lines before: Il. 2.859 ἀλλʼ οὐκ οἰωνοῖσιν ἐρύσατο κῆρα μέλαιναν; 2.873 οὐδέ τί οἱ τό γʼ ἐπήρκεσε λυγρὸν ὄλεθρον), the register critic M5 asked to avoid for "
         "the loser; for the philologist."),
        ("35-36 crowd and heralds (M7; Il. 18.502-503)",
         f"35 is Il. 18.502 verbatim ({pos(cl(35, 'λαοὶ δʼ ἀμφοτέροισιν ἐπήπυον ἀμφὶς ἀρωγοί'))}); 36 keeps κήρυκες δʼ ἄρα λαὸν ἐρήτυον at "
         f"{pos(cl(36, 'κήρυκες δʼ ἄρα λαὸν ἐρήτυον'))} (Il. 18.503) and replaces οἳ δὲ γέροντες by ἔνθα καὶ ἔνθα ({cl(36, 'ἔνθα καὶ ἔνθα')['total']}x, "
         f"{pos(cl(36, 'ἔνθα καὶ ἔνθα'))}); the two Homeric lines are consecutive, as in the poem. ἐρήτυον {cl(36, 'λαὸν ἐρήτυον τὼ (rejected test)')['total']}x, "
         f"{pos(cl(36, 'λαὸν ἐρήτυον τὼ (rejected test)'))}. Both entries exact."),
        ("38 ἤρατο κῦδος counterfactual (M4)",
         f"ἄσπετον ἤρατο κῦδος {cl(38, 'ἄσπετον ἤρατο κῦδος')['total']}x ({pos(cl(38, 'ἄσπετον ἤρατο κῦδος'))}): Il. 3.373 and 18.165, both "
         "καί νύ κεν εἴρυσσέν τε καὶ …, both followed by an εἰ μή line (Il. 3.374, 18.166); the verse keeps 5.5-12 verbatim and the εἰ μή line "
         f"follows (39). καί νύ κεν ἔνθʼ {cl(38, 'καί νύ κεν ἔνθʼ')['total']}x ({pos(cl(38, 'καί νύ κεν ἔνθʼ'))}; Il. 8.90 at 3-5, so 2 at 1-3, "
         f"not 3); ἔλαβεν {pos(cl(38, 'ἔλαβεν'))}, verse 3.5-5, disclosed as mobility."),
        ("40 CP2 (M1)",
         f"στῆ δὲ μάλʼ ἐγγὺς ἰών {pos(cl(40, 'στῆ δὲ μάλʼ ἐγγὺς ἰών'))}; ὃ δέ μιν {pos(cl(40, 'ὃ δέ μιν'))}; οὐδʼ ἀφάμαρτε {pos(cl(40, 'οὐδʼ ἀφάμαρτε'))}; "
         f"βάλεν οὐδʼ ἀφάμαρτε {pos(cl(40, 'βάλεν οὐδʼ ἀφάμαρτε'))} (verse 7.5-12, disclosed as mobility). All exact entries exact; "
         "Djokovic is the subject of the hit verb at 4:11:30, as the critic asked."),
        ("49 τυτθόν (M7, m8)",
         f"τυτθὸν ὀπίσσω {pos(cl(49, 'τυτθὸν ὀπίσσω'))} (Il. 5.443 Τυδεΐδης δʼ ἀνεχάζετο τυτθὸν ὀπίσσω); τυτθόν {cl(49, 'τυτθὸν')['total']}x "
         f"({pos(cl(49, 'τυτθὸν'))}); ὃ δʼ ἐπέσσυτο {pos(cl(49, 'ὃ δʼ ἐπέσσυτο'))} (Il. 21.234, 21.601); ἔκφερεν {pos(cl(49, 'ἔκφερεν'))} "
         f"(verse 3-4, disclosed); ὃ δʼ ἕσπετο removed ({cl(49, 'ὃ δʼ ἕσπετο (removed)')['total']}x in Homer). The entry for the elided ἔκφερʼ "
         "(49/2) is labelled exact although the verse has ἔκφερεν."),
        ("56 ἐέλδωρ (M5)",
         f"ἐέλδωρ {cl(56, 'ἐέλδωρ')['total']}x ({pos(cl(56, 'ἐέλδωρ'))}: one at 6-8, Od. 23.54, so not 'all verse-final'); ἕλκε δὲ μέσσα λαβών· "
         f"ῥέπε δʼ {pos(cl(56, 'ἕλκε δὲ μέσσα λαβών ῥέπε δʼ'))} (Il. 8.72, 22.212); ῥέπε δʼ αἴσιμον ἦμαρ Ἀχαιῶν (Il. 8.72) verified; the "
         f"genitive owner + ἐέλδωρ: Πηλεΐδαο … ἐέλδωρ (Il. 15.74) verified. τότʼ at 9.5 {cl(56, 'τότʼ')['positions'].get('9.5-9.5')}x (count "
         f"field 3, query total {cl(56, 'τότʼ')['total']}). Ἑλβετίου at 7-9 = Ἀτρεΐδης (Il. 14.29) and ἀντιθέου (Od. 20.369): slot shown."),
        ("62 κῦδος ἔδωκε (M4)",
         f"Ζεὺς κῦδος ἔδωκε {pos(cl(62, 'Ζεὺς κῦδος ἔδωκε'))} (Il. 8.216); κῦδος ἔδωκε {cl(62, 'κῦδος ἔδωκε')['total']}x ({pos(cl(62, 'κῦδος ἔδωκε'))}); "
         f"Ἕκτορι κῦδος ἔδωκε {pos(cl(62, 'Ἕκτορι κῦδος ἔδωκε'))}; ἀντιθέῳ {pos(cl(62, 'ἀντιθέῳ'))}; τότε δὴ at 5.5-7 "
         f"{cl(62, 'τότε δὴ')['positions'].get('5.5-7')}x (Il. 10.366, 23.374), not Od. 9.52 (3.5-5) as the entry says. Unclaimed and apt: "
         f"δὴ Ζεὺς κῦδος (Il. 12.437, {pos(cl(62, 'δὴ Ζεὺς κῦδος (unclaimed)'))}, position not the verse's): πρίν γʼ ὅτε δὴ Ζεὺς κῦδος ὑπέρτερον "
         "Ἕκτορι δῶκε follows ὣς μὲν τῶν ἐπὶ ἶσα μάχη τέτατο πτόλεμός τε (Il. 12.436), the line the poem uses in 21: Homer's own sequence "
         f"'level fight, then Zeus gives κῦδος'. Σέρβῳ δʼ at 1-2: the cited τῷ δʼ has τῷ at 1; LL dative names at 1-2 before δʼ: "
         f"{dat['count']} Homeric lines with a dative in -ῳ at 1-2 + δʼ (e.g. Γλαύκῳ δʼ, Il. 16.508)."),
        ("61 the vocative Φεδερεῦ (M7)",
         f"Φεδερεῦ {cl(61, 'Φεδερεῦ')['total']} hits (listed in `coinages`); Ἀχιλεῦ {cl(61, 'Ἀχιλεῦ')['total']}x ({pos(cl(61, 'Ἀχιλεῦ'))}): the three "
         "cited lines have it at 5.5-7, the verse's slot (section 7); the entry's count 3 is the 5.5-7 subset. ἤμβροτες οὐδʼ ἔτυχες "
         f"{pos(cl(61, 'ἤμβροτες οὐδʼ ἔτυχες'))} (Il. 5.287, in direct speech: Il. 5.286 … προσέφη κρατερὸς Διομήδης; the verse makes it the narrator's apostrophe, "
         f"for which Il. 16.787, 4.127 and 16.692-693 are cited and verified); μάλα πολλά {pos(cl(61, 'μάλα πολλὰ'))}; πολλὰ μογήσας "
         f"{pos(cl(61, 'πολλὰ μογήσας'))}; μάλα πολλὰ μογήσας {cl(61, 'μάλα πολλὰ μογήσας (verse 7.5-12)')['total']}x "
         "(disclosed as an expansion on the shared πολλά)."),
        ("34 παρέλασσε (M4, m1)",
         f"παρέλασσʼ {cl(34, 'παρέλασσʼ')['total']}x ({pos(cl(34, 'παρέλασσʼ'))}), the unelided παρέλασσε {cl(34, 'παρέλασσε (verse form)')['total']}x: "
         "a regular but unattested form, disclosed in `modifications` but not in `coinages`, and entry 1 is labelled exact for the elided form. "
         "Both Homeric uses are in a κεν-clause (Il. 23.382 καί νύ κεν ἢ παρέλασσʼ ἢ ἀμφήριστον ἔθηκεν; 23.527 τώ κέν μιν παρέλασσʼ), as is "
         f"ἀμφήριστον ἔθηκεν in 32 ({pos(cl(32, 'ἀμφήριστον ἔθηκεν'))}, the same two lines): the poem makes both race verbs factual (32, 34). "
         f"ὀψὲ δὲ δή {pos(cl(34, 'ὀψὲ δὲ δὴ'))}; ἄφαρ gone (m1)."),
        ("32, 33, 54, 58, 63 (other rebuilt lines)",
         f"32: unclaimed ἂψ ἐπόρουσε (Il. 3.379, 21.33, {pos(cl(32, 'ἂψ ἐπόρουσε (unclaimed)'))}, the verse's position): αὐτὰρ ὃ ἂψ ἐπόρουσε "
         "(Il. 3.379-380, … τὸν δʼ ἐξήρπαξʼ Ἀφροδίτη) is the closer model for 1-5.5 than Od. 11.599 + Il. 11.580. 33: τοῖιν δʼ "
         f"{cl(33, 'τοῖιν δʼ')['total']}x (Il. 13.66), τοῖϊν δέ unelided Od. 18.34. 54: θαλερῶν αἰζηῶν {pos(cl(54, 'θαλερῶν αἰζηῶν'))}, μάχης at 6-7 "
         f"{cl(54, 'μάχης')['positions'].get('6-7')}x. 58: Il. 23.499's 6-12 verbatim; τὴν ἕτερος Od. 8.374; μετέπειτα {pos(cl(58, 'μετέπειτα'))}. "
         f"63: ὣς οἳ μὲν μάρναντο ({pos(cl(63, 'ὣς οἳ μὲν μάρναντο'))}) + Διὸς δʼ ἐτελείετο βουλή ({pos(cl(63, 'Διὸς δʼ ἐτελείετο βουλή'))}), "
         "two exact formulas at their slots; Il. 17.424 shows the half-line with another δέ-clause."),
    ]
    for a, b in items:
        A(f"* **{a}.** {b}")
    A("")

    # ------------------------------------------------------------------ section 6 claims
    A("## 6. Free-text claims recomputed (review/provenance_v4_extra.json, `claims`)")
    A("")
    A("Counts, positions and parallels asserted in the changed records (text, citation, modifications, notes, coinages), the round-3 "
      "corrections and the M8 parallels, rerun with the concordance. 'cited' = the cited line is a hit of the query (its position there).")
    A("")
    A("| line | string | query | Homer: total, positions | record asserts | cited lines (position) | ok |")
    A("|---|---|---|---|---|---|---|")
    for c in extra["claims"]:
        cit = "; ".join(f"{k}@{v}" for k, v in c["cited"].items()) or "-"
        A(f"| {c['n']} | {R.esc(c['label'])} | `{R.esc(c['query'])}` | {c['total']}: {R.esc(pos(c, 5))} | {R.esc(c['asserted'])} | "
          f"{R.esc(cit)} | {'yes' if cited_ok(c) else '**no**'} |")
    A("")

    # ------------------------------------------------------------------ section 7 slots
    A("## 7. Name slots: coined name v. Homeric model word (review/provenance_v4_extra.json)")
    A("")
    A("| verse | coined | position in the verse | word before / after | model | model line | model's position | before / after in the model | same | model word's positions in Homer | note |")
    A("|---|---|---|---|---|---|---|---|---|---|---|")
    for x in extra["name_slots"]:
        A(f"| {x['verse']} | {x['coined']} | {x['verse_position']} | {x['verse_prev'] or '^'} / {x['verse_next'] or '$'} | {x['model']} | "
          f"{x['model_citation']} | {x['model_position']} | {x['model_prev'] or '^'} / {x['model_next'] or '$'} | "
          f"{'yes' if x['same_position'] else '**no**'} | {R.esc(', '.join(f'{p} ({c})' for p, c in list(x['model_form_positions_in_homer'].items())[:4]))} | {R.esc(x['condition'])} |")
    A("")
    notsame = [x for x in extra["name_slots"] if not x["same_position"]]
    A("Every coined name stands where a model word stands in a Homeric line; the rows marked **no** are the records' cited models for "
      + ", ".join(sorted({f"{x['verse']} {x['coined']}" for x in notsame})) + ", each followed by the 'reviewer' row that shows the slot. "
      f"check_line flags none of the {extra['check_line']['n_verses']} verses, so all slots are allowed by Addendum A1; the QUERY is "
      "for the citation, not the metre. New slots in v4: Σέρβος at 3-3.5 (24, as Σέρβον in 48), Νοβήκου at 10-12 (29), Φεδερεῦ at "
      "5.5-7 (61, = Ἀχιλεῦ in all three cited lines), Σέρβῳ at 1-2 (62), Ἑλβετίου at 7-9 (56, = Ἀτρεΐδης Il. 14.29). Accent of Νοβῆκος: "
      f"η + consonant + -ος {acc_os['circumflex_types']} types with the circumflex, {acc_os['acute_types']} with the acute (unchanged from v3).")
    A("")

    # ------------------------------------------------------------------ section 8 per-line
    A("## 8. Per-line table")
    A("")
    A("Entries: `k:E/M/N` = entry k, reviewer's class (details in section 11). Parallels = the record's quoted Homeric parallels found "
      "in the cited line / quoted. Unclaimed = maximal attested windows not contained in any entry. Δ: N = new verse, T = verse text "
      "changed since v3, r = record only; v3 = the v3 line number.")
    A("")
    A("| n | v3 | Δ | verse | verdict | entries | parallels | unclaimed attested windows | reasons |")
    A("|---|---|---|---|---|---|---|---|---|")
    for n, row in rows:
        d = "N" if n in new_lines else "T" if n in text_changed else ("r" if n in rec_changed else "")
        A(f"| {n} | {recs[n].get('v3_line') or '-'} | {d} {row}")
    A("")

    # ------------------------------------------------------------------ section 9
    A("## 9. Unclaimed phrases, coinages, jsonl corrections")
    A("")
    A("* Unclaimed attested windows (all listed in the table): " + "; ".join(
        f"{n}: {w['ngram']} ({w['count']}x, {w['poem_position']}{'' if w['position_attested'] else ', not a Homeric position'})"
        for n, w in unclaimed_all) + ".")
    A(f"  * New in v4 and worth claiming: **32 ἂψ ἐπόρουσε** (3-5.5, Homer's position; Il. 3.379 = 21.33 αὐτὰρ ὃ ἂψ ἐπόρουσε): the verse's "
      "first half is that formula with γʼ added (αὐτὰρ ὅ γʼ ἂψ ἐπόρουσε); **62 δὴ Ζεὺς κῦδος** (Il. 12.437 at 3-5.5; the verse has it at "
      "7-9.5, so a sense parallel, not a slot): the Homeric sequence ἐπὶ ἶσα μάχη τέτατο (Il. 12.436) → Ζεὺς κῦδος … δῶκε (12.437) is the "
      "poem's own (21 … 62); **33 δʼ ἀργαλέῳ** (Il. 15.10, 16.109, 3-5) extends the claimed Il. 13.85 string by the particle.")
    A("  * The rest are as in v3: a particle extending a claimed formula (10, 20, 21, 43), or a fragment of a disclosed shift where the "
      "position is not Homeric (40 ἰών ὃ δέ, 52 δὴ περί, 60 δʼ ἄψ).")
    zl = extra["forms_with_0_homeric_hits"]
    notlisted = sorted({(z["n"], z["form"]) for z in zl if not z["in_coinages"]})
    undisclosed = sorted({(z["n"], z["form"]) for z in zl if not (z["in_coinages"] or z["in_coinage_entry"] or z["named_in_modified_entry"] or z["named_in_modifications"])})
    st = extra["coined_stems_substring_hits"]
    A("* Forms with 0 Homeric hits (`--loose … --word`): " + ", ".join(dens["unattested_forms"]) + ". Undisclosed: "
      + (", ".join(f"{f} ({n})" for n, f in undisclosed) or "none") + ". Disclosed but not listed in `coinages`: "
      + (", ".join(f"{f} ({n})" for n, f in notlisted) or "none") + ".")
    found = [c for c in extra["coinage_forms_in_homer"] if c["loose_hits"] or c["exact_hits"]]
    A("* Claimed coinages that exist in Homer (every form in `coinages`, loose and exact): "
      + ("; ".join(f"{c['n']} {c['form']}: loose {c['loose_hits']}, exact {c['exact_hits']} ({R.esc(c['loose_examples'][0]) if c['loose_examples'] else '-'})" for c in found) or "none")
      + ". `--loose` substrings of the coined stems: " + ", ".join(f"{k} {v}" for k, v in st.items()) + ".")
    A("* jsonl corrections (no verdict effect unless the line is listed in section 2):")
    corr = []
    es = cl(20, "ἐσσυμένως")
    corr.append(f"20/7 ἐσσυμένως: '12x: 7 line-initial, 3 at 7-9' → 12x: {pos(es, 5)}")
    corr.append(f"24/2 μάχῃ: `count` 26 → {cl(24, 'μάχῃ')['total']} ({pos(cl(24, 'μάχῃ'))}) [QUERY]")
    corr.append(f"24 `coinages` 'πύματον 6x' and modification 'πύματον at 3.5-5 (5x) and 5.5-7 (2x)' → {cl(24, 'πύματον')['total']}x: {pos(cl(24, 'πύματον'))} (entry 3 has it right)")
    corr.append(f"24 `coinages` πυμάτῃ '0 hits' → 0 exact, {pum['loose_hits'] if pum else '?'} loose: the nominative πυμάτη (Il. 6.118, 3.5-5); cite it")
    corr.append("24/1 Σέρβος at 3-3.5: cite Il. 12.350 (Τεῦκρος at 3-3.5 before a vowel); Il. 6.45 has the name at 1-3 [QUERY]")
    corr.append(f"29/3 ἐδάμη and 29/5 κρατεροῦ: relabel ATTESTED-MODIFIED (mobility: ἐδάμη {pos(cl(29, 'ἐδάμη'))} only, verse 3.5-5; κρατεροῦ {pos(cl(29, 'κρατεροῦ'))}, verse 5.5-7) [QUERY]")
    corr.append("29 modifications: 'with the epithet before ὑπό as ὑπὸ κρατεροῦ Ἀχιλῆος (Il. 21.553)' → in Il. 21.553 ὑπό precedes the epithet; the split κρατεροῦ ὑπὸ χερσὶ Νοβήκου has no parallel among the 11 ὑπὸ χερσί lines (an agent genitive stands before ὑπὸ χερσί in Il. 11.180, 16.699, Od. 18.156, 24.97)")
    corr.append("29/6 Νοβήκου: cite a model with the SLL genitive at 10-12, e.g. Il. 6.134 ὑπʼ ἀνδροφόνοιο Λυκούργου [QUERY]")
    corr.append(f"33/0 τοῖιν δʼ: `count` 2 → {cl(33, 'τοῖιν δʼ')['total']} (Od. 18.34 has τοῖϊν δέ, unelided: query `--ngram \"τοῖιν δέ\"`) [QUERY]")
    corr.append("33/1 τοῖιν: citation → 'Il. 11.110, 13.66, 23.336, Od. 18.34' [QUERY]")
    corr.append("34/1 παρέλασσʼ: relabel ATTESTED-MODIFIED (the verse has the unelided παρέλασσε) and list παρέλασσε (0x) in `coinages` [QUERY]")
    corr.append("34 modifications: 'as ἐδάμασσε / ἐπόρουσε end at 5.5 before βοήν in 14, 31, 41': 14 has ἀφάμαρτε")
    corr.append(f"37 / 59 modifications (M8 parallels): 'ἔνθα δὲ at 1-2 (13x …)' → {cl(37, 'ἔνθα δὲ')['positions'].get('1-2')}x; 'αἶψα δʼ at 1-2 (17x)' → {cl(37, 'αἶψα δʼ')['positions'].get('1-2')}x (the cited lines are right)")
    corr.append(f"38/0 καί νύ κεν ἔνθʼ: '3x' at 1-3 → {pos(cl(38, 'καί νύ κεν ἔνθʼ'))} (Il. 8.90 at 3-5)")
    corr.append("49/2 ἔκφερʼ: relabel ATTESTED-MODIFIED (parallel only; the verse has ἔκφερεν) [QUERY]")
    corr.append(f"55/9 'τὴν δʼ Ἕκτορος ἱπποδάμοιο' labelled ATTESTED-EXACT: relabel ATTESTED-MODIFIED, or reduce the entry to τὴν δʼ at 6-7 (Il. 22.211; "
                f"{cl(55, 'τὴν δʼ (at 6-7)')['positions'].get('6-7')}x at 6-7, not '5 at 7') [FAIL]")
    corr.append(f"55 modifications: 'pronoun + δʼ αὖ at 6-7 is Homeric 6x' → {pd6}x (the round-3 correction; δʼ αὖ at 7 is {da7}x)")
    corr.append(f"56/4 ἐέλδωρ: 'all verse-final' → {pos(cl(56, 'ἐέλδωρ'))} (Od. 23.54 at 6-8)")
    corr.append(f"56/6 τότʼ: `count` 3 → the query gives {cl(56, 'τότʼ')['total']} ({cl(56, 'τότʼ')['positions'].get('9.5-9.5')} at 9.5); use the 9.5 count with a query that reproduces it [QUERY]")
    corr.append(f"56/7 Ἑλβετίου: `count` 5 is Ἀτρεΐδης at 7-9; the recorded query `--loose ατρειδης --word` gives {cl(56, 'Ἀτρεΐδης')['total']} [QUERY]")
    corr.append(f"61/2 Ἀχιλεῦ: `count` 3 is the 5.5-7 subset; the recorded query gives {cl(61, 'Ἀχιλεῦ')['total']} [QUERY]")
    corr.append("62/0 Σέρβῳ δʼ: cite Il. 16.508 (Γλαύκῳ δʼ, an LL dative name at 1-2 before δʼ) instead of τῷ δʼ (τῷ at 1) [QUERY]")
    corr.append(f"62/2 τότε δή: 'at 5.5-7 … e.g. Od. 9.52' → Od. 9.52 has it at 3.5-5; at 5.5-7: Il. 10.366, 23.374 ({cl(62, 'τότε δὴ')['positions'].get('5.5-7')}x)")
    for p in extra["position_field_mismatches"]:
        if cls_of[(p["n"], p["k"])] == "E":
            corr.append(f"{p['n']}/{p['k']} '{p['text'][:50]}': `position` {p['position_field']}, but the string stands at {', '.join(p['verse_position'])} in the verse")
    for c_ in corr:
        A(f"  * {c_}")
    A("")

    # ------------------------------------------------------------------ section 10 density
    A("## 10. Formulaic density (review/poem_density.py)")
    A("")
    A(f"Method as v1-v3 (review/provenance_v1.md section 6): I = Homer, M = the poem ({dens['verses']} verses, {dens['tokens']} tokens); "
      "n-grams within one verse, compared as `concordance.py --ngram`; coverage = share of tokens inside at least one attested word "
      f"n-gram; `base` drops n-grams made only of function words ({dens['func_words']} frozen loose forms); `min2` = at least 2 Homeric "
      f"occurrences; 95% CI bootstrap over verses, B = {dens['B']}; shuffled = poem tokens permuted over positions, R = {dens['R']}; "
      "Homeric reference = each Homeric verse against the rest of Homer, token-weighted. This is the n-gram coverage method of "
      "analysis/formulas (report.md section 1: common.cover_a / boot_ratio / shuffle_tokens) applied to Greek.")
    A("")
    A("| definition | coverage % [95% CI] | without the verbatim Homeric verses | without tokens unattested in Homer | shuffled % | excess (pp) | Homeric verse v. rest of Homer % | reference v. the 'without verbatim' interval | v3 coverage % |")
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
      f"({', '.join(map(str, dens['verbatim_verse_numbers']))}); v3: {dens1['verses_identical_to_a_homeric_verse']} of {dens1['verses']}. "
      f"The 'without' column drops them ({x0['verses']} verses, {x0['tokens']} tokens). {dens['tokens_unattested_in_homer']} tokens "
      "are forms unattested in Homer (section 9) and can never be covered.")
    A(f"* **Lines with at least one ATTESTED-EXACT formula of 2 or more words**: {dens['lines_with_claimed_exact_formula_ge2_words']} of "
      f"{dens['verses']} = **{dens['lines_with_claimed_exact_formula_ge2_words_pct']}%** (claimed strings found verbatim at a Homeric "
      f"position, poem_density.py; v3 {dens1['lines_with_claimed_exact_formula_ge2_words_pct']}%); by the reviewer's classes (entries "
      f"classed E with 2 or more words): {len(exact2_lines)} of {len(recs)}. Counting only formulas not made of function words alone: "
      f"**{dens['lines_with_claimed_exact_formula_ge2_words_not_function_only_pct']}%** (none in "
      f"{', '.join(map(str, dens['lines_without_claimed_exact_formula_ge2_words_not_function_only'])) or '-'}; v3 "
      f"{dens1['lines_with_claimed_exact_formula_ge2_words_not_function_only_pct']}%, none in "
      f"{', '.join(map(str, dens1['lines_without_claimed_exact_formula_ge2_words_not_function_only']))} in the v3 numbering). Unclaimed included, any "
      f"attested non-function-word n-gram at a Homeric position: {dens['lines_with_any_attested_ngram_at_homeric_position_pct']}% (none "
      f"in {', '.join(map(str, dens['lines_without_any_attested_ngram_at_homeric_position'])) or '-'}).")
    below = [k for k in D if ref[k] < D[k]["excluding_verbatim_verses"]["ci95"][0]]
    inside = [k for k in D if D[k]["excluding_verbatim_verses"]["ci95"][0] <= ref[k] <= D[k]["excluding_verbatim_verses"]["ci95"][1]]
    A(f"* Reading (exploratory; {dens['verses']} verses): with every verse counted the poem's coverage is above the Homeric reference on "
      f"every definition. Without the copied verses the reference lies inside the poem's 95% interval for {', '.join(inside) or 'none'} and "
      f"below it for {', '.join(below) or 'none'}. As in v1-v3, this measures reuse of attested wording by a composer working from the "
      "concordance, not oral composition; Homer's own figure includes his repeated verses, as the poem's includes its copied ones.")
    A("")
    A("## 11. Source entries in detail")
    A("")
    A("Columns as v1: composer's status; cited lines containing the string or hits of the recorded query / cited lines; count claimed / "
      "recorded query's hits / hits of the claimed string (`ngram`); the string's Homeric positions (top 4); its position in the verse "
      "if there word for word; reviewer's class and modification; Homeric parallel for that kind of modification ('-' = none needed "
      "or none offered; the record's own parallels are counted in section 8).")
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
    print("lab_bad:", lab_bad, lab_bad2, "par_bad:", par_bad)
    print("new/text/rec:", new_lines, text_changed, rec_changed, dropped_v3)


if __name__ == "__main__":
    main()
