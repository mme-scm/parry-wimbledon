# Round 2 verdicts (draft v2, 60 lines)

Merged by the orchestrator from review/scansion_v2.md (PASS 59 / FAIL 1 / QUERY 0), review/provenance_v2.md (PASS 58 / QUERY 2 / FAIL 0) and review/philology_v2.md (PASS 55 / FAIL 3 / QUERY 2, plus poem-level query P1). A line passes only if all three pass it.

## Rulings
- **R9 Νοβῆκος.** The name takes the circumflex (η + consonant + -ος: 51 Homeric types, no acute). Round-1 ruling R3 and brief Addendum A1 are corrected accordingly (Addendum A2).
- **R10 Patronymic (P1): REVISE 23, 44, 51.** A Homeric patronymic is built on the father's name (Πηλεΐδης from Πηλεύς, Ἀμαρυγκεΐδης/Ἀμαρυγκείδην from Ἀμαρυγκεύς), so Ζοκοβεύς is the eponym (Đoko) and may not denote Novak. Replace Ζοκοβεύς / Ζοκοβῆος where they refer to Djokovic (23, 44, 51) by Ζοκοβείδης, its genitive (Ζοκοβείδαο or Ζοκοβείδεω with synizesis, on the Πηλεΐδαο / Πηληϊάδεω models: verify), Σέρβος, or Νοβῆκος, re-verifying the slot. Ζοκοβεύς may survive only as the father in a patronymic periphrasis (e.g. "son of Ζοκοβεύς"), if wanted. Record the decision in FOR_HUMAN.md.
- **R11 Counting (33, 55): REVISE.** δεύτερον αὖτις narrates one repeated action; the facts have two aces (points 357-358) and two Djokovic winners (420-421). Make the count match the facts with attested counting language (no δίς + verb; e.g. narrate both strokes, or δοιώ/δοιούς with a noun, or τρὶς μέν … where three occur), and record the point numbers in the jsonl.
- **R12 Subject (37): REVISE 36-37 minimally** so the attacker at "the fourth time" is fixed before the formula (a name, or a τρὶς μέν count naming him), since 36 now ends with Djokovic as subject.

## Per-line verdicts (all other lines PASS in all three reviews)
| n | scansion | provenance | philology | verdict | action |
|---|---|---|---|---|---|
| 23 | PASS | PASS | PASS | REVISE (R10) | Ζοκοβεύς → a Djokovic form per R10 |
| 24 | PASS | QUERY | PASS | REVISE (jsonl) | list δάμασεν as a movable-ν modification in `coinages`/`modifications` with Il. 3.332 ἔδυνεν / 11.19 ἔδυνε as the parallel |
| 33 | PASS | PASS | QUERY | REVISE (R11) | two aces |
| 36 | PASS | PASS | PASS | REVISE only if R12 needs it | |
| 37 | PASS | PASS | QUERY | REVISE (R12) | fix the attacker |
| 44 | PASS | QUERY | FAIL | REVISE | `ἔκφερε δ᾽ αὖ Ζοκοβεύς· ὃ δ᾽ ἐπέσσυτο κέρδεα εἰδώς` is the philologist's fix, but R10 removes Ζοκοβεύς: rebuild the line with a Djokovic form and a marked change of subject (ὃ δ᾽ ἐπέσσυτο, Il. 21.234, 21.601); cite Il. 3.200 for δ᾽ αὖ |
| 51 | PASS | PASS | PASS | REVISE (R10) | Ζοκοβῆος → per R10 |
| 55 | PASS | PASS | FAIL | REVISE | Νοβῆκος (R9); two winners (R11) |
| 56 | FAIL | PASS | PASS | REVISE | αὖθ᾽ Ἑλβέτιος |

Totals: PASS 52, REVISE 8 (24 jsonl-only). Also apply the small jsonl corrections listed in provenance_v2.md §8 (positions on 12/2, 22/1, 22/5, 31/2; mobility labels on 15 and 43; the Σέρβος δ᾽ αὖτ᾽ model Il. 17.304; the Ἀχαιῶν count 96; αὐτὰρ ὅ γ᾽ ἥρως is verse-final; Πηλεΐδης counts 24/51; better -είδης models Il. 4.517, Od. 15.52) and philology_v2.md §6 (stale line numbers, parallels, the gloss of 42).

## Plan-conformance note
Necessary enjambment is 10/60 (16.7%), nine of them in the proem and similes. Raise it inside the narrative where lines 33, 36-37, 44, 55 are rewritten, if it can be done without new faults; otherwise record the shortfall for the paper.
