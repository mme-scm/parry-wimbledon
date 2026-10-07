"""Extract per-clip ASR transcripts from TennisVL test_stats JSON for one match.
Usage: python3 -I tennisvl_transcripts.py FILE match_idx out.jsonl
Writes jsonl with: clip, start_frame, end_frame, first_hit_s, last_hit_s, score_state, transcript, synthetic_commentary."""
import json, sys, ast, re
data = json.load(open(sys.argv[1], encoding="utf-8"))
rec = data[int(sys.argv[2])]
conv = rec["conversations"]
humans = [t["value"] for t in conv if t["from"] == "human"]
gpts = [t["value"] for t in conv if t["from"] == "gpt"]
assert len(humans) == len(gpts) == len(rec["videos"])
with open(sys.argv[3], "w", encoding="utf-8") as f:
    for v, h, g in zip(rec["videos"], humans, gpts):
        m = re.search(r"_(\d+)_(\d+)\.mp4$", v)
        hd = ast.literal_eval(h.split("Metadata:", 1)[1].strip())
        com, _, meta = g.partition("\n\nMetadata:")
        gd = ast.literal_eval(meta.strip()) if meta else {}
        hits = [s["hit_timestamp_second"] for s in hd["rally"]]
        f.write(json.dumps({
            "clip": v.split("/")[-1], "start_frame": int(m.group(1)), "end_frame": int(m.group(2)),
            "first_hit_s": min(hits) if hits else None, "last_hit_s": max(hits) if hits else None,
            "score_state": hd["score_state"], "point_outcome": hd.get("point_outcome"),
            "transcript": gd.get("audio_transcription (background context)", ""),
            "synthetic_commentary": com.strip()}, ensure_ascii=False) + "\n")
