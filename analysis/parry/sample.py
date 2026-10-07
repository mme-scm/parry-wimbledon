"""Fixed 300-utterance coding sample for Phase 2b.2 (seed 2026). 150 from tv_2019wimF, 150 from the other 19 TV streams
in proportion to their token counts. Writes corpus/transcripts/samples/parry_sample_300.jsonl (gitignored: full text) and
analysis/parry/sample_ids.json (committed: ids and word counts only)."""
import json, random, glob, os, re
random.seed(2026)
R = os.path.join(os.path.dirname(__file__), '..', '..')
def load(p):
    return [json.loads(l) for l in open(p) if l.strip()]
def words(t): return len(re.findall(r"[A-Za-z0-9]+(?:['-][A-Za-z0-9]+)*", t))
main = [r for r in load(f'{R}/corpus/transcripts/tv_2019wimF.jsonl') if r.get('text_corrected') and words(r['text_corrected']) >= 3]
others = []
for p in sorted(glob.glob(f'{R}/corpus/transcripts/tv_*.jsonl')):
    if p.endswith('tv_2019wimF.jsonl'): continue
    others += [r for r in load(p) if r.get('text_corrected') and words(r['text_corrected']) >= 3]
s_main = random.sample(main, 150)
w = [words(r['text_corrected']) for r in others]
s_oth = []
seen = set()
while len(s_oth) < 150:
    r = random.choices(others, weights=w, k=1)[0]
    if r['utt_id'] in seen: continue
    seen.add(r['utt_id']); s_oth.append(r)
sample = s_main + s_oth
random.shuffle(sample)
os.makedirs(f'{R}/corpus/transcripts/samples', exist_ok=True)
with open(f'{R}/corpus/transcripts/samples/parry_sample_300.jsonl', 'w') as f:
    for r in sample:
        sb = r.get('score_before') or {}
        f.write(json.dumps({'utt_id': r['utt_id'], 'stream': r['stream'], 'phase': r.get('phase'),
                            'score_before': sb, 'text': r['text_corrected']}, ensure_ascii=False) + '\n')
json.dump([{'utt_id': r['utt_id'], 'stream': r['stream'], 'n_words': words(r['text_corrected'])} for r in sample],
          open(f'{R}/analysis/parry/sample_ids.json', 'w'), indent=0)
print(len(sample), 'utterances;', sum(words(r['text_corrected']) for r in sample), 'words')
