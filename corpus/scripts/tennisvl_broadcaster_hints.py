"""Count mentions of broadcaster / commentator names in each test match's ASR transcripts.
Hints only: a name heard in commentary does not prove who broadcast it.
Usage: python3 -I tennisvl_broadcaster_hints.py FILE"""
import json, sys, ast, re
from collections import Counter
NAMES = ["BBC", "ESPN", "Eurosport", "Tennis Channel", "Sky", "Nine", "Channel 9", "Stan", "Amazon", "Prime",
         "Tennis TV", "CBS", "NBC", "Fox", "TNT", "beIN", "France Télévisions", "Wimbledon Channel",
         "McEnroe", "Cliff", "Drysdale", "Chris Fowler", "Fowler", "Evert", "Chrissie", "Mary Joe", "Carillo",
         "Courier", "Jim", "Henman", "Tim", "Andrew Castle", "Castle", "Boris", "Becker", "Annabel", "Croft",
         "Tracy Austin", "Lindsay", "Davenport", "Todd", "Woodbridge", "Sam Smith", "Pam Shriver", "Brad Gilbert",
         "Brad", "Patrick", "Johnny Mac", "Jason Goodall", "Robbie Koenig", "Mats", "Wilander", "Barbara Schett",
         "Alize", "Martina", "Navratilova", "Fitzgerald", "Rennae", "Casey Dellacqua", "Sam Stosur", "Craig Willis",
         "Gilbert", "Petchey", "Mark Petchey", "Rusedski", "Greg", "Lleyton", "Hewitt", "Jelena", "Dokic",
         "Nick Lester", "Ian Cohen", "Mark Woodforde", "Pat Cash", "Kim", "Clijsters", "Laura Robson", "Murray"]
data = json.load(open(sys.argv[1], encoding="utf-8"))
for i, rec in enumerate(data):
    mid = re.sub(r"_\d+_\d+\.mp4$", "", rec["videos"][0].split("/")[-1])
    text = []
    for t in rec["conversations"]:
        if t["from"] == "gpt":
            _, _, meta = t["value"].partition("\n\nMetadata:")
            if meta:
                text.append(ast.literal_eval(meta.strip()).get("audio_transcription (background context)", "") or "")
    s = " ".join(text)
    c = Counter()
    for n in NAMES:
        k = len(re.findall(r"\b" + re.escape(n) + r"\b", s))
        if k: c[n] = k
    print(i, mid, dict(c.most_common(12)))
