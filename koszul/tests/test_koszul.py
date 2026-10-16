import json
import os
import random
import subprocess
import sys
import tempfile
import unittest
from itertools import combinations

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, ROOT)

import checks  # noqa: E402
from exterior import add, gamma2, mono_mul, monomials, mul, parse  # noqa: E402
from koszul import Computation, Pair, f2_image  # noqa: E402
from zlinalg import smith  # noqa: E402

try:
    import flint
except ImportError:
    flint = None


def parity_sign(s, t):
    seq = s + t
    inv = sum(seq[i] > seq[j] for i in range(len(seq)) for j in range(i + 1, len(seq)))
    return -1 if inv % 2 else 1


def rand_elt(rng, n, k, terms=4):
    out = {}
    mons = monomials(n, k)
    for _ in range(terms):
        out = add(out, {rng.choice(mons): rng.randint(-3, 3)})
    return out


class TestExterior(unittest.TestCase):
    def test_sign_matches_permutation_parity(self):
        rng = random.Random(1)
        for _ in range(2000):
            n = 9
            a = sorted(rng.sample(range(n), rng.randint(0, 4)))
            b = sorted(rng.sample(range(n), rng.randint(0, 4)))
            s, m = mono_mul(sum(1 << i for i in a), sum(1 << i for i in b))
            if set(a) & set(b):
                self.assertEqual(s, 0)
            else:
                self.assertEqual(s, parity_sign(a, b))

    def test_associative_and_graded_commutative(self):
        rng = random.Random(2)
        for _ in range(200):
            p, q, r = rng.randint(0, 3), rng.randint(0, 3), rng.randint(0, 3)
            x, y, z = rand_elt(rng, 8, p), rand_elt(rng, 8, q), rand_elt(rng, 8, r)
            self.assertEqual(mul(mul(x, y), z), mul(x, mul(y, z)))
            yx = mul(y, x)
            self.assertEqual(mul(x, y), {m: c * (-1) ** (p * q) for m, c in yx.items()})

    def test_parse_and_gamma2(self):
        eta = parse("e^1 e^2 + e^3 e^4 + e^5 e^6")
        self.assertEqual(gamma2(eta), parse("e1e2e3e4 + e1e2e5e6 + e3e4e5e6"))
        self.assertEqual(parse("e2 e1"), parse("-e1e2"))


class TestSmith(unittest.TestCase):
    def test_random(self):
        rng = random.Random(3)
        for _ in range(150):
            m, n = rng.randint(0, 7), rng.randint(0, 7)
            r = rng.randint(0, min(m, n))
            # rank-r product of random matrices, entries in a small range
            L = [[rng.randint(-4, 4) for _ in range(r)] for _ in range(m)]
            R = [[rng.randint(-4, 4) for _ in range(n)] for _ in range(r)]
            A = [[sum(L[i][t] * R[t][j] for t in range(r)) for j in range(n)] for i in range(m)]
            s = smith(A, m, n)  # .check() runs inside
            if flint and m and n:
                S = flint.fmpz_mat(m, n, [x for row in A for x in row]).snf()
                theirs = [int(S[i, i]) for i in range(min(m, n)) if S[i, i] != 0]
                self.assertEqual(s.diag, theirs)


class TestKoszulKnownCases(unittest.TestCase):
    def test_symplectic_rank6_with_zero(self):
        # (ω, 0), ω = e1e2+e3e4+e5e6: H_0 = Λ/ωΛ = Z, Z^6, Z^14, Z^14, Z/2 (class of γ_2 ω), 0, 0
        P = Pair(6, parse("e1e2+e3e4+e5e6"), {})
        C = Computation(P)
        h0 = [C.summary(C.H0[d]) for d in range(7)]
        self.assertEqual(h0, [(1, []), (6, []), (14, []), (14, []), (0, [2]), (0, []), (0, [])])
        # H_1^k = H_0^k(ω) ⊕ ker(ω | Λ^k)
        h1 = [C.summary(C.H1[k]) for k in range(7)]
        self.assertEqual(h1, [(1, []), (6, []), (14, []), (28, []), (14, [2]), (6, []), (1, [])])

    def test_one_block_ranks(self):
        # one 4-dim block of the main forms; over Qbar it splits into two rank-2 symplectic pieces
        P = Pair(4, parse("e1e4+e2e3"), parse("e1e3+e2e3+e2e4"))
        C = Computation(P)
        self.assertEqual([C.summary(C.H0[d])[0] for d in range(5)], [1, 4, 4, 0, 0])
        self.assertEqual([C.summary(C.H1[k])[0] for k in range(5)], [0, 4, 10, 4, 0])


class TestMainAndSplitPair(unittest.TestCase):
    def test_split_pair_same_groups_but_f2_zero(self):
        with open(os.path.join(ROOT, "forms.json")) as fh:
            cfg = json.load(fh)
        main = Computation(Pair(12, parse(cfg["eta1"]), parse(cfg["eta2"])))
        split = Computation(Pair(12, parse("e1e2+e3e4+e5e6"), parse("e7e8+e9e10+e11e12")))
        for d in range(13):
            for H in ("H0", "H1"):
                a, b = main.summary(getattr(main, H)[d]), split.summary(getattr(split, H)[d])
                self.assertEqual((a[0], sorted(a[1])), (b[0], sorted(b[1])))
        img = lambda C, k: [s for *_, s in f2_image(C, k) if s != (0, [])]
        self.assertEqual([k for k in range(9) if img(split, k)], [])
        self.assertEqual([k for k in range(9) if img(main, k)], [3])
        self.assertEqual(sorted(q for s in img(main, 3) for q in s[1]), [2] * 16)


class TestLiftsAndEigencycles(unittest.TestCase):
    def comp(self, name):
        with open(os.path.join(ROOT, "lifts", name)) as fh:
            cfg = json.load(fh)
        return Computation(Pair(12, parse(cfg["eta1"]), parse(cfg["eta2"])))

    def image(self, C, k):
        return sorted(q for *_, s in f2_image(C, k) for q in s[1]) + [0] * sum(s[0] for *_, s in f2_image(C, k))

    def test_zeta3_lift_same_answer(self):
        C = self.comp("zeta3.json")
        self.assertEqual([k for k in range(9) if self.image(C, k)], [3])
        self.assertEqual(self.image(C, 3), [2] * 16)

    def test_mixed_lift_f2_zero_over_Z(self):
        C = self.comp("mixed_fib_zeta3.json")
        self.assertEqual(C.summary(C.H1[3]), (0, []))
        self.assertTrue(any(q == 4 for q in C.summary(C.H0[5])[1]))
        self.assertEqual([k for k in range(9) if self.image(C, k)], [])

    def test_eigencycles(self):
        res = subprocess.run([sys.executable, os.path.join(ROOT, "eigencycles.py")], capture_output=True, text=True, cwd=ROOT)
        self.assertEqual(res.returncode, 0, res.stdout + res.stderr)


class TestSymmetry(unittest.TestCase):
    def test_block_swap_preserves_forms(self):
        # e1 -> e4, e2 -> e3, e3 -> -e2, e4 -> -e1 (and the same on the other 4-blocks) fixes η_1 and η_2
        with open(os.path.join(ROOT, "forms.json")) as fh:
            cfg = json.load(fh)
        img = {}
        for b in range(3):
            o = 4 * b
            img.update({o + 1: {1 << (o + 3): 1}, o + 2: {1 << (o + 2): 1}, o + 3: {1 << (o + 1): -1}, o + 4: {1 << o: -1}})

        def sub(a):
            out = {}
            for m, c in a.items():
                t = {0: c}
                for i in range(12):
                    if m >> i & 1:
                        t = mul(t, img[i + 1])
                out = add(out, t)
            return out

        for key in ("eta1", "eta2"):
            f = parse(cfg[key])
            self.assertEqual(sub(f), f)


class TestRandomConsistency(unittest.TestCase):
    """Integral block computation vs ungraded F_p ranks (universal coefficients) and FLINT."""

    def run_pair(self, n, eta1, eta2):
        P = Pair(n, eta1, eta2)
        C = Computation(P)
        for k in range(n + 1):
            f2_image(C, k)  # asserts f_2 kills boundaries
        L, mats = checks.ungraded(P)
        for p in (2, 3, 5):
            h0, h1, _ = checks.fp_dims(P, p, L, mats, with_f2=False)
            self.assertEqual((h0, h1), checks.uct_prediction(C, p))
        if flint:
            mism, _, _ = checks.flint_blocks(C)
            self.assertEqual(mism, [])

    def test_random_pairs(self):
        rng = random.Random(4)
        pairs2 = list(combinations(range(1, 8), 2))
        for trial in range(6):
            n = 7
            forms = []
            for _ in range(2):
                terms = rng.sample(pairs2, rng.randint(2, 6))
                forms.append(parse(" + ".join(f"{rng.choice([1, 1, 2, 3])} e{i}e{j}" for i, j in terms)))
            self.run_pair(n, *forms)

    def test_sparse_graded_pair(self):
        self.run_pair(8, parse("e1e4+e2e3+e5e8+e6e7"), parse("e1e3+e2e3+e2e4+e5e7+e6e7+e6e8"))


class TestCertificateVerifier(unittest.TestCase):
    def test_verifier_rejects_tampering(self):
        path = os.path.join(ROOT, "results", "certificate.json")
        if not os.path.exists(path):
            self.skipTest("run run.py first")
        ok = subprocess.run([sys.executable, os.path.join(ROOT, "verify_certificate.py"), path], capture_output=True, text=True)
        self.assertEqual(ok.returncode, 0, ok.stdout + ok.stderr)
        with open(path) as fh:
            cert = json.load(fh)
        # tamper 1: change one cycle coefficient -> no longer a cycle
        bad = json.loads(json.dumps(cert))
        bad["cycles"][0]["a1"][0][1] += 1
        # tamper 2: drop a monomial from a functional -> it no longer kills the ideal (or the matrix degenerates)
        bad2 = json.loads(json.dumps(cert))
        bad2["functionals"][0]["coeffs"].pop()
        # tamper 3: replace the second form by the first
        bad3 = json.loads(json.dumps(cert))
        bad3["eta2"] = bad3["eta1"]
        for b in (bad, bad2, bad3):
            with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as fh:
                json.dump(b, fh)
            res = subprocess.run([sys.executable, os.path.join(ROOT, "verify_certificate.py"), fh.name], capture_output=True, text=True)
            os.unlink(fh.name)
            self.assertNotEqual(res.returncode, 0)


if __name__ == "__main__":
    unittest.main()
