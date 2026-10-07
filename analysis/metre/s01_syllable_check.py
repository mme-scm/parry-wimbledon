"""Syllable counter accuracy: development fixture (in-sample, rules tuned on it) and held-out fixture (gold written first)."""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import syllables  # noqa: E402
from metre_lib import RES, HERE  # noqa: E402

RES.mkdir(parents=True, exist_ok=True)
dev = syllables.check()
rows = []
for line in open(HERE / "data" / "syllable_heldout_fixture.tsv", encoding="utf-8"):
    if line.startswith("#") or line.startswith("word\t"):
        continue
    w, g = line.rstrip("\n").split("\t")
    rows.append((w, int(g), syllables.count_token(w)))
n = len(rows)
wrong = [(w, g, c) for w, g, c in rows if g != c]
held = {"n_words": n, "n_exact": n - len(wrong), "accuracy": round((n - len(wrong)) / n, 4),
        "within_one": round(sum(abs(g - c) <= 1 for _, g, c in rows) / n, 4),
        "mean_signed_error_counted_minus_gold": round(sum(c - g for _, g, c in rows) / n, 4),
        "mean_abs_error": round(sum(abs(c - g) for _, g, c in rows) / n, 4),
        "n_in_exception_list": sum(w in syllables.EXCEPTIONS for w, _, _ in rows),
        "errors": [{"word": w, "gold": g, "counted": c} for w, g, c in wrong]}
# Wilson 95% CI for held-out accuracy
from statsmodels.stats.proportion import proportion_confint  # noqa: E402
lo, hi = proportion_confint(n - len(wrong), n, method="wilson")
held["accuracy_wilson95"] = [round(lo, 4), round(hi, 4)]
out = {"development_fixture_in_sample": dev, "heldout_fixture": held}
json.dump(out, open(RES / "syllable_check.json", "w"), indent=1)
print(json.dumps({"dev_acc": dev["accuracy"], "heldout_acc": held["accuracy"], "heldout_ci": held["accuracy_wilson95"],
                  "heldout_errors": held["errors"]}, indent=0))
