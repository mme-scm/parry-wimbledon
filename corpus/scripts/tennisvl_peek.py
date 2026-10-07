"""Print match-level summary and first N turns of a TennisVL sharegpt JSON."""
import json, sys
path, idx, n = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
data = json.load(open(path, encoding="utf-8"))
rec = data[idx]
print("videos[:5]:", rec["videos"][:5])
print("n turns:", len(rec["conversations"]), "n videos:", len(rec["videos"]))
from collections import Counter
print(Counter(t["from"] for t in rec["conversations"]))
for t in rec["conversations"][:n]:
    print("----", t["from"], "len", len(t["value"]))
    print(t["value"][:1500])
