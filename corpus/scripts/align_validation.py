"""Step 7: alignment validation. (a) draws 20 random aligned 2019 utterances that contain a parseable score call and writes
corpus/reports/alignment_sample20.tsv (call excerpt <= 12 words, PBP scores around the aligned point) for hand judging;
(b) combines the hand verdicts in corpus/validation/alignment_sample20_judgements.tsv with automatic statistics.
Run: python -I corpus/scripts/align_validation.py"""
import sys, json, csv, re, random, collections
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from corpuslib import *
from textlib import words
import pandas as pd

SEED = 20190715
NUM = {"love": "0", "0": "0", "15": "15", "30": "30", "40": "40", "forty": "40", "thirty": "30", "fifteen": "15"}
CALL = re.compile(r"\b(love|0|15|30|40|forty|thirty|fifteen)[ ,.\-–]+(love|0|15|30|40|forty|thirty|fifteen)\b", re.I)
pts = pd.read_csv(CORPUS / "timing" / "points_2019wimF.csv", dtype=str).set_index("point_idx")
pts.index = pts.index.astype(int)
recs = [json.loads(l) for l in open(CORPUS / "transcripts" / "tv_2019wimF.jsonl", encoding="utf-8")]
cand = [r for r in recs if r["point_idx_pbp"] and CALL.search(r["text_corrected"] or "")]
rng = random.Random(SEED)
sample = sorted(rng.sample(cand, 20), key=lambda r: r["clip_i"])


def sf(j):
    """score before point j in server-first order of point j's server, as 'a-b'"""
    r = pts.loc[j]
    a, b = r.pts_before_p1, r.pts_before_p2
    return f"{a}-{b}" if r.server_pbp == "1" else f"{b}-{a}"


rows = []
for r in sample:
    pi = r["point_idx_pbp"]
    m = CALL.search(r["text_corrected"])
    ws = words(r["text_corrected"][max(0, m.start() - 40):m.end() + 40])
    ex = " ".join(ws[:12])
    rows.append({"utt_id": r["utt_id"], "point_idx": pi, "set": r["set_no"], "game_in_set": r["game_in_set"],
                 "server": pts.loc[pi].server, "pbp_score_before_this_point": sf(pi),
                 "pbp_score_after_this_point": sf(pi + 1) if pi + 1 in pts.index else "end",
                 "pbp_score_after_next_point": sf(pi + 2) if pi + 2 in pts.index else "end",
                 "first_call_in_text": f"{m.group(1)}-{m.group(2)}", "call_context_excerpt": ex,
                 "text_corrected_n_words": len(words(r["text_corrected"]))})
with open(CORPUS / "reports" / "alignment_sample20.tsv", "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0].keys()), delimiter="\t")
    w.writeheader(); w.writerows(rows)

# automatic statistics over all aligned 2019 + 2023 utterances with a call
stats = {}
for cfg in (MAIN, HELD):
    P = pd.read_csv(CORPUS / "timing" / f"points_{cfg['tag']}.csv", dtype=str).set_index("point_idx")
    P.index = P.index.astype(int)
    R = [json.loads(l) for l in open(CORPUS / "transcripts" / f"{cfg['stream']}.jsonl", encoding="utf-8")]
    def sf2(j):
        r = P.loc[j]; a, b = r.pts_before_p1, r.pts_before_p2
        return (a, b) if r.server_pbp == "1" else (b, a)
    c = collections.Counter(); n = 0
    for r in R:
        pi = r["point_idx_pbp"]
        if not pi or not r["text_dedup"]:
            continue
        m = CALL.search(r["text_corrected"])
        if not m:
            continue
        call = (NUM[m.group(1).lower()], NUM[m.group(2).lower()])
        n += 1
        hits = [d for d in (-1, 0, 1, 2, 3) if (pi + d) in P.index and sf2(pi + d) == call]
        c[hits[0] if hits else "none"] += 1
    stats[cfg["tag"]] = {"n_utterances_with_call": n, "first_call_equals_score_before_point_plus_d": {str(k): v for k, v in sorted(c.items(), key=lambda kv: str(kv[0]))},
                         "note": "d=1: the call equals the score after this clip's point (before the next point)"}
jf = CORPUS / "validation" / "alignment_sample20_judgements.tsv"
out = {"seed": SEED, "n_candidates": len(cand), "automatic": stats}
if jf.exists():
    J = list(csv.DictReader(open(jf, encoding="utf-8"), delimiter="\t"))
    out["hand_verdicts"] = dict(collections.Counter(j["verdict"] for j in J))
    out["n_judged"] = len(J)
    out["judgements_match_current_sample"] = [j["utt_id"] for j in J] == [r["utt_id"] for r in rows]
json.dump(out, open(CORPUS / "reports" / "alignment_validation.json", "w"), indent=1)
print(json.dumps(out, indent=1))
for r in rows:
    print(r)
