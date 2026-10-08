# STATUS

Orchestrator log. Phase table at the bottom is printed at the end of every turn.

## Decisions
- 2026-10-07: Project started. Python venv in .venv; requirements.txt committed.
- 2026-10-07: homer-tools (Phase 1 tool build) started during Phase 0 because it has no dependency on the corpus choice; corpus-builder waits for Phase 0.
- 2026-10-07: Phase 2 analysts (formula-analyst, metre-analyst) started as soon as the corpus half of Phase 1 was verified; they do not use homer/. The Homer-tools verification of Phase 1 continues in parallel.
- 2026-10-07: Phase 3 brief drafted (by a research agent from concordance-verified material, then reviewed by the orchestrator) while critic v1 of Phase 2 ran; composer v1 started on the accepted brief while the Phase 2 revision round and critic v2 close. Overlap, not skipping: the brief depends only on the formula top-10 (final) and the Homer tools; the poem depends only on the brief.
- 2026-10-07: press-conference transcripts (same Cornell release as the live text) are used only as a spoken non-commentary baseline in analysis/formulas; SOURCES.md marks them DON'T USE as commentary, which they are not used as.

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

### Phase 1, corpus half (orchestrator checks, 2026-10-07)
- Corpus built by `bash corpus/scripts/build_corpus.sh` (deterministic, ~40 s). Streams: tv_2019wimF 481 clips / 373 with text / 9,702 words after de-duplication; tv_2023wimF 368 / 271 / 7,168; 18 pool streams 103,074 words; text_cornell 175,569 words. Full texts gitignored; manifest with sha256 committed.
- Builder's figures: clip-to-point alignment 473/481 (98.3%) for 2019, 348/368 for 2023; MCP and PBP keys agree on 100% of points; video-to-match-clock offset 26.72 s constant, residual SD 0.28 s (2019); TennisVL shot count = MCP in 82.1% of 358 points (96.9% within one); hand sample of 20 score calls: 14/20 exact, 2 within two points, 4 unconfirmed; ASR proxy 22 errors per 1,000 words (Wilson 95% CI 12-39), a lower bound.
- Check (3), orchestrator: read three stretches of consecutive clips, 579 words in total (seed 7). Counted 13-15 ASR errors (garbles such as "Bedclothes service", "50 no", "Van Dijk", "net caught"; impossible score calls; one "Seven women in finals"), i.e. about 22-26 per 1,000 words, consistent with the builder's lower bound. Verdict: claimed rate acceptable; true WER is higher because plausible-word substitutions are invisible without audio. Errors cluster in short score-call clips, names and idioms.
- Check (4), orchestrator: 20 random points (seed 7) re-derived from the raw TennisVL JSON and the raw MCP codes. Hit times in corpus/timing/shots_2019wimF.csv equal the raw `hit_timestamp_second` values in 20/20 (my first pass showed 4 mismatches that were my own filter on fault/ace clips). My own parse of MCP shot codes equals the builder's mcp_n_shots in 20/20. TennisVL n_shots equals MCP in 15/20, matching the builder's 82%. Conclusion: the derived tables faithfully reproduce their sources; TennisVL's automatic shot parse itself disagrees with human charting in about one point in five, so rally-duration figures carry that noise, while per-point match clock (PBP ElapsedTime, 1 s resolution) is independent of it.
- Not applicable: no audio, so no faster-whisper run, no spectrograms, no librosa onsets.
- Correction 2026-10-08 (found by the Phase 2b analyst): six pool streams' clip frames had been converted at 25 fps although their video is 29.97 fps (five streams) or 29.0 fps (one, non-standard, cause unverified). corpus-builder detected the rate per stream from the hit timestamps (100% of clips consistent), recomputed clip_start_s, clip_end_s, t_since_prev_last_hit_s and t_to_next_first_hit_s for those six streams as a logged step (corpus/timing_corrections.log, corpus/fps_by_stream.json), and rebuilt. tv_2019wimF and tv_2023wimF are byte-identical before and after, so analysis/metre and analysis/formulas are unaffected; the Phase 2b analysis used hit times, not the faulty field.

### Phase 1, Homer tools half (orchestrator checks, 2026-10-07)
- Text: PerseusDL canonical-greekLit at commit 01b725d8 (Iliad: Monro-Allen OCT; Odyssey: Murray 1919 Loeb), 15,687 + 12,107 = 27,794 lines (the edition lacks 9 line numbers; no sub-numbered lines).
- Builder's validation on every line (two-pass scan): 97.65% unique scansion, 2.33% several valid scansions (0.12% true ties), 0.02% fail (5 lines, each explained in homer/validation.md: three ἀνδροτῆτα lines, Od. 8.267, Od. 13.364). Basic rules without licences: 5.17% fail; 50 of those classified by licence needed.
- Check (1), orchestrator: 25 random lines (seed 20261007) scanned by my own reasoning before looking at the tool. 25/25 foot patterns agree, including the licences I had to invoke: digamma (οἱ in Il. 5.7, ἔπεα in Od. 22.343, ἔολπα in Od. 2.275, ἰδέσθαι in Od. 23.107), epic correption (τῷ ἔσσεται, καὶ ὤμων, μοι ἀλλο-), muta cum liquida making position (πὸ κρατός, τὰ φρονέων, τε τράκις), κρᾱτός with long alpha, Ᾱρηϊ, and arsis lengthening of -ας before ἑτάροις at the penthemimeral caesura in Od. 9.288 (the tool scans it identically). Il. 5.829 is listed by the tool as having alternatives; its first choice equals mine. No disagreements, so no adjudication needed.
- Check (2), orchestrator: five well-known formulae (πόδας ὠκὺς Ἀχιλλεύς 30 lines, πολύμητις Ὀδυσσεύς 80, γλαυκῶπις Ἀθήνη 78, ἔπεα πτερόεντα προσηύδα 107, ῥοδοδάκτυλος Ἠώς 27) and five random n-grams from homer/ngrams.tsv: concordance line counts equal my independent accent-insensitive grep of homer/lines.tsv in all ten cases (the TSV output has one header row), and the first cited line of each random n-gram contains it.
- check_line.py runs on Il. 1.1 and reports its scansion; Hermann's bridge (word end at 7.5, 0.92% of lines) is flagged under the 1% rule.
- Fix sent back after check: check_line warned that θεά had no attested quantity, because final long dichrona in princeps were excluded wholesale. homer-tools narrowed the exclusion to contexts where a lengthening licence could apply (commit 363835c): dichrona rows 20,191 to 20,232; θεά now L with 17 attestations; validation 97.73% unique / 2.26% multiple / 0.02% fail. Side effect: 9 forms became conflicts (e.g. Ἄρηα, Θέτι), which the learner then leaves to the metre; acceptable.

## Phase 2 summary (DONE 2026-10-07)
Repeated-n-gram coverage of the 2019 final (9,791 tokens; n ≥ 2, exact strings) is 44.2% [42.5, 46.3] in-sample, 20.3% [18.9, 21.8] split-half, 55.0% [53.1, 57.0] when the formulas are identified on the 18 other matches, and 26.3% when 2019 formulas are measured on the held-out 2023 final; the stricter n ≥ 3 definition gives 19.4 / 4.5 / 24.4 / 6.9%, and the shuffled-word baseline for n ≥ 2 is 16.2%. Exact formulas and one-slot systems are reported separately (1,194 types and 231 systems in 2019; systems add about 4–9 points of coverage). The spoken TV corpus is less repetitive than the written live-text corpus by 19.1 points [16.3, 22.1] at matched size (R = 1000 replicates), a corpus contrast not attributable to medium; the TV-versus-press-conference contrast is indeterminate because 12% injected substitution noise erases it and the ASR error rate (lower bound 22 per 1,000 words) is unknown. The bare surname is 68–77% of player references and descriptive epithets 4–5%; the thrift test finds 91 distinct name forms per player × slot × dead-time cell against 89.6 expected under permutation (p = 0.84), and name length does not track available time (ρ = 0.087, p = 0.12), with minimum detectable effects θ 0.30–0.42 and ρ 0.17–0.22. The metre hypothesis had to be re-specified, since no audio, word times or speakers exist, as a serve-to-serve-cycle frame on clip-level text; it is not supported: words per point track available time (ρ = 0.248 [0.136, 0.359], but consistent with H0 and partly between-category), while formula share in short versus long intervals differs by −2.9 points [−6.0, +1.3], formula syllable count has ρ = −0.040 [−0.088, 0.009], and the changeover contrast is +1.0 points [−2.5, +4.4]; the 2023 replication (changeovers cut from the video) shows nothing significant either. Critic rounds: v1 found 1 critical and 7 major issues, all fixed or recorded in analysis/limitations.md; v2 found 0 critical and 1 major (an overstatement in limitations.md, now corrected) plus minor wording items, fixed. Three main limitations: (1) coverage by repeated strings is a repetition statistic, not Parry's metrically conditioned formula, so the Duggan comparison is an analogy; (2) one machine-transcribed broadcaster, no audio, clip-level text: commentator, medium and match are confounded, ASR noise attenuates every effect by an unknown factor, and the null results exclude only effects above 5–11 points; (3) the written contrast is a different corpus (matches, outlet, segmentation), so no medium effect can be claimed.

- 2026-10-07: the human approved Phase 2b (exploratory): cross-broadcast sharing, Parry calibration with two blind coders, thrift per slot across the pool. Its plan is committed before any test runs.

## Open issues
(see FOR_HUMAN.md for items needing human judgment)

## Phase table
| Phase | Name | Status | Notes |
|---|---|---|---|
| 0 | Find the corpus | DONE | 2019 Wimbledon F; held-out 2023 Wimbledon F; see Phase 0 section |
| 1 | Tools and corpus | DONE | corpus and Homer tools both verified by orchestrator |
| 2 | Analyses | IN PROGRESS | formula-analyst, metre-analyst running |
| 3 | Brief | NOT STARTED | |
| 4 | Composition | IN PROGRESS | composer v1 running |
| 5 | Translation | NOT STARTED | |
| 6 | Paper | NOT STARTED | |
| 7 | Weaving and stitching | NOT STARTED | |
| F | Finish (README) | NOT STARTED | |
