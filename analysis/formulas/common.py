"""Shared definitions for the Phase 2 formula analysis (see plan.md).

Tokeniser, STOP list, stream loaders, formula (a) and system (b) identification, coverage, bootstrap.
All scripts in this directory are run with `python -I`; they add this directory to sys.path explicitly.
"""
from __future__ import annotations

import json
import re
import unicodedata
from collections import Counter, defaultdict
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
TRANSCRIPTS = ROOT / "corpus" / "transcripts"
TIMING = ROOT / "corpus" / "timing"
PRESS_JSON = ROOT / "corpus" / "raw" / "cornell_tennis" / "extracted" / "transcripts_matchinfo.json"
RESULTS = HERE / "results"
HAND = HERE / "hand"
MASTER_SEED = 20190714

MAIN = "tv_2019wimF"
HELDOUT = "tv_2023wimF"
TEXT = "text_cornell"

# ---------------------------------------------------------------- tokenisation (plan section 1)
_DASHES = re.compile(r"[\-‐‑‒–—―/]")
_TOKEN = re.compile(r"[a-z0-9]+(?:'[a-z0-9]+)*")


def normalise(text: str) -> str:
    t = unicodedata.normalize("NFKC", text or "")
    t = t.replace("’", "'").replace("‘", "'").replace("`", "'")
    t = _DASHES.sub(" ", t)
    return t.lower()


def tokenize(text: str) -> list[str]:
    return _TOKEN.findall(normalise(text))


# Frozen with plan.md (182 entries). Digits and player names are never STOP.
STOP = frozenset("""
a an the this that these those
i me my mine myself we us our ours ourselves you your yours yourself yourselves
he him his himself she her hers herself it its itself they them their theirs themselves
i'm i've i'll i'd you're you've you'll you'd he's he'll he'd she's she'll she'd it's it'll it'd
we're we've we'll we'd they're they've they'll they'd that's there's here's what's who's let's
am is are was were be been being have has had having do does did doing done
will would shall should can could may might must
isn't aren't wasn't weren't hasn't haven't hadn't doesn't don't didn't won't wouldn't can't couldn't shouldn't
of in on at by for with from to into onto out up down over under about against between through
during before after above below off than as like
and or but nor if because while although though so then there here
not no yes just very too also only even still
what which who whom whose when where why how
all any both each some such own same other
s t
""".split())

assert len(STOP) == 182, len(STOP)

NUMWORDS = frozenset("love fifteen thirty forty deuce".split())


def is_num(tok: str) -> bool:
    return tok.isdigit() or tok in NUMWORDS


def strip_poss(tok: str) -> str:
    return tok[:-2] if tok.endswith("'s") else tok


# ---------------------------------------------------------------- streams
def load_stream(stream: str, field: str = "text_corrected") -> list[dict]:
    """Records of one stream with non-empty token lists; adds 'toks'."""
    out = []
    with open(TRANSCRIPTS / f"{stream}.jsonl", encoding="utf-8") as fh:
        for line in fh:
            r = json.loads(line)
            toks = tokenize(r.get(field) or "")
            if toks:
                r["toks"] = toks
                out.append(r)
    return out


def tv_streams() -> list[str]:
    man = json.loads((TRANSCRIPTS / "manifest.json").read_text())
    names = sorted(p.stem for p in TRANSCRIPTS.glob("tv_*.jsonl"))
    return names


def pool_streams() -> list[str]:
    return [s for s in tv_streams() if s.startswith("tv_pool_")]


def player_name_lexicon() -> frozenset:
    """First names and surnames of the players of all 20 TennisVL matches (from the stream match ids)."""
    names = set()
    for s in tv_streams():
        recs = []
        with open(TRANSCRIPTS / f"{s}.jsonl", encoding="utf-8") as fh:
            first = json.loads(fh.readline())
        mid = first["match_id"]  # e.g. 20190714-M-Wimbledon-F-Roger_Federer-Novak_Djokovic
        parts = mid.split("-")
        for p in parts[-2:]:
            for w in p.split("_"):
                names.update(tokenize(w))
    return frozenset(names)


def load_press_answers() -> list[dict]:
    """Player answers from the Cornell press-conference transcripts (baseline only; see plan.md section 0)."""
    with open(PRESS_JSON, encoding="utf-8") as fh:
        d = json.load(fh)
    out = []
    for k in sorted(d, key=lambda x: int(x)):
        iv = d[k]
        for qa in iv.get("QandA") or []:
            if not isinstance(qa, (list, tuple)) or len(qa) < 2:
                continue
            toks = tokenize(qa[1] or "")
            if toks:
                out.append({"utt_id": f"press:{k}", "group": iv.get("player") or f"iv{k}", "toks": toks})
    return out


def cornell_group(r: dict) -> str:
    pl = r.get("players") or []
    return "|".join(sorted(p.lower() for p in pl)) if pl else r["utt_id"]


# ---------------------------------------------------------------- formulas (a)
def ngram_utt_counts(utts: list[list[str]], nmax: int = 12, nmin: int = 2):
    """dict ngram(tuple) -> (n distinct utterances, n occurrences)."""
    uttc: Counter = Counter()
    occ: Counter = Counter()
    for toks in utts:
        L = len(toks)
        seen = set()
        for n in range(nmin, min(nmax, L) + 1):
            for i in range(L - n + 1):
                g = tuple(toks[i:i + n])
                occ[g] += 1
                seen.add(g)
        uttc.update(seen)
    return uttc, occ


def formula_set(utts, m: int = 2, nmax: int = 12, stop_filter: bool = True, min_gap=None, clip_idx=None):
    """Formulas of I: n-grams (2..nmax) in >= m distinct utterances and not stop-only.
    min_gap (S4): count only if two occurrences are in utterances whose clip index differs by >= min_gap."""
    if min_gap is None:
        uttc, _ = ngram_utt_counts(utts, nmax)
        F = {g for g, c in uttc.items() if c >= m}
    else:
        where = defaultdict(set)
        for toks, ci in zip(utts, clip_idx):
            L = len(toks)
            for n in range(2, min(nmax, L) + 1):
                for i in range(L - n + 1):
                    where[tuple(toks[i:i + n])].add(ci)
        F = set()
        for g, cs in where.items():
            if len(cs) >= m and max(cs) - min(cs) >= min_gap:
                F.add(g)
    if stop_filter:
        F = {g for g in F if not all(t in STOP for t in g)}
    return F


def cover_a(toks: list[str], F: set, n_min: int = 2, n_max: int = 12, exact_n=None) -> np.ndarray:
    """Per-token max formula length covering it (0 = uncovered)."""
    L = len(toks)
    cov = np.zeros(L, dtype=np.int16)
    ns = [exact_n] if exact_n else range(n_min, min(n_max, L) + 1)
    for n in ns:
        if n > L:
            continue
        for i in range(L - n + 1):
            if tuple(toks[i:i + n]) in F:
                seg = cov[i:i + n]
                np.maximum(seg, n, out=seg)
    return cov


# ---------------------------------------------------------------- systems (b)
def slot_type(tok: str, names: frozenset) -> list[str]:
    t = []
    if strip_poss(tok) in names:
        t.append("NAME")
    if is_num(tok):
        t.append("NUM")
    return t


def frame_keys(toks, i, n, names):
    """Yield (frame_key, filler) for the window toks[i:i+n]; frame_key = (n, j, stype, fixed tuple)."""
    w = toks[i:i + n]
    for j in range(n):
        fixed = tuple(w[:j] + w[j + 1:])
        filler = w[j]
        if 0 < j < n - 1:
            yield (n, j, "OPEN", fixed), filler
        for st in slot_type(filler, names):
            yield (n, j, st, fixed), filler


def system_set(utts, names, nmin=2, nmax=6, min_fillers=2, min_occ=3, min_utts=3, stop_filter=True):
    """Systems of I (plan section 3). Returns dict key -> stats (occ, utts, fillers Counter)."""
    occ = Counter()
    uttsets = defaultdict(set)
    fillers = defaultdict(Counter)
    for ui, toks in enumerate(utts):
        L = len(toks)
        for n in range(nmin, min(nmax, L) + 1):
            for i in range(L - n + 1):
                for key, fil in frame_keys(toks, i, n, names):
                    if key[2] == "OPEN" and n < 3:
                        continue
                    occ[key] += 1
                    uttsets[key].add(ui)
                    fillers[key][fil] += 1
    S = {}
    for key, c in occ.items():
        if c < min_occ or len(uttsets[key]) < min_utts or len(fillers[key]) < min_fillers:
            continue
        fixed = key[3]
        if stop_filter and all(t in STOP for t in fixed):
            continue
        if key[2] == "OPEN" and not (0 < key[1] < key[0] - 1):
            continue
        S[key] = {"occ": c, "utts": len(uttsets[key]), "fillers": fillers[key]}
    return S


def cover_b(toks, S: dict, names, nmin=2, nmax=6) -> np.ndarray:
    L = len(toks)
    cov = np.zeros(L, dtype=bool)
    if not S:
        return cov
    for n in range(nmin, min(nmax, L) + 1):
        for i in range(L - n + 1):
            for key, _ in frame_keys(toks, i, n, names):
                if key in S:
                    cov[i:i + n] = True
                    break
    return cov


def frame_str(key) -> str:
    n, j, st, fixed = key
    parts = list(fixed)
    parts.insert(j, f"<{st}>" if st != "OPEN" else "<_>")
    return " ".join(parts)


# ---------------------------------------------------------------- density + bootstrap
def coverage_arrays(utts, F, S=None, names=None, n_min=2, mask=None):
    """Per-utterance (n_tokens, covered_a, covered_ab) arrays. mask: list of bool arrays (True = keep token)."""
    n = np.zeros(len(utts), dtype=np.int64)
    ca = np.zeros(len(utts), dtype=np.int64)
    cab = np.zeros(len(utts), dtype=np.int64)
    for k, toks in enumerate(utts):
        a = cover_a(toks, F, n_min=n_min) > 0
        if S is not None:
            ab = a | cover_b(toks, S, names)
        else:
            ab = a
        keep = mask[k] if mask is not None else np.ones(len(toks), dtype=bool)
        n[k] = keep.sum()
        ca[k] = (a & keep).sum()
        cab[k] = (ab & keep).sum()
    return n, ca, cab


def boot_ratio(num, den, B=2000, seed=0, strata=None):
    """Percentile bootstrap CI for sum(num)/sum(den), resampling utterances (within strata if given)."""
    num = np.asarray(num, float)
    den = np.asarray(den, float)
    rng = np.random.default_rng(seed)
    if strata is None:
        strata = np.zeros(len(num), dtype=int)
    strata = np.asarray(strata)
    groups = [np.where(strata == s)[0] for s in np.unique(strata)]
    vals = np.empty(B)
    for b in range(B):
        sn = 0.0
        sd = 0.0
        for g in groups:
            idx = rng.choice(g, size=len(g), replace=True)
            sn += num[idx].sum()
            sd += den[idx].sum()
        vals[b] = sn / sd if sd else np.nan
    est = num.sum() / den.sum() if den.sum() else np.nan
    return est, np.nanpercentile(vals, 2.5), np.nanpercentile(vals, 97.5), vals


def subsample(utts_list, target_tokens, rng, exclude=None):
    """Random utterance order without replacement; whole utterances until >= target tokens. Returns indices."""
    order = rng.permutation(len(utts_list))
    out = []
    tot = 0
    for i in order:
        if exclude is not None and i in exclude:
            continue
        out.append(i)
        tot += len(utts_list[i])
        if tot >= target_tokens:
            break
    return out


def write_json(path: Path, obj) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=1, ensure_ascii=False, default=_default) + "\n", encoding="utf-8")


def _default(o):
    if isinstance(o, (np.integer,)):
        return int(o)
    if isinstance(o, (np.floating,)):
        return float(o)
    if isinstance(o, np.ndarray):
        return o.tolist()
    if isinstance(o, (set, frozenset)):
        return sorted(o)
    raise TypeError(type(o))
