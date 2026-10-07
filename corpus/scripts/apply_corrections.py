"""Step 3: apply corpus/corrections_rules.tsv to text_dedup -> text_corrected, as a separate logged step.
text_raw is never touched. Outputs: corpus/corrections.tsv (rules + counts), corpus/corrections.log (one line per applied
rule per utterance with a <=8-word context excerpt on each side of the matched span, in 'before => after' form).
Also checks every replacement name against the player lexicon built from the PBP matches files and the TennisVL match_info.
Run: python -I corpus/scripts/apply_corrections.py"""
import sys, json, re, csv, glob, collections
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from corpuslib import *
from textlib import words

TR = CORPUS / "transcripts"
rules = list(csv.DictReader(open(CORPUS / "corrections_rules.tsv", encoding="utf-8"), delimiter="\t"))

# player-name lexicon (surnames and first names) from PBP matches files + TennisVL + MCP names of the 20 matches
lex = set()
for f in glob.glob(str(PBP_DIR / "*-matches.csv")):
    for r in csv.DictReader(open(f, encoding="utf-8")):
        for k in ("player1", "player2"):
            for t in strip_accents(r.get(k, "")).split():
                lex.add(t)
for m in load_tennisvl():
    for k in ("p1", "p2"):
        for t in strip_accents(m["players"][k]["name"]).split():
            lex.add(t)

comp = []
for r in rules:
    comp.append((r, re.compile(r["pattern"])))

counts = collections.defaultdict(lambda: collections.Counter())
log = open(CORPUS / "corrections.log", "w", encoding="utf-8")
log.write("# corrections.log: one line per applied rule per utterance. Format: stream<TAB>utt_id<TAB>rule<TAB>match -> replacement<TAB>context (<=4 words each side)\n")


def in_scope(rule, mid):
    sc = rule["scope"]
    return sc == "all" or any(s and s in (mid or "") for s in sc.split(","))


def ctx(s, a, b, n=4):
    left = words(s[:a])[-n:]
    right = words(s[b:])[:n]
    return " ".join(left) + " [[" + s[a:b] + "]] " + " ".join(right)


tot_changed = {}
for f in sorted(TR.glob("*.jsonl")):
    stream = f.stem
    recs = [json.loads(l) for l in open(f, encoding="utf-8")]
    changed = 0
    for rec in recs:
        if rec["medium"] != "tv":
            continue
        t = rec["text_dedup"]
        for r, rx in comp:
            if not in_scope(r, rec["match_id"]):
                continue
            def rep(m):
                new = m.expand(r["replacement"])
                log.write(f"{stream}\t{rec['utt_id']}\t{r['id']}\t{m.group(0)} -> {new}\t{ctx(t, m.start(), m.end())}\n")
                counts[r["id"]][stream] += 1
                return new
            t = rx.sub(rep, t)
        if t != rec["text_dedup"]:
            changed += 1
        rec["text_corrected"] = t
    tot_changed[stream] = changed
    with open(f, "w", encoding="utf-8") as fh:
        for rec in recs:
            fh.write(json.dumps(rec, ensure_ascii=False) + "\n")
log.close()

out_rows = []
for r in rules:
    c = counts[r["id"]]
    rep_toks = [t for t in re.findall(r"[A-Z][a-z]+", r["replacement"].replace("\\g", "")) if t not in ("Game", "Love", "Deuce", "Fifth", "Set", "Forty", "Kei")]
    lex_ok = ""
    if r["kind"] == "name":
        lex_ok = "yes" if all(t in lex for t in rep_toks) else "no:" + ",".join(t for t in rep_toks if t not in lex)
    out_rows.append({"id": r["id"], "kind": r["kind"], "scope": r["scope"], "pattern": r["pattern"], "replacement": r["replacement"],
                     "confidence": r["confidence"], "reason": r["reason"], "count_applied": sum(c.values()),
                     "count_2019wimF": c.get("tv_2019wimF", 0), "count_2023wimF": c.get("tv_2023wimF", 0),
                     "count_pool": sum(v for k, v in c.items() if k.startswith("tv_pool_")),
                     "replacement_in_player_lexicon": lex_ok})
with open(CORPUS / "corrections.tsv", "w", newline="", encoding="utf-8") as fh:
    w = csv.DictWriter(fh, fieldnames=list(out_rows[0].keys()), delimiter="\t")
    w.writeheader()
    w.writerows(out_rows)
json.dump({"utterances_changed_per_stream": tot_changed, "total_substitutions": sum(r["count_applied"] for r in out_rows)},
          open(CORPUS / "reports" / "corrections_summary.json", "w"), indent=1)
print("substitutions:", sum(r["count_applied"] for r in out_rows))
for r in out_rows:
    print(r["id"], r["count_applied"], r["replacement_in_player_lexicon"])
