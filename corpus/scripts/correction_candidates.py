"""Step 3b: candidate list that supports the hand-curated corpus/corrections_rules.tsv.
For each of the 20 matches: ASR tokens (from the raw transcripts) that are not in the lower-cased Cornell vocabulary and are
close (difflib ratio >= 0.6) to a token of one of the two players' names. Writes corpus/reports/correction_candidates.tsv
(tokens and counts only, no running text). The rules themselves are curated by hand after reading contexts.
Run: python -I corpus/scripts/correction_candidates.py"""
import sys, re, json, csv, collections, difflib
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from corpuslib import *

cvl = set(w.lower() for c in json.load(open(CORNELL, encoding="utf-8")) for w in re.findall(r"[A-Za-z']+", c["commentary"]))
rows = []
for m in load_tennisvl():
    pl = m["players"]
    toks = [t for n in (pl["p1"]["name"], pl["p2"]["name"]) for t in strip_accents(n).split()]
    cnt = collections.Counter(w for c in m["clips"] for w in re.findall(r"[A-Za-z][A-Za-z']*", c["text"]))
    for w, n in cnt.items():
        if w.lower() in cvl or w in toks:
            continue
        for t in toks:
            r = difflib.SequenceMatcher(None, w.lower(), t.lower()).ratio()
            if r >= 0.6:
                rows.append({"match_date": m["match_id"][:8], "player_token": t, "asr_token": w, "count": n, "ratio": round(r, 2)})
rows.sort(key=lambda r: (r["match_date"], r["player_token"], -r["count"]))
with open(CORPUS / "reports" / "correction_candidates.tsv", "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0].keys()), delimiter="\t")
    w.writeheader(); w.writerows(rows)
print(len(rows), "candidate rows")
