# Metre analysis: pre-registered plan (Phase 2)

Written and committed **before any test script was written or run**. Anything in `report.md` that is not specified here is labelled
**exploratory**. Code: `analysis/metre/`; rerun end to end with `bash analysis/metre/run_all.sh`; all numbers are written to
`analysis/metre/results/`.

## 0. Why the hypothesis must be re-specified (decided before testing)

The original H1 (agent brief): *during rallies, the intervals between strikes act as a metrical frame; intonation-unit (IU) boundaries
align with strikes; formula length is constrained by the time available; between points, composition is freer.*
H0: *no alignment beyond what speech rate and pause distribution predict.*

The corpus (corpus/README.md sections 0, 4, 6, 8; STATUS.md Phase 0) has **no audio, no word timestamps and no speaker labels**. Each
transcript is WhisperX text attached to a TennisVL rally clip (median clip 6.2 s in 2019), and the text window is undocumented and
extends beyond the clip (score calls in the text are the score *after* the point in 68% of the 2019 cases; identical texts recur on
clips a median 17 s apart, see section 7). Therefore the following measures in the brief **cannot be computed and are not attempted**:

* intonation units (pause-based or pitch-reset; no audio for praat-parselmouth, no word times for pauses);
* the phase of IU onsets within the inter-strike cycle (circular statistics need onset times);
* separating speech during rallies from speech between points (no word times; README section 6);
* production speed and variability of frequent formulas against matched non-formulaic phrases (needs audio or word times).

Because speech during rallies cannot be isolated, **H1 is re-specified, explicitly, as follows**: the frame is the **interval between
points** (from the last strike of a point to the first serve of the next point) together with the point itself, and the unit of text is
the **clip-level transcript** aggregated per point. The strike-level ("metrical") version of H1 is untestable with this corpus.

## 1. Re-specified hypotheses

**H1' (frame).** The time available around a point (the point itself plus the dead-ball interval up to the next first serve) is a
frame that the commentary is fitted to. Predictions, each with its direction:
* P1: the amount of text attached to a point increases with the time available (beyond match-level drift).
* P2: commentary is **more formulaic when time is short**: the formula share of words is higher in short-interval units than in long-interval units.
* P3: **formula length is constrained by the time available**: the syllable count of formulaic strings increases with the time available.
* P4: **composition is freer in long dead-ball periods**: formula share is lower in units whose interval contains a changeover or set break than in within-game units.
* P5 (descriptive): if the interval is a frame that is filled, the ceiling of the speech rate (words per second of available time) is
  roughly constant across interval lengths.

**H0.** The commentary is produced at some speech rate with some pause distribution, independent of the point structure: the
amount of text attached to a point reflects only the length of the text window, and the composition of the text (formula share,
formula length) does not depend on the time available.

**What H0 also predicts (important).** If the transcript window spans the available time, H0 *also* predicts P1 (more seconds of
window, more words at a constant rate). P1 is therefore a **precondition** (does clip-level text carry point-level timing information at
all?), **not evidence for H1'** on its own. Only P2-P4 discriminate H1' from H0. A null result for P1 means the clip text cannot test the
frame hypothesis at all (either the window does not follow the interval, or talk is unrelated to it), and P2-P4 must then be read as
weak tests.

## 2. Data, units and sample

* **In-sample**: stream `tv_2019wimF` (2019 Wimbledon men's final). **Held-out replication**: `tv_2023wimF` (2023 final). Text field:
  `text_corrected` (de-duplicated and corrected; README sections 4-5).
* **Formula reference**: the 18 `tv_pool_*` streams (`text_corrected`); never the 2019 or 2023 text, so formula identification is held
  out from both finals.
* **Timing**: `corpus/timing/points_{2019wimF,2023wimF}.csv` (PBP `elapsed_s` = first serve of each point, 1 s resolution; TennisVL
  `tv_last_hit_s`, `offset_used_s`, `resid_s`, `pbp_serve_number`, `tv_clip_fault`, set/game fields).
* **Unit** = one PBP point *p*. Unit text = concatenation, in clip order, of `text_corrected` of **all** clips aligned to *p*
  (`point_idx_pbp == p`: first-serve-fault clip and point-proper clip). Tokens are never joined across clips (n-grams do not cross clip
  boundaries). Empty text is a valid outcome (0 words).
* **Available time** (primary predictor) `A_p = elapsed_s(p+1) - elapsed_s(p)`: the serve-to-serve cycle of point *p* from the PBP
  match clock. For a first-serve point it equals rally duration + dead time from the last strike to the next first serve; for a
  second-serve point it also includes the fault and the pause before the second serve (whose fault-clip text is part of the unit).
  It is independent of the TennisVL parser and is real match time in both finals.
* **Frame proper** (robustness predictor R3) `D_p` = video time of the next first serve minus `tv_last_hit_s(p)`, with the next serve's
  video time = `elapsed_s(p+1) + offset_used_s(p)` (2019: constant 26.72 s; 2023: the level of *p*'s video segment).
* **Dead-ball category** (for P4), fixed by the rules of tennis, not by measured time:
  `changeover` = *p* is the last point of a game that is followed by a seated changeover or set break (game number in the set odd and >= 3, or
  the last game of a set); `within_game` = point *p+1* is in the same game as *p*; all other game-ending units (end of game 1, even games)
  are `other_game_end` and are not used in T4.

### Exclusion rules (applied in this order; counts reported in `results/sample_flow_*.csv`)
* E1: *p* has a point-proper clip (`clip_role` rally, ace or double_fault) aligned to it. (Points with only a fault clip, or no clip, are out.)
* E2: *p* is not the last point of the match (needs *p+1*).
* E3: timing QC: |`resid_s`| <= 3 s, or `resid_s` > 3 s on a second-serve point without a fault clip (explained in README 3.1:
  the clip starts at the second serve). Other residual outliers indicate a misaligned clip and are excluded.
* E4: `A_p` <= 600 s (abnormal interruptions excluded; none expected in 2019).
* E5 (2023 only): no video cut between *p* and *p+1*: a unit is excluded if *p* and *p+1* both lie inside the cut interval
  `[a, b]` of any offset segment (`corpus/reports/timing_report_2023wimF.json`, `offset_segments`), because the 2023 video omits the
  changeover periods and the transcript cannot contain their talk.
* For D_p (R3 only): additionally `D_p > 0`.

## 3. Measures

* **Tokenisation**: Unicode NFC, lower-case, curly apostrophes to `'`, tokens = regex `[a-z0-9]+(?:'[a-z0-9]+)*`. Hyphens and all
  other punctuation split tokens (so `30-15` and `30, 15` both give `30`, `15`); contractions (`it's`) are one token. Punctuation is
  otherwise ignored (ASR punctuation is model-generated). This differs from the README word regex, which keeps hyphenated forms as one word.
  **Words per unit** = number of tokens.
* **Formulas** (identified on the pool only): every n-gram with 2 <= n <= 12 tokens, n-grams taken within a clip, that occurs **>= 3
  times in total** in the 18 pool streams **and in >= 2 distinct pool streams** (the second condition guards against within-match ASR
  repeats from overlapping clip windows, README section 4). Player names are not masked.
* **Formula coverage**: a token of a unit is formulaic if it lies inside at least one occurrence (within the same clip) of a formula
  n-gram. **Formula share** of a set of units = formulaic tokens / all tokens (token-pooled).
* **Formulaic strings** (for P3): each maximal matched occurrence, i.e. a formula occurrence in a clip not properly contained in a
  longer formula occurrence in the same clip (partially overlapping maximal occurrences are both kept).
* **Syllable count**: rule-based English counter (`analysis/metre/syllables.py`): vowel-group count with documented corrections
  (silent final *e*, *-le*, *-es*/*-ed* endings, a short exception list). Digits are expanded to British English number words first
  (`15` fifteen, `350` three hundred and fifty, years 1900-2099 read as two pairs, ordinals `1st`). Accuracy is checked on a
  hand-coded fixture list of commentary words (reported; the fixture is input data, not a result). No pronouncing dictionary is available offline.
* **Speech rate** `r_p = words_p / A_p` (words per second of available time).

## 4. Confirmatory tests

Family per match, two-sided, **alpha = 0.05**, **Holm-Bonferroni** correction within each match's family.
2019 family: T1-T4 (4 tests). 2023 family: T1-T3 (3 tests) plus T4 only if >= 15 `changeover` units survive E5; otherwise T4 is reported as
not testable on 2023.

| test | prediction | statistic (effect size) | H1' predicts |
|---|---|---|---|
| T1 | P1 | Spearman rho(words_p, A_p) over units | rho > 0 |
| T2 | P2 | formula share in the short-A tercile minus share in the long-A tercile (difference in proportions, token-pooled) | > 0 |
| T3 | P3 | Spearman rho(syllables of formulaic string, A of its unit) over all formulaic strings | rho > 0 |
| T4 | P4 | formula share in `within_game` units minus share in `changeover` units | > 0 |

* Terciles: short = A <= 1/3 empirical quantile of A over the analysed units, long = A > 2/3 quantile (numpy linear quantiles; ties at a
  cut go to the lower group). Recomputed on the shifted A in every null draw.
* **Null (p-values)**: circular shift of the **timing sequence** relative to the transcript sequence. The timing sequence is the complete
  PBP sequence of cycles 1..M (M = number of PBP points minus 1; A and the dead-ball category of every cycle, including points without a
  clip). In shift *k*, unit *p* receives the timing values of cycle ((p - 1 + k) mod M) + 1. All shifts k = 10, ..., M - 10 are used
  (exhaustive; shifts within +-9 points are excluded to avoid local autocorrelation). This preserves the serial structure of both
  sequences and breaks only the point-by-point alignment. Two-sided p = min(1, 2 min(p_up, p_down)) with
  p_up = (1 + #{null >= obs}) / (1 + K), p_down likewise.
  *Note on the brief's ">= 5,000 shifts"*: a sequence of M (about 420) cycles has only M - 1 distinct circular shifts, so 5,000 distinct
  index shifts do not exist. The exhaustive index-shift null is the primary null; a **continuous time-shift null with >= 5,000 shifts** is
  run as robustness check R6 (below).
* **CIs**: circular block bootstrap over units in chronological order, block length 10 units (about one game), B = 10,000, percentile
  95% CI, seed 20190714. For T3 the units are resampled and all their strings come along.
* Additionally reported with T1 (secondary, not in the family): OLS slope of words on A (words per extra second) with bootstrap CI and
  index-shift p.

## 5. Pre-registered descriptive measure (not in the Holm family)

* **T5 (P5) rate ceiling**: the 90th percentile of r_p in the short and long A terciles; effect size = log(q90_long / q90_short) with
  block-bootstrap 95% CI. Decision rule: CI inside +-log(1.5) = flat ceiling (frame-like); CI entirely below 0 = ceiling falls with
  time (longer intervals are not filled in proportion); otherwise inconclusive. Also: 0.9 quantile regression of words on A (intercept,
  slope, bootstrap CIs). Caveat fixed in advance: if the text window does not span long intervals (e.g. changeovers), a falling ceiling
  is expected mechanically and says nothing about the commentators.

## 6. Pre-registered robustness checks (reported with CI and index-shift p; not in the Holm family)

* R1: T2-T4 with **score-call tokens removed** before matching (the clip text splits at removed spans; no n-gram crosses them).
  Score-call tokens = maximal runs of tokens from {0, 15, 30, 40, love, fifteen, thirty, forty, all, deuce, advantage, ad, game, set,
  match} containing at least one of {0, 15, 30, 40, love, fifteen, thirty, forty, deuce, advantage}, plus `game`/`advantage` immediately
  followed by a player surname of the match (umpire-style calls). Reason: the umpire's calls are in the transcripts and add a roughly
  fixed amount of highly formulaic text per point, which would make short units look more formulaic under H0.
* R2: stricter formula definition: n >= 3, >= 5 occurrences, >= 3 pool streams (T2-T4).
* R3: D_p (frame proper) instead of A_p (T1-T3); the D shift null shifts within the unit sequence (D is undefined for points without clips).
* R4: T3 as a partial Spearman correlation controlling for the unit's token count (ranks residualised on rank of token count).
* R5: T1-T4 excluding units involved in a cross-point exact repeat (a clip whose text was removed as an exact repeat of a clip of
  another point, or the source of such a repeat).
* R6: T1-T4 with a continuous time-shift null: shift the timing sequence by every integer s in [300, T - 300] seconds of match clock
  (T = span from the first serve to the last cycle's end, about 17,000 shifts in 2019); unit *p* receives the timing values of the cycle
  that contains elapsed(p) + s (wrapped). This samples long cycles more often (size bias); hence secondary.

## 7. Interpretation rules (fixed now)

* H1' is described as **supported** in the 2019 final only if at least one of T2-T4 is Holm-significant in the predicted direction **and**
  the same effect keeps its sign with a 95% CI excluding 0 under R1. It is **replicated** if the same test is Holm-significant in the same
  direction in the 2023 family. T1 alone never counts as support (section 1).
* A significant effect in the direction opposite to H1' is reported as such.
* Non-significant results are reported with their CIs as "not detected", never as evidence of absence unless the CI is narrow
  (stated explicitly).
* Power note (fixed in advance): with about 300 units, a two-sided Spearman test at alpha 0.05 has about 80% power only for |rho| >= 0.16.

## 8. Exploratory (labelled as such in the report)

* X1 medium contrast: length (tokens) of Cornell written live-text updates vs 2019 clip-level and unit-level transcripts. The Cornell
  text has no timing and comes from other matches, so only length distributions are compared; no timing test is possible.
* X2 phase-tag contrast (heuristic `between_points`/score-call-tagged clips vs other clips). Circular for formula share, because the
  `between_points` tag is defined as text that is a score call, and score calls are themselves pool formulas.
* X3 per-clip (instead of per-point) versions of T1-T3; X4 name-masked formulas; X5 words vs number of shots and rally duration;
  X6 T4 on 2023 without E5; anything else added after this commit.

## 9. Data inspected before writing this plan (disclosure)

Only structure, never an outcome-predictor relation: field lists of the jsonl and timing tables; the distribution of A_p (2019: median
34 s, max 305 s; 2023: median 43 s, max 447 s); clip timing relative to hits (clip starts about 1.0 s before the first hit and ends about
2.0 s after the last hit, medians); the timing of the 55 (2019) / 26 (2023) exact-repeat clips (median 17 s after the end of the clip
they repeat, mostly the next point), which shows that a clip's text window reaches well beyond the clip; clip-role and dedup counts;
counts of residual outliers by serve number. No word count, formula share or syllable count was computed before this commit.

---

## Addendum 1 (2026-10-07): POST HOC changes after the critic review `review/critic_analysis_v1.md`

**Label: POST HOC.** Everything in this addendum was decided after the confirmatory results, `report.md` and the critic's
review had been seen. The text above this addendum is unchanged. No confirmatory definition, test, exclusion rule, threshold,
alpha or Holm family is changed, so the confirmatory results and the section-7 verdict are unchanged. Every new analysis
below is reported as **POST HOC** in `report.md`, is outside every Holm family and is used only for interpretation. This
addendum was committed before any of the new analyses was run. New code: `s04b_posthoc.py`. Umpire-mask variants were added
to `metre_lib.py` and `s02_build.py`; all pre-existing outputs are unchanged. The report generator (`s06_make_report.py`)
and the figures (`s05_figures.py`) were extended.

* **PH1 (critic B5), verdict wording.** The summary sentence "The 2019 CIs are narrow enough to exclude a short-interval
  excess in formula share larger than 1.3 pp and a positive syllable-time correlation larger than rho = 0.009" is withdrawn.
  It conflicted with Limitation 2 (attenuation). The replacement states what the 2019 CIs exclude **for the effect as
  measured**: clip-level text attributed to points, ASR text, and the section-3 formula definitions. It then says that
  misattributing text to points and ASR errors both attenuate a true effect towards 0, so the true effect could be larger
  than these bounds. The "unless the CI is narrow" clause of section 7 is not invoked.
* **PH2 (critic B5), minimum detectable effect (MDE) by simulation** for T2, T3 and T4 in 2019 and for T2 and T3 in 2023.
  The method was fixed here before it was run:
  * *Null bases.* Each admissible index shift k0 of the primary null (k0 = 10 ... M-10) is treated in turn as the true
    timing. This breaks the real alignment. It keeps the real N, token counts, formula coverage, string syllables and the
    serial structure of both sequences.
  * *Planted effect, T2 and T4.* Each unit's formula share is shifted additively under the k0 timing:
    delta_u = +d/2 in group 1 (short tercile for T2, within-game for T4), -d/2 in group 2 (long tercile, changeover) and 0
    otherwise. Then n_cov' = clip(n_cov + delta_u * n_tok, 0, n_tok).
  * *Planted effect, T3 (Gaussian copula).* latent = sqrt(1 - w^2) * z(rank of the string's syllables, ties broken at
    random) + w * z(rank of the A of the string's unit). Each string then receives the syllable count of its latent rank
    among the observed syllable counts, so the syllable distribution is preserved exactly. The effect size is the Spearman
    rho between the planted syllables and A.
  * *Test.* The confirmatory statistic at k0 is compared with the shift null formed by all admissible k at circular
    distance >= 10 from k0, using the two-sided p of section 4. A detection is p < alpha with the estimate > 0, the
    direction H1' predicts.
  * *Power and MDE.* Power is the share of k0 at which the test detects. Grids: d = 0 to 0.20 in steps of 0.005;
    w = 0 to 0.60 in steps of 0.02. The MDE is the smallest effect with power >= 0.80, found by linear interpolation, at
    alpha = 0.05 and at alpha/m (the first Holm step; m = 4 in 2019, 3 in 2023). The power at d = 0 or w = 0 is reported
    as the empirical size of the one-directional test.
  * *Attenuation scenarios (illustrative, not estimates).* The misattribution fraction is m_mix in {0, 0.25, 0.5}: a unit's
    measured text is (1 - m_mix) its own interval and m_mix its two neighbours in the unit sequence, in equal parts. For
    T2 and T4 the measured shift is delta_u' = (1 - m_mix) * delta_u + m_mix / 2 * (delta_{u-1} + delta_{u+1}). For T3,
    each string's source unit is its own unit with probability 1 - m_mix and otherwise a neighbour, each with equal
    probability. The plant uses the source unit's A; the test uses the A of the unit the string is assigned to. MDEs are
    reported both as the true (planted) effect and as the expected measured effect.
  * ASR noise is not simulated, because no WER is available (corpus README 7.3). Its attenuating effect is stated in
    words. Seed 20190714.
* **PH3 (critic C4).** T1 is computed within within-game units (Spearman rho, block-bootstrap CI, index-shift p) for both
  matches and reported beside the overall rho. T1 is described as consistent with H0 as well as with H1', and "time-locked
  at the level of points" is qualified.
* **PH4 (critic C6).** The ranges of A (min, q10, median, q90, max) of the analysed units are reported for both matches.
  The 2023 result is described as **not a comparable-range replication**: T4 is not testable there, and T2 and T3 are
  null over a narrower range of A. Exploratory addition: T2 and T3 in 2019 restricted to units with A <= the maximum A of
  the analysed 2023 units (estimate, block-bootstrap CI and index-shift p).
* **PH5 (critic C3, applied to this analysis).** Serial-correlation check: lag-1 Spearman autocorrelation, in unit order, of
  tokens, formula share (units with text) and A. For T1-T4, the ratio of the SD of the index-shift null to the SD of an iid
  label-permutation null (2,000 permutations of the units' timing values), and the permutation p for comparison. The
  circular shift preserves the serial structure of both sequences by construction; the check shows how much that matters.
* **PH6 (critic C2/B6, applied to this analysis).** The pool-only formula list is not filtered for umpire speech. Check: the
  number of formula types that contain `thank you`, `mr <token>`, or `game <player name>` (a name from any pool match id or
  either final), and the number of target tokens in these patterns. Sensitivity runs, outside any Holm family, mask target
  tokens before matching, and the text splits at masked spans as in R1. Variant **U** masks umpire patterns: every
  `thank you` together with an adjacent `please`, or a following `players`; `mr` + the next token; and `game` + a first
  name or surname of either finalist. Variant **R1U** applies U together with the R1 score-call mask. Both variants report
  T2-T4 with CI and index-shift p. The formula list is unchanged, as in R1.
* **PH7 (critic C7).** Hand-entered literals in `s06_make_report.py` are replaced by values read from files: the ASR
  figure from `corpus/reports/asr_proxy.json`, the unit counts in Limitation 8, and the bootstrap B and block length.
* **PH8 (critic C5, wording only).** The strict-formula (R2) share and the R2 estimates for T2-T4 are shown beside the base
  definition in the summary.
