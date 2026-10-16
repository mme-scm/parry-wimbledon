#!/usr/bin/env python3
"""Check the eigen-cycle description of H_1^3 and f_2 for the default (Fibonacci) forms, over Z[φ], φ² = φ + 1.

In block b put ℓx_b = e_{4b-3} + φ e_{4b-2}, ℓy_b = e_{4b-1} - φ̄ e_{4b} (φ̄ = 1 - φ).  Checks:
  (1) η_2 - φ̄ η_1 = Σ_b ℓx_b ℓy_b  (each block part is decomposable);
  (2) for each of the 8 choices c = ℓ_1 ℓ_2 ℓ_3, ℓ_b ∈ {ℓx_b, ℓy_b}: z = (c, φ̄ c) is a cycle,
      f_2(z) = c γ_2(η_1) exactly, and its class in H_0^7 ⊗ F_4 is nonzero;
  (3) c = ℓx_1 (p_2 - p_3), p_b = ℓx_b ℓy_b, gives a cycle with f_2(z) = 0 in H_0^7;
  (4) writing ℓx_1 ℓx_2 ℓx_3 = c_0 + φ c_1, (c_0, c_0 - c_1) and (c_1, -c_0) are integral cycles;
  (5) f_2[a] = [a_1 γ_2(η_1)] for every generator a of H_1^3 over Z.
"""
import json
import os
from itertools import product

from exterior import add, mono_mul, mul, parse, to_str
from koszul import Computation, Pair
from zlinalg import matvec, nullspace_mod_p

HERE = os.path.dirname(os.path.abspath(__file__))
Z0 = (0, 0)


def pm(x, y):  # (a + bφ)(c + dφ)
    return (x[0] * y[0] + x[1] * y[1], x[0] * y[1] + x[1] * y[0] + x[1] * y[1])


def emul(A, B):
    out = {}
    for m1, c1 in A.items():
        for m2, c2 in B.items():
            s, m = mono_mul(m1, m2)
            if s:
                v = pm(c1, c2)
                o = out.get(m, Z0)
                out[m] = (o[0] + s * v[0], o[1] + s * v[1])
    return {m: c for m, c in out.items() if c != Z0}


def eadd(A, B, s=(1, 0)):
    out = dict(A)
    for m, c in B.items():
        v, o = pm(s, c), out.get(m, Z0)
        out[m] = (o[0] + v[0], o[1] + v[1])
    return {m: c for m, c in out.items() if c != Z0}


def main():
    with open(os.path.join(HERE, "forms.json")) as fh:
        cfg = json.load(fh)
    eta1, eta2 = parse(cfg["eta1"]), parse(cfg["eta2"])
    P = Pair(12, eta1, eta2)
    C = Computation(P)
    lift = lambda a: {m: (c, 0) for m, c in a.items()}
    E1, E2, G1, G2 = lift(eta1), lift(eta2), lift(P.g1), lift(P.g2)
    PHI, PHIB, MINUS = (0, 1), (1, -1), (-1, 0)
    e = lambda i: {1 << (i - 1): (1, 0)}
    lx = [eadd(e(4 * b + 1), {1 << (4 * b + 1): PHI}) for b in range(3)]
    ly = [eadd(e(4 * b + 3), {1 << (4 * b + 3): (-1, 1)}) for b in range(3)]  # -φ̄ = φ - 1
    nu = eadd(E2, eadd({}, E1, PHIB), MINUS)
    assert nu == eadd(eadd(emul(lx[0], ly[0]), emul(lx[1], ly[1])), emul(lx[2], ly[2]))
    print("(1) η2 - φ̄ η1 = Σ_b (e_{4b-3} + φ e_{4b-2})(e_{4b-1} - φ̄ e_{4b})")

    lams = []
    for b0 in C.H0[7]:
        m = len(b0.tgt)
        MT = [[b0.M[i][j] for i in range(m)] for j in range(len(b0.M[0]))]
        lams += [dict(zip(b0.tgt, l)) for l in nullspace_mod_p(MT, 2, m)]

    def nonzero_F4(x):  # class in H_0^7 ⊗ F_4, F_4 = F_2[φ]
        for lam in lams:
            v = [sum(c[t] for mono, c in x.items() if lam.get(mono, 0) % 2) % 2 for t in (0, 1)]
            if any(v):
                return True
        return False

    cycle = lambda a1, a2: eadd(emul(a1, E2), emul(a2, E1), MINUS) == {}
    f2 = lambda a1, a2: eadd(emul(a1, G2), emul(a2, G1), MINUS)
    for choice in product("xy", repeat=3):
        c = {0: (1, 0)}
        for b, t in enumerate(choice):
            c = emul(c, lx[b] if t == "x" else ly[b])
        a2 = eadd({}, c, PHIB)
        F = f2(c, a2)
        assert cycle(c, a2) and F == emul(c, G1) and nonzero_F4(F)
    print("(2) all 8 Lagrangian choices: cycle, f2(z) = c·γ2(η1), class ≠ 0 in H0^7 ⊗ F4")

    p = [emul(lx[b], ly[b]) for b in range(3)]
    c = emul(lx[0], eadd(p[1], p[2], MINUS))
    a2 = eadd({}, c, PHIB)
    assert cycle(c, a2) and not nonzero_F4(f2(c, a2))
    print("(3) c = ℓx1 (p2 - p3): cycle with f2(z) = 0 in H0^7")

    c = emul(emul(lx[0], lx[1]), lx[2])
    c0 = {m: v[0] for m, v in c.items() if v[0]}
    c1 = {m: v[1] for m, v in c.items() if v[1]}
    for b1_, b2_ in ((c0, add(c0, c1, -1)), (c1, {m: -v for m, v in c0.items()})):
        assert add(mul(b1_, eta2), mul(b2_, eta1), -1) == {}
    print(f"(4) c0 = {to_str(c0)}\n    c1 = {to_str(c1)}\n    (c0, c0 - c1) and (c1, -c0) are integral cycles")

    for b1 in C.H1[3]:
        b0 = C.H0index[(7, P.shift(b1.w, 2))]
        for i in range(len(b1.orders)):
            a1, a2 = b1.generator(i)
            A1 = {m: v for m, v in zip(b1.basis, a1) if v}
            diff = add(mul(A1, P.g1), dict(zip(b1.f_tgt, matvec(b1.F, a1 + a2))), -1)
            assert not any(b0.coords([diff.get(m, 0) for m in b0.tgt]))
    print("(5) f2[a] = [a1 γ2(η1)] on every generator of H1^3")


if __name__ == "__main__":
    main()
