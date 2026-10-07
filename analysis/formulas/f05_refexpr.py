"""Noun-epithet systems: referring expressions for the players of the 2019 final (and 2023, held-out),
by syntactic slot, length in syllables and timing context (plan section 5).

Inputs (hand-made): hand/epithet_referents.tsv (referent of each epithet occurrence),
                    hand/slot_sample40.tsv (hand slot labels for a random sample of 40 expressions).
Outputs: results/refexpr_tokens_<stream>.csv, results/refexpr_inventory.csv, results/refexpr_by_slot.csv,
results/refexpr_by_context.csv, results/refexpr_syllables.csv, results/pronouns.csv, results/slot_validation.json,
results/epithet_candidates.tsv (all epithet occurrences with excerpt <= 15 words and the hand verdict),
results/epithet_discovery.csv (audit list, exploratory)
Run: python -I analysis/formulas/f05_refexpr.py
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import csv
import json
from collections import Counter, defaultdict
import numpy as np
import spacy
import common as C
import refexpr as R

CTX = ("ctx_phase", "ctx_dtb_terc", "ctx_ta_terc", "ctx_score", "ctx_role")
PERSON_NOUNS = {"man", "champion", "swiss", "serb", "serbian", "spaniard", "maestro", "seed", "player", "king", "legend",
                "veteran", "youngster", "teenager", "kid", "boy", "warrior", "magician", "genius", "master", "great",
                "greatest", "old", "one", "challenger", "favourite", "favorite", "winner", "server", "returner"}


def read_tsv(path):
    if not path.exists():
        return []
    with open(path, encoding="utf-8") as fh:
        return list(csv.DictReader(fh, delimiter="\t"))


def main():
    nlp = spacy.load("en_core_web_sm")
    hand_ref = {(r["utt_id"], int(r["token_start"])): r for r in read_tsv(C.HAND / "epithet_referents.tsv")}
    tokens_all = []
    cand_rows = []
    pron_rows = []
    discovery = Counter()
    for stream in (C.MAIN, C.HELDOUT):
        recs = C.load_stream(stream)
        C.add_contexts(recs, stream)
        players = R.PLAYERS[stream]
        for r in recs:
            doc = nlp(r["text_corrected"])
            exprs = R.find_expressions(doc)
            words, _ = R.word_seq(doc)
            # discovery list: "the (w){0,3} <person noun>"
            for i, w in enumerate(words):
                if w == "the":
                    for L in range(1, 5):
                        if i + L < len(words) and words[i + L] in PERSON_NOUNS:
                            discovery[(stream, " ".join(words[i:i + L + 1]))] += 1
                            break
            named = set()
            utt_tokens = []
            for e in exprs:
                ref = R.referent(e["expr"], e["category"])
                verdict = ""
                if e["category"] == "epithet":
                    h = hand_ref.get((r["utt_id"], e["t0"]))
                    ref = h["referent"] if h else "UNRESOLVED"
                    verdict = ref
                    a = max(0, e["k0"] - 6)
                    cand_rows.append({"stream": stream, "utt_id": r["utt_id"], "token_start": e["t0"], "expression": e["expr"],
                                      "excerpt_max15w": " ".join(words[a:a + 15]), "hand_referent": verdict})
                if ref not in players:
                    continue
                slot, dep = R.slot_of(doc, e["t0"], e["t1"])
                poss = slot == "possessive"
                tok = {"stream": stream, "utt_id": r["utt_id"], "clip_i": r["clip_i"], "token_start": e["t0"], "player": ref,
                       "expression": e["expr"], "category": e["category"], "slot": slot, "spacy_dep": dep,
                       "syllables": R.syllables(e["expr"], poss),
                       "dead_time_before_s": r["ctx_dt_before"], "time_after_s": r["ctx_time_after"],
                       "umpire_pattern": R.umpire_rule(words, e["k0"], e["k1"], e["category"])}
                for c in CTX:
                    tok[c[4:]] = r[c]
                utt_tokens.append(tok)
                named.add(ref)
            tokens_all += utt_tokens
            # pronouns
            toks = r["toks"]
            npron = sum(1 for t in toks if t in R.PRON)
            attributed = next(iter(named)) if len(named) == 1 else "unattributed"
            pron_rows.append({"stream": stream, "utt_id": r["utt_id"], "pronouns": npron, "attributed_to": attributed,
                              **{c[4:]: r[c] for c in CTX}})
    # write per-token files
    fields = list(tokens_all[0])
    for stream in (C.MAIN, C.HELDOUT):
        with open(C.RESULTS / f"refexpr_tokens_{stream}.csv", "w", newline="") as fh:
            w = csv.DictWriter(fh, fieldnames=fields)
            w.writeheader()
            for t in tokens_all:
                if t["stream"] == stream:
                    w.writerow(t)
    with open(C.RESULTS / "epithet_candidates.tsv", "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=list(cand_rows[0]), delimiter="\t")
        w.writeheader()
        w.writerows(cand_rows)
    # inventory
    inv = Counter((t["stream"], t["player"], t["category"], t["expression"]) for t in tokens_all)
    syl = {(t["stream"], t["player"], t["category"], t["expression"]): t["syllables"] for t in tokens_all if t["slot"] != "possessive"}
    syl_any = {(t["stream"], t["player"], t["category"], t["expression"]): t["syllables"] for t in tokens_all}
    slots = defaultdict(Counter)
    for t in tokens_all:
        slots[(t["stream"], t["player"], t["category"], t["expression"])][t["slot"]] += 1
    SL = ["subject", "object", "possessive", "after_preposition", "vocative_exclamation", "other"]
    with open(C.RESULTS / "refexpr_inventory.csv", "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["stream", "player", "category", "expression", "tokens", "syllables_base"] + SL)
        for k in sorted(inv, key=lambda k: (k[0], k[1], -inv[k])):
            w.writerow(list(k) + [inv[k], syl.get(k, syl_any[k])] + [slots[k].get(s, 0) for s in SL])
    # by slot (player x slot)
    with open(C.RESULTS / "refexpr_by_slot.csv", "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["stream", "player", "slot", "tokens", "distinct_expressions", "expressions"])
        g = defaultdict(Counter)
        for t in tokens_all:
            g[(t["stream"], t["player"], t["slot"])][t["expression"]] += 1
        for k in sorted(g):
            w.writerow(list(k) + [sum(g[k].values()), len(g[k]), "; ".join(f"{e}:{c}" for e, c in g[k].most_common())])
    # syllable distribution
    with open(C.RESULTS / "refexpr_syllables.csv", "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["stream", "player", "syllables", "tokens", "expressions"])
        g = defaultdict(Counter)
        for t in tokens_all:
            g[(t["stream"], t["player"], t["syllables"])][t["expression"]] += 1
        for k in sorted(g):
            w.writerow(list(k) + [sum(g[k].values()), "; ".join(f"{e}:{c}" for e, c in g[k].most_common())])
    # by context
    with open(C.RESULTS / "refexpr_by_context.csv", "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["stream", "player", "context", "group", "tokens", "distinct_expressions", "mean_syllables",
                    "share_surname", "expressions"])
        for c in CTX:
            g = defaultdict(list)
            for t in tokens_all:
                g[(t["stream"], t["player"], c[4:], t[c[4:]])].append(t)
            for k in sorted(g):
                L = g[k]
                ex = Counter(t["expression"] for t in L)
                w.writerow(list(k) + [len(L), len(ex), f"{np.mean([t['syllables'] for t in L]):.3f}",
                                      f"{np.mean([t['category'] == 'surname' for t in L]):.3f}",
                                      "; ".join(f"{e}:{n}" for e, n in ex.most_common())])
    # pronouns
    with open(C.RESULTS / "pronouns.csv", "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["stream", "context", "group", "attributed_to", "utterances", "pronouns"])
        for c in ("all",) + tuple(x[4:] for x in CTX):
            g = defaultdict(lambda: [0, 0])
            for p in pron_rows:
                grp = "all" if c == "all" else p[c]
                for att in (p["attributed_to"], "ANY"):
                    g[(p["stream"], c, grp, att)][0] += 1
                    g[(p["stream"], c, grp, att)][1] += p["pronouns"]
            for k in sorted(g):
                w.writerow(list(k) + g[k])
    # discovery
    with open(C.RESULTS / "epithet_discovery.csv", "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["stream", "string", "count"])
        for (s, x), n in sorted(discovery.items(), key=lambda kv: (kv[0][0], -kv[1], kv[0][1])):
            w.writerow([s, x, n])
    # slot validation sample (seed fixed): 40 expression tokens of the 2019 final
    t19 = [t for t in tokens_all if t["stream"] == C.MAIN]
    rng = np.random.default_rng(C.MASTER_SEED)
    pick = sorted(rng.choice(len(t19), size=min(40, len(t19)), replace=False))
    hand = {(r["utt_id"], int(r["token_start"])): r["hand_slot"] for r in read_tsv(C.HAND / "slot_sample40.tsv")}
    agree, n_h, conf = 0, 0, Counter()
    sample_rows = []
    for i in pick:
        t = t19[i]
        hs = hand.get((t["utt_id"], t["token_start"]))
        sample_rows.append((t["utt_id"], t["token_start"], t["expression"]))
        if hs:
            n_h += 1
            agree += int(hs == t["slot"])
            conf[(hs, t["slot"])] += 1
    C.write_json(C.RESULTS / "slot_validation.json", {
        "sample_size": len(pick), "hand_labelled": n_h, "agree": agree,
        "accuracy": agree / n_h if n_h else None,
        "confusion_hand_vs_spacy": {f"{a}|{b}": c for (a, b), c in sorted(conf.items())},
        "sample_keys": [list(x) for x in sample_rows],
    })
    summary = {
        "tokens_by_stream_player": {f"{s}:{p}": n for (s, p), n in Counter((t["stream"], t["player"]) for t in tokens_all).items()},
        "epithet_occurrences": len(cand_rows),
        "epithets_unresolved": sum(1 for c in cand_rows if c["hand_referent"] == "UNRESOLVED"),
        "pronouns_total": {s: sum(p["pronouns"] for p in pron_rows if p["stream"] == s) for s in (C.MAIN, C.HELDOUT)},
        "spacy_model": f"en_core_web_sm {nlp.meta['version']}", "spacy_version": spacy.__version__,
        "umpire_pattern_tokens": {f"{s}:{rule}": n for (s, rule), n in sorted(Counter((t["stream"], t["umpire_pattern"])
                                                                                    for t in tokens_all if t["umpire_pattern"]).items())},
        "umpire_before_patterns": [list(x) for x in R.UMPIRE_BEFORE], "umpire_after_patterns": [list(x) for x in R.UMPIRE_AFTER],
    }
    C.write_json(C.RESULTS / "refexpr_summary.json", summary)
    print(json.dumps(summary, indent=1))


if __name__ == "__main__":
    main()
