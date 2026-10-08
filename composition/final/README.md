# composition/final: the frozen poem

**poem.txt**: 64 dactylic hexameters in the Homeric Kunstsprache narrating the 2019 Wimbledon men's final (Djokovic d. Federer), one verse per line, Unicode NFC, polytonic. The text is draft v4 unchanged: `cmp composition/drafts/v4.txt composition/final/poem.txt` is silent (byte-identical).

**poem.jsonl**: one record per verse (64 lines), the schema of the drafts (`n`, `text`, `gloss`, `scansion`, `enjambment`, `sources` with citation / position / count / status / query, `modifications`, `coinages`, `name_formula`, `quantity`, `notes`, …) plus two fields per record: `final: true` and `frozen_from: "v4"`. The records carry the fourth-round record corrections; the `revision_note` of each corrected record ends with a one-sentence list of its final edits.

**record_edits.md**: the log of every correction applied to the v4 records (139 edits on 38 records), each with its source (the review item), the field, and the old and new value, followed by the 69 concordance queries that were rerun and asserted before the file was written.

**apply_record_corrections.py**: the script that builds poem.jsonl, poem.txt and record_edits.md from composition/drafts/v4.jsonl and v4.txt; rerunning it regenerates all three.

## The drafts and the rounds

| draft | verses | round | verdicts |
|---|---|---|---|
| composition/drafts/v1 | 55 | review/round_1.md (scansion_v1, provenance_v1, philology_v1) | 24/55 PASS |
| composition/drafts/v2 | 60 | review/round_2.md (…_v2) | 52/60 PASS |
| composition/drafts/v3 | 60 | review/round_3.md (…_v3); then the poem critic, review/critic_poem_v1.md (0 critical, 8 major) | 60/60 PASS |
| composition/drafts/v4 | 64 | review/round_4.md: review/scansion_v4.md (PASS 64), review/philology_v4.md (PASS 64), review/provenance_v4.md (PASS 55, QUERY 8, FAIL 1, every item in the records, none in the verse) | text frozen |
| composition/final | 64 | this directory: the v4 text with the record items applied; review/provenance_final.md (PASS 64, QUERY 0, FAIL 0) | final |

The brief is composition/brief.md (target about 50 verses; the poem has 64, recorded as an open note in review/round_4.md). The rulings applied in the rounds are review/round_1.md R1–R8, review/round_2.md R9–R12 and the brief's addenda A1–A2.

## What the final pass changed (records only)

* review/provenance_v4.md §2 and §9: 55/9 relabelled ATTESTED-MODIFIED (the FAIL); the QUERY items on 24, 29, 33, 34, 49, 56, 61, 62 (single words labelled exact relabelled as mobility or parallel; counts set to what the recorded query gives, with the subset stated in the entry text; the slot models Il. 12.350 Τεῦκρος, Il. 6.134 Λυκούργου and Il. 16.508 Γλαύκῳ δ᾽ cited for Σέρβος at 3-3.5, Νοβήκου at 10-12 and Σέρβῳ δ᾽ at 1-2; the Il./Od. order of 33/1's citation); the coinage note on πυμάτῃ (0 exact hits, 1 loose hit = the nominative πυμάτη of Il. 6.118, now cited); παρέλασσε listed in `coinages`; the unclaimed phrases ἂψ ἐπόρουσε (32), δ᾽ ἀργαλέῳ (33) and δὴ Ζεὺς κῦδος (62) claimed; the undercounts of the καὶ βάλεν parallels in 37 and 59 (ἔνθα δέ, αἶψα δ᾽ at 1-2: 31x each); 55's 'pronoun + δ᾽ αὖ at 6-7' 6x → 4x; the smaller count and position fixes of §9 (20/7, 38/0, 56/4, 58/0, 62/2); 40/3's citation text re-worded so that no citation parser reads '3-5.5' as Il. 5.5.
* review/scansion_v4.md 'Discrepancies' items 1–9: the mapping note on 23 (= v3 27 verbatim); 20's stale name-formula clause; 24's πύματον counts (8x: 6 + 2); 33's 'Il. 13.85 verbatim' → verbatim at 3-12; 56's ἐέλδωρ (9 at 10-12, 1 at 6-8); 62's τότε δή (at 5.5-7: Il. 10.366, 23.374) and the ἀντιθέῳ quantity basis; the stale notes of 50–51 after the drop of v3 47; the stale line numbers of 59; the once-attested licences (κρατεροῦ hiatus, 29; αὖ hiatus, 49) noted for the paper.
* review/philology_v4.md §5 'Record corrections': 58 (Il. 23.499: Diomedes is the leader, διώκων absolute 'driving'; the verse's 'pursue' is a sense shift, recorded); 54 (gloss 'two fates of the fight of lusty men'; κῆρε documented from Cunliffe κήρ 3 and LSJ κήρ II); the better models for 32 (αὐτὰρ ὃ ἂψ ἐπόρουσε, Il. 3.379 = 21.33; ἀμφήριστον ἔθηκεν unreal in Homer, actual here), 34 (the whole-verse frame ὀψὲ δὲ δὴ μετέειπε βοὴν ἀγαθὸς Διομήδης, Il. 7.399 = 9.31 = 9.696) and 24 (Il. 16.79 μάχῃ νικῶντες Ἀχαιούς; Il. 8.532, 11.660 ὁ/ὃ Τυδεΐδης); Il. 23.675 (ἐμῇς ὑπὸ χερσὶ δαμέντα, the beaten boxer) as the contest parallel for 29, with Il. 4.248 and 6.92 for the split genitive; Il. 2.96–98 for the heralds of 36; the resumptive-ἔπειτα reading of the count in 41–42 and its caveat (on the 'thereafter' reading the fourth point would be 364) as a note; the narrator-apostrophe note for 61 (both Homeric ἤμβροτες are framed taunts; the person switch is Il. 16.786 → 787); 49's τυτθὸν ὀπίσσω sense shift and Il. 21.601–604; 63's enjambment label (none: high stop); the punctuation notes on 27 and 35; Il. 7.428 = 7.431 for the whole-verse repeat 23 = 28; 51's print suggestion recorded, not applied (text frozen).
* A scan of every record for cross-references found further stale v3 line numbers (records 2, 8, 25, 28, 37, 41–45, 47, 48, 51, 53, 57, 60); corrected and logged as the same kind as scansion_v4 item 8.

Not changed: the verse text, the scansion blocks, the enjambment labels other than 63, and every entry the reviews passed.

## How to re-verify

```
source .venv/bin/activate
cmp composition/drafts/v4.txt composition/final/poem.txt                       # silent: byte-identical
python -I composition/final/apply_record_corrections.py                       # regenerates poem.jsonl, poem.txt, record_edits.md; asserts 69 concordance queries
python homer/check_line.py --file composition/final/poem.txt --json           # 64 verses, 0 flagged, 0 unmetrical
python -I review/provenance_check.py composition/final/poem.jsonl review/provenance_final_evidence.json   # 'CLI cross-check: 258 distinct queries, 0 mismatches'
python -I review/poem_density.py composition/final/poem.jsonl review/poem_density_final.json
python -I review/provenance_v4_extra.py composition/final/poem.jsonl review/provenance_final_evidence.json review/provenance_final_extra.json
python -I review/provenance_report_final.py                                   # review/provenance_final.md: PASS 64, QUERY 0, FAIL 0
```

Results of the final run (review/provenance_final.md): 64 verses, 297 source entries (ATTESTED-EXACT 151, ATTESTED-MODIFIED 146, NOT-ATTESTED 0; 31 COINAGE entries, coined names substituted into attested slots, every slot shown by the cited model line); 258 distinct recorded queries, 0 CLI mismatches; 631 cited lines, none lacking the claimed string; 82 of 82 quoted Homeric parallels found; every form with 0 Homeric hits listed in `coinages`; check_line 0 flagged. Density (unchanged text): n ≥ 2 coverage 81.9% [77.2, 86.2], 19 of 64 verses verbatim Homeric, 64/64 lines with an ATTESTED-EXACT formula of two or more words (95.3% not function words only).

Any single claim in the records can be checked with `python homer/concordance.py <the entry's query>`; positions are half-foot numbers 1 … 12 as in homer/scan.py.
