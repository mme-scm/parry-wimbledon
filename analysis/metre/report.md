# Metre analysis: is the time between points a frame for commentary formulas?

All numbers below are read from `analysis/metre/results/` by `s06_make_report.py`; rerun everything with
`bash analysis/metre/run_all.sh`. The analysis plan (`plan.md`) was committed **before any test script was written or run**
(commit message "metre: pre-registered analysis plan"). Everything not in the plan is labelled **EXPLORATORY** or **POST HOC**.
**Revision 1** follows the critic review `review/critic_analysis_v1.md`. Every change is logged in `plan.md`, Addendum 1, as
a post hoc change. The new analyses are in section 10, and the confirmatory results are unchanged.

## 1. Summary

* **H1 had to be re-specified before testing, and it was.** There is no audio, no word time and no speaker label, so intonation units,
  pitch resets, IU-onset phase in the strike cycle, rally-internal speech and the production speed of formulas **cannot be measured**.
  The tested hypothesis (H1') takes as frame the **interval between points** (point plus dead-ball time up to the next first serve, `A`)
  and as unit the **clip-level transcript aggregated per point**. The strike-level version of H1 remains **untested**.
* **Precondition (T1).** In the 2019 final the number of tokens attached to a point rises with the time available:
  Spearman rho = 0.248 [0.136, 0.359], shift-null p = 0.0050 (Holm 0.0198); about
  0.53 [0.29, 0.90] extra tokens per extra second (OLS slope, secondary; shift-null
  p = 0.0050). Part of this association lies **between** dead-ball categories: changeover/set-break units carry a
  median of 109 tokens against 14 within games. **Within** within-game units, rho =
  0.166 [0.046, 0.280] (n = 290, shift-null p = 0.0099; POST HOC, section 10.2), which is weaker but its CI excludes 0. In the held-out 2023 final,
  rho = 0.163 [0.030, 0.285] (Holm p = 0.0953, **not significant**). Within games there it is
  0.125 [-0.007, 0.252] (n = 197, shift-null p = 0.1016), and the association is carried by points that have an extra fault clip (EXPLORATORY X7: rho =
  0.051 among single-clip units).
  **T1 is consistent with H0 as well as with H1'**: a constant speech rate inside a text window that spans the interval
  produces it. It shows only that clip-level text carries some point-level timing information, and it is not evidence for a frame (section 2).
* **The discriminating predictions were not observed.** Formula share in short- minus long-interval units (T2): -2.9 percentage
  points (pp) [-6.0, +1.3] in 2019, -4.3 pp [-9.6, +1.1] in 2023 (H1' predicted > 0; both
  point estimates have the opposite sign). Syllables of formulaic strings against available time (T3): rho = -0.040
  [-0.088, 0.009] (2019), 0.021 [-0.025, 0.065] (2023) (H1' predicted > 0). Formula share within games
  minus after changeovers/set breaks (T4, 2019 only): +1.0 pp [-2.5, +4.4] (H1' predicted > 0).
  None is significant after Holm correction. The base formula share (0.644 in 2019) is carried by common
  bigrams such as 'in the'. With the **strict** definition (R2: n >= 3, >= 5 pool occurrences in >= 3 pool streams; share
  0.149), the 2019 estimates are T2 -0.7 pp [-3.5, +3.3],
  T3 rho = -0.057 [-0.158, 0.048] and T4 +0.5 pp [-2.7, +3.6].
  With umpire-pattern tokens removed (POST HOC, section 10.5), no umpire-masked estimate has a CI excluding 0.
* **Verdict under the pre-registered rules (plan section 7): H1' is NOT SUPPORTED** in the 2019 final.
  No confirmatory effect is Holm-significant in the direction opposite to H1 either.
  The held-out 2023 final is **not a comparable-range replication**. The 2023 source video omits the changeovers, so the analysed 2023 intervals span
  `A` = 15-117 s, with 1 changeover unit and 2 units over 100 s. In 2019 the range is
  14-305 s, with 27 changeover units and 13 over 100 s. In 2023, T4 is not testable,
  and T2 and T3 are null over the narrower range (no Holm-significant result).
* **What "not detected" can and cannot mean (revised after the critic review: POST HOC, plan Addendum 1, PH1-PH2).**
  The 2019 95% CIs exclude a short-minus-long excess in formula share above +1.3 pp (T2), a syllable-time
  correlation above rho = 0.009 (T3) and a within-game minus changeover excess above +4.4 pp (T4).
  These bounds hold **for the effect as measured**: clip-level text attributed to points, ASR text, and the formula
  definition of section 4. They do not bound the true effect. The text window is undocumented, so part of each unit's
  text belongs to neighbouring intervals, and ASR errors break n-gram matches. Both attenuate a true effect towards 0, so
  **the true effect could be larger than these bounds**, by an unknown factor. The minimum detectable effects (MDE; 80%
  power, simulated at the observed N with the shift-null test, at alpha = 0.05 / at the first Holm step alpha/m) are
  2019: T2 5.3 pp / 6.5 pp, T3 rho = 0.066 / 0.081, T4 8.3 pp / 10.6 pp; 2023: T2 8.2 pp / 9.7 pp, T3 rho = 0.081 / 0.096 (section 10.1).
  All three 2019 CI bounds lie below the MDEs, because the point estimates are near or below 0.
  In an illustrative scenario where half of each unit's text comes from the neighbouring intervals, the true effects needed
  at alpha = 0.05 in 2019 rise to T2 10.8 pp, T3 rho = 0.135, T4 > 19.8 pp (beyond the simulated range). "Not detected" therefore means that measured effects as large as the MDEs
  would probably have been found and are excluded by the 2019 CIs. It does not exclude smaller true effects, effects hidden by
  attenuation, or a frame at the strike level, which this corpus cannot reach.

## 2. Hypotheses as tested (re-specification, from plan.md)

Original H1 (brief): during rallies, the intervals between strikes act as a metrical frame; IU boundaries align with strikes; formula
length is constrained by the time available; between points, composition is freer. H0: no alignment beyond what speech rate and
pause distribution predict.

**Why re-specified.** The corpus (corpus/README.md sections 0, 4, 6, 8) consists of WhisperX transcripts attached to TennisVL rally clips
(median clip 6.2 s in 2019, starting a median 1.04 s before the
first hit and ending 2.0 s after the last), with no audio, no word timestamps and no speaker labels.
A clip's text window is undocumented and reaches beyond the clip: 55 clips repeat the text of an earlier
clip that ended a median 17.2 s before they start (2023:
26 clips, 17.2 s), and score calls in a clip are
usually the score *after* its point (README section 4). Speech during rallies cannot therefore be separated from speech between points, and the corpus cannot show
how much speech occurs during rallies. As the brief requires in that case, the frame was moved to the **interval between points**.

**H1' (tested).** The time available around a point, `A` = serve-to-serve cycle of the point (PBP match clock: rally + dead-ball time to
the next first serve; for second-serve points also the fault interval), is a frame the commentary is fitted to. Predictions: P1 more
text with more time; P2 higher formula share when time is short; P3 longer formulas (in syllables) when time is longer; P4 lower formula
share in changeover/set-break intervals than within games; P5 (descriptive) a flat speech-rate ceiling.
**H0.** Speech at some rate with some pauses, independent of the point structure; formula share and formula length independent of `A`.
**Crucially, H0 also predicts P1** whenever the text window spans the interval, so only P2-P4 discriminate.

**Measures in the brief that were not computed, and why:** intonation units (pause-based and pitch reset via praat-parselmouth): no audio
and no word times. Phase of IU onsets in the strike cycle (circular statistics with time-shifted surrogates): no onset times.
Formula rate in rally vs dead-ball periods: approximated only at clip level by T4 (changeover vs within-game units); rally-internal speech
cannot be isolated. Production speed and variability of frequent formulas vs matched non-formulaic phrases: needs audio or word
times; **impossible, skipped**. Contrast between media: only spoken TV vs written live text from other matches, without timing;
reduced to an EXPLORATORY length comparison (X1).

## 3. Data, units, sample

* In-sample: `tv_2019wimF`; held-out: `tv_2023wimF`; field `text_corrected`. Formula reference: the 18 `tv_pool_*` streams only
  (103675 tokens), so formula identification never sees either final.
* Unit = one PBP point; its text = all clips aligned to the point (fault clip + point-proper clip), never joined across clips.
  `A` from PBP `ElapsedTime` (1 s resolution); `D` (robustness R3) = next first serve (video time via the offset) minus the point's last hit.
* Dead-ball category (T4) by the rules of tennis: `changeover` = last point of an odd game >= 3 or of a set; `within_game` = next point
  in the same game; other game ends are not used in T4.

Sample flow (exclusion rules E1-E5 of the plan):

| step | 2019 | 2023 |
|---|---|---|
| PBP points | 422 | 334 |
| points with any aligned clip | 368 | 276 |
| E1 point-proper clip present | 358 | 268 |
| E2 not the last point | 358 | 268 |
| E3 timing QC (resid) | 353 | 245 |
| E4 A <= 600 s | 353 | 245 |
| E5 no video cut between p and p+1 (2023) | (not applied) | 219 |

Analysed units: 2019 n = 353 (9471 tokens, 63
with no text; median `A` 34 s, IQR 26-47 s;
290 within-game, 27 changeover/set-break, 36 other game-end units). 2023 n = 219 (5623 tokens,
39 with no text; median `A` 42 s; 197 within-game, 1 changeover/set-break, 21 other game-end units).
In 2023 E5 removes the units whose interval contains a video cut (the source video omits changeovers), so only
1 changeover unit remains and T4 is not testable there (pre-registered threshold: 15).

## 4. Definitions

* **Tokens**: NFC, lower case, regex `[a-z0-9]+(?:'[a-z0-9]+)*` (hyphens split, contractions kept); words per unit = tokens.
* **Formula** = n-gram (2 <= n <= 12, within a clip) occurring >= 3 times in the pool and in >= 2 pool streams: 9609 formulas
  (by n: {'2': 6167, '3': 2698, '4': 603, '5': 114, '6': 25, '7': 2}). Strict variant R2 (n >= 3, >= 5 times, >= 3 streams): 1088.
  The definition counts frequent function-word sequences as formulas; the most frequent maximal formulaic strings in the 2019 units are
  'in the' (18), 'of the' (17), 'on the' (15), 'for the' (14), 'from djokovic' (14), '40 15' (13), '30 15' (12), 'novak djokovic' (12), 'thank you' (12), 'djokovic has' (11), '40 30' (10), 'and the' (9). Hence the high overall share (0.644 in 2019, 0.696 in 2023)
  and the much lower strict share (0.149, 0.173). This definition is specific to
  this analysis and is not the formula-analyst's (analysis/formulas/).
* **Formula share** = formulaic tokens / tokens, pooled over the units of a group. **Formulaic string** = maximal matched occurrence.
* **Syllables**: rule-based counter (`syllables.py`), digits read as British English numbers ('0' as *love*). Accuracy on a held-out
  fixture of 120 random pool word types whose gold counts were written before the counter was run on them:
  0.967 (Wilson 95% CI [0.917, 0.987]), mean signed error -0.008
  syllables per word. (On the development fixture, which the rules were tuned on: 0.994; in-sample, not a validation.)
* **Null**: circular shift of the complete PBP timing sequence (A and category of every cycle) against the unit sequence, all shifts
  10 ... M-10 (2019: 402, 2023: 314 shifts; the p-value floor is therefore
  2/(K+1) = 0.0050 and 0.0063). Two-sided p. The brief's ">= 5,000 shifts" cannot
  be met by distinct index shifts of a sequence of about 400; a continuous time-shift null with 1-s steps (R6) supplies
  17220 (2019) and
  16348 (2023) shifts.
* **CIs**: circular block bootstrap over units in time order (block 10 units, B = 10,000), percentile 95%.
* **Multiplicity**: Holm within each match's confirmatory family (2019: T1-T4; 2023: T1-T3), alpha 0.05.

## 5. Confirmatory results

| match | test | H1' predicts | estimate [95% CI] | n | p shift-null (shifts) | p Holm | Holm-significant | sign as H1' |
|---|---|---|---|---|---|---|---|---|
| 2019wimF | T1 | rho > 0 (precondition; H0 with a spanning window predicts it too) | 0.248 [0.136, 0.359] | 353 units | 0.0050 (402) | 0.0198 | yes | yes |
| 2019wimF | T2 | > 0 (short intervals more formulaic) | -2.9 pp [-6.0, +1.3] | 353 units | 0.1092 (402) | 0.3127 | no | no |
| 2019wimF | T3 | rho > 0 (longer formulas when more time) | -0.040 [-0.088, 0.009] | 353 units / 3460 strings | 0.1042 (402) | 0.3127 | no | no |
| 2019wimF | T4 | > 0 (changeover talk freer, less formulaic) | +1.0 pp [-2.5, +4.4] | 353 units | 0.7494 (402) | 0.7494 | no | yes |
| 2023wimF | T1 | rho > 0 (precondition; H0 with a spanning window predicts it too) | 0.163 [0.030, 0.285] | 219 units | 0.0318 (314) | 0.0953 | no | yes |
| 2023wimF | T2 | > 0 (short intervals more formulaic) | -4.3 pp [-9.6, +1.1] | 219 units | 0.1206 (314) | 0.2413 | no | no |
| 2023wimF | T3 | rho > 0 (longer formulas when more time) | 0.021 [-0.025, 0.065] | 219 units / 2255 strings | 0.4318 (314) | 0.4318 | no | yes |
| 2023wimF | T4 | > 0 (changeover talk freer, less formulaic) | not testable: 1 changeover units after exclusions (< 15) | | | | | |

Group shares behind T2 and T4 (token-pooled, 95% CI):

| match | test | group 1 | group 2 |
|---|---|---|---|
| 2019wimF | T2 | short A (A <= 28.0 s): 0.622 [0.595, 0.659], 121 units, 2241 tokens | long A (A > 42.0 s): 0.650 [0.628, 0.670], 109 units, 4773 tokens |
| 2023wimF | T2 | short A (A <= 36.0 s): 0.675 [0.635, 0.718], 78 units, 1306 tokens | long A (A > 48.3 s): 0.718 [0.682, 0.753], 73 units, 2347 tokens |
| 2019wimF | T4 | within game: 0.647 [0.631, 0.664], 290 units, 5734 tokens | changeover/set break: 0.638 [0.605, 0.670], 27 units, 2591 tokens |

**What H1' predicted and what was observed.**
* T1 (P1): predicted rho > 0. Observed in 2019 (significant; OLS slope 0.53 [0.29, 0.90]
  tokens per second, p = 0.0050; 2023: 0.28 [0.04, 0.59], p = 0.0063). In 2023, rho > 0 with a CI excluding 0, but it is not significant after Holm and is
  not present among single-clip units (X7). Within within-game units (POST HOC, section 10.2), rho = 0.166 [0.046, 0.280] (n = 290, shift-null p = 0.0099) in 2019, so
  the association is partly between categories. H0 predicts the same pattern when the text window spans the interval, so T1 is
  consistent with H0 as well as with H1'. It establishes only, for 2019, that clip-level text carries some point-level timing information.
* T2 (P2): predicted more formulaic text in short intervals. Not observed: the point estimates go the other way in both finals
  (short 0.622 vs long 0.650 in 2019; 0.675 vs 0.718 in 2023), and no test is significant.
* T3 (P3): predicted longer formulas with more time. Not observed: rho is near 0 in both finals.
* T4 (P4): predicted less formulaic talk around changeovers. Not observed: within-game 0.647 vs changeover
  0.638. Not testable in 2023.

Figures: `figures/fig1_words_vs_available_time.png` (tokens vs `A`), `figures/fig2_formula_share.png` (shares by tercile and by
category), `figures/fig3_formula_syllables.png` (distribution of string syllables by tercile), `figures/fig4_shift_nulls.png` (null distributions).

## 6. Pre-registered descriptive measure T5: speech-rate ceiling

Rate = tokens per second of `A`. The upper envelope is the 90th percentile of the rate in the short and long `A` terciles; decision rule
(fixed in the plan): ratio CI inside [1/1.5, 1.5] = flat ceiling; CI entirely below 1 = ceiling falls; otherwise inconclusive.

| match | median rate (tokens/s) | q90 rate, short A | q90 rate, long A | ratio long/short | decision | 0.9-quantile regression: intercept; slope (tokens/s) |
|---|---|---|---|---|---|---|
| 2019wimF | 0.41 | 2.00 [1.49, 2.27] | 1.54 [1.16, 1.93] | 0.77 [0.58, 1.13] | inconclusive | 0.3 [-23.1, 13.5]; 1.57 [1.13, 2.34] |
| 2023wimF | 0.45 | 1.55 [1.31, 1.97] | 1.34 [1.09, 1.56] | 0.87 [0.66, 1.05] | inconclusive | 13.1 [-1.4, 46.3]; 1.15 [0.30, 1.58] |

Median rates of about 0.41 tokens per second of available time are far below continuous speech,
so either most of the interval is silent or the text window covers only part of it; the two cannot be told apart without audio.
Quantile-regression bootstrap fits with a convergence warning: 77 (2019),
59 (2023) of 10,000; the intercept CIs are wide and the regression is descriptive only.

## 7. Pre-registered robustness checks (not in the Holm family; used only for interpretation)

R1 score-call tokens removed; R2 strict formulas; R3 `D` (last hit to next serve) instead of `A`, shifted within the unit sequence;
R4 T3 as partial Spearman controlling for the unit's token count; R5 units involved in cross-point exact text repeats excluded;
R6 continuous time-shift null.

| match | check | test | estimate [95% CI] | units | p shift-null (shifts) | CI excludes 0 |
|---|---|---|---|---|---|---|
| 2019wimF | R1 score-call tokens removed | T2 | -3.5 pp [-6.6, +0.9] | 353 | 0.0496 (402) | no |
| 2019wimF | R1 score-call tokens removed | T3 | -0.022 [-0.069, 0.022] | 353 | 0.3176 (402) | no |
| 2019wimF | R1 score-call tokens removed | T4 | +0.4 pp [-3.3, +3.8] | 353 | 0.8685 (402) | no |
| 2019wimF | R2 strict formulas (n>=3, count>=5, streams>=3) | T2 | -0.7 pp [-3.5, +3.3] | 353 | 0.6749 (402) | no |
| 2019wimF | R2 strict formulas (n>=3, count>=5, streams>=3) | T3 | -0.057 [-0.158, 0.048] | 353 | 0.3226 (402) | no |
| 2019wimF | R2 strict formulas (n>=3, count>=5, streams>=3) | T4 | +0.5 pp [-2.7, +3.6] | 353 | 0.8437 (402) | no |
| 2019wimF | R3 predictor D (last hit to next serve), unit-sequence shift | T1 | 0.198 [0.089, 0.306] | 353 | 0.0060 (334) | yes |
| 2019wimF | R3 predictor D (last hit to next serve), unit-sequence shift | T2 | -2.1 pp [-5.7, +1.6] | 353 | 0.2209 (334) | no |
| 2019wimF | R3 predictor D (last hit to next serve), unit-sequence shift | T3 | -0.048 [-0.099, 0.000] | 353 | 0.0418 (334) | no |
| 2019wimF | R4 T3 partial Spearman controlling unit token count | T3 | 0.012 [-0.030, 0.051] | 353 | 0.5707 (402) | no |
| 2019wimF | R5 units in cross-point exact repeats excluded | T1 | 0.237 [0.105, 0.363] | 278 | 0.0050 (402) | yes |
| 2019wimF | R5 units in cross-point exact repeats excluded | T2 | -0.3 pp [-5.7, +4.0] | 278 | 0.8983 (402) | no |
| 2019wimF | R5 units in cross-point exact repeats excluded | T3 | -0.049 [-0.096, -0.001] | 278 | 0.0595 (402) | yes |
| 2019wimF | R5 units in cross-point exact repeats excluded | T4 | +1.3 pp [-2.4, +4.8] | 278 | 0.6997 (402) | no |
| 2019wimF | R6 continuous time-shift null (1-s steps) | T1 | 0.248 [0.136, 0.359] | 353 | 0.0001 (17220) | yes |
| 2019wimF | R6 continuous time-shift null (1-s steps) | T2 | -2.9 pp [-6.0, +1.3] | 353 | 0.0994 (17220) | no |
| 2019wimF | R6 continuous time-shift null (1-s steps) | T3 | -0.040 [-0.088, 0.009] | 353 | 0.0707 (17220) | no |
| 2019wimF | R6 continuous time-shift null (1-s steps) | T4 | +1.0 pp [-2.5, +4.4] | 353 | 0.5239 (17220) | no |
| 2023wimF | R1 score-call tokens removed | T2 | -4.5 pp [-9.9, +1.0] | 219 | 0.1143 (314) | no |
| 2023wimF | R1 score-call tokens removed | T3 | 0.025 [-0.024, 0.072] | 219 | 0.3936 (314) | no |
| 2023wimF | R1 score-call tokens removed | T4 | not testable (1 changeover units) | | | |
| 2023wimF | R2 strict formulas (n>=3, count>=5, streams>=3) | T2 | -0.4 pp [-7.3, +5.1] | 219 | 0.8825 (314) | no |
| 2023wimF | R2 strict formulas (n>=3, count>=5, streams>=3) | T3 | -0.020 [-0.127, 0.083] | 219 | 0.7048 (314) | no |
| 2023wimF | R2 strict formulas (n>=3, count>=5, streams>=3) | T4 | not testable (1 changeover units) | | | |
| 2023wimF | R3 predictor D (last hit to next serve), unit-sequence shift | T1 | -0.007 [-0.149, 0.125] | 217 | 0.9950 (198) | no |
| 2023wimF | R3 predictor D (last hit to next serve), unit-sequence shift | T2 | -3.9 pp [-9.2, +1.4] | 217 | 0.1306 (198) | no |
| 2023wimF | R3 predictor D (last hit to next serve), unit-sequence shift | T3 | 0.031 [-0.026, 0.083] | 217 | 0.2513 (198) | no |
| 2023wimF | R4 T3 partial Spearman controlling unit token count | T3 | 0.025 [-0.021, 0.067] | 219 | 0.3302 (314) | no |
| 2023wimF | R5 units in cross-point exact repeats excluded | T1 | 0.124 [-0.018, 0.258] | 195 | 0.1206 (314) | no |
| 2023wimF | R5 units in cross-point exact repeats excluded | T2 | -4.8 pp [-12.0, +0.2] | 195 | 0.1079 (314) | no |
| 2023wimF | R5 units in cross-point exact repeats excluded | T3 | 0.025 [-0.024, 0.071] | 195 | 0.3873 (314) | no |
| 2023wimF | R5 units in cross-point exact repeats excluded | T4 | not testable (1 changeover units) | | | |
| 2023wimF | R6 continuous time-shift null (1-s steps) | T1 | 0.163 [0.030, 0.285] | 219 | 0.0124 (16348) | yes |
| 2023wimF | R6 continuous time-shift null (1-s steps) | T2 | -4.3 pp [-9.6, +1.1] | 219 | 0.0865 (16348) | no |
| 2023wimF | R6 continuous time-shift null (1-s steps) | T3 | 0.021 [-0.025, 0.065] | 219 | 0.4244 (16348) | no |
| 2023wimF | R6 continuous time-shift null (1-s steps) | T4 | not testable (1 changeover units) | | | |

Reading: checks on T2-T4 with a CI excluding 0 or an unadjusted p < 0.05: 2019wimF R1 T2 (-3.5 pp, CI [-6.6, +0.9], unadjusted p = 0.0496; opposite to H1); 2019wimF R3 T3 (rho = -0.048, CI [-0.099, 0.000], unadjusted p = 0.0418; opposite to H1); 2019wimF R5 T3 (rho = -0.049, CI [-0.096, -0.001], unadjusted p = 0.0595; opposite to H1). None of them is in the direction H1 predicts;
these are uncorrected secondary analyses and are not evidence for the opposite hypothesis either, but they give no sign of an H1 effect
masked in the primary analysis. R3 confirms T1 in 2019 (rho = 0.198) but not in 2023 (rho = -0.007). R4
(rho = 0.012 [-0.030, 0.051]) shows that T3 stays near 0 once the unit's text length is controlled for.

## 8. Held-out replication (2023 final): not a comparable-range replication

The 2023 family (T1-T3) has no Holm-significant result. The 2023 source video omits the changeover periods (README 3.1), so
units whose interval contains a cut were excluded in advance (E5). This removes almost all long dead-ball intervals. The
2023 test therefore covers a narrower and differently composed range of `A`: 15-117 s
(q90 66 s, 1 changeover unit), against 14-305 s in 2019 (q90 66 s,
27 changeover units). Table and checks: section 10.3. The result for 2023 is read as follows. **T4 cannot be tested at a comparable range**;
T2 and T3 are null over the narrower range; and the 2019 T1 association is weaker in 2023 and not robust (R3, X7).
Nothing that was absent in 2019 appears in 2023.

## 9. EXPLORATORY analyses (not pre-registered as tests; no multiplicity correction)

* **X1 medium contrast (lengths only).** Cornell written live-text updates (other matches, no timing) vs 2019 TV transcripts:

| distribution | n | mean | q10 | q25 | median | q75 | q90 | max |
|---|---|---|---|---|---|---|---|---|
| cornell_update | 3962 | 45.12 | 19.0 | 27.0 | 40.0 | 58.0 | 78.9 | 301.0 |
| tv2019_clip_nonempty | 318 | 30.79 | 2.0 | 6.0 | 20.0 | 34.0 | 55.0 | 251.0 |
| tv2019_unit_nonempty | 290 | 32.66 | 2.0 | 7.0 | 21.0 | 37.0 | 71.0 | 251.0 |

  Median difference, updates minus non-empty clips: +20 tokens (iid bootstrap 95% CI
  [17, 23]). Written updates are longer and much less skewed toward very short items (score calls). Medium,
  match and author are confounded; no timing comparison is possible (`figures/fig5_lengths_by_medium_exploratory.png`).
* **X2 phase-tag contrast (circular).** Clips tagged `between_points`/score-call-only vs other clips, formula share
  2019: 0.789 vs 0.642 (difference +14.7 pp,
  CI [-3.7, +30.6]; n = 14 vs 304 clips);
  2023: 0.857 vs 0.699. The tag is defined by score-call text, and score calls are
  pool formulas, so this contrast is circular and was not used as a test (T4 replaced it with a rule-based dead-ball category).
* **X3 point-proper clip only** (fault-clip text dropped): T1 rho = 0.192
  [0.075, 0.308] (2019), 0.119 [-0.009, 0.237] (2023);
  T2 -2.7 pp (2019), -4.5 pp (2023).
* **X4 player names masked** in pool and target before formula identification: T2 -3.3 pp
  [-6.8, +1.1] (2019), -4.0 pp [-9.5, +1.6] (2023);
  T4 +2.0 pp [-2.1, +5.7] (2019).
* **X5 components of `A`.** Spearman of tokens with rally duration 0.176, shots 0.186,
  `D` 0.198 (2019); partial rho(tokens, `D` | rally duration, number of clips) = 0.159
  [0.049, 0.264] in 2019 and
  -0.070 [-0.209, 0.067] in 2023.
* **X6 T4 on 2023 without E5** (12 changeover units whose break is cut from the video):
  -1.6 pp [-7.2, +3.5].
* **X7 number of clips (added after seeing R3 for 2023).** A point with a first-serve fault has a longer cycle and a second transcript
  window. Among single-clip units T1 rho = 0.250 [0.116, 0.379] (2019, n = 251) but
  0.051 [-0.101, 0.193] (2023, n = 160); partial rho(tokens, `A` | number of clips)
  = 0.242 (2019) and 0.049 (2023). In 2023 the T1 association is
  therefore mostly a window-count effect.

## 10. POST HOC analyses after the critic review (plan.md Addendum 1; not pre-registered, outside every Holm family)

### 10.1 Minimum detectable effects of T2-T4 (PH2)

The method was fixed in the addendum before it was run. Each admissible index shift k0 of the primary null is taken in
turn as the true timing (402 bases in 2019, 314 in 2023). This keeps N, the text, the
formula coverage and the serial structure of both sequences, and it breaks the real alignment. An effect is then planted.
For T2 and T4, each unit's formula share is shifted by +d/2 in group 1 and -d/2 in group 2. For T3, a Gaussian copula
links string syllables to the unit's `A`, with the syllable distribution preserved. The confirmatory statistic is tested
against the shift null formed by the other admissible shifts (at least 383 per base in 2019,
295 in 2023). Power is the share of bases with p < alpha in the H1' direction. The MDE is the effect with
80% power, found by linear interpolation. "True" means the planted effect in the text of the unit's own interval.
"Measured" means the expected value of the test statistic. In the misattribution scenarios (illustrative, not estimates),
a fraction of 0.25 or 0.50 of each unit's text comes from the two neighbouring units. ASR noise is not simulated, because no
WER is available. Power at zero effect, the empirical one-directional size, is 0.022-0.025 at alpha = 0.05
against a nominal 0.025, so the shift-null test is calibrated. Power curves: `figures/fig6_power_curves_posthoc.png`.

| match | test | alpha | MDE, no misattribution (true = measured) | MDE true, misattribution 0.25 | MDE true, misattribution 0.50 | MDE measured, misattribution 0.50 | size at zero effect |
|---|---|---|---|---|---|---|---|
| 2019wimF | T2 | 0.0500 | 5.3 pp | 7.1 pp | 10.8 pp | 5.5 pp | 0.022 |
| 2019wimF | T2 | 0.0125 | 6.5 pp | 8.6 pp | 12.9 pp | 6.6 pp | 0.005 |
| 2019wimF | T3 | 0.0500 | 0.066 | 0.089 | 0.135 | 0.066 | 0.025 |
| 2019wimF | T3 | 0.0125 | 0.081 | 0.111 | 0.168 | 0.083 | 0.005 |
| 2019wimF | T4 | 0.0500 | 8.3 pp | 11.6 pp | > 19.8 pp (beyond the simulated range) | not reached | 0.022 |
| 2019wimF | T4 | 0.0125 | 10.6 pp | 14.6 pp | > 19.8 pp (beyond the simulated range) | not reached | 0.005 |
| 2023wimF | T2 | 0.0500 | 8.2 pp | 10.7 pp | 15.4 pp | 8.2 pp | 0.022 |
| 2023wimF | T2 | 0.0167 | 9.7 pp | 12.9 pp | 18.9 pp | 10.1 pp | 0.006 |
| 2023wimF | T3 | 0.0500 | 0.081 | 0.104 | 0.151 | 0.078 | 0.022 |
| 2023wimF | T3 | 0.0167 | 0.096 | 0.126 | 0.187 | 0.097 | 0.006 |

Reading. With misattribution, the measured MDE stays about the same, because the test sees the same statistic. The true
effect needed grows: at misattribution 0.50 it is 1.86-2.05 times the true MDE without misattribution,
where both are within the simulated range. The 2019 CI bounds in section 1 are smaller than these MDEs, because the point estimates are near or below 0.
The CIs bound the measured effect in these data; the MDEs describe what the design could detect.

### 10.2 T1 within dead-ball categories (PH3)

| match | all units | within-game units | units with text | median tokens: within game / other game end / changeover | median `A` (s): within game / changeover |
|---|---|---|---|---|---|
| 2019wimF | 0.248 [0.136, 0.359] (n = 353) | 0.166 [0.046, 0.280] (n = 290, shift-null p = 0.0099) | 0.248 [0.122, 0.365] (n = 290) | 14.0 / 37.5 / 109.0 | 31.0 / 100.0 |
| 2023wimF | 0.163 [0.030, 0.285] (n = 219) | 0.125 [-0.007, 0.252] (n = 197, shift-null p = 0.1016) | 0.283 [0.138, 0.424] (n = 180) | 17.0 / 25.0 / 12.0 | 41.0 / 117.0 |

In 2019, units with no text have a median `A` of 29.0 s, against 35.0 s for units with text
(63 empty units). Excluding units with no text gives rho = 0.248 (2019) and
0.283 (2023). The association is therefore not produced by empty windows. Reading: in 2019, T1 is
partly a between-category effect, because changeover units have both long intervals and long texts. Within games it is
weaker but its CI excludes 0 in 2019, and weaker and cannot be distinguished from 0 in 2023. H0 (a constant rate within a text window that spans
the interval) predicts this as well as H1', so T1 remains a precondition and not support.

### 10.3 Range of `A` and comparability of the 2023 final (PH4)

| match | units | min | q10 | median | q90 | max | units with `A` > 100 s | changeover units |
|---|---|---|---|---|---|---|---|---|
| 2019wimF | 353 | 14 | 20 | 34 | 66 | 305 | 13 | 27 |
| 2023wimF | 219 | 15 | 27 | 42 | 66 | 117 | 2 | 1 |

The 2019 units were restricted to `A` <= 117 s, the 2023 maximum. This drops 5 units (348 remain).
On the restricted units, T2 = -2.9 pp [-6.3, +1.1] (shift-null p = 0.1290) and
T3 rho = -0.028 [-0.074, 0.018] (p = 0.2432). The 2019 nulls are therefore not produced by the few longest intervals. The main difference between the two matches is composition (changeover units), which only T4 tests
and which 2023 lacks.

### 10.4 Serial correlation and the shift null (PH5)

The circular shift moves the whole timing sequence against the whole unit sequence, so both sequences keep their serial
structure in every null draw. Serial correlation is therefore handled by construction, unlike in an iid label permutation.
One-line check: the lag-1 Spearman autocorrelations in unit order are, for tokens,
-0.047 / 0.011; for formula share,
0.060 / -0.033; and for `A`,
-0.020 / 0.161 (2019 / 2023). The ratio of the shift-null SD to the
iid-permutation-null SD (2,000 permutations) is 0.97-1.05 across T1-T4 and both
matches. In these data, then, serial correlation barely widens the null.
No test changes side of p = 0.05 between the two nulls.

### 10.5 Umpire-pattern tokens (PH6)

The formula list used in T2-T4 comes from the pool only, and it was **not** filtered for umpire speech. It contains
17 formula types with `thank you` (188 pool occurrences), 0 with `mr <token>` and
0 with `game <player name>`. Mask U removes every `thank you` (with an adjacent `please` or a
following `players`), `mr` + the next token, and `game` + a finalist's name. In the target units it covers
99 of 9471 tokens (2019) and 8 of 5623 (2023). R1U adds the
pre-registered R1 score-call mask. The text splits at masked spans, and the formula list is unchanged.

| match | check | test | estimate [95% CI] | units | tokens | p shift-null (shifts) | CI excludes 0 |
|---|---|---|---|---|---|---|---|
| 2019wimF | PH6 variant U | T2 | -2.7 pp [-5.9, +1.6] | 353 | 9372 | 0.1290 (402) | no |
| 2019wimF | PH6 variant U | T3 | -0.042 [-0.089, 0.006] | 353 | 9372 | 0.0794 (402) | no |
| 2019wimF | PH6 variant U | T4 | +1.4 pp [-2.0, +4.6] | 353 | 9372 | 0.6501 (402) | no |
| 2019wimF | PH6 variant R1U | T2 | -3.3 pp [-6.4, +1.1] | 353 | 9144 | 0.0447 (402) | no |
| 2019wimF | PH6 variant R1U | T3 | -0.025 [-0.070, 0.019] | 353 | 9144 | 0.2730 (402) | no |
| 2019wimF | PH6 variant R1U | T4 | +0.7 pp [-2.7, +3.9] | 353 | 9144 | 0.7841 (402) | no |
| 2023wimF | PH6 variant U | T2 | -4.4 pp [-9.7, +1.0] | 219 | 5615 | 0.1079 (314) | no |
| 2023wimF | PH6 variant U | T3 | 0.019 [-0.027, 0.064] | 219 | 5615 | 0.4762 (314) | no |
| 2023wimF | PH6 variant U | T4 | not testable (1 changeover units) | | | | |
| 2023wimF | PH6 variant R1U | T2 | -4.6 pp [-10.1, +0.9] | 219 | 5492 | 0.1143 (314) | no |
| 2023wimF | PH6 variant R1U | T3 | 0.023 [-0.025, 0.071] | 219 | 5492 | 0.4190 (314) | no |
| 2023wimF | PH6 variant R1U | T4 | not testable (1 changeover units) | | | | |

Reading: no umpire-masked estimate has a CI excluding 0. Umpire speech in the text does not drive the null results.

## 11. Interpretation

With clip-level text, the only frame that can be tested is the interval between points. In the 2019 final, the amount of
text attached to a point tracks that point's own interval beyond match-level drift (T1). Part of the association runs
across game boundaries, because changeover units have long intervals and long texts. Within games the association is
weaker (rho = 0.166). It shows that clip-level text carries some point-level
timing information, which both H1' and H0 predict. Given that, the formula measures could have shown the pattern H1'
predicts, but they did not. Formula share does not rise in short intervals (the point estimate falls); formula length in
syllables does not grow with the time available; and changeover talk is not less formulaic than within-game talk. At
this resolution and **for the text as measured**, the commentary behaves as H0 describes: more time yields more text,
with no detectable change in formula share or formula length.

"No detectable change" is bounded by the design. With 80% power, the tests would have detected measured effects of about
5.3 pp (T2), rho = 0.066 (T3) and 8.3 pp (T4) in 2019. Misattribution of text to
points and ASR errors make the corresponding true effects larger by an unknown factor: about 1.9-2.1 times
larger if half of a unit's text belonged to neighbouring intervals (section 10.1).

For the analogy with oral-formulaic verse, the data give no support for the idea that the time between points conditions
the length or density of formulas the way a metrical slot would. They cannot exclude effects smaller than the MDEs, or
effects attenuated by the measurement. They say nothing about the strike level, where the brief located the metrical
frame and which this corpus cannot reach, nor about formulaic systems, which were not measured here.

## 12. Limitations

1. **No audio, no word times, no speakers**: intonation units, pitch resets, IU phase, rally-internal speech and
   production speed cannot be measured. The hypothesis tested is the re-specified H1', not H1.
2. **Undocumented text window**: texts are attributed to clips by an unknown rule, and identical texts recur on clips a
   median 17.2 s apart. A unit's text can include talk
   from before the point and can miss talk late in long intervals. This blurs the link between time and text and biases
   every T-test toward 0. **The CIs and MDEs bound the measured effect, not the true one** (illustrative misattribution
   scenarios in section 10.1).
3. **Mixed voices**: umpire calls, Hawk-Eye and announcements are in the text. R1 removes score calls; the post hoc
   variants U and R1U also remove `thank you`, `mr <name>` and `game <name>` (section 10.5). Hawk-Eye and other
   announcements remain.
4. **ASR errors**: a hand-read sample of 500 words found 22 errors per 1,000 words
   (Wilson 95% 12-39;
   `corpus/reports/asr_proxy.json`, README 7.3). This is a lower bound, because plausible-word substitutions are invisible.
   The errors cluster in short score-call clips and in names, and they break n-gram matches. Errors that do not differ
   between groups scale both groups' formula shares down, which shrinks T2 and T4 towards 0. If the error rate is higher
   in short-interval units, it lowers their formula share and works against P2, and it could explain part of the negative
   T2 estimates.
5. **Formula operationalisation**: frequent n-grams from other matches (other broadcasters and commentators) include
   function-word sequences, so the base share mostly measures repetition of common sequences. The strict (R2),
   name-masked (X4) and umpire-masked (U, R1U) variants do not change the conclusions. Other definitions (formulaic
   systems, within-broadcaster formulas) were not tested here.
6. **Timing**: `A` has 1 s resolution and includes the fault interval; `D` depends on the TennisVL parser and the video
   offset. The 2023 video omits changeovers, so the held-out test covers a narrower range of intervals and includes no T4
   (section 10.3).
7. **Short formulaic strings**: maximal formulaic strings are mostly bigrams (79% have two tokens
   in 2019; mean 2.67 syllables and median 2 in 2019; mean
   2.72 in 2023). T3 therefore works on a narrow range of lengths and could miss effects confined
   to long formulas. R2, with n >= 3, covers 509 strings in 2019 and is also null.
8. **Power and dependence**: 353 (2019) and 219 (2023) units.
   Formulaic strings are clustered within units, and the bootstrap resamples units. The index-shift null has a two-sided
   p-value floor of 0.0050 (2019) and 0.0063 (2023).
   The simulated MDEs are in section 10.1.
9. **One broadcaster per match**: commentator identity, broadcaster and match are confounded. The medium contrast (X1)
   compares different matches and is descriptive.
10. Robustness checks, exploratory and post hoc analyses are not corrected for multiplicity; they are used only for
    interpretation.

## 13. Deviations from the plan

* The brief's ">= 5,000 shifts" is met only by the pre-registered secondary null R6. The primary null is the exhaustive index shift, as the plan states.
* All bootstraps use the plan's seed 20190714. Quantile-regression bootstrap fits that raised a convergence warning are kept
  (counts in section 6). X7 was added after the robustness results were seen and is exploratory.
* **Plan Addendum 1 (POST HOC, 2026-10-07)**, written after `review/critic_analysis_v1.md` and committed before the new
  analyses were run:
  * PH1: the summary bound on T2/T3 was withdrawn. It is replaced by a statement about the measured effect together with
    the attenuation caveat.
  * PH2: MDE simulation.
  * PH3: T1 within dead-ball categories.
  * PH4: the ranges of `A`, with 2019 restricted to the 2023 range; the 2023 result is renamed "not a comparable-range
    replication".
  * PH5: serial-correlation check.
  * PH6: umpire-pattern check, with sensitivity variants U and R1U.
  * PH7: hand-entered literals in the report generator were replaced by values read from files (ASR figure, unit
    counts, bootstrap constants).
  * PH8: the R2 estimates are shown beside the base definition in the summary.
* No confirmatory definition, test, exclusion rule, threshold or verdict rule was changed after the plan commit.

## 14. Files

`plan.md` (pre-registration and Addendum 1); `metre_lib.py`, `syllables.py`, `s01_syllable_check.py` ... `s04_exploratory.py`,
`s04b_posthoc.py` (POST HOC), `s05_figures.py`, `s06_make_report.py`, `run_all.sh`; `data/syllable_heldout_fixture.tsv`
(hand-coded fixture); `results/` (all tables: `confirmatory_*.csv`, `robustness_*.csv`, `t5_*.json`, `details_*.json`,
`exploratory.json`, `exploratory_lengths.csv`, `units_*.csv`, `strings_*.csv`, `clips_*.csv`, `sample_flow_*.csv`,
`pool_formulas_*.{json,tsv}`, `top_strings_*.tsv`, `syllable_check.json`, `verdict.json`, `nulls_*.npz`; POST HOC:
`posthoc.json`, `posthoc_mde.csv`, `posthoc_power_curves.csv`, `posthoc_sensitivity.csv`, `posthoc_umpire_check.json`);
`figures/` (fig6 is POST HOC).
