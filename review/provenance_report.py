#!/usr/bin/env python3
"""Write review/provenance_v1.md from the machine evidence and the reviewer's recorded judgments.

    source .venv/bin/activate
    python -I review/provenance_check.py composition/drafts/v1.jsonl review/provenance_v1_evidence.json
    python -I review/poem_density.py composition/drafts/v1.jsonl review/poem_density_v1.json
    python -I review/provenance_report.py review/provenance_v1_evidence.json review/poem_density_v1.json \
        composition/drafts/v1.jsonl review/provenance_v1.md

Classification of every `sources` entry (the reviewer's, independent of the composer's `status`):
  ATTESTED-EXACT     the Homeric string occurs word for word (accent-insensitive, as --ngram; a movable nu is
                     ignored and noted) in the verse, the cited lines contain it, and its metrical position in
                     the verse (homer/scan.py) is one at which Homer has it (concordance positions);
  ATTESTED-MODIFIED  the cited lines contain the string, but the verse has it changed: inflection, substitution,
                     expansion, separation, mobility (same words, position not attested in Homer); 'structural
                     model' = the verse keeps the frame but no word of the string;
  NOT-ATTESTED       the cited lines do not contain the string, or the configuration the entry asserts (e.g. a
                     name slot) does not occur in Homer.
The auto rules are applied by `auto_class`; JUDGMENTS records every non-automatic decision with its reason and
the Homeric parallel (each parallel was printed by homer/concordance.py; see the evidence file and the queries
listed in the report).
Line verdicts: FAIL if a cited line does not contain the claimed string, or an entry the composer labels
ATTESTED-EXACT is not exact (strings of >= 2 words), or a coined form is not marked (neither in `coinages` nor
in a COINAGE entry); QUERY if the classification is debatable (single-word entries labelled exact but used at
a position Homer never gives the word; count claims that the recorded query does not reproduce; analogical
slots that Homer does not show; unattested non-name forms; significant unclaimed Homeric phrases);
PASS otherwise.
"""
import json
import re
import sys
from collections import Counter
from pathlib import Path

# (line, source index) -> reviewer's judgment for entries not settled by auto_class, or overriding it.
# cls: E = ATTESTED-EXACT, M = ATTESTED-MODIFIED, N = NOT-ATTESTED.  q: reason for a QUERY (or None).
J = {
 (1, 0): ("M", "inflection: ἄνδρα → dual ἄνδρε; position 1-5.5 kept",
          "ἄνδρε is line-initial 6x (Il. 23.659 = 23.802 ἄνδρε δύω περὶ τῶνδε κελεύομεν, of the two contestants)", None),
 (1, 3): ("M", "inflection: δαΐφρονα → dual δαΐφρονε (form 0x in Homer); slot 6-8 kept",
          "duals of the same declension: δύο γʼ ἄνδρε (Il. 5.303), δύʼ ἀνέρε (Il. 12.421)",
          "δαΐφρονε is unattested (0 hits, --loose δαιφρονε --word): a regular but unattested dual, not listed in `coinages`"),
 (1, 4): ("M", "structural model: Od. 1.1's relative clause at 9-12 replaced by τὼ περὶ νίκης (no shared word)", "-", None),
 (2, 0): ("M", "substitution of the opening word (ἠμὲν → δηρὸν, 1-1.5); 2-12 kept",
          "ἔριδος πέρι θυμοβόροιο takes three different openings (Il. 7.301, 16.476, 20.253)", None),
 (4, 0): ("M", "structural model: two subjects joined by τε (only τε shared)", "-", None),
 (4, 2): ("M", "substitution: coined Ζοκοβεύς in the 3.5-5 slot of Ὀδυσεύς (Il. 10.340, verified 3.5-5)",
          "SSL names alternate at 3.5-5: Ἀχιλεύς (Il. 20.273), Ὀδυσεύς (Il. 10.340)", None),
 (4, 3): ("M", "substitution: Φεδερῆρος for Διομήδης in βοὴν ἀγαθὸς _ (6-12)",
          "βοὴν ἀγαθὸς Μενέλαος 20x and βοὴν ἀγαθὸς Διομήδης 21x, all 6-12", None),
 (5, 0): ("M", "substitution of the first half (1-5.5); ἐδύσετο τεύχεα καλά 6-12 kept",
          "Il. 3.328 and Od. 23.366 share 4-12 with different openings", None),
 (5, 2): ("M", "expansion: δὲ πρῶτος → δʼ ἄρα πρῶτος (ἄρα inserted); δὲ πρῶτος is not in the verse",
          "δʼ ἄρα 334x", None),
 (5, 3): ("M", "substitution: coined Ἑλβέτιος in the 1-3 slot of Πηλεΐδης (Il. 20.164)",
          "LSSL patronymics at 1-3: Ἀτρεΐδ- 101x at 1-3 (--loose ατρειδ)", None),
 (7, 0): ("M", "substitution θώρηκα → χιτῶνα and expansion αὖ → αὖτε; περὶ στήθεσσιν ἔδυνε(ν) kept (Il. 3.332 and 19.371 read ἔδυνεν: movable nu)",
          "the object slot before περὶ στήθεσσι(ν) holds χιτῶνα in Il. 2.416, 16.841", None),
 (7, 3): ("M", "inflection δεύτερος → δεύτερον and mobility (9-12 → 1-3.5)", "δεύτερος αὖτε 1x (Il. 7.248); δεύτερον αὖτε 0x", None),
 (10, 0): ("M", "substitution: coined Σέρβος in the 1-2 slot of Ἕκτωρ (Il. 8.216, verified 1-2)",
           "the 1-2 LL slot before δʼ αὖθʼ ἑτέρωθεν holds Τρῶες (Il. 8.55)", None),
 (10, 3): ("M", "structural model: the second duellist's arming line (no shared word)", "-", None),
 (12, 2): ("M", "substitution: coined Ἑλβέτιος in the 1-3 slot of Πηλεΐδης (Il. 20.164)",
           "Πάτροκλος δὲ πρῶτος ἀκόντισε δουρὶ φαεινῷ (Il. 16.284): the same line with a Homeric name at 1-3", None),
 (14, 2): ("M", "substitution: Φεδερῆρος for Διομήδης in βοὴν ἀγαθὸς _ (6-12)", "βοὴν ἀγαθὸς Μενέλαος 20x, 6-12", None),
 (15, 1): ("M", "substitution ἀλλʼ → ὃ δʼ at 6-7; ἐσσυμένως λάβʼ ἄεθλον 7-12 kept",
           "ἐσσυμένως after δʼ: δʼ ἐσσυμένως 3x (Od. 9.73, 15.288, 16.51); ὃ δʼ ἐσσυμένως 0x", None),
 (19, 2): ("M", "inflection δεύτερος → δεύτερον; position 9-12 kept", "δεύτερος αὖτε 1x (Il. 7.248); adverbial δεύτερον αὖ 5x (1-3)", None),
 (19, 3): ("M", "substitution: coined Ἑλβέτιος in the 3-5 slot of Δαρδανίδης (Il. 3.303, verified 3-5)",
           "Ἀτρεΐδ- 64x at 3-5 (reproduces with --loose ατρειδ)",
           "count 64 is not what the recorded query gives (--loose δαρδανι: 21 hits, 6 at 3-5); 64 = Ἀτρεΐδ- at 3-5"),
 (20, 1): ("M", "substitution οὐδέ → τρὶς δέ (1-1.5); μιν ἐξενάριξε 2-5.5 kept", "-", None),
 (20, 3): ("M", "structural model: name + ἐξενάριξε (shares only ἐξενάριξε); the Homeric line is not in the verse", "-", None),
 (20, 4): ("M", "substitution: Φεδερῆρος for Διομήδης in βοὴν ἀγαθὸς _ (6-12)", "βοὴν ἀγαθὸς Μενέλαος 20x, 6-12", None),
 (22, 0): ("M", "mobility (prosodic): σφαῖραν at 1-2 (final syllable closed before δʼ) v. Homer 1-1.5, 4-5", "-",
           "single word labelled exact at a position Homer does not give it"),
 (22, 2): ("M", "mobility: βάλλον at 6-7; Homer 1-1.5 (4), 1-2 (3), 11-12 (2), 5-5.5 (2)", "-",
           "single word labelled exact at a position Homer does not give it"),
 (22, 4): ("M", "structural model: the ball game of Od. 8.374-376 (no shared word)", "-", None),
 (23, 1): ("M", "substitution: coined Ζοκοβεύς in the 3.5-5 slot of Ὀδυσεύς", "Ἀχιλεύς at 3.5-5 (Il. 20.273)", None),
 (23, 3): ("M", "truncation + mobility: αὖτις dropped, πάλιν alone at 5.5-6 (πάλιν αὖτις is 3.5-5.5 in 4 of 6); cited as a semantic parallel for the pleonasm δεύτερον αὖ … πάλιν",
           "πάλιν alone at 5.5-6 11x", None),
 (24, 0): ("M", "mobility: δίς at 1 (Homer: once, at 4, Od. 9.491 δὶς τόσσον, multiplicative 'twice as much')", "-",
           "single word labelled exact at a position Homer does not give it; iterative 'twice' is not the sense of Homer's only δίς"),
 (24, 1): ("M", "substitution τὸν → δίς before δʼ αὖτʼ (1-2)", "δʼ αὖτʼ after varied monosyllables is common (τὸν δʼ αὖτʼ 28x); δὶς δʼ αὖτʼ 0x", None),
 (24, 3): ("M", "substitution: Φεδερῆρος for Διομήδης in βοὴν ἀγαθὸς _ (6-12)", "βοὴν ἀγαθὸς Μενέλαος 20x, 6-12", None),
 (25, 0): ("M", "inflection δεύτερος → δεύτερον, substitution αὖτʼ → αὖ and Ἀχιλεύς → Φεδερεύς; 5.5-12 kept",
           "both openings attested at 1-3: δεύτερος αὖτʼ 6x, δεύτερον αὖ 5x", None),
 (25, 3): ("M", "substitution: coined Φεδερεύς in the 3.5-5 slot of Ἀχιλεύς (Il. 20.273, verified)", "Ὀδυσεύς at 3.5-5 (Il. 10.340)", None),
 (27, 1): ("N", "ἰσόθεος φώς is exact at 9-12, but the asserted model 'SLL name at 6-8 + ἰσόθεος φώς' does not occur: in all 14 Homeric lines the word before ἰσόθεος φώς is a verb (or μέγα) at 6-8/7-8, never a name; Il. 23.677 has ἀνίστατο there",
           "-", "the name-epithet unit Ῥογῆρος ἰσόθεος φώς has no Homeric analogue (the brief's 4.1 test only shows that it scans)"),
 (28, 0): ("M", "inflection τέτρατος → τέτρατον, substitution ἔλασεν → ἔλαβεν; 1-5 kept", "-", None),
 (28, 2): ("M", "mobility: ἔλαβεν at 3.5-5; Homer 5.5-7 (2), 1.5-3 (1)", "-",
           "single word labelled exact at a position Homer does not give it"),
 (29, 0): ("M", "substitution: coined Σέρβος in the 1-2 slot of Ἕκτωρ", "Τρῶες at 1-2 before δʼ (Il. 8.55)", None),
 (29, 2): ("M", "substitution of the name (Μενέλαον → Φεδερῆρον); βοὴν ἀγαθὸν 6-9 is exact",
           "βοὴν ἀγαθὸν Μενέλαον 5x at 6-12 (claimed 6x)", "count: 5, not 6 (6 = ἀγαθὸν Μενέλαον)"),
 (29, 3): ("M", "inflection + substitution: accusative of βοὴν ἀγαθὸς Φεδερῆρος",
           "βοὴν ἀγαθὸς Μενέλαος 20x / βοὴν ἀγαθὸν Μενέλαον 5x, both 6-12", None),
 (30, 2): ("M", "substitution: Φεδερῆρος for Διομήδης in βοὴν ἀγαθὸς _ (6-12)", "βοὴν ἀγαθὸς Μενέλαος 20x, 6-12", None),
 (31, 1): ("M", "inflection λέλυνται → λέλυντο (the verse is Il. 13.85 verbatim, which has λέλυντο: the entry is a redundant parallel)",
           "φίλα γυῖα λέλυντο in Il. 13.85 itself", None),
 (32, 3): ("M", "substitution: coined Φεδερεύς in the 3.5-5 slot of Ἀχιλεύς", "Ὀδυσεύς at 3.5-5 (Il. 10.340)", None),
 (33, 0): ("M", "substitution of the pronoun ὁ → τό; 6-12 kept",
           "Homer varies it himself: τὸ δʼ ὑπέρπτατο (Il. 13.408, 22.275, Od. 22.280) / ὁ δʼ ὑπέρπτατο (Od. 8.192)", None),
 (33, 2): ("M", "mobility: βάλʼ at 2; Homer 6 (8), 1.5 (5), 9.5 (1)", "-",
           "single word labelled exact at a position Homer does not give it"),
 (33, 3): ("M", "mobility: δίς at 1 (Homer once, at 4, multiplicative)", "-",
           "single word labelled exact at a position Homer does not give it; iterative sense not Homeric for δίς"),
 (33, 4): ("M", "substitution: coined Ἑλβέτιος in the 3-5 slot of Δαρδανίδης (Il. 3.303)", "Ἀτρεΐδ- 64x at 3-5",
           "count 64 not reproduced by the recorded query (--loose δαρδανι: 21)"),
 (34, 1): ("M", "structural model: the 'would have … had not' frame of Il. 3.373-374 (only καί νύ κεν shared)", "-", None),
 (34, 2): ("M", "structural model: Il. 8.91 (shares βοὴν ἀγαθὸς)", "-", None),
 (34, 4): ("M", "substitution: Φεδερῆρος for Διομήδης in βοὴν ἀγαθὸς _ (6-12)", "βοὴν ἀγαθὸς Μενέλαος 20x, 6-12", None),
 (35, 1): ("M", "substitution of the opening ὅττί ῥα → εἰ μὴ ἄρʼ (1-2); οἱ βέλος ὠκὺ ἐτώσιον ἔκφυγε χειρός 3-12 kept",
           "openings vary before a fixed cast half-line: ἀκόντισε δουρὶ φαεινῷ 14x with different first halves (Il. 4.496, 13.183)", None),
 (38, 0): ("M", "substitution Πηλεΐδης δʼ → Σέρβος δʼ αὖθʼ (1-5.5); ἐναντίον ὦρτο λέων ὣς 6-12 kept",
           "both openings Homeric: Πηλεΐδης δʼ ἑτέρωθεν (Il. 20.164), Τρῶες δʼ αὖθʼ ἑτέρωθεν (Il. 8.55)", None),
 (38, 3): ("M", "substitution: coined Σέρβος in the 1-2 slot of Ἕκτωρ", "Τρῶες at 1-2 (Il. 8.55)", None),
 (41, 0): ("M", "substitution throughout: ἔκφερʼ → unelided ἔκφερε (0x), Ὀϊλιάδης → δʼ αὖ Σέρβος, ἐπί → μετά, δῖος Ὀδυσσεύς → ἰσόθεος φώς", "-",
           "ἔκφερε (unelided) is unattested: Homer has only ἔκφερʼ (3x)"),
 (41, 1): ("M", "substitution of the preverb ἐπί → μετά and δῖος → ἰσόθεος; δʼ ὄρνυτο kept (7-8)",
           "δʼ ὄρνυτο 2x, both ἐπὶ δʼ ὄρνυτο (Il. 23.689, 23.759); μετὰ δʼ 13x (8 at 5.5-7)",
           "μετὰ δʼ ὄρνυτο is not Homeric and Homer shows no preverb variation with this tmesis; debatable"),
 (41, 4): ("M", "substitution: coined Σέρβος in the 4-5 slot of Αἴας (Il. 7.206, verified 4-5)", "-", None),
 (46, 0): ("M", "substitution of both genitives in the τὴν μὲν … τὴν δʼ frame (1-12)",
           "the owners of the κῆρες are named differently in Il. 8.71 (Τρώων θʼ ἱπποδάμων καὶ Ἀχαιῶν χαλκοχιτώνων) and 22.211", None),
 (46, 2): ("M", "substitution of the name (Ὀδυσῆος → Ζοκοβῆος) at 7-12", "ἀντιθέου Ὀδυσῆος 2x (7-12, 1-5.5)", None),
 (46, 3): ("M", "structural (shape) model for ἀντιθέου Ζοκοβῆος: no word shared", "-", None),
 (47, 1): ("M", "substitution Ἕκτορος → Ἑλβετίου and αἴσιμον → κακόν; ῥέπε δʼ 5.5-7 kept",
           "Homer re-cuts the formula: ῥέπε δʼ αἴσιμον ἦμαρ Ἀχαιῶν (Il. 8.72) / ῥέπε δʼ Ἕκτορος αἴσιμον ἦμαρ (Il. 22.212); κακὸν ἦμαρ 7x at 9.5-12", None),
 (47, 2): ("M", "substitution αἴσιμον → κακόν, Ἀχαιῶν → Ἑλβετίου (moved to 7-9)", "as (47, 1)", None),
 (48, 2): ("M", "substitution: Ζοκοβίδης for Διομήδης in κρατερὸς _ (7.5-12)",
           "κρατερὸς + other names at 7.5-12: Πολύφημος (2), Διώρης, Λυκόοργος, Πολυποίτης", None),
 (49, 0): ("M", "mobility: ἀμύνετο at 2-4; Homer 6-8 (2/2)", "-",
           "single word labelled exact at a position Homer does not give it (the record's own modification note says so)"),
 (49, 2): ("M", "mobility: δίς at 1 (Homer once, at 4, multiplicative)", "-",
           "single word labelled exact at a position Homer does not give it; iterative sense not Homeric for δίς"),
 (49, 3): ("N", "as (27, 1): no Homeric name stands at 6-8 before ἰσόθεος φώς", "-",
           "the name-epithet unit Ῥογῆρος ἰσόθεος φώς has no Homeric analogue"),
 (50, 0): ("M", "substitution καὶ βάλεν → δὶς δὲ βάλʼ; οὐδʼ ἀφάμαρτε 3-5.5 kept", "καὶ βάλεν, οὐδʼ ἀφάμαρτε 2x; no other opening attested", None),
 (50, 2): ("M", "mobility: αὖτε at 9-9.5, a position Homer never gives it (200 hits: 2-3 107, 5-5.5 50, 11-12 23, 3-3.5 13, 7-7.5 5, 3-4 2)", "-",
           "single word labelled exact at an unattested position"),
 (50, 3): ("M", "substitution: coined Νοβάκος in the 10-12 slot of Ὀδυσσεύς (Il. 1.145, verified 10-12)", "-",
           "the unit περικλυτὸς αὖτε Νοβάκος has no Homeric analogue: περικλυτός (14x, all 6-8) is followed by ἀμφιγυήεις or by punctuation, and αὖτε is never at 9-9.5"),
 (51, 2): ("M", "καὶ βάλε is not in the verse; βάλε δʼ at 5.5-7 (mobility + loss of καί)",
           "βάλε δʼ 3x (5.5-7: Il. 16.737, Od. 24.179; 7.5-9: Il. 15.541)", None),
 (51, 4): ("M", "substitution: Ζοκοβίδης for Διομήδης in κρατερὸς _ (7.5-12)", "κρατερὸς Πολύφημος, Πολυποίτης etc. at 7.5-12", None),
 (52, 0): ("M", "substitution of the opening ὅττί ῥά οἱ → Ἑλβετίου (1-3); 3.5-12 kept", "as (35, 1)", None),
 (52, 2): ("M", "structural (shape) model for Ἑλβετίου at 1-3: no word shared", "ἀντιθέου line-initial 2x (Od. 14.40, 21.254)", None),
 (53, 0): ("M", "substitution: coined Σέρβος in the 1-2 slot of Ἕκτωρ", "-", None),
 (55, 1): ("M", "mobility: τέλος at 3.5-4; Homer 6-7 (17), 7.5-8 (7), 10-11 (2), 2-3, 4-5, 5.5-6 (1 each)", "-",
           "single word labelled exact at a position Homer does not give it"),
 (55, 3): ("M", "substitution ἤδη γὰρ καὶ ἐπήλυθε → τέλος ἦεν, ὅτʼ ἤλυθε (simplex for compound); δείελον ἦμαρ 9-12 kept",
           "ἐπήλυθε 8x, ἤλυθε 11x; ὅτʼ ἤλυθε 0x (Il. 5.803 has ὅτε τʼ ἤλυθε)", None),
}

# QUERY reasons at line level not tied to one entry
LINE_Q = {
 12: "unclaimed: 4-12 δὲ πρῶτος ἀκόντισε δουρὶ φαεινῷ is Il. 16.284 (Πάτροκλος δὲ πρῶτος ἀκόντισε δουρὶ φαεινῷ), i.e. the verse is Il. 16.284 with a name substitution; the record cites only the pieces",
}
CLASSNAME = {"E": "ATTESTED-EXACT", "M": "ATTESTED-MODIFIED", "N": "NOT-ATTESTED"}


def nu_strip(w):
    return w[:-1] if len(w) >= 4 and (w.endswith("εν") or w.endswith("ιν")) else w


def find_seq(words, seq):
    n = len(seq)
    return [i for i in range(len(words) - n + 1) if words[i:i + n] == seq]


def auto_class(src, rec):
    """E/M/N from the evidence alone, with a movable-nu tolerant search; None if undecidable."""
    frs = src["fragments"]
    if not frs:
        return None, ""
    cited_ok = all(c["contains_any_fragment"] or c["in_query_hits"] for c in src["cited_check"]) if src["cited_check"] else False
    if src["status"] == "COINAGE":
        return None, ""
    if len(frs) == 1:
        f = frs[0]
        if f["in_poem_verbatim"]:
            if f["position_attested"]:
                return ("E" if cited_ok else "N"), ""
            return "M", "mobility"
        # movable nu
        hw = [nu_strip(w) for w in f["H_loose"].split()]
        pw = [nu_strip(w) for w in rec["words"]]
        occ = find_seq(pw, hw)
        if occ:
            wp = rec["scan"]["word_positions"]
            i = occ[0]
            pp = f"{wp[i].split('-')[0]}-{wp[i + len(hw) - 1].split('-')[1]}"
            if pp in f["homer_positions"]:
                return "E", f"exact apart from a movable nu (verse {pp})"
            return "M", "mobility (movable nu)"
    return None, ""


def cited_problem(src):
    """True if some cited line contains none of the fragments, is not a hit of the recorded query, and the
    miss is not explained by a movable nu or by a line range."""
    bad = []
    for c in src["cited_check"]:
        if c["contains_any_fragment"] or c["in_query_hits"]:
            continue
        line_words = c["line"]
        ok_nu = False
        if line_words:
            lw = [nu_strip(w) for w in loose_line(line_words)]
            for f in src["fragments"]:
                if find_seq(lw, [nu_strip(w) for w in f["H_loose"].split()]):
                    ok_nu = True
        bad.append((c["citation"], ok_nu))
    return bad


def loose_line(text):
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "homer"))
    import greek as G
    return [G.loose(t.core) for t in G.tokenize(G.nfc(text))]


def esc(s):
    return str(s).replace("|", "\\|")


def main(ev_path, dens_path, jsonl, out):
    ev = json.load(open(ev_path, encoding="utf-8"))
    dens = json.load(open(dens_path, encoding="utf-8"))
    recs = {json.loads(l)["n"]: json.loads(l) for l in open(jsonl, encoding="utf-8") if l.strip()}
    rows, detail = [], []
    tallies = Counter()
    agree = Counter()
    fails, queries = {}, {}
    unclaimed_all = []
    cit_notes = []
    for r in ev:
        n = r["n"]
        rec = recs[n]
        f_reasons, q_reasons = [], []
        ent_summ = []
        for k, s in enumerate(r["sources"]):
            cls, kind = auto_class(s, r)
            par, qr = "-", None
            if (n, k) in J:
                cls, kind, par, qr = J[(n, k)]
            if cls is None:
                raise SystemExit(f"no judgment for line {n} entry {k}: {s['text']}")
            hw = s["fragments"][0]["H_loose"].split() if s["fragments"] else []
            nwords = len(hw)
            tallies[CLASSNAME[cls]] += 1
            comp = s["status"]
            agree[(comp, CLASSNAME[cls])] += 1
            # citation check
            for cit, ok_nu in cited_problem(s):
                rng = re.search(r"\d+\.\d+-\d+", s["citation"] or "")
                cit_notes.append(f"line {n} entry {k} {cit}: " + ("movable nu" if ok_nu else "inside the cited range" if rng else "MISSING"))
                if ok_nu:
                    kind = (kind + "; " if kind else "") + f"{cit}: same string with a movable nu"
                elif rng:
                    kind = (kind + "; " if kind else "") + f"{cit}: inside the cited range, not required to contain a fragment"
                else:
                    f_reasons.append(f"entry {k}: cited {cit} does not contain '{s['fragments'][0]['H']}'")
            if comp == "ATTESTED-EXACT" and cls != "E":
                if nwords >= 2:
                    f_reasons.append(f"entry {k}: '{s['fragments'][0]['H']}' labelled ATTESTED-EXACT but is {CLASSNAME[cls]} ({kind})")
                elif qr is None:
                    q_reasons.append(f"entry {k}: single word '{s['fragments'][0]['H']}' labelled exact: {kind}")
            if comp == "ATTESTED-MODIFIED" and cls == "E":
                q_reasons.append(f"entry {k}: labelled modified but exact")
            if qr:
                q_reasons.append(f"entry {k}: {qr}")
            f0 = s["fragments"][0] if s["fragments"] else {}
            hpos = ", ".join(f"{p} ({c})" for p, c in list(f0.get("homer_positions", {}).items())[:4]) or "-"
            ppos = ", ".join(f0.get("poem_positions") or []) or "-"
            cc = s["cited_check"]
            cit_ok = sum(1 for c in cc if c["contains_any_fragment"] or c["in_query_hits"])
            detail.append(f"| {n} | {k} | {esc(s['text'])} | {comp} | {esc(s['citation'])} | {cit_ok}/{len(cc)} | "
                          f"{s['claimed_count']} / {s['query_total']} / {f0.get('homer_total', '-')} | {esc(hpos)} | {ppos} | "
                          f"**{CLASSNAME[cls]}**{(': ' + esc(kind)) if kind else ''} | {esc(par)} |")
            ent_summ.append(f"{k}:{cls}")
        # coinage marking
        marked = set()
        for c in rec.get("coinages") or []:
            marked.add(loose_line(c["form"].split()[0])[0])
        for s in rec.get("sources", []):
            if s.get("status") == "COINAGE":
                for w in loose_line(re.sub(r"\(.*", "", s["text"])):
                    marked.add(w)
        for w in r["words"]:
            if w in dens["unattested_forms"] and w not in marked:
                if w in ("δαιφρονε", "εκφερε"):
                    continue  # unattested inflected/unelided forms of Homeric words: QUERY via J
                f_reasons.append(f"coined form {w} not marked")
        # unclaimed windows (maximal)
        allw = r["windows"]

        def contained(w):
            return any(x is not w and x["i"] <= w["i"] and x["i"] + x["n"] >= w["i"] + w["n"] and x["n"] > w["n"]
                       for x in allw if not x["claimed"])
        unc = [w for w in allw if not w["claimed"] and not contained(w)]
        for w in unc:
            unclaimed_all.append((n, w))
        if n in LINE_Q:
            q_reasons.append(LINE_Q[n])
        verdict = "FAIL" if f_reasons else ("QUERY" if q_reasons else "PASS")
        if f_reasons:
            fails[n] = f_reasons
        if q_reasons:
            queries[n] = q_reasons
        unc_s = "; ".join(f"{w['ngram']} ({w['count']}x, {w['poem_position']}{'' if w['position_attested'] else ', position not Homeric'})"
                          for w in unc) or "-"
        reasons = " / ".join(f_reasons + q_reasons) or "-"
        rows.append(f"| {n} | {esc(rec['text'])} | **{verdict}** | {' '.join(ent_summ)} | {esc(unc_s)} | {esc(reasons)} |")

    n_cited = sum(len(s["cited_check"]) for r in ev for s in r["sources"])
    verdicts = Counter("FAIL" if n in fails else "QUERY" if n in queries else "PASS" for n in recs)
    D = dens["coverage"]
    ref = dens["homeric_reference_verse_vs_rest_of_homer"]

    def cov(k):
        d = D[k]
        return (f"{d['coverage']} [{d['ci95'][0]}, {d['ci95'][1]}] | {d['excluding_verbatim_verses']['coverage']} "
                f"[{d['excluding_verbatim_verses']['ci95'][0]}, {d['excluding_verbatim_verses']['ci95'][1]}] | "
                f"{d['excluding_tokens_unattested_in_homer']} | {d['shuffled_mean']} [{d['shuffled_2.5_97.5'][0]}, "
                f"{d['shuffled_2.5_97.5'][1]}] | {d['excess_pp']} | {ref[k]} |")

    L = []
    A = L.append
    A("# Provenance review: composition/drafts/v1 (provenance-verifier)")
    A("")
    A("Generated by `review/provenance_report.py` from `review/provenance_v1_evidence.json` (`review/provenance_check.py`) "
      "and `review/poem_density_v1.json` (`review/poem_density.py`); rerun:")
    A("")
    A("```")
    A("source .venv/bin/activate")
    A("python -I review/provenance_check.py composition/drafts/v1.jsonl review/provenance_v1_evidence.json")
    A("python -I review/poem_density.py composition/drafts/v1.jsonl review/poem_density_v1.json")
    A("python -I review/provenance_report.py review/provenance_v1_evidence.json review/poem_density_v1.json composition/drafts/v1.jsonl review/provenance_v1.md")
    A("```")
    A("")
    A("## 1. Method")
    A("")
    A("* Every `sources` entry of the 55 records: the recorded query was rerun through the same `Concordance` methods as "
      "`homer/concordance.py`'s CLI (`--ngram`, `--loose [--word]`); the Homeric string the entry claims was extracted "
      "(text without parenthetical comments, left of an arrow; for COINAGE entries the query = the Homeric model) and run "
      "with `ngram`; every cited line was checked for that string; the verse was scanned with `homer/scan.py --json` and the "
      "string's metrical position in the verse compared with all its Homeric positions.")
    A("* Classes: **ATTESTED-EXACT** = the string is in the verse word for word (accent-insensitive; a movable nu is ignored and "
      "noted), the cited lines contain it, and its position in the verse is one Homer gives it; **ATTESTED-MODIFIED** = the "
      "cited lines contain it but the verse changes it (inflection, substitution, expansion, separation, mobility = same words "
      "at a position Homer never gives them; *structural model* = frame kept, no word kept); **NOT-ATTESTED** = the string is "
      "not in the cited lines, or the entry asserts a configuration Homer does not have (here: a name slot).")
    A("* Verdicts: **FAIL** if a cited line lacks the claimed string, or an entry labelled ATTESTED-EXACT (string of 2 or more "
      "words) is not exact, or a coined form is unmarked. **QUERY** if the classification is debatable: single-word entries "
      "labelled exact but placed where Homer never places the word (a word is not a formula, so this is not a FAIL); counts "
      "that the recorded query does not reproduce; analogical name slots Homer does not show; unattested non-name forms; "
      "significant unclaimed Homeric phrases. **PASS** otherwise. The composer's labels ATTESTED-EXACT / ATTESTED-MODIFIED / "
      "COINAGE are compared with these classes in section 3.")
    A("* Unclaimed phrases: every word window of every verse (2, 3 and longer) was run through `ngram`; windows with Homeric "
      "hits that no entry of the record contains are listed (maximal ones only) in the table and in section 5.")
    A("")
    A("## 2. Summary")
    A("")
    A(f"* Lines: **PASS {verdicts['PASS']}, QUERY {verdicts['QUERY']}, FAIL {verdicts['FAIL']}** (of {len(recs)}).")
    A(f"* Source entries: {sum(tallies.values())}; reviewer's classes: ATTESTED-EXACT {tallies['ATTESTED-EXACT']}, "
      f"ATTESTED-MODIFIED {tallies['ATTESTED-MODIFIED']}, NOT-ATTESTED {tallies['NOT-ATTESTED']}.")
    cc = ev[0].get("cli_crosscheck") or {}
    A(f"* Recorded queries: {cc.get('distinct_queries')} distinct, each rerun with `python homer/concordance.py … --count`; "
      f"mismatches with the in-process rerun: {len(cc.get('mismatches', {})) if cc else 'not run'}.")
    A(f"* Cited lines checked: {n_cited}; lines that neither contain the claimed string nor are hits of the recorded query: "
      + ("; ".join(cit_notes) if cit_notes else "none")
      + ". (Lines 19 and 33 cite Il. 3.303 for the substring query `--loose δαρδανι`; it is a hit of that query.)")
    A("* FAIL lines: " + "; ".join(f"**{n}** ({' / '.join(v)})" for n, v in sorted(fails.items())))
    A("")
    A("* QUERY lines: " + "; ".join(f"**{n}** ({' / '.join(v)})" for n, v in sorted(queries.items()) if n not in fails))
    A("")
    A("## 3. Composer's labels v. reviewer's classes (source entries)")
    A("")
    A("| composer | reviewer | entries |")
    A("|---|---|---|")
    for (c, m), v in sorted(agree.items()):
        A(f"| {c} | {m} | {v} |")
    A("")
    A("COINAGE entries are classified by their Homeric model: ATTESTED-MODIFIED (substitution of the coined name into an "
      "attested slot) when the model line shows the slot, NOT-ATTESTED when it does not (Ῥογῆρος ἰσόθεος φώς, lines 27, 49). "
      "Composer ATTESTED-EXACT entries that are single words used at an unattested position are QUERY, not FAIL.")
    A("")
    mob = [str(n) for n in sorted(recs) for m in (recs[n].get("modifications") or []) if m.get("kind") == "mobility"]
    A("The records' own `modifications` use *mobility* in lines " + ", ".join(mob) + ". Only in line 49 (ἀμύνετο, 6-8 in "
      "Homer, 2-4 in the verse) does a formula or word move to a position Homer does not give it; elsewhere the record means a "
      "half-line recombined with a new first half at the same position (substitution in the terms used here), and in lines 1 "
      "and 20 the item keeps an attested position (no modification). Not a FAIL, but the labels should be corrected.")
    A("")
    A("## 4. Per-line table")
    A("")
    A("Entries: `k:E/M/N` = entry k of the record's `sources`, reviewer's class (details in section 7). Unclaimed = maximal "
      "attested word windows of the verse not contained in any entry (count in Homer, position in the verse).")
    A("")
    A("| n | verse | verdict | entries | unclaimed attested windows | reasons |")
    A("|---|---|---|---|---|---|")
    L.extend(rows)
    A("")
    A("## 5. Unclaimed attested phrases and coinages")
    A("")
    A("Most unclaimed windows only extend a claimed formula by a particle (δʼ αὖθʼ ἑτέρωθεν, δʼ ἄρα, δʼ ἐξενάριξε). The ones "
      "worth adding to the records:")
    A("")
    A("* line 12: δὲ πρῶτος ἀκόντισε δουρὶ φαεινῷ 4-12 = Il. 16.284 `Πάτροκλος δὲ πρῶτος ἀκόντισε δουρὶ φαεινῷ` (the whole "
      "verse is that line with Ἑλβέτιος for Πάτροκλος);")
    A("* line 47: ἕλκε δὲ μέσσα λαβών· ῥέπε δʼ 1-7 = Il. 8.72, 22.212 (the record gives the two halves separately);")
    A("* line 34: κεν ἐξενάριξε 1x, Il. 21.280 at 8-12 (`… ἀγαθὸν δέ κεν ἐξενάριξε`), in the verse at 2-5.5 (mobility);")
    A("* line 1: ἄνδρε is line-initial in Il. 23.659 = 23.802 `ἄνδρε δύω περὶ τῶνδε κελεύομεν, ὥ περ ἀρίστω` (the call for "
      "two contestants), a closer source than the cited Il. 5.303; τὼ περὶ 1x (Il. 16.756 at 1-2; verse 9-10).")
    A("")
    A("Coinages: the forms unattested in Homer (`--loose … --word`, 0 hits) are " + ", ".join(dens["unattested_forms"]) +
      ". None of the coined names exists in Homer, so no claimed coinage is in fact attested. All name coinages are "
      "marked (in `coinages` or as a COINAGE entry; lines 20, 24, 30, 34, 41 mark them only through the COINAGE entry, "
      "with an empty `coinages` list: harmless, but inconsistent). δαΐφρονε (line 1) and ἔκφερε (line 41) are unattested "
      "forms of Homeric words, disclosed in the record's notes but not listed as coinages: QUERY.")
    A("")
    A("## 6. Formulaic density (review/poem_density.py)")
    A("")
    A(f"Greek analogue of analysis/formulas section 1 (held-out design: I = Homer, {len(dens['per_verse'])} verses of M = the poem, "
      f"{dens['tokens']} tokens; tokens and n-grams as `concordance.py --ngram`, within one verse; coverage = share of tokens "
      "inside at least one word n-gram attested in homer/lines.tsv; `base` excludes n-grams made only of function words "
      f"(frozen list of {dens['func_words']} loose forms in the script), the analogue of the STOP filter; `min2` requires 2 "
      "Homeric occurrences, the strict analogue of 'repeated in I'; 95% CI = bootstrap over verses, B = 2000; shuffled = "
      "poem tokens permuted over positions, verse lengths kept, R = 200; Homeric reference = every Homeric verse measured "
      "against the rest of Homer with the same definition, token-weighted).")
    A("")
    A("| definition | coverage % [95% CI] | without the verbatim Homeric verses | without tokens unattested in Homer | shuffled % | excess (pp) | Homeric verse v. rest of Homer % |")
    A("|---|---|---|---|---|---|---|")
    for k in ["n2_all_min1", "n2_base_min1", "n3_all_min1", "n3_base_min1", "n2_base_min2", "n3_base_min2"]:
        A(f"| {k} | " + cov(k))
    A("")
    A(f"* {dens['verses_identical_to_a_homeric_verse']} of {dens['verses']} verses are identical to a Homeric verse "
      f"({', '.join(map(str, dens['verbatim_verse_numbers']))}); the 'without' column drops them "
      f"({D['n2_all_min1']['excluding_verbatim_verses']['verses']} verses, {D['n2_all_min1']['excluding_verbatim_verses']['tokens']} tokens). "
      f"{dens['tokens_unattested_in_homer']} tokens are forms unattested in Homer (the coined names, δαΐφρονε, ἔκφερε) and can never be covered.")
    A(f"* Verses containing at least one claimed formula of 2 or more words found exactly (same words, Homeric position): "
      f"**{dens['lines_with_claimed_exact_formula_ge2_words']} of {dens['verses']} = {dens['lines_with_claimed_exact_formula_ge2_words_pct']}%** "
      f"(none in lines {', '.join(map(str, dens['lines_without_claimed_exact_formula_ge2_words']))}). Counting unclaimed n-grams too "
      f"(any attested n-gram of 2 or more words, not function-word-only, at a Homeric position): "
      f"{dens['lines_with_any_attested_ngram_at_homeric_position_pct']}% (none in lines "
      f"{', '.join(map(str, dens['lines_without_any_attested_ngram_at_homeric_position']))}, whose exact pieces are function-word-only: "
      "ὣς ἄρʼ ὅ γʼ, ἔνθα καὶ ἔνθα, τὴν μὲν ἄρʼ).")
    A("* Reading (exploratory; the poem is 55 verses, so the intervals are wide): with every verse counted the poem's coverage "
      "is above the Homeric reference on every definition. Without the 19 copied verses, the min1 coverages fall to about the "
      "Homeric reference (the reference value lies inside each 95% interval), while the min2 coverages stay above it (the "
      "reference lies below each interval): the composer reuses frequent formulae more than an average Homeric verse does, but "
      "beyond the copied verses joins them no more tightly. The comparison is not like for like: the poem was built *from* "
      "the concordance, so these figures measure reuse of attested wording, not oral composition; and Homer's own figure "
      "includes his repeated verses, as the poem's includes its copied ones.")
    A("")
    A("## 7. Source entries in detail")
    A("")
    A("Columns: composer's status; cited lines that contain the claimed string or are hits of the recorded query / cited lines; "
      "count claimed / recorded query's hits / hits of the claimed string (`ngram`); the string's Homeric positions (top 4, with "
      "counts); its position in the verse if present word for word; reviewer's class and modification; Homeric parallel for "
      "that kind of modification (all printed by the concordance; '-' = none offered or none found).")
    A("")
    A("| n | k | entry text | composer | citation | cited ok | count c/q/H | Homeric positions | verse position | reviewer | Homeric parallel |")
    A("|---|---|---|---|---|---|---|---|---|---|---|")
    L.extend(detail)
    A("")
    Path(out).write_text("\n".join(L) + "\n", encoding="utf-8")
    print(dict(verdicts), dict(tallies))
    print("FAIL:", {n: v for n, v in sorted(fails.items())})
    print("QUERY:", sorted(n for n in queries if n not in fails))


if __name__ == "__main__":
    main(*sys.argv[1:5])
