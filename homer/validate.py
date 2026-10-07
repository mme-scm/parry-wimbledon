#!/usr/bin/env python3
"""Validate the scanner on every line of Homer and write homer/validation.md.

    python homer/validate.py          (after homer/build_tables.py)

Runs, on all 27,794 lines:
  core      tier-0 rules only (nature, position, muta cum liquida, elision,
            epic correption, hiatus, single digamma, accent rules), α/ι/υ free
  tier<=1   + the common licences (synizesis, lengthening before liquids, ...)
  pass 1    + the rare licences (tier 2) = the full rule set, α/ι/υ free
  final     pass 1 + preferences for attested α/ι/υ quantities (dichrona.tsv,
            dichrona_analogy.tsv) = homer/scansion.tsv
and ablations of the final configuration (no digamma list; accent rules off;
accent rules as hard constraints).  A seeded sample of 50 core failures is
classified by the licence that the full scanner needs for it; the remaining
failures are listed with the explanations in homer/failure_notes.tsv; the
manual checks in homer/manual_checks.tsv are compared with the scanner.
All figures in validation.md and in the generated block of README.md come
from this script.
"""
import collections
import csv
import json
import pathlib
import random
import re
import sys
from multiprocessing import Pool

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import scan as S  # noqa: E402

SEED = 20261007
CAUSE = {
    "synizesis": "synizesis (within a word: θεοί, -εω, χρυσέῳ)",
    "synizesis_cross": "synizesis across words (δὴ αὖ, ἐπεὶ οὐ, ἢ οὐ)",
    "synizesis_i": "consonantal ι/υ (Αἰγυπτίη, πόλιος)",
    "synizesis_rare": "other synizesis",
    "synizesis_cross_rare": "other synizesis across words",
    "lengthening_liquid": "short final vowel lengthened before λ μ ν ρ σ",
    "lengthening_liquid_internal": "short vowel lengthened before λ μ ν ρ σ inside a word",
    "lengthening_closed": "closed final syllable lengthened in arsis before a vowel",
    "internal_correption": "internal correption (οἷος, υἱός, ἥρωος)",
    "hiatus_long": "long vowel kept before a vowel in the biceps",
    "digamma_double": "σϝ/δϝ counted as two consonants (ἀπὸ ἕο, δέος)",
    "metrical_lengthening": "metrical lengthening of a short vowel in arsis",
    "lengthening_hiatus": "short final vowel lengthened in arsis before a vowel",
    "no_position_initial_cluster": "no position before initial ζ / σ+consonant (Σκάμανδρος, Ζάκυνθος)",
    "accent_contra": "α/ι/υ against the accent rule (βλοσυρῶπις, ἦνιν, dative -ι long)",
    "dichronon_contra": "α/ι/υ contrary to attested quantity",
    "analogy_contra": "α/ι/υ contrary to analogy",
}


def run_config(args):
    text, tier, learned, analogy, rules = args
    S.RULES.update(rules)
    res = S.scan(text, learned=learned, analogy=analogy, max_tier=tier)
    out = {"status": res["status"], "tier": res["tier"], "n": res["n_solutions"], "n_best": res["n_best"]}
    if res["analyses"]:
        a = res["analyses"][0]
        out["pattern"] = a["pattern"]
        out["licences"] = [(nm, pos, w) for nm, pos, ti, w in a["licences"]]
    return out


def run(lines, tier, learned=None, analogy=None, rules=None):
    rules = dict({"digamma": True, "accent_rules": True, "accent_hard": False, "disabled": frozenset()},
                 **(rules or {}))
    args = [(r["text"], tier, learned, analogy, rules) for r in lines]
    with Pool() as p:
        return p.map(run_config, args, chunksize=200)


def summary(res):
    n = len(res)
    c = collections.Counter(r["status"] for r in res)
    tied = sum(1 for r in res if r["status"] == "multiple" and r["n_best"] > 1)
    return {"lines": n, "unique": c["unique"], "multiple": c["multiple"], "fail": c["fail"],
            "unique_pct": 100 * c["unique"] / n, "multiple_pct": 100 * c["multiple"] / n,
            "fail_pct": 100 * c["fail"] / n, "tied_best": tied, "tied_best_pct": 100 * tied / n}


def cite(r):
    return f"{r['work']}. {r['book']}.{r['line']}"


MONRO = {
    "correption": "§380", "hiatus_long": "§380", "hiatus": "§§379, 382", "internal_correption": "§§381, 384",
    "muta_cum_liquida": "§370", "muta_cum_liquida_initial": "§370", "no_position_initial_cluster": "§370",
    "lengthening_liquid": "§§371-372", "lengthening_liquid_internal": "§§371-372",
    "lengthening_closed": "§375", "lengthening_hiatus": "§§375, 390 (ἰάχω)", "metrical_lengthening": "§§386-387",
    "synizesis": "§378", "synizesis_i": "§378", "synizesis_cross": "§378", "synizesis_rare": "§378",
    "synizesis_cross_rare": "§378", "digamma": "§§388-392", "digamma_double": "§§391, 394",
    "digamma_internal": "§394", "dichronon_contra": "§§383-384", "analogy_contra": "-",
    "accent_contra": "§§373, 375",
}


def fill_block(txt, name, lines):
    pat = re.compile(rf"<!-- BEGIN GENERATED: {re.escape(name)} -->.*?<!-- END GENERATED: {re.escape(name)} -->",
                     re.S)
    block = "\n".join([f"<!-- BEGIN GENERATED: {name} -->"] + lines + [f"<!-- END GENERATED: {name} -->"])
    return pat.sub(lambda m: block, txt)


def text_block(counts):
    out = ["| poem | books | lines | line numbers absent in the edition |", "|---|---|---|---|"]
    for wk in ("Il", "Od"):
        rows = [r for r in counts if r["work"] == wk and r["book"] != "ALL"]
        total = next(r["lines"] for r in counts if r["work"] == wk and r["book"] == "ALL")
        missing = "; ".join(f"{r['book']}.{r['missing_numbers'].replace(',', ', ')}" for r in rows
                            if r["missing_numbers"])
        out.append(f"| {wk} | {len(rows)} | {total} | {missing or '-'} |")
    lines = S.read_lines()
    br = [f"{l['work']}. {l['book']}.{l['line']}" for l in lines if l.get("bracketed") == "1"]
    out.append("")
    out.append(f"Lines marked `<del>` (bracketed) in the TEI: {', '.join(br) or 'none'}.")
    return out


def licence_block():
    counts = collections.Counter()
    forms = collections.defaultdict(list)
    with open(HERE / "licences.tsv", encoding="utf-8") as f:
        for r in csv.DictReader(f, delimiter="\t", quoting=csv.QUOTE_NONE, escapechar="\\"):
            counts[r["licence"]] += int(r["count"])
            if len(forms[r["licence"]]) < 3:
                forms[r["licence"]].append(f"{r['form']} ({r['citations'].split('; ')[0]})")
    def t(x):
        return "-" if x == 9 else str(x)
    out = ["| licence | tier princeps / biceps | cost p / b | description | Monro | instances in uniquely scanned lines | examples (word, first citation @ position) |",
           "|---|---|---|---|---|---|---|"]
    for nm, (tp, cp, tb, cb, desc) in S.LICENCES.items():
        cps = "-" if cp == float("inf") else f"{cp:g}"
        cbs = "-" if cb == float("inf") else f"{cb:g}"
        out.append(f"| `{nm}` | {t(tp)} / {t(tb)} | {cps} / {cbs} | {desc} | {MONRO.get(nm, '-')} | "
                   f"{counts.get(nm, 0)} | {'; '.join(forms.get(nm, [])) or '-'} |")
    return out


def lic_tier(nm, pos):
    """Tier of a licence instance: princeps (odd integer position) or biceps."""
    princeps = pos.isdigit() and int(pos) % 2 == 1
    return S.LICENCES[nm][0] if princeps else S.LICENCES[nm][2]


def primary_cause(res):
    """Classify a line by the highest-tier metrical licence its scansion uses.
    Preferences for attested α/ι/υ quantities (dichronon_contra,
    analogy_contra) are not causes: the core run ignores them."""
    if res["status"] == "fail":
        return "still unscannable (see failure notes)", []
    inst = [(nm, pos) for nm, pos, w in res.get("licences", [])
            if nm in CAUSE and nm not in ("dichronon_contra", "analogy_contra")]
    inst = [(nm, pos) for nm, pos in inst if lic_tier(nm, pos) >= 1 or nm == "accent_contra"]
    if not inst:
        return "α/ι/υ against its usual quantity (doubtful vowel, e.g. dative -ι long)", []
    best = max(inst, key=lambda x: (lic_tier(*x), S.LICENCES[x[0]][1] if lic_tier(*x) == S.LICENCES[x[0]][0]
                                     else S.LICENCES[x[0]][3]))
    return CAUSE[best[0]], [nm for nm, _ in inst]


def main():
    lines = S.read_lines()
    learned = S.load_learned()
    analogy = S.load_analogy()
    configs = {}
    configs["first version (v1)"] = run(lines, 2, rules={"accent_hard": True, "disabled": frozenset(
        {"synizesis_rare", "synizesis_cross_rare", "lengthening_liquid_internal", "digamma_internal"})})
    configs["core"] = run(lines, 0)
    configs["tier<=1"] = run(lines, 1)
    configs["pass 1"] = run(lines, 2)
    configs["final"] = run(lines, 2, learned, analogy)
    configs["final, no digamma list"] = run(lines, 2, learned, analogy, {"digamma": False})
    configs["final, accent rules off"] = run(lines, 2, learned, analogy, {"accent_rules": False})
    configs["final, accent rules hard"] = run(lines, 2, learned, analogy, {"accent_hard": True})
    summ = {k: summary(v) for k, v in configs.items()}
    final = configs["final"]

    # consistency with scansion.tsv
    scan_rows = list(csv.DictReader(open(HERE / "scansion.tsv", encoding="utf-8"), delimiter="\t",
                                    quoting=csv.QUOTE_NONE, escapechar="\\"))
    agree_tsv = sum(1 for r, f in zip(scan_rows, final) if r["pattern"] == f.get("pattern", ""))

    # failures of the core configuration: sample of 50, classified
    core_fail = [i for i, r in enumerate(configs["core"]) if r["status"] == "fail"]
    rng = random.Random(SEED)
    sample = sorted(rng.sample(core_fail, min(50, len(core_fail))))
    sample_rows = []
    sample_causes = collections.Counter()
    # classified with the final scansion (preferences for attested α/ι/υ quantities
    # make it the most accurate); lexical preferences themselves are not causes
    p1 = final
    for i in sample:
        cause, names = primary_cause(p1[i])
        sample_causes[cause] += 1
        sample_rows.append((cite(lines[i]), lines[i]["text"], p1[i].get("pattern", "-"), cause,
                            ", ".join(f"{nm}@{pos}({w})" for nm, pos, w in p1[i].get("licences", [])
                                      if nm in CAUSE)))
    all_causes = collections.Counter(primary_cause(p1[i])[0] for i in core_fail)

    # tier-1 / tier-2 failures
    t1_fail = [i for i, r in enumerate(configs["tier<=1"]) if r["status"] == "fail"]
    t1_causes = collections.Counter(primary_cause(p1[i])[0] for i in t1_fail)
    v1_fail = [cite(lines[i]) for i, r in enumerate(configs["first version (v1)"]) if r["status"] == "fail"]

    # final failures with notes
    notes = {r["citation"]: r for r in csv.DictReader(open(HERE / "failure_notes.tsv", encoding="utf-8"),
                                                       delimiter="\t")}
    final_fail = [i for i, r in enumerate(final) if r["status"] == "fail"]

    # manual checks
    man = list(csv.DictReader(open(HERE / "manual_checks.tsv", encoding="utf-8"), delimiter="\t"))
    pat = {cite(l): f.get("pattern", "FAIL") for l, f in zip(lines, final)}
    man_by_sample = collections.defaultdict(lambda: [0, 0, []])
    for m in man:
        s = man_by_sample[m["sample"]]
        s[0] += 1
        if pat.get(m["citation"]) == m["manual_pattern"]:
            s[1] += 1
        else:
            s[2].append((m["citation"], m["manual_pattern"], pat.get(m["citation"]), m["note"]))

    stats = json.loads((HERE / "validation_stats.json").read_text())
    counts = list(csv.DictReader(open(HERE / "line_counts.tsv", encoding="utf-8"), delimiter="\t"))
    n_il = next(int(r["lines"]) for r in counts if r["work"] == "Il" and r["book"] == "ALL")
    n_od = next(int(r["lines"]) for r in counts if r["work"] == "Od" and r["book"] == "ALL")
    pos = list(csv.DictReader(open(HERE / "positions.tsv", encoding="utf-8"), delimiter="\t"))
    rare = [p for p in pos if float(p["freq_lex"]) < 0.01]

    md = []
    w = md.append
    w("# Scanner validation\n")
    w("Generated by `python homer/validate.py`; do not edit by hand.\n")
    w(f"Text: {n_il} Iliad lines + {n_od} Odyssey lines = {n_il + n_od} lines (homer/lines.tsv).\n")
    w("## Definitions\n")
    w("* A **scansion** is an alignment of the verse's syllables (after any synizesis) to the hexameter "
      "template, with a quantity for every syllable.  Two scansions differ if the syllable division or any "
      "quantity differs (the final anceps is not counted).")
    w("* Licences are grouped in tiers (README).  For each line the scanner uses the lowest tier that yields "
      "any scansion (minimal-licence principle).  **unique** = exactly one scansion at that tier; "
      "**multiple** = more than one (the cheapest is reported, the others are listed in "
      "`alt_patterns`); **fail** = no scansion even with every licence.")
    w("* **tied best** = multiple scansions whose costs tie, so that the ranking does not decide.\n")
    w("## Headline figures (final configuration = homer/scansion.tsv)\n")
    f = summ["final"]
    w(f"| lines | unique | multiple | of which tied best | fail |\n|---|---|---|---|---|")
    w(f"| {f['lines']} | {f['unique']} ({f['unique_pct']:.2f}%) | {f['multiple']} ({f['multiple_pct']:.2f}%) | "
      f"{f['tied_best']} ({f['tied_best_pct']:.2f}%) | {f['fail']} ({f['fail_pct']:.2f}%) |\n")
    w(f"Rows of homer/scansion.tsv whose pattern agrees with this rerun: {agree_tsv} of {len(scan_rows)}.\n")
    w("By poem (final):\n")
    w("| poem | lines | unique | multiple | fail |\n|---|---|---|---|---|")
    for wk in ("Il", "Od"):
        idx = [i for i, l in enumerate(lines) if l["work"] == wk]
        c = collections.Counter(final[i]["status"] for i in idx)
        w(f"| {wk} | {len(idx)} | {c['unique']} ({100 * c['unique'] / len(idx):.2f}%) | "
          f"{c['multiple']} ({100 * c['multiple'] / len(idx):.2f}%) | {c['fail']} ({100 * c['fail'] / len(idx):.2f}%) |")
    w("")
    tiers = collections.Counter(r["tier"] for r in final if r["status"] != "fail")
    w(f"Lowest tier needed (final): tier 0 {tiers[0]}, tier 1 {tiers[1]}, tier 2 {tiers[2]} lines.\n")
    w("## Iterations and ablations\n")
    w("| configuration | unique | multiple | tied best | fail |\n|---|---|---|---|---|")
    for k, v in summ.items():
        w(f"| {k} | {v['unique_pct']:.2f}% | {v['multiple_pct']:.2f}% | {v['tied_best_pct']:.2f}% | "
          f"{v['fail']} ({v['fail_pct']:.2f}%) |")
    w("")
    w(f"Patterns changed between pass 1 and the final configuration: {stats['pattern_changed_pass1_to_pass2']} lines.\n")
    w(f"An emulation of the first version of the scanner (row v1: accent rules as hard constraints; no internal δϝ, no "
      f"rare or generic cross-word synizesis, no internal lengthening before liquids) failed {len(v1_fail)} "
      f"lines: {', '.join(v1_fail)}.  Examining them led to the rule changes recorded in the README "
      f"(accent rules made soft: βλοσυρῶπις, ἦνιν; ἔδεισα = ἔδδεισα; Πηλείδη ἔθελʼ; ἐλίσσετο; ἤιομεν).  "
      f"The other ablation rows show the effect of single components on the final rule set.\n")
    w(f"## Failure taxonomy: sample of 50 core (tier-0) failures\n")
    w(f"The core configuration fails {len(core_fail)} lines ({100 * len(core_fail) / len(lines):.2f}%).  "
      f"A sample of {len(sample)} (random seed {SEED}) is classified by the highest-tier metrical licence "
      f"used in the line's final scansion:\n")
    w("| cause | in sample | in all core failures |\n|---|---|---|")
    for cause, n in sorted(all_causes.items(), key=lambda x: -x[1]):
        w(f"| {cause} | {sample_causes.get(cause, 0)} | {n} |")
    w("")
    w("<details><summary>The 50 sampled lines</summary>\n")
    w("| citation | line | final pattern | cause | licences |\n|---|---|---|---|---|")
    for row in sample_rows:
        w("| " + " | ".join(x.replace("|", "/") for x in row) + " |")
    w("\n</details>\n")
    w(f"Lines that still fail with tiers 0-1 ({len(t1_fail)}), by the tier-2 licence they need:\n")
    w("| cause | lines |\n|---|---|")
    for cause, n in sorted(t1_causes.items(), key=lambda x: -x[1]):
        w(f"| {cause} | {n} |")
    w("")
    w(f"## Remaining failures ({len(final_fail)}), each explained\n")
    w("| citation | line | cause | explanation | evidence |\n|---|---|---|---|---|")
    for i in final_fail:
        c = cite(lines[i])
        n = notes.get(c, {})
        w(f"| {c} | {lines[i]['text']} | {n.get('cause', 'UNEXPLAINED')} | {n.get('explanation', '')} | "
          f"{n.get('evidence', '')} |")
    w("")
    w("## Manual checks\n")
    w("homer/manual_checks.tsv records scansions made by hand (by reasoning, not from the scanner's "
      "output) for seeded random samples of lines.  Sample A (50 lines, seed 20261007) was checked against "
      "an earlier state of the rules and led to one rule change (cost of `analogy_contra`), so it is "
      "in-sample; sample B (if present) was drawn after the rules were frozen.\n")
    w("| sample | lines | agree | disagreements |\n|---|---|---|---|")
    for smp, (n, ok, dis) in sorted(man_by_sample.items()):
        d = "; ".join(f"{c}: manual {m} vs scanner {s} ({note})" for c, m, s, note in dis) or "-"
        w(f"| {smp} | {n} | {ok} | {d} |")
    w("")
    w("## Internal consistency of α/ι/υ\n")
    d = stats["dichrona"]
    w(f"homer/dichrona.tsv: {d['forms_vowels']} (form, vowel) pairs fixed by {d['attestations']} unambiguous "
      f"attestations; {d['L']} long, {d['S']} short, {d['conflict']} with conflicting attestations "
      f"(minority attestations: {d['conflict_attestations_minority']}, "
      f"{100 * d['conflict_attestations_minority'] / d['attestations']:.2f}% of all).  Conflicts are mostly "
      "genuine Homeric doubtful vowels (Ἄρης, ἀνήρ, ὕδωρ, λίην, ἱερός, ἵκω) and homographs (δύω 'two' / "
      "'sink'; ἰῷ 'one' / 'arrow').\n")
    a = stats["analogy"]["leave_one_out"]
    w("Analogy predictor (quantity of a word-internal α/ι/υ from other forms beginning with the same letters "
      "up to the next vowel), leave-one-form-out:\n")
    w("| key | forms | predicted | coverage | accuracy |\n|---|---|---|---|---|")
    for k, v in a.items():
        w(f"| {k} | {v['forms']} | {v['predicted']} | {v['coverage_pct']}% | {v['accuracy_pct']}% |")
    w("")
    w("## Word-end baseline\n")
    w("Positions where Homer has (lexical) word end in fewer than 1% of the lines in which the position "
      "exists: " + ", ".join(f"{p['position']} ({100 * float(p['freq_lex']):.2f}%; orthographic "
                             f"{100 * float(p['freq_orth']):.2f}%)" for p in rare) + ".\n")
    (HERE / "validation.md").write_text("\n".join(md) + "\n", encoding="utf-8")

    # generated blocks in README
    readme = HERE / "README.md"
    if readme.exists():
        txt = readme.read_text(encoding="utf-8")
        txt = fill_block(txt, "text", text_block(counts))
        txt = fill_block(txt, "licences", licence_block())
        block = ["<!-- BEGIN GENERATED: validate.py -->",
                 f"Lines: Iliad {n_il}, Odyssey {n_od}, total {n_il + n_od}.",
                 "",
                 "| configuration | unique | multiple | fail |", "|---|---|---|---|"]
        for k in ("core", "tier<=1", "pass 1", "final"):
            v = summ[k]
            block.append(f"| {k} | {v['unique']} ({v['unique_pct']:.2f}%) | {v['multiple']} "
                         f"({v['multiple_pct']:.2f}%) | {v['fail']} ({v['fail_pct']:.2f}%) |")
        block.append("")
        block.append(f"Final: tied best scansions {summ['final']['tied_best']} ({summ['final']['tied_best_pct']:.2f}%). "
                     f"Manual checks: " + "; ".join(f"sample {s}: {ok}/{n} agree" for s, (n, ok, _) in
                                                    sorted(man_by_sample.items())) + ".")
        block.append("<!-- END GENERATED: validate.py -->")
        txt = re.sub(r"<!-- BEGIN GENERATED: validate.py -->.*?<!-- END GENERATED: validate.py -->",
                     "\n".join(block), txt, flags=re.S)
        readme.write_text(txt, encoding="utf-8")
    print(json.dumps({k: {kk: round(vv, 3) if isinstance(vv, float) else vv for kk, vv in v.items()}
                      for k, v in summ.items()}, indent=1, ensure_ascii=False))
    print("core failures:", len(core_fail), "final failures:", len(final_fail))


if __name__ == "__main__":
    main()
