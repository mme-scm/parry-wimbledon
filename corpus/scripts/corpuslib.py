"""Shared loaders and helpers for the corpus build (Phase 1).

All raw files are read-only. Run scripts that import this with `python -I` (isolated mode);
the scripts add their own directory to sys.path explicitly, see `_here()` use in each script.
"""
import ast
import csv
import json
import re
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
RAW = ROOT / "corpus" / "raw"
CORPUS = ROOT / "corpus"
TV_JSON = RAW / "tennisexpert_repo" / "data" / "tennis_data_test_stats_.json"
PBP_DIR = RAW / "sackmann_slam_pbp_hfmirror"
MCP_DIR = RAW / "sackmann_mcp"
CORNELL = RAW / "cornell_tennis" / "extracted" / "text_commentaries.json"

MAIN_ID = "20190714-M-Wimbledon-F-Roger_Federer-Novak_Djokovic"
HELD_ID = "20230716-M-Wimbledon-F-Novak_Djokovic-Carlos_Alcaraz"
MAIN = {"id": MAIN_ID, "tag": "2019wimF", "stream": "tv_2019wimF", "pbp_file": "2019-wimbledon-points.csv",
        "pbp_id": "2019-wimbledon-1701", "final_set_tb": 12}
HELD = {"id": HELD_ID, "tag": "2023wimF", "stream": "tv_2023wimF", "pbp_file": "2023-wimbledon-points.csv",
        "pbp_id": "2023-wimbledon-1701", "final_set_tb": 6}
FPS = 25.0


def stream_name(match_id):
    if match_id == MAIN_ID:
        return MAIN["stream"]
    if match_id == HELD_ID:
        return HELD["stream"]
    return "tv_pool_" + match_id


def strip_accents(s):
    return "".join(c for c in unicodedata.normalize("NFKD", s) if not unicodedata.combining(c))


def hms_to_s(x):
    h, m, s = x.split(":")
    return int(h) * 3600 + int(m) * 60 + int(s)


# --------------------------------------------------------------------------------------
# TennisVL
# --------------------------------------------------------------------------------------
def load_tennisvl():
    """Return list of matches (dicts) with clips in file order. synthetic LLM commentary is dropped here."""
    data = json.load(open(TV_JSON, encoding="utf-8"))
    out = []
    for idx, rec in enumerate(data):
        conv = rec["conversations"]
        humans = [t["value"] for t in conv if t["from"] == "human"]
        gpts = [t["value"] for t in conv if t["from"] == "gpt"]
        assert len(humans) == len(gpts) == len(rec["videos"])
        clips = []
        match_id = None
        players = None
        for ci, (v, h, g) in enumerate(zip(rec["videos"], humans, gpts)):
            m = re.search(r"/(.+)_(\d+)_(\d+)\.mp4$", v)
            mid, a, b = m.group(1), int(m.group(2)), int(m.group(3))
            match_id = match_id or mid
            assert mid == match_id
            hd = ast.literal_eval(h.split("Metadata:", 1)[1].strip())
            meta = g.partition("\n\nMetadata:")[2]
            gd = ast.literal_eval(meta.strip()) if meta else {}
            if players is None and gd.get("match_info"):
                mi = gd["match_info"]
                players = {"p1": mi["player_1"], "p2": mi["player_2"],
                           "tournament": mi.get("tournament"), "round": mi.get("round")}
            rally = hd["rally"]
            clips.append({
                "clip_i": ci, "clip": v.split("/")[-1], "start_frame": a, "end_frame": b,
                "score_state": hd["score_state"], "point_outcome": hd.get("point_outcome"),
                "rally": rally,
                "text": gd.get("audio_transcription (background context)", "") or "",
            })
        out.append({"idx": idx, "match_id": match_id, "players": players, "clips": clips})
    return out


def tv_state_key(ss):
    """Normalised score state (before the point) from a TennisVL score_state dict.
    Returns (server_short, sets{short:int}, games{short:int}, pts{short:str})."""
    return ss


def norm_point_token(x):
    x = str(x).strip().upper()
    return "AD" if x in ("AD", "A") else x


def classify_clip(c):
    """clip_role from the rally list (see README)."""
    r = c["rally"]
    first = r[0]
    n = len(r)
    if n == 1 and first["type"] == "first serve" and first["shot_outcome"] == "unforced-error":
        return "first_serve_fault"
    if n == 1 and first["type"] == "second serve" and first["shot_outcome"] == "unforced-error":
        return "double_fault"
    if n == 1 and first["shot_outcome"] == "winner":
        return "ace"
    return "rally"


# --------------------------------------------------------------------------------------
# Sackmann slam point-by-point
# --------------------------------------------------------------------------------------
def load_pbp(cfg):
    """Return (rows, p1_name, p2_name). rows: list of dict per real point (0X/0Y placeholders dropped),
    with the score state BEFORE each point derived from the previous row's after-point state."""
    allrows = list(csv.DictReader(open(PBP_DIR / cfg["pbp_file"], encoding="utf-8")))
    rows = [r for r in allrows if r["match_id"] == cfg["pbp_id"]]
    n_raw = len(rows)
    dropped = [r["PointNumber"] for r in rows if not r["PointNumber"].isdigit()]
    rows = [r for r in rows if r["PointNumber"].isdigit()]
    mrows = list(csv.DictReader(open(PBP_DIR / cfg["pbp_file"].replace("-points", "-matches"), encoding="utf-8")))
    m = [r for r in mrows if r["match_id"] == cfg["pbp_id"]][0]
    p1, p2 = m["player1"], m["player2"]
    out = []
    sets = [0, 0]
    prev = None
    for r in rows:
        n = int(r["PointNumber"])
        if prev is None:
            before = dict(sets=(0, 0), games=(0, 0), pts=("0", "0"))
        else:
            ns = tuple(sets)
            if int(r["SetNo"]) != int(prev["SetNo"]):
                g = (0, 0)
            else:
                g = (int(prev["P1GamesWon"]), int(prev["P2GamesWon"]))
            before = dict(sets=ns, games=g, pts=(norm_point_token(prev["P1Score"]), norm_point_token(prev["P2Score"])))
        d = {
            "pbp_point": n, "elapsed_s": hms_to_s(r["ElapsedTime"]), "elapsed_raw": r["ElapsedTime"],
            "set_no": int(r["SetNo"]), "game_no": int(r["GameNo"]),
            "server": int(r["PointServer"]), "winner": int(r["PointWinner"]),
            "p1_score_after": r["P1Score"], "p2_score_after": r["P2Score"],
            "p1_games_after": int(r["P1GamesWon"]), "p2_games_after": int(r["P2GamesWon"]),
            "set_winner": int(r["SetWinner"]),
            "speed_kmh": r["Speed_KMH"], "serve_number": r["ServeNumber"], "winner_type": r["WinnerType"],
            "rally_count": int(r["RallyCount"]) if r["RallyCount"] != "" else None,
            "before": before,
        }
        if d["set_winner"] in (1, 2):
            sets[d["set_winner"] - 1] += 1
        prev = r
        out.append(d)
    return out, p1, p2, {"n_rows_raw": n_raw, "dropped_placeholders": dropped}


# --------------------------------------------------------------------------------------
# Match Charting Project
# --------------------------------------------------------------------------------------
_MCP_CACHE = {}


def load_mcp_all():
    if "points" in _MCP_CACHE:
        return _MCP_CACHE["points"], _MCP_CACHE["matches"]
    pts = {}
    for f in ["charting-m-points-2010s.csv", "charting-m-points-2020s.csv",
              "charting-w-points-2010s.csv", "charting-w-points-2020s.csv"]:
        with open(MCP_DIR / f, encoding="utf-8") as fh:
            for r in csv.DictReader(fh):
                pts.setdefault(r["match_id"], []).append(r)
    ms = {}
    for f in ["charting-m-matches.csv", "charting-w-matches.csv"]:
        with open(MCP_DIR / f, encoding="utf-8") as fh:
            for r in csv.DictReader(fh):
                ms[r["match_id"]] = r
    _MCP_CACHE["points"], _MCP_CACHE["matches"] = pts, ms
    return pts, ms


SHOT_LETTERS = set("fbrsvzopuylmhijktq")
FAULT_CODES = set("nwdx!eV")


def mcp_parse(first, second):
    """Parse an MCP (1st, 2nd) pair into shot-count information.
    n_shots counts the serve plus every stroke letter in the code that ends the point
    (the 2nd-serve code if present, else the 1st-serve code), including the final erring/winning stroke.
    Heuristic; see README."""
    first = (first or "").strip()
    second = (second or "").strip()
    code = second if second else first
    s = code.lstrip("c")  # 'c' = serve clipped the net cord (let) in MCP
    # remove leading digit serve char
    body = s[1:] if s else ""
    letters = [ch for ch in body if ch in SHOT_LETTERS]
    n = 1 + len(letters)
    serve_fault_code = (len(letters) == 0 and len(body) > 0 and body[-1] in FAULT_CODES and
                        body[-1] not in "*#@")
    first_is_fault = bool(second) and True
    double_fault = bool(second) and serve_fault_code
    ace = (len(letters) == 0 and body.endswith("*"))
    if not code:
        n = None
    return {"n_shots": n, "first_serve_fault": first_is_fault, "double_fault": double_fault, "ace": ace,
            "code": code, "n_serves": 2 if second else 1}


def load_mcp_match(match_id):
    pts, ms = load_mcp_all()
    if match_id not in pts:
        return None, None
    rows = sorted(pts[match_id], key=lambda r: int(r["Pt"]))
    return rows, ms.get(match_id)


def surname_key(name):
    return strip_accents(name).upper().split()[-1] if name else ""
