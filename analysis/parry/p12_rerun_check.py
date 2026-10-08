"""POST HOC (plan.md addendum 1, minor item m2): do the pre-registered 2b outputs reproduce after the revision and the corpus frame-rate
correction? Every results file tracked in the reference commit (476a088, the last full 2b rerun before the review) is compared with the
current file: CSV and other text files byte for byte (sha256); JSON files after dropping run-time fields (keys containing 'runtime' or
ending in '_s', and 'load_s'); refexpr_pool_tokens.csv on its original columns only (two post hoc columns were added); log files are not
compared (they hold timings and warnings).

Output: results/rerun_check.csv, results/rerun_check.json
Run: python -I analysis/parry/p12_rerun_check.py
"""
import csv
import hashlib
import io
import json
import subprocess
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import lib2b as L

REF = "476a088"


def git_show(path):
    return subprocess.run(["git", "show", f"{REF}:{path}"], cwd=L.ROOT, capture_output=True, check=True).stdout


def strip_runtime(o):
    if isinstance(o, dict):
        return {k: strip_runtime(v) for k, v in o.items() if not ("runtime" in k or k.endswith("_s"))}
    if isinstance(o, list):
        return [strip_runtime(x) for x in o]
    return o


def main():
    files = subprocess.run(["git", "ls-tree", "-r", "--name-only", REF, "analysis/parry/results"], cwd=L.ROOT, capture_output=True, text=True,
                           check=True).stdout.split()
    rows = []
    for path in files:
        name = Path(path).name
        cur = L.ROOT / path
        if name.startswith("log_"):
            continue
        old = git_show(path)
        if not cur.exists():
            rows.append({"file": name, "comparison": "missing now", "identical": False})
            continue
        new = cur.read_bytes()
        if name == "refexpr_pool_tokens.csv":
            ro = list(csv.DictReader(io.StringIO(old.decode("utf-8"))))
            rn = list(csv.DictReader(io.StringIO(new.decode("utf-8"))))
            cols = list(ro[0].keys())
            same = len(ro) == len(rn) and all(all(a[c] == b[c] for c in cols) for a, b in zip(ro, rn))
            rows.append({"file": name, "comparison": f"original {len(cols)} columns, {len(ro)} rows (post hoc columns: "
                         f"{', '.join(c for c in rn[0] if c not in cols)})", "identical": same})
        elif name.endswith(".json"):
            same = strip_runtime(json.loads(old)) == strip_runtime(json.loads(new))
            rows.append({"file": name, "comparison": "JSON without run-time fields", "identical": same,
                         "bytes_identical": hashlib.sha256(old).hexdigest() == hashlib.sha256(new).hexdigest()})
        else:
            same = hashlib.sha256(old).hexdigest() == hashlib.sha256(new).hexdigest()
            rows.append({"file": name, "comparison": "sha256", "identical": same})
    L.write_csv(L.RESULTS / "rerun_check.csv", rows, ["file", "comparison", "identical", "bytes_identical"])
    summary = {"reference_commit": REF, "files_compared": len(rows), "identical": sum(bool(r["identical"]) for r in rows),
               "different": [r["file"] for r in rows if not r["identical"]]}
    L.write_json(L.RESULTS / "rerun_check.json", summary)
    print(summary)


if __name__ == "__main__":
    main()
