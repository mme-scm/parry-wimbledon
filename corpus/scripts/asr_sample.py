"""Step 6a: draw the 500-word ASR proxy sample (seeded) from the de-duplicated 2019 final text.
The sample itself contains full source text, so it is written to the gitignored corpus/raw/derived_scratch/ only.
Run: python -I corpus/scripts/asr_sample.py"""
import sys, json, random
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from corpuslib import *
from textlib import words, cut_first_k_words

SEED = 500190714
recs = [json.loads(l) for l in open(CORPUS / "transcripts" / "tv_2019wimF.jsonl", encoding="utf-8")]
pool = [r for r in recs if len(words(r["text_dedup"])) >= 5]
rng = random.Random(SEED)
rng.shuffle(pool)
out, n = [], 0
for r in pool:
    w = words(r["text_dedup"])
    take = min(len(w), 500 - n)
    txt = r["text_dedup"] if take == len(w) else None
    if txt is None:
        # truncate at word `take`
        import re
        spans = [m.end() for m in re.finditer(r"[A-Za-z0-9]+(?:['’\-][A-Za-z0-9]+)*", r["text_dedup"])]
        txt = r["text_dedup"][:spans[take - 1]]
    out.append((r["utt_id"], txt, take))
    n += take
    if n >= 500:
        break
dst = RAW / "derived_scratch" / "asr_sample_500.txt"
with open(dst, "w", encoding="utf-8") as f:
    for uid, txt, k in out:
        f.write(f"### {uid} ({k} words)\n{txt}\n\n")
json.dump({"seed": SEED, "utt_ids": [u for u, _, _ in out], "n_words": n}, open(CORPUS / "reports" / "asr_sample_500_ids.json", "w"), indent=1)
print(dst, n, len(out))
