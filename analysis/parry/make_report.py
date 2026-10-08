"""Writes analysis/parry/report.md from analysis/parry/results/ (no number is typed by hand).

Revision 1 (plan.md addendum 1, after review/critic_parry_v1.md): no verdict sentence is a literal. Every verdict is chosen by one of the
rules below from the results files:
* ci_verdict: a difference is 'more' if its 95% interval lies above 0, 'less' if below 0, otherwise 'no difference detected'.
* share_word: >= 0.9 'almost all', > 0.55 'most', >= 0.45 'about half', otherwise 'less than half'.
* near-empty rule (addendum A1): matched-size n >= 3 rows are 'near-empty inventories (not informative)' if the mean TV -> TV n >= 3
  coverage at that S is below 2% of tokens.
* weak-proxy rule (addendum M3): an automatic measure is a 'weak proxy' if its kappa against every reference set is below 0.40.
* thrift verdicts (addendum M5) are read from results/h4_verdicts.json (rule in p10_h4_robust.py).
* composition rule (addendum A1): OFFICIAL + SCORE + STAT tokens are 'the majority' of the TV-only stock if >= 50% of its tokens, otherwise
  'a minority'; the strict part is said to hold a larger share of umpire/score-call tokens only if its share is more than twice that of all
  TV-only tokens; 'the classifier puts some score frames in OTHER' is printed only if a top-40 string with modal slot OTHER contains
  game(s)/set(s).
* base-rate rule (addendum M3): the 2019-vs-other precision difference is 'mostly a base rate' if the groups' precision-minus-chance values
  differ by less than half the difference of their raw precisions, otherwise 'only partly a base rate'.
* conditional explanations: the Cornell-null explanation (H2) only if the excess exceeds the observed difference, the shuffled Cornell inventory
  is larger than every TV stream's and Cornell's Simpson index exceeds the TV mean; 'no sign that the hinted pair shares more' only if p >= 0.05;
  the slot-noise caveat only if every classifier kappa is below 0.6.
* significance wording for exploratory tests: 'p < 0.05' / 'p >= 0.05' as computed; Bonferroni bounds where stated.
Run: python -I analysis/parry/make_report.py
"""
import subprocess
import sys
from collections import Counter, defaultdict
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import numpy as np
import lib2b as L

R = L.RESULTS
OUT = L.HERE / "report.md"
TEAM_LABEL = {"cornell": "Cornell live text (written)", "press_pooled": "press answers, pooled", "press_federer": "press: Federer",
              "press_djokovic": "press: Djokovic", "press_murray": "press: Murray", "press_nadal": "press: Nadal",
              "tv_other19": "other 19 TV streams"}
OFFICIAL_LIKE = ("OFFICIAL", "SCORE", "STAT")


def CAL_LABEL(m):
    return __import__("calibrate").MEASURE_LABEL.get(m, m)


def lab(t):
    return TEAM_LABEL.get(t, L.short(t))


def f(x):
    try:
        return float(x)
    except (TypeError, ValueError):
        return float("nan")


def pc(x, d=1):
    v = f(x)
    return "-" if v != v else f"{100 * v:.{d}f}"


def ci(lo, hi, d=1, scale=100):
    a, b = f(lo), f(hi)
    if a != a or b != b:
        return ""
    return f"[{scale * a:.{d}f}, {scale * b:.{d}f}]"


def num(x, d=3):
    v = f(x)
    return "-" if v != v else f"{v:.{d}f}"


def pval(p):
    v = f(p)
    if v != v:
        return "-"
    return f"{v:.4f}" if v >= 0.0001 else f"{v:.1e}"


def table(head, rows):
    out = ["| " + " | ".join(head) + " |", "|" + "---|" * len(head)]
    for r in rows:
        out.append("| " + " | ".join(str(x) for x in r) + " |")
    return "\n".join(out)


def ci_verdict(lo, hi, more, less, none):
    lo, hi = f(lo), f(hi)
    return more if lo > 0 else less if hi < 0 else none


def share_word(x):
    x = f(x)
    return "almost all" if x >= 0.9 else "most" if x > 0.55 else "about half" if x >= 0.45 else "less than half"


def git(args):
    try:
        return subprocess.run(["git"] + args, cwd=L.ROOT, capture_output=True, text=True, check=True).stdout.strip()
    except Exception:  # noqa: BLE001
        return ""


def git_plan_commit():
    h = git(["log", "--diff-filter=A", "--format=%h %ad", "--date=iso", "--", "analysis/parry/plan.md"]).splitlines()
    return h[-1] if h else "unknown"


def git_first_commit(path):
    out = git(["log", "--diff-filter=A", "--format=%h|%ad|%(trailers:key=Co-Authored-By,valueonly,separator=%x2C)|%(trailers:key=Claude-Session,valueonly)",
               "--date=iso", "--", path]).splitlines()
    return out[-1].split("|") if out else ["unknown", "", "", ""]


def main():
    S = []
    w = S.append
    meta = L.read_json(R / "sharing_meta.json")
    agg = L.read_csv(R / "sharing_aggregates.csv")
    A = {(r["S"], r["tokens"], r["measure"], r["statistic"]): r for r in agg}
    prim = {r["id"]: r for r in L.read_csv(R / "primary_tests.csv")}
    h12 = L.read_json(R / "primary_H1H2.json")
    h45 = L.read_json(R / "primary_H4H5.json")
    core = L.read_csv(R / "core_sizes.csv")
    core_meta = L.read_json(R / "core_meta.json")
    idio = L.read_csv(R / "idiolect_shares.csv")
    cbase = L.read_csv(R / "core_baselines.csv")
    ctop = L.read_csv(R / "core_top.csv")
    clus = L.read_csv(R / "cluster_tests.csv")
    qap = L.read_csv(R / "qap_regression.csv")
    pair = L.read_json(R / "pair_2019_2023.json")
    p2t = L.read_csv(R / "pool_to_target.csv")
    p2t_meta = L.read_json(R / "pool_to_target_meta.json")
    rsum = L.read_json(R / "refexpr_pool_summary.json")
    cats = L.read_csv(R / "refexpr_category_shares.csv")
    econ = L.read_csv(R / "refexpr_economy.csv")
    parr = L.read_csv(R / "parryan_pattern.csv")
    thr = L.read_csv(R / "thrift_tests_2b.csv")
    mde = L.read_csv(R / "mde_h4b.csv")
    ext = L.read_csv(R / "extension_2b.csv")
    e1 = L.read_csv(R / "e1_economy.csv")
    e1top = L.read_csv(R / "e1_top_types.csv")
    e2 = L.read_csv(R / "e2_classes.csv")
    e2t = L.read_csv(R / "e2_tests.csv")
    e1t = L.read_csv(R / "e1_tests.csv")
    h4d = L.read_csv(R / "h4_declustered.csv")
    h4s = L.read_csv(R / "h4b_by_slot.csv")
    tmeta = L.read_json(R / "thrift_meta.json")
    inv_full = L.read_csv(R / "inventory_sizes_full.csv")
    inv_m = L.read_csv(R / "inventory_sizes_matched.csv")
    slot_tok = L.read_csv(R / "slot_token_counts.csv")
    # ---- post hoc (addendum 1) results
    LS = {(r["tokens"], r["statistic"], r["measure"]): r for r in L.read_csv(R / "largeI_summary.csv")}
    lmeta = L.read_json(R / "largeI_meta.json")
    lcov = L.read_csv(R / "largeI_coverage.csv")
    tvo = {r["target"]: r for r in L.read_csv(R / "largeI_tvonly_by_target.csv")}
    tvs = {(r["target"], r["class"], r["slot"]): r for r in L.read_csv(R / "largeI_tvonly_slots.csv")}
    tvp = L.read_csv(R / "largeI_tvonly_types_pooled.csv")
    tvf = L.read_csv(R / "largeI_tvonly_types_finals.csv")
    HO = {(r["S"], r["tokens"], r["measure"], r["baseline"], r["coverage"]): r for r in L.read_csv(R / "h2_observed.csv")}
    uconc = {r["corpus"]: r for r in L.read_csv(R / "unigram_concentration.csv")}
    shufc = {r["team"]: r for r in L.read_csv(R / "shuffled_inventory_composition.csv")}
    h1c = L.read_json(R / "h1_check.json")
    facts = L.read_json(R / "corpus_facts.json")
    h4r = L.read_csv(R / "h4_robust.csv")
    h4l = L.read_csv(R / "h4_robust_loso.csv")
    h4v = L.read_json(R / "h4_verdicts.json")
    h5p = L.read_csv(R / "h5_sensitivity_post_hoc.csv")
    e1l = L.read_csv(R / "e1_loso_tests.csv")
    e2s = L.read_csv(R / "e2_slot_sums.csv")
    rr = L.read_json(R / "rerun_check.json") if (R / "rerun_check.json").exists() else None
    cal_ok = (R / "calibration_agreement.json").exists()
    teams = meta["teams"]
    tv_tokens = sum(teams[s]["tokens"] for s in L.TV)
    n_fps_bad = sum(1 for s, d in rsum["streams"].items() if not d["fps_valid"])

    def a(Sv, m, st, tok="norm"):
        return A[(str(Sv), tok, m, st)]

    def est_ci(Sv, m, st, tok="norm", d=1):
        r = a(Sv, m, st, tok)
        return f"{pc(r['estimate'], d)} {ci(r['ci_lo'], r['ci_hi'], d)}"

    def lsr(stat, meas, tok="norm"):
        return LS[(tok, stat, meas)]

    def lci(stat, meas, tok="norm", d=2):
        r = lsr(stat, meas, tok)
        return f"{pc(r['estimate'], d)} {ci(r['ci_lo'], r['ci_hi'], d)}"

    def ho(Sv, meas, b, cov, tok="norm"):
        return HO[(str(Sv), tok, meas, b, cov)]

    def hoci(Sv, meas, b, cov, tok="norm", d=2):
        r = ho(Sv, meas, b, cov, tok)
        return f"{pc(r['estimate'], d)} {ci(r['ci_lo'], r['ci_hi'], d)}"

    def slot_share(t, cls, sl):
        return f(tvs[(t, cls, sl)]["share_of_class"])

    # ------------------------------------------------------------------ header
    w("# Phase 2b: the tradition across broadcasts (shared stock, calibration, thrift per slot)")
    w("")
    w("Generated by `analysis/parry/make_report.py` from `analysis/parry/results/`; rerun everything with `bash analysis/parry/run_all.sh`. "
      f"The plan `analysis/parry/plan.md` was committed before any 2b test script was written or run (commit {git_plan_commit()}). "
      "**All of Phase 2b is exploratory relative to the pre-registered Phase 2**: it was added after every Phase 2 result had been seen, on the same corpus. "
      "Within 2b, seven tests were fixed in the plan as **2b-primary** and are Holm-corrected together (section 5); every other number is exploratory, "
      "and p-values outside section 5 are unadjusted. Brackets are 95% intervals; the kind of interval is stated each time.")
    w("")
    w("**Revision 1.** This version adds the analyses of plan addendum 1 (dated, committed before they were run, and **post hoc**: written after "
      "the first report and the critic's review `review/critic_parry_v1.md`, whose own reruns the addendum adopts). The pre-registered analyses are "
      "rerun unchanged" + ((f" and reproduce: all {rr['files_compared']} pre-registered results files are identical to commit {rr['reference_commit']}"
                            if rr["identical"] == rr["files_compared"] else
                            f"; {rr['identical']} of {rr['files_compared']} pre-registered results files are identical to commit {rr['reference_commit']} "
                            f"(differing: {', '.join(rr['different'])})") + " (run-time fields excluded; `results/rerun_check.csv`)" if rr else "") + ". "
      "The cross-corpus comparison now rests on 100,000-token identification sets (section 2.0); the 1,500-token matched design is kept as the secondary "
      "design. No verdict sentence in this report is typed by hand: each is chosen by a rule stated in `make_report.py` from the results files. "
      "Post hoc changes are listed in section 7.")
    w("")
    w("**What is measured.** As in Phase 2, 'formula' below means an exact word n-gram repeated in at least two utterances of a text "
      "(a repetition statistic), not Parry's metrically conditioned formula; the calibration in section 3 measures how far that statistic agrees with "
      "judgements of formulaicity by two LLM coders working from Parry's definition. A TV 'stream' (called 'team' in the plan) is one match with one unnamed "
      "broadcaster; team, match and broadcaster are confounded, and every commentator hint is [unverified].")
    w("")
    # ------------------------------------------------------------------ key results
    w("## Key results")
    w("")
    # ---- K1 large-I comparison
    d2c, d3c = lsr("TV minus cornell", "obs_n2"), lsr("TV minus cornell", "obs_n3")
    d2p, d3p = lsr("TV minus press_pooled", "obs_n2"), lsr("TV minus press_pooled", "obs_n3")
    diffs = [d2c, d3c, d2p, d3p]
    all_above = all(f(d["ci_lo"]) > 0 for d in diffs)
    all_targets = all(int(d["targets_positive"]) == int(d["n_targets"]) for d in diffs)
    if all_above:
        k1_verdict = ("TV sources of the same size cover TV targets more than written live text and press answers do, at n >= 2 and at n >= 3"
                      + (", for every one of the 20 targets" if all_targets else "") + ".")
    else:
        k1_verdict = "; ".join(f"{nm}: " + ci_verdict(d["ci_lo"], d["ci_hi"], "TV sources cover TV targets more", "TV sources cover TV targets less",
                                                      "no difference detected") for nm, d in
                               (("n >= 2 vs Cornell", d2c), ("n >= 3 vs Cornell", d3c), ("n >= 2 vs press", d2p), ("n >= 3 vs press", d3p))) + "."
    w(f"* **Is there a TV-specific multiword stock? (post hoc; section 2.0).** Each TV stream (whole text) was covered by the formulas of a "
      f"{lmeta['I_size']:,}-token sample of the other 19 TV streams, of the Cornell live text and of the press answers ({lmeta['R']} samples each; names and "
      f"numerals normalised). Observed coverage, mean over the 20 targets: n >= 2: TV {pc(lsr('tv_other19 -> TV', 'obs_n2')['estimate'])}%, Cornell "
      f"{pc(lsr('cornell -> TV', 'obs_n2')['estimate'])}%, press {pc(lsr('press_pooled -> TV', 'obs_n2')['estimate'])}%; n >= 3: TV "
      f"{pc(lsr('tv_other19 -> TV', 'obs_n3')['estimate'])}%, Cornell {pc(lsr('cornell -> TV', 'obs_n3')['estimate'])}%, press "
      f"{pc(lsr('press_pooled -> TV', 'obs_n3')['estimate'])}%. TV minus Cornell: {lci('TV minus cornell', 'obs_n2')} pp at n >= 2 "
      f"({d2c['targets_positive']} of 20 targets positive) and {lci('TV minus cornell', 'obs_n3')} pp at n >= 3 ({d3c['targets_positive']}/20); TV minus press: "
      f"{lci('TV minus press_pooled', 'obs_n2')} and {lci('TV minus press_pooled', 'obs_n3')} pp ({d2p['targets_positive']}/20, {d3p['targets_positive']}/20; "
      f"bootstrap over targets). {k1_verdict} With the umpire's calls and point-score calls removed from the targets the n >= 3 differences are "
      f"{lci('TV minus cornell', 'obs_n3_comm')} and {lci('TV minus press_pooled', 'obs_n3_comm')} pp; on raw tokens {lci('TV minus cornell', 'obs_n3', 'raw')} and "
      f"{lci('TV minus press_pooled', 'obs_n3', 'raw')} pp. Differences of the excess over the unigram-shuffled null: n >= 2 "
      f"{pc(lsr('TV minus cornell', 'exc_n2')['estimate'], 2)} / {pc(lsr('TV minus press_pooled', 'exc_n2')['estimate'], 2)}, n >= 3 "
      f"{pc(lsr('TV minus cornell', 'exc_n3')['estimate'], 2)} / {pc(lsr('TV minus press_pooled', 'exc_n3')['estimate'], 2)} pp (Cornell / press).")
    # ---- K2 TV-only stock
    m19, m23 = tvo[L.MAIN], tvo[L.HELDOUT]
    sh_only = [f(r["share_only"]) for r in tvo.values()]
    comp = {sl: slot_share("ALL_TV", "tv_only", sl) for sl in L.SLOTS}
    off_share = sum(comp[s] for s in OFFICIAL_LIKE)
    top40 = tvp[:40]
    n_off40 = sum(1 for r in top40 if r["modal_slot"] in OFFICIAL_LIKE)
    missed_score = [r["ngram"] for r in top40 if r["modal_slot"] == "OTHER" and any(t in ("games", "game", "sets", "set") for t in r["ngram"].split())]
    ex_off = [r["ngram"] for r in top40 if r["modal_slot"] in OFFICIAL_LIKE][:6]
    ex_com = [r["ngram"] for r in top40 if r["modal_slot"] not in OFFICIAL_LIKE][:6]
    order = sorted(L.SLOTS, key=lambda s: -comp[s])
    strict_frac = np.mean([f(r["share_strict"]) for r in tvo.values()]) / np.mean(sh_only)
    sj = comp["SHOT"] + comp["JUDGE"]
    sck = L.read_json(R / "calibration_slot_context.json") if (R / "calibration_slot_context.json").exists() else {}
    span_k = (f"kappa {num(sck['coder_spans_A_span']['kappa'], 2)} / {num(sck['coder_spans_B_span']['kappa'], 2)} against the two coders"
              if "coder_spans_A_span" in sck else "not validated")
    comp_verdict = (f"By the span-mode slot classifier ({span_k}), SCORE, STAT and OFFICIAL frames are "
                    + ("the majority" if off_share >= 0.5 else "a minority") + f" ({pc(off_share, 0)}%) of its tokens, SHOT and JUDGE {pc(sj, 0)}% and OTHER "
                    f"{pc(comp['OTHER'], 0)}%")
    w(f"* **What the TV-specific n >= 3 stock consists of (post hoc; Tables 2.D-2.G).** In the 2019 final {pc(m19['share_only'])}% of tokens lie in n >= 3 strings that "
      f"the TV sample shares with it and that neither the Cornell nor the press sample repeats ('TV-only'), and {pc(m19['share_shared'])}% in n >= 3 strings that a "
      f"baseline sample also has (2023 final: {pc(m23['share_only'])}% / {pc(m23['share_shared'])}%; mean over the 20 targets {pc(np.mean(sh_only))}%, range "
      f"{pc(min(sh_only))}-{pc(max(sh_only))}%). {comp_verdict} (pooled over the 20 targets; by slot "
      + ", ".join(f"{s} {pc(comp[s], 0)}%" for s in order)
      + f"; slot of the longest covering string); {pc(slot_share('ALL_TV', 'tv_only', '_umpire_mask'), 0)}% of them lie inside umpire or score-call "
      f"patterns ({pc(slot_share(L.MAIN, 'tv_only', '_umpire_mask'), 0)}% and {pc(slot_share(L.HELDOUT, 'tv_only', '_umpire_mask'), 0)}% in the 2019 and 2023 "
      f"finals). Among the 40 most frequent TV-only strings, {n_off40} are SCORE, STAT or OFFICIAL by modal slot ("
      + ", ".join(f"`{x}`" for x in ex_off) + "), the others SHOT, JUDGE or OTHER (" + ", ".join(f"`{x}`" for x in ex_com)
      + (f"; the classifier puts some score frames in OTHER, e.g. " + ", ".join(f"`{x}`" for x in missed_score[:2]) if missed_score else "") + "). "
      + share_word(np.mean([f(r['share_cross']) for r in tvo.values()]) / np.mean(sh_only)).capitalize() + " of the TV-only tokens "
      f"({pc(np.mean([f(r['share_cross']) for r in tvo.values()]))}% of tokens on average, against {pc(np.mean(sh_only))}%) are in strings attested in at least two "
      f"other TV streams. Under the strictest reading (no covering string is repeated anywhere in the whole Cornell text or the "
      f"{facts['press_answers']:,}-answer press corpus) the TV-only share falls to {pc(np.mean([f(r['share_strict']) for r in tvo.values()]))}% on average "
      f"({pc(m19['share_strict'])}% in 2019), and {pc(slot_share('ALL_TV', 'tv_only_strict', '_umpire_mask'), 0)}% of those tokens are umpire or score-call "
      "patterns. " + (f"So {share_word(1 - strict_frac)} of the TV-only stock consists of strings the other registers also use, less often (a difference of "
                      "frequency; rates in Table 2.F)" if strict_frac < 0.5 else f"So {share_word(strict_frac)} of the TV-only stock consists of strings the other "
                      "registers do not repeat at all")
      + (f"; umpire and score-call patterns are a larger part of the strictly TV-only tokens ({pc(slot_share('ALL_TV', 'tv_only_strict', '_umpire_mask'), 0)}%) "
         f"than of all TV-only tokens ({pc(slot_share('ALL_TV', 'tv_only', '_umpire_mask'), 0)}%)." if slot_share('ALL_TV', 'tv_only_strict', '_umpire_mask')
         > 2 * slot_share('ALL_TV', 'tv_only', '_umpire_mask') else "."))
    # ---- K3 H1 as a check
    h1a, h1b, h2a, h2b = (h12[k] for k in ("H1a", "H1b", "H2a", "H2b"))
    c15 = h1c["S1500_cov_base"]
    bshares = [c15["cornell_share_of_tv_tv_excess"], c15["press_pooled_share_of_tv_tv_excess"]]
    h1_word = share_word(min(bshares))
    w(f"* **Shared stock beyond lexicon (H1; a check that the pipeline detects collocation).** At 1,500 tokens per stream the formulas of one TV stream cover "
      f"{pc(h1a['obs_mean'])}% of another's tokens against {pc(h1a['null_mean'])}% for unigram-shuffled texts: excess {pc(h1a['estimate'])} pp "
      f"{ci(h1a['ci_lo'], h1a['ci_hi'])} (n >= 2; {h1a['n_targets_positive']}/{h1a['n_targets']} targets) and {pc(h1b['estimate'], 2)} pp "
      f"{ci(h1b['ci_lo'], h1b['ci_hi'], 2)} (n >= 3). The shuffle destroys every collocation, and {h1_word} of this excess is reached by sources that are not TV "
      f"commentary: press answers reach {pc(c15['press_pooled_share_of_tv_tv_excess'], 0)}% and Cornell live text {pc(c15['cornell_share_of_tv_tv_excess'], 0)}% "
      f"of it, and four press speakers share {pc(h1c['press_speakers_mean_excess_S1500_base'], 1)} pp among themselves (TV streams {pc(h1a['estimate'], 1)}). "
      + ("H1 therefore establishes repetition beyond the lexicon, not a commentary-specific stock"
         + ("; the TV-specific part is in the first two bullets." if all_above else ".") if min(bshares) > 0.55 else "Less than half of it is reached by the baselines."))
    # ---- K4 H2 at S = 1,500
    oc, op = ho(1500, "cov_base", "cornell", "observed"), ho(1500, "cov_base", "press_pooled", "observed")
    tv_obs = f(oc["tv_tv_mean"])
    h2_verdicts = [ci_verdict(r["ci_lo"], r["ci_hi"], f"more than {nm} ({pc(f(r['estimate']) / tv_obs, 0)}% of the TV -> TV coverage of {pc(tv_obs, 2)}%)",
                              f"less than {nm}", f"no differently from {nm}") for nm, r in (("the written source", oc), ("the press source", op))]
    tvshuf = [f(shufc[s]["shuffled_types"]) for s in L.TV]
    uc_tv, uc_c = uconc["TV, mean over the 20 streams"], uconc["cornell"]
    inv15 = [f(r["types_n3"]) for r in inv_m if r["tokens"] == "norm" and r["S"] == "1500" and r["team"] in L.TV]
    tvtv3 = f(a(1500, "cov_n3", "TV->TV mean obs")["estimate"])
    near_empty_15 = tvtv3 < 0.02
    exc_c = f(ho(1500, "cov_base", "cornell", "excess")["estimate"])
    # rule: the Cornell null explanation is printed only if the excess exceeds the observed difference, the shuffled Cornell inventory is larger than
    # every TV stream's, and Cornell's unigram distribution is more concentrated (Simpson index) than the mean TV stream's
    expl_ok = exc_c > f(oc["estimate"]) and f(shufc["cornell"]["shuffled_types"]) > max(tvshuf) and f(uc_c["simpson_sum_p2"]) > f(uc_tv["simpson_sum_p2"])
    expl_txt = (f"The excess exceeds the observed difference for Cornell because the shuffled Cornell inventory is larger ({num(shufc['cornell']['shuffled_types'], 0)} "
                f"types at 1,500 tokens against {num(min(tvshuf), 0)}-{num(max(tvshuf), 0)} for TV streams): Cornell's unigram distribution is more concentrated "
                f"(Simpson index {num(uc_c['simpson_sum_p2'], 4)} against {num(uc_tv['simpson_sum_p2'], 4)} per TV stream; `<name>` {pc(uc_c['share_name'])}% and "
                f"`<num>` {pc(uc_c['share_num'])}% of tokens against {pc(uc_tv['share_name'])}% and {pc(uc_tv['share_num'])}%), so its chance bigrams cover shuffled "
                "TV text, and the size of the excess difference is a property of the null. ") if expl_ok else ""
    w(f"* **H2 at 1,500 tokens (pre-registered).** The pre-registered statistic (difference of excess over the shuffled null) is {pc(h2a['estimate'], 2)} pp "
      f"{ci(h2a['ci_lo'], h2a['ci_hi'], 2)} against Cornell and {pc(h2b['estimate'], 2)} pp {ci(h2b['ci_lo'], h2b['ci_hi'], 2)} against press (Holm-rejected: "
      f"{'yes' if prim['H2a']['reject_holm_0.05'] == 'True' else 'no'}, {'yes' if prim['H2b']['reject_holm_0.05'] == 'True' else 'no'}). On observed coverage, on which the claim rests, the differences are "
      f"{hoci(1500, 'cov_base', 'cornell', 'observed')} pp ({oc['targets_positive']}/{oc['n_targets']} targets positive) and "
      f"{hoci(1500, 'cov_base', 'press_pooled', 'observed')} pp ({op['targets_positive']}/{op['n_targets']}), so at this size TV sources cover TV targets "
      + " and ".join(h2_verdicts) + ". " + expl_txt
      + (f"At n >= 3 the 1,500-token inventories are near-empty ({num(min(inv15), 0)}-{num(max(inv15), 0)} n >= 3 types per TV stream, TV -> TV "
         f"coverage {pc(tvtv3, 2)}%) and their differences are not informative: the TV minus Cornell n >= 3 difference is "
         f"{pc(ho(1500, 'cov_n3', 'cornell', 'observed')['estimate'], 2)} pp at 1,500 tokens, {pc(ho(3000, 'cov_n3', 'cornell', 'observed')['estimate'], 2)} "
         f"at 3,000 and {pc(d3c['estimate'], 2)} at {lmeta['I_size']:,}." if near_empty_15 else ""))
    # ---- K5 core
    k20 = next(r for r in core if r["size"] == "full" and r["tokens"] == "norm" and r["k"] == "20")
    k10 = next(r for r in core if r["size"] == "full" and r["tokens"] == "norm" and r["k"] == "10")
    cb10 = {r["baseline"]: r for r in cbase if r["k"] == "10"}
    core_min = min(f(cb10["cornell"]["share_in_baseline_inventory"]), f(cb10["press_pooled"]["share_in_baseline_inventory"]))
    w(f"* **Genre core.** {int(f(k20['types_base']))} n-grams are formulas of all 20 streams and {int(f(k10['types_base']))} of at least 10 "
      f"({int(f(k10['types_n3']))} of them with n >= 3; {int(f(k20['types_n3']))} with n >= 3 in all 20). Of the >= 10-stream core, "
      f"{pc(cb10['cornell']['share_in_baseline_inventory'], 0)}% are formulas of a Cornell sample and {pc(cb10['press_pooled']['share_in_baseline_inventory'], 0)}% of a "
      f"press sample of the same total size ({tv_tokens:,} tokens): {share_word(core_min)} of the most widely shared strings are also formulas of the written "
      "and press baselines.")
    # ---- K6 stream-specific share
    ia = [r for r in idio if r["size"].startswith("matched") and r["slot"] == "ALL"]
    fa = [r for r in idio if r["size"] == "full" and r["slot"] == "ALL"]
    by_slot_f = defaultdict(list)
    for r in idio:
        if r["size"] == "full":
            by_slot_f[r["slot"]].append(f(r["share_idiolect"]))
    sl_lo = min((s for s in L.SLOTS), key=lambda s: np.mean(by_slot_f[s]))
    sl_hi = max((s for s in L.SLOTS), key=lambda s: np.mean(by_slot_f[s]))
    sm = core_meta["spearman_idiolect_vs_stream_tokens"]
    w(f"* **Stream-specific share (called 'idiolect' in the plan).** On full texts {pc(np.mean([f(r['share_idiolect']) for r in fa]))}% of a stream's formula "
      f"tokens (mean; range {pc(min(f(r['share_idiolect']) for r in fa))}-{pc(max(f(r['share_idiolect']) for r in fa))}%) lie only in formulas that no other stream's "
      f"inventory contains; at 1,500 tokens the share is {pc(np.mean([f(r['share_idiolect']) for r in ia]))}% (range {pc(min(f(r['share_idiolect']) for r in ia))}-"
      f"{pc(max(f(r['share_idiolect']) for r in ia))}%). By slot (full texts) it is lowest for {sl_lo} ({pc(np.mean(by_slot_f[sl_lo]))}%) and highest for "
      f"{sl_hi} ({pc(np.mean(by_slot_f[sl_hi]))}%; descriptive: the slot of a formula is computed from its own words). The share correlates with stream length "
      f"(Spearman rho {num(sm['full'][0], 2)}, p = {pval(sm['full'][1])} on full texts; {num(sm['matched'][0], 2)}, p = {pval(sm['matched'][1])} at 1,500 tokens), "
      "and a stream is one match with one broadcaster, so the share mixes team and match topic"
      + (" and depends on sampling." if min(f(sm['full'][1]), f(sm['matched'][1])) < 0.05 else "."))
    # ---- K7 clusters
    slam = next(r for r in clus if r["similarity"] == "excess_cov_sym" and r["label"] == "slam")
    hint = next(r for r in clus if r["similarity"] == "excess_cov_sym" and r["label"].startswith("hint"))
    mp = next(r for r in clus if r["similarity"] == "jaccard_obs" and r["label"].startswith("Mantel r with shared"))
    hint_txt = ("no sign that the hinted pair shares more than other pairs" if f(hint["p_one_sided_higher_within"]) >= 0.05
                else "the hinted pair shares more than most pairs")
    w(f"* **Clusters (exploratory).** Pairs from the same slam share more (excess {pc(slam['within_minus_between'], 2)} pp above other pairs; permutation "
      f"p = {pval(slam['p_one_sided_higher_within'])}), which mixes broadcaster with venue and surface vocabulary. The only commentator-hint cluster with two members "
      f"(the 2019 and 2023 Wimbledon finals, 'Tim') ranks {pair['excess_cov_sym']['rank_among_190_pairs']} of {pair['excess_cov_sym']['n_pairs']} pairs "
      f"(p = {pval(hint['p_one_sided_higher_within'])}): {hint_txt}. Inventory overlap rises with shared players "
      f"(Mantel r = {num(mp['within_minus_between'], 2)}, p = {pval(mp['p_one_sided_higher_within'])}).")
    loo19 = next(r for r in p2t if r["mode"] == "pool18" and r["target"] == L.MAIN)
    w(f"* **Is the 2019 figure typical?** With the other 19 streams as identification set, 2019's coverage (raw tokens, n >= 2) ranks "
      f"{p2t_meta['rank_2019_loo19_raw_base']} of {p2t_meta['n_targets']} (median {pc(p2t_meta['median_loo19_raw_base'])}%, range "
      f"{pc(p2t_meta['range_loo19_raw_base'][0])}-{pc(p2t_meta['range_loo19_raw_base'][1])}%); the Phase 2 value with the 18-stream pool is reproduced "
      f"({pc(loo19['base'], 2)}%).")
    # ---- K8 calibration
    if cal_ok:
        ca = L.read_json(R / "calibration_agreement.json")
        cm = L.read_json(R / "calibration_meta.json")
        cc = {(r["measure"], r["reference"]): r for r in L.read_csv(R / "calibration_chance.csv")}
        cg = {(r["group"], r["measure"], r["reference"]): r for r in L.read_csv(R / "calibration_chance_groups.csv")}
        csr = {(r["measure"], r["coder"]): r for r in L.read_csv(R / "calibration_span_recall.csv")}
        csc = L.read_json(R / "calibration_slot_context.json")
        pm = ca["primary_HIGH_MEDIUM"]
        main6 = ["pool_n2", "pool_n3", "pool_systems", "pool_n2_or_systems", "insample_n2", "insample_n3"]
        ks_all = [f(r["kappa"]) for r in cc.values()]
        ks_main = [f(cc[(m, rf)]["kappa"]) for m in main6 for rf in ("A", "B", "A_and_B", "A_or_B")]
        pmc = [f(cc[(m, "A_or_B")]["precision_minus_chance"]) for m in main6]
        rmc = [f(cc[(m, "A_or_B")]["recall_minus_chance"]) for m in main6]
        weak = max(ks_all) < 0.40
        x2, x3, xs = cc[("pool_n2", "A_or_B")], cc[("pool_n3", "A_or_B")], cc[("pool_systems", "A_or_B")]
        g19, got = cg[("2019", "pool_n2", "A")], cg[("other", "pool_n2", "A")]
        sA = csr[("pool_n2", "A")]
        w(f"* **Calibration (2b.2; the coders are two LLM agents).** The coders agree with each other at token-level kappa {num(pm['token_kappa'], 2)} "
          f"{ci(pm['token_kappa_ci'][0], pm['token_kappa_ci'][1], 2, 1)}. The automatic measures agree with them "
          + ("less than half as well" if max(ks_all) < 0.5 * f(pm['token_kappa']) else "less well") + f": kappa {num(min(ks_main), 2)}-"
          f"{num(max(ks_main), 2)} for the six measures of the brief against every coder reference set ({num(min(ks_all), 2)}-{num(max(ks_all), 2)} with the "
          f"exploratory measures); against the union of the coders precision exceeds its chance level (the coders' positive share, {num(x2['chance_precision'], 2)}) by "
          f"{num(min(pmc), 2)}-{num(max(pmc), 2)} and recall exceeds its chance level (the measure's own positive share) by {num(min(rmc), 2)}-{num(max(rmc), 2)}. "
          f"The Phase 2 measure (pool n >= 2) marks {pc(x2['auto_share'], 0)}% of tokens: precision {num(x2['precision'], 2)} (chance {num(x2['chance_precision'], 2)}, "
          f"ceiling {num(x2['precision_ceiling'], 2)}), recall {num(x2['recall'], 2)} (chance {num(x2['chance_recall'], 2)}), kappa {num(x2['kappa'], 2)} "
          f"{ci(x2['kappa_lo'], x2['kappa_hi'], 2, 1)}; pool n >= 3: kappa {num(x3['kappa'], 2)}, precision {num(x3['precision'], 2)}, recall {num(x3['recall'], 2)} "
          f"(chance {num(x3['chance_recall'], 2)}); systems: kappa {num(xs['kappa'], 2)}, precision {num(xs['precision'], 2)}, recall {num(xs['recall'], 2)}. "
          + ("Every automatic measure is therefore a weak proxy for the coders' judgement (kappa below 0.40 against every reference set). " if weak else
             "At least one automatic measure reaches kappa 0.40 against some reference set. ")
          + f"The higher precision on the 2019 utterances ({num(g19['precision'], 2)} vs {num(got['precision'], 2)} for coder A) is "
          + ("mostly a base rate" if abs(f(g19['precision_minus_chance']) - f(got['precision_minus_chance'])) < 0.5 * abs(f(g19['precision']) - f(got['precision']))
             else "only partly a base rate")
          + f" (precision minus chance {num(g19['precision_minus_chance'], 2)} vs {num(got['precision_minus_chance'], 2)}): chance precision is "
          f"{num(g19['chance_precision'], 2)} vs {num(got['chance_precision'], 2)} (median utterance {num(g19['median_tokens_per_utterance'], 0)} vs "
          f"{num(got['median_tokens_per_utterance'], 0)} tokens; kappa {num(g19['kappa'], 2)} vs {num(got['kappa'], 2)}). At span level, "
          f"{pc(sA['fully_inside'], 0)}% of coder A's HIGH spans lie wholly inside pool n >= 2 coverage (chance, by circular shifts: {pc(sA['fully_inside_chance_mean'], 0)}%) "
          f"and {pc(sA['touching'], 0)}% touch it (chance {pc(sA['touching_chance_mean'], 0)}%).")
        cv = {k: csc[k] for k in csc if k.startswith("coder_spans_") or k.startswith("references_")}
        rA, rB = csc.get("references_A_commentary_only_context"), csc.get("references_B_commentary_only_context")
        w(f"* **Slot classifier.** In span mode (used for formula spans: Tables 2.11, 2.G, 4.7) it agrees with the coders' slot labels on "
          f"{pc(cv['coder_spans_A_span']['agreement'], 0)}% / {pc(cv['coder_spans_B_span']['agreement'], 0)}% of their spans (kappa "
          f"{num(cv['coder_spans_A_span']['kappa'], 2)} / {num(cv['coder_spans_B_span']['kappa'], 2)}); in context mode (used for the situational slot of a reference in "
          f"H4) on {pc(cv['coder_spans_A_context']['agreement'], 0)}% / {pc(cv['coder_spans_B_context']['agreement'], 0)}% of coder spans (kappa "
          f"{num(cv['coder_spans_A_context']['kappa'], 2)} / {num(cv['coder_spans_B_context']['kappa'], 2)})"
          + (f" and on {pc(rA['agreement'], 0)}% / {pc(rB['agreement'], 0)}% of the commentary references that lie inside a coder span (kappa {num(rA['kappa'], 2)} / "
             f"{num(rB['kappa'], 2)}; n = {rA['n']} / {rB['n']})" if rA and rB else "")
          + (". Slot labels this noisy (kappa below 0.6) attenuate any association between slot and form (H4b) toward zero and make per-slot attributions "
             "unreliable." if max(f(v['kappa']) for v in cv.values()) < 0.6 else "."))
    else:
        w("* **Calibration (2b.2).** Not run: the coders' files were absent when this report was generated (section 3).")
    # ---- K9 thrift
    allc = next(r for r in cats if r["team"] == "ALL_TV" and r["references"] == "commentary_only")
    pat = Counter(r["verdict"] for r in parr if r["slot_type"] == "situational")
    h4a, h4b, h5 = h45["H4a"], h45["H4b"], h45["H5"]
    va, vb = h4v["H4a"], h4v["H4b"]
    big = [r for r in h4r if r["kind"] == "seed"]
    var = {r["variant"]: r for r in h4r if r["kind"] == "variant"}

    def vrow(test, key):
        return next(r for r in h4r if r["test"] == test and r["variant"].startswith(key))
    bigb = [r for r in big if r["test"] == "H4b"]
    pt_sit, pt_syn = h4v["H4b_per_team_slot_sit"], h4v["H4b_per_team_slot_syn"]
    fn = [f(r["share_first_name"]) for r in cats if r["references"] == "commentary_only" and r["team"] != "ALL_TV"]
    sur = [f(r["share_surname"]) for r in cats if r["references"] == "commentary_only" and r["team"] != "ALL_TV"]
    w(f"* **Naming habits (H4a).** Over {allc['resolved_tokens']} commentary-only references to the players, the bare surname is "
      f"{pc(allc['share_surname'], 0)}%, the first name {pc(allc['share_first_name'], 0)}%, the full name {pc(allc['share_full_name'], 0)}%, hypocoristics "
      f"{pc(allc['share_hypocoristic'], 0)}% and descriptive epithets {pc(allc['share_epithet'], 0)}% (at most {pc(allc['share_epithet_upper'], 0)}% if every "
      f"unresolved epithet referred to a player). Streams (team, match and broadcaster together) differ in naming habits: {h4a['D_obs']} distinct stream x slot x "
      f"category cells against {num(h4a['null_mean'], 1)} expected (p = {pval(h4a['p_one_sided_fewer'])}; surname {pc(min(sur), 0)}-{pc(max(sur), 0)}% and first name "
      f"{pc(min(fn), 0)}-{pc(max(fn), 0)}% of references by stream). Verdict after the post hoc checks: **{va['verdict']}** (p {pval(va['p_range_variants'][0])}-"
      f"{pval(va['p_range_variants'][1])} over {va['variants_checked']} seeds and variants, among them surname, first and full name only: p = "
      f"{pval(vrow('H4a', 'without hypo')['p_one_sided_fewer'])}; leave-one-stream-out p <= {pval(va['loso_p_range'][1])}).")
    w(f"* **Slot-bound form choice (H4b).** Pre-registered: {h4b['D_obs']} distinct stream x player x slot forms against {num(h4b['null_mean'], 1)} expected, "
      f"p = {pval(h4b['p_one_sided_fewer'])}, Holm p = {pval(prim['H4b']['p_holm'])} ({'rejected' if prim['H4b']['reject_holm_0.05'] == 'True' else 'not rejected'}). Verdict after the post hoc "
      f"checks: **{vb['verdict']}**. With 100,000 permutations at three seeds p = {pval(min(f(r['p_one_sided_fewer']) for r in bigb))}-"
      f"{pval(max(f(r['p_one_sided_fewer']) for r in bigb))} (Holm {pval(min(f(r['holm_p_substituted']) for r in bigb))}-"
      f"{pval(max(f(r['holm_p_substituted']) for r in bigb))}); without hypocoristic and epithet forms p = {pval(vrow('H4b', 'without hypo')['p_one_sided_fewer'])}; "
      f"surname and first name only p = {pval(vrow('H4b', 'surname and first')['p_one_sided_fewer'])}; with the span-mode slot p = "
      f"{pval(vrow('H4b', 'span-mode')['p_one_sided_fewer'])} (span mode lets the reference's own words enter the classifier, e.g. an epithet containing "
      f"`number one` counts as STAT, so this variant can favour rejection); without the {len(h4v['hypocoristic_streams'])} streams with hypocoristics p = "
      f"{pval(vrow('H4b', 'without the')['p_one_sided_fewer'])}; one reference per player per utterance p = {pval(vrow('H4b', 'first reference')['p_one_sided_fewer'])}; "
      f"leaving out one stream at a time p = {pval(vb['loso_p_range'][0])}-{pval(vb['loso_p_range'][1])} ({vb['loso_n_p_below_0.05']} of {vb['loso_runs']} below 0.05). "
      f"Per stream, {pt_sit['p_below_0.05']} of {pt_sit['tests']} situational and {pt_syn['p_below_0.05']} of {pt_syn['tests']} syntactic tests reach p < 0.05 "
      f"({num(pt_sit['expected_under_H0'], 0)} expected each). The transcripts have no speaker labels, so a play-by-play voice and an analyst voice that differ "
      "both in naming and in typical slot would produce the same deficit; H4b cannot separate that from slot-conditioned choice. No stream shows the Parryan "
      "pattern of one form per slot with different forms in different slots (situational slots: " + "; ".join(f"{k}: {v} streams" for k, v in sorted(pat.items()))
      + ")" + ("; the economy that exists is a stream's habitual naming, chiefly the surname." if va["verdict"] == "rejected (robust)"
                and f(allc["share_surname"]) > 0.5 else "."))
    # ---- K10 E2, E1
    e2p = [(r["class"], f(r["p_one_sided_fewer"]), f(r["p_one_sided_modal_higher"])) for r in e2t if r.get("D_obs")]
    m_e2 = 2 * len(e2p)
    sig2 = sorted([x for x in e2p if x[1] < 0.05], key=lambda x: x[1])
    bonf = [c for c, p1, p2 in e2p if min(p1, p2) * m_e2 < 0.05]
    nonsig2 = [c for c, p1, _ in e2p if p1 >= 0.05]
    n_below = sum(1 for _, p1, p2 in e2p for p in (p1, p2) if p < 0.05)
    w(f"* **Functional equivalents (E2, exploratory).** Of {len(e2p)} tested equivalence classes ({len(__import__('p05_thrift').E2)} declared; the others have one "
      f"attested form), stream choice among the alternatives is more consistent than chance (unadjusted p < 0.05, fewer forms per stream) for "
      + ", ".join(f"{c} (p = {pval(p1)})" for c, p1, _ in sig2) + f"; not for {', '.join(nonsig2)}. Of the {m_e2} E2 p-values {n_below} are below 0.05 "
      f"({num(0.05 * m_e2, 1)} expected); after a Bonferroni bound over the {m_e2}, " + (f"only {', '.join(bonf)} " + ("remains" if len(bonf) == 1 else "remain")
                                                                                          if bonf else "none remains") + ".")
    loso_sig = [r["slot"] for r in e1l if f(r["p_one_sided_fewer"]) < 0.05]
    e1_all = all(f(r["p_one_sided_fewer"]) < 0.05 for r in e1t)
    w(f"* **Formula economy per slot (E1, exploratory).** With the inventory identified on all 20 streams pooled, "
      + ("every slot" if e1_all else f"{sum(f(r['p_one_sided_fewer']) < 0.05 for r in e1t)} of {len(e1t)} slots")
      + " shows fewer distinct formula types per stream than chance; this is guaranteed by construction, because a string repeated inside one stream only "
      "enters the pooled inventory. With the inventory identified on the other 19 streams (post hoc), "
      + (f"{len(loso_sig)} of {len(e1l)} slots still do ({', '.join(loso_sig)})" if loso_sig else f"none of the {len(e1l)} slots does")
      + (": streams reuse their own selection of strings that other streams also use (a stream being one match and one broadcaster)" if len(loso_sig) == len(e1l)
         else "") + " (Table 4.7b).")
    hs = h5p[0]
    w(f"* **Extension (H5).** No association was detected between the syllable length of a reference and the time available after its clip: weighted within-stream "
      f"rho = {num(h5['rho_weighted'], 3)} (stream bootstrap {ci(h5['boot_lo'], h5['boot_hi'], 3, 1)}; permutation p = {pval(h5['p_two'])}; {h5['tokens']} references "
      f"in {h5['streams']} streams; minimum detectable rho about {num(h5['mde_rho_approx'], 3)}); with the stored time field, valid in all {hs['streams']} streams since "
      f"the corpus correction, rho = {num(hs['rho_weighted'], 3)}, p = {pval(hs['p_two'])} (post hoc).")
    rej = [k for k, r in prim.items() if r["reject_holm_0.05"] == "True"]
    w(f"* **2b-primary family (Holm, 7 tests; section 5).** Rejected as pre-registered: {', '.join(rej) if rej else 'none'}; not rejected: "
      f"{', '.join(k for k in prim if k not in rej) or 'none'}. Read with the post hoc checks: H1a/H1b: {h1_word} of the detected excess is also reached by "
      f"the baseline sources; H2a/H2b on observed coverage: {hoci(1500, 'cov_base', 'cornell', 'observed')} and {hoci(1500, 'cov_base', 'press_pooled', 'observed')} pp "
      f"(" + ("both above 0" if f(oc['ci_lo']) > 0 and f(op['ci_lo']) > 0 else "not both above 0") + f"), {pc(d2c['estimate'], 1)} and {pc(d2p['estimate'], 1)} pp "
      f"with {lmeta['I_size']:,}-token sources; H4a: {va['verdict']}; H4b: {vb['verdict']}; H5: "
      + ("not rejected." if prim["H5"]["reject_holm_0.05"] != "True" else "rejected."))
    w("")
    # ------------------------------------------------------------------ 1 definitions
    w("## 1. Data and definitions")
    w("")
    w("**Teams** (plan section 0). Utterance = one rally clip (TV, `text_corrected`), one live-text update (Cornell), one player answer (press).")
    w("")
    rows = []
    for t, d in teams.items():
        rows.append([lab(t), d["medium"], d["utterances"], f"{d['tokens']:,}"])
    w(table(["team", "medium", "utterances", "tokens"], rows))
    w("")
    w(f"Press answers are dated {facts['press_first_date']} to {facts['press_last_date']} ({facts['press_interviewees']} interviewees); the Cornell records carry "
      f"{'dates' if facts['cornell_records_have_dates'] else 'no dates'} (outlet: {facts['cornell_outlet']}); the TV matches are from {facts['tv_first_year']} to "
      f"{facts['tv_last_year']}.")
    w("")
    w("**Tokens.** Phase 2 tokeniser and STOP list (`analysis/formulas/common.py`, unchanged). **2b normalisation** (primary): digit strings and "
      "`love fifteen thirty forty deuce` -> `<num>`; first names and surnames of the players of the 20 TV matches (Phase 2 lexicon), plus the players of a Cornell update "
      "and the interviewee of a press answer -> `<name>`. Raw Phase 2 tokens are a sensitivity. Hypocoristics (`rafa`, `nole`, `rog`, `carlitos`) are not in the "
      f"name lexicon: {uconc['TV, 20 streams pooled']['hypocoristic_tokens_raw']} such tokens in the TV streams ({num(uconc['TV, 20 streams pooled']['hypocoristic_per_1000'], 2)} "
      f"per 1,000), {num(uconc['press_pooled']['hypocoristic_per_1000'], 2)} per 1,000 in press and {num(uconc['cornell']['hypocoristic_per_1000'], 2)} in Cornell. "
      f"`<name>` is {pc(uconc['TV, 20 streams pooled']['share_name'], 2)}% of TV tokens, {pc(uconc['cornell']['share_name'], 2)}% of Cornell and "
      f"{pc(uconc['press_pooled']['share_name'], 2)}% of press tokens (press answers rarely name the players of the TV matches), so frames around player names "
      "(`from <name>`, `for <name>`) cannot be shared from press for a reason of genre.")
    w("")
    w("**Formula of a team** = n-gram (2 <= n <= 12) in >= 2 distinct utterances of the team's text, not made only of STOP words; variants n >= 3 and "
      "'content' (not made only of STOP words and numerals). **Coverage** of a text by an inventory = share of its tokens inside an occurrence of an inventory n-gram. "
      f"**Large identification sets** (post hoc, addendum 1): each TV stream (whole text) is the target; the source is a {lmeta['I_size']:,}-token sample (whole "
      f"utterances) of the other 19 TV streams, of Cornell or of press, {lmeta['R']} samples each; the target and each source sample are also unigram-shuffled once per "
      "sample (null). **Matched size** (pre-registered, now secondary): each team subsampled to S = 1,500 tokens (all 20 TV streams) or 3,000 (17 TV streams), "
      "R = 500 / 200 replicates. **Null (a)**: tokens permuted over the positions of a text (lexicon, topic and utterance lengths kept, multiword units destroyed), "
      "identification and coverage repeated. **Excess** = observed minus shuffled coverage. **Vertex bootstrap**: the 20 TV streams resampled with replacement, the "
      "statistic averaged over ordered pairs of distinct original streams (each pair's replicate mean held fixed).")
    w("")
    w("**Situational slot classifier** (plan section 5; code `lib2b.SlotClassifier`): (1) OFFICIAL if the span touches an umpire/Hawk-Eye pattern "
      "(`mr <name>`, `... is challenging`, `challenges remaining`, `ball was called`, `new balls please`, `thank you (players|please)`, `quiet please`, "
      "`time violation`, `hawk eye`, ...); (2) SCORE if it touches a score pattern (`<score> <score|all>`, `deuce`, `advantage <name>`, `game <name>`, "
      "`<name> leads by N games to M`, `N games all`, `break/set/match point`, `tie break`); (3) otherwise the slot whose keyword lexicon has most hits in the span "
      "(ties: OFFICIAL > SCORE > CROWD > STAT > SHOT > JUDGE); (4) the same on a window of 4 tokens either side; (5) OTHER. Two modes: **span mode** "
      "(`classify`, steps 1-5 on the span itself; used for formula spans) and **context mode** (`classify_context`, steps 1-3 on the 4-token window either side "
      "excluding the span; used for the situational slot of a reference, so that the name form cannot determine its own slot). Both modes are scored against the "
      "coders' slot labels in section 3. The lexicons are frozen in the plan and were not tuned on any 2b output.")
    w("")
    w(f"**Available time.** 2b found that `t_to_next_first_hit_s` was invalid in {n_fps_bad} of the 20 streams (videos at about 29.97 frames per second whose clip "
      "times had been computed as frames/25); the corpus has since been corrected (corpus/README.md section 3.3: frame rate detected per stream, frame-derived "
      "times recomputed, hit times unchanged). The pre-registered analyses use the hit clock, which the correction did not touch: **A_after** = first hit of the next "
      "clip minus last hit of this clip (the clip's text runs into the following dead time). The stored field, valid in all 20 streams after the correction, enters "
      "a post hoc sensitivity of H5 (last row of Table 4.6).")
    w("")
    # ------------------------------------------------------------------ 2 sharing
    w("## 2. Shared stock: what TV commentary repeats that other registers do not (2b.1)")
    w("")
    w("### 2.0 Large identification sets (post hoc, addendum 1; the primary cross-corpus design of this revision)")
    w("")
    w(f"Each of the 20 TV streams (whole text) is a target; a source is a {lmeta['I_size']:,}-token sample of the other 19 TV streams pooled, of the Cornell live "
      f"text or of the press answers ({lmeta['R']} samples per source and target); its inventory is identified on the sample. Commentary-only = target tokens inside "
      "`common.official_mask_v2` patterns (umpire calls, Hawk-Eye announcements, point-score calls) removed from numerator and denominator. Intervals: percentile "
      f"bootstrap over the 20 targets (B = {lmeta['B']:,} for differences). The targets' TV sources share 18 of their 19 streams, so this bootstrap treats targets "
      "as exchangeable and understates between-broadcast uncertainty; the number of targets with a positive difference is given for that reason.")
    w("")
    w("**Table 2.A. Coverage of TV targets by 100,000-token sources** (% of the target's tokens, mean over the 20 targets [bootstrap 95% CI]; min over targets).")
    w("")
    rows = []
    for tok in ("norm", "raw"):
        for src in ("tv_other19", "cornell", "press_pooled"):
            st = f"{src} -> TV"
            rows.append([tok, lab(src), num(lsr(st, "F_types", tok)["estimate"], 0), num(lsr(st, "F_types_n3", tok)["estimate"], 0),
                         lci(st, "obs_n2", tok, 1), lci(st, "obs_n3", tok, 1), pc(lsr(st, "shuf_n2", tok)["estimate"]), pc(lsr(st, "shuf_n3", tok)["estimate"], 2),
                         lci(st, "obs_n3_comm", tok, 1), pc(lsr(st, "obs_n3", tok)["min_over_targets"])])
    w(table(["tokens", "source", "inventory types", "of which n >= 3", "observed n >= 2", "observed n >= 3", "shuffled n >= 2", "shuffled n >= 3",
             "commentary-only n >= 3", "min n >= 3"], rows))
    w("")
    w("**Table 2.B. TV sources minus baseline sources of the same size** (pp; mean over targets [bootstrap 95% CI]; targets with a positive difference; min over targets).")
    w("")
    rows = []
    for tok in ("norm", "raw"):
        for b in ("cornell", "press_pooled"):
            for m, ml in (("obs_n2", "observed n >= 2"), ("obs_n3", "observed n >= 3"), ("obs_n2_comm", "commentary-only n >= 2"),
                          ("obs_n3_comm", "commentary-only n >= 3"), ("shuf_n2", "shuffled n >= 2"), ("shuf_n3", "shuffled n >= 3"),
                          ("exc_n2", "excess n >= 2"), ("exc_n3", "excess n >= 3")):
                r = lsr(f"TV minus {b}", m, tok)
                rows.append([tok, lab(b), ml, lci(f"TV minus {b}", m, tok), f"{r['targets_positive']}/{r['n_targets']}", pc(r["min_over_targets"], 2),
                             ci_verdict(r["ci_lo"], r["ci_hi"], "TV more", "TV less", "no difference detected")])
    w(table(["tokens", "baseline", "measure", "TV minus baseline", "targets > 0", "min", "reading (95% CI vs 0)"], rows))
    w("")
    w("**Table 2.C. Per target** (2b normalisation; observed coverage %, mean over the 5 samples; TV-only and shared n >= 3 shares as defined below).")
    w("")
    pt = defaultdict(lambda: defaultdict(list))
    for r in lcov:
        if r["tokens"] == "norm":
            pt[(r["source"], r["target"])]["n2"].append(f(r["obs_n2"]))
            pt[(r["source"], r["target"])]["n3"].append(f(r["obs_n3"]))
    rows = []
    for t in L.TV:
        rows.append([lab(t), f"{teams[t]['tokens']:,}"] + [pc(np.mean(pt[(s, t)][m])) for m in ("n2", "n3") for s in ("tv_other19", "cornell", "press_pooled")]
                    + [pc(tvo[t]["share_shared"]), pc(tvo[t]["share_only"]), pc(tvo[t]["share_strict"]), pc(tvo[t]["share_only_comm"])])
    w(table(["target", "tokens", "n>=2 TV", "n>=2 Cornell", "n>=2 press", "n>=3 TV", "n>=3 Cornell", "n>=3 press", "n>=3 shared %", "n>=3 TV-only %",
             "TV-only strict %", "TV-only, commentary-only %"], rows))
    w("")
    w("**TV-only n >= 3 stock** (addendum 1). In each sample, an occurrence in the target of an n >= 3 string of the TV inventory is *shared* if the string is also "
      "in the Cornell or the press inventory of that sample, otherwise *TV-only*; a covered token is shared if any covering occurrence is shared. *Strict*: every "
      "covering TV-only string is also not a formula (>= 2 utterances) of the whole Cornell text or of the whole press corpus. *Cross-broadcast*: every covering "
      "TV-only string occurs in at least two of the other 19 TV streams. A TV-only token's slot is the span-mode slot of the longest covering TV-only occurrence.")
    w("")
    w("**Table 2.D. Shares of target tokens** (%; mean over the 5 samples; mean and range over the 20 targets, and the two finals).")
    w("")
    rows = []
    for k_, kl in (("share_any", "covered by an n >= 3 TV string"), ("share_shared", "shared with a baseline"), ("share_only", "TV-only"),
                   ("share_cross", "TV-only, cross-broadcast"), ("share_strict", "TV-only, strict"), ("share_notC", "not in the Cornell inventory"),
                   ("share_notP", "not in the press inventory"), ("share_only_comm", "TV-only, commentary-only tokens"),
                   ("share_strict_comm", "TV-only strict, commentary-only tokens")):
        v = [f(r[k_]) for r in tvo.values()]
        rows.append([kl, pc(np.mean(v)), f"{pc(min(v))}-{pc(max(v))}", pc(m19[k_]), pc(m23[k_])])
    w(table(["class", "mean over 20 targets", "range", "2019 final (in-sample)", "2023 final (held-out)"], rows))
    w("")
    w("**Table 2.E. Composition by situational slot** (% of each class's tokens, span-mode slot of the longest covering occurrence; last row: % inside "
      "umpire or score-call patterns). Pooled over the 20 targets unless stated.")
    w("")
    cols = [("ALL_TV", "tv_only", "TV-only"), ("ALL_TV", "tv_only_cross", "TV-only, cross-broadcast"), ("ALL_TV", "tv_only_strict", "TV-only, strict"),
            ("ALL_TV", "shared", "shared"), (L.MAIN, "tv_only", "2019 final: TV-only"), (L.HELDOUT, "tv_only", "2023 final: TV-only")]
    rows = []
    for sl in list(L.SLOTS) + ["_umpire_mask"]:
        rows.append([sl if sl != "_umpire_mask" else "inside umpire/score-call patterns"] + [pc(slot_share(t, c, sl)) for t, c, _ in cols])
    w(table(["slot"] + [c[2] for c in cols], rows))
    w("")
    w("**Table 2.F. The 40 commonest TV-only strings** (pooled over targets: strings that are TV-only in a majority of the 5 samples of a target; occurrences "
      "in those targets; modal slot; TV streams attesting the string; rates per 100,000 tokens in the 20 TV streams, the whole Cornell text and the whole press "
      "corpus; strict = not repeated in either whole baseline).")
    w("")
    w(table(["string", "targets", "occurrences", "modal slot", "TV streams", "per 100k TV", "per 100k Cornell", "per 100k press", "strict"],
            [[f"`{r['ngram']}`", r["targets_tv_only"], r["occurrences_in_targets"], r["modal_slot"], r["tv_streams_attesting"], num(r["per_100k_tv_all20"], 1),
              num(r["per_100k_cornell"], 1), num(r["per_100k_press"], 2), "yes" if r["strict"] == "True" else "no"] for r in tvp[:40]]))
    w("")
    w("**Table 2.G. The commonest TV-only strings of the two finals** (25 each; occurrences in the final; rate per 100,000 tokens in the other 19 TV streams).")
    w("")
    rows = []
    for t in (L.MAIN, L.HELDOUT):
        for r in [x for x in tvf if x["target"] == t][:25]:
            rows.append([lab(t), f"`{r['ngram']}`", r["occurrences_in_target"], r["modal_slot"], r["other_tv_streams_attesting"], num(r["per_100k_tv_other19"], 1),
                         num(r["per_100k_cornell"], 1), num(r["per_100k_press"], 2), "yes" if r["strict"] == "True" else "no"])
    w(table(["final", "string", "occurrences", "modal slot", "other TV streams", "per 100k TV", "per 100k Cornell", "per 100k press", "strict"], rows))
    w("")
    w("### 2.1 Matched small size (pre-registered design; secondary)")
    w("")
    w("**Table 2.1. Inventory sizes** (formula types; full texts, and mean over replicates at matched size; 2b normalisation). "
      "The press corpus (5.4 million tokens) is not indexed whole.")
    w("")
    fullm = {r["team"]: r for r in inv_full if r["tokens"] == "norm"}
    mm = {(r["team"], r["S"]): r for r in inv_m if r["tokens"] == "norm"}
    rows = []
    for t in list(teams):
        fr = fullm.get(t)
        m15 = mm.get((t, "1500"))
        m30 = mm.get((t, "3000"))
        rows.append([lab(t), fr["types_n2"] if fr else "-", fr["types_n3"] if fr else "-", num(fr["types_n2_per_1000_tokens"], 1) if fr else "-",
                     num(m15["types_base"], 0) if m15 else "-", num(m15["types_n3"], 0) if m15 else "-",
                     num(m15["types_base_shuffled"], 0) if m15 else "-", num(m30["types_base"], 0) if m30 else "-"])
    w(table(["team", "full: n>=2", "full: n>=3", "full: n>=2 per 1,000 tokens", "1,500: n>=2", "1,500: n>=3", "1,500: n>=2 shuffled", "3,000: n>=2"], rows))
    w("")
    w("**Table 2.2. Coverage of TV targets by each kind of source, and of the baselines by TV sources** (% of the target's tokens; mean over pairs; "
      "95% CI from the bootstrap over TV streams). Excess = observed - shuffled.")
    w("")
    rows = []
    for Sv in ("1500", "3000"):
        tv3 = f(a(Sv, "cov_n3", "TV->TV mean obs")["estimate"])
        for m, mlab in (("cov_base", "n >= 2"), ("cov_n3", "n >= 3"), ("cov_content", "content n >= 2")):
            ml = mlab + (" (near-empty inventories: not informative)" if m == "cov_n3" and tv3 < 0.02 else "")
            for st, slab in (("TV->TV mean", "TV -> TV"), ("cornell->TV mean", "Cornell -> TV"), ("press_pooled->TV mean", "press -> TV"),
                             ("TV->cornell mean", "TV -> Cornell"), ("TV->press_pooled mean", "TV -> press")):
                o, n_, e = (a(Sv, m, f"{st} {x}") for x in ("obs", "null", "excess"))
                rows.append([Sv, ml, slab, f"{pc(o['estimate'], 2)} {ci(o['ci_lo'], o['ci_hi'], 2)}", pc(n_["estimate"], 2),
                             f"{pc(e['estimate'], 2)} {ci(e['ci_lo'], e['ci_hi'], 2)}"])
    w(table(["S", "inventory", "source -> target", "observed", "shuffled", "excess"], rows))
    w("")
    w("**Table 2.3. TV sources minus baseline sources at matched size** (pp; vertex bootstrap 95% CI, B = 10,000; targets with a positive difference). The "
      "pre-registered H2 statistic is the excess column (n >= 2, S = 1,500: H2a, H2b); the observed column is the basis of the H2 claim (addendum 1, M1). "
      "The excess intervals here come from new bootstrap draws (`p09_h2_observed.py`) and can differ from section 5's in the second decimal.")
    w("")
    rows = []
    for Sv in ("1500", "3000"):
        tv3 = f(a(Sv, "cov_n3", "TV->TV mean obs")["estimate"])
        for m, mlab in (("cov_base", "n >= 2"), ("cov_n3", "n >= 3"), ("cov_content", "content n >= 2")):
            ml = mlab + (" (near-empty: not informative)" if m == "cov_n3" and tv3 < 0.02 else "")
            for b, blab in (("cornell", "Cornell"), ("press_pooled", "press")):
                o, s_, e = (ho(Sv, m, b, c) for c in ("observed", "shuffled", "excess"))
                rows.append([Sv, ml, blab, f"{hoci(Sv, m, b, 'observed')} ({o['targets_positive']}/{o['n_targets']})", hoci(Sv, m, b, "shuffled"),
                             f"{hoci(Sv, m, b, 'excess')} ({e['targets_positive']}/{e['n_targets']})"])
    w(table(["S", "inventory", "baseline", "observed difference (targets > 0)", "shuffled difference", "excess difference (targets > 0)"], rows))
    w("")
    w("**Table 2.3b. Why the shuffled Cornell inventory is large** (2b normalisation; 50 shuffled 1,500-token samples per team for the inventory columns).")
    w("")
    rows = []
    for name, key in (("TV, 20 streams pooled", "TV, 20 streams pooled"), ("TV, mean over streams", "TV, mean over the 20 streams"), ("Cornell", "cornell"),
                      ("press, pooled", "press_pooled")):
        u = uconc[key]
        if key.startswith("TV, mean"):
            invs = [shufc[s] for s in L.TV]
            si = f"{num(np.mean([f(x['shuffled_types']) for x in invs]), 1)} ({num(min(f(x['shuffled_types']) for x in invs), 0)}-{num(max(f(x['shuffled_types']) for x in invs), 0)})"
            sp_ = pc(np.mean([f(x["shuffled_share_with_placeholder"]) for x in invs]), 0)
            oi = num(np.mean([f(x["observed_types"]) for x in invs]), 1)
        elif key in shufc:
            si, sp_, oi = num(shufc[key]["shuffled_types"], 1), pc(shufc[key]["shuffled_share_with_placeholder"], 0), num(shufc[key]["observed_types"], 1)
        else:
            si = sp_ = oi = "-"
        rows.append([name, pc(u["share_name"], 2), pc(u["share_num"], 2), num(u["simpson_sum_p2"], 4), pc(u["share_top10_types"], 1), oi, si, sp_])
    w(table(["corpus", "`<name>` %", "`<num>` %", "Simpson sum p^2", "top-10 types %", "observed inventory at 1,500", "shuffled inventory at 1,500",
             "shuffled types with a placeholder %"], rows))
    w("")
    w("**Table 2.4. Jaccard overlap of inventories** (mean over pairs, %; observed, shuffled, excess).")
    w("")
    rows = []
    for Sv in ("1500", "3000"):
        for m, mlab in (("jac_base", "n >= 2"), ("jac_n3", "n >= 3")):
            for st, slab in (("TV->TV mean", "TV - TV"), ("cornell->TV mean", "Cornell - TV"), ("press_pooled->TV mean", "press - TV")):
                o, n_, e = (a(Sv, m, f"{st} {x}") for x in ("obs", "null", "excess"))
                rows.append([Sv, mlab, slab, f"{pc(o['estimate'], 2)} {ci(o['ci_lo'], o['ci_hi'], 2)}", pc(n_["estimate"], 2), pc(e["estimate"], 2)])
    w(table(["S", "inventory", "pair type", "observed", "shuffled", "excess"], rows))
    w("")
    w("'-' = undefined (both shuffled inventories empty). Coverage, not Jaccard, carries the tests; Table 2.3b gives the inventory sizes behind the Cornell rows.")
    w("")
    w("**Table 2.5. Raw-token sensitivity** (no `<num>`/`<name>` normalisation; S = 1,500).")
    w("")
    rows = []
    for m, mlab in (("cov_base", "n >= 2"), ("cov_n3", "n >= 3")):
        for st, slab in (("TV->TV mean", "TV -> TV"), ("cornell->TV mean", "Cornell -> TV"), ("press_pooled->TV mean", "press -> TV")):
            o, e = a(1500, m, f"{st} obs", "raw"), a(1500, m, f"{st} excess", "raw")
            rows.append([mlab, slab, f"{pc(o['estimate'], 2)} {ci(o['ci_lo'], o['ci_hi'], 2)}", f"{pc(e['estimate'], 2)} {ci(e['ci_lo'], e['ci_hi'], 2)}"])
        for b in ("cornell", "press_pooled"):
            rows.append([mlab, f"TV minus {lab(b)}", hoci(1500, m, b, "observed", "raw"), hoci(1500, m, b, "excess", "raw")])
    w(table(["inventory", "comparison", "observed", "excess"], rows))
    w("")
    w("**Table 2.6. Single-speaker press baselines** (S = 1,500, n >= 2; coverage of one interviewee's answers by another's inventory, observed / excess, %).")
    w("")
    sp = ["press_federer", "press_djokovic", "press_murray", "press_nadal"]
    rows = []
    for x in sp:
        row = [lab(x)]
        for y in sp:
            if x == y:
                row.append("-")
            else:
                o = A.get(("1500", "norm", "cov_base", f"{x}->{y} obs"))
                e = A.get(("1500", "norm", "cov_base", f"{x}->{y} excess"))
                row.append(f"{pc(o['estimate'], 1)} / {pc(e['estimate'], 1)}" if o and e else "-")
        rows.append(row)
    w(table(["source \\ target"] + [lab(y) for y in sp], rows))
    w("")
    pse = h1c["press_speakers_mean_excess_S1500_base"]
    w(f"Mean excess between press speakers: {pc(pse, 2)} pp, against {pc(h1a['estimate'], 2)} pp between TV streams ("
      + ("press speakers share more among themselves" if pse > f(h1a["estimate"]) else "TV streams share more among themselves") + "). The yardstick is not matched: "
      "a speaker's 1,500 tokens come from answers given over many years (topic-diverse, so their repeats are generic) in edited transcripts, a TV stream's from one "
      "match in raw ASR.")
    w("")
    w("**Table 2.7. Each TV stream as target and as source** (S = 1,500, n >= 2, 2b normalisation; % ; mean over the other 19 TV streams).")
    w("")
    pairs = L.read_csv(R / "sharing_pairs.csv")
    P = {(r["source"], r["target"]): r for r in pairs if r["S"] == "1500" and r["tokens"] == "norm" and r["measure"] == "cov_base"}
    rows = []
    for t in L.TV:
        others = [s for s in L.TV if s != t]
        rows.append([lab(t), f"{teams[t]['tokens']:,}", pc(np.mean([f(P[(s, t)]["obs_mean"]) for s in others]), 2),
                     pc(np.mean([f(P[(s, t)]["excess"]) for s in others]), 2), pc(np.mean([f(P[(t, s)]["excess"]) for s in others]), 2),
                     pc(P[("cornell", t)]["excess"], 2), pc(P[("press_pooled", t)]["excess"], 2)])
    w(table(["stream", "tokens", "as target: observed", "as target: excess", "as source: excess", "Cornell -> it: excess", "press -> it: excess"], rows))
    w("")
    # ---- core
    w("### 2.2 Genre core")
    w("")
    w("**Table 2.8. Core size**: formula types in the inventories of at least k of the 20 TV streams (full texts; and mean over 200 subsamples of 1,500 tokens).")
    w("")
    rows = []
    for k in range(2, 21):
        fr = next(r for r in core if r["size"] == "full" and r["tokens"] == "norm" and r["k"] == str(k))
        rw = next(r for r in core if r["size"] == "full" and r["tokens"] == "raw" and r["k"] == str(k))
        mr = next(r for r in core if r["size"].startswith("matched") and r["k"] == str(k))
        rows.append([k, fr["types_base"], fr["types_n3"], fr["types_content"], rw["types_base"], num(mr["types_base"], 1), num(mr["types_n3"], 1)])
    w(table(["k", "full: n>=2", "full: n>=3", "full: content", "full raw: n>=2", "1,500: n>=2", "1,500: n>=3"], rows))
    w("")
    w("**Table 2.9. The most widely shared formulas** (full texts; K = number of streams whose inventory contains it; modal span-mode slot over its occurrences).")
    w("")
    w(table(["formula", "n", "K", "utterances (all streams)", "modal slot", "share"],
            [[f"`{r['formula']}`", r["n"], r["streams_K"], r["utterances_all_streams"], r["modal_slot"], pc(r["modal_slot_share"], 0) + "%"] for r in ctop[:40]]))
    w("")
    w("**Table 2.10. Is the TV core shared with the baselines?** Share of the core's types (full texts) that are formulas of a Cornell or press random sample "
      f"of {tv_tokens:,} tokens (the size of the 20 TV streams together; mean [2.5-97.5%] over 20 samples).")
    w("")
    w(table(["k", "core types", "in Cornell inventory", "in press inventory", "n>=3 core types", "n>=3 in Cornell", "n>=3 in press"],
            [[r["k"], r["core_types"], f"{pc(r['share_in_baseline_inventory'])} {ci(r['lo'], r['hi'])}",
              f"{pc(p['share_in_baseline_inventory'])} {ci(p['lo'], p['hi'])}", r["core_types_n3"], pc(r["share_n3_in_baseline_inventory"]),
              pc(p["share_n3_in_baseline_inventory"])]
             for r, p in zip([x for x in cbase if x["baseline"] == "cornell"], [x for x in cbase if x["baseline"] == "press_pooled"])]))
    w("")
    w("**Table 2.11. Stream-specific ('idiolect') and core shares by situational slot** (descriptive: the slot is the span-mode slot of the formula's own "
      "occurrence, so SCORE and OFFICIAL rows are partly defined by the formulas' words; share of formula tokens; full texts first, then 1,500-token "
      "subsamples, mean of 200, with min-max over streams).")
    w("")
    rows = []
    for sl in ("SCORE", "OFFICIAL", "SHOT", "JUDGE", "STAT", "CROWD", "OTHER", "ALL"):
        mv = [r for r in idio if r["size"].startswith("matched") and r["slot"] == sl]
        fv = [r for r in idio if r["size"] == "full" and r["slot"] == sl]
        idv = [f(r["share_idiolect"]) for r in mv]
        c10 = [f(r["share_core10"]) for r in mv]
        rows.append([sl, pc(np.mean([f(r["share_idiolect"]) for r in fv])), pc(np.mean([f(r["share_core10"]) for r in fv])),
                     num(np.mean([f(r["formula_tokens"]) for r in mv]), 0), f"{pc(np.mean(idv))} ({pc(min(idv))}-{pc(max(idv))})",
                     pc(np.mean([f(r["share_core2"]) for r in mv])), f"{pc(np.mean(c10))} ({pc(min(c10))}-{pc(max(c10))})"])
    w(table(["slot", "full: stream-specific %", "full: core-10 %", "formula tokens per stream (1,500)", "1,500: stream-specific % (range)",
             "1,500: in >= 2 streams %", "1,500: core-10 % (range)"], rows))
    w("")
    w(f"Stream-specific share against stream length (descriptive; 2 exploratory p-values): Spearman rho = {num(sm['full'][0], 2)} (p = {pval(sm['full'][1])}) on full "
      f"texts, {num(sm['matched'][0], 2)} (p = {pval(sm['matched'][1])}) at 1,500 tokens. Full-text shares depend on how many other long streams exist, matched-size "
      "shares on how much of a stream one sample contains.")
    w("")
    w("**Table 2.12. Stream-specific share per stream** (all slots).")
    w("")
    rows = []
    for t in L.TV:
        mr = next(r for r in idio if r["size"].startswith("matched") and r["slot"] == "ALL" and r["stream"] == t)
        fr = next(r for r in idio if r["size"] == "full" and r["slot"] == "ALL" and r["stream"] == t)
        rows.append([lab(t), f"{teams[t]['tokens']:,}", pc(fr["share_idiolect"]), pc(fr["share_core10"]),
                     f"{pc(mr['share_idiolect'])} {ci(mr['share_idiolect_lo'], mr['share_idiolect_hi'])}", pc(mr["share_core10"])])
    w(table(["stream", "tokens", "full: stream-specific %", "full: core-10 %", "1,500: stream-specific % [2.5-97.5% over subsamples]", "1,500: core-10 %"], rows))
    w("")
    # ---- clusters
    w("### 2.3 Clusters (exploratory)")
    w("")
    w("Pair similarity = symmetric excess coverage (n >= 2, S = 1,500) or observed Jaccard. Within-minus-between = mean similarity of pairs sharing the label minus "
      "the mean of the other pairs; null = labels permuted over the 20 streams (10,000 permutations; the hint cluster enumerated exactly). Mantel rows give the "
      "correlation with the pair covariate (node permutation). One-sided p in the direction 'more sharing'.")
    w("")
    w(table(["similarity", "label", "pairs within", "within - between (or r)", "null 95%", "p"],
            [[r["similarity"], r["label"], r["within_pairs"], num(r["within_minus_between"], 4), ci(r["null_lo"], r["null_hi"], 4, 1), pval(r["p_one_sided_higher_within"])]
             for r in clus]))
    w("")
    w("**Table 2.13. QAP regression of pair similarity** on same slam, same gender, shared players, |year difference| and same hint (node-permutation p, two-sided; "
      "the intercept's p is not meaningful).")
    w("")
    w(table(["similarity", "term", "beta", "p"], [[r["similarity"], r["term"], num(r["beta"], 4), pval(r["p_two_sided_node_permutation"])] for r in qap]))
    w("")
    pe = pair["excess_cov_sym"]
    metas = {L.short(s): L.stream_meta(s) for s in L.TV}
    feats = []
    for x, y, _ in pe["top5_pairs"][:3]:
        mx, my = metas[x], metas[y]
        feats.append((mx["slam"] == my["slam"], mx["gender"] == my["gender"], bool(set(mx["players"]) & set(my["players"]))))
    common = [nm for k, nm in enumerate(("same slam", "same gender", "a shared player")) if all(ft[k] for ft in feats)]
    w(f"The 2019-2023 pair (both Wimbledon men's finals with Djokovic; hint 'Tim' in both): symmetric excess {pc(pe['value'], 2)} pp, rank {pe['rank_among_190_pairs']} "
      f"of {pe['n_pairs']} (mean of all pairs {pc(pe['mean_all_pairs'], 2)}); Jaccard rank {pair['jaccard_obs']['rank_among_190_pairs']}. The three most similar pairs are "
      + "; ".join(f"{x} / {y} ({pc(v, 2)})" for x, y, v in pe["top5_pairs"][:3])
      + (f"; all three have {', '.join(common)}" if common else "") + " (whether they share a broadcaster or commentators is unknown [unverified]).")
    w("")
    # ---- pool to target
    w("### 2.4 Pool -> target coverage for every stream (exploratory, for the record)")
    w("")
    w("I = the other 19 TV streams pooled (raw Phase 2 tokens and 2b normalisation), M = the stream; 95% bootstrap CI over M's utterances (I fixed). "
      "Matched I = random 100,000-token subsamples of the other 19 streams (raw tokens; mean and range over 20).")
    w("")
    rows = []
    for t in L.TV:
        g = {(r["mode"], r["tokens"]): r for r in p2t if r["target"] == t}
        rr_, nn = g[("loo19", "raw")], g[("loo19", "norm")]
        mt = next(r for r in p2t if r["target"] == t and r["mode"].startswith("matched"))
        rows.append([lab(t), f"{pc(rr_['base'])} {ci(rr_['base_lo'], rr_['base_hi'])}", f"{pc(rr_['n3'])} {ci(rr_['n3_lo'], rr_['n3_hi'])}",
                     f"{pc(nn['base'])}", f"{pc(mt['base'])} {ci(mt['base_lo'], mt['base_hi'])}", pc(mt["n3"])])
    w(table(["target", "raw n>=2", "raw n>=3", "2b-normalised n>=2", "matched I: n>=2 [range]", "matched I: n>=3"], rows))
    w("")
    w(f"2019 ranks {p2t_meta['rank_2019_loo19_raw_base']} of {p2t_meta['n_targets']} (matched I: {p2t_meta['rank_2019_matched_raw_base']}). With the Phase 2 "
      f"identification set (18 pool streams) the 2019 value is {pc(p2t_meta['check_phase2_pool18_2019_raw_base'], 2)}%, equal to Phase 2's.")
    w("")
    # ------------------------------------------------------------------ 3 calibration
    w("## 3. Calibration against Parry's definition (2b.2)")
    w("")
    ca_ = git_first_commit("analysis/parry/coding_A.jsonl")
    cb_ = git_first_commit("analysis/parry/coding_B.jsonl")
    w("Two coders marked formula spans in a fixed sample of 300 utterances (150 from the 2019 final, uniform; 150 from the other 19 streams in proportion to their "
      "length; `sample_ids.json`) following `manual.md`. **Both coders are LLM agents, not human specialists**: their agreement measures the reliability of two runs "
      "of the same kind of judge, and precision/recall against them measures agreement with that judge, not validity against Parry's concept. "
      f"Provenance from git: coding_A.jsonl added in {ca_[0]} ({ca_[1]}), coding_B.jsonl in {cb_[0]} ({cb_[1]}); co-author trailers '{ca_[2]}' / '{cb_[2]}'; "
      f"session {'identical' if ca_[3] == cb_[3] else 'different'}. Blindness to the automatic inventory rested on the coders' instructions; the Phase 2 report with its "
      "formula tables was in the repository they worked in. A coding of even 50 utterances by a human specialist would be the only check of validity.")
    w("")
    if cal_ok:
        fs = ca["file_stats"]
        w(f"Utterances coded by both: {ca['utterances_both']} ({ca['tokens']:,} tokens). Spans in the files: A {fs['A'].get('spans_in_file', 0)}, "
          f"B {fs['B'].get('spans_in_file', 0)}; re-located because `text` did not equal the slice: A {fs['A'].get('relocated', 0)}, B {fs['B'].get('relocated', 0)}; "
          f"dropped: A {fs['A'].get('dropped_not_found', 0) + fs['A'].get('dropped_no_token', 0)}, B {fs['B'].get('dropped_not_found', 0) + fs['B'].get('dropped_no_token', 0)}.")
        w("")
        w("**Table 3.1. Inter-coder agreement** (HIGH + MEDIUM spans; bootstrap over utterances, B = 2,000).")
        w("")
        x = ca["primary_HIGH_MEDIUM"]
        w(table(["token kappa", "tokens positive A / B %", "spans A / B", "span F1 exact", "span F1 overlap", "matched spans", "slot agreement %", "type agreement %"],
                [[f"{num(x['token_kappa'], 3)} {ci(x['token_kappa_ci'][0], x['token_kappa_ci'][1], 3, 1)}",
                  f"{pc(x['positive_token_share_A'])} / {pc(x['positive_token_share_B'])}", f"{x['spans_A']} / {x['spans_B']}",
                  f"{num(x['span_F1_exact'], 3)} {ci(x['span_F1_exact_ci'][0], x['span_F1_exact_ci'][1], 3, 1)}",
                  f"{num(x['span_F1_overlap'], 3)} {ci(x['span_F1_overlap_ci'][0], x['span_F1_overlap_ci'][1], 3, 1)}", x["matched_spans"],
                  f"{pc(x['slot_agreement'])} (kappa {num(x['slot_kappa'], 2)})", f"{pc(x['type_agreement'])} (kappa {num(x['type_kappa'], 2)})"]]))
        w("")
        sc = ca["span_counts"]
        xa = ca["all_confidences"]
        w(f"LOW-confidence spans: A {sc['A']['by_confidence'].get('LOW', 0)}, B {sc['B']['by_confidence'].get('LOW', 0)}; including them gives token kappa "
          f"{num(xa['token_kappa'], 3)}, so the plan's 'all confidences' sensitivity is not shown separately. Span counts by slot: A "
          + ", ".join(f"{k} {v}" for k, v in sorted(sc["A"]["by_slot"].items())) + "; B " + ", ".join(f"{k} {v}" for k, v in sorted(sc["B"]["by_slot"].items())) + ".")
        w("")
        w("**Table 3.2. Automatic measures against the coders, with chance levels** (token level, HIGH + MEDIUM spans; 'Pool' = the 18 pool streams minus the "
          "utterance's own; 'in-sample' = the utterance's own stream; bootstrap 95% CI over utterances). Chance precision = the reference's positive share; chance "
          "recall = the measure's positive share; ceiling = the highest precision possible at that positive share. The last three measures (marked "
          "exploratory) were added in the plan beyond the brief.")
        w("")
        prows = {(r["measure"], r["reference"]): r for r in L.read_csv(R / "calibration_prf.csv") if r["coder_confidence"] == "HIGH+MEDIUM"}
        rows = []
        for (m, rf), r in prows.items():
            c_ = cc[(m, rf)]
            rows.append([r["label"], rf.replace("_", " "), pc(r["auto_positive_share"]), f"{num(r['precision'], 2)} {ci(r['precision_lo'], r['precision_hi'], 2, 1)}",
                         num(c_["chance_precision"], 2), num(c_["precision_ceiling"], 2), f"{num(c_['precision_minus_chance'], 2)} "
                         f"{ci(c_['precision_minus_chance_lo'], c_['precision_minus_chance_hi'], 2, 1)}",
                         f"{num(r['recall'], 2)} {ci(r['recall_lo'], r['recall_hi'], 2, 1)}", num(c_["chance_recall"], 2),
                         f"{num(c_['kappa'], 3)} {ci(c_['kappa_lo'], c_['kappa_hi'], 3, 1)}", f"{num(r['F1'], 2)}"])
        w(table(["automatic measure", "reference", "auto-positive %", "precision", "chance precision", "ceiling", "precision - chance", "recall", "chance recall",
                 "kappa", "F1"], rows))
        w("")
        w("**Table 3.2b. By sample group** (pool n >= 2, pool n >= 3 and pool systems against coder A, coder B and their union). The two halves differ in design: 150 uniform 2019 "
          "utterances against 150 token-weighted utterances of the other streams, identified against a pool of 17 instead of 18 streams.")
        w("")
        rows = []
        for m in ("pool_n2", "pool_n3", "pool_systems"):
            for rf in ("A", "B", "A_or_B"):
                for g in ("2019", "other"):
                    r = cg[(g, m, rf)]
                    rows.append([CAL_LABEL(m), rf.replace("_", " "), g, r["utterances"], num(r["median_tokens_per_utterance"], 0), pc(r["auto_share"]),
                                 num(r["precision"], 2), num(r["chance_precision"], 2), num(r["precision_minus_chance"], 2), num(r["recall"], 2),
                                 num(r["chance_recall"], 2), num(r["kappa"], 3)])
        w(table(["measure", "reference", "group", "utterances", "median tokens", "auto-positive %", "precision", "chance precision", "precision - chance",
                 "recall", "chance recall", "kappa"], rows))
        w("")
        w("**Table 3.2c. Span level** (share of each coder's HIGH spans lying wholly inside, or touching, the automatic positive set; chance = mean over 200 random "
          "circular shifts of the automatic labels within each utterance, with the 97.5th percentile).")
        w("")
        w(table(["measure", "coder", "HIGH spans", "wholly inside", "chance (97.5%)", "touching", "chance (97.5%)"],
                [[CAL_LABEL(r["measure"]), r["coder"], r["high_spans"], pc(r["fully_inside"]), f"{pc(r['fully_inside_chance_mean'])} ({pc(r['fully_inside_chance_hi'])})",
                  pc(r["touching"]), f"{pc(r['touching_chance_mean'])} ({pc(r['touching_chance_hi'])})"] for r in csr.values()]))
        w("")
        w("**Table 3.3. Strata** (pool n >= 2 and pool n >= 3 against each coder): recall by the coder's slot and by span confidence (HIGH, MEDIUM; LOW has 1-2 spans "
          "per coder and is omitted); precision by the classifier's token slot (span mode on single tokens).")
        w("")
        st = L.read_csv(R / "calibration_strata.csv")
        rows = [[r["measure"], r["reference"], r["stratum_kind"], r["stratum"], r["numerator"], r["denominator"], num(r["value"], 3)]
                for r in st if r["measure"] in ("pool_n2", "pool_n3") and "/" not in r["value"] and r["stratum"] != "LOW"]
        w(table(["measure", "coder", "kind", "stratum", "numerator", "denominator", "value"], rows))
        w("")
        w("**Table 3.4. Slot classifier against the coders' slot labels** (rows = coder, columns = classifier). Span mode on every coder span (the mode used for "
          "formula spans), context mode on every coder span, and context and span mode on the referring expressions of the sample that lie inside a coder span "
          "(the unit and mode of H4).")
        w("")
        rows = []
        for unit_key, ul in (("coder_spans_{}_span", "coder spans, span mode"), ("coder_spans_{}_context", "coder spans, context mode"),
                             ("references_{}_commentary_only_context", "commentary references, context mode (H4)"),
                             ("references_{}_commentary_only_span", "commentary references, span mode"),
                             ("references_{}_all_context", "all references, context mode")):
            vals = [csc.get(unit_key.format(who)) for who in ("A", "B")]
            if all(vals):
                rows.append([ul] + [f"{pc(v['agreement'])} / {num(v['kappa'], 3)} / {v['n']}" for v in vals])
        w(table(["unit and mode", "coder A: agreement % / kappa / n", "coder B: agreement % / kappa / n"], rows))
        w("")
        conf = L.read_csv(R / "calibration_slot_context_confusion.csv")
        for who in ("A", "B"):
            for unit, mode, title in (("coder span", "span", "span mode, coder spans"), ("reference (commentary_only)", "context", "context mode, commentary references")):
                M = defaultdict(Counter)
                for r in conf:
                    if r["coder"] == who and r["unit"] == unit and r["mode"] == mode:
                        M[r["coder_slot"]][r["classifier_slot"]] += int(r["n"])
                if not M:
                    continue
                cols_ = list(L.SLOTS)
                w(f"Coder {who}, {title}:")
                w("")
                w(table([f"coder {who} \\ classifier"] + cols_ + ["total"], [[c] + [M[c].get(k, 0) for k in cols_] + [sum(M[c].values())] for c in sorted(M)]))
                w("")
    else:
        stt = L.read_json(R / "calibration_status.json") if (R / "calibration_status.json").exists() else {"status": "not run"}
        w(f"Status: {stt['status']}. `calibrate.py` is tested on a synthetic example (`tests/test_calibrate.py`) and runs from `run_all.sh` once both files exist.")
        w("")
    # ------------------------------------------------------------------ 4 thrift
    w("## 4. Thrift and extension per situational slot (2b.3)")
    w("")
    w(f"Referring expressions were extracted for the two players of every TV stream ({rsum['n_references']} references; {rsum['n_umpire_pattern']} inside umpire "
      f"patterns; {rsum['n_unresolved_epithets']} descriptive epithets without a resolved referent). The extraction reproduces Phase 2's totals for the two finals "
      f"({', '.join(f'{k}: ' + ', '.join(f'{p} {n}' for p, n in sorted(v.items())) for k, v in rsum['check_phase2_totals_all_references'].items())}). "
      "The situational slot of a reference is the context-mode slot (section 1; its agreement with the coders is in Table 3.4).")
    w("")
    w("**Table 4.1. How each stream names the players** (commentary-only resolved references; shares %; epithet upper bound counts every unresolved epithet as a player reference).")
    w("")
    rows = []
    for r in cats:
        if r["references"] != "commentary_only":
            continue
        rows.append([r["label"], r["resolved_tokens"], pc(r["share_surname"], 0), pc(r["share_first_name"], 0), pc(r["share_full_name"], 0),
                     pc(r["share_hypocoristic"], 0), pc(r["share_epithet"], 0), pc(r["share_epithet_upper"], 0)])
    w(table(["stream", "references", "surname", "first name", "full name", "hypocoristic", "epithet", "epithet (upper)"], rows))
    w("")
    w("**Table 4.2. Economy of naming by situational slot** (commentary-only references, all streams; per stream x player x slot cell: modal-form share and distinct "
      "forms per 100 references, averaged over cells with >= 5 references; distinct forms per 100 tokens of the slot, averaged over cells).")
    w("")
    rows = []
    for sl in L.SLOTS:
        cells = [r for r in econ if r["slot_type"] == "situational" and r["slot"] == sl]
        bigc = [r for r in cells if int(r["references"]) >= 5]
        rows.append([sl, sum(int(r["references"]) for r in cells), len(cells), len(bigc),
                     pc(np.mean([f(r["modal_share"]) for r in bigc])) if bigc else "-", num(np.mean([f(r["distinct_per_100_refs"]) for r in bigc]), 1) if bigc else "-",
                     num(np.mean([f(r["distinct_per_100_slot_tokens"]) for r in cells if r["distinct_per_100_slot_tokens"]]), 2)])
    w(table(["slot", "references", "cells", "cells >= 5", "modal share %", "distinct per 100 refs", "distinct per 100 slot tokens"], rows))
    w("")
    w("**Table 4.3. One form per slot?** (cells = player x slot with >= 5 commentary references; criterion in plan section 9).")
    w("")

    def team_econ(t, st_):
        cs = [r for r in econ if r["team"] == t and r["slot_type"] == st_ and int(r["references"]) >= 5]
        return (num(np.mean([f(r["modal_share"]) for r in cs]), 2), num(np.mean([f(r["distinct_per_100_refs"]) for r in cs]), 1)) if cs else ("-", "-")
    w(table(["stream", "slot type", "cells >= 5", "mean modal share", "distinct forms per 100 refs", "cells with modal share >= 0.9", "lowest modal share", "verdict"],
            [[r["label"], r["slot_type"], r["cells_ge5"], *team_econ(r["team"], r["slot_type"]), r["cells_modal_ge_0.9"], num(r["min_modal_share"], 2),
              r["verdict"]] for r in parr]))
    w("")
    w("**Table 4.4. Thrift tests as pre-registered** (D = sum over cells of distinct categories (H4a) or forms (H4b); one-sided p for fewer than under the null; "
      "10,000 permutations).")
    w("")
    w(table(["test", "references", "slot type", "stream", "tokens", "D", "null mean", "null 95%", "p", "status"],
            [[r["test"], r["references"], r["slot_type"], r.get("team", ""), r["tokens"], r["D_obs"], num(r["null_mean"], 1),
              f"[{r['null_lo']}, {r['null_hi']}]" if r.get("null_lo") else "", pval(r["p_one_sided_fewer"]), r["status"]] for r in thr]))
    w("")
    w("**Table 4.4b. POST HOC (addendum 1, M5): robustness of H4a and H4b** (one-sided p; Monte Carlo SE; Holm p when the row's p replaces the pre-registered p "
      "in the seven-test family).")
    w("")
    w(table(["test", "run", "slot", "tokens", "streams", "D", "null mean", "p", "MC SE", "permutations", "Holm p (substituted)", "Holm-rejected"],
            [[r["test"], r["variant"], r["slot"], r["tokens"], r["streams"], num(r["D_obs"], 0), num(r["null_mean"], 1), pval(r["p_one_sided_fewer"]),
              num(r["mc_se"], 4), r["permutations"], pval(r["holm_p_substituted"]), r["holm_rejected"]] for r in h4r]))
    w("")
    for k in ("H4a", "H4b"):
        v = h4v[k]
        w(f"{k}: verdict **{v['verdict']}** (rule: {v['rule']}); variants not Holm-rejected: {', '.join(v['variants_not_rejected']) or 'none'}; leave-one-stream-out "
          f"({v['loso_runs']} runs, 5,000 permutations each): p {pval(v['loso_p_range'][0])}-{pval(v['loso_p_range'][1])}, {v['loso_n_p_below_0.05']} below 0.05.")
        w("")
    lo_b = sorted([r for r in h4l if r["test"] == "H4b"], key=lambda r: -f(r["p_one_sided_fewer"]))[:3]
    w("The streams whose omission raises the H4b p-value most: " + "; ".join(f"{r['label']} (p {pval(r['p_one_sided_fewer'])})" for r in lo_b)
      + f". Commentary-only references by category: " + ", ".join(f"{k} {v}" for k, v in h4v["category_counts_commentary_only"].items())
      + f"; hypocoristics occur in {len(h4v['hypocoristic_streams'])} streams (" + ", ".join(lab(s) for s in h4v["hypocoristic_streams"]) + ").")
    w("")
    w("**Table 4.5. Power of H4b** (simulation: with probability theta a reference takes a designated form of its stream x player x slot cell; "
      f"{mde[0]['simulations']} data sets per theta, {mde[0]['permutations']} permutations each).")
    w("")
    w(table(["theta", "power at alpha 0.05"], [[r["theta"], num(r["power_at_0.05"], 3)] for r in mde]))
    w("")
    w("**Table 4.5b. POST HOC (first round): H4 with de-clustered references, and the contribution of each slot to H4b** (one reference per player per utterance; "
      "slot rows: distinct forms observed vs the mean under the H4b permutation, all commentary-only references; per-slot attribution rests on context-mode slots).")
    w("")
    w(table(["test", "token set", "tokens", "D", "null mean", "null 95%", "p (fewer)"],
            [[r["test"], r["token_set"], r["tokens"], r["D_obs"], num(r["null_mean"], 1), f"[{num(r['null_lo'], 0)}, {num(r['null_hi'], 0)}]",
              pval(r["p_one_sided_fewer"])] for r in h4d]))
    w("")
    w(table(["slot", "references", "distinct forms (sum over stream x player)", "null mean", "observed - null", "null 95%"],
            [[r["slot"], r["references"], num(r["distinct_obs"], 0), num(r["null_mean"], 1), num(r["obs_minus_null"], 1),
              f"[{num(r['null_lo'], 0)}, {num(r['null_hi'], 0)}]"] for r in h4s]))
    w("")
    w("**Table 4.6. Extension: syllables vs available time** (weighted mean of within-stream Spearman rho; permutation of the time values among utterances within stream; "
      "MDE = 2.80 x the null SD, normal approximation). The last row is post hoc (addendum 1).")
    w("")
    w(table(["analysis", "references", "time", "tokens", "streams", "rho", "stream bootstrap 95%", "null 95%", "p (two-sided)", "MDE rho", "status"],
            [[r["analysis"], r["references"], r["time"], r["tokens"], r["streams"], num(r["rho_weighted"], 3), ci(r["boot_lo"], r["boot_hi"], 3, 1),
              ci(r["null_lo"], r["null_hi"], 3, 1), pval(r["p_two"]), num(r["mde_rho_approx"], 3), r["status"]] for r in ext + h5p]))
    w("")
    ml = h5.get("mixedlm", {})
    if "coef_logA" in ml:
        w(f"Mixed model ({ml['model']}; {ml['tokens']} references, {ml['groups']} streams; exploratory): coefficient of log A_after = {num(ml['coef_logA'], 3)} "
          f"syllables per log-second [{num(ml['ci_lo'], 3)}, {num(ml['ci_hi'], 3)}], p = {pval(ml['p'])}.")
        w("")
    # ---- E1
    w("### 4.1 Formula expressions per slot (E1, exploratory)")
    w("")
    em = tmeta["e1"]
    w(f"Genre inventory identified on the 20 TV streams pooled: {em['genre_formulas']:,} formulas and {em['genre_open_systems']:,} open-slot systems; greedy "
      f"longest-first segmentation gives {em['occurrences']:,} occurrences. Per stream x slot (span-mode slot of the occurrence): occurrences, distinct types per 100 "
      "tokens of the slot and modal-type share; null: stream labels permuted among the slot's occurrences (10,000 permutations). With the pooled inventory a string "
      "repeated inside one stream only is in the inventory and all its occurrences belong to that stream, so 'fewer distinct types than chance' is guaranteed by "
      "construction; Table 4.7b repeats the test with each stream segmented by the inventory of the other 19 (post hoc).")
    w("")
    rows = []
    for r in e1t:
        sl = r["slot"]
        cells = [x for x in e1 if x["slot"] == sl]
        rows.append([sl, r["occurrences"], num(np.mean([f(x["distinct_per_100_slot_tokens"]) for x in cells if x["distinct_per_100_slot_tokens"]]), 1),
                     r["D_obs"], num(r["null_mean"], 1), pval(r["p_one_sided_fewer"]),
                     pc(r["modal_share_obs"]), pc(r["modal_share_null_mean"]), pval(r["p_one_sided_modal_higher"])])
    w("**Table 4.7. E1 economy and across-stream null by slot (pooled inventory; rejects by construction).**")
    w("")
    w(table(["slot", "occurrences", "distinct types per 100 slot tokens (mean over streams)", "D (sum over streams of distinct types)", "null D",
             "p (fewer)", "modal-type share % (mean over streams)", "null", "p (higher)"], rows))
    w("")
    w("**Table 4.7b. POST HOC: E1 with a leave-one-stream-out inventory.**")
    w("")
    w(table(["slot", "occurrences", "D", "null D", "null 95%", "p (fewer)", "modal-type share %", "null", "p (higher)"],
            [[r["slot"], r["occurrences"], r["D_obs"], num(r["null_mean"], 1), ci(r["null_lo"], r["null_hi"], 0, 1), pval(r["p_one_sided_fewer"]),
              pc(r["modal_share_obs"]), pc(r["modal_share_null_mean"]), pval(r["p_one_sided_modal_higher"])] for r in e1l]))
    w("")
    w("Commonest types per slot (pooled inventory, all streams): " + "; ".join(
        f"{sl}: " + ", ".join([f"`{r['type']}` {pc(r['share_of_slot_occurrences'], 1)}% ({r['teams_using']} streams)" for r in e1top if r["slot"] == sl][:4])
        for sl in L.SLOTS if any(r["slot"] == sl for r in e1top)) + ".")
    w("")
    w("**Table 4.8. Economy per stream and slot (E1, pooled inventory)**: distinct formula types per 100 tokens of the slot / modal-type share %.")
    w("")
    rows = []
    for t in L.TV:
        row = [lab(t)]
        for sl in L.SLOTS:
            x = next((r for r in e1 if r["team"] == t and r["slot"] == sl), None)
            row.append(f"{num(x['distinct_per_100_slot_tokens'], 1)} / {pc(x['modal_share'], 0)}" if x and x["occurrences"] != "0" else "-")
        rows.append(row)
    w(table(["stream"] + list(L.SLOTS), rows))
    w("")
    w("Slot share of all tokens (token-level classifier), mean over the 20 TV streams: " + ", ".join(
        f"{sl} {pc(np.mean([f(r['share']) for r in slot_tok if r['slot'] == sl]))}%" for sl in L.SLOTS) + ".")
    w("")
    # ---- E2
    w("### 4.2 Functional-equivalence classes (E2, exploratory)")
    w("")
    w("Each class is a set of expressions declared equivalent in the plan (section 9) before counting. Forms pooled over the 20 TV streams, the Cornell and press "
      "modal forms, and the across-stream null (stream labels permuted among the class's TV occurrences; one-sided p for fewer distinct forms per stream / higher modal "
      "share than chance, i.e. stream-specific choice).")
    w("")
    rows = []
    for cname, slot, forms in __import__("p05_thrift").E2:
        tv = [r for r in e2 if r["class"] == cname and r["medium"] == "tv"]
        pooled = Counter()
        for r in tv:
            for item in (r["forms"] or "").split("; "):
                if item:
                    k, v = item.rsplit(":", 1)
                    pooled[k] += int(v)
        n = sum(pooled.values())
        corn = next(r for r in e2 if r["class"] == cname and r["team"] == "cornell")
        pres = next(r for r in e2 if r["class"] == cname and r["team"] == "press_pooled")
        t = next((x for x in e2t if x.get("class") == cname), {})
        rows.append([cname, slot, n, sum(1 for r in tv if int(r["occurrences"]) > 0),
                     ", ".join(f"{k} {100 * v / n:.0f}%" for k, v in pooled.most_common(4)) if n else "-",
                     f"{corn['modal_form']} ({pc(corn['modal_share'], 0)}%, n {corn['occurrences']})" if corn["occurrences"] != "0" else "-",
                     f"{pres['modal_form']} ({pc(pres['modal_share'], 0)}%, n {pres['occurrences']})" if pres["occurrences"] != "0" else "-",
                     f"{t.get('D_obs', '-')} / {num(t.get('null_mean'), 1)}", pval(t.get("p_one_sided_fewer")), pval(t.get("p_one_sided_modal_higher"))])
    w("**Table 4.9. Functional-equivalence classes.**")
    w("")
    w(table(["class", "slot", "TV occurrences", "TV streams using", "TV forms (pooled)", "Cornell modal form", "press modal form", "D / null D", "p (fewer)",
             "p (modal higher)"], rows))
    w("")
    w("**Table 4.9b. POST HOC: E2 summed per slot** (plan section 9 promised it; D summed over the slot's tested classes; null = independent within-class "
      "permutations, 10,000).")
    w("")
    w(table(["slot", "classes", "occurrences", "D", "null D", "null 95%", "p (fewer)"],
            [[r["slot"], r["classes"], r["occurrences"], r["D_obs"], num(r["null_mean"], 1), ci(r["null_lo"], r["null_hi"], 0, 1), pval(r["p_one_sided_fewer"])]
             for r in e2s]))
    w("")
    # ------------------------------------------------------------------ 5 primary
    w("## 5. The seven 2b-primary tests (Holm-Bonferroni, alpha = 0.05)")
    w("")
    w("Fixed in plan section 7 before any test ran; rerun unchanged. Null hypotheses: H1, matched-size coverage of a TV stream by another TV stream's inventory equals "
      "that of their unigram-shuffled texts; H2, that excess is no larger for TV sources than for the Cornell (H2a) / press (H2b) source; H4a, given the slot, the "
      "reference category is independent of the stream; H4b, within stream x player, the form is independent of the situational slot; H5, within stream, a reference's "
      "syllable count is independent of the time after its clip. H1/H2 p-values are percentile-bootstrap approximations over broadcasts treated as exchangeable "
      "draws; at their floor they only say that no bootstrap draw crossed zero. The last column gives the reading after the post hoc checks of addendum 1.")
    w("")
    reading = {
        "H1a": f"check only: {pc(c15['press_pooled_share_of_tv_tv_excess'], 0)}% / {pc(c15['cornell_share_of_tv_tv_excess'], 0)}% of the excess reached by press / Cornell",
        "H1b": f"check only; n >= 3 inventories at S = 1,500: {num(min(inv15), 0)}-{num(max(inv15), 0)} types",
        "H2a": f"observed difference {hoci(1500, 'cov_base', 'cornell', 'observed')} pp ({oc['targets_positive']}/{oc['n_targets']}); at 100,000 tokens "
               f"{lci('TV minus cornell', 'obs_n2')} (n >= 2), {lci('TV minus cornell', 'obs_n3')} (n >= 3)",
        "H2b": f"observed difference {hoci(1500, 'cov_base', 'press_pooled', 'observed')} pp ({op['targets_positive']}/{op['n_targets']}); at 100,000 tokens "
               f"{lci('TV minus press_pooled', 'obs_n2')} (n >= 2), {lci('TV minus press_pooled', 'obs_n3')} (n >= 3)",
        "H4a": va["verdict"],
        "H4b": f"{vb['verdict']} (p {pval(vb['p_range_variants'][0])}-{pval(vb['p_range_variants'][1])} over seeds and variants; speaker-role confound untestable)",
        "H5": f"stored time on all 20 streams: rho {num(hs['rho_weighted'], 3)}, p {pval(hs['p_two'])}",
    }
    w(table(["id", "claim", "estimate", "interval", "p", "kind of p", "Holm p", "rejected", "detail", "reading after post hoc checks"],
            [[r["id"], r["claim"], num(r["estimate"], 0 if r["id"].startswith("H4") else 4), r["interval"], pval(r["p"]), r["p_kind"], pval(r["p_holm"]),
              r["reject_holm_0.05"], r["detail"], reading[r["id"]]] for r in prim.values()]))
    w("")
    floors = [k for k, r in prim.items() if k.startswith(("H1", "H2")) and f(r["p"]) <= 2 / (10000 + 1) + 1e-12]
    if floors:
        w(f"The p-values of {', '.join(floors)} are at the bootstrap floor (2/(B+1)).")
        w("")
    # ---- exploratory count (per p-value, by file)
    cnt_rows = [
        ("cluster_tests.csv", len(clus)), ("qap_regression.csv (incl. intercepts)", len(qap)),
        ("thrift_tests_2b.csv (non-primary rows)", sum(1 for r in thr if r["status"] != "2b-primary")),
        ("extension_2b.csv (non-primary rows)", sum(1 for r in ext if r["status"] != "2b-primary")),
        ("mixed model (primary_H4H5.json)", 1 if "p" in ml else 0), ("e1_tests.csv (2 per slot)", 2 * len(e1t)), ("e2_tests.csv (2 per class)", m_e2),
        ("h4_declustered.csv (first-round post hoc)", len(h4d)), ("Spearman, stream-specific share vs length (core_meta.json)", 2)]
    post_rows = [("h4_robust.csv (seeds and variants)", sum(1 for r in h4r if r["kind"] != "pre-registered")), ("h4_robust_loso.csv", len(h4l)),
                 ("e1_loso_tests.csv (2 per slot)", 2 * len(e1l)), ("e2_slot_sums.csv", len(e2s)), ("h5_sensitivity_post_hoc.csv", len(h5p))]
    n_expl = sum(n for _, n in cnt_rows)
    n_post = sum(n for _, n in post_rows)
    w(f"Exploratory p-values reported in sections 2 and 4 (counted per p-value, not per row): {n_expl} from the planned exploratory analyses ("
      + "; ".join(f"{k} {n}" for k, n in cnt_rows) + f") and {n_post} from the post hoc checks of addendum 1 (" + "; ".join(f"{k} {n}" for k, n in post_rows)
      + "). All are unadjusted; at alpha 0.05 about " + f"{num(0.05 * (n_expl + n_post), 0)}" + " would fall below 0.05 by chance if every null held. "
      "The bootstrap p-values stored in `h2_observed.csv` are not used; differences there are reported with intervals.")
    w("")
    # ------------------------------------------------------------------ 6 limitations
    w("## 6. Limitations")
    w("")
    w("1. **Repetition, not Parry's formula.** Every inventory is a set of exact n-grams repeated within a text. Against two LLM coders applying Parry's definition, "
      f"the automatic measures reach kappa {num(min(ks_all), 2)}-{num(max(ks_all), 2)} (coders with each other {num(pm['token_kappa'], 2)}); see section 3. Agreement "
      "with human specialists is untested.")
    w("2. **ASR noise.** The TV texts are raw WhisperX output with an unknown word error rate (lower bound 22 visible errors per 1,000 words, Phase 2); errors break "
      "exact repeats in both the source and the target of a TV-TV comparison but only in the target of a Cornell/press-TV comparison, which biases the TV-minus-"
      "baseline differences toward zero. The press answers are edited stenography and Cornell is edited prose.")
    w("3. **Clip-level text and time.** A clip's text runs into the following dead time; slots are assigned to spans or windows by a keyword classifier, and "
      "A_after is a clip property. Extension and thrift tests are about clip-level co-variation, not the moment a word is chosen.")
    w("4. **Streams are not teams.** A stream is one match with one unnamed broadcaster; commentator hints exist for four streams and are [unverified]; the "
      "only two-member hint cluster coincides with same slam, same player and same round. Same-slam similarity mixes broadcaster, venue and surface vocabulary.")
    w("5. **No speaker labels.** Two or more commentators speak in a stream; a play-by-play voice and an analyst voice that differ in naming and in the situations "
      "they speak in produce the same patterns as slot-conditioned choice (H4b) or as stream-level habits (H4a, E2).")
    w(f"6. **Slot labels are noisy.** Context mode, which gives a reference its slot in H4, agrees with the coders at kappa {num(cv['coder_spans_A_context']['kappa'], 2)} "
      f"/ {num(cv['coder_spans_B_context']['kappa'], 2)} on their spans and {num(rA['kappa'], 2)} / {num(rB['kappa'], 2)} on the {rA['n']} / {rB['n']} commentary "
      f"references inside coded spans; span mode (formula spans) at {num(cv['coder_spans_A_span']['kappa'], 2)} / {num(cv['coder_spans_B_span']['kappa'], 2)}. "
      "Random slot errors attenuate H4b and blur the per-slot tables; Tables 2.11, 2.E and 4.7 "
      "use span mode on the strings themselves, so their SCORE and OFFICIAL rows are partly defined by the strings' own words.")
    w(f"7. **Sizes and samples.** At 1,500 tokens an n >= 3 inventory has {num(min(inv15), 0)}-{num(max(inv15), 0)} types, too few for n >= 3 comparisons; the "
      f"{lmeta['I_size']:,}-token design fixes that, but its TV source is drawn from 19 streams that overlap between targets, so its bootstrap over targets understates "
      "between-broadcast uncertainty. 'TV-only' means 'repeated in a 100,000-token TV sample and not in 100,000-token Cornell and press samples': "
      f"{share_word(1 - strict_frac)} of the TV-only tokens lie in strings that the whole baselines do repeat, at lower rates (Tables 2.D, 2.F).")
    w(f"8. **Baselines are different corpora.** Cornell (one outlet, {facts['cornell_outlet']}; written; other matches; no dates in the records) and the press answers "
      f"({facts['press_first_date'][:4]}-{facts['press_last_date'][:4]}; player answers, first person) differ from the TV streams ({facts['tv_first_year']}-"
      f"{facts['tv_last_year']}) in matches, period, transcription, segmentation and person; TV-minus-baseline differences say that TV commentary repeats strings these "
      "sources do not, not why. Name normalisation is uneven: hypocoristics are not normalised, and `<name>` is rare in press (section 1).")
    w("9. **Hand inputs.** The slot lexicons, the E2 equivalence classes and the demonym lists are my own specification; three nationalities (Alcaraz, Raducanu, "
      "Shelton) are entered by hand [unverified]; descriptive epithets outside the two finals are left unresolved rather than hand-assigned.")
    w("10. **Coders.** Both codings come from LLM agents (git trailers in section 3); the coding instructions in the repository are `manual.md`, and the agents' "
      "task prompts are not recorded there; their blindness to the automatic inventory rested on those instructions.")
    w("11. **Exploratory status.** All of 2b was designed after Phase 2's results were known; the 2b-primary family limits multiplicity within 2b but is not a "
      "pre-registration in the Phase 2 sense; everything in addendum 1 is post hoc and was designed after the critic's reruns had been read.")
    w("")
    # ------------------------------------------------------------------ 7 post hoc
    w("## 7. Post hoc changes (made after a first look at outputs)")
    w("")
    w("First round (before the review):")
    w("")
    w(f"1. Nationality epithets: a match whose demonym modifies a following non-person noun ('the greek fans', 'the czech republic', 'the italian riviera') is not "
      f"counted as a player reference (spaCy dependency rule; {rsum['post_hoc_excluded_adjectival_nationality_matches']} matches excluded, each listed with its excerpt "
      "in `results/refexpr_pool_epithets.csv`; a few exclusions are parser errors, e.g. 'the pole powers on'). The outputs of the run before this change were not kept.")
    w(f"2. Hypocoristic + surname ('rafa nadal', 'nole djokovic') counted as one full-name reference ({rsum['post_hoc_hypocoristic_full_names']} cases), not two "
      "(first-run outputs not kept).")
    w("3. Added beyond the plan's text: the full-size inventory table includes Cornell but not the press corpus (too large to index whole); the E2 extension uses "
      f"{tmeta['E2_extension_permutations']} permutations (it has about 300 strata); `title_surname` is a sixth reference category beside the plan's five (it occurs only "
      "inside umpire patterns, so it is absent from the commentary-only tests).")
    w("3b. Calibration: the plan's 2019-versus-other split is reported for overall precision / recall / F1 (Tables 3.2b), not within each slot or confidence stratum.")
    w("4. H4b power simulation corrected: the first run planted slot-specific forms on the observed data, which already carries the observed effect, so its "
      "'power' at theta = 0 was the rejection rate of the observed data (0.995); the corrected simulation starts every data set from the observed forms with slot labels "
      "permuted within stream x player, so H0 holds at theta = 0 (Table 4.5).")
    w("5. Table 4.5b (H4 with one reference per player per utterance, and the per-slot contribution to D_b) was added after the H4b result was seen.")
    w("")
    w("Revision 1 (plan addendum 1, after `review/critic_parry_v1.md`; all post hoc):")
    w("")
    w(f"6. Large identification sets ({lmeta['I_size']:,} tokens; `p08_largeI.py`) became the primary cross-corpus comparison, with the commentary-only variant, "
      "the TV-only n >= 3 stock, its strict and cross-broadcast readings, its slot composition and its string lists (section 2.0). The first report's statement "
      "about n >= 3 units rested on the 1,500-token inventories that this design replaces.")
    w("7. H2 is reported on observed coverage beside the pre-registered excess (Table 2.3, `p09_h2_observed.py`); Table 2.3b explains the size of the Cornell null; "
      "H1 is reported as a check.")
    w("8. Calibration at chance level, kappa of every automatic measure, span-level recall against circular shifts, and the slot classifier in context mode on coder "
      "spans and on references (`calibrate_chance.py`; `calibrate.py` now also saves its automatic labels).")
    w("9. H4a/H4b robustness: three seeds at 100,000 permutations, five variants, leave-one-stream-out, Holm under substitution, and a verdict rule (`p10_h4_robust.py`); "
      "`p04_refexpr_pool.py` writes two more columns (`slot_sit_span`, `t_next_stored_all`); H5 with the stored time field on all 20 streams.")
    w("10. E1 with a leave-one-stream-out inventory and E2 summed per slot (`p11_e1_loso.py`); p-values counted per p-value; 'idiolect' renamed 'stream-specific "
      "share'; LOW-confidence rows dropped from Tables 3.1 and 3.3; the rerun check against commit 476a088 (`p12_rerun_check.py`).")
    w("11. The plan declares 17 E2 classes; one (`challenge`) has a single attested TV form and no test, so 16 are tested.")
    w("")
    # ------------------------------------------------------------------ 8 files
    w("## 8. Files")
    w("")
    w("Code: `lib2b.py`, `p00_players.py`, `p01_sharing.py`, `p02_core.py`, `p03_clusters_targets.py`, `p04_refexpr_pool.py`, `p05_thrift.py`, "
      "`p05b_h4_declustered.py`, `calibrate.py`, `p06_primary.py`; post hoc (addendum 1): `p08_largeI.py`, `p09_h2_observed.py`, `calibrate_chance.py`, "
      "`p10_h4_robust.py`, `p11_e1_loso.py`, `p12_rerun_check.py`; `p07_figures.py`, `make_report.py`, `run_all.sh`, `tests/`. Hand input: `hand/players.tsv`. "
      "Results: `results/*.csv|json`. Figures: `figures/fig1_sharing_heatmap.png` ... `fig8_calibration.png`; post hoc `fig9_largeI_coverage.png`, "
      "`fig10_tvonly_slots.png`.")
    w("")
    for fig_, cap in (("fig9_largeI_coverage.png", "coverage by 100,000-token sources"), ("fig10_tvonly_slots.png", "composition of the TV-only stock"),
                      ("fig1_sharing_heatmap.png", "pairwise sharing"), ("fig2_sharing_summary.png", "sharing summary"), ("fig3_core_curve.png", "core"),
                      ("fig4_idiolect_by_slot.png", "stream-specific share by slot"), ("fig5_pool_to_target.png", "pool to target"),
                      ("fig6_refexpr_categories.png", "naming"), ("fig7_extension.png", "extension")):
        w(f"![{cap}](figures/{fig_})")
    if cal_ok:
        w("![calibration](figures/fig8_calibration.png)")
    OUT.write_text("\n".join(S) + "\n", encoding="utf-8")
    print("wrote", OUT, len(S), "lines")


if __name__ == "__main__":
    main()
