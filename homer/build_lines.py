#!/usr/bin/env python3
"""Parse the Perseus TEI XML into homer/lines.tsv.

Columns: work (Il|Od), book (int), line (the TEI @n, kept as a string so that
sub-numbered lines such as '12a' survive), text (Unicode NFC, exactly the
text content of the <l> element with whitespace collapsed; never edited),
bracketed (1 if the TEI wraps the line in <del>, i.e. the editor brackets it).

Rows are in document order (the edition transposes a few lines, e.g. Od. 3.305
precedes 3.304; that order is kept).  A per-book line count is written to
homer/line_counts.tsv.
"""
import collections
import csv
import json
import pathlib
import re
import sys
import unicodedata

from lxml import etree

ROOT = pathlib.Path(__file__).resolve().parent.parent
TEI = "{http://www.tei-c.org/ns/1.0}"


def parse(path, work):
    tree = etree.parse(str(path))
    body = tree.find(f".//{TEI}body")
    rows = []
    notes = []
    for div in body.iter(f"{TEI}div"):
        if (div.get("subtype") or "").lower() != "book":
            continue
        book = int(div.get("n"))
        for el in div.iter(f"{TEI}l", f"{TEI}note"):
            if el.tag == f"{TEI}note":
                notes.append((work, book, " ".join("".join(el.itertext()).split())))
                continue
            n = el.get("n")
            text = " ".join("".join(el.itertext()).split())
            text = unicodedata.normalize("NFC", text)
            bracketed = int(el.find(f"{TEI}del") is not None)
            rows.append((work, book, n, text, bracketed))
    return rows, notes


def main():
    src = json.loads((ROOT / "homer" / "source.json").read_text())
    all_rows, all_notes = [], []
    for work in ("Il", "Od"):
        path = ROOT / src["files"][work]["local"]
        rows, notes = parse(path, work)
        all_rows += rows
        all_notes += notes
    out = ROOT / "homer" / "lines.tsv"
    with out.open("w", encoding="utf-8", newline="") as f:
        w = csv.writer(f, delimiter="\t", lineterminator="\n", quoting=csv.QUOTE_NONE, escapechar="\\")
        w.writerow(["work", "book", "line", "text", "bracketed"])
        for r in all_rows:
            assert "\t" not in r[3]
            w.writerow(r)
    counts = collections.Counter((r[0], r[1]) for r in all_rows)
    with (ROOT / "homer" / "line_counts.tsv").open("w", encoding="utf-8") as f:
        f.write("work\tbook\tlines\tfirst\tlast\tmissing_numbers\tsubnumbered\n")
        for (work, book), c in sorted(counts.items()):
            ns = [r[2] for r in all_rows if r[0] == work and r[1] == book]
            ints = sorted(int(re.match(r"\d+", n).group()) for n in ns)
            missing = sorted(set(range(1, ints[-1] + 1)) - set(ints))
            sub = [n for n in ns if not n.isdigit()]
            f.write(f"{work}\t{book}\t{c}\t{ints[0]}\t{ints[-1]}\t{','.join(map(str, missing))}\t{','.join(sub)}\n")
        for work in ("Il", "Od"):
            f.write(f"{work}\tALL\t{sum(v for (w_, b), v in counts.items() if w_ == work)}\t\t\t\t\n")
    for n in all_notes:
        print("TEI note:", *n)
    print({w: sum(v for (w_, b), v in counts.items() if w_ == w) for w in ("Il", "Od")},
          "bracketed:", sum(r[4] for r in all_rows), file=sys.stderr)


if __name__ == "__main__":
    main()
