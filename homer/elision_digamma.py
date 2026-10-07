#!/usr/bin/env python3
"""Elision before digamma-initial words: attestation table and lookup.

    python homer/elision_digamma.py          # writes homer/elision_digamma.tsv
                                             # and the generated README block

A word whose final short vowel is elided before a word that began with ϝ
(homer/digamma.tsv) neglects the digamma; Homer keeps the vowel (hiatus) in
many such pairs and elides in others (ἄρα οἱ, never ἄρʼ οἱ).  This module
counts, for every pair (word, next word) in homer/lines.tsv where the next
word begins with a vowel and had a digamma, how often Homer elides the word
(n_elided) and how often he keeps its final short vowel (n_unelided).
check_line.py flags a pair in a new verse that Homer never elides.

Definitions (used for the corpus and for new verses alike):
  * tokens and adjacency: the concordance's tokenisation (concordance.py,
    greek.tokenize); a pair is two consecutive tokens of one line,
    whatever punctuation stands between them.
  * digamma-initial next word: scan.digamma_info() gives a type `w` or `sw`
    entry of homer/digamma.tsv (types `dw`, `dw_aug` begin with δ or with
    the augment and are not relevant to elision), or the word is one of the
    third-person pronoun forms PRON3; and the word begins with a vowel.
    The elided forms in NOT_DIGAMMA are excluded: digamma.tsv matches them,
    but they are the elided preposition/adverb ἐπί, ἔτι (ἔπος, ἔτος end
    in -ος and cannot be elided to ἐπʼ, ἔτʼ).  The entries in
    EXCLUDED_ENTRIES are excluded too (see there).
  * next-word key: greek.form_key (accents kept, grave written acute), so
    that οἱ (enclitic dative or plural article) and οἵ (relative) differ.
  * elided-word key: the loose form of the elided word (accents, breathings,
    case ignored), ending in ʼ; a final τ κ π is written θ χ φ before a
    rough breathing (τε οἱ ~ θʼ οἱ), as the text itself does.
  * unelided word: a word of two or more letters whose last nucleus is a
    single α ε ι ο with no circumflex and no iota subscript (a vowel Homer
    can elide); its key is the loose form with that vowel replaced by ʼ
    (ἄρα -> αρʼ, τε -> θʼ before a rough breathing).  One-vowel words (ὅ, ἅ)
    are not elided and are left out.
"""
import collections
import csv
import json
import pathlib
import random
import re
import sys
import time
import unicodedata

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import greek as G  # noqa: E402
import scan as S  # noqa: E402

TABLE = HERE / "elision_digamma.tsv"
README = HERE / "README.md"
MAX_CIT = 5
SEED = 20261007

# third-person pronoun forms (Monro §391; initial σϝ), accented and enclitic
PRON3 = {G.form_key(w) for w in ("οἱ", "οἷ", "ἑ", "ἕ", "ἕʼ", "ἑο", "ἕο", "ἑοῖ", "ἑθεν", "ἕθεν", "ἑθέν",
                                  "εὑ", "εὗ", "ἑέ")}
# elided forms matched by digamma.tsv that are other words (loose form -> word)
NOT_DIGAMMA = {"επʼ": "ἐπί", "ετʼ": "ἔτι"}
# digamma.tsv entries not used for this check, with the reason
EXCLUDED_ENTRIES = {
    "hos_as": "postpositive ὥς 'as' (Monro §375(1): lengthening before it) is written like ὥς/ὣς "
              "'thus' and ὥς τε 'as', which had no digamma and before which Homer elides freely",
}
ELIDABLE = set("αειο")
ASPIRATE = {"τ": "θ", "κ": "χ", "π": "φ"}
DEASPIRATE = {v: k for k, v in ASPIRATE.items()}
COLUMNS = ["word", "next_word", "digamma_id", "n_elided", "n_unelided", "elided_spellings",
           "unelided_spellings", "citations_elided", "citations_unelided"]


# ---------------------------------------------------------------------------
# keys
# ---------------------------------------------------------------------------
def _lead_vowels(core):
    ls = [l for l in S.letters_of(core) if l.is_vowel or l.is_cons]
    out = []
    for l in ls:
        if not l.is_vowel:
            break
        out.append(l)
        if len(out) == 2:
            break
    return out


def rough_onset(core):
    """True if the word begins with a vowel carrying (or whose diphthong
    carries) a rough breathing."""
    return any(G.ROUGH in l.marks for l in _lead_vowels(core))


def digamma_next(core):
    """(id, type) if `core` is a vowel-initial word with a digamma, else None."""
    if not _lead_vowels(core):
        return None
    lo = G.loose(core)
    if lo in NOT_DIGAMMA:
        return None
    di = S.digamma_info(core)
    if di and di[1] in ("w", "sw") and di[0] not in EXCLUDED_ENTRIES:
        return di
    if G.form_key(core) in PRON3:
        return ("pron3", "sw")
    return None


def _aspirate(stem, next_core):
    if stem and stem[-1] in ASPIRATE and rough_onset(next_core):
        return stem[:-1] + ASPIRATE[stem[-1]]
    return stem


def elided_key(core, next_core):
    """Key of an elided word (core ends in ʼ) before `next_core`."""
    lo = G.loose(core)
    return _aspirate(lo[:-1], next_core) + G.ELISION


def unelided_key(core, next_core):
    """Key the elided form of an unelided word would have, or None if the word
    does not end in an elidable short vowel."""
    if core.endswith(G.ELISION):
        return None
    ls = [l for l in S.letters_of(core) if l.is_vowel or l.is_cons]
    if not ls or not ls[-1].is_vowel:
        return None
    nr = S.word_nuclei(ls)
    s, e = nr[-1]
    last = ls[-1]
    if e - s != 1 or e != len(ls) or last.base not in ELIDABLE or G.CIRC in last.marks or G.ISUB in last.marks:
        return None
    lo = G.loose(core)
    if len(lo) < 2 or lo[-1] != last.base:
        return None
    return _aspirate(lo[:-1], next_core) + G.ELISION


# ---------------------------------------------------------------------------
# regular expressions that reproduce the counts with concordance.py --regex
# ---------------------------------------------------------------------------
_BASES = set("αβγδεζηθικλμνξοπρστυφχψω")


def _letter_classes():
    groups = collections.defaultdict(set)
    for cp in list(range(0x370, 0x400)) + list(range(0x1F00, 0x2000)):
        ch = chr(cp)
        if not unicodedata.category(ch).startswith("L"):
            continue
        d = unicodedata.normalize("NFD", ch)
        base = d[0].lower()
        base = "σ" if base == "ς" else base
        if base in _BASES:
            groups[base].add((ch, frozenset(d[1:])))
    return groups


_CLASSES = _letter_classes()


def _cls(base, final_vowel=False):
    chars = sorted(ch for ch, marks in _CLASSES[base]
                   if not (final_vowel and (G.CIRC in marks or G.ISUB in marks)))
    return "[" + "".join(chars) + "]"


def _exact_word_re(form):
    """Regex for the spellings that have this form_key: acute or grave, an
    enclitic-induced second acute (οἶκόνδε), either case of the first letter."""
    out = []
    seen_accent = False
    for k, ch in enumerate(form):
        var = {ch}
        d = unicodedata.normalize("NFD", ch)
        if G.ACUTE in d:
            var.add(unicodedata.normalize("NFC", d.replace(G.ACUTE, G.GRAVE)))
        elif seen_accent and d[0] in G.VOWELS and not any(m in d for m in G.ACCENTS):
            var.add(unicodedata.normalize("NFC", d + G.ACUTE))
        seen_accent = seen_accent or any(m in d for m in G.ACCENTS)
        if k == 0:
            var |= {v.upper() for v in var}
        out.append(re.escape(ch) if len(var) == 1 else "[" + "".join(sorted(var)) + "]")
    return "".join(out)


SEP = r"[^\w]*\s[^\w]*"


def pair_regex(key, next_form, elided=True):
    """Regex on the NFC text (concordance.py --regex) matching the pair: the
    first word in any accentuation and case, elided (key + ʼ) or with an
    elidable final short vowel; the next word in its form_key spelling (acute
    or grave, either case of the first letter)."""
    stem = key[:-1]
    parts = [_cls(c) if c in _BASES else re.escape(c) for c in stem]
    if stem and stem[-1] in DEASPIRATE and rough_onset(next_form):
        # θʼ before a rough breathing may stand for τ (τε οἱ ~ θʼ οἱ) or for θ (ἔνθα)
        parts[-1] = "(?:" + parts[-1] + "|" + _cls(DEASPIRATE[stem[-1]]) + ")"
    first = "".join(parts)
    if elided:
        first += G.ELISION
    else:
        first += "(?:" + "|".join(_cls(v, final_vowel=True) for v in sorted(ELIDABLE)) + ")"
    return r"(?<!\w)" + first + SEP + _exact_word_re(next_form) + r"(?!\w)"


# ---------------------------------------------------------------------------
# table
# ---------------------------------------------------------------------------
def load_table(path=TABLE):
    out = {}
    with open(path, encoding="utf-8") as f:
        for r in csv.DictReader(f, delimiter="\t", quoting=csv.QUOTE_NONE, escapechar="\\"):
            r["n_elided"] = int(r["n_elided"])
            r["n_unelided"] = int(r["n_unelided"])
            out[(r["word"], r["next_word"])] = r
    return out


def lemma_of():
    out = {"pron3": "ἕο, εὗ, οἱ, ἕ, ἕθεν (§391)"}
    with open(HERE / "digamma.tsv", encoding="utf-8") as f:
        for r in csv.DictReader(f, delimiter="\t"):
            out[r["id"]] = f"{r['lemma']} ({r['monro']})"
    return out


class Index:
    """Lookup used by check_line.py."""

    def __init__(self, path=TABLE):
        self.table = load_table(path)
        self.by_word_group = collections.Counter()
        self.by_next = collections.Counter()
        for (w, nx), r in self.table.items():
            self.by_word_group[(w, r["digamma_id"])] += r["n_elided"]
            self.by_next[nx] += r["n_elided"]
        self.lemma = lemma_of()

    def check_pair(self, core, next_core):
        """None if `next_core` is not a digamma-initial word; otherwise a dict
        with the pair's counts (n_elided == 0: Homer never elides it)."""
        di = digamma_next(next_core)
        if di is None:
            return None
        key, nf = elided_key(core, next_core), G.form_key(next_core)
        r = self.table.get((key, nf))
        return {"word": core, "next_word": next_core, "key": key, "next_form": nf, "digamma_id": di[0],
                "lemma": self.lemma.get(di[0], di[0]),
                "n_elided": r["n_elided"] if r else 0, "n_unelided": r["n_unelided"] if r else 0,
                "elided_spellings": r["elided_spellings"] if r else "",
                "unelided_spellings": r["unelided_spellings"] if r else "",
                "citations_elided": r["citations_elided"].split("; ") if r and r["citations_elided"] else [],
                "citations_unelided": r["citations_unelided"].split("; ") if r and r["citations_unelided"] else [],
                "n_elided_word_before_entry": self.by_word_group[(key, di[0])],
                "n_any_elided_before_next": self.by_next[nf],
                "query_elided": pair_regex(key, nf, elided=True),
                "query_unelided": pair_regex(key, nf, elided=False)}


def collect(conc):
    """Every pair (elided or with an elidable final vowel) before a
    digamma-initial word, from the concordance's lines."""
    rows = {}
    inst = []  # (cit, key, next_form, elided)
    for ln in conc.lines:
        cit = f"{ln.work}. {ln.book}.{ln.line}"
        toks = ln.tokens
        for i in range(len(toks) - 1):
            a, b = toks[i].core, toks[i + 1].core
            di = digamma_next(b)
            if di is None:
                continue
            el = a.endswith(G.ELISION)
            key = elided_key(a, b) if el else unelided_key(a, b)
            if key is None:
                continue
            nf = G.form_key(b)
            r = rows.setdefault((key, nf), {"id": di[0], "n_el": 0, "n_un": 0, "sp_el": collections.Counter(),
                                            "sp_un": collections.Counter(), "c_el": [], "c_un": []})
            if el:
                r["n_el"] += 1
                r["sp_el"][a] += 1
                if len(r["c_el"]) < MAX_CIT:
                    r["c_el"].append(cit)
            else:
                r["n_un"] += 1
                r["sp_un"][a] += 1
                if len(r["c_un"]) < MAX_CIT:
                    r["c_un"].append(cit)
            inst.append((cit, key, nf, el))
    return rows, inst


def _sp(c):
    return ",".join(w for w, _ in c.most_common())


def write_table(rows, path=TABLE):
    with open(path, "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f, delimiter="\t", lineterminator="\n", quoting=csv.QUOTE_NONE, escapechar="\\")
        w.writerow(COLUMNS)
        for (key, nf), r in sorted(rows.items()):
            w.writerow([key, nf, r["id"], r["n_el"], r["n_un"], _sp(r["sp_el"]), _sp(r["sp_un"]),
                        "; ".join(r["c_el"]), "; ".join(r["c_un"])])


def self_test(conc, rows, n_sample=300):
    """Check that pair_regex() reproduces the counts through Concordance.regex:
    every pair Homer elides, and a seeded sample of the unelided pairs."""
    el = [(k, r) for k, r in sorted(rows.items()) if r["n_el"]]
    un = [(k, r) for k, r in sorted(rows.items()) if r["n_un"]]
    rnd = random.Random(SEED)
    un = rnd.sample(un, min(n_sample, len(un)))
    bad = []
    for (key, nf), r in el:
        n = len(conc.regex(pair_regex(key, nf, True)))
        if n != r["n_el"]:
            bad.append((key, nf, "elided", r["n_el"], n))
    for (key, nf), r in un:
        n = len(conc.regex(pair_regex(key, nf, False)))
        if n != r["n_un"]:
            bad.append((key, nf, "unelided", r["n_un"], n))
    return len(el), len(un), bad


def fill_block(txt, name, lines):
    pat = re.compile(rf"<!-- BEGIN GENERATED: {re.escape(name)} -->.*?<!-- END GENERATED: {re.escape(name)} -->",
                     re.S)
    block = "\n".join([f"<!-- BEGIN GENERATED: {name} -->"] + lines + [f"<!-- END GENERATED: {name} -->"])
    return pat.sub(lambda m: block, txt)


def summary_block(rows, inst, test):
    n_el = sum(1 for x in inst if x[3])
    n_un = len(inst) - n_el
    lines_el = {x[0] for x in inst if x[3]}
    # leave-one-line-out: an elided instance whose pair occurs elided in no other line
    lines_of = collections.defaultdict(set)
    for cit, key, nf, el in inst:
        if el:
            lines_of[(key, nf)].add(cit)
    loo = [x for x in inst if x[3] and lines_of[(x[1], x[2])] == {x[0]}]
    loo_lines = {x[0] for x in loo}
    lem = lemma_of()
    by_id = collections.defaultdict(lambda: [0, 0])
    for cit, key, nf, el in inst:
        by_id[rows[(key, nf)]["id"]][0 if el else 1] += 1
    n_te, n_tu, bad = test
    out = [
        f"Pairs before a digamma-initial word: {len(rows)} (word, next word) pairs; "
        f"{sum(1 for r in rows.values() if r['n_el'])} of them elided at least once, "
        f"{sum(1 for r in rows.values() if not r['n_el'])} only with the vowel kept.",
        f"Instances: {n_el} elisions (in {len(lines_el)} lines) and {n_un} final short vowels kept "
        f"(hiatus or position) before such a word.",
        f"Leave-one-line-out: {len(loo)} of the {n_el} elisions ({100 * len(loo) / n_el:.1f}%, "
        f"in {len(loo_lines)} lines) are of a pair elided in no other line; check_line would flag them "
        f"if they were new verses ({sum(1 for x in loo if rows[(x[1], x[2])]['n_un'])} of these pairs occur "
        f"elsewhere with the vowel kept, {sum(1 for x in loo if not rows[(x[1], x[2])]['n_un'])} occur nowhere "
        f"else).",
        f"Regex self-test (concordance.py --regex with the patterns check_line prints): "
        f"{n_te - sum(1 for b in bad if b[2] == 'elided')}/{n_te} elided pairs and "
        f"{n_tu - sum(1 for b in bad if b[2] == 'unelided')}/{n_tu} sampled unelided pairs "
        f"(seed {SEED}) reproduce the table's counts.",
        "",
        "| digamma entry | elided | vowel kept | elided share |",
        "|---|---|---|---|",
    ]
    for i, (e, u) in sorted(by_id.items(), key=lambda x: (-(x[1][0] + x[1][1]), x[0])):
        out.append(f"| `{i}` {lem.get(i, i)} | {e} | {u} | {100 * e / (e + u):.1f}% |")
    return out, bad


def main():
    from concordance import Concordance
    t0 = time.time()
    conc = Concordance(scansion_path=HERE / "_no_scansion_needed")
    rows, inst = collect(conc)
    write_table(rows)
    test = self_test(conc, rows)
    block, bad = summary_block(rows, inst, test)
    txt = README.read_text(encoding="utf-8")
    new = fill_block(txt, "elision_digamma", block)
    if new != txt:
        README.write_text(new, encoding="utf-8")
    print(f"wrote {TABLE.relative_to(HERE.parent)}: {len(rows)} pairs ({time.time() - t0:.0f} s)")
    print("\n".join(block))
    for b in bad:
        print("SELF-TEST MISMATCH", b, file=sys.stderr)
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
