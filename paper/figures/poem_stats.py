#!/usr/bin/env python3
"""Statistics of the poem's records for the paper's composition section.

Reads composition/final/poem.jsonl (one record per verse: sources, modifications, coinages, enjambment,
section, name_formula, commentary_equivalent) and review/poem_density_v4.json (the n-gram density of
the frozen text; the final text is byte-identical to draft v4 and this script re-checks it), and writes
paper/figures/results/poem_stats.json. The labels of the brief's §3 commentary systems are read from
composition/brief.md. Every number of the paper's poem section and of fig5_poem.py comes from this
file; nothing is entered by hand.

    source .venv/bin/activate && python -I paper/figures/poem_stats.py
"""
import json
import re
import sys as _sys
from collections import Counter, OrderedDict
from pathlib import Path as _Path

_sys.path.insert(0, str(_Path(__file__).resolve().parent))  # python -I does not add the script dir
from common import OUT, RES_P, REVIEW, ROOT  # noqa: E402

_sys.path.insert(0, str(ROOT / "homer"))
import greek as G  # noqa: E402  (the tokenizer and loose form of homer/concordance.py)

POEM = ROOT / "composition" / "final" / "poem.jsonl"
V4 = ROOT / "composition" / "drafts" / "v4.jsonl"
DENSITY = REVIEW / "poem_density_v4.json"
BRIEF = ROOT / "composition" / "brief.md"
OUT_JSON = RES_P / "poem_stats.json"

STATUSES = ["ATTESTED-EXACT", "ATTESTED-MODIFIED", "COINAGE"]
ENJ = ["none", "unperiodic", "necessary"]
PLAYERS = ["Federer", "Djokovic"]

# Morphological grouping of the coined forms (a judgement, not a number): inflected form -> (lemma, player).
# A form missing here is kept under its own lemma and flagged `ungrouped`.
COINED_LEMMA = {
    "Φεδερῆρος": ("Φεδερῆρος", "Federer"), "Φεδερῆρον": ("Φεδερῆρος", "Federer"),
    "Φεδερεύς": ("Φεδερεύς", "Federer"), "Φεδερεῦ": ("Φεδερεύς", "Federer"),
    "Ῥογῆρος": ("Ῥογῆρος", "Federer"),
    "Ἑλβέτιος": ("Ἑλβέτιος", "Federer"), "Ἑλβετίου": ("Ἑλβέτιος", "Federer"),
    "Σέρβος": ("Σέρβος", "Djokovic"), "Σέρβον": ("Σέρβος", "Djokovic"),
    "Σέρβου": ("Σέρβος", "Djokovic"), "Σέρβῳ": ("Σέρβος", "Djokovic"),
    "Ζοκοβείδης": ("Ζοκοβείδης", "Djokovic"),
    "Νοβῆκος": ("Νοβῆκος", "Djokovic"), "Νοβήκου": ("Νοβῆκος", "Djokovic"),
    # coined forms of attested words (not names)
    "δαΐφρονε": ("δαΐφρων", None), "πυμάτῃ": ("πύματος", None),
    "δάμασεν": ("δαμάζω", None), "παρέλασσε": ("παρελαύνω", None),
}

# The six definitions of review/poem_density.py, in its order, with labels for the table and the figure.
DEFS = OrderedDict([
    ("n2_all_min1", dict(n_min=2, filter="all n-grams", homer_min=1,
                         label="n ≥ 2, all n-grams, attested ≥ 1× in Homer",
                         short="n ≥ 2\nall n-grams\nHomer ≥ 1×")),
    ("n2_base_min1", dict(n_min=2, filter="not function-word-only", homer_min=1,
                          label="n ≥ 2, not function-word-only, attested ≥ 1× in Homer",
                          short="n ≥ 2\nnot function-only\nHomer ≥ 1×")),
    ("n3_all_min1", dict(n_min=3, filter="all n-grams", homer_min=1,
                         label="n ≥ 3, all n-grams, attested ≥ 1× in Homer",
                         short="n ≥ 3\nall n-grams\nHomer ≥ 1×")),
    ("n3_base_min1", dict(n_min=3, filter="not function-word-only", homer_min=1,
                          label="n ≥ 3, not function-word-only, attested ≥ 1× in Homer",
                          short="n ≥ 3\nnot function-only\nHomer ≥ 1×")),
    ("n2_base_min2", dict(n_min=2, filter="not function-word-only", homer_min=2,
                          label="n ≥ 2, not function-word-only, attested ≥ 2× in Homer",
                          short="n ≥ 2\nnot function-only\nHomer ≥ 2×")),
    ("n3_base_min2", dict(n_min=3, filter="not function-word-only", homer_min=2,
                          label="n ≥ 3, not function-word-only, attested ≥ 2× in Homer",
                          short="n ≥ 3\nnot function-only\nHomer ≥ 2×")),
])

CIT_RE = re.compile(r"(?:Il|Od)\. \d+\.\d+(?:[-–]\d+)?")
# a brief §3 reference "3.N" (N = 1 … 10) that is not the second part of a Homeric citation (Il. 3.303,
# Il. 23.499) and not a decimal inside a longer number
SEC3_RE = re.compile(r"(?<![\d.])(?<!Il\. )(?<!Od\. )3\.(10|[1-9])(?![\d.])")
SEC3_RANGE_RE = re.compile(r"(?<![\d.])3\.([1-9])-3\.(10|[1-9])(?![\d.])")


def load_jsonl(path):
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def loose_tokens(text):
    return [G.loose(t.core) for t in G.tokenize(G.nfc(text))]


def first_word(form):
    """The bare form in a `coinages[].form` entry such as 'Σέρβος (at 9-9.5)' or 'Νοβήκου (gen.)'."""
    return G.nfc(form.split(" (")[0].split()[0])


def brief_section3():
    """Labels of the brief's §3 systems: {'3.1': {'commentary': ..., 'homeric_equivalent': ...}, ...}."""
    text = BRIEF.read_text(encoding="utf-8")
    sec = text.split("\n## 3. ", 1)[1].split("\n## 4. ", 1)[0]
    out = {}
    for m in re.finditer(r"^\*\*(3\.\d+) (.+?)\*\* — (.*)$", sec, flags=re.M):
        num, label, rest = m.group(1), m.group(2), m.group(3)
        hom = None
        if "↔" in rest:
            after = rest.split("↔", 1)[1].strip()
            b = re.match(r"\*\*(.+?)\*\*", after)
            hom = b.group(1) if b else re.split(r" \(|:|;", after, maxsplit=1)[0].strip().strip("`")
        out[num] = {"commentary": label.replace("`", ""), "homeric_equivalent": hom}
    return out


def parse_name_formula(s):
    """'Federer: X (desc); Djokovic: Y (desc)' -> [(player, formula, desc)]."""
    parts = re.split(r"(?:^|; )(Federer|Djokovic): ", s)
    # re.split yields ['', 'Federer', 'X (desc)', 'Djokovic', 'Y (desc)']
    assert parts[0] == "", s
    out = []
    for player, body in zip(parts[1::2], parts[2::2]):
        body = body.strip()
        if " (" in body:
            formula, desc = body.split(" (", 1)
            desc = desc.rstrip()
            desc = desc[:-1] if desc.endswith(")") else desc
        else:
            formula, desc = body, ""
        out.append((player, G.nfc(formula.strip()), desc))
    return out


SHAPE_NUM_RE = re.compile(r"shape (\d)")
METRE_RE = re.compile(r"(?<![A-Za-z])((?:[LSX]{2,})(?: \+ [LSX]{2,})*)(?![A-Za-z])")
POS_RE = re.compile(r"\bat (\d+(?:\.5)?-\d+(?:\.5)?(?: \+ \d+(?:\.5)?-\d+(?:\.5)?)?)")
POS_FALLBACK_RE = re.compile(r"(?<![\d.])(\d+(?:\.5)?-\d+(?:\.5)?)(?![\d.])")


def main():
    recs = load_jsonl(POEM)
    dens = json.loads(DENSITY.read_text(encoding="utf-8"))
    n_lines = len(recs)
    assert [r["n"] for r in recs] == list(range(1, n_lines + 1)), "records must be numbered 1..N"
    assert dens["verses"] == n_lines, (dens["verses"], n_lines)

    # the density file was computed on draft v4; the final text must be identical, line for line
    v4_identical = None
    if V4.exists():
        v4 = load_jsonl(V4)
        v4_identical = [G.nfc(r["text"]) for r in v4] == [G.nfc(r["text"]) for r in recs]
        assert v4_identical, "composition/final/poem.jsonl text differs from drafts/v4.jsonl: rerun poem_density"

    out = OrderedDict()
    out["inputs"] = {
        "poem": str(POEM.relative_to(ROOT)),
        "density": str(DENSITY.relative_to(ROOT)),
        "density_input": dens["input"],
        "density_input_text_identical_to_final_poem": v4_identical,
        "brief": str(BRIEF.relative_to(ROOT)),
    }
    out["n_lines"] = n_lines
    out["n_tokens"] = dens["tokens"]

    # ---------------------------------------------------------------- source entries by status
    status = Counter(s["status"] for r in recs for s in r["sources"])
    unknown = set(status) - set(STATUSES)
    assert not unknown, f"unexpected source status {unknown}"
    per_line = [len(r["sources"]) for r in recs]
    lines_with = {st: sum(1 for r in recs if any(s["status"] == st for s in r["sources"])) for st in STATUSES}
    out["source_entries"] = {
        "total": sum(status.values()),
        "by_status": {st: status.get(st, 0) for st in STATUSES},
        "share_by_status_pct": {st: round(100.0 * status.get(st, 0) / sum(status.values()), 1) for st in STATUSES},
        "entries_per_line": {"mean": round(sum(per_line) / n_lines, 2), "min": min(per_line), "max": max(per_line)},
        "lines_with_at_least_one": lines_with,
        "note": "COINAGE entries are coined names set into an attested slot shown by the cited model line; "
                "review/provenance_final.md counts them with ATTESTED-MODIFIED.",
    }

    # ---------------------------------------------------------------- modification kinds
    mods = OrderedDict()
    for r in recs:
        for m in r.get("modifications", []):
            k = m["kind"]
            cit = CIT_RE.search(m["homeric_parallel"])
            ex = {"line": r["n"], "citation": cit.group(0) if cit else None, "homeric_parallel": m["homeric_parallel"]}
            if k not in mods:
                mods[k] = {"count": 0, "lines": [], "example": ex}
            elif mods[k]["example"]["citation"] is None and cit:
                mods[k]["example"] = ex  # the first instance of the kind whose parallel cites a Homeric line
            mods[k]["count"] += 1
            mods[k]["lines"].append(r["n"])
    mods = OrderedDict(sorted(mods.items(), key=lambda kv: -kv[1]["count"]))
    out["modifications"] = {
        "total": sum(v["count"] for v in mods.values()),
        "lines_with_a_modification": sum(1 for r in recs if r.get("modifications")),
        "by_kind": mods,
    }

    # ---------------------------------------------------------------- coined forms
    tok_lines = {r["n"]: loose_tokens(r["text"]) for r in recs}
    coined = OrderedDict()
    for r in recs:
        for c in r.get("coinages", []):
            form = first_word(c["form"])
            lemma, player = COINED_LEMMA.get(form, (form, None))
            e = coined.setdefault(lemma, {"player": player, "forms": OrderedDict(), "coinage_entries": 0,
                                         "text_occurrences": 0, "lines": [], "ungrouped": form not in COINED_LEMMA})
            f = e["forms"].setdefault(form, {"loose": G.loose(form), "coinage_entries": 0, "coinage_lines": [],
                                             "text_occurrences": 0, "text_lines": [],
                                             "analogical_model": c["analogical_model"]})
            f["coinage_entries"] += 1
            f["coinage_lines"].append(r["n"])
            e["coinage_entries"] += 1
    for lemma, e in coined.items():
        for form, f in e["forms"].items():
            hits = [(n, toks.count(f["loose"])) for n, toks in tok_lines.items() if f["loose"] in toks]
            f["text_occurrences"] = sum(c for _, c in hits)
            f["text_lines"] = [n for n, _ in hits]
            f["coinage_entries_equal_text_occurrences"] = f["text_occurrences"] == f["coinage_entries"]
        e["text_occurrences"] = sum(f["text_occurrences"] for f in e["forms"].values())
        e["lines"] = sorted({n for f in e["forms"].values() for n in f["text_lines"]})
    by_player = {p: OrderedDict((l, e) for l, e in coined.items() if e["player"] == p) for p in PLAYERS}
    others = OrderedDict((l, e) for l, e in coined.items() if e["player"] is None)
    loose_coined = {f["loose"] for e in coined.values() for f in e["forms"].values()}
    unatt = set(dens["unattested_forms"])
    out["coined_forms"] = {
        "distinct_forms": sum(len(e["forms"]) for e in coined.values()),
        "distinct_lemmata": len(coined),
        "coinage_entries": sum(e["coinage_entries"] for e in coined.values()),
        "text_occurrences": sum(e["text_occurrences"] for e in coined.values()),
        "name_forms_per_player": {
            p: {"lemmata": len(by_player[p]), "forms": sum(len(e["forms"]) for e in by_player[p].values()),
                "text_occurrences": sum(e["text_occurrences"] for e in by_player[p].values()),
                "lines": sorted({n for e in by_player[p].values() for n in e["lines"]})}
            for p in PLAYERS},
        "by_name": OrderedDict(list(by_player["Federer"].items()) + list(by_player["Djokovic"].items())),
        "other_coined_forms": others,
        "cross_check_with_density_unattested_forms": {
            "density_unattested_forms": sorted(unatt),
            "coined_loose_forms": sorted(loose_coined),
            "coined_but_loosely_attested_in_homer": sorted(loose_coined - unatt),
            "unattested_but_not_listed_as_coinage": sorted(unatt - loose_coined),
        },
        "note": "text_occurrences counts tokens of the verse text in the loose form of homer/concordance.py "
                "(accents, breathings, subscripts and case ignored); coinage_entries counts the records' "
                "`coinages` entries.",
    }

    # ---------------------------------------------------------------- verbatim Homeric lines
    verb_nums = list(dens["verbatim_verse_numbers"])
    assert len(verb_nums) == dens["verses_identical_to_a_homeric_verse"]
    verbatim = []
    for n in verb_nums:
        r = recs[n - 1]
        whole = [s for s in r["sources"] if s["position"] == "1-12" and s["status"] == "ATTESTED-EXACT"]
        verbatim.append({"n": n, "text": r["text"], "section": r["section"],
                         "citation": whole[0]["citation"] if whole else None,
                         "homeric_occurrences": whole[0]["count"] if whole else None})
    out["verbatim_homeric_lines"] = {
        "count": len(verb_nums), "share_pct": round(100.0 * len(verb_nums) / n_lines, 1),
        "lines": verb_nums, "all_have_whole_line_exact_source": all(v["citation"] for v in verbatim),
        "repeated_in_homer": sum(1 for v in verbatim if (v["homeric_occurrences"] or 0) >= 2),
        "detail": verbatim,
        "definition": "the verse's loose token sequence equals that of a Homeric verse (review/poem_density.py)",
    }

    # ---------------------------------------------------------------- enjambment
    enj = Counter(r["enjambment"] for r in recs)
    assert set(enj) <= set(ENJ), set(enj)
    out["enjambment"] = {
        "counts": {k: enj.get(k, 0) for k in ENJ},
        "share_pct": {k: round(100.0 * enj.get(k, 0) / n_lines, 1) for k in ENJ},
        "enjambed_pct": round(100.0 * (enj.get("unperiodic", 0) + enj.get("necessary", 0)) / n_lines, 1),
        "lines": {k: [r["n"] for r in recs if r["enjambment"] == k] for k in ENJ},
        "denominator": n_lines,
        "note": "Parry's three classes; the last verse of the poem is counted as the record labels it",
    }

    # ---------------------------------------------------------------- lines per plan section
    sections = OrderedDict()
    for r in recs:
        sections.setdefault(r["section"], []).append(r["n"])
    out["sections"] = {
        "count": len(sections),
        "lines_per_section": OrderedDict((s, {"n_lines": len(v), "first": v[0], "last": v[-1],
                                              "contiguous": v == list(range(v[0], v[-1] + 1))})
                                         for s, v in sections.items()),
    }

    # ---------------------------------------------------------------- brief §3 commentary systems realised
    labels3 = brief_section3()
    sys3 = OrderedDict((f"3.{i}", {"commentary_system": labels3.get(f"3.{i}", {}).get("commentary"),
                                   "homeric_equivalent": labels3.get(f"3.{i}", {}).get("homeric_equivalent"),
                                   "lines": []}) for i in range(1, 11))
    no_ce, non3 = [], []
    for r in recs:
        ce = r.get("commentary_equivalent")
        if not ce:
            no_ce.append(r["n"])
            continue
        found = set()
        for m in SEC3_RANGE_RE.finditer(ce):
            found.update(range(int(m.group(1)), int(m.group(2)) + 1))
        for m in SEC3_RE.finditer(ce):
            found.add(int(m.group(1)))
        if not found:
            non3.append({"line": r["n"], "commentary_equivalent": ce})
        for i in sorted(found):
            sys3[f"3.{i}"]["lines"].append(r["n"])
    for v in sys3.values():
        v["n_lines"] = len(v["lines"])
        v["realised"] = bool(v["lines"])
    out["commentary_systems"] = {
        "systems_in_brief": 10,
        "realised": sum(1 for v in sys3.values() if v["realised"]),
        "lines_with_commentary_equivalent": n_lines - len(no_ce),
        "lines_without_commentary_equivalent": no_ce,
        "lines_referring_only_outside_section_3": non3,
        "by_system": sys3,
        "note": "a line counts for every §3 system its commentary_equivalent field cites (3.N; a range 3.a-3.b counts a…b)",
    }

    # ---------------------------------------------------------------- name-epithet formulae
    nf = {p: OrderedDict() for p in PLAYERS}
    lines_with_nf = {p: [] for p in PLAYERS}
    for r in recs:
        s = r.get("name_formula")
        if not s:
            continue
        for player, formula, desc in parse_name_formula(s):
            sn = SHAPE_NUM_RE.search(desc)
            mt = METRE_RE.search(desc)
            ps = POS_RE.search(desc) or POS_FALLBACK_RE.search(desc)
            use = {"line": r["n"], "shape_number": int(sn.group(1)) if sn else None,
                   "metrical_shape": mt.group(1) if mt else None, "position": ps.group(1) if ps else None,
                   "description": desc}
            e = nf[player].setdefault(formula, {"uses": 0, "lines": [], "shape_numbers": [], "metrical_shapes": [],
                                                "positions": [], "detail": []})
            e["uses"] += 1
            e["lines"].append(r["n"])
            e["detail"].append(use)
            lines_with_nf[player].append(r["n"])
    for p in PLAYERS:
        for e in nf[p].values():
            e["shape_numbers"] = sorted({u["shape_number"] for u in e["detail"] if u["shape_number"] is not None})
            e["metrical_shapes"] = sorted({u["metrical_shape"] for u in e["detail"] if u["metrical_shape"]})
            e["positions"] = sorted({u["position"] for u in e["detail"] if u["position"]},
                                    key=lambda x: float(x.split("-")[0]))
        nf[p] = OrderedDict(sorted(nf[p].items(), key=lambda kv: (-kv[1]["uses"], kv[1]["lines"][0])))
    by_shape = {p: {str(k): sorted(u["line"] for e in nf[p].values() for u in e["detail"] if u["shape_number"] == k)
                    for k in (1, 2, 3, None)} for p in PLAYERS}
    out["name_epithet_formulae"] = {
        "lines_with_name_formula": sum(1 for r in recs if r.get("name_formula")),
        "per_player": {p: {"lines": sorted(set(lines_with_nf[p])), "n_lines": len(set(lines_with_nf[p])),
                           "distinct_formulae": len(nf[p]),
                           "lines_by_brief_shape": by_shape[p],
                           "all_three_shapes_used": all(by_shape[p][str(k)] for k in (1, 2, 3)),
                           "formulae": nf[p]} for p in PLAYERS},
        "note": "shape numbers 1-3 are the brief's §4.3 economical systems (1 line-end SSLX/SSLL, 2 line-initial "
                "LSSL/LX, 3 mid-line SLX); 'None' = a slot allowed by addendum A1 or a declined form outside the "
                "three shapes; metrical shape and position are those stated in the record's name_formula field",
    }

    # ---------------------------------------------------------------- density table
    table = OrderedDict()
    for key, meta in DEFS.items():
        c = dens["coverage"][key]
        table[key] = OrderedDict([
            ("label", meta["label"]), ("short_label", meta["short"]),
            ("n_min", meta["n_min"]), ("filter", meta["filter"]), ("homer_min", meta["homer_min"]),
            ("coverage_pct", c["coverage"]), ("ci95", c["ci95"]),
            ("excluding_verbatim_pct", c["excluding_verbatim_verses"]["coverage"]),
            ("excluding_verbatim_ci95", c["excluding_verbatim_verses"]["ci95"]),
            ("excluding_verbatim_verses", c["excluding_verbatim_verses"]["verses"]),
            ("excluding_verbatim_tokens", c["excluding_verbatim_verses"]["tokens"]),
            ("excluding_tokens_unattested_in_homer_pct", c["excluding_tokens_unattested_in_homer"]),
            ("homeric_reference_pct", dens["homeric_reference_verse_vs_rest_of_homer"][key]),
            ("shuffled_mean_pct", c["shuffled_mean"]), ("shuffled_2.5_97.5", c["shuffled_2.5_97.5"]),
            ("excess_over_shuffled_pp", c["excess_pp"]),
            ("excess_over_homeric_reference_pp", round(c["coverage"] - dens["homeric_reference_verse_vs_rest_of_homer"][key], 1)),
        ])
    assert set(table) == set(dens["coverage"]), "definitions of the density file changed"
    out["density"] = {
        "verses": dens["verses"], "tokens": dens["tokens"],
        "verbatim_verses": dens["verses_identical_to_a_homeric_verse"],
        "tokens_unattested_in_homer": dens["tokens_unattested_in_homer"],
        "bootstrap_B": dens["B"], "shuffles_R": dens["R"], "function_words": dens["func_words"],
        "homeric_reference_note": dens["homeric_reference_note"],
        "lines_with_exact_formula_ge2_words_pct": dens["lines_with_claimed_exact_formula_ge2_words_pct"],
        "lines_with_exact_formula_ge2_words": dens["lines_with_claimed_exact_formula_ge2_words"],
        "lines_with_exact_formula_ge2_words_not_function_only_pct": dens["lines_with_claimed_exact_formula_ge2_words_not_function_only_pct"],
        "lines_without_exact_formula_ge2_words_not_function_only": dens["lines_without_claimed_exact_formula_ge2_words_not_function_only"],
        "lines_with_any_attested_ngram_at_homeric_position_pct": dens["lines_with_any_attested_ngram_at_homeric_position_pct"],
        "lines_without_any_attested_ngram_at_homeric_position": dens["lines_without_any_attested_ngram_at_homeric_position"],
        "lines_with_an_attested_exact_source_entry_pct": round(100.0 * lines_with["ATTESTED-EXACT"] / n_lines, 1),
        "definitions": table,
    }

    RES_P.mkdir(exist_ok=True)
    OUT_JSON.write_text(json.dumps(out, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(f"wrote {OUT_JSON.relative_to(OUT)}")
    print("source entries:", dict(out["source_entries"]["by_status"]), "total", out["source_entries"]["total"])
    print("modification kinds:", {k: v["count"] for k, v in mods.items()})
    print("coined forms:", out["coined_forms"]["distinct_forms"], "forms,", out["coined_forms"]["coinage_entries"],
          "entries,", out["coined_forms"]["text_occurrences"], "text occurrences")
    print("verbatim Homeric lines:", out["verbatim_homeric_lines"]["count"])
    print("enjambment:", out["enjambment"]["counts"], out["enjambment"]["share_pct"])
    print("sections:", {s: v["n_lines"] for s, v in out["sections"]["lines_per_section"].items()})
    print("§3 systems realised:", out["commentary_systems"]["realised"], "of 10;",
          {k: v["n_lines"] for k, v in sys3.items()})
    for p in PLAYERS:
        print(f"{p}: {out['name_epithet_formulae']['per_player'][p]['n_lines']} lines, "
              f"{len(nf[p])} formulae, shapes {by_shape[p]}")


if __name__ == "__main__":
    main()
