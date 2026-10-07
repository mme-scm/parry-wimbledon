# Philology review of draft v2 (60 verses)

Reviewed: `composition/drafts/v2.txt`, with glosses, sources and enjambment labels from `composition/drafts/v2.jsonl`. Checked against `review/round_1.md` (rulings R1-R8 and the plan-conformance notes), `composition/brief.md` (§1 facts, §4 names, §5.2 lexicon, §5.4 prohibitions, Addendum A1) and my own v1 report (`review/philology_v1.md`). Reviewer: philologist agent, 2026-10-07. The scansion and provenance verifiers are separate; points for them are in §6.

## 1. Method and sources

* **Homeric evidence.** Every Homeric claim comes from `python homer/concordance.py` (Perseus: Monro-Allen Iliad, Murray Odyssey; homer/README.md), or from small scripts that call its `Concordance` class (Appendix B). Each judgement in §7 gives its query and hits. Positions in square brackets use the half-foot numbering of homer/README.md. The verbatim outputs behind every FAIL and QUERY, and behind the new name forms, are in Appendix A. `check_line.py` was run on the whole draft (60/60 pass with no flags) and on each remedy proposed below.
* **Unchanged verses.** `identity.py` (Appendix B.1) compared every v2 verse character by character with the v1 verse named in its `v1_line` field. 29 verses are identical. 28 of them were v1 PASS lines; each is reported as "unchanged, v1 PASS" after I checked that its new neighbours do not change its syntax or its enjambment. The other two cases were reviewed in full: 45 (= v1 42, a v1 FAIL) and 37 (= v1 37, a v1 PASS whose preceding line changed).
* **Lexica.** I fetched LSJ entries on 2026-10-07 and quote them in Appendix A.10:
  * from the Logeion API (`anastrophe.uchicago.edu/logeion-api/detail?w=…`, LSJ text): δαμάζω, δεύτερος, ἄφαρ, ἄψ, ἐξάλλομαι, ἀνίημι, κέρδος;
  * δαμάζω and δεύτερος were also read on Perseus (`perseus.tufts.edu/hopper/text?doc=Perseus:text:1999.04.0057:entry=…`).

  I did not fetch Cunliffe and make no claim from it. Anything else is marked [unverified].
* **Enjambment.** I used the same criteria as in v1: Parry 1929 as quoted by Dukat 1991 (*Oral Tradition* 6/2-3, 303-315), fetched for v1 on 2026-10-07 and quoted in philology_v1.md A.7. Under Kirk's punctuation test as tabulated by Dukat:
  * a printed strong stop is **none**;
  * a complete sentence continued after a comma, or with no punctuation, is **unperiodic**;
  * an incomplete sentence is **necessary**, including any verse inside an open ὡς δ᾽ ὅτε period before its apodosis.

  Parry's own text was not accessed [unverified at first hand].
* **Verdicts.** **PASS** means no philological defect (notes may still apply). **FAIL** means a defect in morphology, orthography, prosody or syntax, or a mismatch between the Greek and its gloss, shown by the evidence. **QUERY** means a human decision is needed.
* **Reproducibility.** The verdict and enjambment counts in §2 and §5 were printed by the tally script in Appendix B.9, run on the table in §7.

## 2. Summary

**Verdicts (60 lines): PASS 55, FAIL 3, QUERY 2.** One further poem-level QUERY (P1, below) is not counted per line, because ruling R3 sanctions the usage.

**Failing lines (3)**

| line | reason | tested remedy (check_line: no flags) |
|---|---|---|
| 44 | **Unmarked change of subject carried by a participle.** The gloss makes Federer the subject of ὄρνυτο, but the Greek has no new subject. κέρδεα εἰδώς is a participial phrase; it and all 30 Homeric verse-final … εἰδώς phrases stand in apposition to a subject already present. Both Homeric ἐπὶ δ᾽ ὄρνυτο lines name the man who follows (Il. 23.689, 23.759). As written, the line says that Djokovic drew ahead and rushed on, "knowing cunning ways". That also gives Federer's craft epithet to Djokovic. | `ἔκφερε δ᾽ αὖ Ζοκοβεύς· ὃ δ᾽ ἐπέσσυτο κέρδεα εἰδώς.` (ὃ δ᾽ ἐπέσσυτο at 5.5-8: Il. 21.234, 21.601) |
| 55 | **Accent.** Νοβήκος must be **Νοβῆκος**: a long accented penult before short -ος takes the circumflex. Homer has 0 words in η/ω + consonant + -ος with the acute, against 51 types (269 tokens) with the circumflex. The poem itself writes Ῥογῆρος and Φεδερῆρος. The error comes from R3 and A1, which should be corrected as well. The line also has the count problem of line 33. | `καὶ βάλεν, οὐδ᾽ ἀφάμαρτε Νοβῆκος δεύτερον αὖτις·` |
| 56 | **Aspiration.** In αὖτ᾽ Ἑλβέτιος the elided αὖτε stands before a rough breathing, so it must be written **αὖθ᾽**. Homer has αὖθ᾽ before a rough breathing 33x and αὖτ᾽ 0x, and no elided τ/π/κ stands before a rough breathing anywhere in the text. The poem itself writes αὖθ᾽ Ἑλβέτιος in line 24. | `ἔνθ᾽ αὖθ᾽ Ἑλβέτιος προΐει, βάλε δ᾽ ἂψ Ζοκοβείδης,` |

**Query lines (2)**

| line | question for a human |
|---|---|
| 33 (also 55) | **The count.** δεύτερον αὖτις means "a second time". In all 5 Homeric uses it marks one action repeated after an earlier, separately narrated one. So line 33 narrates one unmissed strike, as a repeat of line 27, while the fact behind it is two aces (points 357-358). Line 55 likewise narrates one strike for two winners (points 420-421). The jsonl's claim that "δεύτερον αὖτις counts the two" misreads the phrase, and brief §3.1's arithmetic note ("twice he cast and twice he did not miss") is not met. Line 24 does count correctly: δάμασεν καὶ δεύτερον αὖτις. |
| 37 | **Whose fourth onset?** Line 36 now ends with Djokovic as named subject, so the unexpressed subject of ἐπέσσυτο is first read as Djokovic. Only line 38 (Σέρβος δ᾽ … ἐναντίον) shows that it was Federer. Homer does switch back to an earlier subject unmarked in this very line (Il. 5.437 Apollo → 5.438 Diomedes; 16.703 Apollo → 16.705 Patroclus). But in all four Homeric uses, the τρὶς μέν (… τρὶς δ᾽) lines before it fix who the attacker is. Here no count precedes, and only two of the four points 359-362 are narrated, so "the fourth" has no third. |

**Poem-level QUERY P1 (not counted per line; for FOR_HUMAN.md): the patronymic's base.**
* The poem calls Djokovic both Ζοκοβεύς (23, 44; genitive Ζοκοβῆος in 51) and Ζοκοβείδης, "son of Ζοκοβεύς" (4, 36, 53, 56).
* In Homer a patronymic is built on the father's name, which is a different word from the son's own name: Πηλεΐδης (Achilles) from Πηλεύς; Ἀμαρυγκεΐδης (Il. 2.622, of Diores) from Ἀμαρυγκεύς (Il. 23.630, the father). R3's analogy "Ἀχιλλεύς beside Πηλεΐδης" does not cover a patronymic formed from the hero's own name.
* If Ζοκοβεύς is Đoko, the eponymous ancestor (R3: "Đoković … 'son of Đoko'"), then using Ζοκοβεύς for Novak himself is the anomaly.
* Options:
  * reserve Ζοκοβεύς for the ancestor and give its slots another form (A1 allows any slot that passes check_line);
  * accept the anomaly as a convention and say so in the paper.

**Rulings applied (whole draft; Appendix A.9)**

| ruling | status in v2 | evidence |
|---|---|---|
| R2 Ῥογῆρος not before ἰσόθεος φώς | applied: ἰσόθεος is absent; Ῥογῆρος stands before κ (27) and δ (33), long by position | rulings script: ἰσόθε- 0 |
| R3 Ζοκοβείδης / Νοβήκος | applied: Ζοκοβίδης and Νοβάκος are absent; Ζοκοβείδης is verified as a Homeric formation (line 4). **But the accent of Νοβήκος is wrong (FAIL 55), and P1 is open** | Ζοκοβείδης 4x (4, 36, 53, 56), Νοβήκος 1x (55) |
| R4 no δίς + verb | applied: δίς 0. Its replacement δεύτερον αὖτις counts correctly in 24 but not in 33 or 55 (QUERY) | δίς 0 |
| R5 at most two ἐξενάριξε, inside the aristeia | applied: ἐξεναρ- 0. The victory and break verb is now δαμάζω (20, 24, 29, 30, 34, 58), a Homeric use (LSJ III "subdue, conquer"; non-lethal Il. 6.159, 14.316). Note: 14 of the 18 Homeric active aorists are killings. | ἐξεναρ- 0; δαμασ- 6 (+ 40, Homer verbatim) |
| R6 πάλιν only "back" | applied: only 22 (βάλλον πάλιν "struck back") | πάλιν 1 |
| R7 facts | applied: 5 no longer says "first"; 28 no longer says "thus". No line states anything outside brief §1, and nothing after point 422 is narrated (1.11) | per-line facts in §7 |
| R1 / A1 name slots | all new slots pass check_line with no flags (Σέρβος 9-9.5 in 15, Σέρβον 3-3.5 in 43, Νοβήκος 6-8 in 55, Ἑλβέτιος 3-5 in 24, 54, 56) | check_line --file: 60/60 OK |
| similes need ≥3 lines and an apodosis | applied: horse 16-18 → 19; lion 38-42 → 43; racing horses 45-47 → 48. No simile lacks its apodosis | simile script (A.8) |
| v1 FAILs | 4, 35, 39-40, 42-43 repaired | §7 |

**Dialect and morphology, in brief.**
* The base is Ionic-epic throughout.
* New forms:
  * Ζοκοβείδης has good Homeric models with the diphthong: Ἀμαρυγκείδην Il. 4.517 and Ἀτρείδης Od. 15.52, both with unique scansions.
  * Νοβῆκος (accent corrected) takes Ionic η by ruling R3 (the dialect statement is [unverified] here, as in v1).
  * The duals are all Homeric: ἄνδρε, δαΐφρονε (coined, regular), ἐμαρνάσθην, διαστήτην, ἐρίσαντε, στήτην, ἀμφοτέρω, τώ, δινηθήτην.
* No Attic contractions. The only orthographic slip is the aspiration in 56.

**Lexicon.** No prohibited word occurs (rulings script, A.9). No post-Homeric word occurs except the sanctioned coinages (Ἑλβέτιος, Σέρβος and the name renderings). The Homeric words used in tennis senses all follow brief §5.2.

**Enjambment (composer = reviewer on all 60 lines).** None 32 (53.3%), unperiodic 18 (30.0%), necessary 10 (16.7%). Parry's Iliad sample is 48.5 / 24.8 / 26.6% (Dukat 1991:305). Necessary enjambment rose from 8/55 (14.5%) in v1 to 10/60, still far below the brief's target of "roughly a third".

## 3. Dialect and morphology

* **Ζοκοβείδης (4, 36, 53, 56).**
  * Homer has the diphthongal -είδης beside -εΐδης in patronymics of -εύς names:
    * Ἀμαρυγκείδην (Il. 4.517; scansion.tsv: unique, -κεί- long), beside Ἀμαρυγκεΐδης (Il. 2.622), from Ἀμαρυγκεύς (Il. 23.630);
    * Ἀτρείδης (Od. 15.52, unique, LLL), Ἀτρείδῃσιν (Od. 19.183) and Ἀτρείδαο (Od. 24.35, unique): 3 of the 210 hits of the loose query ατρειδ, the rest Ἀτρεΐδ-;
    * Πηλείδη (Il. 1.277): 1 of the 52 hits of πηλειδ, the other 51 Πηλεΐδ-.
  * The jsonl cites only Il. 1.277. Its scansion in scansion.tsv is `multiple` with a rare cross-word synizesis licence, so Il. 4.517 and Od. 15.52 are the better models.
  * Ζοκοβείδης is SSLL like Διομήδης, so no metre-only quantity is needed (R3's aim is met).
  * Accent: an acute on the long penult before long -ης, as in Ἀτρείδης (Od. 15.52).
  * The initial ζ makes position for the preceding -ος. In all four verses that syllable is a longum (9 after ἀντίθεος, κρατερός ×2; ἂψ before it in 56).
* **Νοβήκος (55): FAIL on the accent**; see §2 and Appendix A.4. Ζοκοβῆος, Ῥογῆρος, Φεδερῆρος and Φεδερῆρον are correctly circumflexed. Ἑλβετίου, ἀντιθέου and Ζοκοβείδης are correctly acute.
* **Aspiration (56): FAIL**; see §2 and A.5. Every other elision in the draft is correct before its breathing (A.5 draft check).
* **Digamma.** Every hiatus before a once-digammated word is inside an attested phrase: ὅ οἱ (9), κατὰ/ἐπὶ ἶσα (13, 21, 26), εἰ μή οἱ (35), δαίμονι ἶσος (37), κέρδεα εἰδώς (27, 44). check_line now flags elision before digamma; it reports none.
* **Augment.** Optional augment as in Homer: ἐδάμασσε / δάμασεν; ἔλαβεν / λάβ᾽; ἀπήμβροτε, ἐνίκα and ἀνῆκε augmented; ἔκφερε and ὄρνυτο unaugmented.
* **Moods.**
  * καί νύ κεν + aorist indicative and εἰ μή + aorist indicative (34-35) form the past unreal (Il. 3.373-374).
  * Generic subjunctives in the relative clause of the simile (39-40) are Homer verbatim.

## 4. Lexicon

* **Prohibited words** (brief §5.2/§5.4: γραμμή, στέγη, ὄχλος, ὥρη "hour", δίκτυον, ῥάβδος, χλόη, χόρτος, δικαστής, ἀθλητής, σφαιριστ-, ἡττ-): 0 (A.9).
* **Coinages, all sanctioned by §4/§5.3:**
  * Ἑλβέτιος (Latin-based [unverified]; v1's note on §5.4's "no Latin-based words" still stands);
  * Σέρβος (post-Homeric ethnic [unverified]);
  * Φεδερῆρος, Φεδερεύς, Ῥογῆρος, Ζοκοβεύς/-ῆος, Ζοκοβείδης, Νοβῆκος.
* **Homeric words in tennis senses** (brief §5.2), all checked:
  * δαμάζω for a break or a set (LSJ III "subdue, conquer"), with ἂψ "in return" (LSJ ἄψ 2) for a break back (30);
  * ἐνίκα for the first set (absolute νικάω: Il. 3.439);
  * τέτρατον for the fourth set as a prize (as Il. 23.538 τὰ πρῶτα);
  * κέρδεα εἰδώς, "skilled in wiles" (LSJ κέρδος II), as Federer's craft epithet;
  * ἀπήμβροτε and ἐτώσιον ἔκφυγε χειρός for errors;
  * καὶ βάλεν, οὐδ᾽ ἀφάμαρτε for winners and aces;
  * ἀμύνετο νηλεὲς ἦμαρ for points saved;
  * the lion and racing-horse similes.
* **Epithet fields** (plan note). ἰσόθεος φώς is gone, and Federer has the craft epithet κέρδεα εἰδώς (27). But Federer's διογενής and Djokovic's ἀντίθεος (4, 51) are still both "divine" epithets; Djokovic has no endurance epithet (brief §4.2 lists none that fits his slots). Line 44 as written would give κέρδεα εἰδώς to Djokovic (FAIL).
* **Fillers.** ἄφαρ was added at 5.5-6 in two lines (23, 32) to replace πάλιν. In 23 it is supported by ἄφαρ … αὐτίκα (Il. 23.593). In 32 it sits beside ὀψὲ δὲ δή ("late, at last"), a combination Homer never has; LSJ's sense 2 ("suddenly, quickly") makes it acceptable.

## 5. Enjambment

Counts from the tally script (Appendix B.9), out of 60 lines:

| | none | unperiodic | necessary |
|---|---|---|---|
| composer (jsonl) | 32 (53.3%) | 18 (30.0%) | 10 (16.7%) |
| reviewer | 32 (53.3%) | 18 (30.0%) | 10 (16.7%) |
| v1 composer (55 lines) | 35 (63.6%) | 12 (21.8%) | 8 (14.5%) |
| Parry's Iliad sample (Dukat 1991:305, from Parry 1929:204) | 48.5% | 24.8% | 26.6% |

* The composer adopted my v1 reclassifications (17, 22, 29, 34, v1 43 = v2 46, v1 54 = v2 59). v1 38 and v1 51 were rewritten, which made their reclassification moot.
* I agree with every label in v2. One judgement depends on my v1 rule that a verse inside an open ὡς δ᾽ ὅτε period is necessary even when the edition prints a raised stop: 47 (Il. 22.164 ends in ·).
* The lion simile (38-43) is a λέων ὣς comparison, not a ὡς δ᾽ ὅτε clause. Its main sentence is complete at 38, so 38 is unperiodic and 40 and 42 (strong stops) are none.
* The necessary lines are 1, 3, 16, 17, 18, 37, 39, 45, 46 and 47: the proem's period and three similes. The duel narrative (sets 1-5, the championship game, the tie-break) has only 37.
* The brief (§2.7) asked for the rallies and the championship game to run on. They do not: 25-27, 33-36 and 53-58 are end-stopped or unperiodic.

## 6. Points for the composer and the other verifiers (not philological verdicts)

* Stale cross-references in the jsonl:
  * jsonl 2 notes "ring with line 54-55"; this is now 59-60;
  * jsonl 46 facts "as line 42" and jsonl 50 facts "as line 44"; these are now 45 and 49.
* jsonl 4, 36, 53, 56 (Ζοκοβείδης): add Il. 4.517 Ἀμαρυγκείδην and Od. 15.52 Ἀτρείδης as the unique-scansion models (Il. 1.277 is `multiple`, with a rare synizesis licence).
* jsonl 15: add Il. 16.477 (absolute ἀπήμβροτε) and the asyndetic apodoses after οἳ δ᾽ ὅτε δή (Il. 3.15-16, 11.232-233).
* jsonl 20: τρὶς δέ without a preceding τρὶς μέν is attested (Od. 4.277; Il. 24.16, 24.273).
* jsonl 23: ἄφαρ strengthened by a second adverb, Il. 23.593.
* jsonl 29, 58: name + δ᾽ αὖτ᾽ + verb, as Il. 17.304 Ἕκτωρ δ᾽ αὖτ᾽ Αἴαντος ἀκόντισε.
* jsonl 30: the pronoun + appositive name-epithet model is αὐτὰρ ὃ … ἄναξ ἀνδρῶν Ἀγαμέμνων (Il. 2.402, 3.81).
* jsonl 33, 55: "counted by δεύτερον αὖτις" misdescribes the phrase (QUERY 33).
* jsonl 36: Il. 4.518-519 (βάλε δὲ + subject, object left to the context) is the closest parallel.
* jsonl 42: change the gloss "leaps out through the deep fold" to "leaps out of the deep fold" (LSJ ἐξάλλομαι).
* jsonl 43: ἀνίημι + accusative of person without an infinitive: Il. 7.25, 10.389, 21.395, 17.705. The structural model is the lion-simile apodosis Il. 12.307 (ὥς ῥα τότ᾽ … θυμὸς ἀνῆκε), which, unlike line 43, has an infinitive in 12.308.
* jsonl 44: the cited separation parallel Il. 11.472 has ὃ δ᾽ and the noun φώς, which line 44 lacks (FAIL).
* round_1.md R3 and brief A1: correct Νοβήκος to Νοβῆκος.
* Plan-conformance notes:
  * the three expanded points carry their clocks in the jsonl (25-27 at 2:47:12; 34-36 at 4:10:58 and 4:11:30; 49-57 at 4:48:30-4:56:59);
  * three extended similes are complete;
  * line 50 keeps κῆρε … θανάτοιο, and the replacement search is documented (round-1 note on v1 45);
  * each player has each of his three name shapes.
## 7. Per-line table

Queries are written as their concordance.py arguments; "ctx" means the context script (B.2); "v1" means the query is in philology_v1.md and was not rerun unless repeated in Appendix A; "identity" means B.1.

| n | verdict | findings (morphology, dialect, syntax, lexicon, sense, idiom, rulings, facts) | evidence: query → hits | enjambment: composer → reviewer |
|---|---|---|---|---|
| 1 | PASS | Unchanged, v1 PASS (= v1 1). | identity → 1=1 | necessary → necessary |
| 2 | PASS | Unchanged, v1 PASS (= v1 2). The jsonl note "ring with line 54-55" is stale (now 59-60). | identity → 2=2 | unperiodic → unperiodic |
| 3 | PASS | Unchanged, v1 PASS (= v1 3). Its subjects now come in line 4 as τε … καί (see 4). | identity → 3=3 | necessary → necessary |
| 4 | PASS | **v1 FAIL (τε) repaired.** Φεδερεύς τε καὶ … Ζοκοβείδης is the τε … καί pattern of Il. 14.29, with Ὀδυσεύς τε καί at the same 3.5-5; τε καὶ ἀντίθεος + an SSLL name is attested 3x at 5.5-12; διογενὴς + SSL name at 1-5 as διογενὴς Ὀδυσεύς (4 of 6 at 1-5). **Ζοκοβείδης (R3)**: the diphthongal -είδης of -εύς patronymics is Homeric (Ἀμαρυγκείδην Il. 4.517 and Ἀτρείδης Od. 15.52, both with unique scansion; Πηλείδη Il. 1.277, multiple scansion), so SSLL needs no metre-only quantity; its acute accent is correct as in Ἀτρείδης; ζ- makes -ος at 9 long, and 9 is a longum. The dual subject of διαστήτην (3) is A τε καὶ B. Notes: διογενής (Federer) and ἀντίθεος (Djokovic) are both "divine" epithets (plan note); P1 applies. | --ngram "Ὀδυσεύς τε καὶ Ἀτρεΐδης Ἀγαμέμνων" → Il. 14.29, 14.380 [3.5-12]; --ngram "τε καὶ ἀντίθεος" → Il. 20.232, Od. 3.414, 8.119 [5.5-9]; --ngram "διογενὴς Ὀδυσεύς" → 6; --regex "είδη[ςνω]?[,.·;]?( \|$)" → Il. 1.277, 4.517, Od. 15.52 (+2 pluperfects of οἶδα); --regex "Ἀτρείδ" → Od. 15.52, 19.183, 24.35; --loose "αμαρυγκε" → Il. 2.622, 4.517, 23.630; scansion.tsv rows (A.6) | none → none |
| 5 | PASS | **R7 applied.** The order of arming is no longer asserted. δ᾽ ἑτέρωθεν keeps its only slot 3.5-5.5 (22x) after an LSSL name, as Πηλεΐδης δ᾽ ἑτέρωθεν (Il. 20.164). ἑτέρωθεν usually marks the second party; here Djokovic was named last in 4, so "on his side, opposite" reads naturally, and 10 answers with αὖθ᾽ ἑτέρωθεν. The second half is verbatim. | --ngram "δ᾽ ἑτέρωθεν" --count → 22; --ngram "ἐδύσετο τεύχεα καλὰ" → Il. 3.328, Od. 23.366 [6-12]; --loose "πηλειδης" --word → Il. 20.164 [1-3] | none → none |
| 6 | PASS | Unchanged, v1 PASS (= v1 6). | identity → 6=6 | unperiodic → unperiodic |
| 7 | PASS | Unchanged, v1 PASS (= v1 7). | identity → 7=7 | unperiodic → unperiodic |
| 8 | PASS | Unchanged, v1 PASS (= v1 8). | identity → 8=8 | unperiodic → unperiodic |
| 9 | PASS | Unchanged, v1 PASS (= v1 9). | identity → 9=9 | none → none |
| 10 | PASS | Unchanged, v1 PASS (= v1 10). | identity → 10=10 | none → none |
| 11 | PASS | Unchanged, v1 PASS (= v1 11). | identity → 11=11 | none → none |
| 12 | PASS | Unchanged, v1 PASS (= v1 12). The jsonl now cites Il. 16.284. | identity → 12=12 | none → none |
| 13 | PASS | Unchanged, v1 PASS (= v1 13). | identity → 13=13 | none → none |
| 14 | PASS | Unchanged, v1 PASS (= v1 14). Its τρὶς μέν is now answered by a complete ἀλλ᾽ ὅτε δὴ τὸ τέταρτον clause (15). | identity → 14=14 | unperiodic → unperiodic |
| 15 | PASS | **v1 QUERY (verbless ὅτε-clause) resolved.** ἀπήμβροτε is in its attested 6-8. Its absolute use (no genitive) is Homeric: Il. 16.477 ἔνθ᾽ αὖ Σαρπηδὼν μὲν ἀπήμβροτε δουρὶ φαεινῷ. An asyndetic apodosis after ὅτε δή is Homeric (Il. 3.15-16 Τρωσὶν μὲν προμάχιζεν; 5.14-15; 11.232-233 Ἀτρεΐδης μὲν ἅμαρτε). ἐνίκα stands at 10-12 (5 of 8). Every Homeric ἐνίκα has an object or πολλόν, but absolute νικάω "win the fight" is Il. 3.439 Μενέλαος ἐνίκησεν. τρίς … τὸ τέταρτον without τρὶς δέ as Il. 22.165 → 22.208. Facts: points 84-87 of 1.4a, the set to Djokovic ✓. Σέρβος at 9-9.5 is an A1 slot. | --loose "απημβροτε" --word → Il. 16.466, 16.477 [6-8]; --loose "ενικα" --word → 8; --loose "ενικησεν" --word → Il. 3.439; ctx "οἳ δ᾽ ὅτε δὴ σχεδὸν ἦσαν ἐπ᾽ ἀλλήλοισιν ἰόντες" +1 → 10 (A.3) | none → none |
| 16 | PASS | Unchanged, v1 PASS (= v1 16). | identity → 16=16 | necessary → necessary |
| 17 | PASS | Unchanged, v1 PASS (= v1 17). The composer adopted "necessary". | identity → 17=17 | necessary → necessary |
| 18 | PASS | Unchanged, v1 PASS (= v1 18). | identity → 18=18 | necessary → necessary |
| 19 | PASS | Unchanged, v1 PASS (= v1 19). | identity → 19=19 | none → none |
| 20 | PASS | **R5 applied.** ἐδάμασσε for ἐξενάριξε, at 3.5-5.5 as Od. 11.171, 22.246, 22.413. A sentence-opening τρὶς δέ with no τρὶς μέν before it is Homeric (Od. 4.277; Il. 24.16, 24.273), so δέ is the narrative connective. μιν = Djokovic, last named in 15, across the simile (there are only two agents). δαμάζω "subdue, conquer" (LSJ III; non-lethal at Il. 6.159, 14.316). Three breaks = τρίς (MF T18) ✓. | --loose "εδαμασσε" --word → 7 (4 at 3.5-5.5); ctx "τρὶς δέ" → 8, of which Od. 4.277 has no τρὶς μέν; ctx "τρὶς δ᾽" → 9, of which Il. 24.16 and 24.273 have none (A.7); LSJ δαμάζω (A.10) | none → none |
| 21 | PASS | Unchanged, v1 PASS (= v1 21). | identity → 21=21 | none → none |
| 22 | PASS | Unchanged, v1 PASS (= v1 22). The jsonl now cites the right parallels (Il. 5.275, 16.337). πάλιν = "back" (R6). | identity → 22=22 | unperiodic → unperiodic |
| 23 | PASS | **R6 applied** (πάλιν gone). ἄφαρ stands at 5.5-6 as Il. 1.349, a rare slot (2 of 34; 16 at 2-3, 15 at 6-7). ἄφαρ strengthened by a second adverb of speed is Homeric (Il. 23.593 ἄφαρ κέ τοι αὐτίκα; LSJ "strengthd."). δεύτερον αὖ opens without a connective as Il. 6.184. "A second time" counts Djokovic's second set, after 15 ✓. Note: ἄφαρ is colour, not fact (the set took 48 min; the tie-break went 5-1 → 5-4 → 7-4). | --loose "αφαρ" --word --count → 34, positions tabulated (A.2); lines.tsv Il. 23.593 (A.2); --ngram "δεύτερον αὖ" → 5 (A.2); LSJ ἄφαρ (A.10) | none → none |
| 24 | PASS | **R4 and R5 applied.** τὸν δ᾽ αὖθ᾽ before the aspirated Ἑλβέτιος, correctly with θ (as Il. 6.144 τὸν δ᾽ αὖθ᾽ Ἱππολόχοιο; Homer αὖθ᾽ + rough 33x, αὖτ᾽ + rough 0x). δάμασεν is the unaugmented single-σ aorist of Il. 22.446, in the same 5.5-7, with movable ν before καί. "δάμασεν καὶ δεύτερον αὖτις" is elliptical, "subdued him, and a second time again": it counts the two breaks of set 4 (2:36:11, 2:42:40) ✓. Every Homeric δεύτερον αὖτις has its own verb, so the ellipsis is unattested but clear. An adverbial reading of καί ("also a second time") is possible but less natural. | --ngram "τὸν δ᾽ αὖθ᾽" → Il. 6.144; aspiration script (A.5); --loose "δαμασε" --word → Il. 22.446 [5.5-7]; ctx "δεύτερον αὖτις" → 5 (A.2); --regex "καὶ (τρὶς\|δεύτερον\|τὸ τρίτον)[,.·;]?$" → 0 | none → none |
| 25 | PASS | Unchanged, v1 PASS (= v1 25). | identity → 25=25 | none → none |
| 26 | PASS | Unchanged, v1 PASS (= v1 26). | identity → 26=26 | unperiodic → unperiodic |
| 27 | PASS | **R2 applied.** Ῥογῆρος now stands before κέρδεα, so -ρος at 8 is long by position. κέρδεα εἰδώς ("skilled in wiles", LSJ κέρδος II, citing Il. 23.709) is appositive to the named subject, as in its only Homeric use. It gives Federer a craft epithet distinct from Djokovic's (plan note). Facts: 35-shot rally won by Federer ✓. | --ngram "κέρδεα εἰδώς" → Il. 23.709 [9-12]; --ngram "καὶ βάλεν οὐδ᾽ ἀφάμαρτε" → Il. 11.350, 13.160 [1-5.5]; LSJ κέρδος (A.10) | none → none |
| 28 | PASS | **R7 applied** (ὣς "thus" → αὖτ᾽, so no cause is asserted). τέτρατον = "the fourth (prize)", its noun supplied from ἄεθλον, as neuter ordinals stand for prizes in Il. 23.538 (τὰ πρῶτα φερέσθω) and 23.615. ἔλαβεν at 3.5-5 is a single-word mobility (jsonl). Subject: Federer (27). | --ngram "ἀτὰρ τὰ πρῶτα φερέσθω" → Il. 23.538; ctx "πέμπτον δ᾽ ὑπελείπετ᾽ ἄεθλον" → Il. 23.614-615 | none → none |
| 29 | PASS | **R5 applied.** Name + δ᾽ αὖτ᾽ + verb at line start, as Il. 17.304 Ἕκτωρ δ᾽ αὖτ᾽ Αἴαντος ἀκόντισε and 14.469. The accusative βοὴν ἀγαθὸν Φεδερῆρον follows βοὴν ἀγαθὸν Μενέλαον (5x). Sense: Homer's active-aorist δαμάζω with a personal object is a killing in 14 of 18 hits. The non-lethal "subdue, conquer" exists (LSJ III; Il. 6.159, 9.118, 14.316), so "subdued … subdued back" (29-30) is a Homeric use under R5, not the reciprocal slaying R5 removed. Facts: break for 4-2 at 3:25:11 ✓. | --regex "^[Α-ΩἈ-Ὼ][^ ]+ δʼ αὖτʼ " → 6, incl. Il. 14.469, 17.304; --ngram "βοὴν ἀγαθὸν Μενέλαον" --count → 5; δαμάζω forms (A.9) → 18 | unperiodic → unperiodic |
| 30 | PASS | **R5 applied.** αὐτὰρ ὅ γ᾽ ἂψ (Od. 11.599) + verb + name-epithet in apposition at verse end. The pattern "pronoun … name-epithet" is Homeric: Il. 2.402 and 3.81 αὐτὰρ ὃ … ἄναξ ἀνδρῶν Ἀγαμέμνων; Od. 5.354; 23 lines of this shape. With ὅ γε no Homeric line has the same man's name (4 lines, each naming another man), the small extension already accepted for 19 in v1. ἂψ with a non-motion verb, "in return": LSJ ἄψ 2 (Il. 22.277, 16.54). Facts: break back to 4-3 at 3:31:55 ✓. | --ngram "αὐτὰρ ὅ γ᾽ ἂψ" → Od. 11.599; oname.py → 23; og.py → 4 (A.7); LSJ ἄψ (A.10) | none → none |
| 31 | PASS | Unchanged, v1 PASS (= v1 31). The jsonl now labels it Il. 13.85 verbatim. | identity → 31=31 | none → none |
| 32 | PASS | **R6 applied** (πάλιν → ἄφαρ at its attested 5.5-6). Homer never combines ὀψὲ δὲ δή ("late, at last") with ἄφαρ. With LSJ's sense 2 ("suddenly, quickly") the line reads "late, at last, Federer suddenly won boundless glory", which fits the 8-7 break at 4:07:16 ✓. ἄσπετον ἤρατο κῦδος occurs only inside the unreal frame in Homer (v1 note). | --regex "ὀψ.*ἄφαρ\|ἄφαρ.*ὀψ" → 0; --ngram "ὀψὲ δὲ δὴ" --count → 12; LSJ ἄφαρ (A.10) | none → none |
| 33 | QUERY | **The count.** δεύτερον αὖτις = "a second time" (LSJ: δεύτερον αὖ, αὖτε, αὖτις). In all 5 Homeric uses it marks a single action repeated after an earlier one narrated separately (Il. 1.513 Thetis asks again after 1.503-510; Od. 9.354, 19.65, 22.69). So the line narrates one unmissed strike, the second, and repeats line 27's half-line (καὶ βάλεν, οὐδ᾽ ἀφάμαρτε, Ῥογῆρος). The fact is two aces (points 357-358, 4:10:13 and 4:10:35). The jsonl's "the two aces counted by δεύτερον αὖτις" misreads the phrase, and brief §3.1's "twice he cast and twice he did not miss" is not met. Otherwise sound: **R4 applied**; Ῥογῆρος at 6-8 before δ follows Μελανθὼ δεύτερον αὖτις (Od. 19.65); v1's σήματα πάντων and τὸ δ᾽ problems are gone. Possible repair: narrate the first ace, then the second in its own clause with δεύτερον αὖ(τις), as 24 does. | ctx "δεύτερον αὖτις" -3 → 5 (A.2); LSJ δεύτερος (A.10) | none → none |
| 34 | PASS | **R5 applied.** καί νύ κεν ἔνθ᾽ (3x) + aorist indicative (as Il. 3.373) + the name formula; the object (Djokovic) is understood. Facts: CP1 ✓. | --ngram "καί νύ κεν ἔνθ᾽" → Il. 5.311, 5.388, 8.90 | unperiodic → unperiodic |
| 35 | PASS | **v1 FAIL (ἄρ᾽ before ϝοι) repaired** with the verifiers' remedy. οἱ = Federer, the subject of 34. Facts: CP1, Federer's inside-out forehand wide ✓. | --ngram "εἰ μή οἱ" → Il. 17.71, 22.203; check_line --file → OK | none → none |
| 36 | PASS | **v1 QUERY (thrower not named) resolved.** στῆ δὲ μάλ᾽ ἐγγὺς ἰών takes Federer (34) as its subject. The second clause names its own subject. βάλε δέ + subject, with the object left to the context, is exactly Il. 4.518-519 (κνήμην δεξιτερήν· βάλε δὲ Θρῃκῶν ἀγὸς ἀνδρῶν); βάλε δέ also stands at 5.5-7 in Od. 22.82. In Homer the man who comes close is the one who acts next (5 of 5). Here the other man acts, and the name makes that clear. Facts: CP2 approach and pass ✓. | --ngram "βάλε δὲ" → Il. 4.519, 5.533, 14.450, Od. 22.82; ctx Il. 4.518-519 (A.8); --ngram "στῆ δὲ μάλ᾽ ἐγγὺς ἰών" → 5 | none → none |
| 37 | QUERY | The text is v1 37 (a v1 PASS), but 36 now ends with Djokovic as named subject. The unexpressed subject of ἐπέσσυτο is therefore first read as Djokovic; only 38 (Σέρβος δ᾽ … ἑτέρωθεν ἐναντίον) shows that it is Federer. Homer returns unmarked to an earlier subject in this very verse (Il. 5.437 Apollo → 5.438 Diomedes; 16.703 Apollo → 16.705 Patroclus), but in all four uses the τρὶς μέν (… τρὶς δ᾽) lines before it fix who the attacker is. Here no count precedes, and of points 359-362 only two (34-35, 36) are narrated, so "the fourth" has no third. The number itself matches 1.7 (362 is the fourth point). Decide whether the Homeric precedent is enough, or make Federer the last subject of 36. | ctx "ἀλλ᾽ ὅτε δὴ τὸ τέταρτον" -2/+1 → 5 (A.3) | necessary → necessary |
| 38 | PASS | The stop of v1 is removed so that λέων ὣς takes a relative clause, the frame of Il. 20.164-165 (λέων ὣς / σίντης, ὅν τε …, a relative with the lion as object). Apodotic δ᾽ after the ὅτε-clause of 37, as Il. 5.439. Aristeia marker ✓. | ctx "Πηλεΐδης δ᾽ ἑτέρωθεν ἐναντίον ὦρτο λέων ὣς" +1 → Il. 20.164-165 (A.8) | unperiodic → unperiodic |
| 39 | PASS | **v1 FAIL (the Serb with a tail) repaired.** Il. 5.137 verbatim. The relative ὅν (object of χραύσῃ) takes λέων of 38 as antecedent, and the lion is subject again in 42 (αὐτὰρ ὃ). The generic subjunctives are the model's. | verbatim.py → Il. 5.137; ctx Il. 5.136-143 (A.8) | necessary → necessary |
| 40 | PASS | Il. 5.138 verbatim. | verbatim.py → Il. 5.138 | none → none |
| 41 | PASS | Il. 5.139 verbatim; the subject is the shepherd. | verbatim.py → Il. 5.139 | unperiodic → unperiodic |
| 42 | PASS | Il. 5.142 verbatim. Dropping 5.140-141 keeps the syntax continuous. αὐτὰρ ὃ now sets the lion against the shepherd, not against the sheep (αἳ μέν, 5.141). The leap out of the fold reads as an escape rather than an exit after slaughter, which suits the two saved championship points. Gloss: "leaps out through the deep fold" should be "out of" (LSJ ἐξάλλομαι: "leap out of", citing this line). | verbatim.py → Il. 5.142; LSJ ἐξάλλομαι (A.10) | none → none |
| 43 | PASS | The simile's apodosis: ὣς τότε (13x line-initial) on Il. 20.174 (μένος καὶ θυμὸς ἀγήνωρ with a singular verb). ἀνῆκε + accusative of person without an infinitive, "set on, roused", is Homeric: Il. 7.25 and 21.395 (μέγας δέ σε θυμὸς ἀνῆκεν;), 10.389, and in a statement 17.705 (Θρασυμήδεα δῖον ἀνῆκεν); LSJ ἀνίημι II.2 "freq. c. acc. pers. only, let loose, excite". The closest model is the apodosis of the lion simile Il. 12.299-307 (ὥς τε λέων … ὅς τ᾽ …, closed by ὥς ῥα τότ᾽ ἀντίθεον Σαρπηδόνα θυμὸς ἀνῆκε), but there an infinitive follows in 12.308, and in 6.256, 7.152 and 22.252 as well. Σέρβον at 3-3.5 is an A1 slot. The simile is complete: vehicle 38-42, apodosis 43. | ctx "θυμὸς ἀνῆκεν" ±1 → Il. 6.256 (+inf.), 7.25, 21.395; ctx "θυμὸς ἀνῆκε" +1 → Il. 7.152, 12.307, 22.252 (+inf.), 10.389 (A.7); ctx "Θρασυμήδεα δῖον ἀνῆκεν" → Il. 17.705; ctx Il. 12.299-308 (A.7); --ngram "μένος καὶ θυμὸς ἀγήνωρ" → Il. 20.174; --ngram "ὣς τότε" → 13; LSJ ἀνίημι (A.10) | none → none |
| 44 | FAIL | **The change of subject is unmarked and carried by a participle.** The gloss ("he who knows cunning ways rose after him") makes Federer the subject of ὄρνυτο; the Greek supplies no new subject. κέρδεα εἰδώς is a participial phrase, and every verse-final … εἰδώς phrase in Homer (30 lines) is appositive to a subject that is named or already in place (Ὀδυσεύς, Μέδων, κῆρυξ, Ζεύς, ἀνήρ, τίς, ὅ γε …). None introduces a new one. Both Homeric uses of ἐπὶ δ᾽ ὄρνυτο name the follower (δῖος Ἐπειός, Il. 23.689; δῖος Ὀδυσσεύς, 23.759). The cited parallel ὃ δ᾽ ἅμ᾽ ἕσπετο ἰσόθεος φώς (Il. 11.472) has both the pronoun ὃ δ᾽ and the noun φώς. Read as Homeric Greek, the line says "Djokovic drew ahead again and rushed on, knowing cunning ways": the gloss is wrong, and Federer's craft epithet goes to Djokovic (economy). Tested remedy: `ἔκφερε δ᾽ αὖ Ζοκοβεύς· ὃ δ᾽ ἐπέσσυτο κέρδεα εἰδώς.` (DDDDDS, no flags). ὃ δ᾽ ἐπέσσυτο stands at 5.5-8 in Il. 21.234 and 21.601 (… ὃ δ᾽ ἐπέσσυτο ποσσὶ διώκειν, of the pursuer). The unelided ἔκφερε is regular and the jsonl marks it. Facts: 9-8 at 4:17:15 ✓. | ctx "ἐπὶ δ᾽ ὄρνυτο" → Il. 23.689, 23.759; --ngram "κέρδεα εἰδώς" → Il. 23.709; ctx "ὃ δ᾽ ἅμ᾽ ἕσπετο ἰσόθεος φώς" → 3; --regex "εἰδώς[.,·;]?$" → 30; --ngram "ὃ δ᾽ ἐπέσσυτο" → Il. 21.234, 21.601; check_line on the remedy (all in A.1) | none → none |
| 45 | PASS | The text is v1 42 (a v1 FAIL for lacking an apodosis). The simile now closes at 48, with vehicle 45-47 as in Il. 22.162-164. | identity → 45=42; verbatim.py → Il. 22.162; simile.py (A.8) | necessary → necessary |
| 46 | PASS | Il. 22.163 verbatim; v1's added stop is removed, matching the edition. | verbatim.py → Il. 22.163 | necessary → necessary |
| 47 | PASS | Il. 22.164 verbatim. The dead man belongs to the vehicle's funeral games and is not said of the loser (§2.6.2). The raised stop is the edition's; the ὡς δ᾽ ὅτε period is still open. | verbatim.py → Il. 22.164 | necessary → necessary |
| 48 | PASS | The apodosis, on Il. 22.165: ὣς τώ (9x line-initial) with the dual δινηθήτην kept at 9-12. πολλάκι stands at 3-4, a mobility (Homer 1-2 ×9, 7-8 ×2), with δή as in Il. 19.85. περὶ τέρματα is at its attested 5.5-8 (Il. 22.162). The model's τρίς is rightly dropped (eight games, 9-8 to 12-12). The apodosis reuses the vehicle's τέρματα instead of naming the tenor's ground; with τέρματα = the court's lines (brief §5.2) this is acceptable. | --ngram "ὣς τὼ" → 9; --loose "πολλακι" --word → 11; --ngram "περὶ τέρματα" → Il. 22.162 [5.5-8]; --loose "δινηθητην" --word → Il. 22.165 [9-12] | unperiodic → unperiodic |
| 49 | PASS | Unchanged, v1 PASS (= v1 44). It now follows a ὣς-apodosis instead of an open simile; καὶ τότε δή reads as "and then". | identity → 49=44 | unperiodic → unperiodic |
| 50 | PASS | Unchanged, v1 PASS (= v1 45). The round-1 plan note is answered in the jsonl (no metrical equivalent found). | identity → 50=45 | unperiodic → unperiodic |
| 51 | PASS | Unchanged, v1 PASS (= v1 46). P1 applies to Ζοκοβῆος. | identity → 51=46 | unperiodic → unperiodic |
| 52 | PASS | Unchanged, v1 PASS (= v1 47). | identity → 52=47 | none → none |
| 53 | PASS | **R3 applied** (Ζοκοβίδης → Ζοκοβείδης in the same slot; see 4). The count 1-1 → 4-1 (points 415-417) = τρὶς μέν ✓, answered by αὐτάρ in 54. | --ngram "τρὶς μὲν ἔπειτ᾽ ἐπόρουσε" → Il. 5.436, 16.784, 20.445 [1-5.5] | unperiodic → unperiodic |
| 54 | PASS | **R2 and R4 applied.** ἀμύνετο νηλεὲς ἦμαρ is now at its attested 6-12 (Il. 11.484, 13.514): "warded off the pitiless day" = points 418-419 (4-3) ✓. ὅ γ᾽ Ἑλβέτιος as in 19. | --ngram "ἀμύνετο νηλεὲς ἦμαρ" → Il. 11.484, 13.514 [6-12] | none → none |
| 55 | FAIL | **Accent: Νοβήκος must be Νοβῆκος.** A long accented penult before a short final syllable takes the circumflex. In Homer no word in η/ω + one consonant + -ος has the acute (0 types), against 51 types and 269 tokens with the circumflex (πρῶτος, δῆμος, κλῆρος, κρητῆρος …). The poem itself writes Ῥογῆρος and Φεδερῆρος. The form comes from R3 and A1, which need the same correction. `καὶ βάλεν, οὐδ᾽ ἀφάμαρτε Νοβῆκος δεύτερον αὖτις·` passes check_line with no flags. The Ionic η is the R3 decision (Ionic η for ᾱ: [unverified] here). The line also has 33's problem: δεύτερον αὖτις narrates one winner, the second after Djokovic's βάλε of 36, whereas the fact is two winners (points 420-421). Otherwise: **R4 applied**; Νοβῆκος at 6-8 on Μελανθὼ δεύτερον αὖτις (Od. 19.65) is an A1 slot. | accent.py → acute 0 / circumflex 51 types, 269 tokens; check_line on the corrected line (A.4); ctx "δεύτερον αὖτις" → 5 (A.2) | none → none |
| 56 | FAIL | **Aspiration: αὖτ᾽ before the rough breathing of Ἑλβέτιος must be αὖθ᾽.** Homer writes elided αὖτε as αὖθ᾽ before a rough breathing 33x and as αὖτ᾽ 0x. No elided τ, π or κ stands before a rough breathing anywhere in the text. The poem itself writes τὸν δ᾽ αὖθ᾽ Ἑλβέτιος (24) and αὖθ᾽ ἑτέρωθεν (10, 38). The corrected `ἔνθ᾽ αὖθ᾽ Ἑλβέτιος προΐει, βάλε δ᾽ ἂψ Ζοκοβείδης,` passes check_line with no flags. The sequence ἔνθ᾽ αὖθ᾽ is unattested only because ἔνθ᾽ αὖτ᾽ (12x) never stands before an aspirated word. Otherwise sound: **v1 QUERY (subject of προΐει) resolved** by naming both men. προΐει without an object as Il. 1.326; βάλε δ᾽ at 7.5-9 as Il. 15.541; ἂψ "back, in return" (LSJ ἄψ 2); **R3 applied**. Facts: point 422, Federer's serve and Djokovic's return ✓. | aspir.py → αὖθ᾽ + rough 33, αὖτ᾽ + rough 0; draft: only 56 (A.5); --ngram "ἔνθ᾽ αὖθ᾽" → 0; --ngram "ἔνθ᾽ αὖτ᾽" → 12; check_line (A.5) | unperiodic → unperiodic |
| 57 | PASS | **v1 QUERY (asyndeton) resolved** with δ᾽ ἄρα (δ᾽ ἄρα τοῦ 13x at 3.5-5). τοῦ μὲν ἀπήμβροτε, "missed him", takes the genitive of the target (Il. 16.466). μέν is answered by δέ in 58, as in τοῦ μὲν ἅμαρθ᾽, ὃ δὲ … (Il. 4.491, 15.430). Facts: Federer's forehand error at 4:56:59 ✓. | ctx "αὐτοῦ μὲν ἀπήμβροτε" → Il. 16.466-467; ctx "τοῦ μὲν ἅμαρθ᾽" → Il. 4.491, 15.430; --ngram "δ᾽ ἄρα τοῦ" → 13 | none → none |
| 58 | PASS | **R5 applied.** Σέρβος δ᾽ αὖτ᾽ + verb as in 29; the object (Federer, the subject of 57) is understood. Διὸς δ᾽ ἐτελείετο βουλή (Il. 1.5) closes the narrative. Nothing after the last point is narrated (1.11) ✓. | --ngram "Διὸς δ᾽ ἐτελείετο βουλή" → Il. 1.5, Od. 11.297 [6-12] | none → none |
| 59 | PASS | Unchanged, v1 PASS (= v1 54). The composer adopted "unperiodic". | identity → 59=54 | unperiodic → unperiodic |
| 60 | PASS | Unchanged, v1 PASS (= v1 55). | identity → 60=55 | none → none |

## Appendix A. Verbatim evidence

Outputs of `python homer/concordance.py` (lines beginning `# [tag]` give the command), of `check_line.py`, and of the scripts in Appendix B, all run on 2026-10-07 from the repository root with `.venv`.

### A.1 Line 44 (subject of ὄρνυτο; κέρδεα εἰδώς; remedy)

```
# context for ngram "ἐπὶ δ᾽ ὄρνυτο" (-1/+0 lines): 2 hit(s)
  Il. 23.688   δεινὸς δὲ χρόμαδος γενύων γένετʼ, ἔρρεε δʼ ἱδρὼς
> Il. 23.689   πάντοθεν ἐκ μελέων· ἐπὶ δʼ ὄρνυτο δῖος Ἐπειός,

  Il. 23.758   τοῖσι δʼ ἀπὸ νύσσης τέτατο δρόμος· ὦκα δʼ ἔπειτα
> Il. 23.759   ἔκφερʼ Ὀϊλιάδης· ἐπὶ δʼ ὄρνυτο δῖος Ὀδυσσεὺς

# [K1] python homer/concordance.py --ngram "κέρδεα εἰδώς"
Il. 23.709   [9-12]  ἂν δʼ Ὀδυσεὺς πολύμητις ἀνίστατο κέρδεα εἰδώς.    <κέρδεα εἰδώς>
-- 1 hit(s)

# context for ngram "ὃ δ᾽ ἅμ᾽ ἕσπετο ἰσόθεος φώς" (-1/+0 lines): 3 hit(s)
  Il. 11.471   ἐσθλὸς ἐών, μεγάλη δὲ ποθὴ Δαναοῖσι γένηται.
> Il. 11.472   ὣς εἰπὼν ὃ μὲν ἦρχʼ, ὃ δʼ ἅμʼ ἕσπετο ἰσόθεος φώς.

  Il. 15.558   Ἴλιον αἰπεινὴν ἑλέειν κτάσθαι τε πολίτας.
> Il. 15.559   ὣς εἰπὼν ὃ μὲν ἦρχʼ, ὃ δʼ ἅμʼ ἕσπετο ἰσόθεος φώς·

  Il. 16.631   τὼ οὔ τι χρὴ μῦθον ὀφέλλειν, ἀλλὰ μάχεσθαι.
> Il. 16.632   ὣς εἰπὼν ὃ μὲν ἦρχʼ, ὃ δʼ ἅμʼ ἕσπετο ἰσόθεος φώς.

# [K2] python homer/concordance.py --regex "εἰδώς[.,·;]?$" --limit "100"
Il. 4.310    [11-12]  ὣς ὃ γέρων ὄτρυνε πάλαι πολέμων ἐῢ εἰδώς·    <εἰδώς·>
Il. 6.438    [11-12]  ἤ πού τίς σφιν ἔνισπε θεοπροπίων ἐῢ εἰδώς,    <εἰδώς,>
Il. 7.278    [11-12]  κῆρυξ Ἰδαῖος πεπνυμένα μήδεα εἰδώς·    <εἰδώς·>
Il. 12.350   [11-12]  καί οἱ Τεῦκρος ἅμα σπέσθω τόξων ἐῢ εἰδώς.    <εἰδώς.>
Il. 12.363   [11-12]  καί οἱ Τεῦκρος ἅμα σπέσθω τόξων ἐῢ εἰδώς.    <εἰδώς.>
Il. 15.679   [11-12]  ὡς δʼ ὅτʼ ἀνὴρ ἵπποισι κελητίζειν ἐῢ εἰδώς,    <εἰδώς,>
Il. 17.325   [11-12]  κηρύσσων γήρασκε φίλα φρεσὶ μήδεα εἰδώς·    <εἰδώς·>
Il. 23.709   [11-12]  ἂν δʼ Ὀδυσεὺς πολύμητις ἀνίστατο κέρδεα εἰδώς.    <εἰδώς.>
Il. 24.88    [11-12]  ὄρσο Θέτι· καλέει Ζεὺς ἄφθιτα μήδεα εἰδώς.    <εἰδώς.>
Od. 1.202    [11-12]  οὔτε τι μάντις ἐὼν οὔτʼ οἰωνῶν σάφα εἰδώς.    <εἰδώς.>
Od. 2.38     [11-12]  κῆρυξ Πεισήνωρ πεπνυμένα μήδεα εἰδώς.    <εἰδώς.>
Od. 2.170    [11-12]  οὐ γὰρ ἀπείρητος μαντεύομαι, ἀλλʼ ἐὺ εἰδώς·    <εἰδώς·>
Od. 2.231    [11-12]  σκηπτοῦχος βασιλεύς, μηδὲ φρεσὶν αἴσιμα εἰδώς,    <εἰδώς,>
Od. 4.460    [11-12]  ἀλλʼ ὅτε δή ῥʼ ἀνίαζʼ ὁ γέρων ὀλοφώια εἰδώς,    <εἰδώς,>
Od. 4.696    [11-12]  τὴν δʼ αὖτε προσέειπε Μέδων πεπνυμένα εἰδώς·    <εἰδώς·>
Od. 4.711    [11-12]  τὴν δʼ ἠμείβετʼ ἔπειτα Μέδων πεπνυμένα εἰδώς·    <εἰδώς·>
Od. 5.9      [11-12]  σκηπτοῦχος βασιλεύς, μηδὲ φρεσὶν αἴσιμα εἰδώς,    <εἰδώς,>
Od. 5.182    [11-12]  ἦ δὴ ἀλιτρός γʼ ἐσσὶ καὶ οὐκ ἀποφώλια εἰδώς,    <εἰδώς,>
Od. 6.12     [11-12]  Ἀλκίνοος δὲ τότʼ ἦρχε, θεῶν ἄπο μήδεα εἰδώς.    <εἰδώς.>
Od. 7.157    [11-12]  καὶ μύθοισι κέκαστο, παλαιά τε πολλά τε εἰδώς·    <εἰδώς·>
Od. 8.584    [11-12]  ἦ τίς που καὶ ἑταῖρος ἀνὴρ κεχαρισμένα εἰδώς,    <εἰδώς,>
Od. 9.428    [11-12]  τῇς ἔπι Κύκλωψ εὗδε πέλωρ, ἀθεμίστια εἰδώς,    <εἰδώς,>
Od. 12.188   [11-12]  ἀλλʼ ὅ γε τερψάμενος νεῖται καὶ πλείονα εἰδώς.    <εἰδώς.>
Od. 14.288   [11-12]  δὴ τότε Φοῖνιξ ἦλθεν ἀνὴρ ἀπατήλια εἰδώς,    <εἰδώς,>
Od. 15.557   [11-12]  ἐσθλὸς ἐὼν ἐνίαυεν, ἀνάκτεσιν ἤπια εἰδώς.    <εἰδώς.>
Od. 17.248   [11-12]  ὢ πόποι, οἷον ἔειπε κύων ὀλοφώϊα εἰδώς,    <εἰδώς,>
Od. 20.287   [11-12]  ἦν δέ τις ἐν μνηστῆρσιν ἀνὴρ ἀθεμίστια εἰδώς,    <εἰδώς,>
Od. 22.361   [11-12]  ὣς φάτο, τοῦ δʼ ἤκουσε Μέδων πεπνυμένα εἰδώς·    <εἰδώς·>
Od. 24.51    [11-12]  εἰ μὴ ἀνὴρ κατέρυκε παλαιά τε πολλά τε εἰδώς,    <εἰδώς,>
Od. 24.442   [11-12]  τοῖσι δὲ καὶ μετέειπε Μέδων πεπνυμένα εἰδώς·    <εἰδώς·>
-- 30 hit(s)

# [K3] python homer/concordance.py --ngram "ὃ δ᾽ ἐπέσσυτο"
Il. 21.234   [5.5-8]  κρημνοῦ ἀπαΐξας· ὃ δʼ ἐπέσσυτο οἴδματι θύων,    <ὃ δʼ ἐπέσσυτο>
Il. 21.601   [5.5-8]  ἔστη πρόσθε ποδῶν, ὃ δʼ ἐπέσσυτο ποσσὶ διώκειν·    <ὃ δʼ ἐπέσσυτο>
-- 2 hit(s)

$ python homer/check_line.py "ἔκφερε δ᾽ αὖ Ζοκοβεύς· ὃ δ᾽ ἐπέσσυτο κέρδεα εἰδώς."
[1] ἔκφερε δ᾽ αὖ Ζοκοβεύς· ὃ δ᾽ ἐπέσσυτο κέρδεα εἰδώς.
  DDDDDS  (unique, tier 0, 1 scansion(s))
  syllables: ἔκ.φε.ρε δʼ αὖ Ζο.κο.βεύς ὃ δʼ ἐ.πέσ.συ.το κέρ.δε.α εἰ.δώς
  positions: 1 1.5 2 3 3.5 4 5 5.5 6 7 7.5 8 9 9.5 10 11 12
  quantities by word: LSS 0 L SSL S 0 SLSS LSS LL
  caesurae: trithemimeral, penthemimeral, trochaic; bucolic diaeresis: D
  licences: digamma@10(εἰδώς)
    digamma 'εἰδώς': 42x in Homer, e.g. Il. 1.385@1, Il. 2.718@10, Il. 4.196@10
  warn quantity_unattested: α in 'κέρδεα' taken as S (accent); no unambiguous Homeric attestation of this form
  OK (no flags)
```

### A.2 Lines 33, 55, 24 (δεύτερον αὖτις, δεύτερον αὖ)

ev_A also holds the ἄφαρ queries for 23 and 32; ev_misc holds the line-28 and P1 queries.

```
# [A1] python homer/concordance.py --loose "αφαρ" --word --count
34

# positions of ἄφαρ (metrical_start-metrical_end: count), from --format tsv
     16 2-3
     15 6-7
      2 5.5-6
      1 1.5-2
Il. 1.349	5.5	6	ἄφαρ	δακρύσας ἑτάρων ἄφαρ ἕζετο νόσφι λιασθείς,
# [A2] python homer/concordance.py --regex "ὀψ.*ἄφαρ|ἄφαρ.*ὀψ"
-- 0 hit(s)

# lines.tsv Il. 23.593
Il	23	593	μεῖζον ἐπαιτήσειας, ἄφαρ κέ τοι αὐτίκα δοῦναι	0
# context for ngram "δεύτερον αὖτις" (-3/+0 lines): 5 hit(s)
  Il. 1.510   υἱὸν ἐμὸν τίσωσιν ὀφέλλωσίν τέ ἑ τιμῇ.
  Il. 1.511   ὣς φάτο· τὴν δʼ οὔ τι προσέφη νεφεληγερέτα Ζεύς,
  Il. 1.512   ἀλλʼ ἀκέων δὴν ἧστο· Θέτις δʼ ὡς ἥψατο γούνων
> Il. 1.513   ὣς ἔχετʼ ἐμπεφυυῖα, καὶ εἴρετο δεύτερον αὖτις·

  Od. 3.158   ἔπλεον, ἐστόρεσεν δὲ θεὸς μεγακήτεα πόντον.
  Od. 3.159   ἐς Τένεδον δʼ ἐλθόντες ἐρέξαμεν ἱρὰ θεοῖσιν,
  Od. 3.160   οἴκαδε ἱέμενοι· Ζεὺς δʼ οὔ πω μήδετο νόστον,
> Od. 3.161   σχέτλιος, ὅς ῥʼ ἔριν ὦρσε κακὴν ἔπι δεύτερον αὖτις.

  Od. 9.351   σχέτλιε, πῶς κέν τίς σε καὶ ὕστερον ἄλλος ἵκοιτο
  Od. 9.352   ἀνθρώπων πολέων, ἐπεὶ οὐ κατὰ μοῖραν ἔρεξας;
  Od. 9.353   ὣς ἐφάμην, ὁ δʼ ἔδεκτο καὶ ἔκπιεν· ἥσατο δʼ αἰνῶς
> Od. 9.354   ἡδὺ ποτὸν πίνων καὶ μʼ ᾔτεε δεύτερον αὖτις·

  Od. 19.62    καὶ δέπα, ἔνθεν ἄρʼ ἄνδρες ὑπερμενέοντες ἔπινον·
  Od. 19.63    πῦρ δʼ ἀπὸ λαμπτήρων χαμάδις βάλον, ἄλλα δʼ ἐπʼ αὐτῶν
  Od. 19.64    νήησαν ξύλα πολλά, φόως ἔμεν ἠδὲ θέρεσθαι.
> Od. 19.65    ἡ δʼ Ὀδυσῆʼ ἐνένιπε Μελανθὼ δεύτερον αὖτις·

  Od. 22.66    ἢ φεύγειν, ὅς κεν θάνατον καὶ κῆρας ἀλύξῃ·
  Od. 22.67    ἀλλά τινʼ οὐ φεύξεσθαι ὀΐομαι αἰπὺν ὄλεθρον.
  Od. 22.68    ὣς φάτο, τῶν δʼ αὐτοῦ λύτο γούνατα καὶ φίλον ἦτορ.
> Od. 22.69    τοῖσιν δʼ Εὐρύμαχος προσεφώνεε δεύτερον αὖτις·

# [T1] python homer/concordance.py --ngram "ἀτὰρ τὰ πρῶτα φερέσθω"
Il. 23.538   [2-8]  δεύτερʼ· ἀτὰρ τὰ πρῶτα φερέσθω Τυδέος υἱός.    <ἀτὰρ τὰ πρῶτα φερέσθω>
-- 1 hit(s)

# context for ngram "πέμπτον δ᾽ ὑπελείπετ᾽ ἄεθλον" (-1/+0 lines): 1 hit(s)
  Il. 23.614   Μηριόνης δʼ ἀνάειρε δύω χρυσοῖο τάλαντα
> Il. 23.615   τέτρατος, ὡς ἔλασεν. πέμπτον δʼ ὑπελείπετʼ ἄεθλον,

# [T2] python homer/concordance.py --ngram "δεύτερον αὖ"
Il. 3.332    [1-3]  δεύτερον αὖ θώρηκα περὶ στήθεσσιν ἔδυνεν    <δεύτερον αὖ>
Il. 6.184    [1-3]  δεύτερον αὖ Σολύμοισι μαχέσσατο κυδαλίμοισι·    <δεύτερον αὖ>
Il. 11.19    [1-3]  δεύτερον αὖ θώρηκα περὶ στήθεσσιν ἔδυνε,    <δεύτερον αὖ>
Il. 16.133   [1-3]  δεύτερον αὖ θώρηκα περὶ στήθεσσιν ἔδυνε    <δεύτερον αὖ>
Il. 19.371   [1-3]  δεύτερον αὖ θώρηκα περὶ στήθεσσιν ἔδυνεν.    <δεύτερον αὖ>
-- 5 hit(s)

# context for ngram "τῶν δ᾽ Ἀμαρυγκεΐδης" (-0/+0 lines): 1 hit(s)
> Il. 2.622   τῶν δʼ Ἀμαρυγκεΐδης ἦρχε κρατερὸς Διώρης·

# context for ngram "Ἀμαρυγκέα θάπτον" (-0/+1 lines): 1 hit(s)
> Il. 23.630   ὡς ὁπότε κρείοντʼ Ἀμαρυγκέα θάπτον Ἐπειοὶ
  Il. 23.631   Βουπρασίῳ, παῖδες δʼ ἔθεσαν βασιλῆος ἄεθλα·

# [G1] python homer/concordance.py --regex "καὶ (αὖτις|ἐξαῦτις|αὖθις)[,.·;]?$"
Il. 1.140    [10-12]  ἀλλʼ ἤτοι μὲν ταῦτα μεταφρασόμεσθα καὶ αὖτις,    <καὶ αὖτις,>
Il. 10.463   [10-12]  πάντων ἀθανάτων ἐπιδωσόμεθʼ· ἀλλὰ καὶ αὖτις    <καὶ αὖτις>
Il. 24.150   [10-12]  ἡμιόνους καὶ ἄμαξαν ἐΰτροχον, ἠδὲ καὶ αὖτις    <καὶ αὖτις>
Il. 24.179   [10-12]  ἡμιόνους καὶ ἄμαξαν ἐΰτροχον, ἠδὲ καὶ αὖτις    <καὶ αὖτις>
-- 4 hit(s)

# [G2] python homer/concordance.py --regex "καὶ (τρὶς|δεύτερον|τὸ τρίτον)[,.·;]?$"
-- 0 hit(s)
```

### A.3 Line 37 and line 15 (ἀλλ᾽ ὅτε δὴ τὸ τέταρτον; asyndetic apodosis; ἀπήμβροτε, ἐνίκα)

```
# [L15a] python homer/concordance.py --loose "απημβροτε" --word
Il. 16.466   [6-8]  Σαρπηδὼν δʼ αὐτοῦ μὲν ἀπήμβροτε δουρὶ φαεινῷ    <ἀπήμβροτε>
Il. 16.477   [6-8]  ἔνθʼ αὖ Σαρπηδὼν μὲν ἀπήμβροτε δουρὶ φαεινῷ,    <ἀπήμβροτε>
-- 2 hit(s)

# [L15b] python homer/concordance.py --loose "ενικα" --word
Il. 4.389    [10-12]  ἀλλʼ ὅ γʼ ἀεθλεύειν προκαλίζετο, πάντα δʼ ἐνίκα    <ἐνίκα>
Il. 5.807    [10-12]  κούρους Καδμείων προκαλίζετο, πάντα δʼ ἐνίκα    <ἐνίκα>
Il. 18.252   [10-12]  ἀλλʼ ὃ μὲν ἂρ μύθοισιν, ὃ δʼ ἔγχεϊ πολλὸν ἐνίκα·    <ἐνίκα>
Il. 20.410   [10-12]  καί οἱ φίλτατος ἔσκε, πόδεσσι δὲ πάντας ἐνίκα    <ἐνίκα>
Il. 23.680   [6-8]  ἐς τάφον· ἔνθα δὲ πάντας ἐνίκα Καδμείωνας.    <ἐνίκα>
Il. 23.742   [6-8]  χάνδανεν, αὐτὰρ κάλλει ἐνίκα πᾶσαν ἐπʼ αἶαν    <ἐνίκα>
Il. 23.756   [10-12]  Ἀντίλοχος· ὃ γὰρ αὖτε νέους ποσὶ πάντας ἐνίκα.    <ἐνίκα>
Od. 3.121    [6-8]  ἤθελʼ, ἐπεὶ μάλα πολλὸν ἐνίκα δῖος Ὀδυσσεὺς    <ἐνίκα>
-- 8 hit(s)

# context for ngram "οἳ δ᾽ ὅτε δὴ σχεδὸν ἦσαν ἐπ᾽ ἀλλήλοισιν ἰόντες" (-0/+1 lines): 10 hit(s)
> Il. 3.15    οἳ δʼ ὅτε δὴ σχεδὸν ἦσαν ἐπʼ ἀλλήλοισιν ἰόντες,
  Il. 3.16    Τρωσὶν μὲν προμάχιζεν Ἀλέξανδρος θεοειδὴς

> Il. 5.14    οἳ δʼ ὅτε δὴ σχεδὸν ἦσαν ἐπʼ ἀλλήλοισιν ἰόντες
  Il. 5.15    Φηγεύς ῥα πρότερος προΐει δολιχόσκιον ἔγχος·

> Il. 5.630   οἳ δʼ ὅτε δὴ σχεδὸν ἦσαν ἐπʼ ἀλλήλοισιν ἰόντες
  Il. 5.631   υἱός θʼ υἱωνός τε Διὸς νεφεληγερέταο,

> Il. 5.850   οἳ δʼ ὅτε δὴ σχεδὸν ἦσαν ἐπʼ ἀλλήλοισιν ἰόντες,
  Il. 5.851   πρόσθεν Ἄρης ὠρέξαθʼ ὑπὲρ ζυγὸν ἡνία θʼ ἵππων

> Il. 11.232   οἳ δʼ ὅτε δὴ σχεδὸν ἦσαν ἐπʼ ἀλλήλοισιν ἰόντες,
  Il. 11.233   Ἀτρεΐδης μὲν ἅμαρτε, παραὶ δέ οἱ ἐτράπετʼ ἔγχος,

> Il. 13.604   οἳ δʼ ὅτε δὴ σχεδὸν ἦσαν ἐπʼ ἀλλήλοισιν ἰόντες
  Il. 13.605   Ἀτρεΐδης μὲν ἅμαρτε, παραὶ δέ οἱ ἐτράπετʼ ἔγχος,

> Il. 16.462   οἳ δʼ ὅτε δὴ σχεδὸν ἦσαν ἐπʼ ἀλλήλοισιν ἰόντες,
  Il. 16.463   ἔνθʼ ἤτοι Πάτροκλος ἀγακλειτὸν Θρασύμηλον,

> Il. 20.176   οἳ δʼ ὅτε δὴ σχεδὸν ἦσαν ἐπʼ ἀλλήλοισιν ἰόντες,
  Il. 20.177   τὸν πρότερος προσέειπε ποδάρκης δῖος Ἀχιλλεύς·

> Il. 21.148   οἳ δʼ ὅτε δὴ σχεδὸν ἦσαν ἐπʼ ἀλλήλοισιν ἰόντες,
  Il. 21.149   τὸν πρότερος προσέειπε ποδάρκης δῖος Ἀχιλλεύς·

> Il. 22.248   οἳ δʼ ὅτε δὴ σχεδὸν ἦσαν ἐπʼ ἀλλήλοισιν ἰόντες,
  Il. 22.249   τὸν πρότερος προσέειπε μέγας κορυθαίολος Ἕκτωρ·

# context for ngram "ἀλλ᾽ ὅτε δὴ τὸ τέταρτον" (-2/+1 lines): 5 hit(s)
  Il. 5.436   τρὶς μὲν ἔπειτʼ ἐπόρουσε κατακτάμεναι μενεαίνων,
  Il. 5.437   τρὶς δέ οἱ ἐστυφέλιξε φαεινὴν ἀσπίδʼ Ἀπόλλων·
> Il. 5.438   ἀλλʼ ὅτε δὴ τὸ τέταρτον ἐπέσσυτο δαίμονι ἶσος,
  Il. 5.439   δεινὰ δʼ ὁμοκλήσας προσέφη ἑκάεργος Ἀπόλλων·

  Il. 16.703   Πάτροκλος, τρὶς δʼ αὐτὸν ἀπεστυφέλιξεν Ἀπόλλων
  Il. 16.704   χείρεσσʼ ἀθανάτῃσι φαεινὴν ἀσπίδα νύσσων.
> Il. 16.705   ἀλλʼ ὅτε δὴ τὸ τέταρτον ἐπέσσυτο δαίμονι ἶσος,
  Il. 16.706   δεινὰ δʼ ὁμοκλήσας ἔπεα πτερόεντα προσηύδα·

  Il. 16.784   τρὶς μὲν ἔπειτʼ ἐπόρουσε θοῷ ἀτάλαντος Ἄρηϊ
  Il. 16.785   σμερδαλέα ἰάχων, τρὶς δʼ ἐννέα φῶτας ἔπεφνεν.
> Il. 16.786   ἀλλʼ ὅτε δὴ τὸ τέταρτον ἐπέσσυτο δαίμονι ἶσος,
  Il. 16.787   ἔνθʼ ἄρα τοι Πάτροκλε φάνη βιότοιο τελευτή·

  Il. 20.445   τρὶς μὲν ἔπειτʼ ἐπόρουσε ποδάρκης δῖος Ἀχιλλεὺς
  Il. 20.446   ἔγχεϊ χαλκείῳ, τρὶς δʼ ἠέρα τύψε βαθεῖαν.
> Il. 20.447   ἀλλʼ ὅτε δὴ τὸ τέταρτον ἐπέσσυτο δαίμονι ἶσος,
  Il. 20.448   δεινὰ δʼ ὁμοκλήσας ἔπεα πτερόεντα προσηύδα·

  Il. 22.206   οὐδʼ ἔα ἱέμεναι ἐπὶ Ἕκτορι πικρὰ βέλεμνα,
  Il. 22.207   μή τις κῦδος ἄροιτο βαλών, ὃ δὲ δεύτερος ἔλθοι.
> Il. 22.208   ἀλλʼ ὅτε δὴ τὸ τέταρτον ἐπὶ κρουνοὺς ἀφίκοντο,
  Il. 22.209   καὶ τότε δὴ χρύσεια πατὴρ ἐτίταινε τάλαντα,

# [V1] python homer/concordance.py --loose "ενικησεν" --word
Il. 3.439    [6-9]  νῦν μὲν γὰρ Μενέλαος ἐνίκησεν σὺν Ἀθήνῃ,    <ἐνίκησεν>
-- 1 hit(s)

# [V2] python homer/concordance.py --loose "νικησε" --word
Il. 23.604   [8-9.5]  ἦσθα πάρος· νῦν αὖτε νόον νίκησε νεοίη.    <νίκησε>
-- 1 hit(s)

# [V3] python homer/concordance.py --loose "νικησεν" --word
Od. 10.46    [8-9.5]  ὣς ἔφασαν, βουλὴ δὲ κακὴ νίκησεν ἑταίρων·    <νίκησεν>
-- 1 hit(s)

# [V4] python homer/concordance.py --ngram "ἔνθ᾽ αὖ Σαρπηδὼν μὲν ἀπήμβροτε"
Il. 16.477   [1-8]  ἔνθʼ αὖ Σαρπηδὼν μὲν ἀπήμβροτε δουρὶ φαεινῷ,    <ἔνθʼ αὖ Σαρπηδὼν μὲν ἀπήμβροτε>
-- 1 hit(s)
```

### A.4 Line 55 (accent of Νοβήκος)

```
acute on long penult (η/ω) + C + ος: types 0 tokens 0
circumflex on penult (η/ω) + C + ος: types 51 tokens 269
   e.g. πρῶτος, ἦμος, στῆθος, δηϊοτῆτος, ποτῆτος, τῆμος, τεθνηῶτος, κρητῆρος, δῆμος, κλῆρος, ζωστῆρος, ἦδος

$ python homer/check_line.py "καὶ βάλεν, οὐδ᾽ ἀφάμαρτε Νοβῆκος δεύτερον αὖτις·"
[1] καὶ βάλεν, οὐδ᾽ ἀφάμαρτε Νοβῆκος δεύτερον αὖτις·
  DDDSDS  (unique, tier 0, 1 scansion(s))
  syllables: καὶ βά.λεν οὐδʼ ἀ.φά.μαρ.τε Νο.βῆ.κος δεύ.τε.ρον αὖ.τις
  positions: 1 1.5 2 3 3.5 4 5 5.5 6 7 8 9 9.5 10 11 12
  quantities by word: L SS L SSLS SLL LSS LX
  caesurae: trochaic; bucolic diaeresis: S
  licences: -
  OK (no flags)
```

### A.5 Line 56 (aspiration before Ἑλβέτιος)

The Homer counts list only non-zero categories: there is no line in which an elided τ, π or κ precedes a word with rough breathing, and αὖτʼ never precedes one.

```
Homer:
  ('αὖθ', 'rough') 33 | e.g. Il. 1.370 Χρύσης δʼ αὖθʼ ἱερεὺς ἑκατηβόλου Ἀπόλλωνος
  ('αὖθ', 'smooth') 3 | e.g. Il. 11.48 ἵππους εὖ κατὰ κόσμον ἐρυκέμεν αὖθʼ ἐπὶ τάφρῳ,
  ('αὖτ', 'smooth') 130 | e.g. Il. 1.202 τίπτʼ αὖτʼ αἰγιόχοιο Διὸς τέκος εἰλήλουθας;
Draft composition/drafts/v2.txt :
  8: ἕλετ᾽ ἀμφιβρότην  next word smooth  -> ok
  10: αὖθ᾽ ἑτέρωθεν  next word rough  -> ok
  14: ἔπειτ᾽ ἀφάμαρτε  next word smooth  -> ok
  19: τότ᾽ ἐπέσσυτο  next word smooth  -> ok
  20: αὖτ᾽ ἐδάμασσε  next word smooth  -> ok
  21: αὖτ᾽ ἐπὶ  next word smooth  -> ok
  24: αὖθ᾽ Ἑλβέτιος  next word rough  -> ok
  28: αὖτ᾽ ἔλαβεν·  next word smooth  -> ok
  28: ὑπελείπετ᾽ ἄεθλον.  next word smooth  -> ok
  29: αὖτ᾽ ἐδάμασσε  next word smooth  -> ok
  31: τ᾽ ἀργαλέῳ  next word smooth  -> ok
  34: ἔνθ᾽ ἐδάμασσε  next word smooth  -> ok
  38: αὖθ᾽ ἑτέρωθεν  next word rough  -> ok
  39: ἐπ᾽ εἰροπόκοις  next word smooth  -> ok
  40: τ᾽ αὐλῆς  next word smooth  -> ok
  41: τ᾽ οὐ  next word smooth  -> ok
  45: ὅτ᾽ ἀεθλοφόροι  next word smooth  -> ok
  53: ἔπειτ᾽ ἐπόρουσε  next word smooth  -> ok
  54: τότ᾽ ἀμύνετο  next word smooth  -> ok
  56: ἔνθ᾽ αὖτ᾽  next word smooth  -> ok
  56: αὖτ᾽ Ἑλβέτιος  next word rough  -> ERROR
  58: αὖτ᾽ ἐδάμασσε,  next word smooth  -> ok
  60: ὅτ᾽ ἤλυθε  next word smooth  -> ok

# [E1] python homer/concordance.py --ngram "ἔνθ᾽ αὖθ᾽"
-- 0 hit(s)

# [E2] python homer/concordance.py --ngram "ἔνθ᾽ αὖτ᾽" --count
12

$ python homer/check_line.py "ἔνθ᾽ αὖθ᾽ Ἑλβέτιος προΐει, βάλε δ᾽ ἂψ Ζοκοβείδης,"
[1] ἔνθ᾽ αὖθ᾽ Ἑλβέτιος προΐει, βάλε δ᾽ ἂψ Ζοκοβείδης,
  SDDDDS  (unique, tier 0, 1 scansion(s))
  syllables: ἔνθʼ αὖθʼ Ἑλ.βέ.τι.ος προ.ΐ.ει βά.λε δʼ ἂψ Ζο.κο.βεί.δης
  positions: 1 2 3 3.5 4 5 5.5 6 7 7.5 8 9 9.5 10 11 12
  quantities by word: L L LSSL SSL SS 0 L SSLL
  caesurae: penthemimeral, hephthemimeral; bucolic diaeresis: D
  licences: -
  warn quantity_unattested: ι in 'Ἑλβέτιος' taken as S (metre only); no unambiguous Homeric attestation of this form
  OK (no flags)
```

### A.6 Line 4 and R3 (Ζοκοβείδης: -είδης patronymics; τε … καί; P1)

```
# [L4f] python homer/concordance.py --regex "είδη[ςνω]?[,.·;]?( |$)"
Il. 1.277    [3-5]  μήτε σὺ Πηλείδη ἔθελʼ ἐριζέμεναι βασιλῆϊ    <είδη >
Il. 4.517    [1.5-5]  ἔνθʼ Ἀμαρυγκείδην Διώρεα μοῖρα πέδησε·    <είδην >
Il. 22.280   [3-5]  ἐκ Διὸς ἠείδης τὸν ἐμὸν μόρον, ἦ τοι ἔφης γε·    <είδης >
Od. 9.206    [1-3]  ἠείδη δμώων οὐδʼ ἀμφιπόλων ἐνὶ οἴκῳ,    <είδη >
Od. 15.52    [3-5]  ἥρως Ἀτρείδης, δουρικλειτὸς Μενέλαος,    <είδης, >
-- 5 hit(s)

# [L4m] python homer/concordance.py --regex "Ἀτρείδ"
Od. 15.52    [3-5]  ἥρως Ἀτρείδης, δουρικλειτὸς Μενέλαος,    <Ἀτρείδ>
Od. 19.183   [3-5.5]  ᾤχεθʼ ἅμʼ Ἀτρείδῃσιν, ἐμοὶ δʼ ὄνομα κλυτὸν Αἴθων,    <Ἀτρείδ>
Od. 24.35    [9-12]  τὸν δʼ αὖτε ψυχὴ προσεφώνεεν Ἀτρείδαο·    <Ἀτρείδ>
-- 3 hit(s)

# [L4k] python homer/concordance.py --loose "αμαρυγκε"
Il. 2.622    [1.5-5]  τῶν δʼ Ἀμαρυγκεΐδης ἦρχε κρατερὸς Διώρης·    <Ἀμαρυγκε>
Il. 4.517    [1.5-5]  ἔνθʼ Ἀμαρυγκείδην Διώρεα μοῖρα πέδησε·    <Ἀμαρυγκε>
Il. 23.630   [5.5-8]  ὡς ὁπότε κρείοντʼ Ἀμαρυγκέα θάπτον Ἐπειοὶ    <Ἀμαρυγκέ>
-- 3 hit(s)

# [L4l] python homer/concordance.py --loose "ατρειδ" --count
210

# [L4c] python homer/concordance.py --loose "πηλειδ" --count
52

# [L4a] python homer/concordance.py --ngram "Ὀδυσεύς τε καὶ Ἀτρεΐδης Ἀγαμέμνων"
Il. 14.29    [3.5-12]  Τυδεΐδης Ὀδυσεύς τε καὶ Ἀτρεΐδης Ἀγαμέμνων.    <Ὀδυσεύς τε καὶ Ἀτρεΐδης Ἀγαμέμνων>
Il. 14.380   [3.5-12]  Τυδεΐδης Ὀδυσεύς τε καὶ Ἀτρεΐδης Ἀγαμέμνων·    <Ὀδυσεύς τε καὶ Ἀτρεΐδης Ἀγαμέμνων>
-- 2 hit(s)

# [L4b] python homer/concordance.py --ngram "τε καὶ ἀντίθεος"
Il. 20.232   [5.5-9]  Ἶλός τʼ Ἀσσάρακός τε καὶ ἀντίθεος Γανυμήδης,    <τε καὶ ἀντίθεος>
Od. 3.414    [5.5-9]  Περσεύς τʼ Ἄρητός τε καὶ ἀντίθεος Θρασυμήδης.    <τε καὶ ἀντίθεος>
Od. 8.119    [5.5-9]  Λαοδάμας θʼ Ἅλιός τε καὶ ἀντίθεος Κλυτόνηος.    <τε καὶ ἀντίθεος>
-- 3 hit(s)

# scansion.tsv rows (status, tier, pattern, syllables, word_meter, licences) for the -είδ- forms
Il. 1.277 multiple tier 2 DSDDDS | μή.τε σὺ Πη.λεί.δη ἔ.θελʼ ἐ.ρι.ζέ.με.ναι βα.σι.λῆ.ϊ | LS S LLL LS SLSSL SSLX | licences: synizesis_cross_rare@5(Πηλείδη)
Il. 4.517 unique tier 0 DSSDDS | ἔνθʼ Ἀ.μα.ρυγ.κεί.δην Δι.ώ.ρε.α μοῖ.ρα πέ.δη.σε | L SSLLL LLSS LS SLX | licences: -
Od. 15.52 unique tier 0 SSSSDS | ἥ.ρως Ἀ.τρεί.δης δου.ρι.κλει.τὸς Με.νέ.λα.ος | LL LLL LLLL SSLX | licences: -
Od. 24.35 unique tier 0 SSDDSS | τὸν δʼ αὖ.τε ψυ.χὴ προ.σε.φώ.νε.εν Ἀ.τρεί.δα.ο | L 0 LL LL SSLSS LLLX | licences: -
```

### A.7 Parallels for 20, 29, 30, 36, 43

ev_B's B2 regex is not used for any claim: its capital-letter class also matches lower-case extended Greek. The ὅ γε and pronoun + name claims rest on og.py and oname.py.

```
# context for ngram "τρὶς δέ" (-2/+0 lines): 8 hit(s)
  Il. 5.435   Αἰνείαν κτεῖναι καὶ ἀπὸ κλυτὰ τεύχεα δῦσαι.
  Il. 5.436   τρὶς μὲν ἔπειτʼ ἐπόρουσε κατακτάμεναι μενεαίνων,
> Il. 5.437   τρὶς δέ οἱ ἐστυφέλιξε φαεινὴν ἀσπίδʼ Ἀπόλλων·

  Il. 18.155   τρὶς μέν μιν μετόπισθε ποδῶν λάβε φαίδιμος Ἕκτωρ
  Il. 18.156   ἑλκέμεναι μεμαώς, μέγα δὲ Τρώεσσιν ὁμόκλα·
> Il. 18.157   τρὶς δὲ δύʼ Αἴαντες θοῦριν ἐπιειμένοι ἀλκὴν

  Il. 18.227   δαιόμενον· τὸ δὲ δαῖε θεὰ γλαυκῶπις Ἀθήνη.
  Il. 18.228   τρὶς μὲν ὑπὲρ τάφρου μεγάλʼ ἴαχε δῖος Ἀχιλλεύς,
> Il. 18.229   τρὶς δὲ κυκήθησαν Τρῶες κλειτοί τʼ ἐπίκουροι.

  Il. 21.175   οὐ δύνατʼ ἐκ κρημνοῖο ἐρύσσαι χειρὶ παχείῃ.
  Il. 21.176   τρὶς μέν μιν πελέμιξεν ἐρύσσασθαι μενεαίνων,
> Il. 21.177   τρὶς δὲ μεθῆκε βίης· τὸ δὲ τέτρατον ἤθελε θυμῷ

  Il. 23.815   δεινὸν δερκομένω· θάμβος δʼ ἔχε πάντας Ἀχαιούς.
  Il. 23.816   ἀλλʼ ὅτε δὴ σχεδὸν ἦσαν ἐπʼ ἀλλήλοισιν ἰόντες,
> Il. 23.817   τρὶς μὲν ἐπήϊξαν, τρὶς δὲ σχεδὸν ὁρμήθησαν.

  Od. 4.275   δαίμων, ὃς Τρώεσσιν ἐβούλετο κῦδος ὀρέξαι·
  Od. 4.276   καί τοι Δηΐφοβος θεοείκελος ἕσπετʼ ἰούσῃ.
> Od. 4.277   τρὶς δὲ περίστειξας κοῖλον λόχον ἀμφαφόωσα,

  Od. 11.205   μητρὸς ἐμῆς ψυχὴν ἑλέειν κατατεθνηυίης.
  Od. 11.206   τρὶς μὲν ἐφωρμήθην, ἑλέειν τέ με θυμὸς ἀνώγει,
> Od. 11.207   τρὶς δέ μοι ἐκ χειρῶν σκιῇ εἴκελον ἢ καὶ ὀνείρῳ

  Od. 21.124   στῆ δʼ ἄρʼ ἐπʼ οὐδὸν ἰὼν καὶ τόξου πειρήτιζε.
  Od. 21.125   τρὶς μέν μιν πελέμιξεν ἐρύσσεσθαι μενεαίνων,
> Od. 21.126   τρὶς δὲ μεθῆκε βίης, ἐπιελπόμενος τό γε θυμῷ,

# context for ngram "τρὶς δ᾽" (-2/+0 lines): 9 hit(s)
  Il. 8.168   ἵππους τε στρέψαι καὶ ἐναντίβιον μαχέσασθαι.
  Il. 8.169   τρὶς μὲν μερμήριξε κατὰ φρένα καὶ κατὰ θυμόν,
> Il. 8.170   τρὶς δʼ ἄρʼ ἀπʼ Ἰδαίων ὀρέων κτύπε μητίετα Ζεὺς

  Il. 11.461   αὐτὰρ ὅ γʼ ἐξοπίσω ἀνεχάζετο, αὖε δʼ ἑταίρους.
  Il. 11.462   τρὶς μὲν ἔπειτʼ ἤϋσεν ὅσον κεφαλὴ χάδε φωτός,
> Il. 11.463   τρὶς δʼ ἄϊεν ἰάχοντος ἄρηι φίλος Μενέλαος.

  Il. 16.701   ἔστη τῷ ὀλοὰ φρονέων, Τρώεσσι δʼ ἀρήγων.
  Il. 16.702   τρὶς μὲν ἐπʼ ἀγκῶνος βῆ τείχεος ὑψηλοῖο
> Il. 16.703   Πάτροκλος, τρὶς δʼ αὐτὸν ἀπεστυφέλιξεν Ἀπόλλων

  Il. 16.783   Πάτροκλος δὲ Τρωσὶ κακὰ φρονέων ἐνόρουσε.
  Il. 16.784   τρὶς μὲν ἔπειτʼ ἐπόρουσε θοῷ ἀτάλαντος Ἄρηϊ
> Il. 16.785   σμερδαλέα ἰάχων, τρὶς δʼ ἐννέα φῶτας ἔπεφνεν.

  Il. 20.444   ῥεῖα μάλʼ ὥς τε θεός, ἐκάλυψε δʼ ἄρʼ ἠέρι πολλῇ.
  Il. 20.445   τρὶς μὲν ἔπειτʼ ἐπόρουσε ποδάρκης δῖος Ἀχιλλεὺς
> Il. 20.446   ἔγχεϊ χαλκείῳ, τρὶς δʼ ἠέρα τύψε βαθεῖαν.

  Il. 24.14    ἀλλʼ ὅ γʼ ἐπεὶ ζεύξειεν ὑφʼ ἅρμασιν ὠκέας ἵππους,
  Il. 24.15    Ἕκτορα δʼ ἕλκεσθαι δησάσκετο δίφρου ὄπισθεν,
> Il. 24.16    τρὶς δʼ ἐρύσας περὶ σῆμα Μενοιτιάδαο θανόντος

  Il. 24.271   καὶ τὸ μὲν εὖ κατέθηκαν ἐϋξέστῳ ἐπὶ ῥυμῷ
  Il. 24.272   πέζῃ ἔπι πρώτῃ, ἐπὶ δὲ κρίκον ἕστορι βάλλον,
> Il. 24.273   τρὶς δʼ ἑκάτερθεν ἔδησαν ἐπʼ ὀμφαλόν, αὐτὰρ ἔπειτα

  Od. 9.359   ἀλλὰ τόδʼ ἀμβροσίης καὶ νέκταρός ἐστιν ἀπορρώξ.
  Od. 9.360   ὣς φάτʼ, ἀτάρ οἱ αὖτις ἐγὼ πόρον αἴθοπα οἶνον.
> Od. 9.361   τρὶς μὲν ἔδωκα φέρων, τρὶς δʼ ἔκπιεν ἀφραδίῃσιν.

  Od. 12.103   τῷ δʼ ἐν ἐρινεὸς ἔστι μέγας, φύλλοισι τεθηλώς·
  Od. 12.104   τῷ δʼ ὑπὸ δῖα Χάρυβδις ἀναρροιβδεῖ μέλαν ὕδωρ.
> Od. 12.105   τρὶς μὲν γάρ τʼ ἀνίησιν ἐπʼ ἤματι, τρὶς δʼ ἀναροιβδεῖ

# [B1] python homer/concordance.py --regex "^[Α-ΩἈ-Ὼ][^ ]+ δʼ αὖτʼ " --limit "12"
Il. 2.407    [1-3]  ἕκτον δʼ αὖτʼ Ὀδυσῆα Διὶ μῆτιν ἀτάλαντον.    <ἕκτον δʼ αὖτʼ >
Il. 14.469   [1-3]  Αἴας δʼ αὖτʼ ἐγέγωνεν ἀμύμονι Πουλυδάμαντι·    <Αἴας δʼ αὖτʼ >
Il. 17.304   [1-3]  Ἕκτωρ δʼ αὖτʼ Αἴαντος ἀκόντισε δουρὶ φαεινῷ·    <Ἕκτωρ δʼ αὖτʼ >
Il. 19.38    [1-4]  Πατρόκλῳ δʼ αὖτʼ ἀμβροσίην καὶ νέκταρ ἐρυθρὸν    <Πατρόκλῳ δʼ αὖτʼ >
Od. 9.248    [1-3]  ἥμισυ δʼ αὖτʼ ἔστησεν ἐν ἄγγεσιν, ὄφρα οἱ εἴη    <ἥμισυ δʼ αὖτʼ >
Od. 11.615   [1-3]  ἔγνω δʼ αὖτʼ ἔμʼ ἐκεῖνος, ἐπεὶ ἴδεν ὀφθαλμοῖσιν,    <ἔγνω δʼ αὖτʼ >
-- 6 hit(s)

# [B2] python homer/concordance.py --regex "^αὐτὰρ ὅ γʼ .*[Α-ΩἈ-Ὼ][^ ]+[,.·;]?$" --limit "20"
Il. 6.474    [1-12]  αὐτὰρ ὅ γʼ ὃν φίλον υἱὸν ἐπεὶ κύσε πῆλέ τε χερσὶν    <αὐτὰρ ὅ γʼ ὃν φίλον υἱὸν ἐπεὶ κύσε πῆλέ τε χερσὶν>
Il. 11.461   [1-12]  αὐτὰρ ὅ γʼ ἐξοπίσω ἀνεχάζετο, αὖε δʼ ἑταίρους.    <αὐτὰρ ὅ γʼ ἐξοπίσω ἀνεχάζετο, αὖε δʼ ἑταίρους.>
Il. 12.40    [1-12]  αὐτὰρ ὅ γʼ ὡς τὸ πρόσθεν ἐμάρνατο ἶσος ἀέλλῃ·    <αὐτὰρ ὅ γʼ ὡς τὸ πρόσθεν ἐμάρνατο ἶσος ἀέλλῃ·>
Il. 15.630   [1-12]  αὐτὰρ ὅ γʼ ὥς τε λέων ὀλοόφρων βουσὶν ἐπελθών,    <αὐτὰρ ὅ γʼ ὥς τε λέων ὀλοόφρων βουσὶν ἐπελθών,>
Il. 17.108   [1-12]  αὐτὰρ ὅ γʼ ἐξοπίσω ἀνεχάζετο, λεῖπε δὲ νεκρὸν    <αὐτὰρ ὅ γʼ ἐξοπίσω ἀνεχάζετο, λεῖπε δὲ νεκρὸν>
Il. 23.42    [1-12]  αὐτὰρ ὅ γʼ ἠρνεῖτο στερεῶς, ἐπὶ δʼ ὅρκον ὄμοσσεν·    <αὐτὰρ ὅ γʼ ἠρνεῖτο στερεῶς, ἐπὶ δʼ ὅρκον ὄμοσσεν·>
Il. 24.189   [1-12]  αὐτὰρ ὅ γʼ υἷας ἄμαξαν ἐΰτροχον ἡμιονείην    <αὐτὰρ ὅ γʼ υἷας ἄμαξαν ἐΰτροχον ἡμιονείην>
Od. 9.237    [1-12]  αὐτὰρ ὅ γʼ εἰς εὐρὺ σπέος ἤλασε πίονα μῆλα    <αὐτὰρ ὅ γʼ εἰς εὐρὺ σπέος ἤλασε πίονα μῆλα>
Od. 11.599   [1-12]  αὐτὰρ ὅ γʼ ἂψ ὤσασκε τιταινόμενος, κατὰ δʼ ἱδρὼς    <αὐτὰρ ὅ γʼ ἂψ ὤσασκε τιταινόμενος, κατὰ δʼ ἱδρὼς>
Od. 16.41    [1-12]  αὐτὰρ ὅ γʼ εἴσω ἴεν καὶ ὑπέρβη λάϊνον οὐδόν.    <αὐτὰρ ὅ γʼ εἴσω ἴεν καὶ ὑπέρβη λάϊνον οὐδόν.>
Od. 18.398   [1-12]  αὐτὰρ ὅ γʼ οἰμώξας πέσεν ὕπτιος ἐν κονίῃσι.    <αὐτὰρ ὅ γʼ οἰμώξας πέσεν ὕπτιος ἐν κονίῃσι.>
-- 11 hit(s)

# [B3] python homer/concordance.py --ngram "αὐτὰρ ὅ γ᾽ ἂψ"
Od. 11.599   [1-3]  αὐτὰρ ὅ γʼ ἂψ ὤσασκε τιταινόμενος, κατὰ δʼ ἱδρὼς    <αὐτὰρ ὅ γʼ ἂψ>
-- 1 hit(s)

# [B4] python homer/concordance.py --regex "ἂψ ἐδάμασσ|ἂψ δάμασ"
-- 0 hit(s)

Il. 8.311	ἀλλʼ ὅ γε καὶ τόθʼ ἅμαρτε· παρέσφηλεν γὰρ Ἀπόλλων·
Il. 13.15	ἔνθʼ ἄρʼ ὅ γʼ ἐξ ἁλὸς ἕζετʼ ἰών, ἐλέαιρε δʼ Ἀχαιοὺς
Il. 22.143	ὣς ἄρʼ ὅ γʼ ἐμμεμαὼς ἰθὺς πέτετο, τρέσε δʼ Ἕκτωρ
Od. 14.526	ἀλλʼ ὅ γʼ ἄρʼ ἔξω ἰὼν ὡπλίζετο· χαῖρε δʼ Ὀδυσσεύς,
-- hits: 4

Il. 2.402	αὐτὰρ ὃ βοῦν ἱέρευσε ἄναξ ἀνδρῶν Ἀγαμέμνων
Il. 3.81	αὐτὰρ ὃ μακρὸν ἄϋσεν ἄναξ ἀνδρῶν Ἀγαμέμνων·
Il. 3.118	αὐτὰρ ὃ Ταλθύβιον προΐει κρείων Ἀγαμέμνων
Il. 4.329	αὐτὰρ ὃ πλησίον ἑστήκει πολύμητις Ὀδυσσεύς,
Il. 5.398	αὐτὰρ ὃ βῆ πρὸς δῶμα Διὸς καὶ μακρὸν Ὄλυμπον
Il. 5.449	αὐτὰρ ὃ εἴδωλον τεῦξʼ ἀργυρότοξος Ἀπόλλων
Il. 10.288	αὐτὰρ ὃ μειλίχιον μῦθον φέρε Καδμείοισι
Il. 13.698	αὐτὰρ ὃ Ἰφίκλοιο πάϊς τοῦ Φυλακίδαο.
Il. 19.40	αὐτὰρ ὃ βῆ παρὰ θῖνα θαλάσσης δῖος Ἀχιλλεὺς
Il. 19.51	αὐτὰρ ὃ δεύτατος ἦλθεν ἄναξ ἀνδρῶν Ἀγαμέμνων
Il. 20.407	αὐτὰρ ὃ βῆ σὺν δουρὶ μετʼ ἀντίθεον Πολύδωρον
Il. 20.460	αὐτὰρ ὃ Λαόγονον καὶ Δάρδανον υἷε Βίαντος
Il. 24.631	αὐτὰρ ὃ Δαρδανίδην Πρίαμον θαύμαζεν Ἀχιλλεὺς
Od. 5.354	αὐτὰρ ὁ μερμήριξε πολύτλας δῖος Ὀδυσσεύς,
Od. 6.224	αὐτὰρ ὁ ἐκ ποταμοῦ χρόα νίζετο δῖος Ὀδυσσεὺς
Od. 7.139	αὐτὰρ ὁ βῆ διὰ δῶμα πολύτλας δῖος Ὀδυσσεὺς
Od. 7.177	αὐτὰρ ὁ πῖνε καὶ ἦσθε πολύτλας δῖος Ὀδυσσεύς.
Od. 7.230	αὐτὰρ ὁ ἐν μεγάρῳ ὑπελείπετο δῖος Ὀδυσσεύς,
Od. 19.1	αὐτὰρ ὁ ἐν μεγάρῳ ὑπελείπετο δῖος Ὀδυσσεύς,
Od. 19.51	αὐτὰρ ὁ ἐν μεγάρῳ ὑπελείπετο δῖος Ὀδυσσεύς,
Od. 20.1	αὐτὰρ ὁ ἐν προδόμῳ εὐνάζετο δῖος Ὀδυσσεύς·
Od. 22.1	αὐτὰρ ὁ γυμνώθη ῥακέων πολύμητις Ὀδυσσεύς,
Od. 24.176	αὐτὰρ ὁ δέξατο χειρὶ πολύτλας δῖος Ὀδυσσεύς,
-- hits: 23

# [F1] python homer/concordance.py --ngram "βάλε δὲ"
Il. 4.519    [5.5-7]  κνήμην δεξιτερήν· βάλε δὲ Θρῃκῶν ἀγὸς ἀνδρῶν    <βάλε δὲ>
Il. 5.533    [7.5-9]  ἦ καὶ ἀκόντισε δουρὶ θοῶς, βάλε δὲ πρόμον ἄνδρα    <βάλε δὲ>
Il. 14.450   [3.5-5]  Πανθοΐδης, βάλε δὲ Προθοήνορα δεξιὸν ὦμον    <βάλε δὲ>
Od. 22.82    [5.5-7]  ἰὸν ἀποπροίει, βάλε δὲ στῆθος παρὰ μαζόν,    <βάλε δὲ>
-- 4 hit(s)

# [F2] python homer/concordance.py --ngram "βάλε δ᾽"
Il. 15.541   [7.5-9]  στῆ δʼ εὐρὰξ σὺν δουρὶ λαθών, βάλε δʼ ὦμον ὄπισθεν·    <βάλε δʼ>
Il. 16.737   [5.5-7]  οὐδʼ ἁλίωσε βέλος, βάλε δʼ Ἕκτορος ἡνιοχῆα    <βάλε δʼ>
Od. 24.179   [5.5-7]  δεινὸν παπταίνων, βάλε δʼ Ἀντίνοον βασιλῆα.    <βάλε δʼ>
-- 3 hit(s)

# [F3] python homer/concordance.py --ngram "στῆ δὲ μάλ᾽ ἐγγὺς ἰών"
Il. 4.496    [1-5]  στῆ δὲ μάλʼ ἐγγὺς ἰὼν καὶ ἀκόντισε δουρὶ φαεινῷ    <στῆ δὲ μάλʼ ἐγγὺς ἰὼν>
Il. 5.611    [1-5]  στῆ δὲ μάλʼ ἐγγὺς ἰών, καὶ ἀκόντισε δουρὶ φαεινῷ,    <στῆ δὲ μάλʼ ἐγγὺς ἰών>
Il. 11.429   [1-5]  στῆ δὲ μάλʼ ἐγγὺς ἰὼν καί μιν πρὸς μῦθον ἔειπεν    <στῆ δὲ μάλʼ ἐγγὺς ἰὼν>
Il. 12.457   [1-5]  στῆ δὲ μάλʼ ἐγγὺς ἰών, καὶ ἐρεισάμενος βάλε μέσσας    <στῆ δὲ μάλʼ ἐγγὺς ἰών>
Il. 17.347   [1-5]  στῆ δὲ μάλʼ ἐγγὺς ἰών, καὶ ἀκόντισε δουρὶ φαεινῷ,    <στῆ δὲ μάλʼ ἐγγὺς ἰών>
-- 5 hit(s)

# [F4] python homer/concordance.py --regex "βάλε[ν]?[,.·;]? (?!.*(ἔγχ|δουρ|ἰ[ῷο]|λᾶ|χερμ))" --limit "0" --count
109

# [N1] python homer/concordance.py --ngram "θυμὸς ἀνῆκεν"
Il. 6.256    [9-12]  μαρνάμενοι περὶ ἄστυ· σὲ δʼ ἐνθάδε θυμὸς ἀνῆκεν    <θυμὸς ἀνῆκεν>
Il. 7.25     [9-12]  ἦλθες ἀπʼ Οὐλύμποιο, μέγας δέ σε θυμὸς ἀνῆκεν;    <θυμὸς ἀνῆκεν>
Il. 21.395   [9-12]  θάρσος ἄητον ἔχουσα, μέγας δέ σε θυμὸς ἀνῆκεν;    <θυμὸς ἀνῆκεν>
-- 3 hit(s)

# [N2] python homer/concordance.py --ngram "θυμὸς ἀνῆκε"
Il. 7.152    [3-5.5]  ἀλλʼ ἐμὲ θυμὸς ἀνῆκε πολυτλήμων πολεμίζειν    <θυμὸς ἀνῆκε>
Il. 10.389   [9-12]  νῆας ἔπι γλαφυράς; ἦ σʼ αὐτὸν θυμὸς ἀνῆκε;    <θυμὸς ἀνῆκε>
Il. 12.307   [9-12]  ὥς ῥα τότʼ ἀντίθεον Σαρπηδόνα θυμὸς ἀνῆκε    <θυμὸς ἀνῆκε>
Il. 22.252   [9-12]  μεῖναι ἐπερχόμενον· νῦν αὖτέ με θυμὸς ἀνῆκε    <θυμὸς ἀνῆκε>
-- 4 hit(s)

# context for ngram "Θρασυμήδεα δῖον ἀνῆκεν" (-0/+1 lines): 1 hit(s)
> Il. 17.705   ἀλλʼ ὅ γε τοῖσιν μὲν Θρασυμήδεα δῖον ἀνῆκεν,
  Il. 17.706   αὐτὸς δʼ αὖτʼ ἐπὶ Πατρόκλῳ ἥρωϊ βεβήκει,

# [N3] python homer/concordance.py --ngram "ὣς τότε" --limit "4"
Il. 1.601    [1-2]  ὣς τότε μὲν πρόπαν ἦμαρ ἐς ἠέλιον καταδύντα    <ὣς τότε>
Il. 5.600    [1-2]  ὣς τότε Τυδεΐδης ἀνεχάζετο, εἶπέ τε λαῷ·    <ὣς τότε>
Il. 17.679   [1-2]  ὣς τότε σοὶ Μενέλαε διοτρεφὲς ὄσσε φαεινὼ    <ὣς τότε>
Il. 19.359   [1-2]  ὣς τότε ταρφειαὶ κόρυθες λαμπρὸν γανόωσαι    <ὣς τότε>
-- 13 hit(s), 4 shown

# [N4] python homer/concordance.py --ngram "μένος καὶ θυμὸς ἀγήνωρ"
Il. 20.174   [6-12]  ὣς Ἀχιλῆʼ ὄτρυνε μένος καὶ θυμὸς ἀγήνωρ    <μένος καὶ θυμὸς ἀγήνωρ>
-- 1 hit(s)

# context for ngram "θυμὸς ἀνῆκεν" (-1/+1 lines): 3 hit(s)
  Il. 6.255   ἦ μάλα δὴ τείρουσι δυσώνυμοι υἷες Ἀχαιῶν
> Il. 6.256   μαρνάμενοι περὶ ἄστυ· σὲ δʼ ἐνθάδε θυμὸς ἀνῆκεν
  Il. 6.257   ἐλθόντʼ ἐξ ἄκρης πόλιος Διὶ χεῖρας ἀνασχεῖν.

  Il. 7.24    τίπτε σὺ δʼ αὖ μεμαυῖα Διὸς θύγατερ μεγάλοιο
> Il. 7.25    ἦλθες ἀπʼ Οὐλύμποιο, μέγας δέ σε θυμὸς ἀνῆκεν;
  Il. 7.26    ἦ ἵνα δὴ Δαναοῖσι μάχης ἑτεραλκέα νίκην

  Il. 21.394   τίπτʼ αὖτʼ ὦ κυνάμυια θεοὺς ἔριδι ξυνελαύνεις
> Il. 21.395   θάρσος ἄητον ἔχουσα, μέγας δέ σε θυμὸς ἀνῆκεν;
  Il. 21.396   ἦ οὐ μέμνῃ ὅτε Τυδεΐδην Διομήδεʼ ἀνῆκας

# context for ngram "θυμὸς ἀνῆκε" (-0/+1 lines): 4 hit(s)
> Il. 7.152   ἀλλʼ ἐμὲ θυμὸς ἀνῆκε πολυτλήμων πολεμίζειν
  Il. 7.153   θάρσεϊ ᾧ· γενεῇ δὲ νεώτατος ἔσκον ἁπάντων·

> Il. 10.389   νῆας ἔπι γλαφυράς; ἦ σʼ αὐτὸν θυμὸς ἀνῆκε;
  Il. 10.390   τὸν δʼ ἠμείβετʼ ἔπειτα Δόλων, ὑπὸ δʼ ἔτρεμε γυῖα·

> Il. 12.307   ὥς ῥα τότʼ ἀντίθεον Σαρπηδόνα θυμὸς ἀνῆκε
  Il. 12.308   τεῖχος ἐπαΐξαι διά τε ῥήξασθαι ἐπάλξεις.

> Il. 22.252   μεῖναι ἐπερχόμενον· νῦν αὖτέ με θυμὸς ἀνῆκε
  Il. 22.253   στήμεναι ἀντία σεῖο· ἕλοιμί κεν ἤ κεν ἁλοίην.

# context for ngram "Θρασυμήδεα δῖον ἀνῆκεν" (-0/+0 lines): 1 hit(s)
> Il. 17.705   ἀλλʼ ὅ γε τοῖσιν μὲν Θρασυμήδεα δῖον ἀνῆκεν,

# context for ngram "ὥς ῥα τότ᾽ ἀντίθεον Σαρπηδόνα θυμὸς ἀνῆκε" (-8/+1 lines): 1 hit(s)
  Il. 12.299   βῆ ῥʼ ἴμεν ὥς τε λέων ὀρεσίτροφος, ὅς τʼ ἐπιδευὴς
  Il. 12.300   δηρὸν ἔῃ κρειῶν, κέλεται δέ ἑ θυμὸς ἀγήνωρ
  Il. 12.301   μήλων πειρήσοντα καὶ ἐς πυκινὸν δόμον ἐλθεῖν·
  Il. 12.302   εἴ περ γάρ χʼ εὕρῃσι παρʼ αὐτόφι βώτορας ἄνδρας
  Il. 12.303   σὺν κυσὶ καὶ δούρεσσι φυλάσσοντας περὶ μῆλα,
  Il. 12.304   οὔ ῥά τʼ ἀπείρητος μέμονε σταθμοῖο δίεσθαι,
  Il. 12.305   ἀλλʼ ὅ γʼ ἄρʼ ἢ ἥρπαξε μετάλμενος, ἠὲ καὶ αὐτὸς
  Il. 12.306   ἔβλητʼ ἐν πρώτοισι θοῆς ἀπὸ χειρὸς ἄκοντι·
> Il. 12.307   ὥς ῥα τότʼ ἀντίθεον Σαρπηδόνα θυμὸς ἀνῆκε
  Il. 12.308   τεῖχος ἐπαΐξαι διά τε ῥήξασθαι ἐπάλξεις.
```

### A.8 Similes (draft check; Il. 5.136-143, 20.164-165, 23.758-759, 4.518-519)

```
simile opener at 16: ὡς δ᾽ ὅτε τις στατὸς ἵππος ἀκοστήσας ἐπὶ φάτνῃ
   apodosis line: 19: ὣς ἄρ᾽ ὅ γ᾽ Ἑλβέτιος τότ᾽ ἐπέσσυτο δεύτερον αὖτε·; vehicle lines 16-18 (3 lines)
simile opener at 38: Σέρβος δ᾽ αὖθ᾽ ἑτέρωθεν ἐναντίον ὦρτο λέων ὣς
   apodosis line: 43: ὣς τότε Σέρβον ἀνῆκε μένος καὶ θυμὸς ἀγήνωρ·; vehicle lines 38-42 (5 lines)
simile opener at 45: ὡς δ᾽ ὅτ᾽ ἀεθλοφόροι περὶ τέρματα μώνυχες ἵπποι
   apodosis line: 48: ὣς τὼ πολλάκι δὴ περὶ τέρματα δινηθήτην,; vehicle lines 45-47 (3 lines)

# context for ngram "ὅν ῥά τε ποιμὴν ἀγρῷ ἐπ᾽ εἰροπόκοις ὀΐεσσι" (-1/+6 lines): 1 hit(s)
  Il. 5.136   δὴ τότε μιν τρὶς τόσσον ἕλεν μένος ὥς τε λέοντα
> Il. 5.137   ὅν ῥά τε ποιμὴν ἀγρῷ ἐπʼ εἰροπόκοις ὀΐεσσι
  Il. 5.138   χραύσῃ μέν τʼ αὐλῆς ὑπεράλμενον οὐδὲ δαμάσσῃ·
  Il. 5.139   τοῦ μέν τε σθένος ὦρσεν, ἔπειτα δέ τʼ οὐ προσαμύνει,
  Il. 5.140   ἀλλὰ κατὰ σταθμοὺς δύεται, τὰ δʼ ἐρῆμα φοβεῖται·
  Il. 5.141   αἳ μέν τʼ ἀγχιστῖναι ἐπʼ ἀλλήλῃσι κέχυνται,
  Il. 5.142   αὐτὰρ ὃ ἐμμεμαὼς βαθέης ἐξάλλεται αὐλῆς·
  Il. 5.143   ὣς μεμαὼς Τρώεσσι μίγη κρατερὸς Διομήδης.

# context for ngram "Πηλεΐδης δ᾽ ἑτέρωθεν ἐναντίον ὦρτο λέων ὣς" (-0/+1 lines): 1 hit(s)
> Il. 20.164   Πηλεΐδης δʼ ἑτέρωθεν ἐναντίον ὦρτο λέων ὣς
  Il. 20.165   σίντης, ὅν τε καὶ ἄνδρες ἀποκτάμεναι μεμάασιν

# context for ngram "ἔκφερ᾽ Ὀϊλιάδης" (-1/+0 lines): 1 hit(s)
  Il. 23.758   τοῖσι δʼ ἀπὸ νύσσης τέτατο δρόμος· ὦκα δʼ ἔπειτα
> Il. 23.759   ἔκφερʼ Ὀϊλιάδης· ἐπὶ δʼ ὄρνυτο δῖος Ὀδυσσεὺς

# context for ngram "βάλε δὲ Θρῃκῶν ἀγὸς ἀνδρῶν" (-1/+0 lines): 1 hit(s)
  Il. 4.518   χερμαδίῳ γὰρ βλῆτο παρὰ σφυρὸν ὀκριόεντι
> Il. 4.519   κνήμην δεξιτερήν· βάλε δὲ Θρῃκῶν ἀγὸς ἀνδρῶν
```

### A.9 Rulings, lexicon and δαμάζω

ev_R holds the remaining queries cited in §7; ev_verbatim lists the draft verses that are whole Homeric lines; ev_identity is the identity check behind every "unchanged" row.

```
R4 δίς: 0 []
R5 ἐξεναρίζω: 0 []
R6 πάλιν: 1 [(22, 'παλιν')]
R2 ἰσόθεος: 0 []
R3 withdrawn Ζοκοβίδης/Νοβάκος: 0 []
Ζοκοβείδης: 4 [(4, 'ζοκοβειδησ'), (36, 'ζοκοβειδησ'), (53, 'ζοκοβειδησ'), (56, 'ζοκοβειδησ')]
Νοβήκος: 1 [(55, 'νοβηκοσ')]
δαμάζω (aor.): 7 [(20, 'εδαμασσε'), (24, 'δαμασεν'), (29, 'εδαμασσε'), (30, 'εδαμασσε'), (34, 'εδαμασσε'), (40, 'δαμασση'), (58, 'εδαμασσε')]
prohibited (γραμμ, στεγ, οχλ, ωρη/ωρα, δικτυ, ραβδ, χλο, χορτ, δικαστ, αθλητησ, σφαιριστ, ηττ): 0 []

# [D1] python homer/concordance.py --loose "εδαμασσε" --word
Il. 6.159    [9.5-12]  Ἀργείων· Ζεὺς γάρ οἱ ὑπὸ σκήπτρῳ ἐδάμασσε.    <ἐδάμασσε>
Il. 13.434   [9.5-12]  τὸν τόθʼ ὑπʼ Ἰδομενῆϊ Ποσειδάων ἐδάμασσε    <ἐδάμασσε>
Il. 16.826   [7.5-9.5]  πολλὰ δέ τʼ ἀσθμαίνοντα λέων ἐδάμασσε βίηφιν·    <ἐδάμασσε>
Od. 11.171   [3.5-5.5]  τίς νύ σε κὴρ ἐδάμασσε τανηλεγέος θανάτοιο;    <ἐδάμασσε>
Od. 11.398   [3.5-5.5]  τίς νύ σε κὴρ ἐδάμασσε τανηλεγέος θανάτοιο;    <ἐδάμασσε>
Od. 22.246   [3.5-5.5]  τοὺς δʼ ἤδη ἐδάμασσε βιὸς καὶ ταρφέες ἰοί.    <ἐδάμασσε>
Od. 22.413   [3.5-5.5]  τούσδε δὲ μοῖρʼ ἐδάμασσε θεῶν καὶ σχέτλια ἔργα·    <ἐδάμασσε>
-- 7 hit(s)

# [D2] python homer/concordance.py --loose "εδαμασσεν" --word
Il. 14.316   [9.5-12]  θυμὸν ἐνὶ στήθεσσι περιπροχυθεὶς ἐδάμασσεν,    <ἐδάμασσεν>
Il. 19.203   [9.5-12]  νῦν δʼ οἳ μὲν κέαται δεδαϊγμένοι, οὓς ἐδάμασσεν    <ἐδάμασσεν>
Od. 11.399   [9.5-12]  ἦε σέ γʼ ἐν νήεσσι Ποσειδάων ἐδάμασσεν    <ἐδάμασσεν>
Od. 11.406   [9.5-12]  οὔτʼ ἐμέ γʼ ἐν νήεσσι Ποσειδάων ἐδάμασσεν    <ἐδάμασσεν>
Od. 24.109   [9.5-12]  ἦ ὔμμʼ ἐν νήεσσι Ποσειδάων ἐδάμασσεν,    <ἐδάμασσεν>
-- 5 hit(s)

# [D3] python homer/concordance.py --loose "δαμασσε" --word
Il. 9.118    [6-7.5]  ὡς νῦν τοῦτον ἔτισε, δάμασσε δὲ λαὸν Ἀχαιῶν.    <δάμασσε>
Il. 11.98    [6-7.5]  ἔνδον ἅπας πεπάλακτο· δάμασσε δέ μιν μεμαῶτα.    <δάμασσε>
Il. 12.186   [6-7.5]  ἔνδον ἅπας πεπάλακτο· δάμασσε δέ μιν μεμαῶτα·    <δάμασσε>
Il. 18.119   [4-5.5]  ἀλλά ἑ μοῖρα δάμασσε καὶ ἀργαλέος χόλος Ἥρης.    <δάμασσε>
Il. 20.400   [6-7.5]  ἔνδον ἅπας πεπάλακτο· δάμασσε δέ μιν μεμαῶτα.    <δάμασσε>
-- 5 hit(s)

# [D4] python homer/concordance.py --loose "δαμασε" --word
Il. 22.446   [5.5-7]  χερσὶν Ἀχιλλῆος δάμασε γλαυκῶπις Ἀθήνη.    <δάμασε>
-- 1 hit(s)

# [D5] python homer/concordance.py --loose "δαμασεν" --word
-- 0 hit(s)

# [D6] python homer/concordance.py --loose "εδαμασε" --word
-- 0 hit(s)

# [R1] python homer/concordance.py --ngram "δ᾽ ἑτέρωθεν" --count
22

# [R2] python homer/concordance.py --ngram "ἐδύσετο τεύχεα καλὰ"
Il. 3.328    [6-12]  αὐτὰρ ὅ γʼ ἀμφʼ ὤμοισιν ἐδύσετο τεύχεα καλὰ    <ἐδύσετο τεύχεα καλὰ>
Od. 23.366   [6-12]  ἦ ῥα καὶ ἀμφʼ ὤμοισιν ἐδύσετο τεύχεα καλά,    <ἐδύσετο τεύχεα καλά>
-- 2 hit(s)

# [R3] python homer/concordance.py --ngram "τὸν δ᾽ αὖθ᾽"
Il. 6.144    [1-2]  τὸν δʼ αὖθʼ Ἱππολόχοιο προσηύδα φαίδιμος υἱός·    <τὸν δʼ αὖθʼ>
-- 1 hit(s)

# [R4] python homer/concordance.py --ngram "ὀψὲ δὲ δὴ" --count
12

# [R5] python homer/concordance.py --ngram "καί νύ κεν ἔνθ᾽"
Il. 5.311    [1-3]  καί νύ κεν ἔνθʼ ἀπόλοιτο ἄναξ ἀνδρῶν Αἰνείας,    <καί νύ κεν ἔνθʼ>
Il. 5.388    [1-3]  καί νύ κεν ἔνθʼ ἀπόλοιτο Ἄρης ἆτος πολέμοιο,    <καί νύ κεν ἔνθʼ>
Il. 8.90     [3-5]  Ἕκτορα· καί νύ κεν ἔνθʼ ὁ γέρων ἀπὸ θυμὸν ὄλεσσεν    <καί νύ κεν ἔνθʼ>
-- 3 hit(s)

# [R6] python homer/concordance.py --ngram "εἰ μή οἱ"
Il. 17.71    [4-5.5]  Ἀτρεΐδης, εἰ μή οἱ ἀγάσσατο Φοῖβος Ἀπόλλων,    <εἰ μή οἱ>
Il. 22.203   [1-3]  εἰ μή οἱ πύματόν τε καὶ ὕστατον ἤντετʼ Ἀπόλλων    <εἰ μή οἱ>
-- 2 hit(s)

# [R7] python homer/concordance.py --ngram "τρὶς μὲν ἔπειτ᾽ ἐπόρουσε"
Il. 5.436    [1-5.5]  τρὶς μὲν ἔπειτʼ ἐπόρουσε κατακτάμεναι μενεαίνων,    <τρὶς μὲν ἔπειτʼ ἐπόρουσε>
Il. 16.784   [1-5.5]  τρὶς μὲν ἔπειτʼ ἐπόρουσε θοῷ ἀτάλαντος Ἄρηϊ    <τρὶς μὲν ἔπειτʼ ἐπόρουσε>
Il. 20.445   [1-5.5]  τρὶς μὲν ἔπειτʼ ἐπόρουσε ποδάρκης δῖος Ἀχιλλεὺς    <τρὶς μὲν ἔπειτʼ ἐπόρουσε>
-- 3 hit(s)

# [R8] python homer/concordance.py --loose "αμυνετο" --word
Il. 11.484   [6-8]  ἀΐσσων ᾧ ἔγχει ἀμύνετο νηλεὲς ἦμαρ.    <ἀμύνετο>
Il. 13.514   [6-8]  τώ ῥα καὶ ἐν σταδίῃ μὲν ἀμύνετο νηλεὲς ἦμαρ,    <ἀμύνετο>
-- 2 hit(s)

# [R9] python homer/concordance.py --ngram "Διὸς δ᾽ ἐτελείετο βουλή"
Il. 1.5      [6-12]  οἰωνοῖσί τε πᾶσι, Διὸς δʼ ἐτελείετο βουλή,    <Διὸς δʼ ἐτελείετο βουλή>
Od. 11.297   [6-12]  θέσφατα πάντʼ εἰπόντα· Διὸς δʼ ἐτελείετο βουλή.    <Διὸς δʼ ἐτελείετο βουλή>
-- 2 hit(s)

# [R10] python homer/concordance.py --ngram "καὶ βάλεν οὐδ᾽ ἀφάμαρτε"
Il. 11.350   [1-5.5]  καὶ βάλεν, οὐδʼ ἀφάμαρτε τιτυσκόμενος κεφαλῆφιν,    <καὶ βάλεν, οὐδʼ ἀφάμαρτε>
Il. 13.160   [1-5.5]  καὶ βάλεν, οὐδʼ ἀφάμαρτε, κατʼ ἀσπίδα πάντοσʼ ἐΐσην    <καὶ βάλεν, οὐδʼ ἀφάμαρτε>
-- 2 hit(s)

# [R11] python homer/concordance.py --ngram "βοὴν ἀγαθὸν Μενέλαον" --count
5

# [R12] python homer/concordance.py --ngram "ἐπέσσυτο" --count
12

     12 6	8
      1 metrical_start	metrical_end
# [R13] python homer/concordance.py --ngram "ἀμύνετο νηλεὲς ἦμαρ"
Il. 11.484   [6-12]  ἀΐσσων ᾧ ἔγχει ἀμύνετο νηλεὲς ἦμαρ.    <ἀμύνετο νηλεὲς ἦμαρ>
Il. 13.514   [6-12]  τώ ῥα καὶ ἐν σταδίῃ μὲν ἀμύνετο νηλεὲς ἦμαρ,    <ἀμύνετο νηλεὲς ἦμαρ>
-- 2 hit(s)

3	Il. 1.6
6	Il. 3.330, Il. 11.17, Il. 16.131, Il. 19.369
8	Il. 11.32
9	Il. 3.338, Od. 17.4
11	Il. 3.344
13	Il. 11.336
16	Il. 6.506, Il. 15.263
17	Il. 6.507, Il. 15.264
18	Il. 6.508, Il. 15.265
26	Il. 12.436, Il. 15.413
31	Il. 13.85
37	Il. 5.438, Il. 16.705, Il. 16.786, Il. 20.447
39	Il. 5.137
40	Il. 5.138
41	Il. 5.139
42	Il. 5.142
45	Il. 22.162
46	Il. 22.163
47	Il. 22.164
49	Il. 8.69, Il. 22.209
50	Il. 8.70, Il. 22.210
59	Il. 11.596, Il. 13.673, Il. 18.1

identical to v1 (v2 n = v1 n): 1=1, 2=2, 3=3, 6=6, 7=7, 8=8, 9=9, 10=10, 11=11, 12=12, 13=13, 14=14, 16=16, 17=17, 18=18, 19=19, 21=21, 22=22, 25=25, 26=26, 31=31, 37=37, 45=42, 49=44, 50=45, 51=46, 52=47, 59=54, 60=55
changed (v2 n <- v1 n): 4<-4, 5<-5, 15<-15, 20<-20, 23<-23, 24<-24, 27<-27, 28<-28, 29<-29, 30<-30, 32<-32, 33<-33, 34<-34, 35<-35, 36<-36, 38<-38, 39<-39, 40<-40, 44<-41, 46<-43, 53<-48, 54<-49, 55<-50, 56<-51, 57<-52, 58<-53
new: [41, 42, 43, 47, 48]
```

### A.10 LSJ (fetched 2026-10-07; Logeion API `anastrophe.uchicago.edu/logeion-api/detail?w=…`, LSJ text with HTML stripped by `lsj_text.py`; δαμάζω and δεύτερος also seen on Perseus `…1999.04.0057:entry=dama/zw`, `entry=deu/teros`)

* **δαμάζω**: "overpower: I of animals, tame, break in … II of maidens, make subject to a husband … III subdue, conquer, Od. 9.59, al. … b of the gods, bring low, Il. 9.118, 16.845 … 2 lay low, kill, esp. in fight … 3 of the powers of nature, etc., overcome, overpower, ἔρος … θυμὸν ἐνὶ στήθεσσιν … ἐδάμασσεν 14.316".
* **δεύτερος**: "neut. as Adv., δεύτερον αὖ, αὖτε, αὖτις, a second time, Il. 3.332, 191, Od. 9.354".
* **ἄφαρ**: "straightway, forthwith, in Hom. mostly at the beginning of a clause, with δέ following … 2 suddenly, quickly, ἄ. κεραοὶ τελέθουσι Od. 4.85: strengthd., ἄ. αὐτίκα Il. 23.593".
* **ἄψ**: "backwards, back again, freq. in Hom., mostly with Verbs of motion … 2 of actions, again, in return, ἂ. διδόναι Il. 22.277; ἂ. ἀφελέσθαι 16.54; ἂ. ἀπολύειν 6.427; ἂ. ἀρέσαι 9.120".
* **ἐξάλλομαι**: "leap out of or forth from, ἐξάλλεται αὐλῆς, of a lion, Il. 5.142".
* **ἀνίημι** II.2: "generally, set on or urge to do a thing, c. inf., … Il. 2.276, 5.422: freq. c. acc. pers. only, let loose, excite, as … μέγας δέ σε θυμὸς ἀνῆκεν Il. 7.25; τοῖσιν μὲν Θρασυμήδεα δῖον ἀνῆκεν urged Thrasymedes to their aid, 17.705".
* **κέρδος** II: "in pl., cunning arts, wiles, ὃς δέ κε κ. εἰδῇ Il. 23.322, cf. 709".

## Appendix B. Scripts

Saved under the session scratchpad and reproduced here. Run from the repository root with `.venv` active; the Python scripts take the repository path (and, where needed, a draft path) as arguments and are run with `python -I`.

### B.1 identity.py (v2 vs v1 verses)

```python
# A.0: which v2 verses are character-identical to their v1 source verse (v2.jsonl v1_line), and v2.txt = v2.jsonl text
import json, sys
d = sys.argv[1]
v1 = {r['n']: r['text'] for r in map(json.loads, open(f'{d}/v1.jsonl', encoding='utf-8'))}
v2 = [json.loads(l) for l in open(f'{d}/v2.jsonl', encoding='utf-8')]
txt = open(f'{d}/v2.txt', encoding='utf-8').read().splitlines()
same, changed, new = [], [], []
for r in v2:
    assert txt[r['n'] - 1].strip() == r['text'].strip()
    m = r.get('v1_line')
    if m is None: new.append(r['n'])
    elif v1[m] == r['text']: same.append((r['n'], m))
    else: changed.append((r['n'], m))
print('identical to v1 (v2 n = v1 n):', ', '.join(f'{a}={b}' for a, b in same))
print('changed (v2 n <- v1 n):', ', '.join(f'{a}<-{b}' for a, b in changed))
print('new:', new)
```

### B.2 ctx.py (hits with context lines)

```python
# usage: python -I ctx.py REPO "ngram" BEFORE AFTER  -> each hit with context lines
import sys
sys.path.insert(0, sys.argv[1] + '/homer')
from concordance import Concordance
c = Concordance(); L = c.lines
idx = {(l.work, l.book, l.line): i for i, l in enumerate(L)}
q, b, a = sys.argv[2], int(sys.argv[3]), int(sys.argv[4])
mode = sys.argv[5] if len(sys.argv) > 5 else 'ngram'
hits = getattr(c, mode)(q) if mode != 'loose_word' else c.loose(q, word=True)
print(f'# context for {mode} "{q}" (-{b}/+{a} lines): {len(hits)} hit(s)')
seen=set()
for h in hits:
    i = idx[(h.work, h.book, h.line)]
    if i in seen: continue
    seen.add(i)
    for j in range(i-b, i+a+1):
        if 0 <= j < len(L) and (L[j].work, L[j].book) == (L[i].work, L[i].book):
            mark = '>' if j == i else ' '
            print(f'{mark} {L[j].work}. {L[j].book}.{L[j].line:<5} {L[j].text}')
    print()
```

### B.3 og.py and oname.py (ὅ γε / pronoun + appositive name)

```python
# lines with "ὅ γʼ"/"ὅ γε" whose last word is a capitalised nominative-looking name (ends in -ς/-ων/-ευς etc.)
import sys, re
sys.path.insert(0, sys.argv[1] + '/homer')
from concordance import Concordance
c = Concordance()
n = 0
for l in c.lines:
    t = l.text
    if not re.search(r'(^|\s)ὅ γ(ʼ|ε)\s', t): continue
    w = re.sub(r'[,.·;:!]+$', '', t.split()[-1])
    if w[:1].isupper() and re.search(r'(ς|ων|ωρ|ευς|ης)$', w):
        n += 1; print(f'{l.work}. {l.book}.{l.line}\t{t}')
print('-- hits:', n)
```

```python
# lines opening "αὐτὰρ ὁ/ὃ" or "ὁ δʼ/ὃ δʼ" with no further punctuation, ending in a capitalised name: pronoun + appositive name
import sys, re
sys.path.insert(0, sys.argv[1] + '/homer')
from concordance import Concordance
c = Concordance(); n = 0
for l in c.lines:
    t = l.text
    if not re.match(r'^(αὐτὰρ (ὁ|ὃ|ὅ γʼ) |ὁ δʼ |ὃ δʼ )', t): continue
    body = re.sub(r'[,.·;:!]+$', '', t)
    if re.search(r'[,.·;]', body): continue
    w = body.split()[-1]
    if w[:1].isupper():
        n += 1; print(f'{l.work}. {l.book}.{l.line}\t{t}')
print('-- hits:', n)
```

### B.4 accent.py (accent of -η/ω + C + ος)

```python
# Homeric words whose penult is a long vowel (η or ω) with ACUTE + one consonant + final -ος (short):
# Greek accent law (long accented penult + short ultima -> circumflex) predicts none.
import sys, re, unicodedata as U, collections
sys.path.insert(0, sys.argv[1] + '/homer')
from concordance import Concordance
c = Concordance()
acute = collections.Counter(); circ = collections.Counter(); ex = {}
for l in c.lines:
    for w in re.findall(r'[^\s,.·;:!ʼ]+', l.text):
        m = re.search(r'([ηωΗΩ][̀-ͯ]*)([βγδζθκλμνπρστφχψ])ος$', U.normalize('NFD', w))
        if not m: continue
        marks = m.group(1)
        if '́' in marks: acute[w] += 1; ex.setdefault(w, f'{l.work}. {l.book}.{l.line}')
        elif '͂' in marks: circ[w] += 1
print('acute on long penult (η/ω) + C + ος: types', len(acute), 'tokens', sum(acute.values()))
for w, n in acute.most_common(20): print('  ', U.normalize('NFC', w), n, ex[w])
print('circumflex on penult (η/ω) + C + ος: types', len(circ), 'tokens', sum(circ.values()))
print('   e.g.', ', '.join(U.normalize('NFC', w) for w, _ in circ.most_common(12)))
```

### B.5 aspir.py (elision before rough breathing)

```python
# Elided τ/π/κ before a word with rough breathing (Homer writes θʼ/φʼ/χʼ there).
# Counts in Homer for αὖτʼ vs αὖθʼ before rough vs smooth breathing, and checks a draft file.
import sys, re, unicodedata as U, collections
sys.path.insert(0, sys.argv[1] + '/homer')
from concordance import Concordance
APOS = "ʼ'’᾽"
def rough(w):
    d = U.normalize('NFD', w)
    for ch in d:
        if ch == '̔': return True
        if ch == '̓': return False
        if U.category(ch).startswith('L') and ch.lower() not in 'αεηιουωρ': return None
    return None
def pairs(text):
    ws = text.split()
    for a, b in zip(ws, ws[1:]):
        if a and a[-1] in APOS: yield a, b
c = Concordance(); cnt = collections.Counter(); ex = {}
for l in c.lines:
    for a, b in pairs(l.text):
        base = a[:-1]
        if base in ('αὖτ', 'αὖθ'):
            r = rough(b); k = (base, 'rough' if r else ('smooth' if r is False else 'other'))
            cnt[k] += 1; ex.setdefault(k, f'{l.work}. {l.book}.{l.line} {l.text}')
        last = base[-1:] if base else ''
        if last in 'τπκ' and rough(b): cnt[('τ/π/κ elided', 'rough')] += 1; ex.setdefault(('τ/π/κ elided','rough'), f'{l.work}. {l.book}.{l.line} {l.text}')
print('Homer:')
for k in sorted(cnt): print(' ', k, cnt[k], '| e.g.', ex[k])
print('Draft', sys.argv[2], ':')
for i, line in enumerate(open(sys.argv[2], encoding='utf-8'), 1):
    for a, b in pairs(line):
        base = a[:-1]
        if base[-1:] in 'τπκθφχ' and rough(b) is not None:
            print(f'  {i}: {a} {b}  next word {"rough" if rough(b) else "smooth"}  -> {"ERROR" if (base[-1] in "τπκ") == bool(rough(b)) and rough(b) else "ok"}')
```

### B.6 rulings.py (R2-R6 forms, prohibited words)

```python
# Ruling and lexicon checks on a draft: R2-R6 forms and the brief's prohibited words (loose forms, homer/greek.py)
import sys, re
sys.path.insert(0, sys.argv[1] + '/homer')
import greek as G
lines = [l.rstrip('\n') for l in open(sys.argv[2], encoding='utf-8')]
def words(l): return [G.loose(w) for w in re.findall(r"[^\s,.·;:!]+", l)]
checks = {
 'R4 δίς': lambda w: w == 'δισ',
 'R5 ἐξεναρίζω': lambda w: w.startswith('εξεναρ'),
 'R6 πάλιν': lambda w: w == 'παλιν',
 'R2 ἰσόθεος': lambda w: w.startswith('ισοθε'),
 'R3 withdrawn Ζοκοβίδης/Νοβάκος': lambda w: w.startswith('ζοκοβιδ') or w.startswith('νοβακ'),
 'Ζοκοβείδης': lambda w: w.startswith('ζοκοβειδ'),
 'Νοβήκος': lambda w: w.startswith('νοβηκ'),
 'δαμάζω (aor.)': lambda w: re.match(r'ε?δαμασ', w) is not None,
 'prohibited (γραμμ, στεγ, οχλ, ωρη/ωρα, δικτυ, ραβδ, χλο, χορτ, δικαστ, αθλητησ, σφαιριστ, ηττ)':
     lambda w: re.match(r'(γραμμ|στεγ|οχλ|ωρη|ωρα|ωρ$|δικτυ|ραβδ|χλο[ηυ]|χορτ|δικαστ|αθλητη[σν]|σφαιριστ|ηττ)', w) is not None,
}
for name, f in checks.items():
    hits = [(i, w) for i, l in enumerate(lines, 1) for w in words(l) if f(w)]
    print(f'{name}: {len(hits)}', hits)
```

### B.7 simile.py (simile openers and apodoses in the draft)

```python
# Similes in a draft: lines with ὡς δʼ ὅτε/ὅτʼ, ἠΰτε, or a comparison 'λέων ὣς'-type ὥς/ὣς after a noun,
# and the first later line opening with ὣς/ὥς/τώς (apodosis) within 14 lines.
import sys, re
sys.path.insert(0, sys.argv[1] + '/homer')
import greek as G
L = [l.strip() for l in open(sys.argv[2], encoding='utf-8')]
for i, l in enumerate(L):
    lw = [G.loose(w) for w in re.findall(r"[^\s,.·;:!]+", l)]
    opener = (lw[:3] in (['ωσ', 'δ᾽', 'οτε'], ['ωσ', 'δ᾽', 'οτ᾽']) or lw[:3] == ['ωσ', "δʼ", 'οτε'] or
              re.match(r'^ὡς δ[᾽ʼ] ὅτ', l) is not None or 'ηυτε' in lw or re.search(r'\w+ ὣς[,.·;]?$', l) is not None)
    if not opener: continue
    apod = next((j for j in range(i + 1, min(len(L), i + 15)) if re.match(r'^(ὣς|ὥς|τώς)\b', L[j])), None)
    print(f'simile opener at {i+1}: {l}')
    print(f'   apodosis line: {apod+1 if apod is not None else None}: {L[apod] if apod is not None else "-"}; vehicle lines {i+1}-{apod if apod is not None else "?"} ({(apod - i) if apod is not None else "?"} lines)')
```

### B.8 verbatim.py, q.sh, lsj_text.py

```python
# For each draft line: whole-line ngram hits in Homer (loose word comparison).
import sys, re
sys.path.insert(0, sys.argv[1] + '/homer')
from concordance import Concordance
c = Concordance()
for i, l in enumerate(open(sys.argv[2], encoding='utf-8'), 1):
    q = re.sub(r'[,.·;:!]', ' ', l.strip()); q = ' '.join(q.split())
    hits = c.ngram(q)
    full = [h for h in hits if len(re.sub(r'[,.·;:!]', ' ', h.text).split()) == len(q.split())]
    if full: print(f'{i}\t' + ', '.join(h.citation for h in full))
```

```bash
#!/bin/bash
# usage: q.sh TAG args...   -> prints "# [TAG] python homer/concordance.py args" then output
tag=$1; shift
printf '# [%s] python homer/concordance.py' "$tag"
for a in "$@"; do if [[ "$a" == --* ]]; then printf ' %s' "$a"; else printf ' "%s"' "$a"; fi; done
echo
python homer/concordance.py "$@"
echo
```

```python
import json, sys, re, html
d = json.load(open(sys.argv[1], encoding='utf-8'))
for dic in d['detail']['dicos']:
    if dic['dname'] == 'LSJ':
        for e in dic['es']:
            t = re.sub(r'<[^>]+>', ' ', e); t = html.unescape(t); t = re.sub(r'\s+', ' ', t)
            print(t[:int(sys.argv[2]) if len(sys.argv) > 2 else 3000])
```

### B.9 tally.py (counts in §2 and §5)

```python
# python3 tally.py review/philology_v2.md   (prints the counts in §2 and §5)
import re, sys, collections
rows = []; inside = False
for line in open(sys.argv[1], encoding='utf-8'):
    if line.startswith('## '): inside = line.startswith('## 7.')
    if not inside or not re.match(r'^\| \d+ \|', line): continue
    cells = [c.strip() for c in re.split(r'(?<!\\)\|', line.strip())[1:-1]]
    comp, rev = [x.strip() for x in cells[-1].split('→')]
    rows.append((int(cells[0]), cells[1], comp, rev))
assert [r[0] for r in rows] == list(range(1, len(rows) + 1))
N = len(rows); v = collections.Counter(r[1] for r in rows)
print('lines', N); print('verdicts', dict(v))
for k in ('FAIL', 'QUERY'): print(k, [r[0] for r in rows if r[1] == k])
for who, i in (('composer', 2), ('reviewer', 3)):
    c = collections.Counter(r[i] for r in rows)
    print(who, {t: f"{c[t]} ({100*c[t]/N:.1f}%)" for t in ('none', 'unperiodic', 'necessary')})
    print('  necessary lines', [r[0] for r in rows if r[i] == 'necessary'])
print('disagreements', [(r[0], r[2], r[3]) for r in rows if r[2] != r[3]])
```
