#!/usr/bin/env python3
"""Appendices A–C of paper/paper.md, generated from the frozen poem records.

Reads composition/final/poem.txt and poem.jsonl (64 verses; the `scansion` block of each record is
the output of homer/check_line.py: foot pattern, caesurae, bucolic diaeresis, licences) and, when it
exists with 64 numbered lines, composition/final/translation.md. Writes
paper/figures/tables/appendix_a_poem.md, appendix_b_translation.md and appendix_c_scansion.md.
Nothing in the appendices is typed by hand.

    source .venv/bin/activate && python -I paper/make_appendices.py
"""
import json
import re
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
POEM_TXT = ROOT / "composition" / "final" / "poem.txt"
POEM_JSONL = ROOT / "composition" / "final" / "poem.jsonl"
TRANSLATION = ROOT / "composition" / "final" / "translation.md"
OUT = ROOT / "paper" / "figures" / "tables"

CAESURA = {"trithemimeral": "3", "penthemimeral": "5", "trochaic": "5½", "hephthemimeral": "7"}
PLACEHOLDER = "[translation to be inserted by the orchestrator from composition/final/translation.md]"


def nfc(s):
    return unicodedata.normalize("NFC", s)


def main():
    verses = [nfc(l.rstrip("\n")) for l in POEM_TXT.read_text(encoding="utf-8").splitlines() if l.strip()]
    records = [json.loads(l) for l in POEM_JSONL.read_text(encoding="utf-8").splitlines() if l.strip()]
    assert len(verses) == 64 and len(records) == 64, (len(verses), len(records))
    for v, r in zip(verses, records):
        assert nfc(r["text"]) == v, r["n"]

    # Appendix A: the poem, numbered
    a = ["| | |", "|---|---|"]
    for i, v in enumerate(verses, 1):
        a.append(f"| {i} | {v} |")
    (OUT / "appendix_a_poem.md").write_text("\n".join(a) + "\n", encoding="utf-8")

    # Appendix B: the translation, line for line, if complete
    b_lines = []
    if TRANSLATION.exists():
        for line in TRANSLATION.read_text(encoding="utf-8").splitlines():
            m = re.match(r"^(\d+)\.\s+(.*\S)\s*$", line)
            if m:
                b_lines.append((int(m.group(1)), m.group(2)))
    complete = [n for n, _ in b_lines] == list(range(1, 65))
    if complete:
        b = ["| | |", "|---|---|"] + [f"| {n} | {t} |" for n, t in b_lines]
        status = "complete"
    else:
        b = [PLACEHOLDER]
        status = f"placeholder ({len(b_lines)} numbered lines found)"
    (OUT / "appendix_b_translation.md").write_text("\n".join(b) + "\n", encoding="utf-8")

    # Appendix C: scansion
    c = ["| line | feet 1–6 | caesurae | bucolic diaeresis | licences (position: word) | enjambment |",
         "|---|---|---|---|---|---|"]
    for r in records:
        sc = r["scansion"]
        caes = ", ".join(CAESURA.get(x, x) for x in sc.get("caesurae", []) or []) or "–"
        buc = {"D": "yes (4th foot dactyl)", "S": "yes (4th foot spondee)", "": "–"}[sc.get("bucolic_diaeresis", "") or ""]
        lic = []
        for item in (sc.get("licences") or "").split(";"):
            if not item:
                continue
            m = re.match(r"^([a-z_]+)@([\d.]+)\((.*)\)$", item)
            lic.append(f"{m.group(1).replace('_', ' ')} at {m.group(2)}: {nfc(m.group(3))}" if m else item)
        c.append(f"| {r['n']} | {sc['pattern']} | {caes} | {buc} | {'; '.join(lic) or '–'} | {r.get('enjambment') or '–'} |")
    (OUT / "appendix_c_scansion.md").write_text("\n".join(c) + "\n", encoding="utf-8")
    print(f"wrote appendix_a_poem.md (64 verses), appendix_b_translation.md ({status}), appendix_c_scansion.md (64 rows)")


if __name__ == "__main__":
    main()
