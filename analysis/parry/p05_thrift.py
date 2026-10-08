"""2b.3 thrift (economy) and extension per situational slot across the 20 TV streams (plan sections 7 H4a/H4b/H5 and 9).

E3 referring expressions (results/refexpr_pool_tokens.csv from p04): category shares per team, economy per team x player x slot,
the Parryan one-form-per-slot pattern, H4a (team labels permuted within slot, on categories), H4b (slot labels permuted within
team x player, on forms), H5 (syllables vs A_after, utterance-level permutation within stream), MDEs.
E1 formula expressions (genre inventory, greedy segmentation) and E2 functional-equivalence classes (frozen in plan section 9): economy per
team x slot / class with across-team permutation nulls. All E1/E2 results and every per-team or sensitivity row are exploratory.

Outputs: results/slot_token_counts.csv, results/refexpr_category_shares.csv, results/refexpr_economy.csv, results/parryan_pattern.csv,
results/thrift_tests_2b.csv, results/extension_2b.csv, results/mde_h4b.csv, results/e1_economy.csv, results/e1_top_types.csv,
results/e2_classes.csv, results/e2_tests.csv, results/primary_H4H5.json, results/thrift_meta.json
Run: python -I analysis/parry/p05_thrift.py
"""
import re
import sys
import time
from collections import Counter, defaultdict
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import numpy as np
from scipy.stats import rankdata, spearmanr
import lib2b as L
import refexpr as R

N_PERM = 10000
B = 2000
MDE_THETAS = (0.0, 0.05, 0.1, 0.15, 0.2, 0.3, 0.4)
MDE_SIMS, MDE_PERMS = 200, 499
CATS = ("surname", "first_name", "full_name", "title_surname", "hypocoristic", "epithet")
SLOTS = L.SLOTS


def fnum(x):
    try:
        v = float(x)
        return None if np.isnan(v) else v
    except (TypeError, ValueError):
        return None


# ---------------------------------------------------------------- generic permutation helpers
def n_distinct(*cols):
    code = np.zeros(len(cols[0]), dtype=np.int64)
    for c in cols:
        c = np.asarray(c, dtype=np.int64)
        code = code * (int(c.max()) + 1 if len(c) else 1) + c
    return len(np.unique(code))


def permute_within(labels, strata, rng):
    out = labels.copy()
    for s in np.unique(strata):
        ix = np.where(strata == s)[0]
        out[ix] = labels[rng.permutation(ix)]
    return out


def econ_stats(team, typ):
    """(sum over teams of distinct types, mean over teams of the modal-type share)."""
    team = np.asarray(team, np.int64)
    typ = np.asarray(typ, np.int64)
    code = team * (int(typ.max()) + 1) + typ
    u, cnt = np.unique(code, return_counts=True)
    tu = u // (int(typ.max()) + 1)
    tot = np.bincount(team)
    mx = np.zeros(len(tot))
    np.maximum.at(mx, tu, cnt)
    present = tot > 0
    return len(u), float(np.mean(mx[present] / tot[present]))


def enc(values):
    keys = sorted(set(values))
    m = {k: i for i, k in enumerate(keys)}
    return np.array([m[v] for v in values], np.int64), keys


# ---------------------------------------------------------------- E3
def load_refs():
    rows = L.read_csv(L.RESULTS / "refexpr_pool_tokens.csv")
    for r in rows:
        r["syllables"] = int(r["syllables"])
        for k in ("A_after", "A_before", "t_next_stored_valid"):
            r[k] = fnum(r[k])
    return rows


def category_shares(rows):
    out = []
    for refset in ("commentary_only", "all_references"):
        for team in L.TV + ["ALL_TV"]:
            rs = [r for r in rows if (team == "ALL_TV" or r["stream"] == team) and (refset == "all_references" or not r["umpire_pattern"])]
            res = [r for r in rs if r["player"] != "UNRESOLVED"]
            unres = len(rs) - len(res)
            c = Counter(r["category"] for r in res)
            n = len(res)
            row = {"team": team, "label": L.short(team) if team != "ALL_TV" else "all 20 TV streams", "references": refset,
                   "resolved_tokens": n, "unresolved_epithets": unres}
            for k in CATS:
                row[f"share_{k}"] = c.get(k, 0) / n if n else float("nan")
            row["share_epithet_upper"] = (c.get("epithet", 0) + unres) / (n + unres) if n + unres else float("nan")
            out.append(row)
    return out


def economy_rows(rows, slot_tokens):
    out = []
    for slot_type, key in (("situational", "slot_sit"), ("syntactic", "slot_syn")):
        g = defaultdict(Counter)
        for r in rows:
            g[(r["stream"], r["player"], r[key])][r["expression"]] += 1
        for (s, p, sl), c in sorted(g.items()):
            n = sum(c.values())
            mf, mc = c.most_common(1)[0]
            st = slot_tokens.get((s, sl)) if slot_type == "situational" else None
            out.append({"team": s, "label": L.short(s), "player": p, "slot_type": slot_type, "slot": sl, "references": n,
                        "distinct_forms": len(c), "modal_form": mf, "modal_share": mc / n, "distinct_per_100_refs": 100 * len(c) / n,
                        "slot_tokens": st if st else "", "distinct_per_100_slot_tokens": 100 * len(c) / st if st else "",
                        "forms": "; ".join(f"{e}:{k}" for e, k in c.most_common())})
    return out


def parryan(econ):
    out = []
    for slot_type in ("situational", "syntactic"):
        for team in L.TV:
            cells = [e for e in econ if e["team"] == team and e["slot_type"] == slot_type and e["references"] >= 5]
            if not cells:
                continue
            by_p = defaultdict(list)
            for e in cells:
                by_p[e["player"]].append(e)
            all_high = all(e["modal_share"] >= 0.9 for e in cells)
            complementary = any(len({e["modal_form"] for e in v}) >= 2 for v in by_p.values())
            if all_high and complementary:
                verdict = "one form per slot, slot-conditioned (Parryan)"
            elif all_high:
                verdict = "one form throughout (economy without slot conditioning)"
            else:
                verdict = "not one form per slot"
            out.append({"team": team, "label": L.short(team), "slot_type": slot_type, "cells_ge5": len(cells),
                        "cells_modal_ge_0.9": sum(e["modal_share"] >= 0.9 for e in cells),
                        "min_modal_share": min(e["modal_share"] for e in cells),
                        "distinct_modal_forms_within_player_max": max(len({e["modal_form"] for e in v}) for v in by_p.values()),
                        "verdict": verdict})
    return out


def h4(rows, rng, slot_key="slot_sit", n_perm=N_PERM):
    team, _ = enc([r["stream"] for r in rows])
    slot, _ = enc([r[slot_key] for r in rows])
    cat, _ = enc([r["category"] for r in rows])
    tp, _ = enc([(r["stream"], r["player"]) for r in rows])
    form, _ = enc([(r["stream"], r["player"], r["expression"]) for r in rows])
    Da = n_distinct(team, slot, cat)
    null_a = np.array([n_distinct(permute_within(team, slot, rng), slot, cat) for _ in range(n_perm)])
    Db = n_distinct(tp, slot, form)
    null_b = np.array([n_distinct(tp, permute_within(slot, tp, rng), form) for _ in range(n_perm)])
    res = {}
    for k, obs, null in (("H4a", Da, null_a), ("H4b", Db, null_b)):
        res[k] = {"D_obs": int(obs), "null_mean": float(null.mean()), "null_lo": float(np.percentile(null, 2.5)),
                  "null_hi": float(np.percentile(null, 97.5)), "null_sd": float(null.std()),
                  "p_one_sided_fewer": float((1 + np.sum(null <= obs)) / (n_perm + 1)), "permutations": n_perm, "tokens": len(rows)}
    return res


def h4b_per_team(rows, rng, slot_key="slot_sit", n_perm=N_PERM):
    out = []
    for team in L.TV:
        rs = [r for r in rows if r["stream"] == team]
        if len(rs) < 10:
            continue
        tp, _ = enc([r["player"] for r in rs])
        slot, _ = enc([r[slot_key] for r in rs])
        form, _ = enc([(r["player"], r["expression"]) for r in rs])
        D = n_distinct(tp, slot, form)
        null = np.array([n_distinct(tp, permute_within(slot, tp, rng), form) for _ in range(n_perm)])
        out.append({"team": team, "label": L.short(team), "slot_type": slot_key, "tokens": len(rs), "D_obs": D,
                    "null_mean": null.mean(), "p_one_sided_fewer": (1 + np.sum(null <= D)) / (n_perm + 1)})
    return out


def mde_h4b(rows, rng):
    """Plan section 9: with probability theta a reference takes a designated form of its team x player x slot cell
    (drawn from the team-player's observed forms in proportion to frequency); power of the H4b test at alpha 0.05."""
    tp, _ = enc([(r["stream"], r["player"]) for r in rows])
    slot, _ = enc([r["slot_sit"] for r in rows])
    form0, keys = enc([(r["stream"], r["player"], r["expression"]) for r in rows])
    forms_of = defaultdict(list)
    for i in range(len(rows)):
        forms_of[tp[i]].append(form0[i])
    out = []
    for th in MDE_THETAS:
        rej = 0
        for _ in range(MDE_SIMS):
            form = form0.copy()
            designated = {}
            for c in np.unique(tp * 100 + slot):
                t = c // 100
                pool = forms_of[t]
                designated[c] = pool[rng.integers(0, len(pool))]
            hit = rng.random(len(rows)) < th
            cells = tp * 100 + slot
            for i in np.where(hit)[0]:
                form[i] = designated[cells[i]]
            D = n_distinct(tp, slot, form)
            null = np.array([n_distinct(tp, permute_within(slot, tp, rng), form) for _ in range(MDE_PERMS)])
            p = (1 + np.sum(null <= D)) / (MDE_PERMS + 1)
            rej += p < 0.05
        out.append({"theta": th, "power_at_0.05": rej / MDE_SIMS, "simulations": MDE_SIMS, "permutations": MDE_PERMS})
    pw = [(o["theta"], o["power_at_0.05"]) for o in out]
    mde = None
    for (t0, p0), (t1, p1) in zip(pw, pw[1:]):
        if p0 < 0.8 <= p1:
            mde = t0 + (0.8 - p0) * (t1 - t0) / (p1 - p0)
            break
    return out, mde


def weighted_rho(groups):
    """groups: list of (x array, y ranks array). Weighted mean of Spearman rho (weights n)."""
    num, den = 0.0, 0
    for x, yr in groups:
        if len(x) < 3:
            continue
        xr = rankdata(x)
        if np.std(xr) == 0 or np.std(yr) == 0:
            continue
        num += np.corrcoef(xr, yr)[0, 1] * len(x)
        den += len(x)
    return num / den if den else float("nan")


def h5(rows, rng, xkey="A_after", n_perm=N_PERM, strata_key="stream"):
    rs = [r for r in rows if r[xkey] is not None]
    groups, perms = [], []
    per_stream = []
    for s in sorted({r[strata_key] for r in rs}):
        g = [r for r in rs if r[strata_key] == s]
        utts = sorted({r["utt_id"] for r in g})
        ui = {u: k for k, u in enumerate(utts)}
        uidx = np.array([ui[r["utt_id"]] for r in g])
        ua = np.array([next(r[xkey] for r in g if r["utt_id"] == u) for u in utts])
        y = np.array([r["syllables"] for r in g], float)
        yr = rankdata(y)
        groups.append((ua[uidx], yr))
        perms.append((uidx, ua, yr))
        rho_s = spearmanr(ua[uidx], y)[0] if len(g) >= 3 and np.std(y) > 0 else float("nan")
        per_stream.append((s, len(g), rho_s))
    obs = weighted_rho(groups)
    null = np.empty(n_perm)
    for p in range(n_perm):
        null[p] = weighted_rho([(ua[rng.permutation(len(ua))][uidx], yr) for uidx, ua, yr in perms])
    p_two = (1 + np.sum(np.abs(null) >= abs(obs))) / (n_perm + 1)
    # stream-cluster bootstrap CI
    ps = [(n, r) for _, n, r in per_stream if not np.isnan(r)]
    nn = np.array([n for n, _ in ps], float)
    rr = np.array([r for _, r in ps], float)
    bs = []
    for _ in range(B):
        ix = rng.integers(0, len(ps), len(ps))
        bs.append(np.sum(nn[ix] * rr[ix]) / np.sum(nn[ix]))
    return {"tokens": len(rs), "streams": len(per_stream), "rho_weighted": obs, "p_two": float(p_two), "null_sd": float(null.std()),
            "null_lo": float(np.percentile(null, 2.5)), "null_hi": float(np.percentile(null, 97.5)),
            "boot_lo": float(np.percentile(bs, 2.5)), "boot_hi": float(np.percentile(bs, 97.5)),
            "mde_rho_approx": float(2.80 * null.std()), "permutations": n_perm}, per_stream


def mixedlm(rows):
    import statsmodels.formula.api as smf
    import pandas as pd
    rs = [r for r in rows if r["A_after"] is not None and r["A_after"] > 0]
    df = pd.DataFrame({"syll": [r["syllables"] for r in rs], "logA": [np.log(r["A_after"]) for r in rs],
                       "stream": [r["stream"] for r in rs]})
    m = smf.mixedlm("syll ~ logA", df, groups=df["stream"]).fit(reml=True)
    ci = m.conf_int().loc["logA"]
    return {"coef_logA": float(m.params["logA"]), "ci_lo": float(ci[0]), "ci_hi": float(ci[1]), "p": float(m.pvalues["logA"]),
            "tokens": len(rs), "groups": int(df["stream"].nunique()), "model": "syllables ~ log(A_after) + (1 | stream), REML"}


# ---------------------------------------------------------------- slot token counts (token-level classifier)
def slot_token_counts(teams):
    out = {}
    rows = []
    for t in teams:
        c = Counter()
        for u in t.raw:
            c.update(L.SlotClassifier(u).token_slots())
        for sl in SLOTS:
            out[(t.name, sl)] = c.get(sl, 0)
            rows.append({"team": t.name, "label": L.short(t.name), "slot": sl, "tokens": c.get(sl, 0), "share": c.get(sl, 0) / t.ntok})
    return out, rows


# ---------------------------------------------------------------- E1
def e1(teams, slot_tokens, rng):
    pooled = [u for t in teams for u in t.norm]
    _, F, _ = L.index_inventory(pooled)
    Sys = L.C.system_set_fast(pooled, frozenset())   # norm tokens: names/numbers are already placeholders -> OPEN frames only
    Sys = {k for k in Sys if k[2] == "OPEN"}
    occ = []   # (team index, type string, slot)
    for ti, t in enumerate(teams):
        for u, ur in zip(t.norm, t.raw):
            cl = None
            i, Lu = 0, len(u)
            while i < Lu:
                found = None
                for n in range(min(12, Lu - i), 1, -1):
                    g = tuple(u[i:i + n])
                    if g in F:
                        found = (n, " ".join(g))
                        break
                    if n <= 6:
                        for j in range(1, n - 1):
                            key = (n, j, "OPEN", g[:j] + g[j + 1:])
                            if key in Sys:
                                found = (n, L.C.frame_str(key))
                                break
                        if found:
                            break
                if found:
                    if cl is None:
                        cl = L.SlotClassifier(ur)
                    occ.append((ti, found[1], cl.classify(i, i + found[0])))
                    i += found[0]
                else:
                    i += 1
    team_idx = np.array([o[0] for o in occ])
    typ, keys = enc([o[1] for o in occ])
    slot = np.array([o[2] for o in occ])
    rows, tests, top = [], [], []
    for sl in SLOTS:
        ix = np.where(slot == sl)[0]
        if len(ix) == 0:
            continue
        for ti, t in enumerate(teams):
            jx = ix[team_idx[ix] == ti]
            c = Counter(typ[jx])
            n = len(jx)
            st = slot_tokens[(t.name, sl)]
            mf, mc = c.most_common(1)[0] if c else (None, 0)
            rows.append({"team": t.name, "label": L.short(t.name), "slot": sl, "slot_tokens": st, "occurrences": n,
                         "distinct_types": len(c), "distinct_per_100_slot_tokens": 100 * len(c) / st if st else "",
                         "distinct_per_100_occurrences": 100 * len(c) / n if n else "", "modal_type": keys[mf] if c else "",
                         "modal_share": mc / n if n else ""})
        D, ms = econ_stats(team_idx[ix], typ[ix])
        nd, nm = np.empty(N_PERM), np.empty(N_PERM)
        for p in range(N_PERM):
            perm = team_idx[ix][rng.permutation(len(ix))]
            nd[p], nm[p] = econ_stats(perm, typ[ix])
        tests.append({"analysis": "E1 formula expressions", "slot": sl, "occurrences": len(ix), "D_obs": D, "null_mean": nd.mean(),
                      "null_lo": np.percentile(nd, 2.5), "null_hi": np.percentile(nd, 97.5),
                      "p_one_sided_fewer": (1 + np.sum(nd <= D)) / (N_PERM + 1), "modal_share_obs": ms, "modal_share_null_mean": nm.mean(),
                      "p_one_sided_modal_higher": (1 + np.sum(nm >= ms)) / (N_PERM + 1), "permutations": N_PERM,
                      "null": "team labels permuted among occurrences within slot", "status": "exploratory"})
        c = Counter(typ[ix])
        for k, n in c.most_common(8):
            teams_using = len(set(team_idx[ix][typ[ix] == k]))
            top.append({"slot": sl, "type": keys[k], "occurrences": n, "share_of_slot_occurrences": n / len(ix), "teams_using": teams_using})
    meta = {"genre_formulas": len(F), "genre_open_systems": len(Sys), "occurrences": len(occ)}
    return rows, tests, top, meta


# ---------------------------------------------------------------- E2 (plan section 9, frozen)
NUMW = r"(?:\d+|one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|thirteen|fourteen|fifteen|sixteen|seventeen|eighteen|nineteen|twenty|thirty|forty|fifty|sixty|seventy|eighty|ninety|hundred)"
PRAISE = "what a|great|good|lovely|brilliant|superb|fantastic|beautiful|terrific|wonderful|unbelievable|incredible|amazing|magnificent|sensational|excellent"
STROKE = "shot|point|rally|return|forehand|backhand|serve|volley|winner|get"
E2 = [
    ("tied_at_forty", "SCORE", [("deuce", r"deuce"), ("40 all", r"40 all"), ("forty all", r"forty all"), ("40 40", r"40 40")]),
    ("match_point", "SCORE", [("match point", r"match points?"), ("championship point", r"championship points?")]),
    ("break_chance", "SCORE", [("break back point", r"break back points?"), ("break point", r"break points?"),
                               ("chance to break", r"chances? to break"), ("break chance", r"break chances?"),
                               ("break opportunity", r"break opportunit(?:y|ies)")]),
    ("challenge", "OFFICIAL", [("is challenging", r"is challenging"), ("challenge from", r"challenge from"),
                               ("going to challenge", r"going to challenge"), ("has challenged", r"has challenged"),
                               ("challenges the call", r"challenges the call")]),
    ("net_error", "SHOT", [("into the bottom of the net", r"into the bottom of the net"), ("into the net", r"into the net"),
                           ("in the net", r"in the net"), ("into the tape", r"into the tape"), ("finds the net", r"(?:finds|found) the net"),
                           ("hits the net", r"(?:hits|hit) the net")]),
    ("along_the_line", "SHOT", [("down the line", r"down the line"), ("up the line", r"up the line")]),
    ("serve_centre", "SHOT", [("down the t", r"down the t"), ("down the middle", r"down the middle"), ("down the centre", r"down the centre"),
                              ("up the t", r"up the t"), ("up the middle", r"up the middle")]),
    ("serve_body", "SHOT", [("into the body", r"into the body"), ("at the body", r"at the body"), ("body serve", r"body serve"),
                            ("to the body", r"to the body")]),
    ("serve_wide", "SHOT", [("out wide", r"out wide"), ("wide serve", r"wide serve"), ("serve wide", r"serve wide"),
                            ("swinging wide", r"swinging wide")]),
    ("small_degree", "JUDGE", [("a little bit", r"a little bit"), ("a little", r"a little"), ("a bit", r"a bit"), ("slightly", r"slightly"),
                               ("a touch", r"a touch")]),
    ("praise_stroke", "JUDGE", [(w, rf"{w} (?:{STROKE})") for w in PRAISE.split("|")]),
    ("well_played", "JUDGE", [("well played", r"well played"), ("nicely played", r"nicely played"), ("beautifully played", r"beautifully played"),
                              ("brilliantly played", r"brilliantly played"), ("superbly played", r"superbly played"), ("well done", r"well done")]),
    ("obligation", "JUDGE", [("got to", r"(?:'s |has |have )?got to"), ("need to", r"needs? to"), ("have to", r"(?:has|have) to"),
                             ("must", r"must")]),
    ("opinion_hedge", "JUDGE", [("i think", r"i think"), ("i feel", r"i feel"), ("i believe", r"i believe"), ("i reckon", r"i reckon"),
                                ("i suspect", r"i suspect"), ("i would say", r"i'd say|i would say"), ("i guess", r"i guess")]),
    ("speed_unit", "STAT", [("miles an hour", rf"{NUMW} miles an hour"), ("miles per hour", rf"{NUMW} miles per hour"), ("mph", rf"{NUMW} mph"),
                            ("kilometres per hour", rf"{NUMW} (?:kilometres|kilometers) (?:an|per) hour"), ("km h", rf"{NUMW} km h"),
                            ("kph", rf"{NUMW} kph")]),
    ("major_titles", "STAT", [("grand slam titles", r"grand slam titles"), ("slam titles", r"slam titles"), ("major titles", r"major titles"),
                              ("grand slams", r"grand slams"), ("majors", r"majors"), ("slams", r"slams")]),
    ("audience", "CROWD", [("crowd", r"crowd"), ("fans", r"fans"), ("spectators", r"spectators"), ("audience", r"audience"),
                           ("supporters", r"supporters")]),
]


def unify(toks):
    s = " ".join(toks)
    s = re.sub(r"\bcrosscourt\b", "cross court", s)
    s = re.sub(r"\bhawkeye\b", "hawk eye", s)
    s = re.sub(r"\btie ?break(?:er)?s?\b", "tie break", s)
    s = re.sub(r"\bper cent\b", "percent", s)
    s = re.sub(r"\bcenter\b", "centre", s)
    return s


E2_RE = [(cname, fname, re.compile(rf"(?<![\w']){pat}(?![\w'])")) for cname, slot, forms in E2 for fname, pat in forms]
E2_EXT_PERM = 2000   # E2 extension has about 300 stream x class strata; fewer permutations (exploratory)


def e2_find(s):
    """Non-overlapping class matches in a unified token string; longest form (in tokens) first across all classes."""
    cands = []
    for cname, fname, rg in E2_RE:
        for m in rg.finditer(s):
            cands.append((m.start(), m.end(), cname, fname, m.group(0)))
    cands.sort(key=lambda c: (-(len(c[4].split())), c[0]))
    taken = []
    out = []
    for a, b, cname, fname, txt in cands:
        if any(a < y and x < b for x, y in taken):
            continue
        taken.append((a, b))
        out.append((a, cname, fname, txt))
    return sorted(out)


def e2(teams, rng, gaps_by_team):
    occ = []   # (team name, utt_id, class, form, syllables, A_after)
    for t in teams:
        gaps = gaps_by_team.get(t.name, {})
        for u, uid in zip(t.raw, t.ids):
            for a, cname, fname, txt in e2_find(unify(u)):
                syl = sum(R.syll_word(w) for w in txt.split())
                occ.append((t.name, uid, cname, fname, syl, (gaps.get(uid) or {}).get("A_after")))
    rows, tests = [], []
    slot_of = {c: s for c, s, _ in E2}
    tvnames = [t.name for t in teams if t.medium == "tv"]
    for cname, slot, forms in E2:
        oc = [o for o in occ if o[2] == cname]
        for t in teams:
            c = Counter(o[3] for o in oc if o[0] == t.name)
            n = sum(c.values())
            mf, mc = c.most_common(1)[0] if c else ("", 0)
            rows.append({"team": t.name, "label": L.short(t.name), "medium": t.medium, "class": cname, "slot": slot, "occurrences": n,
                         "per_10k_tokens": 1e4 * n / t.ntok, "distinct_forms": len(c), "modal_form": mf, "modal_share": mc / n if n else "",
                         "forms": "; ".join(f"{f}:{k}" for f, k in c.most_common())})
        tv_oc = [o for o in oc if o[0] in tvnames]
        if len({o[3] for o in tv_oc}) < 2:
            tests.append({"analysis": "E2 class", "class": cname, "slot": slot, "occurrences": len(tv_oc), "note": "fewer than 2 forms attested"})
            continue
        team_idx, _ = enc([o[0] for o in tv_oc])
        typ, _ = enc([o[3] for o in tv_oc])
        D, ms = econ_stats(team_idx, typ)
        nd, nm = np.empty(N_PERM), np.empty(N_PERM)
        for p in range(N_PERM):
            perm = team_idx[rng.permutation(len(team_idx))]
            nd[p], nm[p] = econ_stats(perm, typ)
        tests.append({"analysis": "E2 class", "class": cname, "slot": slot, "occurrences": len(tv_oc), "teams": len(set(team_idx)),
                      "D_obs": D, "null_mean": nd.mean(), "null_lo": np.percentile(nd, 2.5), "null_hi": np.percentile(nd, 97.5),
                      "p_one_sided_fewer": (1 + np.sum(nd <= D)) / (N_PERM + 1), "modal_share_obs": ms, "modal_share_null_mean": nm.mean(),
                      "p_one_sided_modal_higher": (1 + np.sum(nm >= ms)) / (N_PERM + 1), "permutations": N_PERM,
                      "null": "team labels permuted among the class's occurrences (20 TV teams)", "status": "exploratory"})
    # E2 extension: syllables of the form vs A_after within stream x class (utterance-level permutation within stream x class)
    ext_rows = [{"stream": o[0] + "|" + o[2], "utt_id": o[1], "syllables": o[4], "A_after": o[5]} for o in occ if o[0] in tvnames]
    ext, _ = h5(ext_rows, rng, n_perm=E2_EXT_PERM)
    return rows, tests, ext


def main():
    t0 = time.time()
    rng = np.random.default_rng([L.SEED, 5])
    refs = load_refs()
    comm = [r for r in refs if not r["umpire_pattern"] and r["player"] != "UNRESOLVED"]
    allr = [r for r in refs if r["player"] != "UNRESOLVED"]
    tv_teams = [L.load_tv(s) for s in L.TV]
    slot_tokens, st_rows = slot_token_counts(tv_teams)
    L.write_csv(L.RESULTS / "slot_token_counts.csv", st_rows)
    L.write_csv(L.RESULTS / "refexpr_category_shares.csv", category_shares(refs))
    econ = economy_rows(comm, slot_tokens)
    L.write_csv(L.RESULTS / "refexpr_economy.csv", econ)
    L.write_csv(L.RESULTS / "parryan_pattern.csv", parryan(econ))
    tests = []
    primary = {}
    res = h4(comm, rng)
    for k in ("H4a", "H4b"):
        primary[k] = {**res[k], "statistic": {"H4a": "D_a = sum over team x situational slot of distinct reference categories",
                                              "H4b": "D_b = sum over team x player x situational slot of distinct forms"}[k],
                      "references": "commentary-only, resolved"}
        tests.append({"test": k, "references": "commentary_only", "slot_type": "situational", **res[k], "status": "2b-primary"})
    for refset, rs in (("all_references", allr),):
        r2 = h4(rs, rng)
        for k in ("H4a", "H4b"):
            tests.append({"test": k, "references": refset, "slot_type": "situational", **r2[k], "status": "exploratory (sensitivity)"})
    r3 = h4(comm, rng, slot_key="slot_syn")
    for k in ("H4a", "H4b"):
        tests.append({"test": k, "references": "commentary_only", "slot_type": "syntactic", **r3[k], "status": "exploratory"})
    per_team = h4b_per_team(comm, rng) + h4b_per_team(comm, rng, "slot_syn")
    for p in per_team:
        tests.append({"test": "H4b per team", "references": "commentary_only", "slot_type": p["slot_type"], "team": p["label"],
                      "tokens": p["tokens"], "D_obs": p["D_obs"], "null_mean": p["null_mean"], "p_one_sided_fewer": p["p_one_sided_fewer"],
                      "permutations": N_PERM, "status": "exploratory"})
    mde_rows, mde = mde_h4b(comm, np.random.default_rng([L.SEED, 6]))
    L.write_csv(L.RESULTS / "mde_h4b.csv", mde_rows)
    primary["H4b"]["mde_theta_80pct_power"] = mde
    # ---- H5 and extension sensitivities
    ext_rows = []
    h, per_stream = h5(comm, rng)
    primary["H5"] = {**h, "statistic": "token-weighted mean of within-stream Spearman rho (syllables vs A_after)",
                     "references": "commentary-only, resolved, with A_after"}
    ext_rows.append({"analysis": "H5", "references": "commentary_only", "time": "A_after (hit clock)", **h, "status": "2b-primary"})
    for refset, rs in (("all_references", allr),):
        h2, _ = h5(rs, rng)
        ext_rows.append({"analysis": "H5 sensitivity", "references": refset, "time": "A_after (hit clock)", **h2, "status": "exploratory"})
    h3, _ = h5(comm, rng, xkey="A_before")
    ext_rows.append({"analysis": "H5 sensitivity", "references": "commentary_only", "time": "A_before (hit clock)", **h3, "status": "exploratory"})
    h4_, _ = h5(comm, rng, xkey="t_next_stored_valid")
    ext_rows.append({"analysis": "H5 sensitivity", "references": "commentary_only",
                     "time": "t_to_next_first_hit_s (stored; 25-fps streams only)", **h4_, "status": "exploratory"})
    try:
        ml = mixedlm(comm)
    except Exception as e:  # noqa: BLE001
        ml = {"error": repr(e)}
    primary["H5"]["mixedlm"] = ml
    gaps_by_team = {s: L.hit_gaps(s) for s in L.TV}
    # ---- E1, E2
    e1_rows, e1_tests, e1_top, e1_meta = e1(tv_teams, slot_tokens, rng)
    L.write_csv(L.RESULTS / "e1_economy.csv", e1_rows)
    L.write_csv(L.RESULTS / "e1_top_types.csv", e1_top)
    teams_e2 = tv_teams + [L.load_cornell(), L.load_press(None)]
    e2_rows, e2_tests, e2_ext = e2(teams_e2, rng, gaps_by_team)
    ext_rows.append({"analysis": "E2 extension", "references": "E2 class occurrences (TV)", "time": "A_after (hit clock)", **e2_ext,
                     "status": "exploratory (strata = stream x class)"})
    L.write_csv(L.RESULTS / "e2_classes.csv", e2_rows)
    L.write_csv(L.RESULTS / "e2_tests.csv", e1_tests + e2_tests)
    L.write_csv(L.RESULTS / "thrift_tests_2b.csv", tests,
                ["test", "references", "slot_type", "team", "tokens", "D_obs", "null_mean", "null_lo", "null_hi", "null_sd",
                 "p_one_sided_fewer", "permutations", "status"])
    L.write_csv(L.RESULTS / "extension_2b.csv", ext_rows,
                ["analysis", "references", "time", "tokens", "streams", "rho_weighted", "boot_lo", "boot_hi", "null_lo", "null_hi",
                 "null_sd", "p_two", "mde_rho_approx", "permutations", "status"])
    L.write_csv(L.RESULTS / "extension_per_stream.csv",
                [{"stream": s, "label": L.short(s), "tokens": n, "rho": r} for s, n, r in per_stream])
    L.write_json(L.RESULTS / "primary_H4H5.json", primary)
    L.write_json(L.RESULTS / "thrift_meta.json", {"e1": e1_meta, "runtime_s": round(time.time() - t0, 1), "N_PERM": N_PERM,
                                                  "E2_extension_permutations": E2_EXT_PERM,
                                                  "commentary_refs": len(comm), "all_refs": len(allr)})
    print("done", round(time.time() - t0, 1), "s")


if __name__ == "__main__":
    main()
