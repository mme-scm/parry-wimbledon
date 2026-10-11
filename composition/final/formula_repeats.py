"""Repeated word strings (2+ words, accent-insensitive) in composition/final/poem.txt, with the lines they occur in.
Output: composition/final/formula_repeats.json. The translator fills `english` for each; check_translation.py verifies."""
import json, re, unicodedata, sys, os
H = os.path.dirname(__file__)
def loose(w):
    w = unicodedata.normalize('NFD', w); w = ''.join(c for c in w if not unicodedata.combining(c))
    return w.lower().replace('ς', 'σ').replace('ʼ', '').replace('᾽', '').replace("'", '')
lines = [l.strip() for l in open(f'{H}/poem.txt', encoding='utf-8') if l.strip()]
toks = []
for i, l in enumerate(lines, 1):
    ws = [w for w in re.split(r"[\s,.;·:!?]+", l) if w]
    toks.append([(w, loose(w)) for w in ws])
seen = {}
for i, ws in enumerate(toks, 1):
    for n in range(2, 7):
        for j in range(len(ws) - n + 1):
            key = ' '.join(x[1] for x in ws[j:j+n])
            seen.setdefault(key, {'form': ' '.join(x[0] for x in ws[j:j+n]), 'lines': []})
            if i not in seen[key]['lines']: seen[key]['lines'].append(i)
rep = {k: v for k, v in seen.items() if len(v['lines']) >= 2}
# keep maximal strings only (drop a string if a longer repeated string with the same line set contains it)
keys = sorted(rep, key=lambda k: -len(k.split()))
maximal = {}
for k in keys:
    if any(k in m and set(rep[k]['lines']) == set(rep[m]['lines']) for m in maximal): continue
    maximal[k] = rep[k]
out = [{'loose': k, 'greek': v['form'], 'lines': v['lines'], 'english': ''} for k, v in sorted(maximal.items(), key=lambda kv: kv[1]['lines'])]
json.dump(out, open(f'{H}/formula_repeats.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print(len(out), 'repeated strings')
for o in out: print(o['lines'], o['greek'])
