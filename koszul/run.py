#!/usr/bin/env python3
"""Compute H_0, H_1 and f_2 over Z for a pair of 2-forms; cross-check; write results/.

Usage: python run.py [--config forms.json] [--skip-checks]
"""
import argparse
import json
import math
import os
import time
from collections import Counter
from itertools import combinations

from exterior import mono_mul, mono_str, parse, to_str
from koszul import Computation, Pair, f2_image, group_str, primary
from zlinalg import matvec, rank_mod_p, smith

HERE = os.path.dirname(os.path.abspath(__file__))


def load_config(path):
    with open(path) as fh:
        cfg = json.load(fh)
    return cfg


def label_fn(P, chars):
    """Readable block label: values of the display characters (validated as weights)."""
    if not chars:
        return lambda k, w: str(w)
    for ch in chars:
        vals = {sum(ch[i] for i in range(P.n) if m >> i & 1) for f in (P.eta1, P.eta2) for m in f}
        assert len(vals) == 1, "display character is not a weight of the forms"
    lab = {}
    for k in range(P.n + 1):
        for w, mons in P.blocks[k].items():
            labs = {tuple(sum(ch[i] for i in range(P.n) if m >> i & 1) for ch in chars) for m in mons}
            assert len(labs) == 1
            lab[k, w] = labs.pop()
    for k in range(P.n + 1):
        assert len({lab[k, w] for w in P.blocks[k]}) == len(P.blocks[k]), "labels not injective"
    return lambda k, w: "(" + ", ".join(f"{x:+d}" for x in lab[k, w]) + ")"


def sparse(basis, vec):
    return {m: c for m, c in zip(basis, vec) if c}


def terms_json(d):
    return [[[i + 1 for i in range(m.bit_length()) if m >> i & 1], c] for m, c in sorted(d.items())]


def lll_rows(rows):
    try:
        import flint
    except ImportError:
        return rows
    if not rows:
        return rows
    M = flint.fmpz_mat(len(rows), len(rows[0]), [x for r in rows for x in r]).lll()
    return [[int(M[i, j]) for j in range(M.ncols())] for i in range(M.nrows())]


def nice_h1_basis(b1):
    """Short cycles forming a Z-basis of H_1 in block b1 (when H_1 is free there); else raw generators."""
    raw = [i for i in b1.nontrivial()]
    if not raw:
        return []
    free = [i for i in raw if b1.orders[i] == 0]
    if len(free) != len(raw) or len(free) > 4:
        return [b1.generator(i) for i in raw]
    # Z_1 basis = columns of b1.K; LLL it, then pick vectors whose H_1-coordinates form a unimodular matrix.
    zcols = [[row[j] for row in b1.K] for j in range(b1.zrank)]
    red = sorted(lll_rows(zcols), key=lambda v: sum(x * x for x in v))
    # coordinates in H_1: c = Ux * (K-coordinates);  K-coordinates of v: solve K y = v via Vi of D's Smith form
    Kpinv = _k_coords(b1)
    cands = red[: min(len(red), 10)]
    coords = []
    for v in cands:
        y = Kpinv(v)
        c = matvec(b1.sX.U, y)
        coords.append([c[i] for i in free])
    for S in combinations(range(len(cands)), len(free)):
        M = [coords[s] for s in S]
        if abs(_det(M)) == 1:
            nb = len(b1.basis)
            return [(cands[s][:nb], cands[s][nb:]) for s in S]
    return [b1.generator(i) for i in raw]


def _k_coords(b1):
    return lambda v: matvec(b1.Kc, v)


def _det(M):
    n = len(M)
    if n == 0:
        return 1
    if n == 1:
        return M[0][0]
    return sum((-1) ** j * M[0][j] * _det([r[:j] + r[j + 1:] for r in M[1:]]) for j in range(n))


def inv_mod2(A):
    n = len(A)
    M = [[a % 2 for a in row] + [int(i == j) for j in range(n)] for i, row in enumerate(A)]
    for c in range(n):
        piv = next(i for i in range(c, n) if M[i][c])
        M[c], M[piv] = M[piv], M[c]
        for i in range(n):
            if i != c and M[i][c]:
                M[i] = [(x + y) % 2 for x, y in zip(M[i], M[c])]
    return [row[n:] for row in M]


def mod2_functionals(b0):
    """Basis of the mod-2 functionals on the block Λ^d_w that vanish on the ideal (left kernel of M mod 2)."""
    from zlinalg import nullspace_mod_p

    m = len(b0.tgt)
    if not b0.M or not b0.M[0]:
        return [[int(i == j) for j in range(m)] for i in range(m)]
    MT = [[b0.M[i][j] for i in range(m)] for j in range(len(b0.M[0]))]
    return nullspace_mod_p(MT, 2, m)


def f2_vector(P, a1, a2, basis):
    from exterior import add, mul

    A1, A2 = sparse(basis, a1), sparse(basis, a2)
    return add(mul(A1, P.g2), mul(A2, P.g1), -1)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", default=os.path.join(HERE, "forms.json"))
    ap.add_argument("--out", default=os.path.join(HERE, "results"))
    ap.add_argument("--skip-checks", action="store_true")
    args = ap.parse_args()
    cfg = load_config(args.config)
    n = cfg["n"]
    eta1, eta2 = parse(cfg["eta1"]), parse(cfg["eta2"])
    os.makedirs(args.out, exist_ok=True)
    t0 = time.time()
    P = Pair(n, eta1, eta2)
    C = Computation(P)
    lab = label_fn(P, cfg.get("display_characters"))
    t_main = time.time() - t0

    R = {"n": n, "eta1": to_str(eta1), "eta2": to_str(eta2),
         "gamma2_eta1": to_str(P.g1), "gamma2_eta2": to_str(P.g2),
         "weight_lattice": P.chi, "weight_of_eta": P.c, "H0": {}, "H1": {}, "f2": {}}
    for d in range(n + 1):
        free, tors = C.summary(C.H0[d])
        R["H0"][d] = {"free": free, "torsion": sorted(tors), "group": group_str(free, tors),
                      "primary": {str(q): c for q, c in sorted(primary(tors).items())}}
    for k in range(n + 1):
        free, tors = C.summary(C.H1[k])
        R["H1"][k] = {"free": free, "torsion": sorted(tors), "group": group_str(free, tors),
                      "primary": {str(q): c for q, c in sorted(primary(tors).items())}}

    # f_2: structure of the image in each degree, and 2 f_2 = 0 check
    detail = {}
    for k in range(n + 1):
        img = f2_image(C, k)
        free = sum(s[0] for *_, s in img)
        tors = [q for *_, s in img for q in s[1]]
        for b1, b0, Y, _ in img:
            for j, row in enumerate(Y):
                for v in row:
                    o = b0.orders[j]
                    assert (2 * v) % o == 0 if o else v == 0, "2 f_2 != 0"
        R["f2"][k] = {"target_degree": k + 4, "image": group_str(free, tors), "image_free": free, "image_torsion": sorted(tors)}
        detail[k] = [x for x in img if any(any(r) for r in x[2])]

    # explicit description of f_2 on blocks where H_1 ≠ 0 and the target has 2-torsion
    blocks_out = []
    cert_cycles, cert_funcs = [], []
    for k in range(n + 1):
        for b1 in C.H1[k]:
            if b1.F is None or not b1.nontrivial():
                continue
            b0 = C.H0index[(k + 4, P.shift(b1.w, 2))]
            if 2 not in b0.orders:
                continue
            if any(o not in (1, 2) for o in b0.orders):
                R.setdefault("f2_blocks_not_presented", []).append([k, lab(k, b1.w)])
                continue  # explicit presentation only for targets ≅ (Z/2)^r; the image structure above covers all
            gens = nice_h1_basis(b1)
            lams = mod2_functionals(b0)
            tidx = {m: i for i, m in enumerate(b0.tgt)}
            # H_0 generators: monomials m_1..m_r whose classes form a basis; λ'_i dual to them
            mons, lam_cols = [], []
            for m in b0.tgt:
                v = [l[tidx[m]] % 2 for l in lams]
                if rank_mod_p(lam_cols + [v], 2) > len(lam_cols):
                    mons.append(m)
                    lam_cols.append(v)
                if len(mons) == len(lams):
                    break
            assert len(mons) == len(lams)
            Ainv = inv_mod2([[lam_cols[j][i] for j in range(len(mons))] for i in range(len(lams))])
            lams = [[sum(Ainv[i][t] * lams[t][c] for t in range(len(lams))) % 2 for c in range(len(b0.tgt))] for i in range(len(lams))]
            assert all(lams[i][tidx[mons[j]]] == int(i == j) for i in range(len(mons)) for j in range(len(mons)))
            vals = [f2_vector(P, a1, a2, b1.basis) for a1, a2 in gens]
            mat = [[sum(l[tidx[m]] * c for m, c in v.items()) % 2 for v in vals] for l in lams]
            r = rank_mod_p(mat, 2) if mat and mat[0] else 0
            cls = lambda j: " + ".join(f"[{mono_str(mons[i])}]" for i in range(len(mons)) if mat[i][j]) or "0"
            entry = {"k": k, "block": lab(k, b1.w), "dim_block": len(b1.basis),
                     "H1_block": group_str(*C.summary([b1])), "H0_target_block": group_str(*C.summary([b0])),
                     "H0_generators": [mono_str(m) for m in mons],
                     "cycles": [{"a1": to_str(sparse(b1.basis, a1)), "a2": to_str(sparse(b1.basis, a2)),
                                 "f2": to_str(v), "f2_class": cls(j)} for j, ((a1, a2), v) in enumerate(zip(gens, vals))],
                     "functionals": [to_str({m: 1 for m, c in zip(b0.tgt, l) if c}) for l in lams],
                     "matrix_mod2": mat, "rank": r}
            blocks_out.append(entry)
            if r:
                # pick r cycles and r functionals with invertible minor for the certificate
                rows = next(S for S in combinations(range(len(lams)), r) if rank_mod_p([mat[i] for i in S], 2) == r)
                sub = [mat[i] for i in rows]
                cols = next(T for T in combinations(range(len(gens)), r) if rank_mod_p([[row[j] for j in T] for row in sub], 2) == r)
                for j in cols:
                    a1, a2 = gens[j]
                    cert_cycles.append({"a1": terms_json(sparse(b1.basis, a1)), "a2": terms_json(sparse(b1.basis, a2))})
                for i in rows:
                    cert_funcs.append({"modulus": 2, "coeffs": terms_json({m: 1 for m, c in zip(b0.tgt, lams[i]) if c % 2})})
    key = lambda e: (e["k"], -e["rank"], [-int(x) for x in e["block"].strip("()").split(",")] if e["block"].startswith("(") else e["block"])
    R["f2_blocks"] = sorted(blocks_out, key=key)

    if cert_cycles:
        ks = {e["k"] for e in blocks_out if e["rank"]}
        assert len(ks) == 1, "certificate format assumes a single source degree"
        cert = {"n": n, "k": ks.pop(), "eta1": to_str(eta1), "eta2": to_str(eta2),
                "cycles": cert_cycles, "functionals": cert_funcs}
        with open(os.path.join(args.out, "certificate.json"), "w") as fh:
            json.dump(cert, fh, indent=1)

    # checks
    if not args.skip_checks:
        import checks

        t1 = time.time()
        L, mats = checks.ungraded(P)
        R["fp"] = {}
        for p in cfg.get("primes", [2, 3, 5, 7]):
            h0, h1, f2 = checks.fp_dims(P, p, L, mats, with_f2=(p == 2))
            ph0, ph1 = checks.uct_prediction(C, p)
            R["fp"][p] = {"H0": h0, "H1": h1, "uct_H0": ph0, "uct_H1": ph1, "agree": h0 == ph0 and h1 == ph1}
            if p == 2:
                R["fp"][p]["f2_rank"] = f2
            assert h0 == ph0 and h1 == ph1, f"UCT mismatch at p={p}"
        try:
            mism, img2, imgodd = checks.flint_blocks(C)
            R["flint"] = {"block_mismatches": mism, "f2_image_log2_order": dict(img2), "f2_image_odd_part": dict(imgodd)}
            assert not mism
            for k in range(n + 1):
                if R["f2"][k]["image_free"] == 0 and k in img2:
                    tq = R["f2"][k]["image_torsion"]
                    assert all(q & (q - 1) == 0 for q in tq)
                    mine = sum(q.bit_length() - 1 for q in tq)
                    assert mine == img2[k] and imgodd[k] <= 1, (k, mine, img2[k])
        except ImportError:
            R["flint"] = "python-flint not installed; skipped"
        R["check_seconds"] = round(time.time() - t1, 1)
    R["main_seconds"] = round(t_main, 1)

    with open(os.path.join(args.out, "results.json"), "w") as fh:
        json.dump(R, fh, indent=1, ensure_ascii=False)
    write_report(R, os.path.join(args.out, "report.md"))
    print(f"wrote {args.out}/report.md, results.json" + (", certificate.json" if cert_cycles else ""))


def write_report(R, path):
    n = R["n"]
    L = []
    w = L.append
    w("# Koszul homology of (η₁, η₂) over Z and the map f₂\n")
    w("Generated by `run.py` from `forms.json`; every number below is computed, none is typed in.\n")
    w(f"- η₁ = {R['eta1']}")
    w(f"- η₂ = {R['eta2']}")
    w(f"- γ₂(η₁) = {R['gamma2_eta1']}")
    w(f"- γ₂(η₂) = {R['gamma2_eta2']}\n")
    w("H₁ᵏ = {(a₁, a₂) ∈ (Λᵏ)² : a₁η₂ − a₂η₁ = 0} / {(bη₁, bη₂) : b ∈ Λᵏ⁻²},  "
      "H₀ᵈ = Λᵈ/(η₁Λᵈ⁻² + η₂Λᵈ⁻²),  f₂(a₁, a₂) = a₁γ₂(η₂) − a₂γ₂(η₁) : H₁ᵏ → H₀ᵏ⁺⁴.\n")
    nz = [k for k in range(n + 1) if R["f2"][k]["image"] != "0"]
    w("## Answer\n")
    if nz:
        for k in nz:
            w(f"- **f₂ ≠ 0 over Z.** On H₁^{k} = {R['H1'][k]['group']} it has image {R['f2'][k]['image']} "
              f"inside H₀^{k + 4} = {R['H0'][k + 4]['group']}.")
        w(f"- f₂ = 0 on H₁ᵏ for k ∉ {{{', '.join(map(str, nz))}}}.")
    else:
        w("- f₂ = 0 over Z in every degree.")
    if "fp" in R and 2 in R["fp"]:
        f2r = R["fp"][2]["f2_rank"]
        w(f"- Over F₂ (ungraded, independent code): rank f₂ on H₁ᵏ(F₂) is "
          + ", ".join(f"{r} (k={k})" for k, r in enumerate(f2r) if r) + "; 0 in all other degrees.")
    w("- 2·f₂ = 0 identically: 2f₂(a) = a₁η₂² − a₂η₁² = a₂η₁(η₂ − η₁) ∈ (η₁). So the image of f₂ lies in the "
      "2-torsion of H₀ and f₂ factors through H₁/2H₁ (checked on every generator).")
    if nz:
        w("- A standalone, independently coded check of f₂ ≠ 0 is in `results/certificate.json`; run `python verify_certificate.py`.\n")
    w("## H₀ and H₁ as abelian groups\n")
    has2 = "fp" in R and 2 in R["fp"]
    w("| degree | H₀ over Z | H₁ over Z |" + (" dim H₀(F₂) | dim H₁(F₂) |" if has2 else ""))
    w("|---|---|---|" + ("---|---|" if has2 else ""))
    for d in range(n + 1):
        row = f"| {d} | {R['H0'][d]['group']} | {R['H1'][d]['group']} |"
        if has2:
            row += f" {R['fp'][2]['H0'][d]} | {R['fp'][2]['H1'][d]} |"
        w(row)
    w("\nDegree of H₁ = degree of a₁, a₂.  Torsion primes that occur: "
      + (", ".join(sorted({q for x in list(R['H0'].values()) + list(R['H1'].values()) for q in x['primary']}, key=int)) or "none")
      + " (prime powers).\n")
    w("## f₂ by degree\n")
    w("| k | H₁ᵏ | H₀ᵏ⁺⁴ | image of f₂ over Z |" + (" rank f₂ over F₂ |" if has2 else ""))
    w("|---|---|---|---|" + ("---|" if has2 else ""))
    for k in range(n + 1):
        if k + 4 <= n:
            row = f"| {k} | {R['H1'][k]['group']} | {R['H0'][k + 4]['group']} | {R['f2'][k]['image']} |"
            if has2:
                row += f" {R['fp'][2]['f2_rank'][k]} |"
            w(row)
    w("")
    w("## f₂ in the monomial basis\n")
    w("Every map here preserves the weight grading by the lattice of characters χ: Zⁿ → Z that are constant on the "
      f"monomials of η₁ and η₂ (basis: {R['weight_lattice']}), so H₀, H₁ and f₂ split into weight blocks. "
      "Blocks are labelled by the display characters in `forms.json`; for the default forms these are "
      "δ_b = #{indices among e_{4b−3}, e_{4b−2}} − #{indices among e_{4b−1}, e_{4b}}, b = 1, 2, 3.\n")
    w("Only blocks where H₁ ≠ 0 and the target has 2-torsion can carry a nonzero f₂ (2f₂ = 0). For each such block "
      "the table gives its H₁, the target block of H₀, and the rank of f₂ mod 2.\n")
    ks = sorted({e["k"] for e in R["f2_blocks"]})
    for k in ks:
        bl = [e for e in R["f2_blocks"] if e["k"] == k]
        w(f"### k = {k} → degree {k + 4}\n")
        w("| block | dim Λᵏ block | H₁ block | H₀ block | rank f₂ |")
        w("|---|---|---|---|---|")
        for e in bl:
            w(f"| {e['block']} | {e['dim_block']} | {e['H1_block']} | {e['H0_target_block']} | {e['rank']} |")
        w("")
    w("### Explicit bases and matrices\n")
    w("In each block: H₀ is spanned by the classes of the listed monomials [m₁], [m₂], … (each of order 2), and a Z-basis "
      "z₁, z₂, … of H₁ is given by cycles (a₁, a₂). The line f₂(zⱼ) ≡ … gives the class of a₁γ₂(η₂) − a₂γ₂(η₁) in that basis. "
      "The coordinate of [mᵢ] is the functional λᵢ, which adds up mod 2 the coefficients of the monomials listed for it. "
      "λᵢ vanishes on the ideal and λᵢ(mⱼ) = δᵢⱼ.\n")
    for e in R["f2_blocks"]:
        w(f"#### k = {e['k']}, block {e['block']}: {e['H1_block']} → {e['H0_target_block']}, rank {e['rank']}\n")
        if len(e["cycles"]) > 6:
            w(f"{len(e['cycles'])} cycles (listed in results.json); matrix rank {e['rank']}.\n")
            continue
        w("H₀ basis: " + ", ".join(f"[{g}]" for g in e["H0_generators"]) + "\n")
        for j, z in enumerate(e["cycles"], 1):
            w(f"- z{j}: a₁ = {z['a1']}")
            w(f"  a₂ = {z['a2']}")
            w(f"  f₂(z{j}) ≡ {z['f2_class']}")
        w("\n<details><summary>functionals λᵢ</summary>\n")
        for i, l in enumerate(e["functionals"], 1):
            w(f"- λ{i}: {l}")
        w("\n</details>\n")
    if "fp" in R:
        w("## Checks\n")
        for p, v in R["fp"].items():
            w(f"- F_{p}, ungraded (no weight blocks, no Smith forms), numpy ranks: dim H₀ = {v['H0']}, dim H₁ = {v['H1']}. "
              f"Universal-coefficient prediction from the Z answer: {'agrees' if v['agree'] else 'DISAGREES'}.")
        if isinstance(R.get("flint"), dict):
            w(f"- FLINT (independent SNF/HNF), per block: invariant factors of H₀ and H₁, {len(R['flint']['block_mismatches'])} mismatches; "
              f"log₂ |image f₂| per k, from |coker M| / |coker [M | F·K]| with K from an HNF kernel: {R['flint']['f2_image_log2_order']}.")
        w(f"- Every Smith form carries the certificate U A V = S, U U⁻¹ = I, V V⁻¹ = I, checked exactly. f₂ kills every boundary generator.")
        w(f"- Run time: main {R['main_seconds']} s, checks {R.get('check_seconds')} s.\n")
    with open(path, "w") as fh:
        fh.write("\n".join(L) + "\n")


if __name__ == "__main__":
    main()
