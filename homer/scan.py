#!/usr/bin/env python3
"""Rule-based scanner for the Homeric hexameter.

Pipeline for one verse:
  1. tokenise (homer/greek.py) and find vowel nuclei (diphthongs, diaeresis,
     iota subscript) and the consonant cluster after every nucleus, across
     word boundaries (elided words contribute only consonants);
  2. give every possible syllable (a nucleus, or two nuclei merged by
     synizesis) a set of quantity options, each with a cost and the licences
     it uses (see LICENCES and homer/README.md);
  3. align syllables to the hexameter template by exhaustive dynamic
     programming; every distinct alignment (syllable spans + quantities) is a
     scansion; the cheapest is reported first.

Metrical positions follow the half-foot numbering of O'Neill/Porter: the
longum of foot f is 2f-1; the biceps is 2f (a contracted biceps, or the
second short); the first short of a dactylic biceps is 2f-0.5.  So foot 3 is
5, 5.5, 6; Hermann's bridge concerns word end at 7.5; the penthemimeral
caesura is word end at 5, the trochaic at 5.5, the hephthemimeral at 7, the
bucolic diaeresis at 8.  The final syllable is at 12.

CLI:
    python homer/scan.py "μῆνιν ἄειδε θεὰ Πηληϊάδεω Ἀχιλῆος"
    python homer/scan.py --all-solutions "..."
    python homer/scan.py --corpus            # writes homer/scansion.tsv
"""
import argparse
import csv
import functools
import json
import math
import os
import pathlib
import re
import sys
import unicodedata

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import greek as G  # noqa: E402

HERE = pathlib.Path(__file__).resolve().parent
INF = math.inf

# ---------------------------------------------------------------------------
# licence costs.  (princeps cost, biceps cost).  Lower = preferred.
# ---------------------------------------------------------------------------
# name: (tier in princeps, cost in princeps, tier in biceps, cost in biceps, description)
# A scansion is admitted at tier t if every licence it uses has tier <= t.  The
# scanner tries tier 0, then 1, then 2, and keeps the scansions of the lowest
# tier that yields any ("minimal licence" principle).  Within a tier, costs
# rank the scansions.  INF = never allowed in that place.
LICENCES = {
    "correption": (9, INF, 0, 0.1, "epic correption: final long vowel/diphthong shortened before a vowel"),
    "hiatus_long": (0, 0.3, 1, 1.0, "final long vowel/diphthong kept long before a vowel (hiatus)"),
    "hiatus": (0, 0.2, 0, 0.2, "final short vowel not elided before a vowel (hiatus)"),
    "internal_correption": (9, INF, 1, 1.0, "long vowel/diphthong shortened before a vowel inside a word"),
    "muta_cum_liquida": (9, INF, 0, 0.6, "stop + liquid/nasal inside a word does not make position"),
    "muta_cum_liquida_initial": (9, INF, 0, 0.4, "word-initial stop + liquid/nasal does not lengthen a preceding short final vowel"),
    "no_position_initial_cluster": (9, INF, 2, 2.0, "word-initial ζ / σ+consonant does not lengthen a preceding short final vowel"),
    "lengthening_liquid": (1, 0.5, 2, 1.5, "short final vowel lengthened before initial λ μ ν ρ σ (originally double)"),
    "lengthening_closed": (1, 1.0, 9, INF, "short final syllable ending in a consonant lengthened in arsis before a vowel"),
    "lengthening_hiatus": (2, 2.5, 9, INF, "short final vowel lengthened in arsis before a vowel"),
    "metrical_lengthening": (2, 2.0, 9, INF, "short vowel lengthened in arsis before a single consonant (metrical licence)"),
    "synizesis": (1, 1.0, 1, 1.0, "two adjacent vowels in a word pronounced as one long syllable"),
    "synizesis_i": (2, 1.5, 2, 1.5, "ι or υ before a vowel pronounced consonantally (synizesis)"),
    "synizesis_cross": (1, 0.8, 1, 0.8, "synizesis across a word boundary (δή, ἤ, ἐπεί, μή, ἐγώ + vowel)"),
    "digamma": (0, 0.05, 0, 0.05, "initial ϝ (lost digamma) counted as a consonant"),
    "digamma_double": (1, 0.5, 1, 1.0, "initial σϝ/δϝ counted as two consonants"),
    "synizesis_rare": (2, 2.0, 2, 2.0, "synizesis of other vowel pairs inside a word (ἤιομεν)"),
    "digamma_internal": (0, 0.05, 0, 0.05, "δϝ after the augment counts as two consonants (ἔδεισα = ἔδδεισα)"),
    "synizesis_cross_rare": (2, 2.0, 2, 2.0, "synizesis across a word boundary after another word (Πηλείδη ἔθελʼ)"),
    "lengthening_liquid_internal": (2, 2.0, 2, 2.5, "short vowel lengthened before a single λ μ ν ρ σ inside a word (augment/compound: ἐλίσσετο)"),
    "dichronon_contra": (1, 1.5, 1, 1.5, "α/ι/υ given the quantity contrary to its unambiguous attestations elsewhere"),
    "analogy_contra": (1, 1.5, 1, 1.5, "α/ι/υ given a quantity contrary to other word forms sharing the same beginning (homer/dichrona_analogy.tsv)"),
    "accent_contra": (1, 1.2, 1, 1.2, "α/ι/υ given a quantity contrary to the accentuation (σωτῆρα / antepenult rules)"),
}
MAX_TIER = 2
# switches used only by homer/validate.py for ablation runs
RULES = {"digamma": True, "accent_rules": True, "accent_hard": False, "disabled": frozenset()}


SYNIZESIS_CROSS_FIRST = {"δή", "ἤ", "ἦ", "ἠ", "ἐπεί", "μή", "ἐγώ", "ἠέ", "ἤτοι"}

# appositives (for lexical word end; see README)
PREPOSITIVE = set("""ὁ ἡ αἱ ἐν ἐς εἰς ἐκ ἐξ εἰ αἰ ὡς οὐ οὐκ οὐχ εἰν
ἐνί ἀνά ἀπό ἐπί κατά μετά παρά περί πρό πρός προτί ποτί σύν ξύν ὑπό ὑπέρ ὑπείρ διά ἀμφί ἀντί
ἀνʼ ἀπʼ ἀφʼ ἐπʼ ἐφʼ κατʼ καθʼ μετʼ μεθʼ παρʼ ὑπʼ ὑφʼ διʼ ἀμφʼ ἀντʼ ἀνθʼ κάτ πάρ ἄμ
καί ἀλλά ἀλλʼ ἠδέ ἠδʼ ἰδέ ἰδʼ οὐδέ οὐδʼ μηδέ μηδʼ ἤ ἠέ μή""".split())
# The Homeric article forms are mostly demonstrative pronouns and are NOT treated as
# prepositives (only the unaccented proclitic ὁ ἡ αἱ are); anastrophic prepositions
# (ἄπο, ἔπι, πάρα ...) follow their noun and are not prepositives either.
POSTPOSITIVE = set("""δέ δʼ τε τʼ θʼ γε γʼ κε κεν κʼ ῥα ῥʼ ἄρ ἄρα ἄρʼ ἂρ περ τοι μοι σοι οἱ μιν νιν
σφι σφιν σφε σφεας σφωε σφωιν σφισι σφισιν μευ σευ ἑο εὑ ἑ ἕθεν που πω πως ποτε ποτʼ ποθι ποθεν πη τις τι τινα τινʼ τινες τινας
τινος τινι τευ τεο τῳ τεῳ νυ νυν θην γάρ μέν δή οὖν μʼ σʼ με σε""".split())
PROCLITIC_UNACCENTED = {"ὁ", "ἡ", "αἱ", "ἐν", "ἐς", "εἰς", "ἐκ", "ἐξ", "εἰ", "αἰ", "ὡς", "οὐ", "οὐκ", "οὐχ", "εἰν"}


# ---------------------------------------------------------------------------
# digamma list
# ---------------------------------------------------------------------------
@functools.lru_cache(None)
def load_digamma(path=str(HERE / "digamma.tsv")):
    entries = []
    with open(path, encoding="utf-8") as f:
        for row in csv.DictReader(f, delimiter="\t"):
            m = row["match"]
            excl = {x.strip() for x in (row.get("exclude") or "").split(",") if x.strip()}
            if m.startswith("form:"):
                forms = {G.form_key(x) for x in m[5:].split(",")}
                entries.append((row["id"], row["type"], "form", forms, excl, row.get("cap") or "any",
                                row.get("breathing") or "any"))
            elif m.startswith("red:"):
                entries.append((row["id"], row["type"], "red", re.compile(m[4:]), excl,
                                row.get("cap") or "any", row.get("breathing") or "any"))
            elif m.startswith("re:"):
                entries.append((row["id"], row["type"], "re", re.compile(m[3:]), excl,
                                row.get("cap") or "any", row.get("breathing") or "any"))
    return entries


def loose_diaer(w):
    w = G.norm_apostrophes(G.nfc(w))
    return G.strip_marks(w, keep_isub=True, keep_diaer=True).lower().replace("ς", "σ")


def digamma_info(word):
    """Return (id, type) if `word` (a token core) is in the digamma list."""
    if not RULES["digamma"]:
        return None
    return _digamma_info(word)


@functools.lru_cache(maxsize=200000)
def _digamma_info(word):
    fk = G.form_key(word)
    lo = G.loose(word)
    ld = loose_diaer(word)
    ls = letters_of(word)
    upper = bool(ls) and ls[0].upper
    first_v = next((l for l in ls if l.is_vowel), None)
    rough = first_v is not None and G.ROUGH in first_v.marks and ls[0].is_vowel
    for (eid, typ, kind, pat, excl, cap, breath) in load_digamma():
        if fk in excl:
            continue
        if cap == "lower" and upper:
            continue
        if cap == "upper" and not upper:
            continue
        if breath == "rough" and not rough:
            continue
        if breath == "smooth" and rough:
            continue
        if kind == "form":
            if fk in pat:
                return eid, typ
        elif kind == "re":
            if pat.match(lo):
                return eid, typ
        elif kind == "red":
            if pat.match(ld):
                return eid, typ
    return None


@functools.lru_cache(maxsize=200000)
def letters_of(word):
    w = word.rstrip(G.ELISION)
    return tuple(G.letters(w))


# ---------------------------------------------------------------------------
# nuclei
# ---------------------------------------------------------------------------
DIPHTHONGS = {"αι", "ει", "οι", "υι", "αυ", "ευ", "ου", "ηυ", "ωυ"}


class Nucleus:
    __slots__ = ("idx", "tok", "widx", "text", "cls", "diph", "first", "last",
                 "lets", "accent", "subscript")

    def __repr__(self):
        return f"N({self.text},{self.cls},w{self.tok})"


def word_nuclei(ls):
    """Return list of (start, end) letter index ranges of the nuclei of a word."""
    out = []
    i = 0
    n = len(ls)
    while i < n:
        l = ls[i]
        if l.is_vowel:
            if i + 1 < n:
                nx = ls[i + 1]
                pair = l.base + nx.base
                if (pair in DIPHTHONGS and nx.is_vowel and G.DIAER not in nx.marks
                        and l.accent is None and l.breathing is None and G.ISUB not in l.marks):
                    out.append((i, i + 2))
                    i += 2
                    continue
            out.append((i, i + 1))
        i += 1
    return out


def word_accent_rules(nucs):
    """Accent-based quantity constraints on dichrona.  `nucs` are Nucleus
    objects of one word (in order).  Returns dict nucleus_index -> 'L'/'S'."""
    fixed = {}
    acc = [k for k, n in enumerate(nucs) if n.accent is not None]
    if not acc:
        return fixed
    a = acc[0]  # lexical accent = first accent (a second one is enclitic-induced)
    from_end = len(nucs) - 1 - a
    last = nucs[-1]
    if nucs[a].accent == G.CIRC and from_end == 1 and last.cls == "D" and not last.diph:
        fixed[len(nucs) - 1] = "S"      # σωτῆρα rule: circumflex on penult -> ultima short
    if from_end == 2 and last.cls == "D" and not last.diph:
        fixed[len(nucs) - 1] = "S"      # antepenult accent -> ultima short
    return fixed


class Line:
    """Analysed verse: tokens, nuclei, clusters."""

    def __init__(self, text):
        self.text = G.nfc(text)
        self.tokens = G.tokenize(self.text)
        self.nuclei = []
        self.tok_nuclei = []     # per token: list of nucleus indices
        self.after = []          # per nucleus: cluster string after it ('|' = word boundary)
        self.digamma = []        # per token: (id, type) or None
        self.onset_vowel = []    # per token: begins with a vowel
        self.nonelidable = []
        tok_segs = []
        for t in self.tokens:
            ls = list(letters_of(t.core))
            ls = [l for l in ls if l.is_vowel or l.is_cons]
            nr = word_nuclei(ls)
            tok_segs.append((ls, nr))
            self.digamma.append(digamma_info(t.core))
            self.onset_vowel.append(bool(ls) and ls[0].is_vowel)
        self.tok_segs = tok_segs
        # build nuclei
        for ti, (ls, nr) in enumerate(tok_segs):
            idxs = []
            for k, (s, e) in enumerate(nr):
                n = Nucleus()
                n.idx = len(self.nuclei)
                n.tok = ti
                n.widx = k
                n.lets = ls[s:e]
                n.text = "".join(l.ch for l in n.lets)
                n.diph = e - s == 2
                n.subscript = any(G.ISUB in l.marks for l in n.lets)
                n.accent = next((l.accent for l in n.lets if l.accent), None)
                base = "".join(l.base for l in n.lets)
                if n.diph or n.subscript or base in ("η", "ω"):
                    n.cls = "L"
                elif base in ("ε", "ο"):
                    n.cls = "S"
                else:
                    n.cls = "L" if n.accent == G.CIRC else "D"
                n.first = k == 0
                n.last = k == len(nr) - 1
                self.nuclei.append(n)
                idxs.append(n.idx)
            self.tok_nuclei.append(idxs)
        # accent-based fixing of dichrona
        self.fixed = {}
        self.learned = {}
        self.force = {}
        self.analogy = {}
        for ti, idxs in enumerate(self.tok_nuclei):
            if not idxs:
                continue
            nucs = [self.nuclei[i] for i in idxs]
            for k, q in word_accent_rules(nucs).items():
                self.fixed[idxs[k]] = q
        # clusters after each nucleus
        N = len(self.nuclei)
        for i, n in enumerate(self.nuclei):
            ls, nr = tok_segs[n.tok]
            s, e = nr[n.widx]
            if not n.last:
                s2 = nr[n.widx + 1][0]
                self.after.append("".join(l.base for l in ls[e:s2]))
                continue
            parts = ["".join(l.base for l in ls[e:])]
            tj = n.tok + 1
            while tj < len(self.tokens):
                ls2, nr2 = tok_segs[tj]
                if nr2:
                    parts.append("".join(l.base for l in ls2[:nr2[0][0]]))
                    break
                parts.append("".join(l.base for l in ls2))
                tj += 1
            self.after.append("|".join(parts))

    def next_word_of(self, i):
        """Token index of nucleus i+1 if it is word-initial."""
        if i + 1 >= len(self.nuclei):
            return None
        nx = self.nuclei[i + 1]
        return nx.tok if nx.first else None


def ccount(cl):
    return sum(2 if c in G.DOUBLE else 1 for c in cl if c != "|")


def syl_options(line, span):
    """Quantity options for the syllable made of nuclei span=(i, j) inclusive.
    Returns a list of (q, licences); licences is a tuple of (name, token_index)."""
    i, j = span
    nucs = line.nuclei
    N = len(nucs)
    last_n = nucs[j]
    if j == N - 1:
        return [("X", ())]
    merged = i != j
    cls = "L" if merged else last_n.cls
    extra_variants = []
    weak = False   # quantity only predicted by analogy: no internal correption
    if not merged and cls == "D" and i in line.force:
        cls = line.force[i]
        weak = True   # a forced vowel quantity may not be undone by internal correption
    elif not merged and cls == "D":
        if i in line.learned:
            q = line.learned[i]
            cls = q
            extra_variants.append(("S" if q == "L" else "L", (("dichronon_contra", last_n.tok),)))
        elif i in line.fixed and RULES["accent_rules"]:
            q = line.fixed[i]
            cls = q
            if not RULES["accent_hard"]:
                extra_variants.append(("S" if q == "L" else "L", (("accent_contra", last_n.tok),)))
        elif i in line.analogy:
            q = line.analogy[i]
            cls = q
            weak = True
            extra_variants.append(("S" if q == "L" else "L", (("analogy_contra", last_n.tok),)))
    cl = line.after[j]
    final = last_n.last
    tok = last_n.tok
    elided = line.tokens[tok].elided
    nxt_tok = line.next_word_of(j)
    variants = [(cl, ())]
    if nxt_tok is not None and line.digamma[nxt_tok] and line.onset_vowel[nxt_tok]:
        typ = line.digamma[nxt_tok][1]
        if typ in ("w", "sw"):
            variants.append((cl + "ϝ", (("digamma", nxt_tok),)))
        if typ == "sw":
            variants.append((cl + "ϝϝ", (("digamma_double", nxt_tok),)))
    if nxt_tok is not None and line.digamma[nxt_tok] and line.digamma[nxt_tok][1] == "dw":
        variants.append((cl + "ϝ", (("digamma_double", nxt_tok),)))
    if (not final and last_n.widx == 0 and line.digamma[tok] and line.digamma[tok][1] == "dw_aug"
            and cl == "δ"):
        variants.append(("δϝ", (("digamma_internal", tok),)))
    opts = []
    for c2, extra in [(cls, ())] + extra_variants:
        for cluster, dlic in variants:
            for q, lic in _options_for_cluster(line, c2, merged, last_n, cluster, final, elided, tok, nxt_tok, j):
                if weak and any(nm == "internal_correption" for nm, _ in lic):
                    continue
                opts.append((q, tuple(lic) + tuple(dlic) + tuple(extra)))
    return opts


def _lic_cost(names, princeps):
    c = 0.0
    for nm, _ in names:
        c += LICENCES[nm][1 if princeps else 3]
    return c


def _lic_tier(names, princeps):
    t = 0
    for nm, _ in names:
        t = max(t, LICENCES[nm][0 if princeps else 2])
    return t


def _options_for_cluster(line, cls, merged, nuc, cluster, final, elided, tok, nxt_tok, j):
    out = []

    def add(q, lic):
        out.append((q, tuple(lic)))

    n = ccount(cluster)
    cons = cluster.replace("|", "").replace("ϝ", "")

    if n == 0:
        if not final:
            # internal hiatus
            if cls == "L":
                add("L", ())
                add("S", [("internal_correption", tok)])
            elif cls == "S":
                add("S", ())
                add("L", [("metrical_lengthening", tok)])
            else:
                add("L", ())
                add("S", ())
        else:
            hi = [] if elided else [("hiatus", tok)]
            if cls == "L":
                add("S", [("correption", tok)])
                add("L", [("hiatus_long", tok)])
            elif cls == "S":
                add("S", hi)
                add("L", [("lengthening_hiatus", tok)])
            else:
                add("S", hi)
                add("L", [("hiatus_long", tok)] if not elided else [])
        return out
    if n == 1:
        if cls == "L":
            add("L", ())
            return out
        if cls == "D":
            add("L", ())
            add("S", ())
            return out
        add("S", ())
        if final and cluster.startswith("|") and cons in ("λ", "μ", "ν", "ρ", "σ"):
            add("L", [("lengthening_liquid", nxt_tok if nxt_tok is not None else tok)])
        elif final and cluster.endswith("|") and not cluster.startswith("|"):
            add("L", [("lengthening_closed", tok)])
        elif not final and cons in ("λ", "μ", "ν", "ρ", "σ"):
            add("L", [("lengthening_liquid_internal", tok)])
        else:
            add("L", [("metrical_lengthening", tok)])
        return out
    # two or more consonants
    add("L", ())
    if cls == "L" or "ϝ" in cluster:
        return out
    # muta cum liquida?
    if len(cons) == 2 and cons[0] in G.STOPS and cons[1] in G.LIQUIDS:
        bpos = cluster.find("|")
        if bpos == -1:
            add("S", [("muta_cum_liquida", tok)])
        elif cluster.startswith("|") and cluster.count("|") == 1:
            add("S", [("muta_cum_liquida_initial", nxt_tok)])
        elif cluster.endswith("|") and cluster.count("|") == 1 and not final:
            pass
    if final and cluster.startswith("|") and cluster.count("|") == 1 and (
            cons in ("ζ", "ξ", "ψ") or (len(cons) == 2 and cons[0] == "σ" and cons[1] in G.STOPS | {"μ"})):
        add("S", [("no_position_initial_cluster", nxt_tok)])
    return out


# ---------------------------------------------------------------------------
# synizesis candidates
# ---------------------------------------------------------------------------
def synizesis_options(line, i):
    """Licences allowing nuclei i and i+1 to merge, or None."""
    nucs = line.nuclei
    if i + 1 >= len(nucs):
        return None
    a, b = nucs[i], nucs[i + 1]
    cl = line.after[i]
    if a.tok == b.tok:
        if cl != "":
            return None
        ab = a.lets[-1].base
        if a.diph:
            if a.text and "".join(l.base for l in a.lets) == "ει":
                return ("synizesis", a.tok)
            return None
        if ab == "ε":
            return ("synizesis", a.tok)
        if ab in "ιυ":
            return ("synizesis_i", a.tok)
        if ab == "ο" and "".join(l.base for l in b.lets)[0] in "οω":
            return ("synizesis", a.tok)
        return ("synizesis_rare", a.tok)
    # across words: a is last of its word, b first of next, nothing between
    if a.last and b.first and cl == "|" and not line.tokens[a.tok].elided:
        if G.form_key(line.tokens[a.tok].core) in SYNIZESIS_CROSS_FIRST:
            return ("synizesis_cross", a.tok)
        if a.cls == "L":
            return ("synizesis_cross_rare", a.tok)
    return None


# ---------------------------------------------------------------------------
# hexameter alignment
# ---------------------------------------------------------------------------
# state = (foot, slot); slot 0: longum; 1: first biceps element; 2: second short
END = (7, 0)


def label(foot, slot, q):
    if slot == 0:
        return f"{2 * foot - 1}"
    if foot == 6:
        return "12"
    if slot == 1 and q == "S":
        return f"{2 * foot - 1}.5"
    return f"{2 * foot}"


def transitions(state, q):
    """Yield (next_state, princeps?) for a syllable of quantity q in state."""
    f, s = state
    if f > 6:
        return
    if s == 0:
        if q == "L":
            yield (f, 1), True
    elif s == 1:
        if f == 6:
            if q == "X":
                yield END, False
        else:
            if q == "L":
                yield (f + 1, 0), False
            elif q == "S":
                yield (f, 2), False
    elif s == 2:
        if q == "S":
            yield (f + 1, 0), False


class Scansion:
    __slots__ = ("cost", "syls")   # syls: list of (span, q, state, lic)

    def __init__(self, cost, syls):
        self.cost = cost
        self.syls = syls


def solve(line, max_tier=MAX_TIER, max_solutions=64):
    """All scansions of `line` whose licences all have tier <= max_tier,
    cheapest first (one per distinct alignment)."""
    N = len(line.nuclei)
    if N < 12 or N > 26:
        return []
    opt_cache = {}
    disabled = RULES["disabled"]

    def options(span):
        """[(q, (cost_p, lic_p), (cost_b, lic_b))]: cheapest admissible option
        per quantity and per metrical place (princeps / biceps)."""
        if span not in opt_cache:
            best = {}
            for q, lic in syl_options(line, span):
                if disabled and any(nm in disabled for nm, _ in lic):
                    continue
                bp, bb = best.get(q, ((INF, ()), (INF, ())))
                if _lic_tier(lic, True) <= max_tier:
                    cp = _lic_cost(lic, True)
                    if cp < bp[0]:
                        bp = (cp, lic)
                if _lic_tier(lic, False) <= max_tier:
                    cb = _lic_cost(lic, False)
                    if cb < bb[0]:
                        bb = (cb, lic)
                best[q] = (bp, bb)
            opt_cache[span] = [(q, bp, bb) for q, (bp, bb) in best.items()]
        return opt_cache[span]

    @functools.lru_cache(None)
    def go(k, state):
        if k == N:
            return {(): (0.0, ())} if state == END else {}
        if state == END:
            return {}
        res = {}
        spans = [((k, k), ())]
        syn = synizesis_options(line, k)
        if syn is not None and syn[0] not in disabled:
            spans.append(((k, k + 1), (syn,)))
        for span, slic in spans:
            nk = span[1] + 1
            for q, bp, bb in options(span):
                for nstate, princeps in transitions(state, q):
                    c, lic = bp if princeps else bb
                    if c == INF:
                        continue
                    if slic:
                        if _lic_tier(slic, princeps) > max_tier:
                            continue
                        c += _lic_cost(slic, princeps)
                    sub = go(nk, nstate)
                    if not sub:
                        continue
                    for sig, (sc, path) in sub.items():
                        nsig = ((span, q),) + sig
                        tot = c + sc
                        if nsig not in res or res[nsig][0] > tot:
                            res[nsig] = (tot, ((span, q, state, tuple(lic) + tuple(slic)),) + path)
        return res

    sols = go(0, (1, 0))
    out = [Scansion(c, list(p)) for c, p in sols.values()]
    out.sort(key=lambda s: (round(s.cost, 6), pattern_of(s)))
    return out[:max_solutions]


def pattern_of(sc):
    feet = []
    cur = {}
    for span, q, (f, s), lic in sc.syls:
        cur.setdefault(f, []).append(q)
    for f in range(1, 6):
        feet.append("D" if len(cur.get(f, [])) == 3 else "S")
    return "".join(feet)


# ---------------------------------------------------------------------------
# analysis of a scansion
# ---------------------------------------------------------------------------
def appositive(tok):
    core = tok.core
    fk = G.form_key(core)
    if not G.has_accent(core):
        if fk in PROCLITIC_UNACCENTED:
            return "pre"
        if fk in PREPOSITIVE:
            return "pre"
        return "post"
    if fk in POSTPOSITIVE:
        return "post"
    if fk in PREPOSITIVE:
        return "pre"
    return None


def syllabify_display(line, merged_pairs):
    """Orthographic syllabification of each token, '.' between syllables.
    merged_pairs: set of nucleus indices i such that i and i+1 form one syllable."""
    out = []
    for ti, (ls, nr) in enumerate(line.tok_segs):
        if not nr:
            out.append("".join(l.ch for l in ls) + ("ʼ" if line.tokens[ti].elided else ""))
            continue
        cuts = set()
        base_idx = line.tok_nuclei[ti]
        for k in range(len(nr) - 1):
            e = nr[k][1]
            s2 = nr[k + 1][0]
            if base_idx[k] in merged_pairs:
                continue
            cons = [l.base for l in ls[e:s2]]
            if len(cons) <= 1:
                cuts.add(e if not cons else e)
            elif len(cons) == 2 and cons[0] in G.STOPS and cons[1] in G.LIQUIDS:
                cuts.add(e)
            else:
                cuts.add(e + 1)
            if len(cons) == 1:
                cuts.discard(e)
                cuts.add(e)
        text = ""
        for k, l in enumerate(ls):
            if k in cuts:
                text += "."
            text += l.ch
        if line.tokens[ti].elided:
            text += "ʼ"
        out.append(text)
    return out


def analyse(line, sc):
    """Return a dict describing scansion `sc` of `line`."""
    nucs = line.nuclei
    syl_of = {}
    positions = []
    for k, (span, q, state, lic) in enumerate(sc.syls):
        f, s = state
        lab = label(f, s, q)
        positions.append(lab)
        for i in range(span[0], span[1] + 1):
            syl_of[i] = k
    T = len(line.tokens)
    # per-token syllable ranges
    tok_first = [None] * T
    tok_last = [None] * T
    for ti, idxs in enumerate(line.tok_nuclei):
        if idxs:
            tok_first[ti] = syl_of[idxs[0]]
            tok_last[ti] = syl_of[idxs[-1]]
    # vowel-less tokens attach to the next syllable
    for ti in range(T):
        if tok_first[ti] is None:
            nxt = next((tok_first[tj] for tj in range(ti + 1, T) if tok_first[tj] is not None), len(sc.syls) - 1)
            tok_first[ti] = tok_last[ti] = nxt
    # orthographic word end after syllable k
    orth_end = set()
    for ti in range(T - 1):
        if not line.tok_nuclei[ti]:
            continue
        last_n = line.tok_nuclei[ti][-1]
        k = syl_of[last_n]
        span = sc.syls[k][0]
        if span[1] > last_n:  # merged with next word's vowel (cross-word synizesis)
            continue
        orth_end.add(k)
    # lexical word end: group appositives
    app = [appositive(t) for t in line.tokens]
    lex_end = set()
    for ti in range(T - 1):
        if app[ti] == "pre":
            continue
        # next token with a nucleus, skipping vowel-less postpositives
        tj = ti + 1
        if app[tj] == "post":
            continue
        # last nucleus of the group ending at ti
        tk = ti
        while tk >= 0 and not line.tok_nuclei[tk]:
            tk -= 1
        if tk < 0:
            continue
        last_n = line.tok_nuclei[tk][-1]
        k = syl_of[last_n]
        if sc.syls[k][0][1] > last_n:
            continue
        lex_end.add(k)
    pos_orth = sorted({positions[k] for k in orth_end}, key=float)
    pos_lex = sorted({positions[k] for k in lex_end}, key=float)
    pat = pattern_of(sc)
    final_q = nucs[sc.syls[-1][0][1]].cls
    caes = []
    lexs = set(pos_lex)
    if "3" in lexs:
        caes.append("trithemimeral")
    if "5" in lexs:
        caes.append("penthemimeral")
    if "5.5" in lexs:
        caes.append("trochaic")
    if "7" in lexs:
        caes.append("hephthemimeral")
    if "8" in lexs:
        bucolic = "D" if pat[3] == "D" else "S"
    else:
        bucolic = ""
    anomalies = []
    if not ({"5", "5.5", "7"} & lexs):
        anomalies.append("no_main_caesura")
    if "7.5" in lexs:
        anomalies.append("hermann_bridge")
    if "6" in lexs and not ({"5", "5.5"} & lexs):
        anomalies.append("diaeresis_after_3rd_foot")
    if bucolic == "S":
        anomalies.append("naeke_bridge")
    if pat[4] == "S":
        anomalies.append("spondeiazon")
    lic_list = []
    for k, (span, q, state, lic) in enumerate(sc.syls):
        for nm, ti in lic:
            if nm == "hiatus" and False:
                continue
            word = line.tokens[ti].core if ti is not None else ""
            lic_list.append((nm, positions[k], ti, word))
    # syllable display
    merged = {span[0] for span, q, state, lic in sc.syls if span[1] > span[0]}
    syl_text = syllabify_display(line, merged)
    meter_by_tok = []
    for ti in range(T):
        idxs = line.tok_nuclei[ti]
        if not idxs:
            meter_by_tok.append("0")
            continue
        ks = []
        for i in idxs:
            k = syl_of[i]
            if not ks or ks[-1] != k:
                ks.append(k)
        s = ""
        for k in ks:
            q = sc.syls[k][1]
            s += q if q != "X" else ("L" if final_q == "L" else "X")
        meter_by_tok.append(s)
    word_pos = [f"{positions[tok_first[ti]]}-{positions[tok_last[ti]]}" for ti in range(T)]
    quantities = "".join(q if q != "X" else "X" for _, q, _, _ in sc.syls)
    return {
        "pattern": pat + "S",
        "pattern5": pat,
        "quantities": quantities,
        "positions": positions,
        "syllables": syl_text,
        "word_meter": meter_by_tok,
        "word_positions": word_pos,
        "wordend_orth": pos_orth,
        "wordend_lex": pos_lex,
        "caesurae": caes,
        "bucolic": bucolic,
        "licences": lic_list,
        "anomalies": anomalies,
        "cost": round(sc.cost, 3),
    }


def signature(sc):
    return tuple((span, q) for span, q, _, _ in sc.syls)


ANALOGY_EXTRA = 0  # letters beyond the next vowel included in the key (chosen by
                   # leave-one-out evaluation in build_tables.py)


def analogy_key(word, vowel_no, extra=None):
    """Loose letters of `word` from its start through the first letter of the
    nucleus after nucleus number `vowel_no` (1-based), plus `extra` letters;
    None for the last nucleus."""
    extra = ANALOGY_EXTRA if extra is None else extra
    ls = [l for l in letters_of(word) if l.is_vowel or l.is_cons]
    nr = word_nuclei(ls)
    if vowel_no >= len(nr):
        return None
    end = nr[vowel_no][0] + 1 + extra
    return "".join(l.base for l in ls[:end])


def scan(text, max_solutions=64, learned=None, max_tier=MAX_TIER, analogy=None):
    """Scan a verse.  `learned` maps (form_key, nucleus_index_in_word) -> 'L'/'S'
    (dichrona fixed by unambiguous attestations; see build_tables.py).
    Tries tiers 0..max_tier and keeps the first tier with any scansion."""
    line = Line(text)
    if learned:
        for ti, idxs in enumerate(line.tok_nuclei):
            fk = G.form_key(line.tokens[ti].core)
            for k, i in enumerate(idxs):
                q = learned.get((fk, k + 1))
                if q and line.nuclei[i].cls == "D":
                    line.learned[i] = q
    if analogy:
        for ti, idxs in enumerate(line.tok_nuclei):
            for k, i in enumerate(idxs):
                if line.nuclei[i].cls != "D" or i in line.learned or k == len(idxs) - 1:
                    continue
                key = analogy_key(line.tokens[ti].core, k + 1)
                q = analogy.get(key) if key and len(key) >= ANALOGY_MIN_KEY else None
                if q:
                    line.analogy[i] = q
    sols, tier = [], None
    for t in range(0, max_tier + 1):
        sols = solve(line, max_tier=t, max_solutions=max_solutions)
        if sols:
            tier = t
            break
    if not sols:
        status = "fail"
    elif len(sols) == 1:
        status = "unique"
    else:
        status = "multiple"
    best_cost = sols[0].cost if sols else None
    n_best = sum(1 for s in sols if abs(s.cost - best_cost) < 1e-9) if sols else 0
    return {
        "text": line.text,
        "line": line,
        "status": status,
        "tier": tier,
        "n_solutions": len(sols),
        "n_best": n_best,
        "solutions": sols,
        "analyses": [analyse(line, s) for s in sols],
        "n_nuclei": len(line.nuclei),
    }


def fmt_lic(lics):
    return ";".join(f"{nm}@{pos}({w})" for nm, pos, ti, w in lics)


def describe(res, all_solutions=False):
    out = [res["text"], f"status: {res['status']}  tier: {res['tier']}  scansions: {res['n_solutions']}  tied-best: {res['n_best']}"]
    if res["status"] == "fail":
        line = res["line"]
        out.append("nuclei: " + " ".join(f"{n.text}[{n.cls}]" for n in line.nuclei))
        out.append("clusters: " + " ".join(repr(c) for c in line.after))
        return "\n".join(out)
    show = res["analyses"] if all_solutions else res["analyses"][:1]
    for a in show:
        out.append(f"pattern {a['pattern']}  cost {a['cost']}")
        out.append("  syllables: " + " ".join(a["syllables"]))
        out.append("  positions: " + " ".join(a["positions"]) + "   quantities: " + a["quantities"])
        out.append("  quantities: " + " ".join(a["word_meter"]))
        out.append("  word positions: " + " ".join(a["word_positions"]))
        out.append("  caesurae: " + ",".join(a["caesurae"]) + (f"  bucolic: {a['bucolic']}" if a["bucolic"] else ""))
        out.append("  licences: " + fmt_lic(a["licences"]))
        out.append("  anomalies: " + ",".join(a["anomalies"]))
    return "\n".join(out)


# ---------------------------------------------------------------------------
# corpus mode
# ---------------------------------------------------------------------------
COLUMNS = ["work", "book", "line", "status", "tier", "n_scansions", "n_best", "pattern", "alt_patterns",
           "quantities", "syllables", "word_meter", "word_positions", "wordend_orth", "wordend_lex",
           "caesurae", "bucolic", "licences", "features", "anomalies", "cost"]
FEATURES = {"spondeiazon", "naeke_bridge"}
QUANTITY_LICENCES = {"correption", "hiatus_long", "internal_correption", "lengthening_liquid",
                     "lengthening_closed", "lengthening_hiatus", "metrical_lengthening",
                     "lengthening_liquid_internal", "dichronon_contra"}


def dichronon_attestations(line, sc, tier):
    """Dichrona whose quantity this (unique) scansion fixes.  A vowel counts
    only if (a) its syllable is open or prevocalic so that the syllable
    quantity shows the vowel quantity, (b) no licence that changes quantity
    could apply in that context, and (c) forcing the opposite quantity leaves
    no scansion even when the tier-1 licences are allowed."""
    out = []
    nucs = line.nuclei
    for k, (span, q, state, lic) in enumerate(sc.syls):
        if span[0] != span[1] or q == "X":
            continue
        i = span[0]
        n = nucs[i]
        if n.cls != "D":
            continue
        names = {nm for nm, _ in lic}
        if names & (QUANTITY_LICENCES - {"dichronon_contra"}):
            continue
        cl = line.after[i]
        if "digamma" in names:
            cl += "ϝ"
        if "digamma_double" in names or "digamma_internal" in names:
            cl += "ϝϝ"
        nn = ccount(cl)
        cons = cl.replace("|", "").replace("ϝ", "")
        princeps = state[1] == 0
        final = n.last
        if q == "S":
            if nn == 0 and final:
                continue
            env = "prevocalic" if nn == 0 else ("mcl" if nn >= 2 else ("final" if final else "internal"))
        else:
            if nn >= 2:
                continue
            if nn == 0:
                if final:
                    continue
                env = "prevocalic"
            else:
                if final and princeps:
                    continue
                if final and cl.startswith("|") and cons in ("λ", "μ", "ν", "ρ", "σ"):
                    continue
                env = "final" if final else "internal"
        # (c) forcing the other quantity must leave no scansion, even with the
        # common (tier-1) licences
        line.force = {i: "S" if q == "L" else "L"}
        alt = solve(line, max_tier=max(tier, 1), max_solutions=2)
        line.force = {}
        if alt:
            continue
        out.append((G.form_key(line.tokens[n.tok].core), n.widx + 1, n.text, q, env,
                    "princeps" if princeps else "biceps"))
    return out


def corpus_record(args):
    """Scan one corpus line; return everything the tables need."""
    work, book, ln, text, learned, analogy = args
    rec = {"work": work, "book": book, "line": ln}
    try:
        res = scan(text, learned=learned, analogy=analogy)
    except Exception as e:  # pragma: no cover
        rec.update(status="error", row=[work, book, ln, "error"] + [""] * (len(COLUMNS) - 4))
        rec["error"] = repr(e)
        return rec
    rec["status"] = res["status"]
    rec["tier"] = res["tier"]
    rec["n"] = res["n_solutions"]
    if res["status"] == "fail":
        rec["row"] = [work, book, ln, "fail", "", 0, 0] + [""] * (len(COLUMNS) - 8) + [""]
        rec["row"][COLUMNS.index("anomalies")] = "fail"
        return rec
    a = res["analyses"][0]
    sc = res["solutions"][0]
    line = res["line"]
    alts = []
    for b in res["analyses"][1:]:
        if b["pattern"] not in alts and b["pattern"] != a["pattern"]:
            alts.append(b["pattern"])
    feats = [x for x in a["anomalies"] if x in FEATURES]
    anomalies = [x for x in a["anomalies"] if x not in FEATURES]
    if res["n_best"] > 1:
        anomalies.append("tied_best")
    if res["tier"] == 2:
        anomalies.append("rare_licence")
    rec["row"] = [work, book, ln, res["status"], res["tier"], res["n_solutions"], res["n_best"], a["pattern"],
                  ",".join(alts), a["quantities"], " ".join(a["syllables"]), " ".join(a["word_meter"]),
                  " ".join(a["word_positions"]), ",".join(a["wordend_orth"]), ",".join(a["wordend_lex"]),
                  ",".join(a["caesurae"]), a["bucolic"], fmt_lic(a["licences"]), ",".join(feats),
                  ",".join(anomalies), a["cost"]]
    rec["positions"] = a["positions"]
    rec["wordend_orth"] = a["wordend_orth"]
    rec["wordend_lex"] = a["wordend_lex"]
    rec["pattern"] = a["pattern"]
    rec["licences"] = [(nm, G.form_key(w) if w else "", pos) for nm, pos, ti, w in a["licences"]]
    rec["word_positions"] = a["word_positions"]
    if res["status"] == "unique":
        rec["attest"] = dichronon_attestations(line, sc, res["tier"])
    return rec


def read_lines(path=HERE / "lines.tsv"):
    rows = []
    with open(path, encoding="utf-8") as f:
        r = csv.reader(f, delimiter="\t", quoting=csv.QUOTE_NONE, escapechar="\\")
        header = next(r)
        for row in r:
            d = dict(zip(header, row))
            rows.append(d)
    return rows


def scan_corpus_records(learned=None, analogy=None, workers=None):
    from multiprocessing import Pool
    rows = read_lines()
    args = [(r["work"], r["book"], r["line"], r["text"], learned, analogy) for r in rows]
    workers = workers or os.cpu_count() or 1
    with Pool(workers) as p:
        return p.map(corpus_record, args, chunksize=100)


def write_scansion(records, out_path=HERE / "scansion.tsv"):
    with open(out_path, "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f, delimiter="\t", lineterminator="\n", quoting=csv.QUOTE_NONE, escapechar="\\")
        w.writerow(COLUMNS)
        for r in records:
            w.writerow(r["row"])


LEARN_MIN_SHARE = 0.9   # a dichronon is "learned" if >= 90% of its fixed attestations agree
LEARN_MIN_N_CONFLICT = 5  # ... and, when there is any disagreement, at least 5 attestations


def load_learned(path=HERE / "dichrona.tsv"):
    """(form, vowel_no) -> quantity for dichrona fixed by unambiguous
    attestations: all attestations agree, or (with >= 5 attestations) at
    least 90% agree."""
    learned = {}
    if not pathlib.Path(path).exists():
        return learned
    with open(path, encoding="utf-8") as f:
        for row in csv.DictReader(f, delimiter="\t", quoting=csv.QUOTE_NONE):
            nl, ns = int(row["n_long"]), int(row["n_short"])
            n = nl + ns
            if n == 0:
                continue
            if row["quantity"] in ("L", "S"):
                learned[(row["form"], int(row["vowel_no"]))] = row["quantity"]
            elif n >= LEARN_MIN_N_CONFLICT and max(nl, ns) / n >= LEARN_MIN_SHARE:
                learned[(row["form"], int(row["vowel_no"]))] = "L" if nl > ns else "S"
    return learned


ANALOGY_MIN_FORMS = 3
ANALOGY_MIN_SHARE = 0.9
ANALOGY_MIN_KEY = 3   # keys shorter than 3 letters (e.g. word-initial ἀε-) are not used


def load_analogy(path=HERE / "dichrona_analogy.tsv"):
    out = {}
    if not pathlib.Path(path).exists():
        return out
    with open(path, encoding="utf-8") as f:
        for row in csv.DictReader(f, delimiter="\t", quoting=csv.QUOTE_NONE):
            if row["quantity"] in ("L", "S"):
                out[row["key"]] = row["quantity"]
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("verse", nargs="*")
    ap.add_argument("--corpus", action="store_true", help="scan homer/lines.tsv (runs homer/build_tables.py)")
    ap.add_argument("--no-learned", action="store_true", help="do not use homer/dichrona.tsv")
    ap.add_argument("--all-solutions", action="store_true")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--workers", type=int, default=None)
    args = ap.parse_args()
    if args.corpus:
        import subprocess
        sys.exit(subprocess.call([sys.executable, str(HERE / "build_tables.py")]))
    verses = [" ".join(args.verse)] if args.verse else [l.strip() for l in sys.stdin if l.strip()]
    learned = None if args.no_learned else load_learned()
    analogy = None if args.no_learned else load_analogy()
    for v in verses:
        res = scan(v, learned=learned, analogy=analogy)
        if args.json:
            print(json.dumps({k: res[k] for k in ("text", "status", "n_solutions", "n_best")} |
                             {"analyses": res["analyses"] if args.all_solutions else res["analyses"][:1]},
                             ensure_ascii=False))
        else:
            print(describe(res, args.all_solutions))
            print()


if __name__ == "__main__":
    main()
