#!/usr/bin/env python3
"""Numbers cited in review/critic_poem_v1.md. Run from the repository root with the venv active:
    python -I review/critic_poem_v1_checks.py
Reads only: composition/drafts/v3.txt, composition/drafts/v3.jsonl, corpus/timing/points_2019wimF.csv,
homer/lines.tsv; calls homer/check_line.py for the two scales test lines. Nothing is written."""
import csv, json, re, subprocess, sys, unicodedata
from collections import Counter

ROOT = '/home/user/parry-wimbledon'
POEM = [l.strip() for l in open(f'{ROOT}/composition/drafts/v3.txt', encoding='utf-8') if l.strip()]
RECS = [json.loads(l) for l in open(f'{ROOT}/composition/drafts/v3.jsonl', encoding='utf-8') if l.strip()]
ROWS = list(csv.DictReader(open(f'{ROOT}/corpus/timing/points_2019wimF.csv', encoding='utf-8')))
HOMER = []
with open(f'{ROOT}/homer/lines.tsv', encoding='utf-8') as f:
    for r in csv.DictReader(f, delimiter='\t'):
        HOMER.append((r['work'], int(r['book']), int(r['line']),
                      unicodedata.normalize('NFC', r['text']).replace('ʼ', '᾽')))

def P(*a, **k): print(*a, **k)

# ---------------------------------------------------------------- A. corpus rows behind the fact audit
P('## A. corpus rows (points_2019wimF.csv; Dj-Fe score before the point)')
want = {'183', '242', '243', '244', '357', '358', '359', '360', '361', '362', '363', '364', '365'} | {str(i) for i in range(413, 423)}
for r in ROWS:
    if r['point_idx'] in want:
        P(f"pt {r['point_idx']:>3} s{r['set_no']} g{r['game_in_set']:>2} {r['pbp_elapsed']} srv={r['server'].split()[-1]:8s} "
          f"before {r['pts_before_p1']}-{r['pts_before_p2']:<5} games {r['games_before_p1']}-{r['games_before_p2']:<3} "
          f"win={r['point_winner'].split()[-1]:8s} serve#{r['pbp_serve_number']} rally={r['pbp_rally_count']:>2} "
          f"ace={r['mcp_ace']} mcp={r['mcp_1st']} {r['mcp_2nd']}")
P('breaks (game winner != server, non-tie-break):')
games = {}
for r in ROWS:
    games.setdefault((r['set_no'], r['game_in_set']), []).append(r)
for (s, g), rs in games.items():
    if rs[0]['tiebreak'] == 'True':
        continue
    srv = rs[0]['server'].split()[-1]; win = rs[-1]['point_winner'].split()[-1]
    if srv != win:
        P(f"  set {s} game {g}: {srv} serving, broken by {win} at {rs[-1]['pbp_elapsed']}")

# ---------------------------------------------------------------- B. poem counts
P('\n## B. poem counts (composition/drafts/v3.txt, 60 lines)')
def lines_with(pat):
    return [i + 1 for i, l in enumerate(POEM) if re.search(pat, l)]
for label, pat in [('βοὴν ἀγαθ-', 'βοὴν ἀγαθ'), ('δάμασσ-/δάμασε-/δαμάσσ-', 'δάμασσ|δάμασε|δαμάσσ'),
                   ('δεύτερον αὖ*', 'δεύτερον αὖ'), ('τρὶς μέν', 'τρὶς μὲν'), ('ἶσα μάχη(ν)', 'ἶσα μάχη'),
                   ('verse-final ἦμαρ', 'ἦμαρ[.·,;]?$'), ('καὶ βάλεν', 'καὶ βάλεν'), ('οὐδ᾽ ἀφάμαρτε', 'οὐδ᾽ ἀφάμαρτε'),
                   ('ἑτέρωθεν', 'ἑτέρωθεν'), ('ὀψὲ δὲ δή', 'ὀψὲ δὲ δὴ'), ('ἄφαρ', 'ἄφαρ')]:
    h = lines_with(pat); P(f"  {label}: {len(h)}x lines {h}")
stems = ['Ἑλβέτ', 'Ἑλβετ', 'Φεδερ', 'Ῥογῆρ', 'Σέρβ', 'Ζοκοβ', 'Νοβῆκ']
def ntok(ls): return sum(sum(1 for w in l.split() if any(w.startswith(s) for s in stems)) for l in ls)
P(f"  name tokens: whole poem {ntok(POEM)}/60 = {ntok(POEM)/60:.2f} per line; narrative 12-58 {ntok(POEM[11:58])}/47 = {ntok(POEM[11:58])/47:.2f}")
absent = 'τυτθ|ὀλίγ|ἠβαι|λαο|ὅμιλ|θάμβ|ἴαχ|στενάχ|κήρυ|ἴστορ|σκοπ|ἕρκ|λειμ|ποίη|νήσῳ|ἀγών|ἀγῶν'
P(f"  crowd / umpire / hedge / net / grass / island words ({absent}): lines {lines_with(absent)}")
ce = ' || '.join((r.get('commentary_equivalent') or '') for r in RECS)
P('  brief §3 systems cited in jsonl commentary_equivalent:',
  {s: len(re.findall(r'(?<![\d.])' + re.escape(s) + r'(?![\d])', ce)) for s in ['3.1', '3.2', '3.3', '3.4', '3.5', '3.6', '3.7', '3.8', '3.9', '3.10']})
P('  enjambment (jsonl):', dict(Counter(r['enjambment'] for r in RECS)))
P('  mobility entries (jsonl modifications kind=mobility): lines',
  [r['n'] for r in RECS if any(m.get('kind') == 'mobility' for m in r.get('modifications', []))])
P('  lines whose clock precedes the previous narrative line (excluding simile ranges): ', end='')
def clk(c):
    ts = re.findall(r'\d:\d\d:\d\d', c or '')
    f = lambda t: sum(int(x) * k for x, k in zip(t.split(':'), (3600, 60, 1)))
    return (f(ts[0]), f(ts[-1])) if ts else None
prev = None; inv = []
for r in RECS:
    c = clk(r.get('clock'))
    if c and prev and c[0] < prev[1] and '-' not in (r.get('clock') or '') and '-' not in prevc:
        inv.append((r['n'], r['clock'], prevn, prevc))
    if c: prev, prevn, prevc = c, r['n'], r['clock']
P(inv)

# ---------------------------------------------------------------- C. Homeric benchmarks (homer/lines.tsv)
P('\n## C. Homeric benchmarks')
def hcount(pat): return sum(1 for r in HOMER if re.search(pat, r[3]))
P(f"  lines in lines.tsv: {len(HOMER)}")
P(f"  δεύτερον αὖ*: {hcount('δεύτερον αὖ')}; δεύτερον αὖτε: {hcount('δεύτερον αὖτε')}; δεύτερος αὖτε: {hcount('δεύτερος αὖτε')}")
P(f"  ὀψὲ δὲ δή: {hcount('ὀψὲ δὲ δὴ')}; lines with both ὀψ- and ἄφαρ: {hcount('ὀψ.*ἄφαρ|ἄφαρ.*ὀψ')}")
P(f"  δάμασσε/ἐδάμασσε(ν)/δάμασε(ν) lines: {hcount(r'δάμασσε|ἐδάμασσε|δάμασεν?\b')} (all listed in the review as kill/overpower/subjugate)")
P(f"  ἄσπετον ἤρατο κῦδος: {hcount('ἄσπετον ἤρατο κῦδος')}, preceded by καί νύ κεν in:",
  [f"{r[0]}. {r[1]}.{r[2]}" for r in HOMER if 'ἄσπετον ἤρατο κῦδος' in r[3] and r[3].startswith('καί νύ κεν')])
P(f"  τοῖιν (dual gen./dat.): {hcount(r'\bτοῖ[ιϊ]ν\b')}; θάμβος δ᾽ ἔχεν εἰσορόωντας: {hcount('θάμβος δ᾽ ἔχεν εἰσορόωντας')}")
P(f"  ὣς οἳ μὲν μάρναντο: {hcount('ὣς οἳ μὲν μάρναντο')}; ἐπὶ ἶσα μάχη τέτατο: {hcount('ἐπὶ ἶσα μάχη τέτατο')}")
adj = sum(1 for i in range(1, len(HOMER)) if 'βοὴν ἀγαθ' in HOMER[i - 1][3] and 'βοὴν ἀγαθ' in HOMER[i][3])
P(f"  adjacent Homeric lines both containing βοὴν ἀγαθ-: {adj}")
duels = {'Il. 3.340-382 Paris/Menelaus': ('Il', 3, 340, 382, ['Ἀλέξανδρ', 'Μενέλα', 'Ἀτρεΐδ', 'Ἀτρείδ', 'Πρι']),
         'Il. 7.244-312 Ajax/Hector': ('Il', 7, 244, 312, ['Αἴα', 'Ἕκτ', 'Τελαμών', 'Πριαμίδ']),
         'Il. 22.248-330 Achilles/Hector': ('Il', 22, 248, 330, ['Ἀχιλ', 'Ἕκτ', 'Πηλε', 'Πριαμίδ']),
         'Il. 23.708-739 Odysseus/Ajax': ('Il', 23, 708, 739, ['Ὀδυσ', 'Αἴα', 'Τελαμών', 'Λαερτιάδ']),
         'Il. 21.139-204 Achilles/Asteropaeus': ('Il', 21, 139, 204, ['Ἀχιλ', 'Ἀστεροπαῖ', 'Πηλε'])}
for k, (w, b, l1, l2, st) in duels.items():
    seg = [r for r in HOMER if r[0] == w and r[1] == b and l1 <= r[2] <= l2]
    t = sum(sum(1 for word in r[3].split() if any(word.lstrip('(').startswith(s) for s in st)) for r in seg)
    P(f"  name tokens of the two combatants, {k}: {t}/{len(seg)} = {t/len(seg):.2f} per line")

# ---------------------------------------------------------------- D. scales test lines (metre only; not proposed wording)
P('\n## D. check_line on two death-free second halves for line 50 (metre only)')
for L in ['ἐν δ᾽ ἐτίθει δύο κῆρε, τὸ δὲ μέγα κεῖται ἄεθλον', 'ἐν δ᾽ ἐτίθει δύο νίκας ἐπειγομένων περὶ νίκης']:
    out = subprocess.run([sys.executable, f'{ROOT}/homer/check_line.py', L], capture_output=True, text=True).stdout
    P('  ' + L + ' -> ' + ' | '.join(x.strip() for x in out.splitlines()[1:2] + [y for y in out.splitlines() if y.strip().startswith(('licences', 'warn', 'FLAG', 'UNMETRICAL'))]))
