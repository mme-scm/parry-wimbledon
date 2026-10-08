"""Shared definitions for Phase 2b (analysis/parry/plan.md).

Reuses analysis/formulas/common.py (tokeniser, STOP list, n-gram and system machinery, official-call patterns) unchanged.
Adds: team loaders (20 TV streams, Cornell live text, press answers), the 2b normalisation (<num>, <name>), a joint
n-gram index + inventory builder, coverage by an inventory, the unigram-preserving shuffle, the situational slot classifier
(plan section 5), and the vertex bootstrap. All scripts in this directory run with `python -I` and add the two analysis
directories to sys.path explicitly.
"""
from __future__ import annotations

import csv
import json
import re
import sys
from collections import Counter
from functools import lru_cache
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
sys.path.insert(0, str(ROOT / "analysis" / "formulas"))
import common as C  # noqa: E402

RESULTS = HERE / "results"
FIGURES = HERE / "figures"
HAND = HERE / "hand"
SEED = 20261007

TV = C.tv_streams()                      # 20 streams, sorted
MAIN, HELDOUT = C.MAIN, C.HELDOUT
PRESS_SPEAKERS = ("Roger Federer", "Novak Djokovic", "Andy Murray", "Rafael Nadal")
NAMES = C.player_name_lexicon()          # 44 tokens (Phase 2 lexicon)
NUM_TOKEN = "<num>"
NAME_TOKEN = "<name>"


def short(stream: str) -> str:
    """Compact label of a stream id, e.g. 'tv_pool_20220130-M-Australian_Open-F-...' -> '2022 AO M F Nadal-Medvedev'."""
    if stream == MAIN:
        return "2019 WIM M F Federer-Djokovic"
    if stream == HELDOUT:
        return "2023 WIM M F Alcaraz-Djokovic"
    if not stream.startswith("tv_pool_"):
        return stream
    mid = stream[len("tv_pool_"):]
    p = mid.split("-")
    slam = {"Australian_Open": "AO", "Roland_Garros": "RG", "Wimbledon": "WIM", "US_Open": "USO"}.get(p[2], p[2])
    return f"{p[0][:4]} {slam} {p[1]} {p[3]} {p[4].split('_')[-1]}-{p[5].split('_')[-1]}"


def match_id(stream: str) -> str:
    with open(C.TRANSCRIPTS / f"{stream}.jsonl", encoding="utf-8") as fh:
        return json.loads(fh.readline())["match_id"]


def stream_meta(stream: str) -> dict:
    """Year, slam, gender, round, the two players (full names) and the broadcaster hint of a TV stream."""
    mid = match_id(stream)
    p = mid.split("-")
    with open(C.TRANSCRIPTS / f"{stream}.jsonl", encoding="utf-8") as fh:
        hint = json.loads(fh.readline()).get("broadcaster_hints") or ""
    return {"stream": stream, "match_id": mid, "year": int(p[0][:4]), "gender": p[1],
            "slam": {"Australian_Open": "AO", "Roland_Garros": "RG", "Wimbledon": "WIM", "US_Open": "USO"}[p[2]],
            "round": p[3], "players": (p[4].replace("_", " "), p[5].replace("_", " ")), "hint": hint}


# hint clusters from corpus/README.md and meta_*.csv broadcaster_hints (all [unverified]); plan section 8
HINT_CLUSTER = {MAIN: "Tim", HELDOUT: "Tim",
                "tv_pool_20220130-M-Australian_Open-F-Rafael_Nadal-Daniil_Medvedev": "Brad",
                "tv_pool_20210911-W-US_Open-F-Emma_Raducanu-Leylah_Fernandez": "Kim"}


# ---------------------------------------------------------------- normalisation (plan section 1)
def norm_tokens(toks, extra_names=frozenset()):
    out = []
    for t in toks:
        b = C.strip_poss(t)
        if b in NAMES or b in extra_names:
            out.append(NAME_TOKEN + ("'s" if t.endswith("'s") else ""))
        elif C.is_num(t):
            out.append(NUM_TOKEN)
        else:
            out.append(t)
    return out


# ---------------------------------------------------------------- teams
class Team:
    """One team: lists of raw and normalised token lists (aligned 1:1), utterance ids, and per-utterance records."""

    def __init__(self, name, raw, norm, ids, recs=None, medium="tv"):
        self.name, self.raw, self.norm, self.ids, self.recs, self.medium = name, raw, norm, ids, recs, medium
        self.ntok = sum(len(u) for u in raw)


def load_tv(stream, field="text_corrected"):
    recs = C.load_stream(stream, field)
    raw = [r["toks"] for r in recs]
    norm = [norm_tokens(t) for t in raw]
    return Team(stream, raw, norm, [r["utt_id"] for r in recs], recs, "tv")


def load_cornell():
    recs = C.load_stream(C.TEXT)
    raw, norm = [], []
    for r in recs:
        extra = frozenset(C.tokenize(" ".join(r.get("players") or [])))
        raw.append(r["toks"])
        norm.append(norm_tokens(r["toks"], extra))
    return Team("cornell", raw, norm, [r["utt_id"] for r in recs], None, "text")


@lru_cache(maxsize=1)
def _press():
    return C.load_press_answers()


def load_press(speaker=None):
    out_raw, out_norm, ids = [], [], []
    for r in _press():
        if speaker is not None and r["group"] != speaker:
            continue
        extra = frozenset(C.tokenize(r["group"]))
        out_raw.append(r["toks"])
        out_norm.append(norm_tokens(r["toks"], extra))
        ids.append(r["utt_id"])
    name = "press_pooled" if speaker is None else "press_" + C.tokenize(speaker)[-1]
    return Team(name, out_raw, out_norm, ids, None, "press")


def load_all_teams():
    teams = [load_tv(s) for s in TV]
    teams.append(load_cornell())
    teams.append(load_press(None))
    for sp in PRESS_SPEAKERS:
        teams.append(load_press(sp))
    return teams


# ---------------------------------------------------------------- index, inventory, coverage
def is_stop_only(g):
    return all(t in C.STOP for t in g)


def is_content_free(g):
    return all(t in C.STOP or C.is_numeral(t) or t == NUM_TOKEN for t in g)


def index_inventory(utts, nmax=12, m=2):
    """One pass over utts: occ = dict ngram -> list of flat start positions (n = 2..nmax);
    F = formulas (in >= m distinct utterances, not stop-only). Returns (occ, F, n_tokens)."""
    occ = {}
    last = {}
    cnt = {}
    off = 0
    for ui, toks in enumerate(utts):
        L = len(toks)
        for n in range(2, min(nmax, L) + 1):
            for i in range(L - n + 1):
                g = tuple(toks[i:i + n])
                lst = occ.get(g)
                if lst is None:
                    occ[g] = [off + i]
                else:
                    lst.append(off + i)
                if last.get(g) != ui:
                    last[g] = ui
                    cnt[g] = cnt.get(g, 0) + 1
        off += L
    F = {g for g, c in cnt.items() if c >= m and not is_stop_only(g)}
    return occ, F, off


def coverage(occ, ntok, F, nmin=2):
    """Share of the indexed text's tokens covered by an occurrence of an n-gram of F with len >= nmin."""
    if ntok == 0:
        return float("nan")
    cov = np.zeros(ntok, dtype=bool)
    for g in F:
        n = len(g)
        if n < nmin:
            continue
        pos = occ.get(g)
        if pos:
            for p in pos:
                cov[p:p + n] = True
    return float(cov.mean())


def variants(F):
    """The three inventory variants of plan section 2."""
    return {"base": F, "n3": {g for g in F if len(g) >= 3}, "content": {g for g in F if not is_content_free(g)}}


def shuffle_utts(utts, rng):
    """Unigram-preserving shuffle: tokens permuted over all positions; utterance lengths kept."""
    flat = [t for u in utts for t in u]
    perm = rng.permutation(len(flat))
    flat = [flat[i] for i in perm]
    out, k = [], 0
    for u in utts:
        out.append(flat[k:k + len(u)])
        k += len(u)
    return out


def subsample(n_utts_list, target, rng):
    return C.subsample(n_utts_list, target, rng)


# ---------------------------------------------------------------- situational slot classifier (plan section 5, frozen)
SLOTS = ("SCORE", "OFFICIAL", "SHOT", "JUDGE", "STAT", "CROWD", "OTHER")
TIE_ORDER = ("OFFICIAL", "SCORE", "CROWD", "STAT", "SHOT", "JUDGE")
SC = "(?:0|15|30|40|love|fifteen|thirty|forty|13|14|50|zznum)"
NM = "zzname"

OFFICIAL_PATS = [
    rf"\b(?:mr|miss|ms|mrs) {NM}\b",
    rf"\b(?:{NM} )+(?:is )?(?:challenging|charging|having a call)(?: the call)?\b",
    r"\b(?:\w+ )?has \w+ challenges? (?:remaining|left)\b",
    r"\bchallenges? remaining\b",
    r"\b(?:(?:service )?line )?ball was called(?: out| in| wide| long)?\b",
    r"\bnew balls(?: please)?\b",
    r"\bthank you(?: (?:players|please|all))*\b",
    r"\bquiet please\b",
    r"\btime violation(?: warning)?\b",
    r"\bcode violation\b",
    r"\bplayers ready\b",
    r"\bhawk ?eye\b",
    r"\boverrule[sd]?\b|\boverruled\b",
]
SCORE_PATS = [
    rf"\b{SC} (?:{SC}|all)\b",
    r"\bdeuce\b",
    rf"\badvantage (?:{NM}|server|receiver)\b",
    rf"\bgame (?:and )?(?:(?:\w+ )?set(?: and match)? )?{NM}\b",
    r"\bgame set and match\b",
    rf"\b{NM} leads? (?:by )?\w+ (?:games?|sets?) to \w+\b",
    r"\b\w+ games? all\b",
    r"\b\w+ sets? (?:to|all) \w+\b",
    r"\b(?:break|set|match|championship|game) points?\b",
    r"\btie ?break(?:er)?s?\b",
]
_OFF_RE = [re.compile(p) for p in OFFICIAL_PATS]
_SCO_RE = [re.compile(p) for p in SCORE_PATS]


def _lex(s):
    out = set()
    for item in s.split(","):
        item = item.strip()
        if item:
            out.add(tuple(item.split()))
    return out


LEXICON = {
    "OFFICIAL": _lex("challenge, challenges, challenged, umpire, umpire's, referee, supervisor, linesman, lineswoman, line judge, the call"),
    "SCORE": _lex("love, advantage, deuce, tiebreak, tiebreaker, games all, all square, hold serve, holds serve, held serve, broken, "
                  "break back, breaks back, double break, consolidate, consolidates, consolidated"),
    "SHOT": _lex("forehand, forehands, backhand, backhands, serve, serves, served, serving, volley, volleys, volleyed, smash, smashed, overhead, "
                 "lob, lobs, lobbed, dropshot, drop shot, drop volley, slice, sliced, topspin, return, returns, returned, returner, rally, rallies, "
                 "groundstroke, groundstrokes, passing shot, net, nets, netted, tape, net cord, line, lines, baseline, sideline, tramline, tramlines, "
                 "wide, long, crosscourt, cross court, down the line, inside out, down the t, down the middle, out wide, the body, ace, aces, winner, "
                 "winners, error, errors, unforced, mishit, framed, shot, shots, swing, struck, strike, hit, hits, hitting, angle, angled, approach, "
                 "kick, kicker, spin, pace, deep, short, racket, racquet, footwork, slide, sliding, chase, chased, retrieve, retrieved, defend, defends, "
                 "defended, defending, defence, defense, scramble, scrambled, double fault, fault, faults, stroke, strokes, first serve, second serve"),
    "STAT": _lex("percent, percentage, per cent, statistics, stats, statistic, record, records, title, titles, slam, slams, grand slam, major, majors, "
                 "ranking, rankings, ranked, seed, seeded, seeds, career, history, historic, year, years, season, seasons, times, minutes, hours, hour, "
                 "mph, miles, kilometres, kilometers, km, kph, average, averaging, h2h, head to head, trophy, trophies, debut, age, aged, born, prize, "
                 "money, million, olympic, olympics, weeks, consecutive, streak, in a row, tournament, tournaments, championships, finals, semifinal, "
                 "semifinals, semi final, quarterfinal, quarterfinals, quarter final, number one, world number, first time, last year"),
    "CROWD": _lex("crowd, crowds, fans, fan, spectators, spectator, audience, applause, applauding, applaud, clapping, cheer, cheers, cheering, "
                  "cheered, chant, chanting, ovation, atmosphere, noise, roar, roars, royal, box, stands, stadium, arena, roof, rain, weather, wind, "
                  "windy, breeze, sun, sunshine, heat, hot, cold, temperature, shade, lights, seats, celebrity, celebrities, supporters, flag, flags, "
                  "centre court, center court, arthur ashe, rod laver, chatrier, wife, family, parents"),
    "JUDGE": _lex("good, great, brilliant, superb, lovely, beautiful, beautifully, fantastic, incredible, incredibly, unbelievable, amazing, "
                  "terrific, wonderful, excellent, magnificent, sensational, spectacular, extraordinary, remarkable, impressive, poor, bad, terrible, "
                  "awful, sloppy, loose, careless, tough, difficult, easy, hard, important, crucial, vital, big, huge, key, pressure, nerves, nervous, "
                  "confidence, confident, tension, tense, tight, mental, mentally, physical, physically, tired, fatigue, energy, momentum, rhythm, "
                  "focus, focused, aggressive, aggression, passive, defensive, attacking, tactics, tactical, tactically, plan, strategy, needs, need, "
                  "needed, must, should, has to, have to, got to, think, thinks, thought, feel, feels, felt, believe, believes, know, knows, little bit, "
                  "maybe, perhaps, probably, really, quite, well played, mistake, mistakes, smart, clever, brave, courage, composure, calm, frustrated, "
                  "frustration, angry, upset, emotion, emotions, emotional, happy, disappointed, relief, character, belief, what a, best, better, worse, "
                  "worst, nice, nicely, perfect, perfectly, quality, class, outstanding, typical, special, genius, wow"),
}
LEX_MAXN = max(len(g) for s in LEXICON.values() for g in s)


def canon(toks, names=NAMES):
    """Classifier view of tokens: player names -> 'zzname', 2b placeholders mapped back to pattern tokens."""
    out = []
    for t in toks:
        b = C.strip_poss(t)
        if b in names or b.startswith(NAME_TOKEN):
            out.append(NM)
        elif t == NUM_TOKEN:
            out.append("zznum")
        else:
            out.append(t)
    return out


def _pattern_mask(ct, regs):
    s = " ".join(ct)
    starts = []
    pos = 0
    for t in ct:
        starts.append(pos)
        pos += len(t) + 1
    m = np.zeros(len(ct), dtype=bool)
    for rg in regs:
        for mt in rg.finditer(s):
            a, b = mt.start(), mt.end()
            for ti, st in enumerate(starts):
                if a <= st < b:
                    m[ti] = True
    return m


class SlotClassifier:
    """Plan section 5. classify(span) on one utterance; masks are computed once per utterance."""

    def __init__(self, toks, names=NAMES):
        self.toks = list(toks)
        self.ct = canon(self.toks, names)
        self.off = _pattern_mask(self.ct, _OFF_RE)
        self.sco = _pattern_mask(self.ct, _SCO_RE)

    def _lex_counts(self, idx):
        """Lexicon hits for n-grams lying wholly inside the (sorted, contiguous-run) index list idx."""
        cnt = Counter()
        S = set(idx)
        for i in idx:
            for n in range(1, LEX_MAXN + 1):
                if all((i + k) in S for k in range(n)) and i + n <= len(self.ct):
                    g = tuple(self.ct[i:i + n])
                    for slot, lx in LEXICON.items():
                        if g in lx:
                            cnt[slot] += 1
        return cnt

    def _decide(self, idx):
        if not idx:
            return None
        if any(self.off[i] for i in idx):
            return "OFFICIAL"
        if any(self.sco[i] for i in idx):
            return "SCORE"
        cnt = self._lex_counts(idx)
        if not cnt:
            return None
        best = max(cnt.values())
        for s in TIE_ORDER:
            if cnt.get(s, 0) == best:
                return s
        return None

    def classify(self, a, b, window=4):
        L = len(self.toks)
        s = self._decide(list(range(max(0, a), min(L, b))))
        if s is None:
            s = self._decide(list(range(max(0, a - window), min(L, b + window))))
        return s or "OTHER"

    def classify_context(self, a, b, window=4):
        """Reference-level slot: the window on either side of [a, b), excluding [a, b) itself."""
        L = len(self.toks)
        idx = list(range(max(0, a - window), a)) + list(range(b, min(L, b + window)))
        return self._decide(idx) or "OTHER"

    def token_slots(self):
        return [self.classify(t, t + 1) for t in range(len(self.toks))]


# ---------------------------------------------------------------- vertex bootstrap (plan section 3)
def vertex_boot_pairs(M, B, rng):
    """M: n x n matrix (diagonal ignored). Returns B bootstrap means over ordered pairs of resampled positions with
    different original streams."""
    n = M.shape[0]
    out = np.empty(B)
    for b in range(B):
        idx = rng.integers(0, n, n)
        sub = M[np.ix_(idx, idx)]
        mask = idx[:, None] != idx[None, :]
        out[b] = sub[mask].mean()
    return out


def vertex_boot_vs_baseline(M, base_row, B, rng):
    """H2 statistic: mean over targets j of [mean over TV sources i != j of M[i, j] - base_row[j]], vertex bootstrap."""
    n = M.shape[0]
    out = np.empty(B)
    for b in range(B):
        idx = rng.integers(0, n, n)
        vals = []
        for jb in range(n):
            j = idx[jb]
            src = [idx[a] for a in range(n) if idx[a] != j]
            if not src:
                continue
            vals.append(np.mean(M[src, j]) - base_row[j])
        out[b] = np.mean(vals)
    return out


def boot_p_two(draws, null=0.0):
    """Percentile-bootstrap two-sided p (plan section 7), floor 2/(B+1)."""
    B = len(draws)
    lo = (1 + np.sum(draws <= null)) / (B + 1)
    hi = (1 + np.sum(draws >= null)) / (B + 1)
    return float(min(1.0, 2 * min(lo, hi)))


# ---------------------------------------------------------------- io
def write_csv(path: Path, rows, fields=None):
    path.parent.mkdir(parents=True, exist_ok=True)
    rows = list(rows)
    if fields is None:
        fields = list(rows[0].keys()) if rows else []
    with open(path, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=fields, extrasaction="ignore")
        w.writeheader()
        for r in rows:
            w.writerow({k: _fmt(r.get(k)) for k in fields})


def _fmt(v):
    if isinstance(v, (float, np.floating)):
        return "" if np.isnan(v) else f"{float(v):.6g}"
    if isinstance(v, (np.integer,)):
        return int(v)
    return v


def read_csv(path: Path):
    with open(path, encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def write_json(path: Path, obj):
    C.write_json(path, obj)


def read_json(path: Path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def hit_gaps(stream):
    """Per utt_id: A_after = next clip's first hit - this clip's last hit; A_before = this first hit - previous clip's last hit;
    t_next_stored = the corpus field t_to_next_first_hit_s (valid only where the video is 25 fps). Hit clock only; all clips of the
    stream (with or without text) are used to find the neighbours."""
    rows = []
    with open(C.TRANSCRIPTS / f"{stream}.jsonl", encoding="utf-8") as fh:
        for line in fh:
            rows.append(json.loads(line))
    rows.sort(key=lambda r: r["clip_i"])
    out = {}
    for k, r in enumerate(rows):
        aa = ab = None
        if r.get("last_hit_s") is not None and k + 1 < len(rows) and rows[k + 1].get("first_hit_s") is not None:
            aa = float(rows[k + 1]["first_hit_s"]) - float(r["last_hit_s"])
        if r.get("first_hit_s") is not None and k > 0 and rows[k - 1].get("last_hit_s") is not None:
            ab = float(r["first_hit_s"]) - float(rows[k - 1]["last_hit_s"])
        out[r["utt_id"]] = {"A_after": aa, "A_before": ab, "t_next_stored": r.get("t_to_next_first_hit_s")}
    return out


def fps_valid(stream) -> bool:
    """True if clip seconds (frames/25) and hit seconds agree (25 fps video); plan 'looked at' item 4."""
    rows = []
    with open(C.TRANSCRIPTS / f"{stream}.jsonl", encoding="utf-8") as fh:
        for line in fh:
            r = json.loads(line)
            if r.get("first_hit_s") is not None:
                rows.append((r["clip_start_frame"], r["first_hit_s"]))
    x = np.array([a for a, _ in rows], float)
    y = np.array([b for _, b in rows], float)
    slope = np.polyfit(x, y, 1)[0]
    return bool(abs(1 / slope - 25.0) < 0.5)
