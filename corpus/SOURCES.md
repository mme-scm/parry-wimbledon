# Corpus sources (Phase 0)

Compiled by corpus-scout on 2026-10-07. Every count below comes from the scripts in `corpus/scripts/`
(`bash corpus/scripts/phase0_numbers.sh`, log in `corpus/raw/derived_scratch/phase0_numbers.log`), run on files
fetched by `bash corpus/scripts/fetch_phase0.sh`. Downloads live in `corpus/raw/` (gitignored, never committed).
Commentary quotations here are at most 15 words. "Not inspected" marks claims taken from documentation only.

## 1. Bottom line

* **No acceptable source gives the same match from more than one broadcaster, or in more than one medium.**
  The only acceptable spoken-commentary source is TennisVL. Its ASR transcripts are in the 20 test matches only,
  with one TV commentary track per match. Radio and second-broadcaster routes all need human action (FOR_HUMAN.md).
* **Recommended match: 2019 Wimbledon men's final, Djokovic v Federer, 14 July 2019**
  (`20190714-M-Wimbledon-F-Roger_Federer-Novak_Djokovic`). Four data sources are aligned on it:
  1. TennisVL WhisperX transcripts of one TV commentary, **probably BBC Television**. The files do not name the
     broadcaster. This is inferred because the commentators address "Boris" 19 times and "Tim" 7 times, and one
     line reads "the gentleman on my left, Tim Henman" [unverified].
     Coverage: 373 of 481 rally clips have transcripts, 11,772 words in total, about 9,837 after removing text
     repeated from the previous clip.
  2. TennisVL parser timing: per-shot `hit_timestamp_second` for 1,939 shots, plus clip frame spans
     (25 fps, all 481 of 481 clips checked).
  3. Sackmann slam point-by-point: `ElapsedTime` for all 422 points, running 0:00:00 to 4:56:59.
  4. Match Charting Project: human-charted shot-by-shot records of all 422 points.
* Ranking used: number of broadcasters, then mix of media, then timing, then transcript quality. On the first two,
  all TennisVL matches tie at 1 broadcaster and TV only, so timing decides. The 2019 final is the
  text-richest match that has all three timing layers. 2022 AO F has more text (11,507 unique words) but no
  elapsed-time PBP (see the table in section 4).
* **Held-out partner match:** 2023 Wimbledon final, Alcaraz v Djokovic (`20230716-M-Wimbledon-F-Novak_Djokovic-Carlos_Alcaraz`).
  It has the same three timing layers and 7,225 unique words. Its broadcaster hints differ ("Todd" ×4, "Tim" ×5),
  so it is probably a different broadcaster [unverified].
* **Contrast corpus (written genre):** Cornell Sports Mole live text. It has 3,962 updates and 175,714 words, but
  no match IDs and no timestamps, and it covers different matches.
* **Never use TennisVL's `gpt` "commentary" as commentary.** It was written by an LLM (Gemini 3 Pro).
  At most it could serve as an explicitly labelled LLM contrast; the orchestrator decides.

## 2. What was downloaded (paths under `corpus/raw/`)

Total on disk is about 394 MB, which includes unzipped Cornell JSON and derived scratch files.
About 400 MB was transferred. `corpus/raw/monro` and `corpus/raw/perseus` belong to another agent.

| Path | Bytes | Command (full script: `corpus/scripts/fetch_phase0.sh`) |
|---|---|---|
| `tennisexpert_repo/` (blobless git clone @ 8b778bc; `data/`, `README.md` checked out) | .git 2.9 MB | `git clone --filter=blob:none --no-checkout https://github.com/LZYAndy/TennisExpert.git`; `git checkout HEAD -- data/ README.md` |
| `tennisexpert_repo/data/tennis_data_test_stats_.json` | 18,503,150 | (in repo) sha256 49faad1351c811cc… |
| `tennisexpert_repo/data/tennis_vl_test.json` | 13,393,763 | (in repo) sha256 c9c2c22d1f1d29bd… |
| `tennisexpert_repo/data/{README.md,dataset_info.json}` | 133; 16,547 | (in repo) |
| `tennisvl_train/tennis_data_train_stats_.json` | 123,644,319 | `curl -L "https://drive.usercontent.google.com/download?id=1raeJJoyGxDyZxNeAo7uk2ngsvlwMQ9SI&export=download&confirm=t"` sha256 dd14027989b93b8e… |
| `tennisvl_paper/arxiv_2603.13397v2.html`, `paper.txt` | 498,875 | `curl https://arxiv.org/html/2603.13397v2` |
| `cornell_tennis/tennis_data.zip` + `extracted/` | 15,944,110 (zip) | `curl https://www.cs.cornell.edu/~liye/tennis_data.zip`; `unzip -x '__MACOSX/*'` sha256 0e1c147dd5b4e151… |
| `cornell_tennis/tennis_README.txt`, `tennis.html` | small | `curl` from www.cs.cornell.edu/~liye/ |
| `sackmann_mcp/` README.md, charting-{m,w}-matches.csv, charting-{m,w}-points-{2010s,2020s}.csv | 148,623,198 total | `curl https://raw.githubusercontent.com/JeffSackmann/tennis_MatchChartingProject/1813a13…/<file>` |
| `sackmann_slam_pbp_hfmirror/` LICENSE, README.md, UPSTREAM_README.md, {2019-wimbledon,2020-ausopen,2021-frenchopen,2023-wimbledon}-points.csv, 12 `*-matches.csv` | about 25 MB | `curl -L https://huggingface.co/datasets/Aneeshers/tennis-sackmann-archive/resolve/8ac86f7…/slam_pointbypoint/<file>` |
| `tenniset/README_master.md`, `tenniset/repo/` (blobless; LICENSE, data/README.md), `tenniset/annotations/{captions.txt,points.txt,V006.json}` | about 150 KB | raw.githubusercontent + Google Drive file IDs (see script) |
| `livecc/README.md`, `livecc/live_whisperx_100_for_preview.json` | 1,008,838 | `curl -L https://huggingface.co/datasets/chenjoya/Live-WhisperX-526K/resolve/main/<file>` |
| `hf_misc/SCBench_CommentarySet_README.md`, `hf_misc/TennisNLData_sample.json` | about 118 KB | `curl -L` from huggingface.co |
| `f3set/README_main.md` | 4,892 | raw.githubusercontent |
| `derived_scratch/` | about 400 KB | outputs of `corpus/scripts/*.py` (per-clip JSONL for the 2019 final, ranking TSVs, log) |

Not downloaded on purpose:
* TennisVL `output_clips.zip`: 62 GB of YouTube-derived video on Google Drive.
* LiveCC full JSONL: 4.4 GB.
* TennisDB `data.zip`: 8.4 GB.
* YouTube-Commons: 440 parquet files.
* Any audio or video.

## 3. Candidates and verdicts

| # | Source | Spoken? | Timing | Verdict |
|---|---|---|---|---|
| A | TennisVL `tennis_data_test_stats_.json`: ASR transcripts | yes (TV, ASR) | clip-level + per-shot | **USE** |
| B | TennisVL `tennis_vl_test.json` and train JSON: parser metadata, no transcripts | no | per-shot | **USE** (timing/metadata only) |
| C | TennisVL `gpt` commentary (LLM-synthesised) | no | – | **DON'T USE** as commentary (optional labelled LLM contrast: orchestrator decides) |
| D | TennisVL video clips (`output_clips.zip`) | media | – | **DON'T USE** |
| E | Match Charting Project (Sackmann) | no | point/shot order, no clock | **USE** (structure) |
| F | Grand Slam point-by-point (Sackmann, HF mirror) | no | `ElapsedTime` per point (Wimbledon/USO only) | **USE** (timing) |
| G | Cornell tennis live-text commentary | written | none | **USE** (contrast genre only) |
| H | TenniSet (Faulkner & Dick 2017) | no (annotator captions) | frame spans | **DON'T USE** |
| I | LiveCC Live-WhisperX-526K / Live-CC-5M | yes (YouTube ASR, word timing) | word-level | **DON'T USE** for now |
| J | Internet Archive radio collection (BBC Radio 5 Live, with ASR) | yes (radio) | ASR .srt | **DON'T USE** (access-restricted). See FOR_HUMAN.md |
| K | Internet Archive community-media high-school tennis videos (CC BY-NC-ND / BY-NC-SA) | maybe | none | **DON'T USE** (amateur matches; commentary presence not verified) |
| L | BNC / Audio BNC sports commentaries | yes | Audio BNC alignment | **DON'T USE** (no tennis found; click-through licence) |
| M | SCBench CommentarySet (HF, gated) | ? | ? | **HUMAN DECIDES** (access by request) |
| N | YouTube-Commons (PleIAs, CC-BY transcripts) | yes (YouTube captions) | ? | **DON'T USE** |
| O | Minor/other: TennisNLData, TennisDB, OSL-loc-tennis, F3Set, THETIS, TennisVid2Text, Troveo, Cornell/ConvoKit press conferences | – | – | **DON'T USE** |

### A. TennisVL test split with ASR transcripts: USE

* URL: https://github.com/LZYAndy/TennisExpert. File: `data/tennis_data_test_stats_.json` at commit 8b778bc.
  The paper is https://arxiv.org/abs/2603.13397, v2 HTML downloaded.
* Contents (inspected):
  * One JSON list of 20 records, one per match: `{"conversations": [...], "videos": [...]}`.
  * Per match there is one `system` turn, then alternating `human`/`gpt` turns, one pair per rally clip:
    4,836 clips in total.
  * Each `human` turn holds `<video>Metadata: {...}`, a Python-literal dict, not JSON.
  * Each `gpt` turn holds the LLM commentary, then `\n\nMetadata: {...}`. That dict contains
    **`'audio_transcription (background context)'`**: the broadcast-commentary ASR text for that clip.
  * 3,996 of 4,836 clips have a non-empty transcript, 148,402 words in total. All 20 matches are English:
    their share of common English function words is 0.335 to 0.371.
* Speech transcripts or audio: transcripts only, no audio.
  * ASR system: the paper says "broadcast audio is transcribed using WhisperX". The files do not state the model
    size or the alignment window.
  * There are no speaker labels and no word-level timestamps in the released files.
  * Each transcript is attached to a whole clip. The window it covers is undocumented: the clip on screen lasts
    7 s on average, but transcripts include between-point talk.
  * Consecutive clips sometimes repeat text. In the 2019 final, 55 transcripts are identical to the previous one,
    and 2,066 of 11,903 tokens fall in 6-grams shared with the previous clip.
* Timing (inspected):
  * Clip file names `<match_id>_<start>_<end>.mp4` give frame indices. For the 2019 final, all hits fall inside
    the span at 25 fps in 481 of 481 clips, and in none at 29.97 or 30 fps.
  * Per shot there are `hit_timestamp_second` and `bounce_timestamp_second` (seconds in the source video; bounce
    is sometimes empty), produced by the authors' automatic video parser.
  * There is a score state before each point.
  * The source video is not identified: the files contain no YouTube IDs, although the paper says URLs are provided.
* Matches: 20 Grand Slam matches, 2019 to 2025 (table in section 4).
* Broadcasters: not stated anywhere in the files. The only evidence is names heard in the ASR text
  (`tennisvl_broadcaster_hints.py`):
  * 2019 Wimbledon final: "Boris" 19, "Tim" 7, "Henman" 3.
  * 2022 AO final: "Brad" 19.
  * 2023 Wimbledon final: "Tim" 5, "Todd" 4.
  * 2021 US Open women's final: "Kim" 4, "Amazon" 1, "Prime" 1.
  * Treat all broadcaster labels as unverified.
* Transcript quality: raw WhisperX, with visible errors. Examples from the 2019 final:
  "by beating Kane Nishikori", "gains to 11. Fire set."
  From the 2025 US Open final: "Yannick" for Jannik.
* Size: 18.5 MB JSON; 20 matches; 4,836 clips.
* Licence/terms:
  * No LICENSE file in the repo; `pyproject.toml` says Apache-2.0, which covers the LLaMA-Factory code.
  * Paper, Ethics section (https://arxiv.org/html/2603.13397v2): "We mandate that this dataset be utilized strictly for academic research in sports video understanding".
  * The paper text itself is CC BY 4.0.
* Verdict: **USE**. It is a research dataset publicly released for research use. Our use is non-commercial academic
  research; cite Liu et al. 2026 (arXiv:2603.13397).
  * Caveat 1: the stated purpose is "sports video understanding and automated commentary generation". Our
    linguistic analysis is academic but outside that wording, so the scope question goes to FOR_HUMAN.md.
  * Caveat 2: the transcripts are of copyrighted broadcast speech. Commit only derived data and excerpts of at
    most 15 words.
  * Caveat 3: these are ASR transcripts, not human transcripts. Plan an error-rate estimate in Phase 1. With no
    audio there is nothing to re-transcribe, so the estimate must rest on internal checks, e.g. names against
    MCP/PBP.
* Schema (fields seen in the files):
  * `human` Metadata: `match_info{tournament, round, surface, player_1{name, handedness, short}, player_2{...}}`
    (in `tennis_vl_test.json` and train; absent from `human` turns in test_stats, where it moves to `gpt` Metadata).
  * Also in `human` Metadata: `score_state{server, returner, sets{}, games_in_current_set{}, points_in_current_game{}}`,
    `court_coordinate{...}`, `point_outcome`.
  * `rally[]{shot_index, hit_timestamp_second, hitter, type, wing, technique, direction_rough, approach_net, hitter_pos_rough, hitter_pos_xy, opponent_pos_xy, bounce_pos_xy, bounce_timestamp_second, shot_outcome}`.
  * `gpt` Metadata: `match_info, 'score_state (initial)', rally[]{shot_index, hitter, shot_description}, outcome{point_winner, point_loser, reason} | {next_shot, reason}, 'audio_transcription (background context)'`.
* Two sample records (2019 final, clips 0 and 2; free text cut to at most 15 words):
  ```
  {"video": "output_clips/20190714-M-Wimbledon-F-Roger_Federer-Novak_Djokovic_1626_1742.mp4",
   "score_state": {"server": "Roger Federer", "sets": {"FEDERER": "0", "DJOKOVIC": "0"},
     "games_in_current_set": {"FEDERER": "0", "DJOKOVIC": "0"}, "points_in_current_game": {"FEDERER": "30", "DJOKOVIC": "0"}},
   "rally[0]": {"shot_index": 0, "hit_timestamp_second": 66.08, "hitter": "Roger Federer", "type": "first serve",
     "direction_rough": "serve-wide", "bounce_timestamp_second": 66.48, "shot_outcome": "in"}, "n_shots": 3,
   "point_outcome": "Roger Federer unforced-error",
   "audio_transcription (background context)": "30, 15. 40, 15."}
  {"video": "output_clips/20190714-M-Wimbledon-F-Roger_Federer-Novak_Djokovic_2502_2862.mp4",
   "score_state": {... "points_in_current_game": {"FEDERER": "40", "DJOKOVIC": "15"}},
   "rally[0]": {"shot_index": 0, "hit_timestamp_second": 101.12, "type": "first serve", "shot_outcome": "unforced-error", ...},
   "n_shots": 4, "point_outcome": "Roger Federer winner",
   "audio_transcription (background context)": "First game. 350 match wins in the Grand Slams earlier on. First player in history. [...]"}
  ```

### B. TennisVL `tennis_vl_test.json` and training JSON: USE (parser timing/metadata only)

* URLs:
  * `data/tennis_vl_test.json` in the repo.
  * Training file, linked from the repo's `data/README.md`: https://drive.google.com/file/d/1raeJJoyGxDyZxNeAo7uk2ngsvlwMQ9SI.
    The Drive file name is `tennis_data_train_stats_.json`.
* Contents (inspected):
  * Same sharegpt structure as A, but with **no transcription field**. `tennis_vl_test.json` has 0 occurrences of
    "transcri"/"audio" (`tennisvl_keys.py`). The train file has 0 of 182 matches with `audio_transcription`
    (`tennisvl_train_list.py`).
  * Train `human` turns add `Live Stats: {player: {Aces, Double Faults, '1st Serve In %', ..., 'Total Points Won'}}`.
* Size: test 13.4 MB (20 matches, 4,827 parsed `human` turns). Train 123.6 MB: 182 matches and 35,480 clips;
  the paper says 35,687.
* Train coverage by slam: 76 AO, 23 RG, 78 USO, 5 Wimbledon.
* Licence/terms: as A.
* Verdict: **USE** for timing and score metadata if needed. There is no spoken commentary in these files.
* Two sample records (`tennis_vl_test.json`, 2019 final clips 0–1):
  * `rally[0] {"hit_timestamp_second": 66.08, "type": "first serve", "direction_rough": "serve-wide", "shot_outcome": "in"}`
  * `rally[0] {"hit_timestamp_second": 85.52, "type": "first serve", "direction_rough": "serve-T", "shot_outcome": "winner"}`

### C. TennisVL `gpt` commentary: DON'T USE as commentary

* Paper: "an advanced LLM (Gemini 3 Pro) synthesizes match information".
* The inputs are ASR, TennisAbstract shot descriptions and metadata. The paper reports that 2,000 pairs were human-reviewed.
* Sample: "Vintage. He opens the court with the serve and finishes it with a sharp forehand [...]".
* It is not oral composition. If used at all, it must be labelled LLM-generated, as a contrast to test whether
  formula measures separate LLM text from live speech.

### D. TennisVL video clips: DON'T USE

* URL: https://drive.google.com/file/d/1tGdYvJxKKLIMByrNj_5D56cr-n_u1Syc. Drive's warning page reports `output_clips.zip (62G)`.
* Reasons:
  * It is YouTube-derived broadcast media with no licence; the paper itself says "we do not distribute raw video files".
  * It exceeds the download limits.
  * It would not add multi-broadcaster coverage.

### E. Match Charting Project: USE (point and shot structure)

* URL: https://github.com/JeffSackmann/tennis_MatchChartingProject, commit 1813a13.
* Contents (inspected):
  * `charting-{m,w}-matches.csv` columns: `match_id, Player 1, Player 2, Pl 1 hand, Pl 2 hand, Date, Tournament, Round, Time, Court, Surface, Umpire, Best of, Final TB?, Charted by`.
  * `charting-*-points-*.csv` columns: `match_id, Pt, Set1, Set2, Gm1, Gm2, Pts, Gm#, TbSet, Svr, 1st, 2nd, Notes, PtWinner`.
  * `1st`/`2nd` hold the human-charted shot codes.
  * No clock times. Match IDs use the same format as TennisVL.
* Coverage: 18 of the 20 TennisVL test matches are charted. Missing: 2019 AO women's final and 2021 USO women's final.
  The 2019 Wimbledon final has 422 points, charted by "Zindaras".
* Size: 148.6 MB for the six CSVs plus README.
* Licence: CC BY-NC-SA 4.0. README: "In other words: Attribution is required. Non-commercial use only."
  (https://github.com/JeffSackmann/tennis_MatchChartingProject#license)
* Verdict: **USE** for point and shot structure and for checking ASR names and events. ShareAlike affects how
  derived data is licensed; see FOR_HUMAN.md.
* Two sample records (2019 final):
  * `{"Pt": "1", "Pts": "0-0", "Gm#": "1", "Svr": "1", "1st": "4*", "2nd": "", "PtWinner": "1"}`
  * `{"Pt": "2", "Pts": "15-0", "Svr": "1", "1st": "4n", "2nd": "5f3w@", "PtWinner": "1"}`

### F. Grand Slam point-by-point (Sackmann): USE (per-point elapsed time)

* URL: the original repo https://github.com/JeffSackmann/tennis_slam_pointbypoint returned 404 from raw.githubusercontent,
  and `git ls-remote` asked for authentication on 2026-10-07, so it appears to be removed or private.
  The data were taken from the archival mirror https://huggingface.co/datasets/Aneeshers/tennis-sackmann-archive,
  revision 8ac86f7, which keeps the upstream README.
* Contents (inspected):
  * `*-points.csv` has 65 columns, including `match_id, ElapsedTime, SetNo, GameNo, PointNumber, PointWinner, PointServer, Speed_KMH, P1Score, P2Score, ServeNumber, WinnerType, RallyCount, P1DistanceRun, P2DistanceRun, ServeWidth, ServeDepth, ReturnDepth`.
  * `*-matches.csv` holds match metadata.
* Timing:
  * `ElapsedTime` is filled for Wimbledon matches: 2019 final, 422 points, 0:00:00 to 4:56:59; 2023 final, 334 points,
    0:00:00 to 4:42:27.
  * It is **empty** for the AO 2020 and RG 2021 finals; the AO/FO feeds come from a different provider.
  * The mirror has no AO/FO files for 2022 onwards and nothing for 2025.
* Size: about 25 MB downloaded. The full mirror is larger.
* Licence: CC BY-NC-SA 4.0. Mirror LICENSE: "redistributed under the Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License".
  The upstream README says "Attribution is required. Non-commercial use only."
* Verdict: **USE**, with attribution to Jeff Sackmann.
  * Caveat: the provenance runs through a third-party mirror.
  * Consistency check: 422 points here equals 422 points in MCP for the 2019 final.
* Two sample records (2019-wimbledon-1701; P1 = Djokovic, P2 = Federer):
  * `{"ElapsedTime": "0:00:00", "SetNo": "1", "GameNo": "1", "PointNumber": "1", "PointServer": "2", "Speed_KMH": "172", "P2Score": "15", "RallyCount": "1"}`
  * `{"ElapsedTime": "0:00:15", "SetNo": "1", "GameNo": "1", "PointNumber": "2", "PointServer": "2", "Speed_KMH": "141", "P2Score": "30", "ServeNumber": "2", "RallyCount": "1"}`

### G. Cornell tennis live-text commentary: USE (contrast genre only)

* URL: https://www.cs.cornell.edu/~liye/tennis.html. README: https://www.cs.cornell.edu/~liye/tennis_README.txt.
  Data: `tennis_data.zip`.
* Contents (inspected):
  * `text_commentaries.json` is a list of 3,962 dicts with keys `commentary, scoreline, gender` (1,981 F, 1,981 M).
  * The text comes from Sports Mole live text, per the README.
  * There are **no match IDs, dates or timestamps**. Only the scoreline identifies the match: 265 distinct
    surname pairings, e.g. Djokovic v Murray, 77 updates.
  * The zip also holds post-match press-conference transcripts: `transcripts_matchinfo.json` and
    `questions_matchinfo.json`. These are not commentary.
* Size: zip 15.9 MB. Commentary file 1.4 MB, 175,714 words, mean 44.3 words per update.
* Language: English. Written by a sports-news site, not ASR.
* Licence/terms: none stated in the README or on the landing page (both checked). It is a dataset released
  publicly with the authors' paper (Fu, Danescu-Niculescu-Mizil & Lee 2016).
* Verdict: **USE** as a contrast corpus of the written live-text genre, cited. It cannot be aligned to the
  recommended match.
* Two sample records:
  * `{"commentary": "Makarova slumps back into making unforced errors again as she finds the net with her [...]", "scoreline": "Sharapova 6-3* Makarova", "gender": "F"}`
  * `{"commentary": "Just look in her match with Heather Watson last week, Serena is desperate to shake [...]", "scoreline": "Williams 3-6 2-1* Azarenka", "gender": "F"}`

### H. TenniSet: DON'T USE

* URLs: https://github.com/HaydenFaulkner/Tennis (MIT licence: "MIT License / Copyright (c) 2017 Hayden Faulkner").
  Data on Google Drive.
* Contents (inspected):
  * `points.txt`: point ID, video, start and end frame. Example: `P00000001 V006 25740 25984 0001`.
  * `captions.txt`: annotator-written captions in a 250-word abbreviated vocabulary. Example:
    `np a good serve fp is unable to return it`.
  * `V006.json`: event spans with keys `USE, SPLITS, Set, Match, Game, Hit, Point, Serve`.
* Scope: 5 matches. There is no broadcast speech.
* Verdict: **DON'T USE**. It is not broadcast commentary.

### I. LiveCC Live-WhisperX-526K (and Live-CC-5M): DON'T USE (for now)

* URL: https://huggingface.co/datasets/chenjoya/Live-WhisperX-526K. The licence tag is apache-2.0; the card says
  "We only allow the use of this dataset for academic research and educational purposes."
* Contents (inspected preview of 100 records):
  * Keys: `video, video_start, video_end, query, text_stream`.
  * `text_stream` holds WhisperX words with start and end times, e.g. `[0.2, 0.62, "Hi,"]`.
  * Clips are YouTube videos of 10 minutes or less. 0 of 100 preview records mention tennis.
* Size: 4.4 GB JSONL. Full-text search on the HF datasets-server failed ("Job manager crashed").
* Verdict: **DON'T USE** in Phase 0. Tennis content is unverified, the clips are short highlights rather than whole
  matches, and the broadcaster cannot be identified. A later scan (4.4 GB, within the 20 GB cap) could look for
  tennis clips with word-level timing, if the orchestrator wants it.

### J. Internet Archive radio: BBC Radio 5 Live: DON'T USE (human route)

* URL: collection https://archive.org/details/Radio-BBC-Radio-5-Live, with 24,796 items from 2016 onwards.
  Example item metadata: https://archive.org/metadata/BBC_Radio_5_Live_20220710_140000.
* Contents (metadata only; no content files fetched):
  * Each item has `collection: stream_only, radio_asr` and `access-restricted-item: true`. No licence or rights field.
  * Files include `.mp3`, `.asr.srt`, `.asr.js`.
* Coverage:
  * No items exist for 13 to 15 July 2019. The 2019 final day is missing.
  * Items do exist on 11 Sep 2021 (21:00–24:00 BST; 2021 USO women's final, a TennisVL test match) and on
    30 Jan 2022 (2022 AO final). Whether they contain match commentary is unverified.
* Verdict: **DON'T USE**. The items are access-restricted and have no licence. Listed in FOR_HUMAN.md.

### K. Internet Archive community-media high-school tennis videos: DON'T USE

* Examples: `WCT14810` (Waycross Community Media, CC BY-NC-ND 3.0, 1:02:25), `mmuboystennisU3205152024` (MMCTV, CC BY-NC-ND 4.0),
  `whs-boys-tennis-vs-burlington-may-11-2015` (CC BY-NC-SA 4.0). Metadata inspected only.
* Why not:
  * These are amateur school matches; whether they carry commentary is not verified.
  * Each comes from a single local crew.
  * NC-ND restricts what can be published. Weak fit for Grand Slam commentary.
  * The other CC0 "broadcast" uploads on archive.org (e.g. a recorded WTA broadcast) have no credible rights
    statement and were not considered.

### L. BNC / Audio BNC: DON'T USE

* The BNC genre `S sportslive` holds 4 texts and 33,630 words (http://www.natcorp.ox.ac.uk/docs/URG/codes.html).
* The bibliography (http://www.natcorp.ox.ac.uk/docs/URG/bibliog.html) lists these spoken sports broadcasts:
  HMN "The Central Match - Live", HEY "The Central Match - Goals Extra" (with football items) and
  HEW "Racing: the Morning Line". A grep for tennis and Wimbledon found only written texts.
* Licence (http://www.natcorp.ox.ac.uk/docs/licence.html): "Your use of the BNC is conditional on your acceptance of the terms".
  This is a click-through for the human, not for an agent.

### M. SCBench CommentarySet: HUMAN DECIDES

* URL: https://huggingface.co/datasets/SCBench/CommentarySet. The full data is in the gated `SCBench/CommentarySet_full_data`.
* README: "available upon request and only for academic research".
* Sports and contents are not inspected, because access requires a request with contact details. See FOR_HUMAN.md.

### N. YouTube-Commons (PleIAs): DON'T USE

* URL: https://huggingface.co/datasets/PleIAs/YouTube-Commons. Tag cc-by-4.0; 440 parquet files.
* Not inspected: there is no search endpoint, and the files are very large.
* The CC-BY flags are set by uploaders, so a CC-BY tag on a broadcast tennis upload would not be credible.

### O. Other candidates checked: DON'T USE

| Source | What was checked | Why not |
|---|---|---|
| ramizheman/TennisNLData (HF) | one file inspected: `match{...}, scraped{point_by_point{pointlog_rows[{server, sets, games, points, description}]}}` | scraped TennisAbstract point logs (templated MCP descriptions); no licence card; use MCP directly |
| Tang1166/TennisDB (HF) | tree listing: one `data.zip` of 8.4 GB, no card | undocumented, too large |
| OpenSportsLab/OSL-loc-tennis-public (HF) | card: swing localisation, 3,445 clips, AGPL-3.0 | no commentary |
| F3Set-Tennis (https://github.com/F3Set/F3Set) | README only | shot timestamps for its own broadcast copies; no commentary |
| THETIS | published description only (not inspected) | Kinect recordings of acted strokes; no commentary |
| TennisVid2Text (Sukhwani & Jawahar 2015, arXiv:1511.08522) | abstract | no public release found |
| Troveo "Sports Commentary" (https://www.troveo.ai/datasets/sports-commentary) | web page | commercial; terms unstated (FOR_HUMAN.md) |
| Cornell / ConvoKit tennis interviews; "Sounding Like a Winner?" (arXiv:2506.02283) | descriptions | press conferences, not commentary |
| Wimbledon newsreels (BFI Player, News on Screen) | search results | streaming or licensing only; narrated newsreel is a different genre |

## 4. TennisVL matches ranked (test split: the only one with transcripts)

Source: `corpus/scripts/rank_tennisvl_matches.py`, output `corpus/raw/derived_scratch/tennisvl_test_ranking.tsv`.

Column definitions:
* "unique words": transcript words not inside a 6-gram shared with the previous clip's transcript.
* "states/pts": distinct pre-point score states covered by clips, divided by MCP points.
* "PBP": whether the match is listed in a Sackmann slam `*-matches.csv`. ElapsedTime was verified only where marked ✓.

| Rank | Match | Clips (with transcript) | Transcript words (unique) | Shots with hit time | MCP points | States/pts | Slam PBP | Name hints |
|---|---|---|---|---|---|---|---|---|
| 1 | 2022 AO F Nadal–Medvedev | 389 (337) | 13,622 (11,507) | 1,964 | 371 | 0.782 | none | Brad 19 |
| 2 | **2019 Wimbledon F Djokovic–Federer** | 481 (373) | 11,772 (9,837) | 1,939 | 422 | 0.865 | 2019-wimbledon-1701, ElapsedTime ✓ | Boris 19, Tim 7, Henman 3 |
| 3 | 2024 AO F Sinner–Medvedev | 339 (287) | 11,040 (9,267) | 1,652 | 283 | 0.901 | none | – |
| 4 | 2020 AO F Djokovic–Thiem | 344 (295) | 9,239 (8,397) | 1,578 | 304 | 0.842 | listed, ElapsedTime empty | Stan 4 |
| 5 | 2022 RG QF Djokovic–Nadal | 271 (244) | 9,436 (8,043) | 1,451 | 278 | 0.737 | none | – |
| 7 | 2023 Wimbledon F Alcaraz–Djokovic | 368 (271) | 8,402 (7,225) | 1,488 | 334 | 0.850 | 2023-wimbledon-1701, ElapsedTime ✓ | Tim 5, Todd 4 |

Ranked by the project criteria, the order is: 2019 Wimbledon F, then 2023 Wimbledon F, then 2022 AO F.
* All three tie at one broadcaster and TV only.
* The two Wimbledon finals add per-point elapsed time.
* 2022 AO F has the most text but only clip and shot timing.
* Women's finals have the least text: 1,601 to 3,825 unique words.

## 5. Notes for corpus-builder

* Extraction: use `corpus/scripts/tennisvl_transcripts.py <test_stats> 18 <out.jsonl>`. It writes per clip:
  `clip, start_frame, end_frame, first_hit_s, last_hit_s, score_state, point_outcome, transcript, synthetic_commentary`.
  Drop `synthetic_commentary` before any formula analysis.
* De-duplicate repeated transcript text across consecutive clips before counting n-grams. Log the rule.
* Alignment:
  * TennisVL `score_state` is the score **before** the point. Join to MCP (`Pts`, `Gm#`, `Set1/2`) and to slam PBP
    (`SetNo, GameNo, P1Score/P2Score` after the point).
  * TennisVL times are video seconds; PBP `ElapsedTime` is match clock. Estimate an offset from serve times.
* The ASR has no speakers and no word times. Any per-word timing claim is impossible from these files.
