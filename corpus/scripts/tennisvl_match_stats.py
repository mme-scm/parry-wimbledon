"""Per-match counts for a TennisVL sharegpt JSON that embeds
'audio_transcription (background context)' in gpt turns.
Usage: python3 -I tennisvl_match_stats.py FILE [out.tsv]
Outputs per match: id, clips, gpt turns, non-empty transcripts, transcript words,
synthetic-commentary words, shots, first/last hit timestamp (s), clip-span coverage."""
import json, sys, ast, re
path = sys.argv[1]
out = sys.argv[2] if len(sys.argv) > 2 else None
data = json.load(open(path, encoding="utf-8"))
TKEY = "'audio_transcription (background context)'"
rows = []
for i, rec in enumerate(data):
    vids = rec["videos"]
    mid = re.sub(r"_\d+_\d+\.mp4$", "", vids[0].split("/")[-1])
    ids = {re.sub(r"_\d+_\d+\.mp4$", "", v.split("/")[-1]) for v in vids}
    gpts = [t["value"] for t in rec["conversations"] if t["from"] == "gpt"]
    humans = [t["value"] for t in rec["conversations"] if t["from"] == "human"]
    n_tr = tr_words = com_words = 0
    for g in gpts:
        com, _, meta = g.partition("\n\nMetadata:")
        com_words += len(com.split())
        if meta:
            try:
                d = ast.literal_eval(meta.strip())
                tr = d.get("audio_transcription (background context)", "")
            except Exception:
                tr = ""
            if tr and tr.strip():
                n_tr += 1
                tr_words += len(tr.split())
    shots = 0; ts = []
    for h in humans:
        meta = h.split("Metadata:", 1)[1].strip()
        d = ast.literal_eval(meta)
        for sh in d["rally"]:
            shots += 1
            if sh.get("hit_timestamp_second") is not None:
                ts.append(sh["hit_timestamp_second"])
    # clip frame spans
    spans = []
    for v in vids:
        m = re.search(r"_(\d+)_(\d+)\.mp4$", v)
        spans.append((int(m.group(1)), int(m.group(2))))
    fr = sum(b - a for a, b in spans)
    rows.append((i, mid, len(ids), len(vids), len(gpts), n_tr, tr_words, com_words, shots,
                 min(ts) if ts else None, max(ts) if ts else None, fr, min(a for a, _ in spans), max(b for _, b in spans)))
hdr = ["idx", "match_id", "n_ids", "clips", "gpt_turns", "nonempty_transcripts", "transcript_words",
       "synthetic_commentary_words", "shots", "first_hit_s", "last_hit_s", "clip_frames_total", "first_frame", "last_frame"]
lines = ["\t".join(hdr)] + ["\t".join(str(x) for x in r) for r in rows]
print("\n".join(lines))
if out:
    open(out, "w", encoding="utf-8").write("\n".join(lines) + "\n")
