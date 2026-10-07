"""Summarise one match in a Sackmann slam points CSV: n points, ElapsedTime range, non-empty columns.
Usage: python3 -I pbp_match.py points.csv match_id"""
import csv, sys
rows = [r for r in csv.DictReader(open(sys.argv[1], encoding="utf-8")) if r["match_id"] == sys.argv[2]]
print("rows", len(rows))
real = [r for r in rows if r["PointNumber"] not in ("0", "0X", "0Y")]
print("points (excluding PointNumber 0 rows)", len(real))
print("ElapsedTime first/last:", rows[0]["ElapsedTime"], rows[-1]["ElapsedTime"])
nonempty = [k for k in rows[0].keys() if any(r[k] not in ("", "0") for r in rows)]
print("columns with non-empty/non-zero values:", nonempty)
for r in rows[1:3]:
    print({k: r[k] for k in ["match_id","ElapsedTime","SetNo","GameNo","PointNumber","PointWinner","PointServer","Speed_KMH","Rally","P1Score","P2Score","ServeNumber","WinnerType","RallyCount"]})
