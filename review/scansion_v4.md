# Scansion review: composition/drafts/v4.txt (64 verses)

Reviewer: scansion-verifier, 2026-10-08. Final round, after review/round_3.md and review/critic_poem_v1.md. Order of work:

1. Exact NFC string comparison of every v4 verse against every v3 verse. This was done before opening v4.jsonl.
   * 44 v4 verses are verbatim v3 strings, and all were v3 PASS.
   * 20 are not verbatim: 19, 20, 24, 27, 29, 32, 33, 34, 35, 36, 38, 40, 49, 54, 56, 58, 59, 61, 62, 63.
2. Independent hand scansion of the 20 non-verbatim verses, syllable by syllable (appendix). I wrote it to a scratch sheet before any tool touched the draft: pattern, L/S string, orthographic and lexical word ends, expected licences.
   * Quantities are justified from homer/dichrona.tsv, homer/dichrona_analogy.tsv, homer/digamma.tsv, homer/licences.tsv and homer/positions.tsv.
   * Where the tables have no row, I used concordance or scansion.tsv attestations (commands at the end).
3. Only then `python homer/check_line.py --file composition/drafts/v4.txt --json`, plus a fresh run on v3.txt for the verbatim verses.
4. Only then composition/drafts/v4.jsonl. I used its `v3_line` field only at this stage, to label the counterparts in the table below.

Rulings applied: review/round_1.md R1-R8, review/round_2.md R9-R12, composition/brief.md Addenda A1 and A2. For the sense rulings (R11, R12, A2.3), only their metrical consequences are checked here; sense is for the philologist.

## Summary

* **Verdicts: PASS 64, FAIL 0, QUERY 0** (of 64). No failing lines.
* **Text status.**
  * The 44 verbatim verses (one row each below, "unchanged, v3 PASS") map as follows: 1-18 and 21-22 = v3 1-22; 23 = v3 27; 25-26 = v3 24-25; 28 = v3 27; 30-31 = v3 28-29; 37 = v3 33; 39 = v3 35; 41-48 = v3 36-43; 50-51 = v3 45-46; 52-53 = v3 48-49; 55 = v3 51; 57 = v3 53; 60 = v3 56; 64 = v3 60.
  * v3 47 (= Il. 22.164) has no v4 counterpart: it was dropped.
  * v4 23 and 28 are the same string (v3 27).
  * 59 differs from v3 55 only by the comma after ἀφάμαρτε (round-3 record correction).
  * Both files are NFC. The only elision mark is U+1FBD.
* **Tool drift.** For all 44 verbatim verses, a fresh check_line run on v3.txt gives byte-identical per-verse output to the v4 run.
* **Validity.**
  * All 64 verses are valid hexameters, each with a unique scansion.
  * 63 are tier 0. Verse 51 (= v3 46, Il. 22.163) is tier 1, for the lengthening before μέγα.
  * check_line: 64 verses, 0 flagged, 0 unmetrical, exit 0.
* **Hand scansion against the tool.**
  * On all 20 hand-scanned verses, my pattern and L/S string equal check_line's.
  * The word-end differences are my own slips or conventions, not the tool's errors:
    * 20: λάβ᾽ ends at 9.5 (its β goes to ἄ-), not 10. τρὶς δέ μιν is one lexical unit ending at 2, so there is no lexical end at 1.5.
    * 32: ἀμφήριστον ends at 9.5. I corrected this on my sheet before the tool run, from Il. 23.382.
    * 32, 63: the tool treats αὐτάρ and line-initial ὣς as full words, as it does in Il. 3.379 and Il. 11.596. I had treated them as clitics.
  * None of these touches a verdict.
* **jsonl against the fresh run.** On all 64 verses these equal the fresh run: the jsonl `text`, the `scansion` fields (pattern, quantities, syllables, word_positions, word_quantities, caesurae, bucolic_diaeresis, licences) and the `check_line` blocks (status, tier, flags, warning strings). Every `quantity_unattested` warning has a matching `quantity` entry. There are no scansion discrepancies with the composer. The documentation discrepancies are listed below.
* **Spondaic fifth feet (flagged): 52 and 54.**
  * 52 (= v3 48) has the pattern of Il. 22.165, SDDDSS.
  * **54 is new**, DDDDSS: ἐν δ᾽ ἐτίθει δύο κῆρε μάχης θαλερῶν αἰζηῶν. The spondee ρῶ ναἰ is forced, because αἰ is long and ζη ῶν fill the sixth foot. Both Homeric instances of θαλερῶν αἰζηῶν (Il. 10.259, 14.4, at 7.5-12) are SDDDSS spondeiazontes, and αἰζηῶν is verse-final in all 11 occurrences. The jsonl records the spondeiazon.
  * v3 47's spondeiazon (Il. 22.164) has gone with the line.
  * Baselines: 1364 of 27162 uniquely scanned Homeric lines have a spondaic fifth foot (5.02%); DDDDSS has 287 (1.06%).
* **Word ends against positions.tsv.**
  * No verse has a lexical word end at 7.5, so Hermann's bridge holds in all 64.
  * Orthographic 7.5 occurs only before an enclitic or postpositive: 27 (πάραντά | τε, = Il. 23.116) and 46 (ἔπειτα | δέ, = Il. 5.139).
  * Lexical word end at 11 occurs only in 43 (λέων ὣς, = Il. 20.164, 1.45%).
  * In the 20 changed verses the rarest lexical word end is 56's at 6 (ῥέπε δ᾽, 9.67% lexical). 56 also has a penthemimeral caesura, so it does not have the diaeresis-after-the-third-foot anomaly. Next rarest are 4 (15.76%: 36, 49, 54) and 1 (18.50%: 54, 58, 63).
  * Every verse has a penthemimeral, trochaic or hephthemimeral caesura.
  * Naeke's bridge (lexical word end at 8 after a spondaic fourth foot) occurs in 23, 28, 37 and 59 (the SLX name slot at 6-8 before a consonant, as in v3) and in **62** (new: δὴ Ζεὺς | κῦδος). 62 has the pattern and the word ends from 5 onwards of Il. 8.216 (οἱ Ζεὺς κῦδος ἔδωκε, SDDSDS). Naeke occurs in 1904 of 27162 Homeric lines (7.01%), so it is noted, not flagged.
* **Licences.** In the changed verses: digamma@10(ἶσος) in 19 (19x); correption of καί in 20, 29, 32, 36, 38 (2364x; in 29 = Il. 1.116 ἀλλὰ καὶ ὧς); **hiatus_long@7(κρατεροῦ)** in 29 and **hiatus_long@5(αὖ)** in 49.
  * Both hiatus_long licences are attested for the word, but only once, at another longum: κρατεροῦ at Il. 21.553@9 (ὑπὸ κρατεροῦ Ἀχιλῆος), αὖ at Il. 3.383@3 (αὐτὴ δ᾽ αὖ Ἑλένην). In 49 the hiatus also falls at a sense pause (comma).
  * Whole draft, every licence attested for its form (licence_parallels count > 0 in every case):
    * correption: μοι 1; καί 4, 20, 22, 29, 32, 36, 38; λούεσθαι 18; ἀγρῷ 44; ἐξάλλεται 47; κεῖται 51
    * hiatus: ὠκύ 39; ὃ 47
    * hiatus_long: διαμετρητῷ 11; κρατεροῦ 29; αὖ 49
    * muta cum liquida: ἀμφιβρότην 8; before an initial cluster, Κρονίων 13 and κροαίνων 17
    * digamma: οἱ 9, 39; ἶσα 13, 21; ἶσος 19, 42; εἰδώς 23, 28
    * lengthening before a liquid: μέγα 51
  * v3's hiatus_long@5(γυνή) and the ἶσα of v3 26 left with their lines.
* **Digamma and elision.**
  * The only digamma word in the changed verses is ἶσος (19), after unelided δαίμονι, as in the 7 Homeric lines with ἐπέσσυτο δαίμονι ἶσος at 6-12. The tool also matches line-initial ὣς (19, 63) to its postpositive-ὥς entry, which has no effect with nothing before it.
  * No elision in any changed verse stands before a digamma word (programmatic test against every digamma.tsv rule). The elisions are: ἄρ᾽ ὅ, γ᾽ Ἑλβέτιος, τότ᾽ ἐπέσσυτο (19); αὖτ᾽ ἐδάμασσε, λάβ᾽ ἄεθλον (20); ἀλλ᾽ ὅ (24); δ᾽ ἄναντα, τ᾽ ἦλθον (27); γ᾽ ἂψ (32); δ᾽ ἀργαλέῳ (33); δ᾽ ἀμφοτέροισιν (35); δ᾽ ἄρα (36); ἔνθ᾽ ἔλαβεν (38); μάλ᾽ ἐγγύς, οὐδ᾽ ἀφάμαρτε (40); δ᾽ ἔκφερεν, δ᾽ ἐπέσσυτο (49); δ᾽ ἐτίθει (54); δ᾽ Ἑλβετίου, τότ᾽ ἐέλδωρ (56); δ᾽ ἕτερος (58); οὐδ᾽ ἀφάμαρτε (59); οὐδ᾽ ἔτυχες (61); δ᾽ ἀντιθέῳ (62); δ᾽ ἐτελείετο (63).
  * ἐέλδωρ is not on the digamma list, and Homer elides τ᾽ before it twice (κρηήνατ᾽ ἐέλδωρ, Od. 3.418, 17.242).
  * In the whole draft no elided τ/κ/π stands before a rough breathing. Before an aspirate there are only δ᾽, γ᾽, λλ᾽ and ρ᾽ (δ᾽ ἕτερος, δ᾽ Ἑλβετίου, ἀλλ᾽ ὅ, ἄρ᾽ ὅ, γ᾽ Ἑλβέτιος), plus the aspirated αὖθ᾽ of 10, 25, 43 and 60, unchanged from v3.
  * The elision-before-digamma check is still active: it flags the v1 35 wording `εἰ μὴ ἄρʼ οἱ …` (exit 1).
* **Quantity warnings on Homeric words.** Brief §5.1 allows warnings "only for the invented names' quantities". Round 3 accepted backed non-name warnings that had a jsonl `quantity` entry (κέρδεα, ἀργαλέῳ, ἀντίθεος …), and I apply the same standard. Three non-name warnings are new in v4, and one is carried over. All four are backed, and all have jsonl entries:
  * 24 πυμάτῃ υ, α: "analogy". Every attested πυματ- form has both vowels short: 15/15 for each vowel over 8 forms in dichrona.tsv (πύματον 0/7, πυμάτης 0/2, πύματα 0/2, πυμάτη, πυμάτην, πυμάτῳ, πυμάτοισι 0/1 each). dichrona_analogy.tsv key πυματη: S.
  * 34 παρέλασσε α: "analogy". The elided παρέλασσʼ has α short 0/2 in dichrona.tsv (Il. 23.382, 23.527).
  * 62 ἀντιθέῳ ι: "metre only". ἀντιθέῳ is LSSL in all 8 uniquely scanned Homeric instances, 3 of them at 3-5 as here (Il. 4.377, 5.629, 16.649). All 56 ἀντιθε- instances are LSSL or LSSLX.
  * 33 ἀργαλέῳ second α: "metre only", carried from v3 31. ἀργαλέῳ is LSSL at 3-5 in all 6 instances, including Il. 13.85, whose words 3-12 the verse keeps at the same positions. All 56 ἀργαλε- instances are LSSL or LSSLX.
  * The tool says "metre only" for ἀργαλέῳ and ἀντιθέῳ because dichrona.tsv drops an attestation when another tier-1 scansion would remain (README §4, criterion c; here presumably a long vowel with synizesis of -έῳ). That is an artefact of the attestation filter, not a doubt about the quantity.
* **Names and rulings, metrical side.**
  * R4: no δίς. R5: no ἐξενάριξε. R6: πάλιν only in 22 ("back", unchanged). R2/A1.3: no ἰσόθεος after Ῥογῆρος.
  * R9/A2.1: nominative Νοβῆκος (59) has the circumflex. The genitive Νοβήκου (29) has the acute that Homer's own properispomena take before a long ultima (δῆμος 7 / δήμου 8; νῆσος 5 / νήσου 9; no δῆμου or νῆσου). The accent does not affect quantity.
  * R10/A2.2: no Ζοκοβεύς or Ζοκοβῆος anywhere.
  * R1/A1.1: the new slots all pass with no flag and no unattested licence: Νοβήκου 10-12 SLL after vowel-final χερσί (29); Σέρβος 3-3.5 LS after short γε before a vowel (24, the slot of Σέρβον in 48); Σέρβῳ 1-2 (62); vocative Φεδερεῦ 5.5-7 SSL after ἔτυχες (61), where ς+Φ makes position at the longum 5 (cf. Ἀχιλεῦ at 5.5-7 in Il. 11.606, 24.503, 24.661).
  * Ζοκοβείδης (4, 57, 60) always follows a syllable long at 9. Ῥογῆρος (23, 28, 37) and Νοβῆκος (59) always follow short vowel-final τε at 6.
* **Epithet economy holds.** κρατερός is Djokovic's (29 κρατεροῦ … Νοβήκου, 55, 57). ἀντίθεος is Djokovic's (4, 62). βοὴν ἀγαθός is Federer's (14, 31, 34, 41). κέρδεα εἰδώς and διογενής are Federer's. Each player has all three shapes: Federer Φεδερῆρος / Ἑλβέτιος / Ῥογῆρος; Djokovic Ζοκοβείδης / Σέρβος / Νοβῆκος.

## Names: forms, slots, quantity basis (from the v4 check_line word positions)

| name | v4 verses @ slot (word quantities) | quantity basis | verdict |
|---|---|---|---|
| Φεδερῆρος / -ον | 14, 34, 41 @9.5-12 (SSLX); 31 acc. @9.5-12 | nature | consistent; all after βοὴν ἀγαθός/-όν |
| Φεδερεύς / voc. Φεδερεῦ | 4, 26 @3.5-5 (SSL); **61 voc. @5.5-7 (SSL)** | nature | new slot and form in 61, allowed by A1.1 (no flags) |
| Ῥογῆρος | 23, 28, 37 @6-8 (SLL before κ) | nature; -ρος long by ς+κ | unchanged system |
| Ἑλβέτιος / -ίου | 5, 12 @1-3; 19, 25, 60 @3-5; 55 gen. @3-5; 56 gen. @7-9 (all LSSL) | ι short, metre-only (jsonl `quantity` entry in each) | consistent |
| Ζοκοβείδης | 4, 57, 60 @9.5-12 (SSLL) | nature | ζ always after a syllable long at 9 |
| Σέρβος / -ον / -ου / -ῳ | 10, 31, 43, 49 @1-2 (LL); 15 @9-9.5 (LS); **24 @3-3.5 (LS)**; 48 acc. @3-3.5 (LS); 55 gen. @8-9 (LL); **62 dat. @1-2 (LL)** | σέρ long by ρβ; -ου, -ῳ by nature | new: 24 (the v3 slot of Σέρβον), 62 (dative); no flags |
| Νοβῆκος / gen. Νοβήκου | 59 @6-8 (SLL before κ); **29 gen. @10-12 (SLL after χερσί)** | nature (ο η; -ου) | 29 is a new form and slot, the brief's original Νοβάκος slot (10-12 after a vowel); no flags |

## The 44 verbatim verses

Pattern and licences are from the fresh check_line run, identical to the v3 run. Syllable-level scansion is in the appendices of review/scansion_v1.md to scansion_v3.md.

| v4 | v3 string | pattern | licences | notes | verdict |
|---|---|---|---|---|---|
| 1 | = v3 1 | DDDDDS | correption@2(μοι) | unchanged, v3 PASS; warning δαΐφρονε (as v3) | **PASS** |
| 2 | = v3 2 | DSDDDS | - | unchanged, v3 PASS | **PASS** |
| 3 | = v3 3 | SSDSDS | - | unchanged, v3 PASS | **PASS** |
| 4 | = v3 4 | DDDDDS | correption@6(καὶ) | unchanged, v3 PASS; warning ἀντίθεος (as v3) | **PASS** |
| 5 | = v3 5 | DDDDDS | - | unchanged, v3 PASS | **PASS** |
| 6 | = v3 6 | SSDSDS | - | unchanged, v3 PASS | **PASS** |
| 7 | = v3 7 | DDDSDS | - | unchanged, v3 PASS | **PASS** |
| 8 | = v3 8 | DDDDDS | muta_cum_liquida@3.5(ἀμφιβρότην) | unchanged, v3 PASS | **PASS** |
| 9 | = v3 9 | DDDDDS | digamma@6(οἱ) | unchanged, v3 PASS | **PASS** |
| 10 | = v3 10 | SDDDDS | - | unchanged, v3 PASS | **PASS** |
| 11 | = v3 11 | SSDSDS | hiatus_long@9(διαμετρητῷ) | unchanged, v3 PASS | **PASS** |
| 12 | = v3 12 | DSDDDS | - | unchanged, v3 PASS | **PASS** |
| 13 | = v3 13 | SDDDDS | digamma@4(ἶσα);muta_cum_liquida_initial@9.5(Κρονίων) | unchanged, v3 PASS | **PASS** |
| 14 | = v3 14 | DDDDDS | - | unchanged, v3 PASS | **PASS** |
| 15 | = v3 15 | DDDDDS | - | unchanged, v3 PASS | **PASS** |
| 16 | = v3 16 | DDDSDS | - | unchanged, v3 PASS | **PASS** |
| 17 | = v3 17 | DSSDDS | muta_cum_liquida_initial@9.5(κροαίνων) | unchanged, v3 PASS | **PASS** |
| 18 | = v3 18 | SSDSDS | correption@5.5(λούεσθαι) | unchanged, v3 PASS | **PASS** |
| 21 | = v3 21 | DDDDDS | digamma@4(ἶσα) | unchanged, v3 PASS | **PASS** |
| 22 | = v3 22 | SDSDDS | correption@10(καὶ) | unchanged, v3 PASS | **PASS** |
| 23 | = v3 27 | DDDSDS | digamma@10(εἰδώς) | unchanged, v3 PASS (string = v3 27; the jsonl maps it to v3 23, which it replaces, with `changed: true`: discrepancy note 1); also = v4 28, so the whole line now stands twice, five lines apart; Naeke | **PASS** |
| 25 | = v3 24 | SDDSDS | - | unchanged, v3 PASS | **PASS** |
| 26 | = v3 25 | DDDDDS | - | unchanged, v3 PASS | **PASS** |
| 28 | = v3 27 | DDDSDS | digamma@10(εἰδώς) | unchanged, v3 PASS; Naeke | **PASS** |
| 30 | = v3 28 | DDSDDS | - | unchanged, v3 PASS | **PASS** |
| 31 | = v3 29 | SDDDDS | - | unchanged, v3 PASS | **PASS** |
| 37 | = v3 33 | DDDSDS | - | unchanged, v3 PASS; Naeke | **PASS** |
| 39 | = v3 35 | SDDDDS | digamma@2(οἱ);hiatus@5.5(ὠκὺ) | unchanged, v3 PASS | **PASS** |
| 41 | = v3 36 | DDDDDS | - | unchanged, v3 PASS | **PASS** |
| 42 | = v3 37 | DDDDDS | digamma@10(ἶσος) | unchanged, v3 PASS | **PASS** |
| 43 | = v3 38 | SDDDDS | - | unchanged, v3 PASS; lexical word end at 11 (1.45%), λέων ὣς = Il. 20.164 | **PASS** |
| 44 | = v3 39 | DSDDDS | correption@5.5(ἀγρῷ) | unchanged, v3 PASS | **PASS** |
| 45 | = v3 40 | SSDDDS | - | unchanged, v3 PASS | **PASS** |
| 46 | = v3 41 | SDDDDS | - | unchanged, v3 PASS; orthographic word end at 7.5 (ἔπειτα | δέ), lexical at 8, = Il. 5.139 | **PASS** |
| 47 | = v3 42 | DDDSDS | hiatus@2(ὃ);correption@10(ἐξάλλεται) | unchanged, v3 PASS | **PASS** |
| 48 | = v3 43 | DDDSDS | - | unchanged, v3 PASS | **PASS** |
| 50 | = v3 45 | DDDDDS | - | unchanged, v3 PASS | **PASS** |
| 51 | = v3 46 | DSDDDS (tier 1) | lengthening_liquid@7(μέγα);correption@9.5(κεῖται) | unchanged, v3 PASS; tier 1: lengthening before μέγα, the verbatim Il. 22.163; no line-end punctuation now that v3 47 is gone (note 7) | **PASS** |
| 52 | = v3 48 | SDDDSS | - | unchanged, v3 PASS; **spondaic fifth foot** (flagged), pattern of Il. 22.165 | **PASS** |
| 53 | = v3 49 | DSDDDS | - | unchanged, v3 PASS | **PASS** |
| 55 | = v3 51 | DDSSDS | - | unchanged, v3 PASS | **PASS** |
| 57 | = v3 53 | DDDDDS | - | unchanged, v3 PASS | **PASS** |
| 60 | = v3 56 | SDDDDS | - | unchanged, v3 PASS | **PASS** |
| 64 | = v3 60 | DDDDDS | - | unchanged, v3 PASS | **PASS** |

## The 20 non-verbatim verses

My hand scansion is in the appendix. Pattern, L/S string and licences are the same in my scansion, the jsonl `scansion` and the fresh check_line run. The "v3 counterpart" column is the jsonl `v3_line`, consulted only after the hand scansion. Word ends are given as orthographic / lexical, with the final 12 omitted.

| n | v3 counterpart | pattern | licences | notes | verdict |
|---|---|---|---|---|---|
| 19 | v3 19 (9-12 replaced) | DDDDDS | digamma@10(ἶσος) | 1-5.5 as v3 19 (ὣς ἄρ᾽ ὅ γ᾽ = Il. 22.143, Od. 20.28; Ἑλβέτιος 3-5 MO). ἐπέσσυτο δαίμονι ἶσος at 6-12 = 7 Homeric lines (e.g. Il. 5.438). ϝῖσος blocks the hiatus after δαίμονι (19x). Word ends 1, 1.5, 2, 5, 5.5, 8, 10 / 1.5, 2, 5, 5.5, 8, 10; penthemimeral + trochaic; bucolic D | **PASS** |
| 20 | v3 20 (6-12 replaced) | DDDDDS | correption@6(καὶ) | καὶ correpted before ἐσσυμένως. ἐσσυμένως λάβ᾽ ἄεθλον = Il. 23.511 at 7-12: ἐσσυμένως LSSL at 7-9 (4x), and λάβ᾽ ἄεθλον back in its only Homeric slot, 9.5-12 (answers critic M8). ε of ἄεθλον long by θλ. Word ends 1, 1.5, 2, 3, 5.5, 6, 9, 9.5 / 2, 3, 5.5, 9, 9.5; trithemimeral + trochaic | **PASS** |
| 24 | new | DDDDDS | - | ἀλλ᾽ ὅ γε 1-2 (16x). Σέρβος LS at 3-3.5: γε stays short before single σ; -ος open before ἔπειτα. ἔπειτα 3.5-5.5 (δ᾽ ἄρ᾽ ἔπειτα 12x at 3.5-5.5). μάχῃ SL at 6-7 (24x). πυμάτῃ SSL at 7.5-9: υ and α short by analogy, πυματ- 0/15 each (warning, jsonl entry). μιν 9.5; ἐνίκα 10-12 (5x), ί long (dt 8/0). Word ends 1, 1.5, 2, 3.5, 5.5, 7, 9, 9.5 / 2, 3.5, 5.5, 7, 9.5; trochaic + hephthemimeral | **PASS** |
| 27 | v3 26 (replaced) | DDDDDS | - | = Il. 23.116 verbatim (punctuation aside). Quantities and word ends equal scansion.tsv Il. 23.116: orthographic 7.5 before the enclitic τε, lexical 8, so Hermann holds. Holodactylic. Trochaic; bucolic D | **PASS** |
| 29 | new | DDDDDS | correption@2(καὶ); hiatus_long@7(κρατεροῦ) | ἀλλὰ καὶ ὧς 1-3 (17x; καί correpted as in Il. 1.116). ἐδάμη SSL at 3.5-5 (Homer 1.5-3, 2x). κρατεροῦ SSL at 5.5-7: -οῦ kept long before ὑπό at the longum, attested once for this word (Il. 21.553@9). ὑπὸ χερσὶ at 7.5-9.5 (2x: Il. 3.352, 23.675). Νοβήκου SLL at 10-12 after short -ὶ. Word ends 1.5, 2, 3, 5, 7, 8, 9.5 / 3, 5, 7, 9.5; trithemimeral + penthemimeral + hephthemimeral | **PASS** |
| 32 | v3 30 (3.5-12 replaced) | DDDSDS | correption@6(καὶ) | αὐτὰρ ὅ γ᾽ ἂψ 1-3 (Od. 11.599); ἂψ ἐπόρουσε 3-5.5 (Il. 3.379, 21.33). καὶ correpted before ἀμφήριστον. ἀμφήριστον ἔθηκεν at 7-12 as Il. 23.382, 23.527 (ἀμφήριστον LLLS at 7-9.5): spondaic fourth foot, no word end at 8, so no Naeke. Word ends 1.5, 2, 3, 5.5, 6, 9.5 / 1.5, 2, 3, 5.5, 9.5; trithemimeral + trochaic | **PASS** |
| 33 | v3 31 (1-2 replaced) | SDDDDS | - | τοῖιν δ᾽: -ιν long by νδ, so foot 1 is a spondee (τοῖιν is LL at 1-2 in Il. 13.66). 3-12 = Il. 13.85 at the same positions. ἀργαλέῳ α short (warning, as v3 31; see summary). Word ends 2, 5, 7, 8, 9.5 / same; penthemimeral + hephthemimeral; bucolic D | **PASS** |
| 34 | v3 32 (3.5-12 replaced) | DDDDDS | - | ὀψὲ δὲ δή 1-3 (12x), ὀ long by ψ. παρέλασσε SSLS at 3.5-5.5, unelided before β; α short as in παρέλασσʼ 0/2 (warning, jsonl entry). βοὴν ἀγαθὸς Φεδερῆρος 6-12, -θὸς long by ς+φ. Word ends 1.5, 2, 3, 5.5, 7, 9 / 3, 5.5, 7, 9 | **PASS** |
| 35 | new | SDDDDS | - | = Il. 18.502 verbatim (one comma added). λᾱοί (dt 45/0); ἀμφοτέροισιν ι short (dt 0/9); ἐπήπυον υ short; ἀμφὶς ι short (0/22). Equals scansion.tsv Il. 18.502. Word ends 2, 5.5, 8, 9.5; trochaic; bucolic D | **PASS** |
| 36 | new | SDDDDS | correption@10(καὶ) | 1-8 = Il. 18.503 (same quantities). κήρῡκες υ long (dt 19/0), -κες long by ς+δ, so foot 1 is a spondee. λᾱόν (73/0). ἔνθα καὶ ἔνθα 9-12 (21x). Word ends 3, 4, 5.5, 8, 9.5, 10 / 4, 5.5, 8, 9.5; trochaic; bucolic D | **PASS** |
| 38 | v3 34 (3-12 replaced) | DDDDDS | correption@6(καὶ) | καί νύ κεν ἔνθ᾽ 1-3 (Il. 5.311, 5.388). ἔλαβεν SSL at 3.5-5 (Homer 5.5-7 2x and 1.5-3 1x: moved, no metrical effect), -βέν long by ν+τ. 5.5-12 = Il. 3.373 = 18.165. Word ends 1, 1.5, 2, 3, 5, 5.5, 6, 8, 10 / 2, 3, 5.5, 8, 10; trithemimeral + trochaic; bucolic D | **PASS** |
| 40 | new | DDDDDS | - | στῆ δὲ μάλ᾽ ἐγγὺς ἰών 1-5 (5x; same quantities as Il. 4.496): ἐγγύς υ short (0/20), ἰών ι short (0/87; the 2 long are ἰῶν). ὃ δέ μιν 5.5-7 (8x at this slot); μιν long by ν+β. βάλεν 7.5-8 (14x); οὐδ᾽ ἀφάμαρτε 9-12 (2x). Word ends 1, 1.5, 2, 3.5, 5, 5.5, 6, 7, 8, 9 / 1.5, 2, 3.5, 5, 7, 8; penthemimeral + hephthemimeral; bucolic D | **PASS** |
| 49 | v3 44 (replaced) | SDDDDS | hiatus_long@5(αὖ) | Σέρβος δ᾽ 1-2 (LL). ἔκφερεν LSS at 3-4, ἔκ- long by κφ (ἔκφερ᾽ at 3-3.5 in Il. 23.259). αὖ at 5 kept long before ὃ: attested once (Il. 3.383@3), at a sense pause. ὃ δ᾽ ἐπέσσυτο 5.5-8 (Il. 21.234, 21.601); τυτθὸν ὀπίσσω 9-12 (Il. 5.443). Word ends 2, 4, 5, 5.5, 8, 9.5 / same; penthemimeral + trochaic; bucolic D | **PASS** |
| 54 | v3 50 (6-12 replaced) | DDDDSS | - | ἐν δ᾽ ἐτίθει δύο κῆρε 1-5.5 (Il. 8.70, 22.210). μάχης SL at 6-7 (58x). θαλερῶν αἰζηῶν 7.5-12 (Il. 10.259, 14.4). **Spondaic fifth foot** (flagged): forced, and both Homeric instances are SDDDSS. Word ends 1, 3, 4, 5.5, 7, 9 / same; trithemimeral + trochaic + hephthemimeral | **PASS** |
| 56 | v3 52 (9.5-12 replaced) | DDDDDS | - | 1-9 as v3 52: ἕλκε δὲ μέσσα λαβών· ῥέπε δ᾽ = Il. 8.72, 22.212 (1-7); Ἑλβετίου 7-9 MO. τότ᾽ at 9.5 (3x before a vowel). ἐέλδωρ 10-12 (9 of 10 Homeric instances). Elision before ἐέλδωρ attested (Od. 3.418, 17.242). Word ends 1.5, 2, 3.5, 5, 6, 9, 9.5 / 2, 3.5, 5, 6, 9, 9.5; lexical end at 6 after a penthemimeral caesura | **PASS** |
| 58 | v3 54 (replaced) | DDDDDS | - | τὸν δ᾽ 1-1.5. ἕτερος SSL at 1.5-3 (Od. 8.374), -ος long by ς+μ. μετέπειτα 3.5-5.5 (Il. 14.310). μάλα σχεδὸν ἦλθε διώκων 6-12 = Il. 23.499 (same quantities); -λα long by σχ at 7. Word ends 1, 3, 5.5, 7, 8, 9.5 / same; trithemimeral + trochaic + hephthemimeral; bucolic D | **PASS** |
| 59 | v3 55 (comma only) | DDDSDS | - | Scansion identical to v3 55 (punctuation does not enter it). Νοβῆκος 6-8 after short τε, -κος long by ς+κ. Naeke as 37 | **PASS** |
| 61 | v3 57 (replaced) | DDDDDS | - | ἤμβροτες οὐδ᾽ ἔτυχες 1-5 (Il. 5.287). Here -χες is long by ς+Φ at 5; Il. 5.287 needs lengthening_closed there before ἀτάρ, so this verse is tier 0. Φεδερεῦ SSL at 5.5-7 (cf. Ἀχιλεῦ at 5.5-7 3x). μάλα πολλὰ 7.5-9.5 (5x); πολλὰ μογήσας 9-12 (13x). Word ends 2, 3, 5, 7, 8, 9.5 / 2, 5, 7, 8, 9.5; penthemimeral + hephthemimeral; bucolic D | **PASS** |
| 62 | v3 58 (replaced) | SDDSDS | - | Σέρβῳ δ᾽ LL at 1-2. ἀντιθέῳ LSSL at 3-5: ι short (3x at 3-5; warning, jsonl entry). τότε δή at 5.5-7 (2x: Il. 10.366, 23.374). Ζεὺς κῦδος ἔδωκε 8-12 = Il. 8.216, the same pattern SDDSDS and the same word ends from 5. Naeke (δὴ Ζεὺς). Word ends 2, 5, 6, 7, 8, 9.5 / 2, 5, 7, 8, 9.5; penthemimeral + hephthemimeral | **PASS** |
| 63 | v3 59 (6-12 replaced) | SSDDDS | - | ὣς οἳ μὲν μάρναντο 1-5.5 = Il. 11.596 (same quantities); Διὸς δ᾽ ἐτελείετο βουλή 6-12 = Il. 1.5, Od. 11.297 (Δι short, 0/250; -ὸς long by ς+δ). Word ends 1, 2, 3, 5.5, 7, 10 / 1, 3, 5.5, 7, 10; trithemimeral + trochaic + hephthemimeral | **PASS** |

## Discrepancies with the composer's jsonl and with check_line

**Scansion: none.** On all 64 verses the jsonl `scansion` and `check_line` blocks equal the fresh run, and on the 20 hand-scanned verses they equal my pattern and L/S string. The quantity justifications in the jsonl `quantity_notes` (κρατεροῦ at the longum, κήρῡκες, αὖ before ὃ, ἔτυχες before Φ, δὴ Ζεύς) agree with mine.

Mapping and documentation (none affects a verdict; they are for the record corrections of the final poem.jsonl):

1. **23, mapping.** The jsonl gives `v3_line: 23`, `changed: true`. By string, v4 23 is v3 27 verbatim (= v4 28): the replacement of v3 23 by the line of v3 27, as its `notes` say. I report it as unchanged, v3 PASS. The whole-line repetition at five lines' distance is for the critic.
2. **20.**
   * `sources`: "ἐσσυμένως (12x: 7 line-initial, 3 at 7-9 …)" should read **6 at 1-3, 4 at 7-9, 2 at 3-5** (`--loose "εσσυμενως" --word`).
   * `modifications` (substitution): "the name formula fills 6-12 as in Il. 2.563" is stale, because v4 20 has no name formula.
3. **24.** The πύματον count is given three ways: 8x (sources), "3.5-5 (5x) and 5.5-7 (2x)" (mobility) and "6x" (coinages, quantity_notes). `--loose "πυματον" --word` gives **8: 6 at 3.5-5, 2 at 5.5-7** (Il. 11.759, Od. 2.20).
4. **33.**
   * `quantity` basis and `quantity_notes` say "the line is Il. 13.85 verbatim", and a `sources` entry says "the verse is Il. 13.85 verbatim with λέλυντο". The verse is verbatim only at 3-12, as its own `modifications` say. The quantity argument stands, because ἀργαλέῳ has the same positions.
   * The τοῖιν δ᾽ entry gives count 2 against query_hits 1 (the second is Od. 18.34 τοῖϊν δέ, a different spelling).
5. **56.** "ἐέλδωρ (10x, all verse-final 10-12)": 9 are verse-final, and Od. 23.54 has it at 6-8.
6. **62.**
   * "τότε δὴ (43x; at 5.5-7 … e.g. Od. 9.52)": Od. 9.52 has it at 3.5-5. The 5.5-7 instances are **Il. 10.366, 23.374** (2 of 43; 37 at 1.5-3, 4 at 3.5-5).
   * The ἀντιθέῳ `quantity` basis "attested by position" should say "by the metre of Il. 4.377, 5.629, 16.649 (LSSL at 3-5)". The ι is in an open syllable, so position plays no part.
7. **50-52 (unchanged strings, stale records after dropping v3 47).**
   * 50 `notes`: "now four lines 45-48: Il. 22.162-164 verbatim". It is now three lines, 50-52.
   * 51 `notes`: "ἄεθλον's apposition (ἢ τρίπος …) follows as in Il. 22.164". It no longer follows.
   * 51 has no line-end punctuation before 52's ὣς. Metrically irrelevant; the punctuation and the enjambment label ("necessary") are for the philologist.
8. **59, stale numbering.**
   * `name_formula` "the Ῥογῆρος slot of 27 and 33" should be 23, 28, 37.
   * `notes` "the line is the system of 33" should be 37, and "the next verse (56)" should be 60.
9. **29.** The `quantity` list is empty, which is correct because there is no warning. Note for the paper's licence count: the hiatus after κρατεροῦ rests on a single Homeric attestation (Il. 21.553@9). The same holds for αὖ in 49 (Il. 3.383@3).
10. **Tool observation, outside v4.** homer/digamma.tsv row `eipein` (`re:^ειπ.*$`) also matches εἵπετο, the imperfect of ἕπομαι, which has no digamma. That is why the composer's rejected variant of 49 (`… ὃ δ᾽ εἵπετο τυτθὸν ὀπίσσω`) was flagged elision_before_digamma and licence_unattested. No v4 verse is affected. A homer/ maintainer may want an `exclude` entry for εἵπετο, εἵποντο and the like.

## Evidence commands (repository root, `source .venv/bin/activate`)

* `python homer/check_line.py --file composition/drafts/v4.txt --json`: 64 verses, 0 flagged, 0 unmetrical, exit 0. The same on v3.txt gives byte-identical per-verse output for the 44 verbatim verses.
* Text comparison: Python over both files split on `\n`; every v4 string is looked up among all v3 strings, and `unicodedata.normalize('NFC', s) == s` is checked.
* `python homer/check_line.py "εἰ μὴ ἄρʼ οἱ βέλος ὠκὺ ἐτώσιον ἔκφυγε χειρός"`: flag elision_before_digamma, exit 1, so the check is active.
* Digamma and elision: every token of the changed verses passed through `scan.digamma_info`. Every elided token followed by a word whose initial vowel carries U+0314 (NFD) was listed and checked for τ/κ/π.
* `python homer/concordance.py --ngram` for: ἐπέσσυτο δαίμονι ἶσος (7, all 6-12); ὣς ἄρ᾽ ὅ γ᾽ (2); λάβ᾽ ἄεθλον (1, 9.5-12); ἀλλ᾽ ὅ γε (16); ἐνίκα (8: 5 at 10-12); ἀλλὰ καὶ ὧς (17); ὑπὸ χερσὶ (11: 9 at 3.5-5.5, 2 at 7.5-9.5); ἐδάμη (2); αὐτὰρ ὅ γ᾽ ἂψ (1); ἂψ ἐπόρουσε (2, 3-5.5); ἀμφήριστον ἔθηκεν (2, 7-12); ἀργαλέῳ καμάτῳ φίλα γυῖα (Il. 13.85); ὀψὲ δὲ δὴ (12); παρέλασσ᾽ (2); κήρυκες δ᾽ ἄρα λαὸν ἐρήτυον (Il. 18.503); ἔνθα καὶ ἔνθα (32: 21 at 9-12); καί νύ κεν ἔνθ᾽ (3); ἔλαβεν (3); ἄσπετον ἤρατο κῦδος (2); στῆ δὲ μάλ᾽ ἐγγὺς ἰών (5); ὃ δέ μιν (9: 8 at 5.5-7); οὐδ᾽ ἀφάμαρτε (4: 2 at 9-12); ὃ δ᾽ ἐπέσσυτο (2); τυτθὸν ὀπίσσω (Il. 5.443); ἐν δ᾽ ἐτίθει δύο κῆρε (2); θαλερῶν αἰζηῶν (2); αἰζηῶν (11, all 10-12); ἕλκε δὲ μέσσα λαβών (2); ἐέλδωρ (10: 9 at 10-12); μετέπειτα (5); μάλα σχεδὸν (8: 6 at 6-8); ἦλθε διώκων (2); ἤμβροτες οὐδ᾽ ἔτυχες (Il. 5.287); πολλὰ μογήσας (13, all 9-12); μάλα πολλὰ (20: 5 at 7.5-9.5); Ἀχιλεῦ (13: 3 at 5.5-7); Ζεὺς κῦδος ἔδωκε (Il. 8.216); τότε δὴ (43: 2 at 5.5-7); ὣς οἳ μὲν μάρναντο (5); Διὸς δ᾽ ἐτελείετο βουλή (2); ἀντιθέῳ (11: 3 at 3-5).
* `--loose … --word`: εσσυμενως (12: 6 at 1-3, 4 at 7-9, 2 at 3-5); πυματον (8); πυματην (Il. 18.608); καματω (14: 4 at 5.5-7). `--regex "ʼ ἐέλδωρ"`: Od. 3.418, 17.242. `--regex "ʼ εἵπετο"`: 0. `--exact` δῆμος 7, δήμου 8, νῆσος 5, νήσου 9, δῆμου 0, νῆσου 0.
* Word slots and per-word quantities: a scratch script joining homer/scansion.tsv (unique lines) with homer/lines.tsv, tabulating `word_positions` × `word_meter` per loose form. Results:
  * ἀργαλε- 56 (all LSSL/LSSLX; ἀργαλέῳ LSSL at 3-5 ×6); ἀντιθε- 56 (ἀντιθέῳ LSSL ×8, 3 at 3-5);
  * κρατεροῦ SSL ×3 (7.5-9 ×2, 3.5-5 ×1); ἐδάμη SSL at 1.5-3 ×2; τοῖιν LL at 1-2 ×2, LS at 5-5.5 ×2;
  * βάλεν SS at 7.5-8 ×14; μιν L at 7 ×52; αὖ L at 5 ×11; μάχης SL at 6-7 ×58; μάχῃ SL at 6-7 ×24;
  * ἐπήπυον SLSS at 6-8 ×1; δόχμια LSS at 9-10 ×1; ἔτυχες SSL at 3.5-5 ×1; ἕτερος SSL at 1.5-3, 5.5-7, 7.5-9;
  * ἐπόρουσε SSLS at 3.5-5.5 ×15; ἀμφήριστον LLLS at 7-9.5 ×2; ἀμφίς LS at 9-9.5 ×22; ἀρωγοί SLL at 10-12 ×5; ἔκφερεν LSS at 1-2 ×1.
* scansion.tsv records compared syllable for syllable: Il. 23.116, 18.502, 18.503, 8.216, 11.596, 1.5, 4.496, 23.499, 5.443, 3.379, 2.860, 23.382, 21.553, 3.383, 10.259, 14.4, 13.85, 22.210, 8.72, 5.287.
* dichrona.tsv rows used:
  * ἄρʼ ἄ 0/538; ἐπέσσυτο υ 0/12; δαίμονι ι 0/2; μιν ι 0/277; ἐδάμασσε ά 0/7; ἐσσυμένως υ 0/12; λάβʼ ά 0/3; ἄεθλον ἄ 0/27;
  * ἔπειτα α 0/215; μάχῃ ά 0/24; πυματ- υ 0/15, α 0/15; ἐνίκα ί 8/0; ἄναντα, κάταντα, πάραντα, δόχμια 0/1 each vowel;
  * ἀλλά 0/386; ἐδάμη ά 0/2; κρατεροῦ α 0/3; ὑπό 0/229; χερσί 0/65; αὐτάρ 0/706; τοῖιν ι 0/2; καμάτῳ 0/8; φίλα 0/28, 0/16; γυῖα 0/14; παρέλασσʼ α 0/2; ἀγαθός 0/56;
  * λαοί α 45/0; ἀμφοτέροισιν ι 0/9; ἐπήπυον υ 0/1; ἀμφίς 0/22; ἀρωγοί 0/5; κήρυκες υ 19/0; ἄρα 0/545, 0/408; λαόν α 73/0; ἐρήτυον υ 0/4; ἔνθα 0/259;
  * νύ 0/103; ἔλαβεν 0/3; ἤρατο 0/3; μάλʼ 0/152; ἐγγύς 0/20; ἰών 0/87; βάλεν 0/44; ἀφάμαρτε 0/4; ἐτίθει 0/14; δύο 0/42; μάχης 0/68; θαλερῶν 0/2; μέσσα 0/2; λαβών 0/35;
  * μετέπειτα 0/4; μάλα 0/314, 0/262; διώκων 0/9; ἔτυχες 0/1; πολλά 0/216; Διός 0/250.
* licences.tsv: correption καί 2364 (Il. 1.116@2); digamma ἶσος 19; hiatus_long κρατεροῦ 1 (Il. 21.553@9); hiatus_long αὖ 1 (Il. 3.383@3).
* Baselines: `awk -F'\t' 'NR>1&&$4=="unique"{n++; p[$8]++; if(substr($8,5,1)=="S")s++; if($19~/naeke/)k++} END{print n,p["DDDDSS"],p["SDDSDS"],s,k}' homer/scansion.tsv` → 27162, 287, 1666, 1364, 1904.

## Appendix: hand scansion of the 20 non-verbatim verses, syllable by syllable

Legend, as in scansion_v1-v3:

* L long, S short, X final anceps.
* n = nature (η ω, diphthong, ᾳ ῃ ῳ, circumflex; ε ο short).
* p(..) = position, with the consonants.
* c = epic correption; hl = long vowel kept long in hiatus at a longum.
* d = digamma (homer/digamma.tsv) blocks hiatus.
* dt = homer/dichrona.tsv (long/short counts); an = dichrona_analogy.tsv; cc = concordance or scansion.tsv attestation (cited).
* MO = metre-only quantity of an invented name.

Syllables are written with the consonants they are pronounced with. Word ends are orthographic / lexical, final 12 omitted. In 20 and 32 the word ends are the corrected ones (see Summary).

**19** ὣς ἄρ᾽ ὅ γ᾽ Ἑλβέτιος τότ᾽ ἐπέσσυτο δαίμονι ἶσος·  
DDDDDS: ὣς L n · σἄ S dt(0/538) · ρὅ S n · γἙλ L p(λβ) · βέ S n · τι S MO · ος L p(ς τ) · τό S n · τἐ S n · πέσ L p(σσ) · συ S dt(0/12) · το S n · δαί L n · μο S n · νι S dt(0/2), d · ἶ L n · σος X  
1, 1.5, 2, 5, 5.5, 8, 10 / 1.5, 2, 5, 5.5, 8, 10. Licences: digamma@10(ἶσος).

**20** τρὶς δέ μιν αὖτ᾽ ἐδάμασσε καὶ ἐσσυμένως λάβ᾽ ἄεθλον.  
DDDDDS: τρὶς L p(ς δ) · δέ S n · μι S dt(0/277) · ναὖ L n · τἐ S n · δά S dt(0/7) · μασ L p(σσ) · σε S n · καὶ S c · ἐσ L p(σσ) · συ S dt(0/12) · μέ S n · νως L n · λά S dt(0/3) · βἄ S dt(0/27) · ε L p(θλ), cc(Il. 23.511) · θλον X  
1, 1.5, 2, 3, 5.5, 6, 9, 9.5 / 2, 3, 5.5, 9, 9.5. Licences: correption@6(καὶ).

**24** ἀλλ᾽ ὅ γε Σέρβος ἔπειτα μάχῃ πυμάτῃ μιν ἐνίκα.  
DDDDDS: ἀλ L p(λλ) · λὅ S n · γε S n (single σ) · Σέρ L p(ρβ) · βο S n · σἔ S n · πει L n · τα S dt(0/215) · μά S dt(0/24) · χῃ L n · πυ S dt(πυματ- 0/15), an · μά S dt(πυματ- 0/15), an · τῃ L n · μι S dt(0/277) · νἐ S n · νί L dt(8/0) · κα X  
1, 1.5, 2, 3.5, 5.5, 7, 9, 9.5 / 2, 3.5, 5.5, 7, 9.5. Licences: -.

**27** πολλὰ δ᾽ ἄναντα κάταντα πάραντά τε δόχμιά τ᾽ ἦλθον,  
DDDDDS: πολ L p(λλ) · λὰ S dt(0/216) · δἄ S dt(0/1) · ναν L p(ντ) · τα S dt(0/1) · κά S dt(0/1) · ταν L p(ντ) · τα S dt(0/1) · πά S dt(0/1) · ραν L p(ντ) · τά S dt(0/1) · τε S n · δόχ L p(χμ) · μι S dt(0/1) · ά S dt(0/1) · τἦλ L n · θον X  
1.5, 3.5, 5.5, 7.5, 8, 10 / 1.5, 3.5, 5.5, 8, 10 (= scansion.tsv Il. 23.116). Licences: -.

**29** ἀλλὰ καὶ ὧς ἐδάμη κρατεροῦ ὑπὸ χερσὶ Νοβήκου·  
DDDDDS: ἀλ L p(λλ) · λὰ S dt(0/386) · καὶ S c, cc(Il. 1.116) · ὧ L n · σἐ S n · δά S dt(0/2) · μη L n · κρα S dt(0/3) · τε S n · ροῦ L n, hl, cc(Il. 21.553) · ὑ S dt(0/229) · πὸ S n · χερ L p(ρσ) · σὶ S dt(0/65) · Νο S n · βή L n · κου X  
1.5, 2, 3, 5, 7, 8, 9.5 / 3, 5, 7, 9.5. Licences: correption@2(καὶ); hiatus_long@7(κρατεροῦ).

**32** αὐτὰρ ὅ γ᾽ ἂψ ἐπόρουσε καὶ ἀμφήριστον ἔθηκεν·  
DDDSDS: αὐ L n · τὰ S dt(0/706) · ρὅ S n · γἂπ L p(ψ) · σἐ S n · πό S n · ρου L n · σε S n · καὶ S c · ἀμ L p(μφ) · φή L n · ρισ L p(στ) · το S n · νἔ S n · θη L n · κεν X  
1.5, 2, 3, 5.5, 6, 9.5 / 1.5, 2, 3, 5.5, 9.5. Licences: correption@6(καὶ).

**33** τοῖιν δ᾽ ἀργαλέῳ καμάτῳ φίλα γυῖα λέλυντο.  
SDDDDS: τοῖ L n · ιν L p(νδ) · δἀρ L p(ργ) · γα S cc(ἀργαλε- 56/56 LSSL(X); Il. 13.85) · λέ S n · ῳ L n · κα S dt(0/8) · μά S dt(0/8) · τῳ L n · φί S dt(0/28) · λα S dt(0/16) · γυῖ L n · α S dt(0/14) · λέ S n · λυν L p(ντ) · το X  
2, 5, 7, 8, 9.5 / same. Licences: -.

**34** ὀψὲ δὲ δὴ παρέλασσε βοὴν ἀγαθὸς Φεδερῆρος·  
DDDDDS: ὀπ L p(ψ) · σὲ S n · δὲ S n · δὴ L n · πα S dt(παρέλασσʼ 0/2), an · ρέ S n · λασ L p(σσ) · σε S n · βο S n · ὴν L n · ἀ S dt(0/56) · γα S dt(0/56) · θὸς L p(ς φ) · Φε S n · δε S n · ρῆ L n · ρος X  
1.5, 2, 3, 5.5, 7, 9 / 3, 5.5, 7, 9. Licences: -.

**35** λαοὶ δ᾽ ἀμφοτέροισιν ἐπήπυον, ἀμφὶς ἀρωγοί·  
SDDDDS: λα L dt(45/0) · οὶ L n · δἀμ L p(μφ) · φο S n · τέ S n · ροι L n · σι S dt(0/9) · νἐ S n · πή L n · πυ S dt(0/1) · ο S n · νἀμ L p(μφ) · φὶ S dt(0/22) · σἀ S dt(0/5) · ρω L n · γοί X  
2, 5.5, 8, 9.5 / same (= scansion.tsv Il. 18.502). Licences: -.

**36** κήρυκες δ᾽ ἄρα λαὸν ἐρήτυον ἔνθα καὶ ἔνθα.  
SDDDDS: κή L n · ρῡ L dt(19/0) · κες L p(ς δ) · δἄ S dt(0/545) · ρα S dt(0/408) · λᾱ L dt(73/0) · ὸ S n · νἐ S n · ρή L n · τυ S dt(0/4) · ο S n · νἔν L p(νθ) · θα S dt(0/259) · καὶ S c · ἔν L p(νθ) · θα X  
3, 4, 5.5, 8, 9.5, 10 / 4, 5.5, 8, 9.5. Licences: correption@10(καὶ).

**38** καί νύ κεν ἔνθ᾽ ἔλαβέν τε καὶ ἄσπετον ἤρατο κῦδος,  
DDDDDS: καί L n · νύ S dt(0/103) · κε S n · νἔν L p(νθ) · θἔ S n · λα S dt(0/3) · βέν L p(ν τ) · τε S n · καὶ S c · ἄσ L p(σπ) · πε S n · το S n · νἤ L n · ρα S dt(0/3) · το S n · κῦ L n · δος X  
1, 1.5, 2, 3, 5, 5.5, 6, 8, 10 / 2, 3, 5.5, 8, 10. Licences: correption@6(καὶ).

**40** στῆ δὲ μάλ᾽ ἐγγὺς ἰών, ὃ δέ μιν βάλεν, οὐδ᾽ ἀφάμαρτε.  
DDDDDS: στῆ L n · δὲ S n · μά S dt(0/152) · λἐγ L p(γγ) · γὺ S dt(0/20) · σἰ S dt(0/87) · ὼ L n · νὃ S n · δέ S n · μιν L p(ν β) · βά S dt(0/44) · λε S n · νοὐ L n · δἀ S dt(0/4) · φά S dt(0/4) · μαρ L p(ρτ) · τε X  
1, 1.5, 2, 3.5, 5, 5.5, 6, 7, 8, 9 / 1.5, 2, 3.5, 5, 7, 8. Licences: -.

**49** Σέρβος δ᾽ ἔκφερεν αὖ, ὃ δ᾽ ἐπέσσυτο τυτθὸν ὀπίσσω.  
SDDDDS: Σέρ L p(ρβ) · βος L p(ς δ) · δἔκ L p(κφ) · φε S n · ρε S n · ναὖ L n, hl, cc(Il. 3.383) · ὃ S n · δἐ S n · πέσ L p(σσ) · συ S dt(0/12) · το S n · τυτ L p(τθ) · θὸ S n · νὀ S n · πίσ L p(σσ) · σω X  
2, 4, 5, 5.5, 8, 9.5 / same. Licences: hiatus_long@5(αὖ).

**54** ἐν δ᾽ ἐτίθει δύο κῆρε μάχης θαλερῶν αἰζηῶν,  
DDDDSS: ἐν L p(ν δ) · δἐ S n · τί S dt(0/14) · θει L n · δύ S dt(0/42) · ο S n · κῆ L n · ρε S n · μά S dt(0/68) · χης L n · θα S dt(0/2) · λε S n · ρῶ L n · ναἰ L n · ζη L n · ῶν X  
1, 3, 4, 5.5, 7, 9 / same. Licences: -. Spondaic fifth foot (ρῶ ναἰ), forced.

**56** ἕλκε δὲ μέσσα λαβών· ῥέπε δ᾽ Ἑλβετίου τότ᾽ ἐέλδωρ.  
DDDDDS: ἕλ L p(λκ) · κε S n · δὲ S n · μέσ L p(σσ) · σα S dt(0/2) · λα S dt(0/35) · βών L n · ῥέ S n · πε S n · δἙλ L p(λβ) · βε S n · τί S MO · ου L n · τό S n · τἐ S n · ἔλ L p(λδ) · δωρ X  
1.5, 2, 3.5, 5, 6, 9, 9.5 / 2, 3.5, 5, 6, 9, 9.5. Licences: -.

**58** τὸν δ᾽ ἕτερος μετέπειτα μάλα σχεδὸν ἦλθε διώκων.  
DDDDDS: τὸν L p(ν δ) · δἕ S n · τε S n · ρος L p(ς μ) · με S n · τέ S n · πει L n · τα S dt(0/4) · μά S dt(0/314) · λα L p(σχ) · σχε S n · δὸ S n · νἦλ L n · θε S n · δι S dt(0/9) · ώ L n · κων X  
1, 3, 5.5, 7, 8, 9.5 / same. Licences: -.

**59** καὶ βάλεν, οὐδ᾽ ἀφάμαρτε, Νοβῆκος, καὶ βάλεν αὖτις·  
DDDSDS: καὶ L n · βά S dt(0/44) · λε S n · νοὐ L n · δἀ S dt(0/4) · φά S dt(0/4) · μαρ L p(ρτ) · τε S n · Νο S n · βῆ L n · κος L p(ς κ) · καὶ L n · βά S dt(0/44) · λε S n · ναὖ L n · τις X  
1, 2, 3, 5.5, 8, 9, 10 / 2, 5.5, 8, 10. Licences: -. Naeke.

**61** ἤμβροτες, οὐδ᾽ ἔτυχες, Φεδερεῦ, μάλα πολλὰ μογήσας.  
DDDDDS: ἤμ L n · βρο S n · τε S n · σοὐ L n · δἔ S n · τυ S dt(0/1) · χες L p(ς φ) · Φε S n · δε S n · ρεῦ L n · μά S dt(0/314) · λα S dt(0/262) · πολ L p(λλ) · λὰ S dt(0/216) · μο S n · γή L n · σας X  
2, 3, 5, 7, 8, 9.5 / 2, 5, 7, 8, 9.5. Licences: -.

**62** Σέρβῳ δ᾽ ἀντιθέῳ τότε δὴ Ζεὺς κῦδος ἔδωκε.  
SDDSDS: Σέρ L p(ρβ) · βῳ L n · δἀν L p(ντ) · τι S cc(ἀντιθέῳ LSSL ×8; Il. 4.377, 5.629, 16.649 at 3-5) · θέ S n · ῳ L n · τό S n · τε S n · δὴ L n · Ζεὺς L n · κῦ L n · δο S n · σἔ S n · δω L n · κε X  
2, 5, 6, 7, 8, 9.5 / 2, 5, 7, 8, 9.5. Licences: -. Naeke (as Il. 8.216).

**63** ὣς οἳ μὲν μάρναντο, Διὸς δ᾽ ἐτελείετο βουλή·  
SSDDDS: ὣς L n · οἳ L n · μὲν L p(ν μ) · μάρ L p(ρν) · ναν L p(ντ) · το S n · Δι S dt(0/250) · ὸς L p(ς δ) · δἐ S n · τε S n · λεί L n · ε S n · το S n · βου L n · λή X  
1, 2, 3, 5.5, 7, 10 / 1, 3, 5.5, 7, 10. Licences: -.
