# Critic review, phase "parry" (Phase 2b), v2

Reviewer: critic agent, 2026-10-11. Scope: the revision in commit acba030 (branch `claude/festive-feynman-e1z2rk`): `analysis/parry/plan.md`
(addendum 1 and its implementation notes), `report.md`, `results/`, `figures/fig9-10`, and the new scripts `p08_largeI.py`, `p09_h2_observed.py`,
`calibrate_chance.py`, `p10_h4_robust.py`, `p11_e1_loso.py`, `p12_rerun_check.py`, `make_report.py`; `review/critic_parry_v1.md` as the checklist.
Method: every number below was recomputed or looked up from the committed results files, from `git`, or from scratch scripts in
`/tmp/claude-0/.../scratchpad/` (`check_sameslam.py`, `check_sameslam_eq.py`; the confusion-adjustment and rate-ratio computations ran inline);
nothing under `analysis/` was modified. "My check" = computed in this session.

## Summary verdict

The revision does what the addendum says. The critical item (A1) and majors M1, M2, M3, M5, M6 are fixed in code and in the report; M4 is
recorded with a proxy validation; the twelve minors are fixed or recorded. The plan addendum (9a57c9b, 02:50:53) precedes the first new script
(a74dbea, 03:02:45) and the first new results (6ca7049, 03:04:29; large-I results 697ce10, 03:11:03); the whole pipeline was rerun afterwards
(result mtimes 03:40-04:49) and the 43 pre-registered outputs are identical to 476a088 (p12; my own sha256 pass: 32 of 33 CSVs byte-identical,
the 33rd differing only by the two declared post hoc columns). About 120 report numbers were compared with their results files, 0 mismatches.
No verdict sentence in `make_report.py` is a literal: each is gated by a rule in the docstring, and the only numeric literals left are design
constants (29.97 fps, 200 subsamples, 100,000 tokens).

What remains is interpretation, not arithmetic:

1. **Major.** "So most of the TV-only stock consists of strings the other registers also use, less often (a difference of frequency)" is derived
   from an asymmetric test (a 100,000-token TV sample against the *whole* 5.4-million-token press corpus) and omits the magnitude. Among the 300
   commonest TV-only strings (2,403 occurrences) the occurrence-weighted median TV/baseline rate ratio is 12 (quartiles 8-40); 90% of the
   press-attested strings occur less than once per 100,000 press tokens. Under a frequency-based definition of the formula that is the signature of
   a register-specific stock, not evidence against one. The sentence (and the STATUS headline built on it) deflates the finding.
2. **Major.** The slot composition of the TV-only stock (SCORE + STAT + OFFICIAL 23%, OTHER 29%) is a point estimate from a classifier whose
   OTHER class is a residual: propagating its output through the coder-A/B confusion matrices of Table 3.4 gives SCORE + STAT + OFFICIAL about
   38-39%, JUDGE 31-34% and OTHER 5%. The verdict word ("a minority") survives; the numbers do not.

Counts: 0 critical, 2 major, 9 minor, 12 checks passed. v1 items: 17 FIXED, 3 RECORDED, 0 STILL OPEN (table below).

## Status of the v1 items

| v1 | status | where, and what I verified |
|---|---|---|
| A1 n >= 3 artefact of S = 1,500 | FIXED | `p08_largeI.py`; Tables 2.A-2.G; Key bullets 1-2. 15.14 [14.29, 15.98] / 11.43 [10.70, 12.16] vs Cornell, 13.09 [11.85, 14.22] / 11.33 [10.36, 12.23] vs press, 20/20 targets, equal `largeI_summary.csv`; commentary-only 11.08 / 10.85 and raw 10.63 / 8.06 equal the file; S = 1,500 n >= 3 rows carry the "near-empty" label by rule (TV -> TV 1.02% < 2%). The old sentence is gone from the generator. |
| M1 H2 size is null-specific | FIXED | `p09_h2_observed.py`; Table 2.3 prints observed, shuffled and excess side by side; Key bullet "H2 at 1,500 tokens" bases the claim on observed 0.53 [0.12, 1.01] (15/20) and 3.10 [2.46, 3.84] (20/20), equal `h2_observed.csv` (0.530, 0.118-1.014; 3.097, 2.463-3.842); Table 2.3b gives the Cornell-null mechanism (54.4 shuffled types vs 16-32; Simpson 0.0156 vs 0.0096; `<name>` 5.59% vs 2.62%), all equal `shuffled_inventory_composition.csv` / `unigram_concentration.csv`. |
| M2 H1 decorative | FIXED | Key bullet retitled "a check that the pipeline detects collocation"; section 5 column "check only: 72% / 76%"; `h1_check.json` 0.717 / 0.756, press speakers 0.1086. The wording is consistent in the Key results, section 5 and the family bullet ("Rejected as pre-registered ... read with the post hoc checks"). |
| M3 calibration without chance/kappa | FIXED | `calibrate_chance.py`; Table 3.2 has chance precision, ceiling, precision - chance, chance recall, kappa with CI; Key bullet: kappa 0.13-0.22 (brief) / 0.11-0.22 (all), precision - chance 0.07-0.16, recall - chance 0.10-0.17, pool n >= 2 0.35 / 0.28 / 0.52 / 0.68 / 0.54 / 0.16 [0.14, 0.18]: all equal `calibration_chance.csv` (min kappa 0.130 (a)-or-(b) vs A and B; 0.111 content). 2019-vs-other now explained by base rate (0.43 vs 0.27; P - c 0.09 vs 0.06; chance 0.34 vs 0.21; median 26 vs 59 tokens) = `calibration_chance_groups.csv`. Span level 64 / 35 / 89 / 79 = `calibration_span_recall.csv`. "Weak proxy" is rule-gated (kappa < 0.40 everywhere; max 0.217). |
| M4 slot classifier validated in the wrong mode | RECORDED (partial) | `calibrate_chance.py` scores `classify_context` on coder spans (kappa 0.141 / 0.146) and on the 65 / 69 commentary references inside a coder span (0.354 / 0.388), and `p10` reruns H4b with the span-mode slot (p 0.0055). Limitation 6 and the Key "Slot classifier" bullet carry the caveat. The direct validation v1 asked for (coders label 200 masked reference windows) was not done; see minor 3. |
| M5 H4b not robust | FIXED | `p10_h4_robust.py`: three seeds at 100,000 (p 0.02327-0.02365, Holm 0.0465-0.0473), five variants (0.0646, 0.1232, 0.0097, 0.0055, 0.0443), LOSO 0.0104-0.0902 (17/20), per-stream 2/20 and 3/20, speaker-role confound in the Key bullet and limitation 5; verdict "not robust / inconclusive" read from `h4_verdicts.json`; H4a "rejected (robust)" (p 1e-5-5e-5; LOSO <= 0.0002). Section 5 column agrees. |
| M6 verdict literals | FIXED | Rules in the `make_report.py` docstring (ci_verdict, share_word, near-empty, weak-proxy, thrift file, composition, base-rate, conditional explanations); "2007-2015" from `corpus_facts.json`, "58% / 57%" from `calibration_slot_context.json`, "about a quarter" replaced by computed shares (6% / 36%). Residual: the thresholds were committed after the first outputs (minor 5). |
| m1 exploratory count | FIXED | 125 + 76 counted per p-value (I re-added the components). The report's "10 of 32 E2 p-values below 0.05" is right; v1's "4" counted the fewer-forms column only. Bonferroni: only `speed_unit` (1e-4 x 32); `along_the_line` 0.0018 x 32 = 0.058. |
| m2 stale corpus statements | FIXED | Section 1 reworded ("has since been corrected"); `run_all.sh` rerun on the corrected corpus; `p12` 43/43; Table 4.6 last row uses the stored field on 20 streams (rho 0.025, p 0.1891 = `h5_sensitivity_post_hoc.csv`). |
| m3 E1 rejects by construction | FIXED (wording), see minor 6 | Table 4.7 titled "rejects by construction"; `p11_e1_loso.py` adds the leave-one-stream-out inventory (7/7 slots p = 1e-4). |
| m4 unlogged deviations | FIXED | Section 7 items 3, 3b, 11; E2 per-slot sums (Table 4.9b, `e2_slot_sums.csv`); first-run outputs are still not kept (stated). |
| m5 LOW rows | FIXED | Dropped from Tables 3.1 and 3.3; the hyphenated-score note stands. |
| m6 coder independence | RECORDED | Section 3 (git trailers, same session, blindness by instruction) and limitation 10 ("task prompts are not recorded"). |
| m7 name normalisation | RECORDED | Section 1 gives hypocoristic counts (155 TV tokens, 1.28 / 0.25 / 0.10 per 1,000) and `<name>` shares (2.60 / 5.59 / 0.10%); hypocoristics were not added to the lexicon (pre-registered pipeline kept unchanged, as the addendum requires). |
| m8 "idiolect" | FIXED | "Stream-specific share", full-text 17.0% first, 28.4% at 1,500 second, with the length correlation labelled descriptive. |
| m9 H4a is stream-specificity | FIXED | "Streams (team, match and broadcaster together)". |
| m10 literals | FIXED | = M6. |
| m11 calibration halves | FIXED | Table 3.2b caption states the two designs and the 17- vs 18-stream pool. |
| m12 plan promises | FIXED | Table 2.11 and the Spearman line labelled descriptive / "2 exploratory p-values" and counted in m1. |

## Provenance and reproduction (verified from git)

* `review/critic_parry_v1.md` 02:40 -> addendum 9a57c9b 02:50:53 -> `p08`, `p09` a74dbea 03:02:45 -> p09 outputs 6ca7049 03:04:29 ->
  `calibrate_chance.py` 03:05:29, `p10`/`p11` 03:06:58 -> `p12` and the large-I results 697ce10 03:11:03 -> calibration/H4/E1 results and the new
  `make_report.py` 0deed2f 03:37:02 -> implementation notes in `plan.md` 3c634ca 04:33:25 -> end-to-end rerun (log mtimes 03:40-04:49) ->
  acba030 04:49:41 (regenerated `report.md`, `fig9`, `rerun_check.csv`). So the addendum's designs predate the project's own outputs; the
  addendum says, correctly, that it adopts the critic's numbers, which predate it; the implementation notes (including the verdict thresholds)
  postdate the first outputs and are labelled so.
* Results of the final rerun are byte-identical to the versions committed at 03:11-03:37 for every deterministic file (acba030 touched only
  figures, logs, `rerun_check.csv` and 4 lines of `make_report.py`), as the fixed seeds require.
* Working tree clean; `run_all.sh` lists steps 8-11 for the addendum; `log_p08` 573 s, `log_p10` and `log_p11` show the printed verdicts
  that the report reproduces.

## Major

### N1. "Mostly a difference of frequency" rests on an asymmetric test and omits the magnitude
Where: Key results bullet 2, last sentence; limitation 7; STATUS.md line 58 ("so the difference is mostly one of frequency").
The strict class asks whether a string is repeated in >= 2 utterances of the *whole* Cornell text (1.8x the sample) and the *whole* press
corpus (54x the sample), so "strict" means roughly "rate below 0.04 per 100,000 press tokens". That 81% of the TV-only tokens fail this bar
does not make them "strings the other registers also use" in any sense relevant to a formula. My check on `largeI_tvonly_types_pooled.csv`
(300 commonest TV-only strings, 2,403 occurrences in their targets, occurrence-weighted):

| quantity | value |
|---|---|
| occurrences in strings with zero occurrences in both whole baselines | 13.2% (strict 21.6%) |
| of the 260 strings with some baseline rate: TV / max(Cornell, press) rate ratio, median (quartiles; min) | 12.4 (8.1-40.5; 3.0) |
| TV / press ratio where press > 0: median; share >= 10 | 21.9; 74% |
| press rate among press-attested strings: median; share below 1 per 100,000 | 0.29 per 100,000; 90% |

A string at 0.3 per 100,000 is expected 0.3 times in a 100,000-token sample: it is not a repeated unit of that register at any sample size
the design uses. The implementation notes already concede that "'not a formula of a 100,000-token sample' and 'never repeated in 5.4 million
tokens' are far apart"; the Key results sentence then picks the far end. The symmetric statement is the one the design already gives: at equal
size, 9.6% of a target's tokens (10.3% in 2019) lie in n >= 3 strings repeated in TV and in neither baseline; those strings exist in the
baselines at typically 10-40 times lower rates.
Settle: add the occurrence-weighted rate-ratio distribution (and the share of TV-only tokens whose covering strings have expected count < 1 in
100,000 baseline tokens) to Table 2.D or 2.F, computed by `p08`; replace "a difference of frequency" with "register-specific by rate (typically
more than tenfold), not by absolute absence"; align STATUS.md. The `share_word(1 - strict_frac)` rule should then be driven by the rate-ratio
statistic rather than by the strict share.

### N2. The slot composition of the TV-only stock is biased by the classifier's residual OTHER class
Where: Key results bullet 2 ("a minority (23%) ... SHOT and JUDGE 46% and OTHER 29%"); Table 2.E; fig10; STATUS.md line 58.
The span-mode classifier is used with its kappa (0.49 / 0.48) attached, which is the right caveat, but the point estimates are reported as if
unbiased. Table 3.4 shows the bias is directional, not random: of coder A's spans, 71 of 275 SCORE, 31 of 165 STAT and 110 of 392 JUDGE go to
OTHER, and 82 of 392 JUDGE go to SHOT. My check: propagating the classifier's TV-only output (SCORE 9.3, OFFICIAL 4.6, SHOT 27.8, JUDGE 18.3,
STAT 8.9, CROWD 1.8, OTHER 29.3) through P(coder slot | classifier slot) from `calibration_slot_context_confusion.csv` (span mode):

| slot | classifier | adjusted, coder A | adjusted, coder B |
|---|---|---|---|
| SCORE | 9.3 | 19.2 | 17.0 |
| OFFICIAL | 4.6 | 4.8 | 4.9 |
| STAT | 8.9 | 13.7 | 17.2 |
| SCORE + STAT + OFFICIAL | 22.8 | 37.7 | 39.1 |
| SHOT | 27.8 | 20.4 | 21.8 |
| JUDGE | 18.3 | 33.7 | 30.7 |
| OTHER | 29.3 | 4.7 | 4.7 |

The adjustment assumes the confusion structure measured on coder formula spans transfers to TV-only n-gram occurrences, which is an assumption,
but it is the same assumption under which the kappa is quoted. The "minority" verdict holds either way (38% < 50%); "23%" and "OTHER 29%" do not,
and the direction of the bias is toward v1's reading (score, time and official frames are a larger part of the TV-only stock than the raw
numbers say). The regex check in the generator ("the classifier puts some score frames in OTHER, e.g. `games to two`, `six games to`") catches
2 of the 12 score-like OTHER strings among the top 300 (94 of 765 OTHER occurrences).
Settle: print the confusion-adjusted composition beside the raw one (one matrix product in `p08` or `make_report.py`), or have the two coders
label the slot of 100 TV-only occurrences; say in Table 2.E that OTHER is a residual class.

## Minor

**3. (M4 residue) The context-mode slot is still validated by proxy, and one of the printed figures is not a validation.** The 65 / 69
references' "truth" is the slot of the longest covering coder formula span, not a judgement of the reference's situation; at n = 65 a kappa of
0.35 has a 95% interval of roughly +-0.2. The coder-span row (kappa 0.14 / 0.15) compares the context mode with labels assigned from exactly
the words the context mode excludes, so it measures the design, not the error; printing it in the Key results and limitation 6 makes the slot
variable look worse than is known. Settle: as v1: 200 masked reference windows labelled by the coders; meanwhile give the reference-level kappa
with its bootstrap CI and drop the coder-span context row from the Key results.

**4. The umpire's game-score announcements are not in `official_mask_v2`, so "commentary-only" still contains them.** My check: all 7
occurrences of "leads by" in the 2019 transcript are umpire calls ("game, federer. federer leads by five games to one. second set."); the mask
has patterns for point scores, `advantage <name>`, `game set (and match) <name>`, challenges and `thank you`, but none for `<name> leads by N
games to M`. Hence `<name> leads by` (18 occurrences, 5 targets), `games to one`, `two games to`, `by two games to`, `five games to`, `six
games to` are counted as commentary in the commentary-only rows and as SCORE (not OFFICIAL) in Table 2.E. Size: a few tenths of a point of the
8.8% commentary-only TV-only share in 2019; larger for the OFFICIAL row. Settle: add the pattern to the mask (a logged change, since it is a
`common.py` function used by Phase 2) or report the commentary-only rows with the umpire's game announcements removed as a further variant.

**5. The verdict thresholds were fixed after the first outputs.** The composition rule (50%), the base-rate rule (half the raw difference),
the weak-proxy rule (0.40), the near-empty rule (2%) and the "twice" rule for the strict umpire share are in the implementation notes committed
at 04:33, after the results of 03:04-03:37. The report's "dated, committed before they were run" is true of the designs, not of these rules.
None of the thresholds is near its observed value (23 vs 50; 0.031 vs 0.082; 0.22 vs 0.40; 1.02 vs 2; 17.6 vs 11.6), so no verdict depends on
the choice. Settle: say "(the wording rules were fixed after the first outputs; no observed value lies within a factor of 1.5 of its threshold)".

**6. E1 with the leave-one-stream-out inventory still rejects in every slot for a reason that is not economy.** D below null at p = 1e-4 in
7 of 7 slots is what within-document burstiness produces in any collection (a match's player frames, a broadcaster's speed unit): the same test
on Cornell per-match updates or on press per-interviewee answers would reject too. The report's sentence ("streams reuse their own selection of
strings that other streams also use") is accurate; the section title "Formula economy per slot" and the word "economy" are not earned.
Settle: run the same statistic on the Cornell matches as a yardstick, or rename the quantity "stream-level reuse".

**7. Part of the TV-source advantage is same-slam and same-player sharing, which the baselines cannot have.** My check (`check_sameslam_eq.py`:
every source subsampled to 54,000 tokens, R = 3, 2b normalisation, n >= 3 coverage of the target): 2019 final: other 19 streams 23.0; without
the three other Wimbledon streams 22.9; without the five streams sharing a player 22.3; without both 21.8; Cornell 15.1; press 14.1. 2023 final:
24.8 / 24.0 / 23.7 / 22.9 / 15.0 / 13.5. So 15-19% of the TV-minus-baseline gap is same-slam or same-player sharing and the rest survives.
Limitation 8 says the differences do not say "why"; this is a cheap number that says part of it. Settle: one more source variant in `p08`
("other TV streams, different slam and no shared player", at a common reduced size) and a sentence in section 2.0.

**8. The TV source's five "samples" are not five samples.** A 100,000-token draw from a 109,000-119,000-token pool contains 84-92% of it, so
the R = 5 TV replicates are nearly identical while the press replicates are independent. Harmless for the estimates (the interval is over
targets), but "mean of 5 samples" in Table 2.A and fig9 suggests replication that does not exist for the TV column. Settle: state the overlap
in the caption, or draw the TV source at 80,000 tokens with the baselines matched.

**9. Two wording items.** (a) The report title still says "the tradition across broadcasts", which presupposes what section 2 tests; the
section titles are fine. (b) Revision-1 paragraph: "committed before they were run" needs "except the implementation notes" (minor 5).

**10. Normalisation artefacts among the TV-only strings.** `<name> <name> and`, `of <name> <name>`, `<name> with the` are TV-only partly because
full names (two `<name>` tokens) are a TV habit and Cornell/press rarely produce `<name> <name>` (3 of the top 40; 0.6-1.1 per 100,000 in
Cornell). Settle: mention beside Table 2.F; the raw-token rows already show the gap does not depend on it.

**11. Limitation 7's definition of TV-only is now right; limitation 6 repeats the 0.14 / 0.15 figure (minor 3).**

## Checks that passed

1. Report numbers equal results files: Key bullets 1-2 (coverage means, differences with CIs and target counts, commentary-only and raw rows,
   excess rows, TV-only / shared / cross-broadcast / strict shares for 2019, 2023, mean and range, composition by slot, umpire-mask shares 5.8 /
   18.1 / 17.2 / 17.6, top-40 count 20 of 40), H1 bullet, H2 bullet, calibration bullet, slot-classifier bullet, H4a/H4b/H5 bullets, E2 and E1
   bullets, section 5 table, Tables 2.A, 2.B (10 rows), 2.C (2 rows), 2.D, 2.E, 2.F (40 rows), 2.3, 2.3b, 3.2 (4 rows), 3.2b, 3.2c, 3.4, 4.4b,
   4.6, 4.7b, 4.9b: about 120 values, 0 mismatches. Holm by hand: 0.02364 x 2 = 0.0473; 0.0646 x 2 = 0.129; 0.0055 x 2 = 0.011.
2. Large-I comparison is fair on size: every source is 100,000 tokens of whole utterances, the same tokeniser and 2b normalisation
   (`norm_tokens` with the TV lexicon plus per-document extra names for Cornell and press) and the same inventory rule; the TV inventory is the
   smallest (18,670 types vs Cornell 31,559 and press 20,479), so the TV advantage is not an inventory-size effect; raw tokens give 10.63 / 8.06
   at n >= 3; the commentary-only variant removes the masked tokens from numerator and denominator for all sources alike.
3. Pooling 358 press speakers does not handicap the press baseline: single-speaker sources at 54,000 tokens (Federer 13.9, Djokovic 13.9 at
   n >= 3 for the 2019 target; 13.3 / 12.8 for 2023) cover no more than the pooled press (14.1 / 13.5).
4. The TV-only definition is the conservative one (a token is TV-only only if no covering n >= 3 occurrence is in either baseline inventory);
   "cross-broadcast" is correctly a stricter subset (8.9 of 9.6).
5. `p09`'s vectorised vertex bootstrap is asserted equal to `lib2b.vertex_boot_vs_baseline` on one configuration; the observed/excess columns
   of Table 2.3 agree with `h2_observed.csv`, and the excess column agrees with section 5 to the second decimal as the caption says.
6. `calibrate_chance.py`: chance precision = coder share, chance recall = auto share, ceiling = min(1, c/a) are the right quantities; kappa
   formula from the 2x2 counts is standard; the circular-shift null for span recall keeps the automatic positive share per utterance.
7. `p10`: variants reuse `p05_thrift.h4` unchanged with `slot_key` switched; Holm under substitution recomputes the seven-test family; the
   verdict rule excludes LOSO (which changes the population), as the addendum says; MC SE sqrt(p(1-p)/N) is right.
8. `p11`: the leave-one-stream-out inventory is identified on the other 19 streams only; the E2 per-slot null is the sum of independent
   within-class permutations, as promised in plan section 9.
9. `p12`: compares every results file tracked at 476a088 except logs; JSON compared without run-time keys; `refexpr_pool_tokens.csv` on its
   original 19 columns. My independent sha256 pass agrees.
10. E2 count: 10 of 32 p-values below 0.05 (both columns), Bonferroni leaves `speed_unit` only; the report is right and v1's "4" was one column.
11. Figures 9 and 10 reproduce Tables 2.A and 2.E (dots per target; stacked shares); fig9's regenerated bytes differ only by matplotlib metadata.
12. ASR: the TV-only lists contain no recognisable ASR artefacts (the commonest are umpire, score, time and shot frames); limitation 2 correctly
    notes that ASR noise biases TV-minus-baseline toward zero (sources and targets both noisy in TV-TV, target only in baseline-TV).

## Wording audit: the Parry-Lord bearing in both directions

* A commentary-specific stock at the n >= 3 level: stated at the right strength in bullet 1 (observed differences, every target, equal
  sizes, commentary-only and raw sensitivities) and understated in bullet 2's last sentence (N1). After N1 and N2 the honest summary is: about
  a tenth of a broadcast's tokens lie in three-word-or-longer strings repeated across broadcasts and not repeated in equal-size samples of the
  other registers; those strings occur in the other registers at typically 10-40 times lower rates; by the classifier a quarter, and after
  correcting its confusions about two-fifths, of that stock is the official register and score/time frames, the rest shot description and
  judgement.
* Automatic measures as weak proxies: right strength (kappa, chance, ceiling, span-level recall all shown; "weak proxy" rule-gated).
* Team-level thrift robust: right strength, with the stream/team/broadcaster confound and the speaker-role confound named.
* Slot thrift inconclusive: right strength ("not robust / inconclusive", p range, variants, attenuation by slot noise); the per-slot
  attribution of Table 4.5b is kept out of the Key results, correctly.
* Extension: the report says "no association was detected ... minimum detectable rho about 0.053", not "absent"; that is the right strength.
* No Homeric claim is made; "Parryan pattern of one form per slot" is tested and found absent in 18 of 20 streams, correctly stated.

## Shortest path before the paper

1. N1: add the rate-ratio statistic to `p08` and rewrite the last sentence of bullet 2 and STATUS.md.
2. N2: print the confusion-adjusted composition beside Table 2.E; call OTHER a residual class.
3. Minor 4 and 7: one mask pattern (logged) and one source variant in `p08`; minor 5 and 9: two sentences.
4. Minor 3 remains the one open validation (coder-labelled reference slots); if not done, keep H4b's reading as is and remove the 0.14 / 0.15
   row from the Key results.
