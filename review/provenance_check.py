#!/usr/bin/env python3
"""Machine evidence for the provenance review of a composition draft.

    source .venv/bin/activate
    python -I review/provenance_check.py composition/drafts/v1.jsonl review/provenance_v1_evidence.json

For every record of the draft:
  * scans the verse with homer/scan.py (CLI, --json) and takes the word positions;
  * for every `sources` entry:
      - re-runs the recorded concordance query (same flags as homer/concordance.py's CLI,
        through the same Concordance methods) and records total and hit citations;
      - extracts the Homeric string H the entry claims (text minus parenthetical comments,
        left side of an arrow; for COINAGE entries the query string = the Homeric model);
        fragments separated by "..." or "/" are checked separately;
      - runs `ngram` on H (accent-insensitive whole words, as --ngram) and records every
        Homeric position of H;
      - parses the cited lines and checks that each contains H (a fragment for multi-line
        citations) and appears among the recorded query's hits;
      - locates H in the verse (loose whole-word sequence) and gives its position in the poem,
        or, if H is not there verbatim, the words of H that are/aren't in the verse;
  * every 2- and 3-word window (and every longer window up to the whole line) of the verse is
    run through `ngram`; attested windows are listed with counts, Homeric positions and whether
    any sources entry of the record covers them (claimed) or not (unclaimed);
  * Greek phrase + citation pairs quoted in `modifications[].homeric_parallel` are checked the same way.

Nothing is judged here: review/provenance_v1.md gives the judgments, citing this file.
"""
import json
import re
import subprocess
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "homer"))
import greek as G  # noqa: E402
from concordance import Concordance  # noqa: E402

C = Concordance()
LINE_BY_CIT = {f"{l.work}. {l.book}.{l.line}": l for l in C.lines}


# ------------------------------------------------------------------ helpers
def loose_words(s):
    return [G.loose(t.core) for t in G.tokenize(G.nfc(s))]


def run_query(q):
    """Parse a recorded CLI query string ('--ngram "..."', '--loose "..." --word') and run it."""
    m = re.match(r'\s*--(ngram|loose|exact|regex)\s+"(.*?)"\s*(.*)$', q)
    if not m:
        return None, None
    kind, s, rest = m.groups()
    word = "--word" in rest
    on = "loose" if "--on loose" in rest else "text"
    if kind == "ngram":
        hits = C.ngram(s)
    elif kind == "loose":
        hits = C.loose(s, word=word)
    elif kind == "exact":
        hits = C.exact(s, word=word)
    else:
        hits = C.regex(s, on=on)
    return (kind, s, word), hits


def hits_summary(hits):
    pos = Counter(f"{h.pos_start}-{h.pos_end}" for h in hits)
    return {"total": len(hits), "positions": dict(pos.most_common()),
            "citations": [f"{h.citation}@{h.pos_start}-{h.pos_end}" for h in hits]}


POSPAT = re.compile(r"\b\d+(?:\.5)?-\d+(?:\.5)?\b")


def parse_citations(s):
    """Line citations in a free-text citation field. Parenthetical comments are ignored except
    lists introduced by a count ('(21x: 2.567, 5.114 ...)'); 'Il. 3.373-374' is a range."""
    out = []

    def scan(txt, work):
        for m in re.finditer(r"\b(Il|Od)\.\s*|(\d+)\.(\d+)(?:-(\d+)(?![\.\d]))?", txt):
            if m.group(1):
                work = m.group(1)
                continue
            if work is None:
                continue
            b, l1, l2 = m.group(2), int(m.group(3)), m.group(4)
            if l2 and int(l2) > l1 and int(l2) - l1 < 20:
                out.extend(f"{work}. {b}.{x}" for x in range(l1, int(l2) + 1))
            else:
                out.append(f"{work}. {b}.{l1}")
        return work

    work = None
    pos = 0
    for m in re.finditer(r"\(([^)]*)\)", s):
        work = scan(s[pos:m.start()], work)
        inner = m.group(1)
        mm = re.match(r"\s*\d+x\s*:(.*)", inner)
        if mm:
            work = scan(mm.group(1), work)
        pos = m.end()
    scan(s[pos:], work)
    seen, res = set(), []
    for c in out:
        if c not in seen:
            seen.add(c)
            res.append(c)
    return res


def homeric_string(src):
    if src.get("status") == "COINAGE":
        m = re.match(r'\s*--\w+\s+"(.*?)"', src.get("query", ""))
        return [m.group(1)] if m else []
    t = src["text"]
    t = re.sub(r"\([^)]*\)", "", t)
    t = t.split("→")[0]
    frags = re.split(r"\s*(?:\.\.\.|…|/)\s*", t)
    out = []
    for f in frags:
        f = f.strip(" ,;·.")
        if f and loose_words(f):
            out.append(f)
    return out


def find_seq(words, seq):
    n = len(seq)
    return [i for i in range(len(words) - n + 1) if words[i:i + n] == seq]


def poem_span(wp, i, j):
    return f"{wp[i].split('-')[0]}-{wp[j].split('-')[1]}"


def scan_verse(text):
    out = subprocess.run([sys.executable, str(ROOT / "homer" / "scan.py"), text, "--json"],
                         capture_output=True, text=True, check=True)
    d = json.loads(out.stdout)
    a = d["analyses"][0] if d.get("analyses") else None
    return {"status": d.get("status"), "pattern": a and a["pattern"],
            "word_positions": a and a["word_positions"]}


def ngram_hits_for(words_loose):
    return C.ngram(words_loose)


def check_string_in_line(frag_loose, cit):
    ln = LINE_BY_CIT.get(cit)
    if ln is None:
        return {"exists": False}
    idx = find_seq(ln.loose_tokens, frag_loose)
    if not idx:
        return {"exists": True, "contains": False, "text": ln.text}
    i = idx[0]
    j = i + len(frag_loose) - 1
    p = None
    if ln.word_pos:
        p = f"{ln.word_pos[i].split('-')[0]}-{ln.word_pos[j].split('-')[1]}"
    return {"exists": True, "contains": True, "position": p, "text": ln.text}


GREEK_CHUNK = re.compile(r"([Ͱ-Ͽἀ-῿ʼ᾽'’ ]{3,}?)\s*[\(\[]?\s*((?:Il|Od)\.\s*\d+\.\d+)")


def check_parallels(mods):
    res = []
    for m in mods or []:
        txt = m.get("homeric_parallel", "")
        for mm in GREEK_CHUNK.finditer(txt):
            g = mm.group(1).strip(" ,;·.'")
            words = loose_words(g)
            if len(words) < 1:
                continue
            cit = re.sub(r"\s+", " ", mm.group(2)).replace(". ", ". ")
            cit = re.sub(r"(Il|Od)\.\s*", r"\1. ", cit)
            # try the longest suffix of the chunk that the cited line contains
            best = None
            for k in range(len(words)):
                r = check_string_in_line(words[k:], cit)
                if r.get("contains"):
                    best = {"phrase": " ".join(words[k:]), **r}
                    break
            res.append({"kind": m.get("kind"), "quoted": g, "citation": cit,
                        "verified": bool(best), "match": best})
    return res


# ------------------------------------------------------------------ main
def main(jsonl, out_path):
    recs = [json.loads(l) for l in open(jsonl, encoding="utf-8") if l.strip()]
    out = []
    for r in recs:
        text = r["text"]
        sc = scan_verse(text)
        wp = sc["word_positions"]
        toks = G.tokenize(G.nfc(text))
        words = [G.loose(t.core) for t in toks]
        assert wp is None or len(wp) == len(words), (r["n"], wp, words)
        rec = {"n": r["n"], "text": text, "scan": sc, "words": words, "sources": []}
        claimed_seqs = []
        for s in r.get("sources", []):
            e = {"text": s.get("text"), "citation": s.get("citation"), "status": s.get("status"),
                 "claimed_count": s.get("count"), "claimed_position": s.get("position"),
                 "query": s.get("query")}
            qp, qh = run_query(s.get("query", ""))
            e["query_total"] = None if qh is None else len(qh)
            qcits = set() if qh is None else {h.citation for h in qh}
            frags = homeric_string(s)
            e["H"] = frags
            cits = parse_citations(s.get("citation", ""))
            e["cited_lines"] = cits
            fr_res = []
            for f in frags:
                fl = loose_words(f)
                claimed_seqs.append(fl)
                hh = C.ngram(fl)
                hs = hits_summary(hh)
                occ = find_seq(words, fl)
                poem_pos = [poem_span(wp, i, i + len(fl) - 1) for i in occ] if wp else []
                present = [w for w in fl if w in words]
                fr_res.append({"H": f, "H_loose": " ".join(fl), "homer_total": hs["total"],
                               "homer_positions": hs["positions"],
                               "homer_citations_first40": hs["citations"][:40],
                               "in_poem_verbatim": bool(occ), "poem_positions": poem_pos,
                               "words_in_verse": present,
                               "words_not_in_verse": [w for w in fl if w not in words],
                               "position_attested": any(p in hs["positions"] for p in poem_pos)})
            e["fragments"] = fr_res
            cl = []
            for c in cits:
                per = []
                for f in frags:
                    per.append(check_string_in_line(loose_words(f), c))
                any_contains = any(x.get("contains") for x in per)
                cl.append({"citation": c, "exists": all(x.get("exists") for x in per) if per else c in LINE_BY_CIT,
                           "contains_H": [x.get("contains") for x in per],
                           "contains_any_fragment": any_contains,
                           "H_positions": [x.get("position") for x in per],
                           "in_query_hits": c in qcits,
                           "line": LINE_BY_CIT[c].text if c in LINE_BY_CIT else None})
            e["cited_check"] = cl
            rec["sources"].append(e)
        rec["parallels"] = check_parallels(r.get("modifications"))
        # windows
        wins = []
        L = len(words)
        for n in range(2, L + 1):
            for i in range(L - n + 1):
                seq = words[i:i + n]
                hh = C.ngram(seq)
                if not hh:
                    continue
                hs = hits_summary(hh)
                pp = poem_span(wp, i, i + n - 1) if wp else None
                claimed = any(find_seq(cs, seq) for cs in claimed_seqs)
                wins.append({"n": n, "i": i, "ngram": " ".join(t.core for t in toks[i:i + n]),
                             "count": hs["total"], "poem_position": pp,
                             "homer_positions": hs["positions"],
                             "position_attested": pp in hs["positions"],
                             "claimed": claimed, "examples": hs["citations"][:6]})
        rec["windows"] = wins
        out.append(rec)
        print(f"line {r['n']:>2}: {len(rec['sources'])} sources, {len(wins)} attested windows", file=sys.stderr)
    # cross-check: every distinct recorded query rerun with the CLI itself (--count), 4 at a time
    import shlex
    from concurrent.futures import ThreadPoolExecutor
    qs = sorted({s["query"] for r in recs for s in r.get("sources", []) if s.get("query")})

    def cli(q):
        args = [sys.executable, str(ROOT / "homer" / "concordance.py")] + shlex.split(q) + ["--count"]
        return q, int(subprocess.run(args, capture_output=True, text=True, check=True).stdout.strip())
    with ThreadPoolExecutor(4) as ex:
        cli_counts = dict(ex.map(cli, qs))
    mod_counts = {}
    for r in out:
        for s in r["sources"]:
            mod_counts[s["query"]] = s["query_total"]
    mism = {q: (cli_counts[q], mod_counts.get(q)) for q in qs if cli_counts[q] != mod_counts.get(q)}
    print(f"CLI cross-check: {len(qs)} distinct queries, {len(mism)} mismatches", file=sys.stderr)
    for r in out:
        r["cli_crosscheck"] = {"distinct_queries": len(qs), "mismatches": mism} if r is out[0] else None
    Path(out_path).write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
