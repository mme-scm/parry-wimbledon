# Oral-formulaic tennis commentary and a Homeric match narrative

A test of Parry–Lord oral-formulaic theory on live tennis commentary, a 64-line Homeric hexameter narrative of the same match composed from attested formulae, a line-for-line translation, and a paper. Everything here was produced by orchestrated agents in a cloud session (2026-10-07 to 2026-10-11); every number comes from a script that reruns, every Homeric claim from `homer/concordance.py`, and every step is logged in `STATUS.md`.

## What was done
1. **Corpus (Phase 0–1).** No legally usable source offers one match from more than one broadcaster, or any radio or audio. The corpus is therefore the WhisperX ASR transcript of the single TV commentary track of the **2019 Wimbledon men's final (Djokovic d. Federer 7-6(5) 1-6 7-6(4) 4-6 13-12(3), 4 h 57)** from the TennisVL research release, aligned to Jeff Sackmann's point-by-point clock and Match Charting Project shot records; the 2023 final as held-out match; the other 18 TennisVL test broadcasts as a reference pool; and Cornell's written live text as a contrast. The Homeric side is a reproducible text base (PerseusDL, Monro–Allen / Murray), a concordance, and an automatic hexameter scanner validated on all 27,794 lines (97.7% unique scansion, 0.02% failures, each explained).
2. **Analyses (Phase 2, 2b).** Formula inventory and coverage, noun-epithet economy and extension, and a pre-registered test of rally timing as a metrical frame; then an exploratory study of the formulaic stock across the 20 broadcasts, calibrated against two blind coders. Each analysis went through two adversarial critic rounds.
3. **Composition (Phase 3–4).** A brief built from verified match facts and concordance-verified Homeric models; four drafts checked line by line by independent scansion, provenance and philology verifiers, a poem critic, and a final verifier round. All 64 lines pass.
4. **Translation (Phase 5)** in English accentual hexameter with interlinear gloss and a facing page.
5. **Paper (Phase 6–7)** for a specialist reader, including the section on ῥαψῳδός, ὑφαίνω and the craft words of composition.

## Corpus sources (details and licences in `corpus/SOURCES.md`)
- TennisVL / TennisExpert (Liu et al. 2026, arXiv:2603.13397), test split: WhisperX transcripts and per-shot hit times; "strictly for academic research". Only derived data and excerpts of at most 15 words are committed; transcripts are rebuilt by `bash corpus/scripts/build_corpus.sh`.
- Jeff Sackmann, Grand Slam point-by-point (via the Hugging Face mirror of the removed repository) and the Match Charting Project, CC BY-NC-SA 4.0.
- Cornell / Sports Mole live-text commentary and press-conference transcripts (Fu, Danescu-Niculescu-Mizil and Lee 2016).
- PerseusDL canonical-greekLit for the Iliad and Odyssey.

## Where each deliverable is
| Deliverable | Path |
|---|---|
| Corpus sources and verdicts | `corpus/SOURCES.md`; build and validation: `corpus/README.md` |
| Homeric tools (text, concordance, scanner, check_line) | `homer/` (`make -C homer`) |
| Formula analysis (pre-registered) | `analysis/formulas/plan.md`, `report.md`, `results/` |
| Timing-as-metre analysis (pre-registered) | `analysis/metre/plan.md`, `report.md` |
| Tradition across broadcasts (exploratory, Phase 2b) | `analysis/parry/plan.md`, `report.md`, `manual.md`, `coding_A/B.jsonl` |
| Standing limitations | `analysis/limitations.md` |
| Composition brief | `composition/brief.md` |
| Final poem and records | `composition/final/poem.txt`, `poem.jsonl`, `README.md` |
| Translation, interlinear, scanned translation, facing page | `composition/final/translation.md`, `interlinear.md`, `translation_scanned.md`, `facing.md` |
| Reviews (verifiers, critics, round merges) | `review/` |
| Paper and figures | `paper/paper.md`, `paper/figures/` (`bash paper/figures/make_all.sh`) |
| Orchestration log, decisions, validation figures | `STATUS.md` |
| Items needing a human | `FOR_HUMAN.md` |

## Headline results
- **Coverage by repeated strings.** Word n-grams (n ≥ 2) identified on the other 18 broadcasts cover 55.0% [53.1, 57.0] of the 2019 final's tokens (24.4% at n ≥ 3); split-half within the match 20.3%; shuffled-word baseline 16.2%. The spoken corpus is less repetitive than the written live text by 19.1 points [16.3, 22.1] at matched size, a corpus contrast not attributable to medium; the TV-versus-press-conference contrast is indeterminate under the unknown ASR error rate.
- **Economy and extension.** The surname is 68–77% of player references, descriptive epithets 4–5%; within the match no thrift (91 forms per cell vs 89.6 expected) and no length-for-time extension (ρ = 0.09), with minimum detectable effects reported. Across the 20 broadcasts, team-level naming thrift is robust (303 forms vs 388 expected); slot-bound thrift is inconclusive; extension is absent.
- **Timing as a frame.** Re-specified (no audio) as the serve-to-serve cycle: text volume tracks available time (ρ = 0.25) but formula share, formula length and the changeover contrast do not, in 2019 or in 2023.
- **A commentary-specific stock exists, but as frequency.** With 100k-token identification sets, TV sources cover a TV target 11.4 points [10.7, 12.2] more than written text at n ≥ 3 (11.3 more than press answers; all 20 broadcasts positive); the TV-only strings are about 10% of the finals' tokens, and 78% of their occurrences appear in the baselines below 1 per 100k tokens (occurrence-weighted rate ratio median 8.4, IQR 4.4–26).
- **Calibration.** Two blind coders agree at κ = 0.77; the automatic measures agree with them at κ 0.11–0.22, so every coverage figure above is a repetition statistic, a weak proxy for a Parryan formula.
- **The poem.** 64 lines, 0 metrical flags; 297 source entries (151 exactly attested, 115 attested with a Homeric kind of modification, 31 coined-name substitutions into attested slots); 19 verbatim Homeric lines; coverage of the poem's tokens by Homeric n-grams 81.9% [77.2, 86.2] at n ≥ 2 (a Homeric line against the rest of Homer: 70.0%); 100% of lines contain an exactly attested formula of two or more words; necessary enjambment 14.1% against Parry's 26.6%.

## FOR_HUMAN.md in brief
- **Routes to a second broadcaster or radio** for the 2019 final (Box of Broadcasts via a UK university ERA licence; BBC licensing; Internet Archive researcher access to the access-restricted BBC Radio 5 Live collection; a Guardian API key for written minute-by-minute text). Any of these would allow a real TV-against-radio comparison and a measured ASR error rate, which this study could not have.
- **Licence questions:** TennisVL's stated purpose ("sports video understanding") versus this linguistic use; ShareAlike on derived tables from CC BY-NC-SA data; the third-party mirror of the removed point-by-point repository; SCBench CommentarySet (access by request).
- **Hand judgements to spot-check:** epithet referents and syntactic slots in `analysis/formulas/hand/`; the press-conference baseline's admissibility; one unverified bibliographic item (Kuiper and Austin 1990).
- **Composition decisions taken provisionally:** the Greek renderings of Djokovic (Ζοκοβείδης, Νοβῆκος, Σέρβος; Ζοκοβεύς restricted to the eponym), the rejection of Ῥογῆρος before ἰσόθεος φώς, the limit on ἐξεναρίζω, and the avoidance of δίς + verb.

## Reproduction
`python -m venv .venv && .venv/bin/pip install -r requirements.txt`; fetch the sources with `bash corpus/scripts/fetch_phase0.sh` (downloads to the gitignored `corpus/raw/`); then `bash corpus/scripts/build_corpus.sh`, `make -C homer`, `bash analysis/formulas/run_all.sh`, `bash analysis/metre/run_all.sh`, `bash analysis/parry/run_all.sh`, `bash paper/figures/make_all.sh`. Verify the poem with `python homer/check_line.py --file composition/final/poem.txt --json` and `python review/provenance_check.py`.
