#!/usr/bin/env python3
"""Concordance of the Iliad and Odyssey (homer/lines.tsv).

Queries
  --exact  STRING   exact substring of the NFC text (apostrophe variants unified)
  --loose  STRING   accent-, breathing-, diaeresis-, case- and punctuation-
                    insensitive; final sigma = σ; iota subscript ignored
  --regex  PATTERN  Python regular expression on the NFC text
                    (add --on loose to run it on the loose, punctuation-free text)
  --ngram  "w1 w2"  sequence of whole words compared in loose form; '*' matches
                    any one word
Options
  --word            (exact/loose) match whole words only
  --work Il|Od      restrict to one poem;  --limit N;  --count
  --format text|tsv|json
Every hit gives the citation (Il. 1.1), the line, the words matched and the
metrical positions (homer/scansion.tsv, half-foot numbering 1, 1.5, 2 ... 12)
of the first and last syllable of the words containing the match.

  python homer/concordance.py --loose "ποδας ωκυς"
  python homer/concordance.py --ngram "πόδας ὠκὺς Ἀχιλλεύς"
  python homer/concordance.py --build-ngrams      # writes homer/ngrams.tsv

As a module:
  from concordance import Concordance
  c = Concordance(); hits = c.ngram("γλαυκῶπις Ἀθήνη")
"""
import argparse
import collections
import csv
import json
import pathlib
import re
import sys
import unicodedata

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import greek as G  # noqa: E402


def _loose_char(ch):
    if ch in "’'᾽᾿":
        return G.ELISION
    d = unicodedata.normalize("NFD", ch)
    base = "".join(c for c in d if not unicodedata.combining(c))
    if len(base) != 1:
        return ch
    base = base.lower()
    return "σ" if base == "ς" else base


def loose_query(s):
    return " ".join(G.loose(w) for w in s.split())


class Line:
    __slots__ = ("work", "book", "line", "text", "tokens", "loose_tokens", "loose_text", "loose_map",
                 "word_pos", "bracketed")


class Hit:
    __slots__ = ("work", "book", "line", "text", "tok_start", "tok_end", "pos_start", "pos_end", "match")

    def __init__(self, ln, ts, te, match):
        self.work, self.book, self.line, self.text = ln.work, ln.book, ln.line, ln.text
        self.tok_start, self.tok_end = ts, te
        wp = ln.word_pos
        self.pos_start = wp[ts].split("-")[0] if wp and ts < len(wp) else ""
        self.pos_end = wp[te].split("-")[1] if wp and te < len(wp) else ""
        self.match = match

    @property
    def citation(self):
        return f"{self.work}. {self.book}.{self.line}"

    def as_dict(self):
        return {"citation": self.citation, "text": self.text, "match": self.match,
                "words": [self.tok_start + 1, self.tok_end + 1],
                "metrical_start": self.pos_start, "metrical_end": self.pos_end}


class Concordance:
    def __init__(self, lines_path=HERE / "lines.tsv", scansion_path=HERE / "scansion.tsv"):
        pos = {}
        if pathlib.Path(scansion_path).exists():
            with open(scansion_path, encoding="utf-8") as f:
                for r in csv.DictReader(f, delimiter="\t", quoting=csv.QUOTE_NONE, escapechar="\\"):
                    if r["word_positions"]:
                        pos[(r["work"], r["book"], r["line"])] = r["word_positions"].split()
        self.lines = []
        with open(lines_path, encoding="utf-8") as f:
            for r in csv.DictReader(f, delimiter="\t", quoting=csv.QUOTE_NONE, escapechar="\\"):
                ln = Line()
                ln.work, ln.book, ln.line = r["work"], r["book"], r["line"]
                ln.text = G.norm_apostrophes(r["text"])
                ln.bracketed = r.get("bracketed") == "1"
                ln.tokens = G.tokenize(ln.text)
                ln.loose_tokens = [G.loose(t.core) for t in ln.tokens]
                # loose text: tokens joined by one space, with a map to char offsets
                parts, cmap = [], []
                for ti, t in enumerate(ln.tokens):
                    if ti:
                        parts.append(" ")
                        cmap.append(t.start)
                    for k, ch in enumerate(t.core):
                        parts.append(_loose_char(ch))
                        cmap.append(t.start + k)
                ln.loose_text = "".join(parts)
                ln.loose_map = cmap
                wp = pos.get((ln.work, ln.book, ln.line))
                ln.word_pos = wp if wp and len(wp) == len(ln.tokens) else None
                self.lines.append(ln)

    # -- helpers ----------------------------------------------------------
    @staticmethod
    def _tok_span(ln, a, b):
        """Token indices overlapping char span [a, b) of ln.text."""
        ts = [i for i, t in enumerate(ln.tokens) if t.end > a and t.start < b]
        if not ts:
            return None
        return ts[0], ts[-1]

    def _filter(self, work):
        return [l for l in self.lines if work is None or l.work == work]

    # -- queries ----------------------------------------------------------
    def exact(self, q, word=False, work=None):
        q = G.norm_apostrophes(G.nfc(q))
        pat = re.compile((r"(?<![\wʼ])" if word else "") + re.escape(q) + (r"(?![\w])" if word else ""))
        return self._regex_text(pat, work)

    def loose(self, q, word=False, work=None):
        q = loose_query(q)
        pat = re.compile((r"(?<![\wʼ])" if word else "") + re.escape(q) + (r"(?![\w])" if word else ""))
        return self._regex_loose(pat, work)

    def regex(self, p, on="text", work=None):
        pat = re.compile(p)
        return self._regex_text(pat, work) if on == "text" else self._regex_loose(pat, work)

    def _regex_text(self, pat, work):
        hits = []
        for ln in self._filter(work):
            for m in pat.finditer(ln.text):
                sp = self._tok_span(ln, m.start(), max(m.end(), m.start() + 1))
                if sp:
                    hits.append(Hit(ln, sp[0], sp[1], m.group()))
        return hits

    def _regex_loose(self, pat, work):
        hits = []
        for ln in self._filter(work):
            for m in pat.finditer(ln.loose_text):
                if m.end() <= m.start():
                    continue
                a = ln.loose_map[m.start()]
                b = ln.loose_map[m.end() - 1] + 1
                sp = self._tok_span(ln, a, b)
                if sp:
                    hits.append(Hit(ln, sp[0], sp[1], ln.text[a:b]))
        return hits

    def ngram(self, words, work=None):
        if isinstance(words, str):
            words = words.split()
        q = [None if w == "*" else G.loose(w) for w in words]
        n = len(q)
        hits = []
        for ln in self._filter(work):
            lt = ln.loose_tokens
            for i in range(len(lt) - n + 1):
                if all(x is None or x == lt[i + k] for k, x in enumerate(q)):
                    a, b = ln.tokens[i].start, ln.tokens[i + n - 1].end
                    hits.append(Hit(ln, i, i + n - 1, ln.text[a:b]))
        return hits


# ---------------------------------------------------------------------------
# repeated n-gram index
# ---------------------------------------------------------------------------
def build_ngrams(conc, nmin=2, nmax=7, max_cit=20, out=HERE / "ngrams.tsv"):
    """Every word n-gram (2..7 words, within a line, loose form) occurring at
    least twice.  For each: count, number of distinct lines, the most frequent
    attested spelling, its most frequent metrical localisation and share, and
    up to 20 citations with positions."""
    occ = collections.defaultdict(list)
    for li, ln in enumerate(conc.lines):
        lt = ln.loose_tokens
        for n in range(nmin, nmax + 1):
            for i in range(len(lt) - n + 1):
                occ[(n, " ".join(lt[i:i + n]))].append((li, i))
    rows = []
    for (n, key), lst in occ.items():
        if len(lst) < 2:
            continue
        forms = collections.Counter()
        locs = collections.Counter()
        cits = []
        lines_seen = set()
        for li, i in lst:
            ln = conc.lines[li]
            lines_seen.add(li)
            forms[" ".join(t.core for t in ln.tokens[i:i + n])] += 1
            if ln.word_pos:
                loc = f"{ln.word_pos[i].split('-')[0]}-{ln.word_pos[i + n - 1].split('-')[1]}"
            else:
                loc = "?"
            locs[loc] += 1
            if len(cits) < max_cit:
                cits.append(f"{ln.work}. {ln.book}.{ln.line}@{loc}")
        loc, lc = locs.most_common(1)[0]
        rows.append((n, key, forms.most_common(1)[0][0], len(lst), len(lines_seen), loc,
                     round(lc / len(lst), 3), "; ".join(cits)))
    rows.sort(key=lambda r: (r[0], -r[3], r[1]))
    with open(out, "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f, delimiter="\t", lineterminator="\n", quoting=csv.QUOTE_NONE, escapechar="\\")
        w.writerow(["n", "ngram_loose", "form", "count", "lines", "main_position", "main_position_share",
                    "citations"])
        for r in rows:
            w.writerow(r)
    return collections.Counter(r[0] for r in rows)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--exact")
    g.add_argument("--loose")
    g.add_argument("--regex")
    g.add_argument("--ngram")
    g.add_argument("--build-ngrams", action="store_true")
    ap.add_argument("--on", choices=["text", "loose"], default="text")
    ap.add_argument("--word", action="store_true")
    ap.add_argument("--work", choices=["Il", "Od"])
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--count", action="store_true")
    ap.add_argument("--format", choices=["text", "tsv", "json"], default="text")
    a = ap.parse_args()
    c = Concordance()
    if a.build_ngrams:
        stats = build_ngrams(c)
        print("repeated n-grams written to homer/ngrams.tsv:", dict(sorted(stats.items())))
        return
    if a.exact is not None:
        hits = c.exact(a.exact, word=a.word, work=a.work)
    elif a.loose is not None:
        hits = c.loose(a.loose, word=a.word, work=a.work)
    elif a.regex is not None:
        hits = c.regex(a.regex, on=a.on, work=a.work)
    else:
        hits = c.ngram(a.ngram, work=a.work)
    if a.count:
        print(len(hits))
        return
    total = len(hits)
    if a.limit:
        hits = hits[:a.limit]
    if a.format == "json":
        print(json.dumps({"total": total, "hits": [h.as_dict() for h in hits]}, ensure_ascii=False, indent=1))
    elif a.format == "tsv":
        print("citation\tmetrical_start\tmetrical_end\tmatch\ttext")
        for h in hits:
            print(f"{h.citation}\t{h.pos_start}\t{h.pos_end}\t{h.match}\t{h.text}")
    else:
        for h in hits:
            print(f"{h.citation:<12} [{h.pos_start}-{h.pos_end}]  {h.text}    <{h.match}>")
        print(f"-- {total} hit(s)" + (f", {len(hits)} shown" if a.limit and total > a.limit else ""))


if __name__ == "__main__":
    main()
