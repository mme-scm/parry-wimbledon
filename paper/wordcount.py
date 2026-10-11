#!/usr/bin/env python3
"""Word counts of paper/paper.md: main text against appendices.

Main text = sections 1-9 and "Data and code" (everything before the "## References" heading).
Two counts are given for it: "prose" (HTML comments, markdown tables, fenced and indented quotation
blocks, image lines and headings removed) and "all" (every word, tables and quotations included).
The reference list (from "## References" to the first "## Appendix") and the appendices are
counted whole.
With --update the counts are written into the HTML comment on the second line of the file
(the line starting "<!-- word counts"), which this script owns.

    source .venv/bin/activate && python -I paper/wordcount.py [--update]
"""
import re
import sys
import unicodedata
from pathlib import Path

PAPER = Path(__file__).resolve().parent / "paper.md"
MARK = "<!-- word counts"


def words(text):
    return len(re.findall(r"\S+", text))


def strip_comments(text):
    return re.sub(r"<!--.*?-->", " ", text, flags=re.S)


def prose_only(text):
    text = strip_comments(text)
    out, fenced = [], False
    for line in text.splitlines():
        if line.strip().startswith("```"):
            fenced = not fenced
            continue
        if fenced:
            continue
        s = line.strip()
        if not s:
            continue
        if s.startswith("|") or s.startswith("![") or s.startswith("#"):
            continue
        if line.startswith("    "):  # indented quotation block (Greek, Sanskrit, Old English, Latin)
            continue
        out.append(line)
    return "\n".join(out)


def main():
    text = PAPER.read_text(encoding="utf-8")
    nfc = unicodedata.normalize("NFC", text) == text
    r = re.search(r"^## References", text, flags=re.M)
    a = re.search(r"^## Appendix", text, flags=re.M)
    main_part = text[: r.start()] if r else text
    ref_part = text[r.start(): a.start()] if (r and a) else ""
    app_part = text[a.start():] if a else ""
    counts = {
        "main_prose": words(prose_only(main_part)),
        "main_all": words(strip_comments(main_part)),
        "references_all": words(strip_comments(ref_part)),
        "appendices_all": words(strip_comments(app_part)),
    }
    line = (f"{MARK} (paper/wordcount.py): main text (sections 1-9 and Data and code) {counts['main_prose']} words of prose, "
            f"{counts['main_all']} with tables, captions and quoted passages; references {counts['references_all']} words; "
            f"appendices A-C {counts['appendices_all']} words; Unicode NFC: {'yes' if nfc else 'NO'} -->")
    print(line)
    if "--update" in sys.argv:
        lines = text.split("\n")
        idx = next((i for i, l in enumerate(lines[:5]) if l.startswith(MARK)), None)
        if idx is None:
            lines.insert(1, line)
        else:
            lines[idx] = line
        PAPER.write_text("\n".join(lines), encoding="utf-8")
        print("updated", PAPER)


if __name__ == "__main__":
    main()
