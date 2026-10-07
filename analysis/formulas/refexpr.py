"""Referring-expression inventory, syntactic slot (spaCy) and syllable counts (plan section 5)."""
from __future__ import annotations

import re
from functools import lru_cache

PLAYERS = {
    "tv_2019wimF": ("federer", "djokovic"),
    "tv_2023wimF": ("djokovic", "alcaraz"),
}
FIRST = {"roger": "federer", "novak": "djokovic", "carlos": "alcaraz"}
HYPO = {"nole": "djokovic", "rog": "federer", "carlitos": "alcaraz"}
SURN = ("federer", "djokovic", "alcaraz")

# (regex over the space-joined lower-case word sequence, category). Longest alternatives first; order matters.
PATTERNS = [
    (r"roger federer", "full_name"),
    (r"novak djokovic", "full_name"),
    (r"carlos alcaraz", "full_name"),
    (r"mr (?:federer|djokovic|alcaraz)", "title_surname"),
    (r"the swiss maestro|the great swiss|the swiss", "epithet"),
    (r"the man from (?:basel|belgrade|murcia|el palmar|switzerland|serbia|spain)", "epithet"),
    (r"the maestro", "epithet"),
    (r"the (?:young |younger |great )?(?:serbian|serb)", "epithet"),
    (r"the (?:young |younger |great )?spaniard", "epithet"),
    (r"the world number (?:one|1)", "epithet"),
    (r"the (?:number (?:one|1|two|2)|top|first|second) seed", "epithet"),
    (r"the (?:defending |reigning )?champion", "epithet"),
    (r"the (?:older|younger|young) man", "epithet"),
    (r"the \w+ time (?:grand slam |wimbledon )?champion", "epithet"),
    (r"the \w+ year old", "epithet"),
    (r"federer|djokovic|alcaraz", "surname"),
    (r"roger|novak|carlos", "first_name"),
    (r"nole|rog|carlitos", "hypocoristic"),
]
FIXED_REFERENT_EPITHETS = {}  # every epithet is assigned by hand verdict (hand/epithet_referents.tsv)

PRON = {"he", "him", "his", "himself", "he's", "he'd", "he'll"}

SLOTMAP = {
    "nsubj": "subject", "nsubjpass": "subject", "csubj": "subject", "csubjpass": "subject", "expl": "subject",
    "dobj": "object", "obj": "object", "iobj": "object", "dative": "object", "attr": "object", "oprd": "object",
    "poss": "possessive",
    "pobj": "after_preposition", "agent": "after_preposition",
    "npadvmod": "vocative_exclamation", "intj": "vocative_exclamation", "vocative": "vocative_exclamation",
}


def word_seq(doc):
    """Non-punctuation spaCy tokens except possessive/clitic 's; returns (lower words, spaCy indices)."""
    words, idx = [], []
    for t in doc:
        if t.is_punct or t.is_space or t.text in ("-", "–", "—"):
            continue
        if t.text.lower() in ("'s", "’s") and t.dep_ in ("case", "poss"):
            continue
        txt = t.text.lower().replace("’", "'")
        if txt.endswith("'s") and len(txt) > 2:
            txt = txt[:-2]
        words.append(txt)
        idx.append(t.i)
    return words, idx


def find_expressions(doc):
    """List of dicts: start/end spaCy token indices, words, category."""
    words, idx = word_seq(doc)
    s = " ".join(words)
    starts = []
    p = 0
    for w in words:
        starts.append(p)
        p += len(w) + 1
    pos2tok = {st: k for k, st in enumerate(starts)}
    taken = [False] * len(words)
    out = []
    for pat, cat in PATTERNS:
        for m in re.finditer(r"(?<![\w'])(?:" + pat + r")(?![\w'])", s):
            if m.start() not in pos2tok:
                continue
            k0 = pos2tok[m.start()]
            k1 = k0 + len(m.group(0).split())
            if any(taken[k0:k1]):
                continue
            for k in range(k0, k1):
                taken[k] = True
            out.append({"k0": k0, "k1": k1, "t0": idx[k0], "t1": idx[k1 - 1] + 1, "expr": m.group(0), "category": cat})
    out.sort(key=lambda d: d["t0"])
    return out


def referent(expr, cat):
    if cat in ("full_name", "surname", "title_surname"):
        for s in SURN:
            if s in expr.split():
                return s
    if cat == "first_name":
        return FIRST[expr]
    if cat == "hypocoristic":
        return HYPO[expr]
    return None  # epithets: hand verdict


def slot_of(doc, t0, t1):
    span = doc[t0:t1]
    root = span.root
    tok = root
    poss = any(c.dep_ == "case" and c.text.lower() in ("'s", "’s", "'") for c in root.children) or root.dep_ == "poss"
    if poss:
        return "possessive", root.dep_
    dep = tok.dep_
    for _ in range(6):
        if dep in ("conj", "appos") and tok.head is not tok:
            tok = tok.head
            dep = tok.dep_
            if any(c.dep_ == "case" for c in tok.children) or dep == "poss":
                return "possessive", root.dep_ + ">" + dep
        else:
            break
    if dep in SLOTMAP:
        if dep == "pobj" or dep == "agent":
            return "after_preposition", root.dep_
        return SLOTMAP[dep], root.dep_
    sent = tok.sent
    has_verb = any(t.pos_ in ("VERB", "AUX") for t in sent)
    if dep == "ROOT" and not has_verb:
        return "vocative_exclamation", root.dep_
    if dep == "dep" and tok.i == sent.start:
        return "vocative_exclamation", root.dep_
    return "other", root.dep_


# ---------------------------------------------------------------- syllables
_ONES = "zero one two three four five six seven eight nine ten eleven twelve thirteen fourteen fifteen sixteen seventeen eighteen nineteen".split()
_TENS = "_ _ twenty thirty forty fifty sixty seventy eighty ninety".split()


def num_words(n: int) -> list[str]:
    if n < 20:
        return [_ONES[n]]
    if n < 100:
        return [_TENS[n // 10]] + ([_ONES[n % 10]] if n % 10 else [])
    if n < 1000:
        return [_ONES[n // 100], "hundred"] + (num_words(n % 100) if n % 100 else [])
    if n < 10000:
        return num_words(n // 1000) + ["thousand"] + (num_words(n % 1000) if n % 1000 else [])
    return list(str(n))


@lru_cache(maxsize=None)
def _cmu():
    import cmudict
    return cmudict.dict()


def syll_word(w: str) -> int:
    w = w.lower().strip("'")
    if not w:
        return 0
    if w.isdigit():
        return sum(syll_word(x) for x in num_words(int(w)))
    d = _cmu()
    if w in d:
        return sum(1 for ph in d[w][0] if ph[-1].isdigit())
    groups = re.findall(r"[aeiouy]+", w)
    n = len(groups)
    if w.endswith("e") and not w.endswith(("le", "ee")) and n > 1:
        n -= 1
    return max(1, n)


def syllables(expr: str, possessive: bool) -> int:
    ws = expr.split()
    n = sum(syll_word(w) for w in ws)
    if possessive and re.search(r"(s|z|x|ch|sh|ce|ge)$", ws[-1]):
        n += 1
    return n
