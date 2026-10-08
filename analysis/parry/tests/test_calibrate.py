"""Synthetic test of calibrate.py (plan section 6): three made-up utterances, two made-up coders, hand-computed answers.
No corpus text is used. Run: python -I analysis/parry/tests/test_calibrate.py

Tokens: u1 = game djokovic and a little bit of luck (8); u2 = down the line for a winner (6); u3 = he serves (2); 16 in all.
Coder A (primary = HIGH/MEDIUM): u1 'Game Djokovic' SCORE FRAME HIGH, 'a little bit' JUDGE FIXED MEDIUM; u2 'Down the line' SHOT FIXED HIGH.
Coder B: u1 'Game Djokovic' SCORE FRAME HIGH, 'a little bit of luck' JUDGE FIXED LOW; u2 'Down the line for a winner' SHOT FIXED MEDIUM
         (given with a wrong start_char, so it must be relocated).
Hand computation:
  primary token kappa: agreement 10/16, both coders 8/16 positive -> pe 0.5 -> kappa 0.25
  all-confidence kappa: agreement 11/16, A 8/16, B 11/16 -> pe 0.5 -> kappa 0.375
  span F1 (primary): A 3 spans, B 2 spans; exact matches 1 -> 0.4; overlap matches 2 -> 0.8; slot and type agreement 1.0
  automatic 'pool_n2' = u1 [1,1,0,0,1,1,0,0], u2 [0,1,1,0,0,0], u3 [0,0] (6 positives):
    vs A: TP 6 -> P 1, R 0.75; vs B: TP 4 -> P 2/3, R 0.5; vs A and B (5 positives): TP 4 -> R 0.8; vs A or B (11): TP 6 -> R 6/11
"""
import json
import sys
import tempfile
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import calibrate as CAL

U1 = "Game Djokovic and a little bit of luck"
U2 = "Down the line for a winner"
U3 = "He serves"


def sp(a, b, text, slot, typ, conf):
    return {"start_char": a, "end_char": b, "text": text, "essential_idea": "x", "slot": slot, "type": typ,
            "frame": None, "confidence": conf, "note": ""}


def build(d: Path):
    sample = [{"utt_id": "tv_2019wimF:9001", "stream": "tv_2019wimF", "text": U1},
              {"utt_id": "tv_pool_X:0001", "stream": "tv_pool_X", "text": U2},
              {"utt_id": "tv_pool_X:0002", "stream": "tv_pool_X", "text": U3}]
    (d / "sample.jsonl").write_text("\n".join(json.dumps(r) for r in sample) + "\n")
    A = [{"utt_id": "tv_2019wimF:9001", "spans": [sp(0, 13, "Game Djokovic", "SCORE", "FRAME", "HIGH"),
                                                  sp(18, 30, "a little bit", "JUDGE", "FIXED", "MEDIUM")]},
         {"utt_id": "tv_pool_X:0001", "spans": [sp(0, 13, "Down the line", "SHOT", "FIXED", "HIGH")]},
         {"utt_id": "tv_pool_X:0002", "spans": []}]
    Bc = [{"utt_id": "tv_2019wimF:9001", "spans": [sp(0, 13, "Game Djokovic", "SCORE", "FRAME", "HIGH"),
                                                   sp(18, 38, "a little bit of luck", "JUDGE", "FIXED", "LOW")]},
          {"utt_id": "tv_pool_X:0001", "spans": [sp(5, 31, "Down the line for a winner", "SHOT", "FIXED", "MEDIUM")]},
          {"utt_id": "tv_pool_X:0002", "spans": []}]
    (d / "A.jsonl").write_text("\n".join(json.dumps(r) for r in A) + "\n")
    (d / "B.jsonl").write_text("\n".join(json.dumps(r) for r in Bc) + "\n")
    lab = {"tv_2019wimF:9001": [1, 1, 0, 0, 1, 1, 0, 0], "tv_pool_X:0001": [0, 1, 1, 0, 0, 0], "tv_pool_X:0002": [0, 0]}
    import numpy as np
    auto = {k: {m: np.array(v, bool) for m in CAL.MEASURES} for k, v in lab.items()}
    return auto


def close(a, b, tol=1e-9):
    return abs(a - b) < tol


def test_all():
    with tempfile.TemporaryDirectory() as td:
        d = Path(td)
        auto = build(d)
        agr, prf_rows, strata, meta = CAL.run(d / "sample.jsonl", d / "A.jsonl", d / "B.jsonl", d, auto=auto, B_=50)
        p = agr["primary_HIGH_MEDIUM"]
        assert close(p["token_kappa"], 0.25), p["token_kappa"]
        assert close(agr["all_confidences"]["token_kappa"], 0.375), agr["all_confidences"]["token_kappa"]
        assert close(p["span_F1_exact"], 0.4) and close(p["span_F1_overlap"], 0.8), p
        assert p["slot_agreement"] == 1.0 and p["type_agreement"] == 1.0
        assert agr["file_stats"]["B"].get("relocated") == 1, agr["file_stats"]
        get = {(r["measure"], r["reference"], r["coder_confidence"]): r for r in prf_rows}
        r = get[("pool_n2", "A", "HIGH+MEDIUM")]
        assert close(r["precision"], 1.0) and close(r["recall"], 0.75) and close(r["F1"], 2 * 0.75 / 1.75)
        r = get[("pool_n2", "B", "HIGH+MEDIUM")]
        assert close(r["precision"], 4 / 6) and close(r["recall"], 0.5)
        assert close(get[("pool_n2", "A_and_B", "HIGH+MEDIUM")]["recall"], 0.8)
        assert close(get[("pool_n2", "A_or_B", "HIGH+MEDIUM")]["recall"], 6 / 11)
        # classifier vs coders: A's three spans: SCORE (game djokovic), JUDGE (a little bit), SHOT (down the line) -> 3/3
        assert meta["classifier_vs_coder"]["A"]["agreement"] == 1.0, meta
        # absent files -> status only
        out = CAL.run(d / "sample.jsonl", d / "nope_A.jsonl", d / "B.jsonl", d, auto=auto)
        assert out is None and (d / "calibration_status.json").exists()
    print("ok test_calibrate")


if __name__ == "__main__":
    test_all()
