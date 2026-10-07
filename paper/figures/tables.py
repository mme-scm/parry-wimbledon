"""Writes the four script-generated tables of paper/paper.md as Markdown into paper/figures/tables/.
Reads only analysis/formulas/results/ and analysis/metre/results/. The tables are pasted verbatim into
paper.md; `bash paper/figures/make_all.sh` regenerates them, so a diff shows any drift."""
import pandas as pd

import sys as _sys
from pathlib import Path as _Path

_sys.path.insert(0, str(_Path(__file__).resolve().parent))  # python -I does not add the script dir
from common import RES_F, RES_M, TABLES

TABLES.mkdir(exist_ok=True)


def ci(v, lo, hi, nd=1, scale=100.0, unit=""):
    return f"{scale * v:.{nd}f} [{scale * lo:.{nd}f}, {scale * hi:.{nd}f}]{unit}"


def write(name, lines):
    (TABLES / name).write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"wrote tables/{name}")


# ---------------------------------------------------------------- Table 1: coverage
cf = pd.read_csv(RES_F / "coverage_family.csv")
dm = pd.read_csv(RES_F / "density_main.csv")
DESIGNS = [
    ("D1_in_sample", "tv_2019wimF", "tv_2019wimF", "in-sample (2019 → 2019)"),
    ("D2_split_half", "2019 halves", "2019 other half (pooled)", "split-half (2019 halves)"),
    ("D3_held_out", "pool (18 matches)", "tv_2019wimF", "pool (18 matches) → 2019"),
    ("D3_held_out", "tv_2019wimF", "tv_2023wimF", "2019 → 2023 (held-out final)"),
]
DEFS = [
    ("base", "n ≥ 2, not stop-only (pre-registered (a))"),
    ("content", "n ≥ 2, not function-word/numeral-only"),
    ("n3", "n ≥ 3"),
    ("content_n3", "n ≥ 3, not function-word/numeral-only"),
    ("n4", "n ≥ 4"),
]


def cov_cell(d, i_on, m_on, key):
    r = cf[(cf.design == d) & (cf.identified_on == i_on) & (cf.measured_on == m_on) & (cf.definition == key)]
    assert len(r) == 1
    r = r.iloc[0]
    return ci(r.coverage, r.ci_lo, r.ci_hi)


def shuf_cell(d, i_on, m_on, key):
    r = cf[(cf.design == d) & (cf.identified_on == i_on) & (cf.measured_on == m_on) & (cf.definition == key)].iloc[0]
    return ci(r.shuffled_mean, r.shuffled_lo, r.shuffled_hi)


def ab_cell(d, i_on, m_on):
    r = dm[(dm.design == d) & (dm.identified_on == i_on) & (dm.measured_on == m_on) & (dm.measure == "a+b") & (dm.variant == "primary")]
    assert len(r) == 1
    r = r.iloc[0]
    return ci(r.density, r.ci_lo, r.ci_hi)


L = ["| definition | " + " | ".join(d[3] for d in DESIGNS) + " |", "|---|" + "---|" * len(DESIGNS)]
for key, lab in DEFS:
    L.append(f"| {lab} | " + " | ".join(cov_cell(d, i, m, key) for d, i, m, _ in DESIGNS) + " |")
L.append("| (a) + one-slot systems (b), base definition | " + " | ".join(ab_cell(d, i, m) for d, i, m, _ in DESIGNS) + " |")
L.append("| shuffled-word baseline, base definition (mean [2.5–97.5%]) | " + " | ".join(shuf_cell(d, i, m, "base") for d, i, m, _ in DESIGNS) + " |")
L.append("| shuffled-word baseline, n ≥ 3 | " + " | ".join(shuf_cell(d, i, m, "n3") for d, i, m, _ in DESIGNS) + " |")
tok = cf[(cf.definition == "base")].drop_duplicates(["design", "identified_on", "measured_on"])
L.append("| tokens measured | " + " | ".join(str(int(cf[(cf.design == d) & (cf.identified_on == i) & (cf.measured_on == m) & (cf.definition == "base")].tokens_measured.iloc[0])) for d, i, m, _ in DESIGNS) + " |")
write("table1_coverage.md", L)

# ---------------------------------------------------------------- Table 2: confirmatory C1-C5, R1-R5
c = pd.read_csv(RES_F / "confirmatory.csv").set_index("id")
SHORT = {
    "C1": "coverage, pool → 2019 final, minus press answers (held-out; I ≈ 100k → M 9.8k)",
    "R1": "coverage, pool → 2023 final, minus press answers (held-out)",
    "C2": "split-half coverage at 2019 size: TV pool minus Cornell live text (corpus contrast)",
    "C3a": "coverage (pool-identified), shortest minus longest tercile of dead time before the point",
    "C3b": "coverage (pool-identified), shortest minus longest tercile of time after the point",
    "R3a": "as C3a, 2023 final",
    "R3b": "as C3b, 2023 final",
    "C4": "thrift: distinct name forms per player × slot × dead-time tercile, below permutation null",
    "R4": "as C4, 2023 final",
    "C5": "extension: Spearman ρ of name length (syllables) with dead time before",
    "R5": "as C5, 2023 final",
}
L = ["| id | test | estimate | 95% interval | p (pre-registered statistic) | p (Holm) | MDE (80% power, α = 0.05 / Bonferroni) | verdict |", "|---|---|---|---|---|---|---|---|"]
for i in SHORT:
    r = c.loc[i]
    verdict = str(r.verdict).split(";")[0]
    if i in ("C1", "R1", "C2"):
        est = f"{100 * r.estimate_x:.1f} vs {100 * r.estimate_y:.1f}; diff {100 * r.difference:+.1f} pp"
        iv = f"[{100 * r.diff_lo:+.1f}, {100 * r.diff_hi:+.1f}] pp (replicate differences)"
        p = f"{r.p:.4f} (= floor 2/(R+1); uncalibrated)"
        holm = "—"
        mde = "—"
    elif i.startswith("C3") or i.startswith("R3"):
        est = f"{100 * r.estimate_x:.1f} vs {100 * r.estimate_y:.1f}; diff {100 * r.difference:+.1f} pp"
        iv = f"[{100 * r.diff_lo:+.1f}, {100 * r.diff_hi:+.1f}] pp (bootstrap)"
        p = f"{r.p:.4f} (permutation)"
        holm = f"{r.p_holm:.4f}"
        mde = f"{100 * r.mde_80_alpha05:.1f} / {100 * r.mde_80_bonferroni:.1f} pp"
    elif i in ("C4", "R4"):
        est = f"D = {r.estimate_x:.0f} vs null mean {r.estimate_y:.1f}"
        iv = f"null 95%: [{r.estimate_y + r.diff_lo:.0f}, {r.estimate_y + r.diff_hi:.0f}]"
        p = f"{r.p:.4f} (one-sided permutation)"
        holm = f"{r.p_holm:.4f}"
        mde = f"θ = {r.mde_80_alpha05:.2f} / {r.mde_80_bonferroni:.2f}"
    else:
        est = f"ρ = {r.estimate_x:.3f}"
        iv = f"null 95%: [{r.diff_lo:.3f}, {r.diff_hi:.3f}]"
        p = f"{r.p:.4f} (two-sided permutation)"
        holm = f"{r.p_holm:.4f}"
        mde = f"ρ = {r.mde_80_alpha05:.2f} / {r.mde_80_bonferroni:.2f}"
    L.append(f"| {i} | {SHORT[i]} | {est} | {iv} | {p} | {holm} | {mde} | {verdict} |")
write("table2_confirmatory.md", L)

# ---------------------------------------------------------------- Table 3: metre T1-T4
mde = pd.read_csv(RES_M / "posthoc_mde.csv")


def mde_cell(match, test):
    s = mde[(mde.match == match) & (mde.test == test) & (mde.mix == 0.0)]
    if s.empty:
        return "— (not simulated)"
    a = s[s.alpha_label == "alpha05"].mde_true.iloc[0]
    h = s[s.alpha_label == "alpha_holm1"].mde_true.iloc[0]
    if test in ("T2", "T4"):
        return f"{100 * a:.1f} / {100 * h:.1f} pp"
    return f"ρ = {a:.3f} / {h:.3f}"


PRED = {"T1": "ρ > 0 (precondition; H0 predicts it too)", "T2": "> 0 (short intervals more formulaic)",
        "T3": "ρ > 0 (longer formulas with more time)", "T4": "> 0 (changeover talk less formulaic)"}
L = ["| match | test | H1′ predicts | estimate [95% CI] | n | p (shift null; shifts) | p (Holm) | sign as H1′ | MDE at α = 0.05 / first Holm step |", "|---|---|---|---|---|---|---|---|---|"]
for match in ("2019wimF", "2023wimF"):
    t = pd.read_csv(RES_M / f"confirmatory_{match}.csv")
    for _, r in t.iterrows():
        if not bool(r.testable):
            L.append(f"| {match} | {r.test} | {PRED[r.test]} | {r.note} | | | | | |")
            continue
        if r.test in ("T2", "T4"):
            est = f"{100 * r.estimate:+.1f} pp [{100 * r.ci_lo:+.1f}, {100 * r.ci_hi:+.1f}]"
        else:
            est = f"ρ = {r.estimate:.3f} [{r.ci_lo:.3f}, {r.ci_hi:.3f}]"
        n = f"{int(r.n_units)} units" + (f" / {int(r.n_strings)} strings" if pd.notna(r.n_strings) else "")
        L.append(f"| {match} | {r.test} | {PRED[r.test]} | {est} | {n} | {r.p_shift:.4f} ({int(r.n_shifts)}) | {r.p_holm:.4f} | {'yes' if bool(r.direction_as_H1) else 'no'} | {mde_cell(match, r.test)} |")
write("table3_metre.md", L)

# ---------------------------------------------------------------- Table 4: referring expressions
ext = pd.read_csv(RES_F / "extension.csv")
inv = pd.read_csv(RES_F / "refexpr_inventory.csv")
L = ["| match | player | references (all) | inside umpire patterns (excluded) | commentary-only references | distinct forms (commentary-only) | bare surname % | descriptive epithets % | syllables (min–max) | forms with ≥ 2 tokens (all references) |", "|---|---|---|---|---|---|---|---|---|---|"]
for (stream, player) in [("tv_2019wimF", "federer"), ("tv_2019wimF", "djokovic"), ("tv_2023wimF", "djokovic"), ("tv_2023wimF", "alcaraz")]:
    co = ext[(ext.token_set == "commentary_only") & (ext.stream == stream) & (ext.player == player)].iloc[0]
    al = ext[(ext.token_set == "all_tokens") & (ext.stream == stream) & (ext.player == player)].iloc[0]
    forms = inv[(inv.stream == stream) & (inv.player == player)].sort_values("tokens", ascending=False)
    big = [f"`{e}` {int(t)}" for e, t in zip(forms.expression, forms.tokens) if t >= 2]
    rest = int((forms.tokens < 2).sum())
    fstr = "; ".join(big) + (f"; +{rest} single-token forms" if rest else "")
    L.append(f"| {stream[3:7]} | {player.capitalize()} | {int(al.tokens)} | {int(co.umpire_pattern_tokens_excluded)} | {int(co.tokens)} | {int(co.distinct_expressions)} | {100 * co.share_surname:.0f} | {100 * co.share_epithet:.0f} | {int(co.syllable_min)}–{int(co.syllable_max)} | {fstr} |")
write("table4_refexpr.md", L)
