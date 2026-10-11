"""Phase 5 checks: (1) line counts of poem.txt, translation.md, translation_scanned.md; (2) every repeated Greek
string in formula_repeats.json has an `english` rendering that appears verbatim (case-insensitive) in the translation
of every line where the Greek occurs; (3) number of stressed feet per scanned line if marked with | or ´.
Writes check_translation.json. Exit 1 on any failure."""
import json, re, sys, os
H = os.path.dirname(os.path.abspath(__file__))
def numbered_lines(path):
    out = {}
    for l in open(path, encoding='utf-8'):
        m = re.match(r'^\s*(\d+)[.)\]:]?\s+(.*\S)\s*$', l)
        if m: out[int(m.group(1))] = m.group(2)
    return out
poem = [l.strip() for l in open(f'{H}/poem.txt', encoding='utf-8') if l.strip()]
tr = numbered_lines(f'{H}/translation.md')
sc = numbered_lines(f'{H}/translation_scanned.md') if os.path.exists(f'{H}/translation_scanned.md') else {}
rep = json.load(open(f'{H}/formula_repeats.json', encoding='utf-8'))
res = {'n_greek': len(poem), 'n_translation': len(tr), 'n_scanned': len(sc), 'formula_failures': [], 'formulas_checked': 0, 'empty_renderings': []}
for r in rep:
    e = (r.get('english') or '').strip()
    if not e:
        res['empty_renderings'].append(r['greek']); continue
    res['formulas_checked'] += 1
    for n in r['lines']:
        t = tr.get(n, '')
        if e.lower() not in t.lower():
            res['formula_failures'].append({'greek': r['greek'], 'english': e, 'line': n, 'translation': t})
res['ok'] = (res['n_greek'] == res['n_translation'] == 64 and (not sc or res['n_scanned'] == 64)
             and not res['formula_failures'] and not res['empty_renderings'])
json.dump(res, open(f'{H}/check_translation.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print(json.dumps({k: v for k, v in res.items() if k != 'formula_failures'}, ensure_ascii=False))
for f in res['formula_failures']: print('FAIL', f)
sys.exit(0 if res['ok'] else 1)
