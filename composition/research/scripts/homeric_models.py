#!/usr/bin/env python3
"""Generate composition/research/homeric_models.md.  Every citation and line is produced by
homer/concordance.py (Concordance class), homer/lines.tsv + homer/scansion.tsv, homer/ngrams.tsv,
and homer/check_line.py / scan.py (subprocess).  Prose is in NOTES.
Run from the repository root with the venv active:  python scratchpad/homeric_models.py > composition/research/homeric_models.md
"""
import csv, json, re, subprocess, sys, unicodedata
from collections import Counter, defaultdict
sys.path.insert(0, '/home/user/parry-wimbledon/homer')
from concordance import Concordance, loose_query

ROOT = '/home/user/parry-wimbledon'
C = Concordance()
LINES = {}
ORDER = []
for r in csv.DictReader(open(f'{ROOT}/homer/lines.tsv', encoding='utf-8'), delimiter='\t'):
    LINES[(r['work'], r['book'], r['line'])] = r['text']; ORDER.append((r['work'], r['book'], r['line']))
SC = {(r['work'], r['book'], r['line']): r for r in csv.DictReader(open(f'{ROOT}/homer/scansion.tsv', encoding='utf-8'), delimiter='\t')}
NG = list(csv.DictReader(open(f'{ROOT}/homer/ngrams.tsv', encoding='utf-8'), delimiter='\t'))
LOOSE_INDEX = defaultdict(list)
for k, t in LINES.items():
    LOOSE_INDEX[loose_query(t)].append(k)

out = []
pr = out.append
def cite(k): return f'{k[0]}. {k[1]}.{k[2]}'

def fmt(h):
    return f'{h.citation:<12} [{h.pos_start or "-"}-{h.pos_end or "-"}]  {h.text}    <{h.match}>'

def shape_of(h):
    """L/S shape of the matched words from scansion.tsv word_meter (X = final anceps, 0 = vowel-less elided word)."""
    sc = SC.get((h.work, h.book, h.line))
    if not sc or not sc['word_meter']: return '-'
    wm = sc['word_meter'].split()
    return ' '.join(wm[h.tok_start:h.tok_end + 1])

def run(kind, q, work=None):
    if kind == 'ngram': return C.ngram(q, work=work)
    if kind == 'loose': return C.loose(q, word=True, work=work)
    if kind == 'loosesub': return C.loose(q, word=False, work=work)
    if kind == 'exact': return C.exact(q, word=False, work=work)
    if kind == 'regex': return C.regex(q, on='text', work=work)
    raise ValueError(kind)

def show(kind, q, limit=2, work=None, note=None, shape=False, pos=True):
    hits = run(kind, q, work)
    cmd = {'ngram': f'--ngram "{q}"', 'loose': f'--loose "{q}" --word', 'loosesub': f'--loose "{q}"', 'exact': f'--exact "{q}"', 'regex': f'--regex "{q}"'}[kind]
    if work: cmd += f' --work {work}'
    dist = Counter(f'{h.pos_start}-{h.pos_end}' for h in hits)
    pr(f'`{cmd}` : **{len(hits)} hit(s)**' + (f'; positions {dict(dist.most_common(4))}' if pos and hits else '') + (f' -- {note}' if note else ''))
    pr('```')
    for h in hits[:limit]:
        pr(fmt(h) + (f'  shape {shape_of(h)}' if shape else ''))
    if len(hits) > limit: pr(f'... {len(hits)-limit} more')
    pr('```')
    return hits

def lines(work, book, a, b, dup=False):
    pr('```')
    for n in range(a, b + 1):
        k = (work, book, str(n))
        if k not in LINES: pr(f'{cite(k)}  (absent)'); continue
        sc = SC.get(k, {})
        s = f"{cite(k):<12} {LINES[k]}    [{sc.get('pattern','-')}; {sc.get('word_positions','-')}]"
        if dup:
            others = [cite(x) for x in LOOSE_INDEX[loose_query(LINES[k])] if x != k]
            if others: s += f'    = {", ".join(others)}'
        pr(s)
    pr('```')

def dups(work, book, a, b, title):
    rows = []
    for n in range(a, b + 1):
        k = (work, book, str(n))
        if k not in LINES: continue
        others = [cite(x) for x in LOOSE_INDEX[loose_query(LINES[k])] if x != k]
        if others: rows.append((k, others))
    pr(f'Lines of {title} that recur verbatim elsewhere (whole line identical in loose form; lines.tsv): {len(rows)} of {b-a+1}')
    pr('```')
    for k, others in rows:
        pr(f'{cite(k):<12} {LINES[k]}    = {", ".join(others)}')
    pr('```')

def check(line):
    j = json.loads(subprocess.run([sys.executable, f'{ROOT}/homer/check_line.py', '--json', line], capture_output=True, text=True).stdout)
    v = j['verses'][0]
    s = json.loads(subprocess.run([sys.executable, f'{ROOT}/homer/scan.py', '--json', line], capture_output=True, text=True).stdout)
    an = s['analyses'][0] if s.get('analyses') else None
    def _s(x):
        if isinstance(x, dict): return ':'.join(str(x.get(k)) for k in ('type', 'detail') if x.get(k) is not None)
        return str(x)
    res = f'`{line}`\n    check_line: status={v["status"]} tier={v["tier"]} n_scansions={v["n_scansions"]} flags={[_s(f) for f in v["flags"]]} warnings={[_s(w) for w in v["warnings"]]}'
    if an:
        res += f'\n    scan: pattern {an["pattern"]}; words {list(zip(an["syllables"], an["word_meter"], an["word_positions"]))}; licences {an["licences"]}'
    pr(res)

STOP = set('δʼ τʼ δ τ και δε τε ο η οι αι ος ον τον την τω τους γαρ αρ ρα αρα μεν μην αυταρ ατ αυτ αλλ αλλα εν επι ουδ ουδε ουτ ουτε ουδ ως ουτ ου ουκ ουχ μιν οι σφι σφιν ποτε κεν αν κε περ γε τοι τις τι ηδε ιδε εις ες εκ εξ προς υπο αμφι παρα παρ μετα μετ επ απο απ υπ κατα κατ δια ουν τοτε ετι ει ην οτε δη ουν ουτω ου νυ νυν τω τα το τους ταις τη τον ος ο η οι εμε εμοι με μοι σε σοι εγω συ ε ευ ουδ αμα ενθα ενθ εφ αφ μετ κατ'.split())

def name_system(title, forms, min_count=2, limit=40, nmax=3):
    forms = set(forms)
    rows = []
    for r in NG:
        n = int(r['n'])
        if n > nmax: continue
        words = r['ngram_loose'].split()
        if not (forms & set(words)): continue
        others = [w for w in words if w not in forms]
        if not others or any(w in STOP or len(w) < 3 for w in others): continue
        if int(r['count']) < min_count: continue
        rows.append(r)
    rows.sort(key=lambda r: (-int(r['count']), int(r['n'])))
    pr(f'**{title}** (homer/ngrams.tsv: n-grams of 2-{nmax} words containing the name, no particles/pronouns, count >= {min_count}; shape from scansion.tsv word_meter of the first attestation; L = long, S = short, X = final anceps)')
    pr('| formula (commonest spelling) | n | count | lines | main position (share) | shape | first citations |')
    pr('|---|---|---|---|---|---|---|')
    for r in rows[:limit]:
        hits = C.ngram(r['form'])
        shp = shape_of(hits[0]) if hits else '-'
        pr(f"| {r['form']} | {r['n']} | {r['count']} | {r['lines']} | {r['main_position']} ({float(r['main_position_share']):.2f}) | {shp} | {'; '.join(r['citations'].split('; ')[:3])} |")
    if len(rows) > limit: pr(f'| ... {len(rows)-limit} more rows omitted | | | | | | |')
    pr('')
    return rows

sys.path.insert(0, '/tmp/claude-0/-home-user-parry-wimbledon/37924bc3-6959-57e3-80e8-68de1b53f277/scratchpad')
from hm_notes import NOTES
def note(key):
    if key in NOTES: pr(NOTES[key]); pr('')

# =====================================================================================
pr('# Homeric models for the composition (concordance-verified)')
pr('')
pr('Generated by `scratchpad/homeric_models.py` (copy at the end of this file) from `homer/lines.tsv`, `homer/scansion.tsv`, `homer/ngrams.tsv` through the `Concordance` class of `homer/concordance.py`, and from `homer/check_line.py` / `homer/scan.py` for the test lines of section (i). Nothing Homeric below is quoted from memory: every line is printed from the Perseus text (Monro-Allen Iliad, Murray Odyssey; see homer/README.md) and every citation is a tool hit. Metrical positions are the half-foot numbers of homer/README.md: the longum of foot f is 2f-1, its biceps 2f (first short 2f-0.5); word end at 5 = penthemimeral caesura, 5.5 = trochaic, 7 = hephthemimeral, 8 = bucolic diaeresis; 12 = the last syllable. Each hit is printed as `citation [start-end] full line <matched words>`; `positions {...}` is the distribution of start-end over all hits. Scansion patterns D/S are feet 1-5. The text uses U+02BC for elision; queries use the plain apostrophe.')
pr('')
pr('Scholarship: this file cites no secondary literature. Standard references the composer may want (Parry 1928 on the noun-epithet systems; Arend 1933 on typical scenes; Fenik 1968 on battle scenes; Scott 1974 and Moulton 1977 on similes; Richardson 1993 on Il. 23; Hainsworth 1993 on Il. 11; Edwards 1991 on Il. 16-20) are **[unverified]** here, named only so that the paper can fetch them.')
pr('')

# ---------------------------------------------------------------- (a)
pr('## (a) Proem models')
pr('')
pr('Il. 1.1-7 and Od. 1.1-10 (homer/lines.tsv; pattern and word positions from homer/scansion.tsv):')
lines('Il', '1', 1, 7)
lines('Od', '1', 1, 10)
pr('Invocation formulae, all occurrences:')
show('ngram', 'μῆνιν ἄειδε', shape=True)
show('ngram', "ἄνδρα μοι ἔννεπε", shape=True)
show('ngram', 'ἔννεπε μοῦσα', shape=True)
show('ngram', 'ἔσπετε νῦν μοι μοῦσαι', shape=True)
show('ngram', 'ἔσπετε νῦν μοι μοῦσαι ὀλύμπια δώματ᾽ ἔχουσαι', limit=4)
pr('The line that follows each of the four invocations:')
lines('Il', '2', 485, 485); lines('Il', '11', 219, 219); lines('Il', '14', 509, 509); lines('Il', '16', 113, 113)
show('loose', 'μουσα', limit=3, note='all forms Μοῦσα (nom./voc.)')
show('loose', 'μουσαι', limit=3)
show('loose', 'αειδε', limit=4, note='imperative/imperfect ἄειδε')
show('ngram', 'θεὰ θύγατερ διός', shape=True)
show('ngram', 'εἰπὲ καὶ ἡμῖν', shape=True)
show('ngram', 'διὸς δ᾽ ἐτελείετο βουλή', shape=True)
show('ngram', 'ὃς μάλα πολλὰ', shape=True)
show('ngram', 'ἐξ οὗ δὴ', shape=True)
note('a')

# ---------------------------------------------------------------- (b)
pr('## (b) The arming typical scene')
pr('')
pr('The four arming scenes printed with, for each line, the other places where the same line recurs verbatim (`= ...`).')
pr('Il. 3.330-338 (Paris):')
lines('Il', '3', 330, 338, dup=True)
pr('Il. 11.17-45 (Agamemnon): only the lines that recur verbatim elsewhere (the full scene is 29 lines):')
dups('Il', '11', 17, 45, 'Il. 11.17-45')
pr('Il. 16.131-144 (Patroclus):')
lines('Il', '16', 131, 144, dup=True)
pr('Il. 19.369-391 (Achilles): only the lines that recur verbatim elsewhere (23 lines in all):')
dups('Il', '19', 369, 391, 'Il. 19.369-391')
pr('The shared formulae, each with all its occurrences and positions:')
show('ngram', 'κνημῖδας μὲν πρῶτα', shape=True)
show('ngram', 'περὶ κνήμῃσιν ἔθηκε', shape=True)
show('ngram', 'δεύτερον αὖ θώρηκα', shape=True)
show('ngram', 'περὶ στήθεσσιν ἔδυνε', shape=True)
show('ngram', "ἀμφὶ δ᾽ ἄρ᾽ ὤμοισιν βάλετο ξίφος", shape=True)
show('ngram', "βάλετο ξίφος ἀργυρόηλον", shape=True)
show('ngram', "κρατὶ δ᾽ ἐπ᾽ ἰφθίμῳ κυνέην", shape=True)
show('ngram', "κυνέην εὔτυκτον ἔθηκεν", shape=True)
show('ngram', "εἵλετο δ᾽ ἄλκιμα δοῦρε", shape=True)
show('ngram', "εἵλετο δ᾽ ἄλκιμον ἔγχος", shape=True)
show('ngram', "ἵππουριν δεινὸν δὲ λόφος καθύπερθεν ἔνευεν", shape=True)
show('ngram', "ὅ οἱ παλάμηφιν ἀρήρει", shape=True)
show('ngram', "ἀσπίδα θοῦριν", shape=True)
show('ngram', "ἀμφὶ δ᾽ ἄρ᾽ ὤμοισιν", shape=True, limit=10)
note('b')

# ---------------------------------------------------------------- (c)
pr('## (c) The duel typical scene')
pr('')
pr('Il. 3.340-349 (Paris-Menelaus: approach, cast, miss/no-miss), with verbatim repeats:')
lines('Il', '3', 340, 349, dup=True)
pr('Il. 7.244-254 (Hector-Ajax, the exchange of casts):')
lines('Il', '7', 244, 254, dup=True)
pr('Il. 7.299-305 (the exchange of gifts):')
lines('Il', '7', 299, 305, dup=True)
pr('Il. 7.274-282 (the heralds stop the duel at nightfall):')
lines('Il', '7', 274, 282, dup=True)
pr('Il. 22.273-277 and 22.289-291 (Achilles-Hector):')
lines('Il', '22', 273, 277, dup=True)
lines('Il', '22', 289, 291, dup=True)
dups('Il', '3', 340, 382, 'Il. 3.340-382')
dups('Il', '7', 206, 312, 'Il. 7.206-312')
dups('Il', '22', 248, 369, 'Il. 22.248-369 (the combat itself; 22.131-247 is mostly the gods\' dialogue and its repeats)')
pr('Recurrent duel formulae, counts and positions:')
show('ngram', "οἳ δ᾽ ὅτε δὴ σχεδὸν ἦσαν", shape=True)
show('ngram', "ἐπ᾽ ἀλλήλοισιν ἰόντες", shape=True)
show('ngram', "ἀλλ᾽ ὅτε δὴ", limit=2, shape=True)
show('ngram', "ἦ ῥα καὶ ἀμπεπαλὼν", shape=True)
show('ngram', "προΐει δολιχόσκιον ἔγχος", shape=True)
show('ngram', "καὶ βάλεν", limit=4, shape=True)
show('ngram', "οὐδ᾽ ἀφάμαρτε", shape=True)
show('ngram', "ἤμβροτες οὐδ᾽ ἔτυχες", shape=True)
show('loose', 'κληρους', shape=True)
show('loose', 'κληρον', limit=1, shape=True)
show('ngram', "θάμβος δ᾽ ἔχεν", limit=2, shape=True)
show('ngram', "ἐν κυνέῃ", shape=True)
show('ngram', "χῶρον μὲν πρῶτον διεμέτρεον", shape=True)
note('c')

# ---------------------------------------------------------------- (d)
pr('## (d) Athletic contest scenes (Il. 23.262-897; Od. 8.100-233)')
pr('')
pr('Key lines printed from the text:')
pr('Il. 23.262-264 (the first prize announcement):'); lines('Il', '23', 262, 264, dup=True)
pr('Il. 23.358-361 (the line-up, the turning post and the umpire):'); lines('Il', '23', 358, 361, dup=True)
pr('Il. 23.448-451 (the spectators; Idomeneus seated highest):'); lines('Il', '23', 448, 451, dup=True)
pr('Il. 23.735-737 (the wrestling draw of Ajax and Odysseus):'); lines('Il', '23', 735, 737, dup=True)
pr('Il. 23.757-759 (the footrace start):'); lines('Il', '23', 757, 759, dup=True)
pr('Il. 23.773-779 (Athena trips Ajax; Odysseus wins):'); lines('Il', '23', 773, 779, dup=True)
pr('Il. 23.822-825 (the armed duel stopped by the Achaeans):'); lines('Il', '23', 822, 825, dup=True)
pr('Il. 23.845-849 and 23.869-870 (the shot and the archery):'); lines('Il', '23', 845, 849, dup=True); lines('Il', '23', 869, 870, dup=True)
pr('Od. 8.120-125 (the Phaeacian footrace):'); lines('Od', '8', 120, 125, dup=True)
pr('Od. 8.145-148 (the glory of hands and feet):'); lines('Od', '8', 145, 148, dup=True)
pr('Od. 8.186-193 (Odysseus throws the discus):'); lines('Od', '8', 186, 193, dup=True)
pr('Od. 8.233 (limbs loosened by the sea):'); lines('Od', '8', 233, 233)
pr('Formulae of contest:')
show('loosesub', 'αεθλ', limit=0, note='all forms of ἄεθλον, ἄεθλος, ἀεθλεύω, ἀεθλοφόρος')
show('loose', 'αεθλα', limit=4, shape=True)
show('loose', 'αεθλον', limit=3, shape=True)
show('ngram', "θῆκεν ἄεθλα", shape=True)
show('loosesub', 'νυσσ', limit=3, shape=True, note='νύσσα (also τανύσσ-, γένυσσ-: substring), the turning post / start line')
show('loose', 'νυσση', limit=2, shape=True)
show('loosesub', 'τερμα', limit=8, shape=True, note='τέρμα, the goal / turning mark')
show('ngram', "ἐπὶ ἶσα", shape=True)
show('loosesub', 'νικη', limit=3, shape=True, note='νίκη, νίκης, νίκην, νικάω ...')
show('ngram', "νίκης ἱέσθην", shape=True)
show('ngram', "ὦκα δ᾽", limit=4, shape=True)
show('loosesub', 'επηπυ', shape=True)
show('loose', 'θηευντο', shape=True)
show('ngram', "θηεῦντό τε θάμβησάν τε", shape=True)
show('ngram', "ἐν ἀγῶνι", limit=3, shape=True)
show('ngram', "εὐρὺν ἀγῶνα", shape=True)
show('ngram', "ἐπὶ δ᾽ ἴαχε λαὸς", shape=True)
show('ngram', "περὶ νίκης", limit=3, shape=True)
show('ngram', "τοῖσι δ᾽ ἀπὸ νύσσης", shape=True)
show('ngram', "τέτατο δρόμος", shape=True)
show('ngram', "βόμβησεν δὲ λίθος", shape=True)
show('ngram', "ἧκε στιβαρῆς ἀπὸ χειρός", shape=True)
show('ngram', "καὶ χερσὶν ἑῇσιν", shape=True)
show('loosesub', 'αθλητ', limit=1, shape=True)
show('ngram', "χεῖρας ἀνέσχον", limit=4, shape=True)
show('loose', 'κελαδησαν', limit=2, shape=True)
show('loose', 'βοησαν', limit=3, shape=True)
note('d')

# ---------------------------------------------------------------- (e)
pr('## (e) Similes to model (full text, with scansion patterns)')
pr('')
SIM = [('Il', '12', 41, 48, 'lion/boar among hunters (Hector)'), ('Il', '20', 164, 173, 'the lion roused (Achilles)'),
       ('Il', '22', 139, 142, 'hawk and dove (Achilles pursues Hector)'), ('Il', '15', 690, 692, 'eagle on waterfowl (Hector)'),
       ('Il', '15', 618, 621, 'the rock in the sea (the Danaans hold)'), ('Il', '8', 69, 72, 'the golden scales of Zeus'),
       ('Il', '22', 209, 213, 'the scales for Hector and Achilles'), ('Il', '12', 421, 423, 'two men with measuring rods disputing a boundary'),
       ('Il', '12', 433, 435, 'the woman weighing wool'), ('Il', '6', 506, 511, 'the stalled horse breaks its tether (Paris)'),
       ('Il', '15', 263, 268, 'the same simile (Hector)'), ('Il', '22', 162, 166, 'prize-winning horses round the turning posts'),
       ('Od', '13', 31, 35, 'the ploughman longing for supper (Odysseus)'), ('Il', '22', 26, 32, 'the Dog Star (Achilles)'),
       ('Il', '4', 422, 426, 'waves on the shore (the Danaan ranks)'),
       ('Il', '16', 823, 826, 'lion and boar at a spring (Hector kills Patroclus)')]
for w, b, a, z, t in SIM:
    pr(f'{w}. {b}.{a}-{z} ({t}):'); lines(w, b, a, z, dup=True)
pr('Repetition check Il. 6.506-511 = 15.263-268: see the `=` marks above (every line of 6.506-511 is listed with its twin).')
pr('')
pr('Simile openers and closers, and the sun/time formulae:')
show('ngram', "ὡς δ᾽ ὅτε", limit=2, shape=True)
show('ngram', "ὡς δ᾽ ὅτε τις", limit=3, shape=True)
show('ngram', "ἠΰτε", limit=3, shape=True)
show('ngram', "ὣς οἳ μὲν", limit=2, shape=True)
show('ngram', "ὣς τοῦ", limit=2, shape=True)
show('ngram', "καὶ τότε δὴ χρύσεια πατὴρ ἐτίταινε τάλαντα", limit=2, shape=True)
show('ngram', "ἐν δ᾽ ἐτίθει δύο κῆρε τανηλεγέος θανάτοιο", limit=2, shape=True)
show('ngram', "δύσετό τ᾽ ἠέλιος", limit=3, shape=True)
show('ngram', "ἠέλιος μὲν ἔπειτα", shape=True)
show('ngram', "ἦμος δ᾽", limit=3, shape=True)
show('ngram', "ἠέλιος μέσον οὐρανὸν", limit=2, shape=True)
show('ngram', "μετενίσετο βουλυτὸν", limit=2, shape=True)
show('ngram', "ἦμος δ᾽ ἠριγένεια φάνη ῥοδοδάκτυλος ἠώς", limit=3, shape=True)
show('ngram', "λαμπρὸν φάος ἠελίοιο", shape=True)
show('ngram', "ἠέλιος δ᾽ ἄρ᾽ ἔδυ", shape=True)
show('ngram', "δείελον ἦμαρ", shape=True)
show('ngram', "βουλυτόνδε", shape=True)
show('ngram', "σκιόωντό τε πᾶσαι ἀγυιαί", limit=1, shape=True)
show('ngram', "ὀψὲ δὲ δὴ", limit=2, shape=True)
note('e')

# ---------------------------------------------------------------- (f)
pr('## (f) Aristeia markers')
pr('')
pr('Il. 5.1-8:'); lines('Il', '5', 1, 8, dup=True)
pr('Il. 11.15-16 and 11.44-46:'); lines('Il', '11', 15, 16, dup=True); lines('Il', '11', 44, 46, dup=True)
pr('Il. 16.130-131:'); lines('Il', '16', 130, 131, dup=True)
pr('Il. 18.203-206 and 18.225-227 (the flame over Achilles):'); lines('Il', '18', 203, 206, dup=True); lines('Il', '18', 225, 227, dup=True)
show('ngram', "τοῖόν οἱ πῦρ δαῖεν", shape=True)
show('ngram', "ἀκάματον πῦρ", limit=3, shape=True)
show('ngram', "ἔνθα τίνα πρῶτον", shape=True)
show('ngram', "τίνα δ᾽ ὕστατον", shape=True)
show('ngram', "ἀστέρ᾽ ὀπωρινῷ ἐναλίγκιον", shape=True)
show('ngram', "δαῖέ οἱ ἐκ κόρυθός τε καὶ ἀσπίδος", shape=True)
show('loose', 'λαμπε', limit=6, shape=True)
show('ngram', "μένος καὶ θάρσος", shape=True)
show('ngram', "ἐν δὲ σθένος ὦρσεν", shape=True)
note('f')

# ---------------------------------------------------------------- (g)
pr('## (g) Crowd and assembly formulae')
pr('')
show('ngram', "ὣς ἔφαθ᾽ οἳ δ᾽ ἄρα πάντες ἀκὴν ἐγένοντο σιωπῇ", limit=4, shape=True)
show('ngram', "ἀκὴν ἐγένοντο σιωπῇ", limit=3, shape=True)
show('ngram', "ὣς ἔφαθ᾽ οἳ δ᾽ ἄρα πάντες", limit=0)
show('loose', 'λαοι', limit=2, shape=True)
show('loose', 'λαος', limit=1, shape=True)
show('loose', 'λαον', limit=1, shape=True)
show('loose', 'λαων', limit=1, shape=True)
show('loose', 'ομιλος', limit=5, shape=True)
show('loose', 'ομιλον', limit=2, shape=True)
show('loose', 'ομιλω', limit=1, shape=True)
show('loose', 'πληθυς', limit=1, shape=True)
show('loose', 'ομαδος', limit=1, shape=True)
show('loosesub', 'οχλ', limit=5, shape=True, note='ὄχλος does not occur in Homer; only the verb ὀχλέω/ὀχλίζω')
show('loose', 'πληθυν', limit=4, shape=True)
show('loose', 'δημος', limit=4, shape=True)
show('loose', 'επιαχον', limit=3, shape=True)
show('ngram', "μέγ᾽ ἴαχον", limit=2, shape=True)
show('ngram', "μέγα ἴαχον", limit=2, shape=True)
show('ngram', "μέγα δ᾽ ἴαχε", limit=6, shape=True)
show('ngram', "μεγάλ᾽ ἴαχε", limit=6, shape=True)
show('ngram', "μεγάλ᾽ ἴαχον", limit=4, shape=True)
show('ngram', "ἤϋσεν δὲ διαπρύσιον", shape=True)
show('ngram', "μακρὸν ἄϋσε", limit=5, shape=True)
show('ngram', "ἀλαλητῷ", limit=5, shape=True)
show('ngram', "ἐπὶ δὲ στενάχοντο", shape=True)
show('ngram', "ἡδὺ γέλασσαν", shape=True)
show('ngram', "ἐπὶ δ᾽ ᾔνεον", shape=True)
show('loose', 'επηνησαν', limit=4, shape=True)
show('ngram', "ἐπευφήμησαν ἀχαιοί", shape=True)
show('ngram', "ὣς ἔφαθ᾽ οἳ δ᾽ ἄρα πάντες ἐπίαχον", shape=True)
show('ngram', "κήρυκες δ᾽ ἄρα λαὸν ἐρήτυον", shape=True)
show('ngram', "θαῦμα ἰδέσθαι", limit=4, shape=True)
show('loose', 'ακην', limit=2, shape=True)
show('loose', 'σιωπη', limit=1, shape=True)
note('g')

# ---------------------------------------------------------------- (h)
pr('## (h) Name-epithet systems (data-driven from homer/ngrams.tsv)')
pr('')
pr('Method: all n-grams of 2-3 words (within a line, loose form, count >= 2 in homer/ngrams.tsv) that contain the name form and no particle, pronoun or article (stoplist in the script). The remaining rows are noun-epithet groups or noun + verb groups; the composer should take the epithet rows. Shape is read from scansion.tsv for the first attestation. Oblique cases: the commonest rows only (count >= 3).')
pr('')
for title, nom, obl in [
    ('Achilles', ['Ἀχιλλεύς', 'Ἀχιλεύς'], ['Ἀχιλλῆος', 'Ἀχιλῆος', 'Ἀχιλλῆϊ', 'Ἀχιλῆϊ', 'Ἀχιλλῆα', 'Ἀχιλῆα', 'Ἀχιλλεῦ', 'Ἀχιλεῦ']),
    ('Odysseus', ['Ὀδυσσεύς', 'Ὀδυσεύς'], ['Ὀδυσσῆος', 'Ὀδυσῆος', 'Ὀδυσσῆϊ', 'Ὀδυσῆϊ', 'Ὀδυσσῆα', 'Ὀδυσῆα', 'Ὀδυσσεῦ', 'Ὀδυσεῦ']),
    ('Hector', ['Ἕκτωρ'], ['Ἕκτορος', 'Ἕκτορι', 'Ἕκτορα', 'Ἕκτορ']),
    ('Diomedes', ['Διομήδης'], ['Διομήδεος', 'Διομήδεϊ', 'Διομήδεα', 'Διόμηδες']),
    ('Ajax', ['Αἴας'], ['Αἴαντος', 'Αἴαντι', 'Αἴαντα']),
    ('Menelaus', ['Μενέλαος'], ['Μενελάου', 'Μενελάῳ', 'Μενέλαον', 'Μενέλαε'])]:
    nom = [loose_query(x) for x in nom]; obl = [loose_query(x) for x in obl]
    name_system(f'{title}, nominative', nom, min_count=2, limit=10)
    name_system(f'{title}, oblique cases (gen./dat./acc./voc.)', obl, min_count=3, limit=6)
pr('(The vocative Αἶαν is omitted from the Ajax query: in loose form it coincides with αἶαν "earth"; the vocative formula Αἶαν διογενὲς Τελαμώνιε is checked directly below.)')
pr('')
pr('Generic epithet formulae usable for either player (positions and counts):')
for q in ['ἰσόθεος φώς', 'ὄρχαμος ἀνδρῶν', 'ποιμένα λαῶν', 'ἄναξ ἀνδρῶν']:
    show('ngram', q, limit=1, shape=True)
note('h')

# ---------------------------------------------------------------- (i)
pr('## (i) Greek renderings of the players\' names, with scansion tests')
pr('')
pr('Each candidate is tested inside an attested Homeric line in which it replaces a name or epithet of the same shape; the line is run through `homer/check_line.py --json` (status, flags, warnings) and `homer/scan.py --json` (word positions). The quantities of α ι υ in invented names are free (the scanner chooses) and are reported in the `scan:` line; a `warnings` entry about an unattested quantity is expected for invented words. An ethnic/adjective test uses the same method.')
pr('')
pr('Homeric ethnics and their shapes (for modelling "the Swiss" / "the Serb"):')
for q in ['θρηικ', 'θρηκ', 'δαρδανι', 'αχαιο', 'αργειο', 'φρυγ', 'αιγυπτι', 'σιδονι', 'βοιωτι', 'παιον']:
    show('loosesub', q, limit=2, shape=True)
pr('Patronymic and hero-name shapes used as slots below:')
for q in ['κρονιδ', 'πηλειδ', 'ατρειδ', 'τυδειδ']:
    show('loosesub', q, limit=2, shape=True)
show('ngram', "πηλεΐδης δ᾽ ἑτέρωθεν", shape=True)
show('ngram', "αἶαν διογενὲς τελαμώνιε", shape=True)
pr('')
TESTS = {
 'Federer 1: Φεδερῆρος (SSLX = the shape of Διομήδης, 9.5-12), in the Diomedes formula "βοὴν ἀγαθὸς Διομήδης" (Il. 4.401 pattern: τὸν δ᾽ οὔ τι προσέφη κρατερὸς Διομήδης)': [
    'ὣς φάτο, τὸν δ᾽ οὔ τι προσέφη κρατερὸς Φεδερῆρος',
    'τὸν δ᾽ ἠμείβετ᾽ ἔπειτα βοὴν ἀγαθὸς Φεδερῆρος',
    'Φεδερῆρος δ᾽ ἑτέρωθεν ἀνίστατο ἰσόθεος φώς',
    'ὣς φάτο, μείδησεν δὲ βοὴν ἀγαθὸς Φεδερῆρος',
 ],
 'Federer 2: Φεδερεύς, -ῆος (SSL / SSLX = the shape of Ὀδυσεύς single-sigma and of Ἀχιλῆος gen.): hero-name in -εύς': [
    'μῆνιν ἄειδε θεὰ Πηληϊάδεω Φεδερῆος',
    'διογενὴς Φεδερεύς, Διομήδεα δὲ προσέειπεν',
    'τὸν δ᾽ ἀπαμειβόμενος προσέφη πολύμητις Φεδερεύς',
 ],
 'Federer 3: Ῥογῆρος (SLX = the shape of Ὀδυσσεύς / Ἀχιλλεύς 10-12): initial ῥ lengthens a preceding short vowel, so the word cannot follow a short syllable': [
    'τὸν δ᾽ ἀπαμειβόμενος προσέφη πολύμητις Ῥογῆρος',
    'ὣς φάτο, τὸν δ᾽ οὔ τι προσέφη πόδας ὠκὺς Ῥογῆρος',
    'τὸν δ᾽ ἠμείβετ᾽ ἔπειτα Ῥογῆρος ἰσόθεος φώς',
    'ὣς φάτο, μείδησεν δὲ Ῥογῆρος, ἰσόθεος φώς',
 ],
 'Federer 4: Φεδερίδης / Φεδερείδης (patronymic shape): Φεδερίδης is SSSL and cannot scan; Φεδερείδης is SSLL = Διομήδης': [
    'ὣς φάτο, τὸν δ᾽ οὔ τι προσέφη κρατερὸς Φεδερίδης',
    'ὣς φάτο, τὸν δ᾽ οὔ τι προσέφη κρατερὸς Φεδερείδης',
    'τὸν δ᾽ ἠμείβετ᾽ ἔπειτα βοὴν ἀγαθὸς Φεδερείδης',
 ],
 'Swiss: Ἑλβέτιος (LSSX, the shape of Δαρδάνιος / Ἀτρεΐδης LSSL) and Ἑλουήτιος (SLLSX)': [
    'Ἑλβέτιος δὲ πρῶτος ἀκόντισε δουρὶ φαεινῷ',
    'τὸν δ᾽ ἠμείβετ᾽ ἔπειτα Ἑλβέτιος ἰσόθεος φώς',
    'Ἑλουήτιος δὲ πρῶτος ἀκόντισε δουρὶ φαεινῷ',
 ],
 'Djokovic 1: Νοβάκος with long α (SLX = Ὀδυσσεύς / Ἀχιλλεύς at 10-12); initial Ν makes position after a final consonant, so it cannot follow -ος/-ης/-υς epithets at 9.5': [
    'τὸν δ᾽ ἀπαμειβόμενος προσέφη πολύμητις Νοβάκος',
    'ὣς φάτο, μείδησεν δὲ μέγας κορυθαίολος Νοβάκος',
    'τὸν δ᾽ ἀπαμειβόμενος προσέφη ἀμύμων Νοβάκος',
    'ὣς ἔφατ᾽, οὐδ᾽ ἀπίθησε περικλυτὸς αὖτε Νοβάκος',
 ],
 'Djokovic 2: Νόβακος with short α (SSX): no line-end slot exists for S S X; the scanner can only lengthen the α (metre only) or the first syllable': [
    'ὣς φάτο, γήθησεν δὲ πολύτλας δῖος Νόβακος',
    'Νόβακος Πριαμίδης, ὅτε οἱ Ζεὺς κῦδος ἔδωκε',
 ],
 'Djokovic 3: patronymic from Đoko: Ζοκοβίδης (SSLL if ι is long as in Κρονίδης; SSSL and unmetrical if short as in Πηλεΐδης), Διοκοβίδης (SSSLL, needs an unattested long ι in Διο-), and the hero-name Ζοκοβεύς / Ζοκοβῆος (SSL / SSLX); ζ counts as two consonants': [
    'ὣς φάτο, τὸν δ᾽ οὔ τι προσέφη κρατερὸς Ζοκοβίδης',
    'τὸν δ᾽ ἠμείβετ᾽ ἔπειτα βοὴν ἀγαθὸς Ζοκοβίδης',
    'ὣς φάτο, τὸν δ᾽ οὔ τι προσέφη κρατερὸς Διοκοβίδης',
    'διογενὴς Ζοκοβεύς, Διομήδεα δὲ προσέειπεν',
    'μῆνιν ἄειδε θεὰ Πηληϊάδεω Ζοκοβῆος',
    'τὸν δ᾽ ἀπαμειβόμενος προσέφη πολύμητις Ζοκοβεύς',
 ],
 'Serb: Σέρβος (LX = Ἕκτωρ LL) and Σέρβιος (LSX; LSS before a vowel = a dactyl, LSL before a consonant = a cretic, impossible)': [
    'ὣς φάτο, τὸν δ᾽ οὔ τι προσέφη κορυθαίολος Σέρβος',
    'Σέρβος Πριαμίδης, ὅτε οἱ Ζεὺς κῦδος ἔδωκε',
    'ὣς ἔφατ᾽, οὐδ᾽ ἀπίθησε βοὴν ἀγαθὸς μέγα Σέρβος',
    'τοῖσι δ᾽ ἔπειθ᾽ ἥρως μὲν Σέρβιος ἦρχ᾽ ἀγορεύειν',
    'Σέρβιος ἀντίθεος, μέγα δὲ φρεσὶ θάρσος ἔχει μοι',
 ],
 'Attested control lines (should pass with no flags)': [
    'ὣς φάτο, τὸν δ᾽ οὔ τι προσέφη κρατερὸς Διομήδης',
    'τὸν δ᾽ ἀπαμειβόμενος προσέφη πολύμητις Ὀδυσσεύς',
    'διογενὴς Ὀδυσεύς, Διομήδεα δὲ προσέειπεν',
    'τοῖσι δ᾽ ἔπειθ᾽ ἥρως Αἰγύπτιος ἦρχ᾽ ἀγορεύειν',
    'ὣς φάτο, τὸν δ᾽ οὔ τι προσέφη κορυθαίολος Ἕκτωρ',
 ],
}
for title, ls in TESTS.items():
    pr(f'**{title}**')
    pr('```')
    for l in ls: check(l)
    pr('```')
pr('**Substitution tests: each name dropped into an attested line in place of a Homeric name of the same shape (the original line is printed first, then the substituted line is checked).**')
SUBST = [
 ('Il', '23', '734', 'Ἀχιλλεὺς', ['Ῥογῆρος', 'Νοβάκος'], 'SLL at 2-4 (Ἀχιλλεὺς αὐτὸς ἀνίστατο, 23.491 = 23.734)'),
 ('Il', '20', '164', 'Πηλεΐδης', ['Ἑλβέτιος', 'Σέρβιος'], 'LSSL at 1-3 (Πηλεΐδης δ᾽ ἑτέρωθεν); Σέρβιος LSS + δ᾽ tests the dactyl at 1-2'),
 ('Il', '23', '709', 'Ὀδυσεὺς', ['Φεδερεὺς', 'Ζοκοβεὺς'], 'SSL at 1.5-3 (Ὀδυσεὺς πολύμητις, 23.709 = 23.755)'),
 ('Il', '8', '216', 'Ἕκτωρ', ['Σέρβος'], 'LL at 1-2 (Ἕκτωρ Πριαμίδης, 7x)'),
 ('Il', '5', '114', 'Διομήδης', ['Φεδερῆρος', 'Ζοκοβίδης'], 'SSLL at 9.5-12 (βοὴν ἀγαθὸς Διομήδης, 21x)'),
]
pr('```')
for w, b, l, old, news, why in SUBST:
    k = (w, b, l); text = LINES[k]
    pr(f'{cite(k)}  {text}    [{SC[k]["pattern"]}; {SC[k]["word_positions"]}]  -- slot: {why}')
    for n in news:
        assert old in text, (k, old)
        check(text.replace(old, n))
pr('```')
note('i')

# ---------------------------------------------------------------- (j)
pr('## (j) Anachronism-avoidance lexicon')
pr('')
LEX = [
 ('racket', [('loosesub', 'ροπαλ'), ('loosesub', 'ραβδ'), ('loosesub', 'κορυν'), ('loose', 'σκηπτρον')]),
 ('ball', [('loosesub', 'σφαιρ')]),
 ('net', [('loosesub', 'δικτυ'), ('loose', 'λινον'), ('loose', 'λινω'), ('loose', 'ερκος'), ('loose', 'ερκεα'), ('loose', 'ερκει')]),
 ('court, lines, marks', [('loose', 'αυλη'), ('loose', 'αυλης'), ('loosesub', 'τερμα'), ('loosesub', 'νυσσ'), ('loosesub', 'γραμμ'), ('loose', 'σημα'), ('loose', 'σηματα'), ('loose', 'χωρον'), ('loose', 'πεδιον'), ('loosesub', 'διαμετρ')]),
 ('serve / throw / strike', [('loosesub', 'προιε'), ('loosesub', 'προεηκ'), ('loose', 'ηκε'), ('loose', 'ιει'), ('loosesub', 'αφεηκ'), ('loosesub', 'εφηκ'), ('loose', 'βαλε'), ('loose', 'βαλεν'), ('loosesub', 'ακοντισ'), ('loose', 'ερριψε')]),
 ('miss / hit the mark', [('loosesub', 'αφαμαρτ'), ('loosesub', 'ημβροτ'), ('loose', 'ετυχες'), ('loose', 'σκοπον')]),
 ('grass, turf', [('loosesub', 'ποιη'), ('loosesub', 'χλο'), ('loosesub', 'λειμων'), ('loosesub', 'χορτ')]),
 ('umpire, judge, witness', [('loosesub', 'επισκοπ'), ('loosesub', 'ιστωρ'), ('loosesub', 'ιστορ'), ('loosesub', 'δικασπολ'), ('loosesub', 'δικαζ'), ('loosesub', 'δικαστ')]),
 ('applause, shouting, silence', [('loosesub', 'επευφημ'), ('loosesub', 'επηπυ'), ('loosesub', 'επιαχ'), ('loosesub', 'ιαχ'), ('loose', 'ηυσε'), ('loosesub', 'αλαλητ'), ('loose', 'κλαγγη'), ('loosesub', 'ομαδ'), ('loosesub', 'σιωπ'), ('loosesub', 'ακην')]),
 ('trophy, prize, cup', [('loosesub', 'αεθλ'), ('loose', 'δεπας'), ('loosesub', 'δεπα'), ('loosesub', 'τριποδ'), ('loosesub', 'λεβητ'), ('loosesub', 'κρητηρ'), ('loosesub', 'κυπελλ'), ('loose', 'γερας')]),
 ('crowd, queue, spectators', [('loosesub', 'λαο'), ('loosesub', 'ομιλ'), ('loosesub', 'πληθ'), ('loosesub', 'στιχ'), ('loosesub', 'εισορο'), ('loosesub', 'θηε')]),
 ('rain, roof, sun, shade', [('loosesub', 'ομβρ'), ('loosesub', 'υετ'), ('loosesub', 'οροφ'), ('loosesub', 'τεγε'), ('loosesub', 'μελαθρ'), ('loosesub', 'στεγ'), ('loosesub', 'νεφελ'), ('loosesub', 'ηελι'), ('loosesub', 'σκι')]),
 ('time, hours, length', [('loose', 'ημαρ'), ('loosesub', 'δειελ'), ('loosesub', 'δηρον'), ('loosesub', 'δηθα')]),
 ('tiredness, sweat', [('loosesub', 'καματ'), ('loosesub', 'ιδρω'), ('loose', 'γυια'), ('loosesub', 'κεκμη'), ('loosesub', 'ασθμα')]),
 ('right and left (forehand, backhand)', [('ngram', 'ἐπὶ δεξιά'), ('ngram', 'ἐπ᾽ ἀριστερά'), ('loosesub', 'δεξι'), ('loosesub', 'αριστερ')]),
 ('victory, defeat, draw', [('loosesub', 'νικ'), ('loosesub', 'ηττ'), ('ngram', 'ἐπὶ ἶσα'), ('loosesub', 'ερις')]),
]
pr('| field | query | hits | first hits (citation [positions] <match>) |')
pr('|---|---|---|---|')
for field, qs in LEX:
    for kind, q in qs:
        hits = run(kind, q)
        first = '; '.join(f'{h.citation} [{h.pos_start}-{h.pos_end}] <{h.match}>' for h in hits[:4])
        cmd = {'ngram': f'--ngram "{q}"', 'loose': f'--loose "{q}" --word', 'loosesub': f'--loose "{q}"'}[kind]
        pr(f'| {field} | `{cmd}` | {len(hits)} | {first} |')
pr('')
pr('Verification of the lexical anchors named in the brief (lines printed from the text):')
pr('Od. 6.99-100 and 6.115-116 (Nausicaa\'s ball game):'); lines('Od', '6', 99, 100, dup=True); lines('Od', '6', 115, 116, dup=True)
pr('Od. 8.370-376 (the Phaeacian ball dance):'); lines('Od', '8', 370, 376, dup=True)
pr('Il. 13.204 (σφαιρηδόν):'); lines('Il', '13', 204, 204)
pr('Od. 22.384-388 (the net, δίκτυον):'); lines('Od', '22', 384, 388, dup=True)
pr('Il. 18.497-503 (the arbiter ἴστωρ; the crowd ἐπήπυον):'); lines('Il', '18', 497, 503, dup=True)
pr('Il. 23.485-487 (ἴστωρ Agamemnon as judge of a wager):'); lines('Il', '23', 485, 487, dup=True)
pr('Il. 12.25 (Zeus rains), Il. 24.451 (a roof of reeds), Od. 22.298 (ὀροφή):'); lines('Il', '12', 25, 25); lines('Il', '24', 450, 451); lines('Od', '22', 297, 298)
pr('Word-form anchors with shapes:')
for q in ['σφαίρῃ', 'σφαῖραν', 'ἴστορι', 'ἴστορα', 'ἐπίσκοπος', 'ῥόπαλον', 'κορύνῃ', 'ποίην', 'ὄμβρος', 'δέπας', 'γέρας', 'ἕρκος', 'κάματος']:
    show('loose', loose_query(q), limit=2 if q == 'σφαίρῃ' else 1, shape=True)
show('regex', "ὑετ", limit=3, shape=True, note='ὑετός (the loose substring υετ also matches ἐδεύετο etc.)')
show('regex', "καῦμα|καύματ", limit=2, shape=True)
show('ngram', "χρύσεον δέπας", limit=2, shape=True)
show('loosesub', 'στιχ', limit=2, shape=True, note='στίχες, the ranks')
show('loosesub', 'χλο', limit=9, shape=True, note='no χλόη; the substring hits are other words')
pr('Il. 7.237-239 (Hector: shield-work to right and left):'); lines('Il', '7', 237, 239)
show('ngram', "ὗε δ᾽ ἄρα", shape=True)
note('j')

pr('')
pr('---')
pr('## Reproduction')
pr('')
pr('Every block above is the verbatim output of the `python homer/concordance.py` command printed at its head (plus the `shape` column read from homer/scansion.tsv), every quoted passage is printed from homer/lines.tsv with its scansion row, the tables of (h) are filtered rows of homer/ngrams.tsv, and the tests of (i) are `python homer/check_line.py --json` and `python homer/scan.py --json` on the line shown. The file was generated by `homeric_models.py` (about 600 lines, with its prose module `hm_notes.py`) in the research agent\'s session scratchpad; the orchestrator should copy both under analysis/ so that the file can be regenerated (`python homeric_models.py > composition/research/homeric_models.md`, venv active, about 30 s).')
print('\n'.join(out))
