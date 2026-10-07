"""Check whether clip-name numbers are frame indices: share of clips whose hit timestamps x fps fall inside
[start_frame, end_frame], for candidate fps values. Usage: python3 -I check_clip_frames.py CLIPS_JSONL"""
import json, sys
rows = [json.loads(l) for l in open(sys.argv[1], encoding="utf-8")]
for fps in (25, 29.97, 30, 50):
    ok = sum(1 for r in rows if r["first_hit_s"] is not None and r["start_frame"] <= r["first_hit_s"] * fps <= r["end_frame"]
             and r["start_frame"] <= r["last_hit_s"] * fps <= r["end_frame"])
    print(f"fps={fps}: {ok}/{len(rows)} clips have all hits inside the frame span")
dur = sum(r["end_frame"] - r["start_frame"] for r in rows) / 25
print(f"total clip duration at 25 fps: {dur:.0f} s")
