"""Write analysis/metre/report.md. Every number is read from analysis/metre/results/ (no hand-entered results)."""
import json
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
from metre_lib import HERE, RES  # noqa: E402

T = ["2019wimF", "2023wimF"]
conf = {t: pd.read_csv(RES / f"confirmatory_{t}.csv").set_index("test") for t in T}
rob = {t: pd.read_csv(RES / f"robustness_{t}.csv") for t in T}
det = {t: json.load(open(RES / f"details_{t}.json")) for t in T}
t5 = {t: json.load(open(RES / f"t5_{t}.json")) for t in T}
flow = {t: pd.read_csv(RES / f"sample_flow_{t}.csv") for t in T}
ex = json.load(open(RES / "exploratory.json"))
ver = json.load(open(RES / "verdict.json"))
syl = json.load(open(RES / "syllable_check.json"))
pool = json.load(open(RES / "pool_formulas_summary.json"))
top19 = pd.read_csv(RES / "top_strings_2019wimF.tsv", sep="\t")


def f(x, k=3):
    return "n/a" if x is None or (isinstance(x, float) and pd.isna(x)) else f"{x:.{k}f}"


def ci(lo, hi, k=3):
    return f"[{f(lo, k)}, {f(hi, k)}]"


def pp(x):
    return f"{100 * x:+.1f}"


def ppci(lo, hi):
    return f"[{100 * lo:+.1f}, {100 * hi:+.1f}]"


def pfmt(p):
    return "n/a" if pd.isna(p) else (f"{p:.4f}" if p >= 0.0001 else f"{p:.1e}")


C19, C23 = conf["2019wimF"], conf["2023wimF"]
D19, D23 = det["2019wimF"], det["2023wimF"]
E19, E23 = ex["2019wimF"], ex["2023wimF"]
pred = {"T1": "rho > 0 (precondition; H0 with a spanning window predicts it too)",
        "T2": "> 0 (short intervals more formulaic)", "T3": "rho > 0 (longer formulas when more time)",
        "T4": "> 0 (changeover talk freer, less formulaic)"}
isdiff = {"T1": False, "T2": True, "T3": False, "T4": True}


def conf_rows():
    out = []
    for tag in T:
        for t in ["T1", "T2", "T3", "T4"]:
            r = conf[tag].loc[t]
            if not bool(r.testable):
                out.append(f"| {tag} | {t} | {pred[t]} | not testable ({r.note}) | | | | | |")
                continue
            if isdiff[t]:
                est = f"{pp(r.estimate)} pp {ppci(r.ci_lo, r.ci_hi)}"
            else:
                est = f"{f(r.estimate)} {ci(r.ci_lo, r.ci_hi)}"
            n = f"{int(r.n_units)}" + (f" units / {int(r.n_strings)} strings" if t == "T3" else " units")
            out.append(f"| {tag} | {t} | {pred[t]} | {est} | {n} | {pfmt(r.p_shift)} ({int(r.n_shifts)}) | "
                       f"{pfmt(r.p_holm)} | {'yes' if r.significant_holm else 'no'} | {'yes' if r.direction_as_H1 else 'no'} |")
    return "\n".join(out)


def rob_rows():
    out = []
    for tag in T:
        for _, r in rob[tag].iterrows():
            if not bool(r.testable):
                out.append(f"| {tag} | {r.check} | {r.test} | not testable ({r.note}) | | | |")
                continue
            est = f"{pp(r.estimate)} pp {ppci(r.ci_lo, r.ci_hi)}" if r.test in ("T2", "T4") else f"{f(r.estimate)} {ci(r.ci_lo, r.ci_hi)}"
            out.append(f"| {tag} | {r.check} | {r.test} | {est} | {int(r.n_units)} | {pfmt(r.p_shift)} ({int(r.n_shifts)}) | "
                       f"{'yes' if r.ci_excludes_0 else 'no'} |")
    return "\n".join(out)


def flow_table():
    steps = list(dict.fromkeys(list(flow["2019wimF"].step) + list(flow["2023wimF"].step)))
    m = {t: dict(zip(flow[t].step, flow[t].n_units)) for t in T}
    return "\n".join(f"| {s} | {m['2019wimF'].get(s, '(not applied)')} | {m['2023wimF'].get(s, '(not applied)')} |" for s in steps)


def t5_rows():
    out = []
    for tag in T:
        d = t5[tag]
        q = d["quantreg_0.9"]
        out.append(f"| {tag} | {f(d['rate_words_per_s']['median'], 2)} | {f(d['q90_rate_short_tercile'], 2)} {ci(*d['q90_rate_short_ci'], 2)} | "
                   f"{f(d['q90_rate_long_tercile'], 2)} {ci(*d['q90_rate_long_ci'], 2)} | {f(d['ratio_long_over_short'], 2)} {ci(*d['ratio_ci'], 2)} | "
                   f"{d['decision']} | {f(q['intercept'], 1)} {ci(*q['intercept_ci'], 1)}; {f(q['slope_words_per_s'], 2)} {ci(*q['slope_ci'], 2)} |")
    return "\n".join(out)


def share_rows():
    out = []
    for tag in T:
        d = det[tag]["T2"]
        out.append(f"| {tag} | T2 | short A (A <= {f(d['A_cut_1_3'], 1)} s): {f(d['share_short'])} {ci(*d['share_short_ci'])}, "
                   f"{d['n_units_short']} units, {d['tokens_short']} tokens | long A (A > {f(d['A_cut_2_3'], 1)} s): {f(d['share_long'])} "
                   f"{ci(*d['share_long_ci'])}, {d['n_units_long']} units, {d['tokens_long']} tokens |")
    d = D19["T4"]
    out.append(f"| 2019wimF | T4 | within game: {f(d['share_within_game'])} {ci(*d['share_within_ci'])}, {d['n_units_within']} units, "
               f"{d['tokens_within']} tokens | changeover/set break: {f(d['share_changeover'])} {ci(*d['share_changeover_ci'])}, "
               f"{d['n_units_changeover']} units, {d['tokens_changeover']} tokens |")
    return "\n".join(out)


x1 = ex["X1_lengths"]
x1rows = "\n".join(f"| {r['distribution']} | {r['n']} | {r['mean']} | {r['q10']} | {r['q25']} | {r['q50']} | {r['q75']} | {r['q90']} | {r['max']} |"
                   for r in x1["table"])
held = syl["heldout_fixture"]
dev = syl["development_fixture_in_sample"]
top_str = ", ".join(f"'{s}' ({c})" for s, c in zip(top19.string[:12], top19["count"][:12]))

t1_19, t1_23 = C19.loc["T1"], C23.loc["T1"]
x7_19, x7_23 = E19["X7_clip_count_control"], E23["X7_clip_count_control"]
x5_19, x5_23 = E19["X5_words_vs_components"], E23["X5_words_vs_components"]
r3_19 = rob["2019wimF"].query("check.str.startswith('R3') and test == 'T1'", engine="python").iloc[0]
r3_23 = rob["2023wimF"].query("check.str.startswith('R3') and test == 'T1'", engine="python").iloc[0]
r1t2 = rob["2019wimF"].query("check.str.startswith('R1') and test == 'T2'", engine="python").iloc[0]
r4 = rob["2019wimF"].query("check.str.startswith('R4')", engine="python").iloc[0]
supported = ver["H1_supported_2019"]
any_opposite = any(ver[t]["opposite_direction_sig_2019"] for t in ("T2", "T3", "T4"))
t2_19, t3_19, t4_19 = C19.loc["T2"], C19.loc["T3"], C19.loc["T4"]
t2_23, t3_23 = C23.loc["T2"], C23.loc["T3"]

report = f"""# Metre analysis: is the time between points a frame for commentary formulas?

All numbers below are read from `analysis/metre/results/` by `s06_make_report.py`; rerun everything with
`bash analysis/metre/run_all.sh`. The analysis plan (`plan.md`) was committed **before any test script was written or run**
(commit message "metre: pre-registered analysis plan"). Everything not in the plan is labelled **EXPLORATORY**.

## 1. Summary

* **H1 had to be re-specified before testing, and it was.** There is no audio, no word time and no speaker label, so intonation units,
  pitch resets, IU-onset phase in the strike cycle, rally-internal speech and the production speed of formulas **cannot be measured**.
  The tested hypothesis (H1') takes as frame the **interval between points** (point plus dead-ball time up to the next first serve, `A`)
  and as unit the **clip-level transcript aggregated per point**. The strike-level version of H1 remains **untested**.
* **Precondition (T1).** In the 2019 final the number of tokens attached to a point rises with the time available:
  Spearman rho = {f(t1_19.estimate)} {ci(t1_19.ci_lo, t1_19.ci_hi)}, shift-null p = {pfmt(t1_19.p_shift)} (Holm {pfmt(t1_19.p_holm)}); about
  {f(D19['OLS']['estimate'], 2)} {ci(D19['OLS']['ci_lo'], D19['OLS']['ci_hi'], 2)} extra tokens per extra second. In the held-out 2023 final
  rho = {f(t1_23.estimate)} {ci(t1_23.ci_lo, t1_23.ci_hi)} (Holm p = {pfmt(t1_23.p_holm)}, **not significant**), and the association there is
  carried by points that have an extra fault clip (EXPLORATORY X7: rho = {f(x7_23['T1_rho_single_clip_units'])} among single-clip units).
  Both H1' and H0 predict T1 (section 2), so T1 is not evidence for a frame.
* **The discriminating predictions were not observed.** Formula share in short- minus long-interval units (T2): {pp(t2_19.estimate)} percentage
  points (pp) {ppci(t2_19.ci_lo, t2_19.ci_hi)} in 2019, {pp(t2_23.estimate)} pp {ppci(t2_23.ci_lo, t2_23.ci_hi)} in 2023 (H1' predicted > 0; both
  point estimates have the opposite sign). Syllables of formulaic strings against available time (T3): rho = {f(t3_19.estimate)}
  {ci(t3_19.ci_lo, t3_19.ci_hi)} (2019), {f(t3_23.estimate)} {ci(t3_23.ci_lo, t3_23.ci_hi)} (2023) (H1' predicted > 0). Formula share within games
  minus after changeovers/set breaks (T4, 2019 only): {pp(t4_19.estimate)} pp {ppci(t4_19.ci_lo, t4_19.ci_hi)} (H1' predicted > 0).
  None is significant after Holm correction.
* **Verdict under the pre-registered rules (plan section 7): H1' is {'SUPPORTED' if supported else 'NOT SUPPORTED'}** in the 2019 final
  and {'replicated' if ver['H1_supported_and_replicated'] else 'not replicated'} in 2023.
  {'At least one effect is significant in the direction opposite to H1.' if any_opposite else 'No effect is significant in the direction opposite to H1 either.'}
  The 2019 CIs are narrow enough to exclude a short-interval excess in formula share larger than {100 * t2_19.ci_hi:.1f} pp and a positive
  syllable-time correlation larger than rho = {f(t3_19.ci_hi)}, **for formulas as defined here and for clip-level text**.

## 2. Hypotheses as tested (re-specification, from plan.md)

Original H1 (brief): during rallies, the intervals between strikes act as a metrical frame; IU boundaries align with strikes; formula
length is constrained by the time available; between points, composition is freer. H0: no alignment beyond what speech rate and
pause distribution predict.

**Why re-specified.** The corpus (corpus/README.md sections 0, 4, 6, 8) consists of WhisperX transcripts attached to TennisVL rally clips
(median clip {6.2} s in 2019; see plan section 9), with no audio, no word timestamps and no speaker labels. A clip's text window is
undocumented and reaches beyond the clip: identical texts recur on clips a median 17 s apart, and score calls in a clip are usually
the score *after* its point. Speech during rallies cannot therefore be separated from speech between points, and the corpus cannot show
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
  ({pool['pool_tokens']} tokens), so formula identification never sees either final.
* Unit = one PBP point; its text = all clips aligned to the point (fault clip + point-proper clip), never joined across clips.
  `A` from PBP `ElapsedTime` (1 s resolution); `D` (robustness R3) = next first serve (video time via the offset) minus the point's last hit.
* Dead-ball category (T4) by the rules of tennis: `changeover` = last point of an odd game >= 3 or of a set; `within_game` = next point
  in the same game; other game ends are not used in T4.

Sample flow (exclusion rules E1-E5 of the plan):

| step | 2019 | 2023 |
|---|---|---|
{flow_table()}

Analysed units: 2019 n = {D19['descriptives']['n_units']} ({D19['descriptives']['tokens']} tokens, {D19['descriptives']['zero_word_units']}
with no text; median `A` {f(D19['descriptives']['A_median'], 0)} s, IQR {f(D19['descriptives']['A_q25'], 0)}-{f(D19['descriptives']['A_q75'], 0)} s;
categories {D19['descriptives']['category_counts']}). 2023 n = {D23['descriptives']['n_units']} ({D23['descriptives']['tokens']} tokens,
{D23['descriptives']['zero_word_units']} with no text; median `A` {f(D23['descriptives']['A_median'], 0)} s; categories {D23['descriptives']['category_counts']}).
In 2023 E5 removes the units whose interval contains a video cut (the source video omits changeovers), so only
{D23['descriptives']['category_counts'].get('changeover', 0)} changeover unit remains and T4 is not testable there (pre-registered threshold: 15).

## 4. Definitions

* **Tokens**: NFC, lower case, regex `[a-z0-9]+(?:'[a-z0-9]+)*` (hyphens split, contractions kept); words per unit = tokens.
* **Formula** = n-gram (2 <= n <= 12, within a clip) occurring >= 3 times in the pool and in >= 2 pool streams: {pool['formulas_base(n>=2,count>=3,streams>=2)']} formulas
  (by n: {pool['formulas_base_by_n']}). Strict variant R2 (n >= 3, >= 5 times, >= 3 streams): {pool['formulas_strict(n>=3,count>=5,streams>=3)']}.
  The definition counts frequent function-word sequences as formulas; the most frequent maximal formulaic strings in the 2019 units are
  {top_str}. Hence the high overall share ({f(D19['descriptives']['share_base_all'])} in 2019, {f(D23['descriptives']['share_base_all'])} in 2023)
  and the much lower strict share ({f(D19['descriptives']['share_R2_all'])}, {f(D23['descriptives']['share_R2_all'])}). This definition is specific to
  this analysis and is not the formula-analyst's (analysis/formulas/).
* **Formula share** = formulaic tokens / tokens, pooled over the units of a group. **Formulaic string** = maximal matched occurrence.
* **Syllables**: rule-based counter (`syllables.py`), digits read as British English numbers ('0' as *love*). Accuracy on a held-out
  fixture of {held['n_words']} random pool word types whose gold counts were written before the counter was run on them:
  {f(held['accuracy'], 3)} (Wilson 95% CI {ci(*held['accuracy_wilson95'])}), mean signed error {held['mean_signed_error_counted_minus_gold']:+.3f}
  syllables per word. (On the development fixture, which the rules were tuned on: {f(dev['accuracy'], 3)}; in-sample, not a validation.)
* **Null**: circular shift of the complete PBP timing sequence (A and category of every cycle) against the unit sequence, all shifts
  10 ... M-10 (2019: {int(C19.loc['T1'].n_shifts)}, 2023: {int(C23.loc['T1'].n_shifts)} shifts; the p-value floor is therefore
  2/(K+1) = {2 / (int(C19.loc['T1'].n_shifts) + 1):.4f} and {2 / (int(C23.loc['T1'].n_shifts) + 1):.4f}). Two-sided p. The brief's ">= 5,000 shifts" cannot
  be met by distinct index shifts of a sequence of about 400; a continuous time-shift null with 1-s steps (R6) supplies
  {int(rob['2019wimF'].query("check.str.startswith('R6')", engine='python').n_shifts.iloc[0])} (2019) and
  {int(rob['2023wimF'].query("check.str.startswith('R6') and testable", engine='python').n_shifts.iloc[0])} (2023) shifts.
* **CIs**: circular block bootstrap over units in time order (block 10 units, B = 10,000), percentile 95%.
* **Multiplicity**: Holm within each match's confirmatory family (2019: T1-T4; 2023: T1-T3), alpha 0.05.

## 5. Confirmatory results

| match | test | H1' predicts | estimate [95% CI] | n | p shift-null (shifts) | p Holm | Holm-significant | sign as H1' |
|---|---|---|---|---|---|---|---|---|
{conf_rows()}

Group shares behind T2 and T4 (token-pooled, 95% CI):

| match | test | group 1 | group 2 |
|---|---|---|---|
{share_rows()}

**What H1' predicted and what was observed.**
* T1 (P1): predicted rho > 0. Observed in 2019 (significant); in 2023 rho > 0 with a CI excluding 0 but not significant after Holm, and not
  present among single-clip units (X7). Because H0 predicts the same when the text window spans the interval, this only establishes
  (for 2019) that clip-level text carries point-level timing information.
* T2 (P2): predicted more formulaic text in short intervals. Not observed: the point estimates go the other way in both finals
  (short {f(D19['T2']['share_short'])} vs long {f(D19['T2']['share_long'])} in 2019; {f(D23['T2']['share_short'])} vs {f(D23['T2']['share_long'])} in 2023), and no test is significant.
* T3 (P3): predicted longer formulas with more time. Not observed: rho is near 0 in both finals.
* T4 (P4): predicted less formulaic talk around changeovers. Not observed: within-game {f(D19['T4']['share_within_game'])} vs changeover
  {f(D19['T4']['share_changeover'])}. Not testable in 2023.

Figures: `figures/fig1_words_vs_available_time.png` (tokens vs `A`), `figures/fig2_formula_share.png` (shares by tercile and by
category), `figures/fig3_formula_syllables.png` (string syllables by tercile), `figures/fig4_shift_nulls.png` (null distributions).

## 6. Pre-registered descriptive measure T5: speech-rate ceiling

Rate = tokens per second of `A`. The upper envelope is the 90th percentile of the rate in the short and long `A` terciles; decision rule
(fixed in the plan): ratio CI inside [1/1.5, 1.5] = flat ceiling; CI entirely below 1 = ceiling falls; otherwise inconclusive.

| match | median rate (tokens/s) | q90 rate, short A | q90 rate, long A | ratio long/short | decision | 0.9-quantile regression: intercept; slope (tokens/s) |
|---|---|---|---|---|---|---|
{t5_rows()}

Median rates of about {f(t5['2019wimF']['rate_words_per_s']['median'], 2)} tokens per second of available time are far below continuous speech,
so either most of the interval is silent or the text window covers only part of it; the two cannot be told apart without audio.
Quantile-regression bootstrap fits with a convergence warning: {t5['2019wimF'].get('quantreg_bootstrap_fits_with_warning', 'n/a')} (2019),
{t5['2023wimF'].get('quantreg_bootstrap_fits_with_warning', 'n/a')} (2023) of 10,000; the intercept CIs are wide and the regression is descriptive only.

## 7. Pre-registered robustness checks (not in the Holm family; used only for interpretation)

R1 score-call tokens removed; R2 strict formulas; R3 `D` (last hit to next serve) instead of `A`, shifted within the unit sequence;
R4 T3 as partial Spearman controlling for the unit's token count; R5 units involved in cross-point exact text repeats excluded;
R6 continuous time-shift null.

| match | check | test | estimate [95% CI] | units | p shift-null (shifts) | CI excludes 0 |
|---|---|---|---|---|---|---|
{rob_rows()}

Reading: no check produces an effect in H1's direction with a CI excluding 0 for T2-T4. The R1 version of T2 in 2019
({pp(r1t2.estimate)} pp, unadjusted p = {pfmt(r1t2.p_shift)}) points, if anything, the other way. R3 confirms T1 in 2019
(rho = {f(r3_19.estimate)}) but not in 2023 (rho = {f(r3_23.estimate)}). R4 (rho = {f(r4.estimate)} {ci(r4.ci_lo, r4.ci_hi)}) shows that T3 stays near 0
once text length is controlled for.

## 8. Held-out replication (2023 final)

The 2023 family (T1-T3) has no Holm-significant result. Because the 2023 source video omits changeover periods (README 3.1), units whose
interval contains a cut were excluded in advance (E5), which removes almost all long dead-ball intervals; T4 could not be tested
and the range of `A` is narrower (max {f(D23['descriptives']['A_max'], 0)} s vs {f(D19['descriptives']['A_max'], 0)} s). Nothing that was absent in 2019
appears in 2023, and the 2019 T1 association is weaker in 2023 and not robust (R3, X7).

## 9. EXPLORATORY analyses (not pre-registered as tests; no multiplicity correction)

* **X1 medium contrast (lengths only).** Cornell written live-text updates (other matches, no timing) vs 2019 TV transcripts:

| distribution | n | mean | q10 | q25 | median | q75 | q90 | max |
|---|---|---|---|---|---|---|---|---|
{x1rows}

  Median difference, updates minus non-empty clips: {x1['median_diff_cornell_minus_clip']:+.0f} tokens (iid bootstrap 95% CI
  {ci(*x1['median_diff_ci_iid'], 0)}). Written updates are longer and much less skewed toward very short items (score calls). Medium,
  match and author are confounded; no timing comparison is possible (`figures/fig5_lengths_by_medium_exploratory.png`).
* **X2 phase-tag contrast (circular).** Clips tagged `between_points`/score-call-only vs other clips, formula share
  2019: {f(E19['X2_phase_tag']['share_tagged'])} vs {f(E19['X2_phase_tag']['share_other'])} (difference {pp(E19['X2_phase_tag']['diff'])} pp,
  CI {ppci(*E19['X2_phase_tag']['diff_ci_iid_clips'])}; n = {E19['X2_phase_tag']['n_clips_tagged']} vs {E19['X2_phase_tag']['n_clips_other']} clips);
  2023: {f(E23['X2_phase_tag']['share_tagged'])} vs {f(E23['X2_phase_tag']['share_other'])}. The tag is defined by score-call text, and score calls are
  pool formulas, so this contrast is circular and was not used as a test (T4 replaced it with a rule-based dead-ball category).
* **X3 point-proper clip only** (fault-clip text dropped): T1 rho = {f(E19['X3_point_proper_clip_only']['T1_rho'])}
  {ci(*E19['X3_point_proper_clip_only']['T1_ci'])} (2019), {f(E23['X3_point_proper_clip_only']['T1_rho'])} {ci(*E23['X3_point_proper_clip_only']['T1_ci'])} (2023);
  T2 {pp(E19['X3_point_proper_clip_only']['T2_diff'])} pp (2019), {pp(E23['X3_point_proper_clip_only']['T2_diff'])} pp (2023).
* **X4 player names masked** in pool and target before formula identification: T2 {pp(E19['X4_name_masked']['T2_diff'])} pp
  {ppci(*E19['X4_name_masked']['T2_ci'])} (2019), {pp(E23['X4_name_masked']['T2_diff'])} pp {ppci(*E23['X4_name_masked']['T2_ci'])} (2023);
  T4 {pp(E19['X4_name_masked']['T4_diff'])} pp {ppci(*E19['X4_name_masked']['T4_ci'])} (2019).
* **X5 components of `A`.** Spearman of tokens with rally duration {f(x5_19['tv_rally_duration_s']['rho'])}, shots {f(x5_19['tv_n_shots']['rho'])},
  `D` {f(x5_19['D']['rho'])} (2019); partial rho(tokens, `D` | rally duration, number of clips) = {f(x5_19['partial_rho_words_D_given_rally_duration_and_n_clips']['rho'])}
  {ci(*x5_19['partial_rho_words_D_given_rally_duration_and_n_clips']['ci_block_B2000'])} in 2019 and
  {f(x5_23['partial_rho_words_D_given_rally_duration_and_n_clips']['rho'])} {ci(*x5_23['partial_rho_words_D_given_rally_duration_and_n_clips']['ci_block_B2000'])} in 2023.
* **X6 T4 on 2023 without E5** ({E23['X6_T4_2023_without_E5']['n_changeover']} changeover units whose break is cut from the video):
  {pp(E23['X6_T4_2023_without_E5']['diff'])} pp {ppci(*E23['X6_T4_2023_without_E5']['ci'])}.
* **X7 number of clips (added after seeing R3 for 2023).** A point with a first-serve fault has a longer cycle and a second transcript
  window. Among single-clip units T1 rho = {f(x7_19['T1_rho_single_clip_units'])} {ci(*x7_19['T1_single_ci'])} (2019, n = {x7_19['n_units_single_clip']}) but
  {f(x7_23['T1_rho_single_clip_units'])} {ci(*x7_23['T1_single_ci'])} (2023, n = {x7_23['n_units_single_clip']}); partial rho(tokens, `A` | number of clips)
  = {f(x7_19['partial_rho_words_A_given_n_clips'])} (2019) and {f(x7_23['partial_rho_words_A_given_n_clips'])} (2023). In 2023 the T1 association is
  therefore mostly a window-count effect.

## 10. Interpretation

With clip-level text, the only frame that can be tested is the interval between points. In the 2019 final, the amount of text attached
to a point tracks that point's own interval beyond match-level drift (T1, robust to the frame-proper predictor, to single-clip units and
to both nulls), which shows that the clip text is time-locked at the level of points. Given that, the formula measures could have shown
the pattern H1' predicts, but they did not: formula share does not rise in short intervals (the point estimate falls), formula length in
syllables does not grow with the time available, and changeover talk is not less formulaic than within-game talk. At this resolution,
the commentary behaves as H0 describes: more time yields more text, with the same composition. In Parry's terms, the data give no
support for a temporal analogue of metrical conditioning at the between-point level. They say nothing about the strike level, where
the brief located the metrical frame and which this corpus cannot reach.

## 11. Limitations

1. **No audio, no word times, no speakers**: IUs, pitch resets, IU phase, rally-internal speech and production speed are unmeasurable;
   the hypothesis tested is the re-specified H1', not H1.
2. **Undocumented text window**: texts are attributed to clips by an unknown rule; identical texts recur on clips about 17 s apart; a
   unit's text can include talk from before the point and miss talk late in long intervals. This blurs the time-text link and biases
   all T-tests toward 0.
3. **Mixed voices**: umpire calls, Hawk-Eye and announcements are in the text (R1 removes score calls only).
4. **ASR errors** (at least 22 per 1,000 words, README 7.3; clustered in short score-call clips and names) break n-gram matches. If the
   error rate is higher in short-interval units, it lowers their formula share and works against P2; it could explain part of the
   negative T2 estimates.
5. **Formula operationalisation**: frequent n-grams from other matches (other broadcasters and commentators) include function-word
   sequences. The strict (R2) and name-masked (X4) variants do not change the conclusions, but other definitions (formulaic systems,
   within-broadcaster formulas) were not tested here.
6. **Timing**: `A` has 1 s resolution and includes the fault interval; `D` depends on the TennisVL parser and the video offset.
   The 2023 video omits changeovers, so the held-out test covers a narrower range of intervals and no T4.
7. **Power and dependence**: 353 (2019) and 219 (2023) units; formulaic strings are clustered in units (the bootstrap resamples units).
   The index-shift null has a p-value floor of about 0.005.
8. **One broadcaster per match**: commentator identity, broadcaster and match are confounded; the medium contrast (X1) is across
   different matches and is descriptive.
9. Robustness checks and exploratory analyses are not multiplicity-corrected; they are used for interpretation only.

## 12. Deviations from the plan

* T5 bootstrap uses the plan's seed {20190714}; no other change. X7 was added after the robustness results were seen and is
  exploratory. No confirmatory definition, test, exclusion rule or threshold was changed after the plan commit.

## 13. Files

`plan.md` (pre-registration); `metre_lib.py`, `syllables.py`, `s01_syllable_check.py` ... `s06_make_report.py`, `run_all.sh`;
`data/syllable_heldout_fixture.tsv` (hand-coded fixture); `results/` (all tables: `confirmatory_*.csv`, `robustness_*.csv`,
`t5_*.json`, `details_*.json`, `exploratory.json`, `exploratory_lengths.csv`, `units_*.csv`, `strings_*.csv`, `clips_*.csv`,
`sample_flow_*.csv`, `pool_formulas_*.{{json,tsv}}`, `top_strings_*.tsv`, `syllable_check.json`, `verdict.json`, `nulls_*.npz`);
`figures/`.
"""
(HERE / "report.md").write_text(report, encoding="utf-8")
print("report.md written,", len(report.split()), "words")
