#!/usr/bin/env python3
"""Standalone verifier for results/certificate.json.  Shares no code with the rest of the package.

The certificate lists integral cycles z_j = (a_1, a_2) ∈ (Λ^k Z^n)^2 and functionals
λ_i: Λ^{k+4} Z^n -> Z/2 (given by integer coefficients on monomials).  It checks:
  (1) a_1 η_2 - a_2 η_1 = 0 in Λ(Z^n) for every z_j            (z_j is a cycle over Z);
  (2) λ_i(u η_1) ≡ λ_i(u η_2) ≡ 0 mod 2 for every monomial u of
      degree k+2                                                (λ_i kills the ideal (η_1, η_2));
  (3) the matrix A_ij = λ_i(a_1 γ_2(η_2) - a_2 γ_2(η_1)) mod 2 is invertible over F_2.
By (2) each λ_i factors through H_0^{k+4}(Z) = Λ^{k+4}/(η_1, η_2), so (1) and (3) show that
f_2(z_1), ..., f_2(z_r) are F_2-linearly independent in H_0^{k+4}(Z)/2.  Hence f_2 ≠ 0 over Z,
and its image on H_1^k contains an elementary abelian 2-group of rank r (2 f_2 = 0 always).
Usage: python verify_certificate.py [results/certificate.json]
"""
import json
import re
import sys
from itertools import combinations


def mono_mul(s, t):
    """Product of sorted index tuples s, t: (sign, sorted tuple) or (0, None)."""
    if set(s) & set(t):
        return 0, None
    seq = list(s) + list(t)
    inversions = sum(1 for i in range(len(seq)) for j in range(i + 1, len(seq)) if seq[i] > seq[j])
    return (-1) ** inversions, tuple(sorted(seq))


def mul(a, b):
    out = {}
    for s, c in a.items():
        for t, d in b.items():
            sg, m = mono_mul(s, t)
            if sg:
                out[m] = out.get(m, 0) + sg * c * d
    return {m: c for m, c in out.items() if c}


def lin(*pairs):
    out = {}
    for coef, a in pairs:
        for m, c in a.items():
            out[m] = out.get(m, 0) + coef * c
    return {m: c for m, c in out.items() if c}


def parse(s):
    out = {}
    for sign, coef, gens in re.findall(r"([+-]?)\s*(\d*)\s*((?:e\^?\{?\d+\}?\s*)+)", s):
        idx = [int(i) for i in re.findall(r"e\^?\{?(\d+)\}?", gens)]
        c = (-1 if sign == "-" else 1) * (int(coef) if coef else 1)
        out = lin((1, out), (c, mul({(): 1}, mul_list(idx))))
    return out


def mul_list(idx):
    a = {(): 1}
    for i in idx:
        a = mul(a, {(i,): 1})
    return a


def gamma2(eta):
    terms = sorted(eta.items())
    g = {}
    for (s, c), (t, d) in combinations(terms, 2):
        sg, m = mono_mul(s, t)
        if sg:
            g[m] = g.get(m, 0) + sg * c * d
    g = {m: c for m, c in g.items() if c}
    assert lin((2, g)) == mul(eta, eta), "2 gamma_2(eta) != eta^2"
    return g


def elt(terms):
    return lin(*[(c, {tuple(sorted(m)): 1}) for m, c in terms]) if terms else {}


def rank_f2(A):
    A = [list(r) for r in A]
    r = 0
    for c in range(len(A[0]) if A else 0):
        piv = next((i for i in range(r, len(A)) if A[i][c] % 2), None)
        if piv is None:
            continue
        A[r], A[piv] = A[piv], A[r]
        for i in range(len(A)):
            if i != r and A[i][c] % 2:
                A[i] = [(x + y) % 2 for x, y in zip(A[i], A[r])]
        r += 1
    return r


def main(path):
    cert = json.load(open(path))
    n, k = cert["n"], cert["k"]
    eta1, eta2 = parse(cert["eta1"]), parse(cert["eta2"])
    g1, g2 = gamma2(eta1), gamma2(eta2)
    cycles = [(elt(z["a1"]), elt(z["a2"])) for z in cert["cycles"]]
    lams = [{tuple(sorted(m)): c for m, c in f["coeffs"]} for f in cert["functionals"]]
    assert all(f["modulus"] == 2 for f in cert["functionals"])
    ev = lambda lam, x: sum(lam.get(m, 0) * c for m, c in x.items()) % 2

    for a1, a2 in cycles:
        assert all(len(m) == k for m in list(a1) + list(a2))
        assert lin((1, mul(a1, eta2)), (-1, mul(a2, eta1))) == {}, "not a cycle"
    print(f"(1) {len(cycles)} cycles in degree {k}: a1 η2 - a2 η1 = 0 over Z")

    us = [{m: 1} for m in combinations(range(1, n + 1), k + 2)]
    prods = [mul(u, e) for u in us for e in (eta1, eta2)]
    for lam in lams:
        assert all(len(m) == k + 4 for m in lam)
        assert all(ev(lam, p) == 0 for p in prods), "functional does not kill the ideal"
    print(f"(2) {len(lams)} functionals on Λ^{k + 4} vanish mod 2 on η_i·u for all {len(us)} monomials u of degree {k + 2}")

    f2 = [lin((1, mul(a1, g2)), (-1, mul(a2, g1))) for a1, a2 in cycles]
    A = [[ev(lam, f) for f in f2] for lam in lams]
    r = rank_f2(A)
    print(f"(3) rank over F_2 of [λ_i(f_2(z_j))] = {r} (matrix is {len(lams)} x {len(cycles)})")
    assert r == len(cycles) == len(lams), "matrix not invertible"
    print(f"VERIFIED: f_2 ≠ 0 over Z; its image on H_1^{k} contains (Z/2)^{r}.")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "results/certificate.json")
