# corpus/: commentary corpus for the 2019 Wimbledon final (and held-out / reference / written streams)

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

| stream | medium | records | with text | words raw | words dedup | words corrected | sha256 (jsonl, first 12) |
|---|---|---|---|---|---|---|---|
| `text_cornell` | text | 3962 | 3962 | 175569 | 175569 | 175569 | c878a4075f3a |
| `tv_2019wimF` | tv | 481 | 373 | 11788 | 9702 | 9705 | 4dc19ae8ed8d |
| `tv_2023wimF` | tv | 368 | 271 | 8407 | 7168 | 7171 | 9db11705d879 |
| `tv_pool_20190126-W-Australian_Open-F-Naomi_Osaka-Petra_Kvitova` | tv | 257 | 216 | 8110 | 6503 | 6507 | f9b4b8fdb67b |
| `tv_pool_20200202-M-Australian_Open-F-Novak_Djokovic-Dominic_Thiem` | tv | 344 | 295 | 9236 | 8341 | 8341 | 32bcbb67fcea |
| `tv_pool_20201010-W-Roland_Garros-F-Iga_Swiatek-Sofia_Kenin` | tv | 68 | 55 | 1981 | 1582 | 1582 | ca81bd324ed9 |
| `tv_pool_20210220-W-Australian_Open-F-Naomi_Osaka-Jennifer_Brady` | tv | 164 | 127 | 4031 | 3255 | 3255 | c7ae8bbab485 |
| `tv_pool_20210613-M-Roland_Garros-F-Stefanos_Tsitsipas-Novak_Djokovic` | tv | 298 | 254 | 8918 | 7761 | 7761 | 2ce28a316016 |
| `tv_pool_20210911-W-US_Open-F-Emma_Raducanu-Leylah_Fernandez` | tv | 165 | 131 | 4153 | 3473 | 3473 | 3cd710827281 |
| `tv_pool_20220130-M-Australian_Open-F-Rafael_Nadal-Daniil_Medvedev` | tv | 389 | 337 | 13625 | 11437 | 11437 | 346ca4066090 |
| `tv_pool_20220531-M-Roland_Garros-QF-Novak_Djokovic-Rafael_Nadal` | tv | 271 | 244 | 9447 | 7961 | 7964 | bbc471d04bfd |
| `tv_pool_20220911-M-US_Open-F-Casper_Ruud-Carlos_Alcaraz` | tv | 218 | 167 | 9907 | 6190 | 6190 | f0928bcba7d3 |
| `tv_pool_20230610-W-Roland_Garros-F-Iga_Swiatek-Karolina_Muchova` | tv | 233 | 183 | 4348 | 3775 | 3776 | 4a833636649e |
| `tv_pool_20230910-M-US_Open-F-Novak_Djokovic-Daniil_Medvedev` | tv | 193 | 170 | 7994 | 5961 | 5961 | b0da636efe8b |
| `tv_pool_20240128-M-Australian_Open-F-Jannik_Sinner-Daniil_Medvedev` | tv | 339 | 287 | 11042 | 9231 | 9231 | 4ee179ee7687 |
| `tv_pool_20240608-W-Roland_Garros-F-Iga_Swiatek-Jasmine_Paolini` | tv | 109 | 93 | 2637 | 2342 | 2342 | d3df32a74f1a |
| `tv_pool_20240713-W-Wimbledon-F-Jasmine_Paolini-Barbora_Krejcikova` | tv | 176 | 151 | 4551 | 3796 | 3796 | 8a524011e347 |
| `tv_pool_20240908-M-US_Open-F-Taylor_Fritz-Jannik_Sinner` | tv | 187 | 155 | 8224 | 5744 | 5744 | c58d82362225 |
| `tv_pool_20250124-M-Australian_Open-SF-Jannik_Sinner-Ben_Shelton` | tv | 231 | 197 | 8349 | 7068 | 7070 | 06663598a365 |
| `tv_pool_20250712-W-Wimbledon-F-Amanda_Anisimova-Iga_Swiatek` | tv | 91 | 76 | 2862 | 2581 | 2581 | 71df81f6b398 |
| `tv_pool_20250907-M-US_Open-F-Jannik_Sinner-Carlos_Alcaraz` | tv | 254 | 214 | 8856 | 6073 | 6073 | 5ec10b043363 |

  Roles: `tv_2019wimF` MAIN (in-sample); `tv_2023wimF` HELD-OUT; the 18 `tv_pool_<match_id>` streams are an exploratory REFERENCE POOL
  for cross-match formula identification only (together 3987 records, 3352 with text,
  103074 words after de-duplication); `text_cornell` is the WRITTEN CONTRAST (Cornell / Sports Mole live text,
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
| 1 | `build_timing.py` | `timing/points_{2019wimF,2023wimF}.csv`, `timing/shots_*.csv`, `reports/timing_report_*.json`, `reports/unmatched_*.tsv`, `reports/clip_alignment_*.json` |
| 2 | `validate_timing.py` | `reports/timing_validation_2019wimF.{json,tsv}` |
| 3 | `build_transcripts.py` | `transcripts/<stream>.jsonl` (raw + de-duplicated text, alignment; frame-derived times at nominal 25 fps) |
| 3a | `detect_fps.py`, `apply_fps_correction.py` | `fps_by_stream.json`; frame-derived times recomputed at the detected fps; `timing_corrections.log`, `reports/timing_corrections_summary.json` (section 3.3) |
| 4 | `apply_corrections.py` | `corrections.tsv`, `corrections.log`, `text_corrected` |
| 5 | `tag_phase.py` | `phase*`, `speaker_cues` fields; `reports/phase_summary.json` |
| 6 | `make_manifest.py` | `transcripts/manifest.json`, `transcripts/meta_<stream>.csv` |
| 7-8 | `asr_sample.py`, `asr_proxy.py` | `reports/asr_proxy.json` (sample text itself goes to gitignored `raw/derived_scratch/`) |
| 9 | `align_validation.py` | `reports/alignment_sample20.tsv`, `reports/alignment_validation.json` |
| 10 | `make_readme.py` | this file |

## 2. Provenance of the existing transcripts

* Source: TennisVL test split, `corpus/raw/tennisexpert_repo/data/tennis_data_test_stats_.json` (commit 8b778bc of
  github.com/LZYAndy/TennisExpert; paper Liu et al. 2026, arXiv:2603.13397), field `audio_transcription (background context)` in the
  `Metadata:` dict of each `gpt` turn. File sha256 49faad1351c811cc... (full value in `manifest.json`).
* ASR system: "WhisperX" per the paper; model size, VAD and alignment window are **not stated** in the files. The raw file is untouched; `text_raw`
  is that field verbatim. The LLM-written `gpt` commentary (Gemini 3 Pro per the paper) is **dropped** and never written to any output.
* Broadcaster: not named in the files. `broadcaster` is "unnamed; probably BBC TV [unverified]" for 2019 (hints: 'Boris' 19x, 'Tim' 7x);
  hints for other matches are recorded in `broadcaster_hints`. All labels unverified.
* Timing sources: TennisVL per-shot `hit_timestamp_second` (video seconds, automatic parser); Sackmann slam point-by-point `ElapsedTime`
  (HF mirror of the removed upstream repo, CC BY-NC-SA 4.0, attribution Jeff Sackmann); Match Charting Project shot codes (CC BY-NC-SA 4.0,
  Tennis Abstract MCP, charter "Zindaras" for the 2019 final). No audio onset detection (librosa) was possible: no audio.

## 3. Per-point alignment (TennisVL x PBP x MCP)

**Clips and groups.** The 2019 file has 481 clips, the 2023 file 368. A point can have two clips: a first-serve-fault clip
(single shot, type `first serve`, outcome `unforced-error`, role `first_serve_fault`) and the clip of the point proper. Consecutive clips with an identical
score state are therefore merged into one **group** (a point cannot repeat its score state on the next point). Clip roles, 2019: {'rally': 325, 'ace': 34, 'first_serve_fault': 115, 'double_fault': 7};
2023: {'rally': 261, 'ace': 22, 'first_serve_fault': 80, 'double_fault': 5}. `clip_role` is a field of every record. Groups: 376 (2019), 294 (2023).

**Score states.** PBP: the state *before* each point is the previous row's after-point state (sets from `SetWinner`, games and points from the previous row; the two `0X`/`0Y`
placeholder rows per match are dropped: ['0X', '0Y'] in 2019, ['0X', '0Y'] in 2023; 422 and 334 points remain).
PBP P1 = Djokovic (2019) and Alcaraz (2023); MCP player 1 = Federer (2019) and Djokovic (2023). Everything is therefore keyed by player **surname**.

**Join key** = (server surname, sets by surname, games by surname, points by surname) before the point; occurrence order resolves the
repeats (e.g. several 40-40 states in one game) by a monotone dynamic-programming alignment of the chronological clip groups to the chronological PBP points.
Match tiers, in decreasing strictness: `key` (full key identical, non-tie-break); `key_tb` (tie-breaks: TennisVL writes tie-break points as 0/15/30/40 for counts 0-3 and cannot
express higher counts, so only server+sets+games must agree, with the clock residual within a tolerance); `key_no_server` (TennisVL names the wrong server, a parser error; identical sets/games/points and clock residual within tolerance).
The 5th-set tie-break is at 12-12 in 2019 and 6-6 in 2023 (`final_set_tb`).

| | 2019 final | 2023 final |
|---|---|---|
| clips aligned to a PBP point | 473 of 481 (98.3%) | 348 of 368 (94.6%) |
| groups aligned | 368 of 376 | 276 of 294 |
| match types | {'key_tb': 3, 'key': 359, 'key_no_server': 6} | {'key': 231, 'key_no_server': 44, 'key_tb': 1} |
| PBP points with at least one clip | 368 of 422 (87.2%) | 276 of 334 (82.6%) |
| PBP points with the point-proper (rally/ace/DF) clip | 358 | 268 |
| MCP points whose key equals the PBP key at the same index | 422 of 422 | 334 of 334 |
| TennisVL shots (all listed in `shots_*.csv`) | 1939 | 1488 |

MCP and PBP agree on the key for every point of both finals (`Pts` is server-first; MCP points are therefore joined to PBP by index and verified by key).
**Unmatched clips (2019, 8)**, with their parsed state, are in `reports/unmatched_2019wimF.tsv`:
| first hit s | clip frames | server | n_shots |
|---|---|---|---|
| 1026.76 | 25643_26018 | FEDERER | 10 |
| 1735.0 | 43349_43442 | DJOKOVIC | 2 |
| 2554.88 | 63736_64130 | DJOKOVIC | 4 |
| 5654.6 | 141339_141414 | DJOKOVIC | 1 |
| 8509.6 | 212714_212836 | FEDERER | 1 |
| 8996.2 | 224879_224972 | FEDERER | 2 |
| 9640.16 | 240978_241053 | FEDERER | 1 |
| 12281.8 | 307019_307168 | DJOKOVIC | 3 |

2023: 18 unmatched groups (20 clips); list in `reports/unmatched_2023wimF.tsv`. In both matches most unmatched clips have a
state that the TennisVL parser mis-states (in the cases inspected: a wrong server together with a score or game count that does not occur at that point in PBP); the cause was not checked clip by clip; they are left unaligned
(`point_idx_pbp` null) rather than forced. PBP points **without any clip** (`timing_source = pbp_elapsed_only`): 2019 54 points; 2023 58 points
(point numbers are in the `point_idx` column of the points tables).
Pool streams have no PBP/clock; their clips are aligned to MCP points (key only, no clock) where an MCP chart exists
(all pool matches except 2019 AO women's and 2021 USO women's final). Per pool match, aligned clips: see `meta_<stream>.csv` (`point_idx_mcp`, `align_type`).

### 3.1 Video clock vs PBP clock

The TennisVL time is seconds in the (unnamed) source video; PBP `ElapsedTime` is the match clock. Residual = TennisVL first-serve-attempt time minus (ElapsedTime + offset).

* **2019 final: one constant offset, no cuts.** Intercept 26.75 s with slope 0.999997 (so slope 1); with slope fixed to 1 the offset is
  26.72 s. Residual SD **0.281 s** over the 353 points within 3 s of the offset
  (95.9% of 368 aligned points); robust SD (1.4826 x MAD) 0.356 s; SD over all aligned points
  including the 15 outliers 2.48 s.
  ElapsedTime is the time of the **first serve of the point**: 9 of the 10 positive outliers
  (8.36 to 15.68 s) are second-serve points whose first-serve fault clip is absent from TennisVL, so the clip starts at the second serve.
  5 negative outliers (-15.88 to -13.52 s) are unexplained (clip grouping or a parser timestamp error).
* **2023 final: the offset is piecewise constant.** The source video lacks the changeover/set-break periods: 23 cuts, of which
  21 have a changeover or set break inside the interval between the last point before and the first point after the cut.
  A single linear offset is therefore invalid (SD over all points 43.7 s); the residual about the local level is SD **0.296 s**
  for the 236 of 276 aligned points within 3 s of their level (robust SD 0.415 s). Consequences: video-seconds gaps across changeovers in 2023 are
  censored (`gap_video_*` is not the real elapsed time there; use the PBP-based `gap_pbp_prev_point_s` / `dead_time_before_s`), and the 2023 transcripts contain no talk from the omitted breaks.

2023 segments (level = video seconds minus ElapsedTime; a segment needs at least 3 anchor points):

| start point | level s | jump s | anchors | cut interval (points) | changeover/set break inside |
|---|---|---|---|---|---|
| 2 | 7.36 | - | 9 | - | - |
| 11 | -45.04 | -52.4 | 7 | [10, 11] | True |
| 23 | -131.0 | -85.96 | 10 | [22, 23] | True |
| 36 | -190.84 | -59.84 | 8 | [34, 36] | True |
| 46 | -296.56 | -105.72 | 17 | [43, 46] | True |
| 69 | -371.56 | -75.0 | 17 | [67, 69] | True |
| 89 | -452.52 | -80.96 | 8 | [86, 89] | True |
| 98 | -550.46 | -97.94 | 8 | [96, 98] | True |
| 107 | -636.22 | -85.76 | 9 | [106, 107] | True |
| 121 | -721.22 | -85.0 | 4 | [119, 121] | True |
| 140 | -858.4 | -137.18 | 6 | [125, 140] | True |
| 148 | -908.72 | -50.32 | 10 | [146, 148] | True |
| 160 | -1006.12 | -97.4 | 18 | [159, 160] | True |
| 201 | -1127.84 | -121.72 | 7 | [187, 201] | True |
| 210 | -1559.36 | -431.52 | 4 | [207, 210] | True |
| 216 | -1606.84 | -47.48 | 18 | [214, 216] | True |
| 240 | -1706.6 | -99.76 | 10 | [238, 240] | False |
| 254 | -1815.04 | -108.44 | 7 | [253, 254] | True |
| 266 | -1915.72 | -100.68 | 10 | [263, 266] | True |
| 277 | -2054.04 | -138.32 | 17 | [276, 277] | False |
| 298 | -2145.88 | -91.84 | 7 | [297, 298] | True |
| 307 | -2230.98 | -85.1 | 8 | [306, 307] | True |
| 319 | -2321.2 | -90.22 | 7 | [318, 319] | True |
| 329 | -2413.6 | -92.4 | 5 | [327, 329] | True |

### 3.2 Which source each point's timing uses

`points_*.csv` column `timing_source`: `tennisvl_hit_times` = first/last strike times from TennisVL hit timestamps (point-proper clip present; 2019: 358 points,
2023: 268); `tennisvl_fault_clip_only` = only the first-serve-fault clip exists (2019: 10, 2023: 8);
`pbp_elapsed_only` = no clip, only the PBP clock (2019: 54, 2023: 58); `est_video_serve_s` = ElapsedTime + local offset (an estimate of the video time of the first serve).
`rally_duration_s` = last hit minus first hit of the point-proper clip (TennisVL). `dead_time_before_s` = (ElapsedTime of this point - ElapsedTime of the previous point) - previous rally duration; null when the previous point
has no point-proper clip. `gap_video_prev_last_hit_to_first_attempt_s` = video-clock gap between the previous point's last hit and this point's first serve attempt (both TennisVL).
Hit times for every shot are in `shots_*.csv` (`inter_shot_interval_s` = interval to the previous shot in the same clip).

### 3.3 Video frame rate per stream and the frame-rate correction

`clip_start_frame`/`clip_end_frame` come from the clip file names; `hit_timestamp_second` is seconds in the source video. The first build converted frames at a nominal 25 fps for every stream (Phase 1 had verified 25 fps for the 2019 final only).
The Phase 2b analyst found that this is wrong for some pool streams. `detect_fps.py` now detects the rate per stream from the raw TennisVL data: for each clip, a rate is consistent if all hit times lie inside
[start_frame/fps, end_frame/fps] (tolerance 0.01 s, the rounding of the hit times). The table gives the share of clips consistent with each candidate; the decision is the candidate (25, 29.97 = 30000/1001, 30) with the highest share if that share is >= 0.95.
`feasible interval` = the range of fps consistent with every clip of the stream (max of start/first-hit, min of end/last-hit). Stream 20220911 (0.5% of clips consistent with each of 25, 29.97 and 30 at best) is consistent with 29.0 for 100% of clips
(feasible interval [29.0, 29.0004]); 29.0 is not a broadcast standard rate, so that value is an empirical rate of the file as TennisVL cut it [cause unverified]; it is used as detected and flagged NONSTANDARD.
Frame-derived fields are then recomputed in a separate, logged step (`apply_fps_correction.py`; per-stream before/after summary in `timing_corrections.log`, machine-readable in `reports/timing_corrections_summary.json`):
`clip_start_s`, `clip_end_s`, `t_since_prev_last_hit_s`, `t_to_next_first_hit_s`. Not frame-derived and therefore unchanged: `first_hit_s`, `last_hit_s`, `rally_duration_s`, `dead_time_before_s`,
`gap_video_prev_last_hit_to_first_attempt_s`, and all of `timing/*.csv` (hit-time and PBP based; `build_timing.py` never uses frames). The step asserts this. Raw data in `raw/` is untouched; the per-stream fps is also in `transcripts/manifest.json` (`video_fps`).

| stream | n clips | share @25 | share @29.97 | share @30 | decided fps | feasible interval | flag | clip times changed | max abs change t_to_next (s) | share t_to_next < 0 before -> after |
|---|---|---|---|---|---|---|---|---|---|---|
| pool_20250907-M-US_Open-F-Jannik_Sinner-Carlos_Alcaraz | 254 | 0.000 | 1.000 | 0.209 | 29.97 | [29.9687, 29.9723] | ok | 254 | 1605.008 | 0.984 -> 0.000 |
| pool_20250712-W-Wimbledon-F-Amanda_Anisimova-Iga_Swiatek | 91 | 1.000 | 0.000 | 0.000 | 25.0 | [24.9993, 25.0043] | ok | 0 | 0.0 | 0.000 -> 0.000 |
| pool_20250124-M-Australian_Open-SF-Jannik_Sinner-Ben_Shelton | 231 | 0.000 | 1.000 | 0.264 | 29.97 | [29.9695, 29.9727] | ok | 231 | 1815.172 | 0.983 -> 0.000 |
| pool_20240908-M-US_Open-F-Taylor_Fritz-Jannik_Sinner | 187 | 0.000 | 1.000 | 0.283 | 29.97 | [29.97, 29.9722] | ok | 187 | 1501.09 | 0.968 -> 0.000 |
| pool_20240713-W-Wimbledon-F-Jasmine_Paolini-Barbora_Krejcikova | 176 | 1.000 | 0.000 | 0.000 | 25.0 | [24.9987, 25.0021] | ok | 0 | 0.0 | 0.000 -> 0.000 |
| pool_20240608-W-Roland_Garros-F-Iga_Swiatek-Jasmine_Paolini | 109 | 1.000 | 0.000 | 0.000 | 25.0 | [24.9988, 25.0043] | ok | 0 | 0.0 | 0.000 -> 0.000 |
| pool_20240128-M-Australian_Open-F-Jannik_Sinner-Daniil_Medvedev | 339 | 1.000 | 0.000 | 0.000 | 25.0 | [24.999, 25.0006] | ok | 0 | 0.0 | 0.000 -> 0.000 |
| pool_20230910-M-US_Open-F-Novak_Djokovic-Daniil_Medvedev | 193 | 0.000 | 1.000 | 0.244 | 29.97 | [29.97, 29.9704] | ok | 193 | 1829.361 | 0.990 -> 0.000 |
| tv_2023wimF | 368 | 1.000 | 0.000 | 0.000 | 25.0 | [25.0, 25.0002] | ok | 0 | 0.0 | 0.000 -> 0.000 |
| pool_20230610-W-Roland_Garros-F-Iga_Swiatek-Karolina_Muchova | 233 | 1.000 | 0.000 | 0.000 | 25.0 | [25.0, 25.0006] | ok | 0 | 0.0 | 0.000 -> 0.000 |
| pool_20220911-M-US_Open-F-Casper_Ruud-Carlos_Alcaraz | 218 | 0.000 | 0.005 | 0.005 | 29.0 | [29.0, 29.0004] | NONSTANDARD | 218 | 1971.741 | 0.959 -> 0.000 |
| pool_20220531-M-Roland_Garros-QF-Novak_Djokovic-Rafael_Nadal | 271 | 1.000 | 0.000 | 0.000 | 25.0 | [25.0, 25.0003] | ok | 0 | 0.0 | 0.000 -> 0.000 |
| pool_20220130-M-Australian_Open-F-Rafael_Nadal-Daniil_Medvedev | 389 | 1.000 | 0.000 | 0.000 | 25.0 | [25.0, 25.0002] | ok | 0 | 0.0 | 0.000 -> 0.000 |
| pool_20210911-W-US_Open-F-Emma_Raducanu-Leylah_Fernandez | 165 | 0.000 | 1.000 | 0.364 | 29.97 | [29.9652, 29.9714] | ok | 165 | 1148.184 | 0.982 -> 0.000 |
| pool_20210613-M-Roland_Garros-F-Stefanos_Tsitsipas-Novak_Djokovic | 298 | 1.000 | 0.000 | 0.000 | 25.0 | [24.9998, 25.0009] | ok | 0 | 0.0 | 0.000 -> 0.000 |
| pool_20210220-W-Australian_Open-F-Naomi_Osaka-Jennifer_Brady | 164 | 1.000 | 0.000 | 0.000 | 25.0 | [24.9999, 25.0029] | ok | 0 | 0.0 | 0.000 -> 0.000 |
| pool_20201010-W-Roland_Garros-F-Iga_Swiatek-Sofia_Kenin | 68 | 1.000 | 0.000 | 0.000 | 25.0 | [25.0, 25.0019] | ok | 0 | 0.0 | 0.000 -> 0.000 |
| pool_20200202-M-Australian_Open-F-Novak_Djokovic-Dominic_Thiem | 344 | 1.000 | 0.000 | 0.000 | 25.0 | [25.0, 25.0013] | ok | 0 | 0.0 | 0.000 -> 0.000 |
| tv_2019wimF | 481 | 1.000 | 0.000 | 0.000 | 25.0 | [25.0, 25.0002] | ok | 0 | 0.0 | 0.000 -> 0.000 |
| pool_20190126-W-Australian_Open-F-Naomi_Osaka-Petra_Kvitova | 257 | 1.000 | 0.000 | 0.000 | 25.0 | [24.9994, 25.0016] | ok | 0 | 0.0 | 0.000 -> 0.000 |

## 4. De-duplication (text_raw -> text_dedup)

Consecutive clips often carry the same ASR text (the transcript window of a clip overlaps its neighbours). Rule, applied per stream in clip order:

* **R1 exact repeat**: if the lower-cased word sequence of clip *i* equals that of the most recent preceding non-empty clip at most 3 clips back, `text_dedup` is empty and `dedup_of` points to the first occurrence of the run.
* **R2 suffix-prefix overlap**: otherwise, if the last *k* words of the previous clip equal the first *k* words of this one with *k* >= 6, remove those *k* words from this clip.
* **R3 shared prefix**: otherwise, if the first *k* >= 6 words are identical, remove them.
* Shorter coincidences (1-5 words, e.g. a shared '30') are kept. Exact repeats farther than 3 clips back are kept and counted (diagnostic only).

Effect, 2019 final: 55 exact repeats (R1), 0 R2, 0 R3; 2086 of 11788 words removed
(17.7%). 2023: 26 R1, 1239 of 8407 words (14.7%).
All 20 TV streams together: 503 R1, 1 R2/R3. Far repeats not removed (2019 / 2023): 9 / 7.
Per-stream word counts raw/dedup are in the stream table above. The Cornell text is not de-duplicated (`dedup_action = not_applicable_text`).

Transcript window (finding): the first score call in a clip's text equals the PBP score **after** the clip's point in 40 of 59 2019 utterances
(67.8%) and 28 of 39 2023 utterances
(71.8%); so a clip's transcript window reaches from about the clip start to beyond the clip end (into the dead time after the point). Distribution of the offset d
(call = score before point *p*+d), 2019: {'-1': 1, '0': 2, '1': 40, '2': 2, '3': 1, 'none': 13}; 2023: {'0': 3, '1': 28, '2': 2, 'none': 6}. This is a statement about the
alignment at clip level only.

## 5. Name and term corrections (text_dedup -> text_corrected)

`corpus/corrections_rules.tsv` (hand-curated regex rules; columns id, kind, scope, pattern, replacement, confidence, reason) was built by reading the candidate list `reports/correction_candidates.tsv` (ASR tokens that are not
words of the Cornell vocabulary and are close, difflib ratio >= 0.6, to the match's player names), checking contexts in the 2019 and 2023 transcripts, and
checking each replacement name against a lexicon of player names (all `*-matches.csv` of the PBP mirror plus TennisVL `match_info`; column `replacement_in_player_lexicon` of `corrections.tsv`).
`scope` is `all` or the date prefix of the TennisVL match ids. Applied as a **separate step** (`apply_corrections.py`): `text_raw` and `text_dedup` are never modified; every substitution is logged in `corpus/corrections.log`
(stream, utterance, rule, match -> replacement, 4 words of context each side). Counts per rule are in `corpus/corrections.tsv`; total substitutions: **484**
(on de-duplicated text), in 375 utterances. Rule kinds: `name` (player-name variants), `term` (e.g. `left`/`off`/`loud` for `love` in score calls, `juice` for `deuce`, `Fire set` for `Fifth set`), `normalisation` ('breakpoint' to 'break point', 'down the tee' to 'down the T').
Medium/normalisation confidence rules are marked; only errors visible from context are corrected, **many ASR errors remain uncorrected** (e.g. garbled names of non-players such as 'Rochaferra', 'Legrocha', 'Edverson'; the hand sample below found 2 uncorrected name/score-call errors and 4 garbles).
Correction counts: 2019 41, 2023 11, pool 432.

## 6. Phase, speaker tags and time since last strike

* `phase` = `clip` by default (the transcript belongs to a clip, not to a word). **Heuristic** sub-tags, set by regex on `text_corrected` and flagged `phase_heuristic = true`:
  `between_points` when the whole text is a score call (digits <= 2 chars, love, all, deuce, advantage, game, set, player surnames) or a short 'Game <name>' call;
  `changeover` when a cue such as 'changeover', 'change of ends', 'new balls', 'towel', 'set break' occurs. 2019: {'between_points': 14, 'clip': 463, 'changeover': 4}; 2023: {'between_points': 13, 'clip': 350, 'changeover': 5}.
  `phase_tags` also lists `contains_score_call` (a score call somewhere in longer text: 2019 67 utterances).
  **in_rally vs between_points cannot be separated at word level**: no audio and no word timestamps, and a clip's text window (section 4) spans rally and dead time.
  In particular the `changeover` tag can fire on talk about new balls during play. The `in_rally` value is therefore never assigned.
* `speaker_role` is always `unknown`: the files have no speaker labels, so commentator turns cannot be tagged and commentator identity cannot be separated from medium. `speaker_cues` lists **heuristic** umpire/Hawk-Eye cues
  ('Game <name>', 'new balls please', 'ball was called', 'time violation', 'Mr <name> is challenging'): 2019 {'umpire_ball_called': 4, 'umpire_challenge_call': 6, 'umpire_game_call': 5, 'umpire_new_balls': 1}; 2023 {'umpire_time_violation': 1, 'umpire_ball_called': 7, 'umpire_game_call': 1, 'umpire_new_balls': 3}. The umpire's and Hawk-Eye's voices are inside the transcripts and not separated.
* `t_since_prev_last_hit_s` = clip start minus the last hit of the previous clip; `t_to_next_first_hit_s` = first hit of the next clip minus clip end (video seconds, TennisVL). They are **clip-level**: no word has its own time.
  In 2023 they are censored across video cuts (section 3.1).

## 7. Validation

### 7.1 Timing: TennisVL vs MCP and PBP (2019 final)

Convention found in the data: PBP `RallyCount` counts the **in-play shots** (the final erring shot is not counted; double faults 0); MCP and TennisVL count the erring shot too. PBP minus MCP shots over all 422 points is 0 for winners/aces
and -1 for every error ending (`pbp_minus_mcp` = {'-1': 281, '0': 141}); after adding 1 for error endings ('pbp adj') PBP equals MCP for 99.3% of points.

All 358 points that have a TennisVL point-proper clip: `n_shots` equals MCP shots exactly in 82.1% (within one shot in 96.9%); equals PBP adj in 81.8%
(raw PBP RallyCount: 32.1%, because of the convention above). TennisVL minus MCP: {'-4': 2, '-3': 3, '-2': 5, '-1': 31, '0': 294, '1': 22, '2': 1}; in 13 of the 23 over-count cases the first interval is >= 4 s (an extra early serve).
Other checks: stroke wing (forehand/backhand) agrees with the MCP shot letter for 1022 of 1026 shots (99.6%, points with equal shot counts);
serve hitter equals PBP server in 354 of 358; the last shot's outcome class equals the MCP end code (*, @, #) in 80.9% of 319 (forced/unforced labels differ between sources);
the bounce time lies between the hit and the next hit in 100.0% of 1372 shots;
hit intervals: n 1458, median 1.20 s, mean 1.31 s, 1st-99th percentile 0.64-8.31 s, none non-positive.
**Hit intervals cannot be validated independently**: MCP has no clock and PBP ElapsedTime has 1 s resolution; the only external timing check is the serve time vs PBP clock (section 3.1).

**20 random points** (seed 20190714, drawn from the 358 points with a point-proper clip): exact agreement TennisVL = MCP in 15/20, TennisVL = PBP adj in 15/20; within one shot 19/20 (MCP), 19/20 (PBP adj).

| point_idx | set | game | score_before_p1p2 | tv_n_shots | mcp_n_shots | pbp_rally_count | pbp_rc_adj | tv_eq_mcp | tv_eq_pbp_adj | interval_mean_s | interval_min_s | interval_max_s | wing_agree |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 19 | 1 | 4 | 30-15 | 7 | 6 | 5 | 6 | 0 | 0 | 3.37 | 0.72 | 14.08 |  |
| 24 | 1 | 4 | 40-40 | 2 | 2 | 1 | 2 | 1 | 1 | 0.72 | 0.72 | 0.72 | 1/1 |
| 40 | 1 | 6 | 40-15 | 5 | 4 | 3 | 4 | 0 | 0 | 3.66 | 0.72 | 11.44 |  |
| 41 | 1 | 7 | 0-0 | 10 | 10 | 9 | 10 | 1 | 1 | 1.35 | 0.64 | 2.08 | 9/9 |
| 66 | 1 | 11 | 15-15 | 10 | 12 | 12 | 12 | 0 | 0 | 1.38 | 0.8 | 2.56 |  |
| 89 | 2 | 1 | 15-0 | 5 | 5 | 4 | 5 | 1 | 1 | 1.26 | 0.8 | 1.68 | 4/4 |
| 93 | 2 | 2 | 0-0 | 4 | 4 | 3 | 4 | 1 | 1 | 1.15 | 0.64 | 1.52 | 3/3 |
| 153 | 3 | 6 | 15-15 | 2 | 2 | 1 | 2 | 1 | 1 | 0.64 | 0.64 | 0.64 | 0/1 |
| 160 | 3 | 8 | 0-0 | 2 | 2 | 1 | 2 | 1 | 1 | 0.64 | 0.64 | 0.64 | 1/1 |
| 228 | 4 | 6 | 0-15 | 4 | 4 | 3 | 4 | 1 | 1 | 1.17 | 0.72 | 1.44 | 3/3 |
| 230 | 4 | 6 | 0-40 | 6 | 6 | 5 | 6 | 1 | 1 | 1.2 | 0.96 | 1.36 | 5/5 |
| 257 | 5 | 1 | 30-15 | 5 | 6 | 5 | 6 | 0 | 0 | 1.32 | 0.8 | 2.08 |  |
| 279 | 5 | 4 | 40-40 | 3 | 3 | 2 | 3 | 1 | 1 | 1.16 | 0.8 | 1.52 | 2/2 |
| 310 | 5 | 8 | 30-40 | 1 | 1 | 1 | 1 | 1 | 1 |  |  |  | 0/0 |
| 349 | 5 | 15 | 0-0 | 4 | 4 | 3 | 4 | 1 | 1 | 1.12 | 0.64 | 1.6 | 3/3 |
| 362 | 5 | 16 | AD-40 | 5 | 5 | 4 | 5 | 1 | 1 | 1.18 | 0.72 | 1.52 | 4/4 |
| 365 | 5 | 17 | 30-0 | 9 | 9 | 9 | 9 | 1 | 1 | 1.26 | 0.64 | 1.92 | 8/8 |
| 369 | 5 | 18 | 0-0 | 3 | 3 | 2 | 3 | 1 | 1 | 1.0 | 0.72 | 1.28 | 2/2 |
| 374 | 5 | 19 | 0-0 | 6 | 5 | 4 | 5 | 0 | 0 | 1.22 | 0.72 | 1.76 |  |
| 397 | 5 | 23 | 30-0 | 2 | 2 | 1 | 2 | 1 | 1 | 0.72 | 0.72 | 0.72 | 1/1 |

(`score_before_p1p2` is PBP P1-P2 = Djokovic-Federer. A large `interval_max_s` signals a missing or extra shot in the TennisVL rally, e.g. points 19, 40.)

### 7.2 Alignment of utterances to points (2019 final)

Automatic: of 59 aligned utterances with a score call, the first call equals the PBP score after this clip's point in 40, before it in 2,
two points on in 2, and matches no PBP state in points -1..+3 in 13 (ASR/commentator slips, retrospective mentions). 2023: {'0': 3, '1': 28, '2': 2, 'none': 6}.

**Hand check of 20 random aligned utterances** (seed 20190715; drawn from the 59 that contain a parseable score call; I compared the call in the text with the PBP score, server-first):
verdicts {'match_after_this_point': 14, 'no_match': 2, 'retrospective_narration_not_live_call': 1, 'retrospective_narration_coincidental_match': 1, 'match_before_and_later_skips_after': 1, 'match_two_points_later': 1}. That is 14/20 exact matches to the score after the aligned point, 2 more within two points,
2 not matching and 2 where the call is a retrospective mention (not usable as evidence). 4 of 20 are not confirmed as evidence; the 2 'no_match' cases may be a misalignment or an ASR/commentator slip, and the two cannot be told apart here. Judgements are in `corpus/validation/alignment_sample20_judgements.tsv` (hand-made).

| utt_id | point_idx | set | game_in_set | pbp_score_before_this_point | pbp_score_after_this_point | first_call_in_text | call_context_excerpt | verdict |
|---|---|---|---|---|---|---|---|---|
| tv_2019wimF:0000 | 3 | 1 | 1 | 30-0 | 30-15 | 30-15 | 30 15 40 15 | match_after_this_point |
| tv_2019wimF:0068 | 59 | 1 | 10 | 15-30 | 30-30 | 30-0 | irst serves You'd expect nothing less 30-0 Just seeing how both players | no_match |
| tv_2019wimF:0072 | 63 | 1 | 10 | AD-40 | 0-0 | love-30 | om Novak Djokovic the first search from love 30 down the backhand | retrospective_narration_not_live_call |
| tv_2019wimF:0098 | 97 | 2 | 2 | 30-30 | 40-30 | 40-30 | 40 30 That's the textbook play from Federer | match_after_this_point |
| tv_2019wimF:0119 | 113 | 2 | 5 | 30-15 | 40-15 | 40-15 | 40-15 Well it looks like it's not going to | match_after_this_point |
| tv_2019wimF:0157 | 141 | 3 | 4 | 0-0 | 15-0 | 15-love | 15 love Game on again Djokovic fully engaged | match_after_this_point |
| tv_2019wimF:0174 | 156 | 3 | 7 | 0-0 | 15-0 | 15-0 | 15-0 Not a very even keel throughout the wh | match_after_this_point |
| tv_2019wimF:0178 | 161 | 3 | 8 | 15-0 | 30-0 | 30-love | 30 love Wow | match_after_this_point |
| tv_2019wimF:0189 | 171 | 3 | 10 | 0-0 | 0-15 | love-15 | Djokovic had love 15 on Federer's serve Couldn't take advan | retrospective_narration_coincidental_match |
| tv_2019wimF:0243 | 224 | 4 | 5 | 15-15 | 15-30 | 15-30 | 15 30 | match_after_this_point |
| tv_2019wimF:0254 | 232 | 4 | 7 | 15-0 | 15-15 | 15-0 | 15-0 30-15 | match_before_and_later_skips_after |
| tv_2019wimF:0289 | 263 | 5 | 2 | 40-15 | 40-30 | 40-40 | 40-40 | no_match |
| tv_2019wimF:0293 | 265 | 5 | 3 | 0-0 | 0-15 | Love-15 | Love 15 | match_after_this_point |
| tv_2019wimF:0303 | 273 | 5 | 4 | 0-0 | 0-15 | Love-15 | Love 15 Every point counts double There are n | match_after_this_point |
| tv_2019wimF:0378 | 330 | 5 | 12 | 15-0 | 15-15 | 15-30 | He's rediscovering his greatest shot 15 30 | match_two_points_later |
| tv_2019wimF:0425 | 367 | 5 | 17 | 40-15 | 40-30 | 40-30 | 40-30 Game Djokovic | match_after_this_point |
| tv_2019wimF:0438 | 377 | 5 | 19 | 30-15 | 40-15 | 40-15 | Oh it's working better 40-15 Going through with the ball Gets his | match_after_this_point |
| tv_2019wimF:0451 | 388 | 5 | 21 | 30-30 | 40-30 | 40-30 | 40 30 Reached for the forehand and it flew o | match_after_this_point |
| tv_2019wimF:0463 | 398 | 5 | 23 | 40-0 | 40-15 | 40-15 | 40-15 | match_after_this_point |
| tv_2019wimF:0464 | 399 | 5 | 23 | 40-15 | 40-30 | 40-30 | 40-30 40 love back to 40-30 Djokovic will b | match_after_this_point |

### 7.3 ASR error estimate: WER is unknown

No audio and no human reference transcript exist, so the word error rate **cannot be measured and is unknown**. Internal proxies only:

* **Hand-read sample** (seed 500190714): 500 words in 18 randomly drawn 2019 clips (`text_dedup`), read by me for implausible tokens. Errors found: 11 ({'name_misspelled': 2, 'score_call_impossible': 5, 'other_garble': 4}),
  i.e. **22.0 per 1,000 words** (Wilson 95% CI 12.3-39.0); misspelled player names + impossible score calls only: **14.0 per 1,000**
  (CI 6.8-28.6). 5 of the 11 are fixed by the correction list. The sample is drawn by clip, so short score-call clips are over-represented relative to words; the automatic proxy below is the better rate for score calls.
  This is a **lower bound** on the error rate: substitutions that give a plausible English word cannot be seen without audio.
* **Automatic proxy** (all words of the stream, after de-duplication): player-name variants fixed by rules N*: 2019 1.96 per 1,000 words, 2023 0.56,
  all TV streams 3.34; 'love' errors in score calls fixed by rules T03-T05: 2019 1.65, 2023 0.28, all TV 0.28;
  score calls (after correction) matching no PBP state in points -1..+3 of the aligned point: 2019 7 of 75 (0.72 per 1,000 words), 2023 5 of 42 (0.70 per 1,000).

Errors found in the hand sample (excerpts, `corpus/validation/asr_sample_errors.tsv`):

| utt_id | excerpt | type | fixed by rule |
|---|---|---|---|
| tv_2019wimF:0190 | Novak Legrocha start | name_misspelled | False |
| tv_2019wimF:0284 | Game Diogovic | name_misspelled | True |
| tv_2019wimF:0274 | Holti, 15 | score_call_impossible | False |
| tv_2019wimF:0229 | 15 left | score_call_impossible | True |
| tv_2019wimF:0036 | 30 off | score_call_impossible | True |
| tv_2019wimF:0056 | 15 left | score_call_impossible | True |
| tv_2019wimF:0050 | 15 left | score_call_impossible | True |
| tv_2019wimF:0284 | First game, final second | other_garble | False |
| tv_2019wimF:0224 | For said both | other_garble | False |
| tv_2019wimF:0190 | That's what you sent | other_garble | False |
| tv_2019wimF:0056 | Inter rally | other_garble | False |

## 8. Known gaps

1. No audio: no WER, no word times, no librosa onset times, no speaker labels, no intonation units. Utterance time = clip window; the transcript window extends beyond the clip (section 4).
2. One TV track per match: no broadcaster or medium contrast within a match; broadcaster labels unverified. Commentator identity is confounded with medium and match.
3. Coverage: 373 of 481 2019 clips have text; 54 of 422 points have no clip at all (their commentary is not in the corpus, so the transcript is a sample of the match, not a complete record). 2023: 271 of 368, 58 of 334 points without clip, and changeover talk is cut from the video.
4. The transcripts include the umpire's and Hawk-Eye's voices ('Game <name>', 'ball was called') and stadium announcements, unseparated.
5. TennisVL score states contain parser errors (wrong server, tie-break points), shot counts are within one of MCP in 96.9% only; hit timestamps come from an automatic parser (no manual check of absolute times beyond section 3.1).
6. PBP `ElapsedTime` has 1 s resolution and marks the first serve of a point. PBP `RallyCount` excludes the final erring shot (section 7.1). MCP `Pts` in tie-breaks is unreliable in places (MCP key equals PBP key for all points, but the MCP tie-break score sequence has visible oddities, e.g. in the 2019 first-set tie-break).
7. The MCP shot count is parsed from the shot codes by a simple rule (serve plus every stroke letter in the code that ends the point); `mcp_n_shots` is a heuristic count (agrees with PBP adj in 99.3% of points).
8. Corrections are conservative and incomplete; normalisation rules (T08-T11) change spelling variants and can be switched off by using `text_dedup`.
9. Cornell text: no match ids, dates or timestamps; the scoreline gives only players and score (parsed for all 3962 updates; the `*` marker side is read heuristically as the server side and the dataset README does not define it) [unverified].
10. Licences: TennisVL "strictly for academic research in sports video understanding" (scope question is in FOR_HUMAN.md); MCP and slam PBP CC BY-NC-SA 4.0 (attribution: Jeff Sackmann, Tennis Abstract Match Charting Project); the derived tables committed here (points, shots, meta) inherit ShareAlike; Cornell data from Fu, Danescu-Niculescu-Mizil and Lee 2016, no licence stated.
   Full source texts are never committed (jsonl gitignored); committed text excerpts are at most 15 words.

## 9. Field dictionary (`transcripts/<stream>.jsonl`; `meta_<stream>.csv` has the same fields without the three text fields, plus `n_words_*`)

`stream, medium, broadcaster, broadcaster_hints, match_id, utt_id, clip, clip_i, clip_start_frame, clip_end_frame, clip_start_s, clip_end_s` (frames / the stream's detected fps, section 3.3),
`first_hit_s, last_hit_s, n_shots, clip_role, rally_duration_s` (this clip's TennisVL hits), `score_before` (server, sets, games, points before the point; TennisVL), `point_outcome`,
`set_no, game_in_set, tiebreak_state` (derived from score_before, or from PBP when aligned), `text_raw` (untouched ASR), `text_dedup` (section 4), `text_corrected` (section 5), `dedup_action, dedup_k_removed, dedup_of`,
`phase, phase_heuristic, phase_tags, speaker_role, speaker_cues` (section 6), `t_since_prev_last_hit_s, t_to_next_first_hit_s`,
`point_idx_pbp, point_idx_mcp, game_no_pbp, elapsed_prev_point_s` (ElapsedTime_prev_point), `elapsed_this_point_s` (ElapsedTime_this_point), `dead_time_before_s, rally_count_pbp, rally_count_mcp, align_type, gap_video_prev_last_hit_to_first_attempt_s`.
For `text_cornell`: `gender, scoreline_raw, players, score` (parsed), texts, no timing fields. Pool streams: `point_idx_mcp` and `rally_count_mcp` only.
`points_<tag>.csv` columns: PBP (`pbp_*`, `elapsed_s`), MCP (`mcp_*`), TennisVL (`tv_*`), timing (`offset_used_s, resid_s, est_video_serve_s, timing_source, gap_*, dead_time_before_s, prev_rally_duration_s`).
