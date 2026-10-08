"""Step 3a: detect the video frame rate of each TennisVL stream from the raw data.
For every clip, the clip name carries start_frame/end_frame; hit_timestamp_second are seconds in the source video.
A frame rate fps is CONSISTENT with a clip if all hit_timestamp_second lie inside [start_frame/fps, end_frame/fps]
(plus/minus TOL seconds). Candidates tested: 25, 29.97 (30000/1001), 30 (also 24, 23.976, 50, 59.94, 60 for completeness).
The stream fps is the candidate (25, 29.97, 30 only) with the highest share of consistent clips, provided that share is
>= 0.95; otherwise the stream is flagged NONSTANDARD and the fps is taken from the feasible interval (see below).
For every stream the feasible interval of fps values consistent with ALL clips is also computed:
fps >= max(start_frame/(first hit + TOL)) and fps <= min(end_frame/(last hit - TOL)); an empty interval is reported.
Also reports the least-squares slope (frames per second) of start_frame against first-hit time as an independent estimate.
Output: corpus/fps_by_stream.json (committed, derived), read by apply_fps_correction.py and make_manifest.py.
Reads raw data only. Run: python -I corpus/scripts/detect_fps.py"""
import sys, json
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from corpuslib import *
import numpy as np

CAND = [25.0, 30000 / 1001, 30.0]
EXTRA = [29.0, 24.0, 24000 / 1001, 50.0, 60000 / 1001, 60.0]
TOL = 0.01  # seconds; hit_timestamp_second is rounded to 0.01 s


def share(clips, fps, tol=TOL):
    ok = 0
    for c in clips:
        t = [s["hit_timestamp_second"] for s in c["rally"]]
        if c["start_frame"] / fps - tol <= min(t) and max(t) <= c["end_frame"] / fps + tol:
            ok += 1
    return ok


out = {"method": "share of clips whose hit_timestamp_second values all fall inside [start_frame/fps, end_frame/fps]; "
                 "decision: candidate in {25, 29.97, 30} with the highest share",
       "tolerance_s": TOL, "streams": {}}
for m in load_tennisvl():
    stream = stream_name(m["match_id"])
    clips = m["clips"]
    n = len(clips)
    sh = {f"{f:.3f}": share(clips, f) / n for f in CAND + EXTRA}
    cnt = {f"{f:.3f}": share(clips, f) for f in CAND + EXTRA}
    x = np.array([c["start_frame"] for c in clips], float)
    y = np.array([min(s["hit_timestamp_second"] for s in c["rally"]) for c in clips], float)
    slope = float(np.polyfit(y, x, 1)[0])  # frames per second
    best = max(CAND, key=lambda f: cnt[f"{f:.3f}"])
    t1 = np.array([max(s["hit_timestamp_second"] for s in c["rally"]) for c in clips], float)
    e = np.array([c["end_frame"] for c in clips], float)
    lo = float(np.max(x / (y + TOL))); hi = float(np.min(e / np.maximum(t1 - TOL, 1e-9)))
    nonstd = sh[f"{best:.3f}"] < 0.95
    if nonstd and lo <= hi:
        best = round((lo + hi) / 2, 2)
        cnt[f"{best:.3f}"] = share(clips, best); sh[f"{best:.3f}"] = cnt[f"{best:.3f}"] / n
    ranked = sorted(CAND, key=lambda f: -cnt[f"{f:.3f}"])
    margin = cnt[f"{ranked[0]:.3f}"] - cnt[f"{ranked[1]:.3f}"]
    out["streams"][stream] = {
        "match_id": m["match_id"], "n_clips": n, "fps": round(best, 3), "fps_exact": best, "fps_nominal": str(round(best, 2)),
        "share_consistent": sh, "n_consistent": cnt, "slope_frames_per_s_start_vs_first_hit": round(slope, 3),
        "feasible_fps_interval_all_clips": [round(lo, 4), round(hi, 4)], "feasible_interval_nonempty": bool(lo <= hi),
        "margin_clips_over_runner_up": margin, "share_best": sh[f"{best:.3f}"],
        "flag": ("NONSTANDARD" if nonstd else "ok" if sh[f"{best:.3f}"] >= 0.95 else "REVIEW")}
json.dump(out, open(CORPUS / "fps_by_stream.json", "w"), indent=1)
print(f"{'stream':70s} n  share25 share29.97 share30 share29.0 slope fps feasible_interval flag")
for s, d in out["streams"].items():
    sh = d["share_consistent"]
    print(f"{s[:70]:70s} {d['n_clips']:4d} {sh['25.000']:.3f} {sh['29.970']:.3f} {sh['30.000']:.3f} {sh['29.000']:.3f} {d['slope_frames_per_s_start_vs_first_hit']:.2f} {d['fps']} {d['feasible_fps_interval_all_clips']} {d['flag']}")
