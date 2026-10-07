#!/usr/bin/env python3
"""Supplementary concordance evidence for the provenance review of composition/drafts/v2.

    source .venv/bin/activate
    python -I review/provenance_v2_extra.py composition/drafts/v2.jsonl review/provenance_v2_evidence.json \
        review/provenance_v2_extra.json

Checks that review/provenance_check.py does not make (all through homer/concordance.py's Concordance class,
the same code as its CLI):
  1. forms of the poem with 0 Homeric hits (loose, whole word) and where each record marks them;
  2. the coined name stems (loose substring) have 0 hits;
  3. the analogical model of the patronymic Ζοκοβείδης: -είδ- with the diphthong ει (NFC regex, which keeps
     the diaeresis that the loose form drops) against -εΐδ-, with the metrical positions of every hit;
     the Ionic-η model (Ἀθήνη);
  4. name slots: for every coined name in the verse, the Homeric model word in the cited model line, its
     position there (homer/scansion.tsv), the coined name's position in the verse (homer/scan.py), and the
     number of Homeric occurrences of the model word at that position; with the neighbouring words, since
     some slots depend on a vowel-final word before or a vowel-initial word after;
  5. counts asserted in the records' notes for the name slots, recomputed;
  6. the `position` field of every source entry compared with the position of its string in the verse
     (entries whose string is in the verse word for word).
"""
import json
import re
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "homer"))
sys.path.insert(0, str(ROOT / "review"))
import greek as G  # noqa: E402
import provenance_check as P  # noqa: E402  (P.C = the Concordance)

C = P.C
LINE = P.LINE_BY_CIT


def L(s):
    return [G.loose(t.core) for t in G.tokenize(G.nfc(s))]


def posc(hits):
    return dict(Counter(f"{h.pos_start}-{h.pos_end}" for h in hits).most_common())


# (verse, coined form in the verse, Homeric model word, model citation, what the slot depends on)
SLOTS = [
    (4, "Φεδερεύς", "Ὀδυσεύς", "Il. 10.340", ""),
    (4, "Ζοκοβείδης", "Γανυμήδης", "Il. 20.232", "after τε καὶ ἀντίθεος"),
    (4, "Ζοκοβείδης", "Θρασυμήδης", "Od. 3.414", "after τε καὶ ἀντίθεος"),
    (4, "Ζοκοβείδης", "Κλυτόνηος", "Od. 8.119", "after τε καὶ ἀντίθεος"),
    (5, "Ἑλβέτιος", "Πηλεΐδης", "Il. 20.164", ""),
    (10, "Σέρβος", "Ἕκτωρ", "Il. 8.216", ""),
    (12, "Ἑλβέτιος", "Πάτροκλος", "Il. 16.284", ""),
    (12, "Ἑλβέτιος", "Πηλεΐδης", "Il. 20.164", ""),
    (14, "Φεδερῆρος", "Διομήδης", "Il. 2.563", ""),
    (15, "Σέρβος", "Τεῦκρος", "Il. 8.273", "before a vowel-initial word"),
    (19, "Ἑλβέτιος", "Δαρδανίδης", "Il. 3.303", ""),
    (20, "Φεδερῆρος", "Διομήδης", "Il. 2.563", ""),
    (23, "Ζοκοβεύς", "Ὀδυσεύς", "Il. 10.340", ""),
    (23, "Ζοκοβεύς", "Ἀχιλεύς", "Il. 20.273", ""),
    (24, "Ἑλβέτιος", "Δαρδανίδης", "Il. 3.303", ""),
    (25, "Φεδερεύς", "Ἀχιλεύς", "Il. 20.273", ""),
    (27, "Ῥογῆρος", "Ὀδυσσεύς", "Il. 2.272", "after a vowel-final word"),
    (27, "Ῥογῆρος", "Μελανθώ", "Od. 19.65", "after a vowel-final word"),
    (29, "Σέρβος", "Ἕκτωρ", "Il. 8.216", ""),
    (29, "Σέρβος", "Ἕκτωρ", "Il. 17.304", "name + δʼ αὖτʼ at 1-3"),
    (29, "Φεδερῆρον", "Μενέλαον", "Il. 4.220", ""),
    (30, "Φεδερῆρος", "Διομήδης", "Il. 2.563", ""),
    (32, "Φεδερεύς", "Ἀχιλεύς", "Il. 20.273", ""),
    (33, "Ῥογῆρος", "Ὀδυσσεύς", "Il. 2.272", "after a vowel-final word"),
    (33, "Ῥογῆρος", "Μελανθώ", "Od. 19.65", "after a vowel-final word"),
    (34, "Φεδερῆρος", "Διομήδης", "Il. 8.91", ""),
    (36, "Ζοκοβείδης", "Διομήδης", "Il. 4.401", "after κρατερός"),
    (38, "Σέρβος", "Ἕκτωρ", "Il. 8.216", ""),
    (38, "Σέρβος", "Τρῶες", "Il. 8.55", "before δʼ αὖθʼ ἑτέρωθεν"),
    (43, "Σέρβον", "Τεῦκρος", "Il. 12.350", "before a vowel-initial word"),
    (44, "Ζοκοβεύς", "Ὀδυσεύς", "Il. 10.340", ""),
    (44, "Ζοκοβεύς", "Ἀχιλεύς", "Il. 20.273", ""),
    (51, "Ἑλβετίου", "Δαρδανίδης", "Il. 3.303", ""),
    (51, "Ζοκοβῆος", "Ὀδυσῆος", "Od. 20.369", "after ἀντιθέου"),
    (52, "Ἑλβετίου", "Ἀτρεΐδης", "Il. 14.29", ""),
    (53, "Ζοκοβείδης", "Διομήδης", "Il. 4.401", "after κρατερός"),
    (54, "Ἑλβέτιος", "Δαρδανίδης", "Il. 3.303", ""),
    (55, "Νοβήκος", "Μελανθώ", "Od. 19.65", "after a vowel-final word"),
    (56, "Ἑλβέτιος", "Ἀντίνοος", "Od. 1.383", "after αὖτʼ"),
    (56, "Ἑλβέτιος", "Δαρδανίδης", "Il. 3.303", ""),
    (56, "Ζοκοβείδης", "Διομήδης", "Il. 2.563", "bare name at 9.5-12"),
    (57, "Ἑλβέτιος", "Σαρπηδών", "Il. 16.466", ""),
    (57, "Ἑλβέτιος", "Πηλεΐδης", "Il. 20.164", ""),
    (58, "Σέρβος", "Ἕκτωρ", "Il. 8.216", ""),
    (58, "Σέρβος", "Ἕκτωρ", "Il. 17.304", "name + δʼ αὖτʼ at 1-3"),
]

COINED_STEMS = ["φεδερ", "ρογηρ", "ελβετ", "σερβ", "ζοκοβ", "νοβηκ", "νοβακ"]


def word_at(ln_tokens, wp, i):
    return {"word": ln_tokens[i], "position": wp[i] if wp else None}


def main(jsonl, evid, out_path):
    recs = [json.loads(l) for l in open(jsonl, encoding="utf-8") if l.strip()]
    ev = {r["n"]: r for r in json.load(open(evid, encoding="utf-8"))}
    res = {}

    # 1. forms with 0 Homeric hits
    vocab = Counter(w for ln in C.lines for w in ln.loose_tokens)
    zero = []
    for r in recs:
        marks = " ".join([c.get("form", "") for c in r.get("coinages") or []])
        coin_src = " ".join(s["text"] for s in r.get("sources", []) if s.get("status") == "COINAGE")
        mod_src = " ".join(s["text"] for s in r.get("sources", []) if s.get("status") == "ATTESTED-MODIFIED")
        for t in G.tokenize(G.nfc(r["text"])):
            w = G.loose(t.core)
            if vocab[w] == 0:
                zero.append({"n": r["n"], "form": t.core, "loose": w,
                             "in_coinages": w in L(marks), "in_coinage_entry": w in L(coin_src),
                             "named_in_modified_entry": w in L(mod_src)})
    res["forms_with_0_homeric_hits"] = zero

    # 2. coined stems
    res["coined_stems_substring_hits"] = {s: len(C.loose(s)) for s in COINED_STEMS}

    # 3. patronymic model
    def rx(p):
        hs = C.regex(p)
        return {"total": len(hs), "positions": posc(hs),
                "hits": [f"{h.citation}@{h.pos_start}-{h.pos_end}: {h.match} | {h.text}" for h in hs[:12]]}
    res["patronymic"] = {
        "Πηλείδ (diphthong ει)": rx(r"Πηλείδ\w*"),
        "Πηλεΐδ (ε-ϊ)": rx(r"Πηλεΐδ\w*"),
        "Πηλεΐδης (nom.)": rx(r"Πηλεΐδης"),
        "Πηλείων (diphthong)": rx(r"Πηλείων\w*"),
        "Πηλεΐων (ε-ϊ)": rx(r"Πηλεΐων\w*"),
        "Ἀτρείδ (diphthong)": rx(r"Ἀτρείδ\w*"),
        "Ἀμαρυγκ- (Ἀμαρυγκεύς and patronymics)": rx(r"Ἀμαρυγκ\w*"),
        "capitalised -είδ- with the diphthong (all)": rx(r"\b[Α-ΩἈ-Ὧ]\w*είδ\w*"),
        "capitalised -εΐδ- (all)": rx(r"\b[Α-ΩἈ-Ὧ]\w*εΐδ\w*"),
        "Ζοκοβειδ (loose substring)": len(C.loose("ζοκοβειδ")),
        "Νοβηκ (loose substring)": len(C.loose("νοβηκ")),
    }
    res["ionic_eta"] = {"αθηνη --word": len(C.loose("αθηνη", word=True)),
                        "αθανα --word": len(C.loose("αθανα", word=True)),
                        "αθαναι --word": len(C.loose("αθαναι", word=True))}

    # 4. name slots
    slots = []
    for n, coined, model, cit, cond in SLOTS:
        e = ev[n]
        vw, vwp = e["words"], e["scan"]["word_positions"]
        cl = G.loose(coined)
        vi = vw.index(cl) if cl in vw else None
        ln = LINE.get(cit)
        ml = G.loose(model)
        mi = ln.loose_tokens.index(ml) if ln and ml in ln.loose_tokens else None
        mpos = ln.word_pos[mi] if (mi is not None and ln.word_pos) else None
        vpos = vwp[vi] if vi is not None else None
        same_form_at = posc(C.ngram([ml]))
        d = {"verse": n, "coined": coined, "verse_position": vpos,
             "verse_prev": vw[vi - 1] if vi else None, "verse_next": vw[vi + 1] if vi is not None and vi + 1 < len(vw) else None,
             "model": model, "model_citation": cit, "model_in_line": mi is not None, "model_position": mpos,
             "model_prev": ln.loose_tokens[mi - 1] if mi else None,
             "model_next": ln.loose_tokens[mi + 1] if mi is not None and mi + 1 < len(ln.loose_tokens) else None,
             "model_line": ln.text if ln else None, "same_position": vpos == mpos,
             "model_form_positions_in_homer": same_form_at, "condition": cond}
        slots.append(d)
    res["name_slots"] = slots

    # 5. counts asserted in the notes
    res["note_counts"] = {
        "Διομήδης": posc(C.ngram("Διομήδης")),
        "κρατερὸς Διομήδης": posc(C.ngram("κρατερὸς Διομήδης")),
        "Τεῦκρος": posc(C.ngram("Τεῦκρος")),
        "Παλλὰς": posc(C.ngram("Παλλὰς")),
        "Φοῖβος": posc(C.ngram("Φοῖβος")),
        "Ἀχαιῶν": posc(C.ngram("Ἀχαιῶν")),
        "Ἀπόλλων": posc(C.ngram("Ἀπόλλων")),
        "Ὀδυσσεύς": posc(C.ngram("Ὀδυσσεύς")),
        "Μελανθώ": posc(C.ngram("Μελανθώ")),
        "Ἀτρεΐδης": posc(C.ngram("Ἀτρεΐδης")),
        "ατρειδ (loose substring, the records' query)": posc(C.loose("ατρειδ")),
        "δαρδανιδης --word": posc(C.loose("δαρδανιδης", word=True)),
        "Ἀντίνοος": posc(C.ngram("Ἀντίνοος")),
        "* δʼ αὖτʼ": posc(C.ngram("* δ᾽ αὖτ᾽")),
        "Ἕκτωρ δʼ αὖτʼ": [f"{h.citation}@{h.pos_start}-{h.pos_end}" for h in C.ngram("Ἕκτωρ δ᾽ αὖτ᾽")],
        "Αἴας δʼ αὖτʼ": [f"{h.citation}@{h.pos_start}-{h.pos_end}" for h in C.ngram("Αἴας δ᾽ αὖτ᾽")],
        "τρὶς δέ μιν": len(C.ngram("τρὶς δέ μιν")),
        "δαμασεν --word": len(C.loose("δαμασεν", word=True)),
        "ἔκφερε --word": len(C.loose("εκφερε", word=True)),
        "δαΐφρονε --word": len(C.loose("δαιφρονε", word=True)),
        "ὣς τότε": posc(C.ngram("ὣς τότε")),
        "πολλάκι δή": posc(C.ngram("πολλάκι δή")),
    }

    # 4b. Homeric words beginning with ρ at 6 after a short vowel-final word ending at 5.5 (the Ῥογῆρος slot)
    rho = []
    for ln in C.lines:
        wp = ln.word_pos
        if not wp:
            continue
        for i in range(1, len(ln.loose_tokens)):
            w = ln.loose_tokens[i]
            pw = ln.loose_tokens[i - 1]
            if w.startswith("ρ") and wp[i].split("-")[0] == "6" and wp[i - 1].split("-")[1] == "5.5" \
                    and pw[-1] in "αεηιουω" and not pw.endswith("ʼ"):
                rho.append(f"{ln.work}. {ln.book}.{ln.line}: {pw} {w} | {ln.text}")
    res["rho_initial_at_6_after_vowel_final_word_at_5.5"] = {"count": len(rho), "examples": rho[:12]}

    # 6. position fields
    pf = []
    for r in recs:
        e = ev[r["n"]]
        for k, (s, es) in enumerate(zip(r.get("sources", []), e["sources"])):
            if not es["fragments"]:
                continue
            f0 = es["fragments"][0]
            if f0["in_poem_verbatim"] and s.get("position") and s["position"] not in f0["poem_positions"]:
                pf.append({"n": r["n"], "k": k, "text": s["text"], "position_field": s["position"],
                           "verse_position": f0["poem_positions"], "homer_positions": f0["homer_positions"]})
    res["position_field_mismatches"] = pf
    Path(out_path).write_text(json.dumps(res, ensure_ascii=False, indent=1), encoding="utf-8")
    print(json.dumps({k: (v if k not in ("name_slots", "patronymic") else "...") for k, v in res.items()},
                     ensure_ascii=False, indent=1)[:6000])


if __name__ == "__main__":
    main(*sys.argv[1:4])
