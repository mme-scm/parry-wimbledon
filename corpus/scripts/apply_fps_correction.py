"""Step 3a (after build_transcripts.py): recompute every frame-derived time field with the per-stream fps detected by
detect_fps.py. build_transcripts.py converts frames at the nominal 25 fps (corpuslib.FPS); for streams whose source video is
not 25 fps that is wrong. This step is separate and logged; raw files in corpus/raw/ are never touched and the
25-fps values are reproduced by build_transcripts.py before this step runs.
Fields recomputed (tv streams only):
  clip_start_s   = clip_start_frame / fps          clip_end_s = clip_end_frame / fps
  t_since_prev_last_hit_s = clip_start_s - (last hit of previous clip)        [video seconds]
  t_to_next_first_hit_s   = (first hit of next clip) - clip_end_s
Fields NOT frame-derived (verified unchanged by this step, asserted below): first_hit_s, last_hit_s, rally_duration_s,
  dead_time_before_s (PBP ElapsedTime gap minus previous rally duration from hit times), gap_video_prev_last_hit_to_first_attempt_s,
  and all of corpus/timing/*.csv (hit-time based; build_timing.py does not use frames).
Output: corpus/timing_corrections.log (per-stream before/after summary), rewrites transcripts/<stream>.jsonl in place
(derived, gitignored). Run: python -I corpus/scripts/apply_fps_correction.py"""
import sys, json, statistics as st
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from corpuslib import *

TR = CORPUS / "transcripts"
fpsd = json.load(open(CORPUS / "fps_by_stream.json"))["streams"]
FIELDS = ["clip_start_s", "clip_end_s", "t_since_prev_last_hit_s", "t_to_next_first_hit_s"]
NOT_CHANGED = ["first_hit_s", "last_hit_s", "rally_duration_s", "dead_time_before_s", "gap_video_prev_last_hit_to_first_attempt_s"]


def summ(v):
    v = [x for x in v if x is not None]
    if not v:
        return "n=0"
    return f"n={len(v)} min={min(v):.2f} median={st.median(v):.2f} max={max(v):.2f} frac_neg={sum(x < 0 for x in v) / len(v):.3f}"


summary = {}
log = open(CORPUS / "timing_corrections.log", "w", encoding="utf-8")
log.write("# timing_corrections.log: frame-derived time fields recomputed at the per-stream fps detected by detect_fps.py (fps_by_stream.json).\n")
log.write("# Raw TennisVL data is untouched. 'before' = frames/25 as written by build_transcripts.py; 'after' = frames/fps_detected.\n")
log.write("# Per stream: fps, then for each field: n records changed, max |after-before| (s), and a before/after distribution summary.\n")
for f in sorted(TR.glob("tv_*.jsonl")):
    stream = f.stem
    recs = [json.loads(l) for l in open(f, encoding="utf-8")]
    fps = fpsd[stream]["fps_exact"]
    before = {k: [r[k] for r in recs] for k in FIELDS}
    hits = [(r["first_hit_s"], r["last_hit_s"]) for r in recs]
    nc_before = {k: [r.get(k) for r in recs] for k in NOT_CHANGED}
    for i, r in enumerate(recs):
        r["clip_start_s"] = round(r["clip_start_frame"] / fps, 3)
        r["clip_end_s"] = round(r["clip_end_frame"] / fps, 3)
        r["t_since_prev_last_hit_s"] = None if i == 0 else round(r["clip_start_s"] - hits[i - 1][1], 3)
        r["t_to_next_first_hit_s"] = None if i + 1 == len(recs) else round(hits[i + 1][0] - r["clip_end_s"], 3)
    for k in NOT_CHANGED:
        assert nc_before[k] == [r.get(k) for r in recs], k
    log.write(f"{stream}\tfps={fps:.5f}\tn_records={len(recs)}\tdetected_share_consistent={fpsd[stream]['share_best']:.3f}\n")
    summary[stream] = {"fps": fps, "n_records": len(recs)}
    for k in FIELDS:
        pairs = [(a, r[k]) for a, r in zip(before[k], recs)]
        ch = [(a, b) for a, b in pairs if a != b]
        mx = max((abs(a - b) for a, b in ch if a is not None and b is not None), default=0.0)
        summary[stream][k] = {"n_changed": len(ch), "max_abs_change_s": round(mx, 3),
                              "frac_negative_before": round(sum(a < 0 for a, _ in pairs if a is not None) / max(1, sum(a is not None for a, _ in pairs)), 4),
                              "frac_negative_after": round(sum(b < 0 for _, b in pairs if b is not None) / max(1, sum(b is not None for _, b in pairs)), 4)}
        log.write(f"\t{k}\tn_changed={len(ch)}\tmax_abs_change_s={mx:.3f}\n\t\tbefore: {summ([a for a, _ in pairs])}\n\t\tafter:  {summ([b for _, b in pairs])}\n")
    if abs(fps - 25.0) < 1e-9:
        assert all(a == r[k] for k in FIELDS for a, r in zip(before[k], recs))
    with open(f, "w", encoding="utf-8") as fh:
        for r in recs:
            fh.write(json.dumps(r, ensure_ascii=False) + "\n")
    json.dump(summary, open(CORPUS / "reports" / "timing_corrections_summary.json", "w"), indent=1)
    print(stream, f"fps={fps:.5f}", {k: sum(a != r[k] for a, r in zip(before[k], recs)) for k in FIELDS})
