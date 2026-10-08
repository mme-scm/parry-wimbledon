# Critic review, phase "parry" (Phase 2b), v1

Reviewer: critic agent, 2026-10-08. Scope: `analysis/parry/` (plan.md, report.md, lib2b.py, p00-p07, p05b, calibrate.py,
make_report.py, run_all.sh, manual.md, coding_A.jsonl, coding_B.jsonl, results/, figures/), `analysis/formulas/common.py`
and `refexpr.py` (inherited), PHASES.md (2b), STATUS.md, `analysis/limitations.md`, my earlier reviews v1/v2, and the
corpus README section 3.3 (frame-rate correction). Every check below was run from scratch scripts in
`/tmp/claude-0/.../scratchpad/check_*.py` on the committed results files and on `corpus/transcripts/`; nothing under
`analysis/` was modified. "My check" = computed in this session; report numbers were compared with the results file they
come from (162 strings, 0 mismatches).

## Summary verdict

The machinery is sound and well documented: the plan (34478c3, 00:16:36) precedes the first test script (7cd04e6, 00:26:41);
the seven 2b-primary tests are the plan's; Holm reproduces by hand; the H4 permutation nulls preserve cell sizes; the H5
null permutes time at the utterance level; the hit-clock fix for available time is right and the 2019/2023 streams (25 fps,
byte-identical after the corpus correction) leave Phase 2 untouched; every number I compared equals its results file. The
problems are in what the numbers are taken to mean, and one of them is a headline conclusion that a better-powered version
of the same design contradicts.

1. **Critical.** "The TV-specific part of the shared stock is almost entirely two-word units" and "the cross-broadcast core is
   mostly shared tennis English, not a commentary-only stock" are artefacts of the 1,500-token matched size, at which an
   n >= 3 inventory has about 25 types. With a 100,000-token identification set (the Phase 2 design), TV sources cover a TV
   target's n >= 3 strings 11.4 pp [10.6, 12.1] more than a Cornell source and 11.5 pp [10.4, 12.4] more than a press source
   of the same size (20 of 20 targets); about 10% of the two finals' tokens lie in n >= 3 strings that the TV pool shares
   with them and neither baseline does. Roughly half of the commonest such strings are the umpire's register and score/time
   frames, which is itself the finding to report. The sentence is also hard-coded in `make_report.py` (line 147), so no rerun
   could have changed it.
2. **Major.** H2's size depends on the shuffled-null subtraction: on observed coverage TV sources exceed Cornell by 0.53 pp
   [0.12, 1.00] (15 of 20 targets), not 1.84; the gap comes from Cornell's larger chance inventory (its unigram distribution is
   more concentrated: 5.6% `<name>`, 2.8% `<num>` against 2.6% / 2.1% in TV). The sign is robust (S = 3,000: 2.09 [1.64,
   2.61]; I = 100k: 15.2 pp); the magnitude and "about a quarter of the TV-TV excess" are null-specific.
3. **Major.** H1 is a test that any two English texts pass: 72-76% of the TV-TV excess is matched by press and written
   sources, and press speakers share more among themselves (10.9 pp) than TV teams do (7.6 pp). It should be reported as a
   check, not as the first Key result.
4. **Major.** The calibration headline (precision 0.35, recall 0.68) hides the base rates: every automatic measure has
   kappa = 0.12-0.22 against the coders (coders with each other: 0.77); precision is 0.05-0.10 above chance (0.26-0.28) with a
   ceiling of 0.48-0.52 set by the share of tokens the measure marks; "precision is higher on 2019" is a base-rate artefact
   (chance 0.34 vs 0.21).
5. **Major.** The slot variable used by H4a, H4b and the per-slot tables was never validated: the classifier was calibrated in
   `classify(span)` mode on coder spans (kappa 0.49, JUDGE confused with SHOT/OTHER), but E3 uses `classify_context` (a
   4-token window excluding the reference), a different mode.
6. **Major.** H4b's Holm rejection is not robust: the identical test with another seed gives p = 0.0268 (`h4_declustered.csv`,
   Holm 0.054, not rejected); without hypocoristic and epithet forms (two Nadal streams; hand-resolved finals) p = 0.063 /
   0.12; 5 of the 40 per-team tests reach 0.05 (2 expected); and with no speaker labels a play-by-play/analyst split that
   co-varies with the slot cannot be told from slot-conditioned form choice. The Key results list it among six rejections.

Counts: 1 critical, 6 major, 12 minor, 14 checks passed. No number in the report disagrees with `results/`.

## Critical

### A1. The n >= 3 / "no commentary-only stock" conclusion is an artefact of S = 1,500
Where: Key results bullets 2 ("almost entirely two-word units") and 3 ("mostly shared tennis English, not a commentary-only
stock"); Table 2.3 n >= 3 rows; section 6 item 5 says only that "absolute sharing levels depend on S".

What is wrong. At S = 1,500 an n >= 3 inventory has 17-49 types (Table 2.1) and covers 1.0% of a target; the H2 n >= 3
differences (-0.03, -0.02 pp) are therefore differences between near-empty inventories. The report's own S = 3,000 rows
already move (press 0.47 [0.32, 0.67]). My check (`check_largeI.py`: I = 100,000 tokens, whole utterances, 3 subsamples;
M = each of the 20 TV streams; 2b normalisation; the design of plan section 8 / Phase 2):

| source (100k tokens) | n >= 2 observed | n >= 2 shuffled | n >= 3 observed | n >= 3 shuffled |
|---|---|---|---|---|
| other 19 TV streams | 59.7% | 30.5% | 30.0% | 1.3% |
| Cornell | 44.5% | 25.6% | 18.6% | 2.4% |
| press, pooled | 46.6% | 22.6% | 18.5% | 0.3% |

TV minus Cornell at n >= 3: 11.37 pp, stream bootstrap [10.62, 12.13], 20 of 20 targets; TV minus press 11.45 [10.39, 12.40];
raw tokens 10.66 and 8.12. For the 2019 final, 20.8% of tokens are in n >= 3 strings of the TV pool that a Cornell-or-press
inventory of the same size also has, and 9.9% in strings only the TV pool has (2023: 22.0% / 10.4%). The commonest TV-only
strings are not ASR artefacts: `<name> leads by`, `mr <name> is`, `<name> is challenging`, `ball was called (out)`, `has two
challenges remaining`, `thank you please`, `new balls please`, `players are ready` (umpire register); `<num> miles an hour`,
`hours and <num> minutes`, `games to one`, `by two games to` (score and time frames); `have a look at`, `of all time`, `head to
head`, `break point saved`, `the slice backhand`, `into the forehand` (commentary). So the TV-specific stock is real at the
three-word level and a large part of it is the official register that the broadcast audio carries and the baselines cannot.

Why it matters. The Key results draw the opposite conclusion from the one the pooled design gives, and the sentence is a
literal in the generator (`make_report.py` line 147: "the TV-specific part of the shared stock is almost entirely two-word
units"), so the report would print it whatever the results were (see M6).

Settle: add the pooled design above to p03 (it is one more job type in `_target_job`: I = 100k-token subsample of Cornell /
press beside the existing matched-I TV pool; about 6 minutes), report n >= 2 and n >= 3 for the three sources, and rerun with
`common.official_mask_v2` on the target to separate the umpire register from the commentators' stock. Rewrite both bullets
from those numbers; the S = 1,500 n >= 3 rows should be labelled "no power at this size".

## Major

### M1. H2's magnitude is produced by the null subtraction; the observed difference is a quarter of it
Where: Key results bullet 2; Table 2.3; section 5 rows H2a/H2b; Table 2.4's note already concedes the mechanism for Jaccard.
My check (`check_sharing.py`, vertex bootstrap of the H2 statistic on `sharing_pairs.csv`, S = 1,500, normalised, n >= 2):

| statistic | TV minus Cornell | targets > 0 | TV minus press | targets > 0 |
|---|---|---|---|---|
| observed coverage | 0.53 [0.12, 1.00] | 15/20 | 3.10 [2.47, 3.82] | 20/20 |
| shuffled coverage | -1.31 [-1.36, -1.27] | 0/20 | 0.96 [0.73, 1.23] | 20/20 |
| excess (reported) | 1.84 [1.43, 2.30] | 20/20 | 2.14 [1.66, 2.71] | 20/20 |

The Cornell inventory of shuffled text has 53 types against 17-32 for TV (Table 2.1) because Cornell's unigram distribution
is concentrated (`<name>` 5.6%, `<num>` 2.8% of tokens vs 2.6% / 2.1% in TV; my check); its chance bigrams (`<name> <name>`,
`<num> <num>`, `the <name>`) cover shuffled TV, so the subtraction removes 2.45 pp from Cornell and 1.14 from TV. Those same
bigrams are genuine shared items in the observed texts, so the excess attributes to "lexicon" for Cornell what it counts as
"stock" for TV. The sign of H2a survives every variant (content 0.79 [0.36, 1.29]; raw 1.14 [0.67, 1.69]; S = 3,000 observed
2.09 [1.64, 2.61]; I = 100k 15.2 pp), so the rejection stands, but "1.84 pp, about a quarter of the TV-TV excess" is a
property of the null, and H2b's observed difference (3.10) is larger than its excess.
Settle: report observed and excess side by side in Table 2.3 and the Key results; use a null that equalises chance
inventories (e.g. restrict each source's inventory to the same number of types, or compare at the pooled 100k size where the
shuffled n >= 3 coverage is ~0); say that the Cornell shuffled null is larger because of its token concentration.

### M2. H1 is decorative: the shuffle null cannot fail for English text
Where: Key results bullet 1; section 5 "H1 and H2 are large relative to their intervals".
Press -> TV excess is 5.42 pp and Cornell -> TV 5.72 pp against TV -> TV 7.56 (Table 2.2): 72-76% of what H1 calls "shared
multiword stock beyond lexicon" is shared equally with player interviews and written text, i.e. it is collocational English
plus tennis vocabulary. Table 2.6 shows four press speakers sharing 10.9 pp among themselves, more than the TV teams. H1 has
20 of 20 targets positive because the unigram shuffle destroys every collocation; no two English texts of this size would fail
it. The pairwise machinery is fine (asymmetry |C_ij - C_ji| mean 0.57 pp, max 1.84; replicate spread per pair about 5 pp wide
but R = 500 makes the pair means precise; the vertex CI of +-0.6 pp dominates), the inference is just empty.
Settle: move H1a/H1b out of the Key results into section 2 as a check that the pipeline detects collocation; keep them in the
Holm family (pre-specified) but say what they test.

### M3. The calibration headline omits chance level, ceiling and kappa
Where: Key results "Calibration" bullet; Table 3.2 and its "Reading" paragraph; section 6 item 1.
My check (`check_calib.py`, auto labels recomputed with `calibrate.automatic_labels`, HIGH+MEDIUM spans): coder positive
share A 0.256, B 0.218, union 0.278, intersection 0.196; kappa(A, B) 0.774 (reproduces).

| automatic measure | auto % | kappa vs A | kappa vs B | kappa vs union | precision vs union (chance, ceiling) |
|---|---|---|---|---|---|
| pool n >= 2 | 53.7 | 0.147 | 0.149 | 0.159 | 0.355 (0.278, 0.518) |
| pool n >= 3 | 25.0 | 0.134 | 0.155 | 0.146 | 0.392 (0.278, 1.0) |
| pool systems | 37.9 | 0.203 | 0.212 | 0.217 | 0.406 (0.278, 0.734) |
| in-sample n >= 2 | 40.4 | 0.178 | 0.192 | 0.189 | 0.385 (0.278, 0.689) |
| in-sample n >= 3 | 18.4 | 0.151 | 0.184 | 0.161 | 0.436 (0.278, 1.0) |
| pool (a) or (b) | 62.3 | 0.144 | 0.143 | 0.158 | 0.349 (0.278, 0.447) |

Every measure is at "slight" agreement; the best (systems) is 0.22. The "Reading" sentence "no automatic variant reaches a
precision above about 0.45" describes a ceiling (coder share / auto share = 0.48-0.52 for the n >= 2 measures), not a
property of the measure. "Precision is higher on the 2019 utterances (0.43 vs 0.27)" is explained by the coder base rate:
chance precision is 0.343 on 2019 and 0.211 on the other streams (the "other" half is token-weighted, mean 69 words per
utterance vs 36, and its pool has 17 streams vs 18). Span level: 64% of coder A's 577 HIGH spans are fully inside pool n >= 2
coverage and 89% touch it, which is the one encouraging number and is not in the report.
Settle: add kappa (and/or precision minus chance) per measure to Table 3.2, state the ceiling, replace the 2019-vs-other
sentence with the base-rate explanation, and report the span-level HIGH recall. Then the limitation reads correctly: the
repetition statistic over-marks half the tokens and agrees with Parry-style judgement little better than chance.

### M4. The slot classifier is validated in one mode and used in another
Where: section 1 "Situational slot classifier"; Table 3.4; H4a/H4b (plan section 5 "reference-level slot"); Tables 4.2-4.5b;
Key results "lies mainly in SHOT, JUDGE".
`calibrate.py` scores `sc.classify(sp["s"], sp["e"])` on coder spans (the span's own words decide); `p04_refexpr_pool.py`
assigns `sc.classify_context(k0, k1)` to references (the 4-token window on either side, the reference excluded). The two
modes share lexicons but not inputs; nothing in the results measures the agreement of the context mode with anything. The
confusion matrices show the classifier moving 82 + 110 of coder A's 392 JUDGE spans to SHOT and OTHER and 71 of 275 SCORE
spans to OTHER; label noise of this size attenuates a true slot-form association toward zero, so H4b's small deficit could be
an attenuated larger effect or nothing, and the per-slot attribution (SHOT -15, JUDGE -5) is unreliable. Table 2.11's
idiolect-by-slot and Table 4.7's E1 rows use yet another mode (`classify` on the formula's own span), which is circular for
SCORE/OFFICIAL by construction (the report notes this for the E1 null only).
Settle: have the coders (or a new blind agent) label the slot of a sample of 200 reference windows with the reference masked,
and report kappa for `classify_context`; or re-run H4b with the coder-agreed slots on the 300-utterance sample as a sensitivity.

### M5. H4b is not robust enough to be listed as rejected
Where: Key results "Naming and thrift"; section 5 table and verdict line "rejected: ... H4b".
(i) Monte Carlo: p05 gives p = 0.0221 (Holm 0.0442); p05b runs the identical statistic with seed [SEED, 55] and gets
p = 0.0268 (`h4_declustered.csv` row 2; Holm 0.0536, not rejected); my rerun with 3,000 permutations gives 0.0197. The Holm
verdict flips within Monte Carlo error. (ii) Forms: dropping hypocoristic and epithet forms (`check_h4.py`) gives D = 401 vs
408.8, p = 0.063; surname and first name only, 315 vs 319.5, p = 0.12. Hypocoristics are 135 of 136 in the two Nadal streams
and 24 of 81 epithets are in the two finals where hand resolution exists, so the pooled effect rests on a few team x player
cells (e.g. 2022 AO Nadal: SHOT 15 "rafa" / 9 "nadal", JUDGE 20 / 3). (iii) Per team, 2 of 20 situational and 3 of 20
syntactic tests reach p < 0.05 (2 expected). (iv) Design: with no speaker labels, a play-by-play commentator who says
"Nadal" during rallies and an analyst who says "Rafa" between points produce exactly this deficit; the report's limitation
4 does not name this confound for H4b. H4a, by contrast, is robust (floor p in every variant, including surname/first/full
only: D = 254 vs 282.4) and is the thrift result the data support: naming habits differ by stream.
Settle: report H4b as "not robust (p 0.02-0.03 across seeds; absent without hypocoristic/epithet forms)", raise N_PERM to
100,000 for the primary family so the Holm verdict is stable, add the speaker-role confound to section 6, and keep "rejected"
for H4a only.

### M6. The report generator hard-codes verdict sentences
Where: `make_report.py` lines 144-147 ("about a quarter of the TV-TV excess", "almost entirely two-word units"), line 728
("about 58% agreement"), line 749 ("2007-2015").
A report "generated from results" whose conclusions are literals breaks the project rule that no number or verdict is typed by
hand, and is the proximate cause of A1: the sentence cannot respond to the S = 3,000 rows that already contradict it. "About
58%" happens to match 57.9 / 57.3 and "about a quarter" matches 24% / 28%, so nothing is wrong today.
Settle: compute the fractions from the JSON (h2a/h1a), derive the n >= 3 verdict from the S = 3,000 and pooled rows with an
explicit rule, and read the press years and classifier agreement from the results files.

## Minor

**m1. Exploratory test count.** The report says 99 exploratory p-values; the results files carry 125 (cluster 12, QAP 10 + 2
intercepts, thrift 44, extension 4, mixed model 1, E1 7 x 2, E2 16 x 2, de-clustered 4, two Spearman tests). The generator
counts E1/E2 rows once although each has two p-values and omits the mixed model and the idiolect correlations. Settle: count
p-values, not rows; note that of the 32 E2 p-values 4 are below 0.05 against 1.6 expected and only `speed_unit` (1e-4)
survives a Bonferroni over 32 (`along_the_line` 0.0018 x 32 = 0.058).

**m2. Stale corpus statements.** The corpus was corrected after the final 2b rerun (6209d74 02:20:27 > 476a088 02:15:10);
section 1 ("`t_to_next_first_hit_s` is invalid in 6 of the 20 streams ... values down to about -1,860 s") and limitation 8
("should be fixed in corpus/") no longer describe the corpus. My check on the corrected files: `fps_valid` still flags the same
six streams (it uses `clip_start_frame` and `first_hit_s`, both unchanged), A_after is unchanged (hit clock; minimum 6.8 s,
medians 20.6-43.1 s, no negatives, equal to the plan's figures), 2019/2023 are 25 fps, and STATUS.md line 35 records the
correction correctly. So no 2b number moves; but `run_all.sh` has not been rerun on the corrected corpus, and the
`t_to_next_first_hit_s` sensitivity (Table 4.6) can now use 20 streams instead of 14. Settle: rerun, confirm byte-identity,
reword section 1 and limitation 8 as "found by 2b, since corrected".

**m3. E1 economy tests reject by construction.** The genre inventory is built from n-grams repeated within the pooled text;
an item that recurs only inside one stream enters the inventory and all its occurrences belong to that stream, so "fewer
distinct types per team than under random dealing" (seven p = 1e-4 in Table 4.7) is guaranteed. The report says "stream-specific
repetition" but not "by construction". Settle: identify the E1 inventory leave-one-stream-out, or drop the null.

**m4. Unlogged deviations from the plan.** (a) Plan section 9 promises E2 nulls "per class and summed per slot"; only per
class is reported. (b) Key results say "16 declared equivalence classes"; the plan declares 17 (`challenge` has one form and
no test). (c) Plan section 7 lists five H4a categories; `CATS` adds `title_surname` (moot for commentary-only, used in the
all-references row). (d) Post hoc items 1-2 changed `p04` after a first run of H4/H5 whose outputs are not preserved, so the
reader cannot see whether the 23 re-classified references moved H4b across 0.05. Settle: one line each in section 7; keep
first-run results in `results/first_run/` when a post hoc change is made.

**m5. Confidence levels and single-whitespace-word spans.** Both coders used LOW 1-2 times, so the "all confidences" row of
Table 3.1 duplicates the primary row and the by-confidence recall strata for LOW (3 and 5 tokens) are noise. The 30 (A) and
28 (B) spans that are one whitespace word are hyphenated score calls ("15-30", "40-15"), which the tokeniser splits into two
tokens, so manual rule 1 is not broken; `calibrate.py` handles them correctly. Settle: drop the redundant row and the LOW strata.

**m6. Coder independence and blindness are asserted, not shown.** Both codings were committed from this session by the same
model family (same author and `Claude-Session`, 20 s apart); coder B's spans were generated from hand-written Python specs
(`scratchpad/codeB/part1-4.py`, `gen.py`), i.e. an agent of the same kind as the analyst; and the Phase 2 report with its
top-formula tables was in the repository the coders worked in. The report's wording ("two runs of the same kind of judge") is
right; the paper should add that blindness relied on instruction, and that a human specialist coding of even 50 utterances
would be the only validity check. Settle: record the coder prompts and model ids in `analysis/parry/hand/`.

**m7. Name normalisation is uneven, and press has almost no names.** Hypocoristics (`rafa`, `nole`, `rog`, `carlitos`) are not
in the 44-token lexicon, so 135 "rafa" tokens stay raw in TV; un-normalised player surnames (Sackmann surname list, >= 5
letters) run at 1.04 per 1,000 tokens in TV, 1.00 in press, 0.25 in Cornell, so the asymmetry is small. But `<name>` is 0.10%
of press tokens against 2.6% in TV: `from <name>` / `for <name>` frames cannot be shared from press for a genre reason, which
the H2b sentence about "frames around player names" should say. Settle: add the hypocoristics to the lexicon; state the
`<name>` shares.

**m8. "Idiolect" and "team" overstate the unit.** A stream is one match with one unnamed broadcaster, as the report says; a
28% "idiolect share" at S = 1,500 is what 95-type inventories give (Spearman -0.66 with length). Settle: "stream-specific
share", and present the full-text figure (17%) first.

**m9. H4a is stream-, not team-, specificity.** Robust (see M5), but hypocoristic and epithet categories are bound to players
and to hand resolution; the Key results example ("first names are 0-41% of references by team") is the right one. Settle:
say "stream (team, match and broadcaster together)".

**m10. Literals in the generator** (M6 lists them): "2007-2015", "about 58%", "about a quarter", the two-word-units verdict.

**m11. Calibration sample halves differ in length and pool size.** 150 uniform 2019 utterances (median 25 words) vs 150
token-weighted others (median 59 words; pool of 17 streams instead of 18); any 2019-vs-other comparison inherits both.
Settle: say so beside Table 3.3's group rows.

**m12. Plan section 4 promised the idiolect-size correlation "reported"; it is, but with p-values that are not counted (m1),
and Table 2.11's slot rows depend on the `classify(span)` mode (M4).** Settle: label them descriptive.

## Checks that passed

1. Report numbers equal results files: 162 strings (Tables 2.2, 2.3, 2.5, 2.10, 2.12, 2.2x, 2.3x, 3.1, 3.2, 4.4, 4.5b, 4.6, 4.9
   and the Key results values H1-H5, kappa, classifier agreement) reproduced from the CSV/JSON by `check_report_numbers.py`,
   0 mismatches; Holm recomputed by hand (0.0001 x 7 = 0.0007; 0.0002 x 6 = 0.0012; 0.0221 x 2 = 0.0442); p floors 2/(B+1)
   and 1/(N+1) stated.
2. Order in git: plan 34478c3 (00:16:36) < lib2b/p01 7cd04e6 (00:26:41) < scripts and first results 3f9d9c7 (00:47:44);
   manual and sample e4edc66 (23:56:40) < codings (00:26:12, 00:26:32) < any result; plan.md unchanged since 34478c3;
   post hoc items labelled in section 7.
3. Run reproduces: `run_all.log` shows all ten steps; test logs pass; sharing_meta R = 500 / 200, B = 2,000 / 10,000 as
   planned; the Phase 2 pool-18 value 55.03% is reproduced (`pool_to_target_meta.json`).
4. H4 nulls are size-safe: H4a permutes team labels within slot (per-slot team counts fixed), H4b permutes slot labels
   within team x player (cell sizes fixed), so "fewer cells than expected" is not a small-inventory effect; the de-clustered
   rerun (first reference per player per utterance) gives the same direction.
5. H4b power simulation (post hoc 4) is correctly re-based on permuted slots (size 0.045 at theta = 0) and the MDE 0.328
   equals `mde_h4b.csv` by interpolation.
6. H5: the null permutes A_after among utterances within stream (references of one utterance move together); the stream
   bootstrap, mixed model and MDE (2.80 x null SD = 0.053) agree; the all-references, A_before and stored-time sensitivities
   are null in the same way.
7. Timing fix: `A_after` = next clip's first hit minus this clip's last hit uses fields the frame-rate correction did not touch;
   positive in all 20 streams (min 6.8 s), medians 20.6-43.1 s; the six invalid streams are the five 29.97 fps and the one
   29.0 fps stream of the corpus README; `t_to_next_first_hit_s` has no negative values after the correction. Phase 2 used that
   field only for first-serve-fault clips of the two finals, which are 25 fps and byte-identical, so C3/C5 and the metre
   results are unaffected (STATUS.md line 35 agrees).
8. ASR does not drive H4: after `corrections.tsv`, no name variant (jokovic, federa, alcarez ...) survives in `text_corrected`
   (only the possessive "sinner's"), so form categories are not ASR-dependent; the E3 extraction reproduces Phase 2's totals.
9. Coder files: 0 relocated and 0 dropped spans; no span over 15 words; no overlaps other than FIXED inside FRAME; the only
   one-whitespace-word spans are hyphenated score calls that tokenise to two tokens.
10. Pairwise machinery: asymmetry |C_ij - C_ji| mean 0.57 pp; per-pair replicate spread ~5 pp wide but R = 500; the vertex
    bootstrap excludes pairs of copies of the same stream; baseline teams are held fixed as the plan says.
11. The hint-cluster p (44/190 = 0.2316) and the QAP same-slam term survive shared-players and gender in the model; the
    report attributes same-slam sharing to broadcaster + venue + surface, not to a team.
12. Cornell normalisation uses the update's `players`; press uses the interviewee; the raw-token sensitivity is reported.
13. E2 forms, classes and spelling unifications are the plan's; `speed_unit` (miles vs kilometres) is a sensible broadcaster
    marker and survives correction.
14. Limitation 1-9 in section 6 are consistent with `analysis/limitations.md` and with the Phase 2 wording (repetition
    statistic, not Parry's formula).

## Overclaim audit

* Toward a "tradition": the title and the H1 bullet suggest a shared stock beyond English (M2); H2's size is null-specific
  (M1); "rejected" is printed for six of seven tests although two are trivial and one is fragile (M5). The report must not
  claim a commentary tradition from two-word collocations, and it does not in its prose; the Key results list does.
* Against thrift: the report under-reports what the data support. At pooled size the TV-specific stock at n >= 3 is about
  10% of a target's tokens (A1), much of it the umpire's register plus score and time frames; naming habits are robustly
  stream-specific (H4a, surname 33-98% by stream); unit choice for serve speed is a broadcaster marker. These are the
  Parry-adjacent findings to keep: a fixed official register and stream-level naming economy, not slot-conditioned form choice.
* Homer: no Homeric claim is made in the report; "Parryan one-form-per-slot pattern" is tested and found absent (18 of 20
  teams), which is correctly stated. Section 5's reading of H4b is careful; the Key results line is not.

## Shortest path before the paper

1. Add the 100k-token pooled comparison (A1) with and without the umpire mask; rewrite Key results bullets 2-3 from it.
2. Print observed beside excess for H2 (M1); move H1 to a check (M2).
3. Add kappa and chance/ceiling to Table 3.2 and fix the 2019-vs-other sentence (M3).
4. Validate `classify_context` or add the sensitivity (M4); report H4b as not robust and raise N_PERM (M5).
5. Remove verdict literals from `make_report.py` (M6); rerun `run_all.sh` on the corrected corpus (m2); fix the exploratory
   count (m1).
