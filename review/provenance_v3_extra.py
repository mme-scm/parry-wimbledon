#!/usr/bin/env python3
"""Supplementary concordance evidence for the provenance review of composition/drafts/v3.

    source .venv/bin/activate
    python -I review/provenance_v3_extra.py composition/drafts/v3.jsonl review/provenance_v3_evidence.json \
        review/provenance_v3_extra.json

Adapted from review/provenance_v2_extra.py (same checks 1-6, the SLOTS table updated for the v3 verses) plus
  7. the v3 claims: every concordance count, position and cited line asserted in the changed records (23, 33, 36,
     44, 51, 55, 56) and in the round-2 record corrections, recomputed (CLAIMS below);
  8. the accent of Νοβῆκος (R9): Homeric words in -η + one consonant + -ος, circumflex v. acute (NFC regex);
  9. αὖθʼ / αὖτʼ before a word with a rough breathing (line 56), from the NFC text (U+0314 in the decomposition).

Checks that review/provenance_check.py does not make (all through homer/concordance.py's Concordance class,
the same code as its CLI):
  1. forms of the poem with 0 Homeric hits (loose, whole word) and where each record marks them;
  2. the coined name stems (loose substring) have 0 hits;
  3. the analogical model of the patronymic Ζοκοβείδης: -είδ- with the diphthong ει (NFC regex, which keeps
     the diaeresis that the loose form drops) against -εΐδ-, with the metrical positions of every hit;
     the Ionic-η model (Ἀθήνη);
  4. name slots: for every coined name in the verse, the Homeric model word in the cited model line, its
     position there (homer/scansion.tsv), the coined name's position in the verse (homer/scan.py), and the
     number of Homeric occurrences of the model word at that position; with the neighbouring words, since
     some slots depend on a vowel-final word before or a vowel-initial word after;
  5. counts asserted in the records' notes for the name slots, recomputed;
  6. the `position` field of every source entry compared with the position of its string in the verse
     (entries whose string is in the verse word for word).
"""
import json
import re
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "homer"))
sys.path.insert(0, str(ROOT / "review"))
import greek as G  # noqa: E402
import provenance_check as P  # noqa: E402  (P.C = the Concordance)

C = P.C
LINE = P.LINE_BY_CIT


def L(s):
    return [G.loose(t.core) for t in G.tokenize(G.nfc(s))]


def posc(hits):
    return dict(Counter(f"{h.pos_start}-{h.pos_end}" for h in hits).most_common())


# (verse, coined form in the verse, Homeric model word, model citation, what the slot depends on)
SLOTS = [
    (4, "Φεδερεύς", "Ὀδυσεύς", "Il. 10.340", ""),
    (4, "Ζοκοβείδης", "Γανυμήδης", "Il. 20.232", "after τε καὶ ἀντίθεος"),
    (4, "Ζοκοβείδης", "Θρασυμήδης", "Od. 3.414", "after τε καὶ ἀντίθεος"),
    (4, "Ζοκοβείδης", "Κλυτόνηος", "Od. 8.119", "after τε καὶ ἀντίθεος"),
    (5, "Ἑλβέτιος", "Πηλεΐδης", "Il. 20.164", ""),
    (10, "Σέρβος", "Ἕκτωρ", "Il. 8.216", ""),
    (12, "Ἑλβέτιος", "Πάτροκλος", "Il. 16.284", ""),
    (12, "Ἑλβέτιος", "Πηλεΐδης", "Il. 20.164", ""),
    (14, "Φεδερῆρος", "Διομήδης", "Il. 2.563", ""),
    (15, "Σέρβος", "Τεῦκρος", "Il. 8.273", "before a vowel-initial word"),
    (19, "Ἑλβέτιος", "Δαρδανίδης", "Il. 3.303", ""),
    (20, "Φεδερῆρος", "Διομήδης", "Il. 2.563", ""),
    (23, "Ζοκοβείδης", "Διομήδης", "Il. 4.401", "after κρατερός"),
    (23, "Ζοκοβείδης", "Διομήδης", "Il. 5.143", "after κρατερός after a word ending at 7"),
    (24, "Ἑλβέτιος", "Δαρδανίδης", "Il. 3.303", ""),
    (25, "Φεδερεύς", "Ἀχιλεύς", "Il. 20.273", ""),
    (27, "Ῥογῆρος", "Ὀδυσσεύς", "Il. 2.272", "after a vowel-final word"),
    (27, "Ῥογῆρος", "Μελανθώ", "Od. 19.65", "after a vowel-final word"),
    (29, "Σέρβος", "Ἕκτωρ", "Il. 8.216", ""),
    (29, "Σέρβος", "Ἕκτωρ", "Il. 17.304", "name + δʼ αὖτʼ at 1-3"),
    (29, "Φεδερῆρον", "Μενέλαον", "Il. 4.220", ""),
    (30, "Φεδερῆρος", "Διομήδης", "Il. 2.563", ""),
    (32, "Φεδερεύς", "Ἀχιλεύς", "Il. 20.273", ""),
    (33, "Ῥογῆρος", "Ὀδυσσεύς", "Il. 2.272", "after a vowel-final word"),
    (33, "Ῥογῆρος", "Μελανθώ", "Od. 19.65", "after a vowel-final word, before a consonant"),
    (34, "Φεδερῆρος", "Διομήδης", "Il. 8.91", ""),
    (36, "Φεδερῆρος", "Διομήδης", "Il. 2.563", "inside βοὴν ἀγαθός + name at 6-12"),
    (38, "Σέρβος", "Ἕκτωρ", "Il. 8.216", ""),
    (38, "Σέρβος", "Τρῶες", "Il. 8.55", "before δʼ αὖθʼ ἑτέρωθεν"),
    (43, "Σέρβον", "Τεῦκρος", "Il. 12.350", "before a vowel-initial word"),
    (44, "Νοβῆκος", "γυναῖκας", "Od. 24.278", "after δʼ αὖτε, before a vowel"),
    (44, "Νοβῆκος", "ἄριστος", "Il. 1.91", "before a vowel"),
    (51, "Ἑλβετίου", "Δαρδανίδης", "Il. 3.303", ""),
    (51, "Σέρβου", "κνίσῃ", "Il. 1.460", "LL at 8-9 before an SSLX verse-end word"),
    (51, "Σέρβου", "ἀνδρῶν", "Il. 1.172", "LL at 8-9 before an SSLX verse-end word"),
    (52, "Ἑλβετίου", "Ἀτρεΐδης", "Il. 14.29", ""),
    (53, "Ζοκοβείδης", "Διομήδης", "Il. 4.401", "after κρατερός"),
    (54, "Ἑλβέτιος", "Δαρδανίδης", "Il. 3.303", ""),
    (55, "Νοβῆκος", "Μελανθώ", "Od. 19.65", "after a vowel-final word, before a consonant"),
    (55, "Νοβῆκος", "Ὀδυσσεύς", "Il. 2.272", "after a vowel-final word"),
    (56, "Ἑλβέτιος", "Ἀντίνοος", "Od. 1.383", "after αὖτʼ"),
    (56, "Ἑλβέτιος", "Δαρδανίδης", "Il. 3.303", ""),
    (56, "Ζοκοβείδης", "Διομήδης", "Il. 2.563", "bare name at 9.5-12"),
    (57, "Ἑλβέτιος", "Σαρπηδών", "Il. 16.466", ""),
    (57, "Ἑλβέτιος", "Πηλεΐδης", "Il. 20.164", ""),
    (58, "Σέρβος", "Ἕκτωρ", "Il. 8.216", ""),
    (58, "Σέρβος", "Ἕκτωρ", "Il. 17.304", "name + δʼ αὖτʼ at 1-3"),
]


# (line, label, kind, query, cited lines, what the record asserts)
CLAIMS = [
    (23, "δεύτερον αὖ", "ngram", "δεύτερον αὖ", ["Il. 3.332", "Il. 6.184", "Il. 11.19", "Il. 16.133", "Il. 19.371"], "5x, all line-initial"),
    (23, "λάβʼ ἄεθλον", "ngram", "λάβ᾽ ἄεθλον", ["Il. 23.511"], "Il. 23.511 at 9.5-12; here 3.5-5.5"),
    (23, "ἄεθλον", "ngram", "ἄεθλον", ["Il. 23.892", "Od. 21.91", "Od. 23.261"], "27x: 3 at 4-5.5, 22 at 10-12"),
    (23, "λάβε", "ngram", "λάβε", [], "9.5-10 14x, 7.5-8 9x, 5.5-6 2x, 6-7 1x"),
    (23, "λάβʼ", "ngram", "λάβ᾽", ["Il. 23.511"], "(the elided form actually in the verse)"),
    (23, "ἄφαρ", "loose", "αφαρ", ["Il. 1.594", "Il. 11.418", "Il. 23.593"], "34x: 15 at 6-7, 16 at 2-3"),
    (23, "κρατερὸς Διομήδης", "ngram", "κρατερὸς Διομήδης", ["Il. 4.401", "Il. 5.143"], "20x, 19 verse-final"),
    (23, "μίγη κρατερὸς Διομήδης", "ngram", "μίγη κρατερὸς Διομήδης", ["Il. 5.143"], "6-12"),
    (23, "ἄφαρ κέ τοι αὐτίκα", "ngram", "ἄφαρ κέ τοι αὐτίκα", ["Il. 23.593"], "parallel for ἄφαρ"),
    (23, "οὐδʼ ἀφάμαρτε", "ngram", "οὐδ᾽ ἀφάμαρτε", ["Il. 11.350", "Il. 13.160", "Il. 14.403", "Il. 22.290"], "3-5.5 and 9-12 (the mobility parallel)"),
    (23, "Ζοκοβείδαο (test)", "loose_sub", "ζοκοβειδα", [], "0 (rejected genitive)"),
    (33, "καὶ βάλεν", "ngram", "καὶ βάλεν", ["Il. 3.347", "Il. 11.350", "Il. 13.160"], "11x, all 1-2"),
    (33, "καὶ βάλεν αὖτις", "ngram", "καὶ βάλεν αὖτις", [], "(not claimed; checked for an unclaimed attestation)"),
    (33, "βάλεν αὖτις", "ngram", "βάλεν αὖτις", [], "(not claimed)"),
    (33, "καὶ * αὖτις", "ngram", "καὶ * αὖτις", ["Il. 15.29"], "καί + verb + αὖτις verse-final"),
    (33, "αὖτις", "ngram", "αὖτις", ["Il. 15.29", "Il. 6.367", "Il. 18.59", "Il. 1.140"], "128x: 20 at 11-12"),
    (33, "καὶ ἀνήγαγον αὖτις", "ngram", "καὶ ἀνήγαγον αὖτις", ["Il. 15.29"], "parallel"),
    (33, "ἵξομαι αὖτις", "ngram", "ἵξομαι αὖτις", ["Il. 6.367"], "parallel"),
    (33, "ὑποδέξομαι αὖτις", "ngram", "ὑποδέξομαι αὖτις", ["Il. 18.59"], "parallel"),
    (33, "καὶ εἴρετο δεύτερον αὖτις", "ngram", "καὶ εἴρετο δεύτερον αὖτις", ["Il. 1.513"], "parallel"),
    (33, "καὶ μʼ ᾔτεε δεύτερον αὖτις", "ngram", "καί μ᾽ ᾔτεε δεύτερον αὖτις", ["Od. 9.354"], "parallel"),
    (33, "δεύτερον αὖτις", "ngram", "δεύτερον αὖτις", [], "five Homeric uses (notes)"),
    (33, "Ἀχαιῶν", "ngram", "Ἀχαιῶν", [], "96x at 6-8"),
    (36, "τρὶς μὲν ἔπειτʼ ἐπόρουσε", "ngram", "τρὶς μὲν ἔπειτ᾽ ἐπόρουσε", ["Il. 5.436", "Il. 16.784", "Il. 20.445"], "3x, all 1-5.5"),
    (36, "τρὶς μὲν ἔπειτʼ ἐπόρουσε ποδάρκης δῖος Ἀχιλλεὺς", "ngram", "τρὶς μὲν ἔπειτ᾽ ἐπόρουσε ποδάρκης δῖος Ἀχιλλεὺς", ["Il. 20.445"], "1x"),
    (36, "ἀλλʼ ὅτε δὴ τὸ τέταρτον ἐπέσσυτο δαίμονι ἶσος", "ngram", "ἀλλ᾽ ὅτε δὴ τὸ τέταρτον ἐπέσσυτο δαίμονι ἶσος", ["Il. 5.438", "Il. 16.705", "Il. 16.786", "Il. 20.447"], "follows the τρὶς μέν line (R12)"),
    (36, "κατακτάμεναι μενεαίνων", "ngram", "κατακτάμεναι μενεαίνων", ["Il. 5.436"], "6-12 of the count line"),
    (36, "θοῷ ἀτάλαντος Ἄρηϊ", "ngram", "θοῷ ἀτάλαντος Ἄρηϊ", ["Il. 16.784"], "6-12 of the count line"),
    (36, "βοὴν ἀγαθὸς Διομήδης", "ngram", "βοὴν ἀγαθὸς Διομήδης", ["Il. 2.563", "Il. 5.114"], "21x, all 6-12"),
    (36, "τρὶς μὲν ἔπειτʼ", "ngram", "τρὶς μὲν ἔπειτ᾽", [], "(lines 14, 36, 53 share it)"),
    (44, "ἔκφερʼ", "ngram", "ἔκφερ᾽", ["Il. 23.759", "Il. 23.259", "Il. 23.785"], "3x elided, line-initial in 23.759"),
    (44, "ἔκφερεν", "ngram", "ἔκφερεν", ["Od. 15.470"], "1x line-initial"),
    (44, "ἔκφερε", "loose", "εκφερε", [], "0x"),
    (44, "δʼ αὖτε", "ngram", "δ᾽ αὖτε", ["Od. 24.278", "Il. 23.316", "Od. 2.203", "Od. 3.402", "Od. 20.380"], "141x: 105 at 2-3, 19 at 5-5.5, 12 at 11-12, 5 at 3-3.5"),
    (44, "χωρὶς δʼ αὖτε γυναῖκας", "ngram", "χωρὶς δ᾽ αὖτε γυναῖκας", ["Od. 24.278"], "1-5.5"),
    (44, "ὃς νῦν πολλὸν ἄριστος", "ngram", "ὃς νῦν πολλὸν ἄριστος", ["Il. 1.91"], "ἄριστος at 4-5.5"),
    (44, "δʼ ἕσπετο", "ngram", "δ᾽ ἕσπετο", ["Od. 1.125", "Od. 8.109", "Il. 12.398"], "3x: 7-8 (Od. 1.125, 8.109), 3-4 (Il. 12.398)"),
    (44, "ὃ δʼ ἕσπετο", "ngram", "ὃ δ᾽ ἕσπετο", [], "(the verse's string; not claimed as attested)"),
    (44, "ἡ δʼ ἕσπετο Παλλὰς Ἀθήνη", "ngram", "ἡ δ᾽ ἕσπετο Παλλὰς Ἀθήνη", ["Od. 1.125"], "6-12"),
    (44, "ὃ δʼ ἅμʼ ἕσπετο ἰσόθεος φώς", "ngram", "ὃ δ᾽ ἅμ᾽ ἕσπετο ἰσόθεος φώς", ["Il. 11.472", "Il. 15.559", "Il. 16.632"], "3x"),
    (44, "ὃ δʼ ἐπέσσυτο", "ngram", "ὃ δ᾽ ἐπέσσυτο", ["Il. 21.234", "Il. 21.601"], "2x"),
    (44, "ἕσπετο", "loose", "εσπετο", ["Il. 3.376", "Il. 11.472", "Od. 1.125", "Od. 8.109"], "12x: 8 at 7-8"),
    (44, "κέρδεα εἰδώς", "ngram", "κέρδεα εἰδώς", ["Il. 23.709"], "1x verse-final"),
    (44, "οὗτος δʼ αὖ Λαερτιάδης", "ngram", "οὗτος δ᾽ αὖ Λαερτιάδης", ["Il. 3.200"], "δʼ αὖ at 3 (the v2 citation)"),
    (44, "ἔκφερʼ Ὀϊλιάδης ἐπὶ δʼ ὄρνυτο δῖος Ὀδυσσεὺς", "ngram", "ἔκφερ᾽ Ὀϊλιάδης ἐπὶ δ᾽ ὄρνυτο δῖος Ὀδυσσεὺς", ["Il. 23.759"], "1-12"),
    (51, "τὴν δʼ αὖ", "ngram", "τὴν δ᾽ αὖ", ["Od. 1.213", "Od. 1.230", "Od. 2.371", "Od. 21.343"], "13x, all 1-2"),
    (51, "δʼ αὖ", "ngram", "δ᾽ αὖ", ["Il. 8.324", "Il. 6.462", "Il. 10.108", "Il. 21.105", "Il. 23.724", "Il. 24.732"], "110x: 6 at 7, 28 at 3, 68 at 2"),
    (51, "* δʼ αὖ (pronoun at 6)", "ngram", "* δ᾽ αὖ", [], "pronoun + δʼ αὖ at 6-7: 6x"),
    (51, "τὸν δʼ αὖ κορυθαίολος Ἕκτωρ", "ngram", "τὸν δ᾽ αὖ κορυθαίολος Ἕκτωρ", ["Il. 8.324"], "6-12"),
    (51, "τὴν μὲν ἄρʼ", "ngram", "τὴν μὲν ἄρ᾽", ["Il. 5.353", "Il. 18.148", "Od. 19.440"], "3x, 1-2"),
    (51, "Ἕκτορος (in the frame model)", "ngram", "Ἕκτορος", ["Il. 22.211"], "the second owner's genitive in Il. 22.211"),
    (51, "τὴν δʼ Ἕκτορος ἱπποδάμοιο", "ngram", "τὴν δ᾽ Ἕκτορος ἱπποδάμοιο", ["Il. 22.211"], "model line"),
    (51, "κρατεροῖο", "loose", "κρατεροιο", ["Il. 13.60", "Il. 13.415", "Il. 23.848", "Od. 11.277"], "7x: 5 at 9.5-12"),
    (51, "Πολυποίταο κρατεροῖο", "ngram", "Πολυποίταο κρατεροῖο", ["Il. 23.848"], "8-12 (record's position field)"),
    (51, "κνίσῃ ἐκάλυψαν", "ngram", "κνίσῃ ἐκάλυψαν", ["Il. 1.460", "Il. 2.423", "Od. 3.457", "Od. 12.360"], "4x at 8-12"),
    (51, "ἀνδρῶν Ἀγαμέμνων", "ngram", "ἀνδρῶν Ἀγαμέμνων", ["Il. 1.172"], "36x"),
    (51, "Τρώων θʼ ἱπποδάμων καὶ Ἀχαιῶν χαλκοχιτώνων", "ngram", "Τρώων θ᾽ ἱπποδάμων καὶ Ἀχαιῶν χαλκοχιτώνων", ["Il. 8.71"], "ethnics as the scales' owners"),
    (51, "Πηλεΐδαο", "loose", "πηλειδαο", ["Il. 15.74", "Il. 22.290"], "5x, LSSLS, 3-5.5"),
    (51, "Πηληϊάδεω", "loose", "πηληιαδεω", [], "10x"),
    (51, "Πηληϊάδεω Ἀχιλῆος", "ngram", "Πηληϊάδεω Ἀχιλῆος", [], "8x"),
    (51, "Ζοκοβῆος / Ζοκοβεύς in v3", "loose_sub", "ζοκοβη", [], "(Homer: 0)"),
    (55, "ἡ δʼ Ὀδυσῆʼ ἐνένιπε Μελανθὼ δεύτερον αὖτις", "ngram", "ἡ δ᾽ Ὀδυσῆ᾽ ἐνένιπε Μελανθὼ δεύτερον αὖτις", ["Od. 19.65"], "Μελανθώ at 6-8"),
    (55, "πρῶτος", "loose", "πρωτος", [], "55x"),
    (55, "δῆμος", "loose", "δημος", [], "8x"),
    (55, "κλῆρος", "loose", "κληρος", [], "6x"),
    (55, "Ἀθήνη", "loose", "αθηνη", [], "215x"),
    (56, "ἔνθʼ αὖτʼ", "ngram", "ἔνθ᾽ αὖτ᾽", ["Il. 4.384", "Il. 5.541", "Il. 17.344", "Il. 23.140"], "12x, all line-initial"),
    (56, "ἔνθʼ αὖθʼ", "ngram", "ἔνθ᾽ αὖθ᾽", [], "(the verse's string)"),
    (56, "αὖθʼ ἱερεὺς", "ngram", "αὖθ᾽ ἱερεὺς", ["Il. 1.370"], "1x"),
    (56, "τὸν δʼ αὖθʼ", "ngram", "τὸν δ᾽ αὖθ᾽", ["Il. 6.144"], "1x"),
    (56, "ἔνθʼ αὖτʼ Αἰνείας", "ngram", "ἔνθ᾽ αὖτ᾽ Αἰνείας", ["Il. 5.541", "Il. 17.344"], "2x, 1-5"),
    (56, "προΐει", "loose", "προιει", ["Il. 1.326", "Il. 3.346"], "21x, 19 in the third foot"),
    (56, "βάλε δʼ", "ngram", "βάλε δ᾽", ["Il. 15.541", "Il. 16.737", "Od. 24.179"], "3x, 7.5-9"),
    (56, "Διομήδης", "ngram", "Διομήδης", ["Il. 2.563"], "45x, 44 verse-final"),
    (56, "Αἰγύπτιος", "loose", "αιγυπτιος", ["Od. 2.15"], "LLSS"),
    # round-2 record corrections
    (24, "περὶ στήθεσσιν ἔδυνεν", "ngram", "περὶ στήθεσσιν ἔδυνεν", ["Il. 3.332", "Il. 19.371"], "2x"),
    (24, "περὶ στήθεσσιν ἔδυνε", "ngram", "περὶ στήθεσσιν ἔδυνε", ["Il. 11.19", "Il. 16.133"], "2x"),
    (24, "δάμασε", "loose", "δαμασε", ["Il. 22.446"], "5.5-7"),
    (24, "δάμασεν", "loose", "δαμασεν", [], "0x"),
    (12, "δὲ πρῶτος", "ngram", "δὲ πρῶτος", ["Il. 16.284", "Il. 6.5", "Il. 10.532"], "12x: 5 at 4-5.5, 7 at 3-5"),
    (22, "ἀμφοτέρω", "loose", "αμφοτερω", ["Il. 4.521", "Il. 5.156"], "19x: 15 at 1-3, 4 at 3-5"),
    (22, "πάλιν", "ngram", "πάλιν", ["Il. 1.116", "Il. 1.380"], "57x: 24 at 6-7, 11 at 7.5-8"),
    (31, "καμάτῳ", "loose", "καματω", ["Il. 13.85", "Il. 7.6", "Il. 10.98"], "14x: 4 at 5.5-7"),
    (29, "Ἕκτωρ δʼ αὖτʼ", "ngram", "Ἕκτωρ δ᾽ αὖτ᾽", ["Il. 17.304", "Il. 3.76"], "2x: 1-3 (17.304), 3-5 (3.76)"),
    (29, "Αἴας δʼ αὖτʼ", "ngram", "Αἴας δ᾽ αὖτ᾽", ["Il. 14.469"], "1-3"),
    (30, "αὐτὰρ ὅ γʼ ἥρως", "ngram", "αὐτὰρ ὅ γ᾽ ἥρως", [], "7x, all 9-12"),
    (30, "ἄναξ ἀνδρῶν Ἀγαμέμνων", "ngram", "ἄναξ ἀνδρῶν Ἀγαμέμνων", ["Il. 2.402", "Il. 3.81", "Il. 19.51"], "verse-final"),
    (30, "αὐτὰρ ὃ (line-initial)", "regex", r"^αὐτὰρ ὃ\b", ["Il. 2.402", "Il. 3.81", "Il. 19.51"], "line-initial pronoun"),
    (30, "αὐτὰρ ὅ γʼ ἂψ", "ngram", "αὐτὰρ ὅ γ᾽ ἂψ", ["Od. 11.599"], "1-3"),
    (20, "τρὶς δέ", "ngram", "τρὶς δέ", ["Od. 4.277"], "notes: 7x; entry 0: 8x"),
    (20, "τρὶς δʼ", "ngram", "τρὶς δ᾽", ["Il. 24.16", "Il. 24.273"], "7x"),
    (43, "θυμὸς ἀνῆκεν", "ngram", "θυμὸς ἀνῆκεν", ["Il. 7.25", "Il. 21.395"], "μέγας δέ σε θυμὸς ἀνῆκεν"),
    (43, "θυμὸς ἀνῆκε", "ngram", "θυμὸς ἀνῆκε", ["Il. 10.389", "Il. 12.307"], "ἦ σʼ αὐτὸν θυμὸς ἀνῆκε; Σαρπηδόνα θυμὸς ἀνῆκε"),
    (43, "δῖον ἀνῆκεν", "ngram", "δῖον ἀνῆκεν", ["Il. 17.705"], "Θρασυμήδεα δῖον ἀνῆκεν"),
    (15, "ἀπήμβροτε δουρὶ φαεινῷ", "ngram", "ἀπήμβροτε δουρὶ φαεινῷ", ["Il. 16.477"], "absolute ἀπήμβροτε"),
    (15, "Τρωσὶν μὲν προμάχιζεν", "ngram", "Τρωσὶν μὲν προμάχιζεν", ["Il. 3.16"], "asyndetic apodosis"),
    (15, "Ἀτρεΐδης μὲν ἅμαρτε", "ngram", "Ἀτρεΐδης μὲν ἅμαρτε", ["Il. 11.233"], "asyndetic apodosis"),
    (15, "οἳ δʼ ὅτε δή", "ngram", "οἳ δ᾽ ὅτε δή", ["Il. 3.15", "Il. 11.232"], "the protasis"),
    (4, "Ἀμαρυγκείδην", "regex", r"Ἀμαρυγκείδην", ["Il. 4.517"], "unique scansion, diphthong"),
    (4, "Ἀμαρυγκεΐδης", "regex", r"Ἀμαρυγκεΐδης", ["Il. 2.622"], "-εΐ-"),
    (4, "Ἀμαρυγκέα", "regex", r"Ἀμαρυγκέα", ["Il. 23.630"], "the father"),
    (4, "Ἀτρείδης (diphthong)", "regex", r"Ἀτρείδης", ["Od. 15.52"], "unique scansion"),
    (4, "Πηλείδη (diphthong)", "regex", r"Πηλείδη", ["Il. 1.277"], "LLL"),
    (4, "Πηλεΐδης (nom.)", "regex", r"Πηλεΐδης", [], "24x"),
    (4, "Πηλεΐδ- (all)", "regex", r"Πηλεΐδ\w*", [], "51x"),
    (4, "Πηλείωνα", "regex", r"Πηλείων\w*", ["Il. 22.7"], "diphthong"),
    (4, "Πηλεΐων-", "regex", r"Πηλεΐων\w*", [], "48x"),
]

COINED_STEMS = ["φεδερ", "ρογηρ", "ελβετ", "σερβ", "ζοκοβ", "νοβηκ", "νοβακ", "ζοκοβειδα", "ζοκοβειδε"]


def word_at(ln_tokens, wp, i):
    return {"word": ln_tokens[i], "position": wp[i] if wp else None}


def main(jsonl, evid, out_path):
    recs = [json.loads(l) for l in open(jsonl, encoding="utf-8") if l.strip()]
    ev = {r["n"]: r for r in json.load(open(evid, encoding="utf-8"))}
    res = {}

    # 1. forms with 0 Homeric hits
    vocab = Counter(w for ln in C.lines for w in ln.loose_tokens)
    zero = []
    for r in recs:
        marks = " ".join([c.get("form", "") for c in r.get("coinages") or []])
        coin_src = " ".join(s["text"] for s in r.get("sources", []) if s.get("status") == "COINAGE")
        mod_src = " ".join(s["text"] for s in r.get("sources", []) if s.get("status") == "ATTESTED-MODIFIED")
        for t in G.tokenize(G.nfc(r["text"])):
            w = G.loose(t.core)
            if vocab[w] == 0:
                zero.append({"n": r["n"], "form": t.core, "loose": w,
                             "in_coinages": w in L(marks), "in_coinage_entry": w in L(coin_src),
                             "named_in_modified_entry": w in L(mod_src)})
    res["forms_with_0_homeric_hits"] = zero

    # 2. coined stems
    res["coined_stems_substring_hits"] = {s: len(C.loose(s)) for s in COINED_STEMS}

    # 3. patronymic model
    def rx(p):
        hs = C.regex(p)
        return {"total": len(hs), "positions": posc(hs),
                "hits": [f"{h.citation}@{h.pos_start}-{h.pos_end}: {h.match} | {h.text}" for h in hs[:12]]}
    res["patronymic"] = {
        "Πηλείδ (diphthong ει)": rx(r"Πηλείδ\w*"),
        "Πηλεΐδ (ε-ϊ)": rx(r"Πηλεΐδ\w*"),
        "Πηλεΐδης (nom.)": rx(r"Πηλεΐδης"),
        "Πηλείων (diphthong)": rx(r"Πηλείων\w*"),
        "Πηλεΐων (ε-ϊ)": rx(r"Πηλεΐων\w*"),
        "Ἀτρείδ (diphthong)": rx(r"Ἀτρείδ\w*"),
        "Ἀμαρυγκ- (Ἀμαρυγκεύς and patronymics)": rx(r"Ἀμαρυγκ\w*"),
        "capitalised -είδ- with the diphthong (all)": rx(r"\b[Α-ΩἈ-Ὧ]\w*είδ\w*"),
        "capitalised -εΐδ- (all)": rx(r"\b[Α-ΩἈ-Ὧ]\w*εΐδ\w*"),
        "Ζοκοβειδ (loose substring)": len(C.loose("ζοκοβειδ")),
        "Νοβηκ (loose substring)": len(C.loose("νοβηκ")),
    }
    res["ionic_eta"] = {"αθηνη --word": len(C.loose("αθηνη", word=True)),
                        "αθανα --word": len(C.loose("αθανα", word=True)),
                        "αθαναι --word": len(C.loose("αθαναι", word=True))}

    # 4. name slots
    slots = []
    for n, coined, model, cit, cond in SLOTS:
        e = ev[n]
        vw, vwp = e["words"], e["scan"]["word_positions"]
        cl = G.loose(coined)
        vi = vw.index(cl) if cl in vw else None
        ln = LINE.get(cit)
        ml = G.loose(model)
        mi = ln.loose_tokens.index(ml) if ln and ml in ln.loose_tokens else None
        mpos = ln.word_pos[mi] if (mi is not None and ln.word_pos) else None
        vpos = vwp[vi] if vi is not None else None
        same_form_at = posc(C.ngram([ml]))
        d = {"verse": n, "coined": coined, "verse_position": vpos,
             "verse_prev": vw[vi - 1] if vi else None, "verse_next": vw[vi + 1] if vi is not None and vi + 1 < len(vw) else None,
             "model": model, "model_citation": cit, "model_in_line": mi is not None, "model_position": mpos,
             "model_prev": ln.loose_tokens[mi - 1] if mi else None,
             "model_next": ln.loose_tokens[mi + 1] if mi is not None and mi + 1 < len(ln.loose_tokens) else None,
             "model_line": ln.text if ln else None, "same_position": vpos == mpos,
             "model_form_positions_in_homer": same_form_at, "condition": cond}
        slots.append(d)
    res["name_slots"] = slots

    # 5. counts asserted in the notes
    res["note_counts"] = {
        "Διομήδης": posc(C.ngram("Διομήδης")),
        "κρατερὸς Διομήδης": posc(C.ngram("κρατερὸς Διομήδης")),
        "Τεῦκρος": posc(C.ngram("Τεῦκρος")),
        "Παλλὰς": posc(C.ngram("Παλλὰς")),
        "Φοῖβος": posc(C.ngram("Φοῖβος")),
        "Ἀχαιῶν": posc(C.ngram("Ἀχαιῶν")),
        "Ἀπόλλων": posc(C.ngram("Ἀπόλλων")),
        "Ὀδυσσεύς": posc(C.ngram("Ὀδυσσεύς")),
        "Μελανθώ": posc(C.ngram("Μελανθώ")),
        "Ἀτρεΐδης": posc(C.ngram("Ἀτρεΐδης")),
        "ατρειδ (loose substring, the records' query)": posc(C.loose("ατρειδ")),
        "δαρδανιδης --word": posc(C.loose("δαρδανιδης", word=True)),
        "Ἀντίνοος": posc(C.ngram("Ἀντίνοος")),
        "* δʼ αὖτʼ": posc(C.ngram("* δ᾽ αὖτ᾽")),
        "Ἕκτωρ δʼ αὖτʼ": [f"{h.citation}@{h.pos_start}-{h.pos_end}" for h in C.ngram("Ἕκτωρ δ᾽ αὖτ᾽")],
        "Αἴας δʼ αὖτʼ": [f"{h.citation}@{h.pos_start}-{h.pos_end}" for h in C.ngram("Αἴας δ᾽ αὖτ᾽")],
        "τρὶς δέ μιν": len(C.ngram("τρὶς δέ μιν")),
        "δαμασεν --word": len(C.loose("δαμασεν", word=True)),
        "ἔκφερε --word": len(C.loose("εκφερε", word=True)),
        "δαΐφρονε --word": len(C.loose("δαιφρονε", word=True)),
        "ὣς τότε": posc(C.ngram("ὣς τότε")),
        "πολλάκι δή": posc(C.ngram("πολλάκι δή")),
    }

    # 4b. Homeric words beginning with ρ at 6 after a short vowel-final word ending at 5.5 (the Ῥογῆρος slot)
    rho = []
    for ln in C.lines:
        wp = ln.word_pos
        if not wp:
            continue
        for i in range(1, len(ln.loose_tokens)):
            w = ln.loose_tokens[i]
            pw = ln.loose_tokens[i - 1]
            if w.startswith("ρ") and wp[i].split("-")[0] == "6" and wp[i - 1].split("-")[1] == "5.5" \
                    and pw[-1] in "αεηιουω" and not pw.endswith("ʼ"):
                rho.append(f"{ln.work}. {ln.book}.{ln.line}: {pw} {w} | {ln.text}")
    res["rho_initial_at_6_after_vowel_final_word_at_5.5"] = {"count": len(rho), "examples": rho[:12]}

    # 6. position fields
    pf = []
    for r in recs:
        e = ev[r["n"]]
        for k, (s, es) in enumerate(zip(r.get("sources", []), e["sources"])):
            if not es["fragments"]:
                continue
            f0 = es["fragments"][0]
            if f0["in_poem_verbatim"] and s.get("position") and s["position"] not in f0["poem_positions"]:
                pf.append({"n": r["n"], "k": k, "text": s["text"], "position_field": s["position"],
                           "verse_position": f0["poem_positions"], "homer_positions": f0["homer_positions"]})
    res["position_field_mismatches"] = pf

    # 7. claims of the v3 records (changed verses and round-2 corrections): (line, label, query kind, string,
    #    lines the record cites for it, what the record asserts)
    def run(kind, q):
        if kind == "ngram":
            return C.ngram(q)
        if kind == "loose":
            return C.loose(q, word=True)
        if kind == "loose_sub":
            return C.loose(q)
        return C.regex(q)
    claims = []
    for n, label, kind, q, cits, asserted in CLAIMS:
        hs = run(kind, q)
        hc = {h.citation: f"{h.pos_start}-{h.pos_end}" for h in hs}
        claims.append({"n": n, "label": label, "query": f"{kind} {q}", "total": len(hs), "positions": posc(hs),
                       "cited": {c: hc.get(c, "NOT A HIT") for c in cits},
                       "cited_lines": {c: LINE[c].text for c in cits if c in LINE},
                       "asserted": asserted, "first_hits": [f"{h.citation}@{h.pos_start}-{h.pos_end}: {h.text}" for h in hs[:8]]})
    res["claims"] = claims

    # 8. accent of the name Νοβῆκος: Homeric words ending in η + one consonant + ος, circumflex v. acute
    import unicodedata as U
    cons = "βγδζθκλμνξπρστφχψ"
    circ = Counter(); acute = Counter()
    for ln in C.lines:
        for w in re.findall(r"[\w]+", G.nfc(ln.text)):
            if len(w) < 4 or not w.endswith("ος") or w[-3] not in cons:
                continue
            v = w[-4]
            base = U.normalize("NFD", v)
            if base[0] not in "ηΗ":
                continue
            if "͂" in base:
                circ[w] += 1
            elif "́" in base:
                acute[w] += 1
    res["accent_eta_C_os"] = {"circumflex_types": len(circ), "circumflex_tokens": sum(circ.values()),
                              "acute_types": len(acute), "acute_tokens": sum(acute.values()),
                              "acute_examples": acute.most_common(10), "circumflex_examples": circ.most_common(12)}

    # 9. αὖθʼ / αὖτʼ before a rough breathing
    def rough(w):
        return "̔" in U.normalize("NFD", w[:2])
    asp = {"αὖθʼ + rough": [], "αὖτʼ + rough": [], "αὖθʼ + smooth/consonant": 0, "αὖτʼ + smooth/consonant": 0,
           "ἔνθʼ αὖθʼ": len(C.ngram("ἔνθ᾽ αὖθ᾽")), "ἔνθʼ αὖτʼ": len(C.ngram("ἔνθ᾽ αὖτ᾽"))}
    for ln in C.lines:
        t = G.norm_apostrophes(G.nfc(ln.text))
        for m in re.finditer(r"(?<!\w)αὖ([θτ])ʼ\s+(\w+)", t):
            key = "αὖθʼ" if m.group(1) == "θ" else "αὖτʼ"
            if rough(m.group(2)):
                asp[key + " + rough"].append(f"{ln.work}. {ln.book}.{ln.line}: {m.group(2)}")
            else:
                asp[key + " + smooth/consonant"] += 1
    asp["αὖθʼ + rough (count)"] = len(asp["αὖθʼ + rough"]); asp["αὖτʼ + rough (count)"] = len(asp["αὖτʼ + rough"])
    asp["αὖθʼ + rough"] = asp["αὖθʼ + rough"][:12]
    res["aspiration"] = asp
    Path(out_path).write_text(json.dumps(res, ensure_ascii=False, indent=1), encoding="utf-8")
    print(json.dumps({k: (v if k not in ("name_slots", "patronymic") else "...") for k, v in res.items()},
                     ensure_ascii=False, indent=1)[:6000])


if __name__ == "__main__":
    main(*sys.argv[1:4])
