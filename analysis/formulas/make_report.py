"""Builds analysis/formulas/report.md from results/ (every number is read from a results file, or computed here from them).
Run: python -I analysis/formulas/make_report.py

Revision 1 (plan.md addendum 2): the pre-registered measure is called repeated-n-gram coverage; stricter coverage family and
shuffled baselines; corpus contrasts; C1/R1 indeterminate pending a WER estimate; C1/C2 interval as inferential statistic;
minimum detectable effects; Kuiper section limited to verified records and data; umpire-pattern exclusion; revised top-10 flag.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import csv
import json
import math
from collections import Counter
import common as C
import refexpr as RX

R = C.RESULTS


def rcsv(name, delim=","):
    with open(R / name, encoding="utf-8") as fh:
        return list(csv.DictReader(fh, delimiter=delim))


def rjson(name):
    return json.loads((R / name).read_text())


def pc(x, d=1):
    return "NA" if x in (None, "", "None") else f"{100 * float(x):.{d}f}"


def ci(lo, hi, d=1):
    return f"[{pc(lo, d)}, {pc(hi, d)}]"


def f3(x):
    return f"{float(x):.3f}"


def f2(x):
    return f"{float(x):.2f}"


def es(x, key="e_star_mean_crossing"):
    v = x[key]
    return f"{v:.3f}" if v is not None else f"not reached up to e = {x['max_level_tried']}"


def g2(x):
    return "not reached on the grid" if x in (None, "", "None") else f"{float(x):.2f}"


def pv(p):
    p = float(p)
    return f"{p:.4f}" if p >= 0.0001 else f"{p:.1e}"


def table(header, rows):
    out = ["| " + " | ".join(header) + " |", "|" + "---|" * len(header)]
    for r in rows:
        out.append("| " + " | ".join(str(x) for x in r) + " |")
    return "\n".join(out)


def wilson(k, n, z=1.96):
    p = k / n
    den = 1 + z * z / n
    c = (p + z * z / (2 * n)) / den
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / den
    return c - h, c + h


def main():
    meta = rjson("density_main_meta.json")
    mmeta = rjson("density_medium_meta.json")
    fsum = rjson("formulas_summary.json")
    ssum = rjson("systems_summary.json")
    rsum = rjson("refexpr_summary.json")
    slotv = rjson("slot_validation.json")
    asr = json.loads((C.ROOT / "corpus" / "reports" / "asr_proxy.json").read_text())
    dm = rcsv("density_main.csv")
    ds = rcsv("density_sensitivity.csv")
    dctx = rcsv("density_context.csv")
    dstr = rcsv("density_streams.csv")
    dmed = rcsv("density_medium.csv")
    fam = rcsv("coverage_family.csv")
    conf = rcsv("confirmatory.csv")
    medc = rcsv("medium_contrasts.csv")
    byn = rcsv("formulas_by_n.csv")
    mm = rcsv("maximal_match_2019.csv")
    cs = rcsv("formulas_cross_stream.csv")
    f19 = rcsv("formulas_2019.tsv", "\t")
    s19 = rcsv("systems_2019.tsv", "\t")
    sbt = rcsv("systems_by_type.csv")
    inv = rcsv("refexpr_inventory.csv")
    byc = rcsv("refexpr_by_context.csv")
    syl = rcsv("refexpr_syllables.csv")
    pron = rcsv("pronouns.csv")
    th = rcsv("thrift_tests.csv")
    ext = rcsv("extension.csv")
    lt = rcsv("length_time_tests.csv")
    top = rcsv("top10_for_brief.csv")
    top3 = rcsv("top10_for_brief_n3.csv")
    c3 = rjson("c3_time_tests.json")
    mde = rjson("mde_summary.json")
    circ = rjson("circular_shift_tests.json")
    an = rjson("asr_noise_summary.json")
    kv = rcsv("../hand/kuiper_verification.tsv", "\t")
    dug = rcsv("../hand/duggan_verification.tsv", "\t")[0]
    tok_files = {s: rcsv(f"refexpr_tokens_{s}.csv") for s in (C.MAIN, C.HELDOUT)}
    NPOOL = len(C.pool_streams())

    def dmv(design, ident, meas, measure, rows=dm, variant="primary"):
        for r in rows:
            if r["design"] == design and r["identified_on"] == ident and r["measured_on"] == meas and r["measure"] == measure \
                    and r["variant"] == variant:
                return r
        raise KeyError((design, ident, meas, measure, variant))

    def medv(design, corpus, est, measure):
        for r in dmed:
            if r["design"] == design and r["corpus"] == corpus and r["estimate"] == est and r["measure"] == measure:
                return r
        raise KeyError((design, corpus, est, measure))

    def famv(design, ident, meas, d):
        return next(r for r in fam if r["design"] == design and r["identified_on"] == ident and r["measured_on"] == meas
                    and r["definition"] == d)

    def cf(i):
        return next(r for r in conf if r["id"] == i)

    T19, T23, TP = meta["tokens_2019"], meta["tokens_2023"], meta["tokens_pool"]
    d1 = dmv("D1_in_sample", C.MAIN, C.MAIN, "a")
    d1b = dmv("D1_in_sample", C.MAIN, C.MAIN, "a+b")
    d2 = dmv("D2_split_half", "2019 halves", "2019 other half (pooled)", "a")
    d2b = dmv("D2_split_half", "2019 halves", "2019 other half (pooled)", "a+b")
    d3 = dmv("D3_held_out", "pool (18 matches)", C.MAIN, "a")
    d3b = dmv("D3_held_out", "pool (18 matches)", C.MAIN, "a+b")
    d3x = dmv("D3_held_out", C.MAIN, C.HELDOUT, "a")
    d3xb = dmv("D3_held_out", C.MAIN, C.HELDOUT, "a+b")
    shv = f"D7_shuffled_word_baseline_R{meta['R_shuffle']}"
    sh_in = dmv("D1_in_sample", "2019 shuffled words", "2019 shuffled words", "a", ds, shv)
    sh_sp = dmv("D2_split_half", "2019 shuffled words", "2019 shuffled words", "a", ds, shv)
    DES = [("in-sample", "D1_in_sample", C.MAIN, C.MAIN), ("split-half", "D2_split_half", "2019 halves", "2019 other half (pooled)"),
           ("pool -> 2019", "D3_held_out", "pool (18 matches)", C.MAIN), ("2019 -> 2023", "D3_held_out", C.MAIN, C.HELDOUT)]
    DES_ALL = DES + [("pool -> 2023", "D3_held_out", "pool (18 matches)", C.HELDOUT),
                     ("2023 in-sample", "D1_in_sample", C.HELDOUT, C.HELDOUT),
                     ("2023 split-half", "D2_split_half", "2023 halves", "2023 other half (pooled)")]
    CORP = ("tv_pool_all", C.TEXT, "press_answers")
    labels = {"tv_pool_all": f"TV commentary, pool subsample ({NPOOL} matches)", C.TEXT: "Cornell live text (written)",
              "press_answers": "press answers (spoken, not commentary)"}
    lv = an["levels"]
    cr = an["crossings"]
    R1000 = int(mmeta["R_matched"])
    R200 = int(mmeta["R_matched_systems"])
    pyears = mmeta["press_years"]
    tyears = mmeta["tv_years"]
    sz = mmeta["D5ii_identification_size"]
    szb = mmeta["D5iib_identification_size"]
    covered = sum(int(r["tokens"]) for r in mm if int(r["longest_formula_len"]) >= 2)
    bigram_only = sum(int(r["tokens"]) for r in mm if int(r["longest_formula_len"]) == 2)
    c1, r1, c2 = cf("C1"), cf("R1"), cf("C2")
    fam19 = [r for r in conf if r["family"] == "2019"]

    L = []
    A = L.append
    A("# Formula analysis (Phase 2): repeated-n-gram coverage and oral-formulaic measures on live tennis commentary")
    A("")
    A("Generated by `analysis/formulas/make_report.py` from `analysis/formulas/results/`; rerun everything with "
      "`bash analysis/formulas/run_all.sh`. The design was pre-specified in `analysis/formulas/plan.md` (committed before any "
      "result was computed); this is **revision 1**, made after the adversarial review `review/critic_analysis_v1.md`; every change "
      "is logged in plan.md, addendum 2, and summarised in section 10. Brackets are 95% intervals. Confirmatory tests are C1-C5 "
      "(2019 final) and their replication R1, R3-R5 (2023 final); everything else is exploratory, and analyses added after results "
      "were seen are labelled post hoc.")
    A("")
    A("**Terminology.** The measure computed here is **repeated-n-gram coverage**: the share of word tokens that lie inside an exact "
      "word n-gram repeated in at least two utterances of an identification set. It is a rate of lexical repetition. It is not "
      "Parry's formula (an expression regularly used under the same metrical conditions to express a given essential idea), and it is "
      "not Duggan's \"formulaic density\", which counts repeated verse units (hemistichs) in a metrical text; tennis commentary has no "
      "metre, so no metrical condition can be imposed. \"Formulaic density\" appears below only in quotation marks, when the measure is "
      "related to Duggan's. To let the reader see how much of the repetition is short, function-word-heavy or numeric, every main "
      "design is also reported under a stricter family of definitions (section 1).")
    A("")
    A("## 0. Data")
    A("")
    A(table(["corpus", "role", "kind of text", "utterances", "tokens (this tokeniser)"], [
        [f"`{C.MAIN}`", "MAIN, in-sample", "TV commentary, raw ASR", meta["utterances_2019"], meta["tokens_2019"]],
        [f"`{C.HELDOUT}`", "HELD-OUT", "TV commentary, raw ASR", meta["utterances_2023"], meta["tokens_2023"]],
        [f"{NPOOL} `tv_pool_*`", "reference pool (identification)", "TV commentary, raw ASR", meta["utterances_pool"], meta["tokens_pool"]],
        [f"`{C.TEXT}`", "written contrast", "written live text (edited prose, one outlet)", mmeta["cornell_updates"], mmeta["cornell_tokens"]],
        ["press answers", "spoken non-commentary baseline", "player answers, edited stenographic transcript", mmeta["press_answers"],
         mmeta["press_tokens"]],
    ]))
    A("")
    A(f"Utterance = one rally clip's de-duplicated, corrected ASR text (`text_corrected`; empty clips dropped), one live-text update, or one "
      f"player answer. Mean tokens per utterance: " + ", ".join(f"{k} {v:.1f}" for k, v in mmeta["mean_tokens_per_utterance"].items()) + ". "
      f"TV matches are dated {tyears[0]}-{tyears[1]} (match ids). The press answers (Cornell release, {mmeta['press_interviewees']} "
      f"interviewees, record dates {pyears[0]}-{pyears[1]}) are human transcripts of a non-live genre; `corpus/SOURCES.md` lists them as "
      f"DON'T USE *as commentary*; they are used only as a baseline (FOR_HUMAN.md). The Cornell live-text records carry no dates.")
    A("")
    # ------------------------------------------------------------------ key results
    A("## Key results")
    A("")
    A("**Table K. Repeated-n-gram coverage of the 2019 final under each definition** (% of tokens [bootstrap 95% CI]; section 3, "
      "Table 3.1b gives the shuffled-word baselines and the excess over them).")
    A("")
    rows = []
    for d in C.FAMILY:
        row = [C.FAMILY_LABEL[d]]
        for lab, design, ident, meas in DES:
            r = famv(design, ident, meas, d)
            row.append(f"{pc(r['coverage'])} {ci(r['ci_lo'], r['ci_hi'])}")
        rows.append(row)
    A(table(["definition"] + [x[0] for x in DES], rows))
    A("")
    A(f"* What the pre-registered measure counts: {pc(bigram_only / covered, 0)}% of the covered tokens of the 2019 final have a bigram "
      f"as their longest covering repeat (Table 2.2), and the most widespread items are `{f19[0]['formula']}`, `{f19[1]['formula']}`, "
      f"`{f19[2]['formula']}` (Table 2.4). Requiring n >= 3 cuts in-sample coverage from {pc(famv('D1_in_sample', C.MAIN, C.MAIN, 'base')['coverage'])}% "
      f"to {pc(famv('D1_in_sample', C.MAIN, C.MAIN, 'n3')['coverage'])}%; excluding n-grams made only of function words and numerals "
      f"changes it much less ({pc(famv('D1_in_sample', C.MAIN, C.MAIN, 'content')['coverage'])}%). Shuffling the words (a floor that "
      f"keeps word frequencies and destroys syntax) leaves {pc(famv('D1_in_sample', C.MAIN, C.MAIN, 'base')['shuffled_mean'])}% in-sample "
      f"coverage under the base definition but {pc(famv('D1_in_sample', C.MAIN, C.MAIN, 'n3')['shuffled_mean'])}% for n >= 3, so the "
      f"n >= 3 coverage lies almost wholly above that floor.")
    tvsp, txsp, prsp = (medv("D5i_matched_2019_size", c, "splithalf", "a") for c in CORP)
    tv3, tx3, pr3 = (medv("D5i_matched_2019_size", c, "splithalf", "n3") for c in CORP)
    A(f"* Corpus contrasts at matched size ({T19:,} tokens, split-half, mean over {R1000} subsamples): TV commentary pool "
      f"{pc(tvsp['mean'])}%, Cornell written live text {pc(txsp['mean'])}%, press answers {pc(prsp['mean'])}% (n >= 3: "
      f"{pc(tv3['mean'])}%, {pc(tx3['mean'])}%, {pc(pr3['mean'])}%). These are contrasts between corpora that differ in matches, outlet, "
      "period, transcription (raw ASR vs edited text) and segmentation, not estimates of a medium effect (Table 3.2).")
    hp = cr["heldout|press_answers"]
    sp_ = cr["splithalf_matched|press_answers"]
    A(f"* C1/R1 (commentary vs press answers, held-out): **indeterminate pending a WER estimate**. TV {pc(c1['estimate_x'])}% vs press "
      f"{pc(c1['estimate_y'])}% (difference interval {ci(c1['diff_lo'], c1['diff_hi'])} pp); but injected substitution noise brings the "
      f"press value down to the TV value at e* = {es(hp)} (held-out; split-half e* = "
      f"{es(sp_)}), while the only error estimate for the TV text is a lower bound of "
      f"{asr['hand_sample']['total_per_1000_words']:.0f} visible errors per 1,000 words (Table 3.8, section 9.1).")
    floor200 = 2 / (R200 + 1)
    A(f"* C2 (TV pool vs Cornell live text, split-half at matched size): {c2['verdict']}; difference {pc(c2['difference'])} pp, 95% interval "
      f"over {c2['replicate_pairs']} independent subsample pairs {ci(c2['diff_lo'], c2['diff_hi'])}. The pre-registered replicate-overlap "
      f"\"p\" is {pv(c2['p'])}" + (f", its floor 2/({c2['replicate_pairs']} + 1)," if c2['p_at_floor'] == 'True' else ",") + " and is "
      f"not a calibrated test; the v1 Holm value {(len(fam19) - 1) * floor200:.4f} (= {len(fam19) - 1} x 2/{R200 + 1}) was a resolution "
      "artefact of R, not a borderline result.")
    timing = [cf(x) for x in ("C3a", "C3b", "C4", "C5", "R3a", "R3b", "R4", "R5")]
    c3m = [mde[x]["mde_achieved_alpha05"] for x in ("C3a", "C3b", "R3a", "R3b") if mde[x]["mde_achieved_alpha05"] is not None]
    c3lo, c3hi = min(c3m), max(c3m)
    nrej_t = sum(1 for r in timing if r["reject_at_0.05"] == "True")
    A(f"* Timing tests (C3a, C3b, C4, C5 and replications): {nrej_t} of {len(timing)} rejected. With these sample sizes the tests detect, "
      f"with 80% power at alpha = 0.05, only a coverage difference of about {pc(c3lo)}-{pc(c3hi)} pp between shortest and longest time "
      f"terciles (C3a-R3b), a regime in which {pc(mde['C4']['mde_param_alpha05'], 0)}% (2019) or {pc(mde['R4']['mde_param_alpha05'], 0)}% "
      f"(2023) of references take a tercile-specific form (C4/R4), or a length-time Spearman rho of {g2(mde['C5']['mde_achieved_alpha05'])} "
      f"(C5; R5 {g2(mde['R5']['mde_achieved_alpha05'])}) (Table 4.3). Smaller effects would have gone undetected: the result is \"not detected\", "
      "not evidence of absence.")
    sur = [float(r["share_surname"]) for r in ext if r["token_set"] == "commentary_only"]
    epi = [float(r["share_epithet"]) for r in ext if r["token_set"] == "commentary_only"]
    nump = {s: sum(1 for t in tok_files[s] if t["umpire_pattern"]) for s in tok_files}
    A(f"* Naming (commentary-only references, after removing {nump[C.MAIN]} (2019) and {nump[C.HELDOUT]} (2023) references inside "
      f"umpire/Hawk-Eye patterns): the bare surname is {pc(min(sur), 0)}-{pc(max(sur), 0)}% of each player's references and descriptive "
      f"epithets {pc(min(epi), 0)}-{pc(max(epi), 0)}% (sections 5-6).")
    A("")
    # ------------------------------------------------------------------ 1 definitions
    A("## 1. Definitions (exact)")
    A("")
    A("**Tokens.** NFKC; curly quotes to `'`; hyphens, dashes and `/` to space; lower-case; token = `[a-z0-9]+(?:'[a-z0-9]+)*` "
      "(clitics stay attached: `it's`, `federer's`); other punctuation dropped; digits kept verbatim (`15`, `40`); number words not normalised. "
      "N-grams never cross an utterance boundary but do cross punctuation inside an utterance (WhisperX punctuation is unreliable). "
      f"STOP = a frozen list of {len(C.STOP)} function words (`common.py`); digits and player names are never STOP.")
    A("")
    A("**(a) Repeated n-gram (\"formula\" in the plan).** An n-gram (2 <= n <= 12) is a repeated n-gram of an identification set I if it occurs "
      "in at least m = 2 distinct utterances of I and is not stop-only. **Repeated-n-gram coverage** of a measurement set M = share of M's "
      "tokens lying inside at least one occurrence (in M) of a repeated n-gram of I. In-sample (I = M) a token is covered if its n-gram "
      "recurs elsewhere in the same text, the operational analogue of Duggan's counting of repeated units (the wording of Duggan's own "
      "criterion is [unverified]: only the bibliographic record was fetched, see below). Held-out (I and M disjoint) it is the share of M "
      "that reuses n-grams already repeated in I.")
    A("")
    A("**Stricter coverage family** (revision 1, exploratory). Same I, M and repeated-n-gram inventory; a token counts only if it lies "
      "inside a qualifying repeated n-gram: " + "; ".join(f"`{d}` = {C.FAMILY_LABEL[d]}" for d in C.FAMILY) + ". "
      f"Numerals = digit strings and the {len(C.NUMERAL_WORDS)} words of `common.NUMERAL_WORDS` (tennis score words `love fifteen thirty "
      "forty deuce`, English cardinals and the ordinals `first`-`twelfth`), so `the first` and `40 15` are function/numeral-only, while "
      "`the first set` and `a little` are not.")
    A("")
    A("**(b) System.** A frame is an n-gram (2 <= n <= 6) with exactly one slot. Slot types: `<NAME>` (a first name or surname of any of the "
      f"players of the {len(C.tv_streams())} TennisVL matches, {len(C.player_name_lexicon())} name tokens, possessive stripped), `<NUM>` (a digit string or "
      "`love fifteen thirty forty deuce`), `<_>` (any token). A frame is a system of I if it occurs >= 3 times in >= 3 utterances of I with "
      ">= 2 distinct fillers, has >= 1 non-STOP fixed token, and, if the slot is `<_>`, the slot is internal (fixed tokens on both sides). "
      "(a)+(b) coverage = share of tokens covered by a repeated n-gram or by an occurrence of a system of I (any filler of the right type).")
    A("")
    A("**Shuffled-word baselines.** In-sample and split-half (D7, pre-registered): all tokens of the 2019 stream permuted over positions "
      f"(utterance lengths kept), then identification and measurement repeated (R = {meta['R_shuffle']}). Held-out (revision 1): the tokens "
      "of M permuted the same way while I's inventory is kept. Excess = coverage minus the mean shuffled coverage; its interval pairs "
      "bootstrap draws of the coverage with shuffled replicates at random. The baseline keeps word frequencies and destroys syntax, so "
      "it is a floor, not a syntax-preserving null.")
    A("")
    A("**Designs.** D1 in-sample (I = M). D2 split-half: I = odd clips, M = even clips and vice versa (pooled; CI resamples within halves). "
      f"D3 held-out across matches: I = the {NPOOL} pool matches, M = the 2019 final; I = the 2019 final, M = the 2023 final. "
      "D4 per stream (leave-one-stream-out identification; and small subsamples). D5 per corpus at matched size: (i) in-sample and split-half "
      "in random subsamples of the 2019 size; (ii) held-out with I and M from disjoint groups (pre-registered); (ii-b, post hoc) held-out with "
      "M concentrated in as few groups as possible; (iii) in-sample at pool size. D6 per context. D7 shuffled-word baseline.")
    A("")
    A("**Contexts.** `phase` is the corpus's regex tag (`between_points` = the whole clip text is a score call; `changeover` = a cue word); it "
      "is defined from the text itself, so its contrast is partly definitional. `dead_time_before_s` = PBP time from the end of the "
      "previous rally to this point's first serve. `time_after_s` = `dead_time_before_s` of the next point (or the gap to the second serve for a "
      "first-serve-fault clip), used because the clip transcript runs past the clip end (corpus/README section 4). Terciles are cut per stream: "
      f"2019 dead time before {c3['cuts_2019']['dead_time_before_s'][0]:.1f} / {c3['cuts_2019']['dead_time_before_s'][1]:.1f} s, "
      f"time after {c3['cuts_2019']['time_after_s'][0]:.1f} / {c3['cuts_2019']['time_after_s'][1]:.1f} s; "
      f"2023 {c3['cuts_2023']['dead_time_before_s'][0]:.1f} / {c3['cuts_2023']['dead_time_before_s'][1]:.1f} s and "
      f"{c3['cuts_2023']['time_after_s'][0]:.1f} / {c3['cuts_2023']['time_after_s'][1]:.1f} s. Score situation of the aligned PBP point: "
      "match point > set point > break point > other tie-break point > deuce/advantage > other.")
    A("")
    A("**Umpire-type patterns** (revision 1). Two pattern sets, both in the code: (i) `common.official_mask_v2` (= the pre-registered S5 "
      "patterns plus `mr <name>`, `advantage <name>`, `game (and) set (and match) <name>`, `game and <ordinal> set <name>`, `<name>... (is) "
      "challenging (the call)`, `<name>... has <x> challenge(s) remaining/left`, bare `thank you` (+ `players`/`please`/`all`), point-score "
      "calls `<score> <score|all>` with score = `0 15 30 40 love fifteen thirty forty` and the ASR confusions `13 14 50`, and `deuce`), used "
      "for the top-10 `official` flag and the S5b sensitivity; (ii) `refexpr.umpire_rule` on the word sequence around a player reference: "
      + "; ".join(f"`{n}` before = `{p}`" for n, p in RX.UMPIRE_BEFORE) + "; " +
      "; ".join(f"`{n}` after = `{p}`" for n, p in RX.UMPIRE_AFTER) + "; and every `mr <surname>`. Score calls are said by the umpire and "
      "by the commentators; the transcript does not tell them apart.")
    A("")
    A(f"**Uncertainty.** Coverage: percentile bootstrap over utterances of M (B = {meta['B']}), with I's inventory held fixed, so the "
      "interval covers sampling of the measured text, not uncertainty in identification. Subsample designs report the mean and "
      "2.5-97.5% range over replicates. Tests: section 4.")
    A("")
    A(f"**Reference for Duggan.** {dug['reference']} Status: **{dug['status']}**. Record: {dug['record_fetched']}. Confirms: "
      f"{dug['what_the_record_confirms']}.")
    A("")
    # ------------------------------------------------------------------ 2 formulas / systems
    A("## 2. Repeated n-grams (a) and systems (b) in the 2019 final")
    A("")
    A(f"{fsum['formula_types_stop_filtered']} repeated n-gram types (n = 2..12, stop-only n-grams excluded; {fsum['formula_types_unfiltered']} "
      f"without the filter; {meta['formula_types_2019_content']} after also excluding n-grams made only of function words and numerals). "
      f"In-sample (a) coverage {pc(d1['density'])}% {ci(d1['ci_lo'], d1['ci_hi'])}. {fsum['types_shared_with_any_pool_stream']} of the "
      f"{fsum['formula_types_stop_filtered']} types also occur in at least one of the {NPOOL} other matches, and {fsum['types_in_2023']} "
      "in the 2023 final.")
    A("")
    A("**Table 2.1. Repeated n-grams by length n (in-sample, 2019).** Coverage = share of all 2019 tokens covered by repeats of exactly this length.")
    A("")
    A(table(["n", "filter", "types", "occurrences", "coverage %", "types in >= 1 / >= 3 / >= 9 pool matches", "types in 2023"],
            [[r["n"], r["filter"], r["formula_types"], r["occurrences"], pc(r["coverage_share"]),
              f"{r['types_in_ge1_pool_streams']} / {r['types_in_ge3_pool_streams']} / {r['types_in_ge9_pool_streams']}", r["types_in_2023"]]
             for r in byn]))
    A("")
    A("**Table 2.2. Maximal match** (each token assigned the length of the longest repeat covering it; 0 = uncovered).")
    A("")
    A(table(["longest repeat covering the token", "tokens", "%"], [[r["longest_formula_len"], r["tokens"], pc(r["share"])] for r in mm]))
    A("")
    bins = [(0, 0), (1, 2), (3, 8), (9, NPOOL)]
    A("**Table 2.3. Within vs across matches**: 2019 repeated n-gram types by the number of other matches (pool streams, each a different "
      "match and possibly a different broadcaster) in which they occur.")
    A("")
    A(table(["pool matches attesting the n-gram", "2019 types"],
            [[f"{a}" if a == b else f"{a}-{b}", sum(int(r["formula_types_2019"]) for r in cs if a <= int(r["pool_streams_attested"]) <= b)]
             for a, b in bins]))
    A("")
    ty = next((r for r in f19 if r["formula"] == "thank you"), None)
    A("**Table 2.4. The 25 most widespread repeated n-grams** (by distinct utterances; full list with excerpts in `results/formulas_2019.tsv`)." +
      (f" `thank you` (rank {ty['rank']}) is mostly the umpire's call to the crowd (`thank you players`, `thank you please`), counted here as "
       "pre-registered; it is masked in S5b and flagged `official` in the top-10 lists (section 7)." if ty else ""))
    A("")
    A(table(["rank", "n-gram", "n", "utterances", "occurrences", "coverage %", "pool matches"],
            [[r["rank"], f"`{r['formula']}`", r["n"], r["utterances"], r["occurrences"], pc(r["coverage_share"], 2), r["pool_streams_attested"]]
             for r in f19[:25]]))
    A("")

    def top_share(r):
        first = r["top_fillers"].split("; ")[0]
        return int(first.rsplit(":", 1)[1]) / int(r["occurrences"])
    n_nonalt = sum(1 for r in s19 if top_share(r) >= 2 / 3)
    A(f"**Systems.** {ssum['systems']} systems: " + ", ".join(f"{k} {v}" for k, v in ssum["systems_by_slot_type"].items()) + ". By length: " +
      ", ".join(f"n={r['n']} {r['slot_type']} {r['systems']}" for r in sbt) + f". In {n_nonalt} of the {len(s19)} systems the commonest filler "
      "takes at least two thirds of the occurrences (column 'top filler %'); such a frame barely alternates (e.g. `<NAME> djokovic` is "
      "mostly the full name `novak djokovic`), so it is a system only by the letter of criterion (b).")
    A("")
    A("**Table 2.5. The 25 most widespread systems** (`<_>` open slot; full list in `results/systems_2019.tsv`). "
      "'beyond (a)' = share of all tokens covered by the frame but by no repeated n-gram.")
    A("")
    A(table(["rank", "frame", "slot", "occurrences", "utterances", "fillers (top)", "top filler %", "coverage %", "beyond (a) %", "pool matches"],
            [[r["rank"], f"`{r['frame']}`", r["slot_type"], r["occurrences"], r["utterances"],
              "; ".join(r["top_fillers"].split("; ")[:5]), pc(top_share(r), 0), pc(r["coverage_share"], 2), pc(r["coverage_beyond_a_share"], 2),
              r["pool_streams_attested"]] for r in s19[:25]]))
    A("")
    tbm = rcsv("formulas_top_by_medium.csv")
    A("**Table 2.6. Most widespread repeated n-grams of n >= 3 in each corpus** (exploratory; each corpus identified on itself, whole corpus; "
      "utterance counts and rate per 1,000 tokens; n-grams contained in a longer listed one with the same count dropped).")
    A("")
    cn = ["tv_2019wimF", "tv_pool_18_matches", "text_cornell"]
    rows = []
    for k in range(1, 16):
        row = [k]
        for c_ in cn:
            r = next((x for x in tbm if x["corpus"] == c_ and int(x["rank"]) == k), None)
            row.append(f"`{r['formula']}` {r['utterances']} ({r['utterances_per_1000_tokens']})" if r else "")
        rows.append(row)
    A(table(["rank", "2019 final", f"TV pool ({NPOOL} matches)", "Cornell live text"], rows))
    A("")
    A(f"ASR in score calls: of {ssum['score_call_frame_filler_occurrences']} filler occurrences in two-token score-call frames, "
      f"{ssum['score_call_fillers_not_score_words']} are not possible score words (" +
      ", ".join(f"`{k}` {v}" for k, v in list(ssum["non_score_fillers"].items())[:5]) +
      "), i.e. 'forty' heard as `14`, 'thirty' as `13`, 'fifteen' as `50`. These split exact score-call repeats but are absorbed by `<NUM>` systems.")
    A("")
    # ------------------------------------------------------------------ 3 coverage
    A("## 3. Repeated-n-gram coverage")
    A("")
    A("**Table 3.1. Main coverage, pre-registered definitions** (TV commentary, finals).")
    A("")
    rows = []
    for r in dm:
        if r["measure"] != "a":
            continue
        rb = dmv(r["design"], r["identified_on"], r["measured_on"], "a+b")
        rows.append([r["design"], r["identified_on"], r["measured_on"], r["tokens_measured"], f"{pc(r['density'])} {ci(r['ci_lo'], r['ci_hi'])}",
                     f"{pc(rb['density'])} {ci(rb['ci_lo'], rb['ci_hi'])}"])
    A(table(["design", "identified on", "measured on", "tokens", "(a) %", "(a)+(b) %"], rows))
    A("")
    A(f"In-sample and held-out figures differ as the sizes of I lead one to expect: the 2019 final reuses {pc(d1['density'])}% of its tokens within "
      f"itself, {pc(d2['density'])}% when the repeats must come from the other half of the match, and {pc(d3['density'])}% when they come from "
      f"{NPOOL} other matches ({TP:,} tokens, about {TP / T19:.0f} times the final). Coverage therefore depends strongly on the size of I; "
      "compare only like with like.")
    A("")
    A("**Table 3.1b. Coverage family with shuffled-word baselines** (revision 1, exploratory). Coverage [bootstrap 95% CI]; shuffled = mean "
      "[2.5-97.5%] over shuffled replicates; excess = coverage minus shuffled mean [interval]. Held-out baselines shuffle M only.")
    A("")
    rows = []
    for lab, design, ident, meas in DES_ALL:
        for d in C.FAMILY:
            r = famv(design, ident, meas, d)
            has = r["shuffled_mean"] != ""
            rows.append([lab, d, f"{pc(r['coverage'])} {ci(r['ci_lo'], r['ci_hi'])}",
                         f"{pc(r['shuffled_mean'])} {ci(r['shuffled_lo'], r['shuffled_hi'])}" if has else "-",
                         f"{pc(r['excess_over_shuffled'])} {ci(r['excess_lo'], r['excess_hi'])}" if has else "-"])
    A(table(["design", "definition", "coverage %", "shuffled %", "excess (pp)"], rows))
    A("")
    A("**Table 3.2. Corpus contrasts at matched size** (each corpus identified and measured on itself; mean and 2.5-97.5% over replicates). "
      "TV pool, Cornell and press differ in matches, outlet, period, transcription (raw ASR vs edited prose vs edited stenography) and "
      "segmentation (rally-clip windows that cut sentences vs whole updates vs whole answers); the matched-size design equalises tokens "
      "only. Held-out columns give the realised size of I: the pre-registered rule (I = 100,000 tokens from groups disjoint from M) could not "
      "be met for Cornell, because excluding every player pair touched by M removes most of the corpus (DEVIATION, plan.md addendum 2).")
    A("")
    rows = [["shuffled words, 2019 (D7)", f"{T19:,}", f"{pc(sh_in['density'])} {ci(sh_in['ci_lo'], sh_in['ci_hi'])}",
             f"{pc(sh_sp['density'])} {ci(sh_sp['ci_lo'], sh_sp['ci_hi'])}", "-", "-"],
            ["2019 final (single match)", f"{T19:,}", f"{pc(d1['density'])} {ci(d1['ci_lo'], d1['ci_hi'])}",
             f"{pc(d2['density'])} {ci(d2['ci_lo'], d2['ci_hi'])}", f"{pc(d3['density'])} {ci(d3['ci_lo'], d3['ci_hi'])} (pool -> 2019, I = {TP:,})",
             "-"]]
    for corpus in CORP:
        a = medv("D5i_matched_2019_size", corpus, "insample", "a")
        b = medv("D5i_matched_2019_size", corpus, "splithalf", "a")
        if corpus == "tv_pool_all":
            h, hb = "see D3/D4", "-"
        else:
            hv = medv("D5ii_heldout_disjoint_groups", corpus, "heldout", "a")
            hg = medv("D5iib_heldout_grouped_M", corpus, "heldout", "a")
            x, xb = sz[corpus], szb[corpus]
            h = (f"{pc(hv['mean'])} {ci(hv['p2_5'], hv['p97_5'])}; I = {x['tokens_identification_median']:,.0f} "
                 f"({x['tokens_identification_min']:,}-{x['tokens_identification_max']:,}); M from {x['groups_in_measurement_median']:.0f} groups")
            hb = (f"{pc(hg['mean'])} {ci(hg['p2_5'], hg['p97_5'])}; I = {xb['tokens_identification_median']:,.0f}; M from "
                  f"{xb['groups_in_measurement_median']:.0f} groups ({xb['groups_in_measurement_min']}-{xb['groups_in_measurement_max']})")
        rows.append([labels[corpus], f"{T19:,}", f"{pc(a['mean'])} {ci(a['p2_5'], a['p97_5'])}", f"{pc(b['mean'])} {ci(b['p2_5'], b['p97_5'])}",
                     h, hb])
    A(table(["corpus", "tokens measured", f"in-sample (a) %, R = {R1000}", f"split-half (a) %, R = {R1000}",
             f"held-out (a) %, D5(ii) as pre-registered, R = {mmeta['R_heldout']}",
             f"held-out (a) %, M in few groups, D5(ii-b) post hoc, R = {mmeta['R_heldout_grouped']}"], rows))
    A("")
    tvho = float(d3["density"])
    msg = []
    for corpus, name in ((C.TEXT, "Cornell"), ("press_answers", "press")):
        o = float(medv("D5ii_heldout_disjoint_groups", corpus, "heldout", "a")["mean"])
        g = float(medv("D5iib_heldout_grouped_M", corpus, "heldout", "a")["mean"])
        same = (tvho < o) == (tvho < g)
        msg.append(f"{name} {pc(o)}% (D5(ii)) vs {pc(g)}% (D5(ii-b)), change {pc(g - o)} pp; relative to TV pool -> 2019 ({pc(tvho)}%) the "
                   f"direction is {'unchanged' if same else 'reversed'}")
    A("Cornell size correction (B2) and the concentrated-M check: " + "; ".join(msg) + ". D5(ii-b) changes two things at once (I reaches "
      "the pool size, and M comes from few groups: for press usually one interviewee, the closest analogue of TV's one-match M), so the "
      "change is not attributable to either alone.")
    A("")
    A("**Table 3.2b. Corpus contrasts under the stricter definitions** (split-half at the 2019 size, mean [2.5-97.5%] over "
      f"{R1000} subsamples; in-sample n >= 3 for reference).")
    A("")
    rows = []
    for corpus in CORP:
        row = [labels[corpus]]
        for d, est in (("a", "splithalf"), ("n3", "splithalf"), ("n4", "splithalf"), ("content", "splithalf"), ("content_n3", "splithalf"),
                       ("n3", "insample")):
            v = medv("D5i_matched_2019_size", corpus, est, d)
            row.append(f"{pc(v['mean'])} {ci(v['p2_5'], v['p97_5'])}")
        rows.append(row)
    A(table(["corpus", "split-half base", "split-half n >= 3", "split-half n >= 4", "split-half content", "split-half content n >= 3",
             "in-sample n >= 3"], rows))
    A("")
    A("**Table 3.2c. Held-out coverage family across corpora** (TV: pool -> 2019 final, bootstrap CI; Cornell and press: D5(ii) and D5(ii-b), "
      "mean [2.5-97.5%] over replicates).")
    A("")
    rows = []
    row = [f"TV pool -> 2019 (I = {TP:,})"]
    for d in C.FAMILY:
        r = famv("D3_held_out", "pool (18 matches)", C.MAIN, d)
        row.append(f"{pc(r['coverage'])} {ci(r['ci_lo'], r['ci_hi'])}")
    rows.append(row)
    for design, dl in (("D5ii_heldout_disjoint_groups", "D5(ii)"), ("D5iib_heldout_grouped_M", "D5(ii-b)")):
        for corpus in (C.TEXT, "press_answers"):
            row = [f"{labels[corpus]}, {dl}"]
            for d in C.FAMILY:
                v = medv(design, corpus, "heldout", "a" if d == "base" else d)
                row.append(f"{pc(v['mean'])} {ci(v['p2_5'], v['p97_5'])}")
            rows.append(row)
    A(table(["corpus, design"] + list(C.FAMILY), rows))
    A("")
    rows = []
    for corpus in CORP:
        a = medv("D5i_matched_2019_size", corpus, "insample", "a+b")
        b = medv("D5i_matched_2019_size", corpus, "splithalf", "a+b")
        g = medv("D5iii_insample_pool_size", corpus, "insample", "a")
        g3 = medv("D5iii_insample_pool_size", corpus, "insample", "n3")
        rows.append([labels[corpus], f"{pc(a['mean'])} {ci(a['p2_5'], a['p97_5'])}", f"{pc(b['mean'])} {ci(b['p2_5'], b['p97_5'])}",
                     f"{pc(g['mean'])} {ci(g['p2_5'], g['p97_5'])}", f"{pc(g3['mean'])} {ci(g3['p2_5'], g3['p97_5'])}"])
    A(f"**Table 3.3. (a)+(b) at 2019 size (R = {R200}), and (a) in-sample at pool size** ({TP:,} tokens, R = {mmeta['R_large']}).")
    A("")
    A(table(["corpus", "in-sample (a)+(b) %", "split-half (a)+(b) %", "in-sample (a) % at pool size", "in-sample n >= 3 % at pool size"], rows))
    A("")
    A("At pool size the TV 'subsample' is the whole pool, so its replicates are identical. Written live text is identified and measured only "
      "on itself; nothing is pooled across corpora.")
    A("")
    A(f"**Table 3.4. Per stream** (each stream = one match with one unnamed TV broadcaster; broadcaster, match and commentators are confounded). "
      f"Leave-one-out: I = the pool without this stream (for the finals: the whole pool). {mmeta['S_stream']:,}-token columns: mean over "
      f"{mmeta['R_small_stream']} random subsamples.")
    A("")
    rows = []
    streams = sorted({r["stream"] for r in dstr}, key=lambda s: (s.startswith("tv_pool"), s.startswith("press"), s.startswith("text"), s))
    for s in streams:
        def g(design, meas):
            return next((r for r in dstr if r["stream"] == s and r["design"] == design and r["measure"] == meas), None)
        lo = g("D4i_leave_one_stream_out", "a")
        i15 = g("D4ii_insample_1500", "a")
        s15 = g("D4ii_splithalf_1500", "a")
        rows.append([s.replace("tv_pool_", "pool: ")[:60], lo["tokens_measured"] if lo else "-",
                     f"{pc(lo['density'])} {ci(lo['ci_lo'], lo['ci_hi'])}" if lo else "-",
                     f"{pc(i15['density'])} {ci(i15['ci_lo'], i15['ci_hi'])}", f"{pc(s15['density'])} {ci(s15['ci_lo'], s15['ci_hi'])}"])
    A(table(["stream", "tokens", "leave-one-out held-out (a) %", f"in-sample (a) %, {mmeta['S_stream']:,} tokens",
             f"split-half (a) %, {mmeta['S_stream']:,} tokens"], rows))
    A("")
    ctx_names = {"phase": "phase tag (heuristic)", "dtb_terc": "dead time before (tercile)", "ta_terc": "time after (tercile)",
                 "role": "clip role", "score": "score situation"}
    for stream in (C.MAIN, C.HELDOUT):
        rows = []
        for ctx in ("phase", "dtb_terc", "ta_terc", "role", "score"):
            groups = sorted({r["group"] for r in dctx if r["stream"] == stream and r["context"] == ctx})
            for gname in groups:
                def gv(ident, meas):
                    return next(r for r in dctx if r["stream"] == stream and r["context"] == ctx and r["group"] == gname
                                and r["identified_on"] == ident and r["measure"] == meas)
                a, p, pb = gv("in_sample", "a"), gv("pool", "a"), gv("pool", "a+b")
                rows.append([ctx_names[ctx], gname, a["utterances"], a["tokens"], f"{pc(a['density'])} {ci(a['ci_lo'], a['ci_hi'])}",
                             f"{pc(p['density'])} {ci(p['ci_lo'], p['ci_hi'])}", f"{pc(pb['density'])} {ci(pb['ci_lo'], pb['ci_hi'])}"])
        if stream == C.MAIN:
            A(f"**Table 3.5. Per context, 2019 final** ((a) coverage; in-sample = repeats from the whole 2019 stream; pool = repeats from the "
              f"{NPOOL} other matches).")
        else:
            A("**Table 3.6. Per context, 2023 final (held-out match).**")
        A("")
        A(table(["context", "group", "utterances", "tokens", "in-sample (a) %", "pool (a) %", "pool (a)+(b) %"], rows))
        A("")
    A("**Table 3.7. Sensitivity analyses** (2019 unless stated; S-numbers as in plan.md section 8; S5b = revision 1).")
    A("")
    rows = []
    for r in ds:
        if r["measure"] != "a":
            continue
        rb = next(x for x in ds if x["design"] == r["design"] and x["identified_on"] == r["identified_on"] and x["measured_on"] == r["measured_on"]
                  and x["variant"] == r["variant"] and x["measure"] == "a+b")
        rows.append([r["variant"], r["design"], f"{r['identified_on']} -> {r['measured_on']}", f"{pc(r['density'])} {ci(r['ci_lo'], r['ci_hi'])}",
                     f"{pc(rb['density'])} {ci(rb['ci_lo'], rb['ci_hi'])}"])
    A(table(["variant", "design", "I -> M", "(a) %", "(a)+(b) %"], rows))
    A("")
    A(f"S5 masks {pc(meta['S5_masked_token_share_2019'])}% of 2019 tokens as umpire/Hawk-Eye/announcer calls (score calls not masked); S5b, "
      f"the revised mask that adds score calls, `thank you` and the other umpire forms (section 1), masks {pc(meta['S5b_masked_token_share_2019'])}%.")
    A("")
    A(f"**Table 3.8. POST HOC exploratory: injected ASR-like substitution noise** (added after C1/C2 were seen; plan.md addenda 1-2). Each token "
      f"replaced with probability e by a token drawn from the TV-pool unigram distribution, in both I and M; (a) coverage, mean "
      f"[2.5-97.5%] over {an['R_split']} (split-half) or {an['R_held']} (held-out) replicates. e = {lv[1]} is the corpus's hand-read lower "
      "bound on the TV error rate. For TV rows e is noise added on top of the ASR errors already present; in the TV held-out row I and M are "
      "fixed (one pool, one final), so its range reflects only the noise draws, whereas the Cornell and press rows also resample I and M.")
    A("")
    rows = []
    for design, corpus, label in (("splithalf_matched", "tv_pool_all", "split-half, TV pool subsample"),
                                  ("splithalf_matched", C.TEXT, "split-half, Cornell text"),
                                  ("splithalf_matched", "press_answers", "split-half, press answers"),
                                  ("heldout", "tv_pool_to_2019", "held-out, TV pool -> 2019"),
                                  ("heldout", C.TEXT, f"held-out, Cornell text (I median {sz[C.TEXT]['tokens_identification_median']:,.0f}, Table 3.2)"),
                                  ("heldout", "press_answers", "held-out, press answers")):
        row = [label]
        for e in lv:
            cell = an["cells"].get(f"{design}|{corpus}|{e}")
            row.append(f"{pc(cell['mean'])} [{pc(cell['p2_5'])}, {pc(cell['p97_5'])}]" if cell else "-")
        rows.append(row)
    A(table(["design, corpus"] + [f"e = {e}" for e in lv], rows))
    A("")
    lines = []
    for key, lab in (("splithalf_matched|press_answers", "split-half, press"), ("heldout|press_answers", "held-out, press"),
                     ("splithalf_matched|" + C.TEXT, "split-half, Cornell"), ("heldout|" + C.TEXT, "held-out, Cornell")):
        x = cr[key]
        em = (f"mean reaches the TV value ({pc(x['tv_reference_mean'])}%) at e* = {x['e_star_mean_crossing']:.3f}"
              if x["e_star_mean_crossing"] is not None else
              f"mean stays above the TV value ({pc(x['tv_reference_mean'])}%) up to e = {x['max_level_tried']}")
        eo = (f"ranges first overlap at e = {x['e_first_grid_range_overlap']}" if x["e_first_grid_range_overlap"] is not None
              else f"ranges do not overlap up to e = {x['max_level_tried']}")
        lines.append(f"{lab}: {em}; {eo}")
    A("Crossing points (linear interpolation between grid levels; TV references: split-half TV pool at e = 0, and pool -> 2019): " +
      "; ".join(lines) + ". The noise model is not a bound on the real effect of ASR (section 9.1).")
    A("")
    # ------------------------------------------------------------------ 4 tests
    A("## 4. Confirmatory tests and replication")
    A("")
    A("Revised reporting (plan.md addendum 2): C1/R1 are indeterminate whatever their statistics (A1); for C1/R1/C2 the inferential statistic "
      "is the 95% interval of the replicate differences, and the pre-registered \"p\" (2 x the share of replicate pairs on the minority side) "
      "is shown only with its floor 2/(pairs + 1), because it is not a calibrated null test (B1); C4/C5/R4/R5 use the commentary-only "
      "references (B6; the pre-registered all-token results are in Table 4.1b). Holm-Bonferroni is computed, as pre-registered, within the "
      "2019 family (" + ", ".join(r["id"] for r in fam19) + ") and within the 2023 replication family; it is informative only for the "
      "permutation tests C3-C5.")
    A("")

    def est_cell(r):
        cid = r["id"].split("_")[0]
        if cid in ("C4", "R4"):
            return (f"D = {float(r['estimate_x']):.0f} vs null mean {float(r['estimate_y']):.1f}",
                    f"null: {float(r['estimate_y']) + float(r['diff_lo']):.0f}-{float(r['estimate_y']) + float(r['diff_hi']):.0f}")
        if cid in ("C5", "R5"):
            return f"rho = {f3(r['estimate_x'])}", f"null: {f3(r['diff_lo'])} to {f3(r['diff_hi'])}"
        return (f"{pc(r['estimate_x'])} vs {pc(r['estimate_y'])}; diff {pc(r['difference'])} pp", f"{ci(r['diff_lo'], r['diff_hi'])} pp")

    def p_cell(r):
        s = pv(r["p"])
        if r.get("p_at_floor") == "True":
            s += f" (= floor {pv(r['p_floor'])})"
        return s
    rows = []
    for r in conf:
        if r["family"].endswith("_sensitivity"):
            continue
        e, i = est_cell(r)
        rows.append([r["id"], r["hypothesis"], e, i, p_cell(r), pv(r["p_holm"]), r["verdict"]])
    A(table(["test", "hypothesis / statistic", "estimate", "95% interval", "p (pre-registered statistic)", "p (Holm)", "verdict"], rows))
    A("")
    A("* **C1/R1** (commentary more repetitive than non-commentary tennis speech, held-out): indeterminate pending a WER estimate. "
      f"The difference interval ({ci(c1['diff_lo'], c1['diff_hi'])} pp for 2019, {ci(r1['diff_lo'], r1['diff_hi'])} pp for 2023) excludes 0, "
      "but the comparison confounds commentary with ASR noise, transcription convention and held-out design (section 9.1).")
    A(f"* **C2** (corpus contrast, split-half at matched size, TV pool vs Cornell live text): {c2['verdict']}; TV pool {pc(c2['estimate_x'])}% "
      f"vs Cornell {pc(c2['estimate_y'])}%, difference {pc(c2['difference'])} pp {ci(c2['diff_lo'], c2['diff_hi'])} over "
      f"{c2['replicate_pairs']} independent subsample pairs (R raised from {R200} in v1 to {R1000}; f04 stage runtime "
      f"{mmeta['runtime_seconds']['D5i'] / 60:.1f} min on {mmeta['cpus']} CPUs). Its p is the replicate-overlap share"
      + (f" at its floor 2/({c2['replicate_pairs']} + 1) = {pv(c2['p_floor'])}: every one of the {c2['replicate_pairs']} paired "
         "differences has the same sign" if c2["p_at_floor"] == "True" else "") +
      f". In v1, with R = {R200}, the same statistic was "
      f"{2 / (R200 + 1):.5f} and its Holm value {(len(fam19) - 1) * 2 / (R200 + 1):.4f} (rank 2 of {len(fam19)}); that value reflected R, "
      "not evidence near the 0.05 boundary.")
    c3a, c3b, c4, c5 = (cf(x) for x in ("C3a", "C3b", "C4", "C5"))
    A(f"* **C3a/C3b** (less time, more repetition): {c3a['verdict'].split(';')[0]} / {c3b['verdict'].split(';')[0]} (MDE "
      f"{pc(mde['C3a']['mde_achieved_alpha05'])} / {pc(mde['C3b']['mde_achieved_alpha05'])} pp, Table 4.3). Shortest minus longest tercile: dead time before "
      f"{pc(c3a['difference'])} pp {ci(c3a['diff_lo'], c3a['diff_hi'])}; time after {pc(c3b['difference'])} pp {ci(c3b['diff_lo'], c3b['diff_hi'])}. "
      "C3a's predictor (`dead_time_before_s`) is the interval before the point, when the clip's text has not started; C3b (`time_after_s`) is "
      "the apt one (section 9.2).")
    A(f"* **C4** (thrift bound to available time, commentary-only references): {c4['verdict'].split(';')[0]}; D = "
      f"{float(c4['estimate_x']):.0f}, null mean {float(c4['estimate_y']):.1f} (MDE theta = {g2(mde['C4']['mde_param_alpha05'])}).")
    A(f"* **C5** (longer expressions with more time, commentary-only references): {c5['verdict'].split(';')[0]}; rho = "
      f"{f3(c5['estimate_x'])} (MDE rho = {g2(mde['C5']['mde_achieved_alpha05'])}).")
    A("* Replication on the 2023 final: " + ", ".join(f"{x} {cf(x)['verdict'].split(';')[0]}" for x in ("R1", "R3a", "R3b", "R4", "R5")) + ".")
    A("")
    A("**Table 4.1b. Sensitivity: C4/C5/R4/R5 on the pre-registered token set** (all references, including umpire-pattern ones; these are "
      "the v1 confirmatory results; Holm in the original family composition).")
    A("")
    rows = []
    for r in conf:
        if not r["family"].endswith("_sensitivity"):
            continue
        e, i = est_cell(r)
        rows.append([r["id"], r["hypothesis"], e, i, pv(r["p"]), pv(r["p_holm"]), r["verdict"]])
    A(table(["test", "hypothesis / statistic", "estimate", "null 95%", "p", "p (Holm)", "verdict"], rows))
    A("")
    A(f"**Table 4.3. Minimum detectable effects** (post hoc, `f09_power.py`; {mde['nsim']} simulated data sets per grid point; 80% power; "
      "simulation models in the script's docstring). 'Type I at 0' = rejection rate with no injected effect (should be near 0.05).")
    A("")
    rows = []
    scale = {"C3": "coverage difference T1 - T3 (pp)", "C4": "theta: share of references with a tercile-specific form (Cramer's V)",
             "C5": "Spearman rho, syllables vs dead time"}
    for tid in ("C3a", "C3b", "R3a", "R3b", "C4", "R4", "C5", "R5"):
        x = mde[tid]
        k = tid[:2] if tid[:2] in ("C4", "R4", "C5", "R5") else "C3"
        k = {"R4": "C4", "R5": "C5"}.get(k, k)
        r = cf(tid)
        if k == "C3":
            obs = f"{pc(r['difference'])} {ci(r['diff_lo'], r['diff_hi'])}"
            m05 = f"{pc(x['mde_achieved_alpha05'])}"
            mb = f"{pc(x['mde_achieved_bonferroni'])}"
        elif k == "C4":
            obs = f"V = {f2(x['observed_cramers_v_within_strata'])} (null V = {f2(x['achieved_effect_at_zero'])})"
            dr = x['mde_D_reduction_vs_null_alpha05']
            m05 = (f"theta = {g2(x['mde_param_alpha05'])} (V = {g2(x['mde_achieved_alpha05'])}" +
                   (f"; D {dr:.1f} below its null mean)" if dr is not None else ")"))
            mb = f"theta = {g2(x['mde_param_bonferroni'])} (V = {g2(x['mde_achieved_bonferroni'])})"
        else:
            obs = f"rho = {f3(r['estimate_x'])}"
            m05 = f"rho = {g2(x['mde_achieved_alpha05'])} (latent r = {g2(x['mde_param_alpha05'])})"
            mb = f"rho = {g2(x['mde_achieved_bonferroni'])}"
        rows.append([tid, scale[k], obs, m05, f"{mb} (alpha = {x['alpha_bonferroni']:.4f})", f2(x["type_I_error_at_zero_effect"])])
    A(table(["test", "effect scale", "observed", "MDE, alpha = 0.05", "MDE, Bonferroni alpha", "type I at 0"], rows))
    A("")
    A(f"Simulation runtime {mde['runtime_seconds'] / 60:.1f} min. The C3 MDEs are about {pc(mde['C3a']['mde_achieved_alpha05'], 0)}-"
      f"{pc(mde['C3b']['mde_achieved_alpha05'], 0)} pp on a base of about {pc(c3a['estimate_y'], 0)}%; C4 needs roughly "
      f"{pc(mde['C4']['mde_param_alpha05'], 0)}% of references to take a tercile-specific form (in a design where the surname is the "
      f"commonest form in every stratum); C5 needs rho of about {g2(mde['C5']['mde_achieved_alpha05'])} with ties as observed.")
    A("")
    A(f"**Table 4.4. Serial correlation check** (post hoc, exploratory): circular-shift nulls (the context sequence shifted against the "
      f"text sequence by at least {circ['shift_min']} utterances, all shifts) beside the label permutations used in the tests.")
    A("")
    rows = []
    for tid, key in (("C3a", f"{C.MAIN}:ctx_dtb_terc"), ("C3b", f"{C.MAIN}:ctx_ta_terc"), ("R3a", f"{C.HELDOUT}:ctx_dtb_terc"),
                     ("R3b", f"{C.HELDOUT}:ctx_ta_terc")):
        x = circ[key]
        rows.append([tid, f"{pc(x['observed_diff_T1_minus_T3'])} pp", pv(x["p_two_sided_label_permutation_9999"]),
                     pv(x["p_two_sided_circular_shift"]), x["n_shifts"], f"{pc(x['label_permutation_null_sd'], 2)} / {pc(x['shift_null_sd'], 2)} pp"])
    for tid, stream in (("C5", C.MAIN), ("R5", C.HELDOUT)):
        x = circ[f"{stream}:C5_dead_time_before_s"]
        rows.append([tid, f"rho = {f3(x['observed_rho'])}", pv(cf(tid)["p"]), pv(x["p_two_sided_circular_shift"]), x["n_shifts"], "-"])
    A(table(["test", "observed", "p, label permutation", "p, circular shift", "shifts", "null SD, permutation / shift"], rows))
    A("")
    A("**Table 4.2. Exploratory corpus contrasts** (difference x - y in percentage points, 95% interval over replicate pairs; the p column is "
      "the same replicate-overlap share as for C1/C2, with its floor, and is not a calibrated test).")
    A("")
    A(table(["id", "contrast", "x %", "y %", "diff [95%]", "p (floor)"],
            [[r["id"], r["hypothesis"], pc(r["estimate_x"]), pc(r["estimate_y"]), f"{pc(r['difference'])} {ci(r['diff_lo'], r['diff_hi'])}",
              f"{pv(r['p'])} ({pv(r['p_floor'])})"] for r in medc]))
    A("")
    # ------------------------------------------------------------------ 5 refexpr
    A("## 5. Noun-epithet systems")
    A("")
    tb = rsum["tokens_by_stream_player"]
    A(f"Referring expressions found: 2019 Federer {tb.get('tv_2019wimF:federer')}, Djokovic {tb.get('tv_2019wimF:djokovic')}; "
      f"2023 Djokovic {tb.get('tv_2023wimF:djokovic')}, Alcaraz {tb.get('tv_2023wimF:alcaraz')}. Third-person masculine pronouns "
      f"(excluded from the systems, counted): 2019 {rsum['pronouns_total']['tv_2019wimF']}, 2023 {rsum['pronouns_total']['tv_2023wimF']}. "
      f"{rsum['epithet_occurrences']} descriptive-epithet occurrences were assigned to a referent by hand verdict (`hand/epithet_referents.tsv`); "
      f"{rsum['epithets_unresolved']} unresolved.")
    A("")
    ump = rsum["umpire_pattern_tokens"]
    A("Umpire-pattern references (revision 1, rules in section 1), excluded from the thrift and extension tests: " +
      "; ".join(f"{k.split(':')[0][3:7]} `{k.split(':')[1]}` {v}" for k, v in ump.items()) + ".")
    A("")
    A("Inventory: full name, `mr` + surname (umpire), surname, first name, hypocoristic (`nole`, `rog`, `carlitos`), and descriptive epithets "
      "matched by a fixed regex family (`refexpr.py`). Slot: spaCy `" + rsum["spacy_model"] + "` dependency label of the expression's head, mapped "
      "as in plan.md section 5. Syllables: CMU Pronouncing Dictionary (vowel phonemes), vowel-group fallback for names not in it "
      f"(`djokovic` {RX.syll_word('djokovic')}; `nole` gets {RX.syll_word('nole')}, which is wrong: it has two), digits spelled out.")
    lo, hi = wilson(slotv["agree"], slotv["hand_labelled"])
    A("")
    A(f"Slot accuracy against my hand labels on a random sample: {slotv['agree']}/{slotv['hand_labelled']} = {pc(slotv['accuracy'])}% "
      f"(Wilson 95% {pc(lo)}-{pc(hi)}%). Disagreements (hand|parser): " +
      ", ".join(f"{k} {v}" for k, v in slotv["confusion_hand_vs_spacy"].items() if k.split("|")[0] != k.split("|")[1]) + ".")
    A("")
    import re as _re
    disc = rcsv("epithet_discovery.csv")
    pats = [p for p, cat in RX.PATTERNS if cat == "epithet"]
    outside = [d for d in disc if not any(_re.match(p, d["string"]) for p in pats)
               and (int(d["count"]) >= 2 or _re.search(r"champion|number one|seed|returner|player", d["string"]))]
    A("Audit: strings of the form `the (word){0,3} <person noun>` that the inventory does not match (count >= 2, or containing "
      "champion / number one / seed / player / returner), from `results/epithet_discovery.csv`; they are not added, to keep the pre-specified "
      "inventory: " + "; ".join(f"{d['stream'][3:7]} `{d['string']}` {d['count']}" for d in outside) + ".")
    A("")
    ucount = Counter((t["stream"], t["player"], t["expression"]) for s in tok_files for t in tok_files[s] if t["umpire_pattern"])
    A("**Table 5.1. Every referring expression by player, with syllables and syntactic slot** (all references; 'umpire' = of which inside "
      "an umpire pattern).")
    A("")
    A(table(["match", "player", "category", "expression", "tokens", "umpire", "syll.", "subj", "obj", "poss", "after prep", "voc/excl", "other"],
            [[r["stream"][3:7], r["player"], r["category"], f"`{r['expression']}`", r["tokens"],
              ucount.get((r["stream"], r["player"], r["expression"]), 0), r["syllables_base"], r["subject"], r["object"],
              r["possessive"], r["after_preposition"], r["vocative_exclamation"], r["other"]] for r in inv]))
    A("")
    A("**Table 5.2. Length in syllables** (all references).")
    A("")
    A(table(["match", "player", "syllables", "tokens", "expressions"], [[r["stream"][3:7], r["player"], r["syllables"], r["tokens"], r["expressions"]] for r in syl]))
    A("")
    A("**Table 5.3. Timing context** (all references; dead-time and time-after terciles, phase and score situation; tokens, distinct "
      "expressions, mean syllables, share of bare surname).")
    A("")
    rows = [[r["stream"][3:7], r["player"], r["context"], r["group"], r["tokens"], r["distinct_expressions"], r["mean_syllables"],
             pc(r["share_surname"], 0)] for r in byc if r["context"] in ("dtb_terc", "ta_terc", "score", "phase")]
    A(table(["match", "player", "context", "group", "tokens", "distinct", "mean syll.", "surname %"], rows))
    A("")
    A("**Table 5.4. Pronouns** (he, him, his, himself, he's, he'd, he'll) by dead-time tercile; attribution is heuristic "
      "(the single player named in the same utterance).")
    A("")
    A(table(["match", "group", "attributed to", "utterances", "pronouns"],
            [[r["stream"][3:7], r["group"], r["attributed_to"], r["utterances"], r["pronouns"]] for r in pron
             if r["context"] in ("all", "dtb_terc") and r["attributed_to"] in ("ANY", "federer", "djokovic", "alcaraz", "unattributed")]))
    A("")
    # ------------------------------------------------------------------ 6 thrift
    A("## 6. Economy (thrift) and extension")
    A("")
    nperm_th = th[0]["n_perm"]
    A("Functionally equivalent = different expression types (normalised wording, possessive stripped) referring to the same player in the same "
      "syntactic slot and the same context cell. D = sum over player x slot x context cells of the number of distinct types. Null: context labels "
      f"permuted among tokens within each player x slot stratum ({int(nperm_th):,} permutations); one-sided p for 'fewer types than chance' "
      "(thrift). The utterance-level permutation (exploratory) keeps tokens of one utterance together. Revision 1: the tests are run on the "
      "commentary-only references (Table 6.1); the pre-registered all-reference results are in Table 6.1b and Table 4.1b.")
    A("")
    hdr = ["match", "context", "players", "permutation", "status", "tokens", "cells", "D obs", "null mean [95%]", "p (fewer)", "p (two-sided)",
           "single-type cells %"]

    def th_rows(tset, only_conf=False):
        return [[r["stream"][3:7], r["context"], r["players"], r["permutation"], r["status"], r["tokens"], r["cells_occupied"], r["D_observed"],
                 f"{float(r['null_mean']):.1f} [{float(r['null_lo']):.0f}, {float(r['null_hi']):.0f}]", pv(r["p_one_sided_fewer"]),
                 pv(r["p_two_sided"]), pc(r["thrift_index_single_type_cells"], 0)]
                for r in th if r["token_set"] == tset and (not only_conf or not r["status"].startswith("exploratory"))]
    A("**Table 6.1. Thrift tests, commentary-only references.**")
    A("")
    A(table(hdr, th_rows("commentary_only")))
    A("")
    expl = [r for r in th if r["status"] == "exploratory"]
    low = [r for r in expl if float(r["p_one_sided_fewer"]) < 0.05]
    A(f"Of the {len(expl)} exploratory thrift rows (both reference sets), {len(low)} {'has' if len(low) == 1 else 'have'} an unadjusted one-sided p below 0.05" +
      (": " + "; ".join(f"{r['token_set']} {r['stream'][3:7]} {r['context']} {r['players']} {r['permutation']} p = {pv(r['p_one_sided_fewer'])}"
                        for r in low) + ". With this many exploratory rows such values are expected by chance and are not interpreted."
       if low else "."))
    A("")
    A("**Table 6.1b. Sensitivity: thrift tests on all references (pre-registered token set; exploratory rows in `results/thrift_tests.csv`).**")
    A("")
    A(table(hdr, th_rows("all_tokens", only_conf=True)))
    A("")
    A("**Table 6.2. Extension** (size and range of each player's system).")
    A("")
    A(table(["references", "match", "player", "tokens", "distinct expressions", "categories", "syllables min-max", "distinct lengths",
             "occupied cells (slot x dead-time x length class)", "surname %", "epithet %"],
            [[r["token_set"], r["stream"][3:7], r["player"], r["tokens"], r["distinct_expressions"], r["distinct_categories"],
              f"{r['syllable_min']}-{r['syllable_max']}", r["distinct_syllable_lengths"], r["occupied_cells_slot_x_dtb_x_sylclass"],
              pc(r["share_surname"], 0), pc(r["share_epithet"], 0)] for r in ext]))
    A("")
    A("**Table 6.3. Length vs available time** (Spearman rho over expression tokens).")
    A("")
    A(table(["references", "match", "time", "permutation", "status", "tokens", "rho", "null 95%", "p"],
            [[r["token_set"], r["stream"][3:7], r["time"], r["permutation"], r["status"], r["tokens"], f3(r["rho"]),
              f"{f3(r['null_lo'])} to {f3(r['null_hi'])}", pv(r["p_two_sided"])] for r in lt]))
    A("")
    A("The surname is the commonest form in every player x slot stratum, so most cells hold one or two types whatever the context; with "
      f"these counts the thrift test would detect only a strong context-binding (Table 4.3: theta = {g2(mde['C4']['mde_param_alpha05'])} "
      f"for 2019, {g2(mde['R4']['mde_param_alpha05'])} for 2023). The context is a clip-level tercile, while a clip's text spans the rally and "
      "the following dead time, so the cells do not encode the time available at the moment a name is chosen.")
    A("")
    # ------------------------------------------------------------------ 7 top-10
    A("## 7. Top-10 repeated n-grams and systems for the composition brief (Phase 3)")
    A("")
    A("Pre-specified ranking: distinct utterances, after dropping items contained in a longer item with the same count. Revision 1: "
      "`official` = at least half of the occurrences fall inside the revised umpire/score-call patterns (`common.official_mask_v2`, section 1); "
      "the pre-registered S5 patterns never covered score calls, so the flag did not fire on them in v1. The pre-specified list is shown with "
      "the flag, then the commentary-only list. Situational slot: modal clip role, share of occurrences at pressure points "
      "(break/set/match/tie-break/deuce), median time after and before (s).")
    A("")
    hdr = ["rank", "kind", "item", "utterances", "occurrences", "pool matches", "fillers (top)", "official", "modal role",
           "pressure %", "median time after", "median dead time before"]

    def trow(r):
        return [r["rank"], r["kind"], f"`{r['item']}`", r["utterances"], r["occurrences"], r["pool_streams_attested"],
                "; ".join(r["fillers"].split("; ")[:4]), r["official_call"], r["modal_clip_role"], pc(r["pressure_points_share"], 0),
                r["median_time_after_s"], r["median_dead_time_before_s"]]
    for lst, title in ((top, "Table 7.1"), (top3, "Table 7.2")):
        sub = "pre-specified top 10" if lst is top else "exploratory top 10 restricted to n >= 3 repeats and systems with >= 2 fixed tokens"
        A(f"**{title}a. {sub[0].upper() + sub[1:]}, with the `official` flag.**")
        A("")
        A(table(hdr, [trow(r) for r in lst if r["list"] == "with_official"]))
        A("")
        A(f"**{title}b. {sub[0].upper() + sub[1:]}, umpire/score-call items excluded (commentary only).**")
        A("")
        A(table(hdr, [trow(r) for r in lst if r["list"] == "commentary_only"]))
        A("")
    # ------------------------------------------------------------------ 8 Kuiper
    A("## 8. Kuiper")
    A("")
    for r in kv:
        A(f"* {r['reference']} Status: **{r['status']}**. Record: {r['record_fetched']}. Confirms: {r['what_the_record_confirms']}.")
    A("")
    A("**What the verified records say.** Only the abstract of Kuiper and Haggo (1984) was read (record above): stock auctioneers \"use an "
      "oral formulaic technique\"; the technique \"is a response to performance constraints which place a heavy load on short term memory\"; "
      "and \"the difference between traditional oral formulaic and ordinary spoken language is one of degree, not kind\". For Kuiper (1996), "
      "Smooth Talkers, whose subtitle names auctioneers and sportscasters, and for Kuiper (2004, 2009) only bibliographic data were verified; "
      "nothing is claimed about their content, and the race-calling chapter attributed to Kuiper and Austin is [unverified].")
    A("")
    d13 = famv("D1_in_sample", C.MAIN, C.MAIN, "n3")
    h3 = famv("D3_held_out", "pool (18 matches)", C.MAIN, "n3")
    ge1 = sum(int(r["formula_types_2019"]) for r in cs if int(r["pool_streams_attested"]) >= 1)
    A("**What the data show.**")
    A("")
    A(f"* Repetition in the commentary is real and above a word-frequency floor: {pc(d1['density'])}% of the 2019 final's tokens lie in "
      f"n-grams repeated within the match, {pc(d13['coverage'])}% in repeats of three or more words (shuffled floor "
      f"{pc(d13['shuffled_mean'])}%), and {pc(h3['coverage'])}% of its tokens lie in n >= 3 repeats already found in the {NPOOL} other "
      f"matches; {ge1} of the {fsum['formula_types_stop_filtered']} repeated types of the final recur in at least one other match "
      "(Tables K, 2.3, 3.1b).")
    lower_all = all(float(medv("D5i_matched_2019_size", "tv_pool_all", "splithalf", d)["mean"]) <
                    min(float(medv("D5i_matched_2019_size", c, "splithalf", d)["mean"]) for c in (C.TEXT, "press_answers"))
                    for d in ("a",) + C.FAMILY[1:])
    A("* Degree: no auctioneer, race-call or other sportscaster corpus was measured with this procedure, so the commentary cannot be placed "
      "on a scale relative to Kuiper and Haggo's auctioneers. Among the corpora that were measured, the TV pool has lower matched-size "
      "split-half coverage than Cornell written live text and press answers " +
      ("under every definition in Table 3.2b" if lower_all else "under some but not all definitions of Table 3.2b") +
      "; these are corpus contrasts (section 9.3), and the TV-vs-press comparison is indeterminate pending a WER estimate (C1/R1).")
    A(f"* Performance constraint: if repetition relieved time pressure, coverage and naming should shift toward the clips with the least time. "
      f"No such shift was detected (C3a, C3b, C4, C5 and replications), but the tests could detect only large effects (Table 4.3: about "
      f"{pc(c3lo, 0)}-{pc(c3hi, 0)} pp of coverage, theta = {g2(mde['C4']['mde_param_alpha05'])}, rho = "
      f"{g2(mde['C5']['mde_achieved_alpha05'])}), and available time is assigned per clip rather than per phrase. The data therefore say "
      "nothing either way about whether tennis commentary carries the memory load described for auctioneers.")
    A("")
    # ------------------------------------------------------------------ 9 limitations
    circ_ps = [v["p_two_sided_circular_shift"] for k, v in circ.items() if isinstance(v, dict)]
    A("## 9. Limitations")
    A("")
    A(f"1. **ASR and the TV-vs-press contrast (C1/R1).** The text is WhisperX output with no audio; the word error rate is unknown. The "
      f"corpus's hand-read figure, {asr['hand_sample']['total_per_1000_words']:.0f} errors per 1,000 words (Wilson 95% "
      f"{asr['hand_sample']['wilson95_ci_per_1000_total'][0]:.0f}-{asr['hand_sample']['wilson95_ci_per_1000_total'][1]:.0f}, "
      "`corpus/reports/asr_proxy.json`), counts only visible errors and is a lower bound; plausible-word substitutions are invisible. "
      "Four things make the TV-vs-press contrast uninterpretable as a statement about commentary. (i) ASR noise alone can produce it: "
      f"injected substitutions bring the held-out press value to the TV value at e* = {es(hp)} (split-half {es(sp_)}), a rate that cannot "
      "be excluded because only a lower bound on the TV error rate exists. (ii) Transcription "
      "convention: press answers are edited stenographic transcripts (disfluencies removed, sentences complete), while the TV text is raw ASR "
      "in clip windows with mid-sentence boundaries; both differences raise press repetition independently of how anyone speaks. (iii) The "
      "held-out designs are not analogous: for TV, I is other matches with mostly different commentators; for press, I is other interviewees of "
      "the same genre, transcription house and questioners. (iv) The v1 claim that the one-match TV measurement set favours TV is withdrawn: a "
      f"concentrated M helps only if its recurrent items are in I, and {sum(int(r['formula_types_2019']) for r in cs if int(r['pool_streams_attested']) == 0)} "
      "of the final's repeated types occur in no pool match. In the post hoc check D5(ii-b), where the press M comes from a median of "
      f"{szb['press_answers']['groups_in_measurement_median']:.0f} interviewees, press held-out coverage is "
      f"{pc(medv('D5iib_heldout_grouped_M', 'press_answers', 'heldout', 'a')['mean'])}% against "
      f"{pc(medv('D5ii_heldout_disjoint_groups', 'press_answers', 'heldout', 'a')['mean'])}% with M spread over many interviewees, so "
      "concentrating M did not visibly change the press value. The noise model is not a bound either: independent uniform substitutions drawn "
      "from the unigram distribution are neither clustered (real errors concentrate in names, score calls and overlapping speech) nor include "
      "deletions, insertions or word merges, and frequent-word replacements can create matches. Settling C1/R1 needs a measured WER on a sample "
      "with audio (FOR_HUMAN.md) or a within-convention comparison (e.g. press-conference audio through the same ASR pipeline).")
    A("2. **Clip-level text and time.** No word times: a clip's text spans the rally and the following dead time, so 'available time' is "
      "assigned per clip, not per phrase. C3a's predictor `dead_time_before_s` is the interval before the point, when the clip's text has not "
      "started, so it is misaligned with the text; C3b (`time_after_s`) is the apt predictor. The label permutations of C3-C5 treat adjacent "
      "clips as exchangeable although coverage and context may be serially correlated; with circular-shift nulls instead (Table 4.4) the "
      f"p-values range from {pv(min(circ_ps))} to {pv(max(circ_ps))}, so no conclusion changes. "
      "The phase tags are text-based heuristics; `between_points` clips are score calls by definition.")
    A("3. **Corpus contrasts, not medium contrasts.** TV pool, Cornell and press differ in matches (Cornell has no match ids), outlet (one "
      f"live-text outlet with a house style), period (press record dates {pyears[0]}-{pyears[1]}, TV {tyears[0]}-{tyears[1]}), transcription "
      "(raw ASR vs edited prose vs edited stenography) and segmentation (clip windows vs updates vs answers); matched size equalises tokens "
      "only. A same-match comparison (TV and written minute-by-minute of one match, FOR_HUMAN.md) would be needed before 'medium' is claimed.")
    A("4. **What the measure is.** Repeated-n-gram coverage rises with vocabulary concentration and genre templating, so it orders texts by "
      "repetition rate, not by oral-formulaic composition; the stricter family (Tables K, 3.1b, 3.2b) shows how much rests on short repeats. "
      "The shuffled-word baseline destroys syntax and is a floor, not a null that preserves local grammar.")
    A("5. **One broadcaster per match, no speaker labels.** Commentator identity, broadcaster and match are confounded in every per-stream "
      "comparison; the umpire's and Hawk-Eye's voices are inside the text (S5/S5b mask the clearest calls; score calls are said by both).")
    A("6. **De-duplication.** Exact repeats of the previous clip's text (within 3 clips) were removed by the corpus builder; shorter overlaps "
      "remain. S4 (repeats at least 4 clips apart) and S1 (`text_dedup`) bound the effect.")
    A("7. **Size dependence.** Coverage rises with the size of the identification set; only size-matched comparisons are interpretable "
      f"(Tables 3.2-3.4). For Cornell the pre-registered held-out I could not reach 100,000 tokens (median "
      f"{sz[C.TEXT]['tokens_identification_median']:,.0f}); D5(ii-b) shows the effect of a larger I with a differently drawn M.")
    A("8. **Referring expressions.** The epithet inventory is a fixed regex family checked against a discovery list; referents of descriptive "
      "epithets and the slot validation are single-annotator hand verdicts; pronouns are not resolved. Umpire patterns are excluded by rule, "
      "which may miss unusual calls or catch a commentator echoing one. The thrift and extension tests have little power (Table 4.3).")
    A("9. **CIs** condition on the repeated-n-gram inventory; split-half and random-split distributions (Table 3.7) show the identification "
      "variability. Utterances differ in length across corpora (mean tokens in section 0); because a repeat must recur in two distinct "
      "utterances, the shorter TV utterances make that criterion, if anything, easier for TV to meet.")
    A("")
    # ------------------------------------------------------------------ 10 revision log
    A("## 10. Revision log (after `review/critic_analysis_v1.md`; details in plan.md addendum 2)")
    A("")
    A("* A1: C1/R1 relabelled 'indeterminate pending a WER estimate'; the 'asymmetry favours TV' claim withdrawn; crossing points e* computed "
      f"(f04b, held-out R raised to {an['R_held']}); the substantive discussion moved to section 9.1.")
    A(f"* B1: C1/R1/C2 use the 95% interval of replicate differences; p shown with its floor; D5(i) R raised from {R200} to {R1000} "
      f"(f04 total runtime {mmeta['runtime_seconds']['total'] / 60:.1f} min on {mmeta['cpus']} CPUs; D5(i) stage "
      f"{mmeta['runtime_seconds']['D5i'] / 60:.1f} min).")
    A(f"* B2: Cornell held-out I size corrected (median {sz[C.TEXT]['tokens_identification_median']:,.0f}, range "
      f"{sz[C.TEXT]['tokens_identification_min']:,}-{sz[C.TEXT]['tokens_identification_max']:,} tokens, not {TP:,}); deviation logged; "
      "D5(ii-b) added (Table 3.2).")
    A("* B3: measure renamed repeated-n-gram coverage; stricter family (n >= 3, n >= 4, content-only, content n >= 3) with bootstrap CIs for "
      "in-sample, split-half, pool -> 2019, 2019 -> 2023 and pool -> 2023, and for the corpus contrasts; shuffled baselines and excess for "
      "every definition (Tables K, 3.1b, 3.2b, 3.2c).")
    A("* B4: Kuiper section limited to verified records and data; minimum detectable effects simulated for C3-C5 (Table 4.3).")
    A("* B6: umpire-pattern references excluded from C4/C5/R4/R5 (rules in section 1); all-reference results kept as sensitivity "
      "(Tables 4.1b, 6.1b).")
    A("* B7: every TV/Cornell/press comparison labelled a corpus contrast.")
    A("* Minor: Duggan record fetched (criterion wording [unverified]); dates and replicate counts in the text read from data; top-10 "
      "`official` flag fires on score calls and `thank you`; top-filler share of systems shown; C3a interval and serial correlation "
      "noted, circular-shift check added (Table 4.4); noise-table caption explains the different meaning of the TV held-out range.")
    A("")
    # ------------------------------------------------------------------ 11 files
    A("## 11. Files")
    A("")
    A("`plan.md` (pre-specification and addenda), `common.py` (tokeniser, STOP, numerals, identification, coverage family, masks, contexts), "
      "`refexpr.py`, scripts `f01`-`f09` (`f04b` and `f09` post hoc), `make_report.py`, `run_all.sh`; hand inputs in `hand/` "
      "(`duggan_verification.tsv`, `kuiper_verification.tsv`, `epithet_referents.tsv`, `slot_sample40.tsv`); all tables in `results/` "
      "(`coverage_family.csv`, `density_*.csv` (column `density` = repeated-n-gram coverage), `medium_replicates.csv`, `confirmatory.csv`, "
      "`medium_contrasts.csv`, `power_curves.csv`, `mde_summary.json`, `circular_shift_tests.json`, `asr_noise_*`, `refexpr_*`, `thrift_*`, "
      "`formulas_2019.tsv`, `systems_2019.tsv`, `top10_for_brief*.csv`, `deviations.json`). Transcript excerpts in committed files are at most "
      f"12 words (repeated n-grams {fsum['excerpt_words_written']} words in total, systems {ssum['excerpt_words_written']}) or 15 words "
      "(hand files, epithet candidates).")
    C.write_json(R / "deviations.json", {
        "replicate_changes": [
            {"design": "D5(i)", "planned_R": R200, "used_R_a_family": R1000, "used_R_ab": R200,
             "note": "revision 1 (B1): increase for the (a) family; first replicates identical to v1 (same seeds)"},
            {"design": "f04b held-out noise rows (post hoc)", "v1_R": 10, "used_R": an["R_held"], "note": "revision 1 (critic C8)"},
        ],
        "replicate_reductions": [],
        "D5ii_identification_size": {"planned_tokens": TP, "realised": sz,
                                     "note": "revision 1 (B2): for Cornell the disjoint-group rule exhausts the eligible set; unlogged in v1"},
        "C1_R1_reporting": "revision 1 (A1): reported as indeterminate pending a WER estimate instead of by the Holm decision rule",
        "C1_R1_C2_inferential_statistic": "revision 1 (B1): 95% interval of replicate differences; the pre-registered p is kept with its floor",
        "C4_C5_R4_R5_token_set": {"revised": "commentary_only (umpire-pattern references excluded)", "pre_registered": "all_tokens (sensitivity)",
                                  "excluded_tokens": nump},
        "top10_official_flag": "revision 1: common.official_mask_v2 (S5 + score calls + thank you + other umpire forms) instead of S5",
        "excerpts": "plan section 9 allowed excerpts for the 100 most frequent formulas and 50 most frequent systems; 80 and 40 were "
                    "written, each at most 12 words and never overlapping an already written window, to keep committed transcript text small",
        "post_hoc_additions": ["f04b_asr_noise.py (plan.md addendum 1, written after C1/C2 were seen); exploratory only",
                               "formulas_top_by_medium.csv (exploratory list, added for the report)",
                               "revision 1: coverage family and held-out shuffled baselines (f03, f04), S5b, D5(ii-b), f09_power.py "
                               "(MDE, circular-shift nulls), crossing points in f04b"],
        "inventory_fix_before_hand_labels": "refexpr.word_seq strips a trailing period so that 'Mr.' matches the title_surname pattern; "
                                            "made before the 40-item slot sample was hand-labelled",
    })
    # guard: committed transcript excerpts must be at most 15 words
    for name, col in (("formulas_2019.tsv", "example_excerpt_max12w"), ("systems_2019.tsv", "example_excerpt_max12w"),
                      ("epithet_candidates.tsv", "excerpt_max15w"), ("../hand/epithet_referents.tsv", "excerpt_max15w")):
        for r in rcsv(name, "\t"):
            assert len(r[col].split()) <= 15, (name, r[col])
    text = "\n".join(L) + "\n"
    # guard: retired wording must not reappear
    for bad in ("OPPOSITE", "not with the auctioneers", "favours TV, so"):
        assert bad not in text, bad
    (C.HERE / "report.md").write_text(text, encoding="utf-8")
    print("report.md written:", len(L), "lines")


if __name__ == "__main__":
    main()
