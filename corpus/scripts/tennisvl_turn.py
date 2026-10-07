"""Print full text of one turn. Usage: tennisvl_turn.py FILE match_idx turn_idx [maxchars]"""
import json, sys
data = json.load(open(sys.argv[1], encoding="utf-8"))
t = data[int(sys.argv[2])]["conversations"][int(sys.argv[3])]
mx = int(sys.argv[4]) if len(sys.argv) > 4 else 10**9
print(t["from"]); print(t["value"][:mx])
