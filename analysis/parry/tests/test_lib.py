"""Unit tests of lib2b on synthetic tokens (no corpus text). Run: python -I analysis/parry/tests/test_lib.py"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import numpy as np
import lib2b as L


def test_norm():
    t = L.C.tokenize("Game Djokovic's 40-15 and deuce, Federer")
    n = L.norm_tokens(t)
    assert n == ["game", "<name>'s", "<num>", "<num>", "and", "<num>", "<name>"], n


def test_inventory_coverage():
    utts = [["a", "big", "serve", "out", "wide"], ["big", "serve", "again"], ["out", "wide", "big", "serve"]]
    occ, F, ntok = L.index_inventory(utts)
    assert ("big", "serve") in F and ("out", "wide") in F and ("serve", "out") not in F
    assert ntok == 12
    # coverage of the same text by its own inventory: tokens in 'big serve' or 'out wide': utt0 4/5, utt1 2/3, utt2 4/4 -> 10/12
    assert abs(L.coverage(occ, ntok, F) - 10 / 12) < 1e-12
    assert L.coverage(occ, ntok, F, nmin=3) == 0.0
    v = L.variants(F | {("the", "<num>")})
    assert ("the", "<num>") not in v["content"] and ("the", "<num>") in v["base"]


def test_shuffle():
    rng = np.random.default_rng(1)
    utts = [["a", "b", "c"], ["d"], ["e", "f"]]
    s = L.shuffle_utts(utts, rng)
    assert [len(u) for u in s] == [3, 1, 2]
    assert sorted(t for u in s for t in u) == list("abcdef")


def test_classifier():
    cases = [
        ("30 15 that was a big forehand", 0, 2, "SCORE"),
        ("30 15 that was a big forehand", 5, 7, "SHOT"),          # 'big' JUDGE vs 'forehand' SHOT: 1-1 tie -> SHOT before JUDGE
        ("mr federer is challenging", 0, 2, "OFFICIAL"),
        ("the crowd are on their feet", 0, 2, "CROWD"),
        ("a little bit nervous here", 0, 3, "JUDGE"),
        ("his first serve percentage is 70", 1, 4, "SHOT"),      # SHOT 2 (serve, first serve) vs STAT 1: overlapping entries count separately
        ("and so it goes on", 0, 2, "OTHER"),
        ("game djokovic and he leads", 0, 2, "SCORE"),
    ]
    for text, a, b, want in cases:
        toks = L.C.tokenize(text)
        got = L.SlotClassifier(toks).classify(a, b)
        assert got == want, (text, a, b, got, want)
    sc = L.SlotClassifier(L.C.tokenize("what a shot from federer there"))
    # context of 'federer' = 'what a shot from' | 'there': JUDGE 1 ('what a'), SHOT 1 ('shot'); frozen tie order puts SHOT first
    assert sc.classify_context(4, 5) == "SHOT"


if __name__ == "__main__":
    for name, fn in list(globals().items()):
        if name.startswith("test_"):
            fn()
            print("ok", name)
