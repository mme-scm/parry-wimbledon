"""Build corpus/transcripts/<stream>.jsonl (GITIGNORED: full source text) from the raw TennisVL ASR transcripts and the
Cornell live text. Step 2 of build_corpus.sh. text_corrected and phase fields are filled by later steps.
Run: python -I corpus/scripts/build_transcripts.py"""
import sys, json, csv, re, collections
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from alignlib import *
from textlib import *
import pandas as pd

OUT = CORPUS / "transcripts"
OUT.mkdir(exist_ok=True)
REP = CORPUS / "reports"

BROADCASTER_HINTS = {
    "20190714": "unnamed; probably BBC TV [unverified]. Hints in ASR text: 'Boris' (Becker) addressed 19x, 'Tim' (Henman) 7x, one 'the gentleman on my left, Tim Henman'.",
    "20230716": "unnamed; possibly a different broadcaster from the 2019 track [unverified]. Hints: 'Tim' 5x, 'Todd' 4x.",
    "20220130": "unnamed [unverified]. Hint: 'Brad' addressed 19x.",
    "20210911": "unnamed [unverified]. Hints: 'Kim' 4x, 'Amazon' 1x, 'Prime' 1x.",
}
GENERIC_BROADCASTER = "unnamed in the TennisVL files [unverified]; one TV commentary track per match"


def broadcaster(mid):
    d = mid[:8]
    if d == "20190714":
        return "unnamed; probably BBC TV [unverified]", BROADCASTER_HINTS[d]
    return (GENERIC_BROADCASTER, BROADCASTER_HINTS.get(d, "no name hints counted"))


def mcp_align_pool(tvm):
    """Align clip groups of a pool match to its MCP point sequence (key only; no clock). Returns (clip->mcp dict, info)."""
    mrows, mrow = load_mcp_match(tvm["match_id"])
    if mrows is None:
        return {}, {"mcp": False}
    from build_timing import mcp_keys  # noqa
    groups = group_clips(tvm["clips"], 6)
    mk = mcp_keys(mrows, mrow)
    # tie-breaks: reuse the PBP-style structure
    for k in mk:
        g = list(k["games"].values())
        k["tb"] = is_tiebreak(g[0], g[1], sum(k["sets"].values()) + 1, 6)
    prows = [{"elapsed_s": 0, "rally_count": None} for _ in mk]
    res = dp_align(groups, mk, prows, offset=None, allow_tb=True, tb_time_tol=1e9, nosrv=False)
    out = {}
    for gi, (pj, mt) in res.items():
        mp = mcp_parse(mrows[pj]["1st"], mrows[pj]["2nd"])
        for c in groups[gi]["clips"]:
            out[c["clip"]] = {"mcp_pt": int(mrows[pj]["Pt"]), "n_mcp": mp["n_shots"], "type": mt}
    return out, {"mcp": True, "n_groups": len(groups), "n_matched_groups": len(res), "n_mcp_points": len(mrows),
                 "n_clips": len(tvm["clips"]), "n_matched_clips": len(out)}


def build_tv_stream(tvm, cfg=None):
    mid = tvm["match_id"]
    stream = stream_name(mid)
    clips = tvm["clips"]
    texts = [c["text"] for c in clips]
    dd = dedup_stream(texts)
    bname, bhints = broadcaster(mid)
    pts = None
    clip_al = {}
    if cfg:
        pts = pd.read_csv(CORPUS / "timing" / f"points_{cfg['tag']}.csv", dtype={"mcp_1st": str, "mcp_2nd": str}).set_index("point_idx")
        clip_al = json.load(open(REP / f"clip_alignment_{cfg['tag']}.json"))
        mcp_al, mcp_info = {}, {"mcp": True}
    else:
        mcp_al, mcp_info = mcp_align_pool(tvm)
    recs = []
    pl = tvm["players"]
    for i, c in enumerate(clips):
        ss = c["score_state"]
        hits = [s["hit_timestamp_second"] for s in c["rally"]]
        k = tv_key(ss, 6 if not cfg else cfg["final_set_tb"])
        sets_sum = sum(k["sets"].values())
        gsum = sum(k["games"].values())
        role = classify_clip(c)
        r = {
            "stream": stream, "medium": "tv", "broadcaster": bname, "broadcaster_hints": bhints,
            "match_id": mid, "utt_id": f"{stream}:{i:04d}", "clip": c["clip"], "clip_i": i,
            "clip_start_frame": c["start_frame"], "clip_end_frame": c["end_frame"],
            "clip_start_s": round(c["start_frame"] / FPS, 3), "clip_end_s": round(c["end_frame"] / FPS, 3),
            "first_hit_s": min(hits), "last_hit_s": max(hits), "n_shots": len(hits), "clip_role": role,
            "rally_duration_s": round(max(hits) - min(hits), 3),
            "score_before": {"server": ss["server"], "sets": ss["sets"], "games": ss["games_in_current_set"],
                             "points": ss["points_in_current_game"]},
            "point_outcome": c["point_outcome"],
            "set_no": sets_sum + 1, "game_in_set": gsum + 1, "tiebreak_state": bool(k["tb"]),
            "text_raw": c["text"], "text_dedup": dd[i]["text_dedup"], "text_corrected": None,
            "dedup_action": dd[i]["action"], "dedup_k_removed": dd[i]["k_removed"],
            "dedup_of": None if dd[i]["dedup_of"] is None else f"{stream}:{dd[i]['dedup_of']:04d}",
            "phase": None, "phase_heuristic": None, "phase_tags": None, "speaker_role": "unknown", "speaker_cues": None,
        }
        # neighbours in the video
        r["t_since_prev_last_hit_s"] = None
        r["t_to_next_first_hit_s"] = None
        if i > 0:
            ph = max(s["hit_timestamp_second"] for s in clips[i - 1]["rally"])
            r["t_since_prev_last_hit_s"] = round(r["clip_start_s"] - ph, 3)
        if i + 1 < len(clips):
            nh = min(s["hit_timestamp_second"] for s in clips[i + 1]["rally"])
            r["t_to_next_first_hit_s"] = round(nh - r["clip_end_s"], 3)
        # alignment
        for f in ["point_idx_pbp", "point_idx_mcp", "game_no_pbp", "elapsed_prev_point_s", "elapsed_this_point_s",
                  "dead_time_before_s", "rally_count_pbp", "rally_count_mcp", "align_type", "gap_video_prev_last_hit_to_first_attempt_s"]:
            r[f] = None
        if cfg:
            al = clip_al.get(c["clip"], {})
            pi = al.get("point_idx")
            if pi is not None:
                row = pts.loc[pi]
                r["point_idx_pbp"] = int(pi)
                r["point_idx_mcp"] = int(row.mcp_pt) if pd.notna(row.mcp_pt) else None
                r["game_no_pbp"] = int(row.game_no)
                r["set_no"] = int(row.set_no)
                r["game_in_set"] = int(row.game_in_set)
                r["elapsed_this_point_s"] = int(row.elapsed_s)
                r["elapsed_prev_point_s"] = int(pts.loc[pi - 1].elapsed_s) if (pi - 1) in pts.index else None
                r["dead_time_before_s"] = None if pd.isna(row.dead_time_before_s) else round(float(row.dead_time_before_s), 2)
                r["rally_count_pbp"] = int(row.pbp_rally_count)
                r["rally_count_mcp"] = int(row.mcp_n_shots) if pd.notna(row.mcp_n_shots) else None
                r["align_type"] = row.tv_match_type
                r["gap_video_prev_last_hit_to_first_attempt_s"] = (None if pd.isna(row.gap_video_prev_last_hit_to_first_attempt_s)
                                                                   else round(float(row.gap_video_prev_last_hit_to_first_attempt_s), 2))
        else:
            m_ = mcp_al.get(c["clip"])
            if m_:
                r["point_idx_mcp"] = m_["mcp_pt"]
                r["rally_count_mcp"] = m_["n_mcp"]
                r["align_type"] = "mcp_" + m_["type"]
        recs.append(r)
    return stream, recs, mcp_info


def parse_scoreline(s):
    """Parse a Cornell scoreline like 'Djokovic 4-6 6-3 1-6 2-1* Nadal' / 'Federer 6-3 *0-1 Gasquet'.
    '*' position marks the server side (heuristic reading: before the final score token = first-named player;
    after = second-named) [unverified; README of the dataset does not define it]."""
    m = re.match(r"^(?P<a>.+?) (?P<sc>(?:\*?(?:\[\d+\])?\d+-\d+(?:\(\d+\))?\*?\s?)+)(?P<b>.+)$", s)
    if not m:
        return None
    toks = m.group("sc").split()
    parsed = []
    star = None
    for t in toks:
        pre, post = t.startswith("*"), t.endswith("*")
        core = t.strip("*")
        mm = re.match(r"(?:\[(\d+)\])?(\d+)-(\d+)(?:\((\d+)\))?$", core)
        if not mm:
            return None
        parsed.append([int(mm.group(2)), int(mm.group(3))])
        if pre or post:
            star = "left" if pre else "right"
    return {"player_a": m.group("a").strip(), "player_b": m.group("b").strip(),
            "completed_sets": parsed[:-1], "current_set_games": parsed[-1], "server_marker_side": star,
            "n_set_tokens": len(parsed)}


def build_cornell():
    data = json.load(open(CORNELL, encoding="utf-8"))
    recs = []
    nparsed = 0
    for i, d in enumerate(data):
        p = parse_scoreline(d["scoreline"])
        nparsed += p is not None
        t = d["commentary"]
        r = {"stream": "text_cornell", "medium": "text",
             "broadcaster": "Sports Mole live text (per Cornell dataset README; written, not speech) [source site not independently verified]",
             "broadcaster_hints": "", "match_id": None, "utt_id": f"text_cornell:{i:05d}", "gender": d["gender"],
             "scoreline_raw": d["scoreline"], "players": None if p is None else [p["player_a"], p["player_b"]],
             "score": p, "text_raw": t, "text_dedup": t, "text_corrected": t,
             "dedup_action": "not_applicable_text", "dedup_k_removed": 0,
             "phase": None, "phase_heuristic": None, "phase_tags": None}
        recs.append(r)
    return recs, nparsed


if __name__ == "__main__":
    tv = load_tennisvl()
    summary = {}
    for tvm in tv:
        cfg = MAIN if tvm["match_id"] == MAIN_ID else HELD if tvm["match_id"] == HELD_ID else None
        stream, recs, info = build_tv_stream(tvm, cfg)
        with open(OUT / f"{stream}.jsonl", "w", encoding="utf-8") as f:
            for r in recs:
                f.write(json.dumps(r, ensure_ascii=False) + "\n")
        cnt = collections.Counter(r["dedup_action"] for r in recs)
        summary[stream] = {"n": len(recs), "dedup_actions": dict(cnt),
                           "n_exact_repeats_beyond_max_distance_not_removed": diag_repeats([c["text"] for c in tvm["clips"]]), "mcp_info": info,
                           "n_aligned_pbp": sum(r["point_idx_pbp"] is not None for r in recs),
                           "n_aligned_mcp": sum(r["point_idx_mcp"] is not None for r in recs)}
        print(stream, len(recs), dict(cnt), info)
    recs, nparsed = build_cornell()
    with open(OUT / "text_cornell.jsonl", "w", encoding="utf-8") as f:
        for r in recs:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    summary["text_cornell"] = {"n": len(recs), "n_scoreline_parsed": nparsed}
    print("text_cornell", len(recs), nparsed)
    json.dump(summary, open(REP / "build_transcripts_summary.json", "w"), indent=1)
