# Scansion review: composition/drafts/v3.txt (60 verses)

Reviewer: scansion-verifier, 2026-10-07. Order of work:

1. Exact NFC string comparison of v3.txt with v2.txt, line by line.
2. Independent scansion by hand, syllable by syllable, of the seven changed verses (23, 33, 36, 44, 51, 55, 56). Quantities are justified from homer/dichrona.tsv, homer/dichrona_analogy.tsv, homer/digamma.tsv, homer/licences.tsv, homer/positions.tsv and concordance queries (appendix). Pattern, L/S string, word ends and licences were written down before any tool was run on the draft.
3. Only then `python homer/check_line.py --file composition/drafts/v3.txt --json`, plus a fresh run on v2.txt for the unchanged verses.
4. Only then composition/drafts/v3.jsonl.

Rulings applied: review/round_1.md R1-R3, review/round_2.md R9-R12, composition/brief.md Addenda A1 and A2. The R11 and R12 sense requirements (the counts, the subject of 37) are for the philologist. Here they are checked only for their metrical consequences.

## Summary

* Verdicts: **PASS 60, FAIL 0, QUERY 0** (of 60).
* **The v2 FAIL (56) is repaired.** The verse now reads `ἔνθ᾽ αὖθ᾽ Ἑλβέτιος`. Recount: Homer writes αὖθʼ before a rough breathing 33 times and αὖτʼ never. The scansion is the same as in v2 (SDDDDS, tier 0, no flags). No other elided τ/κ/π in v3 stands before a rough breathing.
* Text status:
  * Exactly the seven announced verses differ from v2: 23, 33, 36, 44, 51, 55, 56.
  * The other 53 are identical to v2 strings and were all v2 PASS. 56, the only v2 FAIL, is among the changed verses.
  * Both files are NFC.
  * A fresh check_line run on v2.txt gives output identical to the v3 run for all 53 unchanged verses, so the tool has not drifted since round 2.
* All 60 verses are valid hexameters, each with a unique scansion. 59 are tier 0. Verse 46 (unchanged) is tier 1, for the lengthening before μέγα in the verbatim Il. 22.163.
* On all seven changed verses, my scansion, the composer's and check_line's agree: pattern, L/S string, orthographic and lexical word ends, and licences. On all 60 verses, the jsonl `scansion` fields and `check_line` blocks equal the fresh run.
* check_line: 60 verses, 0 flagged, 0 unmetrical, exit 0.
* Digamma and elision. The elision-before-digamma check is active: it still flags the v1 35 wording `εἰ μὴ ἄρʼ οἱ …`. It finds nothing in v3. By hand:
  * The elisions in the changed verses are λάβ᾽ ἄεθλον (23), οὐδ᾽ ἀφάμαρτε (33, 55), ἔπειτ᾽ ἐπόρουσε (36), δ᾽ αὖτε and δ᾽ ἕσπετο (44), ἄρ᾽ Ἑλβετίου and δ᾽ αὖ (51), and ἔνθ᾽ αὖθ᾽, αὖθ᾽ Ἑλβέτιος and δ᾽ ἂψ (56).
  * None of the following words matches any row of digamma.tsv (its `re:`, `red:` and `form:` rules, pron3 included), tested programmatically on loose and form_key.
  * ἕσπετο (ἕπομαι) has no digamma, and Homer elides before it (Il. 12.398 ἣ δ᾽ ἕσπετο, Od. 1.125, Od. 8.109). λάβ᾽ ἄεθλον is Homer's own elision (Il. 23.511).
  * The only digamma word in the changed verses is εἰδώς (44), after unelided κέρδεα, = Il. 23.709. licences.tsv has the digamma for εἰδώς 42 times.
* **Spondaic fifth feet: 47 and 48** (unchanged, flagged as in v2). 47 = Il. 22.164, a verbatim spondeiazon. 48 has the pattern of Il. 22.165 (SDDDSS). None of the changed verses has a spondaic fifth foot. Baseline: 1364 of 27162 uniquely scanned Homeric lines (5.02%).
* Word ends against positions.tsv:
  * No verse has a lexical word end at 7.5, so Hermann's bridge holds in all 60.
  * In the changed verses, the rarest lexical word-end position is 6 (44 after ὃ, 51 after τήν): 9.67% lexical, 22.76% orthographic. Both verses also have a caesura at 5.5 or 5, so neither has the diaeresis_after_3rd_foot anomaly.
  * In the whole draft, the only lexical word end under 2% is still 38's λέων ὣς at 11 (1.45%, = Il. 20.164).
  * Every verse has a penthemimeral, trochaic or hephthemimeral caesura. In the changed verses: 23 and 36 trochaic + hephthemimeral; 33, 44 and 55 trochaic; 51 and 56 penthemimeral + hephthemimeral.
* Naeke's bridge (lexical word end at 8 after a spondaic fourth foot) occurs in 27, 33 and 55. It follows from an SLX name at 6-8 before a consonant. It occurs in 1904 of 27162 Homeric lines (7.01%), so it is noted, not flagged.
* Licences:
  * Changed verses: only digamma@10(εἰδώς) in 44, which v2 44 also had. None uses correption, hiatus, lengthening, synizesis or muta cum liquida.
  * Whole draft: the licence list is identical to v2's, each licence attested for the same form (counts in scansion_v2.md):
    * correption: μοι 1; καί 4, 22; λούεσθαι 18; ἀγρῷ 39; ἐξάλλεται 42; κεῖται 46
    * hiatus: ὠκύ 35; ὃ 42
    * hiatus_long: διαμετρητῷ 11; γυνή 47
    * muta cum liquida: ἀμφιβρότην 8; before an initial cluster, Κρονίων 13 and κροαίνων 17
    * digamma: οἱ 9, 35; ἶσα 13, 21, 26; ἶσος 37; εἰδώς 27, 44
    * lengthening before a liquid: μέγα 46
* Rulings, metrical side:
  * R9: Νοβῆκος has the circumflex in 44 and 55, and no acute Νοβήκος remains. The accent does not touch the quantity (η long either way).
  * R10 / A2.2: Ζοκοβεύς and Ζοκοβῆος occur nowhere in v3. Djokovic is Ζοκοβείδης (4, 23, 53, 56), Σέρβος/-ον/-ου (10, 15, 29, 38, 43, 51, 58) or Νοβῆκος (44, 55). The new slots (Νοβῆκος 4-5.5; Σέρβου 8-9) pass check_line with no flags and no licence, which A1.1 requires.
  * R12: 36 is a clean τρὶς μέν count line.
  * R11: 33 and 55 scan exactly as their v2 versions did, apart from the new second clause.
* Epithet economy: κρατερός stays with Djokovic (23 and 53 κρατερὸς Ζοκοβείδης; 51 Σέρβου κρατεροῖο). βοὴν ἀγαθός stays with Federer (14, 20, 29, 30, 34, 36).

## Invented names: consistency, slots, quantity basis

| name | shape | verses (slot) | quantity basis | verdict |
|---|---|---|---|---|
| Φεδερῆρος / -ον | SSLX | 14, 20, 30, 34, 36 nom.; 29 acc. (all 9.5-12 after βοὴν ἀγαθός/-όν) | nature (ε ε η) | consistent, brief slot; 36 is new and in the same slot |
| Φεδερεύς | SSL | 4, 25, 32 (3.5-5) | nature | unchanged |
| Ῥογῆρος | SLX (SLL before a consonant) | 27, 33 (6-8 after τε; before κέρδεα / καί) | nature; -ρος long by position (ς+κ) | consistent; R2 met (no digamma or ἰσόθεος) |
| Ἑλβέτιος / -ίου | LSSL | 5, 12, 57 (1-3); 19, 24, 54, 56 (3-5); 51 gen. (3-5); 52 gen. (7-9) | ι short, metre-only (9 verses, each with a jsonl `quantity` entry "metre-only") | consistent; slots allowed by R1/A1.1 |
| Ζοκοβείδης | SSLL | 4 (after ἀντίθεος), 23 and 53 (after κρατερός), 56 (bare, after ἂψ); all 9.5-12 | nature (ο ο ει η): no metre-only vowel | consistent; ζ always follows a syllable long at 9 (-ος three times, ἂψ once); the v2 36 occurrence has gone with R12 |
| Σέρβος / -ον / -ου | LX; LS before a vowel; gen. LL | 10, 29, 38, 58 (1-2); 15 (9-9.5, LS before ἐνίκα); 43 acc. (3-3.5, LS before ἀνῆκε); **51 gen. Σέρβου (8-9, LL before κρ)** | σέρ long by position (ρβ); gen. -ου by nature | consistent; Σέρβου is a new form in a new slot, allowed by A1.1 (no flags); LL words at 8-9 are common in Homer (922 instances) |
| Νοβῆκος | SLX: SLS before a vowel, SLL before a consonant | **44 (4-5.5 after δ᾽ αὖτε, before ὃ: SLS)**; 55 (6-8 after τε, before καί: SLL) | nature (ο η), final syllable by position or open | consistent; both slots follow a short vowel-final word, so ν makes no position; 4-5.5 is a new slot, allowed by A1.1 (no flags); model γυναῖκας after δ᾽ αὖτε (Od. 24.278) |
| Ζοκοβεύς / -ῆος | - | none (withdrawn: R10, A2.2) | - | - |

## Per-verse table

"pattern" = feet 1-5 plus the sixth foot (S), as in homer/scansion.tsv. For the changed verses it is the same in my hand scansion (appendix), the composer's `scansion.pattern` in v3.jsonl, and the fresh check_line run. For unchanged verses, the pattern and licences come from the fresh check_line run: they are identical to a fresh run on v2 and to the v2 jsonl, and the syllable-level scansion is in the appendices of review/scansion_v2.md and review/scansion_v1.md. "dt" = homer/dichrona.tsv (long/short counts).

| n | text vs v2 | pattern | licences | notes | verdict |
|---|---|---|---|---|---|
| 1 | = v2 1 | DDDDDS | correption@2(μοι) | unchanged, v2 PASS | **PASS** |
| 2 | = v2 2 | DSDDDS | - | unchanged, v2 PASS | **PASS** |
| 3 | = v2 3 | SSDSDS | - | unchanged, v2 PASS | **PASS** |
| 4 | = v2 4 | DDDDDS | correption@6(καὶ) | unchanged, v2 PASS | **PASS** |
| 5 | = v2 5 | DDDDDS | - | unchanged, v2 PASS | **PASS** |
| 6 | = v2 6 | SSDSDS | - | unchanged, v2 PASS | **PASS** |
| 7 | = v2 7 | DDDSDS | - | unchanged, v2 PASS | **PASS** |
| 8 | = v2 8 | DDDDDS | muta_cum_liquida@3.5(ἀμφιβρότην) | unchanged, v2 PASS | **PASS** |
| 9 | = v2 9 | DDDDDS | digamma@6(οἱ) | unchanged, v2 PASS | **PASS** |
| 10 | = v2 10 | SDDDDS | - | unchanged, v2 PASS | **PASS** |
| 11 | = v2 11 | SSDSDS | hiatus_long@9(διαμετρητῷ) | unchanged, v2 PASS | **PASS** |
| 12 | = v2 12 | DSDDDS | - | unchanged, v2 PASS | **PASS** |
| 13 | = v2 13 | SDDDDS | digamma@4(ἶσα);muta_cum_liquida_initial@9.5(Κρονίων) | unchanged, v2 PASS | **PASS** |
| 14 | = v2 14 | DDDDDS | - | unchanged, v2 PASS | **PASS** |
| 15 | = v2 15 | DDDDDS | - | unchanged, v2 PASS; jsonl label corrected to "LS at 9-9.5" (scansion_v2 note 2) | **PASS** |
| 16 | = v2 16 | DDDSDS | - | unchanged, v2 PASS | **PASS** |
| 17 | = v2 17 | DSSDDS | muta_cum_liquida_initial@9.5(κροαίνων) | unchanged, v2 PASS | **PASS** |
| 18 | = v2 18 | SSDSDS | correption@5.5(λούεσθαι) | unchanged, v2 PASS | **PASS** |
| 19 | = v2 19 | DDDDDS | - | unchanged, v2 PASS | **PASS** |
| 20 | = v2 20 | DDDDDS | - | unchanged, v2 PASS | **PASS** |
| 21 | = v2 21 | DDDDDS | digamma@4(ἶσα) | unchanged, v2 PASS | **PASS** |
| 22 | = v2 22 | SDSDDS | correption@10(καὶ) | unchanged, v2 PASS | **PASS** |
| 23 | changed (R10) | DDDDDS | - | δεύτερον αὖ at 1-3 (5x). λάβ᾽ ἄεθλον (Il. 23.511, 9.5-12) moved to 3.5-5.5: ἄεθλον stands at 4-5.5 as SLS 3x (Il. 23.892, Od. 21.91, Od. 23.261), ε long by θλ. λάβ᾽ ά S (dt 0/3; λάβε 0/24). ἄφαρ at 6-7 SL 15x, -φαρ long by ρκ. κρατερὸς at 7.5-9 30x (κρα S dt 0/37); -ρὸς long by ς+ζ at a longum (9). Ζοκοβείδης 9.5-12, nature. Word ends 2, 3, 3.5, 5.5, 7, 9 (3.5: 21.2% lexical); no bucolic. Elision λάβ᾽ before ἄεθλον is Homer's own (Il. 23.511) | **PASS** |
| 24 | = v2 24 | SDDSDS | - | unchanged, v2 PASS; jsonl now records δάμασεν as a modification and coinage (round 2) | **PASS** |
| 25 | = v2 25 | DDDDDS | - | unchanged, v2 PASS | **PASS** |
| 26 | = v2 26 | SDDDDS | digamma@4(ἶσα) | unchanged, v2 PASS | **PASS** |
| 27 | = v2 27 | DDDSDS | digamma@10(εἰδώς) | unchanged, v2 PASS; Naeke (lexical word end at 8 after a spondaic 4th foot) | **PASS** |
| 28 | = v2 28 | DDSDDS | - | unchanged, v2 PASS | **PASS** |
| 29 | = v2 29 | SDDDDS | - | unchanged, v2 PASS | **PASS** |
| 30 | = v2 30 | DDDDDS | - | unchanged, v2 PASS | **PASS** |
| 31 | = v2 31 | DDDDDS | - | unchanged, v2 PASS | **PASS** |
| 32 | = v2 32 | DDDDDS | - | unchanged, v2 PASS | **PASS** |
| 33 | changed (R11) | DDDSDS | - | καὶ βάλεν, οὐδ᾽ ἀφάμαρτε at 1-5.5 (Il. 11.350, 13.160). Ῥογῆρος 6-8 after short τε (single ρ, no lengthening), -ρος long by ς+κ before καί. καί at 9 long by nature before β; βάλεν at 9.5-10 SS 11x; αὖτις 11-12 LX 20x. Lexical word ends 2, 5.5, 8, 10. Naeke as 27. καὶ βάλεν at 9-10 is a new place for the pair (Homer 11x, all 1-2) and βάλεν αὖτις has 0 hits as a pair: no metrical consequence (for provenance) | **PASS** |
| 34 | = v2 34 | DDDDDS | - | unchanged, v2 PASS | **PASS** |
| 35 | = v2 35 | SDDDDS | digamma@2(οἱ);hiatus@5.5(ὠκὺ) | unchanged, v2 PASS | **PASS** |
| 36 | changed (R12) | DDDDDS | - | τρὶς μὲν ἔπειτ᾽ ἐπόρουσε = Il. 5.436, 16.784, 20.445 at 1-5.5 (ἐπόρουσε SSLS at 3.5-5.5 15x) + βοὴν ἀγαθὸς Φεδερῆρος at 6-12 (as 14, 20, 30, 34). τρὶς long by ς+μ; -θὸς long by ς+φ. Word ends 1.5, 3, 5.5, 7, 9. Elision ἔπειτ᾽ before ἐπόρουσε as in the three Homeric lines | **PASS** |
| 37 | = v2 37 | DDDDDS | digamma@10(ἶσος) | unchanged, v2 PASS | **PASS** |
| 38 | = v2 38 | SDDDDS | - | unchanged, v2 PASS; lexical word end at 11 (1.45%), λέων ὣς = Il. 20.164 | **PASS** |
| 39 | = v2 39 | DSDDDS | correption@5.5(ἀγρῷ) | unchanged, v2 PASS | **PASS** |
| 40 | = v2 40 | SSDDDS | - | unchanged, v2 PASS | **PASS** |
| 41 | = v2 41 | SDDDDS | - | unchanged, v2 PASS; orthographic word end at 7.5 (ἔπειτα \| δέ), lexical at 8, = Il. 5.139 | **PASS** |
| 42 | = v2 42 | DDDSDS | hiatus@2(ὃ);correption@10(ἐξάλλεται) | unchanged, v2 PASS | **PASS** |
| 43 | = v2 43 | DDDSDS | - | unchanged, v2 PASS | **PASS** |
| 44 | changed (R10; philology FAIL v2) | DDDDDS | digamma@10(εἰδώς) | ἔκ- long by κφ; ἔκφερε unelided has 0 hits (ἔκφερ᾽ 3x, ἔκφερεν Od. 15.470); before δ᾽ it cannot be elided, so there is no metrical consequence. δ᾽ αὖτε at 3-3.5 (5x; αὖτε at 3-3.5 13x); τε stays short before Ν. **Νοβῆκος at 4-5.5 = SLS** (ο, η by nature; -κος open before ὃ): a new slot, allowed by A1.1 (no flags). SLS words fill 4-5.5 in 1971 Homeric instances, e.g. γυναῖκας after δ᾽ αὖτε (Od. 24.278, SDDDDS, checked). ὃ S at 6: word end at 6 (9.7% lexical), with a trochaic caesura, so no diaeresis anomaly. δ᾽ ἕσπετο: ἕσπετο LSS at 7-8 8x, ἑ- long by σπ; ἕπομαι is not in digamma.tsv and Homer elides before it (Il. 12.398, Od. 1.125, 8.109). κέρδεα εἰδώς = Il. 23.709 at 9-12; κέρδεα α S by the accent rule (tool warning, matching jsonl `quantity` entry); ϝ of εἰδώς blocks the hiatus (digamma 42x). Bucolic D | **PASS** |
| 45 | = v2 45 | DDDDDS | - | unchanged, v2 PASS | **PASS** |
| 46 | = v2 46 | DSDDDS (tier 1) | lengthening_liquid@7(μέγα);correption@9.5(κεῖται) | unchanged, v2 PASS; tier 1: lengthening before μέγα of the verbatim Il. 22.163 | **PASS** |
| 47 | = v2 47 | DDSDSS | hiatus_long@5(γυνὴ) | unchanged, v2 PASS; **spondaic fifth foot** (flagged), = Il. 22.164 (spondeiazon) | **PASS** |
| 48 | = v2 48 | SDDDSS | - | unchanged, v2 PASS; **spondaic fifth foot** (flagged), Il. 22.165 has the same pattern SDDDSS | **PASS** |
| 49 | = v2 49 | DSDDDS | - | unchanged, v2 PASS | **PASS** |
| 50 | = v2 50 | DDDDDS | - | unchanged, v2 PASS | **PASS** |
| 51 | changed (R10) | DDSSDS | - | τὴν μὲν ἄρ᾽ at 1-2 (Il. 5.353, 18.148, Od. 19.440). Ἑλβετίου 3-5, ι S metre-only (warning, jsonl `quantity` entry). τὴν L at 6 (32x); δ᾽ αὖ, αὖ at 7 (6x). **Σέρβου LL at 8-9**: σέρ long by ρβ, -βου by nature; new form and slot, allowed by A1.1 (no flags). LL words at 8-9: 922 Homeric instances, e.g. Τρώων, ἀνδρῶν (ἀνδρῶν Ἀγαμέμνων), κνίσῃ ἐκάλυψαν. κρατεροῖο SSLX at 9.5-12 4x (Il. 13.60, 13.415, 23.848, Od. 11.277), κρα S dt 0/7. Spondees in feet 3 and 4 (ου τὴν \| δαὖ Σέρ). DDSSDS occurs in 377 of 27162 Homeric lines (1.39%). Word ends 2, 5, 6, 7, 9; word end at 6 after a penthemimeral caesura, so no diaeresis anomaly. Elision ἄρ᾽ before the invented name: no digamma | **PASS** |
| 52 | = v2 52 | DDDDDS | - | unchanged, v2 PASS | **PASS** |
| 53 | = v2 53 | DDDDDS | - | unchanged, v2 PASS | **PASS** |
| 54 | = v2 54 | DDDDDS | - | unchanged, v2 PASS | **PASS** |
| 55 | changed (R9, R11) | DDDSDS | - | the system of 33, with Νοβῆκος at 6-8 after short τε: SL by nature, -κος long by ς+κ before καί (SLL in situ). Word ends and Naeke as 33. Circumflex per R9/A2: an accent change only, η is long either way | **PASS** |
| 56 | changed (v2 scansion FAIL) | SDDDDS | - | **v2 FAIL repaired: αὖθ᾽ before the rough-breathing Ἑλβέτιος** (Homer: αὖθʼ + rough breathing 33x, αὖτʼ 0x; recounted). ἔνθ᾽ αὖθ᾽ has 0 hits as a pair because Homer's ἔνθ᾽ αὖτ᾽ (12x) never precedes an aspirated word: orthography, no metrical effect. Ἑλβέτιος 3-5 metre-only (warning, jsonl entry); -ος long by ς+πρ. προΐει 5.5-7 19x (ΐ S dt 0/20). βάλε δ᾽ at 7.5-9 as Il. 15.541. ἂψ long by ψ at 9; Ζοκοβείδης 9.5-12. Word ends 1, 2, 5, 7, 8, 9; bucolic D. Same scansion as v2 56 (SDDDDS) | **PASS** |
| 57 | = v2 57 | DDDDDS | - | unchanged, v2 PASS | **PASS** |
| 58 | = v2 58 | SDDDDS | - | unchanged, v2 PASS | **PASS** |
| 59 | = v2 59 | SSDDDS | - | unchanged, v2 PASS | **PASS** |
| 60 | = v2 60 | DDDDDS | - | unchanged, v2 PASS | **PASS** |

## Discrepancies with the composer's jsonl and with check_line

**Scansion: none.** On all 60 verses the following equal the fresh check_line run:

* the jsonl `text` (equal to v3.txt);
* the `scansion` fields: pattern, quantities, syllables, word_positions, word_quantities, caesurae, bucolic_diaeresis, licences;
* the `check_line` blocks: status, tier, flags, warning texts.

`changed` is true exactly for 23, 33, 36, 44, 51, 55 and 56, and `v2_line` = n throughout, which matches my text comparison. On the seven changed verses the jsonl scansion also equals my hand scansion. Every `quantity_unattested` warning in v3 has a matching jsonl `quantity` entry: Ἑλβέτιος/-ίου (metre-only) and κέρδεα (accent rule) in the changed verses, and the same set as in v2 elsewhere.

Documentation (no effect on any verdict):

1. **51, `sources`:** "κρατεροῖο (7x: 5 at 9.5-12, as here)" should read **4 at 9.5-12** (Il. 13.60, 13.415, 23.848, Od. 11.277, the four citations the entry itself gives) and **3 at 7.5-9.5** (Od. 4.335, 17.126, 24.170). Source: `--loose "κρατεροιο" --word`. This is a count only.
2. **51, `notes` (bears on the R10 record for FOR_HUMAN.md):** "Ζοκοβείδαο (SSLLS) cannot stand in any slot of a hexameter" overstates the case.
   * It is true of the form before a vowel or a single consonant (SSLLS).
   * Before an initial consonant cluster the final -ο is long by position (SSLLL), and the genitive fits at 1.5-5. `python homer/check_line.py "ὣς Ζοκοβείδαο στρατὸς ἤϊεν ἔνθα καὶ ἔνθα"` gives DSDDDS, unique, tier 0, no flags (warning: α of -αο metre-only; the test is metrical only, not proposed wording).
   * The v3 text is not affected: Σέρβου κρατεροῖο scans cleanly. If the R10 decision is recorded in FOR_HUMAN.md, it should not repeat the claim in absolute form.
3. **44, `name_formula`:** "Νοβῆκος (SLX at 4-5.5 before a vowel, final syllable short …)" gives the name's shape as a word. In this slot it scans SLS, as the entry's own `sources` and `quantity_notes` say. Label only. The same kind of label in 15 (scansion_v2 note 2) is now corrected to "LS at 9-9.5".
4. **33, 55:** Naeke's bridge is not mentioned in the jsonl (as in v2). It is common (7.0%), so no action is needed.
5. **33, 55 (for the provenance verifier):** καὶ βάλεν at 9-10 is correctly marked ATTESTED-MODIFIED (Homer 11x, all at 1-2). The pair βάλεν αὖτις has 0 hits. The jsonl cites only verse-final αὖτις after a verb (Il. 15.29, 6.367, 18.59, each checked), not the pair. No metrical point.
6. **The round-2 documentation items from scansion_v2.md are applied:**
   * the Σέρβος label in 15 and the Σέρβον label in 43;
   * the positions of δὲ πρῶτος (12: 4-5.5), ἀμφοτέρω and πάλιν (22: 3-5, 7.5-8), and καμάτῳ (31: 5.5-7);
   * δάμασεν in 24, now recorded as a modification and as a coinage.
7. **Cited parallels checked:**
   * δ᾽ αὖτε at 3-3.5 5x; γυναῖκας at 4-5.5 in Od. 24.278 (SDDDDS);
   * ὃ δ᾽ ἅμ᾽ ἕσπετο Il. 11.472 = 15.559 = 16.632; δ᾽ ἕσπετο 3x;
   * ἄεθλον 27x (22 at 10-12, 3 at 4-5.5); ἄφαρ 15x at 6-7 and 16x at 2-3; λάβε 14x at 9.5-10;
   * δ᾽ αὖ 110x (6 at 7); τὴν δ᾽ αὖ 13x (all 1-2); κνίσῃ ἐκάλυψαν 4x at 8-12;
   * προΐει 19x at 5.5-7; βάλε δ᾽ Il. 15.541 at 7.5-9;
   * τρὶς μὲν ἔπειτ᾽ ἐπόρουσε 3x at 1-5.5.

## Evidence commands (rerun from the repository root, `source .venv/bin/activate`)

* `python homer/check_line.py --file composition/drafts/v3.txt --json` (60 verses, 0 flagged, 0 unmetrical, exit 0). The same command on v2.txt gives identical per-verse output for the 53 unchanged verses.
* Text comparison: Python over the two files split on `\n`, comparing strings line by line and checking `unicodedata.normalize('NFC', s) == s`. Differences at 23, 33, 36, 44, 51, 55, 56 only.
* `python homer/check_line.py "εἰ μὴ ἄρʼ οἱ βέλος ὠκὺ ἐτώσιον ἔκφυγε χειρός"` (flag elision_before_digamma, exit 1: the check is active).
* αὖθʼ / αὖτʼ before a rough breathing: Python over homer/lines.tsv, consecutive word pairs, first word `αὖθʼ` or `αὖτʼ` (apostrophes unified), next word's initial vowel carrying U+0314 in NFD. Result: αὖθʼ 33 (Il. 1.370, 2.540, 2.552, 2.563 …), αὖτʼ 0. The same pass over v3.txt finds no elided τ/κ/π before a rough breathing. Its two hits for θ before a smooth breathing are ἔνθ᾽ = ἔνθα (34, 56), not aspirated τ.
* Digamma: each word after an elision in the changed verses, tested against every `match`/`exclude` rule of homer/digamma.tsv on its loose form. Only εἰδώς matches (row idein).
* `python homer/concordance.py --ngram` for: λάβ᾽ ἄεθλον (1, Il. 23.511), ἄεθλον (27), δεύτερον αὖ (5), κρατερὸς Διομήδης (20), τρὶς μὲν ἔπειτ᾽ ἐπόρουσε (3), καὶ βάλεν (11, all 1-2), βάλεν αὖτις (0), δ᾽ αὖτε (141; 5 at 3-3.5), χωρὶς δ᾽ αὖτε γυναῖκας (Od. 24.278), δ᾽ ἕσπετο (3), ὃ δ᾽ ἕσπετο (0), ὃ δ᾽ ἅμ᾽ ἕσπετο (3), κέρδεα εἰδώς (Il. 23.709), τὴν μὲν ἄρ᾽ (3), τὴν δ᾽ αὖ (13), δ᾽ αὖ (110), κνίσῃ ἐκάλυψαν (4), ἔνθ᾽ αὖθ᾽ (0), βάλε δ᾽ (3), λάβε (26).
* `--loose --word`: αφαρ (34), κρατεροιο (7: 4 at 9.5-12, 3 at 7.5-9.5), προιει (21).
* Word slots and per-word quantities: a scratch script over homer/scansion.tsv (unique lines) joined with homer/lines.tsv, tabulating `word_positions` × `word_meter` per loose form. It gives ἄεθλον SLS at 4-5.5 ×3; ἄφαρ SL at 6-7 ×15; κρατερὸς SSL at 7.5-9 ×30; ἐπόρουσε SSLS at 3.5-5.5 ×15; αὖτε LS at 3-3.5 ×13; ἕσπετο LSS at 7-8 ×8; κέρδεα LSS at 9-10 ×3; βάλεν SS at 9.5-10 ×11; αὖτις LX at 11-12 ×20; τὴν L at 6 ×32; SLS words at 4-5.5: 1971; LL words at 8-9: 922.
* dichrona.tsv rows used: λάβʼ ά S 0/3; λάβε ά S 0/24; ἄεθλον ἄ S 0/27; ἄφαρ ἄ S 0/32, final α S 0/3; κρατερός α S 0/37; κρατεροῖο α S 0/7; βάλεν ά S 0/44; βάλε ά S 0/80; ἀφάμαρτε ἀ, ά S 0/4; ἀγαθός ἀ, α S 0/56; ἄρʼ ἄ S 0/533; αὖτις ι S 0/69; προΐει ΐ S 0/20; τρίς ι S 0/1. κέρδεα has no row: accent rule, check_line warning, jsonl `quantity` entry.
* Baselines: `awk -F'\t' 'NR>1&&$4=="unique"{n++; p[$8]++; if(substr($8,5,1)=="S")s++; if($19~/naeke/)k++} END{print n,p["DDSSDS"],s,k}' homer/scansion.tsv` → 27162, 377, 1364, 1904. licences.tsv: digamma εἰδώς 42.
* Ζοκοβείδαο test: `python homer/check_line.py "ὣς Ζοκοβείδαο στρατὸς ἤϊεν ἔνθα καὶ ἔνθα"` (DSDDDS, unique, tier 0, no flags; one metre-only warning).

## Appendix: my scansion of the seven changed verses, syllable by syllable

Legend, as in scansion_v1.md and scansion_v2.md:

* L long, S short, X final anceps.
* n = nature (η ω, diphthong, circumflex; ε ο short).
* p(..) = position, with the consonants.
* c = epic correption; h = hiatus.
* d = digamma (homer/digamma.tsv) blocks hiatus or correption.
* dt = homer/dichrona.tsv, with the counts (L/S); acc = accent rule; cc = concordance attestation (cited).
* MO = metre-only quantity of an invented name (brief §4).

Syllables are written with the consonants they are pronounced with (βἄ = λάβ᾽ ἄ-). Word ends are given as orthographic / lexical, final 12 omitted. Unchanged verses: see the appendices of review/scansion_v2.md (verses new in v2) and review/scansion_v1.md (verses verbatim since v1).

**23** δεύτερον αὖ λάβ᾽ ἄεθλον ἄφαρ κρατερὸς Ζοκοβείδης.  
DDDDDS: δεύ L n · τε S n · ρο S n · ναὖ L n · λά S dt(λάβʼ 0/3) · βἄ S dt(ἄεθλον 0/27) · ε L p(θλ)+cc(Il. 23.892, Od. 21.91, 23.261) · θλο S n · νἄ S dt(ἄφαρ 0/32) · φαρ L p(ρκ) · κρα S dt(0/37) · τε S n · ρὸς L p(ς ζ) · Ζο S n · κο S n · βεί L n · δης X  
word ends: 2, 3, 3.5, 5.5, 7, 9 / the same. Licences: -

**33** καὶ βάλεν, οὐδ᾽ ἀφάμαρτε, Ῥογῆρος, καὶ βάλεν αὖτις·  
DDDSDS: καὶ L n · βά S dt(0/44) · λε S n · νοὐ L n · δἀ S dt(0/4) · φά S dt(0/4) · μαρ L p(ρτ) · τε S n (no lengthening before Ῥ; no licence) · Ῥο S n · γῆ L n · ρος L p(ς κ) · καὶ L n · βά S dt(0/44) · λε S n · ναὖ L n · τις X  
word ends: 1, 2, 3, 5.5, 8, 9, 10 / 2, 5.5, 8, 10 (καί, οὐδ᾽ prepositive). Licences: -. Bucolic S (Naeke).

**36** τρὶς μὲν ἔπειτ᾽ ἐπόρουσε βοὴν ἀγαθὸς Φεδερῆρος,  
DDDDDS: τρὶς L p(ς μ) · μὲ S n · νἔ S n · πει L n · τἐ S n · πό S n · ρου L n · σε S n · βο S n · ὴν L n · ἀ S dt(0/56) · γα S dt(0/56) · θὸς L p(ς φ) · Φε S n · δε S n · ρῆ L n · ρος X  
word ends: 1, 1.5, 3, 5.5, 7, 9 / 1.5, 3, 5.5, 7, 9 (μέν postpositive). Licences: -

**44** ἔκφερε δ᾽ αὖτε Νοβῆκος, ὃ δ᾽ ἕσπετο κέρδεα εἰδώς.  
DDDDDS: ἔκ L p(κφ) · φε S n · ρε S n · δαὖ L n · τε S n · Νο S n · βῆ L n · κο S n · σὃ S n · δἕσ L p(σπ) · πε S n · το S n · κέρ L p(ρδ) · δε S n · α S acc+cc(Il. 23.709)+d · εἰ L n · δώς X  
word ends: 2, 3.5, 5.5, 6, 8, 10 / the same. Licences: digamma@10(εἰδώς). Bucolic D.

**51** τὴν μὲν ἄρ᾽ Ἑλβετίου, τὴν δ᾽ αὖ Σέρβου κρατεροῖο,  
DDSSDS: τὴν L n · μὲ S n · νἄ S dt(ἄρʼ 0/533) · ρἙλ L p(λβ) · βε S n · τί S MO · ου L n · τὴν L n · δαὖ L n · Σέρ L p(ρβ) · βου L n · κρα S dt(κρατεροῖο 0/7) · τε S n · ροῖ L n · ο X  
word ends: 1, 1.5, 2, 5, 6, 7, 9 / 2, 5, 6, 7, 9 (μέν, ἄρ᾽ postpositive). Licences: -

**55** καὶ βάλεν, οὐδ᾽ ἀφάμαρτε Νοβῆκος, καὶ βάλεν αὖτις·  
DDDSDS: καὶ L n · βά S dt(0/44) · λε S n · νοὐ L n · δἀ S dt(0/4) · φά S dt(0/4) · μαρ L p(ρτ) · τε S n · Νο S n · βῆ L n · κος L p(ς κ) · καὶ L n · βά S dt(0/44) · λε S n · ναὖ L n · τις X  
word ends: 1, 2, 3, 5.5, 8, 9, 10 / 2, 5.5, 8, 10. Licences: -. Bucolic S (Naeke).

**56** ἔνθ᾽ αὖθ᾽ Ἑλβέτιος προΐει, βάλε δ᾽ ἂψ Ζοκοβείδης,  
SDDDDS: ἔν L p(νθ) · θαὖ L n · θἙλ L p(λβ) · βέ S n · τι S MO · ος L p(ς πρ) · προ S n · ΐ S dt(0/20) · ει L n · βά S dt(βάλε 0/80) · λε S n · δἂψ L p(ψ) · Ζο S n · κο S n · βεί L n · δης X  
word ends: 1, 2, 5, 7, 8, 9 / the same. Licences: -. Bucolic D. Orthography now correct (θ᾽ before the rough Ἑ-).
