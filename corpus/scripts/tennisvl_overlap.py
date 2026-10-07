"""Measure duplication between consecutive per-clip transcripts in TennisVL test_stats JSON.
Usage: python3 -I tennisvl_overlap.py FILE
For each match: transcripts identical to previous; share of 6-gram tokens already present in the
previous non-empty transcript; deduplicated word count (words in 6-grams not seen in previous)."""
import json, sys, ast, re
data = json.load(open(sys.argv[1], encoding="utf-8"))
def toks(s): return re.findall(r"[\w']+", s.lower())
print("idx\tmatch\tnonempty\tidentical_to_prev\twords\twords_in_6grams_seen_in_prev\tapprox_unique_words")
for i, rec in enumerate(data):
    gpts = [t["value"] for t in rec["conversations"] if t["from"] == "gpt"]
    trs = []
    for g in gpts:
        _, _, meta = g.partition("\n\nMetadata:")
        d = ast.literal_eval(meta.strip()) if meta else {}
        trs.append(d.get("audio_transcription (background context)", "") or "")
    prev = None; ident = 0; words = 0; seen_words = 0; nonempty = 0
    for tr in trs:
        if not tr.strip():
            continue
        nonempty += 1
        t = toks(tr); words += len(t)
        if prev is not None:
            if tr.strip() == prev.strip(): ident += 1
            pt = toks(prev)
            pg = {tuple(pt[j:j+6]) for j in range(len(pt)-5)}
            covered = [False]*len(t)
            for j in range(len(t)-5):
                if tuple(t[j:j+6]) in pg:
                    for k in range(j, j+6): covered[k] = True
            seen_words += sum(covered)
        prev = tr
    mid = re.sub(r"_\d+_\d+\.mp4$", "", rec["videos"][0].split("/")[-1])
    print(f"{i}\t{mid}\t{nonempty}\t{ident}\t{words}\t{seen_words}\t{words-seen_words}")
