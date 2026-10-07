# Philology review of draft v3 (60 verses)

Reviewed: `composition/drafts/v3.txt`, with glosses, facts, sources and enjambment labels from `composition/drafts/v3.jsonl`. Checked against `review/round_2.md` (rulings R9-R12), `composition/brief.md` (§1 facts, §4 names, §5 constraints, Addenda A1-A2) and my v2 report (`review/philology_v2.md`). Reviewer: philologist agent, 2026-10-07. The scansion and provenance verifiers are separate; points for them and for the composer are in §5.

## 1. Method and sources

* **Homeric evidence.** Every Homeric claim comes from `python homer/concordance.py` (Perseus: Monro-Allen Iliad, Murray Odyssey; homer/README.md), or from small scripts that call its `Concordance` class (Appendix B). Each judgement in §6 names its query; the verbatim outputs are in Appendix A. Positions in square brackets use the half-foot numbering of homer/README.md. `check_line.py --file` was run on the whole draft: 60/60 pass with no flags (A.0).
* **Unchanged verses.** `identity.py` (B.1) compared every v3 verse character by character with the v2 verse named in its `v2_line` field, and checked that v3.txt equals the jsonl text.
  * 53 verses are identical to v2, and 7 changed: 23, 33, 36, 44, 51, 55, 56. This is the list in the brief for this round, and the jsonl `changed` flag agrees on every line.
  * 52 of the identical verses were v2 PASS lines. Each is reported in one row as "Unchanged, v2 PASS". For the neighbours of the changed lines (22, 24, 32, 34, 35, 38, 43, 45, 50, 52, 54, 57) I re-read the passage and record the continuity check in the same row.
  * The 53rd identical verse is 37, a v2 QUERY. Its predecessor changed, so it is reviewed in full.
* **Lexica.** I fetched these entries on 2026-10-07 from the Logeion API (`anastrophe.uchicago.edu/logeion-api/detail?w=…`), which returns both LSJ and Cunliffe's *Lexicon of the Homeric Dialect* ("Cunliffe Homer"):
  * ἐκφέρω, ἕπομαι, αὖθις (LSJ) / αὖτις (Cunliffe), βάλλω and ἔπειτα;
  * excerpts are quoted in A.7.

  Anything else is marked [unverified].
* **Enjambment.** I used the same criteria as in v1 and v2: Parry 1929 as quoted by Dukat 1991 (*Oral Tradition* 6/2-3, 303-315; fetched for v1, quoted in philology_v1.md A.7), with Kirk's punctuation test as Dukat tabulates it:
  * a printed strong stop is **none**;
  * a complete sentence continued after a comma, or with no punctuation, is **unperiodic**;
  * an incomplete sentence is **necessary**, including any verse inside an open ὡς δ᾽ ὅτε period before its apodosis.

  Parry's own text was not accessed [unverified at first hand].
* **Verdicts.**
  * **PASS** means no philological defect; notes may still apply.
  * **FAIL** means a defect in morphology, orthography, prosody or syntax, or a mismatch between the Greek and its gloss or the facts, shown by the evidence.
  * **QUERY** means a human decision is needed.
* **Reproducibility.** The counts in §2 and §4 were printed by `tally.py` (B.9), run on the table in §6. Appendix A was written by `appendix.sh` (B.10).

## 2. Summary

**Verdicts (60 lines): PASS 60, FAIL 0, QUERY 0.** All three v2 FAILs (44, 55, 56) and both v2 QUERYs (33, 37) are resolved. Poem-level query P1 is closed by R10.

**The questions in the brief for this round**

| question | answer | evidence |
|---|---|---|
| Do 33 and 55 now count two aces and two winners? | **Yes.** Each verse has two hit clauses with one subject: καὶ βάλεν, οὐδ᾽ ἀφάμαρτε (Il. 11.350, 13.160) + καὶ βάλεν αὖτις. In Homeric usage βάλλω with its target understood is "hit", opposed to missing (LSJ, quoting τὸν βάλεν, οὐδ᾽ ἀφάμαρτε, Il. 11.350; Cunliffe "strike or wound with a missile"). αὖτις is "again, once more" (Cunliffe 3). A repeated cast with αὖτις is Od. 22.272. So 33 = points 357 and 358, and 55 = points 420 and 421. | A.2, A.7 |
| Does 44's ὃ δ᾽ ἕσπετο mark the change of subject and keep κέρδεα εἰδώς with Federer? | **Yes.** ὃ δ᾽ introduces the other man, and κέρδεα εἰδώς stands in apposition to ὃ. Homeric models: ἡγεῖθ᾽, ἡ δ᾽ ἕσπετο Παλλὰς Ἀθήνη (Od. 1.125); ὃ μὲν ἦρχ᾽, ὃ δ᾽ ἅμ᾽ ἕσπετο ἰσόθεος φώς (Il. 11.472 = 15.559 = 16.632); φεῦγ᾽, ὃ δ᾽ ὄπισθε ῥέων ἕπετο, of a pursuer (Il. 21.256); ἔκφερον … τὰς δὲ μετ᾽ ἐξέφερον (Il. 23.376-377). Note: ὃ δ᾽ ἕσπετο itself has 0 hits, and the aorist ἕσπετο always means "accompany" (12/12); see 44. | A.4, A.7 |
| R12: who rushes on at τὸ τέταρτον in 37? | **Federer, fixed before the formula.** 36 names him as the subject of the count, τρὶς μὲν ἔπειτ᾽ ἐπόρουσε βοὴν ἀγαθὸς Φεδερῆρος. That is the Homeric order: the subject of the τρὶς μέν line is the subject of ἐπέσσυτο in Il. 5.436→438, 16.784→786 and 20.445→447. 38 then switches to Σέρβος, named, with an apodotic δ᾽. The "fourth" now has its three, if CP1 (34-35) is counted as the first of them. Cunliffe classes the ἔπειτα of this formula as "resuming and restating", which supports that count; see 36. | A.3, A.7 |
| Does Ζοκοβεύς still refer to Djokovic anywhere? | **No.** Ζοκοβεύς / Ζοκοβῆ- occur 0 times. Djokovic is named by Ζοκοβείδης (4, 23, 53, 56), Σέρβος / -ον / -ου (10, 15, 29, 38, 43, 51, 58) and Νοβῆκος (44, 55). The eponym is never named. A patronymic standing far from its father's name is Homeric: Ἀμαρυγκεΐδης / Ἀμαρυγκείδην (Il. 2.622, 4.517), while the father Ἀμαρυγκεύς appears only at Il. 23.630. | A.0 (rulings), A.6 |
| Morphology of Νοβῆκος, Σέρβου κρατεροῖο, Ζοκοβείδης | **All sound.** Νοβῆκος (44, 55) is circumflexed per R9: Homer has 51 types in η/ω + one consonant + -ος, all circumflexed, and 0 with the acute. Σέρβου κρατεροῖο mixes a second-declension -ου with an epithet in -οιο, as Μενελάου κυδαλίμοιο, Ἀγαστρόφου ἰφθίμοιο (Il. 11.373) and Ἀρκεισίου ἀντιθέοιο (Od. 14.182). The gen. + κρατεροῖο close is that of Πολυποίταο κρατεροῖο (Il. 23.848). Ζοκοβείδης (23) has the diphthongal -είδης of Ἀμαρυγκείδην (Il. 4.517) and Ἀτρείδης (Od. 15.52), as verified in v2, and stands in the κρατερὸς Διομήδης slot (Il. 5.143). | A.0, A.1, A.5 |

**Rulings applied (whole draft; A.0)**

| ruling | status in v3 | evidence |
|---|---|---|
| R2 Ῥογῆρος not before ἰσόθεος φώς | applied: ἰσόθε- 0; Ῥογῆρος stands before κ in 27 and 33 | rulings.py |
| R3 withdrawn Ζοκοβίδης / Νοβάκος | applied: 0 | rulings.py |
| R4 no δίς + verb | applied: δίς 0 | rulings.py |
| R5 ἐξεναρίζω | applied: 0. δαμάζω is used for breaks and sets (20, 24, 29, 30, 34, 58; 40 is Homer verbatim) | rulings.py |
| R6 πάλιν only "back" | applied: only 22 | rulings.py |
| R9 Νοβῆκος | applied: Νοβῆκος 2 (44, 55), Νοβήκος 0 | rulings.py; accent.py |
| R10 Ζοκοβεύς = the eponym only | applied: 0 Ζοκοβεύς / Ζοκοβῆ-. 23 → κρατερὸς Ζοκοβείδης, 44 → Νοβῆκος, 51 → Σέρβου κρατεροῖο | rulings.py |
| R11 counts match the facts | applied: δεύτερον αὖτις survives only in 24, where it counts the two set-4 breaks (v2 PASS). 33 and 55 have two hit clauses each. The τρίς of 36 counts points 359-361 (see 36) | rulings.py; A.2, A.3 |
| R12 attacker fixed before τὸ τέταρτον | applied: in both τὸ τέταρτον verses (15, 37) Federer is the named subject of the verse before | rulings.py (last line); A.3 |
| aspiration (v2 FAIL 56) | applied: no elided τ/π/κ stands before a rough breathing anywhere in the draft | aspir.py |
| similes need ≥3 lines and an apodosis | unchanged: horse 16-18 → 19; lion 38-42 → 43; racing horses 45-47 → 48 | simile.py |
| no prohibited words | 0 | rulings.py |

**Dialect and morphology, in brief.**
* The base is Ionic-epic throughout.
* The new forms are Homeric or have Homeric analogues:
  * λάβ᾽ (unaugmented, elided before ἄεθλον as in Il. 23.511);
  * ἔκφερε (unaugmented and unelided; ἔκφερ᾽ 3x, ἔκφερεν Od. 15.470);
  * ἕσπετο;
  * the genitives Σέρβου and κρατεροῖο;
  * Νοβῆκος.
* No Attic forms.
* Orthography: all lines are NFC, every elision is written ᾽ (U+1FBD, 57x), and every elision before a rough breathing is aspirated.

**Lexicon.**
* No prohibited or post-Homeric word occurs except the sanctioned name renderings (Σέρβος, Ἑλβέτιος, Νοβῆκος, Ζοκοβείδης, Ῥογῆρος, Φεδερῆρος, Φεδερεύς).
* The words newly used in tennis senses are both lexicon-backed:
  * ἐκφέρω "shoot ahead, take the lead" (44), Cunliffe ἐκφέρω 6 "to draw away from competitors in a race, shoot ahead", Il. 23.376, 377, 759;
  * ἕπομαι "follow (level)" (44), close to LSJ ἕπομαι I.4 "keep pace with".
* Epithet economy holds:
  * κρατερός is Djokovic's (23, 51, 53);
  * βοὴν ἀγαθός and κέρδεα εἰδώς are Federer's (27, 44);
  * ἀντίθεος (Djokovic) now appears only in the proem (4).

**Enjambment (whole poem; §4).** None 31 (51.7%), unperiodic 19 (31.7%), necessary 10 (16.7%). Composer and reviewer agree on all 60 lines. None of the rewritten verses added necessary enjambment. The composer records the shortfall in the jsonl notes of 33, 44 and 55, as the round-2 plan note allows.

## 3. Notes on the changed passages

* **22-24 (set 3).** Line 22 still ends with a comma before the asyndetic δεύτερον αὖ of 23 (as Il. 6.184), and τόν in 24 now refers to Ζοκοβείδης.
  * Il. 23.511 (ἴφθιμος Σθένελος, ἀλλ᾽ ἐσσυμένως λάβ᾽ ἄεθλον) attaches the speed adverb to the victor's side taking the prize.
  * So ἄφαρ λάβ᾽ ἄεθλον in 23 reads "took the prize at once" and no longer suggests that the 48-minute set was quick. My v2 "colour, not fact" note lapses.
* **32-38 (the championship game).** The sequence is now:
  * 32: break to 8-7;
  * 33: two aces (357-358);
  * 34-35: CP1 (359) as a past unreal;
  * 36: τρίς = 359-361, Federer named;
  * 37: the fourth (362);
  * 38: the Serb, named, rises like a lion.

  The count depends on CP1 being one of the three. Cunliffe (ἔπειτα 4) lists exactly this formula, τρὶς μὲν ἔπειτ᾽ ἐπόρουσε (Il. 5.436, 20.445), as ἔπειτα "resuming and restating" an onset already narrated (5.432, 20.442; also 16.783 ἐνόρουσε). I accept that reading.

  The residual difference is that each Homeric precedent states the resumed onset with ἐπ- or ἐνόρουσε, whereas 34-35 has no verb of attack. A reader who takes ἔπειτα as "thereafter" (Cunliffe 1) would put "the fourth" one point late. This is a note, not a query.

  Federer is named in 32, 33, 34 and 36, and βοὴν ἀγαθὸς Φεδερῆρος closes both 34 and 36. A full name-epithet formula repeated two verses apart has one Homeric parallel (Od. 8.2/8.4, ἱερὸν μένος Ἀλκινόοιο), and the two-word tail has eight (e.g. Il. 20.386/388 δῖος Ἀχιλλεύς). This is a stylistic point, not a fault.
* **43-45.** Σέρβον (43) and Νοβῆκος (44) are the same man. 44 is end-stopped before the verbatim simile opener 45.
* **50-52.** τὴν μὲν … τὴν δ᾽ αὖ refers to the dual κῆρε of 50. 52 follows as Il. 22.212.
* **54-57.** Federer is the subject of 54. 55 names Νοβῆκος within the verse. 56 names both men. 57 continues with δ᾽ ἄρα.

## 4. Enjambment

Counts from tally.py (B.9), out of 60 lines:

| | none | unperiodic | necessary |
|---|---|---|---|
| composer (v3 jsonl) | 31 (51.7%) | 19 (31.7%) | 10 (16.7%) |
| reviewer | 31 (51.7%) | 19 (31.7%) | 10 (16.7%) |
| v2 (composer = reviewer) | 32 (53.3%) | 18 (30.0%) | 10 (16.7%) |
| Parry's Iliad sample (Dukat 1991:305, from Parry 1929:204) | 48.5% | 24.8% | 26.6% |

* The only change of label is 36:
  * v2 36 (στῆ δὲ μάλ᾽ ἐγγὺς ἰών, βάλε δὲ κρατερὸς Ζοκοβείδης.) ended with a full stop, so it was none;
  * v3 36 is the τρὶς μέν clause, complete and continued by ἀλλ᾽ ὅτε δή, so it is unperiodic, like 14 and 53 and like Il. 5.436, 16.784 and 20.445.
* The other rewritten lines keep their v2 labels: 23, 33, 44, 55 none; 51, 56 unperiodic.
* The necessary lines are still 1, 3, 16, 17, 18, 37, 39, 45, 46 and 47: the proem's period and three similes. In the duel narrative only 37 is necessary.
* The brief's target of "roughly a third" (§2.7) is not met, and §2.7's wish for the championship game and the rallies to run on is met only by 36 → 37 → 38. This is a shortfall for the paper; it is not a line-level fault.

## 5. Points for the composer and the other verifiers (not philological verdicts)

* **jsonl 51 notes: the claim that Ζοκοβείδαο "cannot stand in any slot of a hexameter" is false.**
  * `τοῦ Ζοκοβείδαο κρατεροῦ μένος ἀντιθέοιο` passes check_line (DSDDDS, tier 0, no flags; A.5): the genitive stands at 1.5-5 when its -ο is lengthened by a following double consonant.
  * Such a slot has no Homeric parallel in Πηλεΐδαο, whose -ο is short in all 5 instances (A.5).
  * The choice of Σέρβου κρατεροῖο is unaffected. The note should say "in the slots tested".
* **jsonl 33, 55: the αὖτις models.**
  * The cited verse-final models are Il. 15.29 (ἀνήγαγον αὖτις), 6.367 (ἵξομαι αὖτις) and 18.59 (ὑποδέξομαι αὖτις), which are "back (again)" (Cunliffe αὖτις 1).
  * The sense used is "again, once more" (Cunliffe 3: Il. 1.513, Od. 9.360 αὖτις οἱ πόρον οἶνον).
  * The closest Homeric model is a repeated cast with αὖτις: Od. 22.272 (αὖτις δὲ μνηστῆρες ἀκόντισαν ὀξέα δοῦρα).
  * Record that no Homeric verse joins a βάλλω form to αὖτις (0) or repeats βάλλω in two co-ordinate clauses (0).
* **jsonl 36:**
  * add Il. 5.432 (Αἰνείᾳ δ᾽ ἐπόρουσε βοὴν ἀγαθὸς Διομήδης: the same name-epithet + ἐπόρουσε, four lines before the count);
  * add Cunliffe ἔπειτα 4 ("resuming and restating", Il. 5.436, 20.445) as the basis for counting CP1 inside τρίς;
  * add Il. 13.20 (τρὶς μὲν … τὸ δὲ τέτρατον) for τρὶς μέν without a τρὶς δέ member (the other 14 Homeric τρὶς μέν lines have one).
* **jsonl 44:**
  * ὃ δ᾽ ἕσπετο has 0 hits; say so in `sources`;
  * add Il. 21.256 (φεῦγ᾽, ὃ δ᾽ ὄπισθε ῥέων ἕπετο: a pursuer marked by ὃ δ᾽), Il. 23.376-377 (ἔκφερον … τὰς δὲ μετ᾽ ἐξέφερον) and Cunliffe ἐκφέρω 6;
  * Od. 2.203 χρήματα δ᾽ αὖτε is the closest model for a dactylic first word + δ᾽ αὖτε at 3-3.5.
* **jsonl 23:** cite Il. 23.511 ἐσσυμένως λάβ᾽ ἄεθλον for the speed adverb with the prize verb (§3), and Il. 16.322-323 / 11.418 for ἄφαρ after its verb.
* **Punctuation of 33 and 55.**
  * 33 reads καὶ βάλεν, οὐδ᾽ ἀφάμαρτε, Ῥογῆρος, as in Il. 13.160, which has a comma after ἀφάμαρτε;
  * 55 reads καὶ βάλεν, οὐδ᾽ ἀφάμαρτε Νοβῆκος, as in Il. 11.350, which has none.
  * Both are Homeric; harmonise them for the printed text if wanted.
* **FOR_HUMAN.md.** The entry "Greek renderings of 'Djokovic'" still says "Σέρβος and Ζοκοβεύς are unchanged". After R10, Ζοκοβεύς no longer occurs in the poem; the later entry on Ζοκοβεύς vs Ζοκοβείδης is current.
* **For the scansion verifier.** Among the changed lines, check_line warns quantity_unattested only on κέρδεα (44; the α is short by the accent rule, inside the verbatim Il. 23.709 wording, as in 27) and on Ἑλβέτι- (51, 56; metre only, brief §4.1). These are the same words and warnings as in v2.

## 6. Per-line table

Queries are written as their concordance.py arguments. "ctx" means the context script (B.2), and "identity" means B.1. Tags in square brackets ([23a] …) point to Appendix A.

| n | verdict | findings (morphology, dialect, syntax, lexicon, sense, idiom, rulings, facts) | evidence: query → hits | enjambment: composer → reviewer |
|---|---|---|---|---|
| 1 | PASS | Unchanged, v2 PASS (= v2 1). | identity → 1=1 | necessary → necessary |
| 2 | PASS | Unchanged, v2 PASS (= v2 2). | identity → 2=2 | unperiodic → unperiodic |
| 3 | PASS | Unchanged, v2 PASS (= v2 3). | identity → 3=3 | necessary → necessary |
| 4 | PASS | Unchanged, v2 PASS (= v2 4). | identity → 4=4 | none → none |
| 5 | PASS | Unchanged, v2 PASS (= v2 5). | identity → 5=5 | none → none |
| 6 | PASS | Unchanged, v2 PASS (= v2 6). | identity → 6=6 | unperiodic → unperiodic |
| 7 | PASS | Unchanged, v2 PASS (= v2 7). | identity → 7=7 | unperiodic → unperiodic |
| 8 | PASS | Unchanged, v2 PASS (= v2 8). | identity → 8=8 | unperiodic → unperiodic |
| 9 | PASS | Unchanged, v2 PASS (= v2 9). | identity → 9=9 | none → none |
| 10 | PASS | Unchanged, v2 PASS (= v2 10). | identity → 10=10 | none → none |
| 11 | PASS | Unchanged, v2 PASS (= v2 11). | identity → 11=11 | none → none |
| 12 | PASS | Unchanged, v2 PASS (= v2 12). | identity → 12=12 | none → none |
| 13 | PASS | Unchanged, v2 PASS (= v2 13). | identity → 13=13 | none → none |
| 14 | PASS | Unchanged, v2 PASS (= v2 14). | identity → 14=14 | unperiodic → unperiodic |
| 15 | PASS | Unchanged, v2 PASS (= v2 15). | identity → 15=15 | none → none |
| 16 | PASS | Unchanged, v2 PASS (= v2 16). | identity → 16=16 | necessary → necessary |
| 17 | PASS | Unchanged, v2 PASS (= v2 17). | identity → 17=17 | necessary → necessary |
| 18 | PASS | Unchanged, v2 PASS (= v2 18). | identity → 18=18 | necessary → necessary |
| 19 | PASS | Unchanged, v2 PASS (= v2 19). | identity → 19=19 | none → none |
| 20 | PASS | Unchanged, v2 PASS (= v2 20). | identity → 20=20 | none → none |
| 21 | PASS | Unchanged, v2 PASS (= v2 21). | identity → 21=21 | none → none |
| 22 | PASS | Unchanged, v2 PASS (= v2 22). Neighbour of 23: it still ends with a comma before the asyndetic δεύτερον αὖ of 23, so the label is unchanged. | identity → 22=22 | unperiodic → unperiodic |
| 23 | PASS | **R10 applied.** Ζοκοβεύς is replaced by κρατερὸς Ζοκοβείδης in the Διομήδης slot 7.5-12, after a word ending at 7, as μίγη κρατερὸς Διομήδης (Il. 5.143); κρατερὸς Διομήδης occurs 20x. **Morphology.** λάβ᾽ is the unaugmented aorist, elided before ἄεθλον as in Il. 23.511. ἄεθλον stands at 4-5.5, with ε long by position before θλ, as in Il. 23.892, Od. 21.91 and 23.261 (3 of 27 hits). **Syntax and idiom.** Line-initial δεύτερον αὖ with no connective follows Il. 6.184. ἄφαρ is at 6-7, its commonest slot (15 of 34). It follows its verb and object, as in Il. 16.322-323 (… οὐδ᾽ ἀφάμαρτεν, / ὦμον ἄφαρ) and 11.418 (μένουσιν ἄφαρ). **Sense.** In Il. 23.511 (ἀλλ᾽ ἐσσυμένως λάβ᾽ ἄεθλον) the speed adverb goes with taking the prize, so ἄφαρ λάβ᾽ ἄεθλον means "took the prize at once". The line therefore no longer implies that the 48-minute set was quick, and my v2 note lapses. The gloss is right. **Facts.** Set 3 went to Djokovic (tie-break 7-4 at 2:15:24); it is his second set after line 15 ✓. **Continuity.** Line 22 still ends with a comma before an asyndetic δεύτερον αὖ, and τόν in 24 now refers to Ζοκοβείδης. | [23a] --ngram "δεύτερον αὖ" → 5, all 1-3; [23b] --ngram "λάβ᾽ ἄεθλον" → Il. 23.511 [9.5-12] + ctx; [23c] --ngram "κρατερὸς Διομήδης" --count → 20; [23d] → Il. 5.143 [6-12]; [23e] --loose "αφαρ" --word → 34 (15 at 6-7, 16 at 2-3) + ctx Il. 16.322-323, 11.416-418; [23f] --loose "αεθλον" --word → 27 (3 at 4-5.5) | none → none |
| 24 | PASS | Unchanged, v2 PASS (= v2 24). Neighbour of 23: τόν now refers to Ζοκοβείδης, the last word of 23; the sense is unchanged. | identity → 24=24 | none → none |
| 25 | PASS | Unchanged, v2 PASS (= v2 25). | identity → 25=25 | none → none |
| 26 | PASS | Unchanged, v2 PASS (= v2 26). | identity → 26=26 | unperiodic → unperiodic |
| 27 | PASS | Unchanged, v2 PASS (= v2 27). | identity → 27=27 | none → none |
| 28 | PASS | Unchanged, v2 PASS (= v2 28). | identity → 28=28 | none → none |
| 29 | PASS | Unchanged, v2 PASS (= v2 29). | identity → 29=29 | unperiodic → unperiodic |
| 30 | PASS | Unchanged, v2 PASS (= v2 30). | identity → 30=30 | none → none |
| 31 | PASS | Unchanged, v2 PASS (= v2 31). | identity → 31=31 | none → none |
| 32 | PASS | Unchanged, v2 PASS (= v2 32). Neighbour of 33: Federer is the subject, and 33 names him again (Ῥογῆρος). | identity → 32=32 | none → none |
| 33 | PASS | **R11 applied: the line counts two hits.** It has two co-ordinate clauses with one subject. Ace 1 (point 357) is καὶ βάλεν, οὐδ᾽ ἀφάμαρτε, as in Il. 11.350 and 13.160 (1-5.5); ace 2 (point 358) is καὶ βάλεν αὖτις. **Lexicon.** With its target understood, βάλλω means "throw so as to hit, hit with a missile" (LSJ, quoting τὸν βάλεν, οὐδ᾽ ἀφάμαρτε, Il. 11.350; Cunliffe: "to strike or wound … with a missile"). So the second clause states a second hit, not merely a second throw. Cunliffe's absolute "let fly" (Il. 3.82) is the weaker reading, and the parallel first clause rules it out. αὖτις means "again, once more" (Cunliffe αὖτις 3: Il. 1.513, Od. 9.360; LSJ αὖθις II). A repeated cast with αὖτις is Od. 22.272 (αὖτις δὲ μνηστῆρες ἀκόντισαν ὀξέα δοῦρα). **Departures from Homer.** In Homer καὶ βάλεν stands only at 1-2 (11x); here it also stands at 9-10, a mobility. No Homeric verse joins a βάλλω form to αὖτις (0 hits), and none repeats βάλλω in two co-ordinate clauses (0 hits); the pieces are attested, the combination is not. **Name slot.** Ῥογῆρος is at 6-8 after a vowel and before καί, so it is long by position (R2 ✓). **Sense and facts.** The gloss is right. Points 357-358 took the score from 15-15 to 15-40 ✓. The v2 misreading of δεύτερον αὖτις is gone. **Note.** The jsonl's models for verse-final αὖτις mean "back (again)" (Cunliffe 1); see §5. | [33a] --ngram "καὶ βάλεν οὐδ᾽ ἀφάμαρτε" → Il. 11.350, 13.160 [1-5.5]; [33b] → 4; [33c] --ngram "καὶ βάλεν" → 11, all [1-2]; [33d] --ngram "βάλεν αὖτις" → 0; [33e] regex βαλ-/οὐτα-/νυξ-/τυψ- + αὖτις → 0; [33h] regex βάλλω … καὶ/δέ βάλλω in one verse → 0; [33g] --loose "αυτις" --word → 128 (20 at 11-12) and Od. 22.272; LSJ βάλλω, αὖθις; Cunliffe βάλλω, αὖτις (A.7) | none → none |
| 34 | PASS | Unchanged, v2 PASS (= v2 34). Neighbour of 33 and 36: the object (Djokovic) is understood. Its closing βοὴν ἀγαθὸς Φεδερῆρος recurs at the end of 36 (see 36). CP1 here is the first of the three onsets counted in 36. | identity → 34=34 | unperiodic → unperiodic |
| 35 | PASS | Unchanged, v2 PASS (= v2 35). Neighbour of 36: οἱ is Federer, and βέλος is the subject. 36 names Federer again, so there is no ambiguity. | identity → 35=35 | none → none |
| 36 | PASS | **R12 met.** The count line names the attacker: τρὶς μὲν ἔπειτ᾽ ἐπόρουσε (Il. 5.436, 16.784, 20.445, all 1-5.5) plus βοὴν ἀγαθὸς Φεδερῆρος at 6-12, the Διομήδης formula. The same epithet and verb occur in Il. 5.432 (Αἰνείᾳ δ᾽ ἐπόρουσε βοὴν ἀγαθὸς Διομήδης), the onset that 5.436 resumes. So the unexpressed subject of ἐπέσσυτο in 37 is Federer, as in all three Homeric sequences. **τρὶς μέν without τρὶς δέ.** Il. 13.20 (τρὶς μὲν ὀρέξατ᾽ ἰών, τὸ δὲ τέτρατον …) and the poem's own 14-15 do the same. The other 14 Homeric τρὶς μέν lines have a τρὶς δ(έ) member. **Count.** The jsonl takes τρίς as points 359-361, with CP1 (359) also narrated in 34-35, and the fourth as 362. Cunliffe classes the ἔπειτα of this very formula (Il. 5.436, 20.445) as "resuming and restating" an onset already told (5.432 and 20.442; 16.783 ἐνόρουσε), so τρίς may include CP1 ✓. The caveat: each Homeric case states the resumed onset with ἐπ- or ἐνόρουσε, while 34-35 has no verb of attack. A reader who takes ἔπειτα as "thereafter" (Cunliffe 1) would count CP1 plus three and place "the fourth" one point late. I judge the Homeric reading sufficient (§3). **Note.** βοὴν ἀγαθὸς Φεδερῆρος also closes 34. The same three-word name formula two verses apart has 1 Homeric parallel (Od. 8.2/8.4), and the two-word tail has 8 (e.g. Il. 20.386/388). **Facts.** Points 359-361 were all lost by Federer on his serve ✓. The CP2 passing shot is no longer narrated, but its fact is kept in the jsonl. The gloss is right. | [36b] --ngram "τρὶς μὲν ἔπειτ᾽ ἐπόρουσε" → Il. 5.436, 16.784, 20.445 [1-5.5]; [36a] --ngram "ἐπόρουσε βοὴν ἀγαθὸς Διομήδης" → Il. 5.432; ctx -4/+3 on the three; ctx "ἀλλ᾽ ὅτε δὴ τὸ τέταρτον" → 5; [36c] trismen.py → 15 τρὶς μέν lines, 1 without τρὶς δ (Il. 13.20); [36d/e] repname.py → 1 / 8 pairs; Cunliffe ἔπειτα 4 (A.7) | unperiodic → unperiodic |
| 37 | PASS | **The text is unchanged, but this was a v2 QUERY, so it is reviewed in full. R12 met.** The subject of ἐπέσσυτο is the named subject of 36 (Federer), with nothing in between, as in Il. 5.436→438, 16.784→786 and 20.445→447. In Homer a τρὶς δ(έ) verse intervenes each time, and Il. 5.437 and 16.703 change the subject there. Line 38 switches to the named Σέρβος with an apodotic δ᾽ (Il. 5.439 δεινὰ δ᾽ ὁμοκλήσας …). **Count.** "The fourth" now has its three (36), and 362 (the break to 8-8) is the fourth point on the reading of 36. **Idiom.** As in Homer, the fourth onset of the man δαίμονι ἶσος is the one that is stopped. | ctx "ἀλλ᾽ ὅτε δὴ τὸ τέταρτον" -2/+1 → 5 (A.3); rulings.py: the τὸ τέταρτον verses 15 and 37 both follow a verse that names Φεδερῆρος | necessary → necessary |
| 38 | PASS | Unchanged, v2 PASS (= v2 38). Neighbour of 37: the subject moves from Federer (36-37) to the named Σέρβος, marked by an apodotic δ᾽. The v2 QUERY 37 is resolved. | identity → 38=38 | unperiodic → unperiodic |
| 39 | PASS | Unchanged, v2 PASS (= v2 39). | identity → 39=39 | necessary → necessary |
| 40 | PASS | Unchanged, v2 PASS (= v2 40). | identity → 40=40 | none → none |
| 41 | PASS | Unchanged, v2 PASS (= v2 41). | identity → 41=41 | unperiodic → unperiodic |
| 42 | PASS | Unchanged, v2 PASS (= v2 42). | identity → 42=42 | none → none |
| 43 | PASS | Unchanged, v2 PASS (= v2 43). Neighbour of 44: Σέρβον is the same man as Νοβῆκος in 44. | identity → 43=43 | none → none |
| 44 | PASS | **v2 FAIL repaired; R10 applied.** The change of subject is now marked by ὃ δ᾽, and κέρδεα εἰδώς stands in apposition to ὃ, i.e. Federer, as in Ῥογῆρος κέρδεα εἰδώς (27). So the craft epithet stays with Federer ✓. **Models for leader and follower.** (1) A pronoun with δέ for the follower: Od. 1.125 (ἡγεῖθ᾽, ἡ δ᾽ ἕσπετο Παλλὰς Ἀθήνη) and Il. 11.472 = 15.559 = 16.632 (ὃ μὲν ἦρχ᾽, ὃ δ᾽ ἅμ᾽ ἕσπετο ἰσόθεος φώς). (2) A pursuer marked by ὃ δ᾽: Il. 21.256 (φεῦγ᾽, ὃ δ᾽ ὄπισθε ῥέων ἕπετο). (3) Race order: Il. 23.376-377 (ἔκφερον … τὰς δὲ μετ᾽ ἐξέφερον). **Lexicon and morphology.** (1) ἔκφερε is intransitive, "to draw away from competitors in a race, shoot ahead" (Cunliffe ἐκφέρω 6: Il. 23.376, 377, 759; LSJ "intr. … shoot forth (before the rest)"). (2) It is unaugmented, and unelided before δ᾽: ἔκφερ᾽ occurs 3x and ἔκφερεν once (Od. 15.470); ἔκφερε itself has 0 hits but is the regular 3 sg. imperfect before a consonant. (3) δ᾽ αὖτε after a dactylic first word stands at 3-3.5, as in Od. 2.203 (χρήματα δ᾽ αὖτε); 5 of 141 hits are at 3-3.5. (4) Νοβῆκος is at 4-5.5 before a vowel, an A1 slot; the accent follows R9 ✓. (5) ἕσπετο is at 7-8 (8 of 12 hits). **Notes.** (1) ὃ δ᾽ ἕσπετο itself has 0 hits. (2) In Homer the aorist ἕσπετο always means "accompany, follow a leader" (12/12; Cunliffe ἕπομαι 1, 5). The hostile sense "follow up, pursue" and the sense "keep up with" belong to the present stem: ἕπετο in Il. 11.165, 16.372, 21.256 and ἕπεθ᾽ in Il. 16.154 (Cunliffe 6, 8; LSJ I.3-4). "He followed" for Federer's hold to 9-9 thus puts the follower of a race-order line into the aorist, a slight extension. **Sense and facts.** The gloss is right. 9-8 at 4:17:15 and 9-9 at 4:21:04 ✓. | [44a] --ngram "ἔκφερ᾽" → 3; [44b] ἔκφερεν → Od. 15.470; [44c] ἔκφερε → 0; ctx Il. 23.759, 23.376-377; [44d] δ᾽ αὖτε → 141 (5 at 3-3.5); [44f] --ngram "ὃ δ᾽ ἕσπετο" → 0; [44g] "δ᾽ ἕσπετο" → 3; [44h] ἕσπετο → 12; [44j] ἕπετο → 4; [44k] ἑσπόμενος → 2; ctx "ὃ δ᾽ ἅμ᾽ ἕσπετο ἰσόθεος φώς" → 3; [44i] κέρδεα εἰδώς → Il. 23.709; Cunliffe ἐκφέρω, ἕπομαι; LSJ ἐκφέρω, ἕπομαι (A.7) | none → none |
| 45 | PASS | Unchanged, v2 PASS (= v2 45). Neighbour of 44: it follows 44's full stop; the simile 45-47 → 48 is intact. | identity → 45=45 | necessary → necessary |
| 46 | PASS | Unchanged, v2 PASS (= v2 46). | identity → 46=46 | necessary → necessary |
| 47 | PASS | Unchanged, v2 PASS (= v2 47). | identity → 47=47 | necessary → necessary |
| 48 | PASS | Unchanged, v2 PASS (= v2 48). | identity → 48=48 | unperiodic → unperiodic |
| 49 | PASS | Unchanged, v2 PASS (= v2 49). | identity → 49=49 | unperiodic → unperiodic |
| 50 | PASS | Unchanged, v2 PASS (= v2 50). Neighbour of 51: the dual κῆρε is the antecedent of τήν … τήν in 51. | identity → 50=50 | unperiodic → unperiodic |
| 51 | PASS | **R10 applied.** ἀντιθέου Ζοκοβῆος is replaced by τὴν δ᾽ αὖ Σέρβου κρατεροῖο. **Morphology.** Σέρβου is a second-declension genitive in -ου, beside an epithet in -οιο. Homer has the same mixture in Μενελάου κυδαλίμοιο (Il. 4.100 etc.), Ἀγαστρόφου ἰφθίμοιο (Il. 11.373) and Ἀρκεισίου ἀντιθέοιο (Od. 14.182). A name in the genitive with κρατεροῖο at verse end is Πολυποίταο κρατεροῖο (Il. 23.848), and 5 of the 7 κρατεροῖο stand at 9.5-12. κρατερός is Djokovic's epithet (23, 53), so economy holds. **Syntax.** The model is τὴν μὲν … τὴν δ᾽ (Il. 22.211), with αὖ added to the second member. τὴν μὲν … τὴν δ᾽ αὖ is not attested (0 hits), but distributive μέν … δ᾽ αὖ is: ἄλλος μέν … ἄλλος δ᾽ αὖ (Od. 8.169/174) and ὁτὲ μέν … ἄλλοτε δ᾽ αὖ (Il. 18.599/602). A pronoun + δ᾽ αὖ at 6-7 is Il. 8.324. **Idiom.** Σέρβου is LL at 8-9 before an SSLX word, the shape of ἀνδρῶν Ἀγαμέμνων (36x) and κνίσῃ ἐκάλυψαν (4x, 8-12). **Sense and facts.** The gloss is right; 12-12 at 4:48:30 ✓. **Continuity.** τήν refers to the dual κῆρε of 50, and 52 (ἕλκε δέ …) follows as in Il. 22.212. **Note.** The jsonl claim that Ζοκοβείδαο fits no slot is false (§5); the choice made here is unaffected. | ctx "τὴν δ᾽ Ἕκτορος ἱπποδάμοιο" → Il. 22.210-212; [51a] "τὴν μὲν ἄρ᾽" → 3; [51b] "τὴν δ᾽ αὖ" → 13, all [1-2]; [51c] menau.py → 2 (neither distributive); [51j] ἄλλ-/ἑτέρ- δ᾽ αὖ → 3 + ctx Od. 8.169-174, Il. 18.599-602; [51e] κρατεροῖο → 7; [51h] -ου + -οιο at verse end → 38; [51i] capitalised -ου + -οιο → 25; [51f] ἀνδρῶν Ἀγαμέμνων → 36; [51g] κνίσῃ ἐκάλυψαν → 4 [8-12]; [51k] check_line on the Ζοκοβείδαο test verse | unperiodic → unperiodic |
| 52 | PASS | Unchanged, v2 PASS (= v2 52). Neighbour of 51: Ἑλβετίου is repeated after 51, as Ἕκτορος is in Il. 22.211-212. | identity → 52=52 | none → none |
| 53 | PASS | Unchanged, v2 PASS (= v2 53). | identity → 53=53 | unperiodic → unperiodic |
| 54 | PASS | Unchanged, v2 PASS (= v2 54). Neighbour of 55: Federer is the subject; 55 names Νοβῆκος inside the verse. | identity → 54=54 | none → none |
| 55 | PASS | **R9 and R11 applied.** Νοβῆκος has the circumflex: Homer has 51 types in η/ω + one consonant + -ος, all circumflexed, and 0 with the acute. **Count.** This is the system of 33, with Νοβῆκος in the Ῥογῆρος slot (6-8 after a vowel; -κος long before καί). It has two hit clauses for two winners, the forehand at 420 and the backhand at 421 ✓; see 33 for βάλλω and αὖτις. **Continuity.** 54 has Ἑλβέτιος as subject; the change is resolved inside this verse by the name. **Punctuation.** 55 prints καὶ βάλεν, οὐδ᾽ ἀφάμαρτε Νοβῆκος with no comma after ἀφάμαρτε, as Il. 11.350; 33 has one, as Il. 13.160. Both are Homeric; harmonise if wanted. **Sense.** The gloss is right. | accent.py → acute 0 / circumflex 51 types, 269 tokens (A.0); rulings.py → Νοβῆκος 44, 55, Νοβήκος 0; A.2 as for 33 | none → none |
| 56 | PASS | **v2 FAIL repaired.** αὖθ᾽ now stands before the rough breathing of Ἑλβέτιος. Homer has αὖθ᾽ + rough breathing 33x and αὖτ᾽ + rough breathing 0x, and the draft now has no elided τ, π or κ before a rough breathing. As noted in v2, ἔνθ᾽ αὖθ᾽ has 0 hits against 12 for ἔνθ᾽ αὖτ᾽, because ἔνθ᾽ αὖτ᾽ never stands before an aspirated word. **Unchanged from v2.** προΐει is absolute; βάλε δ᾽ stands at 7.5-9; ἂψ means "in return"; R3 ✓. **Facts and continuity.** Point 422 ✓. 57 follows with Ἑλβέτιος δ᾽ ἄρα τοῦ μέν … | aspir.py → αὖθ᾽ + rough 33, αὖτ᾽ + rough 0; draft: no ERROR (A.0); [56a] "ἔνθ᾽ αὖθ᾽" → 0; [56b] "ἔνθ᾽ αὖτ᾽" → 12; [56c] "αὖθ᾽ ἱερεὺς" → Il. 1.370 | unperiodic → unperiodic |
| 57 | PASS | Unchanged, v2 PASS (= v2 57). Neighbour of 56: it follows 56 with δ᾽ ἄρα. | identity → 57=57 | none → none |
| 58 | PASS | Unchanged, v2 PASS (= v2 58). | identity → 58=58 | none → none |
| 59 | PASS | Unchanged, v2 PASS (= v2 59). | identity → 59=59 | unperiodic → unperiodic |
| 60 | PASS | Unchanged, v2 PASS (= v2 60). | identity → 60=60 | none → none |

## Appendix A. Verbatim evidence

Printed by `appendix.sh` (B.10) on 2026-10-07, run from the repository root with `.venv` active. Lines beginning `# [tag]` give the command; `python homer/concordance.py` output is unedited, and the hit lists are shown in full except where a header says what is shown.

### A.0 Identity, check_line, rulings, aspiration, accent, similes (whole draft)

```
# [ID] python -I identity.py composition/drafts
v3.txt == v3.jsonl text: 60/60
identical to v2 (v3 n = v2 n): 53 1=1, 2=2, 3=3, 4=4, 5=5, 6=6, 7=7, 8=8, 9=9, 10=10, 11=11, 12=12, 13=13, 14=14, 15=15, 16=16, 17=17, 18=18, 19=19, 20=20, 21=21, 22=22, 24=24, 25=25, 26=26, 27=27, 28=28, 29=29, 30=30, 31=31, 32=32, 34=34, 35=35, 37=37, 38=38, 39=39, 40=40, 41=41, 42=42, 43=43, 45=45, 46=46, 47=47, 48=48, 49=49, 50=50, 52=52, 53=53, 54=54, 57=57, 58=58, 59=59, 60=60
changed (v3 n <- v2 n): 7 23<-23, 33<-33, 36<-36, 44<-44, 51<-51, 55<-55, 56<-56
new: [] | jsonl "changed" flag disagrees with text diff: []

# [CL] python homer/check_line.py --file composition/drafts/v3.txt (summary: lines with OK, exit status)
exit=0
60
```

```
# [RUL] python -I rulings.py . composition/drafts/v3.txt
R2 ἰσόθεος: 0 []
R3 withdrawn Ζοκοβίδης/Νοβάκος: 0 []
R4 δίς: 0 []
R5 ἐξεναρίζω: 0 []
R6 πάλιν: 1 [(22, 'πάλιν')]
R9 Νοβ- with acute (Νοβήκ-): 0 []
R9 Νοβῆκος (circumflex): 2 [(44, 'Νοβῆκος'), (55, 'Νοβῆκος')]
R10 Ζοκοβεύς / Ζοκοβῆ- (eponym forms): 0 []
Ζοκοβείδης (patronymic): 4 [(4, 'Ζοκοβείδης'), (23, 'Ζοκοβείδης'), (53, 'Ζοκοβείδης'), (56, 'Ζοκοβείδης')]
Σέρβ- (ethnic): 7 [(10, 'Σέρβος'), (15, 'Σέρβος'), (29, 'Σέρβος'), (38, 'Σέρβος'), (43, 'Σέρβον'), (51, 'Σέρβου'), (58, 'Σέρβος')]
δαμάζω (aor.): 7 [(20, 'ἐδάμασσε'), (24, 'δάμασεν'), (29, 'ἐδάμασσε'), (30, 'ἐδάμασσε'), (34, 'ἐδάμασσε'), (40, 'δαμάσσῃ'), (58, 'ἐδάμασσε')]
prohibited (γραμμ, στεγ, οχλ, ωρη/ωρα, δικτυ, ραβδ, χλο, χορτ, δικαστ, αθλητησ, σφαιριστ, ηττ): 0 []
R11 "δεύτερον αὖτις": [24]
"καὶ βάλεν … καὶ βάλεν" (two hit clauses): [33, 55]
"τὸ τέταρτον" lines and the subject named in the verse before: [(15, 'Φεδερῆρος'), (37, 'Φεδερῆρος')]
```

```
# [ASP] python -I aspir.py . composition/drafts/v3.txt
Homer:
  ('αὖθ', 'rough') 33 | e.g. Il. 1.370 Χρύσης δʼ αὖθʼ ἱερεὺς ἑκατηβόλου Ἀπόλλωνος
  ('αὖθ', 'smooth') 3 | e.g. Il. 11.48 ἵππους εὖ κατὰ κόσμον ἐρυκέμεν αὖθʼ ἐπὶ τάφρῳ,
  ('αὖτ', 'smooth') 130 | e.g. Il. 1.202 τίπτʼ αὖτʼ αἰγιόχοιο Διὸς τέκος εἰλήλουθας;
Draft composition/drafts/v3.txt :
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
  36: ἔπειτ᾽ ἐπόρουσε  next word smooth  -> ok
  38: αὖθ᾽ ἑτέρωθεν  next word rough  -> ok
  39: ἐπ᾽ εἰροπόκοις  next word smooth  -> ok
  40: τ᾽ αὐλῆς  next word smooth  -> ok
  41: τ᾽ οὐ  next word smooth  -> ok
  45: ὅτ᾽ ἀεθλοφόροι  next word smooth  -> ok
  53: ἔπειτ᾽ ἐπόρουσε  next word smooth  -> ok
  54: τότ᾽ ἀμύνετο  next word smooth  -> ok
  56: ἔνθ᾽ αὖθ᾽  next word smooth  -> ok
  56: αὖθ᾽ Ἑλβέτιος  next word rough  -> ok
  58: αὖτ᾽ ἐδάμασσε,  next word smooth  -> ok
  60: ὅτ᾽ ἤλυθε  next word smooth  -> ok

# [ACC] python -I accent.py .
acute on long penult (η/ω) + C + ος: types 0 tokens 0
circumflex on penult (η/ω) + C + ος: types 51 tokens 269
   e.g. πρῶτος, ἦμος, στῆθος, δηϊοτῆτος, ποτῆτος, τῆμος, τεθνηῶτος, κρητῆρος, δῆμος, κλῆρος, ζωστῆρος, ἦδος
```

```
# [SIM] python -I simile.py . composition/drafts/v3.txt
simile opener at 16: ὡς δ᾽ ὅτε τις στατὸς ἵππος ἀκοστήσας ἐπὶ φάτνῃ
   apodosis line: 19: ὣς ἄρ᾽ ὅ γ᾽ Ἑλβέτιος τότ᾽ ἐπέσσυτο δεύτερον αὖτε·; vehicle lines 16-18 (3 lines)
simile opener at 38: Σέρβος δ᾽ αὖθ᾽ ἑτέρωθεν ἐναντίον ὦρτο λέων ὣς
   apodosis line: 43: ὣς τότε Σέρβον ἀνῆκε μένος καὶ θυμὸς ἀγήνωρ·; vehicle lines 38-42 (5 lines)
simile opener at 45: ὡς δ᾽ ὅτ᾽ ἀεθλοφόροι περὶ τέρματα μώνυχες ἵπποι
   apodosis line: 48: ὣς τὼ πολλάκι δὴ περὶ τέρματα δινηθήτην,; vehicle lines 45-47 (3 lines)
```

### A.1 Line 23 (δεύτερον αὖ, λάβ᾽ ἄεθλον, ἄφαρ, κρατερὸς + SSLL name)

```
# [23a] python homer/concordance.py --ngram "δεύτερον αὖ"
Il. 3.332    [1-3]  δεύτερον αὖ θώρηκα περὶ στήθεσσιν ἔδυνεν    <δεύτερον αὖ>
Il. 6.184    [1-3]  δεύτερον αὖ Σολύμοισι μαχέσσατο κυδαλίμοισι·    <δεύτερον αὖ>
Il. 11.19    [1-3]  δεύτερον αὖ θώρηκα περὶ στήθεσσιν ἔδυνε,    <δεύτερον αὖ>
Il. 16.133   [1-3]  δεύτερον αὖ θώρηκα περὶ στήθεσσιν ἔδυνε    <δεύτερον αὖ>
Il. 19.371   [1-3]  δεύτερον αὖ θώρηκα περὶ στήθεσσιν ἔδυνεν.    <δεύτερον αὖ>
-- 5 hit(s)

# [23b] python homer/concordance.py --ngram "λάβ᾽ ἄεθλον"
Il. 23.511   [9.5-12]  ἴφθιμος Σθένελος, ἀλλʼ ἐσσυμένως λάβʼ ἄεθλον,    <λάβʼ ἄεθλον>
-- 1 hit(s)

# context for ngram "λάβ᾽ ἄεθλον" (-2/+1 lines): 1 hit(s)
  Il. 23.509   αὐτὸς δʼ ἐκ δίφροιο χαμαὶ θόρε παμφανόωντος,
  Il. 23.510   κλῖνε δʼ ἄρα μάστιγα ποτὶ ζυγόν· οὐδὲ μάτησεν
> Il. 23.511   ἴφθιμος Σθένελος, ἀλλʼ ἐσσυμένως λάβʼ ἄεθλον,
  Il. 23.512   δῶκε δʼ ἄγειν ἑτάροισιν ὑπερθύμοισι γυναῖκα

# [23c] python homer/concordance.py --ngram "κρατερὸς Διομήδης" --count
20

# [23d] python homer/concordance.py --ngram "μίγη κρατερὸς Διομήδης"
Il. 5.143    [6-12]  ὣς μεμαὼς Τρώεσσι μίγη κρατερὸς Διομήδης.    <μίγη κρατερὸς Διομήδης>
-- 1 hit(s)

# [23e] python homer/concordance.py --loose "αφαρ" --word
Il. 1.349    [5.5-6]  δακρύσας ἑτάρων ἄφαρ ἕζετο νόσφι λιασθείς,    <ἄφαρ>
Il. 1.594    [6-7]  ἔνθά με Σίντιες ἄνδρες ἄφαρ κομίσαντο πεσόντα.    <ἄφαρ>
Il. 2.453    [2-3]  τοῖσι δʼ ἄφαρ πόλεμος γλυκίων γένετʼ ἠὲ νέεσθαι    <ἄφαρ>
Il. 10.537   [1.5-2]  ὧδʼ ἄφαρ ἐκ Τρώων ἐλασαίατο μώνυχας ἵππους·    <ἄφαρ>
Il. 11.13    [2-3]  τοῖσι δʼ ἄφαρ πόλεμος γλυκίων γένετʼ ἠὲ νέεσθαι    <ἄφαρ>
Il. 11.418   [6-7]  γίγνεται, οἳ δὲ μένουσιν ἄφαρ δεινόν περ ἐόντα,    <ἄφαρ>
Il. 12.221   [2-3]  ζωόν· ἄφαρ δʼ ἀφέηκε πάρος φίλα οἰκίʼ ἱκέσθαι,    <ἄφαρ>
Il. 13.814   [2-3]  νῆας· ἄφαρ δέ τε χεῖρες ἀμύνειν εἰσὶ καὶ ἡμῖν.    <ἄφαρ>
Il. 16.323   [2-3]  ὦμον ἄφαρ· πρυμνὸν δὲ βραχίονα δουρὸς ἀκωκὴ    <ἄφαρ>
Il. 17.392   [2-3]  κυκλόσʼ, ἄφαρ δέ τε ἰκμὰς ἔβη, δύνει δέ τʼ ἀλοιφὴ    <ἄφαρ>
Il. 17.417   [6-7]  πᾶσι χάνοι· τό κεν ἧμιν ἄφαρ πολὺ κέρδιον εἴη    <ἄφαρ>
Il. 17.750   [2-3]  ἴσχει, ἄφαρ δέ τε πᾶσι ῥόον πεδίον δὲ τίθησι    <ἄφαρ>
Il. 19.405   [2-3]  Ξάνθος, ἄφαρ δʼ ἤμυσε καρήατι· πᾶσα δὲ χαίτη    <ἄφαρ>
Il. 21.528   [2-3]  Τρῶες ἄφαρ κλονέοντο πεφυζότες, οὐδέ τις ἀλκὴ    <ἄφαρ>
Il. 22.270   [6-7]  οὔ τοι ἔτʼ ἔσθʼ ὑπάλυξις, ἄφαρ δέ σε Παλλὰς Ἀθήνη    <ἄφαρ>
Il. 23.375   [2-3]  φαίνετʼ, ἄφαρ δʼ ἵπποισι τάθη δρόμος· ὦκα δʼ ἔπειτα    <ἄφαρ>
Il. 23.593   [6-7]  μεῖζον ἐπαιτήσειας, ἄφαρ κέ τοι αὐτίκα δοῦναι    <ἄφαρ>
Il. 24.446   [2-3]  πᾶσιν, ἄφαρ δʼ ὤϊξε πύλας καὶ ἀπῶσεν ὀχῆας,    <ἄφαρ>
Od. 1.410    [5.5-6]  οἷον ἀναΐξας ἄφαρ οἴχεται, οὐδʼ ὑπέμεινε    <ἄφαρ>
Od. 2.95     [6-7]  λεπτὸν καὶ περίμετρον· ἄφαρ δʼ ἡμῖν μετέειπε·    <ἄφαρ>
Od. 2.169    [6-7]  παυέσθων· καὶ γάρ σφιν ἄφαρ τόδε λώιόν ἐστιν.    <ἄφαρ>
Od. 3.456    [6-7]  αἶψʼ ἄρα μιν διέχευαν, ἄφαρ δʼ ἐκ μηρία τάμνον    <ἄφαρ>
Od. 4.85     [6-7]  καὶ Λιβύην, ἵνα τʼ ἄρνες ἄφαρ κεραοὶ τελέθουσι.    <ἄφαρ>
Od. 5.482    [2-3]  δύσετʼ. ἄφαρ δʼ εὐνὴν ἐπαμήσατο χερσὶ φίλῃσιν    <ἄφαρ>
Od. 6.49     [6-7]  Ναυσικάαν ἐύπεπλον· ἄφαρ δʼ ἀπεθαύμασʼ ὄνειρον,    <ἄφαρ>
Od. 8.270    [6-7]  Ἡφαίστοιο ἄνακτος. ἄφαρ δέ οἱ ἄγγελος ἦλθεν    <ἄφαρ>
Od. 8.409    [2-3]  δεινόν, ἄφαρ τὸ φέροιεν ἀναρπάξασαι ἄελλαι.    <ἄφαρ>
Od. 9.328    [2-3]  ἄκρον, ἄφαρ δὲ λαβὼν ἐπυράκτεον ἐν πυρὶ κηλέῳ.    <ἄφαρ>
Od. 10.122   [2-3]  βάλλον· ἄφαρ δὲ κακὸς κόναβος κατὰ νῆας ὀρώρει    <ἄφαρ>
Od. 11.274   [2-3]  γῆμεν· ἄφαρ δʼ ἀνάπυστα θεοὶ θέσαν ἀνθρώποισιν.    <ἄφαρ>
Od. 17.305   [6-7]  ῥεῖα λαθὼν Εὔμαιον, ἄφαρ δʼ ἐρεείνετο μύθῳ·    <ἄφαρ>
Od. 19.140   [6-7]  λεπτὸν καὶ περίμετρον· ἄφαρ δʼ αὐτοῖς μετέειπον·    <ἄφαρ>
Od. 21.307   [6-7]  ἡμετέρῳ ἐνὶ δήμῳ, ἄφαρ δέ σε νηῒ μελαίνῃ    <ἄφαρ>
Od. 24.130   [6-7]  λεπτὸν καὶ περίμετρον· ἄφαρ δʼ ἡμῖν μετέειπε·    <ἄφαρ>
-- 34 hit(s)

# context for ngram "ὦμον ἄφαρ" (-2/+0 lines): 1 hit(s)
  Il. 16.321   στὰς πρόσθεν νέκυος· τοῦ δʼ ἀντίθεος Θρασυμήδης
  Il. 16.322   ἔφθη ὀρεξάμενος πρὶν οὐτάσαι, οὐδʼ ἀφάμαρτεν,
> Il. 16.323   ὦμον ἄφαρ· πρυμνὸν δὲ βραχίονα δουρὸς ἀκωκὴ

# context for ngram "οἳ δὲ μένουσιν ἄφαρ" (-2/+0 lines): 1 hit(s)
  Il. 11.416   θήγων λευκὸν ὀδόντα μετὰ γναμπτῇσι γένυσσιν,
  Il. 11.417   ἀμφὶ δέ τʼ ἀΐσσονται, ὑπαὶ δέ τε κόμπος ὀδόντων
> Il. 11.418   γίγνεται, οἳ δὲ μένουσιν ἄφαρ δεινόν περ ἐόντα,

# [23f] python homer/concordance.py --loose "αεθλον" --word
Il. 22.163   [10-12]  ῥίμφα μάλα τρωχῶσι· τὸ δὲ μέγα κεῖται ἄεθλον    <ἄεθλον>
Il. 23.413   [10-12]  αἴ κʼ ἀποκηδήσαντε φερώμεθα χεῖρον ἄεθλον.    <ἄεθλον>
Il. 23.441   [10-12]  ἀλλʼ οὐ μὰν οὐδʼ ὧς ἄτερ ὅρκου οἴσῃ ἄεθλον.    <ἄεθλον>
Il. 23.511   [10-12]  ἴφθιμος Σθένελος, ἀλλʼ ἐσσυμένως λάβʼ ἄεθλον,    <ἄεθλον>
Il. 23.544   [10-12]  τοῦτο ἔπος· μέλλεις γὰρ ἀφαιρήσεσθαι ἄεθλον    <ἄεθλον>
Il. 23.551   [10-12]  τῶν οἱ ἔπειτʼ ἀνελὼν δόμεναι καὶ μεῖζον ἄεθλον    <ἄεθλον>
Il. 23.615   [10-12]  τέτρατος, ὡς ἔλασεν. πέμπτον δʼ ὑπελείπετʼ ἄεθλον,    <ἄεθλον>
Il. 23.620   [10-12]  ὄψῃ ἐν Ἀργείοισι· δίδωμι δέ τοι τόδʼ ἄεθλον    <ἄεθλον>
Il. 23.748   [6-7.5]  καὶ τὸν Ἀχιλλεὺς θῆκεν ἄεθλον οὗ ἑτάροιο,    <ἄεθλον>
Il. 23.773   [10-12]  ἀλλʼ ὅτε δὴ τάχʼ ἔμελλον ἐπαΐξασθαι ἄεθλον,    <ἄεθλον>
Il. 23.785   [10-12]  Ἀντίλοχος δʼ ἄρα δὴ λοισθήϊον ἔκφερʼ ἄεθλον    <ἄεθλον>
Il. 23.849   [10-12]  νῆας ἔπι γλαφυρὰς ἔφερον βασιλῆος ἄεθλον.    <ἄεθλον>
Il. 23.892   [4-5.5]  ἀλλὰ σὺ μὲν τόδʼ ἄεθλον ἔχων κοίλας ἐπὶ νῆας    <ἄεθλον>
Il. 23.897   [10-12]  Ταλθυβίῳ κήρυκι δίδου περικαλλὲς ἄεθλον.    <ἄεθλον>
Od. 8.133    [10-12]  δεῦτε, φίλοι, τὸν ξεῖνον ἐρώμεθα εἴ τινʼ ἄεθλον    <ἄεθλον>
Od. 8.197    [10-12]  ἀλλὰ πολὺ πρῶτον. σὺ δὲ θάρσει τόνδε γʼ ἄεθλον·    <ἄεθλον>
Od. 11.624   [10-12]  φράζετο τοῦδέ γέ μοι κρατερώτερον εἶναι ἄεθλον·    <ἄεθλον>
Od. 19.572   [10-12]  οἴκου ἀποσχήσει· νῦν γὰρ καταθήσω ἄεθλον,    <ἄεθλον>
Od. 19.576   [6-8]  νῦν δὲ μνηστήρεσσιν ἄεθλον τοῦτον ἐφήσω·    <ἄεθλον>
Od. 19.584   [10-12]  μηκέτι νῦν ἀνάβαλλε δόμοις ἔνι τοῦτον ἄεθλον·    <ἄεθλον>
Od. 21.73    [10-12]  ἀλλʼ ἄγετε, μνηστῆρες, ἐπεὶ τόδε φαίνετʼ ἄεθλον.    <ἄεθλον>
Od. 21.91    [4-5.5]  μνηστήρεσσιν ἄεθλον ἀάατον· οὐ γὰρ ὀΐω    <ἄεθλον>
Od. 21.106   [10-12]  ἀλλʼ ἄγετε, μνηστῆρες, ἐπεὶ τόδε φαίνετʼ ἄεθλον,    <ἄεθλον>
Od. 21.135   [10-12]  τόξου πειρήσασθε, καὶ ἐκτελέωμεν ἄεθλον.    <ἄεθλον>
Od. 21.180   [10-12]  τόξου πειρώμεσθα καὶ ἐκτελέωμεν ἄεθλον.    <ἄεθλον>
Od. 21.268   [10-12]  τόξου πειρώμεσθα καὶ ἐκτελέωμεν ἄεθλον.    <ἄεθλον>
Od. 23.261   [4-5.5]  εἴπʼ ἄγε μοι τὸν ἄεθλον, ἐπεὶ καὶ ὄπισθεν, ὀΐω,    <ἄεθλον>
-- 27 hit(s)

```

### A.2 Lines 33 and 55 (two hit clauses; καὶ βάλεν; αὖτις)

```
# [33a] python homer/concordance.py --ngram "καὶ βάλεν οὐδ᾽ ἀφάμαρτε"
Il. 11.350   [1-5.5]  καὶ βάλεν, οὐδʼ ἀφάμαρτε τιτυσκόμενος κεφαλῆφιν,    <καὶ βάλεν, οὐδʼ ἀφάμαρτε>
Il. 13.160   [1-5.5]  καὶ βάλεν, οὐδʼ ἀφάμαρτε, κατʼ ἀσπίδα πάντοσʼ ἐΐσην    <καὶ βάλεν, οὐδʼ ἀφάμαρτε>
-- 2 hit(s)

# [33b] python homer/concordance.py --ngram "οὐδ᾽ ἀφάμαρτε"
Il. 11.350   [3-5.5]  καὶ βάλεν, οὐδʼ ἀφάμαρτε τιτυσκόμενος κεφαλῆφιν,    <οὐδʼ ἀφάμαρτε>
Il. 13.160   [3-5.5]  καὶ βάλεν, οὐδʼ ἀφάμαρτε, κατʼ ἀσπίδα πάντοσʼ ἐΐσην    <οὐδʼ ἀφάμαρτε>
Il. 14.403   [9-12]  ἔγχει, ἐπεὶ τέτραπτο πρὸς ἰθύ οἱ, οὐδʼ ἀφάμαρτε,    <οὐδʼ ἀφάμαρτε>
Il. 22.290   [9-12]  καὶ βάλε Πηλεΐδαο μέσον σάκος οὐδʼ ἀφάμαρτε·    <οὐδʼ ἀφάμαρτε>
-- 4 hit(s)

# [33c] python homer/concordance.py --ngram "καὶ βάλεν"
Il. 3.347    [1-2]  καὶ βάλεν Ἀτρεΐδαο κατʼ ἀσπίδα πάντοσε ἴσην,    <καὶ βάλεν>
Il. 5.612    [1-2]  καὶ βάλεν Ἄμφιον Σελάγου υἱόν, ὅς ῥʼ ἐνὶ Παισῷ    <καὶ βάλεν>
Il. 7.245    [1-2]  καὶ βάλεν Αἴαντος δεινὸν σάκος ἑπταβόειον    <καὶ βάλεν>
Il. 11.350   [1-2]  καὶ βάλεν, οὐδʼ ἀφάμαρτε τιτυσκόμενος κεφαλῆφιν,    <καὶ βάλεν>
Il. 11.376   [1-2]  καὶ βάλεν, οὐδʼ ἄρα μιν ἅλιον βέλος ἔκφυγε χειρός,    <καὶ βάλεν>
Il. 13.160   [1-2]  καὶ βάλεν, οὐδʼ ἀφάμαρτε, κατʼ ἀσπίδα πάντοσʼ ἐΐσην    <καὶ βάλεν>
Il. 13.371   [1-2]  καὶ βάλεν ὕψι βιβάντα τυχών· οὐδʼ ἤρκεσε θώρηξ    <καὶ βάλεν>
Il. 17.348   [1-2]  καὶ βάλεν Ἱππασίδην Ἀπισάονα ποιμένα λαῶν    <καὶ βάλεν>
Il. 17.517   [1-2]  καὶ βάλεν Ἀρήτοιο κατʼ ἀσπίδα πάντοσʼ ἐΐσην·    <καὶ βάλεν>
Il. 20.274   [1-2]  καὶ βάλεν Αἰνείαο κατʼ ἀσπίδα πάντοσʼ ἐΐσην    <καὶ βάλεν>
Od. 24.523   [1-2]  καὶ βάλεν Εὐπείθεα κόρυθος διὰ χαλκοπαρῄου.    <καὶ βάλεν>
-- 11 hit(s)

# [33d] python homer/concordance.py --ngram "βάλεν αὖτις"
-- 0 hit(s)

# [33e] python homer/concordance.py --regex "(βάλ|βαλ|οὖτα|οὔτα|νύξ|τύψ|ἔβλητο|βλῆτο).*αὖτις|αὖτις.*(βάλ|βαλ|οὖτα|οὔτα|νύξ|τύψ)"
-- 0 hit(s)

# [33h] python homer/concordance.py --regex "(βάλεν|βάλε|ἔβαλε|ἔβαλεν|βάλʼ)[ ,·].*(καὶ|δὲ|δʼ) (βάλεν|βάλε|ἔβαλε|ἔβαλεν|βάλʼ)\b"
-- 0 hit(s)

# [33f] python homer/concordance.py --ngram "δεύτερον αὖτις"
Il. 1.513    [9-12]  ὣς ἔχετʼ ἐμπεφυυῖα, καὶ εἴρετο δεύτερον αὖτις·    <δεύτερον αὖτις>
Od. 3.161    [9-12]  σχέτλιος, ὅς ῥʼ ἔριν ὦρσε κακὴν ἔπι δεύτερον αὖτις.    <δεύτερον αὖτις>
Od. 9.354    [9-12]  ἡδὺ ποτὸν πίνων καὶ μʼ ᾔτεε δεύτερον αὖτις·    <δεύτερον αὖτις>
Od. 19.65    [9-12]  ἡ δʼ Ὀδυσῆʼ ἐνένιπε Μελανθὼ δεύτερον αὖτις·    <δεύτερον αὖτις>
Od. 22.69    [9-12]  τοῖσιν δʼ Εὐρύμαχος προσεφώνεε δεύτερον αὖτις·    <δεύτερον αὖτις>
-- 5 hit(s)

```

```
# [33g] python homer/concordance.py --loose "αυτις" --word  (128 hits; shown: the hit count, the 20 verse-final hits [11-12], and Od. 22.272)
128
Il. 1.140    [11-12]  ἀλλʼ ἤτοι μὲν ταῦτα μεταφρασόμεσθα καὶ αὖτις,    <αὖτις>
Il. 1.513    [11-12]  ὣς ἔχετʼ ἐμπεφυυῖα, καὶ εἴρετο δεύτερον αὖτις·    <αὖτις>
Il. 6.367    [11-12]  οὐ γὰρ οἶδʼ εἰ ἔτι σφιν ὑπότροπος ἵξομαι αὖτις,    <αὖτις>
Il. 9.375    [11-12]  ἐκ γὰρ δή μʼ ἀπάτησε καὶ ἤλιτεν· οὐδʼ ἂν ἔτʼ αὖτις    <αὖτις>
Il. 10.463   [11-12]  πάντων ἀθανάτων ἐπιδωσόμεθʼ· ἀλλὰ καὶ αὖτις    <αὖτις>
Il. 15.29    [11-12]  τὸν μὲν ἐγὼν ἔνθεν ῥυσάμην καὶ ἀνήγαγον αὖτις    <αὖτις>
Il. 17.533   [11-12]  τοὺς ὑποταρβήσαντες ἐχώρησαν πάλιν αὖτις    <αὖτις>
Il. 18.59    [11-12]  Τρωσὶ μαχησόμενον· τὸν δʼ οὐχ ὑποδέξομαι αὖτις    <αὖτις>
Il. 18.89    [11-12]  παιδὸς ἀποφθιμένοιο, τὸν οὐχ ὑποδέξεαι αὖτις    <αὖτις>
Il. 18.440   [11-12]  Τρωσὶ μαχησόμενον· τὸν δʼ οὐχ ὑποδέξομαι αὖτις    <αὖτις>
Il. 21.46    [11-12]  ἐλθὼν ἐκ Λήμνοιο· δυωδεκάτῃ δέ μιν αὖτις    <αὖτις>
Il. 23.75    [11-12]  καί μοι δὸς τὴν χεῖρʼ· ὀλοφύρομαι, οὐ γὰρ ἔτʼ αὖτις    <αὖτις>
Il. 24.150   [11-12]  ἡμιόνους καὶ ἄμαξαν ἐΰτροχον, ἠδὲ καὶ αὖτις    <αὖτις>
Il. 24.179   [11-12]  ἡμιόνους καὶ ἄμαξαν ἐΰτροχον, ἠδὲ καὶ αὖτις    <αὖτις>
Od. 3.161    [11-12]  σχέτλιος, ὅς ῥʼ ἔριν ὦρσε κακὴν ἔπι δεύτερον αὖτις.    <αὖτις>
Od. 5.430    [11-12]  καὶ τὸ μὲν ὣς ὑπάλυξε, παλιρρόθιον δέ μιν αὖτις    <αὖτις>
Od. 9.354    [11-12]  ἡδὺ ποτὸν πίνων καὶ μʼ ᾔτεε δεύτερον αὖτις·    <αὖτις>
Od. 19.65    [11-12]  ἡ δʼ Ὀδυσῆʼ ἐνένιπε Μελανθὼ δεύτερον αὖτις·    <αὖτις>
Od. 19.257   [11-12]  κείνῳ ἄγαλμʼ ἔμεναι· τὸν δʼ οὐχ ὑποδέξομαι αὖτις    <αὖτις>
Od. 22.69    [11-12]  τοῖσιν δʼ Εὐρύμαχος προσεφώνεε δεύτερον αὖτις·    <αὖτις>
Od. 22.272   [1-2]  αὖτις δὲ μνηστῆρες ἀκόντισαν ὀξέα δοῦρα    <αὖτις>
```

### A.3 Lines 36-37 (τρὶς μέν … τὸ τέταρτον; the attacker; repeated name formula)

```
# [36b] python homer/concordance.py --ngram "τρὶς μὲν ἔπειτ᾽ ἐπόρουσε"
Il. 5.436    [1-5.5]  τρὶς μὲν ἔπειτʼ ἐπόρουσε κατακτάμεναι μενεαίνων,    <τρὶς μὲν ἔπειτʼ ἐπόρουσε>
Il. 16.784   [1-5.5]  τρὶς μὲν ἔπειτʼ ἐπόρουσε θοῷ ἀτάλαντος Ἄρηϊ    <τρὶς μὲν ἔπειτʼ ἐπόρουσε>
Il. 20.445   [1-5.5]  τρὶς μὲν ἔπειτʼ ἐπόρουσε ποδάρκης δῖος Ἀχιλλεὺς    <τρὶς μὲν ἔπειτʼ ἐπόρουσε>
-- 3 hit(s)

# [36a] python homer/concordance.py --ngram "ἐπόρουσε βοὴν ἀγαθὸς Διομήδης"
Il. 5.432    [3.5-12]  Αἰνείᾳ δʼ ἐπόρουσε βοὴν ἀγαθὸς Διομήδης,    <ἐπόρουσε βοὴν ἀγαθὸς Διομήδης>
-- 1 hit(s)

# context for ngram "τρὶς μὲν ἔπειτ᾽ ἐπόρουσε" (-4/+3 lines): 3 hit(s)
  Il. 5.432   Αἰνείᾳ δʼ ἐπόρουσε βοὴν ἀγαθὸς Διομήδης,
  Il. 5.433   γιγνώσκων ὅ οἱ αὐτὸς ὑπείρεχε χεῖρας Ἀπόλλων·
  Il. 5.434   ἀλλʼ ὅ γʼ ἄρʼ οὐδὲ θεὸν μέγαν ἅζετο, ἵετο δʼ αἰεὶ
  Il. 5.435   Αἰνείαν κτεῖναι καὶ ἀπὸ κλυτὰ τεύχεα δῦσαι.
> Il. 5.436   τρὶς μὲν ἔπειτʼ ἐπόρουσε κατακτάμεναι μενεαίνων,
  Il. 5.437   τρὶς δέ οἱ ἐστυφέλιξε φαεινὴν ἀσπίδʼ Ἀπόλλων·
  Il. 5.438   ἀλλʼ ὅτε δὴ τὸ τέταρτον ἐπέσσυτο δαίμονι ἶσος,
  Il. 5.439   δεινὰ δʼ ὁμοκλήσας προσέφη ἑκάεργος Ἀπόλλων·

  Il. 16.780   καὶ τότε δή ῥʼ ὑπὲρ αἶσαν Ἀχαιοὶ φέρτεροι ἦσαν.
  Il. 16.781   ἐκ μὲν Κεβριόνην βελέων ἥρωα ἔρυσσαν
  Il. 16.782   Τρώων ἐξ ἐνοπῆς, καὶ ἀπʼ ὤμων τεύχεʼ ἕλοντο,
  Il. 16.783   Πάτροκλος δὲ Τρωσὶ κακὰ φρονέων ἐνόρουσε.
> Il. 16.784   τρὶς μὲν ἔπειτʼ ἐπόρουσε θοῷ ἀτάλαντος Ἄρηϊ
  Il. 16.785   σμερδαλέα ἰάχων, τρὶς δʼ ἐννέα φῶτας ἔπεφνεν.
  Il. 16.786   ἀλλʼ ὅτε δὴ τὸ τέταρτον ἐπέσσυτο δαίμονι ἶσος,
  Il. 16.787   ἔνθʼ ἄρα τοι Πάτροκλε φάνη βιότοιο τελευτή·

  Il. 20.441   αὐτοῦ δὲ προπάροιθε ποδῶν πέσεν. αὐτὰρ Ἀχιλλεὺς
  Il. 20.442   ἐμμεμαὼς ἐπόρουσε κατακτάμεναι μενεαίνων,
  Il. 20.443   σμερδαλέα ἰάχων· τὸν δʼ ἐξήρπαξεν Ἀπόλλων
  Il. 20.444   ῥεῖα μάλʼ ὥς τε θεός, ἐκάλυψε δʼ ἄρʼ ἠέρι πολλῇ.
> Il. 20.445   τρὶς μὲν ἔπειτʼ ἐπόρουσε ποδάρκης δῖος Ἀχιλλεὺς
  Il. 20.446   ἔγχεϊ χαλκείῳ, τρὶς δʼ ἠέρα τύψε βαθεῖαν.
  Il. 20.447   ἀλλʼ ὅτε δὴ τὸ τέταρτον ἐπέσσυτο δαίμονι ἶσος,
  Il. 20.448   δεινὰ δʼ ὁμοκλήσας ἔπεα πτερόεντα προσηύδα·

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

```

```
# [36c] python -I trismen.py .
Il. 5.436	τρὶς δ: yes	τρὶς μὲν ἔπειτʼ ἐπόρουσε κατακτάμεναι μενεαίνων,  ||  next: τρὶς δέ οἱ ἐστυφέλιξε φαεινὴν ἀσπίδʼ Ἀπόλλων·
Il. 8.169	τρὶς δ: yes	τρὶς μὲν μερμήριξε κατὰ φρένα καὶ κατὰ θυμόν,  ||  next: τρὶς δʼ ἄρʼ ἀπʼ Ἰδαίων ὀρέων κτύπε μητίετα Ζεὺς
Il. 11.462	τρὶς δ: yes	τρὶς μὲν ἔπειτʼ ἤϋσεν ὅσον κεφαλὴ χάδε φωτός,  ||  next: τρὶς δʼ ἄϊεν ἰάχοντος ἄρηι φίλος Μενέλαος.
Il. 13.20	τρὶς δ: NO 	τρὶς μὲν ὀρέξατʼ ἰών, τὸ δὲ τέτρατον ἵκετο τέκμωρ  ||  next: Αἰγάς, ἔνθα δέ οἱ κλυτὰ δώματα βένθεσι λίμνης
Il. 16.702	τρὶς δ: yes	τρὶς μὲν ἐπʼ ἀγκῶνος βῆ τείχεος ὑψηλοῖο  ||  next: Πάτροκλος, τρὶς δʼ αὐτὸν ἀπεστυφέλιξεν Ἀπόλλων
Il. 16.784	τρὶς δ: yes	τρὶς μὲν ἔπειτʼ ἐπόρουσε θοῷ ἀτάλαντος Ἄρηϊ  ||  next: σμερδαλέα ἰάχων, τρὶς δʼ ἐννέα φῶτας ἔπεφνεν.
Il. 18.155	τρὶς δ: yes	τρὶς μέν μιν μετόπισθε ποδῶν λάβε φαίδιμος Ἕκτωρ  ||  next: ἑλκέμεναι μεμαώς, μέγα δὲ Τρώεσσιν ὁμόκλα·
Il. 18.228	τρὶς δ: yes	τρὶς μὲν ὑπὲρ τάφρου μεγάλʼ ἴαχε δῖος Ἀχιλλεύς,  ||  next: τρὶς δὲ κυκήθησαν Τρῶες κλειτοί τʼ ἐπίκουροι.
Il. 20.445	τρὶς δ: yes	τρὶς μὲν ἔπειτʼ ἐπόρουσε ποδάρκης δῖος Ἀχιλλεὺς  ||  next: ἔγχεϊ χαλκείῳ, τρὶς δʼ ἠέρα τύψε βαθεῖαν.
Il. 21.176	τρὶς δ: yes	τρὶς μέν μιν πελέμιξεν ἐρύσσασθαι μενεαίνων,  ||  next: τρὶς δὲ μεθῆκε βίης· τὸ δὲ τέτρατον ἤθελε θυμῷ
Il. 23.817	τρὶς δ: yes	τρὶς μὲν ἐπήϊξαν, τρὶς δὲ σχεδὸν ὁρμήθησαν.  ||  next: ἔνθʼ Αἴας μὲν ἔπειτα κατʼ ἀσπίδα πάντοσʼ ἐΐσην
Od. 9.361	τρὶς δ: yes	τρὶς μὲν ἔδωκα φέρων, τρὶς δʼ ἔκπιεν ἀφραδίῃσιν.  ||  next: αὐτὰρ ἐπεὶ Κύκλωπα περὶ φρένας ἤλυθεν οἶνος,
Od. 11.206	τρὶς δ: yes	τρὶς μὲν ἐφωρμήθην, ἑλέειν τέ με θυμὸς ἀνώγει,  ||  next: τρὶς δέ μοι ἐκ χειρῶν σκιῇ εἴκελον ἢ καὶ ὀνείρῳ
Od. 12.105	τρὶς δ: yes	τρὶς μὲν γάρ τʼ ἀνίησιν ἐπʼ ἤματι, τρὶς δʼ ἀναροιβδεῖ  ||  next: δεινόν· μὴ σύ γε κεῖθι τύχοις, ὅτε ῥοιβδήσειεν·
Od. 21.125	τρὶς δ: yes	τρὶς μέν μιν πελέμιξεν ἐρύσσεσθαι μενεαίνων,  ||  next: τρὶς δὲ μεθῆκε βίης, ἐπιελπόμενος τό γε θυμῷ,
```

```
# [36d] python -I repname.py . 3
Od. 8.2 + 4	ὤρνυτʼ ἄρʼ ἐξ εὐνῆς ἱερὸν μένος Ἀλκινόοιο, || τοῖσιν δʼ ἡγεμόνευʼ ἱερὸν μένος Ἀλκινόοιο
-- pairs: 1

# [36e] python -I repname.py . 2
Il. 2.193 + 195	νῦν μὲν πειρᾶται, τάχα δʼ ἴψεται υἷας Ἀχαιῶν. || μή τι χολωσάμενος ῥέξῃ κακὸν υἷας Ἀχαιῶν·
Il. 14.388 + 390	Τρῶας δʼ αὖθʼ ἑτέρωθεν ἐκόσμει φαίδιμος Ἕκτωρ. || κυανοχαῖτα Ποσειδάων καὶ φαίδιμος Ἕκτωρ,
Il. 20.386 + 388	τὸν δʼ ἰθὺς μεμαῶτα βάλʼ ἔγχεϊ δῖος Ἀχιλλεὺς || δούπησεν δὲ πεσών, ὃ δʼ ἐπεύξατο δῖος Ἀχιλλεύς·
Il. 23.838 + 839	ἂν δʼ Αἴας Τελαμωνιάδης καὶ δῖος Ἐπειός. || ἑξείης δʼ ἵσταντο, σόλον δʼ ἕλε δῖος Ἐπειός,
Od. 1.396 + 398	τῶν κέν τις τόδʼ ἔχῃσιν, ἐπεὶ θάνε δῖος Ὀδυσσεύς· || καὶ δμώων, οὕς μοι ληίσσατο δῖος Ὀδυσσεύς.
Od. 8.2 + 4	ὤρνυτʼ ἄρʼ ἐξ εὐνῆς ἱερὸν μένος Ἀλκινόοιο, || τοῖσιν δʼ ἡγεμόνευʼ ἱερὸν μένος Ἀλκινόοιο
Od. 8.130 + 132	πὺξ δʼ αὖ Λαοδάμας, ἀγαθὸς πάϊς Ἀλκινόοιο. || τοῖς ἄρα Λαοδάμας μετέφη πάϊς Ἀλκινόοιο·
Od. 8.421 + 423	τοῖσιν δʼ ἡγεμόνευʼ ἱερὸν μένος Ἀλκινόοιο, || δή ῥα τότʼ Ἀρήτην προσέφη μένος Ἀλκινόοιο·
-- pairs: 8
```

### A.4 Line 44 (ἔκφερε; δ᾽ αὖτε; ὃ δ᾽ ἕσπετο; κέρδεα εἰδώς)

```
# [44a] python homer/concordance.py --ngram "ἔκφερ᾽"
Il. 23.259   [3-3.5]  νηῶν δʼ ἔκφερʼ ἄεθλα λέβητάς τε τρίποδάς τε    <ἔκφερʼ>
Il. 23.759   [1-1.5]  ἔκφερʼ Ὀϊλιάδης· ἐπὶ δʼ ὄρνυτο δῖος Ὀδυσσεὺς    <ἔκφερʼ>
Il. 23.785   [9-9.5]  Ἀντίλοχος δʼ ἄρα δὴ λοισθήϊον ἔκφερʼ ἄεθλον    <ἔκφερʼ>
-- 3 hit(s)

# [44b] python homer/concordance.py --loose "εκφερεν" --word
Od. 15.470   [1-2]  ἔκφερεν· αὐτὰρ ἐγὼν ἑπόμην ἀεσιφροσύνῃσι.    <ἔκφερεν>
-- 1 hit(s)

# [44c] python homer/concordance.py --loose "εκφερε" --word
-- 0 hit(s)

# context for ngram "ἔκφερ᾽ Ὀϊλιάδης" (-1/+1 lines): 1 hit(s)
  Il. 23.758   τοῖσι δʼ ἀπὸ νύσσης τέτατο δρόμος· ὦκα δʼ ἔπειτα
> Il. 23.759   ἔκφερʼ Ὀϊλιάδης· ἐπὶ δʼ ὄρνυτο δῖος Ὀδυσσεὺς
  Il. 23.760   ἄγχι μάλʼ, ὡς ὅτε τίς τε γυναικὸς ἐϋζώνοιο

# context for ngram "ἔκφερον ἵπποι" (-1/+1 lines): 1 hit(s)
  Il. 23.375   φαίνετʼ, ἄφαρ δʼ ἵπποισι τάθη δρόμος· ὦκα δʼ ἔπειτα
> Il. 23.376   αἳ Φηρητιάδαο ποδώκεες ἔκφερον ἵπποι.
  Il. 23.377   τὰς δὲ μετʼ ἐξέφερον Διομήδεος ἄρσενες ἵπποι

# [44d] python homer/concordance.py --ngram "δ᾽ αὖτε" (positions tabulated; hits at 3-3.5 listed)
    105 [2-3]
     19 [5-5.5]
     12 [11-12]
      5 [3-3.5]
Il. 23.316   [3-3.5]  μήτι δʼ αὖτε κυβερνήτης ἐνὶ οἴνοπι πόντῳ    <δʼ αὖτε>
Od. 2.203    [3-3.5]  χρήματα δʼ αὖτε κακῶς βεβρώσεται, οὐδέ ποτʼ ἶσα    <δʼ αὖτε>
Od. 3.402    [3-3.5]  αὐτὸς δʼ αὖτε καθεῦδε μυχῷ δόμου ὑψηλοῖο,    <δʼ αὖτε>
Od. 20.380   [3-3.5]  ἄλλος δʼ αὖτέ τις οὗτος ἀνέστη μαντεύεσθαι.    <δʼ αὖτέ>
Od. 24.278   [3-3.5]  χωρὶς δʼ αὖτε γυναῖκας, ἀμύμονα ἔργα ἰδυίας,    <δʼ αὖτε>

# [44f] python homer/concordance.py --ngram "ὃ δ᾽ ἕσπετο"
-- 0 hit(s)

# [44g] python homer/concordance.py --ngram "δ᾽ ἕσπετο"
Il. 12.398   [3-4]  ἕλχʼ, ἣ δʼ ἕσπετο πᾶσα διαμπερές, αὐτὰρ ὕπερθε    <δʼ ἕσπετο>
Od. 1.125    [7-8]  ὣς εἰπὼν ἡγεῖθʼ, ἡ δʼ ἕσπετο Παλλὰς Ἀθήνη.    <δʼ ἕσπετο>
Od. 8.109    [7-8]  βὰν δʼ ἴμεν εἰς ἀγορήν, ἅμα δʼ ἕσπετο πουλὺς ὅμιλος,    <δʼ ἕσπετο>
-- 3 hit(s)

# [44h] python homer/concordance.py --loose "εσπετο" --word
Il. 3.376    [7-8]  κεινὴ δὲ τρυφάλεια ἅμʼ ἕσπετο χειρὶ παχείῃ.    <ἕσπετο>
Il. 4.476    [7-8]  γείνατʼ, ἐπεί ῥα τοκεῦσιν ἅμʼ ἕσπετο μῆλα ἰδέσθαι·    <ἕσπετο>
Il. 11.472   [7-8]  ὣς εἰπὼν ὃ μὲν ἦρχʼ, ὃ δʼ ἅμʼ ἕσπετο ἰσόθεος φώς.    <ἕσπετο>
Il. 12.398   [3-4]  ἕλχʼ, ἣ δʼ ἕσπετο πᾶσα διαμπερές, αὐτὰρ ὕπερθε    <ἕσπετο>
Il. 13.300   [1-2]  ἕσπετο, ὅς τʼ ἐφόβησε ταλάφρονά περ πολεμιστήν·    <ἕσπετο>
Il. 13.492   [9-10]  λαοὶ ἕπονθʼ, ὡς εἴ τε μετὰ κτίλον ἕσπετο μῆλα    <ἕσπετο>
Il. 15.559   [7-8]  ὣς εἰπὼν ὃ μὲν ἦρχʼ, ὃ δʼ ἅμʼ ἕσπετο ἰσόθεος φώς·    <ἕσπετο>
Il. 16.632   [7-8]  ὣς εἰπὼν ὃ μὲν ἦρχʼ, ὃ δʼ ἅμʼ ἕσπετο ἰσόθεος φώς.    <ἕσπετο>
Od. 1.125    [7-8]  ὣς εἰπὼν ἡγεῖθʼ, ἡ δʼ ἕσπετο Παλλὰς Ἀθήνη.    <ἕσπετο>
Od. 6.164    [9-10]  ἦλθον γὰρ καὶ κεῖσε, πολὺς δέ μοι ἕσπετο λαός,    <ἕσπετο>
Od. 8.109    [7-8]  βὰν δʼ ἴμεν εἰς ἀγορήν, ἅμα δʼ ἕσπετο πουλὺς ὅμιλος,    <ἕσπετο>
Od. 17.53    [7-8]  ξεῖνον, ὅτις μοι κεῖθεν ἅμʼ ἕσπετο δεῦρο κιόντι.    <ἕσπετο>
-- 12 hit(s)

# [44j] python homer/concordance.py --loose "επετο" --word
Il. 11.165   [3.5-5]  Ἀτρεΐδης δʼ ἕπετο σφεδανὸν Δαναοῖσι κελεύων.    <ἕπετο>
Il. 13.644   [7.5-9]  Ἁρπαλίων, ὅ ῥα πατρὶ φίλῳ ἕπετο πτολεμίξων    <ἕπετο>
Il. 16.372   [3.5-5]  Πάτροκλος δʼ ἕπετο σφεδανὸν Δαναοῖσι κελεύων    <ἕπετο>
Il. 21.256   [5.5-7]  φεῦγʼ, ὃ δʼ ὄπισθε ῥέων ἕπετο μεγάλῳ ὀρυμαγδῷ.    <ἕπετο>
-- 4 hit(s)

# [44k] python homer/concordance.py --loose "εσπομενος" --word
Il. 12.395   [7-9]  νύξʼ, ἐκ δʼ ἔσπασεν ἔγχος· ὃ δʼ ἑσπόμενος πέσε δουρὶ    <ἑσπόμενος>
Il. 13.570   [7-9]  ἔνθά οἱ ἔγχος ἔπηξεν· ὃ δʼ ἑσπόμενος περὶ δουρὶ    <ἑσπόμενος>
-- 2 hit(s)

# context for ngram "ὃ δ᾽ ἅμ᾽ ἕσπετο ἰσόθεος φώς" (-0/+0 lines): 3 hit(s)
> Il. 11.472   ὣς εἰπὼν ὃ μὲν ἦρχʼ, ὃ δʼ ἅμʼ ἕσπετο ἰσόθεος φώς.

> Il. 15.559   ὣς εἰπὼν ὃ μὲν ἦρχʼ, ὃ δʼ ἅμʼ ἕσπετο ἰσόθεος φώς·

> Il. 16.632   ὣς εἰπὼν ὃ μὲν ἦρχʼ, ὃ δʼ ἅμʼ ἕσπετο ἰσόθεος φώς.

# [44i] python homer/concordance.py --ngram "κέρδεα εἰδώς"
Il. 23.709   [9-12]  ἂν δʼ Ὀδυσεὺς πολύμητις ἀνίστατο κέρδεα εἰδώς.    <κέρδεα εἰδώς>
-- 1 hit(s)

```

### A.5 Line 51 (τὴν μὲν … τὴν δ᾽ αὖ; Σέρβου κρατεροῖο)

```
# context for ngram "τὴν δ᾽ Ἕκτορος ἱπποδάμοιο" (-1/+1 lines): 1 hit(s)
  Il. 22.210   ἐν δʼ ἐτίθει δύο κῆρε τανηλεγέος θανάτοιο,
> Il. 22.211   τὴν μὲν Ἀχιλλῆος, τὴν δʼ Ἕκτορος ἱπποδάμοιο,
  Il. 22.212   ἕλκε δὲ μέσσα λαβών· ῥέπε δʼ Ἕκτορος αἴσιμον ἦμαρ,

# [51a] python homer/concordance.py --ngram "τὴν μὲν ἄρ᾽"
Il. 5.353    [1-2]  τὴν μὲν ἄρʼ Ἶρις ἑλοῦσα ποδήνεμος ἔξαγʼ ὁμίλου    <τὴν μὲν ἄρʼ>
Il. 18.148   [1-2]  τὴν μὲν ἄρʼ Οὔλυμπον δὲ πόδες φέρον· αὐτὰρ Ἀχαιοὶ    <τὴν μὲν ἄρʼ>
Od. 19.440   [1-2]  τὴν μὲν ἄρʼ οὔτʼ ἀνέμων διάει μένος ὑγρὸν ἀέντων,    <τὴν μὲν ἄρʼ>
-- 3 hit(s)

# [51b] python homer/concordance.py --ngram "τὴν δ᾽ αὖ"
Od. 1.213    [1-2]  τὴν δʼ αὖ Τηλέμαχος πεπνυμένος ἀντίον ηὔδα·    <τὴν δʼ αὖ>
Od. 1.230    [1-2]  τὴν δʼ αὖ Τηλέμαχος πεπνυμένος ἀντίον ηὔδα·    <τὴν δʼ αὖ>
Od. 1.306    [1-2]  τὴν δʼ αὖ Τηλέμαχος πεπνυμένος ἀντίον ηὔδα·    <τὴν δʼ αὖ>
Od. 1.345    [1-2]  τὴν δʼ αὖ Τηλέμαχος πεπνυμένος ἀντίον ηὔδα·    <τὴν δʼ αὖ>
Od. 2.371    [1-2]  τὴν δʼ αὖ Τηλέμαχος πεπνυμένος ἀντίον ηὔδα·    <τὴν δʼ αὖ>
Od. 3.21     [1-2]  τὴν δʼ αὖ Τηλέμαχος πεπνυμένος ἀντίον ηὔδα·    <τὴν δʼ αὖ>
Od. 3.239    [1-2]  τὴν δʼ αὖ Τηλέμαχος πεπνυμένος ἀντίον ηὔδα·    <τὴν δʼ αὖ>
Od. 15.179   [1-2]  τὴν δʼ αὖ Τηλέμαχος πεπνυμένος ἀντίον ηὔδα·    <τὴν δʼ αὖ>
Od. 17.45    [1-2]  τὴν δʼ αὖ Τηλέμαχος πεπνυμένος ἀντίον ηὔδα·    <τὴν δʼ αὖ>
Od. 17.107   [1-2]  τὴν δʼ αὖ Τηλέμαχος πεπνυμένος ἀντίον ηὔδα·    <τὴν δʼ αὖ>
Od. 18.226   [1-2]  τὴν δʼ αὖ Τηλέμαχος πεπνυμένος ἀντίον ηὔδα·    <τὴν δʼ αὖ>
Od. 19.26    [1-2]  τὴν δʼ αὖ Τηλέμαχος πεπνυμένος ἀντίον ηὔδα·    <τὴν δʼ αὖ>
Od. 21.343   [1-2]  τὴν δʼ αὖ Τηλέμαχος πεπνυμένος ἀντίον ηὔδα·    <τὴν δʼ αὖ>
-- 13 hit(s)

# [51c] python -I menau.py .
next verse  Il. 8.323-324	ἤτοι ὃ μὲν φαρέτρης ἐξείλετο πικρὸν ὀϊστόν, / θῆκε δʼ ἐπὶ νευρῇ· τὸν δʼ αὖ κορυθαίολος Ἕκτωρ
next verse  Od. 19.307-308	τοῦ μὲν φθίνοντος μηνός, τοῦ δʼ ἱσταμένοιο. / τὸν δʼ αὖτε προσέειπε περίφρων Πηνελόπεια·
-- hits: 2

# [51j] python homer/concordance.py --regex "(ἄλλ|ἑτέρ)[^ ]* δʼ αὖ(\s|[,.·;]|$)"
Il. 18.602   [1-3]  ἄλλοτε δʼ αὖ θρέξασκον ἐπὶ στίχας ἀλλήλοισι.    <ἄλλοτε δʼ αὖ >
Od. 8.174    [1-3]  ἄλλος δʼ αὖ εἶδος μὲν ἀλίγκιος ἀθανάτοισιν,    <ἄλλος δʼ αὖ >
Od. 21.401   [1-3]  ἄλλος δʼ αὖ εἴπεσκε νέων ὑπερηνορεόντων·    <ἄλλος δʼ αὖ >
-- 3 hit(s)

# context for ngram "ἄλλος δ᾽ αὖ εἶδος μὲν" (-5/+0 lines): 1 hit(s)
  Od. 8.169   ἄλλος μὲν γάρ τʼ εἶδος ἀκιδνότερος πέλει ἀνήρ,
  Od. 8.170   ἀλλὰ θεὸς μορφὴν ἔπεσι στέφει, οἱ δέ τʼ ἐς αὐτὸν
  Od. 8.171   τερπόμενοι λεύσσουσιν· ὁ δʼ ἀσφαλέως ἀγορεύει
  Od. 8.172   αἰδοῖ μειλιχίῃ, μετὰ δὲ πρέπει ἀγρομένοισιν,
  Od. 8.173   ἐρχόμενον δʼ ἀνὰ ἄστυ θεὸν ὣς εἰσορόωσιν.
> Od. 8.174   ἄλλος δʼ αὖ εἶδος μὲν ἀλίγκιος ἀθανάτοισιν,

# context for ngram "ἄλλοτε δ᾽ αὖ θρέξασκον" (-3/+0 lines): 1 hit(s)
  Il. 18.599   οἳ δʼ ὁτὲ μὲν θρέξασκον ἐπισταμένοισι πόδεσσι
  Il. 18.600   ῥεῖα μάλʼ, ὡς ὅτε τις τροχὸν ἄρμενον ἐν παλάμῃσιν
  Il. 18.601   ἑζόμενος κεραμεὺς πειρήσεται, αἴ κε θέῃσιν·
> Il. 18.602   ἄλλοτε δʼ αὖ θρέξασκον ἐπὶ στίχας ἀλλήλοισι.

# [51e] python homer/concordance.py --loose "κρατεροιο" --word
Il. 13.60    [9.5-12]  ἀμφοτέρω κεκοπὼς πλῆσεν μένεος κρατεροῖο,    <κρατεροῖο>
Il. 13.415   [9.5-12]  εἰς Ἄϊδός περ ἰόντα πυλάρταο κρατεροῖο    <κρατεροῖο>
Il. 23.848   [9.5-12]  ἀνστάντες δʼ ἕταροι Πολυποίταο κρατεροῖο    <κρατεροῖο>
Od. 4.335    [7.5-9.5]  ὡς δʼ ὁπότʼ ἐν ξυλόχῳ ἔλαφος κρατεροῖο λέοντος    <κρατεροῖο>
Od. 11.277   [9.5-12]  ἡ δʼ ἔβη εἰς Ἀίδαο πυλάρταο κρατεροῖο,    <κρατεροῖο>
Od. 17.126   [7.5-9.5]  ὡς δʼ ὁπότʼ ἐν ξυλόχῳ ἔλαφος κρατεροῖο λέοντος    <κρατεροῖο>
Od. 24.170   [7.5-9.5]  οὐδέ τις ἡμείων δύνατο κρατεροῖο βιοῖο    <κρατεροῖο>
-- 7 hit(s)

# [51h] python homer/concordance.py --regex "[^ ]ου [^ ]+οιο[,.·;]?$" --count
38

# [51i] python homer/concordance.py --regex "[Α-ΩἈ-ᾯῈ-Ὼ][^ ]*ου [^ ]+οιο[,.·;]?$"
Il. 4.100    [5.5-12]  ἀλλʼ ἄγʼ ὀΐστευσον Μενελάου κυδαλίμοιο,    <Μενελάου κυδαλίμοιο,>
Il. 4.177    [5.5-12]  τύμβῳ ἐπιθρῴσκων Μενελάου κυδαλίμοιο·    <Μενελάου κυδαλίμοιο·>
Il. 7.392    [5.5-12]  κουριδίην δʼ ἄλοχον Μενελάου κυδαλίμοιο    <Μενελάου κυδαλίμοιο>
Il. 9.440    [6-12]  νήπιον οὔ πω εἰδόθʼ ὁμοιΐου πολέμοιο    <ὁμοιΐου πολέμοιο>
Il. 11.373   [6-12]  ἤτοι ὃ μὲν θώρηκα Ἀγαστρόφου ἰφθίμοιο    <Ἀγαστρόφου ἰφθίμοιο>
Il. 13.358   [6-12]  τοὶ δʼ ἔριδος κρατερῆς καὶ ὁμοιΐου πτολέμοιο    <ὁμοιΐου πτολέμοιο>
Il. 13.591   [5.5-12]  ὣς ἀπὸ θώρηκος Μενελάου κυδαλίμοιο    <Μενελάου κυδαλίμοιο>
Il. 13.601   [5.5-12]  Πείσανδρος δʼ ἰθὺς Μενελάου κυδαλίμοιο    <Μενελάου κυδαλίμοιο>
Il. 13.606   [5.5-12]  Πείσανδρος δὲ σάκος Μενελάου κυδαλίμοιο    <Μενελάου κυδαλίμοιο>
Il. 13.635   [6-12]  φυλόπιδος κορέσασθαι ὁμοιΐου πτολέμοιο.    <ὁμοιΐου πτολέμοιο.>
Il. 15.670   [6-12]  ἠμὲν πρὸς νηῶν καὶ ὁμοιΐου πολέμοιο.    <ὁμοιΐου πολέμοιο.>
Il. 17.69    [5.5-12]  ἀντίον ἐλθέμεναι Μενελάου κυδαλίμοιο.    <Μενελάου κυδαλίμοιο.>
Il. 18.242   [6-12]  φυλόπιδος κρατερῆς καὶ ὁμοιΐου πολέμοιο.    <ὁμοιΐου πολέμοιο.>
Il. 21.294   [6-12]  μὴ πρὶν παύειν χεῖρας ὁμοιΐου πολέμοιο    <ὁμοιΐου πολέμοιο>
Od. 4.2      [5.5-12]  πρὸς δʼ ἄρα δώματʼ ἔλων Μενελάου κυδαλίμοιο.    <Μενελάου κυδαλίμοιο.>
Od. 4.16     [5.5-12]  γείτονες ἠδὲ ἔται Μενελάου κυδαλίμοιο,    <Μενελάου κυδαλίμοιο,>
Od. 4.23     [5.5-12]  ὀτρηρὸς θεράπων Μενελάου κυδαλίμοιο,    <Μενελάου κυδαλίμοιο,>
Od. 4.46     [5.5-12]  δῶμα καθʼ ὑψερεφὲς Μενελάου κυδαλίμοιο.    <Μενελάου κυδαλίμοιο.>
Od. 4.217    [5.5-12]  ὀτρηρὸς θεράπων Μενελάου κυδαλίμοιο.    <Μενελάου κυδαλίμοιο.>
Od. 14.182   [6-12]  νώνυμον ἐξ Ἰθάκης Ἀρκεισίου ἀντιθέοιο.    <Ἀρκεισίου ἀντιθέοιο.>
Od. 15.5     [5.5-12]  εὕδοντʼ ἐν προδόμῳ Μενελάου κυδαλίμοιο,    <Μενελάου κυδαλίμοιο,>
Od. 15.141   [5.5-12]  οἰνοχόει δʼ υἱὸς Μενελάου κυδαλίμοιο.    <Μενελάου κυδαλίμοιο.>
Od. 15.507   [7-12]  δαῖτʼ ἀγαθὴν κρειῶν τε καὶ οἴνου ἡδυπότοιο.    <ἴνου ἡδυπότοιο.>
Od. 18.264   [6-12]  ἔκριναν μέγα νεῖκος ὁμοιΐου πολέμοιο.    <ὁμοιΐου πολέμοιο.>
Od. 24.543   [6-12]  ἴσχεο, παῦε δὲ νεῖκος ὁμοιΐου πολέμοιο,    <ὁμοιΐου πολέμοιο,>
-- 25 hit(s)

# [51f] python homer/concordance.py --ngram "ἀνδρῶν Ἀγαμέμνων" --count
36

# [51g] python homer/concordance.py --ngram "κνίσῃ ἐκάλυψαν"
Il. 1.460    [8-12]  μηρούς τʼ ἐξέταμον κατά τε κνίσῃ ἐκάλυψαν    <κνίσῃ ἐκάλυψαν>
Il. 2.423    [8-12]  μηρούς τʼ ἐξέταμον κατά τε κνίσῃ ἐκάλυψαν    <κνίσῃ ἐκάλυψαν>
Od. 3.457    [8-12]  πάντα κατὰ μοῖραν, κατά τε κνίσῃ ἐκάλυψαν    <κνίσῃ ἐκάλυψαν>
Od. 12.360   [8-12]  μηρούς τʼ ἐξέταμον κατά τε κνίσῃ ἐκάλυψαν    <κνίσῃ ἐκάλυψαν>
-- 4 hit(s)

```

```
# [51k] Ζοκοβείδαο slot test (jsonl 51 notes): python homer/check_line.py "τοῦ Ζοκοβείδαο κρατεροῦ μένος ἀντιθέοιο"
[1] τοῦ Ζοκοβείδαο κρατεροῦ μένος ἀντιθέοιο
  DSDDDS  (unique, tier 0, 1 scansion(s))
  syllables: τοῦ Ζο.κο.βεί.δα.ο κρα.τε.ροῦ μέ.νος ἀν.τι.θέ.οι.ο
  positions: 1 1.5 2 3 4 5 5.5 6 7 7.5 8 9 9.5 10 11 12
  quantities by word: L SSLLL SSL SS LSSLX
  caesurae: penthemimeral, hephthemimeral; bucolic diaeresis: D
  licences: -
  warn quantity_unattested: α in 'Ζοκοβείδαο' taken as L (metre only); no unambiguous Homeric attestation of this form
  warn quantity_unattested: ι in 'ἀντιθέοιο' taken as S (metre only); no unambiguous Homeric attestation of this form
  OK (no flags)

exit=0

# [51l] python homer/concordance.py --loose "πηλειδαο" --word
Il. 15.74    [3-5.5]  πρίν γε τὸ Πηλεΐδαο τελευτηθῆναι ἐέλδωρ,    <Πηλεΐδαο>
Il. 15.614   [7-9.5]  Παλλὰς Ἀθηναίη ὑπὸ Πηλεΐδαο βίηφιν.    <Πηλεΐδαο>
Il. 17.199   [3-5.5]  τεύχεσι Πηλεΐδαο κορυσσόμενον θείοιο,    <Πηλεΐδαο>
Il. 21.208   [3-5.5]  χέρσʼ ὕπο Πηλεΐδαο καὶ ἄορι ἶφι δαμέντα.    <Πηλεΐδαο>
Il. 22.290   [3-5.5]  καὶ βάλε Πηλεΐδαο μέσον σάκος οὐδʼ ἀφάμαρτε·    <Πηλεΐδαο>
-- 5 hit(s)

```

### A.6 Line 56 (ἔνθ᾽ αὖθ᾽) and the patronymic (P1)

```
# [56a] python homer/concordance.py --ngram "ἔνθ᾽ αὖθ᾽"
-- 0 hit(s)

# [56b] python homer/concordance.py --ngram "ἔνθ᾽ αὖτ᾽" --count
12

# [56c] python homer/concordance.py --ngram "αὖθ᾽ ἱερεὺς"
Il. 1.370    [3-5]  Χρύσης δʼ αὖθʼ ἱερεὺς ἑκατηβόλου Ἀπόλλωνος    <αὖθʼ ἱερεὺς>
-- 1 hit(s)

# context for ngram "Ἀμαρυγκείδην" (-5/+3 lines): 1 hit(s)
  Il. 4.512   οὐ μὰν οὐδʼ Ἀχιλεὺς Θέτιδος πάϊς ἠϋκόμοιο
  Il. 4.513   μάρναται, ἀλλʼ ἐπὶ νηυσὶ χόλον θυμαλγέα πέσσει.
  Il. 4.514   ὣς φάτʼ ἀπὸ πτόλιος δεινὸς θεός· αὐτὰρ Ἀχαιοὺς
  Il. 4.515   ὦρσε Διὸς θυγάτηρ κυδίστη Τριτογένεια
  Il. 4.516   ἐρχομένη καθʼ ὅμιλον, ὅθι μεθιέντας ἴδοιτο.
> Il. 4.517   ἔνθʼ Ἀμαρυγκείδην Διώρεα μοῖρα πέδησε·
  Il. 4.518   χερμαδίῳ γὰρ βλῆτο παρὰ σφυρὸν ὀκριόεντι
  Il. 4.519   κνήμην δεξιτερήν· βάλε δὲ Θρῃκῶν ἀγὸς ἀνδρῶν
  Il. 4.520   Πείρως Ἰμβρασίδης ὃς ἄρʼ Αἰνόθεν εἰληλούθει.

# [P1] python homer/concordance.py --loose "αμαρυγκε"
Il. 2.622    [1.5-5]  τῶν δʼ Ἀμαρυγκεΐδης ἦρχε κρατερὸς Διώρης·    <Ἀμαρυγκε>
Il. 4.517    [1.5-5]  ἔνθʼ Ἀμαρυγκείδην Διώρεα μοῖρα πέδησε·    <Ἀμαρυγκε>
Il. 23.630   [5.5-8]  ὡς ὁπότε κρείοντʼ Ἀμαρυγκέα θάπτον Ἐπειοὶ    <Ἀμαρυγκέ>
-- 3 hit(s)

```

### A.7 Lexica (Logeion API, fetched 2026-10-07: anastrophe.uchicago.edu/logeion-api/detail?w=…; LSJ and 'Cunliffe Homer' entries, HTML stripped by dico_text.py; excerpts)

```
# Cunliffe ἐκφέρω, sense 6:
6 Intrans. for reflexive, to draw away from competitors in a race, shoot ahead (cf. ὑπεκφέρω 3) Il. 23.376, 377, 759. 
# LSJ ἐκφέρω, intransitive:
intr. (sc. ἑαυτόν ) shoot forth (before the rest), ὦκα δʼ ἔπειτα αἱ Φηρητιάδαο . . ἔκφερον ἵπποι· τὰς δὲ μέτʼ ἐξέφερον Διομήδεος . . ἵπποι Il. 23.376, cf. 759; also, to run away, 
# Cunliffe ἕπομαι, senses 1a, 6a, 8:
1 a To follow in company with, go or come with, accompany, a person or persons or something : ἀλλʼ ἕπεο Il. 10.146. Cf. Il. 10.246, Il. 13.381, 
6 a To follow up, hang upon, the foe : αἰὲν ἀποκτείνων ἕπετο Il. 11.154. Cf. Il. 11.165, 168, 565, 754, Il. 15.277, Il. 16.372, Il. 17.730. Of flowing water Il. 21.256. b With ἅμα: Τρῶες ἅμʼ 
8 To keep up with, play one’s part with . With dat.: ἕπεθʼ ἵπποις ἀθανάτοισιν Il. 16.154. Sim. of the limbs, to keep up with one’s spirit
# LSJ ἕπομαι I.3-4:
3 in hostile sense, pursue, Il. 11.154, etc.; ἀμφὶ δʼ ἄρʼ αὐτὸν ἕποντο they pressed upon him, ib. 
4 keep pace with, ὃς καὶ θνητὸς ἐὼν ἕπεθʼ ἵπποις ἀθανάτοισι Il. 16.154, cf. Od. 6.319:
# Cunliffe αὖτις, senses 1 and 3:
αὖτις 1 In the reverse direction, backwards, back, back again : ἴτην Il. 1.347, ἐλεύσεται 425. Cf. Il. 1.522, Il
3 Again, once more : ἰόντα Il. 1.27. Cf. Il. 1.513, Il. 7.170, Il. 10.463 ( as on former occasions ), Il. 18.153, Il. 22.449 ( giving changed orders ), etc.: αὐ. οἱ πόρον οἶνον Od. 9.360. Cf. Od. 3.161, Od. 9.354, Od. 
# LSJ αὖθις II:
II of Time, again, anew, Il. 4.222, etc.; freq. strengthd., ὕστερον αὖ. 1.27, cf. S
# LSJ βάλλω (hit):
with acc. of person or thing aimed at, throw so as to hit, hit with a missile, freq. opp. striking with a weapon in the hand, βλήμενος ἠὲ τυπείς Il. 15.495; τὸν βάλεν, οὐδʼ ἀφάμαρτε 11.350, cf. 4.473, al.; s
# Cunliffe βάλλω II.1a and I.2 (absolute):
2 To throw or let fly (a missile) : χαλκόν Il. 5.317 = 346: βέλος Od. 9.495. Cf. Od. 9.482, 539, Od. 20.62. Absol.: μὴ βάλλετε Il. 
1 a To strike or wound (a person, etc.) with a missile, and in pass., to be so struck or wounded : υἱὸν Πριάμοιο Il. 4.499, βεβλημέν
# Cunliffe ἔπειτα 1 and 4 (resumptive use):
1 Then, thereupon, after that : πολλὰ δʼ ἐ. ἠρᾶτο Il. 1.35,
Resuming and restating, then : ἐπόρουσε . . . τρὶς ἐ. ἐπόρουσεν Il. 5.436. Cf. Il. 20.445, etc.: Od. 3.62, etc. 
```

### A.8 Enjambment labels (jsonl v2 and v3; v2 reviewer labels from philology_v2.md §7)

```
# [ENJ] python -I enj.py .
v3 labels that differ from the v2 composer or v2 reviewer label of the same verse (n, v2 composer, v3 composer, v2 reviewer): [(36, 'none', 'unperiodic', 'none')]
v3 composer: {'none': 31, 'unperiodic': 19, 'necessary': 10}
unperiodic [2, 6, 7, 8, 14, 22, 26, 29, 34, 36, 38, 41, 48, 49, 50, 51, 53, 56, 59]
necessary [1, 3, 16, 17, 18, 37, 39, 45, 46, 47]
line-final punctuation: [(22, ','), (23, '.'), (24, '·'), (32, '·'), (33, '·'), (34, ','), (35, '.'), (36, ','), (37, ','), (38, 'ς'), (43, '·'), (44, '.'), (45, 'ι'), (50, ','), (51, ','), (52, '.'), (54, '·'), (55, '·'), (56, ','), (57, '.')]
```

## Appendix B. Scripts

Saved under the session scratchpad and reproduced here verbatim. Run from the repository root with `.venv` active; the Python scripts take the repository path (and, where needed, a draft path) as arguments and are run with `python -I`.

### B.1 identity.py (v3 vs v2 verses)

```python
# which v3 verses are character-identical to the v2 verse named in v3.jsonl v2_line; v3.txt = v3.jsonl text; jsonl 'changed' flag agrees
import json, sys
d = sys.argv[1]
v2 = {r['n']: r['text'] for r in map(json.loads, open(f'{d}/v2.jsonl', encoding='utf-8'))}
v2txt = open(f'{d}/v2.txt', encoding='utf-8').read().splitlines()
v3 = [json.loads(l) for l in open(f'{d}/v3.jsonl', encoding='utf-8')]
txt = open(f'{d}/v3.txt', encoding='utf-8').read().splitlines()
assert len(txt) == len(v3) == 60, (len(txt), len(v3))
same, changed, new, flagmis = [], [], [], []
for r in v3:
    assert txt[r['n'] - 1] == r['text'], r['n']
    m = r.get('v2_line')
    if m is None: new.append(r['n']); continue
    assert v2txt[m-1] == v2[m]
    if v2[m] == r['text']: same.append((r['n'], m))
    else: changed.append((r['n'], m))
    if bool(r.get('changed')) != (v2[m] != r['text']): flagmis.append(r['n'])
print('v3.txt == v3.jsonl text: 60/60')
print('identical to v2 (v3 n = v2 n):', len(same), ', '.join(f'{a}={b}' for a, b in same))
print('changed (v3 n <- v2 n):', len(changed), ', '.join(f'{a}<-{b}' for a, b in changed))
print('new:', new, '| jsonl "changed" flag disagrees with text diff:', flagmis)
```

### B.2 ctx.py (hits with context lines)

```python
# usage: python -I ctx.py REPO "query" BEFORE AFTER [mode]  -> each hit with context lines (mode: ngram|exact|regex|loose_word)
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

### B.3 q.sh (tagged concordance call)

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

### B.4 trismen.py (τρὶς μέν and its answering member)

```python
# every Homeric line with "τρὶς μέν": is a τρὶς δ(έ/ʼ) in the same or next 2 lines? what opens the next line?
import sys, re
sys.path.insert(0, sys.argv[1] + '/homer')
from concordance import Concordance
import greek as G
c = Concordance(); L = c.lines
for i, l in enumerate(L):
    if 'τρισ μεν' not in G.loose(l.text): continue
    nxt = [L[j] for j in range(i+1, min(i+3, len(L))) if L[j].book == l.book and L[j].work == l.work]
    after = G.loose(l.text).split('τρισ μεν', 1)[1]
    has = bool(re.search(r'τρισ δ', after)) or any(re.search(r'τρισ δ', G.loose(n.text)) for n in nxt)
    print(f'{l.work}. {l.book}.{l.line}\t{"τρὶς δ: yes" if has else "τρὶς δ: NO "}\t{l.text}  ||  next: {nxt[0].text if nxt else "-"}')
```

### B.5 repname.py (verse-final name formula repeated within two verses)

```python
# Homeric verses whose last three words (a name-epithet formula of 6-12 shape such as βοὴν ἀγαθὸς Διομήδης) recur within the next 2 verses
import sys, re
sys.path.insert(0, sys.argv[1] + '/homer')
from concordance import Concordance
import greek as G
K = int(sys.argv[2]) if len(sys.argv) > 2 else 3
c = Concordance(); L = c.lines
def tail(t): 
    w = [G.loose(x) for x in re.findall(r"[^\s,.·;:!]+", t)]
    return ' '.join(w[-K:])
n = 0
for i, l in enumerate(L[:-2]):
    t = tail(l.text)
    last = re.findall(r"[^\s,.·;:!]+", l.text)[-1]
    if not last[:1].isupper(): continue
    for j in (i+1, i+2):
        if L[j].book == l.book and L[j].work == l.work and tail(L[j].text) == t:
            n += 1; print(f'{l.work}. {l.book}.{l.line} + {L[j].line}\t{l.text} || {L[j].text}')
print('-- pairs:', n)
```

### B.6 menau.py (pronoun μέν … pronoun δ᾽ αὖ)

```python
# "τὸν/τὴν/τὸ μέν ... τὸν/τὴν/τὸ δʼ αὖ(τε)" within one verse or across two consecutive verses (the contrast of line 51)
import sys, re
sys.path.insert(0, sys.argv[1] + '/homer')
from concordance import Concordance
c = Concordance(); L = c.lines
A = re.compile(r'(^|\s)(τὸν|τὴν|τὸ|τοὺς|τὰς|τὰ|τοῦ|τῆς|τῷ|τῇ|ὃ|ἣ|οἳ|αἳ|ὁ|ἡ) μὲν\b')
B = re.compile(r'(^|\s)(τὸν|τὴν|τὸ|τοὺς|τὰς|τὰ|τοῦ|τῆς|τῷ|τῇ|ὃ|ἣ|οἳ|αἳ|ὁ|ἡ) δʼ αὖ(τε|τʼ|θʼ)?(\s|[,.·;]|$)')
n = 0
for i, l in enumerate(L):
    m = A.search(l.text)
    if not m: continue
    rest = l.text[m.end():]
    same = B.search(rest)
    nxt = L[i+1] if i + 1 < len(L) and L[i+1].book == l.book and L[i+1].work == l.work else None
    if same:
        n += 1; print(f'same verse  {l.work}. {l.book}.{l.line}\t{l.text}')
    elif nxt and B.search(nxt.text):
        n += 1; print(f'next verse  {l.work}. {l.book}.{l.line}-{nxt.line}\t{l.text} / {nxt.text}')
print('-- hits:', n)
```

### B.7 aspir.py (elision before rough breathing)

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

### B.7a accent.py (accent of -η/ω + C + ος)

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

### B.8 rulings.py (R2-R12 forms, names, prohibited words)

```python
# Ruling and lexicon checks on a draft: R2-R6 and R9-R11 forms, Djokovic/Federer name forms, prohibited words (loose forms, homer/greek.py)
import sys, re, unicodedata as U
sys.path.insert(0, sys.argv[1] + '/homer')
import greek as G
lines = [l.rstrip('\n') for l in open(sys.argv[2], encoding='utf-8')]
def raw(l): return re.findall(r"[^\s,.·;:!]+", l)
def words(l): return [G.loose(w) for w in raw(l)]
checks = {
 'R2 ἰσόθεος': lambda w, r: w.startswith('ισοθε'),
 'R3 withdrawn Ζοκοβίδης/Νοβάκος': lambda w, r: w.startswith('ζοκοβιδ') or w.startswith('νοβακ'),
 'R4 δίς': lambda w, r: w == 'δισ',
 'R5 ἐξεναρίζω': lambda w, r: w.startswith('εξεναρ'),
 'R6 πάλιν': lambda w, r: w == 'παλιν',
 'R9 Νοβ- with acute (Νοβήκ-)': lambda w, r: w.startswith('νοβηκ') and 'ή' in U.normalize('NFC', r),
 'R9 Νοβῆκος (circumflex)': lambda w, r: w.startswith('νοβηκ') and 'ῆ' in U.normalize('NFC', r),
 'R10 Ζοκοβεύς / Ζοκοβῆ- (eponym forms)': lambda w, r: w.startswith('ζοκοβευ') or w.startswith('ζοκοβη'),
 'Ζοκοβείδης (patronymic)': lambda w, r: w.startswith('ζοκοβειδ'),
 'Σέρβ- (ethnic)': lambda w, r: w.startswith('σερβ'),
 'δαμάζω (aor.)': lambda w, r: re.match(r'ε?δαμασ', w) is not None,
 'prohibited (γραμμ, στεγ, οχλ, ωρη/ωρα, δικτυ, ραβδ, χλο, χορτ, δικαστ, αθλητησ, σφαιριστ, ηττ)':
     lambda w, r: re.match(r'(γραμμ|στεγ|οχλ|ωρη|ωρα|ωρ$|δικτυ|ραβδ|χλο[ηυ]|χορτ|δικαστ|αθλητη[σν]|σφαιριστ|ηττ)', w) is not None,
}
for name, f in checks.items():
    hits = [(i, r) for i, l in enumerate(lines, 1) for w, r in zip(words(l), raw(l)) if f(w, r)]
    print(f'{name}: {len(hits)}', hits)
print('R11 "δεύτερον αὖτις":', [i for i, l in enumerate(lines, 1) if 'δευτερον αυτισ' in ' '.join(words(l))])
print('"καὶ βάλεν … καὶ βάλεν" (two hit clauses):', [i for i, l in enumerate(lines, 1) if ' '.join(words(l)).count('και βαλεν') == 2])
print('"τὸ τέταρτον" lines and the subject named in the verse before:', [(i, raw(lines[i-2])[-1]) for i, l in enumerate(lines, 1) if 'το τεταρτον' in ' '.join(words(l))])
```

### B.9 tally.py (counts in §2 and §4)

```python
# python3 tally.py review/philology_v3.md   (prints the counts in §2 and §4 from the per-line table, section "## 6.")
import re, sys, collections
rows = []; inside = False
for line in open(sys.argv[1], encoding='utf-8'):
    if line.startswith('## '): inside = line.startswith('## 6.')
    if not inside or not re.match(r'^\| \d+ \|', line): continue
    cells = [c.strip() for c in re.split(r'(?<!\\)\|', line.strip())[1:-1]]
    comp, rev = [x.strip() for x in cells[-1].split('→')]
    rows.append((int(cells[0]), cells[1], comp, rev, cells[2]))
assert [r[0] for r in rows] == list(range(1, len(rows) + 1)), [r[0] for r in rows]
N = len(rows); v = collections.Counter(r[1] for r in rows)
print('lines', N); print('verdicts', dict(v))
for k in ('FAIL', 'QUERY'): print(k, [r[0] for r in rows if r[1] == k])
print('rows "Unchanged, v2 PASS":', sum(1 for r in rows if r[4].startswith('Unchanged, v2 PASS')))
for who, i in (('composer', 2), ('reviewer', 3)):
    c = collections.Counter(r[i] for r in rows)
    print(who, {t: f"{c[t]} ({100*c[t]/N:.1f}%)" for t in ('none', 'unperiodic', 'necessary')})
    print('  necessary lines', [r[0] for r in rows if r[i] == 'necessary'])
print('disagreements', [(r[0], r[2], r[3]) for r in rows if r[2] != r[3]])
```

### B.10 appendix.sh (writes Appendix A)

```bash
#!/bin/bash
# usage (repo root, .venv active): appendix.sh SCRIPTDIR LSJDIR  -> prints Appendix A of philology_v3.md
S=$1; D=$2; Q=$S/q.sh
export LC_ALL=C.utf8   # grep -o '.{0,N}' must count characters, not bytes
fence() { echo '```'; "$@" 2>&1; echo '```'; echo; }
echo "### A.0 Identity, check_line, rulings, aspiration, accent, similes (whole draft)"; echo
fence bash -c "echo '# [ID] python -I identity.py composition/drafts'; python -I $S/identity.py composition/drafts; echo; echo '# [CL] python homer/check_line.py --file composition/drafts/v3.txt (summary: lines with OK, exit status)'; python homer/check_line.py --file composition/drafts/v3.txt > /dev/null; echo \"exit=\$?\"; python homer/check_line.py --file composition/drafts/v3.txt | grep -c 'OK (no flags)'"
fence bash -c "echo '# [RUL] python -I rulings.py . composition/drafts/v3.txt'; python -I $S/rulings.py . composition/drafts/v3.txt"
fence bash -c "echo '# [ASP] python -I aspir.py . composition/drafts/v3.txt'; python -I $S/aspir.py . composition/drafts/v3.txt; echo; echo '# [ACC] python -I accent.py .'; python -I $S/accent.py ."
fence bash -c "echo '# [SIM] python -I simile.py . composition/drafts/v3.txt'; python -I $S/simile.py . composition/drafts/v3.txt"
echo "### A.1 Line 23 (δεύτερον αὖ, λάβ᾽ ἄεθλον, ἄφαρ, κρατερὸς + SSLL name)"; echo
fence bash -c "$Q 23a --ngram 'δεύτερον αὖ'; $Q 23b --ngram 'λάβ᾽ ἄεθλον'; python -I $S/ctx.py . 'λάβ᾽ ἄεθλον' 2 1; $Q 23c --ngram 'κρατερὸς Διομήδης' --count; $Q 23d --ngram 'μίγη κρατερὸς Διομήδης'; $Q 23e --loose 'αφαρ' --word; python -I $S/ctx.py . 'ὦμον ἄφαρ' 2 0; python -I $S/ctx.py . 'οἳ δὲ μένουσιν ἄφαρ' 2 0; $Q 23f --loose 'αεθλον' --word"
echo "### A.2 Lines 33 and 55 (two hit clauses; καὶ βάλεν; αὖτις)"; echo
fence bash -c "$Q 33a --ngram 'καὶ βάλεν οὐδ᾽ ἀφάμαρτε'; $Q 33b --ngram 'οὐδ᾽ ἀφάμαρτε'; $Q 33c --ngram 'καὶ βάλεν'; $Q 33d --ngram 'βάλεν αὖτις'; $Q 33e --regex '(βάλ|βαλ|οὖτα|οὔτα|νύξ|τύψ|ἔβλητο|βλῆτο).*αὖτις|αὖτις.*(βάλ|βαλ|οὖτα|οὔτα|νύξ|τύψ)'; $Q 33h --regex '(βάλεν|βάλε|ἔβαλε|ἔβαλεν|βάλʼ)[ ,·].*(καὶ|δὲ|δʼ) (βάλεν|βάλε|ἔβαλε|ἔβαλεν|βάλʼ)\b'; $Q 33f --ngram 'δεύτερον αὖτις'"
fence bash -c "echo '# [33g] python homer/concordance.py --loose \"αυτις\" --word  (128 hits; shown: the hit count, the 20 verse-final hits [11-12], and Od. 22.272)'; python homer/concordance.py --loose 'αυτις' --word > $S/autis_tmp.txt; grep -c '^[IO][ld]\.' $S/autis_tmp.txt; grep '\[11-12\]' $S/autis_tmp.txt; grep '^Od. 22.272 ' $S/autis_tmp.txt; rm -f $S/autis_tmp.txt"
echo "### A.3 Lines 36-37 (τρὶς μέν … τὸ τέταρτον; the attacker; repeated name formula)"; echo
fence bash -c "$Q 36b --ngram 'τρὶς μὲν ἔπειτ᾽ ἐπόρουσε'; $Q 36a --ngram 'ἐπόρουσε βοὴν ἀγαθὸς Διομήδης'; python -I $S/ctx.py . 'τρὶς μὲν ἔπειτ᾽ ἐπόρουσε' 4 3; python -I $S/ctx.py . 'ἀλλ᾽ ὅτε δὴ τὸ τέταρτον' 2 1"
fence bash -c "echo '# [36c] python -I trismen.py .'; python -I $S/trismen.py ."
fence bash -c "echo '# [36d] python -I repname.py . 3'; python -I $S/repname.py . 3; echo; echo '# [36e] python -I repname.py . 2'; python -I $S/repname.py . 2"
echo "### A.4 Line 44 (ἔκφερε; δ᾽ αὖτε; ὃ δ᾽ ἕσπετο; κέρδεα εἰδώς)"; echo
fence bash -c "$Q 44a --ngram 'ἔκφερ᾽'; $Q 44b --loose 'εκφερεν' --word; $Q 44c --loose 'εκφερε' --word; python -I $S/ctx.py . 'ἔκφερ᾽ Ὀϊλιάδης' 1 1; python -I $S/ctx.py . 'ἔκφερον ἵπποι' 1 1; echo '# [44d] python homer/concordance.py --ngram \"δ᾽ αὖτε\" (positions tabulated; hits at 3-3.5 listed)'; python homer/concordance.py --ngram 'δ᾽ αὖτε' | grep -o '\[[0-9.-]*\]' | sort | uniq -c | sort -rn; python homer/concordance.py --ngram 'δ᾽ αὖτε' | grep '\[3-3.5\]'; echo; $Q 44f --ngram 'ὃ δ᾽ ἕσπετο'; $Q 44g --ngram 'δ᾽ ἕσπετο'; $Q 44h --loose 'εσπετο' --word; $Q 44j --loose 'επετο' --word; $Q 44k --loose 'εσπομενος' --word; python -I $S/ctx.py . 'ὃ δ᾽ ἅμ᾽ ἕσπετο ἰσόθεος φώς' 0 0; $Q 44i --ngram 'κέρδεα εἰδώς'"
echo "### A.5 Line 51 (τὴν μὲν … τὴν δ᾽ αὖ; Σέρβου κρατεροῖο)"; echo
fence bash -c "python -I $S/ctx.py . 'τὴν δ᾽ Ἕκτορος ἱπποδάμοιο' 1 1; $Q 51a --ngram 'τὴν μὲν ἄρ᾽'; $Q 51b --ngram 'τὴν δ᾽ αὖ'; echo '# [51c] python -I menau.py .'; python -I $S/menau.py .; echo; $Q 51j --regex '(ἄλλ|ἑτέρ)[^ ]* δʼ αὖ(\s|[,.·;]|$)'; python -I $S/ctx.py . 'ἄλλος δ᾽ αὖ εἶδος μὲν' 5 0; python -I $S/ctx.py . 'ἄλλοτε δ᾽ αὖ θρέξασκον' 3 0; $Q 51e --loose 'κρατεροιο' --word; $Q 51h --regex '[^ ]ου [^ ]+οιο[,.·;]?\$' --count; $Q 51i --regex '[Α-ΩἈ-ᾯῈ-Ὼ][^ ]*ου [^ ]+οιο[,.·;]?\$'; $Q 51f --ngram 'ἀνδρῶν Ἀγαμέμνων' --count; $Q 51g --ngram 'κνίσῃ ἐκάλυψαν'"
fence bash -c "echo '# [51k] Ζοκοβείδαο slot test (jsonl 51 notes): python homer/check_line.py \"τοῦ Ζοκοβείδαο κρατεροῦ μένος ἀντιθέοιο\"'; python homer/check_line.py 'τοῦ Ζοκοβείδαο κρατεροῦ μένος ἀντιθέοιο'; echo \"exit=\$?\"; echo; $Q 51l --loose 'πηλειδαο' --word"
echo "### A.6 Line 56 (ἔνθ᾽ αὖθ᾽) and the patronymic (P1)"; echo
fence bash -c "$Q 56a --ngram 'ἔνθ᾽ αὖθ᾽'; $Q 56b --ngram 'ἔνθ᾽ αὖτ᾽' --count; $Q 56c --ngram 'αὖθ᾽ ἱερεὺς'; python -I $S/ctx.py . 'Ἀμαρυγκείδην' 5 3; $Q P1 --loose 'αμαρυγκε'"
echo "### A.7 Lexica (Logeion API, fetched 2026-10-07: anastrophe.uchicago.edu/logeion-api/detail?w=…; LSJ and 'Cunliffe Homer' entries, HTML stripped by dico_text.py; excerpts)"; echo
fence bash -c "echo '# Cunliffe ἐκφέρω, sense 6:'; python -I $S/dico_text.py $D/ἐκφέρω.json 'Cunliffe Homer' | grep -o '6 Intrans.\{0,140\}'; echo '# LSJ ἐκφέρω, intransitive:'; python -I $S/dico_text.py $D/ἐκφέρω.json LSJ | grep -o 'intr. (sc.\{0,170\}'; echo '# Cunliffe ἕπομαι, senses 1a, 6a, 8:'; python -I $S/dico_text.py $D/ἕπομαι.json 'Cunliffe Homer' | grep -o '1 a To follow in company.\{0,120\}\|6 a To follow up.\{0,175\}\|8 To keep up with.\{0,120\}'; echo '# LSJ ἕπομαι I.3-4:'; python -I $S/dico_text.py $D/ἕπομαι.json LSJ | grep -o '3 in hostile sense.\{0,80\}\|4 keep pace with.\{0,70\}'; echo '# Cunliffe αὖτις, senses 1 and 3:'; python -I $S/dico_text.py $D/αὖτις.json 'Cunliffe Homer' | grep -o 'αὖτις 1 In the reverse.\{0,90\}\|3 Again, once more.\{0,200\}'; echo '# LSJ αὖθις II:'; python -I $S/dico_text.py $D/αὖθις.json LSJ | grep -o 'II of Time, again, anew.\{0,60\}'; echo '# LSJ βάλλω (hit):'; python -I $S/dico_text.py $D/βάλλω.json LSJ | grep -o 'with acc. of person or thing aimed at.\{0,170\}'; echo '# Cunliffe βάλλω II.1a and I.2 (absolute):'; python -I $S/dico_text.py $D/βάλλω.json 'Cunliffe Homer' | grep -o '1 a To strike or wound.\{0,110\}\|2 To throw or let fly.\{0,110\}'; echo '# Cunliffe ἔπειτα 1 and 4 (resumptive use):'; python -I $S/dico_text.py $D/ἔπειτα.json 'Cunliffe Homer' | grep -o '1 Then, thereupon, after that.\{0,30\}\|Resuming and restating.\{0,90\}'"
echo "### A.8 Enjambment labels (jsonl v2 and v3; v2 reviewer labels from philology_v2.md §7)"; echo
fence bash -c "echo '# [ENJ] python -I enj.py .'; python -I $S/enj.py ."
```

### B.10a enj.py (enjambment labels)

```python
# enjambment labels: v3 composer (jsonl) vs v2 composer and v2 reviewer (philology_v2.md §7); counts; line-final punctuation of the changed lines and neighbours
import json, re, sys, collections
d = sys.argv[1]
v2 = {r['n']: r['enjambment'] for r in map(json.loads, open(f'{d}/composition/drafts/v2.jsonl', encoding='utf-8'))}
v3 = [json.loads(l) for l in open(f'{d}/composition/drafts/v3.jsonl', encoding='utf-8')]
rev2 = {}; inside = False
for line in open(f'{d}/review/philology_v2.md', encoding='utf-8'):
    if line.startswith('## '): inside = line.startswith('## 7.')
    m = re.match(r'^\| (\d+) \|', line)
    if inside and m:
        cells = [c.strip() for c in re.split(r'(?<!\\)\|', line.strip())[1:-1]]
        rev2[int(cells[0])] = cells[-1].split('→')[1].strip()
print('v3 labels that differ from the v2 composer or v2 reviewer label of the same verse (n, v2 composer, v3 composer, v2 reviewer):',
      [(r['n'], v2[r['v2_line']], r['enjambment'], rev2[r['v2_line']]) for r in v3 if r['enjambment'] != v2[r['v2_line']] or r['enjambment'] != rev2[r['v2_line']]])
c = collections.Counter(r['enjambment'] for r in v3)
print('v3 composer:', {k: c[k] for k in ('none', 'unperiodic', 'necessary')})
for k in ('unperiodic', 'necessary'): print(k, [r['n'] for r in v3 if r['enjambment'] == k])
print('line-final punctuation:', [(r['n'], r['text'][-1]) for r in v3 if r['n'] in (22,23,24,32,33,34,35,36,37,38,43,44,45,50,51,52,54,55,56,57)])
```

### B.10b dico_text.py (LSJ / Cunliffe text from a Logeion API response)

```python
# usage: python -I dico_text.py FILE.json DICNAME [maxchars]  -> plain text of that dictionary's entries in a Logeion API response
import json, sys, re, html
d = json.load(open(sys.argv[1], encoding='utf-8'))
for dic in d['detail']['dicos']:
    if dic['dname'] == sys.argv[2]:
        for e in dic['es']:
            t = re.sub(r'<[^>]+>', ' ', e); t = html.unescape(t); t = re.sub(r'\s+', ' ', t)
            print(t[:int(sys.argv[3]) if len(sys.argv) > 3 else 100000])
```

### B.10c simile.py (simile openers and apodoses)

```python
# Similes in a draft: lines with ὡς δʼ ὅτε/ὅτʼ, ἠΰτε, or a comparison 'λέων ὣς'-type ὥς/ὣς after a noun,
# and the first later line opening with ὣς/ὥς/τώς (apodosis) within 14 lines.
import sys, re
sys.path.insert(0, sys.argv[1] + '/homer')
import greek as G
L = [l.strip() for l in open(sys.argv[2], encoding='utf-8')]
for i, l in enumerate(L):
    lw = [G.loose(w) for w in re.findall(r"[^\s,.·;:!]+", l)]
    opener = (re.match(r'^ὡς δ[᾽ʼ] ὅτ', l) is not None or 'ηυτε' in lw or re.search(r'\w+ ὣς[,.·;]?$', l) is not None)
    if not opener: continue
    apod = next((j for j in range(i + 1, min(len(L), i + 15)) if re.match(r'^(ὣς|ὥς|τώς)\b', L[j])), None)
    print(f'simile opener at {i+1}: {l}')
    print(f'   apodosis line: {apod+1 if apod is not None else None}: {L[apod] if apod is not None else "-"}; vehicle lines {i+1}-{apod if apod is not None else "?"} ({(apod - i) if apod is not None else "?"} lines)')
```

### B.11 rows.py (builds the §6 table)

```python
# builds the §6 per-line table of philology_v3.md: hand-written rows for the reviewed lines, one "Unchanged, v2 PASS" row for every other verse
# usage: python3 -I rows.py REPO > table.md
import json, sys, re
d = sys.argv[1]
# reviewer labels: my own for the lines reviewed in full; the v2 reviewer label (philology_v2.md §7) for identical verses
mine = {23: 'none', 33: 'none', 36: 'unperiodic', 37: 'necessary', 44: 'none', 51: 'unperiodic', 55: 'none', 56: 'unperiodic'}
rev2 = {}; inside = False
for line in open(f'{d}/review/philology_v2.md', encoding='utf-8'):
    if line.startswith('## '): inside = line.startswith('## 7.')
    m = re.match(r'^\| (\d+) \|', line)
    if inside and m:
        cells = [c.strip() for c in re.split(r'(?<!\\)\|', line.strip())[1:-1]]
        rev2[int(cells[0])] = cells[-1].split('→')[1].strip()
v3 = [json.loads(l) for l in open(f'{d}/composition/drafts/v3.jsonl', encoding='utf-8')]

full = {
23: ("PASS",
 "**R10 applied.** Ζοκοβεύς is replaced by κρατερὸς Ζοκοβείδης in the Διομήδης slot 7.5-12, after a word ending at 7, as μίγη κρατερὸς Διομήδης (Il. 5.143); κρατερὸς Διομήδης occurs 20x. "
 "**Morphology.** λάβ᾽ is the unaugmented aorist, elided before ἄεθλον as in Il. 23.511. ἄεθλον stands at 4-5.5, with ε long by position before θλ, as in Il. 23.892, Od. 21.91 and 23.261 (3 of 27 hits). "
 "**Syntax and idiom.** Line-initial δεύτερον αὖ with no connective follows Il. 6.184. ἄφαρ is at 6-7, its commonest slot (15 of 34). It follows its verb and object, as in Il. 16.322-323 (… οὐδ᾽ ἀφάμαρτεν, / ὦμον ἄφαρ) and 11.418 (μένουσιν ἄφαρ). "
 "**Sense.** In Il. 23.511 (ἀλλ᾽ ἐσσυμένως λάβ᾽ ἄεθλον) the speed adverb goes with taking the prize, so ἄφαρ λάβ᾽ ἄεθλον means \"took the prize at once\". The line therefore no longer implies that the 48-minute set was quick, and my v2 note lapses. The gloss is right. "
 "**Facts.** Set 3 went to Djokovic (tie-break 7-4 at 2:15:24); it is his second set after line 15 ✓. "
 "**Continuity.** Line 22 still ends with a comma before an asyndetic δεύτερον αὖ, and τόν in 24 now refers to Ζοκοβείδης.",
 "[23a] --ngram \"δεύτερον αὖ\" → 5, all 1-3; [23b] --ngram \"λάβ᾽ ἄεθλον\" → Il. 23.511 [9.5-12] + ctx; [23c] --ngram \"κρατερὸς Διομήδης\" --count → 20; [23d] → Il. 5.143 [6-12]; [23e] --loose \"αφαρ\" --word → 34 (15 at 6-7, 16 at 2-3) + ctx Il. 16.322-323, 11.416-418; [23f] --loose \"αεθλον\" --word → 27 (3 at 4-5.5)"),
33: ("PASS",
 "**R11 applied: the line counts two hits.** It has two co-ordinate clauses with one subject. Ace 1 (point 357) is καὶ βάλεν, οὐδ᾽ ἀφάμαρτε, as in Il. 11.350 and 13.160 (1-5.5); ace 2 (point 358) is καὶ βάλεν αὖτις. "
 "**Lexicon.** With its target understood, βάλλω means \"throw so as to hit, hit with a missile\" (LSJ, quoting τὸν βάλεν, οὐδ᾽ ἀφάμαρτε, Il. 11.350; Cunliffe: \"to strike or wound … with a missile\"). So the second clause states a second hit, not merely a second throw. Cunliffe's absolute \"let fly\" (Il. 3.82) is the weaker reading, and the parallel first clause rules it out. αὖτις means \"again, once more\" (Cunliffe αὖτις 3: Il. 1.513, Od. 9.360; LSJ αὖθις II). A repeated cast with αὖτις is Od. 22.272 (αὖτις δὲ μνηστῆρες ἀκόντισαν ὀξέα δοῦρα). "
 "**Departures from Homer.** In Homer καὶ βάλεν stands only at 1-2 (11x); here it also stands at 9-10, a mobility. No Homeric verse joins a βάλλω form to αὖτις (0 hits), and none repeats βάλλω in two co-ordinate clauses (0 hits); the pieces are attested, the combination is not. "
 "**Name slot.** Ῥογῆρος is at 6-8 after a vowel and before καί, so it is long by position (R2 ✓). "
 "**Sense and facts.** The gloss is right. Points 357-358 took the score from 15-15 to 15-40 ✓. The v2 misreading of δεύτερον αὖτις is gone. "
 "**Note.** The jsonl's models for verse-final αὖτις mean \"back (again)\" (Cunliffe 1); see §5.",
 "[33a] --ngram \"καὶ βάλεν οὐδ᾽ ἀφάμαρτε\" → Il. 11.350, 13.160 [1-5.5]; [33b] → 4; [33c] --ngram \"καὶ βάλεν\" → 11, all [1-2]; [33d] --ngram \"βάλεν αὖτις\" → 0; [33e] regex βαλ-/οὐτα-/νυξ-/τυψ- + αὖτις → 0; [33h] regex βάλλω … καὶ/δέ βάλλω in one verse → 0; [33g] --loose \"αυτις\" --word → 128 (20 at 11-12) and Od. 22.272; LSJ βάλλω, αὖθις; Cunliffe βάλλω, αὖτις (A.7)"),
36: ("PASS",
 "**R12 met.** The count line names the attacker: τρὶς μὲν ἔπειτ᾽ ἐπόρουσε (Il. 5.436, 16.784, 20.445, all 1-5.5) plus βοὴν ἀγαθὸς Φεδερῆρος at 6-12, the Διομήδης formula. The same epithet and verb occur in Il. 5.432 (Αἰνείᾳ δ᾽ ἐπόρουσε βοὴν ἀγαθὸς Διομήδης), the onset that 5.436 resumes. So the unexpressed subject of ἐπέσσυτο in 37 is Federer, as in all three Homeric sequences. "
 "**τρὶς μέν without τρὶς δέ.** Il. 13.20 (τρὶς μὲν ὀρέξατ᾽ ἰών, τὸ δὲ τέτρατον …) and the poem's own 14-15 do the same. The other 14 Homeric τρὶς μέν lines have a τρὶς δ(έ) member. "
 "**Count.** The jsonl takes τρίς as points 359-361, with CP1 (359) also narrated in 34-35, and the fourth as 362. Cunliffe classes the ἔπειτα of this very formula (Il. 5.436, 20.445) as \"resuming and restating\" an onset already told (5.432 and 20.442; 16.783 ἐνόρουσε), so τρίς may include CP1 ✓. The caveat: each Homeric case states the resumed onset with ἐπ- or ἐνόρουσε, while 34-35 has no verb of attack. A reader who takes ἔπειτα as \"thereafter\" (Cunliffe 1) would count CP1 plus three and place \"the fourth\" one point late. I judge the Homeric reading sufficient (§3). "
 "**Note.** βοὴν ἀγαθὸς Φεδερῆρος also closes 34. The same three-word name formula two verses apart has 1 Homeric parallel (Od. 8.2/8.4), and the two-word tail has 8 (e.g. Il. 20.386/388). "
 "**Facts.** Points 359-361 were all lost by Federer on his serve ✓. The CP2 passing shot is no longer narrated, but its fact is kept in the jsonl. The gloss is right.",
 "[36b] --ngram \"τρὶς μὲν ἔπειτ᾽ ἐπόρουσε\" → Il. 5.436, 16.784, 20.445 [1-5.5]; [36a] --ngram \"ἐπόρουσε βοὴν ἀγαθὸς Διομήδης\" → Il. 5.432; ctx -4/+3 on the three; ctx \"ἀλλ᾽ ὅτε δὴ τὸ τέταρτον\" → 5; [36c] trismen.py → 15 τρὶς μέν lines, 1 without τρὶς δ (Il. 13.20); [36d/e] repname.py → 1 / 8 pairs; Cunliffe ἔπειτα 4 (A.7)"),
37: ("PASS",
 "**The text is unchanged, but this was a v2 QUERY, so it is reviewed in full. R12 met.** The subject of ἐπέσσυτο is the named subject of 36 (Federer), with nothing in between, as in Il. 5.436→438, 16.784→786 and 20.445→447. In Homer a τρὶς δ(έ) verse intervenes each time, and Il. 5.437 and 16.703 change the subject there. Line 38 switches to the named Σέρβος with an apodotic δ᾽ (Il. 5.439 δεινὰ δ᾽ ὁμοκλήσας …). "
 "**Count.** \"The fourth\" now has its three (36), and 362 (the break to 8-8) is the fourth point on the reading of 36. "
 "**Idiom.** As in Homer, the fourth onset of the man δαίμονι ἶσος is the one that is stopped.",
 "ctx \"ἀλλ᾽ ὅτε δὴ τὸ τέταρτον\" -2/+1 → 5 (A.3); rulings.py: the τὸ τέταρτον verses 15 and 37 both follow a verse that names Φεδερῆρος"),
44: ("PASS",
 "**v2 FAIL repaired; R10 applied.** The change of subject is now marked by ὃ δ᾽, and κέρδεα εἰδώς stands in apposition to ὃ, i.e. Federer, as in Ῥογῆρος κέρδεα εἰδώς (27). So the craft epithet stays with Federer ✓. "
 "**Models for leader and follower.** "
 "(1) A pronoun with δέ for the follower: Od. 1.125 (ἡγεῖθ᾽, ἡ δ᾽ ἕσπετο Παλλὰς Ἀθήνη) and Il. 11.472 = 15.559 = 16.632 (ὃ μὲν ἦρχ᾽, ὃ δ᾽ ἅμ᾽ ἕσπετο ἰσόθεος φώς). "
 "(2) A pursuer marked by ὃ δ᾽: Il. 21.256 (φεῦγ᾽, ὃ δ᾽ ὄπισθε ῥέων ἕπετο). "
 "(3) Race order: Il. 23.376-377 (ἔκφερον … τὰς δὲ μετ᾽ ἐξέφερον). "
 "**Lexicon and morphology.** "
 "(1) ἔκφερε is intransitive, \"to draw away from competitors in a race, shoot ahead\" (Cunliffe ἐκφέρω 6: Il. 23.376, 377, 759; LSJ \"intr. … shoot forth (before the rest)\"). "
 "(2) It is unaugmented, and unelided before δ᾽: ἔκφερ᾽ occurs 3x and ἔκφερεν once (Od. 15.470); ἔκφερε itself has 0 hits but is the regular 3 sg. imperfect before a consonant. "
 "(3) δ᾽ αὖτε after a dactylic first word stands at 3-3.5, as in Od. 2.203 (χρήματα δ᾽ αὖτε); 5 of 141 hits are at 3-3.5. "
 "(4) Νοβῆκος is at 4-5.5 before a vowel, an A1 slot; the accent follows R9 ✓. "
 "(5) ἕσπετο is at 7-8 (8 of 12 hits). "
 "**Notes.** "
 "(1) ὃ δ᾽ ἕσπετο itself has 0 hits. "
 "(2) In Homer the aorist ἕσπετο always means \"accompany, follow a leader\" (12/12; Cunliffe ἕπομαι 1, 5). The hostile sense \"follow up, pursue\" and the sense \"keep up with\" belong to the present stem: ἕπετο in Il. 11.165, 16.372, 21.256 and ἕπεθ᾽ in Il. 16.154 (Cunliffe 6, 8; LSJ I.3-4). \"He followed\" for Federer's hold to 9-9 thus puts the follower of a race-order line into the aorist, a slight extension. "
 "**Sense and facts.** The gloss is right. 9-8 at 4:17:15 and 9-9 at 4:21:04 ✓.",
 "[44a] --ngram \"ἔκφερ᾽\" → 3; [44b] ἔκφερεν → Od. 15.470; [44c] ἔκφερε → 0; ctx Il. 23.759, 23.376-377; [44d] δ᾽ αὖτε → 141 (5 at 3-3.5); [44f] --ngram \"ὃ δ᾽ ἕσπετο\" → 0; [44g] \"δ᾽ ἕσπετο\" → 3; [44h] ἕσπετο → 12; [44j] ἕπετο → 4; [44k] ἑσπόμενος → 2; ctx \"ὃ δ᾽ ἅμ᾽ ἕσπετο ἰσόθεος φώς\" → 3; [44i] κέρδεα εἰδώς → Il. 23.709; Cunliffe ἐκφέρω, ἕπομαι; LSJ ἐκφέρω, ἕπομαι (A.7)"),
51: ("PASS",
 "**R10 applied.** ἀντιθέου Ζοκοβῆος is replaced by τὴν δ᾽ αὖ Σέρβου κρατεροῖο. "
 "**Morphology.** Σέρβου is a second-declension genitive in -ου, beside an epithet in -οιο. Homer has the same mixture in Μενελάου κυδαλίμοιο (Il. 4.100 etc.), Ἀγαστρόφου ἰφθίμοιο (Il. 11.373) and Ἀρκεισίου ἀντιθέοιο (Od. 14.182). A name in the genitive with κρατεροῖο at verse end is Πολυποίταο κρατεροῖο (Il. 23.848), and 5 of the 7 κρατεροῖο stand at 9.5-12. κρατερός is Djokovic's epithet (23, 53), so economy holds. "
 "**Syntax.** The model is τὴν μὲν … τὴν δ᾽ (Il. 22.211), with αὖ added to the second member. τὴν μὲν … τὴν δ᾽ αὖ is not attested (0 hits), but distributive μέν … δ᾽ αὖ is: ἄλλος μέν … ἄλλος δ᾽ αὖ (Od. 8.169/174) and ὁτὲ μέν … ἄλλοτε δ᾽ αὖ (Il. 18.599/602). A pronoun + δ᾽ αὖ at 6-7 is Il. 8.324. "
 "**Idiom.** Σέρβου is LL at 8-9 before an SSLX word, the shape of ἀνδρῶν Ἀγαμέμνων (36x) and κνίσῃ ἐκάλυψαν (4x, 8-12). "
 "**Sense and facts.** The gloss is right; 12-12 at 4:48:30 ✓. "
 "**Continuity.** τήν refers to the dual κῆρε of 50, and 52 (ἕλκε δέ …) follows as in Il. 22.212. "
 "**Note.** The jsonl claim that Ζοκοβείδαο fits no slot is false (§5); the choice made here is unaffected.",
 "ctx \"τὴν δ᾽ Ἕκτορος ἱπποδάμοιο\" → Il. 22.210-212; [51a] \"τὴν μὲν ἄρ᾽\" → 3; [51b] \"τὴν δ᾽ αὖ\" → 13, all [1-2]; [51c] menau.py → 2 (neither distributive); [51j] ἄλλ-/ἑτέρ- δ᾽ αὖ → 3 + ctx Od. 8.169-174, Il. 18.599-602; [51e] κρατεροῖο → 7; [51h] -ου + -οιο at verse end → 38; [51i] capitalised -ου + -οιο → 25; [51f] ἀνδρῶν Ἀγαμέμνων → 36; [51g] κνίσῃ ἐκάλυψαν → 4 [8-12]; [51k] check_line on the Ζοκοβείδαο test verse"),
55: ("PASS",
 "**R9 and R11 applied.** Νοβῆκος has the circumflex: Homer has 51 types in η/ω + one consonant + -ος, all circumflexed, and 0 with the acute. "
 "**Count.** This is the system of 33, with Νοβῆκος in the Ῥογῆρος slot (6-8 after a vowel; -κος long before καί). It has two hit clauses for two winners, the forehand at 420 and the backhand at 421 ✓; see 33 for βάλλω and αὖτις. "
 "**Continuity.** 54 has Ἑλβέτιος as subject; the change is resolved inside this verse by the name. "
 "**Punctuation.** 55 prints καὶ βάλεν, οὐδ᾽ ἀφάμαρτε Νοβῆκος with no comma after ἀφάμαρτε, as Il. 11.350; 33 has one, as Il. 13.160. Both are Homeric; harmonise if wanted. "
 "**Sense.** The gloss is right.",
 "accent.py → acute 0 / circumflex 51 types, 269 tokens (A.0); rulings.py → Νοβῆκος 44, 55, Νοβήκος 0; A.2 as for 33"),
56: ("PASS",
 "**v2 FAIL repaired.** αὖθ᾽ now stands before the rough breathing of Ἑλβέτιος. Homer has αὖθ᾽ + rough breathing 33x and αὖτ᾽ + rough breathing 0x, and the draft now has no elided τ, π or κ before a rough breathing. As noted in v2, ἔνθ᾽ αὖθ᾽ has 0 hits against 12 for ἔνθ᾽ αὖτ᾽, because ἔνθ᾽ αὖτ᾽ never stands before an aspirated word. "
 "**Unchanged from v2.** προΐει is absolute; βάλε δ᾽ stands at 7.5-9; ἂψ means \"in return\"; R3 ✓. "
 "**Facts and continuity.** Point 422 ✓. 57 follows with Ἑλβέτιος δ᾽ ἄρα τοῦ μέν …",
 "aspir.py → αὖθ᾽ + rough 33, αὖτ᾽ + rough 0; draft: no ERROR (A.0); [56a] \"ἔνθ᾽ αὖθ᾽\" → 0; [56b] \"ἔνθ᾽ αὖτ᾽\" → 12; [56c] \"αὖθ᾽ ἱερεὺς\" → Il. 1.370"),
}

neighbour = {
22: "Neighbour of 23: it still ends with a comma before the asyndetic δεύτερον αὖ of 23, so the label is unchanged.",
24: "Neighbour of 23: τόν now refers to Ζοκοβείδης, the last word of 23; the sense is unchanged.",
32: "Neighbour of 33: Federer is the subject, and 33 names him again (Ῥογῆρος).",
34: "Neighbour of 33 and 36: the object (Djokovic) is understood. Its closing βοὴν ἀγαθὸς Φεδερῆρος recurs at the end of 36 (see 36). CP1 here is the first of the three onsets counted in 36.",
35: "Neighbour of 36: οἱ is Federer, and βέλος is the subject. 36 names Federer again, so there is no ambiguity.",
38: "Neighbour of 37: the subject moves from Federer (36-37) to the named Σέρβος, marked by an apodotic δ᾽. The v2 QUERY 37 is resolved.",
43: "Neighbour of 44: Σέρβον is the same man as Νοβῆκος in 44.",
45: "Neighbour of 44: it follows 44's full stop; the simile 45-47 → 48 is intact.",
50: "Neighbour of 51: the dual κῆρε is the antecedent of τήν … τήν in 51.",
52: "Neighbour of 51: Ἑλβετίου is repeated after 51, as Ἕκτορος is in Il. 22.211-212.",
54: "Neighbour of 55: Federer is the subject; 55 names Νοβῆκος inside the verse.",
57: "Neighbour of 56: it follows 56 with δ᾽ ἄρα.",
}

for r in v3:
    n = r['n']; comp = r['enjambment']
    if n in full:
        v, f, e = full[n]
        print(f"| {n} | {v} | {f} | {e} | {comp} → {mine[n]} |")
    else:
        note = (' ' + neighbour[n]) if n in neighbour else ''
        print(f"| {n} | PASS | Unchanged, v2 PASS (= v2 {r['v2_line']}).{note} | identity → {n}={r['v2_line']} | {comp} → {mine.get(n, rev2[r['v2_line']])} |")
```

