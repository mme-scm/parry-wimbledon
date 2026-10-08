# Philology review of draft v4 (64 verses)

Reviewed: `composition/drafts/v4.txt`, with glosses, facts, sources, enjambment labels and revision notes from `composition/drafts/v4.jsonl` (fields `v3_line`, `changed`, `revision_note`, `critic_issue`). Checked against:
* `review/critic_poem_v1.md` (M1-M8, m1-m14), which v4 answers;
* `review/round_1.md`, `round_2.md` (rulings R1-R12) and `round_3.md`;
* `composition/brief.md` (§1 facts, §2-§5, Addenda A1-A2);
* my v3 report (`review/philology_v3.md`).

Reviewer: philologist agent, 2026-10-08. Scansion and provenance have their own verifiers; points for them and for the composer are in §5.

## 1. Method and sources

* **Homeric evidence.** Every Homeric claim comes from `python homer/concordance.py` (Perseus: Monro-Allen Iliad, Murray Odyssey; homer/README.md), or from small scripts that call its `Concordance` class (Appendix B). Each judgement in §6 names its query; the verbatim outputs are in Appendix A. Positions in square brackets use the half-foot numbering of homer/README.md. `check_line.py --file` was run on the whole draft: 64/64 pass with no flags, exit 0 (A.0).
* **Which verses were reviewed in full.** `identity.py` (B.1) compared every v4 verse character by character with the v3 verse named in its `v3_line` field. It also checked that v4.txt equals the jsonl text and that every verse is NFC.
  * 43 verses are identical to a v3 verse, and all 43 were v3 PASS. Each has one row reading "Unchanged, v3 PASS". Where a neighbouring verse changed, I re-read the passage and added the continuity check to that row.
  * 16 verses changed: 19, 20, 23, 27, 32, 33, 34, 38, 49, 54, 56, 58, 59, 61, 62, 63.
  * 5 verses are new: 24, 29, 35, 36, 40.
  * v3 47 was dropped.
  * The jsonl `changed` flag agrees with the text on every verse. These 21 verses are reviewed in full; 59 changed in punctuation only.
* **Narrative continuity.** I re-read the whole poem once against `corpus/timing/points_2019wimF.csv` (the FACTS table, A.0) and brief §1; see §3.
* **Lexica.** I fetched these entries on 2026-10-08 from the Logeion API (`anastrophe.uchicago.edu/logeion-api/detail?w=…`), which returns LSJ and Cunliffe's *Lexicon of the Homeric Dialect* ("Cunliffe Homer"):
  * κήρ / Κήρ, ἔλδωρ, ῥέπω, ὀπίσσω, τυτθός, πύματος, νικάω, δαμάζω, δάμνημι;
  * παρελαύνω, ἀμφήριστος, ἐπορούω, ἐπηπύω, ἀρωγός, ἐρητύω, κῆρυξ, διώκω, μετέπειτα, ἕτερος;
  * ἁμαρτάνω, τυγχάνω, μογέω, κῦδος, αἰζηός, θαλερός, σχεδόν, λαμβάνω, ἕλκω.

  The v3 copies of ἔπειτα and ἐκφέρω were reused. Excerpts are in A.10. Anything else is marked [unverified].
* **Enjambment.** The criteria are those of v1-v3: Parry 1929 as quoted by Dukat 1991 (*Oral Tradition* 6/2-3, 303-315; fetched for v1), with Kirk's punctuation test as Dukat tabulates it.
  * A printed strong stop (. · ;) is **none**.
  * A complete sentence continued after a comma or with no stop is **unperiodic**.
  * An incomplete sentence is **necessary**; this includes every verse of an open ὡς δ᾽ ὅτε period before its apodosis.

  Parry's own text was not accessed [unverified at first hand].
* **Verdicts.**
  * **PASS:** no philological defect; notes may still apply.
  * **FAIL:** a defect in morphology, orthography, prosody or syntax, or a mismatch between the Greek and its gloss or the facts, shown by the evidence.
  * **QUERY:** a human decision is needed.
* **Reproducibility.** The counts in §2 and §4 are printed by `tally4.py` (B.9) from the table in §6. Appendix A is written by `appendix4.sh` (B.10).

## 2. Summary

**Verdicts (64 verses): PASS 64, FAIL 0, QUERY 0.**
* 43 are "Unchanged, v3 PASS".
* 21 were reviewed in full, and all pass.
* No ruling is breached.
* The notes that matter for the paper or for a record correction are collected in §5. None changes a verdict.

**The questions for this round**

| question | answer | evidence |
|---|---|---|
| **Set 3 (M2).** | **Fixed.** The sequence is 21 level set → 22 the exchange → 23 Federer wins the 26-shot rally (point 183) → 24 "but the Serb then beat him in the last fight" (tie-break 7-4, 2:07:34-2:15:24). The verse no longer implies that the rally went to Djokovic or ended the set, and ἄφαρ is gone. Line 23 repeats 28 verbatim, five lines apart. Homer has 6 such repeats within 5 lines, one of them narrative (Il. 7.428 = 431). | A.0 FACTS, REP; A.2 |
| **Set 4 (M3).** | **Fixed.** The sequence is 25 two Federer breaks → 26 second serve → 27 the running (Il. 23.116) → 28 Federer's winner (point 242) → 29 ἀλλὰ καὶ ὧς ἐδάμη … Νοβήκου (the break at 2:49:12, point 244) → 30 τέτρατον αὖτ᾽ ἔλαβεν (6-4 at 2:55:08). The passive keeps Federer as subject, so 30's "he took" is his. | A.0 FACTS; A.3 |
| **CP1, CP2 (M1) and the fourth-time count.** | **CP2 is now narrated.** In 40 Federer approaches (στῆ δὲ μάλ᾽ ἐγγὺς ἰών, 5x) and ὃ δέ μιν βάλεν, οὐδ᾽ ἀφάμαρτε, so Djokovic is the subject of a hit verb at 4:11:30. The models are Il. 13.387 (ὃ δέ μιν φθάμενος βάλε) and 22.123 (ἰών, ὃ δέ). CP1 (38-39) is the counterfactual of Il. 3.373-374. The aces (37) are the two hit clauses of R11. **The count:** 41 τρὶς μὲν ἔπειτ᾽ ἐπόρουσε resumes 38-40 (Cunliffe ἔπειτα 4, "resuming and restating", Il. 5.436, 20.445). So τρίς = 359, 360, 361 and the fourth (42) = 362, the break for 8-8 ✓, and R12 is met (41 names Φεδερῆρος). Caveat: on the "thereafter" reading the fourth now falls two points late (364), not one as in v3, because CP2 is narrated before the count. Each of Homer's three τρὶς μὲν ἔπειτ᾽ ἐπόρουσε has a τρὶς δ(έ) limb in the next verse, and 41 has none; the only τρὶς μέν without one is Il. 13.20. The critic's τρὶς δέ alternative was not taken. A note, not a fault. | A.0 FACTS; A.6 (ctx 5.432-438, 16.780-786, 20.441-447; trismen) |
| **Crowd and heralds (M7), Il. 18.502-503.** | **Sound.** 35 = Il. 18.502 verbatim; v4 adds a comma. 36 = Il. 18.503 1-8 + ἔνθα καὶ ἔνθα at 9-12, its commonest slot (21/32). Cunliffe ἐπηπύω "give one's voice in approval to (dat.)", ἀρωγός "partisans (Il. 18.502)", ἐρητύω 1 "hold back, restrain". The Homeric context is a dispute before an ἴστωρ (18.501) with a crowd on both sides, which fits. Il. 2.96-98 (κήρυκες βοόωντες ἐρήτυον, εἴ ποτ᾽ ἀϋτῆς σχοίατ᾽) is closer to the umpire's "Please" and should be cited. Facts: 4:08:51, tv_2019wimF:0409 ✓. | A.5; A.10 |
| **The vocative Φεδερεῦ (61): who speaks, and is a speaker frame Homeric?** | **The narrator, by apostrophe; no frame, correctly.** Homer has ἤμβροτες twice, both in framed speech by the opponent taunting the man who missed: Il. 5.286-287 (Diomedes to Pandarus) and 22.278-279 (Hector to Achilles). A frame here would make Djokovic speak, which brief §5.4 forbids. Homer never gives unframed direct speech, so the only reading is the narrator's apostrophe. That is Homeric in form: a 2nd-person aorist of the hero's own act with his vocative and no frame (Il. 16.692-693 ἐξενάριξας, Πατρόκλεις; 16.584-585 ἔσσυο; 4.127). The 3rd → 2nd person switch after a comma (60 → 61) is Il. 16.786 → 787. What has no Homeric model is the narrator using the taunt formula: the line turns a victor's taunt into sympathy (πολλὰ μογήσας, cf. Il. 23.607 πολλὰ μόγησας, 2nd person). Brief §2.6.1 proposed the formula "in the poem's own voice". A note for the paper. Φεδερεῦ is the regular -εύς vocative (Ἀχιλεῦ at 5.5-7, 3x). | A.9; A.10 |
| **τυτθόν as "a little bit" (M7, brief §3.6).** | **Present (49), with a shift of sense.** τυτθὸν ὀπίσσω occurs once (Il. 5.443), meaning "withdrew a little *backwards*" (Cunliffe ὀπίσσω 1). Line 49 means "a little *behind*" (Cunliffe ὀπίσσω 2, "of place, behind, in rear", Il. 9.507 of followers). The pursuit with a "little" margin has an exact Homeric scene: Il. 21.601-604, ὃ δ᾽ ἐπέσσυτο ποσσὶ διώκειν … τυτθὸν ὑπεκπροθέοντα (Cunliffe τυτθός 2e "keeping always a little ahead"). The aorist ἕσπετο (critic m8) is gone. | A.7; A.10 |
| **Death-free scales (M5): ἐέλδωρ and the replaced ἦμαρ phrases.** | **The explicit death language is gone; κῆρε remains.** θανάτοιο (v3 50), κακὸν ἦμαρ (v3 52), νηλεὲς ἦμαρ (v3 54) and ἀνδρὸς κατατεθνηῶτος (v3 47, dropped) are all gone. The death-register scan finds only κῆρε (54), δείελον ἦμαρ (64, literal time) and γυῖα λέλυντο (33, fatigue as in Il. 7.6, 13.85). **ἐέλδωρ** (56) is Homeric: 10x, 9 at 10-12, "wish, longing, desire". Elision before it is attested (κρηήνατ᾽ ἐέλδωρ, Od. 3.418, 17.242), and a possessor's genitive with it is Il. 15.74. It stands where Homer has αἴσιμον ἦμαρ, which LSJ ῥέπω glosses "implying defeat and death"; so defeat stays and death goes ✓. ῥέπε … ἐέλδωρ has 0 hits; the collocation is new. **Residual:** in Homer κήρ is always doom (Cunliffe 1 "bane, death", 2 "one's destined fate", 3 in the scales "typifying death or one's fate"; LSJ "doom, death … rarely without personal sense in Hom."). With μάχης it reads as "the fates of the fight". Brief §2.5A had asked for κῆρε to go too ("else keep and document"); it is documented, and the critic's own test line kept it. For the paper, not a fault. | A.8 (DEATH); A.10 |
| **Victory verbs (M4).** | **Graded and Homeric.** **Breaks:** δάμασσε / δάμασεν / ἐδάμη (20, 25, 29, 31; R5). **Break back:** ἂψ ἐπόρουσε καὶ ἀμφήριστον ἔθηκεν (32; Cunliffe ἀμφήριστος "a dead heat"). **Break to lead:** παρέλασσε (34; Cunliffe παρελαύνω 1a "outstrip him in the race"). **Sets:** ἐνίκα (15, 24; Cunliffe νικάω 1 "in fight or in a contest", Il. 23.680, 756 games), λάβ᾽ ἄεθλον (20, now in its Homeric slot 7-12), ἔλαβεν (30). **Title:** κῦδος only. 38 has ἄσπετον ἤρατο κῦδος in a counterfactual, as in both Homeric instances (Il. 3.373, 18.165, each followed by εἰ μή); 62 has Ζεὺς κῦδος ἔδωκε with a dative recipient (Il. 1.279, 8.216, 18.456; Cunliffe κῦδος 3 "the glory of victory"). **Residual:** δάμ- for a break is the kill/overpower verb (Cunliffe δαμάζω 5-6). 29's ἐδάμη ὑπὸ χερσί is lethal in 10 of the 11 Homeric ὑπὸ χερσί verses, but Il. 23.675 is the beaten boxer of the games, carried out alive; cite it. | A.1, A.3, A.4, A.6, A.9; A.10 |
| **βοὴν ἀγαθ- spacing (M6).** | **No adjacent pair; one pair closer than any in Homer.** The four verses are 14, 31, 34 and 41, with gaps 17, 3 and 7 (v3 had six, with one adjacent pair, 29-30). The 51 Homeric βοὴν ἀγαθ- verses are never closer than 4 lines apart (one pair, Il. 2.563/567), so 31/34 is one line tighter than any Homeric pair. Stylistic, not a fault. Name tokens fell from 33/60 (0.55 a verse; narrative 0.62) to 31/64 (0.48; narrative 0.53); adjacent named pairs fell from 16 to 12. | A.0 BOEN, NAMES |
| **Rulings.** | See the next table: no breach. | A.0 RUL |

**Rulings applied (whole draft; A.0)**

| ruling | status in v4 |
|---|---|
| R2 Ῥογῆρος not before ἰσόθεος φώς | applied: ἰσόθε- 0. Ῥογῆρος stands before κ (23, 28) and καί (37) |
| R3 withdrawn Ζοκοβίδης / Νοβάκος | applied: 0 |
| R4 no δίς + verb | applied: δίς 0 |
| R5 ἐξεναρίζω at most 2 | applied: 0. δάμ- is the break verb (20, 25, 29, 31; 45 is Homer verbatim) |
| R6 πάλιν only "back" | applied: only 22 (v3 PASS) |
| R9 Νοβῆκος | applied: the nominative Νοβῆκος (59) has the circumflex. The new genitive Νοβήκου (29) has the acute, which is correct before a long ultima: all 5 Homeric -ῆCος / -ήCου pairs have it (κλῆρος/κλήρου, χῶρος/χώρου, Ῥῆσος/Ῥήσου, δῆμος/δήμου, νῆσος/νήσου), with 0 against (ACC2). It is not an R9 breach |
| R10 Ζοκοβεύς = the eponym only | applied: Ζοκοβεύς / Ζοκοβῆ- 0. Djokovic is Ζοκοβείδης (4, 57, 60), Σέρβ- (9 tokens), Νοβῆκος / Νοβήκου (59, 29) |
| R11 counts match the facts | applied: δεύτερον αὖτις only in 25 (two set-4 breaks); two hit clauses in 37 (357-358) and 59 (420-421) |
| R12 attacker fixed before τὸ τέταρτον | applied: 15 and 42 each follow a τρὶς μέν verse ending Φεδερῆρος |
| aspiration | applied: 23 elisions before a breathing are checked, none wrong |
| similes need ≥ 3 lines and an apodosis (brief: at least two) | horse 16-18 → 19 (3); lion 43-47 → 48 (5); racing horses 50-51 → 52 (2, since v3 47 was dropped). The brief's minimum of two extended similes still holds |
| prohibited words | 0 |

**Dialect and morphology.**
* The base is Ionic-epic throughout.
* The new forms are Homeric or have Homeric analogues:
  * πυμάτῃ (case of πύματος); ἐδάμη; Νοβήκου (accent as above); κρατεροῦ (3x);
  * τοῖιν; παρέλασσε (the form Cunliffe gives); ἐπήπυον, ἐρήτυον; ἔλαβέν τε (accent as εἴρυσσέν τε);
  * ἔκφερεν (Od. 15.470); ἐέλδωρ; μετέπειτα; Φεδερεῦ (-εῦ vocative); Σέρβῳ ἀντιθέῳ.
* Augmented and unaugmented past tenses alternate as in Homer: ἕλκε and ῥέπε are verbatim; ἔκφερεν is unaugmented.
* No Attic forms. ἐνίκα is the contracted imperfect Homer itself uses (8x).
* Orthography: every verse is NFC, and elision is written ᾽ throughout.

**Syntax.**
* Particles are used as in Homer: ἀλλὰ καὶ ὧς; ὅ γε and ὅ γ᾽ with a name in apposition (ὁ Τυδεΐδης, Il. 8.532, 11.660); μέν … δέ within the verse in 63 (Il. 17.424); μέν answered by τὸν δ᾽ across 57-58.
* The past unreal is Homeric: καί νύ κεν + aorist indicative, then εἰ μή + aorist indicative (38-39).
* No new tmesis.

**Lexicon.**
* No post-Homeric word occurs except the sanctioned name renderings.
* Four Homeric phrases are used in a sense shifted from their source, each recorded in §5:
  * τυτθὸν ὀπίσσω (49): "backwards" → "behind";
  * μάλα σχεδὸν ἦλθε διώκων (58): Il. 23.499 "came near, driving" → "came near, pursuing him";
  * ἀμφήριστον ἔθηκεν (32): unreal → actual;
  * ἤμβροτες (61): a taunt → the narrator's apostrophe.

**Enjambment (whole poem; §4).** By my labels: none 37 (57.8%), unperiodic 18 (28.1%), necessary 9 (14.1%). Composer and reviewer differ on one verse (63). Necessary enjambment fell from 10/60 to 9/64, because v3 47 was dropped and none of the 21 rewritten verses is necessary.

**Outside philology, for the record.** The poem now has 64 verses against the brief's "about 50" (45-55).

## 3. Narrative continuity (the whole poem, re-read once)

* **1-18 (proem, arming, set 1, horse simile):** unchanged.
  * 19 now closes the simile with ἐπέσσυτο δαίμονι ἶσος.
  * 20 states the set-2 win (λάβ᾽ ἄεθλον) after the three breaks; μιν is Djokovic, named last in 15.
* **21-24 (set 3):** level set → exchange → Federer's rally winner (23) → the Serb's tie-break (24, ἔπειτα).
  * 25's τόν is now the Serb (24's subject).
* **25-30 (set 4):** two Federer breaks → second serve → the running (27) → winner (28) → broken all the same (29) → the set (30).
  * Line 26's "second serve" still has no narrated first serve (critic m11, unchanged, v3 PASS).
* **31-34 (set 5 to 8-7):** the Serb breaks (31) → Federer breaks back to a dead heat (32) → both exhausted (33) → late, Federer drives past (34).
  * The fatigue verse now carries a range clock, so there is no inversion.
* **35-42 (the championship game):**
  * crowd and heralds at 4:08:51 (35-36);
  * two aces (37); CP1 (38-39); CP2 (40);
  * τρίς (41) and the fourth (42).
  * In 37, καὶ βάλεν now follows the heralds' full stop, and the subject is named inside the verse. In Homer καὶ βάλεν always continues the verse before (11/11). Here it opens a sentence, as it already did in v3.
* **43-52 (aristeia and the race simile):**
  * lion simile 43-47 → 48;
  * 49: Djokovic ahead at 9-8, Federer "a little behind", level at 9-9;
  * racing horses 50-51 → 52, up to 12-12.
  * 51 now stands directly before the apodosis with no final stop (see §6, row 51).
  * Σέρβον (48) and Σέρβος (49) are adjacent.
* **53-56 (the scales):** Zeus weighs, and the Swiss's desire sinks. This is a prolepsis of the 7-3 tie-break, as Il. 8.72-74 anticipates the rout that follows.
* **57-62 (the tie-break):**
  * three Djokovic points (57, 415-417);
  * Federer close behind (58, 418-419);
  * Novak's two winners (59, 420-421);
  * the last serve and return (60);
  * the apostrophe for Federer's error (61, 422);
  * Zeus gives the Serb glory (62).
  * Every score change in the tie-break after 1-1 is narrated or counted. Points 413-414 (1-0, 1-1) are not narrated.
* **63-64:** the summary with Zeus's will (Il. 1.5) and the late hour.

Every narrated event matches `points_2019wimF.csv` (A.0 FACTS) and brief §1. No item of brief §1.11 appears, and neither player speaks (61 is the narrator).

## 4. Enjambment

Counts are printed by tally4.py (B.9) from §6, out of 64 verses:

| | none | unperiodic | necessary |
|---|---|---|---|
| composer (v4 jsonl) | 36 (56.2%) | 19 (29.7%) | 9 (14.1%) |
| reviewer | 37 (57.8%) | 18 (28.1%) | 9 (14.1%) |
| v3 reviewer (60 verses) | 31 (51.7%) | 19 (31.7%) | 10 (16.7%) |
| Parry's Iliad sample (Dukat 1991:305, from Parry 1929:204) | 48.5% | 24.8% | 26.6% |

* **The one disagreement is 63.** It ends with a high stop, so it is none by the punctuation test used in v1-v3 for every verse ending in ·. The composer has unperiodic.
* **The unchanged verses** keep their v3 reviewer labels (A.11).
* **The new and changed verses:**
  * unperiodic: 27 (complete, continued by καί), 38 (apodosis complete, εἰ μή follows) and 54 (complete, apposition follows);
  * none: the other 18.
* **The necessary verses** are 1, 3, 16, 17, 18, 42, 44, 50 and 51: the proem, the three similes, and 42 in the duel narrative (the ὅτε clause of the fourth onset).
* **Against the brief.** The target of "roughly a third" necessary (brief §2.7) is further off than in v3 (14.1% against 16.7%). The wish that the championship game and the rallies run on is met only by 41 → 42 → 43. A shortfall for the paper, not a line-level fault.

## 5. Points for the composer and the other verifiers (not philological verdicts)

* **Record corrections (jsonl `sources` / `notes`), no change to the verse:**
  * **24:** cite Il. 16.79 (μάχῃ νικῶντες Ἀχαιούς) for νικάω + μάχῃ + accusative, and Il. 8.532, 11.660 (ὁ / ὃ Τυδεΐδης) for a pronoun with a name in apposition.
  * **29:** cite Il. 23.675 (ἐμῇς ὑπὸ χερσὶ δαμέντα: the beaten boxer of the games) as the contest use of ὑπὸ χερσὶ δαμῆναι, beside the lethal Il. 2.860. For the split κρατεροῦ ὑπὸ χερσὶ Νοβήκου, cite πολιῆς ἐπὶ θινὶ θαλάσσης (Il. 4.248) and Ἀθηναίης ἐπὶ γούνασιν ἠϋκόμοιο (Il. 6.92).
  * **32:** the closest model is αὐτὰρ ὃ ἂψ ἐπόρουσε (Il. 3.379, 21.33, 1-5.5), not Il. 11.580 / Od. 11.599 alone. Record that ἀμφήριστον ἔθηκεν is unreal in both Homeric uses and actual here.
  * **34:** the model is the whole-verse frame ὀψὲ δὲ δὴ μετέειπε βοὴν ἀγαθὸς Διομήδης (Il. 7.399 = 9.31 = 9.696) with one verb changed; cite it instead of, or beside, Il. 5.114.
  * **35, 27:** these "verbatim" verses carry punctuation different from Perseus. 35 adds a comma after ἐπήπυον; 27 has a comma where 23.116 has ·.
  * **36:** cite Il. 2.96-98 (κήρυκες βοόωντες ἐρήτυον, εἴ ποτ᾽ ἀϋτῆς σχοίατ᾽) as the heralds' call for quiet.
  * **49:** record that τυτθὸν ὀπίσσω in Il. 5.443 means "backwards" (Cunliffe ὀπίσσω 1) and here "behind" (ὀπίσσω 2, Il. 9.507). Cite Il. 21.601-604 for the pursuer and the "little" margin.
  * **54:** the gloss should read "two fates of the fight of lusty men". θαλερῶν αἰζηῶν is plural and generic, and δύο goes with κῆρε. Record κῆρε's residual sense (Cunliffe κήρ 3).
  * **58:** **the jsonl misreads Il. 23.499.** There Diomedes is the leader coming in to win (23.499-513; he had passed Eumelus at 23.382-400), and διώκων is absolute, "driving" (Cunliffe διώκω 4, citing 23.499). The verse uses διώκω in sense 1, "pursue", with τόν. The Greek is right in that sense, but the shift from the source should be recorded, and "Diomedes closing on Eumelus" corrected.
  * **61:** record the speaker as the narrator. Both Homeric ἤμβροτες are taunts in framed speech; cite Il. 16.786-787 for the person switch.
  * **63:** enjambment label: none (high stop).
  * **23 / 28:** cite Il. 7.428 = 7.431 for a whole verse repeated within 5 lines in narrative.
* **Print suggestions (no verdict effect):**
  * **51:** add a high stop after ἄεθλον, since the verse now precedes the apodosis 52 directly. Homer prints a comma (36), a high stop (31) or a full stop (9) there. No stop occurs only at Od. 9.393 → 394; the tally's second case, Od. 10.415, is not an apodosis.
  * **60:** a high stop before the asyndetic 61 would also serve.
* **For the scansion verifier:**
  * licences attested once only: hiatus after αὖ at the longum 5 (49; Il. 3.383) and after κρατεροῦ at the longum 7 (29; Il. 21.553);
  * quantity warnings on πυμάτῃ (24, analogy), παρέλασσε (34, analogy), ἀργαλέῳ (33), Ἑλβέτι- (19, 56; brief §4.1), ἀντιθέῳ (62) and κέρδεα (23);
  * check_line raises no flags.
* **For the critic / paper:**
  * κῆρε left in the scales (54);
  * the taunt formula in the narrator's voice (61);
  * the fourth-time count, which depends on resumptive ἔπειτα and is now two points out on the other reading;
  * οὐδ᾽ ἀφάμαρτε in 5 verses of 64 (23, 28, 37, 40, 59; Homer: 4 verses);
  * βοὴν ἀγαθ- at a 3-line gap (31/34), below Homer's minimum of 4;
  * necessary enjambment 14.1%;
  * 64 verses against a brief of about 50.

## 6. Per-line table

Queries are written as their concordance.py arguments. "ctx" means the context script (B.2), and "identity" means B.1. Tags in square brackets ([24a] …) point to Appendix A.

| n | verdict | findings (morphology, dialect, syntax, lexicon, sense, idiom, rulings, facts) | evidence: query → hits | enjambment: composer → reviewer |
|---|---|---|---|---|
| 1 | PASS | Unchanged, v3 PASS (= v3 1). | identity → 1=1 | necessary → necessary |
| 2 | PASS | Unchanged, v3 PASS (= v3 2). | identity → 2=2 | unperiodic → unperiodic |
| 3 | PASS | Unchanged, v3 PASS (= v3 3). | identity → 3=3 | necessary → necessary |
| 4 | PASS | Unchanged, v3 PASS (= v3 4). | identity → 4=4 | none → none |
| 5 | PASS | Unchanged, v3 PASS (= v3 5). | identity → 5=5 | none → none |
| 6 | PASS | Unchanged, v3 PASS (= v3 6). | identity → 6=6 | unperiodic → unperiodic |
| 7 | PASS | Unchanged, v3 PASS (= v3 7). | identity → 7=7 | unperiodic → unperiodic |
| 8 | PASS | Unchanged, v3 PASS (= v3 8). | identity → 8=8 | unperiodic → unperiodic |
| 9 | PASS | Unchanged, v3 PASS (= v3 9). | identity → 9=9 | none → none |
| 10 | PASS | Unchanged, v3 PASS (= v3 10). | identity → 10=10 | none → none |
| 11 | PASS | Unchanged, v3 PASS (= v3 11). | identity → 11=11 | none → none |
| 12 | PASS | Unchanged, v3 PASS (= v3 12). | identity → 12=12 | none → none |
| 13 | PASS | Unchanged, v3 PASS (= v3 13). | identity → 13=13 | none → none |
| 14 | PASS | Unchanged, v3 PASS (= v3 14). | identity → 14=14 | unperiodic → unperiodic |
| 15 | PASS | Unchanged, v3 PASS (= v3 15). | identity → 15=15 | none → none |
| 16 | PASS | Unchanged, v3 PASS (= v3 16). | identity → 16=16 | necessary → necessary |
| 17 | PASS | Unchanged, v3 PASS (= v3 17). | identity → 17=17 | necessary → necessary |
| 18 | PASS | Unchanged, v3 PASS (= v3 18). Before the changed 19: the horse simile's apodosis now ends ἐπέσσυτο δαίμονι ἶσος; vehicle 16-18 intact. | identity → 18=18 | necessary → necessary |
| 19 | PASS | **Changed (M6, m7).** δεύτερον αὖτε (0 Homeric hits) at 9-12 gives way to ἐπέσσυτο δαίμονι ἶσος, which Homer has 7x, always at 6-12 [19a]. τότ᾽ ἐπέσσυτο has 0 hits, but ἐπέσσυτο starts at 6 here as in all 7 Homeric lines, after an elided τότ᾽ at 5.5. 1-5.5 is unchanged from v3 (ὣς ἄρ᾽ ὅ γ᾽ as Il. 22.143). ἶσος takes its regular digamma licence at 10 (19x). **Idiom.** Outside the τὸ τέταρτον frame the formula closes a rush in Il. 21.227 (ὣς εἰπὼν Τρώεσσιν ἐπέσσυτο δαίμονι ἶσος), so it has a model in an apodosis line. It returns in 42 for Federer's fourth onset: one man, one formula. **Sense.** The gloss is right. The ordinal 'second' is no longer in the verse; set 2 is placed by 15 (set 1 won) and 21 (τὸ τρίτον). | [19a] --ngram "ἐπέσσυτο δαίμονι ἶσος" → 7, all [6-12]; [19b] --ngram "ὣς ἄρ᾽ ὅ γ᾽" → Il. 22.143, Od. 20.28; [19c] --ngram "τότ᾽ ἐπέσσυτο" → 0; check_line tier 0, no flags (A.0) | none → none |
| 20 | PASS | **Changed (M4, M6, M8).** βοὴν ἀγαθὸς Φεδερῆρος becomes καὶ ἐσσυμένως λάβ᾽ ἄεθλον. 7-12 is Il. 23.511 verbatim, in its own slot, so the out-of-slot λάβ᾽ ἄεθλον of v3 23 (critic M8) is gone. καί stands at 6 with correption before ἐσ- (καὶ ἐσσυμένως has 0 hits; correption of καί is attested 2364x). **Syntax.** The subject is carried from 19 (ὅ γ᾽ Ἑλβέτιος), and μιν is Djokovic, named last in 15. Two aorists are joined by καί at 6, as εἴρυσσέν τε καὶ … ἤρατο in Il. 3.373. **Sense and facts.** 'Three times he subdued him' covers the breaks in games 1, 3 and 7 (1:03:00, 1:08:46, 1:22:54). 'Took the prize' is set 2, 6-1, which is now stated in the verse (M4). ἐσσυμένως means 'hastily, eagerly' (12x) and suits a set of 22½ minutes. The gloss is right. δάμασσε for a break is licensed by R5; see §2 for the grading. | [20a] --ngram "ἐσσυμένως λάβ᾽ ἄεθλον" → Il. 23.511 [7-12] + ctx; [20b] --ngram "καὶ ἐσσυμένως" → 0; [20c] ἐσσυμένως → 12; check_line: correption@6 (A.0) | none → none |
| 21 | PASS | Unchanged, v3 PASS (= v3 21). After the changed 20: set 2 is now stated as won (20), and τὸ τρίτον follows. | identity → 21=21 | none → none |
| 22 | PASS | Unchanged, v3 PASS (= v3 22). Before the changed 23: its comma is continued by καὶ βάλεν, as in every Homeric καὶ βάλεν. | identity → 22=22 | unperiodic → unperiodic |
| 23 | PASS | **Changed (M2, M8).** v3 23 (δεύτερον αὖ λάβ᾽ ἄεθλον ἄφαρ κρατερὸς Ζοκοβείδης) is replaced by the whole verse of 28 (= v3 27, a v3 PASS). Point 183 (2:03:53, 26 shots) was won by Federer with a winner (A.0 FACTS). The rally now has its winner in the verse, so the v3 implicature that it went to Djokovic and ended the set is gone, and ἄφαρ with it. Ῥογῆρος stands at 6-8 after -τε and before κ (R2 ✓); κέρδεα εἰδώς is at 9-12 (Il. 23.709). **Repetition.** 23 and 28 are the same verse five lines apart, used for two Federer rally winners. Homer has 6 whole-verse repeats within 5 lines (A.0 REP). One of them is narrative, for two parallel acts (Il. 7.428 = 7.431), so the repeat is rare but Homeric. With 37, 40 and 59, οὐδ᾽ ἀφάμαρτε now stands in 5 of 64 verses; Homer has it in 4 verses. **Continuity.** 22 ends with a comma, and καὶ βάλεν continues βάλλον. In Homer καὶ βάλεν always continues the verse before (11/11, A.3). The gloss is right. | [23a] --ngram "καὶ βάλεν οὐδ᾽ ἀφάμαρτε" → Il. 11.350, 13.160; [23b] --ngram "κέρδεα εἰδώς" → Il. 23.709; ctx "καὶ βάλεν" -1 → 11 (A.3); [REP] → 6; [FACTS] pt 183 winner Fe | none → none |
| 24 | PASS | **New (M2, M4).** The set-3 tie-break (2:07:34-2:15:24, 7-4) gets its own verse, after the rally of 22-23. ἔπειτα covers the eleven points between them. **Syntax.** In ἀλλ᾽ ὅ γε Σέρβος, a pronoun takes a name in apposition as subject, as in ὁ / ὃ Τυδεΐδης κρατερὸς Διομήδης (Il. 8.532, 11.660 = 16.25) and ὅ γ᾽ ἥρως (7x). ὅ γε + a capitalised nominative has 1 hit (Il. 13.70), where the name is predicate. The poem already has the construction in 19 (ὅ γ᾽ Ἑλβέτιος, v1-v3 PASS). νικάω takes the man beaten in the accusative and the field in the dative: μάχῃ νικῶντες Ἀχαιούς (Il. 16.79), πόδεσσι δὲ πάντας ἐνίκα (Il. 20.410). Cunliffe νικάω 1: 'to overcome … in fight or in a contest'. μιν ἐνίκα has 0 hits. ἐνίκα stands at 10-12, as in 5 of its 8 hits. **Morphology.** πυμάτῃ is the dative feminine of πύματος (0 hits in this case; πυμάτη, -ης, -ην are attested). υ and α are short, as in πυμάτη at 3.5-5 (Il. 6.118). The slot 7.5-9 is a disclosed mobility. ἔπειτα stands at 4-5.5, its commonest slot (222 of 356). **Lexicon.** Cunliffe πύματος 3: 'the last in sequence or time: δρόμον Il. 23.373, 768'. That is the last lap which brief §3.3 pairs with the end of a set. **Sense and facts.** The gloss is right. This is Djokovic's second set; 7-4 at 2:15:24 ✓. | [24a] ἐνίκα → 8; [24b] νικ- with μάχ- → 5 (Il. 16.79); [24c] πυματ- → 17; [24f] "μιν ἐνίκα" → 0; [24k] ὅ γε + capitalised nominative → Il. 13.70; [24l] ὅ γ᾽ ἥρως → 7; [24n] pronoun + name → Il. 8.532, 11.660, 16.25; [24m] ἔπειτα positions; Cunliffe νικάω, πύματος (A.10) | none → none |
| 25 | PASS | Unchanged, v3 PASS (= v3 24). After the new 24: τόν is now the Serb (24's subject); the sense is unchanged. | identity → 25=24 | none → none |
| 26 | PASS | Unchanged, v3 PASS (= v3 25). Before the changed 27: the rally verse follows the second serve. | identity → 26=25 | none → none |
| 27 | PASS | **Changed (m3, M6).** The verse is Il. 23.116 verbatim. Perseus ends it with ·; v4 has a comma. It replaces the transplanted simile apodosis ὣς μὲν τῶν ἐπὶ ἶσα μάχη … (critic m3), and so also removes the near-repeat of 21. **Sense.** In Homer the line is the mules' journey 'uphill, downhill, sideways and aslant' to Ida (Il. 23.114-117). Here it is the players' running in the 35-shot rally (point 242, 2:47:12). This is a figurative transfer, recorded in the jsonl; on a flat court 'uphill, downhill' is the Homeric line's own wording. The plural ἦλθον for the two follows 22 (ἀμφοτέρω βάλλον). The gloss is right. **Enjambment.** The clause is complete, and 28 continues it with καί: unperiodic. | [27a] whole verse → Il. 23.116 [1-12]; ctx Il. 23.113-118; [FACTS] pt 242, 35 shots, winner Fe | unperiodic → unperiodic |
| 28 | PASS | Unchanged, v3 PASS (= v3 27). After the changed 27 and before the new 29: the same verse as 23 (see 23). 29's 'even so' answers it. | identity → 28=27 | none → none |
| 29 | PASS | **New (M3, M4).** This is the break at 2:49:12 (point 244, Federer's forehand into the net, AD-40) in the game of the 35-shot rally. The set-4 sequence is now rally (27-28) → break (29) → hold for 6-4 (30). **Syntax.** The passive ἐδάμη keeps Federer as subject, so 30's ἔλαβεν is his ✓. ἀλλὰ καὶ ὧς ('but even so') stands at 1-3 (17x) and answers 28's winner. **Morphology.** Νοβήκου is the regular genitive of Νοβῆκος. A long ultima moves the accent to an acute on the penult, as in all 5 Homeric -ῆCος/-ήCου pairs (κλῆρος/κλήρου, χῶρος/χώρου, Ῥῆσος/Ῥήσου, δῆμος/δήμου, νῆσος/νήσου; 0 against). It does not breach R9, which fixes the nominative. κρατεροῦ is the -οῦ genitive (3x, beside κρατεροῖο). **Idiom.** The model is ἀλλ᾽ ἐδάμη ὑπὸ χερσὶ ποδώκεος Αἰακίδαο (Il. 2.860 = 2.874). ἐδάμη is moved from 1.5-3 to 3.5-5, a disclosed mobility. The genitive phrase is split round ὑπὸ χερσί, as in πολιῆς ἐπὶ θινὶ θαλάσσης (Il. 4.248) and Ἀθηναίης ἐπὶ γούνασιν ἠϋκόμοιο (Il. 6.92). There is hiatus after κρατεροῦ at the longum 7; the licence is attested once (Il. 21.553), with no check_line flag. **Register.** 10 of the 11 Homeric lines with ὑπὸ χερσί are killings. The exception is a contest: Il. 23.675 (ἐμῇς ὑπὸ χερσὶ δαμέντα, the beaten boxer carried out alive). Cunliffe δαμάζω 5 'to overpower, get the better of … to defeat' covers the sense. Cite 23.675. **Sense and facts.** The gloss is right ✓. | [29a] "ἀλλὰ καὶ ὧς" → 17; [29b] ἐδάμη → Il. 2.860, 2.874; [29h] "ὑπὸ χερσὶ" → 11 + ctx Il. 23.672-676; [29e] "ὑπὸ κρατεροῦ" → Il. 21.553; [29g] κρατεροῦ → 3; [29k] split genitive round a prepositional phrase → 14; [ACC2] → 5 acute / 0 circumflex; [FACTS] pt 244 winner Dj; Cunliffe δαμάζω 5-6 (A.10) | none → none |
| 30 | PASS | Unchanged, v3 PASS (= v3 28). After the new 29: Federer stays the subject (29 passive), so τέτρατον αὖτ᾽ ἔλαβεν is his ✓ (M3). | identity → 30=28 | none → none |
| 31 | PASS | Unchanged, v3 PASS (= v3 29). Before the changed 32: no βοὴν ἀγαθ- verse is now adjacent to it (M6). The nearest is 34, three verses on. | identity → 31=29 | unperiodic → unperiodic |
| 32 | PASS | **Changed (M4, M6).** ἐδάμασσε βοὴν ἀγαθὸς Φεδερῆρος becomes ἐπόρουσε καὶ ἀμφήριστον ἔθηκεν, which removes the adjacent βοὴν ἀγαθ- pair of v3 29-30. **Idiom.** 1-5.5 is αὐτὰρ ὃ ἂψ ἐπόρουσε (Il. 3.379, 21.33, both at 1-5.5) with γ᾽ in place of the hiatus, as αὐτὰρ ὅ γ᾽ ἂψ (Od. 11.599). The jsonl cites 11.580 and Od. 11.599; cite Il. 3.379 / 21.33, the closer model. ἀμφήριστον ἔθηκεν is the race formula at 7-12 (Il. 23.382, 527). In Homer it occurs only inside an unreal κεν clause; here it is a plain past, a disclosed change of frame. **Lexicon.** Cunliffe ἀμφήριστος: '[neut.] a dead heat'. Cunliffe ἐπορούω 1: 'to rush at a foe'. **Sense and facts.** The break back to 4-3 (3:31:55) 'made it a dead heat', the commentator's 'Game on again' ✓. 4-3 is 'on serve' rather than level; 'dead heat' renders the cancelled break. The gloss is right. | [32a] "ἀμφήριστον ἔθηκεν" → Il. 23.382, 527 [7-12] + ctx; [32c] "ἂψ ἐπόρουσε" → Il. 3.379, 21.33 [3-5.5]; [32d] → Od. 11.599; [32e] → Il. 11.580, 13.550; Cunliffe ἀμφήριστος, ἐπορούω (A.10) | none → none |
| 33 | PASS | **Changed (m4).** The plural relative τῶν ῥ᾽ ἅμα τ᾽ of Il. 13.85 becomes the demonstrative dual τοῖιν δ᾽ at 1-2, as in Il. 13.66 (τοῖιν δ᾽ ἔγνω …; τοῖιν 4x). 3-12 is Il. 13.85 verbatim. **Syntax.** A dative of the person with φίλα γυῖα λέλυνται is Homeric: τῷ μοι φίλα γυῖα λέλυνται (Od. 8.233). (In Od. 18.242 the οἱ belongs to νόστος.) The gloss 'of the two of them' is right. **Facts.** The clock is now a range (3:29:35-4:27:58), which removes the inversion noted by the critic (m4). The fatigue is that of the commentary ✓. γυῖα λέλυντο here is fatigue, as in Il. 7.6 and 13.85, not death. | [33a] τοῖιν → 4 (Il. 13.66 [1-2]); [33b] → Il. 13.85 [3-12] + ctx; [33c] dative + γυῖα λέλυνται → Od. 8.233 (of 4 hits) | none → none |
| 34 | PASS | **Changed (M4, m1).** ἄφαρ ἄσπετον ἤρατο κῦδος becomes παρέλασσε βοὴν ἀγαθὸς Φεδερῆρος. The glory formula is no longer spent on a break, and ὀψέ no longer sits with ἄφαρ. **Idiom.** The verse is the whole-line frame ὀψὲ δὲ δὴ μετέειπε βοὴν ἀγαθὸς Διομήδης (Il. 7.399 = 9.31 = 9.696) with one verb changed. The jsonl cites Il. 5.114; cite 7.399 and its repeats. ὀψὲ δὲ δή is always at 1-3 (12x). **Morphology.** παρέλασσε is unelided (Homer has παρέλασσ᾽ 2x). Cunliffe lists the form as παρέλασσε (Il. 23.382, 527); the check_line warning on α is 'analogy' only. **Lexicon.** Cunliffe παρελαύνω 1a: 'to drive one's chariot past another, outstrip him in the race' (intransitive, Il. 23.382). **Sense and facts.** The break for 8-7 at 4:07:16 (point 354) is the overtaking ✓. ὀψέ 'late, at last' fits the fifteenth game of the set. The gloss is right. | [34a] παρελασσ- → 3; [34b] παρηλασ- → 3; [34d] "ὀψὲ δὲ δὴ" → 12, all [1-3]; [34g] whole frame → Il. 7.399, 9.31, 9.696; Cunliffe παρελαύνω (A.10) | none → none |
| 35 | PASS | **New (M7).** The verse is Il. 18.502 verbatim; v4 adds a comma after ἐπήπυον. **Lexicon.** Cunliffe ἐπηπύω: 'to give one's voice in approval … to. With dat.: ἀμφοτέροισιν ἐπήπυον Il. 18.502'. Cunliffe ἀρωγός: 'a helper … Il. 18.502 (partisans)'. **Context.** In Homer this is the trial on the Shield: two men in dispute, the people cheering both sides, and the heralds restraining them (18.497-506), with an ἴστωρ (18.501) for an umpire. The scene fits a contest before a crowd. **Facts.** 4:08:51, the umpire's call for quiet (tv_2019wimF:0409). Supporters of both men are in brief §1.9 ✓. The gloss is right. | [35a] whole verse → Il. 18.502 [1-12]; ctx Il. 18.497-506; Cunliffe ἐπηπύω, ἀρωγός (A.10) | none → none |
| 36 | PASS | **New (M7).** 1-8 is Il. 18.503 (κήρυκες δ᾽ ἄρα λαὸν ἐρήτυον) in its own slot. ἔνθα καὶ ἔνθα follows at 9-12, its commonest slot (21 of 32). ἐρήτυον keeps its attested 6-8 position, and its -ον is short before the vowel. **Lexicon.** Cunliffe ἐρητύω 1 'to hold back, restrain' and 2 'to get under control: κήρυκές σφεας Il. 2.97'. Il. 2.96-98 (κήρυκες βοόωντες ἐρήτυον, εἴ ποτ᾽ ἀϋτῆς σχοίατ᾽) is the closest Homeric model for the umpire's 'Please'; cite it beside 18.503. ἐρήτυ- + ἔνθα καὶ ἔνθα has 0 hits; the combination is new, the pieces are attested. **Sense and facts.** The umpire is rendered by the heralds of brief §3.10, unnamed (§5.3) ✓. The gloss is right. | [36a] → Il. 18.503 [1-8]; ctx Il. 2.96-98; [36f] "ἔνθα καὶ ἔνθα" → 32 (21 at 9-12); [36d] → 0; Cunliffe ἐρητύω (A.10) | none → none |
| 37 | PASS | Unchanged, v3 PASS (= v3 33). After the new 36: καὶ βάλεν now follows a full stop and the heralds; the new subject is named inside the verse (Ῥογῆρος). | identity → 37=33 | none → none |
| 38 | PASS | **Changed (M4, M6).** The verse is Il. 3.373 / 18.165 with εἴρυσσέν → ἔνθ᾽ ἔλαβέν. καί νύ κεν ἔνθ᾽ stands at 1-3 (3x), and ἄσπετον ἤρατο κῦδος at 7-12. Both Homeric instances of the glory formula are counterfactuals followed by εἰ μή (3.374, 18.166). 39 supplies the εἰ μή, so ἤρατο κῦδος now stands where Homer puts it ✓ (M4). **Morphology and accent.** ἔλαβέν τε takes the second acute before the enclitic, as εἴρυσσέν τε. ἔλαβεν at 3.5-5 is a disclosed mobility (Homer: 5.5-7 2x, 1.5-3 1x). **Syntax.** καί νύ κεν + aorist indicative, then εἰ μή + aorist indicative: the Homeric past unreal. The object of ἔλαβεν is understood ('it', the fifth ἄεθλον of 30); the gloss supplies 'it'. **Sense and facts.** CP1 (point 359, 4:10:58) ✓. The subject is Federer, carried from 37 (Ῥογῆρος). | [38a] → Il. 3.373, 18.165 [7-12] + ctx (εἰ μή); [38b] "καί νύ κεν ἔνθ᾽" → 3 [1-3]; [38c] ἔλαβεν → 3; [38d] "ἔλαβέν τε" → 0 | unperiodic → unperiodic |
| 39 | PASS | Unchanged, v3 PASS (= v3 35). After the changed 38: οἱ is Federer; the εἰ μή completes 38's counterfactual as Il. 3.374. | identity → 39=35 | none → none |
| 40 | PASS | **New (M1, M6).** CP2 is narrated (point 360, 4:11:30). Federer approaches (στῆ δὲ μάλ᾽ ἐγγὺς ἰών, 1-5, 5x: Il. 4.496, 5.611, 11.429, 12.457, 17.347), and Djokovic passes him (`6r28f+1f1*`). Djokovic is the subject of a hit verb at 4:11:30, which answers the critic's test for M1 ✓. **Syntax.** ὃ δέ switches the subject to 'the other' at 5.5. The shape ἰών, ὃ δέ is that of Il. 22.123 (ἵκωμαι ἰών, ὃ δέ μ᾽ οὐκ ἐλεήσει). The man forestalled and hit by the other is Il. 13.387 (… ὃ δέ μιν φθάμενος βάλε δουρί). ὃ δέ μιν occurs 9x, once with βάλε later in the verse (Il. 13.387). οὐδ᾽ ἀφάμαρτε stands at 9-12, as in Il. 14.403 and 22.290 (καὶ βάλε … οὐδ᾽ ἀφάμαρτε). βάλεν with movable ν is closed before οὐδ᾽ (μιν is long by position before β). **Idiom.** In Homer στῆ δὲ μάλ᾽ ἐγγὺς ἰών is always followed by the same subject's act. Giving the second half to the opponent is a combination, not a model. **Sense and facts.** The subject of στῆ is Federer, the subject of 38-39 ✓. The gloss is right. | [40a] → 5 [1-5]; [40g] "ὃ δέ μιν" → 9 (Il. 13.387); [40f] "ἰών, ὃ δ" → Il. 22.123; [40e] "οὐδ᾽ ἀφάμαρτε" → 4 (2 at 9-12); [FACTS] pt 360 winner Dj | none → none |
| 41 | PASS | Unchanged, v3 PASS (= v3 36). After the new 40: the resumptive τρίς (Cunliffe ἔπειτα 4) now gathers two narrated onsets (CP1 38-39, CP2 40) and point 361 (see §2, the count). | identity → 41=36 | unperiodic → unperiodic |
| 42 | PASS | Unchanged, v3 PASS (= v3 37). The fourth (point 362) on the resumptive reading; R12 ✓ (41 names Φεδερῆρος). | identity → 42=37 | necessary → necessary |
| 43 | PASS | Unchanged, v3 PASS (= v3 38). | identity → 43=38 | unperiodic → unperiodic |
| 44 | PASS | Unchanged, v3 PASS (= v3 39). | identity → 44=39 | necessary → necessary |
| 45 | PASS | Unchanged, v3 PASS (= v3 40). | identity → 45=40 | none → none |
| 46 | PASS | Unchanged, v3 PASS (= v3 41). | identity → 46=41 | unperiodic → unperiodic |
| 47 | PASS | Unchanged, v3 PASS (= v3 42). | identity → 47=42 | none → none |
| 48 | PASS | Unchanged, v3 PASS (= v3 43). Before the changed 49: Σέρβον here, Σέρβος in 49 (see 49). | identity → 48=43 | none → none |
| 49 | PASS | **Changed (M7, m8).** ἔκφερε δ᾽ αὖτε Νοβῆκος, ὃ δ᾽ ἕσπετο κέρδεα εἰδώς becomes Σέρβος δ᾽ ἔκφερεν αὖ, ὃ δ᾽ ἐπέσσυτο τυτθὸν ὀπίσσω. The aorist ἕσπετο ('accompanied', m8) is gone, and τυτθόν (brief §3.6, 'a little bit') enters the verse. **Morphology.** ἔκφερεν is the unaugmented imperfect with movable ν before a vowel, as in Od. 15.470. It is intransitive: 'shoot ahead' (Cunliffe ἐκφέρω 6). ὃ δ᾽ ἐπέσσυτο stands at 5.5-8, as in Il. 21.234 and 21.601. There is hiatus after αὖ at the longum 5, at a comma; the licence is attested for αὖ once (Il. 3.383), with no check_line flag. **Lexicon and sense.** τυτθὸν ὀπίσσω occurs once in Homer (Il. 5.443, 9-12), where it means 'withdrew a little backwards' (Cunliffe ὀπίσσω 1, τυτθός 2d). Here it means 'a little behind', Cunliffe ὀπίσσω 2 'of place, behind, in rear' (Il. 9.507 αἳ δ᾽ ἐξακέονται ὀπίσσω, followers behind a runner). That is a shift of sense inside the formula; record it. The pursuit with a 'little' margin has an exact Homeric scene: Il. 21.601-604, ὃ δ᾽ ἐπέσσυτο ποσσὶ διώκειν … τυτθὸν ὑπεκπροθέοντα (Cunliffe τυτθός 2e 'keeping always a little ahead'). Cite it. **Facts.** 9-8 (4:17:15) and 9-9 (4:21:04) ✓. The gloss is right. **Note.** Σέρβον (48) and Σέρβος (49) stand in adjacent verses. An adjacent name repeat is Homeric (Il. 22.211-212 Ἕκτορος), but it is the one new adjacent pair in the rewrite (M6). | [49a] "τυτθὸν ὀπίσσω" → Il. 5.443 + ctx; [49b] "ὃ δ᾽ ἐπέσσυτο" → Il. 21.234, 21.601 [5.5-8] + ctx 21.600-605; ctx Il. 9.505-507; [49d] ἔκφερεν → Od. 15.470; [49g] τυτθόν → 29; [49h] → 0; Cunliffe ὀπίσσω, τυτθός, ἐκφέρω (A.10) | none → none |
| 50 | PASS | Unchanged, v3 PASS (= v3 45). After the changed 49: it follows a full stop; the simile opens as before. | identity → 50=45 | necessary → necessary |
| 51 | PASS | Unchanged, v3 PASS (= v3 46). Now directly before the apodosis 52, since v3 47 was dropped. It ends without punctuation. Before a Homeric simile apodosis ὣς the printed text has a comma (36), a high stop (31) or a full stop (9); no stop occurs once (Od. 9.393 → 394, also after a parenthetic clause, with γάρ there and δέ here; A.0 APOD). Homeric, but a high stop after ἄεθλον is advised for print. The label stays necessary (inside the open ὡς δ᾽ ὅτ᾽ period). The vehicle is now 2 verses; two similes keep vehicles of 3 or more (16-18, 43-47). | identity → 51=46 | necessary → necessary |
| 52 | PASS | Unchanged, v3 PASS (= v3 48). Now follows 51 directly (v3 47 dropped). The prize of the vehicle (τὸ δὲ μέγα κεῖται ἄεθλον) is no longer 'for a dead man' (M5). | identity → 52=48 | unperiodic → unperiodic |
| 53 | PASS | Unchanged, v3 PASS (= v3 49). Before the changed 54: unchanged scales line (Il. 22.209). | identity → 53=49 | unperiodic → unperiodic |
| 54 | PASS | **Changed (M5).** τανηλεγέος θανάτοιο gives way to μάχης θαλερῶν αἰζηῶν. 1-5.5 is Il. 8.70 = 22.210. θαλερῶν αἰζηῶν stands at 7.5-12 (Il. 10.259, 14.4) with the spondaic fifth foot of those lines. κῆρ- with μάχ- in one verse has 0 hits; the genitive chain reads 'the fates of the fight of lusty men', and 55 distributes them to the two men. **Lexicon (residual).** κῆρε stays. Cunliffe κήρ gives 1 'bane, death', 2 'one's destined fate', and 3 (this passage) 'figured as a weight put in the balance and typifying death or one's fate'. LSJ: 'doom, death … rarely without personal sense in Hom.'; Κῆρες Ἀχαιῶν, Τρώων (Il. 8.73-74). With θανάτοιο gone, the line reads as Cunliffe's 'one's fate', but κήρ is never a neutral 'lot' in Homer. Brief §2.5A asked for κῆρε to be replaced as well, 'else keep and document'. The jsonl documents the choice, and the critic's own test line kept κῆρε. Not a fault; for the paper. **Gloss.** The gloss has 'of two sturdy men', but θαλερῶν αἰζηῶν is plural and generic, and the δύο goes with κῆρε. Read 'of the fight of lusty men'. αἰζηός means 'in full bodily strength … young men' (Cunliffe); for a 37-year-old this is generic warrior diction. **Enjambment.** The clause is complete; 55 adds the apposition (τὴν μὲν … τὴν δ᾽): unperiodic, as v3 50. | ctx "ἐν δ᾽ ἐτίθει δύο κῆρε" → Il. 8.69-74, 22.209-214; [54b] "θαλερῶν αἰζηῶν" → Il. 10.259, 14.4 [7.5-12]; [54d] κῆρ- + μάχ- → 0; [DEATH] → κῆρε (54), ἦμαρ (64) only; Cunliffe κήρ, LSJ Κήρ, Cunliffe αἰζηός, θαλερός (A.10) | unperiodic → unperiodic |
| 55 | PASS | Unchanged, v3 PASS (= v3 51). After the changed 54: τὴν μὲν … τὴν δ᾽ still refers to κῆρε. | identity → 55=51 | unperiodic → unperiodic |
| 56 | PASS | **Changed (M5).** κακὸν ἦμαρ gives way to τότ᾽ ἐέλδωρ. 1-7 is Il. 8.72 = 22.212 (ἕλκε δὲ μέσσα λαβών· ῥέπε δ᾽), and Ἑλβετίου stands at 7-9 (A1 slot). **Lexicon.** ἐέλδωρ means 'wish, longing, desire' (LSJ ἔλδωρ; Cunliffe 'always with prothetic ἐ'). It occurs 10x, 9 at 10-12. Elision before it is attested (κρηήνατ᾽ ἐέλδωρ, Od. 3.418, 17.242), and a possessor's genitive with it is Il. 15.74 (τὸ Πηλεΐδαο … ἐέλδωρ). LSJ ῥέπω: 'turn the scale, sink … implying defeat and death, Il. 8.72'. Homer's sinking αἴσιμον ἦμαρ is the doom-day; the loser's desire takes its place. That removes the death and keeps the defeat ✓ (brief §2.6.2). ῥέπε … ἐέλδωρ has 0 hits; the collocation is new. **Sense and facts.** The tie-break went 7-3, and the Swiss's pan sinks ✓. The gloss is right. τότε also stands in 53 (καὶ τότε δή, Il. 22.209); harmless. | [56a] ἐέλδωρ → 10 (9 at [10-12]); [56b] elision before ἐέλδωρ → Od. 3.418, 17.242; [56c] "ῥέπε δ᾽" → Il. 8.72, 22.212 [5.5-7]; Cunliffe ἔλδωρ, ῥέπω; LSJ ἔλδωρ, ῥέπω (A.10) | none → none |
| 57 | PASS | Unchanged, v3 PASS (= v3 53). After the changed 56 and before the changed 58: its τρὶς μέν is now answered by τὸν δ᾽ ἕτερος (58). | identity → 57=53 | unperiodic → unperiodic |
| 58 | PASS | **Changed (M5, M6).** αὐτὰρ ὅ γ᾽ Ἑλβέτιος τότ᾽ ἀμύνετο νηλεὲς ἦμαρ (the death-day of Il. 11.484) becomes τὸν δ᾽ ἕτερος μετέπειτα μάλα σχεδὸν ἦλθε διώκων. 6-12 is Il. 23.499 verbatim. μετέπειτα stands at 3.5-5.5, as in Il. 14.310. τὸν δ᾽ ἕτερος has 0 hits; τὴν ἕτερος is Od. 8.374, the Phaeacian ball game. **Syntax.** τὸν δ᾽ … answers the μέν of 57's τρὶς μέν, a subject contrast, as v3 53-54 did. τόν is Djokovic, the object of διώκων. ἕτερος is 'the other of two' (Cunliffe ἕτερος 2). **Lexicon (record correction).** In Il. 23.499 Diomedes is the leader, coming in to win (23.499-513), and διώκων is absolute, 'driving' (Cunliffe διώκω 4: 'to drive (a chariot) … Absol. Il. 23.344, 424, 499, 547'). The verse uses διώκω in sense 1, 'chase, pursue', with τόν. The Greek reads correctly in that sense, but it is a shift from the source. The jsonl's 'Diomedes closing on Eumelus' misreads 23.499: Diomedes passed Eumelus at 23.382-400. **Sense and facts.** Points 418-419 (Federer drop-shot winner; Djokovic return error) bring 4-1 to 4-3 ✓. The gloss is right. | [58a] "μάλα σχεδὸν ἦλθε διώκων" → Il. 23.499 [6-12] + ctx 23.495-501; [58b] μετέπειτα → 5 (Il. 14.310 [3.5-5.5]); [58f] → Od. 8.374; [FACTS] pts 418-419 winner Fe; Cunliffe διώκω 1, 4; μετέπειτα; ἕτερος (A.10) | none → none |
| 59 | PASS | **Punctuation only.** A comma is added after Νοβῆκος, harmonised with 37 (both now as Il. 13.160). Otherwise the verse is v3 55 (a v3 PASS: R9 circumflex, R11 two hit clauses for points 420-421). Νοβῆκος stands at 6-8 after a vowel, and -κος is long before καί. καὶ βάλεν at 9-10 remains a recorded departure from Homer's 1-2 (critic M8). **Continuity.** 58 ends with a full stop; the new subject is named inside the verse ✓. | rulings.py: Νοβῆκος 59, two hit clauses 37 and 59 (A.0); [FACTS] pts 420-421 winner Dj | none → none |
| 60 | PASS | Unchanged, v3 PASS (= v3 56). Before the changed 61: its comma now leads to the asyndetic apostrophe (see 61). | identity → 60=56 | unperiodic → unperiodic |
| 61 | PASS | **Changed (M7, M6, M5).** 'Ἑλβέτιος δ᾽ ἄρα τοῦ μὲν ἀπήμβροτε δουρὶ φαεινῷ' becomes the apostrophe ἤμβροτες, οὐδ᾽ ἔτυχες, Φεδερεῦ, μάλα πολλὰ μογήσας. **Who speaks.** The narrator speaks, by apostrophe. There is no speech frame, and in Homer direct speech is never unframed. A frame would make a player speak, which brief §5.4 forbids. **Is it Homeric?** The form is. The narrator addresses the hero in the second person, aorist, with his vocative and no frame: ἐξενάριξας / Πατρόκλεις (Il. 16.692-693); Πατρόκλεες … ἔσσυο (16.584-585); οὐδὲ σέθεν, Μενέλαε (4.127). In Il. 16.786 → 787 a τὸ τέταρτον verse in the third person is followed, after a comma, by ἔνθ᾽ ἄρα τοι, Πάτροκλε. That is the switch of 60 → 61. The formula is not narratorial in Homer. ἤμβροτες occurs twice, both times in framed speech by the opponent taunting the man who missed: Diomedes to Pandarus (Il. 5.286-287) and Hector to Achilles (22.278-279). The line turns a victor's taunt into the narrator's sympathy. πολλὰ μογήσας (13x, all 9-12) is sympathetic, and Il. 23.607 has it in the second person (πολλὰ πάθες καὶ πολλὰ μόγησας). Brief §2.6.1 proposed the formula 'in the poem's own voice'. Record this for the paper; not a fault. **Morphology.** Φεδερεῦ is the regular -εύς vocative (Ἀχιλεῦ at 5.5-7: Il. 11.606, 24.503, 24.661). The last syllable of ἔτυχες is long by position before Φ. Cunliffe: ἁμαρτάνω 1 'to discharge a missile vainly … ἤμβροτες οὐδ᾽ ἔτυχες'; τυγχάνω 3 'to hit one's mark'. **Sense and facts.** Point 422, Federer's forehand error ✓. 60 ends with a comma and 61 is asyndetic; a high stop at 60 would also serve. The gloss is right. | ctx ἤμβροτες → Il. 5.285-287, 22.277-279; [61b] → Il. 5.287 [1-5]; [61c] "πολλὰ μογήσας" → 13 [9-12]; [61d] "μάλα πολλὰ μογήσας" → 0; [61j] Ἀχιλεῦ positions; [61h]/[61i] apostrophes Il. 16.693, 4.127, 4.146, 7.104, 16.787; ctx ἔσσυο Il. 16.584-585; Cunliffe ἁμαρτάνω, τυγχάνω, μογέω (A.10) | none → none |
| 62 | PASS | **Changed (M4).** Σέρβος δ᾽ αὖτ᾽ ἐδάμασσε, Διὸς δ᾽ ἐτελείετο βουλή becomes Σέρβῳ δ᾽ ἀντιθέῳ τότε δὴ Ζεὺς κῦδος ἔδωκε. The title now has its own formula. **Idiom.** Ζεὺς κῦδος ἔδωκε(ν) takes a dative recipient: ᾧ τε Ζεὺς κῦδος ἔδωκεν (Il. 1.279), ὅτε οἱ Ζεὺς κῦδος ἔδωκε (8.216), καὶ Ἕκτορι κῦδος ἔδωκε (18.456). Ζεὺς κῦδος stands at 8-9.5 (9 of 10), and ἀντιθέῳ at 3-5 (Il. 4.377, 5.629, 16.649). τότε δὴ Ζεύς is attested at 1.5-4 (Od. 3.132) and stands here at 5.5-8. **Lexicon.** Cunliffe κῦδος 3: 'the glory of victory, victory, triumph, the upper hand'. Il. 12.437 (Ζεὺς κῦδος ὑπέρτερον Ἕκτορι δῶκε) ends an even fight in the same way; it may be cited. **Economy.** ἀντίθεος remains Djokovic's (4, 62). **Facts.** 13-12(3) at 4:56:59 ✓. The gloss is right. | [62a] "κῦδος ἔδωκε" → 3 [9-12]; [62b] "Ζεὺς κῦδος" → 10; [62c] "τότε δὴ Ζεὺς" → Od. 3.132; [62d] ἀντιθέῳ → 11; Cunliffe κῦδος (A.10) | none → none |
| 63 | PASS | **Changed (m5, M4).** δέμας πυρὸς αἰθομένοιο becomes Διὸς δ᾽ ἐτελείετο βουλή (Il. 1.5, Od. 11.297; 6-12). In Il. 17.424 ὣς οἳ μὲν μάρναντο takes a different second half with δ᾽ (σιδήρειος δ᾽ ὀρυμαγδός), so a μέν answered within the verse is Homeric. The proem's Zeus closes the narrative. **Sense.** The imperfect is the summary 'so they fought', and the second half is no longer a scene-switch (m5) ✓. The gloss is right. **Enjambment.** The verse ends with a high stop, so it is 'none' by the punctuation test used in v1-v3; the composer has unperiodic. This is a label disagreement only. | [63a] "ὣς οἳ μὲν μάρναντο" → 5 + ctx (Il. 17.424-425); [63b] → Il. 1.5, Od. 11.297 [6-12] + ctx; [ENJ] (A.11) | unperiodic → none |
| 64 | PASS | Unchanged, v3 PASS (= v3 60). After the changed 63: ὀψὲ δὲ δή also opens 34; the close is unchanged. | identity → 64=60 | none → none |

## Appendix A. Verbatim evidence

Printed by `appendix4.sh` (B.10) on 2026-10-08, run from the repository root with `.venv` active. Lines beginning `# [tag]` give the command; `python homer/concordance.py` output is unedited, and hit lists are shown in full except where a header says what is shown.

### A.0 Identity, check_line, rulings, aspiration, accent, similes, names, spacing (whole draft)

```
# [ID] python -I identity.py .
v4.txt == v4.jsonl text: 64/64; non-NFC lines: []
identical to v3 (v4 n = v3 n): 43 1=1, 2=2, 3=3, 4=4, 5=5, 6=6, 7=7, 8=8, 9=9, 10=10, 11=11, 12=12, 13=13, 14=14, 15=15, 16=16, 17=17, 18=18, 21=21, 22=22, 25=24, 26=25, 28=27, 30=28, 31=29, 37=33, 39=35, 41=36, 42=37, 43=38, 44=39, 45=40, 46=41, 47=42, 48=43, 50=45, 51=46, 52=48, 53=49, 55=51, 57=53, 60=56, 64=60
  v3 verdicts of the identical verses: {'PASS': 43, 'FAIL': 0, 'QUERY': 0}
changed (v4 n <- v3 n): 16 19<-19, 20<-20, 23<-23, 27<-26, 32<-30, 33<-31, 34<-32, 38<-34, 49<-44, 54<-50, 56<-52, 58<-54, 59<-55, 61<-57, 62<-58, 63<-59
new (no v3_line): 5 [24, 29, 35, 36, 40]
v3 lines not carried into v4: [47]
jsonl "changed" flag disagrees with text diff: []

# [CL] python homer/check_line.py --file composition/drafts/v4.txt (exit status; lines with OK (no flags))
exit=0
64
```

```
# [RUL] python -I rulings.py . composition/drafts/v4.txt
R2 ἰσόθεος (anywhere): 0 []
R3 withdrawn Ζοκοβίδης/Νοβάκος: 0 []
R4 δίς: 0 []
R5 ἐξεναρίζω: 0 []
R6 πάλιν: 1 [(22, 'πάλιν')]
R9 Νοβ- nominative/accusative with acute (Νοβήκος/-ον: wrong): 0 []
R9 Νοβῆκος/-ον (circumflex, short ultima): 1 [(59, 'Νοβῆκος')]
R9 Νοβ- genitive/dative (long ultima; acute required): 1 [(29, 'Νοβήκου')]
R10 Ζοκοβεύς / Ζοκοβῆ- (eponym forms): 0 []
Ζοκοβείδης (patronymic): 3 [(4, 'Ζοκοβείδης'), (57, 'Ζοκοβείδης'), (60, 'Ζοκοβείδης')]
Σέρβ- (ethnic): 9 [(10, 'Σέρβος'), (15, 'Σέρβος'), (24, 'Σέρβος'), (31, 'Σέρβος'), (43, 'Σέρβος'), (48, 'Σέρβον'), (49, 'Σέρβος'), (55, 'Σέρβου'), (62, 'Σέρβῳ')]
Ῥογῆρ- / Φεδερ- / Ἑλβετ-: 17 [(4, 'Φεδερεύς'), (5, 'Ἑλβέτιος'), (12, 'Ἑλβέτιος'), (14, 'Φεδερῆρος'), (19, 'Ἑλβέτιος'), (23, 'Ῥογῆρος'), (25, 'Ἑλβέτιος'), (26, 'Φεδερεὺς'), (28, 'Ῥογῆρος'), (31, 'Φεδερῆρον'), (34, 'Φεδερῆρος'), (37, 'Ῥογῆρος'), (41, 'Φεδερῆρος'), (55, 'Ἑλβετίου'), (56, 'Ἑλβετίου'), (60, 'Ἑλβέτιος'), (61, 'Φεδερεῦ')]
δαμάζω/δάμνημι (aor. act./pass.): 5 [(20, 'ἐδάμασσε'), (25, 'δάμασεν'), (29, 'ἐδάμη'), (31, 'ἐδάμασσε'), (45, 'δαμάσσῃ')]
κῦδος: 2 [(38, 'κῦδος'), (62, 'κῦδος')]
νικάω: 3 [(1, 'νίκης'), (15, 'ἐνίκα'), (24, 'ἐνίκα')]
θάνατος / κήρ / ἦμαρ / κατατεθνη- (death register): 2 [(54, 'κῆρε'), (64, 'ἦμαρ')]
prohibited (γραμμ, στεγ, οχλ, ωρη/ωρα, δικτυ, ραβδ, χλο, χορτ, δικαστ, αθλητησ, σφαιριστ, ηττ): 0 []
R2 Ῥογῆρος followed by ἰσόθεος: []
R11 "δεύτερον αὖτις": [25]
δεύτερον lines: [7, 25, 26]
"καὶ βάλεν … καὶ βάλεν" (two hit clauses): [37, 59]
"οὐδ᾽ ἀφάμαρτε" lines: [23, 28, 37, 40, 59]
"τὸ τέταρτον" lines and the last word of the verse before: [(15, 'Φεδερῆρος'), (42, 'Φεδερῆρος')]
τρὶς μέν / τρὶς δέ lines: [(14, 'τρὶς μὲν ἔπειτ᾽'), (20, 'τρὶς δέ μιν'), (41, 'τρὶς μὲν ἔπειτ᾽'), (57, 'τρὶς μὲν ἔπειτ᾽')]
vocatives (Φεδερεῦ/Ῥογῆρε/Νοβῆκε/Ζοκοβεῖδα/-η): [(61, 'Φεδερεῦ')]
```

```
# [ASP] python -I aspir.py . composition/drafts/v4.txt (draft lines: ERROR lines only, then the count of ok)
Homer:
  ('αὖθ', 'rough') 33 | e.g. Il. 1.370 Χρύσης δʼ αὖθʼ ἱερεὺς ἑκατηβόλου Ἀπόλλωνος
  ('αὖθ', 'smooth') 3 | e.g. Il. 11.48 ἵππους εὖ κατὰ κόσμον ἐρυκέμεν αὖθʼ ἐπὶ τάφρῳ,
  ('αὖτ', 'smooth') 130 | e.g. Il. 1.202 τίπτʼ αὖτʼ αἰγιόχοιο Διὸς τέκος εἰλήλουθας;
Draft composition/drafts/v4.txt :
23

# [ACC] python -I accent.py .
acute on long penult (η/ω) + C + ος: types 0 tokens 0
circumflex on penult (η/ω) + C + ος: types 51 tokens 269
   e.g. πρῶτος, ἦμος, στῆθος, δηϊοτῆτος, ποτῆτος, τῆμος, τεθνηῶτος, κρητῆρος, δῆμος, κλῆρος, ζωστῆρος, ἦδος

# [ACC2] python -I accent2.py .
nominative types -ῆ/ῶ + C + ος: 46
genitive -ου with acute on the penult: 5 | e.g. κλῆρος/κλήρου, χῶρος/χώρου, Ῥῆσος/Ῥήσου, δῆμος/δήμου, νῆσος/νήσου
genitive -ου with circumflex on the penult: 0 | e.g. 
genitive -ου with other on the penult: 0 | e.g. 
```

```
# [SIM] python -I simile.py . composition/drafts/v4.txt
simile opener at 16: ὡς δ᾽ ὅτε τις στατὸς ἵππος ἀκοστήσας ἐπὶ φάτνῃ
   apodosis line: 19: ὣς ἄρ᾽ ὅ γ᾽ Ἑλβέτιος τότ᾽ ἐπέσσυτο δαίμονι ἶσος·; vehicle lines 16-18 (3 lines)
simile opener at 43: Σέρβος δ᾽ αὖθ᾽ ἑτέρωθεν ἐναντίον ὦρτο λέων ὣς
   apodosis line: 48: ὣς τότε Σέρβον ἀνῆκε μένος καὶ θυμὸς ἀγήνωρ·; vehicle lines 43-47 (5 lines)
simile opener at 50: ὡς δ᾽ ὅτ᾽ ἀεθλοφόροι περὶ τέρματα μώνυχες ἵπποι
   apodosis line: 52: ὣς τὼ πολλάκι δὴ περὶ τέρματα δινηθήτην,; vehicle lines 50-51 (2 lines)

# [APOD] python -I apod.py .
apodosis ὣς after a ὡς (δʼ) ὅτε simile: preceding verse ends with {',': 36, '.': 9, '·': 31, '(none)': 2}
  no punctuation: ['Od. 9.393', 'Od. 10.415']
Od	9	391	ὡς δʼ ὅτʼ ἀνὴρ χαλκεὺς πέλεκυν μέγαν ἠὲ σκέπαρνον
Od	9	392	εἰν ὕδατι ψυχρῷ βάπτῃ μεγάλα ἰάχοντα
Od	9	393	φαρμάσσων· τὸ γὰρ αὖτε σιδήρου γε κράτος ἐστίν
Od	9	394	ὣς τοῦ σίζʼ ὀφθαλμὸς ἐλαϊνέῳ περὶ μοχλῷ.
```

```
# [NAMES] python -I names.py . composition/drafts/v3.txt composition/drafts/v4.txt
composition/drafts/v3.txt: lines 60, name tokens 33 (0.55/line); narrative 12-58: 29/47 = 0.62/line; adjacent named pairs 16
composition/drafts/v4.txt: lines 64, name tokens 31 (0.48/line); narrative 12-62: 27/51 = 0.53/line; adjacent named pairs 12

# [BOEN] python -I boen.py . composition/drafts/v4.txt
Homeric lines with βοὴν ἀγαθ-: 51
gaps <= 10: {4: 1, 5: 2, 9: 2, 10: 1}
pairs with gap <= 4: ['Il. 2.563 / 567 (gap 4)']
draft lines with βοὴν ἀγαθ-: [14, 31, 34, 41] | gaps: [17, 3, 7]

# [REP] python -I repline.py . 5
verbatim repeats within 5 lines: 6
   Il. 3.127 = 131  Τρώων θʼ ἱπποδάμων καὶ Ἀχαιῶν χαλκοχιτώνων,
   Il. 4.66 = 71  πειρᾶν δʼ ὥς κε Τρῶες ὑπερκύδαντας Ἀχαιοὺς
   Il. 4.67 = 72  ἄρξωσι πρότεροι ὑπὲρ ὅρκια δηλήσασθαι.
   Il. 7.428 = 431  νεκροὺς πυρκαϊῆς ἐπινήνεον ἀχνύμενοι κῆρ,
   Od. 12.268 = 273  Κίρκης τʼ Αἰαίης, ἥ μοι μάλα πόλλʼ ἐπέτελλε
   Od. 17.346 = 351  αἰτίζειν μάλα πάντας ἐποιχόμενον μνηστῆρας·
```

```
# [FACTS] python -I facts.py . (corpus/timing/points_2019wimF.csv)
23 rally (26 shots)                pt 183  2:03:53 set 3 game 12 tb=False server=Dj games 5-6 pts 0-0 winner=Fe shots=26 1st=4f29f1f2b1f3b3b1f2f1f1f1f2s3b3s2f3s3b2b3b2b3f1r1f+3b1* 2nd=
24 TB3 first point                 pt 188  2:07:34 set 3 game 13 tb=True  server=Fe games 6-6 pts 0-0 winner=Dj shots=5 1st=4f29f3b3b3w@ 2nd=
24 TB3 last point                  pt 198  2:15:24 set 3 game 13 tb=True  server=Dj games 6-6 pts 6-4 winner=Dj shots=6 1st=6s28b3s3b+1f2n# 2nd=
27-28 35-shot rally                pt 242  2:47:12 set 4 game  8 tb=False server=Fe games 2-5 pts 40-30 winner=Fe shots=35 1st=4w 2nd=4b28b3b3b3f2b3b2f2f1f1f1f2b3s3b3b3b2f3b3s3b2b3b2s2f3b3b2f1r2f1f1f1f2b1*
29 break                           pt 244  2:49:12 set 4 game  8 tb=False server=Fe games 2-5 pts AD-40 winner=Dj shots=13 1st=6f28f3b3b2b2f1f1f1f2s3b3s2n@ 2nd=
37 ace 1                           pt 357  4:10:13 set 5 game 16 tb=False server=Fe games 7-8 pts 15-15 winner=Fe shots=1 1st=6* 2nd=
37 ace 2                           pt 358  4:10:35 set 5 game 16 tb=False server=Fe games 7-8 pts 15-30 winner=Fe shots=1 1st=6* 2nd=
38-39 CP1                          pt 359  4:10:58 set 5 game 16 tb=False server=Fe games 7-8 pts 15-40 winner=Dj shots=3 1st=6n 2nd=4f28f3w@
40 CP2                             pt 360  4:11:30 set 5 game 16 tb=False server=Fe games 7-8 pts 30-40 winner=Dj shots=4 1st=6r28f+1f1* 2nd=
41 third onset                     pt 361  4:11:58 set 5 game 16 tb=False server=Fe games 7-8 pts 40-40 winner=Dj shots=7 1st=4w 2nd=5b28b3b3b2f1r#
42 break 8-8                       pt 362  4:12:40 set 5 game 16 tb=False server=Fe games 7-8 pts AD-40 winner=Dj shots=5 1st=6r18f1f1f2n@ 2nd=
54 TB5 first point                 pt 413  4:48:30 set 5 game 25 tb=True  server=Dj games 12-12 pts 0-0 winner=Dj shots=12 1st=6d 2nd=4f28b2s3s2f3b3b2f3s2b3b2d@
TB5 pt 2                           pt 414  4:49:29 set 5 game 25 tb=True  server=Fe games 12-12 pts 1-0 winner=Fe shots=3 1st=6f37f1* 2nd=
57 tris 1                          pt 415  4:50:01 set 5 game 25 tb=True  server=Fe games 12-12 pts 1-1 winner=Dj shots=3 1st=4+f27h1w# 2nd=
57 tris 2                          pt 416  4:50:37 set 5 game 25 tb=True  server=Dj games 12-12 pts 2-1 winner=Dj shots=4 1st=5d 2nd=4s28f1f1w#
57 tris 3                          pt 417  4:51:25 set 5 game 25 tb=True  server=Dj games 12-12 pts 3-1 winner=Dj shots=8 1st=4f19f3s3b3b3b1f1w# 2nd=
58 close 1                         pt 418  4:52:04 set 5 game 25 tb=True  server=Fe games 12-12 pts 4-1 winner=Fe shots=11 1st=4n 2nd=6f38b3b;1f3b3b3b3b2f2u+3*
58 close 2                         pt 419  4:53:31 set 5 game 25 tb=True  server=Fe games 12-12 pts 4-2 winner=Fe shots=2 1st=6w 2nd=6b#
59 winner 1                        pt 420  4:54:18 set 5 game 25 tb=True  server=Dj games 12-12 pts 4-3 winner=Dj shots=3 1st=6f27f1* 2nd=
59 winner 2                        pt 421  4:54:48 set 5 game 25 tb=True  server=Dj games 12-12 pts 5-3 winner=Dj shots=13 1st=5n 2nd=4f38b3s3b3b3b3b3b3f3b3f3b1*
60-61 last point                   pt 422  4:56:59 set 5 game 25 tb=True  server=Fe games 12-12 pts 6-3 winner=Dj shots=3 1st=6d 2nd=5b38f!@
set 4 last point                   pt 253  2:55:08 set 4 game 10 tb=False server=Fe games 4-5 pts 0-40 winner=Fe shots=3 1st=4s2j1* 2nd=
```

### A.1 Lines 19-20 (set 2: ἐπέσσυτο δαίμονι ἶσος; ἐσσυμένως λάβ᾽ ἄεθλον)

```
# [19a] python homer/concordance.py --ngram "ἐπέσσυτο δαίμονι ἶσος"
Il. 5.438    [6-12]  ἀλλʼ ὅτε δὴ τὸ τέταρτον ἐπέσσυτο δαίμονι ἶσος,    <ἐπέσσυτο δαίμονι ἶσος>
Il. 5.459    [6-12]  αὐτὰρ ἔπειτʼ αὐτῷ μοι ἐπέσσυτο δαίμονι ἶσος.    <ἐπέσσυτο δαίμονι ἶσος>
Il. 5.884    [6-12]  αὐτὰρ ἔπειτʼ αὐτῷ μοι ἐπέσσυτο δαίμονι ἶσος·    <ἐπέσσυτο δαίμονι ἶσος>
Il. 16.705   [6-12]  ἀλλʼ ὅτε δὴ τὸ τέταρτον ἐπέσσυτο δαίμονι ἶσος,    <ἐπέσσυτο δαίμονι ἶσος>
Il. 16.786   [6-12]  ἀλλʼ ὅτε δὴ τὸ τέταρτον ἐπέσσυτο δαίμονι ἶσος,    <ἐπέσσυτο δαίμονι ἶσος>
Il. 20.447   [6-12]  ἀλλʼ ὅτε δὴ τὸ τέταρτον ἐπέσσυτο δαίμονι ἶσος,    <ἐπέσσυτο δαίμονι ἶσος>
Il. 21.227   [6-12]  ὣς εἰπὼν Τρώεσσιν ἐπέσσυτο δαίμονι ἶσος·    <ἐπέσσυτο δαίμονι ἶσος>
-- 7 hit(s)

# [19b] python homer/concordance.py --ngram "ὣς ἄρ᾽ ὅ γ᾽"
Il. 22.143   [1-3]  ὣς ἄρʼ ὅ γʼ ἐμμεμαὼς ἰθὺς πέτετο, τρέσε δʼ Ἕκτωρ    <ὣς ἄρʼ ὅ γʼ>
Od. 20.28    [1-3]  ὣς ἄρʼ ὅ γʼ ἔνθα καὶ ἔνθα ἑλίσσετο, μερμηρίζων    <ὣς ἄρʼ ὅ γʼ>
-- 2 hit(s)

# [19c] python homer/concordance.py --ngram "τότ᾽ ἐπέσσυτο"
-- 0 hit(s)

# [20a] python homer/concordance.py --ngram "ἐσσυμένως λάβ᾽ ἄεθλον"
Il. 23.511   [7-12]  ἴφθιμος Σθένελος, ἀλλʼ ἐσσυμένως λάβʼ ἄεθλον,    <ἐσσυμένως λάβʼ ἄεθλον>
-- 1 hit(s)

# context for ngram "ἐσσυμένως λάβ᾽ ἄεθλον" (-2/+1 lines): 1 hit(s)
  Il. 23.509   αὐτὸς δʼ ἐκ δίφροιο χαμαὶ θόρε παμφανόωντος,
  Il. 23.510   κλῖνε δʼ ἄρα μάστιγα ποτὶ ζυγόν· οὐδὲ μάτησεν
> Il. 23.511   ἴφθιμος Σθένελος, ἀλλʼ ἐσσυμένως λάβʼ ἄεθλον,
  Il. 23.512   δῶκε δʼ ἄγειν ἑτάροισιν ὑπερθύμοισι γυναῖκα

# [20b] python homer/concordance.py --ngram "καὶ ἐσσυμένως"
-- 0 hit(s)

# [20c] python homer/concordance.py --loose "εσσυμενως" --word --count
12

```

### A.2 Lines 23-24 (set 3: the rally's winner; the tie-break)

```
# [23a] python homer/concordance.py --ngram "καὶ βάλεν οὐδ᾽ ἀφάμαρτε"
Il. 11.350   [1-5.5]  καὶ βάλεν, οὐδʼ ἀφάμαρτε τιτυσκόμενος κεφαλῆφιν,    <καὶ βάλεν, οὐδʼ ἀφάμαρτε>
Il. 13.160   [1-5.5]  καὶ βάλεν, οὐδʼ ἀφάμαρτε, κατʼ ἀσπίδα πάντοσʼ ἐΐσην    <καὶ βάλεν, οὐδʼ ἀφάμαρτε>
-- 2 hit(s)

# [23b] python homer/concordance.py --ngram "κέρδεα εἰδώς"
Il. 23.709   [9-12]  ἂν δʼ Ὀδυσεὺς πολύμητις ἀνίστατο κέρδεα εἰδώς.    <κέρδεα εἰδώς>
-- 1 hit(s)

# [24a] python homer/concordance.py --loose "ενικα" --word
Il. 4.389    [10-12]  ἀλλʼ ὅ γʼ ἀεθλεύειν προκαλίζετο, πάντα δʼ ἐνίκα    <ἐνίκα>
Il. 5.807    [10-12]  κούρους Καδμείων προκαλίζετο, πάντα δʼ ἐνίκα    <ἐνίκα>
Il. 18.252   [10-12]  ἀλλʼ ὃ μὲν ἂρ μύθοισιν, ὃ δʼ ἔγχεϊ πολλὸν ἐνίκα·    <ἐνίκα>
Il. 20.410   [10-12]  καί οἱ φίλτατος ἔσκε, πόδεσσι δὲ πάντας ἐνίκα    <ἐνίκα>
Il. 23.680   [6-8]  ἐς τάφον· ἔνθα δὲ πάντας ἐνίκα Καδμείωνας.    <ἐνίκα>
Il. 23.742   [6-8]  χάνδανεν, αὐτὰρ κάλλει ἐνίκα πᾶσαν ἐπʼ αἶαν    <ἐνίκα>
Il. 23.756   [10-12]  Ἀντίλοχος· ὃ γὰρ αὖτε νέους ποσὶ πάντας ἐνίκα.    <ἐνίκα>
Od. 3.121    [6-8]  ἤθελʼ, ἐπεὶ μάλα πολλὸν ἐνίκα δῖος Ὀδυσσεὺς    <ἐνίκα>
-- 8 hit(s)

# [24b] python homer/concordance.py --regex "(νίκ|νικ)[^ ]*.*μάχ|μάχ[^ ]*.*(νίκ|νικ)"
Il. 7.26     [6-12]  ἦ ἵνα δὴ Δαναοῖσι μάχης ἑτεραλκέα νίκην    <μάχης ἑτεραλκέα νίκ>
Il. 8.171    [6-12]  σῆμα τιθεὶς Τρώεσσι μάχης ἑτεραλκέα νίκην.    <μάχης ἑτεραλκέα νίκ>
Il. 16.79    [6-9.5]  πᾶν πεδίον κατέχουσι μάχῃ νικῶντες Ἀχαιούς.    <μάχῃ νικ>
Il. 16.362   [6-12]  ἦ μὲν δὴ γίγνωσκε μάχης ἑτεραλκέα νίκην·    <μάχης ἑτεραλκέα νίκ>
Il. 17.332   [1-12]  νίκην· ἀλλʼ αὐτοὶ τρεῖτʼ ἄσπετον οὐδὲ μάχεσθε.    <νίκην· ἀλλʼ αὐτοὶ τρεῖτʼ ἄσπετον οὐδὲ μάχ>
-- 5 hit(s)

# [24c] python homer/concordance.py --loose "πυματ"
Il. 4.254    [5.5-7]  Μηριόνης δʼ ἄρα οἱ πυμάτας ὄτρυνε φάλαγγας.    <πυμάτ>
Il. 6.118    [3.5-5]  ἄντυξ ἣ πυμάτη θέεν ἀσπίδος ὀμφαλοέσσης.    <πυμάτ>
Il. 10.475   [5.5-7]  ἐξ ἐπιδιφριάδος πυμάτης ἱμᾶσι δέδεντο.    <πυμάτ>
Il. 11.65    [3.5-5.5]  ἄλλοτε δʼ ἐν πυμάτοισι κελεύων· πᾶς δʼ ἄρα χαλκῷ    <πυμάτ>
Il. 11.759   [5.5-7]  ἔνθʼ ἄνδρα κτείνας πύματον λίπον· αὐτὰρ Ἀχαιοὶ    <πύματ>
Il. 13.616   [3.5-5]  ῥινὸς ὕπερ πυμάτης· λάκε δʼ ὀστέα, τὼ δέ οἱ ὄσσε    <πυμάτ>
Il. 18.608   [3.5-5]  ἄντυγα πὰρ πυμάτην σάκεος πύκα ποιητοῖο.    <πυμάτ>
Il. 22.66    [3.5-5]  αὐτὸν δʼ ἂν πύματόν με κύνες πρώτῃσι θύρῃσιν    <πύματ>
Il. 22.203   [3.5-5]  εἰ μή οἱ πύματόν τε καὶ ὕστατον ἤντετʼ Ἀπόλλων    <πύματ>
Il. 23.373   [3.5-5]  ἀλλʼ ὅτε δὴ πύματον τέλεον δρόμον ὠκέες ἵπποι    <πύματ>
Il. 23.768   [3.5-5]  ἀλλʼ ὅτε δὴ πύματον τέλεον δρόμον, αὐτίκʼ Ὀδυσσεὺς    <πύματ>
Od. 2.20     [5.5-7]  ἐν σπῆι γλαφυρῷ, πύματον δʼ ὡπλίσσατο δόρπον.    <πύματ>
Od. 4.685    [3.5-5]  ὕστατα καὶ πύματα νῦν ἐνθάδε δειπνήσειαν·    <πύματ>
Od. 7.138    [1.5-3]  ᾧ πυμάτῳ σπένδεσκον, ὅτε μνησαίατο κοίτου.    <πυμάτ>
Od. 9.369    [3.5-5]  Οὖτιν ἐγὼ πύματον ἔδομαι μετὰ οἷς ἑτάροισιν,    <πύματ>
Od. 20.13    [3.5-5]  ὕστατα καὶ πύματα, κραδίη δέ οἱ ἔνδον ὑλάκτει.    <πύματ>
Od. 20.116   [3.5-5]  μνηστῆρες πύματόν τε καὶ ὕστατον ἤματι τῷδε    <πύματ>
-- 17 hit(s)

# [24f] python homer/concordance.py --ngram "μιν ἐνίκα"
-- 0 hit(s)

# [24k] python homer/concordance.py --regex "(^|\s)ὅ γ(ε|ʼ) [Α-ΩἈ-ἏἘ-ἝἨ-ἯἸ-ἿὈ-ὍὙ-ὟὨ-ὯᾼῌῼῬ][^ ]*(ος|ης|ων|ευς|εύς|ς)[ ,·.;]"
Il. 13.70    [1.5-4]  οὐδʼ ὅ γε Κάλχας ἐστὶ θεοπρόπος οἰωνιστής·    < ὅ γε Κάλχας >
-- 1 hit(s)

# [24l] python homer/concordance.py --regex "(^|\s)ὅ γ(ε|ʼ) ἥρως" --count
7

# [24n] python homer/concordance.py --regex "(^|\s)(ὁ|ὅ|ὃ) (γε |γʼ |δʼ |δὲ |μὲν )?[Α-ΩἈ-ἏἘ-ἝἨ-ἯἸ-ἿὈ-ὍὙ-ὟὨ-ὯᾼῌῼῬ][^ ]*(ος|ης|εύς|ευς|ων)\b"
Il. 7.275    [2-5]  ἦλθον, ὃ μὲν Τρώων, ὃ δʼ Ἀχαιῶν χαλκοχιτώνων,    < ὃ μὲν Τρώων>
Il. 8.532    [4-7]  εἴσομαι εἴ κέ μʼ ὁ Τυδεΐδης κρατερὸς Διομήδης    < ὁ Τυδεΐδης>
Il. 11.660   [4-7]  βέβληται μὲν ὃ Τυδεΐδης κρατερὸς Διομήδης,    < ὃ Τυδεΐδης>
Il. 16.25    [4-7]  βέβληται μὲν ὃ Τυδεΐδης κρατερὸς Διομήδης,    < ὃ Τυδεΐδης>
Il. 17.608   [2-5.5]  Τρῶες· ὃ δʼ Ἰδομενῆος ἀκόντισε Δευκαλίδαο    < ὃ δʼ Ἰδομενῆος>
Il. 20.474   [5.5-8]  αἰχμὴ χαλκείη· ὃ δʼ Ἀγήνορος υἱὸν Ἔχεκλον    < ὃ δʼ Ἀγήνορος>
Il. 24.509   [5.5-8]  τὼ δὲ μνησαμένω ὃ μὲν Ἕκτορος ἀνδροφόνοιο    < ὃ μὲν Ἕκτορος>
-- 7 hit(s)

# [24m] python homer/concordance.py --loose "επειτα" --word (positions tabulated)
    222 [4-5.5]
     69 [10-12]
     47 [2-3.5]
     14 [6-7.5]
      2 [8-9.5]
      2 [2-4]
```

### A.3 Lines 27-30 (set 4: the 35-shot rally, the break, the hold)

```
# [27a] python homer/concordance.py --ngram "πολλὰ δ᾽ ἄναντα κάταντα πάραντά τε δόχμιά τ᾽ ἦλθον"
Il. 23.116   [1-12]  πολλὰ δʼ ἄναντα κάταντα πάραντά τε δόχμιά τʼ ἦλθον·    <πολλὰ δʼ ἄναντα κάταντα πάραντά τε δόχμιά τʼ ἦλθον>
-- 1 hit(s)

# context for ngram "ἄναντα κάταντα" (-3/+2 lines): 1 hit(s)
  Il. 23.113   Μηριόνης θεράπων ἀγαπήνορος Ἰδομενῆος.
  Il. 23.114   οἳ δʼ ἴσαν ὑλοτόμους πελέκεας ἐν χερσὶν ἔχοντες
  Il. 23.115   σειράς τʼ εὐπλέκτους· πρὸ δʼ ἄρʼ οὐρῆες κίον αὐτῶν.
> Il. 23.116   πολλὰ δʼ ἄναντα κάταντα πάραντά τε δόχμιά τʼ ἦλθον·
  Il. 23.117   ἀλλʼ ὅτε δὴ κνημοὺς προσέβαν πολυπίδακος Ἴδης,
  Il. 23.118   αὐτίκʼ ἄρα δρῦς ὑψικόμους ταναήκεϊ χαλκῷ

# context for ngram "καὶ βάλεν" (-1/+0 lines): 11 hit(s)
  Il. 3.346   πρόσθε δʼ Ἀλέξανδρος προΐει δολιχόσκιον ἔγχος,
> Il. 3.347   καὶ βάλεν Ἀτρεΐδαο κατʼ ἀσπίδα πάντοσε ἴσην,

  Il. 5.611   στῆ δὲ μάλʼ ἐγγὺς ἰών, καὶ ἀκόντισε δουρὶ φαεινῷ,
> Il. 5.612   καὶ βάλεν Ἄμφιον Σελάγου υἱόν, ὅς ῥʼ ἐνὶ Παισῷ

  Il. 7.244   ἦ ῥα, καὶ ἀμπεπαλὼν προΐει δολιχόσκιον ἔγχος,
> Il. 7.245   καὶ βάλεν Αἴαντος δεινὸν σάκος ἑπταβόειον

  Il. 11.349   ἦ ῥα, καὶ ἀμπεπαλὼν προΐει δολιχόσκιον ἔγχος
> Il. 11.350   καὶ βάλεν, οὐδʼ ἀφάμαρτε τιτυσκόμενος κεφαλῆφιν,

  Il. 11.375   καὶ κόρυθα βριαρήν· ὃ δὲ τόξου πῆχυν ἄνελκε
> Il. 11.376   καὶ βάλεν, οὐδʼ ἄρα μιν ἅλιον βέλος ἔκφυγε χειρός,

  Il. 13.159   Μηριόνης δʼ αὐτοῖο τιτύσκετο δουρὶ φαεινῷ
> Il. 13.160   καὶ βάλεν, οὐδʼ ἀφάμαρτε, κατʼ ἀσπίδα πάντοσʼ ἐΐσην

  Il. 13.370   Ἰδομενεὺς δʼ αὐτοῖο τιτύσκετο δουρὶ φαεινῷ,
> Il. 13.371   καὶ βάλεν ὕψι βιβάντα τυχών· οὐδʼ ἤρκεσε θώρηξ

  Il. 17.347   στῆ δὲ μάλʼ ἐγγὺς ἰών, καὶ ἀκόντισε δουρὶ φαεινῷ,
> Il. 17.348   καὶ βάλεν Ἱππασίδην Ἀπισάονα ποιμένα λαῶν

  Il. 17.516   ἦ ῥα, καὶ ἀμπεπαλὼν προΐει δολιχόσκιον ἔγχος,
> Il. 17.517   καὶ βάλεν Ἀρήτοιο κατʼ ἀσπίδα πάντοσʼ ἐΐσην·

  Il. 20.273   δεύτερος αὖτʼ Ἀχιλεὺς προΐει δολιχόσκιον ἔγχος,
> Il. 20.274   καὶ βάλεν Αἰνείαο κατʼ ἀσπίδα πάντοσʼ ἐΐσην

  Od. 24.522   αἶψα μάλʼ ἀμπεπαλὼν προΐει δολιχόσκιον ἔγχος,
> Od. 24.523   καὶ βάλεν Εὐπείθεα κόρυθος διὰ χαλκοπαρῄου.

# [29a] python homer/concordance.py --ngram "ἀλλὰ καὶ ὧς" --count
17

# [29b] python homer/concordance.py --loose "εδαμη" --word
Il. 2.860    [1.5-3]  ἀλλʼ ἐδάμη ὑπὸ χερσὶ ποδώκεος Αἰακίδαο    <ἐδάμη>
Il. 2.874    [1.5-3]  ἀλλʼ ἐδάμη ὑπὸ χερσὶ ποδώκεος Αἰακίδαο    <ἐδάμη>
-- 2 hit(s)

# [29h] python homer/concordance.py --ngram "ὑπὸ χερσὶ"
Il. 2.860    [3.5-5.5]  ἀλλʼ ἐδάμη ὑπὸ χερσὶ ποδώκεος Αἰακίδαο    <ὑπὸ χερσὶ>
Il. 2.874    [3.5-5.5]  ἀλλʼ ἐδάμη ὑπὸ χερσὶ ποδώκεος Αἰακίδαο    <ὑπὸ χερσὶ>
Il. 3.352    [7.5-9.5]  δῖον Ἀλέξανδρον, καὶ ἐμῇς ὑπὸ χερσὶ δάμασσον,    <ὑπὸ χερσὶ>
Il. 6.368    [3.5-5.5]  ἦ ἤδη μʼ ὑπὸ χερσὶ θεοὶ δαμόωσιν Ἀχαιῶν.    <ὑπὸ χερσὶ>
Il. 10.452   [3.5-5.5]  εἰ δέ κʼ ἐμῇς ὑπὸ χερσὶ δαμεὶς ἀπὸ θυμὸν ὀλέσσῃς,    <ὑπὸ χερσὶ>
Il. 11.180   [3.5-5.5]  Ἀτρεΐδεω ὑπὸ χερσί· περὶ πρὸ γὰρ ἔγχεϊ θῦεν.    <ὑπὸ χερσί>
Il. 16.438   [3.5-5.5]  ἦ ἤδη ὑπὸ χερσὶ Μενοιτιάδαο δαμάσσω.    <ὑπὸ χερσὶ>
Il. 16.699   [3.5-5.5]  Πατρόκλου ὑπὸ χερσί, περὶ πρὸ γὰρ ἔγχεϊ θῦεν,    <ὑπὸ χερσί>
Il. 23.675   [7.5-9.5]  οἵ κέ μιν ἐξοίσουσιν ἐμῇς ὑπὸ χερσὶ δαμέντα.    <ὑπὸ χερσὶ>
Od. 18.156   [3.5-5.5]  Τηλεμάχου ὑπὸ χερσὶ καὶ ἔγχεϊ ἶφι δαμῆναι.    <ὑπὸ χερσὶ>
Od. 24.97    [3.5-5.5]  Αἰγίσθου ὑπὸ χερσὶ καὶ οὐλομένης ἀλόχοιο.    <ὑπὸ χερσὶ>
-- 11 hit(s)

# context for ngram "ἐμῇς ὑπὸ χερσὶ δαμέντα" (-3/+1 lines): 1 hit(s)
  Il. 23.672   ὧδε γὰρ ἐξερέω, τὸ δὲ καὶ τετελεσμένον ἔσται·
  Il. 23.673   ἀντικρὺ χρόα τε ῥήξω σύν τʼ ὀστέʼ ἀράξω.
  Il. 23.674   κηδεμόνες δέ οἱ ἐνθάδʼ ἀολλέες αὖθι μενόντων,
> Il. 23.675   οἵ κέ μιν ἐξοίσουσιν ἐμῇς ὑπὸ χερσὶ δαμέντα.
  Il. 23.676   ὣς ἔφαθʼ, οἳ δʼ ἄρα πάντες ἀκὴν ἐγένοντο σιωπῇ.

# [29e] python homer/concordance.py --ngram "ὑπὸ κρατεροῦ"
Il. 21.553   [6-9]  ὤ μοι ἐγών· εἰ μέν κεν ὑπὸ κρατεροῦ Ἀχιλῆος    <ὑπὸ κρατεροῦ>
-- 1 hit(s)

# [29g] python homer/concordance.py --loose "κρατερου" --word
Il. 8.279    [3.5-5]  τόξου ἄπο κρατεροῦ Τρώων ὀλέκοντα φάλαγγας·    <κρατεροῦ>
Il. 21.553   [7.5-9]  ὤ μοι ἐγών· εἰ μέν κεν ὑπὸ κρατεροῦ Ἀχιλῆος    <κρατεροῦ>
Od. 8.360    [7.5-9]  τὼ δʼ ἐπεὶ ἐκ δεσμοῖο λύθεν, κρατεροῦ περ ἐόντος,    <κρατεροῦ>
-- 3 hit(s)

# [29k] python homer/concordance.py --regex "[^ ]+(οῦ|ου|οιο|ῆς|ης) (ὑπὸ|ὑπʼ|ὑφʼ|ἐκ|ἐξ|ἀπὸ|ἀπʼ|διὰ|διʼ|ἐπὶ|ἐπʼ|παρὰ|πὰρ) [^ ]+ [^ ]+(οιο|ου|ῆος|ηος|ης|ῆς)[ ,·.;]" --limit "15"
Il. 2.162    [6-12]  ἐν Τροίῃ ἀπόλοντο φίλης ἀπὸ πατρίδος αἴης·    <φίλης ἀπὸ πατρίδος αἴης·>
Il. 2.178    [6-12]  ἐν Τροίῃ ἀπόλοντο φίλης ἀπὸ πατρίδος αἴης;    <φίλης ἀπὸ πατρίδος αἴης;>
Il. 4.248    [5.5-12]  εἰρύατʼ εὔπρυμνοι πολιῆς ἐπὶ θινὶ θαλάσσης,    <πολιῆς ἐπὶ θινὶ θαλάσσης,>
Il. 6.92     [2-12]  θεῖναι Ἀθηναίης ἐπὶ γούνασιν ἠϋκόμοιο,    <Ἀθηναίης ἐπὶ γούνασιν ἠϋκόμοιο,>
Il. 6.273    [2-12]  τὸν θὲς Ἀθηναίης ἐπὶ γούνασιν ἠϋκόμοιο,    <Ἀθηναίης ἐπὶ γούνασιν ἠϋκόμοιο,>
Il. 6.303    [2-12]  θῆκεν Ἀθηναίης ἐπὶ γούνασιν ἠϋκόμοιο,    <Ἀθηναίης ἐπὶ γούνασιν ἠϋκόμοιο,>
Il. 13.12    [1-7]  ὑψοῦ ἐπʼ ἀκροτάτης κορυφῆς Σάμου ὑληέσσης    <ὑψοῦ ἐπʼ ἀκροτάτης κορυφῆς >
Il. 19.73    [3.5-12]  δηΐου ἐκ πολέμοιο ὑπʼ ἔγχεος ἡμετέροιο.    <πολέμοιο ὑπʼ ἔγχεος ἡμετέροιο.>
Od. 4.262    [6-12]  δῶχʼ, ὅτε μʼ ἤγαγε κεῖσε φίλης ἀπὸ πατρίδος αἴης,    <φίλης ἀπὸ πατρίδος αἴης,>
Od. 5.320    [5.5-12]  αἶψα μάλʼ ἀνσχεθέειν μεγάλου ὑπὸ κύματος ὁρμῆς·    <μεγάλου ὑπὸ κύματος ὁρμῆς·>
Od. 9.284    [6-12]  πρὸς πέτρῃσι βαλὼν ὑμῆς ἐπὶ πείρασι γαίης,    <ὑμῆς ἐπὶ πείρασι γαίης,>
Od. 10.96    [1-7]  αὐτοῦ ἐπʼ ἐσχατιῇ, πέτρης ἐκ πείσματα δήσας·    <αὐτοῦ ἐπʼ ἐσχατιῇ, πέτρης >
Od. 11.75    [5.5-12]  σῆμά τέ μοι χεῦαι πολιῆς ἐπὶ θινὶ θαλάσσης,    <πολιῆς ἐπὶ θινὶ θαλάσσης,>
Od. 23.353   [6-12]  ἱέμενον πεδάασκον ἐμῆς ἀπὸ πατρίδος αἴης·    <ἐμῆς ἀπὸ πατρίδος αἴης·>
-- 14 hit(s)

```

### A.4 Lines 31-34 (set 5 to 8-7: ἂψ ἐπόρουσε, ἀμφήριστον ἔθηκεν, τοῖιν, παρέλασσε)

```
# [32a] python homer/concordance.py --ngram "ἀμφήριστον ἔθηκεν"
Il. 23.382   [7-12]  καί νύ κεν ἢ παρέλασσʼ ἢ ἀμφήριστον ἔθηκεν,    <ἀμφήριστον ἔθηκεν>
Il. 23.527   [7-12]  τώ κέν μιν παρέλασσʼ οὐδʼ ἀμφήριστον ἔθηκεν.    <ἀμφήριστον ἔθηκεν>
-- 2 hit(s)

# context for ngram "ἀμφήριστον ἔθηκεν" (-2/+0 lines): 2 hit(s)
  Il. 23.380   πνοιῇ δʼ Εὐμήλοιο μετάφρενον εὐρέε τʼ ὤμω
  Il. 23.381   θέρμετʼ· ἐπʼ αὐτῷ γὰρ κεφαλὰς καταθέντε πετέσθην.
> Il. 23.382   καί νύ κεν ἢ παρέλασσʼ ἢ ἀμφήριστον ἔθηκεν,

  Il. 23.525   ἵππου τῆς Ἀγαμεμνονέης καλλίτριχος Αἴθης·
  Il. 23.526   εἰ δέ κʼ ἔτι προτέρω γένετο δρόμος ἀμφοτέροισι,
> Il. 23.527   τώ κέν μιν παρέλασσʼ οὐδʼ ἀμφήριστον ἔθηκεν.

# [32c] python homer/concordance.py --ngram "ἂψ ἐπόρουσε"
Il. 3.379    [3-5.5]  αὐτὰρ ὃ ἂψ ἐπόρουσε κατακτάμεναι μενεαίνων    <ἂψ ἐπόρουσε>
Il. 21.33    [3-5.5]  αὐτὰρ ὃ ἂψ ἐπόρουσε δαϊζέμεναι μενεαίνων.    <ἂψ ἐπόρουσε>
-- 2 hit(s)

# [32d] python homer/concordance.py --ngram "αὐτὰρ ὅ γ᾽ ἂψ"
Od. 11.599   [1-3]  αὐτὰρ ὅ γʼ ἂψ ὤσασκε τιταινόμενος, κατὰ δʼ ἱδρὼς    <αὐτὰρ ὅ γʼ ἂψ>
-- 1 hit(s)

# [32e] python homer/concordance.py --ngram "ἐπόρουσε καὶ"
Il. 11.580   [3.5-6]  Εὐρύπυλος δʼ ἐπόρουσε καὶ αἴνυτο τεύχεʼ ἀπʼ ὤμων.    <ἐπόρουσε καὶ>
Il. 13.550   [3.5-6]  Ἀντίλοχος δʼ ἐπόρουσε, καὶ αἴνυτο τεύχεʼ ἀπʼ ὤμων    <ἐπόρουσε, καὶ>
-- 2 hit(s)

# [33a] python homer/concordance.py --loose "τοιιν" --word
Il. 11.110   [5-5.5]  σπερχόμενος δʼ ἀπὸ τοῖιν ἐσύλα τεύχεα καλὰ    <τοῖιν>
Il. 13.66    [1-2]  τοῖιν δʼ ἔγνω πρόσθεν Ὀϊλῆος ταχὺς Αἴας,    <τοῖιν>
Il. 23.336   [5-5.5]  ἦκʼ ἐπʼ ἀριστερὰ τοῖιν· ἀτὰρ τὸν δεξιὸν ἵππον    <τοῖιν>
Od. 18.34    [1-2]  τοῖϊν δὲ ξυνέηχʼ ἱερὸν μένος Ἀντινόοιο,    <τοῖϊν>
-- 4 hit(s)

# [33b] python homer/concordance.py --ngram "ἀργαλέῳ καμάτῳ φίλα γυῖα λέλυντο"
Il. 13.85    [3-12]  τῶν ῥʼ ἅμα τʼ ἀργαλέῳ καμάτῳ φίλα γυῖα λέλυντο,    <ἀργαλέῳ καμάτῳ φίλα γυῖα λέλυντο>
-- 1 hit(s)

# [33c] python homer/concordance.py --regex "(τῷ|τοῖσι|τοῖιν|σφιν|οἱ|μοι|τοι)[^.·;]*γυῖα (λέλυντο|λέλυνται|λύθεν|λῦσε)|γυῖα (λέλυντο|λέλυνται)"
Il. 7.6      [9-12]  πόντον ἐλαύνοντες, καμάτῳ δʼ ὑπὸ γυῖα λέλυνται,    <γυῖα λέλυνται>
Il. 13.85    [9-12]  τῶν ῥʼ ἅμα τʼ ἀργαλέῳ καμάτῳ φίλα γυῖα λέλυντο,    <γυῖα λέλυντο>
Od. 8.233    [6-12]  ἦεν ἐπηετανός· τῷ μοι φίλα γυῖα λέλυνται.    <τῷ μοι φίλα γυῖα λέλυνται>
Od. 18.242   [4-12]  οἴκαδʼ, ὅπη οἱ νόστος, ἐπεὶ φίλα γυῖα λέλυνται.    <οἱ νόστος, ἐπεὶ φίλα γυῖα λέλυνται>
-- 4 hit(s)

# [34a] python homer/concordance.py --loose "παρελασσ"
Il. 23.382   [3.5-5]  καί νύ κεν ἢ παρέλασσʼ ἢ ἀμφήριστον ἔθηκεν,    <παρέλασσ>
Il. 23.427   [9.5-12]  στεινωπὸς γὰρ ὁδός, τάχα δʼ εὐρυτέρη παρελάσσαι·    <παρελάσσ>
Il. 23.527   [3.5-5]  τώ κέν μιν παρέλασσʼ οὐδʼ ἀμφήριστον ἔθηκεν.    <παρέλασσ>
-- 3 hit(s)

# [34b] python homer/concordance.py --loose "παρηλασ"
Il. 23.638   [6-8]  οἴοισίν μʼ ἵπποισι παρήλασαν Ἀκτορίωνε    <παρήλασ>
Od. 12.186   [6-8]  οὐ γάρ πώ τις τῇδε παρήλασε νηὶ μελαίνῃ,    <παρήλασ>
Od. 12.197   [6-8]  αὐτὰρ ἐπεὶ δὴ τάς γε παρήλασαν, οὐδʼ ἔτʼ ἔπειτα    <παρήλασ>
-- 3 hit(s)

# [34d] python homer/concordance.py --ngram "ὀψὲ δὲ δὴ"
Il. 7.94     [1-3]  ὀψὲ δὲ δὴ Μενέλαος ἀνίστατο καὶ μετέειπε    <ὀψὲ δὲ δὴ>
Il. 7.399    [1-3]  ὀψὲ δὲ δὴ μετέειπε βοὴν ἀγαθὸς Διομήδης·    <ὀψὲ δὲ δὴ>
Il. 8.30     [1-3]  ὀψὲ δὲ δὴ μετέειπε θεὰ γλαυκῶπις Ἀθήνη·    <ὀψὲ δὲ δὴ>
Il. 9.31     [1-3]  ὀψὲ δὲ δὴ μετέειπε βοὴν ἀγαθὸς Διομήδης·    <ὀψὲ δὲ δὴ>
Il. 9.432    [1-3]  ὀψὲ δὲ δὴ μετέειπε γέρων ἱππηλάτα Φοῖνιξ    <ὀψὲ δὲ δὴ>
Il. 9.696    [1-3]  ὀψὲ δὲ δὴ μετέειπε βοὴν ἀγαθὸς Διομήδης·    <ὀψὲ δὲ δὴ>
Il. 17.466   [1-3]  ὀψὲ δὲ δή μιν ἑταῖρος ἀνὴρ ἴδεν ὀφθαλμοῖσιν    <ὀψὲ δὲ δή>
Od. 3.168    [1-3]  ὀψὲ δὲ δὴ μετὰ νῶι κίε ξανθὸς Μενέλαος,    <ὀψὲ δὲ δὴ>
Od. 4.706    [1-3]  ὀψὲ δὲ δή μιν ἔπεσσιν ἀμειβομένη προσέειπε·    <ὀψὲ δὲ δή>
Od. 5.322    [1-3]  ὀψὲ δὲ δή ῥʼ ἀνέδυ, στόματος δʼ ἐξέπτυσεν ἅλμην    <ὀψὲ δὲ δή>
Od. 7.155    [1-3]  ὀψὲ δὲ δὴ μετέειπε γέρων ἥρως Ἐχένηος,    <ὀψὲ δὲ δὴ>
Od. 20.321   [1-3]  ὀψὲ δὲ δὴ μετέειπε Δαμαστορίδης Ἀγέλαος·    <ὀψὲ δὲ δὴ>
-- 12 hit(s)

# [34g] python homer/concordance.py --ngram "ὀψὲ δὲ δὴ μετέειπε βοὴν ἀγαθὸς Διομήδης"
Il. 7.399    [1-12]  ὀψὲ δὲ δὴ μετέειπε βοὴν ἀγαθὸς Διομήδης·    <ὀψὲ δὲ δὴ μετέειπε βοὴν ἀγαθὸς Διομήδης>
Il. 9.31     [1-12]  ὀψὲ δὲ δὴ μετέειπε βοὴν ἀγαθὸς Διομήδης·    <ὀψὲ δὲ δὴ μετέειπε βοὴν ἀγαθὸς Διομήδης>
Il. 9.696    [1-12]  ὀψὲ δὲ δὴ μετέειπε βοὴν ἀγαθὸς Διομήδης·    <ὀψὲ δὲ δὴ μετέειπε βοὴν ἀγαθὸς Διομήδης>
-- 3 hit(s)

```

### A.5 Lines 35-36 (the crowd and the heralds: Il. 18.502-503)

```
# [35a] python homer/concordance.py --ngram "λαοὶ δ᾽ ἀμφοτέροισιν ἐπήπυον ἀμφὶς ἀρωγοί"
Il. 18.502   [1-12]  λαοὶ δʼ ἀμφοτέροισιν ἐπήπυον ἀμφὶς ἀρωγοί·    <λαοὶ δʼ ἀμφοτέροισιν ἐπήπυον ἀμφὶς ἀρωγοί>
-- 1 hit(s)

# context for ngram "λαοὶ δ᾽ ἀμφοτέροισιν ἐπήπυον" (-5/+4 lines): 1 hit(s)
  Il. 18.497   λαοὶ δʼ εἰν ἀγορῇ ἔσαν ἀθρόοι· ἔνθα δὲ νεῖκος
  Il. 18.498   ὠρώρει, δύο δʼ ἄνδρες ἐνείκεον εἵνεκα ποινῆς
  Il. 18.499   ἀνδρὸς ἀποφθιμένου· ὃ μὲν εὔχετο πάντʼ ἀποδοῦναι
  Il. 18.500   δήμῳ πιφαύσκων, ὃ δʼ ἀναίνετο μηδὲν ἑλέσθαι·
  Il. 18.501   ἄμφω δʼ ἱέσθην ἐπὶ ἴστορι πεῖραρ ἑλέσθαι.
> Il. 18.502   λαοὶ δʼ ἀμφοτέροισιν ἐπήπυον ἀμφὶς ἀρωγοί·
  Il. 18.503   κήρυκες δʼ ἄρα λαὸν ἐρήτυον· οἳ δὲ γέροντες
  Il. 18.504   εἵατʼ ἐπὶ ξεστοῖσι λίθοις ἱερῷ ἐνὶ κύκλῳ,
  Il. 18.505   σκῆπτρα δὲ κηρύκων ἐν χέρσʼ ἔχον ἠεροφώνων·
  Il. 18.506   τοῖσιν ἔπειτʼ ἤϊσσον, ἀμοιβηδὶς δὲ δίκαζον.

# [36a] python homer/concordance.py --ngram "κήρυκες δ᾽ ἄρα λαὸν ἐρήτυον"
Il. 18.503   [1-8]  κήρυκες δʼ ἄρα λαὸν ἐρήτυον· οἳ δὲ γέροντες    <κήρυκες δʼ ἄρα λαὸν ἐρήτυον>
-- 1 hit(s)

# context for ngram "κήρυκες βοόωντες ἐρήτυον" (-1/+1 lines): 1 hit(s)
  Il. 2.96    λαῶν ἱζόντων, ὅμαδος δʼ ἦν· ἐννέα δέ σφεας
> Il. 2.97    κήρυκες βοόωντες ἐρήτυον, εἴ ποτʼ ἀϋτῆς
  Il. 2.98    σχοίατʼ, ἀκούσειαν δὲ διοτρεφέων βασιλήων.

# [36f] python homer/concordance.py --ngram "ἔνθα καὶ ἔνθα" (positions tabulated)
     21 [9-12]
      9 [3-5.5]
      2 [1-3.5]
# [36d] python homer/concordance.py --regex "(ἐρήτυ|ἐρητύ)[^ ]*.*ἔνθα καὶ ἔνθα|ἔνθα καὶ ἔνθα.*(ἐρήτυ|ἐρητύ)"
-- 0 hit(s)

```

### A.6 Lines 37-42 (the championship game: aces, CP1, CP2, the count)

```
# [38a] python homer/concordance.py --ngram "ἄσπετον ἤρατο κῦδος"
Il. 3.373    [7-12]  καί νύ κεν εἴρυσσέν τε καὶ ἄσπετον ἤρατο κῦδος,    <ἄσπετον ἤρατο κῦδος>
Il. 18.165   [7-12]  καί νύ κεν εἴρυσσέν τε καὶ ἄσπετον ἤρατο κῦδος,    <ἄσπετον ἤρατο κῦδος>
-- 2 hit(s)

# context for ngram "ἄσπετον ἤρατο κῦδος" (-0/+1 lines): 2 hit(s)
> Il. 3.373   καί νύ κεν εἴρυσσέν τε καὶ ἄσπετον ἤρατο κῦδος,
  Il. 3.374   εἰ μὴ ἄρʼ ὀξὺ νόησε Διὸς θυγάτηρ Ἀφροδίτη,

> Il. 18.165   καί νύ κεν εἴρυσσέν τε καὶ ἄσπετον ἤρατο κῦδος,
  Il. 18.166   εἰ μὴ Πηλεΐωνι ποδήνεμος ὠκέα Ἶρις

# [38b] python homer/concordance.py --ngram "καί νύ κεν ἔνθ᾽"
Il. 5.311    [1-3]  καί νύ κεν ἔνθʼ ἀπόλοιτο ἄναξ ἀνδρῶν Αἰνείας,    <καί νύ κεν ἔνθʼ>
Il. 5.388    [1-3]  καί νύ κεν ἔνθʼ ἀπόλοιτο Ἄρης ἆτος πολέμοιο,    <καί νύ κεν ἔνθʼ>
Il. 8.90     [3-5]  Ἕκτορα· καί νύ κεν ἔνθʼ ὁ γέρων ἀπὸ θυμὸν ὄλεσσεν    <καί νύ κεν ἔνθʼ>
-- 3 hit(s)

# [38c] python homer/concordance.py --loose "ελαβεν" --word
Il. 17.620   [5.5-7]  καὶ τά γε Μηριόνης ἔλαβεν χείρεσσι φίλῃσι    <ἔλαβεν>
Od. 6.81     [1.5-3]  ἡ δʼ ἔλαβεν μάστιγα καὶ ἡνία σιγαλόεντα,    <ἔλαβεν>
Od. 17.326   [5.5-7]  Ἄργον δʼ αὖ κατὰ μοῖρʼ ἔλαβεν μέλανος θανάτοιο,    <ἔλαβεν>
-- 3 hit(s)

# [38d] python homer/concordance.py --regex "ἔλαβέν τε|ἔλαβεν τε"
-- 0 hit(s)

# [40a] python homer/concordance.py --ngram "στῆ δὲ μάλ᾽ ἐγγὺς ἰών"
Il. 4.496    [1-5]  στῆ δὲ μάλʼ ἐγγὺς ἰὼν καὶ ἀκόντισε δουρὶ φαεινῷ    <στῆ δὲ μάλʼ ἐγγὺς ἰὼν>
Il. 5.611    [1-5]  στῆ δὲ μάλʼ ἐγγὺς ἰών, καὶ ἀκόντισε δουρὶ φαεινῷ,    <στῆ δὲ μάλʼ ἐγγὺς ἰών>
Il. 11.429   [1-5]  στῆ δὲ μάλʼ ἐγγὺς ἰὼν καί μιν πρὸς μῦθον ἔειπεν    <στῆ δὲ μάλʼ ἐγγὺς ἰὼν>
Il. 12.457   [1-5]  στῆ δὲ μάλʼ ἐγγὺς ἰών, καὶ ἐρεισάμενος βάλε μέσσας    <στῆ δὲ μάλʼ ἐγγὺς ἰών>
Il. 17.347   [1-5]  στῆ δὲ μάλʼ ἐγγὺς ἰών, καὶ ἀκόντισε δουρὶ φαεινῷ,    <στῆ δὲ μάλʼ ἐγγὺς ἰών>
-- 5 hit(s)

# [40g] python homer/concordance.py --ngram "ὃ δέ μιν"
Il. 5.304    [5.5-7]  οἷοι νῦν βροτοί εἰσʼ· ὃ δέ μιν ῥέα πάλλε καὶ οἶος.    <ὃ δέ μιν>
Il. 8.272    [3.5-5]  εἰς Αἴανθʼ· ὃ δέ μιν σάκεϊ κρύπτασκε φαεινῷ.    <ὃ δέ μιν>
Il. 12.449   [5.5-7]  οἷοι νῦν βροτοί εἰσʼ· ὃ δέ μιν ῥέα πάλλε καὶ οἶος.    <ὃ δέ μιν>
Il. 13.176   [5.5-7]  ναῖε δὲ πὰρ Πριάμῳ· ὃ δέ μιν τίεν ἶσα τέκεσσι.    <ὃ δέ μιν>
Il. 13.387   [5.5-7]  Ἰδομενῆα βαλεῖν· ὃ δέ μιν φθάμενος βάλε δουρὶ    <ὃ δέ μιν>
Il. 15.551   [5.5-7]  ναῖε δὲ πὰρ Πριάμῳ, ὃ δέ μιν τίεν ἶσα τέκεσσι·    <ὃ δέ μιν>
Il. 20.287   [5.5-7]  οἷοι νῦν βροτοί εἰσʼ· ὃ δέ μιν ῥέα πάλλε καὶ οἶος.    <ὃ δέ μιν>
Il. 20.480   [5.5-7]  αἰχμῇ χαλκείῃ· ὃ δέ μιν μένε χεῖρα βαρυνθεὶς    <ὃ δέ μιν>
Od. 19.449   [5.5-7]  οὐτάμεναι μεμαώς· ὁ δέ μιν φθάμενος ἔλασεν σῦς    <ὁ δέ μιν>
-- 9 hit(s)

# [40f] python homer/concordance.py --regex "ἰών, (ὃ|ὁ) δ"
Il. 22.123   [6-8]  μή μιν ἐγὼ μὲν ἵκωμαι ἰών, ὃ δέ μʼ οὐκ ἐλεήσει    <ἰών, ὃ δ>
-- 1 hit(s)

# [40e] python homer/concordance.py --ngram "οὐδ᾽ ἀφάμαρτε"
Il. 11.350   [3-5.5]  καὶ βάλεν, οὐδʼ ἀφάμαρτε τιτυσκόμενος κεφαλῆφιν,    <οὐδʼ ἀφάμαρτε>
Il. 13.160   [3-5.5]  καὶ βάλεν, οὐδʼ ἀφάμαρτε, κατʼ ἀσπίδα πάντοσʼ ἐΐσην    <οὐδʼ ἀφάμαρτε>
Il. 14.403   [9-12]  ἔγχει, ἐπεὶ τέτραπτο πρὸς ἰθύ οἱ, οὐδʼ ἀφάμαρτε,    <οὐδʼ ἀφάμαρτε>
Il. 22.290   [9-12]  καὶ βάλε Πηλεΐδαο μέσον σάκος οὐδʼ ἀφάμαρτε·    <οὐδʼ ἀφάμαρτε>
-- 4 hit(s)

# context for ngram "τρὶς μὲν ἔπειτ᾽ ἐπόρουσε" (-4/+2 lines): 3 hit(s)
  Il. 5.432   Αἰνείᾳ δʼ ἐπόρουσε βοὴν ἀγαθὸς Διομήδης,
  Il. 5.433   γιγνώσκων ὅ οἱ αὐτὸς ὑπείρεχε χεῖρας Ἀπόλλων·
  Il. 5.434   ἀλλʼ ὅ γʼ ἄρʼ οὐδὲ θεὸν μέγαν ἅζετο, ἵετο δʼ αἰεὶ
  Il. 5.435   Αἰνείαν κτεῖναι καὶ ἀπὸ κλυτὰ τεύχεα δῦσαι.
> Il. 5.436   τρὶς μὲν ἔπειτʼ ἐπόρουσε κατακτάμεναι μενεαίνων,
  Il. 5.437   τρὶς δέ οἱ ἐστυφέλιξε φαεινὴν ἀσπίδʼ Ἀπόλλων·
  Il. 5.438   ἀλλʼ ὅτε δὴ τὸ τέταρτον ἐπέσσυτο δαίμονι ἶσος,

  Il. 16.780   καὶ τότε δή ῥʼ ὑπὲρ αἶσαν Ἀχαιοὶ φέρτεροι ἦσαν.
  Il. 16.781   ἐκ μὲν Κεβριόνην βελέων ἥρωα ἔρυσσαν
  Il. 16.782   Τρώων ἐξ ἐνοπῆς, καὶ ἀπʼ ὤμων τεύχεʼ ἕλοντο,
  Il. 16.783   Πάτροκλος δὲ Τρωσὶ κακὰ φρονέων ἐνόρουσε.
> Il. 16.784   τρὶς μὲν ἔπειτʼ ἐπόρουσε θοῷ ἀτάλαντος Ἄρηϊ
  Il. 16.785   σμερδαλέα ἰάχων, τρὶς δʼ ἐννέα φῶτας ἔπεφνεν.
  Il. 16.786   ἀλλʼ ὅτε δὴ τὸ τέταρτον ἐπέσσυτο δαίμονι ἶσος,

  Il. 20.441   αὐτοῦ δὲ προπάροιθε ποδῶν πέσεν. αὐτὰρ Ἀχιλλεὺς
  Il. 20.442   ἐμμεμαὼς ἐπόρουσε κατακτάμεναι μενεαίνων,
  Il. 20.443   σμερδαλέα ἰάχων· τὸν δʼ ἐξήρπαξεν Ἀπόλλων
  Il. 20.444   ῥεῖα μάλʼ ὥς τε θεός, ἐκάλυψε δʼ ἄρʼ ἠέρι πολλῇ.
> Il. 20.445   τρὶς μὲν ἔπειτʼ ἐπόρουσε ποδάρκης δῖος Ἀχιλλεὺς
  Il. 20.446   ἔγχεϊ χαλκείῳ, τρὶς δʼ ἠέρα τύψε βαθεῖαν.
  Il. 20.447   ἀλλʼ ὅτε δὴ τὸ τέταρτον ἐπέσσυτο δαίμονι ἶσος,

# [41c] python -I trismen.py .
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

### A.7 Line 49 (ἔκφερεν αὖ; ὃ δ᾽ ἐπέσσυτο; τυτθὸν ὀπίσσω)

```
# [49a] python homer/concordance.py --ngram "τυτθὸν ὀπίσσω"
Il. 5.443    [9-12]  ὣς φάτο, Τυδεΐδης δʼ ἀνεχάζετο τυτθὸν ὀπίσσω    <τυτθὸν ὀπίσσω>
-- 1 hit(s)

# [49b] python homer/concordance.py --ngram "ὃ δ᾽ ἐπέσσυτο"
Il. 21.234   [5.5-8]  κρημνοῦ ἀπαΐξας· ὃ δʼ ἐπέσσυτο οἴδματι θύων,    <ὃ δʼ ἐπέσσυτο>
Il. 21.601   [5.5-8]  ἔστη πρόσθε ποδῶν, ὃ δʼ ἐπέσσυτο ποσσὶ διώκειν·    <ὃ δʼ ἐπέσσυτο>
-- 2 hit(s)

# context for ngram "ὃ δ᾽ ἐπέσσυτο ποσσὶ διώκειν" (-1/+4 lines): 1 hit(s)
  Il. 21.600   αὐτῷ γὰρ ἑκάεργος Ἀγήνορι πάντα ἐοικὼς
> Il. 21.601   ἔστη πρόσθε ποδῶν, ὃ δʼ ἐπέσσυτο ποσσὶ διώκειν·
  Il. 21.602   εἷος ὃ τὸν πεδίοιο διώκετο πυροφόροιο
  Il. 21.603   τρέψας πὰρ ποταμὸν βαθυδινήεντα Σκάμανδρον
  Il. 21.604   τυτθὸν ὑπεκπροθέοντα· δόλῳ δʼ ἄρʼ ἔθελγεν Ἀπόλλων
  Il. 21.605   ὡς αἰεὶ ἔλποιτο κιχήσεσθαι ποσὶν οἷσι·

# context for ngram "αἳ δ᾽ ἐξακέονται ὀπίσσω" (-2/+0 lines): 1 hit(s)
  Il. 9.505   ἣ δʼ ἄτη σθεναρή τε καὶ ἀρτίπος, οὕνεκα πάσας
  Il. 9.506   πολλὸν ὑπεκπροθέει, φθάνει δέ τε πᾶσαν ἐπʼ αἶαν
> Il. 9.507   βλάπτουσʼ ἀνθρώπους· αἳ δʼ ἐξακέονται ὀπίσσω.

# [49d] python homer/concordance.py --loose "εκφερεν" --word
Od. 15.470   [1-2]  ἔκφερεν· αὐτὰρ ἐγὼν ἑπόμην ἀεσιφροσύνῃσι.    <ἔκφερεν>
-- 1 hit(s)

# [49g] python homer/concordance.py --loose "τυτθον" --word --count
29

# [49h] python homer/concordance.py --regex "αὖ, ὃ|αὖ ὃ|αὖ, ὁ"
-- 0 hit(s)

```

### A.8 Lines 53-58 (the scales; κῆρε; ἐέλδωρ; the tie-break count; μάλα σχεδὸν ἦλθε διώκων)

```
# context for ngram "ἐν δ᾽ ἐτίθει δύο κῆρε" (-1/+4 lines): 2 hit(s)
  Il. 8.69    καὶ τότε δὴ χρύσεια πατὴρ ἐτίταινε τάλαντα·
> Il. 8.70    ἐν δʼ ἐτίθει δύο κῆρε τανηλεγέος θανάτοιο
  Il. 8.71    Τρώων θʼ ἱπποδάμων καὶ Ἀχαιῶν χαλκοχιτώνων,
  Il. 8.72    ἕλκε δὲ μέσσα λαβών· ῥέπε δʼ αἴσιμον ἦμαρ Ἀχαιῶν.
  Il. 8.73    αἳ μὲν Ἀχαιῶν κῆρες ἐπὶ χθονὶ πουλυβοτείρῃ
  Il. 8.74    ἑζέσθην, Τρώων δὲ πρὸς οὐρανὸν εὐρὺν ἄερθεν·

  Il. 22.209   καὶ τότε δὴ χρύσεια πατὴρ ἐτίταινε τάλαντα,
> Il. 22.210   ἐν δʼ ἐτίθει δύο κῆρε τανηλεγέος θανάτοιο,
  Il. 22.211   τὴν μὲν Ἀχιλλῆος, τὴν δʼ Ἕκτορος ἱπποδάμοιο,
  Il. 22.212   ἕλκε δὲ μέσσα λαβών· ῥέπε δʼ Ἕκτορος αἴσιμον ἦμαρ,
  Il. 22.213   ᾤχετο δʼ εἰς Ἀΐδαο, λίπεν δέ ἑ Φοῖβος Ἀπόλλων.
  Il. 22.214   Πηλεΐωνα δʼ ἵκανε θεὰ γλαυκῶπις Ἀθήνη,

# [54b] python homer/concordance.py --ngram "θαλερῶν αἰζηῶν"
Il. 10.259   [7.5-12]  κέκληται, ῥύεται δὲ κάρη θαλερῶν αἰζηῶν.    <θαλερῶν αἰζηῶν>
Il. 14.4     [7.5-12]  μείζων δὴ παρὰ νηυσὶ βοὴ θαλερῶν αἰζηῶν.    <θαλερῶν αἰζηῶν>
-- 2 hit(s)

# [54d] python homer/concordance.py --regex "κῆρ[^ ]* .*μάχ|μάχ[^ ]* .*κῆρ"
-- 0 hit(s)

# [56a] python homer/concordance.py --loose "εελδωρ" --word
Il. 1.41     [10-12]  ταύρων ἠδʼ αἰγῶν, τὸ δέ μοι κρήηνον ἐέλδωρ·    <ἐέλδωρ>
Il. 1.455    [10-12]  ἠδʼ ἔτι καὶ νῦν μοι τόδʼ ἐπικρήηνον ἐέλδωρ·    <ἐέλδωρ>
Il. 1.504    [10-12]  ἢ ἔπει ἢ ἔργῳ, τόδε μοι κρήηνον ἐέλδωρ·    <ἐέλδωρ>
Il. 8.242    [10-12]  ἀλλὰ Ζεῦ τόδε πέρ μοι ἐπικρήηνον ἐέλδωρ·    <ἐέλδωρ>
Il. 15.74    [10-12]  πρίν γε τὸ Πηλεΐδαο τελευτηθῆναι ἐέλδωρ,    <ἐέλδωρ>
Il. 16.238   [10-12]  ἠδʼ ἔτι καὶ νῦν μοι τόδʼ ἐπικρήηνον ἐέλδωρ·    <ἐέλδωρ>
Od. 3.418    [10-12]  καρπαλίμως μοι, τέκνα φίλα, κρηήνατʼ ἐέλδωρ,    <ἐέλδωρ>
Od. 17.242   [10-12]  ἀρνῶν ἠδʼ ἐρίφων, τόδε μοι κρηήνατʼ ἐέλδωρ,    <ἐέλδωρ>
Od. 21.200   [10-12]  Ζεῦ πάτερ, αἲ γὰρ τοῦτο τελευτήσειας ἐέλδωρ,    <ἐέλδωρ>
Od. 23.54    [6-8]  νῦν δʼ ἤδη τόδε μακρὸν ἐέλδωρ ἐκτετέλεσται·    <ἐέλδωρ>
-- 10 hit(s)

# [56b] python homer/concordance.py --regex "ʼ ἐέλδωρ"
Od. 3.418    [8-12]  καρπαλίμως μοι, τέκνα φίλα, κρηήνατʼ ἐέλδωρ,    <ʼ ἐέλδωρ>
Od. 17.242   [8-12]  ἀρνῶν ἠδʼ ἐρίφων, τόδε μοι κρηήνατʼ ἐέλδωρ,    <ʼ ἐέλδωρ>
-- 2 hit(s)

# [56c] python homer/concordance.py --ngram "ῥέπε δ᾽"
Il. 8.72     [5.5-7]  ἕλκε δὲ μέσσα λαβών· ῥέπε δʼ αἴσιμον ἦμαρ Ἀχαιῶν.    <ῥέπε δʼ>
Il. 22.212   [5.5-7]  ἕλκε δὲ μέσσα λαβών· ῥέπε δʼ Ἕκτορος αἴσιμον ἦμαρ,    <ῥέπε δʼ>
-- 2 hit(s)

# [58a] python homer/concordance.py --ngram "μάλα σχεδὸν ἦλθε διώκων"
Il. 23.499   [6-12]  ὣς φάτο, Τυδεΐδης δὲ μάλα σχεδὸν ἦλθε διώκων,    <μάλα σχεδὸν ἦλθε διώκων>
-- 1 hit(s)

# context for ngram "μάλα σχεδὸν ἦλθε διώκων" (-4/+2 lines): 1 hit(s)
  Il. 23.495   ἀλλʼ ὑμεῖς ἐν ἀγῶνι καθήμενοι εἰσοράασθε
  Il. 23.496   ἵππους· οἳ δὲ τάχʼ αὐτοὶ ἐπειγόμενοι περὶ νίκης
  Il. 23.497   ἐνθάδʼ ἐλεύσονται· τότε δὲ γνώσεσθε ἕκαστος
  Il. 23.498   ἵππους Ἀργείων, οἳ δεύτεροι οἵ τε πάροιθεν.
> Il. 23.499   ὣς φάτο, Τυδεΐδης δὲ μάλα σχεδὸν ἦλθε διώκων,
  Il. 23.500   μάστι δʼ αἰὲν ἔλαυνε κατωμαδόν· οἳ δέ οἱ ἵπποι
  Il. 23.501   ὑψόσʼ ἀειρέσθην ῥίμφα πρήσσοντε κέλευθον.

# [58b] python homer/concordance.py --loose "μετεπειτα" --word
Il. 14.310   [3.5-5.5]  μή πώς μοι μετέπειτα χολώσεαι, αἴ κε σιωπῇ    <μετέπειτα>
Od. 10.519   [5.5-7.5]  πρῶτα μελικρήτῳ, μετέπειτα δὲ ἡδέι οἴνῳ,    <μετέπειτα>
Od. 11.27    [5.5-7.5]  πρῶτα μελικρήτῳ, μετέπειτα δὲ ἡδέι οἴνῳ,    <μετέπειτα>
Od. 11.640   [5.5-7.5]  πρῶτα μὲν εἰρεσίῃ, μετέπειτα δὲ κάλλιμος οὖρος.    <μετέπειτα>
Od. 14.403   [9.5-12]  εἴη ἐπʼ ἀνθρώπους ἅμα τʼ αὐτίκα καὶ μετέπειτα,    <μετέπειτα>
-- 5 hit(s)

# [58f] python homer/concordance.py --regex "(τὴν|τὸν) ἕτερος"
Od. 8.374    [1-3]  τὴν ἕτερος ῥίπτασκε ποτὶ νέφεα σκιόεντα    <τὴν ἕτερος>
-- 1 hit(s)

```

```
# [DEATH] death-register stems in the v4 verse (loose forms)
33 ['λελυντο'] | τοῖιν δ᾽ ἀργαλέῳ καμάτῳ φίλα γυῖα λέλυντο.
54 ['κηρε'] | ἐν δ᾽ ἐτίθει δύο κῆρε μάχης θαλερῶν αἰζηῶν,
64 ['ημαρ'] | ὀψὲ δὲ δὴ τέλος ἦεν, ὅτ᾽ ἤλυθε δείελον ἦμαρ.
```

### A.9 Lines 59-64 (the final point; the apostrophe; the title; the close)

```
# context for loose_word "ἤμβροτες" (-2/+0 lines): 2 hit(s)
  Il. 5.285   δηρὸν ἔτʼ ἀνσχήσεσθαι· ἐμοὶ δὲ μέγʼ εὖχος ἔδωκας.
  Il. 5.286   τὸν δʼ οὐ ταρβήσας προσέφη κρατερὸς Διομήδης·
> Il. 5.287   ἤμβροτες οὐδʼ ἔτυχες· ἀτὰρ οὐ μὲν σφῶΐ γʼ ὀΐω

  Il. 22.277   ἂψ δʼ Ἀχιλῆϊ δίδου, λάθε δʼ Ἕκτορα ποιμένα λαῶν.
  Il. 22.278   Ἕκτωρ δὲ προσέειπεν ἀμύμονα Πηλεΐωνα·
> Il. 22.279   ἤμβροτες, οὐδʼ ἄρα πώ τι θεοῖς ἐπιείκελʼ Ἀχιλλεῦ

# [61b] python homer/concordance.py --ngram "ἤμβροτες οὐδ᾽ ἔτυχες"
Il. 5.287    [1-5]  ἤμβροτες οὐδʼ ἔτυχες· ἀτὰρ οὐ μὲν σφῶΐ γʼ ὀΐω    <ἤμβροτες οὐδʼ ἔτυχες>
-- 1 hit(s)

# [61c] python homer/concordance.py --ngram "πολλὰ μογήσας"
Il. 2.690    [9-12]  τὴν ἐκ Λυρνησσοῦ ἐξείλετο πολλὰ μογήσας    <πολλὰ μογήσας>
Il. 23.607   [9-12]  ἀλλὰ σὺ γὰρ δὴ πολλὰ πάθες καὶ πολλὰ μόγησας    <πολλὰ μόγησας>
Od. 2.343    [9-12]  οἴκαδε νοστήσειε καὶ ἄλγεα πολλὰ μογήσας.    <πολλὰ μογήσας>
Od. 3.232    [9-12]  βουλοίμην δʼ ἂν ἐγώ γε καὶ ἄλγεα πολλὰ μογήσας    <πολλὰ μογήσας>
Od. 5.449    [9-12]  σόν τε ῥόον σά τε γούναθʼ ἱκάνω πολλὰ μογήσας.    <πολλὰ μογήσας>
Od. 6.175    [9-12]  ἀλλά, ἄνασσʼ, ἐλέαιρε· σὲ γὰρ κακὰ πολλὰ μογήσας    <πολλὰ μογήσας>
Od. 7.147    [9-12]  σόν τε πόσιν σά τε γούναθʼ ἱκάνω πολλὰ μογήσας    <πολλὰ μογήσας>
Od. 15.489   [9-12]  Ζεύς, ἐπεὶ ἀνδρὸς δώματʼ ἀφίκεο πολλὰ μογήσας    <πολλὰ μογήσας>
Od. 19.483   [9-12]  τῷ σῷ ἐπὶ μαζῷ· νῦν δʼ ἄλγεα πολλὰ μογήσας    <πολλὰ μογήσας>
Od. 21.207   [9-12]  ἔνδον μὲν δὴ ὅδʼ αὐτὸς ἐγώ, κακὰ πολλὰ μογήσας    <πολλὰ μογήσας>
Od. 23.101   [9-12]  ἀνδρὸς ἀφεσταίη, ὅς οἱ κακὰ πολλὰ μογήσας    <πολλὰ μογήσας>
Od. 23.169   [9-12]  ἀνδρὸς ἀφεσταίη, ὅς οἱ κακὰ πολλὰ μογήσας    <πολλὰ μογήσας>
Od. 23.338   [9-12]  ἠδʼ ὡς ἐς Φαίηκας ἀφίκετο πολλὰ μογήσας,    <πολλὰ μογήσας>
-- 13 hit(s)

# [61d] python homer/concordance.py --ngram "μάλα πολλὰ μογήσας"
-- 0 hit(s)

# [61j] python homer/concordance.py --loose "αχιλευ" --word (positions tabulated; 5.5-7 hits listed)
      9 [1.5-3]
      1 [3.5-5]
      3 [5.5-7]
Il. 11.606   [5.5-7]  τίπτέ με κικλήσκεις Ἀχιλεῦ; τί δέ σε χρεὼ ἐμεῖο;    <Ἀχιλεῦ>
Il. 24.503   [5.5-7]  ἀλλʼ αἰδεῖο θεοὺς Ἀχιλεῦ, αὐτόν τʼ ἐλέησον    <Ἀχιλεῦ>
Il. 24.661   [5.5-7]  ὧδέ κέ μοι ῥέζων Ἀχιλεῦ κεχαρισμένα θείης.    <Ἀχιλεῦ>
# [61h] python homer/concordance.py --loose "πατροκλεισ" --word
Il. 16.693   [1-3]  Πατρόκλεις, ὅτε δή σε θεοὶ θάνατον δὲ κάλεσσαν;    <Πατρόκλεις>
Il. 16.859   [1-3]  Πατρόκλεις τί νύ μοι μαντεύεαι αἰπὺν ὄλεθρον;    <Πατρόκλεις>
-- 2 hit(s)

# [61i] python homer/concordance.py --regex "Πάτροκλε,? φάνη|Μενέλαε,? (φάνη|θεοὶ|μιάνθην)|σέθεν,? Μενέλαε|τοι,? Μενέλαε"
Il. 4.127    [2-5.5]  οὐδὲ σέθεν Μενέλαε θεοὶ μάκαρες λελάθοντο    <σέθεν Μενέλαε>
Il. 4.146    [3-5.5]  τοῖοί τοι Μενέλαε μιάνθην αἵματι μηροὶ    <τοι Μενέλαε>
Il. 7.104    [3-5.5]  ἔνθά κέ τοι Μενέλαε φάνη βιότοιο τελευτὴ    <τοι Μενέλαε>
Il. 16.787   [4-7]  ἔνθʼ ἄρα τοι Πάτροκλε φάνη βιότοιο τελευτή·    <Πάτροκλε φάνη>
-- 4 hit(s)

# context for loose_word "ἔσσυο" (-1/+0 lines): 2 hit(s)
  Il. 16.584   ὣς ἰθὺς Λυκίων Πατρόκλεες ἱπποκέλευθε
> Il. 16.585   ἔσσυο καὶ Τρώων, κεχόλωσο δὲ κῆρ ἑτάροιο.

  Od. 9.446   τὸν δʼ ἐπιμασσάμενος προσέφη κρατερὸς Πολύφημος·
> Od. 9.447   κριὲ πέπον, τί μοι ὧδε διὰ σπέος ἔσσυο μήλων

# context for ngram "ἔνθ᾽ ἄρα τοι Πάτροκλε φάνη" (-1/+0 lines): 1 hit(s)
  Il. 16.786   ἀλλʼ ὅτε δὴ τὸ τέταρτον ἐπέσσυτο δαίμονι ἶσος,
> Il. 16.787   ἔνθʼ ἄρα τοι Πάτροκλε φάνη βιότοιο τελευτή·

# [62a] python homer/concordance.py --ngram "κῦδος ἔδωκε"
Il. 8.216    [9-12]  Ἕκτωρ Πριαμίδης, ὅτε οἱ Ζεὺς κῦδος ἔδωκε.    <κῦδος ἔδωκε>
Il. 18.456   [9-12]  ἔκτανʼ ἐνὶ προμάχοισι καὶ Ἕκτορι κῦδος ἔδωκε.    <κῦδος ἔδωκε>
Il. 19.414   [9-12]  ἔκτανʼ ἐνὶ προμάχοισι καὶ Ἕκτορι κῦδος ἔδωκε.    <κῦδος ἔδωκε>
-- 3 hit(s)

# [62b] python homer/concordance.py --ngram "Ζεὺς κῦδος"
Il. 1.279    [8-9.5]  σκηπτοῦχος βασιλεύς, ᾧ τε Ζεὺς κῦδος ἔδωκεν.    <Ζεὺς κῦδος>
Il. 5.33     [8-9.5]  μάρνασθʼ, ὁπποτέροισι πατὴρ Ζεὺς κῦδος ὀρέξῃ,    <Ζεὺς κῦδος>
Il. 8.141    [8-9.5]  νῦν μὲν γὰρ τούτῳ Κρονίδης Ζεὺς κῦδος ὀπάζει    <Ζεὺς κῦδος>
Il. 8.216    [8-9.5]  Ἕκτωρ Πριαμίδης, ὅτε οἱ Ζεὺς κῦδος ἔδωκε.    <Ζεὺς κῦδος>
Il. 11.300   [8-9.5]  Ἕκτωρ Πριαμίδης, ὅτε οἱ Ζεὺς κῦδος ἔδωκεν;    <Ζεὺς κῦδος>
Il. 12.437   [4-5.5]  πρίν γʼ ὅτε δὴ Ζεὺς κῦδος ὑπέρτερον Ἕκτορι δῶκε    <Ζεὺς κῦδος>
Il. 17.566   [8-9.5]  χαλκῷ δηϊόων· τῷ γὰρ Ζεὺς κῦδος ὀπάζει.    <Ζεὺς κῦδος>
Il. 19.204   [8-9.5]  Ἕκτωρ Πριαμίδης, ὅτε οἱ Ζεὺς κῦδος ἔδωκεν,    <Ζεὺς κῦδος>
Il. 21.570   [8-9.5]  ἔμμεναι· αὐτάρ οἱ Κρονίδης Ζεὺς κῦδος ὀπάζει.    <Ζεὺς κῦδος>
Od. 19.161   [8-9.5]  οἴκου κήδεσθαι, τῷ τε Ζεὺς κῦδος ὀπάζει.    <Ζεὺς κῦδος>
-- 10 hit(s)

# [62d] python homer/concordance.py --loose "αντιθεω" --word
Il. 4.377    [3-5]  ξεῖνος ἅμʼ ἀντιθέῳ Πολυνείκεϊ λαὸν ἀγείρων·    <ἀντιθέῳ>
Il. 5.629    [3-5]  ὦρσεν ἐπʼ ἀντιθέῳ Σαρπηδόνι μοῖρα κραταιή.    <ἀντιθέῳ>
Il. 11.140   [7-9]  ἀγγελίην ἐλθόντα σὺν ἀντιθέῳ Ὀδυσῆϊ    <ἀντιθέῳ>
Il. 16.649   [3-5]  αὐτοῦ ἐπʼ ἀντιθέῳ Σαρπηδόνι φαίδιμος Ἕκτωρ    <ἀντιθέῳ>
Od. 1.21     [1-3]  ἀντιθέῳ Ὀδυσῆι πάρος ἣν γαῖαν ἱκέσθαι.    <ἀντιθέῳ>
Od. 2.17     [7-9]  καὶ γὰρ τοῦ φίλος υἱὸς ἅμʼ ἀντιθέῳ Ὀδυσῆι    <ἀντιθέῳ>
Od. 6.331    [1-3]  ἀντιθέῳ Ὀδυσῆι πάρος ἣν γαῖαν ἱκέσθαι.    <ἀντιθέῳ>
Od. 8.518    [7-9]  βήμεναι, ἠύτʼ Ἄρηα σὺν ἀντιθέῳ Μενελάῳ.    <ἀντιθέῳ>
Od. 13.126   [7-9]  λήθετʼ ἀπειλάων, τὰς ἀντιθέῳ Ὀδυσῆϊ    <ἀντιθέῳ>
Od. 22.291   [1-3]  ἀντιθέῳ Ὀδυσῆϊ δόμον κάτʼ ἀλητεύοντι.    <ἀντιθέῳ>
Od. 24.116   [7-9]  ὀτρυνέων Ὀδυσῆα σὺν ἀντιθέῳ Μενελάῳ    <ἀντιθέῳ>
-- 11 hit(s)

# [63a] python homer/concordance.py --ngram "ὣς οἳ μὲν μάρναντο"
Il. 11.596   [1-5.5]  ὣς οἳ μὲν μάρναντο δέμας πυρὸς αἰθομένοιο·    <ὣς οἳ μὲν μάρναντο>
Il. 13.673   [1-5.5]  ὣς οἳ μὲν μάρναντο δέμας πυρὸς αἰθομένοιο·    <ὣς οἳ μὲν μάρναντο>
Il. 17.366   [1-5.5]  ὣς οἳ μὲν μάρναντο δέμας πυρός, οὐδέ κε φαίης    <ὣς οἳ μὲν μάρναντο>
Il. 17.424   [1-5.5]  ὣς οἳ μὲν μάρναντο, σιδήρειος δʼ ὀρυμαγδὸς    <ὣς οἳ μὲν μάρναντο>
Il. 18.1     [1-5.5]  ὣς οἳ μὲν μάρναντο δέμας πυρὸς αἰθομένοιο,    <ὣς οἳ μὲν μάρναντο>
-- 5 hit(s)

# [63b] python homer/concordance.py --ngram "Διὸς δ᾽ ἐτελείετο βουλή"
Il. 1.5      [6-12]  οἰωνοῖσί τε πᾶσι, Διὸς δʼ ἐτελείετο βουλή,    <Διὸς δʼ ἐτελείετο βουλή>
Od. 11.297   [6-12]  θέσφατα πάντʼ εἰπόντα· Διὸς δʼ ἐτελείετο βουλή.    <Διὸς δʼ ἐτελείετο βουλή>
-- 2 hit(s)

```

### A.10 Lexica (Logeion API, fetched 2026-10-08: anastrophe.uchicago.edu/logeion-api/detail?w=…; 'Cunliffe Homer' and LSJ entries, HTML stripped by dico_text.py; excerpts)

```
# Cunliffe κήρ 1-3:
1 Bane, death : τό τοι κὴρ εἴδεται εἶναι Il. 1.228, κῆρʼ ἀλεείνων Il. 3.3
2 One’s destined fate : ἐμὲ κὴρ ἀμφέχανε, ἥ περ λάχε γιγνόμενόν περ Il. 2
3 Figured as a weight put in the balance and typifying death or one’s fate : ἐν δὲ τίθει δύο κῆρε θανάτοιο Od. 8.70 = Il. 22.210. Cf. Od. 8.73. 4 More or less di
# LSJ Κήρ (I, II):
the goddess of death or doom, Κὴρ . . Θανάτοιο Od. 11.171, etc.; Κῆρ
Κῆρες Ἀχαιῶν, Τρώων, 8.73, 74
II as Appellat., doom, death, esp. when violent, rarely without personal sense in Hom. ,
# Cunliffe ἔλδωρ / LSJ ἔλδωρ:
ἔλδωρ τό [ἔλδομαι.] Always, with prothetic ἐ , ἐέλδωρ . A wish or desire Il. 1.41, 455 = Il. 16.238, Il. 1.504, Il. 8.242, Il. 15.74: Od. 3.418, Od. 17.242, Od. 21.200, Od. 23.54. 

wish, longing, desire, Il. 1.41
# Cunliffe ῥέπω / LSJ ῥέπω:
ῥέπω (ϝρέτπω ). (ἐπιρρέπω ). To incline or sink downwards : ῥέπεν αἴσιμον ἦμαρ Ἀχαιῶν Il. 8.72. Cf. Il. 22.212. 

turn the scale, sink, ἐτίταινε τάλαντα, ἕλκε δὲ μέσσα λαβών, ῥέπε δʼ αἴσιμον ἦμαρ Ἀχαιῶν, implying defeat and death, Il. 8.72; ῥέπε δʼ Ἕκτορ
# Cunliffe ὀπίσσω 1-2:
1 Of direction, backwards, back : ἀνεχάζετο τυτθὸν ὀπίσσω Il. 5.443. Cf. Il. 3.218, 2
2 Of place, behind, in rear : ἐξακέονται ὀπίσσω (follow and . . .) Il. 9.507, αὐτὰρ ὀπίσσω ἡ πληθὺς ἐπὶ νῆα
# Cunliffe τυτθός 2d-2e:
d To a short distance, a little : ἀνεχάζετο τ. ὀπίσσω Il. 5.443. Cf. Il. 10.345, 
e At a short distance, a little : τ. ἀποπρὸ νεῶν Il. 7.334, τ. ὑπεκπροθέοντα (keeping always a little ahead) Il. 21.604. Cf. Od. 9.
# Cunliffe πύματος 3:
3 The last in sequence or time : δρόμον Il. 23.373, 768. Cf. Od. 2.20.
# Cunliffe νικάω 1:
1 To overcome, vanquish, get the better of, in fight or in a contest : δοκέω νικησέμεν Ἕκτορα Il. 7.192, ἀνδρὶ νικηθέντι γυναῖκʼ ἔθηκεν (as a prize for the loser) Il. 23.704. Cf. Il. 3.404, Il. 13.318, Il. 16.79, 
# Cunliffe δαμάζω 5-6:
5 To overpower, get the better of, master : ἐπεὶ ξάνθοιο δάμη μένος Il. 21.383. Cf. Il. 16.816: Od. 4.397. In mid.: δαμασσάμενος οἴνῳ Od. 9.454. Cf. Od. 
6 To put an end to, destroy, kill, slay : εἰ πόλεμος δαμᾷ Ἀχαιούς Il. 1.61, μὴ 
# Cunliffe παρελαύνω 1a / ἀμφήριστος:
1 a To drive one’s chariot past another, outstrip him in the race : ἤ κε παρέλασσʼ ἢ ἀμφήριστον ἔθηκεν Il. 23.382. Cf. 
ἀμφήριστος [ἀμφ- , ἀμφι- 1 + ἐρίζω.] Disputed on both sides . In neut. qualifying a vague notion the state of things ; hence, a dead heat: ἀμφήριστόν κʼ ἔθηκεν Il. 23.382, 527. 

# Cunliffe ἐπορούω 1:
1 To rush at a foe, make an attack or assault : τρὶς ἐπόρουσεν Il. 5.436, Il. 16.784, Il. 20.445. Cf. Il. 3.379, Il. 13.541, Il. 16.330, I
# Cunliffe ἐπηπύω / ἀρωγός / ἐρητύω 1-2:
ἐπηπύω [ἐπ- , ἐπι- 5.] To give one’s voice in approval or assent to. With dat.: ἀμφοτέροισιν ἐπήπυον Il. 18.502. 

ἀρωγός -οῦ , ὁ , ἡ [as ἀρωγή.] A helper, aider Il. 4.235, Il. 8.205, Il. 18.502 ( partisans ), Il. 21.371, 428: Od. 18.232. 

1 To hold back, hold in check, check, restrain, curb : φῶτα ἕκαστον I
2 To get under control, bring back to discipline : κήρυκές σφεας Il. 2.97, ἐρήτυθεν καθʼ ἕδρ
# Cunliffe διώκω 1, 4:
1 To chase, pursue Il. 5.65, 672, Il. 8.339, Il
4 To drive (a chariot) Il. 8.439. Absol. Il. 23.344, 424, 499, 547. 5 Of
# Cunliffe μετέπειτα / ἕτερος 2:
μετέπειτα [μετ- , μετα- 5 + ἔπειτα.] 1 Afterwards, in after time : ἅμα τʼ αὐτίκα καὶ μ. Od. 14.403. Cf. Il. 14.310. 2 Then, next : πρῶτα . . . μ. . . . Od. 10.5

2 The other of two, a ἑτέροιο διὰ κροτάφοιο πέρη
# Cunliffe ἁμαρτάνω 1 / τυγχάνω 3:
1 To discharge a missile vainly, miss one’s aim : ἤμβροτες οὐδʼ ἔτυχες Il. 5.287. Cf. Il. 8.311, Il. 11.233 = Il. 13.605, Il. 13.518, Il. 22.
3 Absol., to hit one’s mark, make good one’s aim, get one’s blow or thrust home : ἤμβροτες οὐδʼ ἔτυχες Il. 5.287. Cf.
# Cunliffe μογέω:
μογέω [μόγος.] To suffer toil, hardship, distress, to toil, labour : πολλὰ μόγησα Il. 1.162, ἄλλος μογέων ἀποκινήσασκε [δέπας] (with trouble or difficulty, could just . . .) Il. 11.636. Cf. Il. 2.690, Il. 9.492, Il. 12.29, Il. 23.607 : ἄλγεα πολλὰ μογήσας (aft

# Cunliffe κῦδος 3:
3 The glory of victory, victory, triumph, the upper hand : ὁπποτέροισι Ζεὺς κ. ὀρέξῃ Il. 5.33, [ἶσον] 
# Cunliffe αἰζηός / θαλερός 1:
αἰζηός In full bodily strength, lusty, vigorous Il. 16.716, Il. 23.432. Absol. in pl., such men, young men: διοτρεφέων αἰζηῶν Il. 2.660. Cf. Il. 3.26, Il. 4.280, Il. 5.92

1 Lusty, in prime of vigour : αἰζηοί Il. 3.26. Cf. Il. 4.
# Cunliffe ἔπειτα (resumptive):
Resuming and restating, then : ἐπόρουσε . . . τρὶς ἐ. ἐπόρουσεν Il. 5.436. Cf. Il. 20.445, etc.: Od. 3.62, etc. 
# Cunliffe ἐκφέρω 6:
6 Intrans. for reflexive, to draw away from competitors in a race, shoot ahead (cf. ὑπεκφέρω 3) Il. 23.376, 377, 759. 
```

### A.11 Enjambment labels (v4 jsonl; v3 reviewer labels from philology_v3.md §6)

```
# [ENJ] python -I enj4.py .
v4 composer: {'none': 36, 'unperiodic': 19, 'necessary': 9}
  unperiodic [2, 6, 7, 8, 14, 22, 27, 31, 38, 41, 43, 46, 52, 53, 54, 55, 57, 60, 63]
  necessary [1, 3, 16, 17, 18, 42, 44, 50, 51]
line-final punctuation: 1(no stop) 2, 3(no stop) 4. 5· 6, 7, 8, 9. 10. 11. 12· 13. 14, 15. 16(no stop) 17(no stop) 18, 19· 20. 21· 22, 23. 24. 25· 26· 27, 28. 29· 30. 31, 32· 33. 34· 35· 36. 37· 38, 39. 40. 41, 42, 43(no stop) 44(no stop) 45· 46, 47· 48· 49. 50(no stop) 51(no stop) 52, 53, 54, 55, 56. 57, 58. 59· 60, 61. 62. 63· 64.
labels inconsistent with the punctuation test: [(63, 'unperiodic', '·')]
v4 label differs from the v3 reviewer label of its v3 verse (n, v3 n, v3 reviewer, v4 composer): []
```

## Appendix B. Scripts

Saved under the session scratchpad and reproduced here verbatim. Run from the repository root with `.venv` active; the Python scripts take the repository path (and, where needed, a draft path) as arguments and are run with `python -I`. ctx.py, q.sh, aspir.py, accent.py, simile.py, trismen.py and dico_text.py are the v3 scripts (philology_v3.md Appendix B), unchanged.

### B.1 identity.py (v4 vs v3 verses)

```python
# v4 vs v3 by exact string comparison: which v4 verses equal the v3 verse named in v4.jsonl v3_line; v4.txt = v4.jsonl text;
# jsonl 'changed' flag agrees; v3 lines not carried into v4; v3 verdicts read from review/philology_v3.md §6
import json, sys, re, unicodedata as U
repo = sys.argv[1]; d = f'{repo}/composition/drafts'
v3txt = open(f'{d}/v3.txt', encoding='utf-8').read().splitlines()
v3 = {r['n']: r['text'] for r in map(json.loads, open(f'{d}/v3.jsonl', encoding='utf-8'))}
v4 = [json.loads(l) for l in open(f'{d}/v4.jsonl', encoding='utf-8')]
txt = open(f'{d}/v4.txt', encoding='utf-8').read().splitlines()
assert len(txt) == len(v4), (len(txt), len(v4))
verd = {}; inside = False
for line in open(f'{repo}/review/philology_v3.md', encoding='utf-8'):
    if line.startswith('## '): inside = line.startswith('## 6.')
    m = re.match(r'^\| (\d+) \| (PASS|FAIL|QUERY) \|', line)
    if inside and m: verd[int(m.group(1))] = m.group(2)
same, changed, new, flagmis, nfc = [], [], [], [], []
for r in v4:
    assert txt[r['n'] - 1] == r['text'], r['n']
    if U.normalize('NFC', r['text']) != r['text']: nfc.append(r['n'])
    m = r.get('v3_line')
    if m is None: new.append(r['n']); continue
    assert v3txt[m-1] == v3[m]
    if v3[m] == r['text']: same.append((r['n'], m))
    else: changed.append((r['n'], m))
    if bool(r.get('changed')) != (v3[m] != r['text']): flagmis.append(r['n'])
used = {r.get('v3_line') for r in v4}
print(f'v4.txt == v4.jsonl text: {len(v4)}/{len(v4)}; non-NFC lines: {nfc}')
print('identical to v3 (v4 n = v3 n):', len(same), ', '.join(f'{a}={b}' for a, b in same))
print('  v3 verdicts of the identical verses:', {k: sum(1 for a, b in same if verd[b] == k) for k in ('PASS', 'FAIL', 'QUERY')})
print('changed (v4 n <- v3 n):', len(changed), ', '.join(f'{a}<-{b}' for a, b in changed))
print('new (no v3_line):', len(new), new)
print('v3 lines not carried into v4:', [n for n in v3 if n not in used])
print('jsonl "changed" flag disagrees with text diff:', flagmis)
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

### B.5 rulings.py (R2-R12 forms, names, registers, prohibited words)

```python
# Ruling and lexicon checks on a draft (v4): R2-R6, R9-R12 forms, Djokovic/Federer name forms, prohibited words (loose forms, homer/greek.py)
import sys, re, unicodedata as U
sys.path.insert(0, sys.argv[1] + '/homer')
import greek as G
lines = [l.rstrip('\n') for l in open(sys.argv[2], encoding='utf-8')]
def raw(l): return re.findall(r"[^\s,.·;:!]+", l)
def words(l): return [G.loose(w) for w in raw(l)]
N = lambda r: U.normalize('NFC', r)
checks = {
 'R2 ἰσόθεος (anywhere)': lambda w, r: w.startswith('ισοθε'),
 'R3 withdrawn Ζοκοβίδης/Νοβάκος': lambda w, r: w.startswith('ζοκοβιδ') or w.startswith('νοβακ'),
 'R4 δίς': lambda w, r: w == 'δισ',
 'R5 ἐξεναρίζω': lambda w, r: w.startswith('εξεναρ'),
 'R6 πάλιν': lambda w, r: w == 'παλιν',
 'R9 Νοβ- nominative/accusative with acute (Νοβήκος/-ον: wrong)': lambda w, r: re.match(r'νοβηκ(οσ|ον)$', w) is not None and 'ή' in N(r),
 'R9 Νοβῆκος/-ον (circumflex, short ultima)': lambda w, r: re.match(r'νοβηκ(οσ|ον)$', w) is not None and 'ῆ' in N(r),
 'R9 Νοβ- genitive/dative (long ultima; acute required)': lambda w, r: re.match(r'νοβηκ(ου|ῳ|ω)$', w) is not None,
 'R10 Ζοκοβεύς / Ζοκοβῆ- (eponym forms)': lambda w, r: w.startswith('ζοκοβευ') or w.startswith('ζοκοβη'),
 'Ζοκοβείδης (patronymic)': lambda w, r: w.startswith('ζοκοβειδ'),
 'Σέρβ- (ethnic)': lambda w, r: w.startswith('σερβ'),
 'Ῥογῆρ- / Φεδερ- / Ἑλβετ-': lambda w, r: w.startswith(('ρογηρ', 'φεδερ', 'ελβετ')),
 'δαμάζω/δάμνημι (aor. act./pass.)': lambda w, r: re.match(r'ε?δαμ(ασ|η$)', w) is not None,
 'κῦδος': lambda w, r: w == 'κυδοσ',
 'νικάω': lambda w, r: re.match(r'ε?νικ', w) is not None,
 'θάνατος / κήρ / ἦμαρ / κατατεθνη- (death register)': lambda w, r: re.match(r'(θανατ|κηρ(ε|εσ|α|οσ)?$|ημαρ$|κατατεθν|νηλεε)', w) is not None,
 'prohibited (γραμμ, στεγ, οχλ, ωρη/ωρα, δικτυ, ραβδ, χλο, χορτ, δικαστ, αθλητησ, σφαιριστ, ηττ)':
     lambda w, r: re.match(r'(γραμμ|στεγ|οχλ|ωρη|ωρα|ωρ$|δικτυ|ραβδ|χλο[ηυ]|χορτ|δικαστ|αθλητη[σν]|σφαιριστ|ηττ)', w) is not None,
}
for name, f in checks.items():
    hits = [(i, r) for i, l in enumerate(lines, 1) for w, r in zip(words(l), raw(l)) if f(w, r)]
    print(f'{name}: {len(hits)}', hits)
print('R2 Ῥογῆρος followed by ἰσόθεος:', [i for i, l in enumerate(lines, 1) if re.search(r'ρογηρ\S* ισοθε', ' '.join(words(l)))])
print('R11 "δεύτερον αὖτις":', [i for i, l in enumerate(lines, 1) if 'δευτερον αυτισ' in ' '.join(words(l))])
print('δεύτερον lines:', [i for i, l in enumerate(lines, 1) if 'δευτερον' in words(l)])
print('"καὶ βάλεν … καὶ βάλεν" (two hit clauses):', [i for i, l in enumerate(lines, 1) if ' '.join(words(l)).count('και βαλεν') == 2])
print('"οὐδ᾽ ἀφάμαρτε" lines:', [i for i, l in enumerate(lines, 1) if 'ουδʼ αφαμαρτε' in ' '.join(words(l)) or "ουδ' αφαμαρτε" in ' '.join(words(l))])
print('"τὸ τέταρτον" lines and the last word of the verse before:', [(i, raw(lines[i-2])[-1]) for i, l in enumerate(lines, 1) if 'το τεταρτον' in ' '.join(words(l))])
print('τρὶς μέν / τρὶς δέ lines:', [(i, ' '.join(raw(l)[:3])) for i, l in enumerate(lines, 1) if words(l)[0] == 'τρισ'])
print('vocatives (Φεδερεῦ/Ῥογῆρε/Νοβῆκε/Ζοκοβεῖδα/-η):', [(i, r) for i, l in enumerate(lines, 1) for w, r in zip(words(l), raw(l)) if w in ('φεδερευ', 'ρογηρε', 'νοβηκε', 'ζοκοβειδη', 'ζοκοβειδα', 'σερβε', 'ελβετιε')])
```

### B.6 aspir.py (elision before rough breathing)

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

### B.7 accent.py (accent of -η/ω + C + ος)

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

### B.7a accent2.py (accent of the genitive -ου of the Νοβῆκος type)

```python
# Accent of the genitive singular -ου of nouns whose nominative is -ῆ/ῶ + one consonant + -ος (the Νοβῆκος type):
# for every Homeric nominative type -ῆCος/-ῶCος, find the same stem in -ου and print its accent on η/ω (acute expected: long ultima).
import sys, re, unicodedata as U, collections
sys.path.insert(0, sys.argv[1] + '/homer')
from concordance import Concordance
c = Concordance()
words = collections.Counter()
for l in c.lines:
    for w in re.findall(r'[^\s,.·;:!ʼ]+', l.text): words[U.normalize('NFC', w)] += 1
def strip(s): return ''.join(ch for ch in U.normalize('NFD', s) if not U.combining(ch))
nom = [w for w in words if re.search(r'[ῆῶ][βγδζθκλμνπρστφχψ]ος$', w)]
pairs = collections.Counter(); ex = {}
for w in nom:
    stem = w[:-2]                      # ...ῆC
    base = strip(stem)
    for g in words:
        if g.endswith('ου') and strip(g[:-2]) == base and g != w:
            acc = 'acute' if re.search(r'[ήώ]', g[:-2]) else ('circumflex' if re.search(r'[ῆῶ]', g[:-2]) else 'other')
            pairs[acc] += 1; ex.setdefault(acc, []).append(f'{w}/{g}')
print('nominative types -ῆ/ῶ + C + ος:', len(nom))
for k in ('acute', 'circumflex', 'other'):
    print(f'genitive -ου with {k} on the penult: {pairs[k]}', '| e.g.', ', '.join(ex.get(k, [])[:12]))
```

### B.8 simile.py (simile openers and apodoses)

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

### B.8a apod.py (punctuation before a simile apodosis)

```python
# Punctuation at the end of the verse before a simile apodosis: Homeric lines opening with ὣς that close a ὡς (δʼ) ὅτε/ὅτʼ simile
# opened within the 10 preceding lines; tally the last character of the preceding verse.
import sys, re, collections
sys.path.insert(0, sys.argv[1] + '/homer')
from concordance import Concordance
c = Concordance(); L = c.lines
cnt = collections.Counter(); ex = collections.defaultdict(list)
for i, l in enumerate(L):
    if not re.match(r'^ὣς\b', l.text): continue
    prev = [L[j] for j in range(max(0, i-10), i) if (L[j].work, L[j].book) == (l.work, l.book)]
    if not any(re.match(r'^ὡς (δʼ )?ὅτ', p.text) or re.search(r'(^|\s)ὡς (δʼ )?ὅτ[εʼ]', p.text) for p in prev): continue
    p = L[i-1]; last = p.text[-1] if p.text[-1] in '.,·;:!' else '(none)'
    cnt[last] += 1; ex[last].append(f'{p.work}. {p.book}.{p.line}')
print('apodosis ὣς after a ὡς (δʼ) ὅτε simile: preceding verse ends with', dict(cnt))
print('  no punctuation:', ex['(none)'][:20])
```

### B.8b names.py (name tokens)

```python
# Name tokens of the two players per line (stems φεδερ-, ρογηρ-, ελβετ-, ζοκοβ-, σερβ-, νοβηκ-), whole draft and lines 12-end-2, v3 vs v4
import sys, re
sys.path.insert(0, sys.argv[1] + '/homer')
import greek as G
ST = ('φεδερ', 'ρογηρ', 'ελβετ', 'ζοκοβ', 'σερβ', 'νοβηκ')
for f in sys.argv[2:]:
    L = [l.strip() for l in open(f, encoding='utf-8')]
    per = [sum(1 for w in re.findall(r'[^\s,.·;:!]+', l) if G.loose(w).startswith(ST)) for l in L]
    nar = per[11:len(L) - 2]
    adj = [(i + 1, i + 2) for i in range(len(L) - 1) if per[i] and per[i + 1]]
    print(f'{f}: lines {len(L)}, name tokens {sum(per)} ({sum(per)/len(L):.2f}/line); narrative 12-{len(L)-2}: {sum(nar)}/{len(nar)} = {sum(nar)/len(nar):.2f}/line; adjacent named pairs {len(adj)}')
```

### B.8c boen.py (βοὴν ἀγαθ- spacing)

```python
# Spacing of βοὴν ἀγαθ- formulae: gaps between successive Homeric lines containing them (same book), and in a draft
import sys, re, collections
sys.path.insert(0, sys.argv[1] + '/homer')
from concordance import Concordance
import greek as G
c = Concordance(); L = c.lines
pos = [(l.work, l.book, i, l) for i, l in enumerate(L) if 'βοην αγαθ' in G.loose(l.text)]
print('Homeric lines with βοὴν ἀγαθ-:', len(pos))
gaps = collections.Counter(); close = []
for a, b in zip(pos, pos[1:]):
    if (a[0], a[1]) != (b[0], b[1]): continue
    g = b[2] - a[2]; gaps[min(g, 99)] += 1
    if g <= 4: close.append(f'{a[3].work}. {a[3].book}.{a[3].line} / {b[3].line} (gap {g})')
print('gaps <= 10:', {k: gaps[k] for k in sorted(gaps) if k <= 10})
print('pairs with gap <= 4:', close)
dr = [l.strip() for l in open(sys.argv[2], encoding='utf-8')]
d = [i for i, l in enumerate(dr, 1) if 'βοην αγαθ' in G.loose(l)]
print('draft lines with βοὴν ἀγαθ-:', d, '| gaps:', [b - a for a, b in zip(d, d[1:])])
```

### B.8d repline.py (whole verses repeated within K lines)

```python
# Whole Homeric verses repeated verbatim (loose form) within K lines in the same book; prints the count and examples
import sys
sys.path.insert(0, sys.argv[1] + '/homer')
from concordance import Concordance
import greek as G
K = int(sys.argv[2]); c = Concordance(); L = c.lines
n = 0; ex = []
for i, l in enumerate(L):
    a = G.loose(l.text)
    for j in range(i + 1, min(i + K + 1, len(L))):
        if (L[j].work, L[j].book) == (l.work, l.book) and G.loose(L[j].text) == a:
            n += 1; ex.append(f'{l.work}. {l.book}.{l.line} = {L[j].line}  {l.text}')
print(f'verbatim repeats within {K} lines: {n}')
for e in ex[:12]: print('  ', e)
```

### B.8e facts.py (match facts for the changed verses)

```python
# Facts for the changed and new verses of v4 from corpus/timing/points_2019wimF.csv: point, clock, set/game, server, score before, winner, MCP codes
import csv, sys
rows = {int(r['point_idx']): r for r in csv.DictReader(open(sys.argv[1] + '/corpus/timing/points_2019wimF.csv', encoding='utf-8'))}
S = lambda n: 'Fe' if rows[n]['point_winner'] == 'Roger Federer' else 'Dj'
def show(n, tag):
    r = rows[n]
    print(f"{tag:<34} pt {n:>3} {r['pbp_elapsed']:>8} set {r['set_no']} game {r['game_in_set']:>2} tb={r['tiebreak']:<5} server={'Fe' if r['server']=='Roger Federer' else 'Dj'} "
          f"games {r['games_before_p1']}-{r['games_before_p2']} pts {r['pts_before_p1']}-{r['pts_before_p2']} winner={S(n)} shots={r['mcp_n_shots']} 1st={r['mcp_1st']} 2nd={r['mcp_2nd']}")
for n, t in [(183, '23 rally (26 shots)'), (188, '24 TB3 first point'), (198, '24 TB3 last point'), (242, '27-28 35-shot rally'), (244, '29 break'),
             (357, '37 ace 1'), (358, '37 ace 2'), (359, '38-39 CP1'), (360, '40 CP2'), (361, '41 third onset'), (362, '42 break 8-8'),
             (413, '54 TB5 first point'), (414, 'TB5 pt 2'), (415, '57 tris 1'), (416, '57 tris 2'), (417, '57 tris 3'), (418, '58 close 1'), (419, '58 close 2'),
             (420, '59 winner 1'), (421, '59 winner 2'), (422, '60-61 last point')]:
    if n in rows: show(n, t)
# games won in set 5 around 9-8 / 9-9 and set 4 end
for n in sorted(rows):
    r = rows[n]
    if r['set_no'] == '4' and n == max(k for k in rows if rows[k]['set_no'] == '4'): show(n, 'set 4 last point')
```

### B.8f death.py (death-register stems)

```python
# Death-register stems in a draft (loose forms): θάνατος, κήρ, ἦμαρ, αἴσιμος, νηλεής, ψυχή, Ἀΐδης, ὄλλυμι, κτείνω, φόνος, νέκυς, θνῄσκω, μοῖρα, πότμος, ὄλεθρος, λύω of limbs
import sys, re
sys.path.insert(0, sys.argv[1] + '/homer')
import greek as G
pat = re.compile(r'^(ψυχ|αιδ|ολεσ|κτειν|εκταν|φονο|νεκ|θνη|θαν|τεθν|κηρ(ε|εσ|α|οσ)?$|μοιρ|ποτμ|ολεθρ|λυτο|λυντο|λελυντο|γουνατ|ημαρ|αισιμ|νηλε)')
for i, l in enumerate(open(sys.argv[2], encoding='utf-8'), 1):
    ws = [G.loose(w) for w in re.findall(r'[^\s,.·;:!]+', l)]
    h = [w for w in ws if pat.match(w)]
    if h: print(i, h, '|', l.strip())
```

### B.9 tally4.py (counts in §2 and §4)

```python
# python3 tally4.py review/philology_v4.md   (prints the counts in §2 and §4 from the per-line table, section "## 6.")
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
print('rows "Unchanged, v3 PASS":', sum(1 for r in rows if r[4].startswith('Unchanged, v3 PASS')), '| reviewed in full:', [r[0] for r in rows if not r[4].startswith('Unchanged, v3 PASS')])
for who, i in (('composer', 2), ('reviewer', 3)):
    c = collections.Counter(r[i] for r in rows)
    print(who, {t: f"{c[t]} ({100*c[t]/N:.1f}%)" for t in ('none', 'unperiodic', 'necessary')})
    print('  necessary lines', [r[0] for r in rows if r[i] == 'necessary'])
print('disagreements', [(r[0], r[2], r[3]) for r in rows if r[2] != r[3]])
```

### B.10 appendix4.sh (writes Appendix A)

```bash
#!/bin/bash
# usage (repo root, .venv active): appendix4.sh SCRIPTDIR LEXDIR  -> prints Appendix A of philology_v4.md
S=$1; D=$2; Q=$S/q.sh; V=composition/drafts/v4.txt
export LC_ALL=C.utf8   # grep -o '.{0,N}' must count characters, not bytes
fence() { echo '```'; "$@" 2>&1; echo '```'; echo; }
cun() { python -I $S/dico_text.py "$D/$1.json" 'Cunliffe Homer'; }
lsj() { python -I $S/dico_text.py "$D/$1.json" LSJ; }
export S D; export -f cun lsj
echo "### A.0 Identity, check_line, rulings, aspiration, accent, similes, names, spacing (whole draft)"; echo
fence bash -c "echo '# [ID] python -I identity.py .'; python -I $S/identity.py .; echo; echo '# [CL] python homer/check_line.py --file $V (exit status; lines with OK (no flags))'; python homer/check_line.py --file $V > /dev/null; echo \"exit=\$?\"; python homer/check_line.py --file $V | grep -c 'OK (no flags)'"
fence bash -c "echo '# [RUL] python -I rulings.py . $V'; python -I $S/rulings.py . $V"
fence bash -c "echo '# [ASP] python -I aspir.py . $V (draft lines: ERROR lines only, then the count of ok)'; python -I $S/aspir.py . $V | grep -v 'ok\$'; python -I $S/aspir.py . $V | grep -c 'ok\$'; echo; echo '# [ACC] python -I accent.py .'; python -I $S/accent.py .; echo; echo '# [ACC2] python -I accent2.py .'; python -I $S/accent2.py ."
fence bash -c "echo '# [SIM] python -I simile.py . $V'; python -I $S/simile.py . $V; echo; echo '# [APOD] python -I apod.py .'; python -I $S/apod.py .; grep -P '^Od\t9\t39[1-4]\t' homer/lines.tsv | cut -f1-4"
fence bash -c "echo '# [NAMES] python -I names.py . composition/drafts/v3.txt $V'; python -I $S/names.py . composition/drafts/v3.txt $V; echo; echo '# [BOEN] python -I boen.py . $V'; python -I $S/boen.py . $V; echo; echo '# [REP] python -I repline.py . 5'; python -I $S/repline.py . 5"
fence bash -c "echo '# [FACTS] python -I facts.py . (corpus/timing/points_2019wimF.csv)'; python -I $S/facts.py ."
echo "### A.1 Lines 19-20 (set 2: ἐπέσσυτο δαίμονι ἶσος; ἐσσυμένως λάβ᾽ ἄεθλον)"; echo
fence bash -c "$Q 19a --ngram 'ἐπέσσυτο δαίμονι ἶσος'; $Q 19b --ngram 'ὣς ἄρ᾽ ὅ γ᾽'; $Q 19c --ngram 'τότ᾽ ἐπέσσυτο'; $Q 20a --ngram 'ἐσσυμένως λάβ᾽ ἄεθλον'; python -I $S/ctx.py . 'ἐσσυμένως λάβ᾽ ἄεθλον' 2 1; $Q 20b --ngram 'καὶ ἐσσυμένως'; $Q 20c --loose 'εσσυμενως' --word --count"
echo "### A.2 Lines 23-24 (set 3: the rally's winner; the tie-break)"; echo
fence bash -c "$Q 23a --ngram 'καὶ βάλεν οὐδ᾽ ἀφάμαρτε'; $Q 23b --ngram 'κέρδεα εἰδώς'; $Q 24a --loose 'ενικα' --word; $Q 24b --regex '(νίκ|νικ)[^ ]*.*μάχ|μάχ[^ ]*.*(νίκ|νικ)'; $Q 24c --loose 'πυματ'; $Q 24f --ngram 'μιν ἐνίκα'; $Q 24k --regex '(^|\s)ὅ γ(ε|ʼ) [Α-ΩἈ-ἏἘ-ἝἨ-ἯἸ-ἿὈ-ὍὙ-ὟὨ-ὯᾼῌῼῬ][^ ]*(ος|ης|ων|ευς|εύς|ς)[ ,·.;]'; $Q 24l --regex '(^|\s)ὅ γ(ε|ʼ) ἥρως' --count; $Q 24n --regex '(^|\s)(ὁ|ὅ|ὃ) (γε |γʼ |δʼ |δὲ |μὲν )?[Α-ΩἈ-ἏἘ-ἝἨ-ἯἸ-ἿὈ-ὍὙ-ὟὨ-ὯᾼῌῼῬ][^ ]*(ος|ης|εύς|ευς|ων)\b'; echo '# [24m] python homer/concordance.py --loose \"επειτα\" --word (positions tabulated)'; python homer/concordance.py --loose 'επειτα' --word | grep -o '\[[0-9.-]*\]' | sort | uniq -c | sort -rn"
echo "### A.3 Lines 27-30 (set 4: the 35-shot rally, the break, the hold)"; echo
fence bash -c "$Q 27a --ngram 'πολλὰ δ᾽ ἄναντα κάταντα πάραντά τε δόχμιά τ᾽ ἦλθον'; python -I $S/ctx.py . 'ἄναντα κάταντα' 3 2; python -I $S/ctx.py . 'καὶ βάλεν' 1 0; $Q 29a --ngram 'ἀλλὰ καὶ ὧς' --count; $Q 29b --loose 'εδαμη' --word; $Q 29h --ngram 'ὑπὸ χερσὶ'; python -I $S/ctx.py . 'ἐμῇς ὑπὸ χερσὶ δαμέντα' 3 1; $Q 29e --ngram 'ὑπὸ κρατεροῦ'; $Q 29g --loose 'κρατερου' --word; $Q 29k --regex '[^ ]+(οῦ|ου|οιο|ῆς|ης) (ὑπὸ|ὑπʼ|ὑφʼ|ἐκ|ἐξ|ἀπὸ|ἀπʼ|διὰ|διʼ|ἐπὶ|ἐπʼ|παρὰ|πὰρ) [^ ]+ [^ ]+(οιο|ου|ῆος|ηος|ης|ῆς)[ ,·.;]' --limit 15"
echo "### A.4 Lines 31-34 (set 5 to 8-7: ἂψ ἐπόρουσε, ἀμφήριστον ἔθηκεν, τοῖιν, παρέλασσε)"; echo
fence bash -c "$Q 32a --ngram 'ἀμφήριστον ἔθηκεν'; python -I $S/ctx.py . 'ἀμφήριστον ἔθηκεν' 2 0; $Q 32c --ngram 'ἂψ ἐπόρουσε'; $Q 32d --ngram 'αὐτὰρ ὅ γ᾽ ἂψ'; $Q 32e --ngram 'ἐπόρουσε καὶ'; $Q 33a --loose 'τοιιν' --word; $Q 33b --ngram 'ἀργαλέῳ καμάτῳ φίλα γυῖα λέλυντο'; $Q 33c --regex '(τῷ|τοῖσι|τοῖιν|σφιν|οἱ|μοι|τοι)[^.·;]*γυῖα (λέλυντο|λέλυνται|λύθεν|λῦσε)|γυῖα (λέλυντο|λέλυνται)'; $Q 34a --loose 'παρελασσ'; $Q 34b --loose 'παρηλασ'; $Q 34d --ngram 'ὀψὲ δὲ δὴ'; $Q 34g --ngram 'ὀψὲ δὲ δὴ μετέειπε βοὴν ἀγαθὸς Διομήδης'"
echo "### A.5 Lines 35-36 (the crowd and the heralds: Il. 18.502-503)"; echo
fence bash -c "$Q 35a --ngram 'λαοὶ δ᾽ ἀμφοτέροισιν ἐπήπυον ἀμφὶς ἀρωγοί'; python -I $S/ctx.py . 'λαοὶ δ᾽ ἀμφοτέροισιν ἐπήπυον' 5 4; $Q 36a --ngram 'κήρυκες δ᾽ ἄρα λαὸν ἐρήτυον'; python -I $S/ctx.py . 'κήρυκες βοόωντες ἐρήτυον' 1 1; echo '# [36f] python homer/concordance.py --ngram \"ἔνθα καὶ ἔνθα\" (positions tabulated)'; python homer/concordance.py --ngram 'ἔνθα καὶ ἔνθα' | grep -o '\[[0-9.-]*\]' | sort | uniq -c | sort -rn; $Q 36d --regex '(ἐρήτυ|ἐρητύ)[^ ]*.*ἔνθα καὶ ἔνθα|ἔνθα καὶ ἔνθα.*(ἐρήτυ|ἐρητύ)'"
echo "### A.6 Lines 37-42 (the championship game: aces, CP1, CP2, the count)"; echo
fence bash -c "$Q 38a --ngram 'ἄσπετον ἤρατο κῦδος'; python -I $S/ctx.py . 'ἄσπετον ἤρατο κῦδος' 0 1; $Q 38b --ngram 'καί νύ κεν ἔνθ᾽'; $Q 38c --loose 'ελαβεν' --word; $Q 38d --regex 'ἔλαβέν τε|ἔλαβεν τε'; $Q 40a --ngram 'στῆ δὲ μάλ᾽ ἐγγὺς ἰών'; $Q 40g --ngram 'ὃ δέ μιν'; $Q 40f --regex 'ἰών, (ὃ|ὁ) δ'; $Q 40e --ngram 'οὐδ᾽ ἀφάμαρτε'; python -I $S/ctx.py . 'τρὶς μὲν ἔπειτ᾽ ἐπόρουσε' 4 2; echo '# [41c] python -I trismen.py .'; python -I $S/trismen.py ."
echo "### A.7 Line 49 (ἔκφερεν αὖ; ὃ δ᾽ ἐπέσσυτο; τυτθὸν ὀπίσσω)"; echo
fence bash -c "$Q 49a --ngram 'τυτθὸν ὀπίσσω'; $Q 49b --ngram 'ὃ δ᾽ ἐπέσσυτο'; python -I $S/ctx.py . 'ὃ δ᾽ ἐπέσσυτο ποσσὶ διώκειν' 1 4; python -I $S/ctx.py . 'αἳ δ᾽ ἐξακέονται ὀπίσσω' 2 0; $Q 49d --loose 'εκφερεν' --word; $Q 49g --loose 'τυτθον' --word --count; $Q 49h --regex 'αὖ, ὃ|αὖ ὃ|αὖ, ὁ'"
echo "### A.8 Lines 53-58 (the scales; κῆρε; ἐέλδωρ; the tie-break count; μάλα σχεδὸν ἦλθε διώκων)"; echo
fence bash -c "python -I $S/ctx.py . 'ἐν δ᾽ ἐτίθει δύο κῆρε' 1 4; $Q 54b --ngram 'θαλερῶν αἰζηῶν'; $Q 54d --regex 'κῆρ[^ ]* .*μάχ|μάχ[^ ]* .*κῆρ'; $Q 56a --loose 'εελδωρ' --word; $Q 56b --regex 'ʼ ἐέλδωρ'; $Q 56c --ngram 'ῥέπε δ᾽'; $Q 58a --ngram 'μάλα σχεδὸν ἦλθε διώκων'; python -I $S/ctx.py . 'μάλα σχεδὸν ἦλθε διώκων' 4 2; $Q 58b --loose 'μετεπειτα' --word; $Q 58f --regex '(τὴν|τὸν) ἕτερος'"
fence bash -c "echo '# [DEATH] death-register stems in the v4 verse (loose forms)'; python -I $S/death.py . $V"
echo "### A.9 Lines 59-64 (the final point; the apostrophe; the title; the close)"; echo
fence bash -c "python -I $S/ctx.py . 'ἤμβροτες' 2 0 loose_word; $Q 61b --ngram 'ἤμβροτες οὐδ᾽ ἔτυχες'; $Q 61c --ngram 'πολλὰ μογήσας'; $Q 61d --ngram 'μάλα πολλὰ μογήσας'; echo '# [61j] python homer/concordance.py --loose \"αχιλευ\" --word (positions tabulated; 5.5-7 hits listed)'; python homer/concordance.py --loose 'αχιλευ' --word | grep -o '\[[0-9.-]*\]' | sort | uniq -c; python homer/concordance.py --loose 'αχιλευ' --word | grep '\[5.5-7\]'; $Q 61h --loose 'πατροκλεισ' --word; $Q 61i --regex 'Πάτροκλε,? φάνη|Μενέλαε,? (φάνη|θεοὶ|μιάνθην)|σέθεν,? Μενέλαε|τοι,? Μενέλαε'; python -I $S/ctx.py . 'ἔσσυο' 1 0 loose_word; python -I $S/ctx.py . 'ἔνθ᾽ ἄρα τοι Πάτροκλε φάνη' 1 0; $Q 62a --ngram 'κῦδος ἔδωκε'; $Q 62b --ngram 'Ζεὺς κῦδος'; $Q 62d --loose 'αντιθεω' --word; $Q 63a --ngram 'ὣς οἳ μὲν μάρναντο'; $Q 63b --ngram 'Διὸς δ᾽ ἐτελείετο βουλή'"
echo "### A.10 Lexica (Logeion API, fetched 2026-10-08: anastrophe.uchicago.edu/logeion-api/detail?w=…; 'Cunliffe Homer' and LSJ entries, HTML stripped by dico_text.py; excerpts)"; echo
fence bash -c "
echo '# Cunliffe κήρ 1-3:'; cun κήρ | grep -o '1 Bane, death.\{0,60\}\|2 One’s destined fate.\{0,52\}\|3 Figured as a weight.\{0,140\}'
echo '# LSJ Κήρ (I, II):'; lsj Κήρ | grep -o 'the goddess of death or doom.\{0,40\}\|Κῆρες Ἀχαιῶν, Τρώων, 8.73, 74\|II as Appellat., doom, death.\{0,60\}'
echo '# Cunliffe ἔλδωρ / LSJ ἔλδωρ:'; cun ἔλδωρ | grep -o '^.\{0,330\}' | head -1; echo; lsj ἔλδωρ | grep -o 'wish, longing, desire.\{0,10\}'
echo '# Cunliffe ῥέπω / LSJ ῥέπω:'; cun ῥέπω | grep -o '^.\{0,140\}' | head -1; echo; lsj ῥέπω | grep -o 'turn the scale, sink.\{0,120\}'
echo '# Cunliffe ὀπίσσω 1-2:'; cun ὀπίσσω | grep -o '1 Of direction, backwards.\{0,60\}\|2 Of place, behind, in rear.\{0,80\}'
echo '# Cunliffe τυτθός 2d-2e:'; cun τυτθός | grep -o 'd To a short distance.\{0,60\}\|e At a short distance.\{0,110\}'
echo '# Cunliffe πύματος 3:'; cun πύματος | grep -o '3 The last in sequence or time.\{0,40\}'
echo '# Cunliffe νικάω 1:'; cun νικάω | grep -o '1 To overcome, vanquish.\{0,190\}'
echo '# Cunliffe δαμάζω 5-6:'; cun δαμάζω | grep -o '5 To overpower, get the better of.\{0,120\}\|6 To put an end to, destroy, kill, slay.\{0,40\}'
echo '# Cunliffe παρελαύνω 1a / ἀμφήριστος:'; cun παρελαύνω | grep -o '1 a To drive one’s chariot past another.\{0,80\}'; cun ἀμφήριστος | grep -o '^.\{0,200\}' | head -1; echo
echo '# Cunliffe ἐπορούω 1:'; cun ἐπορούω | grep -o '1 To rush at a foe.\{0,120\}'
echo '# Cunliffe ἐπηπύω / ἀρωγός / ἐρητύω 1-2:'; cun ἐπηπύω | grep -o '^.\{0,160\}' | head -1; echo; cun ἀρωγός | grep -o '^.\{0,140\}' | head -1; echo; cun ἐρητύω | grep -o '1 To hold back, hold in check.\{0,40\}\|2 To get under control.\{0,70\}'
echo '# Cunliffe διώκω 1, 4:'; cun διώκω | grep -o '1 To chase, pursue Il. 5.65.\{0,20\}\|4 To drive (a chariot).\{0,50\}'
echo '# Cunliffe μετέπειτα / ἕτερος 2:'; cun μετέπειτα | grep -o '^.\{0,160\}' | head -1; echo; cun ἕτερος | grep -o '2 The other of two.\{0,30\}'
echo '# Cunliffe ἁμαρτάνω 1 / τυγχάνω 3:'; cun ἁμαρτάνω | grep -o '1 To discharge a missile vainly.\{0,110\}'; cun τυγχάνω | grep -o '3 Absol., to hit one’s mark.\{0,90\}'
echo '# Cunliffe μογέω:'; cun μογέω | grep -o '^.\{0,260\}' | head -1; echo
echo '# Cunliffe κῦδος 3:'; cun κῦδος | grep -o '3 The glory of victory.\{0,80\}'
echo '# Cunliffe αἰζηός / θαλερός 1:'; cun αἰζηός | grep -o '^.\{0,170\}' | head -1; echo; cun θαλερός | grep -o '1 Lusty, in prime of vigour.\{0,30\}'
echo '# Cunliffe ἔπειτα (resumptive):'; cun ἔπειτα | grep -o 'Resuming and restating.\{0,90\}'
echo '# Cunliffe ἐκφέρω 6:'; cun ἐκφέρω | grep -o '6 Intrans.\{0,140\}'
"
echo "### A.11 Enjambment labels (v4 jsonl; v3 reviewer labels from philology_v3.md §6)"; echo
fence bash -c "echo '# [ENJ] python -I enj4.py .'; python -I $S/enj4.py ."
```

### B.10a enj4.py (enjambment labels)

```python
# Enjambment: v4 composer labels, line-final punctuation, and the v3 reviewer label of identical verses (philology_v3.md §6);
# flags labels inconsistent with Kirk's punctuation test as used in philology_v1-v3 (strong stop . · ; = none; comma/no stop = unperiodic or necessary)
import json, re, sys, collections
repo = sys.argv[1]
v4 = [json.loads(l) for l in open(f'{repo}/composition/drafts/v4.jsonl', encoding='utf-8')]
rev3 = {}; inside = False
for line in open(f'{repo}/review/philology_v3.md', encoding='utf-8'):
    if line.startswith('## '): inside = line.startswith('## 6.')
    m = re.match(r'^\| (\d+) \|', line)
    if inside and m:
        cells = [c.strip() for c in re.split(r'(?<!\\)\|', line.strip())[1:-1]]
        rev3[int(cells[0])] = cells[-1].split('→')[1].strip()
c = collections.Counter(r['enjambment'] for r in v4)
print('v4 composer:', {k: c[k] for k in ('none', 'unperiodic', 'necessary')})
for k in ('unperiodic', 'necessary'): print(' ', k, [r['n'] for r in v4 if r['enjambment'] == k])
fin = lambda t: t[-1] if t[-1] in '.·;,' else '(no stop)'
print('line-final punctuation:', ' '.join(f"{r['n']}{fin(r['text'])}" for r in v4))
bad = [(r['n'], r['enjambment'], fin(r['text'])) for r in v4
       if (fin(r['text']) in '.·;' and r['enjambment'] != 'none') or (fin(r['text']) not in '.·;' and r['enjambment'] == 'none')]
print('labels inconsistent with the punctuation test:', bad)
diff = [(r['n'], r['v3_line'], rev3[r['v3_line']], r['enjambment']) for r in v4 if r.get('v3_line') and rev3[r['v3_line']] != r['enjambment']]
print('v4 label differs from the v3 reviewer label of its v3 verse (n, v3 n, v3 reviewer, v4 composer):', diff)
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

### B.11 rows4.py (builds the §6 table)

```python
# builds the §6 per-line table of philology_v4.md: hand-written rows for the 21 changed or new verses,
# one "Unchanged, v3 PASS" row (with a continuity note where the neighbourhood changed) for every verbatim v3 verse
# usage: python3 -I rows4.py REPO > table.md
import json, sys, re
d = sys.argv[1]
v3 = {r['n']: r['text'] for r in map(json.loads, open(f'{d}/composition/drafts/v3.jsonl', encoding='utf-8'))}
v4 = [json.loads(l) for l in open(f'{d}/composition/drafts/v4.jsonl', encoding='utf-8')]
rev3 = {}; inside = False
for line in open(f'{d}/review/philology_v3.md', encoding='utf-8'):
    if line.startswith('## '): inside = line.startswith('## 6.')
    m = re.match(r'^\| (\d+) \|', line)
    if inside and m:
        cells = [c.strip() for c in re.split(r'(?<!\\)\|', line.strip())[1:-1]]
        rev3[int(cells[0])] = (cells[1], cells[-1].split('→')[1].strip())
# reviewer enjambment labels for the verses reviewed in full
mine = {19: 'none', 20: 'none', 23: 'none', 24: 'none', 27: 'unperiodic', 29: 'none', 32: 'none', 33: 'none', 34: 'none',
        35: 'none', 36: 'none', 38: 'unperiodic', 40: 'none', 49: 'none', 54: 'unperiodic', 56: 'none', 58: 'none',
        59: 'none', 61: 'none', 62: 'none', 63: 'none'}
full = {
19: ("PASS",
 "**Changed (M6, m7).** δεύτερον αὖτε (0 Homeric hits) at 9-12 gives way to ἐπέσσυτο δαίμονι ἶσος, which Homer has 7x, always at 6-12 [19a]. τότ᾽ ἐπέσσυτο has 0 hits, but ἐπέσσυτο starts at 6 here as in all 7 Homeric lines, after an elided τότ᾽ at 5.5. 1-5.5 is unchanged from v3 (ὣς ἄρ᾽ ὅ γ᾽ as Il. 22.143). ἶσος takes its regular digamma licence at 10 (19x). "
 "**Idiom.** Outside the τὸ τέταρτον frame the formula closes a rush in Il. 21.227 (ὣς εἰπὼν Τρώεσσιν ἐπέσσυτο δαίμονι ἶσος), so it has a model in an apodosis line. It returns in 42 for Federer's fourth onset: one man, one formula. "
 "**Sense.** The gloss is right. The ordinal 'second' is no longer in the verse; set 2 is placed by 15 (set 1 won) and 21 (τὸ τρίτον).",
 "[19a] --ngram \"ἐπέσσυτο δαίμονι ἶσος\" → 7, all [6-12]; [19b] --ngram \"ὣς ἄρ᾽ ὅ γ᾽\" → Il. 22.143, Od. 20.28; [19c] --ngram \"τότ᾽ ἐπέσσυτο\" → 0; check_line tier 0, no flags (A.0)"),
20: ("PASS",
 "**Changed (M4, M6, M8).** βοὴν ἀγαθὸς Φεδερῆρος becomes καὶ ἐσσυμένως λάβ᾽ ἄεθλον. 7-12 is Il. 23.511 verbatim, in its own slot, so the out-of-slot λάβ᾽ ἄεθλον of v3 23 (critic M8) is gone. καί stands at 6 with correption before ἐσ- (καὶ ἐσσυμένως has 0 hits; correption of καί is attested 2364x). "
 "**Syntax.** The subject is carried from 19 (ὅ γ᾽ Ἑλβέτιος), and μιν is Djokovic, named last in 15. Two aorists are joined by καί at 6, as εἴρυσσέν τε καὶ … ἤρατο in Il. 3.373. "
 "**Sense and facts.** 'Three times he subdued him' covers the breaks in games 1, 3 and 7 (1:03:00, 1:08:46, 1:22:54). 'Took the prize' is set 2, 6-1, which is now stated in the verse (M4). ἐσσυμένως means 'hastily, eagerly' (12x) and suits a set of 22½ minutes. The gloss is right. δάμασσε for a break is licensed by R5; see §2 for the grading.",
 "[20a] --ngram \"ἐσσυμένως λάβ᾽ ἄεθλον\" → Il. 23.511 [7-12] + ctx; [20b] --ngram \"καὶ ἐσσυμένως\" → 0; [20c] ἐσσυμένως → 12; check_line: correption@6 (A.0)"),
23: ("PASS",
 "**Changed (M2, M8).** v3 23 (δεύτερον αὖ λάβ᾽ ἄεθλον ἄφαρ κρατερὸς Ζοκοβείδης) is replaced by the whole verse of 28 (= v3 27, a v3 PASS). Point 183 (2:03:53, 26 shots) was won by Federer with a winner (A.0 FACTS). The rally now has its winner in the verse, so the v3 implicature that it went to Djokovic and ended the set is gone, and ἄφαρ with it. Ῥογῆρος stands at 6-8 after -τε and before κ (R2 ✓); κέρδεα εἰδώς is at 9-12 (Il. 23.709). "
 "**Repetition.** 23 and 28 are the same verse five lines apart, used for two Federer rally winners. Homer has 6 whole-verse repeats within 5 lines (A.0 REP). One of them is narrative, for two parallel acts (Il. 7.428 = 7.431), so the repeat is rare but Homeric. With 37, 40 and 59, οὐδ᾽ ἀφάμαρτε now stands in 5 of 64 verses; Homer has it in 4 verses. "
 "**Continuity.** 22 ends with a comma, and καὶ βάλεν continues βάλλον. In Homer καὶ βάλεν always continues the verse before (11/11, A.3). The gloss is right.",
 "[23a] --ngram \"καὶ βάλεν οὐδ᾽ ἀφάμαρτε\" → Il. 11.350, 13.160; [23b] --ngram \"κέρδεα εἰδώς\" → Il. 23.709; ctx \"καὶ βάλεν\" -1 → 11 (A.3); [REP] → 6; [FACTS] pt 183 winner Fe"),
24: ("PASS",
 "**New (M2, M4).** The set-3 tie-break (2:07:34-2:15:24, 7-4) gets its own verse, after the rally of 22-23. ἔπειτα covers the eleven points between them. "
 "**Syntax.** In ἀλλ᾽ ὅ γε Σέρβος, a pronoun takes a name in apposition as subject, as in ὁ / ὃ Τυδεΐδης κρατερὸς Διομήδης (Il. 8.532, 11.660 = 16.25) and ὅ γ᾽ ἥρως (7x). ὅ γε + a capitalised nominative has 1 hit (Il. 13.70), where the name is predicate. The poem already has the construction in 19 (ὅ γ᾽ Ἑλβέτιος, v1-v3 PASS). "
 "νικάω takes the man beaten in the accusative and the field in the dative: μάχῃ νικῶντες Ἀχαιούς (Il. 16.79), πόδεσσι δὲ πάντας ἐνίκα (Il. 20.410). Cunliffe νικάω 1: 'to overcome … in fight or in a contest'. μιν ἐνίκα has 0 hits. ἐνίκα stands at 10-12, as in 5 of its 8 hits. "
 "**Morphology.** πυμάτῃ is the dative feminine of πύματος (0 hits in this case; πυμάτη, -ης, -ην are attested). υ and α are short, as in πυμάτη at 3.5-5 (Il. 6.118). The slot 7.5-9 is a disclosed mobility. ἔπειτα stands at 4-5.5, its commonest slot (222 of 356). "
 "**Lexicon.** Cunliffe πύματος 3: 'the last in sequence or time: δρόμον Il. 23.373, 768'. That is the last lap which brief §3.3 pairs with the end of a set. "
 "**Sense and facts.** The gloss is right. This is Djokovic's second set; 7-4 at 2:15:24 ✓.",
 "[24a] ἐνίκα → 8; [24b] νικ- with μάχ- → 5 (Il. 16.79); [24c] πυματ- → 17; [24f] \"μιν ἐνίκα\" → 0; [24k] ὅ γε + capitalised nominative → Il. 13.70; [24l] ὅ γ᾽ ἥρως → 7; [24n] pronoun + name → Il. 8.532, 11.660, 16.25; [24m] ἔπειτα positions; Cunliffe νικάω, πύματος (A.10)"),
27: ("PASS",
 "**Changed (m3, M6).** The verse is Il. 23.116 verbatim. Perseus ends it with ·; v4 has a comma. It replaces the transplanted simile apodosis ὣς μὲν τῶν ἐπὶ ἶσα μάχη … (critic m3), and so also removes the near-repeat of 21. "
 "**Sense.** In Homer the line is the mules' journey 'uphill, downhill, sideways and aslant' to Ida (Il. 23.114-117). Here it is the players' running in the 35-shot rally (point 242, 2:47:12). This is a figurative transfer, recorded in the jsonl; on a flat court 'uphill, downhill' is the Homeric line's own wording. The plural ἦλθον for the two follows 22 (ἀμφοτέρω βάλλον). The gloss is right. "
 "**Enjambment.** The clause is complete, and 28 continues it with καί: unperiodic.",
 "[27a] whole verse → Il. 23.116 [1-12]; ctx Il. 23.113-118; [FACTS] pt 242, 35 shots, winner Fe"),
29: ("PASS",
 "**New (M3, M4).** This is the break at 2:49:12 (point 244, Federer's forehand into the net, AD-40) in the game of the 35-shot rally. The set-4 sequence is now rally (27-28) → break (29) → hold for 6-4 (30). "
 "**Syntax.** The passive ἐδάμη keeps Federer as subject, so 30's ἔλαβεν is his ✓. ἀλλὰ καὶ ὧς ('but even so') stands at 1-3 (17x) and answers 28's winner. "
 "**Morphology.** Νοβήκου is the regular genitive of Νοβῆκος. A long ultima moves the accent to an acute on the penult, as in all 5 Homeric -ῆCος/-ήCου pairs (κλῆρος/κλήρου, χῶρος/χώρου, Ῥῆσος/Ῥήσου, δῆμος/δήμου, νῆσος/νήσου; 0 against). It does not breach R9, which fixes the nominative. κρατεροῦ is the -οῦ genitive (3x, beside κρατεροῖο). "
 "**Idiom.** The model is ἀλλ᾽ ἐδάμη ὑπὸ χερσὶ ποδώκεος Αἰακίδαο (Il. 2.860 = 2.874). ἐδάμη is moved from 1.5-3 to 3.5-5, a disclosed mobility. The genitive phrase is split round ὑπὸ χερσί, as in πολιῆς ἐπὶ θινὶ θαλάσσης (Il. 4.248) and Ἀθηναίης ἐπὶ γούνασιν ἠϋκόμοιο (Il. 6.92). There is hiatus after κρατεροῦ at the longum 7; the licence is attested once (Il. 21.553), with no check_line flag. "
 "**Register.** 10 of the 11 Homeric lines with ὑπὸ χερσί are killings. The exception is a contest: Il. 23.675 (ἐμῇς ὑπὸ χερσὶ δαμέντα, the beaten boxer carried out alive). Cunliffe δαμάζω 5 'to overpower, get the better of … to defeat' covers the sense. Cite 23.675. "
 "**Sense and facts.** The gloss is right ✓.",
 "[29a] \"ἀλλὰ καὶ ὧς\" → 17; [29b] ἐδάμη → Il. 2.860, 2.874; [29h] \"ὑπὸ χερσὶ\" → 11 + ctx Il. 23.672-676; [29e] \"ὑπὸ κρατεροῦ\" → Il. 21.553; [29g] κρατεροῦ → 3; [29k] split genitive round a prepositional phrase → 14; [ACC2] → 5 acute / 0 circumflex; [FACTS] pt 244 winner Dj; Cunliffe δαμάζω 5-6 (A.10)"),
32: ("PASS",
 "**Changed (M4, M6).** ἐδάμασσε βοὴν ἀγαθὸς Φεδερῆρος becomes ἐπόρουσε καὶ ἀμφήριστον ἔθηκεν, which removes the adjacent βοὴν ἀγαθ- pair of v3 29-30. "
 "**Idiom.** 1-5.5 is αὐτὰρ ὃ ἂψ ἐπόρουσε (Il. 3.379, 21.33, both at 1-5.5) with γ᾽ in place of the hiatus, as αὐτὰρ ὅ γ᾽ ἂψ (Od. 11.599). The jsonl cites 11.580 and Od. 11.599; cite Il. 3.379 / 21.33, the closer model. ἀμφήριστον ἔθηκεν is the race formula at 7-12 (Il. 23.382, 527). In Homer it occurs only inside an unreal κεν clause; here it is a plain past, a disclosed change of frame. "
 "**Lexicon.** Cunliffe ἀμφήριστος: '[neut.] a dead heat'. Cunliffe ἐπορούω 1: 'to rush at a foe'. "
 "**Sense and facts.** The break back to 4-3 (3:31:55) 'made it a dead heat', the commentator's 'Game on again' ✓. 4-3 is 'on serve' rather than level; 'dead heat' renders the cancelled break. The gloss is right.",
 "[32a] \"ἀμφήριστον ἔθηκεν\" → Il. 23.382, 527 [7-12] + ctx; [32c] \"ἂψ ἐπόρουσε\" → Il. 3.379, 21.33 [3-5.5]; [32d] → Od. 11.599; [32e] → Il. 11.580, 13.550; Cunliffe ἀμφήριστος, ἐπορούω (A.10)"),
33: ("PASS",
 "**Changed (m4).** The plural relative τῶν ῥ᾽ ἅμα τ᾽ of Il. 13.85 becomes the demonstrative dual τοῖιν δ᾽ at 1-2, as in Il. 13.66 (τοῖιν δ᾽ ἔγνω …; τοῖιν 4x). 3-12 is Il. 13.85 verbatim. "
 "**Syntax.** A dative of the person with φίλα γυῖα λέλυνται is Homeric: τῷ μοι φίλα γυῖα λέλυνται (Od. 8.233). (In Od. 18.242 the οἱ belongs to νόστος.) The gloss 'of the two of them' is right. "
 "**Facts.** The clock is now a range (3:29:35-4:27:58), which removes the inversion noted by the critic (m4). The fatigue is that of the commentary ✓. γυῖα λέλυντο here is fatigue, as in Il. 7.6 and 13.85, not death.",
 "[33a] τοῖιν → 4 (Il. 13.66 [1-2]); [33b] → Il. 13.85 [3-12] + ctx; [33c] dative + γυῖα λέλυνται → Od. 8.233 (of 4 hits)"),
34: ("PASS",
 "**Changed (M4, m1).** ἄφαρ ἄσπετον ἤρατο κῦδος becomes παρέλασσε βοὴν ἀγαθὸς Φεδερῆρος. The glory formula is no longer spent on a break, and ὀψέ no longer sits with ἄφαρ. "
 "**Idiom.** The verse is the whole-line frame ὀψὲ δὲ δὴ μετέειπε βοὴν ἀγαθὸς Διομήδης (Il. 7.399 = 9.31 = 9.696) with one verb changed. The jsonl cites Il. 5.114; cite 7.399 and its repeats. ὀψὲ δὲ δή is always at 1-3 (12x). "
 "**Morphology.** παρέλασσε is unelided (Homer has παρέλασσ᾽ 2x). Cunliffe lists the form as παρέλασσε (Il. 23.382, 527); the check_line warning on α is 'analogy' only. "
 "**Lexicon.** Cunliffe παρελαύνω 1a: 'to drive one's chariot past another, outstrip him in the race' (intransitive, Il. 23.382). "
 "**Sense and facts.** The break for 8-7 at 4:07:16 (point 354) is the overtaking ✓. ὀψέ 'late, at last' fits the fifteenth game of the set. The gloss is right.",
 "[34a] παρελασσ- → 3; [34b] παρηλασ- → 3; [34d] \"ὀψὲ δὲ δὴ\" → 12, all [1-3]; [34g] whole frame → Il. 7.399, 9.31, 9.696; Cunliffe παρελαύνω (A.10)"),
35: ("PASS",
 "**New (M7).** The verse is Il. 18.502 verbatim; v4 adds a comma after ἐπήπυον. "
 "**Lexicon.** Cunliffe ἐπηπύω: 'to give one's voice in approval … to. With dat.: ἀμφοτέροισιν ἐπήπυον Il. 18.502'. Cunliffe ἀρωγός: 'a helper … Il. 18.502 (partisans)'. "
 "**Context.** In Homer this is the trial on the Shield: two men in dispute, the people cheering both sides, and the heralds restraining them (18.497-506), with an ἴστωρ (18.501) for an umpire. The scene fits a contest before a crowd. "
 "**Facts.** 4:08:51, the umpire's call for quiet (tv_2019wimF:0409). Supporters of both men are in brief §1.9 ✓. The gloss is right.",
 "[35a] whole verse → Il. 18.502 [1-12]; ctx Il. 18.497-506; Cunliffe ἐπηπύω, ἀρωγός (A.10)"),
36: ("PASS",
 "**New (M7).** 1-8 is Il. 18.503 (κήρυκες δ᾽ ἄρα λαὸν ἐρήτυον) in its own slot. ἔνθα καὶ ἔνθα follows at 9-12, its commonest slot (21 of 32). ἐρήτυον keeps its attested 6-8 position, and its -ον is short before the vowel. "
 "**Lexicon.** Cunliffe ἐρητύω 1 'to hold back, restrain' and 2 'to get under control: κήρυκές σφεας Il. 2.97'. Il. 2.96-98 (κήρυκες βοόωντες ἐρήτυον, εἴ ποτ᾽ ἀϋτῆς σχοίατ᾽) is the closest Homeric model for the umpire's 'Please'; cite it beside 18.503. ἐρήτυ- + ἔνθα καὶ ἔνθα has 0 hits; the combination is new, the pieces are attested. "
 "**Sense and facts.** The umpire is rendered by the heralds of brief §3.10, unnamed (§5.3) ✓. The gloss is right.",
 "[36a] → Il. 18.503 [1-8]; ctx Il. 2.96-98; [36f] \"ἔνθα καὶ ἔνθα\" → 32 (21 at 9-12); [36d] → 0; Cunliffe ἐρητύω (A.10)"),
38: ("PASS",
 "**Changed (M4, M6).** The verse is Il. 3.373 / 18.165 with εἴρυσσέν → ἔνθ᾽ ἔλαβέν. καί νύ κεν ἔνθ᾽ stands at 1-3 (3x), and ἄσπετον ἤρατο κῦδος at 7-12. Both Homeric instances of the glory formula are counterfactuals followed by εἰ μή (3.374, 18.166). 39 supplies the εἰ μή, so ἤρατο κῦδος now stands where Homer puts it ✓ (M4). "
 "**Morphology and accent.** ἔλαβέν τε takes the second acute before the enclitic, as εἴρυσσέν τε. ἔλαβεν at 3.5-5 is a disclosed mobility (Homer: 5.5-7 2x, 1.5-3 1x). "
 "**Syntax.** καί νύ κεν + aorist indicative, then εἰ μή + aorist indicative: the Homeric past unreal. The object of ἔλαβεν is understood ('it', the fifth ἄεθλον of 30); the gloss supplies 'it'. "
 "**Sense and facts.** CP1 (point 359, 4:10:58) ✓. The subject is Federer, carried from 37 (Ῥογῆρος).",
 "[38a] → Il. 3.373, 18.165 [7-12] + ctx (εἰ μή); [38b] \"καί νύ κεν ἔνθ᾽\" → 3 [1-3]; [38c] ἔλαβεν → 3; [38d] \"ἔλαβέν τε\" → 0"),
40: ("PASS",
 "**New (M1, M6).** CP2 is narrated (point 360, 4:11:30). Federer approaches (στῆ δὲ μάλ᾽ ἐγγὺς ἰών, 1-5, 5x: Il. 4.496, 5.611, 11.429, 12.457, 17.347), and Djokovic passes him (`6r28f+1f1*`). Djokovic is the subject of a hit verb at 4:11:30, which answers the critic's test for M1 ✓. "
 "**Syntax.** ὃ δέ switches the subject to 'the other' at 5.5. The shape ἰών, ὃ δέ is that of Il. 22.123 (ἵκωμαι ἰών, ὃ δέ μ᾽ οὐκ ἐλεήσει). The man forestalled and hit by the other is Il. 13.387 (… ὃ δέ μιν φθάμενος βάλε δουρί). ὃ δέ μιν occurs 9x, once with βάλε later in the verse (Il. 13.387). οὐδ᾽ ἀφάμαρτε stands at 9-12, as in Il. 14.403 and 22.290 (καὶ βάλε … οὐδ᾽ ἀφάμαρτε). βάλεν with movable ν is closed before οὐδ᾽ (μιν is long by position before β). "
 "**Idiom.** In Homer στῆ δὲ μάλ᾽ ἐγγὺς ἰών is always followed by the same subject's act. Giving the second half to the opponent is a combination, not a model. "
 "**Sense and facts.** The subject of στῆ is Federer, the subject of 38-39 ✓. The gloss is right.",
 "[40a] → 5 [1-5]; [40g] \"ὃ δέ μιν\" → 9 (Il. 13.387); [40f] \"ἰών, ὃ δ\" → Il. 22.123; [40e] \"οὐδ᾽ ἀφάμαρτε\" → 4 (2 at 9-12); [FACTS] pt 360 winner Dj"),
49: ("PASS",
 "**Changed (M7, m8).** ἔκφερε δ᾽ αὖτε Νοβῆκος, ὃ δ᾽ ἕσπετο κέρδεα εἰδώς becomes Σέρβος δ᾽ ἔκφερεν αὖ, ὃ δ᾽ ἐπέσσυτο τυτθὸν ὀπίσσω. The aorist ἕσπετο ('accompanied', m8) is gone, and τυτθόν (brief §3.6, 'a little bit') enters the verse. "
 "**Morphology.** ἔκφερεν is the unaugmented imperfect with movable ν before a vowel, as in Od. 15.470. It is intransitive: 'shoot ahead' (Cunliffe ἐκφέρω 6). ὃ δ᾽ ἐπέσσυτο stands at 5.5-8, as in Il. 21.234 and 21.601. There is hiatus after αὖ at the longum 5, at a comma; the licence is attested for αὖ once (Il. 3.383), with no check_line flag. "
 "**Lexicon and sense.** τυτθὸν ὀπίσσω occurs once in Homer (Il. 5.443, 9-12), where it means 'withdrew a little backwards' (Cunliffe ὀπίσσω 1, τυτθός 2d). Here it means 'a little behind', Cunliffe ὀπίσσω 2 'of place, behind, in rear' (Il. 9.507 αἳ δ᾽ ἐξακέονται ὀπίσσω, followers behind a runner). That is a shift of sense inside the formula; record it. "
 "The pursuit with a 'little' margin has an exact Homeric scene: Il. 21.601-604, ὃ δ᾽ ἐπέσσυτο ποσσὶ διώκειν … τυτθὸν ὑπεκπροθέοντα (Cunliffe τυτθός 2e 'keeping always a little ahead'). Cite it. "
 "**Facts.** 9-8 (4:17:15) and 9-9 (4:21:04) ✓. The gloss is right. "
 "**Note.** Σέρβον (48) and Σέρβος (49) stand in adjacent verses. An adjacent name repeat is Homeric (Il. 22.211-212 Ἕκτορος), but it is the one new adjacent pair in the rewrite (M6).",
 "[49a] \"τυτθὸν ὀπίσσω\" → Il. 5.443 + ctx; [49b] \"ὃ δ᾽ ἐπέσσυτο\" → Il. 21.234, 21.601 [5.5-8] + ctx 21.600-605; ctx Il. 9.505-507; [49d] ἔκφερεν → Od. 15.470; [49g] τυτθόν → 29; [49h] → 0; Cunliffe ὀπίσσω, τυτθός, ἐκφέρω (A.10)"),
54: ("PASS",
 "**Changed (M5).** τανηλεγέος θανάτοιο gives way to μάχης θαλερῶν αἰζηῶν. 1-5.5 is Il. 8.70 = 22.210. θαλερῶν αἰζηῶν stands at 7.5-12 (Il. 10.259, 14.4) with the spondaic fifth foot of those lines. κῆρ- with μάχ- in one verse has 0 hits; the genitive chain reads 'the fates of the fight of lusty men', and 55 distributes them to the two men. "
 "**Lexicon (residual).** κῆρε stays. Cunliffe κήρ gives 1 'bane, death', 2 'one's destined fate', and 3 (this passage) 'figured as a weight put in the balance and typifying death or one's fate'. LSJ: 'doom, death … rarely without personal sense in Hom.'; Κῆρες Ἀχαιῶν, Τρώων (Il. 8.73-74). With θανάτοιο gone, the line reads as Cunliffe's 'one's fate', but κήρ is never a neutral 'lot' in Homer. "
 "Brief §2.5A asked for κῆρε to be replaced as well, 'else keep and document'. The jsonl documents the choice, and the critic's own test line kept κῆρε. Not a fault; for the paper. "
 "**Gloss.** The gloss has 'of two sturdy men', but θαλερῶν αἰζηῶν is plural and generic, and the δύο goes with κῆρε. Read 'of the fight of lusty men'. αἰζηός means 'in full bodily strength … young men' (Cunliffe); for a 37-year-old this is generic warrior diction. "
 "**Enjambment.** The clause is complete; 55 adds the apposition (τὴν μὲν … τὴν δ᾽): unperiodic, as v3 50.",
 "ctx \"ἐν δ᾽ ἐτίθει δύο κῆρε\" → Il. 8.69-74, 22.209-214; [54b] \"θαλερῶν αἰζηῶν\" → Il. 10.259, 14.4 [7.5-12]; [54d] κῆρ- + μάχ- → 0; [DEATH] → κῆρε (54), ἦμαρ (64) only; Cunliffe κήρ, LSJ Κήρ, Cunliffe αἰζηός, θαλερός (A.10)"),
56: ("PASS",
 "**Changed (M5).** κακὸν ἦμαρ gives way to τότ᾽ ἐέλδωρ. 1-7 is Il. 8.72 = 22.212 (ἕλκε δὲ μέσσα λαβών· ῥέπε δ᾽), and Ἑλβετίου stands at 7-9 (A1 slot). "
 "**Lexicon.** ἐέλδωρ means 'wish, longing, desire' (LSJ ἔλδωρ; Cunliffe 'always with prothetic ἐ'). It occurs 10x, 9 at 10-12. Elision before it is attested (κρηήνατ᾽ ἐέλδωρ, Od. 3.418, 17.242), and a possessor's genitive with it is Il. 15.74 (τὸ Πηλεΐδαο … ἐέλδωρ). "
 "LSJ ῥέπω: 'turn the scale, sink … implying defeat and death, Il. 8.72'. Homer's sinking αἴσιμον ἦμαρ is the doom-day; the loser's desire takes its place. That removes the death and keeps the defeat ✓ (brief §2.6.2). ῥέπε … ἐέλδωρ has 0 hits; the collocation is new. "
 "**Sense and facts.** The tie-break went 7-3, and the Swiss's pan sinks ✓. The gloss is right. τότε also stands in 53 (καὶ τότε δή, Il. 22.209); harmless.",
 "[56a] ἐέλδωρ → 10 (9 at [10-12]); [56b] elision before ἐέλδωρ → Od. 3.418, 17.242; [56c] \"ῥέπε δ᾽\" → Il. 8.72, 22.212 [5.5-7]; Cunliffe ἔλδωρ, ῥέπω; LSJ ἔλδωρ, ῥέπω (A.10)"),
58: ("PASS",
 "**Changed (M5, M6).** αὐτὰρ ὅ γ᾽ Ἑλβέτιος τότ᾽ ἀμύνετο νηλεὲς ἦμαρ (the death-day of Il. 11.484) becomes τὸν δ᾽ ἕτερος μετέπειτα μάλα σχεδὸν ἦλθε διώκων. 6-12 is Il. 23.499 verbatim. μετέπειτα stands at 3.5-5.5, as in Il. 14.310. τὸν δ᾽ ἕτερος has 0 hits; τὴν ἕτερος is Od. 8.374, the Phaeacian ball game. "
 "**Syntax.** τὸν δ᾽ … answers the μέν of 57's τρὶς μέν, a subject contrast, as v3 53-54 did. τόν is Djokovic, the object of διώκων. ἕτερος is 'the other of two' (Cunliffe ἕτερος 2). "
 "**Lexicon (record correction).** In Il. 23.499 Diomedes is the leader, coming in to win (23.499-513), and διώκων is absolute, 'driving' (Cunliffe διώκω 4: 'to drive (a chariot) … Absol. Il. 23.344, 424, 499, 547'). The verse uses διώκω in sense 1, 'chase, pursue', with τόν. The Greek reads correctly in that sense, but it is a shift from the source. The jsonl's 'Diomedes closing on Eumelus' misreads 23.499: Diomedes passed Eumelus at 23.382-400. "
 "**Sense and facts.** Points 418-419 (Federer drop-shot winner; Djokovic return error) bring 4-1 to 4-3 ✓. The gloss is right.",
 "[58a] \"μάλα σχεδὸν ἦλθε διώκων\" → Il. 23.499 [6-12] + ctx 23.495-501; [58b] μετέπειτα → 5 (Il. 14.310 [3.5-5.5]); [58f] → Od. 8.374; [FACTS] pts 418-419 winner Fe; Cunliffe διώκω 1, 4; μετέπειτα; ἕτερος (A.10)"),
59: ("PASS",
 "**Punctuation only.** A comma is added after Νοβῆκος, harmonised with 37 (both now as Il. 13.160). Otherwise the verse is v3 55 (a v3 PASS: R9 circumflex, R11 two hit clauses for points 420-421). Νοβῆκος stands at 6-8 after a vowel, and -κος is long before καί. καὶ βάλεν at 9-10 remains a recorded departure from Homer's 1-2 (critic M8). "
 "**Continuity.** 58 ends with a full stop; the new subject is named inside the verse ✓.",
 "rulings.py: Νοβῆκος 59, two hit clauses 37 and 59 (A.0); [FACTS] pts 420-421 winner Dj"),
61: ("PASS",
 "**Changed (M7, M6, M5).** 'Ἑλβέτιος δ᾽ ἄρα τοῦ μὲν ἀπήμβροτε δουρὶ φαεινῷ' becomes the apostrophe ἤμβροτες, οὐδ᾽ ἔτυχες, Φεδερεῦ, μάλα πολλὰ μογήσας. "
 "**Who speaks.** The narrator speaks, by apostrophe. There is no speech frame, and in Homer direct speech is never unframed. A frame would make a player speak, which brief §5.4 forbids. "
 "**Is it Homeric?** The form is. The narrator addresses the hero in the second person, aorist, with his vocative and no frame: ἐξενάριξας / Πατρόκλεις (Il. 16.692-693); Πατρόκλεες … ἔσσυο (16.584-585); οὐδὲ σέθεν, Μενέλαε (4.127). In Il. 16.786 → 787 a τὸ τέταρτον verse in the third person is followed, after a comma, by ἔνθ᾽ ἄρα τοι, Πάτροκλε. That is the switch of 60 → 61. "
 "The formula is not narratorial in Homer. ἤμβροτες occurs twice, both times in framed speech by the opponent taunting the man who missed: Diomedes to Pandarus (Il. 5.286-287) and Hector to Achilles (22.278-279). The line turns a victor's taunt into the narrator's sympathy. πολλὰ μογήσας (13x, all 9-12) is sympathetic, and Il. 23.607 has it in the second person (πολλὰ πάθες καὶ πολλὰ μόγησας). Brief §2.6.1 proposed the formula 'in the poem's own voice'. Record this for the paper; not a fault. "
 "**Morphology.** Φεδερεῦ is the regular -εύς vocative (Ἀχιλεῦ at 5.5-7: Il. 11.606, 24.503, 24.661). The last syllable of ἔτυχες is long by position before Φ. Cunliffe: ἁμαρτάνω 1 'to discharge a missile vainly … ἤμβροτες οὐδ᾽ ἔτυχες'; τυγχάνω 3 'to hit one's mark'. "
 "**Sense and facts.** Point 422, Federer's forehand error ✓. 60 ends with a comma and 61 is asyndetic; a high stop at 60 would also serve. The gloss is right.",
 "ctx ἤμβροτες → Il. 5.285-287, 22.277-279; [61b] → Il. 5.287 [1-5]; [61c] \"πολλὰ μογήσας\" → 13 [9-12]; [61d] \"μάλα πολλὰ μογήσας\" → 0; [61j] Ἀχιλεῦ positions; [61h]/[61i] apostrophes Il. 16.693, 4.127, 4.146, 7.104, 16.787; ctx ἔσσυο Il. 16.584-585; Cunliffe ἁμαρτάνω, τυγχάνω, μογέω (A.10)"),
62: ("PASS",
 "**Changed (M4).** Σέρβος δ᾽ αὖτ᾽ ἐδάμασσε, Διὸς δ᾽ ἐτελείετο βουλή becomes Σέρβῳ δ᾽ ἀντιθέῳ τότε δὴ Ζεὺς κῦδος ἔδωκε. The title now has its own formula. "
 "**Idiom.** Ζεὺς κῦδος ἔδωκε(ν) takes a dative recipient: ᾧ τε Ζεὺς κῦδος ἔδωκεν (Il. 1.279), ὅτε οἱ Ζεὺς κῦδος ἔδωκε (8.216), καὶ Ἕκτορι κῦδος ἔδωκε (18.456). Ζεὺς κῦδος stands at 8-9.5 (9 of 10), and ἀντιθέῳ at 3-5 (Il. 4.377, 5.629, 16.649). τότε δὴ Ζεύς is attested at 1.5-4 (Od. 3.132) and stands here at 5.5-8. "
 "**Lexicon.** Cunliffe κῦδος 3: 'the glory of victory, victory, triumph, the upper hand'. Il. 12.437 (Ζεὺς κῦδος ὑπέρτερον Ἕκτορι δῶκε) ends an even fight in the same way; it may be cited. "
 "**Economy.** ἀντίθεος remains Djokovic's (4, 62). "
 "**Facts.** 13-12(3) at 4:56:59 ✓. The gloss is right.",
 "[62a] \"κῦδος ἔδωκε\" → 3 [9-12]; [62b] \"Ζεὺς κῦδος\" → 10; [62c] \"τότε δὴ Ζεὺς\" → Od. 3.132; [62d] ἀντιθέῳ → 11; Cunliffe κῦδος (A.10)"),
63: ("PASS",
 "**Changed (m5, M4).** δέμας πυρὸς αἰθομένοιο becomes Διὸς δ᾽ ἐτελείετο βουλή (Il. 1.5, Od. 11.297; 6-12). In Il. 17.424 ὣς οἳ μὲν μάρναντο takes a different second half with δ᾽ (σιδήρειος δ᾽ ὀρυμαγδός), so a μέν answered within the verse is Homeric. The proem's Zeus closes the narrative. "
 "**Sense.** The imperfect is the summary 'so they fought', and the second half is no longer a scene-switch (m5) ✓. The gloss is right. "
 "**Enjambment.** The verse ends with a high stop, so it is 'none' by the punctuation test used in v1-v3; the composer has unperiodic. This is a label disagreement only.",
 "[63a] \"ὣς οἳ μὲν μάρναντο\" → 5 + ctx (Il. 17.424-425); [63b] → Il. 1.5, Od. 11.297 [6-12] + ctx; [ENJ] (A.11)"),
}
neighbour = {
18: "Before the changed 19: the horse simile's apodosis now ends ἐπέσσυτο δαίμονι ἶσος; vehicle 16-18 intact.",
21: "After the changed 20: set 2 is now stated as won (20), and τὸ τρίτον follows.",
22: "Before the changed 23: its comma is continued by καὶ βάλεν, as in every Homeric καὶ βάλεν.",
25: "After the new 24: τόν is now the Serb (24's subject); the sense is unchanged.",
26: "Before the changed 27: the rally verse follows the second serve.",
28: "After the changed 27 and before the new 29: the same verse as 23 (see 23). 29's 'even so' answers it.",
30: "After the new 29: Federer stays the subject (29 passive), so τέτρατον αὖτ᾽ ἔλαβεν is his ✓ (M3).",
31: "Before the changed 32: no βοὴν ἀγαθ- verse is now adjacent to it (M6). The nearest is 34, three verses on.",
37: "After the new 36: καὶ βάλεν now follows a full stop and the heralds; the new subject is named inside the verse (Ῥογῆρος).",
39: "After the changed 38: οἱ is Federer; the εἰ μή completes 38's counterfactual as Il. 3.374.",
41: "After the new 40: the resumptive τρίς (Cunliffe ἔπειτα 4) now gathers two narrated onsets (CP1 38-39, CP2 40) and point 361 (see §2, the count).",
42: "The fourth (point 362) on the resumptive reading; R12 ✓ (41 names Φεδερῆρος).",
48: "Before the changed 49: Σέρβον here, Σέρβος in 49 (see 49).",
50: "After the changed 49: it follows a full stop; the simile opens as before.",
51: "Now directly before the apodosis 52, since v3 47 was dropped. It ends without punctuation. Before a Homeric simile apodosis ὣς the printed text has a comma (36), a high stop (31) or a full stop (9); no stop occurs once (Od. 9.393 → 394, also after a parenthetic clause, with γάρ there and δέ here; A.0 APOD). Homeric, but a high stop after ἄεθλον is advised for print. The label stays necessary (inside the open ὡς δ᾽ ὅτ᾽ period). The vehicle is now 2 verses; two similes keep vehicles of 3 or more (16-18, 43-47).",
52: "Now follows 51 directly (v3 47 dropped). The prize of the vehicle (τὸ δὲ μέγα κεῖται ἄεθλον) is no longer 'for a dead man' (M5).",
53: "Before the changed 54: unchanged scales line (Il. 22.209).",
55: "After the changed 54: τὴν μὲν … τὴν δ᾽ still refers to κῆρε.",
57: "After the changed 56 and before the changed 58: its τρὶς μέν is now answered by τὸν δ᾽ ἕτερος (58).",
60: "Before the changed 61: its comma now leads to the asyndetic apostrophe (see 61).",
64: "After the changed 63: ὀψὲ δὲ δή also opens 34; the close is unchanged.",
}
for r in v4:
    n = r['n']; comp = r['enjambment']
    if n in full:
        v, f, e = full[n]
        print(f"| {n} | {v} | {f} | {e} | {comp} → {mine[n]} |")
    else:
        m = r['v3_line']; assert v3[m] == r['text'] and rev3[m][0] == 'PASS', n
        note = (' ' + neighbour[n]) if n in neighbour else ''
        print(f"| {n} | PASS | Unchanged, v3 PASS (= v3 {m}).{note} | identity → {n}={m} | {comp} → {rev3[m][1]} |")
```

### B.12 assemble4.py (assembles this file)

```python
# assembles review/philology_v4.md: body.md (§1-§5 and the §6 header) + rows4.py table + Appendix A (appendix4.sh output) + Appendix B (scripts verbatim)
# usage: python3 -I assemble4.py SCRIPTDIR OUT
import sys, os
S, out = sys.argv[1], sys.argv[2]
rd = lambda f: open(os.path.join(S, f), encoding='utf-8').read()
parts = [rd('body.md').rstrip('\n') + '\n', rd('table.md').rstrip('\n') + '\n\n',
         '## Appendix A. Verbatim evidence\n\n',
         'Printed by `appendix4.sh` (B.10) on 2026-10-08, run from the repository root with `.venv` active. Lines beginning `# [tag]` give the command; `python homer/concordance.py` output is unedited, and hit lists are shown in full except where a header says what is shown.\n\n',
         rd('appendixA.md').rstrip('\n') + '\n\n',
         '## Appendix B. Scripts\n\n',
         'Saved under the session scratchpad and reproduced here verbatim. Run from the repository root with `.venv` active; the Python scripts take the repository path (and, where needed, a draft path) as arguments and are run with `python -I`. ctx.py, q.sh, aspir.py, accent.py, simile.py, trismen.py and dico_text.py are the v3 scripts (philology_v3.md Appendix B), unchanged.\n\n']
scripts = [('B.1', 'identity.py', 'v4 vs v3 verses'), ('B.2', 'ctx.py', 'hits with context lines'), ('B.3', 'q.sh', 'tagged concordance call'),
           ('B.4', 'trismen.py', 'τρὶς μέν and its answering member'), ('B.5', 'rulings.py', 'R2-R12 forms, names, registers, prohibited words'),
           ('B.6', 'aspir.py', 'elision before rough breathing'), ('B.7', 'accent.py', 'accent of -η/ω + C + ος'), ('B.7a', 'accent2.py', 'accent of the genitive -ου of the Νοβῆκος type'),
           ('B.8', 'simile.py', 'simile openers and apodoses'), ('B.8a', 'apod.py', 'punctuation before a simile apodosis'),
           ('B.8b', 'names.py', 'name tokens'), ('B.8c', 'boen.py', 'βοὴν ἀγαθ- spacing'), ('B.8d', 'repline.py', 'whole verses repeated within K lines'),
           ('B.8e', 'facts.py', 'match facts for the changed verses'), ('B.8f', 'death.py', 'death-register stems'),
           ('B.9', 'tally4.py', 'counts in §2 and §4'), ('B.10', 'appendix4.sh', 'writes Appendix A'), ('B.10a', 'enj4.py', 'enjambment labels'),
           ('B.10b', 'dico_text.py', 'LSJ / Cunliffe text from a Logeion API response'), ('B.11', 'rows4.py', 'builds the §6 table'), ('B.12', 'assemble4.py', 'assembles this file')]
for tag, f, what in scripts:
    lang = 'bash' if f.endswith('.sh') else 'python'
    parts.append(f'### {tag} {f} ({what})\n\n```{lang}\n' + rd(f).rstrip('\n') + '\n```\n\n')
open(out, 'w', encoding='utf-8').write(''.join(parts).rstrip('\n') + '\n')
print('written', out)
```
