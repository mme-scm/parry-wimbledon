"""Shared code for the metre analysis (definitions in analysis/metre/plan.md; section numbers refer to it)."""
import glob
import json
import re
import unicodedata
from collections import defaultdict
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
TR = ROOT / "corpus" / "transcripts"
TM = ROOT / "corpus" / "timing"
RP = ROOT / "corpus" / "reports"
HERE = ROOT / "analysis" / "metre"
RES = HERE / "results"
FIG = HERE / "figures"
TAGS = ["2019wimF", "2023wimF"]
SEED = 20190714
POINT_PROPER = {"rally", "ace", "double_fault"}

# ---------------------------------------------------------------- tokenisation (plan 3)
TOKEN_RE = re.compile(r"[a-z0-9]+(?:'[a-z0-9]+)*")


def tokenize(text):
    t = unicodedata.normalize("NFC", text or "").lower()
    t = t.replace("’", "'").replace("‘", "'").replace("ʼ", "'")
    return TOKEN_RE.findall(t)


def read_jsonl(path):
    with open(path, encoding="utf-8") as f:
        return [json.loads(line) for line in f if line.strip()]


def pool_paths():
    return sorted(glob.glob(str(TR / "tv_pool_*.jsonl")))


def stream_name(path):
    return Path(path).stem


# ---------------------------------------------------------------- score calls (plan 6, R1)
SCORE_VOCAB = {"0", "15", "30", "40", "love", "fifteen", "thirty", "forty", "all", "deuce", "advantage", "ad",
               "game", "set", "match"}
SCORE_CORE = {"0", "15", "30", "40", "love", "fifteen", "thirty", "forty", "deuce", "advantage"}


def score_call_mask(tokens, surnames):
    n = len(tokens)
    mask = [False] * n
    i = 0
    while i < n:
        if tokens[i] in SCORE_VOCAB:
            j = i
            while j < n and tokens[j] in SCORE_VOCAB:
                j += 1
            if any(t in SCORE_CORE for t in tokens[i:j]):
                for k in range(i, j):
                    mask[k] = True
            i = j
        else:
            i += 1
    for i in range(n - 1):
        if tokens[i] in ("game", "advantage") and tokens[i + 1] in surnames:
            mask[i] = mask[i + 1] = True
    return mask


def split_unmasked(tokens, mask):
    segs, cur = [], []
    for t, m in zip(tokens, mask):
        if m:
            if cur:
                segs.append(cur)
            cur = []
        else:
            cur.append(t)
    if cur:
        segs.append(cur)
    return segs


# ---------------------------------------------------------------- umpire patterns (POST HOC, plan addendum 1, PH6)
UMPIRE_ADJ = {"please", "players"}


def umpire_mask(tokens, names):
    """Mask umpire-pattern tokens: every `thank you` (with an adjacent `please`, or a following `players`),
    `mr` + next token, and `game` + a first or last name of either finalist (`names`)."""
    n = len(tokens)
    mask = [False] * n
    for i in range(n - 1):
        a, b = tokens[i], tokens[i + 1]
        if a == "thank" and b == "you":
            mask[i] = mask[i + 1] = True
            if i + 2 < n and tokens[i + 2] in UMPIRE_ADJ:
                mask[i + 2] = True
            if i >= 1 and tokens[i - 1] == "please":
                mask[i - 1] = True
        elif a == "mr":
            mask[i] = mask[i + 1] = True
        elif a == "game" and b in names:
            mask[i] = mask[i + 1] = True
    return mask


# ---------------------------------------------------------------- names (exploratory X4)
def names_from_match_id(match_id):
    parts = match_id.split("-")
    toks = set()
    for p in parts[-2:]:
        toks.update(w.lower() for w in p.split("_") if w)
    return toks


def mask_names(tokens, names):
    return ["<p>" if t in names else t for t in tokens]


# ---------------------------------------------------------------- formulas (plan 3)
NMIN, NMAX = 2, 12


def pool_ngram_table(mask_player_names=False):
    """Return dict ngram_string -> [total count, number of pool streams containing it] for 2 <= n <= 12."""
    table = {}
    for path in pool_paths():
        local = defaultdict(int)
        for r in read_jsonl(path):
            toks = tokenize(r.get("text_corrected"))
            if mask_player_names:
                toks = mask_names(toks, names_from_match_id(r["match_id"]))
            L = len(toks)
            for n in range(NMIN, NMAX + 1):
                for i in range(L - n + 1):
                    local[" ".join(toks[i:i + n])] += 1
        for g, c in local.items():
            v = table.get(g)
            if v is None:
                table[g] = [c, 1]
            else:
                v[0] += c
                v[1] += 1
    return table


def formula_set(table, nmin=2, min_count=3, min_streams=2):
    return {g for g, (c, s) in table.items() if c >= min_count and s >= min_streams and g.count(" ") + 1 >= nmin}


def match_segment(seg, F, nmin=2):
    """Occurrences (start, end) of formula n-grams in one token segment, the covered mask, and maximal occurrences."""
    L = len(seg)
    occ = []
    for n in range(max(nmin, NMIN), NMAX + 1):
        for i in range(L - n + 1):
            if " ".join(seg[i:i + n]) in F:
                occ.append((i, i + n))
    cov = np.zeros(L, dtype=bool)
    for a, b in occ:
        cov[a:b] = True
    maximal = [o for o in occ if not any((p[0] <= o[0] and p[1] >= o[1] and p != o) for p in occ)]
    return occ, cov, maximal


# ---------------------------------------------------------------- timing (plan 2)
def load_points(tag):
    P = pd.read_csv(TM / f"points_{tag}.csv").sort_values("point_idx").reset_index(drop=True)
    return P


def surnames(tag):
    P = load_points(tag)
    return {P.p1_name.iloc[0].split()[-1].lower(), P.p2_name.iloc[0].split()[-1].lower()}


def full_names(tag):
    P = load_points(tag)
    out = set()
    for nm in (P.p1_name.iloc[0], P.p2_name.iloc[0]):
        out.update(w.lower() for w in nm.split())
    return out


def timing_sequence(tag):
    """Cycles 1..M (every PBP point except the last): A = serve-to-serve time, dead-ball category (plan 2)."""
    P = load_points(tag)
    nxt = P.shift(-1)
    P["A"] = nxt.elapsed_s - P.elapsed_s
    same_game = nxt.game_no == P.game_no
    new_set = nxt.set_no != P.set_no
    odd3 = (P.game_in_set % 2 == 1) & (P.game_in_set >= 3)
    P["category"] = np.where(same_game, "within_game",
                             np.where(new_set | odd3, "changeover", "other_game_end"))
    C = P.iloc[:-1].copy().reset_index(drop=True)
    C["cyc"] = np.arange(len(C))
    t_end = float(P.elapsed_s.iloc[-1])
    return C, t_end


def cut_intervals(tag):
    if tag != "2023wimF":
        return []
    rep = json.load(open(RP / f"timing_report_{tag}.json"))
    return [tuple(s["cut_interval_points"]) for s in rep["offset_segments"] if s.get("cut_interval_points")]


def build_units(tag):
    """Units (plan 2) with exclusion flow. Returns (units DataFrame, flow list, clip DataFrame, clips_by_point dict)."""
    recs = read_jsonl(TR / f"tv_{tag}.jsonl")
    P = load_points(tag).set_index("point_idx")
    C, _ = timing_sequence(tag)
    cyc_of = dict(zip(C.point_idx, C.cyc))
    A_of = dict(zip(C.point_idx, C.A))
    cat_of = dict(zip(C.point_idx, C.category))
    last_point = int(P.index.max())
    cuts = cut_intervals(tag)

    utt_point = {r["utt_id"]: r["point_idx_pbp"] for r in recs}
    repeat_points = set()
    for r in recs:
        if r["dedup_action"] == "exact_repeat" and r["dedup_of"]:
            p_src = utt_point.get(r["dedup_of"])
            if r["point_idx_pbp"] is not None and p_src is not None and p_src != r["point_idx_pbp"]:
                repeat_points.update([int(r["point_idx_pbp"]), int(p_src)])

    clips_by_point = defaultdict(list)
    for r in sorted(recs, key=lambda r: r["clip_i"]):
        if r["point_idx_pbp"] is not None:
            clips_by_point[int(r["point_idx_pbp"])].append(r)

    flow = [("PBP points", len(P)), ("points with any aligned clip", len(clips_by_point))]
    pts = sorted(p for p, cl in clips_by_point.items() if any(c["clip_role"] in POINT_PROPER for c in cl))
    flow.append(("E1 point-proper clip present", len(pts)))
    pts = [p for p in pts if p < last_point]
    flow.append(("E2 not the last point", len(pts)))

    def qc(p):
        row = P.loc[p]
        res = row.resid_s
        if pd.isna(res):
            return False
        if abs(res) <= 3:
            return True
        return bool(res > 3 and row.pbp_serve_number == 2 and pd.isna(row.tv_clip_fault))
    pts = [p for p in pts if qc(p)]
    flow.append(("E3 timing QC (resid)", len(pts)))
    pts = [p for p in pts if A_of[p] <= 600]
    flow.append(("E4 A <= 600 s", len(pts)))
    if tag == "2023wimF":
        pts = [p for p in pts if not any(a <= p and p + 1 <= b for a, b in cuts)]
        flow.append(("E5 no video cut between p and p+1 (2023)", len(pts)))

    rows = []
    for p in pts:
        row = P.loc[p]
        nxt = P.loc[p + 1]
        D = float(nxt.elapsed_s + row.offset_used_s - row.tv_last_hit_s) if pd.notna(row.offset_used_s) and pd.notna(row.tv_last_hit_s) else np.nan
        cl = clips_by_point[p]
        rows.append({
            "point_idx": p, "cyc": cyc_of[p], "elapsed_s": float(row.elapsed_s), "A": float(A_of[p]), "D": D,
            "category": cat_of[p], "set_no": int(row.set_no), "game_no": int(row.game_no),
            "game_in_set": int(row.game_in_set), "tiebreak": bool(row.tiebreak),
            "serve_number": row.pbp_serve_number, "n_clips": len(cl),
            "clip_roles": "+".join(c["clip_role"] for c in cl),
            "tv_rally_duration_s": row.tv_rally_duration_s, "tv_n_shots": row.tv_n_shots,
            "repeat_involved": p in repeat_points,
        })
    U = pd.DataFrame(rows)
    return U, flow, clips_by_point


# ---------------------------------------------------------------- statistics helpers (plan 4)
def rank_rows(X):
    """Average ranks along axis 1 (handles ties)."""
    from scipy.stats import rankdata
    return rankdata(X, axis=-1)


def pearson_rows(X, Y):
    Xc = X - X.mean(axis=-1, keepdims=True)
    Yc = Y - Y.mean(axis=-1, keepdims=True)
    num = (Xc * Yc).sum(axis=-1)
    den = np.sqrt((Xc ** 2).sum(axis=-1) * (Yc ** 2).sum(axis=-1))
    with np.errstate(invalid="ignore", divide="ignore"):
        return num / den


def spearman_rows(X, Y):
    return pearson_rows(rank_rows(X), rank_rows(Y))


def block_bootstrap_indices(n, B, L=10, seed=SEED):
    rng = np.random.default_rng(seed)
    nb = int(np.ceil(n / L))
    starts = rng.integers(0, n, size=(B, nb))
    idx = (starts[:, :, None] + np.arange(L)[None, None, :]) % n
    return idx.reshape(B, nb * L)[:, :n]


def two_sided_p(obs, null):
    null = np.asarray(null)
    null = null[~np.isnan(null)]
    K = len(null)
    up = (1 + np.sum(null >= obs)) / (1 + K)
    dn = (1 + np.sum(null <= obs)) / (1 + K)
    return float(min(1.0, 2 * min(up, dn))), K


def holm(pvals):
    p = np.asarray(pvals, dtype=float)
    order = np.argsort(p)
    m = len(p)
    adj = np.empty(m)
    run = 0.0
    for rank, i in enumerate(order):
        run = max(run, (m - rank) * p[i])
        adj[i] = min(1.0, run)
    return adj
