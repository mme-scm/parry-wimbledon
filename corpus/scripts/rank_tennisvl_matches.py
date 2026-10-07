"""Rank TennisVL test matches (the only split with ASR transcripts) by commentary text and timing coverage.
Usage: python3 -I rank_tennisvl_matches.py TEST_STATS_JSON MCP_DIR SLAM_PBP_DIR OUT_TSV
Columns:
  clips, clips_with_transcript, transcript_words (raw), unique_words (6-gram dedup vs previous clip),
  score_states (distinct score/server states covered by clips), mcp_points (Match Charting Project points),
  state_coverage = score_states / mcp_points, shots_with_hit_ts, slam_pbp (match found in Sackmann slam
  point-by-point *-matches.csv with ElapsedTime), mcp (charted)."""
import json, sys, ast, re, csv, os, glob
src, mcp_dir, pbp_dir, out = sys.argv[1:5]
data = json.load(open(src, encoding="utf-8"))
def toks(s): return re.findall(r"[\w']+", s.lower())
# MCP point counts
mcp_pts = {}
for f in glob.glob(os.path.join(mcp_dir, "charting-*-points-*.csv")):
    with open(f, encoding="utf-8", errors="replace") as fh:
        for r in csv.reader(fh):
            if r and r[0] != "match_id":
                mcp_pts[r[0]] = mcp_pts.get(r[0], 0) + 1
mcp_ids = set()
for f in glob.glob(os.path.join(mcp_dir, "charting-*-matches.csv")):
    with open(f, encoding="utf-8", errors="replace") as fh:
        for r in csv.DictReader(fh):
            mcp_ids.add(r["match_id"])
# slam pbp matches
slam_map = {"Australian_Open": "ausopen", "Roland_Garros": "frenchopen", "Wimbledon": "wimbledon", "US_Open": "usopen"}
def pbp_lookup(mid):
    date, sex, tour, rnd, p1, p2 = mid.split("-", 5)
    f = os.path.join(pbp_dir, f"{date[:4]}-{slam_map[tour]}-matches.csv")
    if not os.path.exists(f):
        return "no-file"
    # match on surname + first initial, since AO/FO files abbreviate first names ("D. Thiem", "S Tsitsipas")
    def key(n):
        parts = n.replace("_", " ").replace(".", "").split()
        return (parts[0][0].lower(), parts[-1].lower())
    k1, k2 = key(p1), key(p2)
    hits = []
    for r in csv.DictReader(open(f, encoding="utf-8", errors="replace")):
        ks = {key(r["player1"]), key(r["player2"])}
        if k1 in ks and k2 in ks:
            hits.append(r["match_id"])
    return ";".join(hits) if hits else "not-found"
rows = []
for rec in data:
    mid = re.sub(r"_\d+_\d+\.mp4$", "", rec["videos"][0].split("/")[-1])
    conv = rec["conversations"]
    humans = [t["value"] for t in conv if t["from"] == "human"]
    gpts = [t["value"] for t in conv if t["from"] == "gpt"]
    trs = []
    for g in gpts:
        _, _, meta = g.partition("\n\nMetadata:")
        d = ast.literal_eval(meta.strip()) if meta else {}
        trs.append(d.get("audio_transcription (background context)", "") or "")
    words = sum(len(t.split()) for t in trs)
    prev = None; uniq = 0
    for tr in trs:
        if not tr.strip(): continue
        t = toks(tr)
        if prev is None:
            uniq += len(t)
        else:
            pg = {tuple(prev[j:j+6]) for j in range(len(prev)-5)}
            cov = [False]*len(t)
            for j in range(len(t)-5):
                if tuple(t[j:j+6]) in pg:
                    for k in range(j, j+6): cov[k] = True
            uniq += len(t) - sum(cov)
        prev = t
    states = set(); shots_ts = 0
    for h in humans:
        d = ast.literal_eval(h.split("Metadata:", 1)[1].strip())
        s = d["score_state"]
        states.add(json.dumps([s["server"], s["sets"], s["games_in_current_set"], s["points_in_current_game"]], sort_keys=True))
        shots_ts += sum(1 for sh in d["rally"] if sh.get("hit_timestamp_second") is not None)
    mp = mcp_pts.get(mid, 0)
    rows.append(dict(match_id=mid, clips=len(humans), clips_with_transcript=sum(1 for t in trs if t.strip()),
                     transcript_words=words, unique_words=uniq, score_states=len(states), mcp_points=mp,
                     state_coverage=round(len(states)/mp, 3) if mp else "", shots_with_hit_ts=shots_ts,
                     slam_pbp=pbp_lookup(mid), mcp="yes" if mid in mcp_ids else "no"))
rows.sort(key=lambda r: -r["unique_words"])
with open(out, "w", encoding="utf-8", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0].keys()), delimiter="\t")
    w.writeheader(); w.writerows(rows)
for r in rows: print("\t".join(str(v) for v in r.values()))
