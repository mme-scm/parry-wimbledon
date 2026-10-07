"""Shared Greek-text utilities: normalisation, tokenisation, letter analysis.

Everything here is deterministic and rule-based; no Greek text is stored.
"""
import re
import unicodedata

# combining marks (NFD)
ACUTE, GRAVE, CIRC = "́", "̀", "͂"
SMOOTH, ROUGH = "̓", "̔"
DIAER, ISUB = "̈", "ͅ"
MACRON, BREVE = "̄", "̆"
ACCENTS = {ACUTE, GRAVE, CIRC}
ALL_MARKS = {ACUTE, GRAVE, CIRC, SMOOTH, ROUGH, DIAER, ISUB, MACRON, BREVE}

# elision marks found in Greek e-texts; normalised to U+02BC
APOSTROPHES = "ʼ’'᾽᾿̓"
ELISION = "ʼ"

VOWELS = set("αεηιουω")
CONSONANTS = set("βγδζθκλμνξπρστφχψ")  # ς mapped to σ before lookup
DOUBLE = set("ζξψ")
STOPS = set("πβφτδθκγχ")
LIQUIDS = set("λρμν")

GREEK_LETTER_RE = re.compile(r"[Ͱ-Ͽἀ-῿]")
# characters treated as punctuation when they sit at token edges
PUNCT = ",.;··;:!?\"“”‘«»()[]⟨⟩—–-…"


def nfc(s):
    return unicodedata.normalize("NFC", s)


def norm_apostrophes(s):
    """Map every apostrophe-like character that ends a word to U+02BC."""
    out = []
    for i, ch in enumerate(s):
        if ch in "’'᾽᾿":
            out.append(ELISION)
        else:
            out.append(ch)
    return "".join(out)


def strip_marks(s, keep_isub=False, keep_diaer=False):
    """Remove accents, breathings (and by default diaeresis, iota subscript)."""
    d = unicodedata.normalize("NFD", s)
    keep = set()
    if keep_isub:
        keep.add(ISUB)
    if keep_diaer:
        keep.add(DIAER)
    d = "".join(c for c in d if not (unicodedata.combining(c) and c not in keep))
    return unicodedata.normalize("NFC", d)


def loose(s):
    """Accent-, breathing-, diaeresis-, case-insensitive form; final sigma -> σ;
    apostrophes -> U+02BC.  Iota subscript is dropped."""
    s = norm_apostrophes(nfc(s))
    s = strip_marks(s).lower().replace("ς", "σ")
    return s


def grave_to_acute(s):
    d = unicodedata.normalize("NFD", s)
    return unicodedata.normalize("NFC", d.replace(GRAVE, ACUTE))


def form_key(word):
    """Normalised word form for lexical tables (dichrona, licences):
    NFC, lowercase, apostrophes -> U+02BC, grave -> acute, and an enclitic-
    induced second acute on the final syllable removed (ἄλγεά -> ἄλγεα)."""
    w = norm_apostrophes(nfc(word)).lower().replace("ς", "σ")
    w = grave_to_acute(w)
    d = unicodedata.normalize("NFD", w)
    acc_pos = [i for i, c in enumerate(d) if c in ACCENTS]
    if len(acc_pos) >= 2:
        last = acc_pos[-1]
        d = d[:last] + d[last + 1:]
    w = unicodedata.normalize("NFC", d)
    if w.endswith("σ"):
        w = w[:-1] + "ς"
    return w


class Letter:
    __slots__ = ("ch", "base", "marks", "upper")

    def __init__(self, ch, base, marks, upper):
        self.ch = ch          # original (NFC) character(s)
        self.base = base      # lowercase base letter, ς -> σ
        self.marks = marks    # set of combining marks
        self.upper = upper

    @property
    def is_vowel(self):
        return self.base in VOWELS

    @property
    def is_cons(self):
        return self.base in CONSONANTS

    @property
    def accent(self):
        for m in (ACUTE, GRAVE, CIRC):
            if m in self.marks:
                return m
        return None

    @property
    def breathing(self):
        if ROUGH in self.marks:
            return ROUGH
        if SMOOTH in self.marks:
            return SMOOTH
        return None

    def __repr__(self):
        return f"L({self.ch})"


def letters(word):
    """Split an NFC word into Letter objects (combining marks attached)."""
    out = []
    for ch in nfc(word):
        d = unicodedata.normalize("NFD", ch)
        base = d[0]
        marks = set(d[1:])
        low = base.lower()
        if low == "ς":
            low = "σ"
        out.append(Letter(ch, low, marks, base != base.lower()))
    return out


class Token:
    """A word token of a verse line."""
    __slots__ = ("i", "text", "core", "start", "end", "elided", "lead", "trail")

    def __init__(self, i, text, core, start, end, elided, lead, trail):
        self.i = i
        self.text = text      # the whitespace-delimited token as in the line
        self.core = core      # token without edge punctuation (elision mark kept)
        self.start = start    # char offset of core in the line
        self.end = end
        self.elided = elided
        self.lead = lead
        self.trail = trail

    def __repr__(self):
        return f"Token({self.core})"


def tokenize(line):
    """Whitespace tokens that contain Greek letters, with edge punctuation
    removed and char offsets into `line` (which should be NFC)."""
    toks = []
    for m in re.finditer(r"\S+", line):
        t = m.group()
        if not GREEK_LETTER_RE.search(t):
            continue
        s, e = 0, len(t)
        while s < e and t[s] in PUNCT:
            s += 1
        while e > s and t[e - 1] in PUNCT:
            e -= 1
        core = t[s:e]
        core_n = norm_apostrophes(core)
        elided = core_n.endswith(ELISION)
        toks.append(Token(len(toks), t, core_n, m.start() + s, m.start() + e, elided, t[:s], t[e:]))
    return toks


def has_accent(word):
    d = unicodedata.normalize("NFD", word)
    return any(c in ACCENTS for c in d)
