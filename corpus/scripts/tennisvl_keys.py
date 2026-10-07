"""Collect all metadata keys seen in TennisVL human turns; search for transcript-like fields.
Usage: python3 -I tennisvl_keys.py FILE"""
import json, sys, ast, re
from collections import Counter
path = sys.argv[1]
data = json.load(open(path, encoding="utf-8"))
print("top-level type", type(data).__name__, "len", len(data))
first = data[0] if isinstance(data, list) else data[next(iter(data))]
print("record keys:", list(first.keys()) if isinstance(first, dict) else type(first))
topkeys, rallykeys, scorekeys = Counter(), Counter(), Counter()
bad = 0
for rec in data:
    for t in rec.get("conversations", rec.get("messages", [])):
        if t.get("from", t.get("role")) in ("human", "user"):
            v = t.get("value", t.get("content", ""))
            m = v.split("Metadata:", 1)
            if len(m) < 2:
                bad += 1; continue
            s = m[1].strip()
            try:
                d = ast.literal_eval(s)
            except Exception:
                # might have trailing text
                try:
                    d = ast.literal_eval(s[: s.rfind("}") + 1])
                except Exception:
                    bad += 1; continue
            topkeys.update(d.keys())
            for sh in d.get("rally", []):
                rallykeys.update(sh.keys())
print("metadata top keys:", dict(topkeys))
print("rally shot keys:", dict(rallykeys))
print("unparsed human turns:", bad)
raw = open(path, encoding="utf-8").read()
for pat in ["transcri", "audio", "whisper", "asr", "broadcast", "commentator said"]:
    print(pat, len(re.findall(pat, raw, flags=re.I)))
