"""Step 6b: ASR error proxy. NO audio exists, so WER is unknown. Two internal proxies:
(A) automatic: per 1,000 words of de-duplicated text, (i) player-name variants fixed by the correction list (name rules N*),
    (ii) score-call terms fixed by the term rules (T03-T05), (iii) score calls that match no PBP score state in a window
    around the aligned point (2019/2023 only).
(B) hand-read 500-word sample of the 2019 final (corpus/raw/derived_scratch/asr_sample_500.txt, gitignored), errors listed in
    corpus/validation/asr_sample_errors.tsv; rates are computed here from that file.
Outputs corpus/reports/asr_proxy.json.
Run: python -I corpus/scripts/asr_proxy.py"""
import sys, json, csv, re, collections
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from corpuslib import *
from textlib import words
import pandas as pd

rep = {"wer": "unknown (no audio, no human reference transcript)"}
# ---- A. automatic
corr = list(csv.DictReader(open(CORPUS / "corrections.tsv", encoding="utf-8"), delimiter="\t"))
name_ids = [r for r in corr if r["kind"] == "name"]
lovefix = [r for r in corr if r["id"] in ("T03", "T04", "T05")]
manifest = json.load(open(CORPUS / "transcripts" / "manifest.json"))
A = {}
for stream in ("tv_2019wimF", "tv_2023wimF"):
    nw = manifest["streams"][stream]["n_words_dedup"]
    col = "count_2019wimF" if stream == "tv_2019wimF" else "count_2023wimF"
    nn = sum(int(r[col]) for r in name_ids)
    nl = sum(int(r[col]) for r in lovefix)
    A[stream] = {"n_words_dedup": nw, "name_variants_corrected": nn, "name_variants_per_1000_words": 1000 * nn / nw,
                 "love_score_call_errors_corrected": nl, "love_errors_per_1000_words": 1000 * nl / nw}
nw = sum(v["n_words_dedup"] for k, v in manifest["streams"].items() if k.startswith("tv_"))
nn = sum(int(r["count_applied"]) for r in name_ids)
nl = sum(int(r["count_applied"]) for r in lovefix)
A["all_tv_streams"] = {"n_words_dedup": nw, "name_variants_corrected": nn, "name_variants_per_1000_words": 1000 * nn / nw,
                       "love_score_call_errors_corrected": nl, "love_errors_per_1000_words": 1000 * nl / nw}

# (iii) score calls vs PBP window (2019, 2023)
NUM = {"love": "0", "0": "0", "15": "15", "30": "30", "40": "40", "forty": "40", "thirty": "30", "fifteen": "15"}
CALL = re.compile(r"\b(love|0|15|30|40|forty|thirty|fifteen)[ ,.\-–]+(love|0|15|30|40|forty|thirty|fifteen)\b", re.I)
for cfg in (MAIN, HELD):
    pts = pd.read_csv(CORPUS / "timing" / f"points_{cfg['tag']}.csv", dtype=str).set_index("point_idx")
    pts.index = pts.index.astype(int)
    recs = [json.loads(l) for l in open(CORPUS / "transcripts" / f"{cfg['stream']}.jsonl", encoding="utf-8")]
    n_calls = n_match = n_first = n_first_match_after = 0
    for r in recs:
        pi = r["point_idx_pbp"]
        if pi is None or not r["text_corrected"]:
            continue
        calls = CALL.findall(r["text_corrected"])
        states = set()
        for j in range(pi - 1, pi + 4):
            if j in pts.index:
                a, b = pts.loc[j].pts_before_p1, pts.loc[j].pts_before_p2
                states.add((a, b)); states.add((b, a))
        for k, (a, b) in enumerate(calls):
            a, b = NUM[a.lower()], NUM[b.lower()]
            n_calls += 1
            n_match += (a, b) in states
        if calls:
            n_first += 1
            a, b = NUM[calls[0][0].lower()], NUM[calls[0][1].lower()]
            if pi + 1 in pts.index:
                s = (pts.loc[pi + 1].pts_before_p1, pts.loc[pi + 1].pts_before_p2)
                n_first_match_after += (a, b) in (s, s[::-1])
    A[cfg["stream"]]["score_calls_parsed"] = n_calls
    A[cfg["stream"]]["score_calls_matching_pbp_window_p-1..p+3"] = n_match
    A[cfg["stream"]]["score_call_mismatch_per_1000_words"] = 1000 * (n_calls - n_match) / A[cfg["stream"]]["n_words_dedup"]
    A[cfg["stream"]]["clips_with_call"] = n_first
    A[cfg["stream"]]["first_call_equals_score_after_this_point"] = n_first_match_after
rep["automatic"] = A

# ---- B. hand-read sample
ids = json.load(open(CORPUS / "reports" / "asr_sample_500_ids.json"))
errs = list(csv.DictReader(open(CORPUS / "validation" / "asr_sample_errors.tsv", encoding="utf-8"), delimiter="\t"))
recs = {json.loads(l)["utt_id"]: json.loads(l) for l in open(CORPUS / "transcripts" / "tv_2019wimF.jsonl", encoding="utf-8")}
chk = []
for e in errs:
    assert e["utt_id"] in ids["utt_ids"], e
    assert len(e["excerpt"].split()) <= 15
    t = recs[e["utt_id"]]
    present = e["excerpt"] in t["text_dedup"]
    fixed = present and (e["excerpt"] not in t["text_corrected"])
    chk.append({**e, "excerpt_found_in_text_dedup": present, "fixed_by_correction_list": fixed})
by = collections.Counter(e["error_type"] for e in errs)
n = ids["n_words"]
def wilson(k, n, z=1.96):
    p = k / n
    d = 1 + z * z / n
    c = p + z * z / (2 * n)
    h = z * ((p * (1 - p) / n + z * z / (4 * n * n)) ** 0.5)
    return [1000 * (c - h) / d, 1000 * (c + h) / d]


rep["hand_sample"] = {"wilson95_ci_per_1000_total": wilson(len(errs), n),
                      "wilson95_ci_per_1000_name_plus_score": wilson(by["name_misspelled"] + by["score_call_impossible"], n),"n_words": n, "n_utterances": len(ids["utt_ids"]), "seed": ids["seed"],
                      "errors_by_type": dict(by), "errors_total": len(errs),
                      "per_1000_words": {k: 1000 * v / n for k, v in by.items()},
                      "total_per_1000_words": 1000 * len(errs) / n,
                      "name_plus_score_call_per_1000_words": 1000 * (by["name_misspelled"] + by["score_call_impossible"]) / n,
                      "n_fixed_by_correction_list": sum(c["fixed_by_correction_list"] for c in chk),
                      "all_excerpts_found": all(c["excerpt_found_in_text_dedup"] for c in chk),
                      "caveat": "recall-limited: only errors detectable by plausibility without audio are counted; WER is certainly higher"}
rep["hand_sample_errors"] = [{k: v for k, v in c.items()} for c in chk]
json.dump(rep, open(CORPUS / "reports" / "asr_proxy.json", "w"), indent=1)
print(json.dumps(rep, indent=1)[:4000])
