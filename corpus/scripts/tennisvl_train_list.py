"""List matches in a TennisVL train JSON: match id, clips, shots, synthetic-commentary words,
and whether any turn contains an audio transcription field.
Usage: python3 -I tennisvl_train_list.py FILE out.tsv"""
import json, sys, ast, re
data = json.load(open(sys.argv[1], encoding="utf-8"))
rows = []
for i, rec in enumerate(data):
    vids = rec["videos"]
    mid = re.sub(r"_\d+_\d+\.mp4$", "", vids[0].split("/")[-1])
    conv = rec["conversations"]
    gpts = [t["value"] for t in conv if t["from"] == "gpt"]
    humans = [t["value"] for t in conv if t["from"] == "human"]
    has_tr = any("audio_transcription" in t["value"] for t in conv)
    shots = 0
    for h in humans:
        meta = h.split("Metadata:", 1)[1].split("\n\nLive Stats:", 1)[0].strip()
        shots += len(ast.literal_eval(meta)["rally"])
    words = sum(len(g.split("\n\nMetadata:")[0].split()) for g in gpts)
    rows.append((i, mid, len(vids), shots, words, has_tr))
with open(sys.argv[2], "w", encoding="utf-8") as f:
    f.write("idx\tmatch_id\tclips\tshots\tsynthetic_commentary_words\thas_audio_transcription\n")
    for r in rows:
        f.write("\t".join(map(str, r)) + "\n")
print("matches", len(rows), "with transcription field:", sum(r[5] for r in rows))
print("total clips", sum(r[2] for r in rows))
from collections import Counter
print("matches per slam:", dict(Counter(r[1].split("-")[2] for r in rows)))
print("matches per year:", dict(sorted(Counter(r[1][:4] for r in rows).items())))
