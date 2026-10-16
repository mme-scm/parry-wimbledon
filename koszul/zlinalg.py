"""Exact integer linear algebra on dense list-of-rows matrices of Python ints.

Every Smith form is returned with transforms and inverses, and is checked:
U A V = S, U Ui = I, V Vi = I (so U, V are unimodular), S diagonal with
s_1 | s_2 | ... | s_r, s_i > 0.
"""


def zeros(m, n):
    return [[0] * n for _ in range(m)]


def eye(n):
    I = zeros(n, n)
    for i in range(n):
        I[i][i] = 1
    return I


def matmul(A, B):
    if not A:
        return []
    n = len(B[0]) if B else 0
    out = []
    for row in A:
        r = [0] * n
        for k, a in enumerate(row):
            if a:
                for j, b in enumerate(B[k]):
                    if b:
                        r[j] += a * b
        out.append(r)
    return out


def matvec(A, x):
    return [sum(a * b for a, b in zip(row, x) if a) for row in A]


def transpose(A, ncols=None):
    if not A:
        return [[] for _ in range(ncols or 0)]
    return [list(c) for c in zip(*A)]


def hstack(*Ms):
    m = len(Ms[0])
    return [sum((M[i] for M in Ms), []) for i in range(m)]


def vstack(*Ms):
    return [list(r) for M in Ms for r in M]


class Smith:
    """U A V = S with S = diag(s_0, ..., s_{r-1}, 0, ...)."""

    def __init__(self, A, m, n):
        self.m, self.n = m, n
        A = [list(r) for r in A]
        U, Ui, V, Vi = eye(m), eye(m), eye(n), eye(n)

        def row_add(i, t, q):  # row_i += q row_t
            if q:
                A[i] = [a + q * b for a, b in zip(A[i], A[t])]
                U[i] = [a + q * b for a, b in zip(U[i], U[t])]
                for r in Ui:  # Ui <- Ui (I - q E_it): col_t -= q col_i
                    if r[i]:
                        r[t] -= q * r[i]

        def col_add(j, t, q):  # col_j += q col_t
            if q:
                for r in A:
                    if r[t]:
                        r[j] += q * r[t]
                for r in V:
                    if r[t]:
                        r[j] += q * r[t]
                Vi[t] = [a - q * b for a, b in zip(Vi[t], Vi[j])]  # Vi <- (I - q E_tj) Vi

        def row_swap(i, j):
            if i != j:
                A[i], A[j] = A[j], A[i]
                U[i], U[j] = U[j], U[i]
                for r in Ui:
                    r[i], r[j] = r[j], r[i]

        def col_swap(i, j):
            if i != j:
                for M in (A, V):
                    for r in M:
                        r[i], r[j] = r[j], r[i]
                Vi[i], Vi[j] = Vi[j], Vi[i]

        def row_neg(i):
            A[i] = [-a for a in A[i]]
            U[i] = [-a for a in U[i]]
            for r in Ui:
                r[i] = -r[i]

        t = 0
        diag = []
        while t < min(m, n):
            best = None
            for i in range(t, m):
                for j in range(t, n):
                    a = A[i][j]
                    if a and (best is None or abs(a) < best[0]):
                        best = (abs(a), i, j)
                        if best[0] == 1:
                            break
                if best and best[0] == 1:
                    break
            if best is None:
                break
            _, i, j = best
            row_swap(t, i)
            col_swap(t, j)
            while True:
                p = A[t][t]
                done = True
                for i in range(t + 1, m):
                    if A[i][t]:
                        row_add(i, t, -(A[i][t] // p))
                        if A[i][t]:
                            done = False
                for j in range(t + 1, n):
                    if A[t][j]:
                        col_add(j, t, -(A[t][j] // p))
                        if A[t][j]:
                            done = False
                if not done:
                    # move the smallest nonzero remainder in row/col t to the pivot
                    cand = [(abs(A[i][t]), i, t) for i in range(t + 1, m) if A[i][t]]
                    cand += [(abs(A[t][j]), t, j) for j in range(t + 1, n) if A[t][j]]
                    _, i, j = min(cand)
                    row_swap(t, i)
                    col_swap(t, j)
                    continue
                # divisibility of the remaining block by the pivot
                bad = None
                for i in range(t + 1, m):
                    for j in range(t + 1, n):
                        if A[i][j] % p:
                            bad = i
                            break
                    if bad is not None:
                        break
                if bad is None:
                    break
                row_add(t, bad, 1)
            if A[t][t] < 0:
                row_neg(t)
            diag.append(A[t][t])
            t += 1
        self.S = A
        self.U, self.Ui, self.V, self.Vi = U, Ui, V, Vi
        self.diag = diag
        self.rank = len(diag)

    def check(self, A0):
        m, n = self.m, self.n
        assert matmul(matmul(self.U, A0), self.V) == self.S if m and n else True
        assert matmul(self.U, self.Ui) == eye(m)
        assert matmul(self.V, self.Vi) == eye(n)
        for i in range(m):
            for j in range(n):
                want = self.diag[i] if (i == j and i < self.rank) else 0
                assert self.S[i][j] == want
        for a, b in zip(self.diag, self.diag[1:]):
            assert a > 0 and b % a == 0
        return True


def smith(A, m, n, check=True):
    s = Smith(A, m, n)
    if check:
        s.check(A)
    return s


def rank_mod_p(A, p):
    """Rank over F_p of an integer matrix given as a numpy array or list of rows."""
    import numpy as np

    M = np.array(A, dtype=np.int64) % p
    if M.size == 0:
        return 0
    m, n = M.shape
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
        inv = pow(int(M[r, c]), -1, p)
        M[r] = (M[r] * inv) % p
        rows = np.nonzero(M[:, c])[0]
        rows = rows[rows != r]
        if rows.size:
            M[rows] = (M[rows] - np.outer(M[rows, c], M[r])) % p
        r += 1
    return r


def nullspace_mod_p(A, p, ncols):
    """Basis (list of vectors) of {x in F_p^ncols : A x = 0}."""
    m = len(A)
    M = [[a % p for a in row] for row in A]
    pivots = []
    r = 0
    for c in range(ncols):
        piv = next((i for i in range(r, m) if M[i][c]), None)
        if piv is None:
            continue
        M[r], M[piv] = M[piv], M[r]
        inv = pow(M[r][c], -1, p)
        M[r] = [(a * inv) % p for a in M[r]]
        for i in range(m):
            if i != r and M[i][c]:
                f = M[i][c]
                M[i] = [(a - f * b) % p for a, b in zip(M[i], M[r])]
        pivots.append(c)
        r += 1
    free = [c for c in range(ncols) if c not in set(pivots)]
    basis = []
    for f in free:
        x = [0] * ncols
        x[f] = 1
        for i, c in enumerate(pivots):
            x[c] = (-M[i][f]) % p
        basis.append(x)
    return basis
