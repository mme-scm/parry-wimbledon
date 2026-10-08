"""Step 5: corpus/transcripts/manifest.json and meta_<stream>.csv (all fields except the text fields).
Run: python -I corpus/scripts/make_manifest.py"""
import sys, json, csv, hashlib
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from corpuslib import *
from textlib import words

TR = CORPUS / "transcripts"
TEXT_FIELDS = ["text_raw", "text_dedup", "text_corrected"]


def sha(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


FPS_BY = json.load(open(CORPUS / "fps_by_stream.json"))["streams"]
manifest = {"note": "jsonl files are gitignored (full source text); this manifest and meta_<stream>.csv are committed",
            "word_definition": "regex [A-Za-z0-9]+(?:['-][A-Za-z0-9]+)*  (digits count as words)", "streams": {}}
for f in sorted(TR.glob("*.jsonl")):
    recs = [json.loads(l) for l in open(f, encoding="utf-8")]
    nw = {k: 0 for k in ("raw", "dedup", "corrected")}
    nonempty = 0
    flat = []
    for r in recs:
        a, b, c = (len(words(r["text_raw"])), len(words(r["text_dedup"])), len(words(r["text_corrected"] or "")))
        nw["raw"] += a; nw["dedup"] += b; nw["corrected"] += c
        nonempty += a > 0
        d = {k: v for k, v in r.items() if k not in TEXT_FIELDS}
        d["n_words_raw"], d["n_words_dedup"], d["n_words_corrected"] = a, b, c
        for k, v in list(d.items()):
            if isinstance(v, (dict, list)):
                d[k] = json.dumps(v, ensure_ascii=False)
        flat.append(d)
    cols = list(flat[0].keys())
    with open(TR / f"meta_{f.stem}.csv", "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=cols)
        w.writeheader()
        w.writerows(flat)
    manifest["streams"][f.stem] = {"medium": recs[0]["medium"], "n_records": len(recs), "n_records_nonempty_text": nonempty,
                                   "n_words_raw": nw["raw"], "n_words_dedup": nw["dedup"], "n_words_corrected": nw["corrected"],
                                   "sha256_jsonl": sha(f),
                                   **({"video_fps": FPS_BY[f.stem]["fps"],
                                       "fps_share_clips_consistent": round(FPS_BY[f.stem]["share_best"], 4),
                                       "fps_source": "detect_fps.py: hit_timestamp_second inside [start_frame/fps, end_frame/fps] (corpus/fps_by_stream.json); frame-derived times corrected by apply_fps_correction.py (corpus/timing_corrections.log)"}
                                      if f.stem in FPS_BY else {"video_fps": None, "fps_source": "not applicable (written text)"}),
                                   "fields": [k for k in recs[0].keys()]}
manifest["inputs_sha256"] = {
    "tennis_data_test_stats_.json": sha(TV_JSON),
    "2019-wimbledon-points.csv": sha(PBP_DIR / "2019-wimbledon-points.csv"),
    "2023-wimbledon-points.csv": sha(PBP_DIR / "2023-wimbledon-points.csv"),
    "text_commentaries.json": sha(CORNELL),
    "corrections_rules.tsv": sha(CORPUS / "corrections_rules.tsv"),
}
json.dump(manifest, open(TR / "manifest.json", "w"), indent=1)
for k, v in manifest["streams"].items():
    print(k, v["n_records"], v["n_records_nonempty_text"], v["n_words_raw"], v["n_words_dedup"], v["n_words_corrected"])
