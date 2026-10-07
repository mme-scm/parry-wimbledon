#!/usr/bin/env python3
"""Formulaic density of a composed poem, measured against Homer with the n-gram method of analysis/formulas.

    source .venv/bin/activate
    python -I review/poem_density.py composition/drafts/v1.jsonl review/poem_density_v1.json

Greek analogue of analysis/formulas (report.md section 1, common.cover_a / boot_ratio / shuffle_tokens):
  * tokens   = homer/greek.tokenize on the NFC verse, compared in the loose form of homer/concordance.py
               (accents, breathings, diaeresis, iota subscript, case and punctuation ignored; elision kept),
               i.e. exactly what `concordance.py --ngram` compares;
  * n-grams  = contiguous word n-grams inside one verse (never across a line end), as utterances in the
               English analysis;
  * I        = Homer (homer/lines.tsv, Iliad + Odyssey); M = the poem (held-out design: I and M disjoint);
  * coverage = share of M's tokens lying inside at least one occurrence of a word n-gram (n >= 2, resp. n >= 3)
               that occurs in I at least once (`min1`, the definition asked for) or at least twice (`min2`, the
               strict analogue of 'repeated in I');
  * filters  = `all` (every n-gram) and `base` (n-grams made only of function words excluded, the analogue of
               the STOP filter; the Greek list FUNC below is frozen here and applies to loose forms);
  * CI       = percentile bootstrap over verses (B = 2000, seed 0), I fixed, as common.boot_ratio;
  * baseline = shuffled-word baseline: the poem's tokens permuted over positions with verse lengths kept
               (R = 200, seed 20190714), I fixed, as the held-out baselines of f03 (only M is shuffled);
  * Homeric reference: each Homeric verse measured against the rest of Homer (an n-gram counts if it occurs
    in at least one other verse), the same definitions; token-weighted over all verses;
  * exact-formula lines: share of verses containing at least one claimed `sources` string of >= 2 words
    (status other than COINAGE; Homeric string extracted as in review/provenance_check.py) found verbatim in
    the verse at a metrical position at which Homer has it (positions: homer/scan.py on the verse,
    homer/scansion.tsv via the concordance for Homer); the same share counting only formulas that are not
    made of function words alone (FUNC); and, unclaimed included, the share of verses containing any attested
    n-gram (n >= 2, not function-word-only) at a Homeric position.
"""
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "homer"))
sys.path.insert(0, str(ROOT / "review"))
import greek as G  # noqa: E402
import provenance_check as P  # noqa: E402  (builds the Concordance once: P.C)

B = 2000
R = 200
SEED_BOOT = 0
SEED_SHUFFLE = 20190714

# Function words, loose forms (frozen with this script). Articles, pronouns, particles, conjunctions,
# prepositions/preverbs, negations; elided variants included.
FUNC = frozenset("""
ο η το του τησ τω τη των τον την τα οι αι τοι ται τοισ τοισι τησι ταισ τουσ τασ τοιν
οσ ου ω ον α ων οισ οισι ασ ουσ ησ ησι οσσ οττι οτι
μιν ε εο ευ σφι σφιν σφισι σφε σφεασ σφωε σφωιν μοι με μευ μου εμοι εμε εμεο εμευ εγω εγων
συ σε σοι σευ σεο τυνη νωι νωιν ημεισ ημιν ημασ ημεασ υμιν υμεισ υμμι υμμιν αυτοσ αυτον αυτου αυτω αυτη αυτην
αυτοι αυτων αυτουσ αυτα τισ τι τινα τινι του
δε δʼ μεν τε τʼ γε γʼ αρα αρʼ αρ ρα ρʼ δη νυ κε κεν κʼ αν περ αλλα αλλʼ και ηδε ιδε ηε
ου ουκ ουχ ουδε ουδʼ μη μηδε μηδʼ ει αι ωσ οτε οτʼ οθʼ οππωσ επει επειτα επειτʼ αυ αυτε αυτʼ αυθʼ αυτισ
τοτε τοτʼ ενθα ενθʼ νυν ηδη γαρ ουν θην οφρα τοφρα ηυτε ημεν
εν ενι εσ εισ εκ εξ απο απʼ αφʼ επι επʼ εφʼ περι παρα παρʼ παρ κατα κατʼ καθʼ καδ μετα μετʼ μεθʼ ανα αμφι αμφʼ
προσ προτι ποτι υπο υπʼ υφʼ υπαι υπερ συν ξυν δια διʼ προ
""".split())


def loose_tokens(text):
    return [G.loose(t.core) for t in G.tokenize(G.nfc(text))]


def build_homer_index(nmax):
    occ = Counter()       # occurrences of each n-gram (2..nmax)
    nlines = Counter()    # distinct verses containing it
    lines = []
    for ln in P.C.lines:
        lt = ln.loose_tokens
        lines.append(lt)
        seen = set()
        L = len(lt)
        for n in range(2, min(nmax, L) + 1):
            for i in range(L - n + 1):
                g = tuple(lt[i:i + n])
                occ[g] += 1
                seen.add(g)
        nlines.update(seen)
    return occ, nlines, lines


def is_func_only(g):
    return all(w in FUNC for w in g)


def cover(toks, ok, n_min):
    """bool array: token inside >= 1 n-gram (n >= n_min) for which ok(g) is True."""
    L = len(toks)
    cov = np.zeros(L, dtype=bool)
    for n in range(n_min, L + 1):
        for i in range(L - n + 1):
            g = tuple(toks[i:i + n])
            if ok(g):
                cov[i:i + n] = True
    return cov


def boot_ratio(num, den, B=B, seed=SEED_BOOT):
    num = np.asarray(num, float)
    den = np.asarray(den, float)
    rng = np.random.default_rng(seed)
    idx = rng.integers(0, len(num), size=(B, len(num)))
    vals = num[idx].sum(1) / den[idx].sum(1)
    return float(num.sum() / den.sum()), float(np.percentile(vals, 2.5)), float(np.percentile(vals, 97.5))


def shuffle_tokens(utts, rng):
    flat = [t for u in utts for t in u]
    perm = rng.permutation(len(flat))
    flat = [flat[i] for i in perm]
    out, k = [], 0
    for u in utts:
        out.append(flat[k:k + len(u)])
        k += len(u)
    return out


def main(jsonl, out_path):
    recs = [json.loads(l) for l in open(jsonl, encoding="utf-8") if l.strip()]
    poem = [loose_tokens(r["text"]) for r in recs]
    nmax = max(len(t) for t in poem)
    homer_nmax = max(len(l.loose_tokens) for l in P.C.lines)
    occ, nlines, hlines = build_homer_index(max(nmax, homer_nmax))
    homer_line_set = {tuple(l) for l in hlines}

    defs = {
        "n2_all_min1": (2, lambda g: occ.get(g, 0) >= 1),
        "n2_base_min1": (2, lambda g: occ.get(g, 0) >= 1 and not is_func_only(g)),
        "n3_all_min1": (3, lambda g: occ.get(g, 0) >= 1),
        "n3_base_min1": (3, lambda g: occ.get(g, 0) >= 1 and not is_func_only(g)),
        "n2_base_min2": (2, lambda g: occ.get(g, 0) >= 2 and not is_func_only(g)),
        "n3_base_min2": (3, lambda g: occ.get(g, 0) >= 2 and not is_func_only(g)),
    }
    coinage_forms = set()
    for r in recs:
        for c in r.get("coinages") or []:
            coinage_forms.add(G.loose(c["form"].split()[0]))
    # also every token unattested in Homer counts as a coinage-type token for the 'non-coined tokens' variant
    vocab = Counter(w for l in hlines for w in l)
    unattested = {w for t in poem for w in t if vocab[w] == 0}

    verbatim = [tuple(t) in homer_line_set for t in poem]
    res = {"input": jsonl, "verses": len(poem), "tokens": int(sum(len(t) for t in poem)),
           "verses_identical_to_a_homeric_verse": int(sum(verbatim)),
           "verbatim_verse_numbers": [r["n"] for r, v in zip(recs, verbatim) if v],
           "tokens_unattested_in_homer": int(sum(1 for t in poem for w in t if w in unattested)),
           "unattested_forms": sorted(unattested),
           "func_words": len(FUNC), "B": B, "R": R, "coverage": {}, "per_verse": []}

    per_verse_cov = {}
    for name, (nmin, ok) in defs.items():
        covs = [cover(t, ok, nmin) for t in poem]
        per_verse_cov[name] = covs
        num = [c.sum() for c in covs]
        den = [len(c) for c in covs]
        est, lo, hi = boot_ratio(num, den)
        # excluding verbatim Homeric verses
        num_x = [c.sum() for c, v in zip(covs, verbatim) if not v]
        den_x = [len(c) for c, v in zip(covs, verbatim) if not v]
        est_x, lo_x, hi_x = boot_ratio(num_x, den_x)
        # excluding tokens unattested in Homer (the coined names), from the denominator
        num_c = [sum(1 for k, w in enumerate(t) if c[k] and w not in unattested) for t, c in zip(poem, covs)]
        den_c = [sum(1 for w in t if w not in unattested) for t in poem]
        est_c = float(sum(num_c) / sum(den_c))
        # shuffled baseline
        rng = np.random.default_rng(SEED_SHUFFLE)
        sh = []
        for _ in range(R):
            sp = shuffle_tokens(poem, rng)
            cs = [cover(t, ok, nmin) for t in sp]
            sh.append(sum(c.sum() for c in cs) / sum(len(c) for c in cs))
        sh = np.array(sh)
        res["coverage"][name] = {
            "coverage": round(100 * est, 1), "ci95": [round(100 * lo, 1), round(100 * hi, 1)],
            "excluding_verbatim_verses": {"coverage": round(100 * est_x, 1),
                                          "ci95": [round(100 * lo_x, 1), round(100 * hi_x, 1)],
                                          "verses": int(len(num_x)), "tokens": int(sum(den_x))},
            "excluding_tokens_unattested_in_homer": round(100 * est_c, 1),
            "shuffled_mean": round(100 * float(sh.mean()), 1),
            "shuffled_2.5_97.5": [round(100 * float(np.percentile(sh, 2.5)), 1),
                                  round(100 * float(np.percentile(sh, 97.5)), 1)],
            "excess_pp": round(100 * (est - float(sh.mean())), 1)}

    # Homeric reference: each verse against the rest of Homer (n-gram in >= 1 other verse)
    ref = {}
    for name, (nmin, base, thr) in {"n2_all_min1": (2, False, 1), "n2_base_min1": (2, True, 1),
                                    "n3_all_min1": (3, False, 1), "n3_base_min1": (3, True, 1),
                                    "n2_base_min2": (2, True, 2), "n3_base_min2": (3, True, 2)}.items():
        tot = cov_ = 0
        for lt in hlines:
            here = Counter()
            L = len(lt)
            for n in range(2, L + 1):
                for i in range(L - n + 1):
                    here[tuple(lt[i:i + n])] += 1

            def ok(g, here=here):
                if base and is_func_only(g):
                    return False
                # occurrences outside this verse (and, for thr = 1, at least one other verse)
                if thr == 1:
                    return nlines.get(g, 0) - 1 >= 1
                return occ.get(g, 0) - here[g] >= 2
            c = cover(lt, ok, nmin)
            tot += len(c)
            cov_ += int(c.sum())
        ref[name] = round(100 * cov_ / tot, 1)
    res["homeric_reference_verse_vs_rest_of_homer"] = ref
    res["homeric_reference_note"] = ("min1: n-gram in >= 1 other Homeric verse; min2: >= 2 occurrences outside "
                                     "the verse; token-weighted over all %d verses" % len(hlines))

    # exact-formula lines
    exact_lines, any_attested_pos_lines, exact_content_lines = [], [], []
    for r, toks in zip(recs, poem):
        sc = P.scan_verse(r["text"])
        wp = sc["word_positions"]
        found = []
        for s in r.get("sources", []):
            if s.get("status") == "COINAGE":
                continue
            for f in P.homeric_string(s):
                fl = P.loose_words(f)
                if len(fl) < 2:
                    continue
                occs = P.find_seq(toks, fl)
                if not occs:
                    continue
                hpos = {f"{h.pos_start}-{h.pos_end}" for h in P.C.ngram(fl)}
                for i in occs:
                    pp = P.poem_span(wp, i, i + len(fl) - 1)
                    if pp in hpos:
                        found.append({"formula": f, "position": pp})
        anyp = []
        L = len(toks)
        for n in range(2, L + 1):
            for i in range(L - n + 1):
                g = tuple(toks[i:i + n])
                if occ.get(g, 0) and not is_func_only(g):
                    hpos = {f"{h.pos_start}-{h.pos_end}" for h in P.C.ngram(list(g))}
                    pp = P.poem_span(wp, i, i + n - 1)
                    if pp in hpos:
                        anyp.append(" ".join(g))
        exact_lines.append(bool(found))
        exact_content_lines.append(any(not is_func_only(tuple(P.loose_words(x["formula"]))) for x in found))
        any_attested_pos_lines.append(bool(anyp))
        res["per_verse"].append({
            "n": r["n"], "tokens": len(toks), "verbatim_homeric_verse": verbatim[recs.index(r)],
            **{k: int(per_verse_cov[k][recs.index(r)].sum()) for k in per_verse_cov},
            "claimed_exact_formulas_ge2": found, "has_claimed_exact_ge2": bool(found),
            "has_any_attested_ngram_at_homeric_position": bool(anyp)})
    res["lines_with_claimed_exact_formula_ge2_words_pct"] = round(100 * sum(exact_lines) / len(recs), 1)
    res["lines_with_claimed_exact_formula_ge2_words"] = int(sum(exact_lines))
    res["lines_without_claimed_exact_formula_ge2_words"] = [r["n"] for r, e in zip(recs, exact_lines) if not e]
    res["lines_with_claimed_exact_formula_ge2_words_not_function_only_pct"] = round(
        100 * sum(exact_content_lines) / len(recs), 1)
    res["lines_without_claimed_exact_formula_ge2_words_not_function_only"] = [
        r["n"] for r, e in zip(recs, exact_content_lines) if not e]
    res["lines_with_any_attested_ngram_at_homeric_position_pct"] = round(
        100 * sum(any_attested_pos_lines) / len(recs), 1)
    res["lines_without_any_attested_ngram_at_homeric_position"] = [
        r["n"] for r, e in zip(recs, any_attested_pos_lines) if not e]
    Path(out_path).write_text(json.dumps(res, ensure_ascii=False, indent=1), encoding="utf-8")
    print(json.dumps({k: v for k, v in res.items() if k != "per_verse"}, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
