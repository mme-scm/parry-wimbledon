"""Print two truncated sample records from each downloaded annotation file, for corpus/SOURCES.md.
Free-text fields are cut to at most 15 words so that excerpts can be committed.
Usage: python3 -I print_samples.py RAW_DIR"""
import json, sys, os, ast, csv, itertools
raw = sys.argv[1]
def cut(s, n=15):
    w = str(s).split()
    return " ".join(w[:n]) + (" [...]" if len(w) > n else "")
def tvl(path, idx, clip_ids, has_tr):
    data = json.load(open(path, encoding="utf-8"))
    rec = data[idx]
    conv = rec["conversations"]
    humans = [t for t in conv if t["from"] == "human"]
    gpts = [t for t in conv if t["from"] == "gpt"]
    for i in clip_ids:
        h = humans[i]["value"]
        meta = h.split("Metadata:", 1)[1].split("\n\nLive Stats:", 1)[0].strip()
        d = ast.literal_eval(meta)
        sh = d["rally"][0]
        out = {"video": rec["videos"][i], "score_state": d["score_state"],
               "n_shots": len(d["rally"]), "rally[0]": {k: sh[k] for k in ("shot_index", "hit_timestamp_second", "hitter", "type", "direction_rough", "bounce_timestamp_second", "shot_outcome")},
               "point_outcome": d.get("point_outcome")}
        com, _, gm = gpts[i]["value"].partition("\n\nMetadata:")
        out["gpt (LLM-synthesised commentary)"] = cut(com)
        if gm:
            g = ast.literal_eval(gm.strip())
            out["gpt.Metadata keys"] = list(g.keys())
            out["audio_transcription (background context)"] = cut(g.get("audio_transcription (background context)", ""))
        if "Live Stats:" in h:
            out["human.Live Stats keys (per player)"] = list(ast.literal_eval(h.split("Live Stats:", 1)[1].strip()).values())[0].keys().__repr__()
        print(json.dumps(out, ensure_ascii=False))
print("## TennisVL test_stats (match idx 18 = 2019 Wimbledon final), clips 0 and 2")
tvl(os.path.join(raw, "tennisexpert_repo/data/tennis_data_test_stats_.json"), 18, [0, 2], True)
print("## TennisVL tennis_vl_test.json (match idx 18), clip 0")
tvl(os.path.join(raw, "tennisexpert_repo/data/tennis_vl_test.json"), 18, [0, 1], False)
print("## TennisVL train stats (match idx 0), clips 0,1")
tvl(os.path.join(raw, "tennisvl_train/tennis_data_train_stats_.json"), 0, [0, 1], False)
print("## Cornell text_commentaries.json records 0,1")
d = json.load(open(os.path.join(raw, "cornell_tennis/extracted/text_commentaries.json"), encoding="utf-8"))
for r in d[:2]:
    print(json.dumps({"commentary": cut(r["commentary"]), "scoreline": r["scoreline"], "gender": r["gender"]}, ensure_ascii=False))
print("## MCP charting-m-matches.csv (2019 Wimbledon final row)")
for r in csv.DictReader(open(os.path.join(raw, "sackmann_mcp/charting-m-matches.csv"), encoding="utf-8", errors="replace")):
    if r["match_id"] == "20190714-M-Wimbledon-F-Roger_Federer-Novak_Djokovic":
        print(json.dumps(r))
print("## MCP charting-m-points-2010s.csv: first two points of the 2019 Wimbledon final (by Pt)")
rows = [r for r in csv.DictReader(open(os.path.join(raw, "sackmann_mcp/charting-m-points-2010s.csv"), encoding="utf-8", errors="replace")) if r["match_id"] == "20190714-M-Wimbledon-F-Roger_Federer-Novak_Djokovic"]
rows.sort(key=lambda r: int(r["Pt"]))
for r in rows[:2]: print(json.dumps(r))
print("## Slam PBP 2019-wimbledon-points.csv: points 1-2 of 2019-wimbledon-1701 (selected columns)")
cols = ["match_id", "ElapsedTime", "SetNo", "GameNo", "PointNumber", "PointWinner", "PointServer", "Speed_KMH", "P1Score", "P2Score", "ServeNumber", "WinnerType", "RallyCount", "P1DistanceRun", "P2DistanceRun"]
rows = [r for r in csv.DictReader(open(os.path.join(raw, "sackmann_slam_pbp_hfmirror/2019-wimbledon-points.csv"), encoding="utf-8")) if r["match_id"] == "2019-wimbledon-1701" and r["PointNumber"] in ("1", "2")]
for r in rows: print(json.dumps({c: r[c] for c in cols}))
print("## TenniSet annotations: captions.txt, points.txt (first 2 lines each)")
for fn in ("captions.txt", "points.txt"):
    for line in itertools.islice(open(os.path.join(raw, "tenniset/annotations", fn), encoding="utf-8"), 2):
        print(fn, "|", cut(line.rstrip("\n")))
v = json.load(open(os.path.join(raw, "tenniset/annotations/V006.json"), encoding="utf-8"))
print("V006.json top keys:", list(v.keys()), "classes keys:", list(v["classes"].keys()))
