# Round 1 verdicts (draft v1, 55 lines)

Merged by the orchestrator from review/scansion_v1.md (PASS 47 / FAIL 1 / QUERY 7), review/provenance_v1.md (PASS 34 / QUERY 11 / FAIL 10) and review/philology_v1.md (PASS 36 / FAIL 6 / QUERY 13). A line passes only if all three pass it. Orchestrator rulings on QUERY items are marked [ruling]; items needing a human are copied to FOR_HUMAN.md and the line is revised under a provisional decision so the loop can continue.

## Rulings on recurring QUERY items
- **R1 Name slots.** The brief's §4 slot list was a set of passing tests, not an exhaustive licence. A rendering in any slot where check_line.py passes with no flags and no unattested licence is allowed (Ἑλβέτιος at 3-5 and 7-9, Σέρβος at 4-5: PASS on metre). Brief addendum A1.
- **R2 Ῥογῆρος ἰσόθεος φώς (27, 49): REVISE.** -ρος at position 8 is long only if ς + ϝ(ἰσόθεος) makes position; Homer's two cases of ἰσόθεος after a consonant (Il. 2.565, 11.428 κίεν ἰσόθεος) scan the consonant-final syllable short, and the only Homeric word before ἰσόθεος φώς is a verb or μέγα. Use Ῥογῆρος elsewhere (e.g. before a consonant-initial word, or Ῥογῆρα at 5.5-7 which the brief tested) or another Federer formula.
- **R3 Djokovic renderings (48, 50, 51): REVISE under a provisional decision (FOR_HUMAN.md).** Ζοκοβίδης needs a long ι that no Homeric -ίδης has (Κρονίδης is SSL with short ι), and Νοβάκος needs a long non-Ionic ᾱ. Replace by forms that need no un-Homeric quantity: **Ζοκοβείδης** (SSLL, patronymic in -είδης from Ζοκοβεύς, as Πηλείδης from Πηλεύς; verify Πηλείδ- with the concordance; Đoković is itself a patronymic, "son of Đoko" = Ζοκοβεύς), genitive Ζοκοβείδαο / Ζοκοβείδεω (as Πηλεΐδαο / Πηληϊάδεω: verify), and **Νοβήκος** (SLX, the Ionic-epic form of the name with η for ᾱ, as Ἀθήνη for Ἀθάνα), replacing Νοβάκος in the same slots. Σέρβος and Ζοκοβεύς stay. Record the change in the jsonl name_formula fields; Ζοκοβεύς may remain as the nominative hero-name (Ἀχιλλεύς beside Πηλεΐδης).
- **R4 δίς + verb (24, 33, 49, 50): REVISE.** Homer has δίς only in δὶς τόσσον (Od. 9.491). Count with attested patterns: δεύτερον αὖ(τε), τὸ δεύτερον, τρὶς μέν … τρὶς δέ, ἀλλ᾽ ὅτε δὴ τὸ τέταρτον, or δοιώ/δοιούς with a noun.
- **R5 ἐξενάριξε for winning a point or game (20, 24, 29, 30, 34, 53): REVISE to at most two uses**, both inside the aristeia (37-41 region), where the kill-and-strip metaphor is licensed by the ἔνθα τίνα πρῶτον … ἐξενάριξε catalogue; elsewhere use attested victory language verified by the concordance (e.g. νίκησε / ἐνίκα, ἤρατο κῦδος, ἕλε κῦδος, δάμασσε, λάβ᾽ ἄεθλον). A man "slain" must not slay his slayer in the next line.
- **R6 πάλιν = "again" (23, 32): REVISE** to αὖτις / αὖ / αὖτε / ἐξαῦτις (verify positions); Homeric πάλιν means "back".
- **R7 Facts.** Lines 5 ("first to arm") and 28 (the cause asserted for the fifth set) state things not in brief §1: REVISE to what §1 supports, or make the order explicitly conventional (the typical scene's order, not a fact).
- **R8 Source labels.** Every entry the provenance verifier lists as mislabelled (5, 15, 20, 23, 24, 29, 31, 46, 51, 52; the single words at unattested positions in 22, 24, 28, 33, 49, 50, 55; the uncited Il. 16.284 model of 12; δαΐφρονε and ἔκφερε as modified/coined forms in 1 and 41; the ἀτρειδ- query in 19 and 33; the "mobility" labels that are really substitutions) must be corrected in v2.jsonl even where the verse text does not change. Add the unclaimed attested phrases (47 ἕλκε δὲ μέσσα λαβών· ῥέπε δ᾽, 34 κεν ἐξενάριξε, 1 ἄνδρε δύω).

## Per-line verdicts
| n | scansion | provenance | philology | round verdict | required action |
|---|---|---|---|---|---|
| 1 | PASS | QUERY | PASS | REVISE (jsonl) | mark δαΐφρονε as modified inflection (dual of δαΐφρων, cite the singular/plural forms); add ἄνδρε δύω Il. 23.659 |
| 2 | PASS | PASS | PASS | PASS | |
| 3 | PASS | PASS | PASS | PASS | |
| 4 | PASS | PASS | FAIL | REVISE | τε placement: use τε … καί (Il. 1.7 model) or τε after the second name |
| 5 | PASS | FAIL | PASS | REVISE | relabel δ᾽ ἄρα πρῶτος; R7 ("first") |
| 6 | PASS | PASS | PASS | PASS | |
| 7 | PASS | PASS | PASS | PASS | |
| 8 | PASS | PASS | PASS | PASS | |
| 9 | PASS | PASS | PASS | PASS | |
| 10 | PASS | PASS | PASS | PASS | |
| 11 | PASS | PASS | PASS | PASS | |
| 12 | PASS | QUERY | PASS | REVISE (jsonl) | cite Il. 16.284 as the whole-line model |
| 13 | PASS | PASS | PASS | PASS | |
| 14 | PASS | PASS | PASS | PASS | |
| 15 | PASS | FAIL | QUERY | REVISE | supply the verb of the ὅτε-clause; relabel ὃ δ᾽ ἐσσυμένως |
| 16 | PASS | PASS | PASS | PASS | |
| 17 | PASS | PASS | PASS | PASS | |
| 18 | PASS | PASS | PASS | PASS | |
| 19 | QUERY→PASS (R1) | QUERY | PASS | REVISE (jsonl) | fix the ἀτρειδ- query/count; slot allowed |
| 20 | PASS | FAIL | QUERY | REVISE | R5; relabel Il. 5.151 as model only |
| 21 | PASS | PASS | PASS | PASS | |
| 22 | PASS | QUERY | PASS | REVISE (jsonl, optionally text) | relabel σφαῖραν/βάλλον positions; fix the parallel; note dual ἀμφοτέρω with plural βάλλον (acceptable only with a Homeric parallel: cite one or use ἀμφότεροι / a dual verb) |
| 23 | PASS | FAIL | QUERY | REVISE | R6; drop πάλιν αὖτις as a source |
| 24 | PASS | FAIL | QUERY | REVISE | R4, R5; relabel |
| 25 | PASS | PASS | PASS | PASS | |
| 26 | PASS | PASS | PASS | PASS | |
| 27 | QUERY | QUERY | PASS | REVISE | R2 |
| 28 | PASS | QUERY | PASS | REVISE | relabel ἔλαβεν position; R7 |
| 29 | PASS | FAIL | QUERY | REVISE | R5; relabel βοὴν ἀγαθὸν Μενέλαον (count 5) |
| 30 | PASS | PASS | QUERY | REVISE | R5 |
| 31 | PASS | FAIL | PASS | REVISE (jsonl) | the verse is Il. 13.85 verbatim: label it so (λέλυντο) |
| 32 | PASS | PASS | QUERY | REVISE | R6 |
| 33 | QUERY→PASS (R1) | QUERY | QUERY | REVISE | antecedent of τὸ δ᾽; σήματα πάντων reads as "out" under the brief's lexicon; the jsonl's "fastest serve" claim contradicts §1.2 (fastest serve 202 km/h at 3:35:36 was Federer's; Djokovic's was 199): correct the fact or the line |
| 34 | PASS | PASS | PASS | PASS (add κεν ἐξενάριξε Il. 21.280 to jsonl; R5 may change the verb) | |
| 35 | FAIL | PASS | FAIL | REVISE | εἰ μή οἱ βέλος ὠκὺ ἐτώσιον ἔκφυγε χειρός (both verifiers' fix; passes check_line) |
| 36 | PASS | PASS | QUERY | REVISE | name the agent; in Homeric idiom the line says the cast missed Federer, the reverse of the passing winner |
| 37 | PASS | PASS | PASS | PASS | |
| 38 | PASS | PASS | PASS | PASS (its simile continues in 39-40, which change) | |
| 39 | PASS | PASS | FAIL | REVISE | the lion must be the subject: keep the relative clause of Il. 20.164-171 (or another cited lion simile) and the tense sequence; the simile needs ≥3 lines and an apodosis |
| 40 | PASS | PASS | FAIL | REVISE | as 39 |
| 41 | QUERY→PASS (R1) | QUERY | PASS | REVISE | ἐπὶ δ᾽ ὄρνυτο (Homer's only pattern); ἔκφερε unelided is unattested: mark or change |
| 42 | PASS | PASS | FAIL | REVISE | the ὡς δ᾽ ὅτ᾽ simile needs its ὣς apodosis before the scales begin (Il. 22.165 model) |
| 43 | PASS | PASS | FAIL | REVISE | as 42 |
| 44 | PASS | PASS | PASS | PASS | |
| 45 | PASS | PASS | PASS | PASS (plan note: brief 2.5A asked for the two fates of death to become the two victories if a metrical equivalent exists; try δύο νίκας / δύο κῆρας with an attested genitive of the shape SLSSL SSLX, else keep and document) | |
| 46 | QUERY→PASS (R1) | FAIL | PASS | REVISE (jsonl; text if R3 changes the genitive) | relabel the name-substituted models |
| 47 | QUERY→PASS (R1) | PASS | PASS | PASS (jsonl: add Il. 8.72 / 22.212 for ἕλκε δὲ μέσσα λαβών· ῥέπε δ᾽) | |
| 48 | PASS | PASS | QUERY | REVISE | R3 |
| 49 | QUERY | QUERY | PASS | REVISE | R2, R4; ἀμύνετο at an unattested position |
| 50 | PASS | QUERY | QUERY | REVISE | R3, R4; αὖτε is never at 9-9.5 in Homer; περικλυτὸς αὖτε Νοβάκος has no Homeric pattern |
| 51 | PASS | FAIL | QUERY | REVISE | subject of προΐει must be clear; relabel βάλε δ᾽; R3 |
| 52 | PASS | FAIL | QUERY | REVISE | connective particle; relabel the shape model |
| 53 | PASS | PASS | PASS | PASS (R5 may change the verb) | |
| 54 | PASS | PASS | PASS | PASS | |
| 55 | PASS | QUERY | PASS | REVISE (jsonl) | relabel τέλος position |

Totals: PASS 24, REVISE 31 (of which jsonl-only: 1, 12, 19, 22, 31, 46, 55).

## Plan-conformance notes for v2 (not per-line failures, but brief requirements)
- At least two sound extended similes (≥3 lines, with apodosis): after 39-40 and 42-43 are repaired, the horse (16-19), lion and racing-horses similes should all be complete.
- The three expanded decisive points (brief §2.3: the 35-shot rally at 2:47:12, CP1/CP2 at 4:10:58/4:11:30, the 12-12 tie-break) must be identifiable in the verse and carry their clocks in the jsonl.
- Necessary enjambment is 8/55 (reviewer 9/55) against a target near a third: raise it where lines are rewritten.
- Epithet separation: ἀντίθεος (Djokovic) and ἰσόθεος φώς (Federer) both mean "godlike"; prefer distinct semantic fields (brief §4: craft for Federer, endurance for Djokovic).
- Line 45: see note above.
- Keep the jsonl field `quantity: metre-only` per brief §5.5 and record every check_line warning (τεύχεα, ἀκοστήσας, ἀργαλέῳ are in verbatim Homeric wording: say so).
