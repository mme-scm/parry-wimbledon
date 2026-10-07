"""Tokenisation, de-duplication and phase heuristics (shared)."""
import re

WORD_RE = re.compile(r"[A-Za-z0-9]+(?:['’\-][A-Za-z0-9]+)*")


def words(s):
    return WORD_RE.findall(s or "")


def norm_tokens(s):
    return [w.lower() for w in words(s)]


def cut_first_k_words(s, k):
    """Remove the first k words (and the text before them) from s; return the remainder, leading punctuation stripped."""
    spans = [m.end() for m in WORD_RE.finditer(s)]
    if k <= 0:
        return s
    if k >= len(spans):
        return ""
    return s[spans[k - 1]:].lstrip(" .,;:!?-–\n")


def suffix_prefix_overlap(a, b):
    for k in range(min(len(a), len(b)), 0, -1):
        if a[-k:] == b[:k]:
            return k
    return 0


def common_prefix_len(a, b):
    k = 0
    while k < min(len(a), len(b)) and a[k] == b[k]:
        k += 1
    return k


# --- dedup rule parameters (documented in README) ---
MIN_OVERLAP_TOKENS = 6      # R2/R3: partial overlaps shorter than this are treated as coincidence
MAX_EXACT_DUP_DISTANCE = 3  # R1: exact repeat of the most recent non-empty transcript at most 3 clips back


def dedup_stream(texts):
    """texts: list of raw transcript strings in clip order.
    Returns list of dicts: text_dedup, action, dedup_of(index), k_removed."""
    out = []
    last_nonempty = None  # (index, tokens)
    for i, t in enumerate(texts):
        toks = norm_tokens(t)
        rec = {"text_dedup": t, "action": "none", "dedup_of": None, "k_removed": 0}
        if not toks:
            out.append(rec)
            continue
        if last_nonempty is not None:
            j, ptoks = last_nonempty
            if toks == ptoks and i - j <= MAX_EXACT_DUP_DISTANCE:
                # exact repeat of a recent transcript: attribute to the first occurrence in the run
                src = out[j]["dedup_of"] if out[j]["action"] == "exact_repeat" else j
                rec.update({"text_dedup": "", "action": "exact_repeat", "dedup_of": src, "k_removed": len(toks)})
                # keep last_nonempty pointing at the same text (do not move it: later repeats still map to the first)
                out.append(rec)
                last_nonempty = (i, toks)
                continue
            k = suffix_prefix_overlap(ptoks, toks)
            if k >= MIN_OVERLAP_TOKENS:
                rec.update({"text_dedup": cut_first_k_words(t, k), "action": "suffix_prefix_overlap", "dedup_of": j, "k_removed": k})
            else:
                l = common_prefix_len(ptoks, toks)
                if l >= MIN_OVERLAP_TOKENS:
                    rec.update({"text_dedup": cut_first_k_words(t, l), "action": "shared_prefix", "dedup_of": j, "k_removed": l})
        out.append(rec)
        last_nonempty = (i, toks)
    return out


# --------------------------------------------------------------------------------------
# Phase heuristics (clip-level; no audio and no word times, so in_rally vs between_points cannot be separated)
# --------------------------------------------------------------------------------------
SCORE_NUM = r"(?:0|15|30|40|forty|thirty|fifteen|love|all|deuce|ad|advantage)"
SCORE_CALL_RE = re.compile(
    r"\b(?:15|30|40|forty|thirty|fifteen|love)\b[\s,.\-–]+(?:15|30|40|love|all|0|forty|thirty|fifteen)\b"
    r"|\b(?:love|deuce)\b[\s,.\-–]+(?:all|15|30|40)\b|\bdeuce\b|\badvantage\s+[A-Z][a-z]+", re.I)
SCORE_VOCAB = {"love", "all", "deuce", "advantage", "ad", "forty", "thirty", "fifteen", "game", "set", "and", "to"}
CHANGEOVER_RE = re.compile(r"\bchange(?:\s|-)?overs?\b|\bchange of ends\b|\bchanging ends\b|\bnew balls\b|\bchange(?:s|d)? ends\b"
                           r"|\btowel(?:s|ing)?\b|\bbreak in play\b|\bmedical time ?out\b|\bset break\b|\btake a seat\b|\bsit(?:s|ting)? down\b", re.I)
UMPIRE_CUES = [
    ("umpire_game_call", re.compile(r"^\s*Game[,.]?\s+[A-Z][a-z]+", re.M)),
    ("umpire_new_balls", re.compile(r"\bnew balls,? please\b", re.I)),
    ("umpire_ball_called", re.compile(r"\bball was called\b", re.I)),
    ("umpire_time_violation", re.compile(r"\btime violation\b", re.I)),
    ("umpire_challenge_call", re.compile(r"\bMr\.? [A-Z][a-z]+ is (?:challenging|charging|having a call)\b")),
]


def phase_tags(text, surnames=()):
    """Return (phase, tags, speaker_cues). phase in {clip, between_points, changeover}.
    HEURISTIC: regex over clip-level text; flagged phase_heuristic=True by the caller when phase != 'clip'."""
    tags = []
    toks = norm_tokens(text)
    sn = {s.lower() for s in surnames}
    if SCORE_CALL_RE.search(text or ""):
        tags.append("contains_score_call")
    if CHANGEOVER_RE.search(text or ""):
        tags.append("changeover_cue")
    cues = [name for name, rx in UMPIRE_CUES if rx.search(text or "")]
    only = bool(toks) and all((t.isdigit() and len(t) <= 2) or t in SCORE_VOCAB or t in sn for t in toks) \
        and any(t.isdigit() or t in ("love", "deuce", "advantage", "all") for t in toks) or (bool(toks) and "umpire_game_call" in cues and len(toks) <= 3)
    if only:
        tags.append("score_call_only")
    phase = "clip"
    if "changeover_cue" in tags:
        phase = "changeover"
    elif "score_call_only" in tags:
        phase = "between_points"
    return phase, tags, cues


def diag_repeats(texts):
    """Diagnostics (not applied): exact repeats of an earlier non-empty transcript at distance > MAX_EXACT_DUP_DISTANCE clips."""
    seen = {}
    far = 0
    for i, t in enumerate(texts):
        k = tuple(norm_tokens(t))
        if not k:
            continue
        if k in seen and i - seen[k] > MAX_EXACT_DUP_DISTANCE:
            far += 1
        seen[k] = i
    return far
