"""Point alignment helpers: score-state keys, clip grouping, monotone DP alignment."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from corpuslib import *  # noqa

TB_MAP = {"0": 0, "15": 1, "30": 2, "40": 3, "AD": 4}


def is_tiebreak(g1, g2, setno=1, final_tb=12):
    """Tie-break game: 6-6 in sets 1-4; in the 5th set at `final_tb` games all (12 under the 2019 Wimbledon rule,
    6 under the 2022+ rule)."""
    if g1 != g2:
        return False
    return (g1 == 6) if setno < 5 else (g1 == final_tb)


def pbp_keys(rows, p1, p2, final_tb=12):
    """Key per PBP point, named by player surname. key = (server, sets, games, pts) with dicts as sorted tuples."""
    s1, s2 = surname_key(p1), surname_key(p2)
    out = []
    for r in rows:
        b = r["before"]
        srv = s1 if r["server"] == 1 else s2
        out.append({
            "server": srv,
            "sets": {s1: b["sets"][0], s2: b["sets"][1]},
            "games": {s1: b["games"][0], s2: b["games"][1]},
            "pts": {s1: b["pts"][0], s2: b["pts"][1]},
            "tb": is_tiebreak(b["games"][0], b["games"][1], b["sets"][0] + b["sets"][1] + 1, final_tb),
        })
    return out


def tv_key(ss, final_tb=12):
    def sh(d):
        return {strip_accents(k).upper(): v for k, v in d.items()}
    srv = surname_key(ss["server"])
    sets = {k: int(v) for k, v in sh(ss["sets"]).items()}
    games = {k: int(v) for k, v in sh(ss["games_in_current_set"]).items()}
    pts = {k: norm_point_token(v) for k, v in sh(ss["points_in_current_game"]).items()}
    g = list(games.values())
    return {"server": srv, "sets": sets, "games": games, "pts": pts,
            "tb": is_tiebreak(g[0], g[1], sum(sets.values()) + 1, final_tb)}


def key_tuple(k, with_pts=True):
    t = (k["server"], tuple(sorted(k["sets"].items())), tuple(sorted(k["games"].items())))
    if with_pts:
        t += (tuple(sorted(k["pts"].items())),)
    return t


def tv_pts_as_count(k):
    return {n: TB_MAP.get(v) for n, v in k["pts"].items()}


def pts_equal_tb(tvk, pk):
    """Soft comparison in tie-breaks: TennisVL writes tie-break points in game-score tokens
    (0,15,30,40 = counts 0..3)."""
    c = tv_pts_as_count(tvk)
    ok = True
    for n, v in pk["pts"].items():
        pc = int(v)
        if c.get(n) is None:
            continue
        if pc <= 3 and c[n] != pc:
            ok = False
    return ok


def group_clips(clips, final_tb=12):
    """Group consecutive clips with identical score state (same point: fault clip + rally clip)."""
    groups = []
    for c in clips:
        k = key_tuple(tv_key(c["score_state"], final_tb))
        if groups and groups[-1]["keyt"] == k:
            groups[-1]["clips"].append(c)
        else:
            groups.append({"keyt": k, "key": tv_key(c["score_state"], final_tb), "clips": [c]})
    for g in groups:
        for c in g["clips"]:
            c["role"] = classify_clip(c)
        first = g["clips"][0]
        last = g["clips"][-1]
        g["first_attempt_s"] = min(s["hit_timestamp_second"] for s in first["rally"])
        g["has_rally_clip"] = last["role"] in ("rally", "ace", "double_fault")
        if g["has_rally_clip"]:
            hits = [s["hit_timestamp_second"] for s in last["rally"]]
            g["first_hit_s"], g["last_hit_s"], g["n_shots"] = min(hits), max(hits), len(hits)
        else:
            g["first_hit_s"] = g["last_hit_s"] = g["n_shots"] = None
    return groups


def dp_align(groups, pkeys, prows, offset=None, allow_tb=False, tb_time_tol=20.0, use_time=True, nosrv=False):
    """Monotone alignment of clip groups (chronological) to PBP points (chronological).
    Compatible pairs: identical full key (non-tiebreak); in tie-breaks (if allow_tb) identical server/sets/games and
    soft points agreement, with |video - (elapsed+offset)| <= tb_time_tol. Score favours small time residual and
    n_shots == RallyCount. Returns dict group_index -> (point_index, match_type)."""
    m, n = len(groups), len(pkeys)
    pk_full = [key_tuple(k) for k in pkeys]
    pk_nopts = [key_tuple(k, False) for k in pkeys]
    NEG = -1e9

    def s(i, j):
        g, pk = groups[i], pkeys[j]
        resid = None
        if offset is not None and use_time:
            off = offset(j) if callable(offset) else offset
            resid = g["first_attempt_s"] - (prows[j]["elapsed_s"] + off)
        if not pk["tb"] and not g["key"]["tb"] and g["keyt"] == pk_full[j]:
            mt = "key"
            base = 10.0
        elif allow_tb and pk["tb"] and g["key"]["tb"] and key_tuple(g["key"], False) == pk_nopts[j]:
            if resid is None or abs(resid) > tb_time_tol:
                return None
            mt = "key_tb" if pts_equal_tb(g["key"], pk) else "key_tb_pts_mismatch"
            base = 6.0 if mt == "key_tb" else 3.0
        elif allow_tb and nosrv and key_tuple(g["key"], True)[1:] == pk_full[j][1:]:
            # tier 3: TennisVL names the wrong server (parser error): identical sets/games/points, time-consistent
            if resid is None or abs(resid) > tb_time_tol:
                return None
            mt = "key_no_server"
            base = 5.0
        else:
            return None
        sc = base
        if resid is not None:
            sc -= min(abs(resid) / 2.0, 4.5)
        rc = prows[j]["rally_count"]
        if g["n_shots"] is not None and rc and g["n_shots"] == rc:
            sc += 1.0
        return sc, mt

    dp = [[0.0] * (n + 1) for _ in range(m + 1)]
    bt = [[None] * (n + 1) for _ in range(m + 1)]
    cache = {}
    for i in range(m):
        for j in range(n):
            best, how = dp[i][j + 1], "up"
            if dp[i + 1][j] > best:
                best, how = dp[i + 1][j], "left"
            r = s(i, j)
            if r is not None and dp[i][j] + r[0] > best:
                best, how = dp[i][j] + r[0], "diag"
                cache[(i, j)] = r[1]
            dp[i + 1][j + 1] = best
            bt[i + 1][j + 1] = how
    i, j = m, n
    res = {}
    while i > 0 and j > 0:
        how = bt[i][j]
        if how == "diag":
            res[i - 1] = (j - 1, cache[(i - 1, j - 1)])
            i -= 1
            j -= 1
        elif how == "up":
            i -= 1
        else:
            j -= 1
    return res
