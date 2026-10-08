"""2b.3 E3 inventory: every referring expression for the two players of each of the 20 TV streams (plan section 9).

Forms (longest first; possessive stripped): full name; title + surname (mr|miss|ms|mrs); nationality epithet
`the (young |younger |great |big )?<demonym>` (hand/players.tsv; resolved by nationality); descriptive epithets (Phase 2 family plus
woman / teenager / qualifier / maestro; resolved only by Phase 2's hand verdicts in the two finals, otherwise 'unresolved'); surname;
first name; hypocoristic (nole, rog, rafa, carlitos). Syntactic slot (spaCy, Phase 2 mapping), syllables (Phase 2 counter), situational
slot (lib2b classifier on the 4-token context window), umpire-pattern flag (Phase 2 rule, title extended to miss/ms/mrs), timing
(hit-clock A_after / A_before; stored t_to_next_first_hit_s where the stream is 25 fps).

Outputs: results/refexpr_pool_tokens.csv (one row per reference; no text beyond the expression), results/refexpr_pool_epithets.csv
(every epithet with an excerpt of at most 15 words and its resolution), results/refexpr_pool_summary.json
Run: python -I analysis/parry/p04_refexpr_pool.py
"""
import csv
import re
import sys
from collections import Counter
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import spacy
import lib2b as L
import refexpr as R   # analysis/formulas/refexpr.py (on sys.path via lib2b)

HYPO = {"nole": "djokovic", "rog": "federer", "rafa": "nadal", "carlitos": "alcaraz"}
# POST HOC (after inspecting the first run; logged in the report): (1) a nationality-epithet match whose demonym modifies a following
# noun that is not a person noun ('the greek fans', 'the czech republic', 'the italian riviera') is not a reference to a player;
# (2) hypocoristic + surname ('rafa nadal', 'nole djokovic') is one full-name reference, not two.
PERSON_NOUNS = {"man", "champion", "maestro", "seed", "player", "king", "legend", "veteran", "youngster", "teenager", "kid", "boy",
                "warrior", "magician", "genius", "master", "great", "greatest", "one", "challenger", "favourite", "favorite", "winner",
                "server", "returner", "star", "superstar", "woman", "girl", "lady", "queen", "number"}
DESCRIPTIVE = [
    r"the man from (?:basel|belgrade|murcia|el palmar|switzerland|serbia|spain)",
    r"the maestro",
    r"the world number (?:one|1)",
    r"the (?:number (?:one|1|two|2)|top|first|second) seed",
    r"the (?:defending |reigning )?champion",
    r"the (?:older|younger|young) (?:man|woman)",
    r"the \w+ time (?:grand slam |wimbledon )?champion",
    r"the \w+ year old",
    r"the teenager",
    r"the qualifier",
]


def players_table():
    with open(L.HAND / "players.tsv", encoding="utf-8") as fh:
        return {r["player"]: r for r in csv.DictReader(fh, delimiter="\t")}


def patterns_for(stream, ptab):
    meta = L.stream_meta(stream)
    ps = [ptab[p] for p in meta["players"]]
    sur = [p["surname"] for p in ps]
    pats = []
    for p in ps:
        hy = [h for h, s_ in HYPO.items() if s_ == p["surname"]]
        firsts = "|".join([p["first"]] + hy)
        pats.append((rf"(?:{firsts}) {p['surname']}", "full_name", p["surname"]))
    pats.append((r"(?:mr|miss|ms|mrs) (?:" + "|".join(sur) + ")", "title_surname", None))
    for p in ps:
        pats.append((rf"the (?:young |younger |great |big )?(?:{p['demonyms']})", "epithet_nationality", p["surname"]))
    for d in DESCRIPTIVE:
        pats.append((d, "epithet_descriptive", None))
    pats.append(("|".join(sur), "surname", None))
    pats.append(("|".join(p["first"] for p in ps), "first_name", None))
    hy = [h for h, s in HYPO.items() if s in sur]
    if hy:
        pats.append(("|".join(hy), "hypocoristic", None))
    first_to_sur = {p["first"]: p["surname"] for p in ps}
    return pats, sur, first_to_sur


def find(words, pats):
    s = " ".join(words)
    starts, p = [], 0
    for w in words:
        starts.append(p)
        p += len(w) + 1
    pos2tok = {st: k for k, st in enumerate(starts)}
    taken = [False] * len(words)
    out = []
    for pat, cat, ref in pats:
        for m in re.finditer(r"(?<![\w'])(?:" + pat + r")(?![\w'])", s):
            if m.start() not in pos2tok:
                continue
            k0 = pos2tok[m.start()]
            k1 = k0 + len(m.group(0).split())
            if any(taken[k0:k1]):
                continue
            for k in range(k0, k1):
                taken[k] = True
            out.append((k0, k1, m.group(0), cat, ref))
    out.sort()
    return out


def umpire(words, k0, k1, cat):
    if cat == "title_surname":
        return "title_surname"
    return R.umpire_rule(words, k0, k1, cat)


def main():
    nlp = spacy.load("en_core_web_sm")
    ptab = players_table()
    hand = {}
    with open(L.ROOT / "analysis" / "formulas" / "hand" / "epithet_referents.tsv", encoding="utf-8") as fh:
        for r in csv.DictReader(fh, delimiter="\t"):
            hand[(r["utt_id"], int(r["token_start"]))] = r["referent"]
    rows, ep_rows = [], []
    excluded_adj = 0
    summary = {"streams": {}}
    for stream in L.TV:
        pats, sur, f2s = patterns_for(stream, ptab)
        recs = L.C.load_stream(stream)
        gaps = L.hit_gaps(stream)
        valid = L.fps_valid(stream)
        cnt = Counter()
        texts = [r["text_corrected"] for r in recs]
        for r, doc in zip(recs, nlp.pipe(texts, batch_size=64)):
            words, idx = R.word_seq(doc)
            found = find(words, pats)
            if not found:
                continue
            sc = L.SlotClassifier(words)
            for k0, k1, expr, cat, ref in found:
                t0, t1 = idx[k0], idx[k1 - 1] + 1
                resolution = ""
                if cat == "epithet_nationality":
                    dem = doc[idx[k1 - 1]]
                    if dem.dep_ in ("amod", "compound") and dem.head.i > dem.i and dem.head.lemma_.lower() not in PERSON_NOUNS:
                        a = max(0, k0 - 6)
                        ep_rows.append({"stream": stream, "utt_id": r["utt_id"], "token_start": t0, "expression": expr, "category": cat,
                                        "excerpt_max15w": " ".join(words[a:a + 15]), "referent": "",
                                        "resolution": f"excluded: adjectival (modifies '{dem.head.text.lower()}')"})
                        excluded_adj += 1
                        continue
                if cat in ("full_name",):
                    player = ref
                elif cat in ("surname", "title_surname"):
                    player = [s for s in sur if s in expr.split()][0]
                elif cat == "first_name":
                    player = f2s[expr]
                elif cat == "hypocoristic":
                    player = HYPO[expr]
                else:
                    h = hand.get((r["utt_id"], t0))
                    if h is not None:
                        player, resolution = h, "hand verdict (Phase 2)"
                    elif cat == "epithet_nationality":
                        player, resolution = ref, "nationality"
                    else:
                        player, resolution = "UNRESOLVED", "unresolved"
                    a = max(0, k0 - 6)
                    ep_rows.append({"stream": stream, "utt_id": r["utt_id"], "token_start": t0, "expression": expr, "category": cat,
                                    "excerpt_max15w": " ".join(words[a:a + 15]), "referent": player, "resolution": resolution})
                if player not in sur and player != "UNRESOLVED":
                    continue   # a hand verdict naming someone else
                slot, dep = R.slot_of(doc, t0, t1)
                poss = slot == "possessive"
                g = gaps.get(r["utt_id"], {})
                rows.append({"stream": stream, "utt_id": r["utt_id"], "clip_i": r["clip_i"], "token_start": t0, "word_k0": k0,
                             "player": player, "expression": expr, "category": "epithet" if cat.startswith("epithet") else cat,
                             "epithet_kind": cat if cat.startswith("epithet") else "", "resolution": resolution,
                             "slot_syn": slot, "spacy_dep": dep, "slot_sit": sc.classify_context(k0, k1),
                             "syllables": R.syllables(expr, poss), "umpire_pattern": umpire(words, k0, k1, cat),
                             "A_after": g.get("A_after"), "A_before": g.get("A_before"),
                             "t_next_stored_valid": g.get("t_next_stored") if valid else None, "fps_valid": valid})
                cnt[(player, cat)] += 1
        summary["streams"][stream] = {"players": sur, "fps_valid": valid,
                                      "counts": {f"{p}:{c}": n for (p, c), n in sorted(cnt.items())}}
    fields = list(rows[0].keys())
    L.write_csv(L.RESULTS / "refexpr_pool_tokens.csv", rows, fields)
    L.write_csv(L.RESULTS / "refexpr_pool_epithets.csv", ep_rows)
    # check against Phase 2 (2019/2023 totals per player, all references)
    p2 = {}
    for s in (L.MAIN, L.HELDOUT):
        c = Counter(r["player"] for r in rows if r["stream"] == s and r["player"] != "UNRESOLVED")
        p2[s] = dict(c)
    summary["check_phase2_totals_all_references"] = p2
    summary["n_references"] = len(rows)
    summary["post_hoc_excluded_adjectival_nationality_matches"] = excluded_adj
    summary["post_hoc_hypocoristic_full_names"] = sum(1 for r in rows if r["category"] == "full_name" and r["expression"].split()[0] in HYPO)
    summary["n_unresolved_epithets"] = sum(1 for r in rows if r["player"] == "UNRESOLVED")
    summary["n_umpire_pattern"] = sum(1 for r in rows if r["umpire_pattern"])
    summary["spacy_model"] = f"en_core_web_sm {nlp.meta['version']}"
    L.write_json(L.RESULTS / "refexpr_pool_summary.json", summary)
    print({k: v for k, v in summary.items() if k != "streams"})


if __name__ == "__main__":
    main()
