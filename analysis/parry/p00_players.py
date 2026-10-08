"""Builds hand/players.tsv: the players of the 20 TV matches with nationality and the demonyms used for nationality epithets (plan section 9).
Nationality is read from the Sackmann slam `*-matches.csv` files (nation1/nation2, corpus/raw/sackmann_slam_pbp_hfmirror); the three
players absent from those files are entered by hand below and marked [unverified]. Demonym lists are my own (plan section 9).
Run: python -I analysis/parry/p00_players.py
"""
import collections
import csv
import glob
import json
from pathlib import Path

R = Path(__file__).resolve().parents[2]
DEM = {"SUI": "swiss", "SRB": "serb|serbian", "ESP": "spaniard", "ITA": "italian", "RUS": "russian", "GRE": "greek", "NOR": "norwegian",
       "AUT": "austrian", "POL": "pole", "CZE": "czech", "USA": "american", "JPN": "japanese", "CAN": "canadian", "GBR": "brit|briton"}
HAND = {"Carlos Alcaraz": "ESP", "Emma Raducanu": "GBR", "Ben Shelton": "USA"}   # [unverified], general knowledge


def main():
    players = {}
    for p in sorted(glob.glob(str(R / "corpus/transcripts/tv_*.jsonl"))):
        mid = json.loads(open(p, encoding="utf-8").readline())["match_id"]
        for x in mid.split("-")[-2:]:
            players[x.replace("_", " ")] = None
    nat = collections.defaultdict(collections.Counter)
    for f in sorted(glob.glob(str(R / "corpus/raw/sackmann_slam_pbp_hfmirror/*matches.csv"))):
        for r in csv.DictReader(open(f, encoding="utf-8")):
            for k in ("1", "2"):
                n, c = r.get("player" + k, ""), r.get("nation" + k, "")
                if n and c:
                    nat[n][c] += 1
    rows = []
    for pl in sorted(players):
        first, sur = pl.split()[0], pl.split()[-1]
        key = f"{first[0]}. {sur}"
        if key in nat:
            c = nat[key].most_common(1)[0][0]
            src = f"Sackmann slam *-matches.csv nation1/nation2 ({key}, {sum(nat[key].values())} rows)"
        else:
            c = HAND[pl]
            src = "entered by hand from general knowledge [unverified]: absent from the Sackmann match files"
        rows.append([pl, first.lower(), sur.lower(), c, DEM[c], src])
    out = Path(__file__).resolve().parent / "hand" / "players.tsv"
    out.parent.mkdir(exist_ok=True)
    with open(out, "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh, delimiter="\t")
        w.writerow(["player", "first", "surname", "nation", "demonyms", "source"])
        w.writerows(rows)
    print(len(rows), "players written to", out)


if __name__ == "__main__":
    main()
