#!/usr/bin/env python3
"""Build composition/final/poem.jsonl from composition/drafts/v4.jsonl: record-only corrections, verse text frozen.

    source .venv/bin/activate
    python -I composition/final/apply_record_corrections.py

The verse text of every record is left untouched (poem.txt is a byte copy of v4.txt). The records are corrected as
the fourth-round reviews ask (review/provenance_v4.md sections 2, 9; review/scansion_v4.md 'Discrepancies' items;
review/philology_v4.md section 5 'Record corrections'), plus stale v3 line numbers found by a scan of every record
for cross-references. Every edit is an explicit old -> new replacement that fails if the old value is not found
exactly once, and every new count, position or citation is re-run through homer/concordance.py's Concordance class
(the code behind the CLI) and asserted before the file is written. The log is composition/final/record_edits.md.
Each record gets `final: true` and `frozen_from: "v4"`; the `revision_note` of an edited record gets a one-sentence
summary of its final edits.
"""
import json
import re
import shutil
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "homer"))
from concordance import Concordance  # noqa: E402

SRC = ROOT / "composition/drafts/v4.jsonl"
SRC_TXT = ROOT / "composition/drafts/v4.txt"
OUT = ROOT / "composition/final/poem.jsonl"
OUT_TXT = ROOT / "composition/final/poem.txt"
LOG = ROOT / "composition/final/record_edits.md"

C = Concordance()
LOG_ROWS = []          # (line, field, kind, source, summary)
QUERIES = {}           # query string -> (total, positions)
TOUCHED = {}           # line -> [summaries]


def run_query(q):
    m = re.match(r'\s*--(ngram|loose|exact|regex)\s+"(.*?)"\s*(.*)$', q)
    kind, s, rest = m.groups()
    word = "--word" in rest
    if kind == "ngram":
        hits = C.ngram(s)
    elif kind == "loose":
        hits = C.loose(s, word=word)
    elif kind == "exact":
        hits = C.exact(s, word=word)
    else:
        hits = C.regex(s)
    pos = Counter(f"{h.pos_start}-{h.pos_end}" for h in hits)
    return hits, dict(pos.most_common())


def verify(q, total, positions=None, cited=None):
    """Assert that query q gives `total` hits, the given position counts and that each cited line is a hit."""
    hits, pos = run_query(q)
    assert len(hits) == total, (q, len(hits), total)
    for p, c in (positions or {}).items():
        assert pos.get(p) == c, (q, p, pos.get(p), c)
    cits = {h.citation: f"{h.pos_start}-{h.pos_end}" for h in hits}
    for c in cited or []:
        assert c in cits, (q, c, "not a hit")
    QUERIES[q] = (len(hits), pos)
    return hits


def get(rec, path):
    o = rec
    for p in path:
        o = o[p]
    return o


def setp(rec, path, val):
    o = rec
    for p in path[:-1]:
        o = o[p]
    o[path[-1]] = val


def pathname(path):
    return ".".join(str(p) for p in path)


def log(n, path, kind, source, summary, detail=None):
    """summary: one short clause for the record's revision_note; detail: the full old -> new for record_edits.md."""
    field = pathname(path) if isinstance(path, tuple) else path
    LOG_ROWS.append((n, field, kind, source, detail or summary))
    TOUCHED.setdefault(n, []).append(summary)


def clip(v, k=160):
    v = v if isinstance(v, str) else repr(v)
    return v if len(v) <= k else v[:k] + "…"


def rep(rec, path, old, new, kind, source, summary=None):
    """Replace the unique occurrence of `old` inside the string at `path`."""
    s = get(rec, path)
    assert isinstance(s, str) and s.count(old) == 1, (rec["n"], pathname(path), old[:60], s.count(old) if isinstance(s, str) else s)
    setp(rec, path, s.replace(old, new))
    field = pathname(path)
    log(rec["n"], path, kind, source, summary or f"{kind} in {field}", f"{summary + ': ' if summary else ''}'{clip(old)}' -> '{clip(new)}'")


def setv(rec, path, old, new, kind, source, summary=None):
    """Set the value at `path`, asserting its current value is `old`."""
    cur = get(rec, path)
    assert cur == old, (rec["n"], pathname(path), cur, old)
    setp(rec, path, new)
    field = pathname(path)
    log(rec["n"], path, kind, source, summary or f"{kind} in {field}", f"{summary + ': ' if summary else ''}{clip(old)} -> {clip(new)}")


def append_note(rec, text, kind, source, summary):
    rec["notes"] = (rec["notes"] + " " if rec.get("notes") else "") + text
    log(rec["n"], ("notes",), kind, source, summary)


def add_source(rec, entry, source, summary):
    rec["sources"].append(entry)
    log(rec["n"], ("sources", len(rec["sources"]) - 1), "new entry", source, summary)


def add_coinage(rec, entry, source, summary):
    rec["coinages"].append(entry)
    log(rec["n"], ("coinages", len(rec["coinages"]) - 1), "new coinage", source, summary)


PROV = "provenance_v4 §9"
SCAN = "scansion_v4 discrepancies"
PHIL = "philology_v4 §5"
STALE = "stale v3 line number (scan of every record; the kind of scansion_v4 item 8)"


def main():
    recs = [json.loads(l) for l in open(SRC, encoding="utf-8") if l.strip()]
    R = {r["n"]: r for r in recs}

    # ---------------------------------------------------------------- 2, 8 (stale cross-references)
    rep(R[2], ("notes",), "ring with lines 59-60 (the end)", "ring with lines 63-64 (the end)", "stale number", STALE)
    rep(R[8], ("facts",), "cf. line 27's parry", "cf. the strokes of 23 and 28, καὶ βάλεν, οὐδ᾽ ἀφάμαρτε (v3 27)", "stale number", STALE)

    # ---------------------------------------------------------------- 20
    r = R[20]
    verify('--loose "εσσυμενως" --word', 12, {"1-3": 6, "7-9": 4, "3-5": 2}, ["Il. 23.511", "Il. 15.698", "Il. 21.610", "Od. 15.288"])
    rep(r, ("sources", 7, "text"), "ἐσσυμένως (12x: 7 line-initial, 3 at 7-9 as here: Il. 15.698, 21.610, 23.511)",
        "ἐσσυμένως (12x: 1-3 6x, 7-9 4x as here: Il. 15.698, 21.610, 23.511, Od. 15.288; 3-5 2x)", "count", f"{PROV} 20/7; {SCAN} item 2")
    setv(r, ("sources", 7, "citation"), "Il. 23.511, 15.698, 21.610", "Il. 23.511, 15.698, 21.610, Od. 15.288", "citation", f"{PROV} 20/7")
    verify('--ngram "ἐσσυμένως λάβ᾽ ἄεθλον"', 1, {"7-12": 1}, ["Il. 23.511"])
    rep(r, ("modifications", 1, "homeric_parallel"), "; the name formula fills 6-12 as in Il. 2.563",
        "; the prize formula fills 7-12, as ἐσσυμένως λάβ᾽ ἄεθλον (Il. 23.511) does (the v3 name formula at 6-12 is gone)",
        "stale note", f"{SCAN} item 2")

    # ---------------------------------------------------------------- 23 (mapping note; the whole-verse repeat parallel)
    verify('--ngram "νεκροὺς πυρκαϊῆς ἐπινήνεον ἀχνύμενοι κῆρ"', 2, {"1-12": 2}, ["Il. 7.428", "Il. 7.431"])
    append_note(R[23], "Final record note: by string this verse is v3 27 verbatim (= v4 28); `v3_line` 23 and `changed` true refer to the "
                "line number, whose v3 verse was withdrawn (revision_note; scansion_v4 item 1). A whole narrative verse repeated within "
                "five lines is Homeric: Il. 7.428 = 7.431 νεκροὺς πυρκαϊῆς ἐπινήνεον ἀχνύμενοι κῆρ (--ngram: 2 hits, both 1-12; "
                "philology_v4 §5).", "note", f"{SCAN} item 1; {PHIL} 23/28", "mapping note; Il. 7.428 = 7.431 cited for 23 = 28")

    # ---------------------------------------------------------------- 24
    r = R[24]
    verify('--ngram "καί οἱ Τεῦκρος"', 3, {"1-3.5": 3}, ["Il. 12.350", "Il. 12.363", "Il. 12.371"])
    verify('--ngram "Τεῦκρος"', 19, {"1-2": 10, "3-3.5": 3, "6-7": 2, "9-9.5": 2, "5-5.5": 2})
    setv(r, ("sources", 1, "text"),
         "Σέρβος (LX at 3-3.5 before a vowel, the final syllable short; a slot allowed by A1: check_line passes with no flags; the shape of a bare name before ἔπειτα, as Ἄδρηστος δ᾽ ἄρ᾽ ἔπειτα Il. 6.45 at 1-5.5)",
         "Σέρβος (LS at 3-3.5 before a vowel, the final syllable short; slot model Τεῦκρος at 3-3.5 before a vowel in καί οἱ Τεῦκρος ἅμα σπέσθω, Il. 12.350 = 12.363 and 12.371, the model of Σέρβον in 48; Τεῦκρος 19x: 1-2 10x, 3-3.5 3x, 5-5.5 2x, 6-7 2x, 9-9.5 2x; a slot allowed by A1: check_line passes with no flags)",
         "citation", f"{PROV} 24/1 [QUERY]", "slot model Il. 6.45 (Ἄδρηστος at 1-3) -> Il. 12.350 (Τεῦκρος at 3-3.5)")
    setv(r, ("sources", 1, "citation"), "Il. 6.45 (δ᾽ ἄρ᾽ ἔπειτα 12x, all 3.5-5.5)", "Il. 12.350, 12.363, 12.371 (Τεῦκρος at 3-3.5 before a vowel)", "citation", f"{PROV} 24/1")
    setv(r, ("sources", 1, "query"), '--ngram "δ᾽ ἄρ᾽ ἔπειτα"', '--ngram "καί οἱ Τεῦκρος"', "query", f"{PROV} 24/1")
    setv(r, ("sources", 1, "count"), 12, 3, "count", f"{PROV} 24/1")
    setv(r, ("sources", 1, "query_hits"), 12, 3, "count", f"{PROV} 24/1")
    verify('--ngram "Ἄδρηστος δ᾽ ἄρ᾽ ἔπειτα"', 1, {"1-5.5": 1}, ["Il. 6.45"])
    verify('--ngram "δ᾽ ἄρ᾽ ἔπειτα"', 12, {"3.5-5.5": 12})
    add_source(r, {"text": "Ἄδρηστος δ᾽ ἄρ᾽ ἔπειτα λαβὼν ἐλίσσετο γούνων (a bare name as subject before ἔπειτα, 1-5.5; δ᾽ ἄρ᾽ ἔπειτα 12x, all 3.5-5.5) → Σέρβος ἔπειτα (3-5.5)",
                   "citation": "Il. 6.45", "position": "1-5.5", "count": 1, "status": "ATTESTED-MODIFIED",
                   "query": '--ngram "Ἄδρηστος δ᾽ ἄρ᾽ ἔπειτα"', "query_hits": 1}, f"{PROV} 24/1",
               "the Il. 6.45 'name before ἔπειτα' model moved out of the COINAGE entry into its own entry")
    verify('--loose "μαχη" --word', 28, {"6-7": 24, "4-5": 3, "8-9": 1}, ["Il. 7.113", "Il. 8.448", "Od. 4.497"])
    setv(r, ("sources", 2, "text"), "μάχῃ (26x; at 6-7, e.g. Il. 7.113, 8.448, Od. 4.497 with the word ending at 7)",
         "μάχῃ (28x: 6-7 24x, as here, e.g. Il. 7.113, 8.448, Od. 4.497 with the word ending at 7; 4-5 3x; 8-9 1x)", "count", f"{PROV} 24/2 [QUERY]")
    setv(r, ("sources", 2, "count"), 26, 28, "count", f"{PROV} 24/2 [QUERY]")
    setv(r, ("sources", 2, "query_hits"), 26, 28, "count", f"{PROV} 24/2")
    verify('--ngram "πύματον"', 8, {"3.5-5": 6, "5.5-7": 2}, ["Il. 23.373", "Il. 23.768"])
    rep(r, ("sources", 3, "text"), "πύματον 8x: 3.5-5 and 5.5-7;", "πύματον 8x: 3.5-5 6x, 5.5-7 2x;", "count", f"{SCAN} item 3")
    rep(r, ("modifications", 2, "homeric_parallel"), "Homer sets πύματον at 3.5-5 (5x) and 5.5-7 (2x)", "Homer sets πύματον at 3.5-5 (6x) and 5.5-7 (2x)", "count", f"{PROV} 24; {SCAN} item 3")
    verify('--loose "πυματη" --word', 1, {"3.5-5": 1}, ["Il. 6.118"])
    verify('--exact "πυμάτῃ"', 0)
    verify('--ngram "πυμάτη"', 1, {"3.5-5": 1}, ["Il. 6.118"])
    setv(r, ("coinages", 0, "form"), "πυμάτῃ (dative feminine; 0 hits)",
         "πυμάτῃ (dative feminine; 0 exact hits; in the concordance's accent- and subscript-blind loose form 1 hit, the nominative πυμάτη of Il. 6.118 at 3.5-5)",
         "coinage", f"{PROV} 24 coinages πυμάτῃ")
    setv(r, ("coinages", 0, "analogical_model"),
         "πυμάτην Il. 18.608, πυμάτῳ Od. 7.138, πύματον 6x; quantities υ short, α short by analogy with the attested forms (check_line warns quantity_unattested, analogy)",
         "the feminine πυμάτη (Il. 6.118 ἄντυξ ἣ πυμάτη θέεν ἀσπίδος ὀμφαλοέσσης, nom., 3.5-5: the closest model, identical to the verse's form in the loose comparison), πυμάτην Il. 18.608, πυμάτῳ Od. 7.138 for the dative, πύματον 8x (3.5-5 6x, 5.5-7 2x); quantities υ short, α short by analogy with the attested forms (check_line warns quantity_unattested, analogy)",
         "coinage", f"{PROV} 24 coinages πυμάτῃ, πύματον 6x -> 8x")
    add_source(r, {"text": "πυμάτη (the attested feminine, nom., 3.5-5: the same form as the verse's πυμάτῃ in the loose comparison) → πυμάτῃ (dat., 7.5-9)",
                   "citation": "Il. 6.118 (ἄντυξ ἣ πυμάτη θέεν ἀσπίδος ὀμφαλοέσσης)", "position": "3.5-5", "count": 1, "status": "ATTESTED-MODIFIED",
                   "query": '--ngram "πυμάτη"', "query_hits": 1}, f"{PROV} 24 coinages πυμάτῃ", "Il. 6.118 πυμάτη cited as the closest model")
    rep(r, ("quantity_notes",), "πύματον (6x)", "πύματον (8x)", "count", f"{SCAN} item 3")
    verify('--ngram "μάχῃ νικῶντες Ἀχαιούς"', 1, {"6-12": 1}, ["Il. 16.79"])
    verify('--regex "(ὁ|ὃ) Τυδεΐδης"', 3, {"4-7": 3}, ["Il. 8.532", "Il. 11.660", "Il. 16.25"])
    add_source(r, {"text": "μάχῃ νικῶντες Ἀχαιούς (νικάω + μάχῃ + the accusative of the beaten: the construction of μάχῃ … μιν ἐνίκα)",
                   "citation": "Il. 16.79", "position": "6-12", "count": 1, "status": "ATTESTED-MODIFIED",
                   "query": '--ngram "μάχῃ νικῶντες Ἀχαιούς"', "query_hits": 1}, f"{PHIL} 24", "Il. 16.79 cited for νικάω + μάχῃ + accusative")
    add_source(r, {"text": "ὃ Τυδεΐδης κρατερὸς Διομήδης (the pronoun ὁ / ὃ with a name in apposition, as ὅ γε Σέρβος)",
                   "citation": "Il. 11.660 (= 16.25), 8.532 (ὁ Τυδεΐδης)", "position": "4-7", "count": 3, "status": "ATTESTED-MODIFIED",
                   "query": '--regex "(ὁ|ὃ) Τυδεΐδης"', "query_hits": 3}, f"{PHIL} 24", "Il. 8.532, 11.660 cited for pronoun + name in apposition")
    rep(r, ("modifications", 0, "homeric_parallel"), "μιν the man beaten, as πάντας ἐνίκα (Il. 23.680)",
        "μιν the man beaten, as πάντας ἐνίκα (Il. 23.680) and μάχῃ νικῶντες Ἀχαιούς (Il. 16.79); ὅ γε + the name in apposition as ὁ Τυδεΐδης κρατερὸς Διομήδης (Il. 8.532) and ὃ Τυδεΐδης (Il. 11.660); Σέρβος at 3-3.5 before a vowel as Τεῦκρος (Il. 12.350)",
        "parallel", f"{PHIL} 24; {PROV} 24/1")

    # ---------------------------------------------------------------- 25, 27, 28 (stale numbers; punctuation; repeat parallel)
    rep(R[25], ("notes",), "is given in line 28", "is given in line 30 (τέτρατον αὖτ᾽ ἔλαβεν)", "stale number", STALE)
    append_note(R[27], "Punctuation: the Perseus text of Il. 23.116 ends with a high stop (·); the verse prints a comma because the "
                "sentence runs on into 28 (philology_v4 §5); the wording is verbatim.", "note", f"{PHIL} 35/27", "punctuation note (· in Il. 23.116, comma here)")
    rep(R[28], ("notes",), "the expanded 35-shot point (lines 25-27) ends here", "the expanded 35-shot point (lines 26-28) ends here", "stale number", STALE)
    append_note(R[28], "23 = 28 verbatim at five lines' distance: Il. 7.428 = 7.431 is Homer's whole narrative verse repeated within "
                "five lines (philology_v4 §5; --ngram: 2 hits).", "note", f"{PHIL} 23/28", "Il. 7.428 = 7.431 cited for the repeat")

    # ---------------------------------------------------------------- 29
    r = R[29]
    verify('--ngram "ἐδάμη"', 2, {"1.5-3": 2}, ["Il. 2.860", "Il. 2.874"])
    setv(r, ("sources", 3, "status"), "ATTESTED-EXACT", "ATTESTED-MODIFIED", "relabel", f"{PROV} 29/3 [QUERY]", "ἐδάμη: mobility (Homer 1.5-3 2x only; verse 3.5-5)")
    setv(r, ("sources", 3, "text"), "ἐδάμη (2x, both 1.5-3; here 3.5-5 after ἀλλὰ καὶ ὧς)",
         "ἐδάμη (2x, both 1.5-3; here 3.5-5 after ἀλλὰ καὶ ὧς: mobility of a single SSL word)", "relabel", f"{PROV} 29/3")
    verify('--ngram "κρατεροῦ"', 3, {"7.5-9": 2, "3.5-5": 1}, ["Il. 8.279", "Il. 21.553", "Od. 8.360"])
    setv(r, ("sources", 5, "status"), "ATTESTED-EXACT", "ATTESTED-MODIFIED", "relabel", f"{PROV} 29/5 [QUERY]", "κρατεροῦ: mobility (Homer 7.5-9 2x, 3.5-5 1x; verse 5.5-7)")
    setv(r, ("sources", 5, "text"), "κρατεροῦ (3x: 3.5-5, 7.5-9; the genitive epithet of Djokovic's κρατερός, as κρατεροῖο in 55)",
         "κρατεροῦ (3x: 7.5-9 2x, 3.5-5 1x; here 5.5-7: mobility; the genitive epithet of Djokovic's κρατερός, as κρατεροῖο in 55)", "relabel", f"{PROV} 29/5")
    verify('--ngram "ὑπ᾽ ἀνδροφόνοιο Λυκούργου"', 1, {"6-12": 1}, ["Il. 6.134"])
    verify('--ngram "Λυκούργου"', 1, {"10-12": 1}, ["Il. 6.134"])
    verify('--ngram "Σκαμάνδρου"', 3, {"10-12": 1, "6-8": 1, "7-9": 1}, ["Il. 5.77"])
    setv(r, ("sources", 6, "text"),
         "Νοβήκου (genitive of Νοβῆκος, SLL at 10-12 after the vowel -ὶ; the SLL genitive closing ὑπὸ χερσὶ + name as Αἰακίδαο closes Il. 2.860)",
         "Νοβήκου (genitive of Νοβῆκος, SLL at 10-12 after the vowel -ὶ; slot model Λυκούργου, the SLL name genitive in -ου at 10-12 after ὑπ᾽ + epithet in θύσθλα χαμαὶ κατέχευαν ὑπ᾽ ἀνδροφόνοιο Λυκούργου, Il. 6.134; the only other capitalised -ου genitives at 10-12 are Ὀλύμπου 3x and Σκαμάνδρου 1x, Il. 5.77)",
         "citation", f"{PROV} 29/6 [QUERY]", "slot model Il. 21.553 / 2.860 (name at 9.5-12 / 9-12) -> Il. 6.134 (Λυκούργου at 10-12)")
    setv(r, ("sources", 6, "citation"), "Il. 21.553 (ὑπὸ κρατεροῦ Ἀχιλῆος: epithet + name genitive after ὑπό)",
         "Il. 6.134 (Λυκούργου at 10-12; Σκαμάνδρου at 10-12 in Il. 5.77)", "citation", f"{PROV} 29/6")
    setv(r, ("sources", 6, "query"), '--ngram "ὑπὸ κρατεροῦ Ἀχιλῆος"', '--ngram "ὑπ᾽ ἀνδροφόνοιο Λυκούργου"', "query", f"{PROV} 29/6")
    verify('--ngram "ὑπὸ κρατεροῦ Ἀχιλῆος"', 1, {"6-12": 1}, ["Il. 21.553"])
    add_source(r, {"text": "ὑπὸ κρατεροῦ Ἀχιλῆος (ὑπό + the epithet κρατεροῦ + a name genitive at the verse end: the function of κρατεροῦ … Νοβήκου; in Homer ὑπό precedes the epithet)",
                   "citation": "Il. 21.553", "position": "6-12", "count": 1, "status": "ATTESTED-MODIFIED",
                   "query": '--ngram "ὑπὸ κρατεροῦ Ἀχιλῆος"', "query_hits": 1}, f"{PROV} 29/6", "Il. 21.553 kept as the function model in its own entry")
    verify('--ngram "ἐμῇς ὑπὸ χερσὶ δαμέντα"', 1, {"6-12": 1}, ["Il. 23.675"])
    add_source(r, {"text": "ἐμῇς ὑπὸ χερσὶ δαμέντα (the beaten boxer of the games, carried out alive: ὑπὸ χερσὶ δαμῆναι of a contest, not a death; ὑπὸ χερσί at 7.5-9.5 as here)",
                   "citation": "Il. 23.675", "position": "6-12", "count": 1, "status": "ATTESTED-MODIFIED",
                   "query": '--ngram "ἐμῇς ὑπὸ χερσὶ δαμέντα"', "query_hits": 1}, f"{PHIL} 29", "Il. 23.675 cited: the contest use of ὑπὸ χερσὶ δαμῆναι")
    verify('--ngram "πολιῆς ἐπὶ θινὶ θαλάσσης"', 2, {"5.5-12": 2}, ["Il. 4.248", "Od. 11.75"])
    verify('--ngram "Ἀθηναίης ἐπὶ γούνασιν ἠϋκόμοιο"', 3, {"2-12": 3}, ["Il. 6.92", "Il. 6.273", "Il. 6.303"])
    add_source(r, {"text": "πολιῆς ἐπὶ θινὶ θαλάσσης (a genitive adjective before the preposition, its noun after it: the order of κρατεροῦ ὑπὸ χερσὶ Νοβήκου)",
                   "citation": "Il. 4.248, Od. 11.75", "position": "5.5-12", "count": 2, "status": "ATTESTED-MODIFIED",
                   "query": '--ngram "πολιῆς ἐπὶ θινὶ θαλάσσης"', "query_hits": 2}, f"{PHIL} 29", "Il. 4.248 cited for the split genitive")
    add_source(r, {"text": "Ἀθηναίης ἐπὶ γούνασιν ἠϋκόμοιο (a genitive name before the preposition, its epithet after it: the split around ὑπὸ χερσί)",
                   "citation": "Il. 6.92 (= 6.273, 6.303)", "position": "2-12", "count": 3, "status": "ATTESTED-MODIFIED",
                   "query": '--ngram "Ἀθηναίης ἐπὶ γούνασιν ἠϋκόμοιο"', "query_hits": 3}, f"{PHIL} 29", "Il. 6.92 cited for the split genitive")
    verify('--ngram "ὑπὸ χερσὶ"', 11, {"3.5-5.5": 9, "7.5-9.5": 2}, ["Il. 11.180", "Il. 16.699", "Od. 18.156", "Od. 24.97", "Il. 2.860", "Il. 16.438", "Il. 3.352", "Il. 23.675"])
    setv(r, ("modifications", 0, "homeric_parallel"),
         "ἀλλ᾽ ἐδάμη ὑπὸ χερσὶ ποδώκεος Αἰακίδαο (Il. 2.860): ἀλλ᾽ → ἀλλὰ καὶ ὧς (Il. 23.516), ποδώκεος Αἰακίδαο → κρατεροῦ … Νοβήκου with the epithet before ὑπό as ὑπὸ κρατεροῦ Ἀχιλῆος (Il. 21.553); ὑπὸ χερσὶ at its attested 7.5-9.5 (Il. 3.352)",
         "ἀλλ᾽ ἐδάμη ὑπὸ χερσὶ ποδώκεος Αἰακίδαο (Il. 2.860): ἀλλ᾽ → ἀλλὰ καὶ ὧς (Il. 23.516), ποδώκεος Αἰακίδαο → κρατεροῦ … Νοβήκου, the epithet set before ὑπὸ χερσί and the name after it. The function (ὑπό + κρατεροῦ + name genitive) is that of ὑπὸ κρατεροῦ Ἀχιλῆος (Il. 21.553), but there ὑπό precedes the epithet; among the 11 Homeric ὑπὸ χερσί lines the agent genitive stands whole, before the phrase (Ἀτρεΐδεω ὑπὸ χερσί Il. 11.180, Πατρόκλου ὑπὸ χερσί Il. 16.699, Τηλεμάχου ὑπὸ χερσὶ Od. 18.156, Αἰγίσθου ὑπὸ χερσὶ Od. 24.97) or after it (Il. 2.860, 16.438), never split around it. The split genitive around a preposition phrase has the parallels πολιῆς ἐπὶ θινὶ θαλάσσης (Il. 4.248) and Ἀθηναίης ἐπὶ γούνασιν ἠϋκόμοιο (Il. 6.92); ὑπὸ χερσὶ at its attested 7.5-9.5 (Il. 3.352, 23.675)",
         "parallel", f"{PROV} 29 modifications; {PHIL} 29", "the Il. 21.553 order corrected; the split genitive given its parallels")
    rep(r, ("modifications", 1, "homeric_parallel"), "ἐδάμη at 3.5-5 (Homer 1.5-3, 2x): a single SSL word moved one foot;",
        "ἐδάμη at 3.5-5 (Homer 1.5-3, 2x) and κρατεροῦ at 5.5-7 (Homer 7.5-9 2x, 3.5-5 1x): single words moved;", "relabel", f"{PROV} 29/3, 29/5")
    setv(r, ("coinages", 0, "analogical_model"),
         "Νοβῆκος (R9/A2: Ionic η, circumflex) declined like δῆμος → δήμου (the accent shifts to acute before a long ultima); SLL at 10-12 after a vowel as Ὀδυσσεύς / Ἀχιλλεύς in that slot (brief 4.2), here the genitive Ἀχιλῆος of Il. 21.553",
         "Νοβῆκος (R9/A2: Ionic η, circumflex) declined like δῆμος → δήμου (the accent shifts to acute before a long ultima: 12 Homeric types / 41 tokens in -η + one consonant + -ου carry the acute, e.g. νήσου, δήμου, σιδήρου, none the circumflex; provenance_v4 §5, review/provenance_v4_extra.json accent_eta_C_ou); SLL at 10-12 after a vowel as Ὀδυσσεύς / Ἀχιλλεύς in that slot (brief 4.2); the slot of a name genitive in -ου after ὑπ᾽ + epithet: Λυκούργου (Il. 6.134, 10-12)",
         "coinage", f"{PROV} 29/6; {PROV} §5 accent")
    rep(r, ("quantity_notes",), "κρατεροῦ -οῦ long at the longum 7 before the hiatus",
        "κρατεροῦ -οῦ long at the longum 7 before the hiatus (licence hiatus_long, attested once for κρατεροῦ: Il. 21.553@9; scansion_v4 item 9, for the paper's licence count)",
        "note", f"{SCAN} item 9")
    append_note(r, "Final record note: Il. 23.675 (ἐμῇς ὑπὸ χερσὶ δαμέντα, the boxer beaten and carried out alive) is the contest use of "
                "ὑπὸ χερσὶ δαμῆναι, which the verse takes (Cunliffe δαμάζω 5 'overpower, get the better of, master'); Il. 2.860 = 2.874 is a "
                "death in both uses, and ὑπὸ χερσί is lethal in 10 of its 11 Homeric lines (philology_v4 §2, §5; provenance_v4 §5), "
                "recorded for the paper.", "note", f"{PHIL} 29", "contest-sense note (Il. 23.675)")

    # ---------------------------------------------------------------- 32
    r = R[32]
    verify('--ngram "ἂψ ἐπόρουσε"', 2, {"3-5.5": 2}, ["Il. 3.379", "Il. 21.33"])
    verify('--ngram "αὐτὰρ ὃ ἂψ ἐπόρουσε"', 2, {"1-5.5": 2}, ["Il. 3.379", "Il. 21.33"])
    verify('--ngram "ἀμφήριστον ἔθηκεν"', 2, {"7-12": 2}, ["Il. 23.382", "Il. 23.527"])
    add_source(r, {"text": "ἂψ ἐπόρουσε", "citation": "Il. 3.379, 21.33 (αὐτὰρ ὃ ἂψ ἐπόρουσε; ἂψ ἐπόρουσε at 3-5.5, as here)",
                   "position": "3-5.5", "count": 2, "status": "ATTESTED-EXACT", "query": '--ngram "ἂψ ἐπόρουσε"', "query_hits": 2},
               f"{PROV} §9 unclaimed 32", "unclaimed ἂψ ἐπόρουσε (2x, 3-5.5) claimed")
    add_source(r, {"text": "αὐτὰρ ὃ ἂψ ἐπόρουσε (the whole first half; the verse adds γ᾽) → αὐτὰρ ὅ γ᾽ ἂψ ἐπόρουσε",
                   "citation": "Il. 3.379 (αὐτὰρ ὃ ἂψ ἐπόρουσε κατακτάμεναι μενεαίνων), 21.33", "position": "1-5.5", "count": 2,
                   "status": "ATTESTED-MODIFIED", "query": '--ngram "αὐτὰρ ὃ ἂψ ἐπόρουσε"', "query_hits": 2},
               f"{PHIL} 32; {PROV} §5", "the closest model of 1-5.5 (Il. 3.379 = 21.33) cited")
    setv(r, ("modifications", 0, "homeric_parallel"),
         "ἐδάμασσε βοὴν ἀγαθὸς Φεδερῆρος (v3) → ἐπόρουσε καὶ ἀμφήριστον ἔθηκεν: the verb of Il. 11.580 (ἐπόρουσε καὶ …) at its slot 3.5-6 with the race formula of Il. 23.382 at its slot 7-12; the subject by pronoun (ὅ γ᾽ = the man subdued in 31), as αὐτὰρ ὅ γ᾽ ἂψ ὤσασκε (Od. 11.599) resumes Sisyphus",
         "ἐδάμασσε βοὴν ἀγαθὸς Φεδερῆρος (v3) → ἐπόρουσε καὶ ἀμφήριστον ἔθηκεν: the closest model of 1-5.5 is αὐτὰρ ὃ ἂψ ἐπόρουσε (Il. 3.379 = 21.33, 1-5.5), with γ᾽ added as in αὐτὰρ ὅ γ᾽ ἂψ ὤσασκε (Od. 11.599); the verb of Il. 11.580 (ἐπόρουσε καὶ …) at its slot 3.5-6 with the race formula of Il. 23.382 at its slot 7-12; the subject by pronoun (ὅ γ᾽ = the man subdued in 31), as Od. 11.599 resumes Sisyphus. ἀμφήριστον ἔθηκεν is unreal in both Homeric uses, κεν-clauses (Il. 23.382 καί νύ κεν ἢ παρέλασσ᾽ ἢ ἀμφήριστον ἔθηκεν; 23.527 τώ κέν μιν παρέλασσ᾽ οὐδ᾽ ἀμφήριστον ἔθηκεν), and actual here (philology_v4 §5)",
         "parallel", f"{PHIL} 32", "αὐτὰρ ὃ ἂψ ἐπόρουσε recorded as the closest model; the unreal → actual shift recorded")

    # ---------------------------------------------------------------- 33
    r = R[33]
    verify('--ngram "τοῖιν δ᾽"', 1, {"1-3": 1}, ["Il. 13.66"])
    verify('--ngram "τοῖιν δέ"', 1, {"1-3": 1}, ["Od. 18.34"])
    verify('--loose "τοιιν" --word', 4, {"5-5.5": 2, "1-2": 2}, ["Il. 11.110", "Il. 13.66", "Il. 23.336", "Od. 18.34"])
    setv(r, ("sources", 0, "text"), "τοῖιν δ᾽ (the dual genitive/dative of the two men, line-initial)",
         "τοῖιν δ᾽ (the dual genitive/dative of the two men, line-initial; the elided form 1x: Il. 13.66; the unelided τοῖϊν δέ opens Od. 18.34, the next entry)", "count", f"{PROV} 33/0 [QUERY]")
    setv(r, ("sources", 0, "citation"), "Il. 13.66 (τοῖιν δ᾽ ἔγνω πρόσθεν Ὀϊλῆος ταχὺς Αἴας); Od. 18.34 τοῖϊν δὲ",
         "Il. 13.66 (τοῖιν δ᾽ ἔγνω πρόσθεν Ὀϊλῆος ταχὺς Αἴας; the unelided τοῖϊν δέ at 1-3 in Od. 18.34 is the next entry)", "citation", f"{PROV} 33/0")
    setv(r, ("sources", 0, "count"), 2, 1, "count", f"{PROV} 33/0 [QUERY]")
    add_source(r, {"text": "τοῖιν δέ (the unelided form, line-initial 1-3) → τοῖιν δ᾽", "citation": "Od. 18.34 (τοῖϊν δὲ ξυνέηχ᾽ ἱερὸν μένος Ἀντινόοιο)",
                   "position": "1-3", "count": 1, "status": "ATTESTED-MODIFIED", "query": '--ngram "τοῖιν δέ"', "query_hits": 1},
               f"{PROV} 33/0", "Od. 18.34 τοῖϊν δέ given its own entry with the query that reproduces it")
    setv(r, ("sources", 1, "citation"), "Il. 13.66, Od. 18.34 (line-initial), 11.110, 23.336",
         "Il. 11.110 (5-5.5), 13.66 (1-2), 23.336 (5-5.5), Od. 18.34 (1-2)", "citation", f"{PROV} 33/1 [QUERY]", "Il./Od. order of the citation corrected")
    setv(r, ("sources", 1, "text"), "τοῖιν (4x: Il. 11.110, 13.66, 23.336, Od. 18.34)", "τοῖιν (4x: Il. 11.110, 13.66, 23.336, Od. 18.34; 1-2 2x as here, 5-5.5 2x)", "citation", f"{PROV} 33/1")
    rep(r, ("sources", 3, "text"), "the verse is Il. 13.85 verbatim with λέλυντο", "the verse keeps the pluperfect λέλυντο of Il. 13.85, whose 3-12 it reproduces verbatim", "stale note", f"{SCAN} item 4")
    verify('--ngram "δ᾽ ἀργαλέῳ"', 2, {"3-5": 2}, ["Il. 15.10", "Il. 16.109"])
    add_source(r, {"text": "δ᾽ ἀργαλέῳ", "citation": "Il. 15.10 (ὃ δ᾽ ἀργαλέῳ ἔχετ᾽ ἄσθματι), 16.109 (both 3-5, as here)", "position": "3-5",
                   "count": 2, "status": "ATTESTED-EXACT", "query": '--ngram "δ᾽ ἀργαλέῳ"', "query_hits": 2},
               f"{PROV} §9 unclaimed 33", "unclaimed δ᾽ ἀργαλέῳ (2x, 3-5) claimed: the particle extends the Il. 13.85 string")
    setv(r, ("quantity_notes",), "ἀργαλέῳ: second α short (check_line warns quantity_unattested); the line is Il. 13.85 verbatim",
         "ἀργαλέῳ: second α short (check_line warns quantity_unattested); the verse reproduces Il. 13.85 verbatim at 3-12, with ἀργαλέῳ at the same position 3-5 (LSSL at 3-5 6x in Homer: scansion_v4)", "stale note", f"{SCAN} item 4")
    setv(r, ("quantity", 0, "basis"), "verbatim Homeric wording (Il. 13.85)", "verbatim Homeric wording at 3-12 (Il. 13.85), ἀργαλέῳ at its position 3-5", "stale note", f"{SCAN} item 4")

    # ---------------------------------------------------------------- 34
    r = R[34]
    verify('--ngram "παρέλασσ᾽"', 2, {"3.5-5": 2}, ["Il. 23.382", "Il. 23.527"])
    verify('--loose "παρελασσε" --word', 0)
    setv(r, ("sources", 1, "status"), "ATTESTED-EXACT", "ATTESTED-MODIFIED", "relabel", f"{PROV} 34/1 [QUERY]", "παρέλασσ᾽ → παρέλασσε (unelided, 0x): modified")
    setv(r, ("sources", 1, "text"), "παρέλασσ᾽ ('drove past', the chariot race; 2x, both 3.5-5, here unelided at 3.5-5.5)",
         "παρέλασσ᾽ ('drove past', the chariot race; 2x, both 3.5-5 and both in a κεν-clause, 'would have driven past') → παρέλασσε (the unelided form, 0x in Homer, written out before the consonant of βοήν at 3.5-5.5; the race verb made factual)", "relabel", f"{PROV} 34/1")
    add_coinage(r, {"form": "παρέλασσε (unelided aorist; 0 hits)",
                    "analogical_model": "the attested elided παρέλασσ᾽ (Il. 23.382, 23.527, 3.5-5) written out before a consonant, as an aorist in -ε stands unelided before βοὴν ἀγαθ- in Il. 5.432 (Αἰνείᾳ δ᾽ ἐπόρουσε βοὴν ἀγαθὸς Διομήδης) and in 14, 31, 41 (ἀφάμαρτε / ἐδάμασσε / ἐπόρουσε ending at 5.5); the form Cunliffe gives (παρελαύνω 1a); first α short as in παρέλασσ᾽"},
                f"{PROV} 34 [QUERY]", "παρέλασσε (0 hits) listed in coinages")
    rep(r, ("modifications", 0, "homeric_parallel"), "as ἐδάμασσε / ἐπόρουσε end at 5.5 before βοήν in 14, 31, 41",
        "as ἀφάμαρτε / ἐδάμασσε / ἐπόρουσε end at 5.5 before βοήν in 14, 31, 41", "note", f"{PROV} 34 modifications (14 has ἀφάμαρτε)")
    verify('--ngram "ὀψὲ δὲ δὴ μετέειπε βοὴν ἀγαθὸς Διομήδης"', 3, {"1-12": 3}, ["Il. 7.399", "Il. 9.31", "Il. 9.696"])
    add_source(r, {"text": "ὀψὲ δὲ δὴ μετέειπε βοὴν ἀγαθὸς Διομήδης (the whole-verse frame: ὀψὲ δὲ δή + an aorist at 3.5-5.5 + the name formula at 6-12, one verb changed) → ὀψὲ δὲ δὴ παρέλασσε βοὴν ἀγαθὸς Φεδερῆρος",
                   "citation": "Il. 7.399 = 9.31 = 9.696", "position": "1-12", "count": 3, "status": "ATTESTED-MODIFIED",
                   "query": '--ngram "ὀψὲ δὲ δὴ μετέειπε βοὴν ἀγαθὸς Διομήδης"', "query_hits": 3}, f"{PHIL} 34", "the whole-verse frame Il. 7.399 = 9.31 = 9.696 cited")
    rep(r, ("modifications", 0, "homeric_parallel"), "the race verb of Il. 23.382 at its slot, the formula of Il. 5.114's shape at 6-12;",
        "the race verb of Il. 23.382 at its slot inside the whole-verse frame ὀψὲ δὲ δὴ μετέειπε βοὴν ἀγαθὸς Διομήδης (Il. 7.399 = 9.31 = 9.696; one verb changed), the formula of Il. 5.114's shape at 6-12;",
        "parallel", f"{PHIL} 34")

    # ---------------------------------------------------------------- 35, 36
    verify('--ngram "λαοὶ δ᾽ ἀμφοτέροισιν ἐπήπυον ἀμφὶς ἀρωγοί"', 1, {"1-12": 1}, ["Il. 18.502"])
    append_note(R[35], "Punctuation: the verse adds a comma after ἐπήπυον, which the Perseus text of Il. 18.502 lacks (philology_v4 §5); the wording is verbatim.",
                "note", f"{PHIL} 35/27", "punctuation note (comma added)")
    r = R[36]
    verify('--ngram "κήρυκες βοόωντες ἐρήτυον"', 1, {"1-8": 1}, ["Il. 2.97"])
    add_source(r, {"text": "κήρυκες βοόωντες ἐρήτυον (the heralds' call for quiet in the assembly, Il. 2.96-98: κήρυκες at 1-3 and ἐρήτυον at 6-8 as here; the closer model for the umpire's 'Please')",
                   "citation": "Il. 2.97 (λαῶν ἱζόντων, ὅμαδος δ᾽ ἦν· ἐννέα δέ σφεας / κήρυκες βοόωντες ἐρήτυον, εἴ ποτ᾽ ἀϋτῆς / σχοίατ᾽, Il. 2.96-98)",
                   "position": "1-8", "count": 1, "status": "ATTESTED-MODIFIED", "query": '--ngram "κήρυκες βοόωντες ἐρήτυον"', "query_hits": 1},
               f"{PHIL} 36", "Il. 2.96-98 cited as the heralds' call for quiet")
    append_note(r, "Final record note (philology_v4 §5): Il. 2.96-98 (κήρυκες βοόωντες ἐρήτυον, εἴ ποτ᾽ ἀϋτῆς / σχοίατ᾽) is the heralds' call for "
                "quiet, closer to the umpire's 'Please' than the trial scene of Il. 18.503 (Cunliffe ἐρητύω 2 'get under control, bring back to "
                "discipline: κήρυκές σφεας Il. 2.97'; ἐρητύω 1 'hold back, restrain' for 18.503).", "note", f"{PHIL} 36", "Il. 2.96-98 note")

    # ---------------------------------------------------------------- 37, 59 (M8 parallel counts; stale numbers in 37 and 59)
    verify('--ngram "ἔνθα δὲ"', 44, {"1-2": 31, "9-10": 8, "3-4": 5}, ["Il. 2.550", "Il. 6.245", "Il. 6.249", "Il. 18.497"])
    verify('--ngram "αἶψα δ᾽"', 41, {"1-2": 31, "9-10": 5, "3-4": 5}, ["Il. 1.387", "Il. 6.514", "Il. 18.532"])
    verify('--ngram "καὶ σάκος"', 4, {"1-2": 2, "9-10": 2}, ["Il. 10.257", "Od. 14.277", "Il. 15.125", "Il. 15.474"])
    verify('--ngram "καὶ βάλεν"', 11, {"1-2": 11})
    for n in (37, 59):
        rep(R[n], ("modifications", 0, "homeric_parallel"),
            "ἔνθα δὲ at 1-2 (13x, e.g. Il. 2.550) and at 9-10 (Il. 6.245, 6.249, 18.497); αἶψα δ᾽ at 1-2 (17x) and at 9-10 (Il. 1.387, 6.514, 18.532)",
            "ἔνθα δὲ at 1-2 (31x, e.g. Il. 2.550) and at 9-10 (8x: Il. 6.245, 6.249, 18.497 …; 44x in all, 5 at 3-4); αἶψα δ᾽ at 1-2 (31x) and at 9-10 (5x: Il. 1.387, 6.514, 18.532 …; 41x in all, 5 at 3-4)",
            "count", f"{PROV} 37/59 modifications (undercounts)")
    r = R[37]
    rep(r, ("notes",), "(here it was read against line 27)", "(here it was read against line 28, v3 27)", "stale number", STALE)
    rep(r, ("notes",), "the next verse (34, verbatim v2) opens a new sentence", "the next verse (38) opens a new sentence", "stale number", STALE)
    rep(r, ("quantity_notes",), "as before κέρδεα in 27", "as before κέρδεα in 23 and 28", "stale number", STALE)
    r = R[59]
    setv(r, ("name_formula",), "Djokovic: Νοβῆκος (SLX at 6-8 after a vowel-final word, before a consonant; shape 3; the Ῥογῆρος slot of 27 and 33: one system, two names)",
         "Djokovic: Νοβῆκος (SLX at 6-8 after a vowel-final word, before a consonant; shape 3; the Ῥογῆρος slot of 23, 28 and 37: one system, two names)", "stale number", f"{SCAN} item 8")
    rep(r, ("notes",), "the line is the system of 33 with the other name", "the line is the system of 37 with the other name", "stale number", f"{SCAN} item 8")
    rep(r, ("notes",), "the next verse (56) opens a new sentence", "the next verse (60) opens a new sentence", "stale number", f"{SCAN} item 8")

    # ---------------------------------------------------------------- 38
    verify('--ngram "καί νύ κεν ἔνθ᾽"', 3, {"1-3": 2, "3-5": 1}, ["Il. 5.311", "Il. 5.388", "Il. 8.90"])
    setv(R[38], ("sources", 0, "text"), "καί νύ κεν ἔνθ᾽", "καί νύ κεν ἔνθ᾽ (3x: 1-3 2x, as here; Il. 8.90 at 3-5)", "count", f"{PROV} 38/0")
    setv(R[38], ("sources", 0, "citation"), "Il. 5.311 (καί νύ κεν ἔνθ᾽ ἀπόλοιτο ἄναξ ἀνδρῶν Αἰνείας), 5.388, 8.90",
         "Il. 5.311 (καί νύ κεν ἔνθ᾽ ἀπόλοιτο ἄναξ ἀνδρῶν Αἰνείας), 5.388 (1-3), 8.90 (3-5)", "citation", f"{PROV} 38/0")

    # ---------------------------------------------------------------- 40 (citation text read as 'Il. 5.5' by the citation parser)
    setv(R[40], ("sources", 3, "citation"), "Il. 14.403, 22.290 (καὶ βάλε Πηλεΐδαο μέσον σάκος οὐδ᾽ ἀφάμαρτε); 11.350, 13.160 at 3-5.5",
         "Il. 14.403, 22.290 (verse-final, as here; καὶ βάλε Πηλεΐδαο μέσον σάκος οὐδ᾽ ἀφάμαρτε); 11.350, 13.160 (third foot)", "citation",
         "provenance_v4 §2 (parser artefact 'Il. 5.5')", "the position '3-5.5' moved into a parenthesis so that no citation parser reads it as Il. 5.5")

    # ---------------------------------------------------------------- 41, 42 (ἔπειτα reading; stale numbers)
    verify('--ngram "τρὶς μὲν ἔπειτ᾽ ἐπόρουσε"', 3, {"1-5.5": 3}, ["Il. 5.436", "Il. 16.784", "Il. 20.445"])
    r = R[41]
    rep(r, ("notes",), "names the attacker before ἀλλ᾽ ὅτε δὴ τὸ τέταρτον (37), the Homeric sequence", "names the attacker before ἀλλ᾽ ὅτε δὴ τὸ τέταρτον (42), the Homeric sequence", "stale number", STALE)
    rep(r, ("notes",), "so the unexpressed subject of 37 is Federer", "so the unexpressed subject of 42 is Federer", "stale number", STALE)
    rep(r, ("notes",), "because a name after ἐπέσσυτο in 37 does not scan", "because a name after ἐπέσσυτο in 42 does not scan", "stale number", STALE)
    rep(r, ("notes",), "and 37 must keep the formula", "and 42 must keep the formula", "stale number", STALE)
    rep(r, ("commentary_equivalent",), "the fourth-time climax is 37", "the fourth-time climax is 42", "stale number", STALE)
    append_note(r, "Final record note (philology_v4 §2, §5): the count rests on the resumptive ἔπειτα (Cunliffe ἔπειτα 'resuming and restating, "
                "then: ἐπόρουσε … τρὶς ἔπειτα ἐπόρουσεν Il. 5.436; cf. 20.445'): τρίς = points 359 (CP1, 38-39), 360 (CP2, 40) and 361, and the "
                "fourth (42) = point 362, the break for 8-8 (corpus/timing/points_2019wimF.csv). On the alternative 'thereafter' reading (three "
                "attacks after the CP2 of 40) the fourth would be point 364, two points late, because CP2 is narrated before the count. Each "
                "Homeric τρὶς μὲν ἔπειτ᾽ ἐπόρουσε has a τρὶς δέ limb in the next verse (Il. 5.437, 16.785, 20.446); 41 → 42 contracts it, as "
                "Il. 13.20 has τρὶς μέν and τὸ δὲ τέτρατον in one verse (the only Homeric τρὶς μέν without a τρὶς δέ).", "note", f"{PHIL} 41-42", "the ἔπειτα reading and its caveat recorded")
    rep(R[42], ("notes",), "fixed by the τρὶς μέν count naming him in 36 (R12)", "fixed by the τρὶς μέν count naming him in 41 (R12; the count's resumptive ἔπειτα and the alternative reading are noted at 41)", "stale number", STALE)

    # ---------------------------------------------------------------- 43-48 (stale numbers)
    rep(R[43], ("notes",), "Il. 5.136-143 (lines 39-42) and closed by the ὣς-apodosis of line 43", "Il. 5.136-143 (lines 44-47) and closed by the ὣς-apodosis of line 48", "stale number", STALE)
    rep(R[44], ("notes",), "lines 39-42 = Il. 5.137-139, 5.142 verbatim", "lines 44-47 = Il. 5.137-139, 5.142 verbatim", "stale number", STALE)
    rep(R[45], ("notes",), "the relative clause of 39-40 is complete", "the relative clause of 44-45 is complete", "stale number", STALE)
    rep(R[47], ("facts",), "as line 41;", "as line 46;", "stale number", STALE)
    rep(R[47], ("notes",), "(see 39)", "(see 44)", "stale number", STALE)
    rep(R[48], ("commentary_equivalent",), "the lead at 9-8 follows in 44", "the lead at 9-8 follows in 49", "stale number", STALE)

    # ---------------------------------------------------------------- 49
    r = R[49]
    verify('--ngram "ἔκφερ᾽"', 3, {"3-3.5": 1, "1-1.5": 1, "9-9.5": 1}, ["Il. 23.259", "Il. 23.759", "Il. 23.785"])
    verify('--ngram "ἔκφερεν"', 1, {"1-2": 1}, ["Od. 15.470"])
    setv(r, ("sources", 2, "status"), "ATTESTED-EXACT", "ATTESTED-MODIFIED", "relabel", f"{PROV} 49/2 [QUERY]", "ἔκφερ᾽: parallel only, the verse has ἔκφερεν")
    setv(r, ("sources", 2, "text"), "ἔκφερ᾽ (3x: 1-1.5 Il. 23.759 ἔκφερ᾽ Ὀϊλιάδης, 3-3.5 Il. 23.259 νηῶν δ᾽ ἔκφερ᾽ ἄεθλα, 9-9.5 Il. 23.785 ἔκφερ᾽ ἄεθλον)",
         "ἔκφερ᾽ (the elided form, 3x: 1-1.5 Il. 23.759 ἔκφερ᾽ Ὀϊλιάδης, 3-3.5 Il. 23.259 νηῶν δ᾽ ἔκφερ᾽ ἄεθλα, 9-9.5 Il. 23.785 ἔκφερ᾽ ἄεθλον: the slot parallel at 3 for the verse's unelided ἔκφερεν at 3-4) → ἔκφερεν (parallel only; the unelided form is entry 1)", "relabel", f"{PROV} 49/2")
    verify('--ngram "τυτθὸν ὑπεκπροθέοντα"', 1, {"1-5.5": 1}, ["Il. 21.604"])
    verify('--ngram "ὃ δ᾽ ἐπέσσυτο ποσσὶ διώκειν"', 1, {"5.5-12": 1}, ["Il. 21.601"])
    add_source(r, {"text": "τυτθὸν ὑπεκπροθέοντα (the pursued man keeping a little ahead: the pursuit with the 'little' margin, Il. 21.601-604, after ὃ δ᾽ ἐπέσσυτο ποσσὶ διώκειν)",
                   "citation": "Il. 21.604", "position": "1-5.5", "count": 1, "status": "ATTESTED-MODIFIED",
                   "query": '--ngram "τυτθὸν ὑπεκπροθέοντα"', "query_hits": 1}, f"{PHIL} 49", "Il. 21.601-604 cited for the pursuer and the little margin")
    append_note(r, "Final record note (philology_v4 §2, §5): τυτθὸν ὀπίσσω in Il. 5.443 means 'backwards' (Cunliffe ὀπίσσω 1 'of direction, "
                "backwards, back: ἀνεχάζετο τυτθὸν ὀπίσσω'); here it means 'behind' (ὀπίσσω 2 'of place, behind, in rear', Il. 9.507), a shift of "
                "sense recorded for the paper. The pursuit with a 'little' margin is Il. 21.601-604 (ὃ δ᾽ ἐπέσσυτο ποσσὶ διώκειν … τυτθὸν "
                "ὑπεκπροθέοντα; Cunliffe τυτθός 2e 'keeping always a little ahead'). Licence: the hiatus after αὖ at the longum 5 rests on one "
                "Homeric attestation (Il. 3.383@3; scansion_v4 item 9, for the paper's licence count).", "note", f"{PHIL} 49; {SCAN} item 9", "sense-shift note; Il. 21.601-604; single-attestation licence")

    # ---------------------------------------------------------------- 50, 51 (stale notes after the drop of v3 47)
    setv(R[50], ("notes",), "simile E (brief 2.5), now four lines 45-48: Il. 22.162-164 verbatim and the ὣς-apodosis of 22.165 adapted (the philology FAIL on v1 42-43)",
         "simile E (brief 2.5), now three lines 50-52: Il. 22.162-163 verbatim (50-51) and the ὣς-apodosis of 22.165 adapted (52); the third verse of v3 (Il. 22.164 ἢ τρίπος ἠὲ γυνὴ ἀνδρὸς κατατεθνηῶτος, v3 47) was dropped in v4 (critic M5, death register), so the simile has two verses before its apodosis (philology_v4 §2: the brief's minimum of two extended similes still holds); the philology FAIL on v1 42-43 is resolved",
         "stale note", f"{SCAN} item 7")
    setv(R[51], ("facts",), "as line 45; the 12-12 tie-break rule, first used in a men's final (MF E1-E2)", "as line 50; the 12-12 tie-break rule, first used in a men's final (MF E1-E2)", "stale number", STALE)
    setv(R[51], ("notes",), "tier-1 licence (lengthening before μέγα) is the attested line's own (Il. 22.163); the verse-final stop of v1 removed: ἄεθλον's apposition (ἢ τρίπος …) follows as in Il. 22.164, and the ὡς δ᾽ ὅτε period is still open (necessary)",
         "tier-1 licence (lengthening before μέγα) is the attested line's own (Il. 22.163); the verse-final stop of v1 was removed in v2 because ἄεθλον's apposition (ἢ τρίπος …, Il. 22.164) followed; that verse (v3 47) was dropped in v4, so 51 now stands directly before the apodosis 52 with no stop at the verse end (the text is frozen as v4); Homer prints a comma, a high stop or a full stop before a simile apodosis in all cases but Od. 9.393-394, so a high stop after ἄεθλον would be the Homeric practice (philology_v4 §5 print suggestion, recorded, not applied); the ὡς δ᾽ ὅτε period is still open (necessary)",
         "stale note", f"{SCAN} item 7; {PHIL} 51 print suggestion")

    # ---------------------------------------------------------------- 53, 57 (stale numbers)
    rep(R[53], ("notes",), "lines 49-52, Il. 8.69-72", "lines 53-56, Il. 8.69-72", "stale number", STALE)
    rep(R[57], ("notes",), "the 12-12 tie-break expanded (lines 49-57,", "the 12-12 tie-break expanded (lines 53-61,", "stale number", STALE)

    # ---------------------------------------------------------------- 54
    r = R[54]
    verify('--ngram "δύο κῆρε"', 2, {"3.5-5.5": 2}, ["Il. 8.70", "Il. 22.210"])
    verify('--ngram "θαλερῶν αἰζηῶν"', 2, {"7.5-12": 2}, ["Il. 10.259", "Il. 14.4"])
    setv(r, ("gloss",), "and set in them two fates of the fight of two sturdy men,", "and set in them two fates of the fight of lusty men,", "gloss", f"{PHIL} 54",
         "gloss: θαλερῶν αἰζηῶν is plural and generic, δύο goes with κῆρε")
    append_note(r, "Final record note (philology_v4 §2, §5): κῆρε is documented, not removed. Cunliffe κήρ 3 'figured as a weight put in the "
                "balance and typifying death or one's fate: ἐν δὲ τίθει δύο κῆρε θανάτοιο Il. 8.70 = 22.210'; LSJ κήρ II 'doom, death … rarely "
                "without personal sense in Hom.': in Homer κήρ is always doom, and with μάχης the two κῆρε read as the two fates of the fight, "
                "as in Il. 8.73-74 the losers' κῆρες sit down on the earth and the army is routed, not killed; the residual death colour is "
                "recorded for the paper (the critic's own test line kept κῆρε). θαλερῶν αἰζηῶν is plural and generic ('lusty men': Cunliffe "
                "αἰζηός 'in full bodily strength, lusty', θαλερός 1 'lusty, in prime of vigour'), not 'two sturdy men': δύο goes with κῆρε "
                "(gloss corrected).", "note", f"{PHIL} 54", "κῆρε documented (Cunliffe κήρ 3, LSJ κήρ II)")

    # ---------------------------------------------------------------- 55
    r = R[55]
    verify('--ngram "τὴν δ᾽ Ἕκτορος"', 1, {"6-8": 1}, ["Il. 22.211"])
    verify('--ngram "τὴν δ᾽"', 130, {"1-2": 61, "1-1.5": 57, "6-7": 5}, ["Il. 14.168", "Il. 22.211", "Od. 3.11", "Od. 5.58", "Od. 16.357"])
    setv(r, ("sources", 9, "status"), "ATTESTED-EXACT", "ATTESTED-MODIFIED", "relabel", f"{PROV} 55/9 [FAIL]", "τὴν δ᾽ Ἕκτορος ἱπποδάμοιο is not in the verse: modified (only τὴν δ᾽ is, 6-7)")
    setv(r, ("sources", 9, "text"), "τὴν δ᾽ Ἕκτορος ἱπποδάμοιο (τὴν δ᾽ at 6 in the model line itself; τὴν δ᾽ 130x: 5 at 7)",
         "τὴν δ᾽ Ἕκτορος ἱπποδάμοιο (τὴν δ᾽ at 6-7 in the model line itself, as here; Ἕκτορος ἱπποδάμοιο replaced, αὖ added) → τὴν δ᾽ αὖ Σέρβου κρατεροῖο", "relabel", f"{PROV} 55/9")
    setv(r, ("sources", 9, "position"), "6-8", "6-12", "position", f"{PROV} 55/9")
    add_source(r, {"text": "τὴν δ᾽ (at 6-7, as in the model line Il. 22.211; 130x in all: 1-2 61x, 1-1.5 57x, 6-7 5x)",
                   "citation": "Il. 22.211, 14.168, Od. 3.11, 5.58, 16.357 (the five at 6-7)", "position": "6-7", "count": 130, "status": "ATTESTED-EXACT",
                   "query": '--ngram "τὴν δ᾽"', "query_hits": 130}, f"{PROV} 55/9", "τὴν δ᾽ at 6-7 (5x, Il. 22.211) given its own exact entry")
    verify('--ngram "* δ᾽ αὖ"', 110, {"6-7": 4}, ["Il. 6.462", "Il. 8.324", "Il. 23.724", "Il. 24.732"])
    verify('--ngram "δ᾽ αὖ"', 110, {"7-7": 6, "2-2": 68, "3-3": 28, "5-5": 5, "1.5-1.5": 3})
    rep(r, ("modifications", 1, "homeric_parallel"), "pronoun + δ᾽ αὖ at 6-7 is Homeric 6x (Il. 8.324 τὸν δ᾽ αὖ κορυθαίολος Ἕκτωρ)",
        "a one-syllable word + δ᾽ αὖ at 6-7 is Homeric 4x (Il. 8.324 τὸν δ᾽ αὖ κορυθαίολος Ἕκτωρ, 6.462 σοὶ δ᾽ αὖ, 23.724 τὰ δ᾽ αὖ, 24.732 σὺ δ᾽ αὖ; δ᾽ αὖ at 7 6x in all: --ngram \"* δ᾽ αὖ\")",
        "count", f"{PROV} 55 modifications (6x -> 4x, the round-3 correction)")

    # ---------------------------------------------------------------- 56
    r = R[56]
    verify('--loose "εελδωρ" --word', 10, {"10-12": 9, "6-8": 1}, ["Od. 23.54", "Od. 21.200", "Il. 15.74"])
    setv(r, ("sources", 4, "text"), "ἐέλδωρ (10x, all verse-final 10-12: τόδε μοι κρήηνον ἐέλδωρ)",
         "ἐέλδωρ (10x: 9 verse-final at 10-12, as here, e.g. τόδε μοι κρήηνον ἐέλδωρ; 1 at 6-8, Od. 23.54)", "count", f"{PROV} 56/4; {SCAN} item 5")
    setv(r, ("sources", 4, "citation"), "Il. 1.41, 1.455, 1.504, 8.242, 15.74, 16.238, Od. 3.418, 17.242",
         "Il. 1.41, 1.455, 1.504, 8.242, 15.74, 16.238, Od. 3.418, 17.242, 21.200 (10-12), 23.54 (6-8)", "citation", f"{PROV} 56/4")
    verify('--ngram "τότ᾽"', 105, {"9.5-9.5": 9}, ["Il. 5.502", "Il. 6.314", "Il. 9.131"])
    setv(r, ("sources", 6, "text"), "τότ᾽ (at 9.5 before a vowel: Il. 5.502, 6.314, 9.131)",
         "τότ᾽ (105x; 9 at 9.5 before a vowel, as here: Il. 5.502, 6.314, 9.131, 9.273, 14.287, 15.636, Od. 4.98, 5.306, 21.99)", "count", f"{PROV} 56/6 [QUERY]")
    setv(r, ("sources", 6, "count"), 3, 105, "count", f"{PROV} 56/6 [QUERY]", "count 3 (the 9.5 subset) -> 105 (the query's total; 9 at 9.5 stated in the text)")
    setv(r, ("sources", 6, "query_hits"), 3, 105, "count", f"{PROV} 56/6")
    verify('--loose "ατρειδης" --word', 83, {"7-9": 5}, ["Il. 14.29", "Il. 14.380", "Il. 17.580", "Od. 4.185", "Od. 14.470"])
    verify('--ngram "ἀντιθέου"', 3, {"7-9": 1, "1-3": 2}, ["Od. 20.369"])
    setv(r, ("sources", 7, "text"), "Ἑλβετίου (gen., LSSL at 7-9 after δ᾽; model Ἀτρεΐδης at 7-9, Il. 14.29; ἀντιθέου Od. 20.369)",
         "Ἑλβετίου (gen., LSSL at 7-9 after δ᾽; model Ἀτρεΐδης at 7-9, Il. 14.29: 5 of its 83 occurrences stand at 7-9; the genitive model ἀντιθέου at 7-9 is the next entry)", "count", f"{PROV} 56/7 [QUERY]")
    setv(r, ("sources", 7, "citation"), "Il. 14.29 (5x), Od. 20.369", "Il. 14.29, 14.380, 17.580, Od. 4.185, 14.470 (Ἀτρεΐδης at 7-9)", "citation", f"{PROV} 56/7")
    setv(r, ("sources", 7, "count"), 5, 83, "count", f"{PROV} 56/7 [QUERY]", "count 5 (the 7-9 subset) -> 83 (the query's total; 5 at 7-9 stated in the text)")
    setv(r, ("sources", 7, "query_hits"), 5, 83, "count", f"{PROV} 56/7")
    add_source(r, {"text": "Ἑλβετίου (gen.; the genitive LSSL at 7-9 as ἀντιθέου in οἳ δῶμα κάτ᾽ ἀντιθέου Ὀδυσῆος)", "citation": "Od. 20.369 (ἀντιθέου at 7-9; 3x in all, 1-3 2x)",
                   "position": "7-9", "count": 3, "status": "COINAGE", "query": '--ngram "ἀντιθέου"', "query_hits": 3}, f"{PROV} 56/7",
               "the ἀντιθέου (Od. 20.369) model given its own COINAGE entry with the query that reproduces it")
    setv(r, ("coinages", 0, "analogical_model"), "LSSL at 7-9: Ἀτρεΐδης Il. 14.29 (5x), ἀντιθέου Od. 20.369",
         "LSSL at 7-9: Ἀτρεΐδης Il. 14.29 (5 of 83 at 7-9), the genitive ἀντιθέου Od. 20.369", "count", f"{PROV} 56/7")

    # ---------------------------------------------------------------- 58
    r = R[58]
    verify('--ngram "τὸν δ᾽"', 466, {"1-2": 262, "1-1.5": 146, "6-7": 26})
    verify('--ngram "μάλα σχεδὸν ἦλθε διώκων"', 1, {"6-12": 1}, ["Il. 23.499"])
    setv(r, ("sources", 0, "position"), "1-2", "1-1.5", "position", f"{PROV} 58/0", "τὸν δ᾽ stands at 1-1.5 in the verse (scan.py), as in 146 Homeric lines")
    setv(r, ("sources", 0, "text"), "τὸν δ᾽", "τὸν δ᾽ (466x: 1-2 262x, 1-1.5 146x as here, 6-7 26x)", "count", f"{PROV} 58/0")
    setv(r, ("sources", 4, "text"), "μάλα σχεδὸν ἦλθε διώκων", "μάλα σχεδὸν ἦλθε διώκων (in Il. 23.499 of Diomedes, the leader: 'came very near, driving', διώκω absolute; here 'came very near, pursuing him', διώκω with τόν as its object)", "sense", f"{PHIL} 58")
    setv(r, ("notes",), "critic M5 (ἀμύνετο νηλεὲς ἦμαρ, the pitiless day of Il. 11.484 = death) and M6 (names): the chariot-race line Il. 23.499 (Diomedes closing on Eumelus) renders 4-3 with no name, ἕτερος = Federer after 57's Ζοκοβείδης; the drop shot (brief 2.5 B, optional) stays in the facts",
         "critic M5 (ἀμύνετο νηλεὲς ἦμαρ, the pitiless day of Il. 11.484 = death) and M6 (names): the chariot-race line Il. 23.499 renders 4-3 with no name, ἕτερος = Federer after 57's Ζοκοβείδης; the drop shot (brief 2.5 B, optional) stays in the facts. Final record note (philology_v4 §5): the earlier note 'Diomedes closing on Eumelus' misread Il. 23.499: there Diomedes is the leader coming in to win (23.499-513; he had passed Eumelus at 23.382-400) and διώκων is absolute, 'driving' (Cunliffe διώκω 4 'to drive (a chariot) … Absol. Il. 23.344, 424, 499, 547'); the verse uses διώκω in sense 1, 'chase, pursue', with τόν as its object, so the Greek is right in that sense but the sense shifts from the source (recorded for the paper)",
         "sense", f"{PHIL} 58", "the Il. 23.499 misreading corrected (Diomedes leads; διώκων absolute, 'driving')")
    rep(r, ("facts",), "(the pursuer very close behind the leader, Il. 23.499)", "(the pursuer very close behind the leader; the formula of Il. 23.499, where the subject is the leader: see notes)", "sense", f"{PHIL} 58")

    # ---------------------------------------------------------------- 61
    r = R[61]
    verify('--ngram "Ἀχιλεῦ"', 13, {"1.5-3": 9, "5.5-7": 3, "3.5-5": 1}, ["Il. 11.606", "Il. 24.503", "Il. 24.661"])
    verify('--ngram "ἤμβροτες"', 2, {"1-2": 2}, ["Il. 5.287", "Il. 22.279"])
    verify('--ngram "ἔνθ᾽ ἄρα τοι Πάτροκλε"', 1, {"1-5.5": 1}, ["Il. 16.787"])
    verify('--ngram "ἐπέσσυτο δαίμονι ἶσος"', 7, {"6-12": 7}, ["Il. 16.786"])
    setv(r, ("sources", 2, "text"), "Ἀχιλεῦ (the -εῦ vocative SSL at 5.5-7: Il. 11.606, 24.503, 24.661; the slot of Φεδερεῦ)",
         "Ἀχιλεῦ (the -εῦ vocative, 13x: 1.5-3 9x; 5.5-7 3x, Il. 11.606, 24.503, 24.661, the slot of Φεδερεῦ; 3.5-5 1x)", "count", f"{PROV} 61/2 [QUERY]")
    setv(r, ("sources", 2, "count"), 3, 13, "count", f"{PROV} 61/2 [QUERY]", "count 3 (the 5.5-7 subset) -> 13 (the query's total; 3 at 5.5-7 stated in the text)")
    rep(r, ("sources", 3, "text"), "(the narrator's apostrophe in the second person after the fourth-onset line; the apostrophe's form, not its death)",
        "(the narrator's apostrophe in the second person after the fourth-onset line Il. 16.786 ἀλλ᾽ ὅτε δὴ τὸ τέταρτον ἐπέσσυτο δαίμονι ἶσος: the switch from the third person to the second across the verse end, as 60 → 61; the apostrophe's form, not its death)", "note", f"{PHIL} 61")
    append_note(r, "Final record note (philology_v4 §2, §5): the speaker is the narrator, by apostrophe; there is no speech frame, and brief 5.4 "
                "forbids the players speaking. Both Homeric ἤμβροτες are taunts in framed speech by the opponent (Il. 5.286-287 τὸν δ᾽ οὐ "
                "ταρβήσας προσέφη κρατερὸς Διομήδης· / ἤμβροτες οὐδ᾽ ἔτυχες, Diomedes to Pandarus; Il. 22.278-279 Ἕκτωρ δὲ προσέειπεν ἀμύμονα "
                "Πηλεΐωνα· / ἤμβροτες, οὐδ᾽ ἄρα πώ τι, Hector to Achilles); the narrator's use of the taunt formula, turned to sympathy by πολλὰ "
                "μογήσας (cf. Il. 23.607 πολλὰ πάθες καὶ πολλὰ μόγησας, 2nd person), has no Homeric model and is recorded for the paper. The "
                "switch from the third person (60 Ἑλβέτιος) to the second after a comma is Il. 16.786 → 16.787 (ἀλλ᾽ ὅτε δὴ τὸ τέταρτον "
                "ἐπέσσυτο δαίμονι ἶσος, / ἔνθ᾽ ἄρα τοι Πάτροκλε φάνη βιότοιο τελευτή).", "note", f"{PHIL} 61", "narrator-apostrophe note; Il. 16.786-787 for the person switch")

    # ---------------------------------------------------------------- 62
    r = R[62]
    verify('--ngram "Γλαύκῳ δ᾽"', 1, {"1-3": 1}, ["Il. 16.508"])
    verify('--regex "^\\S+ῳ δ[ʼ᾽]"', 27, {"1-3": 20, "1-4": 4, "1-3.5": 3}, ["Il. 16.508"])
    verify('--ngram "τῷ δ᾽"', 148)
    setv(r, ("sources", 0, "text"), "Σέρβῳ δ᾽ (dative of the ethnic, LL at 1-2 as τῷ δ᾽ 148x)",
         "Σέρβῳ δ᾽ (dative of the ethnic, LL at 1-2 before δ᾽; slot model Γλαύκῳ δ᾽ αἰνὸν ἄχος γένετο, Il. 16.508, a dative name LL at 1-2 before δ᾽; a dative in -ῳ at 1-2 + δ᾽ opens 20 Homeric verses: --regex \"^\\S+ῳ δ[ʼ᾽]\" 27 hits, 20 with the dative at 1-2, review/provenance_final_extra.json slot_dat_omega_1_2_before_de 20; slot allowed by A1)",
         "citation", f"{PROV} 62/0 [QUERY]", "slot model τῷ δ᾽ (τῷ at 1 only) -> Γλαύκῳ δ᾽ (Il. 16.508)")
    setv(r, ("sources", 0, "citation"), "Il. 1.250 (τῷ δ᾽ ἤδη δύο μὲν γενεαὶ)", "Il. 16.508 (Γλαύκῳ δ᾽ αἰνὸν ἄχος γένετο φθογγῆς ἀΐοντι)", "citation", f"{PROV} 62/0")
    setv(r, ("sources", 0, "query"), '--ngram "τῷ δ᾽"', '--ngram "Γλαύκῳ δ᾽"', "query", f"{PROV} 62/0")
    setv(r, ("sources", 0, "count"), 148, 1, "count", f"{PROV} 62/0")
    setv(r, ("sources", 0, "query_hits"), 148, 1, "count", f"{PROV} 62/0")
    verify('--ngram "τότε δὴ"', 43, {"1.5-3": 37, "3.5-5": 4, "5.5-7": 2}, ["Il. 10.366", "Il. 23.374", "Il. 1.92", "Il. 8.69", "Od. 9.52"])
    setv(r, ("sources", 2, "text"), "τότε δὴ (43x; at 5.5-7 after a word ending at 5, e.g. Od. 9.52)",
         "τότε δὴ (43x: 1.5-3 37x, 3.5-5 4x, 5.5-7 2x, as here after a word ending at 5: Il. 10.366 φεύγων ἐς νῆας, τότε δὴ μένος ἔμβαλ᾽ Ἀθήνη, 23.374)", "citation", f"{PROV} 62/2; {SCAN} item 6")
    setv(r, ("sources", 2, "citation"), "Il. 1.92, 8.69, Od. 9.52", "Il. 10.366, 23.374 (5.5-7); 1.92, 8.69 (1.5-3); Od. 9.52 (3.5-5)", "citation", f"{PROV} 62/2; {SCAN} item 6", "Od. 9.52 (3.5-5) replaced by the two hits at 5.5-7, Il. 10.366 and 23.374")
    verify('--ngram "δὴ Ζεὺς κῦδος"', 1, {"3-5.5": 1}, ["Il. 12.437"])
    verify('--ngram "ἐπὶ ἶσα μάχη τέτατο πτόλεμός τε"', 2, {"3.5-12": 2}, ["Il. 12.436", "Il. 15.413"])
    add_source(r, {"text": "δὴ Ζεὺς κῦδος (Il. 12.437 πρίν γ᾽ ὅτε δὴ Ζεὺς κῦδος ὑπέρτερον Ἕκτορι δῶκε, at 3-5.5; here 7-9.5: a sense parallel, not a slot; it follows ὣς μὲν τῶν ἐπὶ ἶσα μάχη τέτατο πτόλεμός τε, Il. 12.436, the line used in 21: Homer's own sequence 'level fight, then Zeus gives κῦδος')",
                   "citation": "Il. 12.437 (after 12.436 = 15.413)", "position": "7-9.5", "count": 1, "status": "ATTESTED-MODIFIED",
                   "query": '--ngram "δὴ Ζεὺς κῦδος"', "query_hits": 1}, f"{PROV} §9 unclaimed 62", "unclaimed δὴ Ζεὺς κῦδος (Il. 12.437) claimed as a sense parallel (mobility)")
    verify('--ngram "ἀντιθέῳ"', 11, {"7-9": 5, "3-5": 3, "1-3": 3}, ["Il. 4.377", "Il. 5.629", "Il. 16.649"])
    setv(r, ("quantity", 0, "basis"), "attested by position (Il. 4.377, 5.629 at 3-5); verbatim Homeric word (check_line warns for the form only)",
         "the metre of Il. 4.377, 5.629, 16.649 (ἀντιθέῳ LSSL at 3-5); the ι is in an open syllable, so position plays no part; verbatim Homeric word (check_line warns for the form only)", "note", f"{SCAN} item 6")
    setv(r, ("coinages", 0, "analogical_model"), "Ἕκτορι in καὶ Ἕκτορι κῦδος ἔδωκε (Il. 18.456) for the function; LL at 1-2 as τῷ δ᾽ (Il. 1.250); Σέρβος itself as Ἕκτωρ Πριαμίδης (Il. 8.216, brief 4.2)",
         "Ἕκτορι in καὶ Ἕκτορι κῦδος ἔδωκε (Il. 18.456) for the function; the slot, an LL dative at 1-2 before δ᾽, as Γλαύκῳ δ᾽ (Il. 16.508; 20 Homeric verses open with a dative in -ῳ at 1-2 + δ᾽); τῷ δ᾽ (148x) has τῷ at 1 only, so it shows the function, not the slot; Σέρβος itself as Ἕκτωρ Πριαμίδης (Il. 8.216, brief 4.2)", "coinage", f"{PROV} 62/0")

    # ---------------------------------------------------------------- 63
    setv(R[63], ("enjambment",), "unperiodic", "none", "enjambment", f"{PHIL} 63; philology_v4 §4",
         "enjambment unperiodic -> none: the verse ends with a high stop, the punctuation test applied to every other verse ending in · (the reviewer's poem tally: none 37, unperiodic 18, necessary 9)")
    append_note(R[63], "Final record note: the enjambment label is none (philology_v4 §4, §5: the verse ends with a high stop, so by the punctuation "
                "test used for every other verse ending in · it is none; the composer had unperiodic because μέν … δέ runs on into 64).",
                "note", f"{PHIL} 63", "enjambment note")

    # ---------------------------------------------------------------- 60 (round-3 cross-reference clarified)
    rep(R[60], ("revision_note",), "the 56/1 position field corrected (round 3)", "the position field of entry 1 (round-3 item 56/1 in the v3 numbering, = this line) corrected", "stale number", STALE)

    # ---------------------------------------------------------------- finalise
    for r in recs:
        r["final"] = True
        r["frozen_from"] = "v4"
        if r["n"] in TOUCHED:
            s = ("Final (record only, text frozen as v4): " + "; ".join(dict.fromkeys(TOUCHED[r["n"]]))
                 + " (every edit with its old and new value: composition/final/record_edits.md).")
            r["revision_note"] = (r["revision_note"] + " " if r.get("revision_note") else "") + s
    assert [r["text"] for r in recs] == [l for l in SRC_TXT.read_text(encoding="utf-8").split("\n") if l], "jsonl text != v4.txt"
    OUT.write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in recs), encoding="utf-8")
    shutil.copyfile(SRC_TXT, OUT_TXT)
    assert OUT_TXT.read_bytes() == SRC_TXT.read_bytes()

    # log
    L = ["# Record corrections applied to composition/drafts/v4.jsonl to make composition/final/poem.jsonl", "",
         "Generated by composition/final/apply_record_corrections.py (rerun it to regenerate poem.jsonl and this log). The verse text is "
         "untouched: composition/final/poem.txt is a byte copy of composition/drafts/v4.txt. Sources: review/provenance_v4.md §2 and §9 "
         "(PROV), review/scansion_v4.md 'Discrepancies' (SCAN), review/philology_v4.md §5 'Record corrections' (PHIL), and a scan of every "
         "record for stale v3 line numbers (the kind of scansion_v4 item 8).", "",
         f"Edits: {len(LOG_ROWS)} on {len(TOUCHED)} records. Concordance queries rerun and asserted before writing: {len(QUERIES)}.", "",
         "## Edits", "", "| line | field | kind | source | edit |", "|---|---|---|---|---|"]
    for n, f, k, s, summ in LOG_ROWS:
        L.append(f"| {n} | {f} | {k} | {s} | {summ.replace('|', '\\|')} |")
    L += ["", "## Concordance queries verified (homer/concordance.py, the Concordance class behind the CLI)", "",
          "| query | total | positions |", "|---|---|---|"]
    for q, (t, pos) in QUERIES.items():
        L.append(f"| `{q.replace('|', '\\|')}` | {t} | {', '.join(f'{p} {c}x' for p, c in list(pos.items())[:6])} |")
    LOG.write_text("\n".join(L) + "\n", encoding="utf-8")
    print(f"edits: {len(LOG_ROWS)} on records {sorted(TOUCHED)}; queries verified: {len(QUERIES)}")
    print(f"wrote {OUT} ({len(recs)} records), {OUT_TXT}, {LOG}")


if __name__ == "__main__":
    main()
