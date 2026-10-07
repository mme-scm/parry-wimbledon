# Critic review, phase "poem", v1

Reviewer: critic agent, 2026-10-07. Adversarial pass on `composition/drafts/v3.txt` (60 hexameters) and `v3.jsonl`,
after round 3 passed all 60 lines on scansion, provenance and philology. Read: CLAUDE.md, `composition/brief.md` (§1-5,
A1-A2), `review/round_1.md`-`round_3.md`, `scansion_v3.md`, `provenance_v3.md`, `philology_v3.md`,
`composition/research/match_facts.md`, `corpus/timing/points_2019wimF.csv`, the transcript index. Every number below is
printed by `review/critic_poem_v1_checks.py` (sections A-D; reads only the files named there) or by the concordance
command quoted at the item; nothing is typed from memory. Homeric contexts were read from `homer/lines.tsv`.

What I did not re-open: the metre (60 PASS, scansion_v3), the source labels and counts (provenance_v3), rulings R1-R12
and Addenda A1-A2 (names, patronymic, accent, δίς, πάλιν, ἐξενάριξε), the enjambment tally (10/60 necessary, recorded in
round 3 as a shortfall for the paper). Those I accept as settled unless a line below says otherwise.

## Summary verdict

No critical issue: no verse asserts a fact that the corpus contradicts, no line uses an item from brief §1.11's
"not available" list, every line scans. The structural requirements of the brief are met except one (the second
championship point, required expanded, is not in the verse). The weaknesses a specialist will see are of two kinds:
**fact legibility** (three places where the verse's juxtaposition or its ungraded victory language implies something the
corpus does not support, while the record's `facts` field carries the truth), and **mechanical reuse** (name density 2-3
times that of Homeric duels, the same formula in adjacent lines, four δεύτερον-phrases with four referents in seven lines,
formulae moved out of their Homeric slots). 0 critical, 8 major, 14 minor.

## 1. Critical

None.

## 2. Major

**M1. CP2 (4:11:30) is not in the poem.** Brief §2.3(2) and §2.0 require both championship points expanded: CP2 =
first serve to the T, slice return, Federer's approach, Djokovic's cross-court passing winner (`6r28f+1f1*`, point 360),
"καὶ βάλε … οὐδ᾽ ἀφάμαρτε". v3 has CP1 in 34-35 and then folds CP2 into the count of 36 (τρὶς μὲν ἔπειτ᾽ ἐπόρουσε
… Φεδερῆρος); the jsonl of 36 says "the CP2 detail now stands in the facts field only". The one stroke of the match the
commentary itself singles out (tv_2019wimF:0416 "just as Federer passed Djokovic … Djokovic denies Federer") is the one
Djokovic stroke the poem never narrates; the aristeia (38-44) therefore opens without the deed that justifies it.
*Test:* no line whose `clock` includes 4:11:30 has Djokovic as the subject of a hit verb (checks §B; 36 is a Federer
count line). *Direction:* the v2 line 36 (στῆ δὲ μάλ᾽ ἐγγὺς ἰών, βάλε δὲ κρατερὸς Ζοκοβείδης) was withdrawn only because
37's subject had to be fixed; a τρὶς δέ limb naming the Serb's answer (the Homeric sequence always has one, m2) would
restore CP2 and fix R12 at once.

**M2. Lines 22-23 imply Federer lost the 26-shot rally.** 22 narrates the rally (point 183, 2:03:53) without a result;
23 follows at once with "δεύτερον αὖ λάβ᾽ ἄεθλον ἄφαρ κρατερὸς Ζοκοβείδης". A reader of the Greek concludes that the
rally went to Djokovic and ended the set. Corpus: point 183 won by **Federer** (26 shots), in game 12 at 5-6; the set was
decided in the tie-break 2:07:34-2:15:24, eleven points later (checks §A). ἄφαρ ("at once") makes the false
implicature explicit; the philologist read ἄφαρ with λάβ᾽ (Il. 23.511) and let the colour pass, which settles the word's
grammar but not what the two lines together say about the match. *Test:* `points_2019wimF.csv` row 183 `point_winner`;
brief §1.3 set 3. *Direction:* give the rally its winner (the οὐδ᾽ ἀφάμαρτε / Ῥογῆρος close used at 27) or move ἄφαρ.

**M3. Set 4: the break at 2:49:12 is omitted and the verse implies the rally won the set.** 27 (Federer's winner,
2:47:12) is followed by 28 "τέτρατον αὖτ᾽ ἔλαβεν" (Federer takes the fourth set). Corpus: Federer was broken in that
same game two points later (point 244, 2:49:12, forehand into the net) and held for 6-4 only at 2:55:08 (checks §A).
The brief's line budget (§2.0 "two breaks, the 35-shot rally expanded, broken back, 6-4") and §2.3(1) ("then broken at
2:49:12") plan the break; round-1 R7 removed the causal ὣς from 28, but removing the word did not remove the implicature,
and the fact now sits only in the `facts` field of 27, a line whose verse says Federer hit a winner. *Test:* rows 242-244;
brief §2.0 set-4 row. *Direction:* one line between 27 and 28 (the τὸν δ᾽ αὖθ᾽ … δάμασεν pattern of 24, with the Serb as
subject) restores the sequence rally → break → hold.

**M4. Victory language is not graded, so the match's hierarchy is illegible in the Greek.** ἐδάμασσε / δάμασεν stands
for a break of serve (20, 24, 29, 30) and for the title (34 "would have", 58 the end); ἄσπετον ἤρατο κῦδος, Homer's
largest glory formula, is spent on the service break for 8-7 (32), while the sets get ἐνίκα (15), λάβ᾽ ἄεθλον (23),
ἔλαβεν (28) and set 2 is never said to be won at all (19-20 narrate three breaks and stop). In Homer all 20 lines with
δάμασσε / ἐδάμασσε(ν) / δάμασε(ν) are kill, overpower or subjugate (a god, fate, a lion, arrows, Zeus's sceptre; checks §C,
`--regex "δάμασσε|ἐδάμασσε|δάμασε"`), never "beat in a contest"; Homer's contest verb is ἐνίκα (Il. 4.389, 5.807, 23.680,
23.756: games and footraces), which the poem uses once, for a set. ἄσπετον ἤρατο κῦδος is attested twice (Il. 3.373,
18.165), both times inside καί νύ κεν … εἰ μή (would have won, and did not): the formula's own sense is CP1, where the
poem instead uses ἐδάμασσε. Read without the jsonl, 29 says the Serb overcame Federer at 3:25:11 and 30 that Federer
overcame him back; 58 says the same thing a third time. The rulings (R5) licensed δάμασσε among others; they did not ask
for one verb to do every job. *Test:* the concordance contexts above; show 29-30 and 58 to a Homerist without the records.
*Direction:* reserve one verb for the match (ἐνίκα / νίκησε, the contest verb) and keep ἤρατο κῦδος for CP1's
counterfactual, where Homer puts it.

**M5. The 12-12 tie-break is narrated as Federer's death, four times over.** 50 "δύο κῆρε τανηλεγέος θανάτοιο" (two
fates of death), 52 "ῥέπε δ᾽ Ἑλβετίου κακὸν ἦμαρ" (the sunken day is, in Il. 22.212-213, the day Hector goes to Hades),
54 "ἀμύνετο νηλεὲς ἦμαρ" (Il. 11.484, 13.514: warding off one's death), and 47 "ἀνδρὸς κατατεθνηῶτος" (the prize for a
dead man, in a simile whose tenor has no dead man). Brief §2.6.2 "Keep the loser alive" and §2.5A "Replace κῆρε …
θανάτοιο by the two νίκαι or ἄεθλα"; round 1 allowed "else keep and document". The jsonl of 50 documents a search limited to
"a genitive pair of the same shape SLSSL + SSLX" (0 hits) and concludes the line must stay. The search was too narrow: the
second half need not be a genitive pair. `check_line` passes `ἐν δ᾽ ἐτίθει δύο κῆρε, τὸ δὲ μέγα κεῖται ἄεθλον` (DDDDDS,
tier 1, the same lengthening before μέγα as the verbatim 46) and `ἐν δ᾽ ἐτίθει δύο νίκας ἐπειγομένων περὶ νίκης` (DDDDDS,
tier 0, a quantity warning on νίκας) (checks §D; metre only, not proposed wording). *Test:* those two runs; whether any
reading of 50-54 avoids "the Swiss's death". *Direction:* replace θανάτοιο's half-line and consider dropping 47 (the
simile keeps three lines, 45-46-48, only if 46 is counted as the vehicle's second line; otherwise keep 47 and accept the
tripod and the woman as Homeric colour, but say so in the paper).

**M6. Repetition that is mechanical rather than formulaic.** Counts (checks §B-C):

| item | poem | Homer | note |
|---|---|---|---|
| βοὴν ἀγαθὸν Φεδερῆρον / βοὴν ἀγαθὸς Φεδερῆρος in **adjacent** lines (29-30) | 1 pair | 0 adjacent pairs of any βοὴν ἀγαθ- formula in 27,794 lines | the philologist found the nearest parallel two lines apart (Od. 8.2/8.4) |
| βοὴν ἀγαθ- + Φεδερῆρ- | 6 in 60 lines (14, 20, 29, 30, 34, 36) | 51 lines in all Homer | 34 and 36 two lines apart as well |
| δεύτερον αὖ / αὖτε / αὖτις | 5 (7, 19, 23, 24, 25); 4 in lines 19-25 with four referents: second set, Djokovic's second set-win, second break, second serve | 12 lines | the reader cannot tell which "second" is which; 25's "second serve" has no narrated first serve |
| name tokens of the two players | 33/60 = 0.55 per line; 29/47 = 0.62 in the narrative 12-58 | 0.21-0.24 per line in Il. 3.340-382, 7.244-312, 22.248-330, 21.139-204; 0.41 in the wrestling Il. 23.708-739 | exploratory benchmark, stems listed in the script |
| ἐπὶ/κατὰ ἶσα μάχη(ν) | 3 in lines 13-26 (set 1, set 3, one rally) | 3 lines in all Homer | the whole-line 21 ≈ 26 five lines apart for a set and a point |
| verse-final ἦμαρ | 3 in lines 52-60, three senses (evil day, pitiless day, late afternoon) | — | the literal δείελον ἦμαρ arrives after two days of death |
| καὶ βάλεν, οὐδ᾽ ἀφάμαρτε + name + καὶ βάλεν αὖτις | 33 = 55 with the name swapped; 27 a third καὶ βάλεν, οὐδ᾽ ἀφάμαρτε | καὶ βάλεν 11x, οὐδ᾽ ἀφάμαρτε(ν) 6x in all Homer; βάλλω + αὖτις 0x | whole-line reuse is Homeric; the 9-10 καὶ βάλεν is not (M8) |

Homer repeats whole lines and name-epithet formulae freely, but not the same formula in consecutive lines and not four
ordinal phrases with shifting referents in seven lines; the density of names here is that of a scoreboard, not of a
duel narrative. *Test:* the counts above (rerun the script). *Direction:* 30 can take a pronoun (ὃ δ᾽ ἂψ …) or Ῥογῆρος;
19/23/24/25 should keep at most two δεύτερον, with the set ordinal carried by the Il. 23.301/23.351 pattern the brief
gives in §3.4.

**M7. Two of the ten commentary systems have no Homeric equivalent in the poem, and the match has no spectators.**
Brief §3: "use the Homeric equivalent wherever the commentators used theirs … record the pairing in the jsonl". The
`commentary_equivalent` fields cite 3.1-3.5 and 3.7-3.9 (4-11 times each) and **never 3.6 or 3.10** (checks §B).
3.6 (`a little bit` / `a little`, 39 utterances, attested in 18 of 18 pool streams, "the most widely shared formula")
↔ τυτθόν / ὀλίγον / οὐδ᾽ ἠβαιόν: 0 tokens in the verse. 3.10 (`mr <NAME>`, the umpire's calls, 11 utterances) ↔ the
vocative address and κήρυκες: no umpire, no herald, no vocative anywhere. The crowd, present in the corpus (brief §1.9,
twelve clips; MF T15 ten) and planned twice (§2.0 ending row; §2.6.3 "use the generic lines"), is absent: no λαοί, ὅμιλος,
θάμβος, ἴαχον or στενάχοντο (checks §B). A Homeric duel without onlookers has no parallel (θάμβος δ᾽ ἔχεν εἰσορόωντας,
Il. 3.342 = 4.79, closes the arming scene the poem copies). The ending shrank from the planned eight lines to three. *Test:*
`grep` of the verse and the jsonl field (script §B). *Direction:* one τυτθόν line at the one-millimetre challenge
(1:28:22, brief §3.6) or at a one-game lead; one generic crowd line (§2.6.3) after 37 or 58; the umpire's "Please" at
4:08:51 as κήρυκες δ᾽ ἄρα λαὸν ἐρήτυον (§3.10).

**M8. Formulae moved out of their Homeric slots, in a poem meant to exhibit Parry's "same metrical conditions".** The
jsonl discloses eight `mobility` modifications (lines 22, 23, 28, 33, 48, 51, 55, 60; checks §B), three of them multi-word
formulae at positions Homer never gives them: λάβ᾽ ἄεθλον 9.5-12 → 3.5-5.5 (23), καὶ βάλεν 1-2 (11/11) → 9-10 (33, 55),
τὴν δ᾽ αὖ 1-2 (13/13) → 6-7 (51); plus single words (σφαῖραν, βάλλον 22; ἔλαβεν 28; πολλάκι 48; τέλος 60) and the
provenance's two "not a Homeric position" fragments (48 δὴ περί, 56 δ᾽ ἄψ). The verifiers accept these as disclosed
modifications, correctly; but a formula used under other metrical conditions is, by the definition the paper quotes
(paper.md §1), no longer that formula, and the composer's defence ("the kind as οὐδ᾽ ἀφάμαρτε, which Homer sets at 3-5.5
and 9-12") confuses a formula that Homer has in two shapes with one that Homer has in one. *Test:* `--ngram "καὶ βάλεν"`
(11x, all 1-2), `--ngram "λάβ᾽ ἄεθλον"` (1x, 9.5-12), `--ngram "τὴν δ᾽ αὖ"` (13x, all 1-2). *Direction:* either restore the
slots (33/55 could open the second clause with a different hit verb; 23 can close on λάβ᾽ ἄεθλον) or have the paper's §5
count these as departures from the Homeric localisation, not under the neutral label "mobility"
(`paper/weaving_section_draft.md` line 231 plans to count exactly this from the jsonl).

## 3. Minor

**m1 (32).** ὀψὲ δὲ δὴ … ἄφαρ: "late at last … forthwith" in one line. Homer has ὀψὲ δὲ δή 9x, always "at last [after
a silence or delay] X spoke / came", and no line with both ὀψ- and ἄφαρ (checks §C). *Test:* `--regex "ὀψ.*ἄφαρ"`.

**m2 (36-37).** The count works only on the resumptive reading of ἔπειτα (CP1 of 34-35 counted inside τρίς), which the
philologist accepted from Cunliffe; a reader taking ἔπειτα as "thereafter" gets five points for four (359-362). In Homer
every τρὶς μὲν ἔπειτ᾽ ἐπόρουσε (Il. 5.436, 16.784, 20.445) has a τρὶς δέ limb before ἀλλ᾽ ὅτε δὴ τὸ τέταρτον, and of the
12 line-initial τρὶς μέν lines 11 have τρὶς δέ (the twelfth, Il. 13.20, has τὸ δὲ τέτρατον in the same line); 36 → 37 is
a contraction. Also "sprang to the attack" for point 361 (a seven-shot backhand exchange ending in a Federer forced
error, `5b28b3b3b2f1r#`) is loose: the τρίς counts points lost, not onsets. *Test:* `--ngram "τρὶς μὲν"` with the next two
lines; row 361. The τρὶς δέ limb is the natural home for CP2 (M1).

**m3 (26).** ὣς μὲν τῶν ἐπὶ ἶσα μάχη τέτατο πτόλεμός τε is, in both Homeric uses (Il. 12.436 after the wool-weighing
woman, 15.413 after the carpenter's line), the apodosis of a simile, with μέν answered by πρίν γ᾽ ὅτε / ἄλλοι δ᾽. Here no
simile precedes, ὣς points at nothing and μέν is unanswered: a verbatim line transplanted with its joints showing. *Test:*
`--ngram "ἐπὶ ἶσα μάχη τέτατο"` with three lines of context.

**m4 (31).** Il. 13.85 verbatim: τῶν there is a relative continuing 13.83-84 (τοὺς … Ἀχαιούς, οἳ … τῶν ῥ᾽); here it is
a demonstrative for two men, where the dual τοῖιν (4x in Homer) is available, and the epic τ᾽ of a general clause sits in
a particular statement. The clock (3:29:35) also precedes line 30's (3:31:55): the fatigue line is placed after the
break-back it preceded, the only clock inversion outside the similes (checks §B). *Test:* context of Il. 13.83-85;
`--loose "τοιιν" --word`.

**m5 (59).** ὣς οἳ μὲν μάρναντο δέμας πυρὸς αἰθομένοιο is in all five Homeric uses (Il. 11.596, 13.673, 17.366,
17.424, 18.1) a scene-switch, the next line turning to Nestor, Hector, Antilochus; as the penultimate line after the
match has ended (58) it says "so they were fighting" of a finished fight. *Test:* the five contexts (checks §C).

**m6 (5, 10).** Both players are introduced with ἑτέρωθεν. In Homer's 22 "X δ᾽ ἑτέρωθεν" and 8 "δ᾽ αὖθ᾽ ἑτέρωθεν" lines the
phrase answers a first party already narrated without it (Il. 8.53-55 Achaeans arm, Τρῶες δ᾽ αὖθ᾽ ἑτέρωθεν; Il. 3.328-339
Paris arms with αὐτὰρ ὅ γ᾽, Menelaus with ὣς δ᾽ αὔτως). Line 5's "on the other side" has no first side. The arming order
itself (Federer in full, Djokovic in one line) is the conventional Paris/Menelaus order and asserts no fact (R7), but a
reader will read it as the match's order; the jsonl says so, the paper should too. *Test:* `--ngram "δ᾽ ἑτέρωθεν"` with
one line of context.

**m7 (7, 19).** δεύτερον αὖτε: 0 hits in Homer (δεύτερος αὖτε 1x, Il. 7.248; δεύτερον αὖ 4x, αὖτις 6x, αὖτ᾽ 2x). Disclosed
as a modification; it is the only unattested two-word collocation used twice. *Test:* `--ngram "δεύτερον αὖτε" --count`.

**m8 (44).** ὃ δ᾽ ἕσπετο (0x) stretches an aorist that in all 12 Homeric instances means "accompanied" to "kept pace at
9-9" (the philologist's own note), and κέρδεα εἰδώς identifies Federer only for a reader who remembers line 27, seventeen
lines earlier. *Test:* `--loose "εσπετο" --word`.

**m9 (48).** The apodosis repeats the vehicle (περὶ τέρματα δινηθήτην) instead of stating the tenor: the two men went
round nothing, and the verse clocked to 4:17:15-4:47:47 reports none of the eight holds, the 14-point game or the
24-shot rally that its `facts` field lists. In Il. 22.165 the apodosis names the tenor's own course (Πριάμοιο πόλιν πέρι).
*Test:* compare the verse with its `facts` field.

**m10 (8, 22, 56).** The racket is armed as ἀμφιβρότην πολυδαίδαλον ἀσπίδα θοῦριν (Agamemnon's Gorgon shield, Il. 11.32)
and never acts: the rally is βάλλον σφαῖραν (22; Homer's ball is thrown, ἔρριψε / ῥίπτασκε, Od. 6.115, 8.372-377, never
βάλλω) and the return βάλε δ᾽ ἂψ (56). The shield is decorative, and "man-encompassing" for a racket is the brief's joke
made literal. The brief sanctioned σάκος/ἀσπίς; a plainer epithet line would carry the mapping better. *Test:*
`--loose "σφαιρ"`.

**m11 (25).** δεύτερον αὖ Φεδερεὺς προΐει: the first serve (fault `4w`) is not narrated, so "a second time" has no first;
it follows 24's δεύτερον αὖτις (the second break). Part of M6. Likewise 56's ἔνθ᾽ αὖθ᾽ … προΐει is glossed "second serve"
in the jsonl, but αὖθ᾽ is "again / in turn": the fact (second serve after `6d`) is in the record, not the verse.

**m12 (1-3).** τὼ περὶ νίκης / δηρὸν ἐμαρνάσθην ἔριδος πέρι θυμοβόροιο / ἐξ οὗ δὴ τὰ πρῶτα διαστήτην ἐρίσαντε: two περί
in two lines ("for victory … over strife"), and the ἐξ οὗ clause, which in Il. 1.6 depends on ἄειδε, here depends on
ἐμαρνάσθην ("fought from the time they first stood apart in strife"), which is circular. Readable; a specialist will
notice. *Test:* Il. 1.6-7 and 7.301 contexts.

**m13 (jsonl `facts`).** The field carries facts the verse does not state: 2 (the longest final; δηρόν says "long"),
4 (seeds), 13 (the break point at 0:15:23), 16 (22½ minutes, 26-12, winners 9/2), 23 (5-1, 5-4), 26 (43.44 s, distance
run), 27 (the 2:49:12 break: M3), 45/48 (the 14-point game, the 24-shot rally), 47/58 (the records). For the paper's
"every fact sourced" claim the field should separate "stated in the verse" from "context", or the audit is circular.

**m14 (16-18).** The horse simile is cut after Il. 6.508 (a participle), losing 6.509-511 (κυδιόων, head high, mane
streaming, knees carrying him to the haunts of horses), which is the point of the simile for a player who has just
lost a set and now runs free; syntax is complete, sense is thin. Not a fault; a choice to record.

Recorded, not new: necessary enjambment 10/60 (16.7%) against the brief's ~33% and Parry's 26.6%; in the duel narrative
only 37 runs on, and that end-stopping is what makes the narrative read as a catalogue of transplanted lines (round 3
note; paper limitation).

## 4. Structural requirements (brief §2, §5)

| requirement | status | where |
|---|---|---|
| proem (theme, two names, "from where they first stood apart") | met | 1-4; Διὸς βουλή deferred to 58 |
| arming as typical scene, attested order | met (greaves, tunic, shield, spear; sword and helmet skipped as allowed) | 5-11; see m6, m10 |
| set by set | met | 12-15, 16-20, 21-23, 24-28, 29-57 |
| expanded decisive points: 35-shot rally; CP1 and CP2; 12-12 tie-break | 35-shot rally 25-27 met; CP1 34-35 met; **CP2 absent (M1)**; tie-break 49-57 met | |
| aristeia (Djokovic) | met | 38-44 (lion simile, ἀνῆκε μένος, ἔκφερε) |
| ≥ 2 extended similes (≥ 3 lines) with apodosis | met: horse 16-18 → 19; lion 38-42 → 43; racing horses 45-47 → 48 | see m14, m9, M5 |
| ending: loser's hope, crowd, handshake, prize, hour | hope 52; hour 60; handshake and prize rightly omitted (§1.11); **crowd absent (M7)** | 58-60 |
| ten commentary systems' equivalents used where the plan said | 3.1-3.5, 3.7-3.9 used; **3.6 and 3.10 never (M7)** | jsonl `commentary_equivalent` |
| each player's three metrical shapes; one epithet assignment | met: Federer Φεδερῆρος 9.5-12 / Ἑλβέτιος 1-3 / Ῥογῆρος 6-8 (+ Φεδερεύς); Djokovic Ζοκοβείδης / Σέρβος / Νοβῆκος; βοὴν ἀγαθός + κέρδεα εἰδώς v. κρατερός + ἀντίθεος | scansion_v3 table |
| counting formula at every narrated score change; victory formula at every game/set won | counting met (14, 20, 36, 53); victory formulae present but ungraded (M4); set 2's win unstated | |
| enjambment near a third necessary | not met (16.7%), recorded | round 3 |
| nothing from §1.11; no sunset; no speech; no named third party | met | 60 δείελον ἦμαρ |
| line count 45-55 | 60 (10 over; the ending is 5 under plan, the similes 6 over) | |

## 5. Match-fact audit (every fact-bearing line against `points_2019wimF.csv` and brief §1; checks §A)

| lines | verse asserts | corpus | verdict |
|---|---|---|---|
| 12 | Federer served first | point 1 server Federer | OK |
| 13 | set 1 level, no break | T4: 0 breaks in set 1 | OK |
| 14-15 | Federer missed three times, then a fourth; the Serb won | TB1 points 84 UE, 85 UE, 86 FE, 87 UE, all Federer errors from 5-3; 7-5 | OK ("three … four" = four consecutive errors) |
| 19-20 | second set; Federer "subdued him" three times | breaks in set-2 games 1, 3, 7, all by Federer | OK; set win itself unstated (M4) |
| 21 | third set level | 0 breaks in set 3 | OK |
| 22-23 | ball struck back and forth; at once Djokovic took the prize a second time | point 183 (26 shots) **won by Federer**, game 12; TB 7-4 later | verse true, implicature false (M2) |
| 24 | Federer broke him, and a second time | set-4 games 5 (2:36:11), 7 (2:42:40) | OK |
| 25-27 | second serve; even exchange; Federer hit and did not miss | point 242: `4w` fault, 2nd serve, 35 shots, Federer backhand winner | OK (the fault itself unnarrated, m11) |
| 28 | Federer took the fourth; the fifth remained | Federer 6-4 at 2:55:08 | OK as fact; the 2:49:12 break omitted (M3) |
| 29-30 | Serb broke, Federer broke back | games 6 (3:25:11, Dj) and 7 (3:31:55, Fe) | OK |
| 31 | both exhausted | tv_2019wimF:0341 3:29:35 | OK; clock before 30 (m4) |
| 32 | Federer won glory (break) | game 15, 4:07:16, `4s27f+1f1*` | OK (register, M4) |
| 33 | hit, did not miss, hit again | 357 ace 201 km/h, 358 ace 193 km/h, both `mcp_ace=1` | OK |
| 34-35 | would have won, had his missile not flown vainly | CP1 359: `6n` fault, 2nd serve, Dj return, Federer forehand wide `4f28f3w@` | OK |
| 36 | three times Federer attacked | 359, 360, 361 all Djokovic | OK on the resumptive reading (m2); CP2 not narrated (M1) |
| 37 | the fourth time | 362, break, Federer forehand into net | OK |
| 38-43 | the Serb rose like a lion, grazed not killed | 359-365 seven points in a row (tv:0422) | OK |
| 44 | Novak drew ahead again; the other followed | 9-8 at 4:17:15, 9-9 at 4:21:04 | OK (sense, m8) |
| 45-48 | many turns round the posts | 9-8 → 12-12 | vehicle only (m9) |
| 49-52 | scales; the Swiss's day sank | TB 7-3 | OK as outcome; death register (M5) |
| 53 | three times Djokovic rushed | 415, 416, 417 all Djokovic (Federer FE ×3) from 1-1 | OK |
| 54 | the Swiss warded off the day | 418 Federer drop-shot winner `…f2u+3*`, 419 Dj return error `6b#`; 4-3 | OK |
| 55 | Novak hit, did not miss, hit again | 420 `6f27f1*`, 421 `…f3b1*`, both Djokovic winners; 6-3 | OK |
| 56-57 | the Swiss served, Djokovic struck back, the Swiss missed | 422: `6d` fault, 2nd serve 143 km/h, Dj backhand return, Federer forehand UE `5b38f!@` | OK ("second serve" not in verse, m11) |
| 58 | the Serb won; Zeus's will done | 13-12(3), 4:56:59 | OK |
| 60 | the end came late in the afternoon | 14:10 start + 4:57; sun not set | OK |

No item of brief §1.11 (toss, walk-on, kit, ceremony, handshake, speeches, crowd reaction to the last point, sunset)
appears in the verse; the arming scene is generic (m6).

## 6. The 22 verbatim lines

Integrated (the Homeric context fits the tennis one): 3, 6, 8, 9, 11, 13, 16-18, 37, 39-42, 45-46, 49.
Transplanted with visible joints: 26 (simile apodosis without a simile, m3), 31 (plural relative τῶν for two men, m4),
47 (a dead man's prize, M5), 50 (fates of death, M5), 59 (scene-switch line as a close, m5). The verbatim share
(22/60 = 37%) is itself worth stating in the paper beside the density figures, since it drives them (provenance_v3 §9:
81.9% → 71.9% without them).

## 7. What a revision should not touch

The metre, the name system and the rulings are sound; the fixes above are local (M1-M3 one line each; M4 a verb in
four lines; M5 a half-line; M6 two or three lines; M7 three lines; M8 three lines) and none requires re-running the
whole loop more than once.

## Appendix: commands

```
source .venv/bin/activate
python -I review/critic_poem_v1_checks.py                        # sections A-D, every number above
python homer/concordance.py --regex "δάμασσε|ἐδάμασσε|δάμασε"      # M4: 20 lines, none a contest
python homer/concordance.py --ngram "ἄσπετον ἤρατο κῦδος"           # M4: Il. 3.373, 18.165, both after καί νύ κεν
python homer/concordance.py --ngram "καὶ βάλεν"                     # M8: 11x, all 1-2
python homer/concordance.py --ngram "τὴν δ᾽ αὖ"                     # M8: 13x, all 1-2
python homer/concordance.py --ngram "λάβ᾽ ἄεθλον"                   # M8: 1x, 9.5-12
python homer/concordance.py --ngram "δεύτερον αὖτε" --count         # m7: 0
python homer/concordance.py --regex "ὀψ.*ἄφαρ|ἄφαρ.*ὀψ" --count     # m1: 0
python homer/concordance.py --ngram "ἐπὶ ἶσα μάχη τέτατο"           # m3: Il. 12.436, 15.413
python homer/concordance.py --ngram "ὣς οἳ μὲν μάρναντο"            # m5: 5x
python homer/concordance.py --loose "τοιιν" --word --count          # m4: 4
python homer/check_line.py "ἐν δ᾽ ἐτίθει δύο κῆρε, τὸ δὲ μέγα κεῖται ἄεθλον"   # M5: tier 1, no flags
```
