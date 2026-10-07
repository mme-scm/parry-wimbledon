# STATUS

Orchestrator log. Phase table at the bottom is printed at the end of every turn.

## Decisions
- 2026-10-07: Project started. Python venv in .venv; requirements.txt committed.
- 2026-10-07: homer-tools (Phase 1 tool build) started during Phase 0 because it has no dependency on the corpus choice; corpus-builder waits for Phase 0.

## Phase 0: corpus choice (DONE 2026-10-07)
Orchestrator verified every USE source by opening the downloaded files (scratch script verify_phase0.py; results below).
- TennisVL test split (tennis_data_test_stats_.json, commit 8b778bc): 20 matches; the 2019 Wimbledon final has 481 clips, 373 with a non-empty `audio_transcription (background context)` field, 11,772 words; human-turn metadata has score_state, rally[] with hit_timestamp_second / bounce_timestamp_second. Confirmed.
- tennis_vl_test.json: match_info, score_state, rally timing; no transcription field anywhere. Confirmed.
- Match Charting Project: 422 points for the 2019 final with Pts, Svr, 1st/2nd shot codes, PtWinner; match row (Centre Court, umpire Damian Steiner, charted by Zindaras). Confirmed.
- Sackmann slam point-by-point (HF mirror of the removed GitHub repo): 2019-wimbledon-1701 has 424 rows (2 are `0X` placeholder rows), ElapsedTime 0:00:00 to 4:56:59 on every row. Confirmed.
- Cornell live text: 3,962 records with commentary/scoreline/gender, 175,714 words, no timestamps or match ids. Confirmed.

**Choice: 2019 Wimbledon men's final (Djokovic d. Federer 7-6(5) 1-6 7-6(4) 4-6 13-12(3)).**
Reasons, in the order PHASES.md prescribes: (1) no acceptable source has any match with spoken commentary from more than one broadcaster, so criterion 1 cannot be met; (2) among single-broadcaster matches the two Wimbledon finals are the only ones with all three timing layers (per-shot hit times, per-point match clock, charted shot sequences); (3) of those two, the 2019 final has the most transcript text (9,837 words after removing text repeated across clips vs 7,225). The 2023 final is held out. The 2022 AO final has more text but no match clock.

**Prominent limitation (to be restated in the paper):** the spoken corpus is one machine-transcribed (WhisperX) TV commentary track per match, with no audio, no speaker labels, no word-level timestamps, and transcripts attached to rally clips of ~7 s whose exact audio window is undocumented. Consequences: (a) no broadcaster or medium contrast within a match; the only medium contrast is spoken TV vs written live text, on different matches; (b) intonation units cannot be measured from pitch; the metre test must be re-specified with the between-point interval (point end to next serve, from ElapsedTime and hit times) as the frame, and with clip-level text; (c) the ASR error rate cannot be measured against audio; only internal checks (names vs MCP/PBP, score calls vs PBP) are possible; (d) commentator identity cannot be separated from medium.

Licence notes: TennisVL terms "strictly for academic research in sports video understanding"; MCP and slam PBP CC BY-NC-SA 4.0; Cornell data released with a paper, no licence stated. Full transcripts are never committed (corpus/transcripts/*.jsonl gitignored); only derived tables and excerpts of at most 15 words.

## Validation figures
(filled per phase)

## Open issues
(see FOR_HUMAN.md for items needing human judgment)

## Phase table
| Phase | Name | Status | Notes |
|---|---|---|---|
| 0 | Find the corpus | DONE | 2019 Wimbledon F; held-out 2023 Wimbledon F; see Phase 0 section |
| 1 | Tools and corpus | IN PROGRESS | homer-tools running; corpus-builder starting |
| 2 | Analyses | NOT STARTED | |
| 3 | Brief | NOT STARTED | |
| 4 | Composition | NOT STARTED | |
| 5 | Translation | NOT STARTED | |
| 6 | Paper | NOT STARTED | |
| 7 | Weaving and stitching | NOT STARTED | |
| F | Finish (README) | NOT STARTED | |
