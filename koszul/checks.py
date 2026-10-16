"""Independent checks of the integral computation in koszul.py.

1. Ungraded F_p (numpy, no weight blocks, no Smith forms): dim H_0(F_p)^d,
   dim H_1(F_p)^k, and rank of f_2 over F_p, compared with the universal
   coefficient prediction from the integral answer:
     dim H_0(F_p)^d = rank H_0^d + #{invariant factors of H_0^d divisible by p}
     dim H_1(F_p)^k = rank H_1^k + #{... of H_1^k ...} + #{... of H_0^{k+2} ...}.
2. FLINT (python-flint): per block, invariant factors of H_0 and of H_1
   (torsion H_1 = torsion coker E since Z_1 is saturated), and the order of
   the image of f_2, |coker M| / |coker [M | F K]|, with K a Z-basis of ker D
   taken from the HNF of [D^T | I] (independent of zlinalg).
"""
from collections import Counter

import numpy as np

from exterior import monomials
from koszul import _neg
from zlinalg import hstack, vstack


def rref_mod_p(A, p):
    M = np.array(A, dtype=np.int64).reshape(len(A), -1) % p
    m, n = M.shape
    pivots = []
    r = 0
    for c in range(n):
        if r == m:
            break
        nz = np.nonzero(M[r:, c])[0]
        if nz.size == 0:
            continue
        piv = r + nz[0]
        if piv != r:
            M[[r, piv]] = M[[piv, r]]
        M[r] = (M[r] * pow(int(M[r, c]), -1, p)) % p
        rows = np.nonzero(M[:, c])[0]
        rows = rows[rows != r]
        if rows.size:
            M[rows] = (M[rows] - np.outer(M[rows, c], M[r])) % p
        pivots.append(c)
        r += 1
    return M[:r], pivots


def rank_p(A, p):
    if not A or not A[0]:
        return 0
    return len(rref_mod_p(A, p)[1])


def nullspace_p(A, p, n):
    """Columns (n x dim) spanning {x : A x = 0 mod p}."""
    if not A:
        return np.eye(n, dtype=np.int64)
    R, piv = rref_mod_p(A, p)
    free = [c for c in range(n) if c not in set(piv)]
    N = np.zeros((n, len(free)), dtype=np.int64)
    for t, f in enumerate(free):
        N[f, t] = 1
        for i, c in enumerate(piv):
            N[c, t] = (-R[i, f]) % p
    return N


def ungraded(P):
    """Full (ungraded) matrices M_d, D_k, E_k, F_k."""
    n = P.n
    L = [monomials(n, k) for k in range(n + 1)]
    get = lambda k: L[k] if 0 <= k <= n else []
    mats = {}
    for d in range(n + 1):
        tgt, src = get(d), get(d - 2)
        mats["M", d] = hstack(P.mult(P.eta1, src, tgt), P.mult(P.eta2, src, tgt)) if src else []
    for k in range(n + 1):
        a, t2, b, t4 = get(k), get(k + 2), get(k - 2), get(k + 4)
        mats["D", k] = hstack(P.mult(P.eta2, a, t2), _neg(P.mult(P.eta1, a, t2))) if t2 else []
        mats["E", k] = vstack(P.mult(P.eta1, b, a), P.mult(P.eta2, b, a)) if b else []
        mats["F", k] = hstack(P.mult(P.g2, a, t4), _neg(P.mult(P.g1, a, t4))) if t4 else []
    return L, mats


def fp_dims(P, p, L, mats, with_f2):
    n = P.n
    h0 = [len(L[d]) - rank_p(mats["M", d], p) for d in range(n + 1)]
    h1, f2 = [], []
    for k in range(n + 1):
        N1 = 2 * len(L[k])
        rD = rank_p(mats["D", k], p)
        h1.append(N1 - rD - rank_p(mats["E", k], p))
        if with_f2 and mats["F", k] and h1[-1]:
            Z = nullspace_p(mats["D", k], p, N1)
            FZ = (np.array(mats["F", k], dtype=np.int64) % p) @ Z % p
            Mk = np.array(mats["M", k + 4], dtype=np.int64).reshape(len(L[k + 4]), -1) if mats["M", k + 4] else np.zeros((len(L[k + 4]), 0), dtype=np.int64)
            both = np.hstack([Mk % p, FZ]).tolist()
            f2.append(rank_p(both, p) - rank_p(Mk.tolist(), p))
        else:
            f2.append(0)
    return h0, h1, f2


def uct_prediction(C, p):
    n = C.P.n
    h0, h1 = [], []
    for d in range(n + 1):
        free, tors = C.summary(C.H0[d])
        h0.append(free + sum(q % p == 0 for q in tors))
    for k in range(n + 1):
        free, tors = C.summary(C.H1[k])
        extra = sum(q % p == 0 for q in C.summary(C.H0[k + 2])[1]) if k + 2 <= n else 0
        h1.append(free + sum(q % p == 0 for q in tors) + extra)
    return h0, h1


def flint_blocks(C):
    """Cross-check every block's invariant factors with FLINT; return f_2 image orders per k."""
    import flint

    def snf_diag(A, m, n):
        if m == 0 or n == 0:
            return []
        S = flint.fmpz_mat(m, n, [x for r in A for x in r]).snf()
        return [int(S[i, i]) for i in range(min(m, n)) if S[i, i] != 0]

    def int_kernel(D, m, n):
        """Z-basis (list of vectors) of ker D via HNF of [D^T | I_n]."""
        if m == 0:
            return [[int(i == j) for j in range(n)] for i in range(n)]
        aug = [[D[i][j] for i in range(m)] + [int(j == t) for t in range(n)] for j in range(n)]
        H = flint.fmpz_mat(n, m + n, [x for r in aug for x in r]).hnf()
        out = []
        for i in range(n):
            if all(H[i, j] == 0 for j in range(m)):
                out.append([int(H[i, m + t]) for t in range(n)])
        assert len(out) == n - flint.fmpz_mat(m, n, [x for r in D for x in r]).rank()
        return out

    mismatches = []
    for d, blocks in C.H0.items():
        for b in blocks:
            diag = snf_diag(b.M, len(b.tgt), 2 * len(b.src))
            mine = sorted(q for q in b.orders if q > 1)
            theirs = sorted(q for q in diag if q > 1)
            if mine != theirs or len(b.tgt) - len(diag) != sum(o == 0 for o in b.orders):
                mismatches.append(("H0", d, b.w))
    image_log2 = Counter()
    image_odd = Counter()
    for k, blocks in C.H1.items():
        for b in blocks:
            N = 2 * len(b.basis)
            K = int_kernel(b.D, len(b.D), N) if b.D else [[int(i == j) for j in range(N)] for i in range(N)]
            rE = len(snf_diag(b.E, N, len(b.b_src))) if b.b_src else 0
            tors = sorted(q for q in (snf_diag(b.E, N, len(b.b_src)) if b.b_src else []) if q > 1)
            free = len(K) - rE
            mine = sorted(q for q in b.orders if q > 1)
            if mine != tors or free != sum(o == 0 for o in b.orders):
                mismatches.append(("H1", k, b.w))
            if b.F is None or not K:
                continue
            b0 = C.H0index[(k + 4, C.P.shift(b.w, 2))]
            if any(o == 0 for o in b0.orders):
                continue  # only finite targets are needed here
            FK = [[sum(f * x for f, x in zip(row, v)) for v in K] for row in b.F]
            m0 = len(b0.tgt)
            before = snf_diag(b0.M, m0, len(b0.M[0]) if b0.M and b0.M[0] else 0)
            after = snf_diag([r1 + r2 for r1, r2 in zip(b0.M, FK)] if b0.M and b0.M[0] else FK, m0, (len(b0.M[0]) if b0.M and b0.M[0] else 0) + len(K))
            prod = lambda xs: __import__("math").prod(xs)
            order = prod(before) // prod(after)
            assert prod(before) % prod(after) == 0
            v = 0
            while order % 2 == 0:
                order //= 2
                v += 1
            image_log2[k] += v
            image_odd[k] = max(image_odd[k], order)
    return mismatches, image_log2, image_odd
