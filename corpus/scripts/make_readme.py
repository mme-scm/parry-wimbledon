"""Step 10: write corpus/README.md. All numbers are read from corpus/reports/*.json|tsv and corpus/transcripts/manifest.json;
prose is fixed text in this script. Run: python -I corpus/scripts/make_readme.py"""
import sys, json, csv
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from corpuslib import *

R = CORPUS / "reports"
J = lambda n: json.load(open(R / n))
man = json.load(open(CORPUS / "transcripts" / "manifest.json"))
t19, t23 = J("timing_report_2019wimF.json"), J("timing_report_2023wimF.json")
tv19 = J("timing_validation_2019wimF.json")
al = J("alignment_validation.json")
asr = J("asr_proxy.json")
bt = J("build_transcripts_summary.json")
ph = J("phase_summary.json")
cs = J("corrections_summary.json")
corr = list(csv.DictReader(open(CORPUS / "corrections.tsv", encoding="utf-8"), delimiter="\t"))
samp20 = list(csv.DictReader(open(R / "timing_validation_2019wimF.tsv", encoding="utf-8"), delimiter="\t"))
alsamp = list(csv.DictReader(open(R / "alignment_sample20.tsv", encoding="utf-8"), delimiter="\t"))
alj = {r["utt_id"]: r for r in csv.DictReader(open(CORPUS / "validation" / "alignment_sample20_judgements.tsv", encoding="utf-8"), delimiter="\t")}
unm19 = list(csv.DictReader(open(R / "unmatched_2019wimF.tsv", encoding="utf-8"), delimiter="\t"))
unm23 = list(csv.DictReader(open(R / "unmatched_2023wimF.tsv", encoding="utf-8"), delimiter="\t"))
import pandas as pd
p19 = pd.read_csv(CORPUS / "timing" / "points_2019wimF.csv", dtype=str)
p23 = pd.read_csv(CORPUS / "timing" / "points_2023wimF.csv", dtype=str)


def md(rows, cols):
    out = ["| " + " | ".join(cols) + " |", "|" + "---|" * len(cols)]
    for r in rows:
        out.append("| " + " | ".join(str(r.get(c, "")) for c in cols) + " |")
    return "\n".join(out)


def f(x, nd=2):
    return f"{x:.{nd}f}"


def pct(a, b):
    return f"{100 * a / b:.1f}%"


S = man["streams"]
stream_rows = []
for k, v in S.items():
    short = k if len(k) < 26 else k[:26] + "..."
    stream_rows.append({"stream": f"`{k}`", "medium": v["medium"], "records": v["n_records"], "with text": v["n_records_nonempty_text"],
                        "words raw": v["n_words_raw"], "words dedup": v["n_words_dedup"], "words corrected": v["n_words_corrected"],
                        "sha256 (jsonl, first 12)": v["sha256_jsonl"][:12]})
tvs = {k: v for k, v in S.items() if k.startswith("tv_")}
pool = {k: v for k, v in tvs.items() if k.startswith("tv_pool_")}
sum_pool = {x: sum(v[x] for v in pool.values()) for x in ("n_records", "n_records_nonempty_text", "n_words_raw", "n_words_dedup", "n_words_corrected")}

o19, o23 = t19["offset"], t23["offset"]
lf = o19["linear_fit"]
seg23 = t23["offset_segments"]
ro = tv19["resid_outliers"]
rb = tv19["resid_breakdown"]
ap = tv19["all_points"]
hs = asr["hand_sample"]
unfixed_ns = sum(1 for e in asr["hand_sample_errors"] if e["error_type"] in ("name_misspelled", "score_call_impossible") and not e["fixed_by_correction_list"])
n_garble = sum(1 for e in asr["hand_sample_errors"] if e["error_type"] == "other_garble")
A = asr["automatic"]
aa = al["automatic"]
hv = al["hand_verdicts"]
n_unconf = hv.get('no_match', 0) + hv.get('retrospective_narration_not_live_call', 0) + hv.get('retrospective_narration_coincidental_match', 0)
n_dd = {k: bt[k]["dedup_actions"] for k in bt if "dedup_actions" in bt[k]}
dd19 = n_dd["tv_2019wimF"]
words_removed19 = S["tv_2019wimF"]["n_words_raw"] - S["tv_2019wimF"]["n_words_dedup"]
words_removed23 = S["tv_2023wimF"]["n_words_raw"] - S["tv_2023wimF"]["n_words_dedup"]
sp_n = sum(d.get("suffix_prefix_overlap", 0) + d.get("shared_prefix", 0) for d in n_dd.values())
far = {k: bt[k].get("n_exact_repeats_beyond_max_distance_not_removed", 0) for k in bt if k.startswith("tv_")}
nocl19 = p19[p19.tv_match_type.isna()].point_idx.astype(int).tolist()
nocl23 = p23[p23.tv_match_type.isna()].point_idx.astype(int).tolist()
ts19 = p19.timing_source.value_counts().to_dict()
ts23 = p23.timing_source.value_counts().to_dict()

segtab = [{"start point": s["start_point"], "level s": s["level_s"], "jump s": "-" if s["jump_s"] is None else s["jump_s"], "anchors": s["n_anchors"],
           "cut interval (points)": "-" if s["cut_interval_points"] is None else s["cut_interval_points"], "changeover/set break inside": "-" if s["changeover_or_set_break_in_interval"] is None else s["changeover_or_set_break_in_interval"]}
          for s in seg23]

txt = f"""# corpus/: commentary corpus for the 2019 Wimbledon final (and held-out / reference / written streams)

Built by `bash corpus/scripts/build_corpus.sh` from the downloads in `corpus/raw/` (never edited). Every number in this file is
read from `corpus/reports/*.json` and `corpus/transcripts/manifest.json` by `corpus/scripts/make_readme.py`; none is typed by hand.
The only hand-made inputs are the correction rules (`corpus/corrections_rules.tsv`) and two sets of hand verdicts in
`corpus/validation/` (ASR error list for a 500-word sample; alignment verdicts for 20 utterances). Both are listed below.

## 0. What this corpus is, and what it is not

* Spoken commentary exists only as **WhisperX ASR transcripts, one TV commentary track per match**, attached to rally clips
  of the TennisVL test split. There is **no audio**, **no speaker label**, **no word timestamp** in the released files.
* Consequently: no faster-whisper run was possible or needed (the chunking rule and model-speed choice in CLAUDE.md do not apply: no audio
  was downloaded or transcribed); the **word error rate is unknown** (section 7); commentators cannot be tagged (section 6);
  **in_rally vs between_points cannot be separated at word level** (section 6); time of an utterance is known only as the clip window.
* Streams (one per broadcaster per medium; `medium` is `tv` or `text`, never mixed):

{md(stream_rows, ["stream", "medium", "records", "with text", "words raw", "words dedup", "words corrected", "sha256 (jsonl, first 12)"])}

  Roles: `tv_2019wimF` MAIN (in-sample); `tv_2023wimF` HELD-OUT; the 18 `tv_pool_<match_id>` streams are an exploratory REFERENCE POOL
  for cross-match formula identification only (together {sum_pool['n_records']} records, {sum_pool['n_records_nonempty_text']} with text,
  {sum_pool['n_words_dedup']} words after de-duplication); `text_cornell` is the WRITTEN CONTRAST (Cornell / Sports Mole live text,
  different matches, no timestamps). Word = regex `[A-Za-z0-9]+(?:['-][A-Za-z0-9]+)*`, so digits count as words; this differs slightly from the
  whitespace count in SOURCES.md (11,772 words for the 2019 final).
* The `.jsonl` files hold the full source text and are **gitignored**. Committed: `corpus/transcripts/manifest.json`
  (per-stream counts and sha256 of each jsonl) and `corpus/transcripts/meta_<stream>.csv` (every field except the three text fields).

## 1. Rebuild

```
bash corpus/scripts/build_corpus.sh      # needs corpus/raw/ (see SOURCES.md section 2) and .venv
```
Steps and their outputs (all scripts are run with `python -I`):

| # | script | output |
|---|---|---|
| 1 | `build_timing.py` | `timing/points_{{2019wimF,2023wimF}}.csv`, `timing/shots_*.csv`, `reports/timing_report_*.json`, `reports/unmatched_*.tsv`, `reports/clip_alignment_*.json` |
| 2 | `validate_timing.py` | `reports/timing_validation_2019wimF.{{json,tsv}}` |
| 3 | `build_transcripts.py` | `transcripts/<stream>.jsonl` (raw + de-duplicated text, alignment) |
| 4 | `apply_corrections.py` | `corrections.tsv`, `corrections.log`, `text_corrected` |
| 5 | `tag_phase.py` | `phase*`, `speaker_cues` fields; `reports/phase_summary.json` |
| 6 | `make_manifest.py` | `transcripts/manifest.json`, `transcripts/meta_<stream>.csv` |
| 7-8 | `asr_sample.py`, `asr_proxy.py` | `reports/asr_proxy.json` (sample text itself goes to gitignored `raw/derived_scratch/`) |
| 9 | `align_validation.py` | `reports/alignment_sample20.tsv`, `reports/alignment_validation.json` |
| 10 | `make_readme.py` | this file |

## 2. Provenance of the existing transcripts

* Source: TennisVL test split, `corpus/raw/tennisexpert_repo/data/tennis_data_test_stats_.json` (commit 8b778bc of
  github.com/LZYAndy/TennisExpert; paper Liu et al. 2026, arXiv:2603.13397), field `audio_transcription (background context)` in the
  `Metadata:` dict of each `gpt` turn. File sha256 {man['inputs_sha256']['tennis_data_test_stats_.json'][:16]}... (full value in `manifest.json`).
* ASR system: "WhisperX" per the paper; model size, VAD and alignment window are **not stated** in the files. The raw file is untouched; `text_raw`
  is that field verbatim. The LLM-written `gpt` commentary (Gemini 3 Pro per the paper) is **dropped** and never written to any output.
* Broadcaster: not named in the files. `broadcaster` is "unnamed; probably BBC TV [unverified]" for 2019 (hints: 'Boris' 19x, 'Tim' 7x);
  hints for other matches are recorded in `broadcaster_hints`. All labels unverified.
* Timing sources: TennisVL per-shot `hit_timestamp_second` (video seconds, automatic parser); Sackmann slam point-by-point `ElapsedTime`
  (HF mirror of the removed upstream repo, CC BY-NC-SA 4.0, attribution Jeff Sackmann); Match Charting Project shot codes (CC BY-NC-SA 4.0,
  Tennis Abstract MCP, charter "Zindaras" for the 2019 final). No audio onset detection (librosa) was possible: no audio.

## 3. Per-point alignment (TennisVL x PBP x MCP)

**Clips and groups.** The 2019 file has {t19['n_clips']} clips, the 2023 file {t23['n_clips']}. A point can have two clips: a first-serve-fault clip
(single shot, type `first serve`, outcome `unforced-error`, role `first_serve_fault`) and the clip of the point proper. Consecutive clips with an identical
score state are therefore merged into one **group** (a point cannot repeat its score state on the next point). Clip roles, 2019: {t19['clip_roles']};
2023: {t23['clip_roles']}. `clip_role` is a field of every record. Groups: {t19['n_groups']} (2019), {t23['n_groups']} (2023).

**Score states.** PBP: the state *before* each point is the previous row's after-point state (sets from `SetWinner`, games and points from the previous row; the two `0X`/`0Y`
placeholder rows per match are dropped: {t19['pbp']['dropped_placeholders']} in 2019, {t23['pbp']['dropped_placeholders']} in 2023; {t19['n_points_pbp']} and {t23['n_points_pbp']} points remain).
PBP P1 = Djokovic (2019) and Alcaraz (2023); MCP player 1 = Federer (2019) and Djokovic (2023). Everything is therefore keyed by player **surname**.

**Join key** = (server surname, sets by surname, games by surname, points by surname) before the point; occurrence order resolves the
repeats (e.g. several 40-40 states in one game) by a monotone dynamic-programming alignment of the chronological clip groups to the chronological PBP points.
Match tiers, in decreasing strictness: `key` (full key identical, non-tie-break); `key_tb` (tie-breaks: TennisVL writes tie-break points as 0/15/30/40 for counts 0-3 and cannot
express higher counts, so only server+sets+games must agree, with the clock residual within a tolerance); `key_no_server` (TennisVL names the wrong server, a parser error; identical sets/games/points and clock residual within tolerance).
The 5th-set tie-break is at 12-12 in 2019 and 6-6 in 2023 (`final_set_tb`).

| | 2019 final | 2023 final |
|---|---|---|
| clips aligned to a PBP point | {t19['n_matched_clips']} of {t19['n_clips']} ({pct(t19['n_matched_clips'], t19['n_clips'])}) | {t23['n_matched_clips']} of {t23['n_clips']} ({pct(t23['n_matched_clips'], t23['n_clips'])}) |
| groups aligned | {t19['pass2_matched_groups']} of {t19['n_groups']} | {t23['pass2_matched_groups']} of {t23['n_groups']} |
| match types | {t19['match_types']} | {t23['match_types']} |
| PBP points with at least one clip | {t19['n_points_with_clip']} of {t19['n_points_pbp']} ({pct(t19['n_points_with_clip'], t19['n_points_pbp'])}) | {t23['n_points_with_clip']} of {t23['n_points_pbp']} ({pct(t23['n_points_with_clip'], t23['n_points_pbp'])}) |
| PBP points with the point-proper (rally/ace/DF) clip | {t19['n_points_with_rally_clip']} | {t23['n_points_with_rally_clip']} |
| MCP points whose key equals the PBP key at the same index | {t19['mcp_vs_pbp']['key_equal_at_same_index']} of {t19['mcp_vs_pbp']['n_pbp']} | {t23['mcp_vs_pbp']['key_equal_at_same_index']} of {t23['mcp_vs_pbp']['n_pbp']} |
| TennisVL shots (all listed in `shots_*.csv`) | {t19['n_shots_total']} | {t23['n_shots_total']} |

MCP and PBP agree on the key for every point of both finals (`Pts` is server-first; MCP points are therefore joined to PBP by index and verified by key).
**Unmatched clips (2019, {t19['n_unmatched_clips']})**, with their parsed state, are in `reports/unmatched_2019wimF.tsv`:
{md([{"first hit s": u["first_attempt_s"], "clip frames": u["clips"], "server": u["server"], "n_shots": u["n_shots"]} for u in unm19], ["first hit s", "clip frames", "server", "n_shots"])}

2023: {len(unm23)} unmatched groups ({t23['n_unmatched_clips']} clips); list in `reports/unmatched_2023wimF.tsv`. In both matches most unmatched clips have a
state that the TennisVL parser mis-states (in the cases inspected: a wrong server together with a score or game count that does not occur at that point in PBP); the cause was not checked clip by clip; they are left unaligned
(`point_idx_pbp` null) rather than forced. PBP points **without any clip** (`timing_source = pbp_elapsed_only`): 2019 {len(nocl19)} points; 2023 {len(nocl23)} points
(point numbers are in the `point_idx` column of the points tables).
Pool streams have no PBP/clock; their clips are aligned to MCP points (key only, no clock) where an MCP chart exists
(all pool matches except 2019 AO women's and 2021 USO women's final). Per pool match, aligned clips: see `meta_<stream>.csv` (`point_idx_mcp`, `align_type`).

### 3.1 Video clock vs PBP clock

The TennisVL time is seconds in the (unnamed) source video; PBP `ElapsedTime` is the match clock. Residual = TennisVL first-serve-attempt time minus (ElapsedTime + offset).

* **2019 final: one constant offset, no cuts.** Intercept {f(lf['intercept_s'])} s with slope {lf['slope']:.6f} (so slope 1); with slope fixed to 1 the offset is
  {f(lf['offset_slope1_median_s'])} s. Residual SD **{f(lf['residual_sd_s'], 3)} s** over the {lf['n']} points within 3 s of the offset
  ({pct(o19['n_within_3s'], o19['n_matched_groups'])} of {o19['n_matched_groups']} aligned points); robust SD (1.4826 x MAD) {f(o19['residual_mad_sd_s'], 3)} s; SD over all aligned points
  including the {o19['n_outliers_gt_3s']} outliers {f(o19['residual_sd_all_s'])} s.
  ElapsedTime is the time of the **first serve of the point**: {ro['n_positive_second_serve_point_without_fault_clip']} of the {ro['n_positive']} positive outliers
  ({ro['positive_range_s'][0]} to {ro['positive_range_s'][1]} s) are second-serve points whose first-serve fault clip is absent from TennisVL, so the clip starts at the second serve.
  {ro['n_negative']} negative outliers ({ro['negative_range_s'][0]} to {ro['negative_range_s'][1]} s) are unexplained (clip grouping or a parser timestamp error).
* **2023 final: the offset is piecewise constant.** The source video lacks the changeover/set-break periods: {t23['n_cuts']} cuts, of which
  {t23['n_cuts_with_changeover_in_interval']} have a changeover or set break inside the interval between the last point before and the first point after the cut.
  A single linear offset is therefore invalid (SD over all points {f(o23['residual_sd_all_s'], 1)} s); the residual about the local level is SD **{f(o23['residual_sd_within_3s_s'], 3)} s**
  for the {o23['n_within_3s']} of {o23['n_matched_groups']} aligned points within 3 s of their level (robust SD {f(o23['residual_mad_sd_s'], 3)} s). Consequences: video-seconds gaps across changeovers in 2023 are
  censored (`gap_video_*` is not the real elapsed time there; use the PBP-based `gap_pbp_prev_point_s` / `dead_time_before_s`), and the 2023 transcripts contain no talk from the omitted breaks.

2023 segments (level = video seconds minus ElapsedTime; a segment needs at least 3 anchor points):

{md(segtab, ["start point", "level s", "jump s", "anchors", "cut interval (points)", "changeover/set break inside"])}

### 3.2 Which source each point's timing uses

`points_*.csv` column `timing_source`: `tennisvl_hit_times` = first/last strike times from TennisVL hit timestamps (point-proper clip present; 2019: {ts19.get('tennisvl_hit_times', 0)} points,
2023: {ts23.get('tennisvl_hit_times', 0)}); `tennisvl_fault_clip_only` = only the first-serve-fault clip exists (2019: {ts19.get('tennisvl_fault_clip_only', 0)}, 2023: {ts23.get('tennisvl_fault_clip_only', 0)});
`pbp_elapsed_only` = no clip, only the PBP clock (2019: {ts19.get('pbp_elapsed_only', 0)}, 2023: {ts23.get('pbp_elapsed_only', 0)}); `est_video_serve_s` = ElapsedTime + local offset (an estimate of the video time of the first serve).
`rally_duration_s` = last hit minus first hit of the point-proper clip (TennisVL). `dead_time_before_s` = (ElapsedTime of this point - ElapsedTime of the previous point) - previous rally duration; null when the previous point
has no point-proper clip. `gap_video_prev_last_hit_to_first_attempt_s` = video-clock gap between the previous point's last hit and this point's first serve attempt (both TennisVL).
Hit times for every shot are in `shots_*.csv` (`inter_shot_interval_s` = interval to the previous shot in the same clip).

## 4. De-duplication (text_raw -> text_dedup)

Consecutive clips often carry the same ASR text (the transcript window of a clip overlaps its neighbours). Rule, applied per stream in clip order:

* **R1 exact repeat**: if the lower-cased word sequence of clip *i* equals that of the most recent preceding non-empty clip at most {3} clips back, `text_dedup` is empty and `dedup_of` points to the first occurrence of the run.
* **R2 suffix-prefix overlap**: otherwise, if the last *k* words of the previous clip equal the first *k* words of this one with *k* >= 6, remove those *k* words from this clip.
* **R3 shared prefix**: otherwise, if the first *k* >= 6 words are identical, remove them.
* Shorter coincidences (1-5 words, e.g. a shared '30') are kept. Exact repeats farther than 3 clips back are kept and counted (diagnostic only).

Effect, 2019 final: {dd19.get('exact_repeat', 0)} exact repeats (R1), {dd19.get('suffix_prefix_overlap', 0)} R2, {dd19.get('shared_prefix', 0)} R3; {words_removed19} of {S['tv_2019wimF']['n_words_raw']} words removed
({pct(words_removed19, S['tv_2019wimF']['n_words_raw'])}). 2023: {n_dd['tv_2023wimF'].get('exact_repeat', 0)} R1, {words_removed23} of {S['tv_2023wimF']['n_words_raw']} words ({pct(words_removed23, S['tv_2023wimF']['n_words_raw'])}).
All 20 TV streams together: {sum(d.get('exact_repeat', 0) for k, d in n_dd.items() if k.startswith('tv_'))} R1, {sp_n} R2/R3. Far repeats not removed (2019 / 2023): {far['tv_2019wimF']} / {far['tv_2023wimF']}.
Per-stream word counts raw/dedup are in the stream table above. The Cornell text is not de-duplicated (`dedup_action = not_applicable_text`).

Transcript window (finding): the first score call in a clip's text equals the PBP score **after** the clip's point in {aa['2019wimF']['first_call_equals_score_before_point_plus_d'].get('1', 0)} of {aa['2019wimF']['n_utterances_with_call']} 2019 utterances
({pct(aa['2019wimF']['first_call_equals_score_before_point_plus_d'].get('1', 0), aa['2019wimF']['n_utterances_with_call'])}) and {aa['2023wimF']['first_call_equals_score_before_point_plus_d'].get('1', 0)} of {aa['2023wimF']['n_utterances_with_call']} 2023 utterances
({pct(aa['2023wimF']['first_call_equals_score_before_point_plus_d'].get('1', 0), aa['2023wimF']['n_utterances_with_call'])}); so a clip's transcript window reaches from about the clip start to beyond the clip end (into the dead time after the point). Distribution of the offset d
(call = score before point *p*+d), 2019: {aa['2019wimF']['first_call_equals_score_before_point_plus_d']}; 2023: {aa['2023wimF']['first_call_equals_score_before_point_plus_d']}. This is a statement about the
alignment at clip level only.

## 5. Name and term corrections (text_dedup -> text_corrected)

`corpus/corrections_rules.tsv` (hand-curated regex rules; columns id, kind, scope, pattern, replacement, confidence, reason) was built by reading the candidate list `reports/correction_candidates.tsv` (ASR tokens that are not
words of the Cornell vocabulary and are close, difflib ratio >= 0.6, to the match's player names), checking contexts in the 2019 and 2023 transcripts, and
checking each replacement name against a lexicon of player names (all `*-matches.csv` of the PBP mirror plus TennisVL `match_info`; column `replacement_in_player_lexicon` of `corrections.tsv`).
`scope` is `all` or the date prefix of the TennisVL match ids. Applied as a **separate step** (`apply_corrections.py`): `text_raw` and `text_dedup` are never modified; every substitution is logged in `corpus/corrections.log`
(stream, utterance, rule, match -> replacement, 4 words of context each side). Counts per rule are in `corpus/corrections.tsv`; total substitutions: **{cs['total_substitutions']}**
(on de-duplicated text), in {sum(cs['utterances_changed_per_stream'].values())} utterances. Rule kinds: `name` (player-name variants), `term` (e.g. `left`/`off`/`loud` for `love` in score calls, `juice` for `deuce`, `Fire set` for `Fifth set`), `normalisation` ('breakpoint' to 'break point', 'down the tee' to 'down the T').
Medium/normalisation confidence rules are marked; only errors visible from context are corrected, **many ASR errors remain uncorrected** (e.g. garbled names of non-players such as 'Rochaferra', 'Legrocha', 'Edverson'; the hand sample below found {unfixed_ns} uncorrected name/score-call errors and {n_garble} garbles).
Correction counts: 2019 {sum(int(r['count_2019wimF']) for r in corr)}, 2023 {sum(int(r['count_2023wimF']) for r in corr)}, pool {sum(int(r['count_pool']) for r in corr)}.

## 6. Phase, speaker tags and time since last strike

* `phase` = `clip` by default (the transcript belongs to a clip, not to a word). **Heuristic** sub-tags, set by regex on `text_corrected` and flagged `phase_heuristic = true`:
  `between_points` when the whole text is a score call (digits <= 2 chars, love, all, deuce, advantage, game, set, player surnames) or a short 'Game <name>' call;
  `changeover` when a cue such as 'changeover', 'change of ends', 'new balls', 'towel', 'set break' occurs. 2019: {ph['tv_2019wimF']['phase']}; 2023: {ph['tv_2023wimF']['phase']}.
  `phase_tags` also lists `contains_score_call` (a score call somewhere in longer text: 2019 {ph['tv_2019wimF']['tags'].get('contains_score_call', 0)} utterances).
  **in_rally vs between_points cannot be separated at word level**: no audio and no word timestamps, and a clip's text window (section 4) spans rally and dead time.
  In particular the `changeover` tag can fire on talk about new balls during play. The `in_rally` value is therefore never assigned.
* `speaker_role` is always `unknown`: the files have no speaker labels, so commentator turns cannot be tagged and commentator identity cannot be separated from medium. `speaker_cues` lists **heuristic** umpire/Hawk-Eye cues
  ('Game <name>', 'new balls please', 'ball was called', 'time violation', 'Mr <name> is challenging'): 2019 {ph['tv_2019wimF']['umpire_cues']}; 2023 {ph['tv_2023wimF']['umpire_cues']}. The umpire's and Hawk-Eye's voices are inside the transcripts and not separated.
* `t_since_prev_last_hit_s` = clip start minus the last hit of the previous clip; `t_to_next_first_hit_s` = first hit of the next clip minus clip end (video seconds, TennisVL). They are **clip-level**: no word has its own time.
  In 2023 they are censored across video cuts (section 3.1).

## 7. Validation

### 7.1 Timing: TennisVL vs MCP and PBP (2019 final)

Convention found in the data: PBP `RallyCount` counts the **in-play shots** (the final erring shot is not counted; double faults 0); MCP and TennisVL count the erring shot too. PBP minus MCP shots over all 422 points is 0 for winners/aces
and -1 for every error ending (`pbp_minus_mcp` = {tv19['pbp_minus_mcp']}); after adding 1 for error endings ('pbp adj') PBP equals MCP for {pct(round(tv19['pbp_rc_adj_equals_mcp_all_points'] * 422), 422)} of points.

All {ap['n']} points that have a TennisVL point-proper clip: `n_shots` equals MCP shots exactly in {pct(ap['tv_vs_mcp_exact'] * ap['n'], ap['n'])} (within one shot in {pct(ap['tv_vs_mcp_within1'] * ap['n'], ap['n'])}); equals PBP adj in {pct(ap['tv_vs_pbp_adj_exact'] * ap['n'], ap['n'])}
(raw PBP RallyCount: {pct(ap['tv_vs_pbp_raw_exact'] * ap['n'], ap['n'])}, because of the convention above). TennisVL minus MCP: {ap['tv_minus_mcp_dist']}; in {tv19['tv_more_than_mcp']['n_first_interval_ge_4s']} of the {tv19['tv_more_than_mcp']['n']} over-count cases the first interval is >= 4 s (an extra early serve).
Other checks: stroke wing (forehand/backhand) agrees with the MCP shot letter for {ap['wing_agreement']['n_agree']} of {ap['wing_agreement']['n_shots_compared']} shots ({pct(ap['wing_agreement']['n_agree'], ap['wing_agreement']['n_shots_compared'])}, points with equal shot counts);
serve hitter equals PBP server in {ap['serve_hitter_vs_pbp_server']['n_agree']} of {ap['serve_hitter_vs_pbp_server']['n']}; the last shot's outcome class equals the MCP end code (*, @, #) in {pct(ap['final_shot_outcome_vs_mcp_end_char']['n_agree'], ap['final_shot_outcome_vs_mcp_end_char']['n'])} of {ap['final_shot_outcome_vs_mcp_end_char']['n']} (forced/unforced labels differ between sources);
the bounce time lies between the hit and the next hit in {pct(tv19['bounce_between_hits']['rate_hit<bounce<next_hit'] * tv19['bounce_between_hits']['n'], tv19['bounce_between_hits']['n'])} of {tv19['bounce_between_hits']['n']} shots;
hit intervals: n {tv19['hit_intervals_s']['n']}, median {f(tv19['hit_intervals_s']['median'])} s, mean {f(tv19['hit_intervals_s']['mean'])} s, 1st-99th percentile {f(tv19['hit_intervals_s']['p1'])}-{f(tv19['hit_intervals_s']['p99'])} s, none non-positive.
**Hit intervals cannot be validated independently**: MCP has no clock and PBP ElapsedTime has 1 s resolution; the only external timing check is the serve time vs PBP clock (section 3.1).

**20 random points** (seed {tv19['seed']}, drawn from the {tv19['n_points_with_tv_rally_clip']} points with a point-proper clip): exact agreement TennisVL = MCP in {tv19['sample20']['tv_eq_mcp']}/20, TennisVL = PBP adj in {tv19['sample20']['tv_eq_pbp_adj']}/20; within one shot {tv19['sample20']['tv_within1_mcp']}/20 (MCP), {tv19['sample20']['tv_within1_pbp_adj']}/20 (PBP adj).

{md(samp20, ["point_idx", "set", "game", "score_before_p1p2", "tv_n_shots", "mcp_n_shots", "pbp_rally_count", "pbp_rc_adj", "tv_eq_mcp", "tv_eq_pbp_adj", "interval_mean_s", "interval_min_s", "interval_max_s", "wing_agree"])}

(`score_before_p1p2` is PBP P1-P2 = Djokovic-Federer. A large `interval_max_s` signals a missing or extra shot in the TennisVL rally, e.g. points 19, 40.)

### 7.2 Alignment of utterances to points (2019 final)

Automatic: of {aa['2019wimF']['n_utterances_with_call']} aligned utterances with a score call, the first call equals the PBP score after this clip's point in {aa['2019wimF']['first_call_equals_score_before_point_plus_d'].get('1', 0)}, before it in {aa['2019wimF']['first_call_equals_score_before_point_plus_d'].get('0', 0)},
two points on in {aa['2019wimF']['first_call_equals_score_before_point_plus_d'].get('2', 0)}, and matches no PBP state in points -1..+3 in {aa['2019wimF']['first_call_equals_score_before_point_plus_d'].get('none', 0)} (ASR/commentator slips, retrospective mentions). 2023: {aa['2023wimF']['first_call_equals_score_before_point_plus_d']}.

**Hand check of 20 random aligned utterances** (seed {al['seed']}; drawn from the {al['n_candidates']} that contain a parseable score call; I compared the call in the text with the PBP score, server-first):
verdicts {hv}. That is {hv.get('match_after_this_point', 0)}/20 exact matches to the score after the aligned point, {hv.get('match_two_points_later', 0) + hv.get('match_before_and_later_skips_after', 0)} more within two points,
{hv.get('no_match', 0)} not matching and {hv.get('retrospective_narration_not_live_call', 0) + hv.get('retrospective_narration_coincidental_match', 0)} where the call is a retrospective mention (not usable as evidence). {n_unconf} of 20 are not confirmed as evidence; the {hv.get('no_match', 0)} 'no_match' cases may be a misalignment or an ASR/commentator slip, and the two cannot be told apart here. Judgements are in `corpus/validation/alignment_sample20_judgements.tsv` (hand-made).

{md([{**{k: r[k] for k in ("utt_id", "point_idx", "set", "game_in_set", "pbp_score_before_this_point", "pbp_score_after_this_point", "first_call_in_text", "call_context_excerpt")}, "verdict": alj[r["utt_id"]]["verdict"]} for r in alsamp], ["utt_id", "point_idx", "set", "game_in_set", "pbp_score_before_this_point", "pbp_score_after_this_point", "first_call_in_text", "call_context_excerpt", "verdict"])}

### 7.3 ASR error estimate: WER is unknown

No audio and no human reference transcript exist, so the word error rate **cannot be measured and is unknown**. Internal proxies only:

* **Hand-read sample** (seed {hs['seed']}): {hs['n_words']} words in {hs['n_utterances']} randomly drawn 2019 clips (`text_dedup`), read by me for implausible tokens. Errors found: {hs['errors_total']} ({hs['errors_by_type']}),
  i.e. **{f(hs['total_per_1000_words'], 1)} per 1,000 words** (Wilson 95% CI {f(hs['wilson95_ci_per_1000_total'][0], 1)}-{f(hs['wilson95_ci_per_1000_total'][1], 1)}); misspelled player names + impossible score calls only: **{f(hs['name_plus_score_call_per_1000_words'], 1)} per 1,000**
  (CI {f(hs['wilson95_ci_per_1000_name_plus_score'][0], 1)}-{f(hs['wilson95_ci_per_1000_name_plus_score'][1], 1)}). {hs['n_fixed_by_correction_list']} of the {hs['errors_total']} are fixed by the correction list. The sample is drawn by clip, so short score-call clips are over-represented relative to words; the automatic proxy below is the better rate for score calls.
  This is a **lower bound** on the error rate: substitutions that give a plausible English word cannot be seen without audio.
* **Automatic proxy** (all words of the stream, after de-duplication): player-name variants fixed by rules N*: 2019 {f(A['tv_2019wimF']['name_variants_per_1000_words'], 2)} per 1,000 words, 2023 {f(A['tv_2023wimF']['name_variants_per_1000_words'], 2)},
  all TV streams {f(A['all_tv_streams']['name_variants_per_1000_words'], 2)}; 'love' errors in score calls fixed by rules T03-T05: 2019 {f(A['tv_2019wimF']['love_errors_per_1000_words'], 2)}, 2023 {f(A['tv_2023wimF']['love_errors_per_1000_words'], 2)}, all TV {f(A['all_tv_streams']['love_errors_per_1000_words'], 2)};
  score calls (after correction) matching no PBP state in points -1..+3 of the aligned point: 2019 {A['tv_2019wimF']['score_calls_parsed'] - A['tv_2019wimF']['score_calls_matching_pbp_window_p-1..p+3']} of {A['tv_2019wimF']['score_calls_parsed']} ({f(A['tv_2019wimF']['score_call_mismatch_per_1000_words'], 2)} per 1,000 words), 2023 {A['tv_2023wimF']['score_calls_parsed'] - A['tv_2023wimF']['score_calls_matching_pbp_window_p-1..p+3']} of {A['tv_2023wimF']['score_calls_parsed']} ({f(A['tv_2023wimF']['score_call_mismatch_per_1000_words'], 2)} per 1,000).

Errors found in the hand sample (excerpts, `corpus/validation/asr_sample_errors.tsv`):

{md([{"utt_id": e["utt_id"], "excerpt": e["excerpt"], "type": e["error_type"], "fixed by rule": e["fixed_by_correction_list"]} for e in asr["hand_sample_errors"]], ["utt_id", "excerpt", "type", "fixed by rule"])}

## 8. Known gaps

1. No audio: no WER, no word times, no librosa onset times, no speaker labels, no intonation units. Utterance time = clip window; the transcript window extends beyond the clip (section 4).
2. One TV track per match: no broadcaster or medium contrast within a match; broadcaster labels unverified. Commentator identity is confounded with medium and match.
3. Coverage: {S['tv_2019wimF']['n_records_nonempty_text']} of {S['tv_2019wimF']['n_records']} 2019 clips have text; {t19['n_points_pbp'] - t19['n_points_with_clip']} of {t19['n_points_pbp']} points have no clip at all (their commentary is not in the corpus, so the transcript is a sample of the match, not a complete record). 2023: {S['tv_2023wimF']['n_records_nonempty_text']} of {S['tv_2023wimF']['n_records']}, {t23['n_points_pbp'] - t23['n_points_with_clip']} of {t23['n_points_pbp']} points without clip, and changeover talk is cut from the video.
4. The transcripts include the umpire's and Hawk-Eye's voices ('Game <name>', 'ball was called') and stadium announcements, unseparated.
5. TennisVL score states contain parser errors (wrong server, tie-break points), shot counts are within one of MCP in {pct(ap['tv_vs_mcp_within1'] * ap['n'], ap['n'])} only; hit timestamps come from an automatic parser (no manual check of absolute times beyond section 3.1).
6. PBP `ElapsedTime` has 1 s resolution and marks the first serve of a point. PBP `RallyCount` excludes the final erring shot (section 7.1). MCP `Pts` in tie-breaks is unreliable in places (MCP key equals PBP key for all points, but the MCP tie-break score sequence has visible oddities, e.g. in the 2019 first-set tie-break).
7. The MCP shot count is parsed from the shot codes by a simple rule (serve plus every stroke letter in the code that ends the point); `mcp_n_shots` is a heuristic count (agrees with PBP adj in {pct(round(tv19['pbp_rc_adj_equals_mcp_all_points'] * 422), 422)} of points).
8. Corrections are conservative and incomplete; normalisation rules (T08-T11) change spelling variants and can be switched off by using `text_dedup`.
9. Cornell text: no match ids, dates or timestamps; the scoreline gives only players and score (parsed for all {man['streams']['text_cornell']['n_records']} updates; the `*` marker side is read heuristically as the server side and the dataset README does not define it) [unverified].
10. Licences: TennisVL "strictly for academic research in sports video understanding" (scope question is in FOR_HUMAN.md); MCP and slam PBP CC BY-NC-SA 4.0 (attribution: Jeff Sackmann, Tennis Abstract Match Charting Project); the derived tables committed here (points, shots, meta) inherit ShareAlike; Cornell data from Fu, Danescu-Niculescu-Mizil and Lee 2016, no licence stated.
   Full source texts are never committed (jsonl gitignored); committed text excerpts are at most 15 words.

## 9. Field dictionary (`transcripts/<stream>.jsonl`; `meta_<stream>.csv` has the same fields without the three text fields, plus `n_words_*`)

`stream, medium, broadcaster, broadcaster_hints, match_id, utt_id, clip, clip_i, clip_start_frame, clip_end_frame, clip_start_s, clip_end_s` (frames/25),
`first_hit_s, last_hit_s, n_shots, clip_role, rally_duration_s` (this clip's TennisVL hits), `score_before` (server, sets, games, points before the point; TennisVL), `point_outcome`,
`set_no, game_in_set, tiebreak_state` (derived from score_before, or from PBP when aligned), `text_raw` (untouched ASR), `text_dedup` (section 4), `text_corrected` (section 5), `dedup_action, dedup_k_removed, dedup_of`,
`phase, phase_heuristic, phase_tags, speaker_role, speaker_cues` (section 6), `t_since_prev_last_hit_s, t_to_next_first_hit_s`,
`point_idx_pbp, point_idx_mcp, game_no_pbp, elapsed_prev_point_s` (ElapsedTime_prev_point), `elapsed_this_point_s` (ElapsedTime_this_point), `dead_time_before_s, rally_count_pbp, rally_count_mcp, align_type, gap_video_prev_last_hit_to_first_attempt_s`.
For `text_cornell`: `gender, scoreline_raw, players, score` (parsed), texts, no timing fields. Pool streams: `point_idx_mcp` and `rally_count_mcp` only.
`points_<tag>.csv` columns: PBP (`pbp_*`, `elapsed_s`), MCP (`mcp_*`), TennisVL (`tv_*`), timing (`offset_used_s, resid_s, est_video_serve_s, timing_source, gap_*, dead_time_before_s, prev_rally_duration_s`).
"""
open(CORPUS / "README.md", "w", encoding="utf-8").write(txt)
print("README written", len(txt))
