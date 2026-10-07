"""Crude language check of TennisVL ASR transcripts: share of tokens that are common English function words,
and count of transcripts that are identical to the previous clip's transcript. Also totals.
Usage: python3 -I tennisvl_language_check.py TEST_STATS_JSON"""
import json, sys, ast, re
EN = set("the a an and of to in is it that he she you i we for on with at this was his her be but not have so they what there just".split())
data = json.load(open(sys.argv[1], encoding="utf-8"))
tot_w = tot_clips = tot_tr = 0
for rec in data:
    mid = re.sub(r"_\d+_\d+\.mp4$", "", rec["videos"][0].split("/")[-1])
    trs = []
    for t in rec["conversations"]:
        if t["from"] == "gpt":
            _, _, meta = t["value"].partition("\n\nMetadata:")
            trs.append((ast.literal_eval(meta.strip()) if meta else {}).get("audio_transcription (background context)", "") or "")
    toks = [w for tr in trs for w in re.findall(r"[a-zà-ÿ']+", tr.lower())]
    en = sum(1 for w in toks if w in EN)
    tot_w += sum(len(t.split()) for t in trs); tot_clips += len(trs); tot_tr += sum(1 for t in trs if t.strip())
    print(f"{mid}\ttokens={len(toks)}\tenglish_function_word_share={en/len(toks):.3f}")
print(f"TOTAL clips={tot_clips} clips_with_transcript={tot_tr} transcript_words={tot_w}")
