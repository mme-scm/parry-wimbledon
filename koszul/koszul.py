"""Koszul homology of a pair of 2-forms on Λ(Z^n) and the map f_2: H_1 -> H_0.

Gradings.  a = (a_1, a_2) is in degree k if a_i ∈ Λ^k.  Then
  H_1^k = ker(D_k: (Λ^k)^2 -> Λ^{k+2}, (a_1,a_2) |-> a_1 η_2 - a_2 η_1)
          / im(E_k: Λ^{k-2} -> (Λ^k)^2, b |-> (b η_1, b η_2)),
  H_0^d = coker(M_d: (Λ^{d-2})^2 -> Λ^d, (u,v) |-> u η_1 + v η_2),
  f_2: H_1^k -> H_0^{k+4},  (a_1,a_2) |-> a_1 γ_2(η_2) - a_2 γ_2(η_1).

Every map above is homogeneous for any weight χ: Z^n -> Z under which all
monomials of η_1 and η_2 have the same weight (γ_2(η_i) then has twice that
weight).  We compute the lattice of such χ and split each graded piece into
weight blocks.  This is an exact block decomposition of every matrix; the
ungraded F_p computations in checks.py verify it independently.
"""
from collections import Counter, defaultdict
from functools import lru_cache

from exterior import gamma2, is_homogeneous, mono_mul, monomials
from zlinalg import smith, vstack, hstack, matvec, matmul


def weight_lattice(n, forms):
    """Z-basis of {χ ∈ Z^n : χ(m) is the same for every monomial m of every form}."""
    mons = sorted({m for f in forms for m in f})
    vec = lambda m: [(m >> i) & 1 for i in range(n)]
    m0 = vec(mons[0])
    C = [[a - b for a, b in zip(vec(m), m0)] for m in mons[1:]]
    if not C:
        C = [[0] * n]
    s = smith(C, len(C), n)
    return [[s.V[i][j] for i in range(n)] for j in range(s.rank, n)]


class Pair:
    def __init__(self, n, eta1, eta2):
        assert is_homogeneous(eta1, 2) and is_homogeneous(eta2, 2)
        self.n, self.eta1, self.eta2 = n, eta1, eta2
        self.g1, self.g2 = gamma2(eta1), gamma2(eta2)
        self.chi = weight_lattice(n, [eta1, eta2])
        self.c = self.weight(next(iter(eta1)))
        for f in (eta1, eta2):
            assert all(self.weight(m) == self.c for m in f)
        for f in (self.g1, self.g2):
            assert all(self.weight(m) == self.shift(self.c) for m in f)
        self.blocks = []  # blocks[k] = {weight: [masks]}
        for k in range(n + 1):
            b = defaultdict(list)
            for m in monomials(n, k):
                b[self.weight(m)].append(m)
            self.blocks.append(dict(b))

    def weight(self, m):
        return tuple(sum(ch[i] for i in range(self.n) if m >> i & 1) for ch in self.chi)

    def shift(self, w, t=1):
        return tuple(a + t * b for a, b in zip(w, self.c))

    def block(self, k, w):
        if 0 <= k <= self.n:
            return self.blocks[k].get(w, [])
        return []

    def mult(self, form, src, tgt):
        """Matrix (rows = tgt monomials, cols = src monomials) of x |-> x ∧ form."""
        idx = {m: i for i, m in enumerate(tgt)}
        A = [[0] * len(src) for _ in tgt]
        for j, m in enumerate(src):
            for fm, c in form.items():
                s, p = mono_mul(m, fm)
                if s:
                    A[idx[p]][j] += s * c
        return A


def _neg(A):
    return [[-a for a in r] for r in A]


class BlockH0:
    """H_0 in degree d, weight w: coker M, M = [η_1 | η_2] : (Λ^{d-2}_{w-c})^2 -> Λ^d_w."""

    def __init__(self, P, d, w):
        self.d, self.w = d, w
        self.tgt = P.block(d, w)
        self.src = P.block(d - 2, P.shift(w, -1))
        m, s = len(self.tgt), len(self.src)
        self.M = hstack(P.mult(P.eta1, self.src, self.tgt), P.mult(P.eta2, self.src, self.tgt)) if s else [[] for _ in range(m)]
        self.S = smith(self.M, m, 2 * s)
        # coker ≅ ⊕_{i<rank} Z/diag[i] ⊕ Z^{m-rank}; coordinates y = U x
        self.orders = self.S.diag + [0] * (m - self.S.rank)  # 0 means Z

    def coords(self, x):
        """Class of x ∈ Λ^d_w (vector in tgt basis) in coker coordinates, reduced."""
        y = matvec(self.S.U, x)
        return [yi % o if o else yi for yi, o in zip(y, self.orders)]

    def generator(self, i):
        """Representative in Λ^d_w of the i-th cyclic generator (column i of U^{-1})."""
        return [row[i] for row in self.S.Ui]


class BlockH1:
    """H_1 in a-degree k, weight w (a_i ∈ Λ^k_w)."""

    def __init__(self, P, k, w):
        self.k, self.w = k, w
        self.basis = P.block(k, w)
        self.b_src = P.block(k - 2, P.shift(w, -1))
        self.d_tgt = P.block(k + 2, P.shift(w, 1))
        self.f_tgt = P.block(k + 4, P.shift(w, 2))
        nb = len(self.basis)
        N = 2 * nb
        # D (a_1, a_2) = a_1 η_2 - a_2 η_1
        if self.d_tgt:
            D = hstack(P.mult(P.eta2, self.basis, self.d_tgt), _neg(P.mult(P.eta1, self.basis, self.d_tgt)))
        else:
            D = []
        # E b = (b η_1, b η_2)
        if self.b_src:
            E = vstack(P.mult(P.eta1, self.b_src, self.basis), P.mult(P.eta2, self.b_src, self.basis))
        else:
            E = [[] for _ in range(N)]
        self.D, self.E = D, E
        if D:
            sD = smith(D, len(D), N)
            r = sD.rank
            K = [row[r:] for row in sD.V]  # N x (N-r), saturated basis of ker D
            self.Kc = sD.Vi[r:]  # cycle v = K (Kc v)
            KiE = matmul([row for row in sD.Vi[r:]], E) if self.b_src else [[] for _ in range(N - r)]
            assert all(not any(row) for row in matmul(sD.Vi[:r], E)) if self.b_src else True
        else:
            r = 0
            K = [[int(i == j) for j in range(N)] for i in range(N)]
            self.Kc = K
            KiE = E
        self.K = K
        self.zrank = N - r
        assert all(not any(v) for v in matmul(D, K)) if D and K and K[0] else True
        # X: coordinates of im E in the basis K.  H_1 = Z^{zrank} / X Z^{|b_src|}
        X = KiE
        self.sX = smith(X, self.zrank, len(self.b_src))
        self.orders = self.sX.diag + [0] * (self.zrank - self.sX.rank)
        # generators: columns of K Ux^{-1}
        self.G = matmul(K, self.sX.Ui) if self.zrank else [[] for _ in range(N)]
        self.F = None
        if self.f_tgt:
            self.F = hstack(P.mult(P.g2, self.basis, self.f_tgt), _neg(P.mult(P.g1, self.basis, self.f_tgt)))

    def generator(self, i):
        v = [row[i] for row in self.G]
        nb = len(self.basis)
        return v[:nb], v[nb:]

    def nontrivial(self):
        return [i for i, o in enumerate(self.orders) if o != 1]


def group_str(free, torsion):
    parts = []
    if free:
        parts.append("Z" if free == 1 else f"Z^{free}")
    for q, mult in sorted(Counter(torsion).items()):
        parts.append(f"(Z/{q})" + (f"^{mult}" if mult > 1 else ""))
    return " ⊕ ".join(parts) if parts else "0"


def primary(torsion):
    out = Counter()
    for q in torsion:
        x, p = q, 2
        while x > 1:
            e = 0
            while x % p == 0:
                x //= p
                e += 1
            if e:
                out[p**e] += 1
            p += 1
    return out


class Computation:
    def __init__(self, P):
        self.P = P
        n = P.n
        self.H0 = {d: [BlockH0(P, d, w) for w in sorted(P.blocks[d])] for d in range(n + 1)}
        self.H1 = {k: [BlockH1(P, k, w) for w in sorted(P.blocks[k])] for k in range(n + 1)}
        self.H0index = {(b.d, b.w): b for d in self.H0 for b in self.H0[d]}

    @staticmethod
    def summary(blocks):
        free = sum(o == 0 for b in blocks for o in b.orders)
        tors = [o for b in blocks for o in b.orders if o > 1]
        return free, tors

    def f2_block(self, b1):
        """f_2 on block b1: list of (generator index, order, image coords in H_0 block) for nontrivial gens."""
        if b1.F is None:
            return None, []
        b0 = self.H0index[(b1.k + 4, self.P.shift(b1.w, 2))]
        out = []
        for i in range(len(b1.orders)):
            a1, a2 = b1.generator(i)
            y = b0.coords(matvec(b1.F, a1 + a2))
            if b1.orders[i] == 1:
                assert not any(y[j] for j in range(len(y))), "boundary with nonzero f_2"
                continue
            out.append((i, b1.orders[i], y))
        return b0, out


def subgroup_structure(Y, orders):
    """Structure of the subgroup of G = ⊕_j Z/orders[j] (0 = Z) generated by the columns of Y.

    Returns (free_rank, torsion invariant factors > 1).  The relation lattice
    {x : Y x ∈ ⊕ orders[j] Z} is the projection of ker [Y | diag(orders)].
    """
    r = len(orders)
    g = len(Y[0]) if Y else 0
    if g == 0:
        return 0, []
    A = [list(Y[j]) + [orders[j] if i == j else 0 for i in range(r)] for j in range(r)]
    s = smith(A, r, g + r)
    rel = [[s.V[i][c] for c in range(s.rank, g + r)] for i in range(g)]  # g x (#kernel vectors)
    t = smith(rel, g, len(rel[0]) if rel and rel[0] else 0)
    return g - t.rank, [q for q in t.diag if q > 1]


def f2_image(C, k):
    """Per-block image of f_2 on H_1^k: list of (b1, b0, Y, (free, torsion))."""
    out = []
    for b1 in C.H1[k]:
        if b1.F is None or not b1.orders:
            continue
        b0 = C.H0index[(k + 4, C.P.shift(b1.w, 2))]
        Y = [[] for _ in b0.orders]
        for i in range(len(b1.orders)):
            a1, a2 = b1.generator(i)
            y = b0.coords(matvec(b1.F, a1 + a2))
            if b1.orders[i] == 1:  # boundary: f_2 must vanish (well-definedness)
                assert not any(y), "boundary with nonzero f_2"
            for j, v in enumerate(y):
                Y[j].append(v)
        out.append((b1, b0, Y, subgroup_structure(Y, b0.orders)))
    return out
