#!/usr/bin/env python3
"""Supplementary concordance evidence for the provenance review of composition/drafts/v4.

    source .venv/bin/activate
    python -I review/provenance_v4_extra.py composition/drafts/v4.jsonl review/provenance_v4_evidence.json \
        review/provenance_v4_extra.json

Adapted from review/provenance_v3_extra.py (checks 1-9 kept; the SLOTS table rebuilt for the v4 numbering and the
new verses; CLAIMS rebuilt for the verses changed or added in v4 and for the critic's M8 parallels) plus
 10. every form listed in a record's `coinages`, looked up in Homer (loose, whole word, and exact NFC): claimed
     coinages that already exist in Homer;
 11. forms with 0 Homeric hits: whether they are named in the record's `modifications` (disclosure outside the
     `sources` entries), in addition to `coinages` and the source entries (check 1);
 12. homer/check_line.py on every verse (A1: a name slot is allowed where check_line passes with no flags);
 13. the accent of the genitive Νοβήκου: Homeric words in -η + one consonant + -ου, circumflex v. acute;
 14. Homeric genitives in -ου of three syllables at 10-12 (the slot of Νοβήκου, line 29) and LL datives in -ῳ at
     1-2 before δʼ (the slot of Σέρβῳ, line 62);
 15. the v3 → v4 mapping (records' `v3_line`), the verses whose text changed, and the critic's issues per record.

Checks 1-6 as in v3 (see review/provenance_v3_extra.py): forms with 0 Homeric hits; coined stems as loose
substrings; the -είδης models; name slots (coined name in the verse v. the Homeric model word in the cited model
line, positions from homer/scan.py and homer/scansion.tsv); counts in the notes; `position` fields.
All lookups go through homer/concordance.py's Concordance class (the code behind its CLI).
"""
import json
import re
import subprocess
import sys
import unicodedata as U
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


# (verse, coined form in the verse, Homeric model word, model citation, what the slot depends on).
# Model words named in the records' COINAGE entries (and, marked 'reviewer', parallels found in this review).
SLOTS = [
    (4, "Φεδερεύς", "Ὀδυσεύς", "Il. 10.340", ""),
    (4, "Ζοκοβείδης", "Γανυμήδης", "Il. 20.232", "after τε καὶ ἀντίθεος"),
    (4, "Ζοκοβείδης", "Θρασυμήδης", "Od. 3.414", "after τε καὶ ἀντίθεος"),
    (4, "Ζοκοβείδης", "Κλυτόνηος", "Od. 8.119", "after τε καὶ ἀντίθεος"),
    (5, "Ἑλβέτιος", "Πηλεΐδης", "Il. 20.164", ""),
    (10, "Σέρβος", "Ἕκτωρ", "Il. 8.216", ""),
    (12, "Ἑλβέτιος", "Πηλεΐδης", "Il. 20.164", ""),
    (14, "Φεδερῆρος", "Διομήδης", "Il. 2.563", ""),
    (15, "Σέρβος", "Τεῦκρος", "Il. 8.273", "before a vowel-initial word"),
    (19, "Ἑλβέτιος", "Δαρδανίδης", "Il. 3.303", ""),
    (23, "Ῥογῆρος", "Ὀδυσσεύς", "Il. 2.272", "after a vowel-final word"),
    (23, "Ῥογῆρος", "Μελανθώ", "Od. 19.65", "after a vowel-final word"),
    (24, "Σέρβος", "Ἄδρηστος", "Il. 6.45", "record's model: bare name before (δʼ ἄρʼ) ἔπειτα"),
    (24, "Σέρβος", "Ἕκτωρ", "Il. 8.216", "record's model for the name (coinages)"),
    (24, "Σέρβος", "Τεῦκρος", "Il. 12.350", "reviewer: LS name at 3-3.5 before a vowel (the model of 48)"),
    (25, "Ἑλβέτιος", "Δαρδανίδης", "Il. 3.303", ""),
    (26, "Φεδερεύς", "Ἀχιλεύς", "Il. 20.273", ""),
    (28, "Ῥογῆρος", "Ὀδυσσεύς", "Il. 2.272", "after a vowel-final word"),
    (28, "Ῥογῆρος", "Μελανθώ", "Od. 19.65", "after a vowel-final word"),
    (29, "Νοβήκου", "Αἰακίδαο", "Il. 2.860", "record's whole-line model"),
    (29, "Νοβήκου", "Ἀχιλῆος", "Il. 21.553", "record's model: epithet + name genitive after ὑπό"),
    (29, "Νοβήκου", "Ἀχαιῶν", "Il. 1.12", "reviewer: SLL genitive at 10-12 after a short vowel"),
    (29, "Νοβήκου", "Λυκούργου", "Il. 6.134", "reviewer: SLL name genitive in -ου at 10-12, agent after ὑπʼ + epithet"),
    (31, "Σέρβος", "Ἕκτωρ", "Il. 8.216", ""),
    (31, "Φεδερῆρον", "Μενέλαον", "Il. 4.220", ""),
    (34, "Φεδερῆρος", "Διομήδης", "Il. 2.563", ""),
    (37, "Ῥογῆρος", "Ὀδυσσεύς", "Il. 2.272", "after a vowel-final word"),
    (37, "Ῥογῆρος", "Μελανθώ", "Od. 19.65", "after a vowel-final word, before a consonant"),
    (41, "Φεδερῆρος", "Διομήδης", "Il. 2.563", "inside βοὴν ἀγαθός + name at 6-12"),
    (43, "Σέρβος", "Ἕκτωρ", "Il. 8.216", ""),
    (43, "Σέρβος", "Τρῶες", "Il. 8.55", "before δʼ αὖθʼ ἑτέρωθεν"),
    (48, "Σέρβον", "Τεῦκρος", "Il. 12.350", "before a vowel-initial word"),
    (49, "Σέρβος", "Ἕκτωρ", "Il. 8.216", ""),
    (55, "Ἑλβετίου", "Δαρδανίδης", "Il. 3.303", ""),
    (55, "Σέρβου", "κνίσῃ", "Il. 1.460", "LL at 8-9 before an SSLX verse-end word"),
    (55, "Σέρβου", "ἀνδρῶν", "Il. 1.172", "LL at 8-9 before an SSLX verse-end word"),
    (56, "Ἑλβετίου", "Ἀτρεΐδης", "Il. 14.29", ""),
    (56, "Ἑλβετίου", "ἀντιθέου", "Od. 20.369", "genitive LSSL at 7-9"),
    (57, "Ζοκοβείδης", "Διομήδης", "Il. 4.401", "after κρατερός"),
    (59, "Νοβῆκος", "Μελανθώ", "Od. 19.65", "after a vowel-final word, before a consonant"),
    (59, "Νοβῆκος", "Ὀδυσσεύς", "Il. 2.272", "after a vowel-final word"),
    (60, "Ἑλβέτιος", "Ἀντίνοος", "Od. 1.383", "after αὖτʼ"),
    (60, "Ἑλβέτιος", "Δαρδανίδης", "Il. 3.303", ""),
    (60, "Ζοκοβείδης", "Διομήδης", "Il. 2.563", "bare name at 9.5-12"),
    (61, "Φεδερεῦ", "Ἀχιλεῦ", "Il. 11.606", "vocative SSL at 5.5-7"),
    (61, "Φεδερεῦ", "Ἀχιλεῦ", "Il. 24.503", "vocative SSL at 5.5-7"),
    (61, "Φεδερεῦ", "Ἀχιλεῦ", "Il. 24.661", "vocative SSL at 5.5-7"),
    (62, "Σέρβῳ", "τῷ", "Il. 1.250", "record's model: τῷ δʼ"),
    (62, "Σέρβῳ", "Ἕκτωρ", "Il. 8.216", "record's model for the name (coinages)"),
    (62, "Σέρβῳ", "Γλαύκῳ", "Il. 16.508", "reviewer: LL dative name at 1-2 before δʼ"),
]

# (line, label, kind, query, cited lines, what the record asserts)
CLAIMS = [
    # 19
    (19, "ἐπέσσυτο δαίμονι ἶσος", "ngram", "ἐπέσσυτο δαίμονι ἶσος", ["Il. 5.438", "Il. 5.459", "Il. 5.884", "Il. 16.705", "Il. 16.786", "Il. 20.447", "Il. 21.227"], "7x, all 6-12"),
    (19, "δαίμονι ἶσος", "ngram", "δαίμονι ἶσος", ["Il. 5.438"], "9x, all 9-12"),
    (19, "ὣς ἄρʼ ὅ γʼ", "ngram", "ὣς ἄρ᾽ ὅ γ᾽", ["Il. 22.143", "Od. 20.28"], "2x, 1-3 (simile close)"),
    (19, "δεύτερον αὖτε (removed)", "ngram", "δεύτερον αὖτε", [], "0x in Homer (critic m7)"),
    # 20
    (20, "ἐσσυμένως λάβʼ ἄεθλον", "ngram", "ἐσσυμένως λάβ᾽ ἄεθλον", ["Il. 23.511"], "7-12"),
    (20, "λάβʼ ἄεθλον", "ngram", "λάβ᾽ ἄεθλον", ["Il. 23.511"], "its only slot 9.5-12 (M8 restored)"),
    (20, "ἐσσυμένως", "loose", "εσσυμενως", ["Il. 23.511", "Il. 15.698", "Il. 21.610"], "12x: 7 line-initial, 3 at 7-9"),
    (20, "ἐδάμασσε", "loose", "εδαμασσε", ["Od. 11.171", "Od. 11.398", "Od. 22.246", "Od. 22.413", "Il. 6.159", "Il. 13.434", "Il. 16.826"], "7x: 4 at 3.5-5.5, 6.159 and 13.434 verse-final, 16.826 fourth-fifth foot"),
    (20, "κὴρ ἐδάμασσε", "ngram", "κὴρ ἐδάμασσε", ["Od. 11.171"], "parallel (long monosyllable before ἐδάμασσε)"),
    (20, "μοῖρʼ ἐδάμασσε", "ngram", "μοῖρ᾽ ἐδάμασσε", ["Od. 22.413"], "parallel"),
    (20, "τρὶς μέν μιν", "ngram", "τρὶς μέν μιν", ["Il. 18.155", "Il. 21.176", "Od. 21.125"], "3x, all line-initial"),
    (20, "τρὶς δέ", "ngram", "τρὶς δέ", ["Od. 4.277"], "8x (7 line-initial): round-3 correction"),
    (20, "τρὶς δʼ", "ngram", "τρὶς δ᾽", ["Il. 24.16", "Il. 24.273"], "9x: round-3 correction"),
    (20, "δεύτερος αὖτʼ", "ngram", "δεύτερος αὖτ᾽", ["Il. 20.273"], "6x, all line-initial"),
    (20, "εἴρυσσέν τε καὶ", "ngram", "εἴρυσσέν τε καὶ", ["Il. 3.373"], "two verbs joined by τε καί, καί at 6"),
    # 24
    (24, "ἀλλʼ ὅ γε", "ngram", "ἀλλ᾽ ὅ γε", ["Il. 1.281", "Il. 1.320", "Il. 2.3", "Il. 2.420", "Il. 5.321", "Il. 8.311"], "16x, all 1-2"),
    (24, "ἀλλʼ ὅ γʼ … ἐνίκα (frame)", "ngram", "ἀλλ᾽ ὅ γ᾽ ἀεθλεύειν", ["Il. 4.389"], "the contest line whose frame is used"),
    (24, "δʼ ἄρʼ ἔπειτα", "ngram", "δ᾽ ἄρ᾽ ἔπειτα", ["Il. 6.45"], "12x, all 3.5-5.5"),
    (24, "Ἄδρηστος (Il. 6.45)", "ngram", "Ἄδρηστος δ᾽ ἄρ᾽ ἔπειτα", ["Il. 6.45"], "bare name before ἔπειτα, 1-5.5"),
    (24, "Τεῦκρος at 3-3.5 (reviewer)", "ngram", "καί οἱ Τεῦκρος", ["Il. 12.350"], "LS name at 3-3.5 before a vowel"),
    (24, "μάχῃ", "loose", "μαχη", ["Il. 7.113", "Il. 8.448", "Od. 4.497"], "26x; at 6-7"),
    (24, "πύματον", "ngram", "πύματον", ["Il. 23.373", "Il. 23.768"], "8x: 3.5-5 and 5.5-7 (entry 3); 6x (coinages); 5x at 3.5-5 + 2x at 5.5-7 (modifications)"),
    (24, "πυμάτην", "ngram", "πυμάτην", ["Il. 18.608"], "3.5-5"),
    (24, "πυμάτῳ", "ngram", "πυμάτῳ", ["Od. 7.138"], "the dative masc."),
    (24, "πυμάτῃ (loose: = πυμάτη)", "loose", "πυματη", [], "'0 hits' (coinages)"),
    (24, "πυμάτῃ (exact NFC)", "exact", "πυμάτῃ", [], "'0 hits' (coinages)"),
    (24, "ἐνίκα", "loose", "ενικα", ["Il. 23.756", "Il. 4.389", "Il. 23.680"], "8x: 5 at 10-12, 3 at 6-8"),
    (24, "πόδεσσι δὲ πάντας ἐνίκα", "ngram", "πόδεσσι δὲ πάντας ἐνίκα", ["Il. 20.410"], "dative of the contest"),
    (24, "κάλλει ἐνίκα", "ngram", "κάλλει ἐνίκα", ["Il. 23.742"], "dative of the contest"),
    (24, "πάντας ἐνίκα", "ngram", "πάντας ἐνίκα", ["Il. 23.680"], "accusative of the man beaten"),
    # 29
    (29, "ἀλλὰ καὶ ὧς", "ngram", "ἀλλὰ καὶ ὣς", ["Il. 23.516"], "17x, all 1-3"),
    (29, "ἐδάμη", "ngram", "ἐδάμη", ["Il. 2.860", "Il. 2.874"], "2x, both 1.5-3 (here 3.5-5)"),
    (29, "ὑπὸ χερσὶ", "ngram", "ὑπὸ χερσὶ", ["Il. 3.352", "Il. 2.860", "Il. 6.368", "Il. 10.452", "Il. 16.438"], "11x: 3.5-5.5 and 7.5-9.5"),
    (29, "κρατεροῦ", "ngram", "κρατεροῦ", ["Il. 8.279", "Il. 21.553", "Od. 8.360"], "3x: 3.5-5, 7.5-9 (here 5.5-7)"),
    (29, "ὑπὸ κρατεροῦ Ἀχιλῆος", "ngram", "ὑπὸ κρατεροῦ Ἀχιλῆος", ["Il. 21.553"], "'the epithet before ὑπό as ὑπὸ κρατεροῦ Ἀχιλῆος'"),
    (29, "genitive + ὑπὸ χερσί (name first)", "regex", r"\S+ ὑπὸ χερσ[ίὶ]", ["Il. 11.180", "Il. 16.699", "Od. 18.156", "Od. 24.97"], "(reviewer: what precedes ὑπὸ χερσί in Homer)"),
    # 32
    (32, "αὐτὰρ ὅ γʼ ἂψ", "ngram", "αὐτὰρ ὅ γ᾽ ἂψ", ["Od. 11.599"], "1-3"),
    (32, "ἐπόρουσε καὶ", "ngram", "ἐπόρουσε καὶ", ["Il. 11.580", "Il. 13.550"], "3.5-6"),
    (32, "ἀμφήριστον ἔθηκεν", "ngram", "ἀμφήριστον ἔθηκεν", ["Il. 23.382", "Il. 23.527"], "7-12"),
    (32, "ἂψ ἐπόρουσε (unclaimed)", "ngram", "ἂψ ἐπόρουσε", ["Il. 3.379", "Il. 21.33"], "(reviewer: αὐτὰρ ὃ ἂψ ἐπόρουσε)"),
    (32, "αὐτὰρ ὃ ἂψ ἐπόρουσε (unclaimed)", "ngram", "αὐτὰρ ὃ ἂψ ἐπόρουσε", ["Il. 3.379", "Il. 21.33"], "(reviewer)"),
    # 33
    (33, "τοῖιν δʼ", "ngram", "τοῖιν δ᾽", ["Il. 13.66"], "count 2 (Il. 13.66; Od. 18.34 τοῖϊν δέ)"),
    (33, "τοῖιν δέ (unelided)", "ngram", "τοῖιν δέ", ["Od. 18.34"], "Od. 18.34"),
    (33, "τοῖιν", "loose", "τοιιν", ["Il. 11.110", "Il. 13.66", "Il. 23.336", "Od. 18.34"], "4x"),
    (33, "φίλα γυῖα λέλυνται", "ngram", "φίλα γυῖα λέλυνται", ["Od. 8.233", "Od. 18.242"], "2x"),
    (33, "δʼ ἀργαλέῳ (unclaimed)", "ngram", "δ᾽ ἀργαλέῳ", ["Il. 15.10", "Il. 16.109"], "(reviewer)"),
    # 34
    (34, "ὀψὲ δὲ δὴ", "ngram", "ὀψὲ δὲ δὴ", ["Il. 7.94", "Il. 7.399", "Il. 8.30"], "12x, all line-initial"),
    (34, "παρέλασσʼ", "ngram", "παρέλασσ᾽", ["Il. 23.382", "Il. 23.527"], "2x, both 3.5-5"),
    (34, "παρέλασσε (verse form)", "loose", "παρελασσε", [], "(written unelided in the verse)"),
    (34, "παρελασ- (all)", "loose_sub", "παρελασ", [], "(reviewer)"),
    (34, "βοὴν ἀγαθὸς", "ngram", "βοὴν ἀγαθὸς", ["Il. 2.408"], "43x"),
    (34, "δὴ τότʼ ἔπειτʼ ἠρᾶτο βοὴν ἀγαθὸς Διομήδης", "ngram", "δὴ τότ᾽ ἔπειτ᾽ ἠρᾶτο βοὴν ἀγαθὸς Διομήδης", ["Il. 5.114"], "aorist at 4-5.5 + name formula 6-12"),
    # 35-36
    (35, "λαοὶ δʼ ἀμφοτέροισιν ἐπήπυον ἀμφὶς ἀρωγοί", "ngram", "λαοὶ δ᾽ ἀμφοτέροισιν ἐπήπυον ἀμφὶς ἀρωγοί", ["Il. 18.502"], "Il. 18.502 verbatim"),
    (36, "κήρυκες δʼ ἄρα λαὸν ἐρήτυον", "ngram", "κήρυκες δ᾽ ἄρα λαὸν ἐρήτυον", ["Il. 18.503"], "1-8"),
    (36, "ἔνθα καὶ ἔνθα", "ngram", "ἔνθα καὶ ἔνθα", ["Il. 2.476", "Il. 2.812", "Il. 7.156", "Il. 10.264"], "32x; 21 at 9-12"),
    (36, "ἡγεμόνες διεκόσμεον ἔνθα καὶ ἔνθα", "ngram", "ἡγεμόνες διεκόσμεον ἔνθα καὶ ἔνθα", ["Il. 2.476"], "parallel"),
    (36, "λαὸν ἐρήτυον τὼ (rejected test)", "ngram", "ἐρήτυον", ["Il. 18.503"], "(the verb's Homeric uses)"),
    # 38
    (38, "καί νύ κεν ἔνθʼ", "ngram", "καί νύ κεν ἔνθ᾽", ["Il. 5.311", "Il. 5.388", "Il. 8.90"], "3x, 1-3"),
    (38, "καί νύ κεν", "ngram", "καί νύ κεν", ["Il. 3.373", "Il. 5.311"], "16x, 14 at 1-2"),
    (38, "ἄσπετον ἤρατο κῦδος", "ngram", "ἄσπετον ἤρατο κῦδος", ["Il. 3.373", "Il. 18.165"], "2x, both in καί νύ κεν … εἰ μή"),
    (38, "ἔλαβεν", "ngram", "ἔλαβεν", ["Il. 17.620", "Od. 6.81", "Od. 17.326"], "3x: 5.5-7 2x, 1.5-3 1x"),
    # 40
    (40, "στῆ δὲ μάλʼ ἐγγὺς ἰών", "ngram", "στῆ δὲ μάλ᾽ ἐγγὺς ἰών", ["Il. 4.496", "Il. 5.611", "Il. 11.429", "Il. 12.457", "Il. 17.347"], "5x, all 1-5"),
    (40, "ὃ δέ μιν", "ngram", "ὃ δέ μιν", ["Il. 5.304", "Il. 13.176", "Il. 13.387", "Il. 15.551"], "9x, 8 at 5.5-7"),
    (40, "βάλεν οὐδʼ ἀφάμαρτε", "ngram", "βάλεν οὐδ᾽ ἀφάμαρτε", ["Il. 11.350", "Il. 13.160"], "2x, 1.5-5.5 (here 7.5-12)"),
    (40, "οὐδʼ ἀφάμαρτε", "ngram", "οὐδ᾽ ἀφάμαρτε", ["Il. 14.403", "Il. 22.290", "Il. 11.350", "Il. 13.160"], "4x: 9-12 2x, 3-5.5 2x"),
    # 49
    (49, "ἔκφερʼ", "ngram", "ἔκφερ᾽", ["Il. 23.259", "Il. 23.759", "Il. 23.785"], "3x: 1-1.5, 3-3.5, 9-9.5"),
    (49, "ἔκφερεν", "ngram", "ἔκφερεν", ["Od. 15.470"], "1x line-initial (here 3-4)"),
    (49, "ὃ δʼ ἐπέσσυτο", "ngram", "ὃ δ᾽ ἐπέσσυτο", ["Il. 21.234", "Il. 21.601"], "2x, 5.5-8"),
    (49, "τυτθὸν ὀπίσσω", "ngram", "τυτθὸν ὀπίσσω", ["Il. 5.443"], "1x, 9-12"),
    (49, "τυτθὸν", "ngram", "τυτθὸν", ["Il. 5.443", "Il. 1.354", "Il. 6.222"], "29x; 9-9.5 the commonest slot"),
    (49, "ὃ δʼ ἕσπετο (removed)", "ngram", "ὃ δ᾽ ἕσπετο", [], "0x (critic m8)"),
    # 54
    (54, "δύο κῆρε", "ngram", "δύο κῆρε", ["Il. 8.70", "Il. 22.210"], "2x"),
    (54, "μάχης", "ngram", "μάχης", ["Il. 7.26", "Il. 8.171", "Il. 2.391"], "71x; at 6-7"),
    (54, "μάχης ἑτεραλκέα νίκην", "ngram", "μάχης ἑτεραλκέα νίκην", ["Il. 7.26"], "μάχης at 6-7 before a 7.5-12 phrase"),
    (54, "θαλερῶν αἰζηῶν", "ngram", "θαλερῶν αἰζηῶν", ["Il. 10.259", "Il. 14.4"], "2x, 7.5-12"),
    (54, "αἰζηῶν", "loose", "αιζηων", ["Il. 2.660", "Il. 4.280", "Il. 5.92", "Il. 8.298", "Il. 10.259", "Il. 14.4", "Il. 15.315", "Il. 20.167"], "11x, all verse-final"),
    (54, "Τρώων θʼ ἱπποδάμων καὶ Ἀχαιῶν χαλκοχιτώνων", "ngram", "Τρώων θ᾽ ἱπποδάμων καὶ Ἀχαιῶν χαλκοχιτώνων", ["Il. 8.71"], "the two parties' genitives after the scales line"),
    (54, "τανηλεγέος θανάτοιο (removed)", "ngram", "τανηλεγέος θανάτοιο", ["Il. 8.70", "Il. 22.210"], "(critic M5)"),
    # 56
    (56, "ἕλκε δὲ μέσσα λαβών ῥέπε δʼ", "ngram", "ἕλκε δὲ μέσσα λαβών ῥέπε δ᾽", ["Il. 8.72", "Il. 22.212"], "2x, 1-7"),
    (56, "ῥέπε δʼ αἴσιμον ἦμαρ Ἀχαιῶν", "ngram", "ῥέπε δ᾽ αἴσιμον ἦμαρ Ἀχαιῶν", ["Il. 8.72"], "the same formula for a defeat"),
    (56, "ἐέλδωρ", "loose", "εελδωρ", ["Il. 1.41", "Il. 1.455", "Il. 1.504", "Il. 8.242", "Il. 15.74", "Il. 16.238", "Od. 3.418", "Od. 17.242"], "10x, all 10-12"),
    (56, "τελευτηθῆναι ἐέλδωρ", "ngram", "τελευτηθῆναι ἐέλδωρ", ["Il. 15.74"], "a hero's ἐέλδωρ with his name in the genitive"),
    (56, "τότʼ", "ngram", "τότ᾽", ["Il. 5.502", "Il. 6.314", "Il. 9.131"], "at 9.5 before a vowel (count field 3)"),
    (56, "Ἀτρεΐδης", "ngram", "Ἀτρεΐδης", ["Il. 14.29"], "5x at 7-9 (count field 5; the recorded query is `--loose ατρειδης --word`)"),
    (56, "ἀντιθέου", "ngram", "ἀντιθέου", ["Od. 20.369"], "LSSL at 7-9"),
    (56, "κακὸν ἦμαρ (removed)", "ngram", "κακὸν ἦμαρ", [], "(critic M5)"),
    # 58
    (58, "ἕτερος", "loose", "ετεροσ", ["Od. 8.374", "Od. 9.302", "Il. 5.258", "Il. 24.528"], "4x: 1.5-3, 5.5-7, 7.5-9 2x"),
    (58, "τὴν ἕτερος", "ngram", "τὴν ἕτερος", ["Od. 8.374"], "1.5-3"),
    (58, "μετέπειτα", "ngram", "μετέπειτα", ["Il. 14.310", "Od. 10.519"], "5x: 3.5-5.5 1x, 5.5-7.5 3x, 9.5-12 1x"),
    (58, "μάλα σχεδὸν ἦλθε διώκων", "ngram", "μάλα σχεδὸν ἦλθε διώκων", ["Il. 23.499"], "6-12"),
    (58, "μάλα σχεδὸν", "ngram", "μάλα σχεδὸν", ["Il. 5.607", "Il. 11.116", "Il. 23.499"], "8x, 6 at 6-8"),
    (58, "νηλεὲς ἦμαρ (removed)", "ngram", "νηλεὲς ἦμαρ", ["Il. 11.484", "Il. 13.514"], "(critic M5)"),
    # 61
    (61, "ἤμβροτες οὐδʼ ἔτυχες", "ngram", "ἤμβροτες οὐδ᾽ ἔτυχες", ["Il. 5.287"], "1-5"),
    (61, "ἤμβροτες", "ngram", "ἤμβροτες", ["Il. 5.287", "Il. 22.279"], "2x, both 1-2"),
    (61, "Ἀχιλεῦ", "ngram", "Ἀχιλεῦ", ["Il. 11.606", "Il. 24.503", "Il. 24.661"], "13x (coinages); 3 at 5.5-7 (count field 3)"),
    (61, "Φεδερεῦ", "loose", "φεδερευ", [], "0 hits (coinages)"),
    (61, "Ὀδυσεῦ", "ngram", "Ὀδυσεῦ", [], "named in `coinages`"),
    (61, "ἔνθʼ ἄρα τοι Πάτροκλε", "ngram", "ἔνθ᾽ ἄρα τοι Πάτροκλε", ["Il. 16.787"], "the narrator's apostrophe"),
    (61, "οὐδὲ σέθεν Μενέλαε", "ngram", "οὐδὲ σέθεν Μενέλαε", ["Il. 4.127"], "apostrophe"),
    (61, "ἐξενάριξας", "ngram", "ἐξενάριξας", ["Il. 16.692"], "apostrophe (16.692-693)"),
    (61, "Πατρόκλεις", "ngram", "Πατρόκλεις", ["Il. 16.693"], "apostrophe (16.692-693)"),
    (61, "μάλα πολλὰ", "ngram", "μάλα πολλὰ", ["Il. 1.156", "Il. 2.255", "Il. 8.22"], "20x: 7.5-9.5, 3.5-5.5"),
    (61, "πολλὰ μογήσας", "ngram", "πολλὰ μογήσας", ["Il. 2.690", "Il. 23.607", "Od. 2.343", "Od. 3.232", "Od. 5.449", "Od. 6.175", "Od. 7.147", "Od. 15.489"], "13x, all 9-12"),
    (61, "μάλα πολλὰ μογήσας (verse 7.5-12)", "ngram", "μάλα πολλὰ μογήσας", [], "(reviewer)"),
    (61, "πολλὰ πάθες καὶ πολλὰ μόγησας", "ngram", "πολλὰ πάθες καὶ πολλὰ μόγησας", ["Il. 23.607"], "2nd person, πολλὰ μόγησας at 9-12"),
    # 62
    (62, "τῷ δʼ", "ngram", "τῷ δ᾽", ["Il. 1.250"], "148x"),
    (62, "ἀντιθέῳ", "ngram", "ἀντιθέῳ", ["Il. 4.377", "Il. 5.629", "Il. 16.649"], "11x: 3-5, 7-9, 1-3"),
    (62, "τότε δὴ", "ngram", "τότε δὴ", ["Il. 1.92", "Il. 8.69", "Od. 9.52"], "43x; at 5.5-7 after a word ending at 5, 'e.g. Od. 9.52'"),
    (62, "τότε δὴ at 5.5-7 (reviewer)", "ngram", "τότε δὴ", ["Il. 10.366", "Il. 23.374"], "(reviewer: the two hits at 5.5-7)"),
    (62, "τότε δὴ Ζεὺς", "ngram", "τότε δὴ Ζεὺς", ["Od. 3.132"], "1.5-4"),
    (62, "Ζεὺς κῦδος ἔδωκε", "ngram", "Ζεὺς κῦδος ἔδωκε", ["Il. 8.216"], "8-12"),
    (62, "κῦδος ἔδωκε", "ngram", "κῦδος ἔδωκε", ["Il. 8.216", "Il. 18.456", "Il. 19.414"], "3x, all 9-12"),
    (62, "Ἕκτορι κῦδος ἔδωκε", "ngram", "Ἕκτορι κῦδος ἔδωκε", ["Il. 18.456", "Il. 19.414"], "2x, 7-12"),
    (62, "δὴ Ζεὺς κῦδος (unclaimed)", "ngram", "δὴ Ζεὺς κῦδος", ["Il. 12.437"], "(reviewer: after ὣς μὲν τῶν ἐπὶ ἶσα μάχη τέτατο, Il. 12.436)"),
    (62, "ἐπὶ ἶσα μάχη τέτατο πτόλεμός τε", "ngram", "ἐπὶ ἶσα μάχη τέτατο πτόλεμός τε", ["Il. 12.436", "Il. 15.413"], "(reviewer: the line before Il. 12.437)"),
    (29, "ὑπʼ ἀνδροφόνοιο Λυκούργου (reviewer)", "ngram", "ὑπ᾽ ἀνδροφόνοιο Λυκούργου", ["Il. 6.134"], "(reviewer: ὑπό + epithet + name genitive at 10-12)"),
    # 63
    (63, "ὣς οἳ μὲν μάρναντο", "ngram", "ὣς οἳ μὲν μάρναντο", ["Il. 11.596", "Il. 13.673", "Il. 17.366", "Il. 17.424", "Il. 18.1"], "5x, all 1-5.5"),
    (63, "ὣς οἳ μὲν", "ngram", "ὣς οἳ μὲν", ["Il. 1.318", "Il. 5.84"], "50x"),
    (63, "Διὸς δʼ ἐτελείετο βουλή", "ngram", "Διὸς δ᾽ ἐτελείετο βουλή", ["Il. 1.5", "Od. 11.297"], "2x, 6-12"),
    (63, "δέμας πυρὸς αἰθομένοιο (removed)", "ngram", "δέμας πυρὸς αἰθομένοιο", ["Il. 11.596", "Il. 13.673", "Il. 18.1"], "6-12 (and 17.366)"),
    # M8 parallels (37, 59: καὶ βάλεν at 9-10; 55: τὴν δʼ αὖ at 6-7)
    (37, "καὶ βάλεν", "ngram", "καὶ βάλεν", ["Il. 3.347", "Il. 11.350", "Il. 13.160"], "11x, all 1-2"),
    (37, "καὶ σάκος", "ngram", "καὶ σάκος", ["Il. 10.257", "Od. 14.277", "Il. 15.125", "Il. 15.474"], "1-2 (Il. 10.257, Od. 14.277), 9-10 (Il. 15.125, 15.474)"),
    (37, "ἔνθα δὲ", "ngram", "ἔνθα δὲ", ["Il. 2.550", "Il. 6.245", "Il. 6.249", "Il. 18.497"], "1-2 13x (e.g. Il. 2.550), 9-10 (Il. 6.245, 6.249, 18.497)"),
    (37, "αἶψα δʼ", "ngram", "αἶψα δ᾽", ["Il. 1.387", "Il. 6.514", "Il. 18.532"], "1-2 17x, 9-10 (Il. 1.387, 6.514, 18.532)"),
    (37, "αὖτις δὲ μνηστῆρες ἀκόντισαν", "ngram", "αὖτις δὲ μνηστῆρες ἀκόντισαν", ["Od. 22.272"], "round-3 correction: αὖτις of a second cast"),
    (37, "καὶ βάλεν αὖτις", "ngram", "καὶ βάλεν αὖτις", [], "(not claimed as attested)"),
    (55, "τὴν δʼ αὖ", "ngram", "τὴν δ᾽ αὖ", ["Od. 1.213", "Od. 1.230", "Od. 2.371", "Od. 21.343"], "13x, all 1-2 (here 6-7)"),
    (55, "τὴν δʼ (at 6-7)", "ngram", "τὴν δ᾽", ["Il. 22.211"], "'τὴν δʼ 130x: 5 at 7' (entry 9); at 6 in Il. 22.211"),
    (55, "τὸν δʼ (at 6-7)", "ngram", "τὸν δ᾽", ["Il. 2.396", "Il. 2.701"], "τὸν δʼ at 6-7 (M8 parallel)"),
    (55, "τὴν δʼ Ἕκτορος", "ngram", "τὴν δ᾽ Ἕκτορος", ["Il. 22.211"], "6-8 (entry 9, labelled ATTESTED-EXACT)"),
    (55, "* δʼ αὖ (pronoun at 6)", "ngram", "* δ᾽ αὖ", [], "'pronoun + δʼ αὖ at 6-7 is Homeric 6x' (modifications); round 3: 4x"),
    (55, "δʼ αὖ", "ngram", "δ᾽ αὖ", ["Il. 8.324"], "110x: 68 at 2, 28 at 3, 6 at 7, 5 at 5, 3 at 1.5 (notes)"),
    (55, "κρατεροῖο", "loose", "κρατεροιο", ["Il. 13.60", "Il. 13.415", "Il. 23.848", "Od. 11.277"], "7x: 9.5-12 4x, 7.5-9.5 3x (round-3 correction)"),
    (55, "Πολυποίταο κρατεροῖο", "ngram", "Πολυποίταο κρατεροῖο", ["Il. 23.848"], "5.5-12 (round-3 correction)"),
    # record-only changes
    (41, "ἐπόρουσε βοὴν ἀγαθὸς Διομήδης", "ngram", "ἐπόρουσε βοὴν ἀγαθὸς Διομήδης", ["Il. 5.432"], "3.5-12 (round-3 correction)"),
    (41, "τρὶς μὲν ὀρέξατʼ ἰών", "ngram", "τρὶς μὲν ὀρέξατ᾽ ἰών", ["Il. 13.20"], "the τρὶς μέν line with τὸ δὲ τέτρατον (round-3 correction)"),
    (41, "τρὶς μὲν ἔπειτʼ ἐπόρουσε", "ngram", "τρὶς μὲν ἔπειτ᾽ ἐπόρουσε", ["Il. 5.436", "Il. 16.784", "Il. 20.445"], "3x, 1-5.5"),
    (41, "τρὶς δʼ (the intervening line)", "regex", r"τρὶς δ", ["Il. 5.437", "Il. 16.785", "Il. 20.446"], "a τρὶς δέ line between the τρὶς μέν line and ἀλλʼ ὅτε δὴ τὸ τέταρτον"),
    (60, "αὖθʼ ἱερεὺς", "ngram", "αὖθ᾽ ἱερεὺς", ["Il. 1.370"], "position 3-5 (round-3 correction)"),
    (15, "ἐνίκα", "loose", "ενικα", ["Il. 4.389", "Il. 5.807", "Il. 18.252", "Il. 20.410", "Il. 23.756", "Il. 23.680", "Il. 23.742", "Od. 3.121"], "8x: 5 verse-final, 3 fourth foot"),
]

COINED_STEMS = ["φεδερ", "ρογηρ", "ελβετ", "σερβ", "ζοκοβ", "νοβηκ", "νοβακ", "ζοκοβειδα", "ζοκοβειδε"]


def main(jsonl, evid, out_path):
    recs = [json.loads(l) for l in open(jsonl, encoding="utf-8") if l.strip()]
    ev = {r["n"]: r for r in json.load(open(evid, encoding="utf-8"))}
    res = {}

    # 1 + 11. forms with 0 Homeric hits and where they are disclosed
    vocab = Counter(w for ln in C.lines for w in ln.loose_tokens)
    zero = []
    for r in recs:
        marks = " ".join([c.get("form", "") for c in r.get("coinages") or []])
        coin_src = " ".join(s["text"] for s in r.get("sources", []) if s.get("status") == "COINAGE")
        mod_src = " ".join(s["text"] for s in r.get("sources", []) if s.get("status") == "ATTESTED-MODIFIED")
        mods = " ".join(m.get("homeric_parallel", "") for m in r.get("modifications") or [])
        for t in G.tokenize(G.nfc(r["text"])):
            w = G.loose(t.core)
            if vocab[w] == 0:
                zero.append({"n": r["n"], "form": t.core, "loose": w,
                             "in_coinages": w in L(marks), "in_coinage_entry": w in L(coin_src),
                             "named_in_modified_entry": w in L(mod_src),
                             "named_in_modifications": w in L(mods)})
    res["forms_with_0_homeric_hits"] = zero

    # 2. coined stems
    res["coined_stems_substring_hits"] = {s: len(C.loose(s)) for s in COINED_STEMS}

    # 10. every form listed in `coinages`, looked up in Homer
    cf = []
    for r in recs:
        for c in r.get("coinages") or []:
            form = re.sub(r"\(.*", "", c.get("form", "")).strip()
            for w in G.tokenize(G.nfc(form)):
                lw = G.loose(w.core)
                lh = C.loose(lw, word=True)
                eh = C.exact(w.core, word=True)
                cf.append({"n": r["n"], "form": w.core, "loose_hits": len(lh), "exact_hits": len(eh),
                           "loose_examples": [f"{h.citation}@{h.pos_start}-{h.pos_end}: {h.match} | {h.text}" for h in lh[:4]],
                           "coinage_text": c.get("form", "")})
    res["coinage_forms_in_homer"] = cf

    # 3. patronymic model (as v3)
    def rx(p):
        hs = C.regex(p)
        return {"total": len(hs), "positions": posc(hs),
                "hits": [f"{h.citation}@{h.pos_start}-{h.pos_end}: {h.match} | {h.text}" for h in hs[:12]]}
    res["patronymic"] = {
        "Πηλείδ (diphthong ει)": rx(r"Πηλείδ\w*"),
        "Πηλεΐδ (ε-ϊ)": rx(r"Πηλεΐδ\w*"),
        "Ἀμαρυγκ-": rx(r"Ἀμαρυγκ\w*"),
        "Ἀτρείδ (diphthong)": rx(r"Ἀτρείδ\w*"),
    }

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
        slots.append({"verse": n, "coined": coined, "verse_position": vpos,
                      "verse_prev": vw[vi - 1] if vi else None,
                      "verse_next": vw[vi + 1] if vi is not None and vi + 1 < len(vw) else None,
                      "model": model, "model_citation": cit, "model_in_line": mi is not None, "model_position": mpos,
                      "model_prev": ln.loose_tokens[mi - 1] if mi else None,
                      "model_next": ln.loose_tokens[mi + 1] if mi is not None and mi + 1 < len(ln.loose_tokens) else None,
                      "model_line": ln.text if ln else None, "same_position": vpos == mpos,
                      "model_form_positions_in_homer": posc(C.ngram([ml])), "condition": cond})
    res["name_slots"] = slots

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

    # 7. claims
    def run(kind, q):
        if kind == "ngram":
            return C.ngram(q)
        if kind == "loose":
            return C.loose(q, word=True)
        if kind == "loose_sub":
            return C.loose(q)
        if kind == "exact":
            return C.exact(q, word=True)
        return C.regex(q)
    claims = []
    for n, label, kind, q, cits, asserted in CLAIMS:
        hs = run(kind, q)
        hc = {h.citation: f"{h.pos_start}-{h.pos_end}" for h in hs}
        claims.append({"n": n, "label": label, "query": f"{kind} {q}", "total": len(hs), "positions": posc(hs),
                       "cited": {c: hc.get(c, "NOT A HIT") for c in cits},
                       "cited_lines": {c: LINE[c].text for c in cits if c in LINE},
                       "asserted": asserted,
                       "first_hits": [f"{h.citation}@{h.pos_start}-{h.pos_end}: {h.text}" for h in hs[:8]]})
    res["claims"] = claims

    # 8 + 13. accents: η + one consonant + ος (Νοβῆκος) and + ου (Νοβήκου)
    cons = "βγδζθκλμνξπρστφχψ"

    def acc(ending):
        circ, acute = Counter(), Counter()
        for ln in C.lines:
            for w in re.findall(r"[\w]+", G.nfc(ln.text)):
                if len(w) < 4 or not w.endswith(ending) or w[-3] not in cons:
                    continue
                base = U.normalize("NFD", w[-4])
                if base[0] not in "ηΗ":
                    continue
                if "͂" in base:
                    circ[w] += 1
                elif "́" in base:
                    acute[w] += 1
        return {"circumflex_types": len(circ), "circumflex_tokens": sum(circ.values()),
                "acute_types": len(acute), "acute_tokens": sum(acute.values()),
                "acute_examples": acute.most_common(10), "circumflex_examples": circ.most_common(10)}
    res["accent_eta_C_os"] = acc("ος")
    res["accent_eta_C_ou"] = acc("ου")

    # 9. αὖθʼ / αὖτʼ before a rough breathing (as v3)
    def rough(w):
        return "̔" in U.normalize("NFD", w[:2])
    asp = {"αὖθʼ + rough": 0, "αὖτʼ + rough": 0, "ἔνθʼ αὖθʼ": len(C.ngram("ἔνθ᾽ αὖθ᾽")), "ἔνθʼ αὖτʼ": len(C.ngram("ἔνθ᾽ αὖτ᾽"))}
    for ln in C.lines:
        t = G.norm_apostrophes(G.nfc(ln.text))
        for m in re.finditer(r"(?<!\w)αὖ([θτ])ʼ\s+(\w+)", t):
            if rough(m.group(2)):
                asp[("αὖθʼ" if m.group(1) == "θ" else "αὖτʼ") + " + rough"] += 1
    res["aspiration"] = asp

    # 12. check_line on every verse
    txt = "\n".join(r["text"] for r in recs) + "\n"
    tmp = Path(out_path).with_suffix(".verses.txt")
    tmp.write_text(txt, encoding="utf-8")
    cl = json.loads(subprocess.run([sys.executable, str(ROOT / "homer" / "check_line.py"), "--file", str(tmp), "--json"],
                                   capture_output=True, text=True).stdout)
    tmp.unlink()
    res["check_line"] = {"n_verses": cl["n_verses"], "n_flagged": cl["n_flagged"], "n_unmetrical": cl["n_unmetrical"],
                         "flagged": [(i + 1, v["flags"]) for i, v in enumerate(cl["verses"]) if v["flags"]],
                         "warnings": [(i + 1, [w["type"] + ":" + w.get("word", "") for w in v["warnings"]])
                                      for i, v in enumerate(cl["verses"]) if v["warnings"]]}

    # 14. slot shapes for Νοβήκου (genitive -ου, 3 syllables at 10-12) and Σέρβῳ (dative -ῳ at 1-2 before δʼ)
    gen = Counter()
    gen_ex = []
    dat = []
    for ln in C.lines:
        wp = ln.word_pos
        if not wp:
            continue
        toks = [t.core for t in G.tokenize(G.nfc(ln.text))]
        if len(toks) != len(wp):
            continue
        t, p = toks[-1], wp[-1]
        if p == "10-12" and t.endswith("ου") and t[0].isupper():
            gen[t] += 1
            if len(gen_ex) < 12:
                gen_ex.append(f"{ln.work}. {ln.book}.{ln.line}: {t}")
        if wp[0] == "1-2" and toks[0].endswith("ῳ") and len(toks) > 1 and G.loose(toks[1]) == "δʼ":
            dat.append(f"{ln.work}. {ln.book}.{ln.line}: {toks[0]} δʼ | {ln.text}")
    res["slot_gen_ou_10_12_capitalised"] = {"types": len(gen), "tokens": sum(gen.values()), "examples": gen_ex,
                                            "by_type": gen.most_common(15)}
    res["slot_dat_omega_1_2_before_de"] = {"count": len(dat), "examples": dat}

    # 15. mapping and changes
    res["mapping"] = [{"n": r["n"], "v3_line": r.get("v3_line"), "changed": r.get("changed"),
                       "critic_issue": r.get("critic_issue")} for r in recs]
    Path(out_path).write_text(json.dumps(res, ensure_ascii=False, indent=1), encoding="utf-8")
    bad = [c for c in claims if any(v == "NOT A HIT" for v in c["cited"].values())]
    print(f"claims: {len(claims)}, with a cited line that is not a hit: {len(bad)}")
    for c in bad:
        print("  ", c["n"], c["label"], {k: v for k, v in c["cited"].items() if v == "NOT A HIT"})
    print("zero-hit forms:", sorted({(z['n'], z['form'], z['in_coinages'], z['named_in_modifications']) for z in zero}))
    print("coinage forms with Homeric hits:", [(c["n"], c["form"], c["loose_hits"], c["exact_hits"]) for c in cf if c["loose_hits"] or c["exact_hits"]])
    print("slots not same:", [(s["verse"], s["coined"], s["model"], s["model_citation"], s["verse_position"], s["model_position"]) for s in slots if not s["same_position"]])
    print("check_line:", res["check_line"]["n_flagged"], res["check_line"]["n_unmetrical"])
    print("gen -ου at 10-12:", res["slot_gen_ou_10_12_capitalised"]["by_type"][:10])
    print("dat -ῳ δʼ at 1-2:", res["slot_dat_omega_1_2_before_de"]["count"])
    print("accent ου:", {k: v for k, v in res["accent_eta_C_ou"].items() if "examples" not in k}, res["accent_eta_C_ou"]["acute_examples"][:5], res["accent_eta_C_ou"]["circumflex_examples"][:5])


if __name__ == "__main__":
    main(*sys.argv[1:4])
