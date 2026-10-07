"""Join TennisVL clips, Sackmann slam PBP and Match Charting Project per point, for the 2019 and 2023 Wimbledon finals.
Outputs: corpus/timing/points_<tag>.csv, shots_<tag>.csv, corpus/reports/timing_report_<tag>.json,
         corpus/reports/unmatched_<tag>.tsv, and a pickle-free alignment file corpus/reports/clip_alignment_<tag>.json
         (clip -> point index) used by build_transcripts.py.
Run: python -I corpus/scripts/build_timing.py
"""
import sys, json, csv, statistics as st
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from alignlib import *
import numpy as np

OUT_T = CORPUS / "timing"
OUT_R = CORPUS / "reports"
OUT_T.mkdir(exist_ok=True); OUT_R.mkdir(exist_ok=True)


def mcp_keys(rows, mrow):
    s1, s2 = surname_key(mrow["Player 1"]), surname_key(mrow["Player 2"])
    out = []
    for r in rows:
        svr = int(r["Svr"])
        a, b = r["Pts"].split("-")
        a, b = norm_point_token(a), norm_point_token(b)
        p1, p2 = (a, b) if svr == 1 else (b, a)
        out.append({"server": s1 if svr == 1 else s2,
                    "sets": {s1: int(r["Set1"]), s2: int(r["Set2"])},
                    "games": {s1: int(r["Gm1"]), s2: int(r["Gm2"])},
                    "pts": {s1: p1, s2: p2}})
    return out


def robust_levels(matches, groups, rows, jump=5.0, agree=3.0):
    """Segment the sequence of residuals (video first-attempt time minus PBP ElapsedTime) into constant-offset
    segments. A new segment starts when a residual departs from the current level by more than `jump` seconds
    AND the next matched residual agrees with it within `agree` seconds (isolated departures are outliers).
    Returns list of (point_index, residual, segment_level, segment_id); level = median residual of the segment."""
    items = sorted((pj, groups[gi]["first_attempt_s"] - rows[pj]["elapsed_s"]) for gi, (pj, _) in matches.items())
    seg_of = []
    seg = 0
    cur = [items[0][1]]
    seg_of.append(0)
    for k in range(1, len(items)):
        r = items[k][1]
        level = float(np.median(cur[-5:]))
        nxt = items[k + 1][1] if k + 1 < len(items) else None
        if abs(r - level) > jump and nxt is not None and abs(nxt - r) <= agree:
            seg += 1
            cur = [r]
        elif abs(r - level) > jump and nxt is None:
            pass
        else:
            if abs(r - level) <= jump:
                cur.append(r)
        seg_of.append(seg)
    # segments supported by fewer than 3 anchors are not trusted: merged into the preceding segment
    cnt = {}
    for sg in seg_of:
        cnt[sg] = cnt.get(sg, 0) + 1
    prev_ok = 0
    fixed = []
    for sg in seg_of:
        if cnt[sg] >= 3:
            prev_ok = sg
        fixed.append(prev_ok)
    seg_of = fixed
    # merge neighbouring segments whose levels differ by <= jump (a spurious split)
    def lev_of(sg):
        v = [r for (pj, r), s_ in zip(items, seg_of) if s_ == sg]
        return float(np.median(v))
    merged = []
    last = None
    for sg in seg_of:
        if last is None:
            last = sg
        elif sg != last and abs(lev_of(sg) - lev_of(last)) <= jump:
            pass  # stay in `last`
        else:
            last = sg
        merged.append(last)
    seg_of = merged
    lv = {}
    for (pj, r), sg in zip(items, seg_of):
        lv.setdefault(sg, []).append(r)
    # level = median of residuals within `jump` of the segment's median
    seg_level = {}
    for sg, v in lv.items():
        med = float(np.median(v))
        core = [x for x in v if abs(x - med) <= jump]
        seg_level[sg] = float(np.median(core))
    return [(pj, r, seg_level[sg], sg) for (pj, r), sg in zip(items, seg_of)]


def make_offset_fn(levels, nrows):
    """Piecewise-constant: offset at point j = level of nearest anchor (by point index)."""
    idx = np.array([l[0] for l in levels])
    lev = np.array([l[2] for l in levels])

    def f(j):
        k = int(np.argmin(np.abs(idx - j)))
        return float(lev[k])
    return f


def segments(levels, jump=5.0):
    segs = []
    prev = None
    n = {}
    for pj, r, lev, sg in levels:
        n[sg] = n.get(sg, 0) + 1
        if not segs or segs[-1]["id"] != sg:
            segs.append({"id": sg, "start_point": pj + 1, "level_s": round(lev, 2),
                         "jump_s": None if prev is None else round(lev - prev, 2)})
        prev = lev
    for sgd in segs:
        sgd["n_anchors"] = n[sgd["id"]]
    return segs


def fmt(x, nd=2):
    return "" if x is None else (round(x, nd) if isinstance(x, float) else x)


def build(cfg):
    tag = cfg["tag"]
    tv = [m for m in load_tennisvl() if m["match_id"] == cfg["id"]][0]
    rows, p1, p2, pinfo = load_pbp(cfg)
    ftb = cfg["final_set_tb"]
    pk = pbp_keys(rows, p1, p2, ftb)
    groups = group_clips(tv["clips"], ftb)
    report = {"match": cfg["id"], "pbp_id": cfg["pbp_id"], "p1": p1, "p2": p2, "pbp": pinfo,
              "n_clips": len(tv["clips"]), "n_groups": len(groups), "n_points_pbp": len(rows)}
    role_counts = {}
    for c in tv["clips"]:
        role_counts[c["role"]] = role_counts.get(c["role"], 0) + 1
    report["clip_roles"] = role_counts

    # ---- pass 1: key only, no time
    r1 = dp_align(groups, pk, rows, offset=None, allow_tb=False)
    levels = robust_levels(r1, groups, rows)
    segs = segments(levels)
    report["pass1_matched_groups"] = len(r1)
    # where do the cuts fall? A changeover (end of an odd game, set end, or tie-break at 6 points) in the interval
    # between the last anchor of the previous segment and the first anchor of the new one?
    anchors = [(l[0], l[3]) for l in levels]
    for k, sgd in enumerate(segs):
        if k == 0:
            sgd["cut_interval_points"] = None
            sgd["changeover_or_set_break_in_interval"] = None
            continue
        prev_last = max(pj for pj, sg in anchors if sg == segs[k - 1]["id"])
        first_new = min(pj for pj, sg in anchors if sg == sgd["id"])
        lo, hi = prev_last, first_new  # 0-based indices; the cut lies after point lo and before point hi
        found = False
        for jj in range(lo, hi):
            r_ = rows[jj]
            nxt = rows[jj + 1] if jj + 1 < len(rows) else None
            if nxt is None:
                continue
            if nxt["game_no"] != r_["game_no"]:
                gsum = r_["p1_games_after"] + r_["p2_games_after"]
                if r_["set_winner"] in (1, 2) or gsum % 2 == 1:
                    found = True
            elif r_["before"]["games"][0] == r_["before"]["games"][1] and is_tiebreak(
                    r_["before"]["games"][0], r_["before"]["games"][1], r_["before"]["sets"][0] + r_["before"]["sets"][1] + 1, cfg["final_set_tb"]):
                tbp = int(r_["before"]["pts"][0]) + int(r_["before"]["pts"][1]) + 1
                if tbp % 6 == 0:
                    found = True
        sgd["cut_interval_points"] = [lo + 1, hi + 1]
        sgd["changeover_or_set_break_in_interval"] = found
    report["offset_segments"] = segs
    report["n_cuts"] = len(segs) - 1
    report["n_cuts_with_changeover_in_interval"] = sum(1 for sgd in segs[1:] if sgd["changeover_or_set_break_in_interval"])
    stepwise = len(segs) > 1
    off_fn = make_offset_fn(levels, len(rows))
    # ---- pass 2: add tie-break pairs and time consistency
    tol = 130.0 if stepwise else 20.0
    r2 = dp_align(groups, pk, rows, offset=off_fn, allow_tb=True, tb_time_tol=tol, nosrv=True)
    report["tb_time_tolerance_s"] = tol
    report["pass2_matched_groups"] = len(r2)
    report["match_types"] = {}
    for gi, (pj, mt) in r2.items():
        report["match_types"][mt] = report["match_types"].get(mt, 0) + 1
    point_to_group = {pj: gi for gi, (pj, mt) in r2.items()}
    # ---- MCP
    mrows, mrow = load_mcp_match(cfg["id"])
    mk = mcp_keys(mrows, mrow)
    mcp_rate = {"n_mcp": len(mrows), "n_pbp": len(rows)}
    pk_t = [key_tuple(k) for k in pk]
    # PBP/MCP name-orientation check
    mk_t = [key_tuple(k) for k in mk]
    same_idx = 0
    mism = []
    for i in range(min(len(mk_t), len(pk_t))):
        if mk_t[i] == pk_t[i]:
            same_idx += 1
        else:
            mism.append(i + 1)
    mcp_rate["key_equal_at_same_index"] = same_idx
    mcp_rate["mismatch_points"] = mism
    mcp_rate["join_key"] = "server surname + sets + games + points (before point), occurrence order; MCP Pts is server-first"
    # resync via DP when counts differ or mismatches exist (key-only, with tie-break soft)
    mcp_map = {i: i for i in range(min(len(mk_t), len(pk_t)))}
    report["mcp_vs_pbp"] = mcp_rate

    # ---- final offset stats
    first_attempt_resid = []
    final_clip_resid = []
    for gi, (pj, mt) in r2.items():
        g = groups[gi]
        off = off_fn(pj)
        first_attempt_resid.append(g["first_attempt_s"] - rows[pj]["elapsed_s"] - off)
        if g["has_rally_clip"]:
            final_clip_resid.append(g["first_hit_s"] - rows[pj]["elapsed_s"] - off)
    # stats of raw residual (video first_attempt minus elapsed), by local level
    raw = sorted((rows[pj]["elapsed_s"], groups[gi]["first_attempt_s"] - rows[pj]["elapsed_s"],
                  groups[gi]["has_rally_clip"] and len(groups[gi]["clips"]) > 1, mt)
                 for gi, (pj, mt) in r2.items())
    x = np.array([r[0] for r in raw], float); y = np.array([r[1] for r in raw], float)
    level = np.array([off_fn(pj) for gi, (pj, mt) in sorted(r2.items(), key=lambda kv: rows[kv[1][0]]["elapsed_s"])])
    res = y - level
    inl = np.abs(res) <= 3.0
    stats = {
        "n_matched_groups": int(len(x)),
        "residual_sd_all_s": float(np.std(res, ddof=1)),
        "residual_mad_sd_s": float(1.4826 * np.median(np.abs(res - np.median(res)))),
        "n_within_3s": int(inl.sum()), "frac_within_3s": float(inl.mean()),
        "residual_sd_within_3s_s": float(np.std(res[inl], ddof=1)),
        "n_outliers_gt_3s": int((~inl).sum()),
    }
    if not stepwise:
        # linear fit on inliers: video_s = a + b * elapsed_s
        b, a = np.polyfit(x[inl], y[inl] + x[inl], 1)
        fit_res = (y[inl] + x[inl]) - (a + b * x[inl])
        stats["linear_fit"] = {"intercept_s": float(a), "slope": float(b),
                               "residual_sd_s": float(np.std(fit_res, ddof=2)), "n": int(inl.sum()),
                               "offset_slope1_median_s": float(np.median(y[inl])),
                               "offset_slope1_sd_s": float(np.std(y[inl], ddof=1))}
    else:
        # within-segment SD about the segment median
        stats["stepwise_note"] = "video offset is piecewise constant (cuts); SD is about the local level"
        stats["n_segments"] = len(segs)
    # outliers by group type: fault clip + rally clip vs rally clip only vs other
    outl = {"with_fault_clip": [0, 0], "without_fault_clip": [0, 0]}
    for (gi, (pj, mt)), r in zip(sorted(r2.items(), key=lambda kv: rows[kv[1][0]]["elapsed_s"]), res):
        k = "with_fault_clip" if groups[gi]["clips"][0]["role"] == "first_serve_fault" else "without_fault_clip"
        outl[k][0] += 1
        outl[k][1] += int(abs(r) > 3.0)
    stats["outliers_by_group_type[n,n_gt3s]"] = outl
    report["offset"] = stats

    # unmatched
    matched_groups = set(r2)
    um = []
    for gi, g in enumerate(groups):
        if gi not in matched_groups:
            k = g["key"]
            um.append({"group": gi, "clips": ";".join(c["clip"].split("_")[-2] + "_" + c["clip"].split("_")[-1][:-4] for c in g["clips"]),
                       "first_attempt_s": g["first_attempt_s"], "server": k["server"],
                       "sets": json.dumps(k["sets"]), "games": json.dumps(k["games"]), "pts": json.dumps(k["pts"]),
                       "n_shots": g["n_shots"], "tb": k["tb"]})
    report["n_unmatched_groups"] = len(um)
    report["n_unmatched_clips"] = int(sum(len(groups[u["group"]]["clips"]) for u in um))
    report["n_matched_clips"] = int(sum(len(groups[gi]["clips"]) for gi in matched_groups))
    with open(OUT_R / f"unmatched_{tag}.tsv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(um[0].keys()) if um else ["group"], delimiter="\t")
        w.writeheader(); [w.writerow(u) for u in um]

    # ---- points table
    s1, s2 = surname_key(p1), surname_key(p2)
    names = {1: p1, 2: p2}
    prow_out = []
    prev_rally_dur = None
    prev_last_hit = None
    prev_elapsed = None
    prev_g = None
    shots_out = []
    clip_align = {}
    for j, r in enumerate(rows):
        b = r["before"]
        gi = point_to_group.get(j)
        g = groups[gi] if gi is not None else None
        mi = mcp_map.get(j)
        mr = mrows[mi] if mi is not None else None
        mp = mcp_parse(mr["1st"], mr["2nd"]) if mr is not None else None
        d = {
            "point_idx": r["pbp_point"], "set_no": r["set_no"], "game_no": r["game_no"],
            "game_in_set": b["games"][0] + b["games"][1] + 1,
            "tiebreak": is_tiebreak(b["games"][0], b["games"][1], b["sets"][0] + b["sets"][1] + 1, ftb),
            "p1_name": p1, "p2_name": p2, "server": names[r["server"]], "server_pbp": r["server"],
            "sets_before_p1": b["sets"][0], "sets_before_p2": b["sets"][1],
            "games_before_p1": b["games"][0], "games_before_p2": b["games"][1],
            "pts_before_p1": b["pts"][0], "pts_before_p2": b["pts"][1],
            "point_winner": names[r["winner"]],
            "pbp_elapsed": r["elapsed_raw"], "elapsed_s": r["elapsed_s"],
            "pbp_speed_kmh": r["speed_kmh"], "pbp_serve_number": r["serve_number"],
            "pbp_winner_type": r["winner_type"], "pbp_rally_count": r["rally_count"],
            "pbp_p1_score_after": r["p1_score_after"], "pbp_p2_score_after": r["p2_score_after"],
        }
        if mr is not None:
            d.update({"mcp_pt": mr["Pt"], "mcp_pts": mr["Pts"], "mcp_gm_no": mr["Gm#"], "mcp_svr": mr["Svr"],
                      "mcp_1st": mr["1st"], "mcp_2nd": mr["2nd"], "mcp_ptwinner": mr["PtWinner"],
                      "mcp_n_shots": mp["n_shots"], "mcp_double_fault": int(mp["double_fault"]),
                      "mcp_ace": int(mp["ace"]), "mcp_key_match": int(mk_t[mi] == pk_t[j])})
        else:
            d.update({k: "" for k in ["mcp_pt", "mcp_pts", "mcp_gm_no", "mcp_svr", "mcp_1st", "mcp_2nd", "mcp_ptwinner",
                                      "mcp_n_shots", "mcp_double_fault", "mcp_ace", "mcp_key_match"]})
        gap_pbp = None if prev_elapsed is None else r["elapsed_s"] - prev_elapsed
        d["gap_pbp_prev_point_s"] = gap_pbp
        d["dead_time_before_s"] = (None if (gap_pbp is None or prev_rally_dur is None) else gap_pbp - prev_rally_dur)
        d["prev_rally_duration_s"] = prev_rally_dur
        if g is not None:
            final = g["clips"][-1]
            hits = [s["hit_timestamp_second"] for s in final["rally"]] if g["has_rally_clip"] else []
            off = off_fn(j)
            d.update({
                "tv_match_type": r2[gi][1], "tv_n_clips": len(g["clips"]),
                "tv_clip_fault": g["clips"][0]["clip"] if g["clips"][0]["role"] == "first_serve_fault" else "",
                "tv_clip_rally": final["clip"] if g["has_rally_clip"] else "",
                "tv_first_attempt_s": g["first_attempt_s"],
                "tv_first_hit_s": g["first_hit_s"], "tv_last_hit_s": g["last_hit_s"], "tv_n_shots": g["n_shots"],
                "tv_hit_times": json.dumps(hits), "tv_point_outcome": final["point_outcome"] if g["has_rally_clip"] else "",
                "tv_rally_duration_s": (g["last_hit_s"] - g["first_hit_s"]) if g["has_rally_clip"] else None,
                "offset_used_s": off, "resid_s": g["first_attempt_s"] - r["elapsed_s"] - off,
                "timing_source": "tennisvl_hit_times" if g["has_rally_clip"] else "tennisvl_fault_clip_only",
                "est_video_serve_s": r["elapsed_s"] + off,
            })
            if prev_g is not None and prev_g["has_rally_clip"]:
                d["gap_video_prev_last_hit_to_first_attempt_s"] = g["first_attempt_s"] - prev_g["last_hit_s"]
            for c in g["clips"]:
                clip_align[c["clip"]] = {"point_idx": r["pbp_point"], "role": c["role"]}
                prev_s = None
                for s in c["rally"]:
                    t = s["hit_timestamp_second"]
                    shots_out.append({"clip": c["clip"], "clip_role": c["role"], "point_idx": r["pbp_point"],
                                      "shot_index": s["shot_index"], "hitter": s["hitter"], "type": s["type"],
                                      "wing": s.get("wing"), "technique": s.get("technique"),
                                      "direction_rough": s.get("direction_rough"),
                                      "hit_timestamp_second": t,
                                      "bounce_timestamp_second": s.get("bounce_timestamp_second"),
                                      "shot_outcome": s.get("shot_outcome"),
                                      "inter_shot_interval_s": None if prev_s is None else round(t - prev_s, 2)})
                    prev_s = t
        else:
            d.update({k: "" for k in ["tv_match_type", "tv_n_clips", "tv_clip_fault", "tv_clip_rally", "tv_first_attempt_s",
                                      "tv_first_hit_s", "tv_last_hit_s", "tv_n_shots", "tv_hit_times", "tv_point_outcome",
                                      "tv_rally_duration_s", "offset_used_s", "resid_s", "gap_video_prev_last_hit_to_first_attempt_s"]})
            d["timing_source"] = "pbp_elapsed_only"
            d["est_video_serve_s"] = r["elapsed_s"] + off_fn(j)
        if "gap_video_prev_last_hit_to_first_attempt_s" not in d:
            d["gap_video_prev_last_hit_to_first_attempt_s"] = ""
        prev_elapsed = r["elapsed_s"]
        if g is not None and g["has_rally_clip"]:
            prev_rally_dur = g["last_hit_s"] - g["first_hit_s"]
        else:
            prev_rally_dur = None
        prev_g = g
        prow_out.append(d)
    # unaligned clips
    for g in groups:
        for c in g["clips"]:
            clip_align.setdefault(c["clip"], {"point_idx": None, "role": c["role"]})
    cols = list(prow_out[0].keys())
    with open(OUT_T / f"points_{tag}.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=cols)
        w.writeheader()
        for d in prow_out:
            w.writerow({k: fmt(v) for k, v in d.items()})
    # shots for clips that are not aligned to any point (so every shot is listed)
    aligned_clips = {s["clip"] for s in shots_out}
    for g in groups:
        for c in g["clips"]:
            if c["clip"] in aligned_clips:
                continue
            prev_s = None
            for s in c["rally"]:
                t = s["hit_timestamp_second"]
                shots_out.append({"clip": c["clip"], "clip_role": c["role"], "point_idx": "",
                                  "shot_index": s["shot_index"], "hitter": s["hitter"], "type": s["type"],
                                  "wing": s.get("wing"), "technique": s.get("technique"),
                                  "direction_rough": s.get("direction_rough"), "hit_timestamp_second": t,
                                  "bounce_timestamp_second": s.get("bounce_timestamp_second"),
                                  "shot_outcome": s.get("shot_outcome"),
                                  "inter_shot_interval_s": None if prev_s is None else round(t - prev_s, 2)})
                prev_s = t
    shots_out.sort(key=lambda s: (s["hit_timestamp_second"], s["shot_index"]))
    with open(OUT_T / f"shots_{tag}.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(shots_out[0].keys()))
        w.writeheader()
        for s in shots_out:
            w.writerow({k: fmt(v) for k, v in s.items()})
    report["n_shots_total"] = len(shots_out)
    report["n_points_with_clip"] = sum(1 for d in prow_out if d["tv_match_type"] != "")
    report["n_points_with_rally_clip"] = sum(1 for d in prow_out if d["tv_clip_rally"] != "")
    report["points_match_rate_clips"] = report["n_matched_clips"] / report["n_clips"]
    report["points_coverage_pbp"] = report["n_points_with_clip"] / len(rows)
    # pbp/mcp numbers
    report["mcp_key_match_rate"] = sum(1 for d in prow_out if d["mcp_key_match"] == 1) / len(rows)
    json.dump(clip_align, open(OUT_R / f"clip_alignment_{tag}.json", "w"), indent=0)
    json.dump(report, open(OUT_R / f"timing_report_{tag}.json", "w"), indent=1, default=float)
    return report


if __name__ == "__main__":
    for cfg in (MAIN, HELD):
        rep = build(cfg)
        print(cfg["tag"], json.dumps({k: rep[k] for k in rep if k not in ("mcp_vs_pbp",)}, indent=1, default=float)[:3500])
        print(rep["mcp_vs_pbp"])
