"""Exterior algebra Λ(Z^n) with integer coefficients.

A monomial e^{i_1} ... e^{i_k} (i_1 < ... < i_k) is the bitmask with bits i_j - 1 set.
An element is a dict {mask: nonzero int}.
"""
import re
from itertools import combinations


def mono_mul(m1, m2):
    """e^{m1} e^{m2} = sign * e^{m1|m2}; returns (sign, m1|m2), or (0, 0) if they overlap."""
    if m1 & m2:
        return 0, 0
    # sign = (-1)^#{(i, j) : i in m1, j in m2, i > j}
    inv = 0
    x = m2
    while x:
        low = x & -x
        inv += (m1 & ~((low << 1) - 1)).bit_count()
        x ^= low
    return (-1 if inv & 1 else 1), m1 | m2


def mul(a, b):
    out = {}
    for m1, c1 in a.items():
        for m2, c2 in b.items():
            s, m = mono_mul(m1, m2)
            if s:
                out[m] = out.get(m, 0) + s * c1 * c2
    return {m: c for m, c in out.items() if c}


def add(a, b, cb=1):
    out = dict(a)
    for m, c in b.items():
        out[m] = out.get(m, 0) + cb * c
    return {m: c for m, c in out.items() if c}


def reduce_mod(a, p):
    out = {m: c % p for m, c in a.items()}
    return {m: c for m, c in out.items() if c}


def degree(m):
    return m.bit_count()


def is_homogeneous(a, k):
    return all(degree(m) == k for m in a)


def gamma2(eta):
    """Second divided power of a 2-form over Z, defined by 2*gamma2(eta) = eta^2.

    Λ(Z^n) is torsion-free, so this determines gamma2 uniquely; the result is
    cross-checked against sum_{s<t} c_s c_t m_s m_t over the distinct monomials of eta.
    """
    assert is_homogeneous(eta, 2)
    sq = mul(eta, eta)
    assert all(c % 2 == 0 for c in sq.values())
    g = {m: c // 2 for m, c in sq.items()}
    terms = sorted(eta.items())
    g2 = {}
    for (m1, c1), (m2, c2) in combinations(terms, 2):
        s, m = mono_mul(m1, m2)
        if s:
            g2[m] = g2.get(m, 0) + s * c1 * c2
    assert g == {m: c for m, c in g2.items() if c}
    return g


_TERM = re.compile(r"\s*([+-])?\s*(\d+)?\s*\*?\s*((?:e\^?\{?\d+\}?\s*)+)")
_GEN = re.compile(r"e\^?\{?(\d+)\}?")


def parse(s):
    """Parse e.g. 'e^1 e^4 + e^2 e^3 - 2 e5e8' into an element."""
    out = {}
    pos = 0
    s = s.strip()
    while pos < len(s):
        t = _TERM.match(s, pos)
        if not t or t.end() == pos:
            raise ValueError(f"cannot parse at {s[pos:]!r}")
        sign = -1 if t.group(1) == "-" else 1
        coef = int(t.group(2)) if t.group(2) else 1
        elt = {0: sign * coef}
        for i in _GEN.findall(t.group(3)):
            elt = mul(elt, {1 << (int(i) - 1): 1})
        out = add(out, elt)
        pos = t.end()
    return out


def mono_str(m):
    if m == 0:
        return "1"
    return " ".join(f"e{i + 1}" for i in range(m.bit_length()) if m >> i & 1)


def to_str(a):
    if not a:
        return "0"
    parts = []
    for m in sorted(a, key=lambda m: [i for i in range(m.bit_length()) if m >> i & 1]):
        c = a[m]
        sign = "-" if c < 0 else "+"
        mag = "" if abs(c) == 1 and m else f"{abs(c)} "
        parts.append(f"{sign} {mag}{mono_str(m)}")
    s = " ".join(parts)
    return s[2:] if s.startswith("+ ") else s


def monomials(n, k):
    return [sum(1 << i for i in c) for c in combinations(range(n), k)]
