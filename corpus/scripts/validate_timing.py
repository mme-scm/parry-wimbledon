"""Timing validation for the 2019 final: TennisVL n_shots / shot types / hit intervals vs MCP and PBP.
Outputs corpus/reports/timing_validation_2019wimF.{json,tsv}  (tsv = the 20-point sample table)
Run: python -I corpus/scripts/validate_timing.py"""
import sys, json, random, csv
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from corpuslib import *
import numpy as np
import pandas as pd

SEED = 20190714
pts = pd.read_csv(CORPUS / "timing" / "points_2019wimF.csv", dtype={"mcp_1st": str, "mcp_2nd": str})
shots = pd.read_csv(CORPUS / "timing" / "shots_2019wimF.csv")
pts["mcp_code"] = pts.mcp_2nd.fillna(pts.mcp_1st)
pts["mcp_end"] = pts.mcp_code.str[-1]
# PBP RallyCount convention (derived below): count of in-play shots; the final erring shot is not counted
pts["pbp_rc_adj"] = pts.pbp_rally_count + (pts.mcp_end != "*").astype(int) * (pts.mcp_end != "C").astype(int)
pts.loc[pts.pbp_rally_count == 0, "pbp_rc_adj"] = pts.pbp_rally_count + 1  # double fault: 0 in PBP, 1 serve in MCP

rep = {"seed": SEED}
q = pts[pts.tv_clip_rally.notna()].copy()
rep["n_points_with_tv_rally_clip"] = int(len(q))

# --- convention check PBP vs MCP over all 422 points
d = (pts.pbp_rally_count - pts.mcp_n_shots)
rep["pbp_minus_mcp"] = {str(int(k)): int(v) for k, v in d.value_counts().sort_index().items()}
conv = pts.assign(d=d).groupby("mcp_end").d.value_counts().unstack(1).fillna(0).astype(int)
rep["pbp_minus_mcp_by_mcp_final_char"] = {k: {str(int(c)): int(v) for c, v in row.items() if v} for k, row in conv.iterrows()}
rep["pbp_rc_adj_equals_mcp_all_points"] = float((pts.pbp_rc_adj == pts.mcp_n_shots).mean())

# --- agreement over all points that have a TennisVL rally clip
def agree(a, b):
    return float((a == b).mean()), float(((a - b).abs() <= 1).mean())
rep["all_points"] = {
    "tv_vs_mcp_exact": agree(q.tv_n_shots, q.mcp_n_shots)[0], "tv_vs_mcp_within1": agree(q.tv_n_shots, q.mcp_n_shots)[1],
    "tv_vs_pbp_raw_exact": agree(q.tv_n_shots, q.pbp_rally_count)[0],
    "tv_vs_pbp_adj_exact": agree(q.tv_n_shots, q.pbp_rc_adj)[0], "tv_vs_pbp_adj_within1": agree(q.tv_n_shots, q.pbp_rc_adj)[1],
    "n": int(len(q)),
}
dd = (q.tv_n_shots - q.mcp_n_shots)
rep["all_points"]["tv_minus_mcp_dist"] = {str(int(k)): int(v) for k, v in dd.value_counts().sort_index().items()}

# --- per-shot checks: serve hitter vs PBP server; stroke wing vs MCP letter; final-shot outcome vs MCP end char
FH = set("frzovlmhi")  # forehand-side letters used for the comparison (forehand, forehand slice, ...)
def mcp_letters(code):
    s = code.lstrip("c")
    return [ch for ch in s[1:] if ch in SHOT_LETTERS]
wing_ok = wing_n = 0
for _, r in q.iterrows():
    if r.tv_n_shots != r.mcp_n_shots:
        continue
    L = mcp_letters(r.mcp_code)
    sh = shots[(shots["clip"] == r.tv_clip_rally)].sort_values("shot_index")
    for k, (_, s) in enumerate(sh.iterrows()):
        if k == 0 or k - 1 >= len(L):
            continue
        ch = L[k - 1]
        if ch in "fr" and s.wing in ("forehand", "backhand"):
            wing_n += 1; wing_ok += int(s.wing == "forehand")
        elif ch in "bs" and s.wing in ("forehand", "backhand"):
            wing_n += 1; wing_ok += int(s.wing == "backhand")
rep["all_points"]["wing_agreement"] = {"n_shots_compared": wing_n, "n_agree": wing_ok,
                                       "rate": wing_ok / wing_n if wing_n else None,
                                       "rule": "points with equal shot counts; MCP f,r = forehand and b,s = backhand vs TennisVL wing"}
# serve hitter vs PBP server
srv_ok = srv_n = 0
for _, r in q.iterrows():
    sh = shots[(shots["clip"] == r.tv_clip_rally) & (shots.shot_index == 0)]
    if len(sh):
        srv_n += 1; srv_ok += int(sh.iloc[0].hitter == r.server)
rep["all_points"]["serve_hitter_vs_pbp_server"] = {"n": srv_n, "n_agree": srv_ok}
# final outcome: TennisVL last shot outcome vs MCP final char
mp = {"*": "winner", "@": "unforced-error", "#": "forced-error"}
oc_n = oc_ok = 0
for _, r in q.iterrows():
    if r.tv_n_shots < 2 or r.mcp_end not in mp:
        continue
    sh = shots[(shots["clip"] == r.tv_clip_rally)].sort_values("shot_index")
    oc_n += 1; oc_ok += int(sh.iloc[-1].shot_outcome == mp[r.mcp_end])
rep["all_points"]["final_shot_outcome_vs_mcp_end_char"] = {"n": oc_n, "n_agree": oc_ok, "rate": oc_ok / oc_n}
# when TennisVL has MORE shots than MCP, is the extra one an early serve (long first interval)?
extra = q[q.tv_n_shots > q.mcp_n_shots]
fi = []
for _, r in extra.iterrows():
    sh = shots[shots["clip"] == r.tv_clip_rally].sort_values("shot_index")
    fi.append(float(sh.inter_shot_interval_s.dropna().iloc[0]) if sh.inter_shot_interval_s.notna().sum() else np.nan)
rep["tv_more_than_mcp"] = {"n": int(len(extra)), "n_first_interval_ge_4s": int(sum(1 for x in fi if x >= 4.0)),
                           "n_mcp_code_starts_with_c_or_has_let": int(extra.mcp_code.str.startswith("c").sum())}
# hit-interval internal consistency
sr = shots[shots.clip_role.isin(["rally", "ace", "double_fault"]) & shots.inter_shot_interval_s.notna()]
iv = sr.inter_shot_interval_s
rep["hit_intervals_s"] = {"n": int(len(iv)), "mean": float(iv.mean()), "median": float(iv.median()), "sd": float(iv.std()),
                          "p1": float(iv.quantile(.01)), "p99": float(iv.quantile(.99)), "min": float(iv.min()), "max": float(iv.max()),
                          "n_nonpositive": int((iv <= 0).sum())}
b = shots.copy()
b["bounce"] = pd.to_numeric(b.bounce_timestamp_second, errors="coerce")
b["next_hit"] = b.groupby("clip").hit_timestamp_second.shift(-1)
bb = b[b.bounce.notna() & b.next_hit.notna()]
rep["bounce_between_hits"] = {"n": int(len(bb)), "rate_hit<bounce<next_hit": float(((bb.hit_timestamp_second < bb.bounce) & (bb.bounce < bb.next_hit)).mean())}
# serve-time agreement with PBP clock (offset residual): from points table
r_ = pts.resid_s.dropna()
rep["pbp_clock_vs_first_serve"] = {"n": int(len(r_)), "within_1s": float((r_.abs() <= 1).mean()), "within_3s": float((r_.abs() <= 3).mean())}

# residual breakdown: is ElapsedTime the time of the first serve of the point?
qq = pts[pts.resid_s.notna()].copy()
qq["has_fault_clip"] = qq.tv_clip_fault.notna()
qq["outlier"] = qq.resid_s.abs() > 3
bd = qq.groupby(["has_fault_clip", "pbp_serve_number"]).agg(n=("resid_s", "size"), n_outlier=("outlier", "sum"), median_resid=("resid_s", "median"))
rep["resid_breakdown"] = [{"has_fault_clip": bool(i[0]), "pbp_serve_number": int(i[1]), "n": int(r.n), "n_outlier_gt3s": int(r.n_outlier),
                           "median_resid_s": float(r.median_resid)} for i, r in bd.iterrows()]
o = qq[qq.outlier]
rep["resid_outliers"] = {"n": int(len(o)), "n_positive": int((o.resid_s > 0).sum()), "n_negative": int((o.resid_s < 0).sum()),
                         "positive_range_s": [float(o[o.resid_s > 0].resid_s.min()), float(o[o.resid_s > 0].resid_s.max())],
                         "negative_range_s": [float(o[o.resid_s < 0].resid_s.min()), float(o[o.resid_s < 0].resid_s.max())],
                         "n_positive_second_serve_point_without_fault_clip": int(((o.resid_s > 0) & (~o.has_fault_clip) & (o.pbp_serve_number == 2)).sum())}
# --- 20 random points (sample table)
rng = random.Random(SEED)
ids = sorted(q.point_idx.tolist())
sample = sorted(rng.sample(ids, 20))
rows = []
for pi in sample:
    r = q[q.point_idx == pi].iloc[0]
    sh = shots[shots["clip"] == r.tv_clip_rally].sort_values("shot_index")
    ivs = sh.inter_shot_interval_s.dropna()
    L = mcp_letters(r.mcp_code)
    wing_cmp = ""
    if r.tv_n_shots == r.mcp_n_shots:
        ok = n = 0
        for k, (_, s) in enumerate(sh.iterrows()):
            if k == 0 or k - 1 >= len(L):
                continue
            ch = L[k - 1]
            if ch in "frbs" and s.wing in ("forehand", "backhand"):
                n += 1; ok += int((ch in "fr") == (s.wing == "forehand"))
        wing_cmp = f"{ok}/{n}"
    rows.append({
        "point_idx": int(pi), "set": int(r.set_no), "game": int(r.game_in_set),
        "score_before_p1p2": f"{r.pts_before_p1}-{r.pts_before_p2}",
        "tv_n_shots": int(r.tv_n_shots), "mcp_n_shots": int(r.mcp_n_shots), "mcp_code_end": r.mcp_code[-6:],
        "pbp_rally_count": int(r.pbp_rally_count), "pbp_rc_adj": int(r.pbp_rc_adj),
        "tv_eq_mcp": int(r.tv_n_shots == r.mcp_n_shots), "tv_eq_pbp_adj": int(r.tv_n_shots == r.pbp_rc_adj),
        "tv_dur_s": round(float(r.tv_rally_duration_s), 2),
        "interval_mean_s": round(float(ivs.mean()), 2) if len(ivs) else "", "interval_min_s": round(float(ivs.min()), 2) if len(ivs) else "",
        "interval_max_s": round(float(ivs.max()), 2) if len(ivs) else "", "wing_agree": wing_cmp,
    })
with open(CORPUS / "reports" / "timing_validation_2019wimF.tsv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0].keys()), delimiter="\t")
    w.writeheader(); [w.writerow(x) for x in rows]
S = pd.DataFrame(rows)
rep["sample20"] = {"tv_eq_mcp": int(S.tv_eq_mcp.sum()), "tv_eq_pbp_adj": int(S.tv_eq_pbp_adj.sum()),
                   "tv_within1_mcp": int(((S.tv_n_shots - S.mcp_n_shots).abs() <= 1).sum()),
                   "tv_within1_pbp_adj": int(((S.tv_n_shots - S.pbp_rc_adj).abs() <= 1).sum()),
                   "n": 20, "mean_interval_s": float(pd.to_numeric(S.interval_mean_s, errors="coerce").mean())}
json.dump(rep, open(CORPUS / "reports" / "timing_validation_2019wimF.json", "w"), indent=1)
print(json.dumps(rep, indent=1))
print(S.to_string())
