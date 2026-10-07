# Critic review, phase "analysis", v1

Reviewer: critic agent, 2026-10-07. Scope: `analysis/formulas/` (plan.md, report.md, common.py, f01-f08, f04b, make_report.py,
results/) and `analysis/metre/` (plan.md, report.md, metre_lib.py, s02-s06, results/), read against CLAUDE.md, STATUS.md,
corpus/README.md sections 0, 4, 6, 7, 8 and corpus/SOURCES.md section 1. Checks were run from scratch scripts
(`/tmp/claude-0/.../scratchpad/check1-3.py` and inline python) on the committed results files and on
`corpus/transcripts/*.jsonl`; nothing under `analysis/` was modified. Every number quoted below as "my check" was computed in
this session; every number quoted from a report was compared with the results file it cites.

## Summary verdict

The two analyses are unusually well documented, the plans do predate the scripts in git, the held-out boundaries are clean,
and every table number I compared (about 60) equals the value in `results/`. The problems are in what the numbers are taken
to mean. One confirmatory result (C1/R1, "TV commentary is less formulaic than press-conference speech") is not interpretable
and should not be reported as a rejection in either direction; one baseline is mislabelled (Cornell held-out identification
set is ~65k tokens, not 103,675); the "p-values" for C1/C2 are replicate-overlap statistics at their floor, so the Holm
"rejection" of C2 at 0.0498 is an artefact of R = 200; the metre summary claims a bound that its own limitations section says
the design cannot give; and the Kuiper paragraph places the commentary "not with the auctioneers" on data that contain no
auctioneers. The density measure itself is a measure of lexical repetitiveness rather than of formulaic composition, which
the paper must say in plain words.

Counts: 1 critical, 7 major, 9 minor, 11 checks passed.

## Critical

### A1. C1/R1 ("rejected, OPPOSITE to the predicted direction") is not supported by the design
Where: formulas report, Key results bullet 3; section 4 table and C1 bullet; section 8 "Degree".

What is wrong. Four things make the TV-vs-press contrast uninterpretable as a statement about commentary:
1. ASR noise alone can produce it. The report's own post hoc Table 3.8 shows press held-out density falling to 56.9
   [56.2, 58.5] at e = 0.10 and 52.3 at e = 0.15, against TV 55.0; the corpus's 22/1,000 is a lower bound on *visible*
   errors only (README 7.3), and 10-15% substitution-equivalent error is a plausible rate for WhisperX on crowd-noise
   broadcast audio. The direction of C1 therefore depends on an unknown quantity, and the addendum says so ("robust only to
   modest ASR noise"), but the Key results and the confirmatory table still print the rejection.
2. Transcription convention differs: press answers are edited stenographic transcripts (disfluencies removed, sentences
   complete); TV text is raw ASR cut into ~7 s clip windows with mid-sentence boundaries. Both raise press repetition relative
   to TV independently of how the speakers talk.
3. The held-out designs are not analogous. For TV, I = 18 other matches with unknown, mostly different broadcasters and
   commentators; for press, I = other interviewees in the same genre, same transcription house, same journalists' questions.
   Cross-broadcaster held-out density is penalised by commentator-specific phrasing in a way the press design is not.
4. The bullet's claim that the M asymmetry "favours TV, so it cannot explain a TV deficit" is unsupported: concentration of M
   on one match only helps if the concentrated items are in I, and 275 of the 1194 in-sample 2019 formulas occur in no pool
   match (Table 2.3; Federer plays in no pool match, `federer <_> to` has 0 pool matches).

The noise model (f04b) is also not a bound: independent uniform substitutions drawn from the unigram distribution are neither
clustered (real errors sit in names, score calls, fast overlapping speech) nor do they include deletions, insertions or
word-boundary merges ("Inter rally", "net caught"); frequent-word replacements can even create matches ("the X").

Check that would settle it. (a) A measured WER on a sample with audio (FOR_HUMAN route: BoB/BBC audio); or (b) a
within-convention comparison, e.g. ASR of press-conference audio with the same WhisperX pipeline, or a non-commentary speech
corpus transcribed by ASR; or (c) at minimum: report the e* at which the press and TV ranges meet (between 0.10 and 0.15
held-out; 0.15 split-half), state C1/R1 as "indeterminate pending WER", and remove "OPPOSITE to the predicted direction" from
the Key results. The exploratory per-stream table (all 20 TV streams 48-62% vs press 66%) may be cited as descriptive.

## Major

### B1. The C1/C2 "p-values" are replicate-overlap statistics at their floor; the C2 Holm rejection is an artefact of R = 200
Where: f07_confirmatory.py `p_two`, `pair_diff`; report section 4.
My check: all 200 TV-Cornell replicate pairs are negative, so p = 2/201 = 0.00995 = the floor; Holm rank 2 of 6 gives
5 x 0.00995 = 0.04975 < 0.05. With R = 199 it would be 0.05 and "not rejected". For C1 the floor is 2/10,001 = 0.0002
(also hit). These are not null-hypothesis tests: the "difference distribution" pairs bootstrap draws of one quantity
(TV: M resampled, I fixed, one match) with subsample replicates of another (press: I and M both resampled, many
interviewees), and P(diff <= 0) over such pairs has no null calibration. The effect sizes (-19 pp, -11 pp) are large and
the ordering is consistent across designs, but the inferential statements are decorative.
Settle: report effect sizes with replicate ranges and drop p/Holm for C1/C2, or define a sampling unit (utterance, match)
and run a label-permutation test; if Holm is kept, state that the C2 p is at its floor and the rejection is resolution-limited.

### B2. The Cornell held-out identification set is ~65k tokens, not the 103,675 the report states; unlogged deviation
Where: report Table 3.2 header "held-out (a) %, I = 103,675 tokens, disjoint groups"; Table 4.2 E-C1-text / E-R1-text;
plan D5(ii) "I = a 100,000-token subsample".
My check: `results/medium_replicates.csv`, D5ii rows for text_cornell: tokens_identification min 56,574, median 65,444,
max 76,850 (press: 103,675-103,860, correct). Cause: `_job_heldout` excludes every player-pair touched by the 9.8k-token
measurement sample (median 137 of 496 groups), which removes ~115k of Cornell's 178,770 tokens; my simulation of the rule
gives a median eligible set of 63,601 tokens. `deviations.json` does not record this. Direction is conservative (a larger I
raises Cornell further), so no conclusion flips, but the "matched size" claim is false as printed.
Settle: fix the header to the actual I size per corpus; re-run D5(ii) for Cornell with M drawn from a small number of
groups (e.g. whole matches, <= 20 pairs) so that I reaches 100k; log the deviation.

### B3. "Formulaic density" as implemented measures lexical repetitiveness, not oral-formulaic composition
Where: both reports' headline densities; formulas report sections 2-3; metre report section 4.
Evidence: the top 2019 formulas are `the first`, `a little`, `the match`, `going to`, `you know`, `the forehand`, `the line`,
`to get`, `an hour`, `the court` (Table 2.4); 745 of 1194 types are bigrams and bigrams give 42 of the 44 density points
(Table 2.1). The STOP filter removes only stop-*only* n-grams, so "the + content noun" dominates. In the metre analysis
there is no stop filter at all: the base "formula share" of 0.644 is carried by `in the`, `of the`, `on the`, `for the`
(report section 4), and the strict variant is 0.149. A text's score on this measure rises with vocabulary concentration and
genre templating (hence written live text 85% at pool size), which is why press answers ("I think", "you know") and
Sports Mole updates ("into the net", "with a forehand winner") score high. Parry's formula is a unit fitted to a metrical
slot and expressing an essential idea; Duggan's hemistich count presupposes verse lines. Neither is approximated by "any
repeated non-stop-only bigram". The shuffled-word baseline destroys syntax, so "2.7 times as repetitive as its own words
shuffled" is true of any English text and is decorative.
Settle: make n >= 3 (S6) or m >= 3 (S3) densities and the metre R2 definition co-primary in the Key results; add a baseline
that preserves syntax (e.g. text generated from a bigram model fitted on the pool, at matched size); state in the paper
that the measure is repetition rate, and that the medium ordering is an ordering of repetition rate.

### B4. The Kuiper paragraph places the commentary "not with the auctioneers" without any auctioneer data
Where: formulas report section 8, "Degree" and "Performance constraint" bullets.
No auctioneer or race-call text was measured with this procedure; Kuiper and Haggo's claim is qualitative and verified only
from an abstract. "On a 'degree' scale this TV commentary sits at the low end, not with the auctioneers" is an analogy the
data do not support. The second bullet infers that "tennis television may not impose the continuous load described for
auctioneers" from four null results (C3a, C3b, C4, C5) whose tests have essentially no power (B6) and whose context
variable is a clip-level tercile (C3/C4 below).
Settle: delete the auctioneer placement, or measure an auctioneer/race-call corpus with the same procedure; replace the
"performance constraint" inference with "not detected; the tests had little power".

### B5. Metre summary claims a bound its own limitations section disclaims
Where: metre report section 1, last bullet: "The 2019 CIs are narrow enough to exclude a short-interval excess in formula
share larger than 1.3 pp and a positive syllable-time correlation larger than rho = 0.009"; Limitation 2: the undocumented
window "biases all T-tests toward 0".
Both cannot stand: if the text-to-time assignment is attenuated (text windows of unknown extent, exact repeats a median
17 s after the source clip, tokens per second of clip+gap reaching 5.9 at the 99th percentile in my check, i.e. windows
overlapping beyond the next clip), the CI bounds the attenuated effect, not the true one. Plan section 7 also forbids
reading non-significance as evidence of absence "unless the CI is narrow (stated explicitly)"; the explicit statement here
ignores the attenuation.
Settle: remove the bound, or quantify attenuation by simulation (assign text to units under plausible window rules and
report the implied shrinkage of T2/T3 effects).

### B6. Thrift/extension tests (C4, C5, R4, R5) cannot detect anything and mix speakers
Where: formulas report sections 5-6; f05_refexpr.py, f06_thrift.py.
My check: 2019 has 36 cells, 318 tokens, surname 68-77% of each player's references; the null interval for D is 86-93 around
D = 91 (a +-4% band); C5's null range is +-0.11 with observed 0.087. The inventory includes the umpire's register: all 11
`mr <surname>` tokens are subject-slot ("Mr Federer is challenging"), and `game <surname>` calls are the vocative cell, so
"distinct expression types per cell" partly counts a second speaker's fixed formula, not the commentators' choice. The
context label (dead-time tercile) is assigned to the whole clip whose text spans 20-40 s, so "choice under time pressure"
is not what the cell encodes. The report says the surname "leaves little room" but then uses the null results (B4).
Settle: exclude tokens inside S5 official-call patterns from the inventory; report the minimum detectable effect for C4/C5;
do not cite them as evidence about time pressure.

### B7. The medium ordering is presented as a medium contrast but is a corpus contrast
Where: formulas report Key results bullet 2 and section 8 ("written live text 35.3% > press answers 24.7% > TV commentary
16.2%"); C2.
Confounds are listed in Limitation 6 but not carried into the headline: different matches (Cornell has no match ids), one
outlet (Sports Mole) with a house style, a different period (2007-2015 vs 2019-2025), editorial prose vs raw ASR, and
segmentation (coherent updates vs ~7 s clip windows that cut sentences; q10 of TV clip length is 2 tokens). The matched-size
design equalises tokens, not any of these.
Settle: label C2 as a corpus contrast; the Guardian minute-by-minute of the same match (FOR_HUMAN item 5) would remove the
match confound; at least one TV-vs-written comparison on the same match is needed before "medium" is claimed.

## Minor

### C1. "Duggan" is cited without a fetched record or an [unverified] tag
Where: formulas plan section 2, report section 1 ("Duggan's criterion 'repeated elsewhere in the text'"). CLAUDE.md requires
scholarship to be verified by fetching a source or marked [unverified]. Settle: fetch a catalogue record for Duggan 1973
(The Song of Roland: Formulaic Style and Poetic Craft) and quote the criterion, or mark [unverified].

### C2. Umpire speech counted as commentary formulas; the (b) criterion admits non-alternating frames
My check: `thank you` (rank 6; 15 utterances, 26 occurrences) is the umpire's "thank you, players" / "thank you, please" in
13 of 15 clips; S5 masks only `thank you please` / `please thank you`. `mr <NAME>` (system rank 13) is likewise the umpire's.
`<NAME> djokovic` (system rank 6, 21 occurrences) is the fixed full name `novak djokovic` in 16 of 21 and qualifies as a
"system" through three `federer djokovic` tokens, so the frame does not alternate in Parry's sense. Settle: extend S5 to
bare `thank you` in umpire position; require the top filler to be < 2/3 of occurrences for a frame to count as a system, or
report that statistic.

### C3. C3a uses the wrong interval; C3 permutations ignore serial correlation
`dead_time_before_s` is the dead time *before* the clip's point, when the clip's text has not started (README 4: the text
runs from the rally into the following dead time); C3b (`time_after_s`) is the apt predictor. The label permutation among
T1/T3 utterances treats adjacent clips as exchangeable, whereas the metre analysis uses circular shifts for that reason.
Both null anyway. Settle: present C3b as primary; use a block or circular-shift null.

### C4. Metre T1 is partly a between-category and presence-of-text effect
My check on `units_2019wimF.csv`: rho(words, A) = 0.248 overall, 0.166 within within-game units (n = 290), 0.136 for
A <= 45 s; changeover units have median 109 words vs 14 within games; zero-token clips have a median gap to the next clip
of 12 s vs 21 s for clips with text. The report's "time-locked at the level of points" should be qualified as "mostly
across game boundaries and the presence of a window". T1 is not used as evidence, so the consequence is only wording.

### C5. Metre base formula definition should not carry the headline share
See B3: the base share (0.644) is a common-bigram share; R2 (0.149) is the only variant with lexical content. Settle:
report R2 beside the base in the summary.

### C6. 2023 "replication" is not a replication at comparable range
E5 removes 26 units and leaves 1 changeover unit; A max 117 s vs 305 s; T1 there is a fault-clip window-count effect (X7).
"Not replicated" should read "not testable at comparable range for T4; T2/T3 null over a narrower range".

### C7. Hand-entered numbers in report generators
`make_report.py` line 145: "2007-2015"; `s06_make_report.py` line 373: "at least 22 per 1,000 words" is a literal, not read
from `asr_proxy.json` (the formulas generator reads it). Trivial, but the project rule is "no hand-entered results".

### C8. Noise check cell sizes
Held-out noise rows use R = 10 replicates and the TV row's range is [53.0, 53.5] at e = 0.022 because I and M are fixed
(only the noise draws vary); the press/Cornell rows vary I and M as well. The table compares ranges of different meaning.
Settle: say so in the caption, or use R = 50 throughout.

### C9. Top-10 "official" flag never fires on score calls
By design (S5 excludes score calls), the pre-specified top 10 is six score-call systems flagged `official = False`
although the umpire says most of them. The brief for Phase 3 should carry the caveat that items 1, 2, 4, 5, 9 are umpire
calls as often as commentary.

## Checks that passed (no defect found)

1. Report numbers equal results files: formulas Tables 2.1-2.3, 3.1, 3.2 (values), 3.7, 4, 4.2, 5-7 and all metre sections
   3-9 (about 60 values compared; `report.md` C2 p "0.0100" is 0.009950 rounded).
2. Pre-registration order in git: metre plan 6db5d39 13:12:47 and formulas plan de5788a 13:14:07 precede the first commit of
   any test script or result (951adb5 13:23:15). The only later edit to a plan is the labelled post hoc addendum (fcab897
   13:45:56). X7 and f04b are labelled post hoc in the reports.
3. Held-out boundaries: pool -> 2019, pool -> 2023, 2019 -> 2023 use disjoint I and M; the metre formula list is pool-only.
   The NAME lexicon for (b) is built from all 20 match ids (includes the finals' players) but is used only to type slots.
4. De-duplication leak: 7 duplicate texts remain (40 tokens, all short score calls, > 3 clips apart); 0 adjacent clip pairs
   share a 2-5 word suffix/prefix; 34 adjacent pairs share at least one bigram (49 types). S4 (43.9 vs 44.2), S7 (19.8 vs
   20.3) and S8 (20.6 vs 20.3) bound the effect below 1 pp, so parity split-half is not inflated by window overlap.
5. Score-call utterances do not inflate held-out density: pool -> 2019 density is 55.03% with and 55.07% without the 55
   utterances of <= 3 tokens.
6. Size matching is by tokens with whole utterances; utterance counts differ (about 277 TV, 217 Cornell, 148 press per 9,791
   tokens), which makes the >= 2-utterance criterion harder for press and Cornell, i.e. conservative for the reported ordering.
7. Holm adjustments recomputed by hand for both families (C2: 5 x 0.00995 = 0.0498; metre T1: 4 x 0.00496 = 0.0198).
8. Metre T1 is unchanged without zero-word units (rho 0.248 both ways) and without exact-repeat units (R5: 0.237); the
   circular shift recomputes terciles and categories on the shifted sequence; the +-9 exclusion and the 2/(K+1) floor are
   pre-registered and stated.
9. The between-point cycle A = serve(p) -> serve(p+1) is the right interval for text that spans the rally and the following
   dead time; fault clips are inside the unit; sample-flow counts match E1-E5; points with no clip are excluded rather than
   zeroed.
10. Number of tests run equals the number reported: 6 + 5 confirmatory with Holm; 10 exploratory contrasts, 16 thrift rows,
    8 length-time rows; metre 4 + 3 confirmatory, 6 robustness checks, 7 exploratory analyses, all labelled.
11. ASR digit confusions in score calls (`14` for forty, `13` for thirty, `50` for fifteen: 29 of 195 fillers) are documented
    and absorbed by `<NUM>` systems, as the report says.

## Required before the paper (shortest path)

1. Reword C1/R1 as indeterminate; move the ASR caveat into the same sentence; drop "OPPOSITE".
2. Replace C1/C2 p/Holm with effect sizes and ranges, or add a calibrated test.
3. Fix the Cornell held-out I size (header and deviations.json) or re-run D5(ii).
4. Delete the auctioneer placement and the "continuous load" inference; delete the metre 1.3 pp bound.
5. Put the strict/n >= 3 definitions beside the base in both summaries and say that density here is a repetition rate.
6. Mark Duggan [unverified] or fetch a record.
