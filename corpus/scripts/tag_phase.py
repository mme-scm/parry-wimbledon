"""Step 4: heuristic rally-phase tags on text_corrected (clip level). HEURISTIC, flagged with phase_heuristic.
phase = 'clip' by default; 'between_points' when the whole text is a score call (digits/love/all/deuce/advantage/game ...);
'changeover' when a changeover cue ('changeover', 'change of ends', 'new balls', 'towel', ...) is present.
in_rally vs between_points cannot be separated at word level: there is no audio and no word timing.
Run: python -I corpus/scripts/tag_phase.py"""
import sys, json, collections
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from corpuslib import *
from textlib import phase_tags

summary = {}
for f in sorted((CORPUS / "transcripts").glob("*.jsonl")):
    recs = [json.loads(l) for l in open(f, encoding="utf-8")]
    c = collections.Counter(); tagc = collections.Counter(); cuec = collections.Counter()
    for r in recs:
        if r["medium"] != "tv":
            r["phase"] = "not_applicable_text"; r["phase_heuristic"] = False; r["phase_tags"] = []
            continue
        sn = list(r["score_before"]["sets"].keys())
        ph, tags, cues = phase_tags(r["text_corrected"] or "", sn)
        r["phase"] = ph
        r["phase_heuristic"] = ph != "clip"
        r["phase_tags"] = tags
        r["speaker_cues"] = cues
        r["speaker_role"] = "unknown"
        c[ph] += 1
        tagc.update(tags); cuec.update(cues)
    with open(f, "w", encoding="utf-8") as fh:
        for r in recs:
            fh.write(json.dumps(r, ensure_ascii=False) + "\n")
    summary[f.stem] = {"phase": dict(c), "tags": dict(tagc), "umpire_cues": dict(cuec)}
json.dump(summary, open(CORPUS / "reports" / "phase_summary.json", "w"), indent=1)
for k, v in summary.items():
    if k in ("tv_2019wimF", "tv_2023wimF"):
        print(k, v)
