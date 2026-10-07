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
                out.append({"utt_id": f"press:{k}", "group": iv.get("player") or f"iv{k}", "toks": toks,
                            "date": iv.get("date") or ""})
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
    """Percentile bootstrap CI for sum(num)/sum(den), resampling utterances (within strata if given).
    Returns (estimate, lo, hi, draws)."""
    num = np.asarray(num, float)
    den = np.asarray(den, float)
    rng = np.random.default_rng(seed)
    if strata is None:
        strata = np.zeros(len(num), dtype=int)
    strata = np.asarray(strata)
    sn = np.zeros(B)
    sd = np.zeros(B)
    for s_ in np.unique(strata):
        g = np.where(strata == s_)[0]
        idx = g[rng.integers(0, len(g), size=(B, len(g)))]
        sn += num[idx].sum(1)
        sd += den[idx].sum(1)
    with np.errstate(invalid="ignore", divide="ignore"):
        vals = sn / sd
    est = num.sum() / den.sum() if den.sum() else np.nan
    return float(est), float(np.nanpercentile(vals, 2.5)), float(np.nanpercentile(vals, 97.5)), vals


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


# ---------------------------------------------------------------- fast identification (replicates)
def formula_set_fast(utts, m: int = 2, nmax: int = 12, stop_filter: bool = True):
    """Same result as formula_set(..., min_gap=None) but without per-key sets (last-seen utterance trick)."""
    last = {}
    cnt = {}
    for ui, toks in enumerate(utts):
        L = len(toks)
        for n in range(2, min(nmax, L) + 1):
            for i in range(L - n + 1):
                g = tuple(toks[i:i + n])
                if last.get(g) != ui:
                    last[g] = ui
                    cnt[g] = cnt.get(g, 0) + 1
    F = {g for g, c in cnt.items() if c >= m}
    if stop_filter:
        F = {g for g in F if not all(t in STOP for t in g)}
    return F


def system_set_fast(utts, names, nmin=2, nmax=6, min_occ=3, min_utts=3, stop_filter=True):
    """Same criteria as system_set (>= 2 distinct fillers, >= min_occ occurrences in >= min_utts utterances);
    returns the set of frame keys only."""
    occ = {}
    nutt = {}
    last = {}
    fil1 = {}
    multi = set()
    for ui, toks in enumerate(utts):
        L = len(toks)
        for n in range(nmin, min(nmax, L) + 1):
            for i in range(L - n + 1):
                for key, fil in frame_keys(toks, i, n, names):
                    if key[2] == "OPEN" and n < 3:
                        continue
                    occ[key] = occ.get(key, 0) + 1
                    if last.get(key) != ui:
                        last[key] = ui
                        nutt[key] = nutt.get(key, 0) + 1
                    f0 = fil1.get(key)
                    if f0 is None:
                        fil1[key] = fil
                    elif f0 != fil:
                        multi.add(key)
    S = set()
    for key in multi:
        if occ[key] < min_occ or nutt[key] < min_utts:
            continue
        if stop_filter and all(t in STOP for t in key[3]):
            continue
        S.add(key)
    return S


def cover_b_set(toks, S: set, names, nmin=2, nmax=6) -> np.ndarray:
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


def densities(meas_utts, F, S, names, n_min=2, masks=None):
    """Per-utterance arrays (tokens, covered a, covered a+b). S may be a set or dict of frame keys."""
    k = len(meas_utts)
    n = np.zeros(k, dtype=np.int64)
    ca = np.zeros(k, dtype=np.int64)
    cab = np.zeros(k, dtype=np.int64)
    Sset = set(S) if S is not None else set()
    for j, toks in enumerate(meas_utts):
        a = cover_a(toks, F, n_min=n_min) > 0
        b = cover_b_set(toks, Sset, names) if Sset else np.zeros(len(toks), bool)
        keep = masks[j] if masks is not None else np.ones(len(toks), bool)
        n[j] = keep.sum()
        ca[j] = (a & keep).sum()
        cab[j] = ((a | b) & keep).sum()
    return n, ca, cab


def ratio(num, den):
    num = np.asarray(num).sum()
    den = np.asarray(den).sum()
    return float(num / den) if den else float("nan")


# ---------------------------------------------------------------- official-call masks (plan S5)
def official_mask(toks, names) -> np.ndarray:
    """True = keep; False = token inside an umpire/Hawk-Eye/announcer pattern (plan section 8, S5)."""
    nm = "(?:" + "|".join(sorted(re.escape(x) for x in names)) + ")(?:'s)?"
    ords = "(?:first|second|third|fourth|fifth|final)"
    pats = [
        rf"\bgame (?:mr |miss |ms )?{nm}\b",
        rf"\b{nm} leads? (?:by )?\w+ (?:games?|sets?) to \w+(?: {ords} set)?\b",
        rf"\b\w+ games? all(?: {ords} set)?\b",
        rf"\b(?:mr |miss |ms )?{nm} is challenging\b",
        r"\b(?:mr |miss |ms )?\w+ has \w+ challenges? (?:remaining|left)\b",
        r"\bchallenges? remaining\b",
        r"\b(?:service line |line )?ball was called(?: out| in| wide| long)?\b",
        r"\bnew balls please\b",
        r"\b(?:thank you )+please\b",
        r"\bplease thank you\b",
        r"\btime violation(?: warning)?\b",
        r"\bplayers ready\b",
    ]
    s = " ".join(toks)
    # char offset -> token index
    starts = []
    pos = 0
    for t in toks:
        starts.append(pos)
        pos += len(t) + 1
    keep = np.ones(len(toks), dtype=bool)
    for p in pats:
        for mt in re.finditer(p, s):
            a, b = mt.start(), mt.end()
            for ti, st in enumerate(starts):
                if st >= a and st < b:
                    keep[ti] = False
    return keep


# ---------------------------------------------------------------- revision 1 (plan.md addendum 2): stricter coverage family
# Numerals for the "content" filter: digit strings, tennis score words, English cardinal and ordinal number words.
NUMERAL_WORDS = frozenset("""
love fifteen thirty forty deuce
zero one two three four five six seven eight nine ten eleven twelve thirteen fourteen sixteen seventeen eighteen nineteen
twenty fifty sixty seventy eighty ninety hundred thousand million
first second third fourth fifth sixth seventh eighth ninth tenth eleventh twelfth
""".split())


def is_numeral(tok: str) -> bool:
    return tok.isdigit() or tok in NUMERAL_WORDS


def is_function_or_numeral(tok: str) -> bool:
    return tok in STOP or is_numeral(tok)


def content_formulas(F) -> set:
    """Formulas with at least one token that is neither a STOP word nor a numeral."""
    return {g for g in F if not all(is_function_or_numeral(t) for t in g)}


# Definitions of the coverage family. 'base' is the pre-registered (a) measure (n >= 2, not stop-only).
FAMILY = ("base", "n3", "n4", "content", "content_n3")
FAMILY_LABEL = {
    "base": "n >= 2, not stop-only (pre-registered (a))",
    "n3": "n >= 3",
    "n4": "n >= 4",
    "content": "n >= 2, not function-word/numeral-only",
    "content_n3": "n >= 3, not function-word/numeral-only",
}


def cover_family_utt(toks, F, Fc) -> dict:
    """Per-token boolean coverage under each FAMILY definition. F = formulas of I, Fc = content_formulas(F)."""
    mx = cover_a(toks, F)
    mc = cover_a(toks, Fc) if Fc is not None else mx
    return {"base": mx >= 2, "n3": mx >= 3, "n4": mx >= 4, "content": mc >= 2, "content_n3": mc >= 3}


def family_arrays(utts, F, Fc=None, masks=None) -> dict:
    """Per-utterance arrays: 'tokens' and covered tokens under each FAMILY definition."""
    if Fc is None:
        Fc = content_formulas(F)
    out = {k: np.zeros(len(utts), dtype=np.int64) for k in ("tokens",) + FAMILY}
    for j, toks in enumerate(utts):
        fam = cover_family_utt(toks, F, Fc)
        keep = masks[j] if masks is not None else np.ones(len(toks), bool)
        out["tokens"][j] = keep.sum()
        for k in FAMILY:
            out[k][j] = (fam[k] & keep).sum()
    return out


# ---------------------------------------------------------------- revision 1: umpire-type and score-call patterns (S5b)
SCORE_TOKS = "(?:0|15|30|40|love|fifteen|thirty|forty|13|14|50)"  # 13/14/50 = documented ASR confusions of thirty/forty/fifteen


def official_mask_v2(toks, names) -> np.ndarray:
    """True = keep. S5 patterns plus (revision 1): `mr <name>`, `advantage <name>`, `game set (and match) <name>`,
    `game and <ordinal> set <name>`, `<name>... (is) challenging (the call)`, `<name>... has <n> challenge(s) remaining/left`,
    bare `thank you` (with following `players`/`please`/`all`), and point-score calls (`<score> <score|all>`, `deuce`).
    Score calls are said by the umpire and by commentators; the transcript does not tell them apart."""
    keep = official_mask(toks, names)
    nm = "(?:" + "|".join(sorted(re.escape(x) for x in names)) + ")(?:'s)?"
    ords = "(?:first|second|third|fourth|fifth|final)"
    pats = [
        rf"\bmr {nm}\b",
        rf"\badvantage {nm}\b",
        rf"\bgame (?:and )?set(?: and match)? {nm}\b",
        rf"\bgame and {ords} set {nm}\b",
        rf"\b(?:{nm} )+(?:is )?challenging(?: the call)?\b",
        rf"\b(?:{nm} )+has (?:\w+) challenges? (?:remaining|left)\b",
        r"\bthank you(?: (?:players|please|all))*\b",
        rf"\b{SCORE_TOKS} (?:{SCORE_TOKS}|all)\b",
        r"\bdeuce\b",
    ]
    s = " ".join(toks)
    starts = []
    pos = 0
    for t in toks:
        starts.append(pos)
        pos += len(t) + 1
    for p in pats:
        for mt in re.finditer(p, s):
            a, b = mt.start(), mt.end()
            for ti, st in enumerate(starts):
                if a <= st < b:
                    keep[ti] = False
    return keep


# ---------------------------------------------------------------- contexts (plan sections 4-5)
def _f(x):
    try:
        if x is None or x == "":
            return None
        v = float(x)
        return None if np.isnan(v) else v
    except (TypeError, ValueError):
        return None


def load_points(tag: str) -> dict:
    import csv
    pts = {}
    with open(TIMING / f"points_{tag}.csv", encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            pts[int(r["point_idx"])] = r
    return pts


def _pt_val(x, tb):
    if tb:
        return int(x)
    return {"0": 0, "15": 1, "30": 2, "40": 3, "AD": 4}[x]


def score_situation(r: dict, final_set_tb_target: int) -> str:
    """Most pressing category of the PBP state before the point (plan section 4)."""
    tb = r["tiebreak"] == "True"
    set_no = int(r["set_no"])
    p = [_pt_val(r["pts_before_p1"], tb), _pt_val(r["pts_before_p2"], tb)]
    g = [int(r["games_before_p1"]), int(r["games_before_p2"])]
    s = [int(r["sets_before_p1"]), int(r["sets_before_p2"])]
    server = int(r["server_pbp"]) - 1
    cats = set()
    for x in (0, 1):
        o = 1 - x
        if tb:
            target = final_set_tb_target if set_no == 5 else 7
            gp = p[x] >= target - 1 and p[x] - p[o] >= 1
        else:
            gp = (p[x] == 3 and p[o] <= 2) or p[x] == 4
        if not gp:
            continue
        if tb:
            sp = True
        else:
            gx = g[x] + 1
            sp = gx >= 6 and gx - g[o] >= 2
            if set_no < 5 and g[x] == 6 and g[o] == 5:
                sp = True
        if sp and s[x] == 2:
            cats.add("match_point")
        elif sp:
            cats.add("set_point")
        elif x != server and not tb:
            cats.add("break_point")
    for c in ("match_point", "set_point", "break_point"):
        if c in cats:
            return c
    if tb:
        return "tiebreak"
    if p[0] >= 3 and p[1] >= 3:
        return "deuce_ad"
    return "other"


def tercile(values):
    """Return (labels, cuts): T1/T2/T3 by the 1/3 and 2/3 quantiles of the non-missing values; NA if missing."""
    v = np.array([x for x in values if x is not None], float)
    q1, q2 = np.quantile(v, [1 / 3, 2 / 3])
    lab = []
    for x in values:
        if x is None:
            lab.append("NA")
        elif x <= q1:
            lab.append("T1")
        elif x <= q2:
            lab.append("T2")
        else:
            lab.append("T3")
    return lab, (float(q1), float(q2))


STREAM_TAG = {MAIN: "2019wimF", HELDOUT: "2023wimF"}
FINAL_SET_TB = {MAIN: 7, HELDOUT: 10}


def add_contexts(recs: list[dict], stream: str) -> dict:
    """Adds ctx_* fields to the records of a final (2019/2023). Returns tercile cut points."""
    pts = load_points(STREAM_TAG[stream])
    allrecs = []
    with open(TRANSCRIPTS / f"{stream}.jsonl", encoding="utf-8") as fh:
        for line in fh:
            allrecs.append(json.loads(line))
    by_i = {r["clip_i"]: r for r in allrecs}
    for r in recs:
        p = r.get("point_idx_pbp")
        r["ctx_dt_before"] = _f(r.get("dead_time_before_s"))
        ta = None
        if p is not None:
            if r["clip_role"] == "first_serve_fault":
                nxt = by_i.get(r["clip_i"] + 1)
                if nxt is not None and nxt.get("point_idx_pbp") == p:
                    ta = _f(r.get("t_to_next_first_hit_s"))
            else:
                nr = pts.get(int(p) + 1)
                if nr is not None:
                    ta = _f(nr.get("dead_time_before_s"))
        r["ctx_time_after"] = ta
        r["ctx_score"] = score_situation(pts[int(p)], FINAL_SET_TB[stream]) if p is not None else "NA"
        r["ctx_phase"] = r.get("phase") or "clip"
        r["ctx_role"] = r.get("clip_role") or "NA"
    lb, cb = tercile([r["ctx_dt_before"] for r in recs])
    la, ca = tercile([r["ctx_time_after"] for r in recs])
    for r, x, y in zip(recs, lb, la):
        r["ctx_dtb_terc"] = x
        r["ctx_ta_terc"] = y
    return {"dead_time_before_s": cb, "time_after_s": ca}


def excerpt(toks, i, n, width=15):
    """Lower-cased token window of at most `width` tokens containing toks[i:i+n]."""
    extra = max(0, width - n)
    a = max(0, i - extra // 2)
    b = min(len(toks), a + width)
    a = max(0, b - width)
    return " ".join(toks[a:b])
