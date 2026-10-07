#!/usr/bin/env python3
"""Check a newly composed hexameter against Homeric practice.

    python homer/check_line.py "ὣς ἔφατʼ, οὐδʼ ἀπίθησε θεὰ γλαυκῶπις Ἀθήνη"
    python homer/check_line.py --file composition/drafts/v1.txt [--json]

For each verse the script scans it with homer/scan.py (same rules and the same
learned α/ι/υ quantities as the corpus scan) and reports the scansion.  It
FLAGS:
  * unmetrical          no hexameter scansion under the licences of scan.py
  * rare_word_end       a word end at a metrical position where Homer has word
                        end in < 1% of the lines in which that position exists
                        (homer/positions.tsv; lexical word ends, i.e. with
                        appositives joined to their host, by default).
                        Hermann's bridge (7.5) falls out of this.
  * licence_unattested  a licence (correption, synizesis, lengthening, hiatus,
                        digamma effect, muta cum liquida ...) used for a word
                        form that Homer never uses it with (homer/licences.tsv,
                        built from the lines with a unique scansion)
  * quantity_contrary   an α/ι/υ given a quantity contrary to its unambiguous
                        Homeric attestations (homer/dichrona.tsv)
  * elision_before_digamma
                        a word elided before a vowel-initial word that had a
                        digamma (homer/digamma.tsv, or the pronoun οἱ ἑ ἕο ἑοῖ
                        ἕθεν) where Homer never elides that word (loose form)
                        before that form (homer/elision_digamma.tsv, built by
                        homer/elision_digamma.py); the flag gives the elided and
                        unelided Homeric counts of the pair and the concordance
                        regexes that reproduce them
It WARNS (no effect on the exit code unless --strict) about α/ι/υ whose
quantity is not attested for that form, tied alternative scansions, and
caesura anomalies.

Exit code: 0 if every verse scans with no flags, 1 otherwise.
"""
import argparse
import csv
import json
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import elision_digamma as E  # noqa: E402
import greek as G  # noqa: E402
import scan as S  # noqa: E402

THRESHOLD = 0.01
# licences that are not lexical choices (the text itself determines them) or
# that are recorded on another table
NOT_CHECKED = {"dichronon_contra", "analogy_contra", "accent_contra"}


def load_positions(path=HERE / "positions.tsv"):
    out = {}
    with open(path, encoding="utf-8") as f:
        for r in csv.DictReader(f, delimiter="\t"):
            out[r["position"]] = {"orth": float(r["freq_orth"]), "lex": float(r["freq_lex"]),
                                  "n": int(r["lines_with_position"])}
    return out


def load_licences(path=HERE / "licences.tsv"):
    exact, loose = {}, {}
    with open(path, encoding="utf-8") as f:
        for r in csv.DictReader(f, delimiter="\t", quoting=csv.QUOTE_NONE, escapechar="\\"):
            exact[(r["licence"], r["form"])] = (int(r["count"]), r["citations"].split("; ")[:3])
            k = (r["licence"], r["loose"])
            c = loose.get(k, (0, []))
            loose[k] = (c[0] + int(r["count"]), c[1] or r["citations"].split("; ")[:3])
    return exact, loose


def load_dichrona(path=HERE / "dichrona.tsv"):
    out = {}
    with open(path, encoding="utf-8") as f:
        for r in csv.DictReader(f, delimiter="\t", quoting=csv.QUOTE_NONE, escapechar="\\"):
            out[(r["form"], int(r["vowel_no"]))] = r
    return out


class Checker:
    def __init__(self, tier="lex"):
        self.positions = load_positions()
        self.lic_exact, self.lic_loose = load_licences()
        self.dichrona = load_dichrona()
        self.learned = S.load_learned()
        self.analogy = S.load_analogy()
        self.elision = E.Index()
        self.tier = tier

    def elision_check(self, text, word_positions=None):
        """Elided words before digamma-initial words: (flags, parallels)."""
        flags, parallels = [], []
        toks = G.tokenize(G.nfc(text))
        for i in range(len(toks) - 1):
            if not toks[i].elided:
                continue
            h = self.elision.check_pair(toks[i].core, toks[i + 1].core)
            if h is None:
                continue
            if word_positions and len(word_positions) == len(toks):
                h["position"] = word_positions[i + 1].split("-")[0]
            if h["n_elided"]:
                parallels.append(h)
                continue
            kept = (f"{h['n_unelided']} with the vowel kept ({h['unelided_spellings']} {h['next_form']}: "
                    f"{', '.join(h['citations_unelided'][:3])})") if h["n_unelided"] else "0 with the vowel kept"
            h["type"] = "elision_before_digamma"
            h["detail"] = (f"'{h['word']}' elided before '{h['next_word']}' (ϝ: {h['lemma']}): Homer never elides "
                           f"'{h['key']}' before '{h['next_form']}': 0 elided, {kept}; '{h['key']}' elided before "
                           f"other words of this digamma entry {h['n_elided_word_before_entry']}x; any word elided "
                           f"before '{h['next_form']}' {h['n_any_elided_before_next']}x")
            flags.append(h)
        return flags, parallels

    def check(self, verse):
        res = S.scan(verse, learned=self.learned, analogy=self.analogy)
        out = {"verse": res["text"], "status": res["status"], "tier": res["tier"],
               "n_scansions": res["n_solutions"], "flags": [], "warnings": []}
        if res["status"] == "fail":
            out["flags"].append({"type": "unmetrical", "detail": "no hexameter scansion found"})
            el_flags, el_par = self.elision_check(verse)
            out["flags"].extend(el_flags)
            if el_par:
                out["elision_parallels"] = el_par
            return out
        a = res["analyses"][0]
        sc = res["solutions"][0]
        line = res["line"]
        out["scansion"] = {
            "pattern": a["pattern"], "syllables": " ".join(a["syllables"]),
            "positions": " ".join(a["positions"]), "quantities": a["quantities"],
            "word_quantities": " ".join(a["word_meter"]), "word_positions": " ".join(a["word_positions"]),
            "caesurae": a["caesurae"], "bucolic_diaeresis": a["bucolic"],
            "wordend_lex": a["wordend_lex"], "wordend_orth": a["wordend_orth"],
            "licences": S.fmt_lic(a["licences"]), "cost": a["cost"]}
        if res["n_best"] > 1 or len(res["analyses"]) > 1:
            out["warnings"].append({"type": "alternative_scansions",
                                    "detail": [f"{b['pattern']} (cost {b['cost']}; {S.fmt_lic(b['licences'])})"
                                               for b in res["analyses"][1:6]]})
        for an in a["anomalies"]:
            if an not in S.FEATURES:
                out["warnings"].append({"type": "anomaly", "detail": an})
        # 1. word ends at rare positions
        ends = a["wordend_lex"] if self.tier == "lex" else a["wordend_orth"]
        for p in ends:
            f = self.positions.get(p)
            if f and f[self.tier] < THRESHOLD:
                out["flags"].append({"type": "rare_word_end", "position": p,
                                     "homeric_freq_lex": f["lex"], "homeric_freq_orth": f["orth"],
                                     "detail": f"word end at {p}: Homer {100 * f[self.tier]:.2f}% "
                                               f"({'lexical' if self.tier == 'lex' else 'orthographic'})"})
        # 2. licences not attested for the word
        for nm, pos, ti, w in a["licences"]:
            if nm in NOT_CHECKED or ti is None:
                continue
            fk = G.form_key(w)
            hit = self.lic_exact.get((nm, fk)) or self.lic_loose.get((nm, G.loose(w)))
            if not hit:
                out["flags"].append({"type": "licence_unattested", "licence": nm, "word": w, "position": pos,
                                     "detail": f"{nm} on/before '{w}' at {pos} is not attested for this form "
                                               f"in Homer ({S.LICENCES[nm][4]})"})
            else:
                out.setdefault("licence_parallels", []).append(
                    {"licence": nm, "word": w, "position": pos, "homeric_count": hit[0], "examples": hit[1]})
        for nm, pos, ti, w in a["licences"]:
            if nm in ("dichronon_contra", "analogy_contra", "accent_contra"):
                out["flags"].append({"type": "quantity_contrary", "licence": nm, "word": w, "position": pos,
                                     "detail": f"α/ι/υ in '{w}' at {pos}: {S.LICENCES[nm][4]}"})
        # 3. elision before a digamma-initial word that Homer never elides
        el_flags, el_par = self.elision_check(verse, a["word_positions"])
        out["flags"].extend(el_flags)
        if el_par:
            out["elision_parallels"] = el_par
        # 4. dichrona: attested or not
        nucs = line.nuclei
        for k, (span, q, state, lic) in enumerate(sc.syls):
            if span[0] != span[1] or q == "X":
                continue
            n = nucs[span[0]]
            if n.cls != "D":
                continue
            ccl = S.ccount(line.after[span[0]])
            if q == "L" and ccl >= 2:
                continue  # long by position: vowel quantity irrelevant
            w = line.tokens[n.tok].core
            fk = G.form_key(w)
            row = self.dichrona.get((fk, n.widx + 1))
            if row is None:
                src = "analogy" if span[0] in line.analogy else (
                    "accent" if span[0] in line.fixed else "metre only")
                out["warnings"].append({"type": "quantity_unattested", "word": w, "vowel": n.text,
                                        "vowel_no": n.widx + 1, "quantity": q, "position": a["positions"][k],
                                        "detail": f"{n.text} in '{w}' taken as {q} ({src}); no unambiguous "
                                                  f"Homeric attestation of this form"})
            elif row["quantity"] in ("L", "S") and row["quantity"] != q and \
                    not any(nm.endswith("_contra") for nm, _ in lic):
                out["flags"].append({"type": "quantity_contrary", "word": w, "vowel": n.text,
                                     "detail": f"{n.text} in '{w}' scanned {q}, Homer has {row['quantity']} "
                                               f"({row['citations_long' if row['quantity'] == 'L' else 'citations_short'][:60]})"})
        return out


def render(o):
    lines = [o["verse"]]
    if o["status"] == "fail":
        lines.append("  UNMETRICAL: no hexameter scansion found")
    else:
        s = o["scansion"]
        lines.append(f"  {s['pattern']}  ({o['status']}, tier {o['tier']}, {o['n_scansions']} scansion(s))")
        lines.append(f"  syllables: {s['syllables']}")
        lines.append(f"  positions: {s['positions']}")
        lines.append(f"  quantities by word: {s['word_quantities']}")
        lines.append(f"  caesurae: {', '.join(s['caesurae']) or '-'}; bucolic diaeresis: {s['bucolic_diaeresis'] or '-'}")
        lines.append(f"  licences: {s['licences'] or '-'}")
        for p in o.get("licence_parallels", []):
            lines.append(f"    {p['licence']} '{p['word']}': {p['homeric_count']}x in Homer, e.g. {', '.join(p['examples'])}")
    for p in o.get("elision_parallels", []):
        lines.append(f"  elision before digamma word '{p['word']} {p['next_word']}': elided {p['n_elided']}x in Homer "
                     f"({', '.join(p['citations_elided'][:3])}), vowel kept {p['n_unelided']}x")
    for f in o["flags"]:
        lines.append(f"  FLAG {f['type']}: {f['detail']}")
        if f["type"] == "elision_before_digamma":
            lines.append(f"    reproduce: python homer/concordance.py --regex '{f['query_elided']}' --count")
            lines.append(f"               python homer/concordance.py --regex '{f['query_unelided']}' --count")
    for w in o["warnings"]:
        d = w["detail"] if isinstance(w["detail"], str) else "; ".join(w["detail"])
        lines.append(f"  warn {w['type']}: {d}")
    if not o["flags"]:
        lines.append("  OK (no flags)")
    return "\n".join(lines)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("verse", nargs="*")
    ap.add_argument("--file")
    ap.add_argument("--json", action="store_true", help="print a JSON summary")
    ap.add_argument("--tier", choices=["lex", "orth"], default="lex",
                    help="word-end tier for the <1%% test (default: lexical)")
    ap.add_argument("--strict", action="store_true", help="warnings also make the exit code 1")
    a = ap.parse_args()
    if a.file:
        verses = [l.strip() for l in open(a.file, encoding="utf-8") if l.strip()]
    elif a.verse:
        verses = [" ".join(a.verse)]
    else:
        verses = [l.strip() for l in sys.stdin if l.strip()]
    ck = Checker(tier=a.tier)
    results = [ck.check(v) for v in verses]
    bad = any(r["flags"] or (a.strict and r["warnings"]) for r in results)
    if a.json:
        summary = {"n_verses": len(results), "n_flagged": sum(1 for r in results if r["flags"]),
                   "n_unmetrical": sum(1 for r in results if r["status"] == "fail"), "verses": results}
        print(json.dumps(summary, ensure_ascii=False, indent=1))
    else:
        for i, r in enumerate(results, 1):
            print(f"[{i}] " + render(r))
            print()
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
