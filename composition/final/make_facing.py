"""Write composition/final/facing.md: two-column table, Greek left, English right, one row per line."""
import re, os
H = os.path.dirname(os.path.abspath(__file__))
poem = [l.strip() for l in open(f'{H}/poem.txt', encoding='utf-8') if l.strip()]
tr = {}
for l in open(f'{H}/translation.md', encoding='utf-8'):
    m = re.match(r'^\s*(\d+)[.)\]:]?\s+(.*\S)\s*$', l)
    if m: tr[int(m.group(1))] = m.group(2)
assert len(poem) == 64 and len(tr) == 64, (len(poem), len(tr))
with open(f'{H}/facing.md', 'w', encoding='utf-8') as f:
    f.write('# The match at Wimbledon, 14 July 2019: Greek and English facing\n\n')
    f.write('Greek: composition/final/poem.txt (64 hexameters, verified in review/round_4.md). English: composition/final/translation.md (accentual hexameter, line for line; repeated formulae rendered identically, see formula_repeats.json).\n\n')
    f.write('| n | Greek | English |\n|---|---|---|\n')
    for i, g in enumerate(poem, 1):
        f.write(f'| {i} | {g} | {tr[i]} |\n')
print('facing.md written, 64 rows')
