# Critic review, phase "analysis", v2

Reviewer: critic agent, 2026-10-07. Second adversarial pass after the revision round (formulas: commits 282fd31, 63e9a90,
6c5d6eb; metre: 3c38cd7, fa5d3d4; orchestrator: 1d5180e `analysis/limitations.md`). Read: both `plan.md` addenda, both
`report.md`, `analysis/limitations.md`, `results/deviations.json`, the revised scripts (`f03`, `f04b`, `f07`, `f08`, `f09`,
`common.official_mask_v2`, `refexpr.umpire_rule`, `f06`, `s04b_posthoc.py`), `composition/brief.md` sections 1.10 and 3,
and `STATUS.md`. Every report number quoted below was compared with the results file it cites; git history was used to
check the order of addenda, scripts and results; replicate-level checks were run from scratch scripts in the scratchpad.
Nothing under `analysis/` was modified.

## Summary verdict

The revision does what the addenda say it does, and I could not find a number in either report or in `limitations.md`
that disagrees with `results/`. The critical item of v1 (C1/R1 printed as a rejection in the opposite direction) is gone:
C1/R1 are "indeterminate pending a WER estimate" in the Key results, in Table 4, in `confirmatory.csv` and in
`limitations.md`. R = 1000 was actually run (3,000 D5(i) rows, 1,000 distinct seeds per corpus) and the first 200
replicates reproduce v1 to the sixth decimal (2,940 values, 0 mismatches). The Cornell identification size is now the
realised one everywhere it appears (median 65,444; 56,574-76,850). Umpire-pattern references are excluded in the
primary C4/C5/R4/R5 (31 + 31 tokens; verified in `thrift_tests.csv`, `extension.csv`, `refexpr_summary.json`). The
`official` flag fires on score calls (five of the pre-specified top 10 flagged True, shares 0.925-1.000). Section 8 cites
only the five records in `hand/kuiper_verification.tsv`, and the auctioneer placement and the "continuous load" inference
are gone. The metre verdict and Limitation 2 are now consistent (the CI bounds are stated "for the effect as measured" and
are placed beside simulated MDEs that exceed them). The MDE simulations are sensibly implemented and report their own size
at zero effect (0.022-0.055 against nominal 0.025/0.05).

What remains is wording that could still travel into the paper: one robustness sentence in `limitations.md` that is true
for the confirmatory split-half design but not for the exploratory held-out design, a C2 verdict string that asserts "not
a medium effect" instead of "not attributable to medium", the revised C4/C5 carrying the bare label "confirmatory", and
one wrong range in the composition brief. No critical issue; 1 major; 11 minor; 14 v1 items FIXED, 5 RECORDED, 0 STILL OPEN.

## 1. Status of the v1 items

| v1 | status | evidence (verified, not taken from the addenda) |
|---|---|---|
| A1 C1/R1 reported as a rejection in the opposite direction | FIXED | Key results bullet 3, Table 4 rows C1/R1, `confirmatory.csv` `verdict` = "indeterminate pending a WER estimate", `limitations.md` item 2. "OPPOSITE" removed; the "M asymmetry favours TV" sentence withdrawn (section 9.1 iv). Crossing points computed: e* = 0.1218 (held-out) and 0.1424 (split-half) in `asr_noise_summary.json["crossings"]`, printed as 0.122 / 0.142. |
| B1 p at floor; C2 Holm 0.0498 an artefact of R | FIXED | `density_medium.csv` D5(i) (a) family rows have `replicates` = 1000; `medium_replicates.csv` has 1,000 rows per corpus with 1,000 distinct seeds; the v1 seeds are the first 200 in the same order and all 2,940 shared values are identical. C2 interval [-22.1, -16.3] from `diff_lo/diff_hi`; `p_floor` = 2/1001 = 0.001998 and `p_at_floor` = True; the report says so in words. |
| B2 Cornell I = 103,675 stated, actually ~65k | FIXED | `density_medium_meta.json` and `deviations.json` carry min/median/max 56,574 / 65,444.5 / 76,850; Table 3.2, Table 3.8 caption and Table 4.2 print "I median 65,444". Post hoc D5(ii-b) (I = 103,706, M from a median of 29 groups) added and its two simultaneous changes stated. |
| B3 measure is repetition, not Parry's formula | RECORDED (partly fixed) | Renamed "repeated-n-gram coverage" throughout; n >= 3 / n >= 4 / content / content n >= 3 with shuffled floors in Tables K, 3.1b, 3.2b, 3.2c; `limitations.md` item 1 and report Limitation 4 say the measure orders texts by repetition rate. The syntax-preserving baseline suggested in v1 was not built; recorded as a limitation. |
| B4 auctioneer placement without auctioneer data | FIXED | Section 8 "Degree" bullet: "no auctioneer, race-call or other sportscaster corpus was measured ... cannot be placed"; "Performance constraint" bullet ends "say nothing either way". Every citation in section 8 matches a row of `hand/kuiper_verification.tsv`; the Kuiper and Austin chapter is marked [unverified]. |
| B5 metre bound contradicts Limitation 2 | FIXED | Summary now: "These bounds hold for the effect as measured ... the true effect could be larger than these bounds"; MDEs from `posthoc_mde.csv` (T2 5.3/6.5 pp, T3 0.066/0.081, T4 8.3/10.6 pp; 2023 8.2/9.7, 0.081/0.096) and the misattribution scenario (10.8 pp, 0.135, > 19.8 pp) all equal the file. Plan section 7's "unless the CI is narrow" clause is explicitly not invoked. |
| B6 thrift/extension mix speakers, no power | FIXED + RECORDED | `refexpr.umpire_rule` and `f06` `TOKEN_SETS`; `extension.csv` `umpire_pattern_tokens_excluded` 16 + 15 (2019) and 19 + 12 (2023) = 31 each, matching `refexpr_summary.json` counts (mr 11, game 9, leads 8, advantage 2, challenging 1). MDEs in Table 4.3 equal `mde_summary.json`. Clip-level context recorded in `limitations.md` item 5 and report Limitation 2. |
| B7 medium ordering is a corpus contrast | FIXED (wording) + RECORDED | Key results bullet 2, Table 3.2 caption, C2 verdict, section 8, Limitation 3, `limitations.md` item 3. See M1 and m2 below for two residual sentences. |
| C1 Duggan unverified | FIXED | `hand/duggan_verification.tsv`: Open Library OL5224003M, Crossref 10.2307/jj.8085370 and 10.2307/2851011; criterion wording marked [unverified] in section 1. |
| C2 `thank you` and non-alternating frames | RECORDED | Table 2.5 has a `top filler %` column; "84 of the 231 systems" reproduces from `systems_2019.tsv` (84). `thank you` is masked in S5b (4.6% of tokens) and flagged in the top-10 lists, but stays in the pre-registered (a) inventory, as stated in Table 2.4. |
| C3 C3a wrong interval; iid permutations | RECORDED + checked | Section 9.2 and `limitations.md` item 6 state it; Table 4.4 circular-shift nulls (299/226 shifts) equal `circular_shift_tests.json`; no p changes side of 0.05. C3a is still printed first in the family (it is pre-registered), with the caveat. |
| C4 metre T1 partly between-category | FIXED | PH3: within-game rho 0.166 [0.046, 0.280], p = 0.0099 (2019); 0.125 [-0.007, 0.252] (2023); medians 109 vs 14 tokens; all equal `posthoc.json`. Summary wording qualified. |
| C5 metre base share carries the headline | FIXED | R2 (0.149) and the R2 estimates for T2-T4 are in the Summary beside the base. |
| C6 2023 not a comparable-range replication | FIXED | Section 8 renamed; PH4 ranges (15-117 vs 14-305 s; 1 vs 27 changeover units) and the 2019 restriction (348 units, T2 -2.9 pp, T3 -0.028) equal `posthoc.json` / `posthoc_sensitivity.csv`. |
| C7 hand-entered literals | FIXED | `make_report.py` reads `press_years` and `asr_proxy.json` (lines 239, 911); `s06_make_report.py` reads `asr['n_words']`, `asr['total_per_1000_words']`, `L_BLOCK`, `B_BOOT`. No literal result found by grep. |
| C8 noise rows R = 10 | FIXED | `R_HELD = 50` in `f04b`; `asr_noise_summary.json` cells have 50 replicates; Table 3.8 caption explains why the TV held-out range has a different meaning. |
| C9 official flag never fires on score calls | FIXED | `top10_for_brief.csv`: `<NUM> 15` True (0.925), `15 <NUM>`, `<NUM> 30`, `40 <NUM>`, `30 <NUM>` True (1.000); `commentary_only` list excludes them. |

## 2. Checks that passed

1. Report numbers equal results files. Formulas: Table K (20 values), Table 3.1b (all 25 base/n3/n4/content rows for 2019), Table 3.2 (16 values incl. I sizes and group counts), Table 3.2c, Table 3.8 (30 cells and all four crossings), Table 4 (every estimate, interval, p, p_floor, Holm and MDE for C1-R5 and the four `_all_tokens` rows), Table 4.3 (all 8 rows against `mde_summary.json`), Table 4.4 (against `circular_shift_tests.json`), Tables 6.1-6.3 (spot-checked 12 rows), Tables 7.1a/b, 7.2a, section 2 counts (1194 / 1503 / 1113 types; 919; 467; 231 systems; 84 of 231). Metre: Summary and section 10 against `confirmatory_*.csv`, `posthoc_mde.csv`, `posthoc_sensitivity.csv`, `posthoc.json`, `posthoc_umpire_check.json` (about 50 values). `limitations.md`: every number in items 2, 4, 5, 6, 7, 8, 10 equals the file it comes from (22/1,000; 12.2%; 6.4-7.2; 5.3-6.5; 0.30-0.42; 0.17-0.22; 0.066-0.081; 8.3-10.6; 33/40; 3-5%; 15-117 / 14-305; 0.166 [0.046, 0.280]; 17.7% from `corpus/README.md` section 4).
2. Order in git. Metre addendum 3c38cd7 (14:28:59) precedes `s04b_posthoc.py` (mtime 14:31) and the post hoc results (first committed 282fd31, 14:48:18); the metre plan is byte-identical since 3c38cd7 and nothing above either addendum was edited (no deletions in `git diff` from the pre-registration commits). The metre confirmatory, robustness and exploratory results files are byte-identical to the v1 commit 4b60443; `units_*.csv` only gained the U/R1U columns. Formulas plan: byte-identical since 282fd31; no edits above the addenda. See m3 for what the formulas addendum's timing does and does not show.
3. Rerun determinism. Between the WIP run (63e9a90) and the final run (6c5d6eb) only the n3 CI bounds of `coverage_family.csv` changed (by <= 0.03 pp); the cause is the seed-line edit in `f03` committed in 63e9a90 (n3 rows now reuse the S6 seeds), not nondeterminism. HEAD results correspond to HEAD code; `report.md` equals the final run.
4. The MDE simulations (formulas `f09`, metre `s04b`) use the test statistics and permutation/shift schemes as run, keep N and group sizes, report size at zero effect (0.0325-0.055 for C3-C5; 0.022-0.025 for T2-T4 at alpha 0.05), interpolate at 80% power, and state their effect models in docstrings and in the addenda. Metre: the re-implementation check asserts equality with `confirmatory_*.csv` before planting effects. The T3 copula preserves the syllable distribution exactly; the T2/T4 plant is clipped to [0, n_tok].
5. Holm recomputed by hand for the revised 2019 family (C5: rank 3 of 6, 4 x 0.1295 = 0.518) and the sensitivity family (C5_all_tokens: 4 x 0.1173 = 0.469).
6. Consistency of the brief with the revised results (`composition/brief.md`, written 14:47, before the formulas rerun): every count I compared is unchanged by the rerun and equals the current CSVs: score-call systems 40/36, 30/29, 28/22, 19/19, 19/15, pool 16-17, median time after 25-30 s, pressure 0-14%; `game <NAME>` 9/9 (7/2, pool 9); `<NAME> leads by` 7/7, `by <_> games to` 9/9 with 78% inside official patterns (0.778, present already in v1 because S5 covered "leads by"); `the <_> set` 27/21 with the six fillers; `in the <_> set` 9/9; `the first set` 10/8; `in <_> fifth` 9/9 (6/3; 44%); `a little bit` 15/14; `a little` 24/22; `the <_> serve` 8/8 with its fillers; `<NUM> minutes` 14/12; `the match` 17/17; `mr <NAME>` 11/11 (6/5, pool 2); and all 17 epithet/name counts of section 1.10 equal `refexpr_inventory.csv`. The brief's statement that the n >= 2 lists are "dominated by score calls" and its umpire attributions for `game <NAME>` and `mr <NAME>` agree with the new flag and with `refexpr_summary.json`. Section 7 of the report is still the top-10 section the brief cites. Exception: m4.

## 3. Remaining and new issues

### Critical

None.

### Major

**M1. `limitations.md` item 3 overstates the noise robustness of the TV-vs-Cornell difference.** "The sign is stable under
every noise level tried and under subsampling to matched size, so a difference between the two corpora is established."
This holds for the confirmatory split-half design (Cornell 23.1 [20.7, 25.6] vs TV 16.3 at e = 0.15). In the held-out
design the Cornell mean at e = 0.15 is 55.6 [53.6, 57.9] against TV 55.0 [53.1, 57.0]: the ranges overlap
(`asr_noise_summary.json` `heldout|text_cornell` `e_first_grid_range_overlap` = 0.15) and a linear extrapolation of the
means (60.6 at 0.10, 55.6 at 0.15) crosses 55.0 at about e = 0.156. Table 3.8's caption in the report says this correctly;
the limitations file, which is what the paper will cite, does not. Settle: name the design ("in the split-half design at
matched size"), or extend the noise grid to e = 0.20 and report e* for held-out Cornell as for press. Rank major because
this is the one positive finding that survives the revision and its robustness statement must be exact.

### Minor

**m1. Revised C4/C5/R4/R5 carry the bare label "confirmatory".** `confirmatory.csv` `status` = "confirmatory" and Table 4
list the commentary-only rows as the confirmatory tests, although the token set was changed after the v1 results were
seen (addendum 2 item 6 calls it a DEVIATION). Both token sets are null, so nothing turns on it, but a reader of the CSV
alone cannot see the deviation. Settle: `status` = "confirmatory (deviation: token set revised post hoc; pre-registered
set in *_all_tokens)".

**m2. C2 verdict string asserts a negative it cannot support.** "corpus difference: 95% interval of differences excludes 0
(not a medium effect)" (`f07` line building `verdict`; Key results; Table 4). The data do not show it is *not* a medium
effect; they show it cannot be *attributed* to medium. Settle: "(not attributable to medium: matches, outlet, period,
transcription and segmentation differ)".

**m3. The formulas addendum 2 is a log, not a pre-registration, and should say so.** It was committed in 282fd31
(14:48:18) together with the first results of the analyses it describes (`mde_summary.json`, `circular_shift_tests.json`,
`power_curves.csv`, the commentary-only `thrift_tests.csv` / `extension.csv`, `top10_for_brief.csv`, `coverage_family.csv`),
and the post hoc scripts predate the addendum text (`f05` 14:30, `f06` 14:31, `f09` 14:35, `common.py` 14:40 vs
`plan.md` 14:44). The addendum does not claim to precede the runs and labels every item post hoc or DEVIATION, so nothing
is presented as pre-registered; but the report's "every change is logged in plan.md, addendum 2" reads like the metre
addendum, which was committed before its analyses (3c38cd7 14:28:59 < `s04b` 14:31). Settle: one sentence in addendum 2:
"written alongside the revised scripts and committed with their first outputs; not a pre-registration".

**m4. One wrong range and one unverifiable attribution in the brief.** Section 3.8: "27-38% at pressure points" for the
four name-verb frames; `top10_for_brief_n3.csv` gives 0.273, 0.200, 0.375, 0.375, so "20-38%". Section 3.1: "the systems
are the umpire's calls repeated by the commentator" asserts speaker attribution that the report says cannot be made
(section 1: "the transcript does not tell them apart"). Settle: correct the range; reword to "score calls, said by the
umpire and often echoed by the commentators". Also, section 3.5 presents `in <_> fifth` (fillers the:6, this:3; top filler
67%) as a system without the report's new caveat that such frames barely alternate.

**m5. `reject_at_0.05` = True for C1/R1 in `confirmatory.csv`, and Table 4 prints their Holm p (0.0012, 0.0010).**
The verdict column overrides, and the section intro says Holm "is informative only for the permutation tests C3-C5", but
a reader of the CSV sees a rejection next to "indeterminate". Settle: blank `p_holm` and `reject_at_0.05` for C1/R1/C2 or
rename the column `holm_on_uncalibrated_p`.

**m6. Two values for the same quantity.** Table 3.8's e = 0 column (its own 50 replicates: TV 16.3, Cornell 35.2, press
24.7) differs in the last digit from Table 3.2 (1,000 replicates: 16.2, 35.3, 24.6), and the crossing e* uses 16.3 as the
TV reference. Settle: compute the split-half crossing against the Table 3.2 means, or say in the caption that the e = 0
column is a 50-replicate re-estimate.

**m7. The metre attenuation factor is a property of the mixing model, not of the data.** "The true effect needed grows:
at misattribution 0.50 it is 1.86-2.05 times the true MDE" follows almost identically from delta' = (1 - m) delta +
(m/2)(delta_prev + delta_next) with lag-1 autocorrelation of A near 0 (-0.02 / 0.16), i.e. a factor of about 1/(1 - m).
The report labels the scenarios "illustrative, not estimates", which is right; the unknown that matters is m itself.
Settle: say that the factor is analytic, and bound m from the corpus: the 55 clips whose text repeats a clip ending a
median 17.2 s earlier show that a window spans at least that gap plus a clip, which gives a data-based lower bound on
the share of text belonging to neighbouring intervals.

**m8. "The shift-null test is calibrated" (metre 10.1) is a self-consistency check.** Size at zero effect is measured
under the same shifted-timing construction the test uses, so it shows internal consistency, not calibration against the
true timing process. Settle: "internally consistent (size equals nominal under its own null)".

**m9. The two analyses use different umpire masks.** Metre variant U masks `thank you` (+please/players), `mr` + next
token and `game` + a finalist's name; the formulas mask v2 also covers `advantage <name>`, `leads by ... games to`,
challenge announcements, game-set calls and point-score calls. U removes 99 tokens in 2019, almost all `thank you`. Both
are sensitivities and both are null, so no conclusion changes; the paper should not describe them as the same check.

**m10. `limitations.md` "Fixed" list mislabels one item.** "C2 (official flag fixed)" describes v1's C9; v1's C2
(`thank you` as a commentary formula; non-alternating frames) is the partly fixed one. Cosmetic, but the paper's
revision note will copy it.

**m11. STATUS.md does not record the revision round.** No entry for critic v1, the revision commits, the orchestrator's
validation of the revisions, or `limitations.md`; "Open issues" is empty; the phase table says Phase 3 NOT STARTED while
the decisions list says the brief was accepted and composer v1 started. CLAUDE.md assigns this log to the orchestrator.
Settle: add the validation figures (e.g. the replicate-reproduction check, the identical metre confirmatory files) and
the open items (WER, same-match written text).

## 4. Overclaim audit (question 3)

* "Formulaic density" appears only in quotation marks and only when related to Duggan; the measure is named
  repeated-n-gram coverage in both reports' headlines. The metre report keeps "formula share" for its pool n-grams and
  says the definition is specific to that analysis; the paper should use "pool-repeated n-gram share" to avoid the
  Parry sense.
* Homer analogy: section 8 ("Degree", "Performance constraint") and metre section 11 claim nothing the data do not
  show; the Duggan comparison is labelled an analogy and its criterion [unverified].
* Medium: every TV/Cornell/press comparison I found is labelled a corpus contrast, except the two sentences in M1 and m2.
* Null results: every "not rejected" is paired with an MDE, and the Key results say "not detected, not evidence of
  absence"; the metre report says the same with the attenuation caveat. No null is read as support for H0.

## 5. Shortest path before the paper

1. Reword `limitations.md` item 3 (M1) and the C2 verdict string (m2); blank the Holm/reject cells for C1/R1/C2 (m5).
2. Label the revised C4/C5 rows as a deviation in `confirmatory.csv` (m1); add the one-sentence timing note to
   addendum 2 (m3).
3. Fix "27-38%" and the umpire-attribution sentence in the brief (m4).
4. Record the revision round and open items in STATUS.md (m11).
