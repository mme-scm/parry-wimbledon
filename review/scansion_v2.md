# Scansion review: composition/drafts/v2.txt (60 verses)

Reviewer: scansion-verifier, 2026-10-07. Order of work: (1) text comparison of v2 with v1 (exact NFC string match); (2) independent scansion, syllable by syllable, of every verse whose text is not verbatim v1, with quantities justified from homer/dichrona.tsv, homer/dichrona_analogy.tsv, homer/digamma.tsv, homer/licences.tsv, homer/positions.tsv and concordance queries (appendix); for verbatim v1 verses the v1 appendix scansion (review/scansion_v1.md) stands; (3) only then `python homer/check_line.py --file composition/drafts/v2.txt --json`; (4) only then composition/drafts/v2.jsonl. Rulings applied: review/round_1.md R1-R3 and composition/brief.md Addendum A1. Invented names are checked for consistency, slot and the quantities they need; where a name has a dichronon (Ἑλβέτιος) its quantity is metre-only by brief §4.

## Summary

* Verdicts: **PASS 59, FAIL 1, QUERY 0** (of 60).
* FAIL: **56**. `αὖτ᾽` stands before the rough-breathing Ἑλβέτιος and must be `αὖθ᾽`. Homer writes αὖθ᾽ before a rough breathing 33 times and αὖτ᾽ never; line 24 of this draft writes αὖθ᾽ Ἑλβέτιος. The error is orthographic, not metrical. The corrected verse `ἔνθ᾽ αὖθ᾽ Ἑλβέτιος προΐει, βάλε δ᾽ ἂψ Ζοκοβείδης,` gives check_line SDDDDS, unique, tier 0, no flags (one warning: Ἑλβέτιος ι, metre-only).
* Text status: 29 verses are verbatim v1 (1-3, 6-14, 16-19, 21, 22, 25, 26, 31, 37, 45, 49-52, 59, 60). 26 of them were v1 PASS. The other three (19, 51, 52) were v1 QUERY on the name slot only, which R1/A1.1 now allows; they have no flag. Verses 38 and 46 differ from v1 38 and v1 43 only in the verse-final stop, and their scansion is unchanged. 29 verses are new or rewritten.
* All 60 are valid hexameters, each with a unique scansion. 59 are tier 0. Verse 46 is tier 1: the lengthening before μέγα of the verbatim Il. 22.163, as in v1.
* My scansion, the composer's scansion and check_line agree on all 60 verses: pattern and L/S string, plus, for the jsonl, syllables, word positions, word quantities, caesurae, bucolic diaeresis and licences. The jsonl `check_line` blocks (status, tier, flags, warning texts) equal a fresh run.
* check_line: 0 flagged, 0 unmetrical, exit 0. The new elision-before-digamma check is active (it flags the v1 35 wording, `εἰ μὴ ἄρʼ οἱ …`) and finds nothing in v2. By hand: no elision in v2 stands before a word in digamma.tsv or the pron3 list.
* **Spondaic fifth feet: 47 and 48** (flagged). 47 is Il. 22.164 verbatim (κατατεθνηῶτος; scansion.tsv marks it spondeiazon). 48 follows Il. 22.165 (δινηθήτην; Homer has the same pattern, SDDDSS). Each ends in a word of four or more syllables. The two are consecutive, as in the model. Baseline: 1364 of 27162 uniquely scanned Homeric lines (5.02%) have a spondaic fifth foot, and 73 such pairs are consecutive.
* Word ends (positions.tsv): no lexical word end at a position under 1%, so Hermann's bridge holds in all 60. The only orthographic word end at 7.5 is ἔπειτα | δέ in 41, which is Il. 5.139 verbatim; the lexical word end there is at 8. The only lexical word end under 2% is at 11 (1.45%), in λέων ὣς (38, = Il. 20.164). Every verse has a penthemimeral or a trochaic caesura.
* Naeke's bridge (lexical word end at 8 after a spondaic fourth foot): 27, 33, 55. This is inherent in an SLX name at 6-8 before a consonant (Ῥογῆρος, Νοβήκος). It occurs in 1904 of 27162 Homeric lines (7.01%), so it is noted, not flagged. In 24 and 43 the orthographic word end at 8 comes after the proclitic καί, and the lexical word end is at 7.
* Licences used (each attested for the same form in licences.tsv; Homeric counts from check_line):
  * correption: μοι (1; 318x), καί (4, 22; 2364x), λούεσθαι (18; 2x), ἀγρῷ (39; Il. 5.137 itself), ἐξάλλεται (42; Il. 5.142 itself), κεῖται (46; 22x);
  * hiatus: ὠκύ (35; 2x), ὃ (42; 15x);
  * hiatus_long: διαμετρητῷ (11; 1x), γυνή (47; 3x);
  * muta cum liquida: ἀμφιβρότην (8); before an initial cluster, Κρονίων (13; 41x) and κροαίνων (17; 2x);
  * digamma: οἱ (9, 35; 768x), ἶσα (13, 21, 26; 5x), ἶσος (37; 19x), εἰδώς (27, 44; 42x);
  * lengthening before a liquid: μέγα (46; 30x).

  No licence is used outside a form that has it in Homer. The licences that drew v1 queries are gone: the digamma of ἰσόθεος used to make position after -ς, and elision before ϝοι.
* Rulings: R2 holds. Ῥογῆρος (27, 33) stands after a short vowel-final τε and before κ/δ, so -ρος is long by position and needs no digamma; ἰσόθεος does not occur in v2. R3 holds. Ζοκοβίδης and Νοβάκος are absent; Ζοκοβείδης and Νοβήκος have no dichronon, so neither needs a metre-only quantity. The withdrawn δίς and ἐξενάριξε are absent from v2. (Whether R4-R6 are met in sense is for the other verifiers.)

## Invented names: consistency, slots, quantity basis

| name | shape | verses (slot) | quantity basis | verdict |
|---|---|---|---|---|
| Φεδερῆρος / -ον | SSLX | 14, 20, 30, 34 nom.; 29 acc. (all 9.5-12 after βοὴν ἀγαθός/-όν) | nature (ε ε η) | consistent, brief slot |
| Φεδερεύς | SSL | 4 (3.5-5 after διογενής, = διογενὴς Ὀδυσεύς Il. 10.340); 25, 32 (3.5-5) | nature | consistent, brief slot |
| Ῥογῆρος | SLX | 27, 33 (6-8 after τε; before κέρδεα / δεύτερον) | nature; -ρος long by position (ς+κ, ς+δ) | consistent, brief slot, R2 met |
| Ἑλβέτιος / -ίου | LSSL | 5, 12, 57 (1-3); 19, 24, 54, 56 (3-5); 51 gen. (3-5); 52 gen. (7-9) | ι short, metre-only (9 verses, each with a jsonl `quantity` entry "metre-only") | consistent; 3-5 and 7-9 allowed by R1/A1.1 (no flags) |
| Ζοκοβείδης | SSLL | 4 (after ἀντίθεος), 36, 53 (after κρατερός), 56 (bare, after ἂψ); all 9.5-12 | nature (ο ο ει η): no metre-only vowel | consistent; ζ always follows a long syllable (-ος at 9 three times, ἂψ at 9) |
| Ζοκοβεύς / -ῆος | SSL / SSLX | 23, 44 nom. (3.5-5 after αὖ); 51 gen. (9.5-12 after ἀντιθέου) | nature | consistent, brief slot |
| Σέρβος / -ον | LX; LS before a vowel | 10, 29, 38, 58 (1-2); 15 (9-9.5 before ἐνίκα: LS, the slot of Τεῦκρος Il. 8.273); 43 acc. Σέρβον (3-3.5 before ἀνῆκε: LS) | σέρ long by position (ρβ) | consistent; 9-9.5 and 3-3.5 are new slots, allowed by A1.1 (no flags) |
| Νοβήκος | SLX | 55 (6-8 after τε, before δεύτερον) | nature (ο η) + position (ς+δ) | consistent; new slot (A1 named 10-12), allowed by A1.1 (no flags) |

The diphthongal patronymic shape of Ζοκοβείδης (R3: "verify Πηλείδ-") is attested. A loose search merges Πηλείδ- with Πηλεΐδης, so I searched exactly: `--exact "Πηλείδ"` gives 1 hit, Il. 1.277 Πηλείδη (voc., at 3-5). The diphthongal -είδης/-είδην occurs also in Ἀτρείδης (Od. 15.52, 3-5) and Ἀμαρυγκείδην (Il. 4.517, 1.5-5). The nominative Πηλείδης itself is not attested; the jsonl cites Il. 1.277 correctly.

## Per-verse table

Patterns are feet 1-5 plus the sixth foot (S), as in homer/scansion.tsv. "mine" for new verses = the appendix below; for verbatim v1 verses = the v1 appendix. "composer" = `scansion.pattern` in v2.jsonl. "check_line" = fresh run. In every row the three agree.

| n | text vs v1 | mine = composer = check_line | licences | notes | verdict |
|---|---|---|---|---|---|
| 1 | = v1 1 | DDDDDS | correption@2(μοι) | unchanged, v1 PASS | **PASS** |
| 2 | = v1 2 | DSDDDS | - | unchanged, v1 PASS | **PASS** |
| 3 | = v1 3 | SSDSDS | - | unchanged, v1 PASS | **PASS** |
| 4 | new | DDDDDS | correption@6(καί) | ἀντίθεος ι S at 7.5, as in Il. 20.232, Od. 3.414, Od. 8.119, Il. 16.321 (all uniquely scanned; tool warns for the form only). Ζοκοβείδης has no dichronon. Lexical word ends at 3, 5.5 and 9: trochaic caesura after enclitic τε, as Ἀσσάρακός τε in Il. 20.232 | **PASS** |
| 5 | new | DDDDDS | - | Ἑλβέτιος ι S metre-only, 1-3. δ᾽ ἑτέρωθεν as Il. 20.164. ἐδύσετο τεύχεα καλά = Il. 3.328 / Od. 23.366 at 6-12; τεύχεα α S by the accent rule | **PASS** |
| 6 | = v1 6 | SSDSDS | - | unchanged, v1 PASS | **PASS** |
| 7 | = v1 7 | DDDSDS | - | unchanged, v1 PASS | **PASS** |
| 8 | = v1 8 | DDDDDS | muta_cum_liquida@3.5(ἀμφιβρότην) | unchanged, v1 PASS | **PASS** |
| 9 | = v1 9 | DDDDDS | digamma@6(οἱ) | unchanged, v1 PASS | **PASS** |
| 10 | = v1 10 | SDDDDS | - | unchanged, v1 PASS | **PASS** |
| 11 | = v1 11 | SSDSDS | hiatus_long@9(διαμετρητῷ) | unchanged, v1 PASS | **PASS** |
| 12 | = v1 12 | DSDDDS | - | unchanged, v1 PASS | **PASS** |
| 13 | = v1 13 | SDDDDS | digamma@4(ἶσα); muta_cum_liquida_initial@9.5(Κρονίων) | unchanged, v1 PASS | **PASS** |
| 14 | = v1 14 | DDDDDS | - | unchanged, v1 PASS | **PASS** |
| 15 | new | DDDDDS | - | ἀπήμβροτε at 6-8 as Il. 16.466, 16.477 (ἀ S dt 2/0). Σέρβος at 9-9.5 = LS before a vowel, the slot of Τεῦκρος (Il. 8.273); new slot, A1.1. ἐνίκα at 10-12 as Il. 4.389 etc. (ί L dt 8/0) | **PASS** |
| 16 | = v1 16 | DDDSDS | - | unchanged, v1 PASS | **PASS** |
| 17 | = v1 17 | DSSDDS | muta_cum_liquida_initial@9.5(κροαίνων) | unchanged, v1 PASS | **PASS** |
| 18 | = v1 18 | SSDSDS | correption@5.5(λούεσθαι) | unchanged, v1 PASS | **PASS** |
| 19 | = v1 19 | DDDDDS | - | unchanged; the v1 QUERY was the slot only (Ἑλβέτιος at 3-5), now allowed by R1/A1.1 with no flags | **PASS** |
| 20 | new | DDDDDS | - | same quantities as v1 20 (ἐξενάριξε → αὖτ᾽ ἐδάμασσε). ἐδάμασσε at 3.5-5.5 as Od. 11.171, 11.398, 22.246, 22.413 (ά S dt 7/0) | **PASS** |
| 21 | = v1 21 | DDDDDS | digamma@4(ἶσα) | unchanged, v1 PASS | **PASS** |
| 22 | = v1 22 | SDSDDS | correption@10(καί) | unchanged, v1 PASS | **PASS** |
| 23 | new | DDDDDS | - | πάλιν → ἄφαρ, same quantities. ἄφαρ at 5.5-6 as Il. 1.349 (ἄ S dt 32/0; final α S 3/0). Ζ follows αὖ, long by nature | **PASS** |
| 24 | new | SDDSDS | - | δάμασεν is an unattested form (δάμασε 1x, Il. 22.446, same slot 5.5-7; δάμασσεν 2x, Il. 5.106, 18.432). Both α S (analogy δαμα- 33 forms; Il. 22.446). The movable ν is load-bearing: σεν is long by ν+κ at 7, and without it the fourth longum would be short. No licence is involved; for the philologist. Ἑλβέτιος 3-5 after αὖθ᾽ (A1.1). Orthographic word end at 8 after καί, lexical at 7 | **PASS** |
| 25 | = v1 25 | DDDDDS | - | unchanged, v1 PASS | **PASS** |
| 26 | = v1 26 | SDDDDS | digamma@4(ἶσα) | unchanged, v1 PASS | **PASS** |
| 27 | new | DDDSDS | digamma@10(εἰδώς) | Ῥογῆρος at 6-8 after a short τε (single ρ: τε stays short); -ρος long by position before κ, so the v1 digamma problem (R2) is gone. κέρδεα εἰδώς = Il. 23.709 at 9-12 (α S by accent; ϝ blocks hiatus). Naeke: lexical word end at 8 after a spondaic fourth foot (7.0% of Homeric lines) | **PASS** |
| 28 | new | DDSDDS | - | same quantities as v1 28 (ὣς → αὖτ᾽). πέμπτον δ᾽ ὑπελείπετ᾽ ἄεθλον = Il. 23.615 at 6-12 (ὑ S dt 1/0) | **PASS** |
| 29 | new | SDDDDS | - | same quantities as v1 29 (ἐξενάριξε → αὖτ᾽ ἐδάμασσε) | **PASS** |
| 30 | new | DDDDDS | - | αὐτὰρ ὅ γ᾽ ἂψ = Od. 11.599 at 1-3; ἂψ long by ψ | **PASS** |
| 31 | = v1 31 | DDDDDS | - | unchanged, v1 PASS (= Il. 13.85) | **PASS** |
| 32 | new | DDDDDS | - | πάλιν → ἄφαρ, same quantities. ἄσπετον ἤρατο κῦδος at 7-12 = Il. 3.373, 18.165 | **PASS** |
| 33 | new | DDDSDS | - | as 27 to 8; δεύτερον αὖτις at 9-12 (5x, Il. 1.513). Naeke as 27 | **PASS** |
| 34 | new | DDDDDS | - | καί νύ κεν ἔνθ᾽ = Il. 5.311, 5.388 at 1-3 | **PASS** |
| 35 | new (v1 35 FAIL) | SDDDDS | digamma@2(οἱ); hiatus@5.5(ὠκύ) | the fix proposed in scansion_v1. μή stays long before ϝοι (εἰ μή οἱ, Il. 17.71, 22.203); nothing is elided before οἱ; ὠκὺ ἐτώσιον as Il. 14.407 | **PASS** |
| 36 | new | DDDDDS | - | στῆ δὲ μάλ᾽ ἐγγὺς ἰών at 1-5 (5x). βάλε δὲ at 5.5-7 as Il. 4.519, Od. 22.82; δέ long by position before κρ, as before Θρ in Il. 4.519. Ζοκοβείδης after -ος at 9 | **PASS** |
| 37 | = v1 37 | DDDDDS | digamma@10(ἶσος) | unchanged, v1 PASS | **PASS** |
| 38 | v1 38 minus final · | SDDDDS | - | scansion identical to v1 38 (PASS). λέων ὣς gives a lexical word end at 11 (1.45%), as in Il. 20.164 | **PASS** |
| 39 | new (= Il. 5.137) | DSDDDS | correption@5.5(ἀγρῷ) | verbatim; equals scansion.tsv. ἐπ᾽ εἰροπόκοις: εἶρος is not in digamma.tsv (no flag), and the pair is Homer's own | **PASS** |
| 40 | new (= Il. 5.138) | SSDDDS | - | verbatim; equals scansion.tsv | **PASS** |
| 41 | new (= Il. 5.139) | SDDDDS | - | verbatim; equals scansion.tsv. τε is long by position before σθ. Orthographic word end at 7.5 (ἔπειτα \| δέ), lexical word end at 8, as in Homer's line | **PASS** |
| 42 | new (= Il. 5.142) | DDDSDS | hiatus@2(ὃ); correption@10(ἐξάλλεται) | verbatim; equals scansion.tsv (βαθέης α S: analogy βαθε- 6 forms) | **PASS** |
| 43 | new | DDDSDS | - | Σέρβον at 3-3.5, LS before a vowel; new slot, A1.1. ἀνῆκε at 4-5.5 as Il. 5.405, 7.152. μένος καὶ θυμὸς ἀγήνωρ = Il. 20.174 at 6-12 (θυ L dt 215/0). Orthographic word end at 8 after καί, lexical at 7 | **PASS** |
| 44 | new (from v1 41) | DDDDDS | digamma@10(εἰδώς) | Ζοκοβεύς at 3.5-5 after αὖ. ἐπὶ δ᾽ ὄρνυτο at 5.5-8 = Il. 23.689, 23.759. κέρδεα εἰδώς as 27. ἔκφερε unelided (Homer has only ἔκφερ᾽, Il. 23.759); no metrical consequence | **PASS** |
| 45 | = v1 42 | DDDDDS | - | unchanged, v1 PASS | **PASS** |
| 46 | v1 43 minus final · | DSDDDS (tier 1) | lengthening_liquid@7(μέγα); correption@9.5(κεῖται) | = Il. 22.163; the tier-1 licence is Homer's own | **PASS** |
| 47 | new (= Il. 22.164) | DDSDSS | hiatus_long@5(γυνή) | **spondaic fifth foot** (τε long by θν, θνη long). Verbatim Homeric spondeiazon (scansion.tsv feature `spondeiazon`). κα, τα S (analogy κατα- 161 forms; the metre fixes them) | **PASS** (spondaic 5th flagged) |
| 48 | new (model Il. 22.165) | SDDDSS | - | **spondaic fifth foot** δι.νη; Il. 22.165 has the same pattern SDDDSS. δινηθήτην ῑ L (dt 1/0, Il. 22.165). Consecutive with 47, as in the model. πολλάκι at 3-4 is a new place for this word (Homer: 1-2 9x, 7-8 2x; the jsonl marks it ATTESTED-MODIFIED); word end at 4 is ordinary (15.8% lex.) | **PASS** (spondaic 5th flagged) |
| 49 | = v1 44 | DSDDDS | - | unchanged, v1 PASS | **PASS** |
| 50 | = v1 45 | DDDDDS | - | unchanged, v1 PASS | **PASS** |
| 51 | = v1 46 | DDSDDS | - | unchanged; the v1 QUERY was the slot only (Ἑλβετίου at 3-5), now allowed by R1/A1.1 with no flags | **PASS** |
| 52 | = v1 47 | DDDDDS | - | unchanged; the v1 QUERY was the slot only (Ἑλβετίου at 7-9), now allowed by R1/A1.1 with no flags | **PASS** |
| 53 | new | DDDDDS | - | v1 48 with Ζοκοβίδης → Ζοκοβείδης: same quantities, now by nature, so the metre-only ῑ is gone | **PASS** |
| 54 | new | DDDDDS | - | Ἑλβέτιος at 3-5 after ὅ γ᾽ (as 19). ἀμύνετο νηλεὲς ἦμαρ = Il. 11.484, 13.514 at 6-12 (ύ L dt 1/0) | **PASS** |
| 55 | new | DDDSDS | - | Νοβήκος at 6-8 after τε: SL by nature, -κος long by position before δ; new slot, A1.1. Naeke as 27. Unlike 27 and 33, there is no comma after ἀφάμαρτε (punctuation only) | **PASS** |
| 56 | new | SDDDDS | - | **αὖτ᾽ before the rough-breathing Ἑλβέτιος must be αὖθ᾽.** Homer has αὖθ᾽ before a rough breathing 33x and αὖτ᾽ 0x; line 24 has αὖθ᾽ Ἑλβέτιος; the cited model ἔνθ᾽ αὖτ᾽ Αἰνείας has a smooth breathing. Metre unaffected; the corrected verse scans identically (SDDDDS, tier 0, no flags) | **FAIL** |
| 57 | new | DDDDDS | - | ἀπήμβροτε δουρὶ φαεινῷ = Il. 16.466, 16.477 at 6-12 | **PASS** |
| 58 | new | SDDDDS | - | same quantities as v1 53 (ἐξενάριξε → αὖτ᾽ ἐδάμασσε). Διὸς δ᾽ ἐτελείετο βουλή = Il. 1.5 at 6-12 | **PASS** |
| 59 | = v1 54 | SSDDDS | - | unchanged, v1 PASS | **PASS** |
| 60 | = v1 55 | DDDDDS | - | unchanged, v1 PASS | **PASS** |

## Discrepancies with the composer's jsonl and with check_line

Scansion: **none**. On all 60 verses the jsonl `scansion` fields (pattern, quantities, syllables, word_positions, word_quantities, caesurae, bucolic_diaeresis, licences) equal the fresh check_line run and my scansion. The jsonl `check_line` blocks (status, tier, flags, warning texts) equal the fresh run. `changed` and `v1_line` agree with my text comparison: v2 38 and 46 count as changed because of punctuation.

Documentation and judgement:

1. **Verse 56** (the FAIL): the jsonl does not notice αὖτ᾽ before a rough breathing. Its own model, ἔνθ᾽ αὖτ᾽ Αἰνείας (Il. 5.541, 17.344), has a smooth-breathing name.
2. Verse 15: `name_formula` calls Σέρβος "LX at 9-9.5". In this slot the final syllable is short (βο is open before ἐνίκα), i.e. LS, as Τεῦκρος in the cited model Il. 8.273. Label only.
3. Verse 24: the `quantity` basis "δάμασε Il. 22.446 (verbatim form + movable ν)" is accurate for the quantities, but δάμασεν itself has 0 Homeric hits. The movable ν carries the metre (σεν long at 7). No metrical objection.
4. Verses 47, 48: the spondaic fifth feet are recorded in `quantity_notes` ("as the model"). That agrees with my flag.
5. Verses 27, 33, 55: Naeke's bridge is not mentioned in the jsonl. It is common enough (7.0%) that no action is needed; the note is for the record.
6. Quantity flags: the round 1 format discrepancy is resolved. Every check_line `quantity_unattested` warning in v2 has a matching jsonl `quantity` entry: Ἑλβέτιος/-ίου (9 verses, basis "metre-only"), δαΐφρονε, ἀντίθεος, ἀντιθέου, τεύχεα, κέρδεα, δάμασεν, ἀκοστήσας, ἀργαλέῳ, βαθέης and κατατεθνηῶτος. The cited parallels check out: θυμὸς ἀγήνωρ 24x; Αἰγύπτιος LLSS at Od. 2.15; Τεῦκρος at 9-9.5 in Il. 8.273; δάμασε SSL at 5.5-7 in Il. 22.446; Πηλείδη at Il. 1.277.
7. For the provenance verifier (these concern the Homeric parallels' positions, not the draft's scansion): ATTESTED-EXACT sources whose claimed position differs from the position in the draft are δὲ πρῶτος in 12 (claimed 3-5, draft 4-5.5), ἀμφοτέρω and πάλιν in 22 (claimed 1-3 and 6-7, draft 3-5 and 7.5-8), and καμάτῳ in 31 (claimed 3.5-5; the verse is Il. 13.85, where it stands at 5.5-7).
8. check_line passes all 60. My verdict differs only on 56, for a reason the tool does not test (aspiration of the elided consonant). That is not a scansion disagreement.

## Evidence commands (rerun from the repository root, `source .venv/bin/activate`)

* `python homer/check_line.py --file composition/drafts/v2.txt --json` (60 verses, 0 flagged, 0 unmetrical)
* `python homer/check_line.py "ἔνθ᾽ αὖθ᾽ Ἑλβέτιος προΐει, βάλε δ᾽ ἂψ Ζοκοβείδης,"` (SDDDDS, tier 0, no flags)
* `python homer/check_line.py "εἰ μὴ ἄρʼ οἱ βέλος ὠκὺ ἐτώσιον ἔκφυγε χειρός"` (flag elision_before_digamma: the check is active)
* αὖτ᾽ / αὖθ᾽ before a rough breathing: Python over homer/lines.tsv, consecutive word pairs, with the first word `αὖτʼ` or `αὖθʼ` and the rough breathing (U+0314, NFD) on the next word's initial vowel: αὖθʼ 33 (Il. 1.370 αὖθʼ ἱερεὺς, Il. 2.540 αὖθʼ ἡγεμόνευʼ …), αὖτʼ 0
* `python homer/concordance.py --ngram "ὅν ῥά τε ποιμὴν ἀγρῷ ἐπ᾽ εἰροπόκοις ὀΐεσσι"` (Il. 5.137); likewise 5.138, 5.139, 5.142, 22.163, 22.164; `awk -F'\t' '$1=="Il"&&$2=="22"&&($3=="164"||$3=="165")' homer/scansion.tsv` (DDSDSS and SDDDSS, both `spondeiazon`)
* `python homer/concordance.py --exact "Πηλείδ"` (1: Il. 1.277); `--regex "[Α-Ωἀ-ῼ]\w*[εέ]ίδη[ςνω]?\b"` (Ἀτρείδης Od. 15.52, Ἀμαρυγκείδην Il. 4.517)
* `python homer/concordance.py --ngram "ἀντίθεος"` (6; 4 at 7-9) and the scansion.tsv rows Il. 20.232, Od. 3.414, Od. 8.119, Il. 16.321 (ι S)
* `--ngram "δάμασεν"` (0), `--ngram "δάμασε"` (1, Il. 22.446@5.5-7), `--ngram "δάμασσεν"` (2)
* `--ngram` for ἀπήμβροτε (2, 6-8), ἐνίκα (8), ἄφαρ (34; Il. 1.349 at 5.5-6), δεύτερον αὖτις (5, 9-12), κέρδεα εἰδώς (Il. 23.709), ἀμύνετο νηλεὲς ἦμαρ (2, 6-12), πολλάκι (11: 1-2 9x, 7-8 2x), δινηθήτην (Il. 22.165), αὐτὰρ ὅ γ᾽ ἂψ (Od. 11.599), καί νύ κεν ἔνθ᾽ (3), ἀνῆκε (11; 4-5.5 2x), μένος καὶ θυμὸς ἀγήνωρ (Il. 20.174), ἐπὶ δ᾽ ὄρνυτο (2), ἔκφερε (0), ἤρατο κῦδος (2), ὑπελείπετ᾽ (Il. 23.615), βάλε δὲ (4), ἐγγὺς ἰών (5), θυμὸς ἀγήνωρ (24), ἔνθ᾽ αὖτ᾽ (12)
* Spondeiazon and Naeke baselines: `awk -F'\t' 'NR>1&&$4=="unique"{n++; if(substr($8,5,1)=="S")s++; if($19~/naeke/)k++} END{print s,k,n}' homer/scansion.tsv` (1364, 1904, 27162)

## Appendix: my scansion of the new and changed verses, syllable by syllable

The legend is as in scansion_v1.md:

* L long, S short, X final anceps.
* n = nature (η ω, diphthong, circumflex; ε ο short).
* p(..) = position, with the consonants.
* c = epic correption; h = hiatus; hl = long vowel kept in hiatus.
* d = digamma (homer/digamma.tsv) blocks hiatus or correption.
* m / mi = muta cum liquida inside a word / before an initial cluster leaves the vowel short.
* ll = lengthening before an initial liquid.
* dt = homer/dichrona.tsv, with the counts (L/S); an = dichrona_analogy.tsv; acc = accent rule; cc = concordance attestation (cited).
* MO = metre-only quantity of an invented name (brief §4).

Syllables are written with the consonants they are pronounced with (δἄ = δ᾽ ἄ). Verbatim v1 verses: see the appendix of review/scansion_v1.md under the v1 number given in the table.

**4** διογενὴς Φεδερεύς τε καὶ ἀντίθεος Ζοκοβείδης.  
DDDDDS: δι L dt(διογενής ι 13/0) · ο S n · γε S n · νὴς L n · Φε S n · δε S n · ρεύς L n · τε S n · καὶ S c · ἀν L p(ντ) · τί S cc(Il. 20.232, Od. 3.414, 8.119 at 7.5) · θε S n · ος L p(ς ζ) · Ζο S n · κο S n · βεί L n · δης X  
licences: correption@6(καί)

**5** Ἑλβέτιος δ᾽ ἑτέρωθεν ἐδύσετο τεύχεα καλά·  
DDDDDS: Ἑλ L p(λβ) · βέ S n · τι S MO · ος L p(ς δ) · δἑ S n · τέ S n · ρω L n · θε S n · νἐ S n · δύ L dt(13/0) · σε S n · το S n · τεύ L n · χε S n · α S acc+cc(Il. 3.328) · κα L dt(109/0) · λά X  
licences: -

**15** ἀλλ᾽ ὅτε δὴ τὸ τέταρτον ἀπήμβροτε, Σέρβος ἐνίκα.  
DDDDDS: ἀλ L p(λλ) · λὅ S n · τε S n · δὴ L n · τὸ S n · τέ S n · ταρ L p(ρτ) · το S n · νἀ S dt(2/0) · πήμ L n · βρο S n · τε S n · Σέρ L p(ρβ) · βο S n · σἐ S n · νί L dt(8/0) · κα X  
licences: -

**20** τρὶς δέ μιν αὖτ᾽ ἐδάμασσε βοὴν ἀγαθὸς Φεδερῆρος.  
DDDDDS: τρὶς L p(ς δ) · δέ S n · μι S dt(277/0) · ναὖ L n · τἐ S n · δά S dt(7/0) · μας L p(σσ) · σε S n · βο S n · ὴν L n · ἀ S dt(56/0) · γα S dt(56/0) · θὸς L p(ς φ) · Φε S n · δε S n · ρῆ L n · ρος X  
licences: -

**23** δεύτερον αὖ Ζοκοβεὺς ἄφαρ ἐσσυμένως λάβ᾽ ἄεθλον.  
DDDDDS: δεύ L n · τε S n · ρο S n · ναὖ L n · Ζο S n · κο S n · βεὺς L n · ἄ S dt(32/0) · φα S dt(3/0) · ρἐσ L p(σσ) · συ S dt(12/0) · μέ S n · νως L n · λά S dt(3/0) · βἄ S dt(27/0) · ε L p(θλ) · θλον X  
licences: -

**24** τὸν δ᾽ αὖθ᾽ Ἑλβέτιος δάμασεν καὶ δεύτερον αὖτις·  
SDDSDS: τὸν L p(ν δ) · δαὖ L n · θἙλ L p(λβ) · βέ S n · τι S MO · ος L p(ς δ) · δά S an(δαμα- S, 33 forms)+cc(δάμασε Il. 22.446) · μα S cc(Il. 22.446) · σεν L p(ν κ; movable ν) · καὶ L n · δεύ L n · τε S n · ρο S n · ναὖ L n · τις X  
licences: -

**27** καὶ βάλεν, οὐδ᾽ ἀφάμαρτε, Ῥογῆρος κέρδεα εἰδώς.  
DDDSDS: καὶ L n · βά S dt(44/0) · λε S n · νοὐ L n · δἀ S dt(4/0) · φά S dt(4/0) · μαρ L p(ρτ) · τε S n · Ῥο S n · γῆ L n · ρος L p(ς κ) · κέρ L p(ρδ) · δε S n · α S acc+cc(Il. 23.709)+d · εἰ L n · δώς X  
licences: digamma@10(εἰδώς)

**28** τέτρατον αὖτ᾽ ἔλαβεν· πέμπτον δ᾽ ὑπελείπετ᾽ ἄεθλον.  
DDSDDS: τέ L p(τρ) · τρα S dt(7/0) · το S n · ναὖ L n · τἔ S n · λα S dt(3/0) · βεν L p(ν π) · πέμ L p(μπ) · πτον L p(ν δ) · δὑ S dt(1/0) · πε S n · λεί L n · πε S n · τἄ S dt · ε L p(θλ) · θλον X  
licences: -

**29** Σέρβος δ᾽ αὖτ᾽ ἐδάμασσε βοὴν ἀγαθὸν Φεδερῆρον,  
SDDDDS: Σέρ L p(ρβ) · βος L p(ς δ) · δαὖ L n · τἐ S n · δά S dt · μας L p(σσ) · σε S n · βο S n · ὴν L n · ἀ S dt(27/0) · γα S dt(27/0) · θὸν L p(ν φ) · Φε S n · δε S n · ρῆ L n · ρον X  
licences: -

**30** αὐτὰρ ὅ γ᾽ ἂψ ἐδάμασσε βοὴν ἀγαθὸς Φεδερῆρος·  
DDDDDS: αὐ L n · τὰ S dt(706/0) · ρὅ S n · γἂψ L p(ψ) · ἐ S n · δά S dt · μας L p(σσ) · σε S n · βο S n · ὴν L n · ἀ S dt · γα S dt · θὸς L p(ς φ) · Φε S n · δε S n · ρῆ L n · ρος X  
licences: -

**32** ὀψὲ δὲ δὴ Φεδερεὺς ἄφαρ ἄσπετον ἤρατο κῦδος·  
DDDDDS: ὀ L p(ψ) · ψὲ S n · δὲ S n · δὴ L n · Φε S n · δε S n · ρεὺς L n · ἄ S dt · φα S dt · ρἄσ L p(σπ) · πε S n · το S n · νἤ L n · ρα S dt(3/0) · το S n · κῦ L n · δος X  
licences: -

**33** καὶ βάλεν, οὐδ᾽ ἀφάμαρτε, Ῥογῆρος δεύτερον αὖτις·  
DDDSDS: καὶ L n · βά S dt · λε S n · νοὐ L n · δἀ S dt · φά S dt · μαρ L p(ρτ) · τε S n · Ῥο S n · γῆ L n · ρος L p(ς δ) · δεύ L n · τε S n · ρο S n · ναὖ L n · τις X  
licences: -

**34** καί νύ κεν ἔνθ᾽ ἐδάμασσε βοὴν ἀγαθὸς Φεδερῆρος,  
DDDDDS: καί L n · νύ S dt(103/0) · κε S n · νἔν L p(νθ) · θἐ S n · δά S dt · μας L p(σσ) · σε S n · βο S n · ὴν L n · ἀ S dt · γα S dt · θὸς L p(ς φ) · Φε S n · δε S n · ρῆ L n · ρος X  
licences: -

**35** εἰ μή οἱ βέλος ὠκὺ ἐτώσιον ἔκφυγε χειρός.  
SDDDDS: εἰ L n · μή L n+d(ϝοι) · οἱ L n · βέ S n · λο S n · σὠ L n · κὺ S dt(6/0)+h · ἐ S n · τώ L n · σι S dt(5/0) · ο S n · νἔκ L p(κφ) · φυ S dt(8/0) · γε S n · χει L n · ρός X  
licences: digamma@2(οἱ); hiatus@5.5(ὠκύ)

**36** στῆ δὲ μάλ᾽ ἐγγὺς ἰών, βάλε δὲ κρατερὸς Ζοκοβείδης.  
DDDDDS: στῆ L n · δὲ S n · μά S dt(152/0) · λἐγ L p(γγ) · γὺ S dt(20/0) · σἰ S dt(87/0) · ών L n · βά S dt(80/0) · λε S n · δὲ L p(κρ) · κρα S dt(37/0) · τε S n · ρὸς L p(ς ζ) · Ζο S n · κο S n · βεί L n · δης X  
licences: -

**38** Σέρβος δ᾽ αὖθ᾽ ἑτέρωθεν ἐναντίον ὦρτο λέων ὣς  
SDDDDS: Σέρ L p(ρβ) · βος L p(ς δ) · δαὖ L n · θἑ S n · τέ S n · ρω L n · θε S n · νἐ S n · ναν L p(ντ) · τί S dt(17/0) · ο S n · νὦρ L p(ρτ) · το S n · λέ S n · ω L n · νὣς X  
licences: -

**39** ὅν ῥά τε ποιμὴν ἀγρῷ ἐπ᾽ εἰροπόκοις ὀΐεσσι  
DSDDDS: ὅν L p(ν ῥ) · ῥά S dt(60/0) · τε S n · ποι L n · μὴ L n · νἀγ L p(γρ) · ρῷ S c · ἐ S n · πεἰ L n · ρο S n · πό S n · κοις L n · ὀ S n · ΐ S dt(2/0) · εσ L p(σσ) · σι X  
licences: correption@5.5(ἀγρῷ)

**40** χραύσῃ μέν τ᾽ αὐλῆς ὑπεράλμενον οὐδὲ δαμάσσῃ·  
SSDDDS: χραύ L n · σῃ L n · μέν L p(ν τ) · ταὐ L n · λῆ L n · σὑ S dt(1/0) · πε S n · ράλ L p(λμ) · με S n · νο S n · νοὐ L n · δὲ S n · δα S dt(3/0) · μάσ L p(σσ) · σῃ X  
licences: -

**41** τοῦ μέν τε σθένος ὦρσεν, ἔπειτα δέ τ᾽ οὐ προσαμύνει,  
SDDDDS: τοῦ L n · μέν L p(ν τ) · τε L p(σθ) · σθέ S n · νο S n · σὦρ L p(ρσ) · σε S n · νἔ S n · πει L n · τα S dt(215/0) · δέ S n · τοὐ L n · προ S n · σα S dt(1/0) · μύ L dt(1/0) · νει X  
licences: -

**42** αὐτὰρ ὃ ἐμμεμαὼς βαθέης ἐξάλλεται αὐλῆς·  
DDDSDS: αὐ L n · τὰ S dt · ρὃ S n+h · ἐμ L p(μμ) · με S n · μα S dt(6/0) · ὼς L n · βα S an(βαθε- 6 forms)+cc(Il. 5.142) · θέ S n · η L n · σἐ L p(ξ) · ξάλ L p(λλ) · λε S n · ται S c · αὐ L n · λῆς X  
licences: hiatus@2(ὃ); correption@10(ἐξάλλεται)

**43** ὣς τότε Σέρβον ἀνῆκε μένος καὶ θυμὸς ἀγήνωρ·  
DDDSDS: ὣς L n · τό S n · τε S n · Σέρ L p(ρβ) · βο S n · νἀ S dt(11/0) · νῆ L n · κε S n · μέ S n · νος L p(ς κ) · καὶ L n · θυ L dt(215/0) · μὸ S n · σἀ S dt(29/0) · γή L n · νωρ X  
licences: -

**44** ἔκφερε δ᾽ αὖ Ζοκοβεύς, ἐπὶ δ᾽ ὄρνυτο κέρδεα εἰδώς.  
DDDDDS: ἔκ L p(κφ) · φε S n · ρε S n · δαὖ L n · Ζο S n · κο S n · βεύ L n · σἐ S n · πὶ S dt(503/0) · δὄρ L p(ρν) · νυ S dt(13/0) · το S n · κέρ L p(ρδ) · δε S n · α S acc+cc(Il. 23.709)+d · εἰ L n · δώς X  
licences: digamma@10(εἰδώς)

**46** ῥίμφα μάλα τρωχῶσι· τὸ δὲ μέγα κεῖται ἄεθλον  
DSDDDS: ῥίμ L p(μφ) · φα S dt(10/0) · μά S dt(314/0) · λα L p(τρ) · τρω L n · χῶ L n · σι S dt(1/0) · τὸ S n · δὲ L ll(μ) · μέ S n · γα S dt · κεῖ L n · ται S c · ἄ S dt · ε L p(θλ) · θλον X  
licences: lengthening_liquid@7(μέγα); correption@9.5(κεῖται)

**47** ἢ τρίπος ἠὲ γυνὴ ἀνδρὸς κατατεθνηῶτος·  
DDSDSS: ἢ L n · τρί S dt(1/0) · πο S n · σἠ L n · ὲ S n · γυ S dt(33/0) · νὴ L hl · ἀν L p(νδρ) · δρὸς L p(ς κ) · κα S an(κατα- 161 forms)+cc(Il. 22.164) · τα S cc(Il. 22.164) · τε L p(θν) · θνη L n · ῶ L n · τος X  
licences: hiatus_long@5(γυνή). Spondaic fifth foot (τε θνη).

**48** ὣς τὼ πολλάκι δὴ περὶ τέρματα δινηθήτην,  
SDDDSS: ὣς L n · τὼ L n · πολ L p(λλ) · λά S dt(8/0) · κι S dt(8/0) · δὴ L n · πε S n · ρὶ S dt(250/0) · τέρ L p(ρμ) · μα S dt(1/0) · τα S dt(1/0) · δι L dt(1/0, Il. 22.165) · νη L n · θή L n · την X  
licences: -. Spondaic fifth foot (δι νη).

**53** τρὶς μὲν ἔπειτ᾽ ἐπόρουσε θοῶς κρατερὸς Ζοκοβείδης,  
DDDDDS: τρὶς L p(ς μ) · μὲ S n · νἔ S n · πει L n · τἐ S n · πό S n · ρου L n · σε S n · θο S n · ῶς L n · κρα S dt(37/0) · τε S n · ρὸς L p(ς ζ) · Ζο S n · κο S n · βεί L n · δης X  
licences: -

**54** αὐτὰρ ὅ γ᾽ Ἑλβέτιος τότ᾽ ἀμύνετο νηλεὲς ἦμαρ·  
DDDDDS: αὐ L n · τὰ S dt · ρὅ S n · γἙλ L p(λβ) · βέ S n · τι S MO · ος L p(ς τ) · τό S n · τἀ S dt(1/0) · μύ L dt(1/0) · νε S n · το S n · νη L n · λε S n · ὲ S n · σἦ L n · μαρ X  
licences: -

**55** καὶ βάλεν, οὐδ᾽ ἀφάμαρτε Νοβήκος δεύτερον αὖτις·  
DDDSDS: καὶ L n · βά S dt · λε S n · νοὐ L n · δἀ S dt · φά S dt · μαρ L p(ρτ) · τε S n · Νο S n · βή L n · κος L p(ς δ) · δεύ L n · τε S n · ρο S n · ναὖ L n · τις X  
licences: -

**56** ἔνθ᾽ αὖτ᾽ Ἑλβέτιος προΐει, βάλε δ᾽ ἂψ Ζοκοβείδης,  
SDDDDS: ἔν L p(νθ) · θαὖ L n · τἙλ L p(λβ) · βέ S n · τι S MO · ος L p(ς πρ) · προ S n · ΐ S dt(20/0) · ει L n · βά S dt(80/0) · λε S n · δἂψ L p(ψ) · Ζο S n · κο S n · βεί L n · δης X  
licences: -. Orthography: τ᾽ before the rough Ἑ- must be θ᾽ (αὖθ᾽ Ἑλβέτιος, as in 24).

**57** Ἑλβέτιος δ᾽ ἄρα τοῦ μὲν ἀπήμβροτε δουρὶ φαεινῷ.  
DDDDDS: Ἑλ L p(λβ) · βέ S n · τι S MO · ος L p(ς δ) · δἄ S dt(545/0) · ρα S dt(408/0) · τοῦ L n · μὲ S n · νἀ S dt(2/0) · πήμ L n · βρο S n · τε S n · δου L n · ρὶ S dt(76/0) · φα S dt(24/0) · ει L n · νῷ X  
licences: -

**58** Σέρβος δ᾽ αὖτ᾽ ἐδάμασσε, Διὸς δ᾽ ἐτελείετο βουλή.  
SDDDDS: Σέρ L p(ρβ) · βος L p(ς δ) · δαὖ L n · τἐ S n · δά S dt · μας L p(σσ) · σε S n · Δι S dt(250/0) · ὸς L p(ς δ) · δἐ S n · τε S n · λεί L n · ε S n · το S n · βου L n · λή X  
licences: -
