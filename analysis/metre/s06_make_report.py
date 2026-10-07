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
wd = json.load(open(RES / "window_diagnostics.json"))
_s19 = pd.read_csv(RES / "strings_2019wimF.csv").query("variant == 'base'")
bigram_share_19 = float((_s19.ntok == 2).mean())
from metre_lib import SEED, RP  # noqa: E402
from s03_confirmatory import B as B_BOOT, L_BLOCK  # noqa: E402

# ---- POST HOC results (plan.md Addendum 1)
ph = json.load(open(RES / "posthoc.json"))
mde_t = pd.read_csv(RES / "posthoc_mde.csv")
sens = pd.read_csv(RES / "posthoc_sensitivity.csv")
asr = json.load(open(RP / "asr_proxy.json"))["hand_sample"]
umc = ph["PH6_umpire_check"]


def mde_row(tag, test, mix=0.0, alpha="alpha05"):
    return mde_t[(mde_t.match == tag) & (mde_t.test == test) & (mde_t.mix == mix) & (mde_t.alpha_label == alpha)].iloc[0]


def mde_fmt(tag, test, mix=0.0, alpha="alpha05", kind="mde_true", rho_prefix=False):
    r = mde_row(tag, test, mix, alpha)
    v = r[kind]
    if pd.isna(v):
        if kind == "mde_measured":
            return "not reached"
        gm = r.grid_max_true_effect
        return (f"> {100 * gm:.1f} pp" if test != "T3" else f"rho > {gm:.2f}") + " (beyond the simulated range)"
    if test == "T3":
        return f"rho = {v:.3f}" if rho_prefix else f"{v:.3f}"
    return f"{100 * v:.1f} pp"


def mde_pair(tag, test):
    return f"{mde_fmt(tag, test, rho_prefix=True)} / {mde_fmt(tag, test, alpha='alpha_holm1')}"


A_H = {t: float(mde_t[(mde_t.match == t) & (mde_t.alpha_label == "alpha_holm1")].alpha.iloc[0]) for t in T}
MDE_TESTS = {t: [x for x in ["T2", "T3", "T4"] if ((mde_t.match == t) & (mde_t.test == x)).any()] for t in T}
mde_sum = "; ".join(f"{tag[:4]}: " + ", ".join(f"{x} {mde_pair(tag, x)}" for x in MDE_TESTS[tag]) for tag in T)
mde_half19 = ", ".join(f"{x} {mde_fmt('2019wimF', x, 0.5, rho_prefix=True)}" for x in MDE_TESTS["2019wimF"])
_z = mde_t[(mde_t.mix == 0) & (mde_t.alpha_label == "alpha05")]
size_lo, size_hi = float(_z.size_at_zero_effect.min()), float(_z.size_at_zero_effect.max())
_r = []
for tag in T:
    for x in MDE_TESTS[tag]:
        a0, a5 = mde_row(tag, x, 0.0).mde_true, mde_row(tag, x, 0.5).mde_true
        if pd.notna(a0) and pd.notna(a5):
            _r.append(a5 / a0)
ratio_lo, ratio_hi = min(_r), max(_r)


def mde_table():
    out = []
    for tag in T:
        for x in MDE_TESTS[tag]:
            for al in ("alpha05", "alpha_holm1"):
                r0 = mde_row(tag, x, 0.0, al)
                out.append(f"| {tag} | {x} | {r0.alpha:.4f} | {mde_fmt(tag, x, 0.0, al)} | {mde_fmt(tag, x, 0.25, al)} | "
                           f"{mde_fmt(tag, x, 0.5, al)} | {mde_fmt(tag, x, 0.5, al, kind='mde_measured')} | {r0.size_at_zero_effect:.3f} |")
    return "\n".join(out)


PH3 = {t: ph[t]["PH3_T1_within_category"] for t in T}
PH4 = {t: ph[t]["PH4_A_range"] for t in T}
PH5 = {t: ph[t]["PH5_serial_correlation"] for t in T}
ph5_ratios = [v["ratio_shift_over_perm"] for t in T for v in PH5[t]["tests"].values()]
ph5_p = [(t, k, v["p_shift"], v["p_perm"]) for t in T for k, v in PH5[t]["tests"].items()]
ph5_flip = [f"{t} {k}" for t, k, a, b in ph5_p if (a < 0.05) != (b < 0.05)]


def wg(t, extra=""):
    r = PH3[t]["T1_within_game_units"]
    return f"{f(r['estimate'])} {ci(r['ci_lo'], r['ci_hi'])} (n = {r['n_units']}, shift-null p = {pfmt(r['p_shift'])}{extra})"


def wg_state(t):
    r = PH3[t]["T1_within_game_units"]
    return "weaker but its CI excludes 0" if r["ci_lo"] > 0 else "weaker and cannot be distinguished from 0"



def range_rows():
    return "\n".join(f"| {t} | {PH4[t]['n_units']} | {f(PH4[t]['min'], 0)} | {f(PH4[t]['q10'], 0)} | {f(PH4[t]['median'], 0)} | "
                     f"{f(PH4[t]['q90'], 0)} | {f(PH4[t]['max'], 0)} | {PH4[t]['n_units_A_over_100s']} | {PH4[t]['n_changeover_units']} |"
                     for t in T)


def sens_rows(prefix):
    out = []
    for _, r in sens[sens.check.str.startswith(prefix)].iterrows():
        if not bool(r.testable):
            out.append(f"| {r.match} | {r.check} | {r.test} | not testable ({int(r.n_changeover_units)} changeover units) | | | | |")
            continue
        est = f"{pp(r.estimate)} pp {ppci(r.ci_lo, r.ci_hi)}" if r.test in ("T2", "T4") else f"{f(r.estimate)} {ci(r.ci_lo, r.ci_hi)}"
        out.append(f"| {r.match} | {r.check} | {r.test} | {est} | {int(r.n_units)} | {int(r.tokens)} | {pfmt(r.p_shift)} ({int(r.n_shifts)}) | "
                   f"{'yes' if r.ci_excludes_0 else 'no'} |")
    return "\n".join(out)


ph6 = sens[sens.check.str.startswith("PH6") & sens.testable.astype(bool)]
ph6_excl = ph6[ph6.ci_excludes_0.astype(bool)]
ph6_text = ("no umpire-masked estimate has a CI excluding 0" if len(ph6_excl) == 0 else
            "CIs excluding 0: " + "; ".join(f"{r.match} {r.variant} {r.test} ({r.estimate:+.3f}, "
                                            f"{'H1 direction' if r.estimate > 0 else 'opposite to H1'})" for _, r in ph6_excl.iterrows()))
ph4r = sens[sens.check.str.startswith("PH4")].set_index("test")


def f(x, k=3):
    return "n/a" if x is None or (isinstance(x, float) and pd.isna(x)) else f"{x:.{k}f}"


def ci(lo, hi, k=3):
    return f"[{f(lo, k)}, {f(hi, k)}]"


def pp(x):
    return f"{100 * x:+.1f}"


def ppci(lo, hi):
    return f"[{100 * lo:+.1f}, {100 * hi:+.1f}]"


def cats(d):
    c = d["descriptives"]["category_counts"]
    return f"{c.get('within_game', 0)} within-game, {c.get('changeover', 0)} changeover/set-break, {c.get('other_game_end', 0)} other game-end units"


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
                out.append(f"| {tag} | {t} | {pred[t]} | {r.note} | | | | | |")
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
flag_rows = []
for tag in T:
    for _, r in rob[tag].iterrows():
        if bool(r.testable) and r.test in ("T2", "T3", "T4") and (bool(r.ci_excludes_0) or r.p_shift < 0.05):
            val = f"{pp(r.estimate)} pp" if r.test in ("T2", "T4") else f"rho = {f(r.estimate)}"
            flag_rows.append(f"{tag} {r.check.split(' ')[0]} {r.test} ({val}, CI {ppci(r.ci_lo, r.ci_hi) if r.test in ('T2', 'T4') else ci(r.ci_lo, r.ci_hi)}, "
                             f"unadjusted p = {pfmt(r.p_shift)}; {'H1 direction' if r.estimate > 0 else 'opposite to H1'})")
n_h1dir = sum("H1 direction" in x for x in flag_rows)
flag_text = ("; ".join(flag_rows)) if flag_rows else "none"
any_opposite = any(ver[t]["opposite_direction_sig_2019"] for t in ("T2", "T3", "T4"))
t2_19, t3_19, t4_19 = C19.loc["T2"], C19.loc["T3"], C19.loc["T4"]
t2_23, t3_23 = C23.loc["T2"], C23.loc["T3"]
r2_19 = rob["2019wimF"][rob["2019wimF"].check.str.startswith("R2")].set_index("test")

ci_below_mde = all(C19.loc[x].ci_hi < mde_row("2019wimF", x).mde_true for x in MDE_TESTS["2019wimF"])
size_ok = 0.015 <= size_lo and size_hi <= 0.035
ph4_null = all((ph4r.loc[x].ci_lo <= 0) and (ph4r.loc[x].ci_hi >= 0) for x in ("T2", "T3"))

report = f"""# Metre analysis: is the time between points a frame for commentary formulas?

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
  Spearman rho = {f(t1_19.estimate)} {ci(t1_19.ci_lo, t1_19.ci_hi)}, shift-null p = {pfmt(t1_19.p_shift)} (Holm {pfmt(t1_19.p_holm)}); about
  {f(D19['OLS']['estimate'], 2)} {ci(D19['OLS']['ci_lo'], D19['OLS']['ci_hi'], 2)} extra tokens per extra second (OLS slope, secondary; shift-null
  p = {pfmt(D19['OLS']['p_shift'])}). Part of this association lies **between** dead-ball categories: changeover/set-break units carry a
  median of {f(PH3['2019wimF']['median_tokens_by_category']['changeover'], 0)} tokens against {f(PH3['2019wimF']['median_tokens_by_category']['within_game'], 0)} within games. **Within** within-game units, rho =
  {wg('2019wimF', '; POST HOC, section 10.2')}, which is {wg_state('2019wimF')}. In the held-out 2023 final,
  rho = {f(t1_23.estimate)} {ci(t1_23.ci_lo, t1_23.ci_hi)} (Holm p = {pfmt(t1_23.p_holm)}, **not significant**). Within games there it is
  {wg('2023wimF')}, and the association is carried by points that have an extra fault clip (EXPLORATORY X7: rho =
  {f(x7_23['T1_rho_single_clip_units'])} among single-clip units).
  **T1 is consistent with H0 as well as with H1'**: a constant speech rate inside a text window that spans the interval
  produces it. It shows only that clip-level text carries some point-level timing information, and it is not evidence for a frame (section 2).
* **The discriminating predictions were not observed.** Formula share in short- minus long-interval units (T2): {pp(t2_19.estimate)} percentage
  points (pp) {ppci(t2_19.ci_lo, t2_19.ci_hi)} in 2019, {pp(t2_23.estimate)} pp {ppci(t2_23.ci_lo, t2_23.ci_hi)} in 2023 (H1' predicted > 0; both
  point estimates have the opposite sign). Syllables of formulaic strings against available time (T3): rho = {f(t3_19.estimate)}
  {ci(t3_19.ci_lo, t3_19.ci_hi)} (2019), {f(t3_23.estimate)} {ci(t3_23.ci_lo, t3_23.ci_hi)} (2023) (H1' predicted > 0). Formula share within games
  minus after changeovers/set breaks (T4, 2019 only): {pp(t4_19.estimate)} pp {ppci(t4_19.ci_lo, t4_19.ci_hi)} (H1' predicted > 0).
  None is significant after Holm correction. The base formula share ({f(D19['descriptives']['share_base_all'])} in 2019) is carried by common
  bigrams such as 'in the'. With the **strict** definition (R2: n >= 3, >= 5 pool occurrences in >= 3 pool streams; share
  {f(D19['descriptives']['share_R2_all'])}), the 2019 estimates are T2 {pp(r2_19.loc['T2'].estimate)} pp {ppci(r2_19.loc['T2'].ci_lo, r2_19.loc['T2'].ci_hi)},
  T3 rho = {f(r2_19.loc['T3'].estimate)} {ci(r2_19.loc['T3'].ci_lo, r2_19.loc['T3'].ci_hi)} and T4 {pp(r2_19.loc['T4'].estimate)} pp {ppci(r2_19.loc['T4'].ci_lo, r2_19.loc['T4'].ci_hi)}.
  With umpire-pattern tokens removed (POST HOC, section 10.5), {ph6_text}.
* **Verdict under the pre-registered rules (plan section 7): H1' is {'SUPPORTED' if supported else 'NOT SUPPORTED'}** in the 2019 final.
  {'At least one confirmatory effect is Holm-significant in the direction opposite to H1.' if any_opposite else 'No confirmatory effect is Holm-significant in the direction opposite to H1 either.'}
  The held-out 2023 final is **not a comparable-range replication**. The 2023 source video omits the changeovers, so the analysed 2023 intervals span
  `A` = {f(PH4['2023wimF']['min'], 0)}-{f(PH4['2023wimF']['max'], 0)} s, with {PH4['2023wimF']['n_changeover_units']} changeover unit and {PH4['2023wimF']['n_units_A_over_100s']} units over 100 s. In 2019 the range is
  {f(PH4['2019wimF']['min'], 0)}-{f(PH4['2019wimF']['max'], 0)} s, with {PH4['2019wimF']['n_changeover_units']} changeover units and {PH4['2019wimF']['n_units_A_over_100s']} over 100 s. In 2023, T4 is not testable,
  and T2 and T3 are null over the narrower range ({'Holm-significant result present' if ver['H1_supported_and_replicated'] else 'no Holm-significant result'}).
* **What "not detected" can and cannot mean (revised after the critic review: POST HOC, plan Addendum 1, PH1-PH2).**
  The 2019 95% CIs exclude a short-minus-long excess in formula share above {pp(t2_19.ci_hi)} pp (T2), a syllable-time
  correlation above rho = {f(t3_19.ci_hi)} (T3) and a within-game minus changeover excess above {pp(t4_19.ci_hi)} pp (T4).
  These bounds hold **for the effect as measured**: clip-level text attributed to points, ASR text, and the formula
  definition of section 4. They do not bound the true effect. The text window is undocumented, so part of each unit's
  text belongs to neighbouring intervals, and ASR errors break n-gram matches. Both attenuate a true effect towards 0, so
  **the true effect could be larger than these bounds**, by an unknown factor. The minimum detectable effects (MDE; 80%
  power, simulated at the observed N with the shift-null test, at alpha = 0.05 / at the first Holm step alpha/m) are
  {mde_sum} (section 10.1).
  {'All three 2019 CI bounds lie below the MDEs, because the point estimates are near or below 0.' if ci_below_mde else 'Not every 2019 CI bound lies below its MDE.'}
  In an illustrative scenario where half of each unit's text comes from the neighbouring intervals, the true effects needed
  at alpha = 0.05 in 2019 rise to {mde_half19}. "Not detected" therefore means that measured effects as large as the MDEs
  would probably have been found{' and are excluded by the 2019 CIs' if ci_below_mde else ''}. It does not exclude smaller true effects, effects hidden by
  attenuation, or a frame at the strike level, which this corpus cannot reach.

## 2. Hypotheses as tested (re-specification, from plan.md)

Original H1 (brief): during rallies, the intervals between strikes act as a metrical frame; IU boundaries align with strikes; formula
length is constrained by the time available; between points, composition is freer. H0: no alignment beyond what speech rate and
pause distribution predict.

**Why re-specified.** The corpus (corpus/README.md sections 0, 4, 6, 8) consists of WhisperX transcripts attached to TennisVL rally clips
(median clip {wd['2019wimF']['median_clip_duration_s']} s in 2019, starting a median {wd['2019wimF']['median_first_hit_minus_clip_start_s']} s before the
first hit and ending {wd['2019wimF']['median_clip_end_minus_last_hit_s']} s after the last), with no audio, no word timestamps and no speaker labels.
A clip's text window is undocumented and reaches beyond the clip: {wd['2019wimF']['n_exact_repeat_clips']} clips repeat the text of an earlier
clip that ended a median {wd['2019wimF']['median_gap_source_clip_end_to_repeat_clip_start_s']} s before they start (2023:
{wd['2023wimF']['n_exact_repeat_clips']} clips, {wd['2023wimF']['median_gap_source_clip_end_to_repeat_clip_start_s']} s), and score calls in a clip are
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

* In-sample: `tv_2019wimF`; held-out: `tv_2023wimF`; field `text_corrected`. Formula reference: the {pool['pool_streams']} `tv_pool_*` streams only
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
{cats(D19)}). 2023 n = {D23['descriptives']['n_units']} ({D23['descriptives']['tokens']} tokens,
{D23['descriptives']['zero_word_units']} with no text; median `A` {f(D23['descriptives']['A_median'], 0)} s; {cats(D23)}).
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
* **CIs**: circular block bootstrap over units in time order (block {L_BLOCK} units, B = {B_BOOT:,}), percentile 95%.
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
* T1 (P1): predicted rho > 0. Observed in 2019 (significant; OLS slope {f(D19['OLS']['estimate'], 2)} {ci(D19['OLS']['ci_lo'], D19['OLS']['ci_hi'], 2)}
  tokens per second, p = {pfmt(D19['OLS']['p_shift'])}; 2023: {f(D23['OLS']['estimate'], 2)} {ci(D23['OLS']['ci_lo'], D23['OLS']['ci_hi'], 2)}, p = {pfmt(D23['OLS']['p_shift'])}). In 2023, rho > 0 with a CI excluding 0, but it is not significant after Holm and is
  not present among single-clip units (X7). Within within-game units (POST HOC, section 10.2), rho = {wg('2019wimF')} in 2019, so
  the association is partly between categories. H0 predicts the same pattern when the text window spans the interval, so T1 is
  consistent with H0 as well as with H1'. It establishes only, for 2019, that clip-level text carries some point-level timing information.
* T2 (P2): predicted more formulaic text in short intervals. Not observed: the point estimates go the other way in both finals
  (short {f(D19['T2']['share_short'])} vs long {f(D19['T2']['share_long'])} in 2019; {f(D23['T2']['share_short'])} vs {f(D23['T2']['share_long'])} in 2023), and no test is significant.
* T3 (P3): predicted longer formulas with more time. Not observed: rho is near 0 in both finals.
* T4 (P4): predicted less formulaic talk around changeovers. Not observed: within-game {f(D19['T4']['share_within_game'])} vs changeover
  {f(D19['T4']['share_changeover'])}. Not testable in 2023.

Figures: `figures/fig1_words_vs_available_time.png` (tokens vs `A`), `figures/fig2_formula_share.png` (shares by tercile and by
category), `figures/fig3_formula_syllables.png` (distribution of string syllables by tercile), `figures/fig4_shift_nulls.png` (null distributions).

## 6. Pre-registered descriptive measure T5: speech-rate ceiling

Rate = tokens per second of `A`. The upper envelope is the 90th percentile of the rate in the short and long `A` terciles; decision rule
(fixed in the plan): ratio CI inside [1/1.5, 1.5] = flat ceiling; CI entirely below 1 = ceiling falls; otherwise inconclusive.

| match | median rate (tokens/s) | q90 rate, short A | q90 rate, long A | ratio long/short | decision | 0.9-quantile regression: intercept; slope (tokens/s) |
|---|---|---|---|---|---|---|
{t5_rows()}

Median rates of about {f(t5['2019wimF']['rate_words_per_s']['median'], 2)} tokens per second of available time are far below continuous speech,
so either most of the interval is silent or the text window covers only part of it; the two cannot be told apart without audio.
Quantile-regression bootstrap fits with a convergence warning: {t5['2019wimF'].get('quantreg_bootstrap_fits_with_warning', 'n/a')} (2019),
{t5['2023wimF'].get('quantreg_bootstrap_fits_with_warning', 'n/a')} (2023) of {B_BOOT:,}; the intercept CIs are wide and the regression is descriptive only.

## 7. Pre-registered robustness checks (not in the Holm family; used only for interpretation)

R1 score-call tokens removed; R2 strict formulas; R3 `D` (last hit to next serve) instead of `A`, shifted within the unit sequence;
R4 T3 as partial Spearman controlling for the unit's token count; R5 units involved in cross-point exact text repeats excluded;
R6 continuous time-shift null.

| match | check | test | estimate [95% CI] | units | p shift-null (shifts) | CI excludes 0 |
|---|---|---|---|---|---|---|
{rob_rows()}

Reading: checks on T2-T4 with a CI excluding 0 or an unadjusted p < 0.05: {flag_text}. {'None of them is in the direction H1 predicts' if n_h1dir == 0 else str(n_h1dir) + ' of them in the direction H1 predicts'};
these are uncorrected secondary analyses and are not evidence for the opposite hypothesis either, but they give no sign of an H1 effect
masked in the primary analysis. R3 confirms T1 in 2019 (rho = {f(r3_19.estimate)}) but not in 2023 (rho = {f(r3_23.estimate)}). R4
(rho = {f(r4.estimate)} {ci(r4.ci_lo, r4.ci_hi)}) shows that T3 stays near 0 once the unit's text length is controlled for.

## 8. Held-out replication (2023 final): not a comparable-range replication

The 2023 family (T1-T3) has no Holm-significant result. The 2023 source video omits the changeover periods (README 3.1), so
units whose interval contains a cut were excluded in advance (E5). This removes almost all long dead-ball intervals. The
2023 test therefore covers a narrower and differently composed range of `A`: {f(PH4['2023wimF']['min'], 0)}-{f(PH4['2023wimF']['max'], 0)} s
(q90 {f(PH4['2023wimF']['q90'], 0)} s, {PH4['2023wimF']['n_changeover_units']} changeover unit), against {f(PH4['2019wimF']['min'], 0)}-{f(PH4['2019wimF']['max'], 0)} s in 2019 (q90 {f(PH4['2019wimF']['q90'], 0)} s,
{PH4['2019wimF']['n_changeover_units']} changeover units). Table and checks: section 10.3. The result for 2023 is read as follows. **T4 cannot be tested at a comparable range**;
T2 and T3 are null over the narrower range; and the 2019 T1 association is weaker in 2023 and not robust (R3, X7).
Nothing that was absent in 2019 appears in 2023.

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

## 10. POST HOC analyses after the critic review (plan.md Addendum 1; not pre-registered, outside every Holm family)

### 10.1 Minimum detectable effects of T2-T4 (PH2)

The method was fixed in the addendum before it was run. Each admissible index shift k0 of the primary null is taken in
turn as the true timing ({ph['2019wimF']['mde_setup']['n_base_shifts']} bases in 2019, {ph['2023wimF']['mde_setup']['n_base_shifts']} in 2023). This keeps N, the text, the
formula coverage and the serial structure of both sequences, and it breaks the real alignment. An effect is then planted.
For T2 and T4, each unit's formula share is shifted by +d/2 in group 1 and -d/2 in group 2. For T3, a Gaussian copula
links string syllables to the unit's `A`, with the syllable distribution preserved. The confirmatory statistic is tested
against the shift null formed by the other admissible shifts (at least {ph['2019wimF']['mde_setup']['null_shifts_per_base_min']} per base in 2019,
{ph['2023wimF']['mde_setup']['null_shifts_per_base_min']} in 2023). Power is the share of bases with p < alpha in the H1' direction. The MDE is the effect with
{ph['2019wimF']['mde_setup']['power_target']:.0%} power, found by linear interpolation. "True" means the planted effect in the text of the unit's own interval.
"Measured" means the expected value of the test statistic. In the misattribution scenarios (illustrative, not estimates),
a fraction of {' or '.join(f'{m:.2f}' for m in ph['2019wimF']['mde_setup']['mix_scenarios'] if m > 0)} of each unit's text comes from the two neighbouring units. ASR noise is not simulated, because no
WER is available. Power at zero effect, the empirical one-directional size, is {size_lo:.3f}-{size_hi:.3f} at alpha = 0.05
against a nominal 0.025{', so the shift-null test is calibrated' if size_ok else '; the test is not well calibrated'}. Power curves: `figures/fig6_power_curves_posthoc.png`.

| match | test | alpha | MDE, no misattribution (true = measured) | MDE true, misattribution 0.25 | MDE true, misattribution 0.50 | MDE measured, misattribution 0.50 | size at zero effect |
|---|---|---|---|---|---|---|---|
{mde_table()}

Reading. With misattribution, the measured MDE stays about the same, because the test sees the same statistic. The true
effect needed grows: at misattribution 0.50 it is {ratio_lo:.2f}-{ratio_hi:.2f} times the true MDE without misattribution,
where both are within the simulated range. {'The 2019 CI bounds in section 1 are smaller than these MDEs, because the point estimates are near or below 0.' if ci_below_mde else 'Not every 2019 CI bound in section 1 is smaller than its MDE.'}
The CIs bound the measured effect in these data; the MDEs describe what the design could detect.

### 10.2 T1 within dead-ball categories (PH3)

| match | all units | within-game units | units with text | median tokens: within game / other game end / changeover | median `A` (s): within game / changeover |
|---|---|---|---|---|---|
| 2019wimF | {f(PH3['2019wimF']['T1_all_units']['rho'])} {ci(*PH3['2019wimF']['T1_all_units']['ci'])} (n = {PH3['2019wimF']['T1_all_units']['n']}) | {wg('2019wimF')} | {f(PH3['2019wimF']['T1_units_with_text']['estimate'])} {ci(PH3['2019wimF']['T1_units_with_text']['ci_lo'], PH3['2019wimF']['T1_units_with_text']['ci_hi'])} (n = {PH3['2019wimF']['T1_units_with_text']['n_units']}) | {f(PH3['2019wimF']['median_tokens_by_category'].get('within_game'), 1)} / {f(PH3['2019wimF']['median_tokens_by_category'].get('other_game_end'), 1)} / {f(PH3['2019wimF']['median_tokens_by_category'].get('changeover'), 1)} | {f(PH3['2019wimF']['median_A_by_category'].get('within_game'), 1)} / {f(PH3['2019wimF']['median_A_by_category'].get('changeover'), 1)} |
| 2023wimF | {f(PH3['2023wimF']['T1_all_units']['rho'])} {ci(*PH3['2023wimF']['T1_all_units']['ci'])} (n = {PH3['2023wimF']['T1_all_units']['n']}) | {wg('2023wimF')} | {f(PH3['2023wimF']['T1_units_with_text']['estimate'])} {ci(PH3['2023wimF']['T1_units_with_text']['ci_lo'], PH3['2023wimF']['T1_units_with_text']['ci_hi'])} (n = {PH3['2023wimF']['T1_units_with_text']['n_units']}) | {f(PH3['2023wimF']['median_tokens_by_category'].get('within_game'), 1)} / {f(PH3['2023wimF']['median_tokens_by_category'].get('other_game_end'), 1)} / {f(PH3['2023wimF']['median_tokens_by_category'].get('changeover'), 1)} | {f(PH3['2023wimF']['median_A_by_category'].get('within_game'), 1)} / {f(PH3['2023wimF']['median_A_by_category'].get('changeover'), 1)} |

In 2019, units with no text have a median `A` of {f(PH3['2019wimF']['median_A_zero_token_units'], 1)} s, against {f(PH3['2019wimF']['median_A_units_with_text'], 1)} s for units with text
({PH3['2019wimF']['n_zero_token_units']} empty units). Excluding units with no text gives rho = {f(PH3['2019wimF']['T1_units_with_text']['estimate'])} (2019) and
{f(PH3['2023wimF']['T1_units_with_text']['estimate'])} (2023). {'The association is therefore not produced by empty windows.' if all(PH3[t]['T1_units_with_text']['ci_lo'] > 0 for t in T) else 'Empty windows contribute to the association.'} Reading: in 2019, T1 is
partly a between-category effect, because changeover units have both long intervals and long texts. Within games it is
{wg_state('2019wimF')} in 2019, and {wg_state('2023wimF')} in 2023. H0 (a constant rate within a text window that spans
the interval) predicts this as well as H1', so T1 remains a precondition and not support.

### 10.3 Range of `A` and comparability of the 2023 final (PH4)

| match | units | min | q10 | median | q90 | max | units with `A` > 100 s | changeover units |
|---|---|---|---|---|---|---|---|---|
{range_rows()}

The 2019 units were restricted to `A` <= {f(ph['PH4_2019_restricted']['A_max_2023'], 0)} s, the 2023 maximum. This drops {ph['PH4_2019_restricted']['n_units_2019_dropped']} units ({ph['PH4_2019_restricted']['n_units_2019_restricted']} remain).
On the restricted units, T2 = {pp(ph4r.loc['T2'].estimate)} pp {ppci(ph4r.loc['T2'].ci_lo, ph4r.loc['T2'].ci_hi)} (shift-null p = {pfmt(ph4r.loc['T2'].p_shift)}) and
T3 rho = {f(ph4r.loc['T3'].estimate)} {ci(ph4r.loc['T3'].ci_lo, ph4r.loc['T3'].ci_hi)} (p = {pfmt(ph4r.loc['T3'].p_shift)}). {'The 2019 nulls are therefore not produced by the few longest intervals.' if ph4_null else 'Restricting the range changes the 2019 result.'} The main difference between the two matches is composition (changeover units), which only T4 tests
and which 2023 lacks.

### 10.4 Serial correlation and the shift null (PH5)

The circular shift moves the whole timing sequence against the whole unit sequence, so both sequences keep their serial
structure in every null draw. Serial correlation is therefore handled by construction, unlike in an iid label permutation.
One-line check: the lag-1 Spearman autocorrelations in unit order are, for tokens,
{f(PH5['2019wimF']['lag1_spearman_unit_order']['tokens'])} / {f(PH5['2023wimF']['lag1_spearman_unit_order']['tokens'])}; for formula share,
{f(PH5['2019wimF']['lag1_spearman_unit_order']['formula_share_units_with_text'])} / {f(PH5['2023wimF']['lag1_spearman_unit_order']['formula_share_units_with_text'])}; and for `A`,
{f(PH5['2019wimF']['lag1_spearman_unit_order']['A'])} / {f(PH5['2023wimF']['lag1_spearman_unit_order']['A'])} (2019 / 2023). The ratio of the shift-null SD to the
iid-permutation-null SD ({PH5['2019wimF']['n_permutations']:,} permutations) is {min(ph5_ratios):.2f}-{max(ph5_ratios):.2f} across T1-T4 and both
matches. {'In these data, then, serial correlation barely widens the null.' if max(ph5_ratios) < 1.1 else 'Serial correlation widens the null in these data.'}
{'No test changes side of p = 0.05 between the two nulls.' if not ph5_flip else 'Tests whose p changes side of 0.05 between the two nulls: ' + ', '.join(ph5_flip) + ' (the shift null is the pre-registered one).'}

### 10.5 Umpire-pattern tokens (PH6)

The formula list used in T2-T4 comes from the pool only, and it was **not** filtered for umpire speech. It contains
{umc['thank you']['n_formula_types']} formula types with `thank you` ({umc['thank you']['pool_count_of_types']} pool occurrences), {umc['mr <token>']['n_formula_types']} with `mr <token>` and
{umc['game <player name>']['n_formula_types']} with `game <player name>`. Mask U removes every `thank you` (with an adjacent `please` or a
following `players`), `mr` + the next token, and `game` + a finalist's name. In the target units it covers
{umc['target_tokens_masked_U_2019wimF']} of {umc['target_tokens_2019wimF']} tokens (2019) and {umc['target_tokens_masked_U_2023wimF']} of {umc['target_tokens_2023wimF']} (2023). R1U adds the
pre-registered R1 score-call mask. The text splits at masked spans, and the formula list is unchanged.

| match | check | test | estimate [95% CI] | units | tokens | p shift-null (shifts) | CI excludes 0 |
|---|---|---|---|---|---|---|---|
{sens_rows('PH6')}

Reading: {ph6_text}. Umpire speech in the text does not drive the null results.

## 11. Interpretation

With clip-level text, the only frame that can be tested is the interval between points. In the 2019 final, the amount of
text attached to a point tracks that point's own interval beyond match-level drift (T1). Part of the association runs
across game boundaries, because changeover units have long intervals and long texts. Within games the association is
weaker (rho = {f(PH3['2019wimF']['T1_within_game_units']['estimate'])}). It shows that clip-level text carries some point-level
timing information, which both H1' and H0 predict. Given that, the formula measures could have shown the pattern H1'
predicts, but they did not. Formula share does not rise in short intervals (the point estimate falls); formula length in
syllables does not grow with the time available; and changeover talk is not less formulaic than within-game talk. At
this resolution and **for the text as measured**, the commentary behaves as H0 describes: more time yields more text,
with no detectable change in formula share or formula length.

"No detectable change" is bounded by the design. With 80% power, the tests would have detected measured effects of about
{mde_fmt('2019wimF', 'T2')} (T2), {mde_fmt('2019wimF', 'T3', rho_prefix=True)} (T3) and {mde_fmt('2019wimF', 'T4')} (T4) in 2019. Misattribution of text to
points and ASR errors make the corresponding true effects larger by an unknown factor: about {ratio_lo:.1f}-{ratio_hi:.1f} times
larger if half of a unit's text belonged to neighbouring intervals (section 10.1).

For the analogy with oral-formulaic verse, the data give no support for the idea that the time between points conditions
the length or density of formulas the way a metrical slot would. They cannot exclude effects smaller than the MDEs, or
effects attenuated by the measurement. They say nothing about the strike level, where the brief located the metrical
frame and which this corpus cannot reach, nor about formulaic systems, which were not measured here.

## 12. Limitations

1. **No audio, no word times, no speakers**: intonation units, pitch resets, IU phase, rally-internal speech and
   production speed cannot be measured. The hypothesis tested is the re-specified H1', not H1.
2. **Undocumented text window**: texts are attributed to clips by an unknown rule, and identical texts recur on clips a
   median {wd['2019wimF']['median_gap_source_clip_end_to_repeat_clip_start_s']} s apart. A unit's text can include talk
   from before the point and can miss talk late in long intervals. This blurs the link between time and text and biases
   every T-test toward 0. **The CIs and MDEs bound the measured effect, not the true one** (illustrative misattribution
   scenarios in section 10.1).
3. **Mixed voices**: umpire calls, Hawk-Eye and announcements are in the text. R1 removes score calls; the post hoc
   variants U and R1U also remove `thank you`, `mr <name>` and `game <name>` (section 10.5). Hawk-Eye and other
   announcements remain.
4. **ASR errors**: a hand-read sample of {asr['n_words']} words found {asr['total_per_1000_words']:.0f} errors per 1,000 words
   (Wilson 95% {asr['wilson95_ci_per_1000_total'][0]:.0f}-{asr['wilson95_ci_per_1000_total'][1]:.0f};
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
7. **Short formulaic strings**: maximal formulaic strings are mostly bigrams ({100 * bigram_share_19:.0f}% have two tokens
   in 2019; mean {f(D19['T3']['mean_syll'], 2)} syllables and median {f(D19['T3']['median_syll'], 0)} in 2019; mean
   {f(D23['T3']['mean_syll'], 2)} in 2023). T3 therefore works on a narrow range of lengths and could miss effects confined
   to long formulas. R2, with n >= 3, covers {int(rob['2019wimF'].query("check.str.startswith('R2') and test == 'T3'", engine='python').n_strings.iloc[0])} strings in 2019 and is also null.
8. **Power and dependence**: {D19['descriptives']['n_units']} (2019) and {D23['descriptives']['n_units']} (2023) units.
   Formulaic strings are clustered within units, and the bootstrap resamples units. The index-shift null has a two-sided
   p-value floor of {2 / (int(C19.loc['T1'].n_shifts) + 1):.4f} (2019) and {2 / (int(C23.loc['T1'].n_shifts) + 1):.4f} (2023).
   The simulated MDEs are in section 10.1.
9. **One broadcaster per match**: commentator identity, broadcaster and match are confounded. The medium contrast (X1)
   compares different matches and is descriptive.
10. Robustness checks, exploratory and post hoc analyses are not corrected for multiplicity; they are used only for
    interpretation.

## 13. Deviations from the plan

* The brief's ">= 5,000 shifts" is met only by the pre-registered secondary null R6. The primary null is the exhaustive index shift, as the plan states.
* All bootstraps use the plan's seed {SEED}. Quantile-regression bootstrap fits that raised a convergence warning are kept
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
`pool_formulas_*.{{json,tsv}}`, `top_strings_*.tsv`, `syllable_check.json`, `verdict.json`, `nulls_*.npz`; POST HOC:
`posthoc.json`, `posthoc_mde.csv`, `posthoc_power_curves.csv`, `posthoc_sensitivity.csv`, `posthoc_umpire_check.json`);
`figures/` (fig6 is POST HOC).
"""
(HERE / "report.md").write_text(report, encoding="utf-8")
print("report.md written,", len(report.split()), "words")
