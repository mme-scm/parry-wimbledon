"""Summarise Cornell text_commentaries.json: counts, words, distinct player pairings in scorelines.
Usage: python3 -I cornell_stats.py FILE"""
import json, sys, re
from collections import Counter
d = json.load(open(sys.argv[1], encoding="utf-8"))
print("records", len(d), "keys", Counter(tuple(sorted(r.keys())) for r in d))
print("gender", Counter(r["gender"] for r in d))
w = [len(r["commentary"].split()) for r in d]
print("total words", sum(w), "mean", round(sum(w)/len(w), 1), "max", max(w))
pairs = Counter()
for r in d:
    s = re.sub(r"[\d\-\*\(\)]+", " ", r["scoreline"]).split()
    pairs[" v ".join(sorted(s))] += 1
print("distinct name-pairs in scorelines", len(pairs))
for p, c in pairs.most_common(15): print(c, p)
print("sample scorelines:", [r["scoreline"] for r in d[:5]])
