#!/usr/bin/env python3
"""Compute every number used in composition/research/match_facts.md from the corpus files.

Sources (all on disk, none edited):
  P  corpus/timing/points_2019wimF.csv               merged per-point table (PBP x MCP x TennisVL)
  R  corpus/raw/sackmann_slam_pbp_hfmirror/2019-wimbledon-points.csv  (match_id 2019-wimbledon-1701; P1 = Djokovic, P2 = Federer)
  M  corpus/raw/sackmann_mcp/charting-m-points-2010s.csv (match_id 20190714-M-Wimbledon-F-Roger_Federer-Novak_Djokovic; player 1 = Federer)
  S  corpus/timing/shots_2019wimF.csv                 TennisVL per-shot timing
  T  corpus/transcripts/tv_2019wimF.jsonl             TennisVL WhisperX transcript, one record per clip
Run:  python -I match_facts.py > match_facts_out.md
"""
import csv, json, re, statistics, sys
from collections import Counter, defaultdict

ROOT = '/home/user/parry-wimbledon'
P = list(csv.DictReader(open(f'{ROOT}/corpus/timing/points_2019wimF.csv', encoding='utf-8')))
R = [r for r in csv.DictReader(open(f'{ROOT}/corpus/raw/sackmann_slam_pbp_hfmirror/2019-wimbledon-points.csv', encoding='utf-8'))
     if r['match_id'] == '2019-wimbledon-1701' and r['PointNumber'] not in ('0X', '0Y')]
M = [r for r in csv.DictReader(open(f'{ROOT}/corpus/raw/sackmann_mcp/charting-m-points-2010s.csv', encoding='utf-8'))
     if r['match_id'] == '20190714-M-Wimbledon-F-Roger_Federer-Novak_Djokovic']
M.sort(key=lambda r: int(r['Pt']))
S = list(csv.DictReader(open(f'{ROOT}/corpus/timing/shots_2019wimF.csv', encoding='utf-8')))
T = [json.loads(l) for l in open(f'{ROOT}/corpus/transcripts/tv_2019wimF.jsonl', encoding='utf-8')]

assert len(P) == 422 and len(R) == 422 and len(M) == 422, (len(P), len(R), len(M))
for i, (p, r, m) in enumerate(zip(P, R, M), 1):
    assert int(p['point_idx']) == i == int(r['PointNumber']) == int(m['Pt'])
    assert p['pbp_elapsed'] == r['ElapsedTime']
    assert p['mcp_1st'] == m['1st'] and p['mcp_2nd'] == m['2nd']

DJ, FE = 'Novak Djokovic', 'Roger Federer'
NAME = {'1': 'Djokovic', '2': 'Federer'}           # PBP P1/P2
MCPNAME = {'1': 'Federer', '2': 'Djokovic'}        # MCP player 1/2
by_point = defaultdict(list)
for t in T:
    if t.get('point_idx_pbp') is not None:
        by_point[int(t['point_idx_pbp'])].append(t)

def hms(s):
    s = int(s); return f'{s//3600}:{(s%3600)//60:02d}:{s%60:02d}'

def excerpt(text, kw=None, n=15):
    """At most n words; centred on the first match of kw if given."""
    words = text.split()
    if len(words) <= n:
        return ' '.join(words)
    if kw:
        for i, w in enumerate(words):
            if re.search(kw, w, re.I):
                lo = max(0, i - n // 2); hi = lo + n
                if hi > len(words):
                    hi = len(words); lo = hi - n
                return ('… ' if lo > 0 else '') + ' '.join(words[lo:hi]) + (' …' if hi < len(words) else '')
    return ' '.join(words[:n]) + ' …'

def clips_for(idx):
    """Transcript records for PBP point idx: (utt_id, clip_role, clip_start_s, text_corrected)."""
    out = []
    for t in by_point.get(idx, []):
        out.append((t['utt_id'], t['clip_role'], t['clip_start_s'], t['text_corrected'] or ''))
    return out

def commentary(idx, n=15):
    parts = []
    for u, role, cs, txt in clips_for(idx):
        if txt.strip():
            parts.append(f'{u} ({role}, video {cs:.1f}s): "{excerpt(txt, None, n)}"')
    return '; '.join(parts) if parts else '(no transcribed clip)'

def mcp_end(code):
    """Point-ending class from the last MCP shot code: * winner, @ unforced error, # forced error."""
    c = (code or '').strip()
    return {'*': 'winner', '@': 'unforced error', '#': 'forced error'}.get(c[-1:], '?')

def mcp_desc(p):
    first, second = p['mcp_1st'], p['mcp_2nd']
    if second:
        return f'1st `{first}` (fault), 2nd `{second}` -> {mcp_end(second)}'
    return f'`{first}` -> {mcp_end(first)}'

out = []
pr = out.append

# ---------------------------------------------------------------- 1. score set by set
pr('## T1. Score set by set (R: last row of each SetNo; tie-break score = P1Score/P2Score after the penultimate point + the winner of the last point)')
pr('| set | games Djokovic-Federer | set winner | tie-break (Djokovic-Federer) | first point clock | last point clock | points in set | games in set |')
pr('|---|---|---|---|---|---|---|---|')
set_rows = defaultdict(list)
for r in R:
    set_rows[r['SetNo']].append(r)
for s in sorted(set_rows):
    rows = set_rows[s]
    last = rows[-1]
    tb = [r for r in rows if r['GameNo'] == (str(max(int(x['GameNo']) for x in rows)) if int(last['P1GamesWon']) + int(last['P2GamesWon']) in (13, 25) else '-')]
    tbtxt = '-'
    if tb:
        # score before the last tb point, then add the winner's point
        # R's P1Score/P2Score are the state AFTER the point (the last row resets to 0-0):
        a, b = int(tb[-2]['P1Score']), int(tb[-2]['P2Score'])
        if tb[-1]['PointWinner'] == '1': a += 1
        else: b += 1
        tbtxt = f'{a}-{b}'
    pr(f"| {s} | {last['P1GamesWon']}-{last['P2GamesWon']} | {NAME[last['SetWinner']]} | {tbtxt} | {rows[0]['ElapsedTime']} | {last['ElapsedTime']} | {len(rows)} | {len(set(r['GameNo'] for r in rows))} |")
pr(f"\nDuration = last ElapsedTime (R) = **{R[-1]['ElapsedTime']}** (first serve of the last point; the match clock starts 0:00:00 at point 1).")
pr(f"Sets: Djokovic {sum(1 for s in set_rows if set_rows[s][-1]['SetWinner']=='1')}, Federer {sum(1 for s in set_rows if set_rows[s][-1]['SetWinner']=='2')}.")
pr('')

# ---------------------------------------------------------------- 2. points won
pr('## T2. Points won')
pw = Counter(r['PointWinner'] for r in R)
pr(f"R PointWinner counts: Djokovic {pw['1']}, Federer {pw['2']} (total {sum(pw.values())}); R running columns at the last row: P1PointsWon={R[-1]['P1PointsWon']} (Djokovic), P2PointsWon={R[-1]['P2PointsWon']} (Federer).")
pwm = Counter(m['PtWinner'] for m in M)
pr(f"M PtWinner counts: Federer {pwm['1']}, Djokovic {pwm['2']}.")
pr('Per set (R):')
pr('| set | Djokovic | Federer |')
pr('|---|---|---|')
for s in sorted(set_rows):
    c = Counter(r['PointWinner'] for r in set_rows[s])
    pr(f"| {s} | {c['1']} | {c['2']} |")
# service points won
pr('\nService points (R: PointServer = server; won = PointWinner == PointServer):')
pr('| server | service points | won | % |')
pr('|---|---|---|---|')
for sv in ('1', '2'):
    n = sum(1 for r in R if r['PointServer'] == sv); w = sum(1 for r in R if r['PointServer'] == sv and r['PointWinner'] == sv)
    pr(f"| {NAME[sv]} | {n} | {w} | {100*w/n:.1f} |")
pr('')

# ---------------------------------------------------------------- 3. aces, DFs, winners, UEs per set
pr('## T3. Aces, double faults, winners, unforced errors per player per set (R columns P1Ace/P2Ace, P1DoubleFault/P2DoubleFault, P1Winner/P2Winner, P1UnfErr/P2UnfErr; 1 = that point)')
pr('| set | aces Dj | aces Fe | DF Dj | DF Fe | winners Dj | winners Fe | UE Dj | UE Fe | net pts Dj (won) | net pts Fe (won) |')
pr('|---|---|---|---|---|---|---|---|---|---|---|')
tot = Counter()
for s in sorted(set_rows) + ['all']:
    rows = R if s == 'all' else set_rows[s]
    c = {k: sum(int(r[k]) for r in rows) for k in ('P1Ace','P2Ace','P1DoubleFault','P2DoubleFault','P1Winner','P2Winner','P1UnfErr','P2UnfErr','P1NetPoint','P2NetPoint','P1NetPointWon','P2NetPointWon')}
    pr(f"| {s} | {c['P1Ace']} | {c['P2Ace']} | {c['P1DoubleFault']} | {c['P2DoubleFault']} | {c['P1Winner']} | {c['P2Winner']} | {c['P1UnfErr']} | {c['P2UnfErr']} | {c['P1NetPoint']} ({c['P1NetPointWon']}) | {c['P2NetPoint']} ({c['P2NetPointWon']}) |")
# does P1Winner include aces?
both = sum(1 for r in R if r['P1Ace']=='1' and r['P1Winner']=='1') + sum(1 for r in R if r['P2Ace']=='1' and r['P2Winner']=='1')
pr(f"\nAces counted also as winners in R (rows with Ace=1 and Winner=1 for the same player): {both} of {sum(int(r['P1Ace'])+int(r['P2Ace']) for r in R)} aces -> the Winner columns {'include' if both else 'exclude'} aces.")
empty = [c for c in R[0] if all(r[c] == '' for r in R)]
pr(f"R columns that are empty for every point of this match: {', '.join(empty)}.")
pr("R columns filled: all others; WinnerType is 'S' for 8 points (serve winners), WinnerShotType F/B for 105 points; Rally is empty (RallyCount is filled).")
# MCP cross-check
pr('\nCross-check from M (Match Charting Project; ending symbol of the last shot code: `*` winner, `@` unforced error, `#` forced error; mcp_ace / mcp_double_fault from P):')
mc = Counter()
for p in P:
    code = p['mcp_2nd'] or p['mcp_1st']
    hitter_is_server = (p['mcp_n_shots'] and int(p['mcp_n_shots']) % 2 == 1)
    srv = MCPNAME[p['mcp_svr']]
    other = 'Djokovic' if srv == 'Federer' else 'Federer'
    hitter = srv if hitter_is_server else other
    end = mcp_end(code)
    if p['mcp_ace'] == '1': mc[(srv, 'ace')] += 1
    if p['mcp_double_fault'] == '1': mc[(srv, 'double fault')] += 1
    if end == 'winner' and p['mcp_ace'] != '1': mc[(hitter, 'winner (non-ace)')] += 1
    if end == 'unforced error' and p['mcp_double_fault'] != '1': mc[(hitter, 'unforced error (non-DF)')] += 1
    if end == 'forced error': mc[(hitter, 'forced error')] += 1
pr('| | Djokovic | Federer |')
pr('|---|---|---|')
for k in ('ace', 'double fault', 'winner (non-ace)', 'unforced error (non-DF)', 'forced error'):
    pr(f"| {k} | {mc[('Djokovic', k)]} | {mc[('Federer', k)]} |")
pr('(hitter of the last shot inferred from the parity of mcp_n_shots: odd = server hit last; the MCP charter\'s own @/# labels differ from the official R labels, see corpus/README.md section 7.1)')
pr('')

# ---------------------------------------------------------------- 4. break points
pr('## T4. Break points (R: P1BreakPoint = Djokovic holds a break point (Federer serving), P1BreakPointWon = converted; P2* likewise for Federer)')
chk = Counter((r['PointServer']) for r in R if r['P1BreakPoint'] == '1')
pr(f"Sanity: server on the points with P1BreakPoint=1: {dict(chk)} (2 = Federer serving, as expected).")
pr('| set | BP for Djokovic (converted) | BP for Federer (converted) | breaks of serve in set (game winner != server) |')
pr('|---|---|---|---|')
for s in sorted(set_rows) + ['all']:
    rows = R if s == 'all' else set_rows[s]
    b1 = sum(int(r['P1BreakPoint']) for r in rows); w1 = sum(int(r['P1BreakPointWon']) for r in rows)
    b2 = sum(int(r['P2BreakPoint']) for r in rows); w2 = sum(int(r['P2BreakPointWon']) for r in rows)
    brk = [(r['SetNo'], r['GameNo'], NAME[r['GameWinner']]) for r in rows if r['GameWinner'] != '0' and r['GameWinner'] != r['PointServer'] and not (int(r['P1GamesWon'])+int(r['P2GamesWon']) in (13,25) and r['SetWinner']!='0')]
    pr(f"| {s} | {b1} ({w1}) | {b2} ({w2}) | {'; '.join(f's{a} g{g} by {w}' for a,g,w in brk) if s!='all' else len(brk)} |")
pr('(a tie-break game is excluded from the break column.)')
pr('')

# ---------------------------------------------------------------- 5. serve speed
pr('## T5. Serve speed (R: Speed_KMH of the serve that started the point, by PointServer and ServeNumber; 0 = not recorded)')
pr('| server | serves recorded | 1st-serve n | 1st max | 1st mean | 2nd n | 2nd max | 2nd mean | all max | all mean | all min |')
pr('|---|---|---|---|---|---|---|---|---|---|---|')
for sv in ('1', '2'):
    sp = [(int(r['Speed_KMH']), r['ServeNumber']) for r in R if r['PointServer'] == sv and int(r['Speed_KMH']) > 0]
    s1 = [v for v, n in sp if n == '1']; s2 = [v for v, n in sp if n == '2']; sa = [v for v, n in sp]
    pr(f"| {NAME[sv]} | {len(sa)} | {len(s1)} | {max(s1)} | {statistics.mean(s1):.1f} | {len(s2)} | {max(s2)} | {statistics.mean(s2):.1f} | {max(sa)} | {statistics.mean(sa):.1f} | {min(sa)} |")
zero = sum(1 for r in R if int(r['Speed_KMH']) == 0)
pr(f"Points with Speed_KMH = 0 (unrecorded): {zero} of 422.")
for sv in ('1','2'):
    best = max((r for r in R if r['PointServer']==sv), key=lambda r:int(r['Speed_KMH']))
    pr(f"Fastest serve {NAME[sv]}: {best['Speed_KMH']} km/h ({best['Speed_MPH']} mph) at {best['ElapsedTime']}, set {best['SetNo']} game {best['GameNo']}, point {best['PointNumber']}, serve {best['ServeNumber']}, ace={best['P'+sv+'Ace']}; MCP {mcp_desc(P[int(best['PointNumber'])-1])}; commentary: {commentary(int(best['PointNumber']))}")
pr('')

# ---------------------------------------------------------------- 6. longest rally
pr('## T6. Longest rallies')
pr('Conventions (corpus/README.md 7.1): R RallyCount counts in-play shots (the erring final shot is not counted); M and TennisVL count the erring shot too.')
top_m = sorted(P, key=lambda p: -int(p['mcp_n_shots'] or 0))[:6]
pr('| rank | point_idx | clock (R ElapsedTime) | set/game, score before (server first, PBP) | MCP shots | R RallyCount | TV n_shots | TV rally s | winner | ending (MCP) | commentary (TennisVL clip) |')
pr('|---|---|---|---|---|---|---|---|---|---|---|')
for i, p in enumerate(top_m, 1):
    idx = int(p['point_idx']); r = R[idx-1]
    sc = f"s{p['set_no']} g{p['game_in_set']}{' TB' if p['tiebreak']=='True' else ''}, {p['pts_before_p1']}-{p['pts_before_p2']} (Dj-Fe), games {p['games_before_p1']}-{p['games_before_p2']}, server {p['server'].split()[-1]}"
    pr(f"| {i} | {idx} | {p['pbp_elapsed']} | {sc} | {p['mcp_n_shots']} | {r['RallyCount']} | {p['tv_n_shots'] or '-'} | {p['tv_rally_duration_s'] or '-'} | {p['point_winner'].split()[-1]} | {mcp_desc(p)} | {commentary(idx)} |")
top_tv = sorted([p for p in P if p['tv_n_shots']], key=lambda p: -int(p['tv_n_shots']))[:3]
pr('\nLongest by TennisVL shot count: ' + '; '.join(f"point {p['point_idx']} ({p['tv_n_shots']} shots, {p['tv_rally_duration_s']} s, MCP {p['mcp_n_shots']}, clock {p['pbp_elapsed']})" for p in top_tv))
top_r = sorted(R, key=lambda r: -int(r['RallyCount']))[:3]
pr('Longest by R RallyCount: ' + '; '.join(f"point {r['PointNumber']} ({r['RallyCount']} in-play shots, clock {r['ElapsedTime']})" for r in top_r))
# longest by TV duration
top_dur = sorted([p for p in P if p['tv_rally_duration_s']], key=lambda p: -float(p['tv_rally_duration_s']))[:3]
pr('Longest by TennisVL rally duration (first hit to last hit): ' + '; '.join(f"point {p['point_idx']} ({p['tv_rally_duration_s']} s, {p['tv_n_shots']} shots, clock {p['pbp_elapsed']})" for p in top_dur))
# distance run on the longest point
r = R[int(top_m[0]['point_idx'])-1]
pr(f"R distance run on point {r['PointNumber']}: Djokovic {r['P1DistanceRun']} m, Federer {r['P2DistanceRun']} m (units as in the file; the column is unlabelled).")
# rally length distribution
rc = [int(p['mcp_n_shots']) for p in P if p['mcp_n_shots']]
pr(f"MCP shots per point: mean {statistics.mean(rc):.2f}, median {statistics.median(rc)}, points with >= 10 shots: {sum(1 for x in rc if x>=10)}, 1-shot points (aces/DF/unreturned serves counted as 1 or 2): {sum(1 for x in rc if x<=2)}.")
pr('')

# ---------------------------------------------------------------- helper for tie-break tables
def tb_table(set_no, game_no, title):
    pr(f'## {title}')
    pr('| pt | clock | score before (Dj-Fe) | server | serve km/h (no.) | winner | R RallyCount | MCP shots | MCP code -> ending | R flags | commentary |')
    pr('|---|---|---|---|---|---|---|---|---|---|---|')
    rows = [(i, r) for i, r in enumerate(R, 1) if r['SetNo'] == set_no and r['GameNo'] == game_no]
    prev = None
    for i, r in rows:
        p = P[i-1]
        flags = [k for k in ('P1Ace','P2Ace','P1DoubleFault','P2DoubleFault','P1Winner','P2Winner','P1UnfErr','P2UnfErr','P1NetPoint','P2NetPoint') if r[k]=='1']
        flags = ','.join(f.replace('P1','Dj:').replace('P2','Fe:') for f in flags)
        pr(f"| {i} | {r['ElapsedTime']} | {p['pts_before_p1']}-{p['pts_before_p2']} | {NAME[r['PointServer']]} | {r['Speed_KMH']} ({r['ServeNumber']}) | {NAME[r['PointWinner']]} | {r['RallyCount']} | {p['mcp_n_shots']} | {mcp_desc(p)} | {flags} | {commentary(i)} |")
    last = rows[-1][1]
    pr(f"Tie-break first point {rows[0][1]['ElapsedTime']}, last point {last['ElapsedTime']}; {len(rows)} points; game winner {NAME[last['GameWinner']]}; set winner {NAME[last['SetWinner']]}.")
    pr('')

tb_table('1', '13', 'T7. First-set tie-break (R: SetNo 1, GameNo 13), point by point')
tb_table('3', '13', 'T8. Third-set tie-break (R: SetNo 3, GameNo 13), point by point')

# ---------------------------------------------------------------- fifth set game by game
pr('## T9. Fifth set game by game (R: SetNo 5; clock = ElapsedTime of the first point of the game; games after = P1GamesWon-P2GamesWon at the game\'s last point)')
pr('| game (set) | R GameNo (restarts each set) | clock first point | clock last point | server | points (Dj-Fe) | game winner | break? | games after (Dj-Fe) | note (R flags) |')
pr('|---|---|---|---|---|---|---|---|---|---|')
games = defaultdict(list)
for i, r in enumerate(R, 1):
    if r['SetNo'] == '5':
        games[int(r['GameNo'])].append((i, r))
g5first = min(games)
for g in sorted(games):
    rows = games[g]
    first, last = rows[0][1], rows[-1][1]
    c = Counter(r['PointWinner'] for _, r in rows)
    srv = NAME[first['PointServer']]
    win = NAME[last['GameWinner']]
    brk = 'BREAK' if (win != srv and g != 25) else ''
    notes = []
    bp1 = sum(int(r['P1BreakPoint']) for _, r in rows); bp2 = sum(int(r['P2BreakPoint']) for _, r in rows)
    if bp1: notes.append(f'{bp1} BP for Djokovic')
    if bp2: notes.append(f'{bp2} BP for Federer')
    aces = sum(int(r['P1Ace'])+int(r['P2Ace']) for _, r in rows); dfs = sum(int(r['P1DoubleFault'])+int(r['P2DoubleFault']) for _, r in rows)
    if aces: notes.append(f'{aces} ace(s)')
    if dfs: notes.append(f'{dfs} DF')
    if g == 25: notes.append('TIE-BREAK at 12-12 (first ever at this score in a Wimbledon final: see external section)')
    pr(f"| {g-g5first+1} | {g} | {first['ElapsedTime']} | {last['ElapsedTime']} | {srv} | {c['1']}-{c['2']} | {win} | {brk} | {last['P1GamesWon']}-{last['P2GamesWon']} | {'; '.join(notes)} |")
s5 = set_rows['5']
pr(f"\nFifth set: {len(s5)} points, from {s5[0]['ElapsedTime']} to {s5[-1]['ElapsedTime']}; points won Djokovic {sum(1 for r in s5 if r['PointWinner']=='1')}, Federer {sum(1 for r in s5 if r['PointWinner']=='2')}.")
pr('')

# ---------------------------------------------------------------- championship points
pr('## T10. The two championship points: Federer serving at 8-7 (set 5, R: SetNo 5, GameNo 16; games 7-8 Dj-Fe before the game; PointServer=2), at 40-15 and 40-30')
cp_game = [(i, r) for i, r in enumerate(R, 1) if r['SetNo']=='5' and r['GameNo']=='16']
assert all(r['PointServer']=='2' for _, r in cp_game) and cp_game[0][1]['P1GamesWon']=='7' and cp_game[0][1]['P2GamesWon']=='8'
pr('Whole game (every point):')
pr('| pt | clock | score before (Dj-Fe) | serve km/h (no.) | winner | R RallyCount | MCP code -> ending | R flags | TennisVL (n_shots, outcome, hit times) | commentary |')
pr('|---|---|---|---|---|---|---|---|---|---|')
for i, r in cp_game:
    p = P[i-1]
    flags = ','.join(k.replace('P1','Dj:').replace('P2','Fe:') for k in ('P1Ace','P2Ace','P1DoubleFault','P2DoubleFault','P1Winner','P2Winner','P1UnfErr','P2UnfErr','P1NetPoint','P2NetPoint','P1BreakPoint','P1BreakPointWon','P1BreakPointMissed') if r[k]=='1')
    tv = f"{p['tv_n_shots'] or '-'}, {p['tv_point_outcome'] or '-'}, {p['tv_hit_times'] or '-'}"
    pr(f"| {i} | {r['ElapsedTime']} | {p['pts_before_p1']}-{p['pts_before_p2']} | {r['Speed_KMH']} ({r['ServeNumber']}) | {NAME[r['PointWinner']]} | {r['RallyCount']} | {mcp_desc(p)} | {flags} | {tv} | {commentary(i, 15)} |")
pr('')
pr('Full MCP shot codes and TennisVL shot lists of the two championship points and the two break points that followed:')
for i, r in cp_game:
    p = P[i-1]
    if p['pts_before_p2'] == '40' or r['P1BreakPoint'] == '1':
        pr(f"* point {i} ({r['ElapsedTime']}, {p['pts_before_p1']}-{p['pts_before_p2']} Dj-Fe): MCP 1st=`{p['mcp_1st']}` 2nd=`{p['mcp_2nd'] or '-'}`; MCP winner {MCPNAME[M[i-1]['PtWinner']]}; R winner {NAME[r['PointWinner']]}; R ServeWidth={r['ServeWidth']} ServeDepth={r['ServeDepth']} ReturnDepth={r['ReturnDepth']}; distance run Dj {r['P1DistanceRun']} Fe {r['P2DistanceRun']}.")
        shots = [s for s in S if s['point_idx'] == str(i)]
        for s in shots:
            pr(f"    - TV shot {s['shot_index']} {s['hitter'].split()[-1]}: {s['type']} {s['wing'] or ''} {s['technique'] or ''} {s['direction_rough'] or ''} hit {s['hit_timestamp_second']}s outcome {s['shot_outcome']} (clip {s['clip'].split('_')[-2]}_{s['clip'].split('_')[-1]})")
        for u, role, cs, txt in clips_for(i):
            pr(f"    - transcript {u} ({role}, video {cs:.2f}s): \"{excerpt(txt, None, 15)}\"  [full length {len(txt.split())} words]")
pr('')

# ---------------------------------------------------------------- the break and the break back in set 5
pr('## T11. Breaks of serve in the fifth set (R: GameWinner != PointServer, non-tie-break games)')
for g in sorted(games):
    rows = games[g]; first, last = rows[0][1], rows[-1][1]
    if g != 25 and last['GameWinner'] != first['PointServer']:
        pr(f"* Game {g} (set-5 game {g-g5first+1}): {NAME[first['PointServer']]} serving at {first['P1GamesWon']}-{first['P2GamesWon']} (Dj-Fe); broken by {NAME[last['GameWinner']]}; clock {first['ElapsedTime']} to {last['ElapsedTime']}; games after {last['P1GamesWon']}-{last['P2GamesWon']}.")
        for i, r in rows:
            p = P[i-1]
            pr(f"    - pt {i} {r['ElapsedTime']} {p['pts_before_p1']}-{p['pts_before_p2']} serve {r['Speed_KMH']}({r['ServeNumber']}) -> {NAME[r['PointWinner']]}; MCP {mcp_desc(p)}; {commentary(i, 15)}")
pr('')

# ---------------------------------------------------------------- 12-12 tie-break
tb_table('5', '25', 'T12. The 12-12 tie-break (R: SetNo 5, GameNo 25), point by point with the clock')

# ---------------------------------------------------------------- final point
pr('## T13. The final point')
i = 422; r = R[-1]; p = P[-1]
pr(f"Point {i}: clock {r['ElapsedTime']}; score before {p['pts_before_p1']}-{p['pts_before_p2']} (Dj-Fe) in the tie-break, games 12-12; server {NAME[r['PointServer']]}, serve {r['Speed_KMH']} km/h ({r['Speed_MPH']} mph), serve number {r['ServeNumber']} (ServeWidth {r['ServeWidth']}, ServeDepth {r['ServeDepth']}, ReturnDepth {r['ReturnDepth']}); winner {NAME[r['PointWinner']]}; R RallyCount {r['RallyCount']}; R flags: P2UnfErr={r['P2UnfErr']} (Federer unforced error); MCP 1st=`{p['mcp_1st']}` 2nd=`{p['mcp_2nd']}` -> {mcp_desc(p)}; MCP shots {p['mcp_n_shots']}; distance run Dj {r['P1DistanceRun']} Fe {r['P2DistanceRun']}.")
for s in [s for s in S if s['point_idx'] == '422']:
    pr(f"    - TV shot {s['shot_index']} {s['hitter'].split()[-1]}: {s['type']} {s['wing'] or ''} {s['technique'] or ''} {s['direction_rough'] or ''} hit {s['hit_timestamp_second']}s outcome {s['shot_outcome']}")
for u, role, cs, txt in clips_for(422):
    pr(f"    - transcript {u} ({role}, video {cs:.2f}s): \"{excerpt(txt, None, 15)}\" [full length {len(txt.split())} words]")
pr('')

# ---------------------------------------------------------------- transcript coverage and typical-scene material
pr('## T14. Transcript coverage (T)')
n_txt = sum(1 for t in T if (t['text_corrected'] or '').strip())
pr(f"{len(T)} clip records; {n_txt} with non-empty text_corrected; first clip starts at video {min(t['clip_start_s'] for t in T):.2f} s (point {T[0]['point_idx_pbp']}), last clip at {max(t['clip_start_s'] for t in T):.2f} s. Words (text_corrected): {sum(len((t['text_corrected'] or '').split()) for t in T)}.")
pr('The clips are rally/serve clips only: there is no footage or transcript of the walk-on, warm-up, coin toss or trophy ceremony in this corpus (see search results below).')
pr('')
pr('## T15. Keyword search in text_corrected (typical-scene material). Excerpt <= 15 words around the first hit; score_before and clock from the record.')
KW = {
 'walk-on / warm-up / toss / umpire': r'\b(walk|warm[- ]?up|coin|toss|umpire|chair|steiner)\b',
 'Royal Box / royalty / celebrities': r'\b(royal|duchess|prince|princess|kate|meghan|box)\b',
 'crowd': r'\b(crowd|applause|cheer|cheering|roar|noise|chant|standing ovation|ovation|fans|centre court|centre-court)\b',
 'weather / roof / sun / shadow / wind / heat': r'\b(roof|sun|sunshine|shadow|shade|wind|breeze|hot|heat|warm|cloud|rain|weather|humid|temperature|light)\b',
 'trophy / ceremony / presentation': r'\b(trophy|trophies|ceremon\w*|presentation|speech|winner\'?s|runner-up|plate|cup)\b',
 'history / records / titles': r'\b(history|historic|record|longest|oldest|sixteenth|16th|fifth title|grand slam|grand slams|titles?|100)\b',
 'rituals: new balls, towel, ball kids, changeover, racket': r'\b(new balls|towel|ball ?(boy|girl|kid)s?|changeover|change of ends|bounces?|bouncing|racket|racquet|strings?|shoes|water|banana)\b',
 'line calls / challenge / Hawk-Eye / umpire calls': r'\b(challenge\w*|hawk-?eye|called|call|line judge|replay|overrule\w*|let\b|fault)\b',
 'Boris': r'\bboris\b',
 'Tim': r'\btim\b',
 'grass / court / lines / net': r'\b(grass|baseline|line|lines|net|court|chalk|tramline)\b',
 'serve / ace / second serve': r'\b(ace|aces|serve|serving|second serve|first serve)\b',
 'break / championship point / match point': r'\b(break point|break points|championship point|championship points|match point|set point)\b',
 'time / clock / hours / length': r'\b(hour|hours|minutes|clock|longest|four hours|five hours)\b',
 'tiredness / legs / fatigue / cramp': r'\b(tired|fatigue|legs|cramp|exhaust|energy|heavy)\b',
 'quiet / silence': r'\b(quiet|silence|silent|hush)\b',
}
for label, pat in KW.items():
    hits = [t for t in T if re.search(pat, t['text_corrected'] or '', re.I)]
    pr(f"### {label}: {len(hits)} clip(s)")
    for t in hits[:12]:
        sb = t['score_before']; pts = sb.get('points', {})
        sc = f"s{t['set_no']} {sb['games'].get('DJOKOVIC','?')}-{sb['games'].get('FEDERER','?')} {pts.get('DJOKOVIC','?')}-{pts.get('FEDERER','?')} (Dj-Fe) srv {str(sb.get('server','?')).split()[-1]}"
        clk = hms(t['elapsed_this_point_s']) if t.get('elapsed_this_point_s') is not None else '-'
        pr(f"* {t['utt_id']} clip_i {t['clip_i']} video {t['clip_start_s']:.1f}s, PBP pt {t['point_idx_pbp']}, clock {clk}, {sc}: \"{excerpt(t['text_corrected'], pat)}\"")
    if len(hits) > 12:
        pr(f"* … {len(hits)-12} more")
pr('')

# names of the commentators' addressees
pr('## T16. Address terms in the transcript (whole-word counts over text_corrected)')
for w in ['Boris', 'Tim', 'Andrew', 'John', 'Henman', 'Becker', 'Castle', 'McEnroe']:
    n = sum(len(re.findall(rf'\b{w}\b', t['text_corrected'] or '', re.I)) for t in T)
    pr(f"* {w}: {n}")
pr('')

# first and last transcribed clips
pr('## T17. The first five and last five transcribed clips (chronological), <= 15 words each')
tt = [t for t in T if (t['text_corrected'] or '').strip()]
for t in tt[:5] + tt[-5:]:
    pr(f"* {t['utt_id']} video {t['clip_start_s']:.1f}s PBP pt {t['point_idx_pbp']} clock {hms(t['elapsed_this_point_s']) if t.get('elapsed_this_point_s') is not None else '-'}: \"{excerpt(t['text_corrected'])}\"")
pr('')

# ---------------------------------------------------------------- game count, service games, match summary
pr('## T18. Miscellany')
pr(f"Games in match (R: distinct (SetNo, GameNo)): {len(set((r['SetNo'], r['GameNo']) for r in R))}; tie-breaks: 3 (sets 1, 3, 5).")
pr(f"Points per set: " + ', '.join(f"set {s}: {len(set_rows[s])}" for s in sorted(set_rows)) + '.')
rc_adj = [int(r['RallyCount']) + (1 if (r['P1UnfErr']=='1' or r['P2UnfErr']=='1' or r['P1DoubleFault']=='1' or r['P2DoubleFault']=='1') else 0) for r in R]
pr(f"Mean RallyCount (R, raw) {statistics.mean(int(r['RallyCount']) for r in R):.2f}; points with RallyCount 0 or 1 (serve not returned in play or DF): {sum(1 for r in R if int(r['RallyCount'])<=1)}.")
# serve-and-volley / net
pr(f"Net points (R): Djokovic {sum(int(r['P1NetPoint']) for r in R)} (won {sum(int(r['P1NetPointWon']) for r in R)}), Federer {sum(int(r['P2NetPoint']) for r in R)} (won {sum(int(r['P2NetPointWon']) for r in R)}).")
d1 = sum(float(r['P1DistanceRun']) for r in R); d2 = sum(float(r['P2DistanceRun']) for r in R)
pr(f"Sum of DistanceRun (R, unit unlabelled, presumably metres): Djokovic {d1:.0f}, Federer {d2:.0f}.")
# set 2 and 4 narrative: who broke when
pr('Breaks of serve, whole match (R; set, match game no., server, broken by, clock of the game\'s last point):')
for i, r in enumerate(R, 1):
    if r['GameWinner'] != '0' and r['GameWinner'] != r['PointServer'] and not (r['SetWinner'] != '0' and r['GameNo'] in ('13','25') and r['SetNo'] in ('1','3','5')):
        pr(f"* set {r['SetNo']} game {r['GameNo']}: {NAME[r['PointServer']]} serving, broken by {NAME[r['GameWinner']]} at {r['ElapsedTime']}; games after {r['P1GamesWon']}-{r['P2GamesWon']} (Dj-Fe); {commentary(i, 15)}")
# match metadata from MCP matches file
mm = [r for r in csv.DictReader(open(f'{ROOT}/corpus/raw/sackmann_mcp/charting-m-matches.csv', encoding='utf-8', errors='replace')) if r['match_id'] == '20190714-M-Wimbledon-F-Roger_Federer-Novak_Djokovic']
if mm:
    r = mm[0]
    pr(f"MCP matches file: date {r['Date']}, tournament {r['Tournament']}, round {r['Round']}, time {r['Time']}, court {r['Court']}, surface {r['Surface']}, umpire {r['Umpire']}, best of {r['Best of']}, final TB {r['Final TB?']}, charted by {r['Charted by']}; players {r['Player 1']} (1) and {r['Player 2']} (2), handedness {r['Pl 1 hand']}/{r['Pl 2 hand']}.")
print('\n'.join(out))
