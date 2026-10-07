# Phase 2 formula analysis: pre-specified plan

Written and committed before any density, system, epithet or permutation result was computed.
Allowed before this commit: reading corpus/README.md, STATUS.md, SOURCES.md; two data-quality looks
(raw counts of player-name tokens and of "the + role-noun" strings in the two finals, to build the referring-expression
inventory below; and a count of repeated 4- and 6-grams whose occurrences are only in clips at most 3 apart, to check
whether the de-duplication left ASR-window overlap: 4 of 92 repeated 4-gram types in 2019, 0 of 11 6-grams).
Anything not listed here and computed later is **exploratory** and is labelled so in the report.

## 0. Data and roles

| role | stream(s) | use |
|---|---|---|
| MAIN, in-sample | `tv_2019wimF` | all in-sample tables; confirmatory tests C1-C5 |
| HELD-OUT | `tv_2023wimF` | measurement only (formulas identified elsewhere); replication R1-R5 |
| REFERENCE POOL | 18 `tv_pool_*` streams | identification for held-out density; per-stream table (exploratory) |
| WRITTEN CONTRAST | `text_cornell` (medium = text) | identified and measured on itself only; never pooled with speech |
| SPOKEN NON-COMMENTARY BASELINE | player answers in Cornell press-conference transcripts (`corpus/raw/cornell_tennis/extracted/transcripts_matchinfo.json`) | baseline only, never pooled with commentary |

The press-conference file is part of the same Cornell release as the USE source G in SOURCES.md; SOURCES.md row O
lists the press conferences as DON'T USE *as commentary* ("press conferences, not commentary"). They are used here only
as a non-commentary baseline, at the orchestrator's request; this is flagged in the report and in FOR_HUMAN.md, and
every result that depends on them is tagged `baseline_press`. If the human vetoes this use, drop those rows: no other
result depends on them. They are human (stenographic, ASAP Sports) transcripts, not ASR, and 2007-2015.

Text field: `text_corrected` (primary); `text_dedup` as sensitivity S1. Utterances with no tokens are dropped.
Utterance = one clip's text (TV); one live-text update (Cornell); one player answer (press). No speaker labels exist.

## 1. Tokenisation

1. Unicode NFKC; curly apostrophes to `'`; hyphen, en dash, em dash, slash to space ("40-15" -> `40 15`, "six-love" -> `six love`).
2. Lower-case (full case folding).
3. Token = regex `[a-z0-9]+(?:'[a-z0-9]+)*` on the folded text: apostrophe-internal clitics stay in the token (`it's`, `federer's`);
   all other punctuation is discarded. Digits are kept verbatim as tokens (`15`, `40`, `2019`); number words are not normalised.
4. N-grams are contiguous token sequences inside one utterance; they cross punctuation inside an utterance (WhisperX
   punctuation is inconsistent and absent in many clips) but never cross utterances.
5. STOP = a fixed list of 182 English function words (in `common.py`, frozen with this plan: articles, pronouns,
   auxiliaries and modals with their clitic forms, prepositions, conjunctions, `not`, `so`, `then`, `there`, `here`, `just`, `very`...).
   Digits and player names are never STOP.

Word counts therefore differ slightly from corpus/README (hyphen split).

## 2. Formulas (a): exact repeated n-grams

* An n-gram g (2 <= n <= 12) is a **formula of an identification set I** if it occurs in at least **m = 2 distinct utterances** of I
  and is not stop-only (at least one token not in STOP).
* **Coverage / density on a measurement set M**: a token of M is covered if it lies inside at least one occurrence, in M, of a
  formula of I with length >= n_min. Density = covered tokens / all tokens of M. Primary: **n_min = 2**.
* Per-n table: coverage by formulas of length exactly n, n = 2..7; numbers of formula types and occurrences per n.
* Maximal match: each covered token gets the length of the longest formula covering it (2..12); distribution reported.
* In-sample (I = M): an n-gram counts if it is in >= 2 utterances of the same text, i.e. "repeated elsewhere" (Duggan).
* Within vs across streams: for every 2019 formula, the number of pool streams (0..18) in which it occurs at least once.

## 3. Formulaic systems (b): frames with exactly one open slot

* Frame = n-gram (2 <= n <= 6) with exactly one position j replaced by a slot. Slot types:
  `NAME` (token, possessive stripped, in the player-name lexicon = first names and surnames of the players of all 20 TennisVL matches, from the stream match ids),
  `NUM` (digit string, or one of `love fifteen thirty forty deuce`), `OPEN` (any token).
* A frame is a **system of I** if, in I: (i) it occurs with >= 2 distinct fillers; (ii) it occurs >= 3 times in >= 3 distinct utterances;
  (iii) at least one fixed token is not STOP; (iv) an `OPEN` slot must be **internal** (fixed tokens on both sides, so n >= 3);
  typed slots (`NAME`, `NUM`) may be at any position, so `game <NAME>` and `<NUM> love` (n = 2) qualify. For a typed frame only
  occurrences whose filler is of that type count.
  Rationale for (iv): an open slot at the edge of a frame is indistinguishable from a repeated (n-1)-gram followed by any word.
* (b) coverage on M: a token is covered if it lies inside an occurrence in M of a system of I whose filler satisfies the slot type
  (the filler need not have been seen in I). **(a)+(b) density** = union of (a)-covered and (b)-covered tokens / all tokens.
* Systems are listed by occurrences, with fillers and counts (`systems_2019.tsv`).

## 4. Density designs (every density reported for (a) and for (a)+(b))

* **D1 in-sample**: I = M = 2019.
* **D2 split-half**: halves by parity of `clip_i` (odd vs even). Identify on odd, measure on even and vice versa; report both and the pooled
  value (covered tokens of both directions / tokens of both halves). Sensitivities: S7 alternating blocks of 20 consecutive clips;
  S8 200 random half-splits of utterances (distribution).
* **D3 held-out across matches**: I = 18 pool streams pooled, M = 2019; I = 2019, M = 2023; also I = pool, M = 2023.
* **D4 per stream** (exploratory; stream = one match x one unnamed broadcaster, so broadcaster and match are confounded): for each of the
  20 TV streams, (i) leave-one-stream-out held-out density (I = all pool streams except this one; M = the full stream), and
  (ii) in-sample and split-half density in random subsamples of 1,500 tokens (R = 200).
* **D5 per medium at matched size**: corpora = TV pool (18 streams, multi-match), Cornell text (multi-match), press answers.
  Subsample = random utterance order without replacement, taking whole utterances until >= S tokens.
  (i) S = 9,700 tokens (about the 2019 final): in-sample and split-half (parity of sampled order) density, R = 200 subsamples per corpus.
  (ii) Held-out at pool size: I = a 100,000-token subsample, M = a disjoint 9,700-token subsample drawn from **disjoint groups**
  (Cornell: player-pair of the scoreline as a match proxy; press: interviewee), R = 50. The TV analogue is D3 (pool -> 2019).
  (iii) In-sample at S = 100,000 for Cornell, press and the TV pool, R = 20.
  Written text and speech are always identified on themselves; nothing is pooled across media.
* **D6 per context** (2019; repeated on 2023): density per group, with formulas identified (i) in-sample on the whole stream and
  (ii) on the pool (held-out). Groups: heuristic `phase` (clip / between_points / changeover); tercile of `dead_time_before_s`;
  tercile of `time_after_s` (below); `clip_role`; score situation (below). Terciles are cut on the stream's own utterances with a value; missing = `NA` group.
  `phase` is set by regex on the text itself (score-call-only clips are `between_points`), so its density contrast is partly
  definitional: it is exploratory and reported with that warning.
* **D7 baselines**: (i) shuffled-word: all tokens of the 2019 stream randomly permuted over positions (utterance lengths kept), then
  D1 and D2 recomputed, R = 200; (ii) press answers (D5).

`time_after_s` (pre-specified because corpus/README section 4 shows the clip text runs past the clip end into the following dead time):
for a rally/ace/double-fault clip aligned to PBP point p, `dead_time_before_s` of point p+1 (points table); for a first-serve-fault clip,
`t_to_next_first_hit_s` when the next clip belongs to the same point; otherwise NA.

Score situation (from PBP score before the aligned point; most pressing category wins): `match_point` > `set_point` > `break_point` >
`tiebreak` (any other tie-break point) > `deuce_ad` (40-40 or advantage) > `other`; `NA` if unaligned. Computed for either player.

**Uncertainty.** For every density: 95% percentile bootstrap CI, B = 2,000, resampling utterances of M with replacement while the formula
inventory of I is held fixed (so the CI covers sampling of the measured text, not uncertainty in identification). For split-half pooled values,
resampling is within each half. Subsample designs (D4ii, D5, D7) report the mean and the 2.5-97.5% range over replicates.

## 5. Referring expressions (noun-epithet systems)

* Players: 2019 Federer, Djokovic; 2023 (held-out) Djokovic, Alcaraz.
* Inventory (longest match first, on tokens; possessive `'s` stripped and recorded):
  full name (`roger federer`, `novak djokovic`, `carlos alcaraz`); title + surname (`mr <surname>`); surname; first name (`roger`, `novak`, `carlos`);
  hypocoristics (`nole`, `rog`, `fed`, `carlitos`); epithets matched by the regex family in `epithets.py`:
  `the (great |young |older |younger )?(swiss|serb|serbian|spaniard|maestro|man from basel|man from belgrade|man from murcia)`,
  `the world('s)? number one`, `the (number one|top|first|second) seed`, `the (defending |reigning )?champion`,
  `the (older|younger|young) man`, `the <number> time champion`, `the <number> year old`.
  Epithets whose referent is not fixed by the words (`the champion`, `the world number one`, `the young/older/younger man`, seeds, ages)
  are assigned by a hand verdict per occurrence (`hand/epithet_referents.tsv`: utterance id, excerpt <= 15 words, referent, reason);
  nationality epithets are assigned by nationality (Swiss = Federer, Serb/Serbian = Djokovic, Spaniard = Alcaraz).
  A discovery list of all `the (<adj>)* <noun>` strings with person nouns is written for audit (exploratory).
* Pronouns `he him his himself he's he'd he'll` are excluded from the inventory but counted per context; heuristic attribution
  (exploratory): to the single player named in the same utterance, else unattributed.
* Syntactic slot: spaCy `en_core_web_sm` 3.8.0 dependency parse of the utterance text (`text_corrected`, original case and punctuation),
  label of the expression's head token: `nsubj`/`nsubjpass`/`csubj` -> subject; `dobj`/`obj`/`iobj`/`dative`/`attr`/`oprd` -> object;
  `poss` or a possessive `'s` -> possessive; `pobj`/`agent` -> after_preposition; `ROOT` of a sentence with no VERB/AUX token, `npadvmod`,
  `intj`, `vocative`, `dep` at sentence start -> vocative_exclamation (includes umpire calls such as `Game, Federer`); `conj`/`appos` -> slot of
  the head it attaches to (recursively); anything else (e.g. `compound`) -> other. Parser accuracy is checked on a hand-labelled random
  sample of 40 expressions (seed 20190714; `hand/slot_sample40.tsv`) and reported.
* Length in syllables: CMU Pronouncing Dictionary (`cmudict` 1.1.3 package), number of vowel phonemes in the first pronunciation;
  out-of-dictionary tokens: number of maximal vowel-letter groups `[aeiouy]+` minus a silent final `e` (minimum 1); digits are spelled
  out in English words first; possessive `'s` adds 1 syllable after a sibilant-final base, else 0.
* Timing context: `phase`, `dead_time_before_s` tercile, `time_after_s` tercile, score situation, `clip_role`.

## 6. Economy (thrift) and extension

* **Functionally equivalent** expressions: different expression types (normalised forms without possessive, e.g. `federer`, `roger federer`,
  `roger`, `the great swiss`) that refer to the same player and occupy the same syntactic slot in the same context cell. They are
  denotationally and syntactically interchangeable there; they differ only in form (wording, length).
* Cell = player x slot x context. Statistic D = sum over cells of the number of distinct expression types.
* Null: permute the context labels among the expression tokens **within each player x slot stratum** (cell sizes and marginals kept),
  10,000 permutations, seed 20190714. Report observed D, null mean, 95% null interval, one-sided p = (1 + #{D_null <= D_obs}) / (1 + 10,000)
  (thrift predicts fewer types per cell than chance), and the two-sided p. Tokens with NA context are dropped for that context.
* Descriptives: thrift index = share of occupied cells with exactly one type; extension = number of distinct types per player, number of
  occupied cells per player (slot x context x syllable-length class), range of syllable lengths.
* Length-time test (extension analogue of metrical shape): Spearman rho between expression length in syllables and available time,
  p from 10,000 permutations of the time values within player.

## 7. Confirmatory hypotheses (2019 final), Holm-Bonferroni over the six p-values, alpha = 0.05

| id | hypothesis | statistic and test |
|---|---|---|
| C1 | TV commentary is more formulaic than tennis speech that is not commentary | (a) density, I = pool (103k tokens) -> M = 2019, minus press D5(ii) (I = 100k, M = 9.7k disjoint). Difference distribution from 10,000 random pairs (bootstrap draw of the TV value, replicate of the press value); two-sided p = 2 min(P(diff <= 0), P(diff >= 0)) |
| C2 | Spoken TV commentary differs in formulaic density from written live text at matched size | split-half (a) density, D5(i), TV pool vs Cornell; difference over 200 paired replicates; p as in C1 |
| C3a | Less available time, more formulaic speech (time before the point) | (a) density, pool-identified, in the shortest vs longest `dead_time_before_s` tercile; token-weighted difference; p from 5,000 permutations of tercile labels among T1 and T3 utterances; two-sided; bootstrap CI |
| C3b | Same, time after the point | as C3a with `time_after_s` |
| C4 | Thrift: expression choice is context-bound | D with context = `dead_time_before_s` tercile, both players, one-sided p as in section 6 |
| C5 | Extension: longer expressions where there is more time | Spearman rho, length vs `dead_time_before_s`, both players, two-sided permutation p |

**Replication on the held-out 2023 final** (R1 = C1 with M = 2023; R3a, R3b, R4, R5 as C3a-C5 on 2023), Holm over these five.
C2 does not involve the finals and has no replication.

Everything else is **exploratory**: per-n tables, systems lists, (a)+(b) densities, per-stream and per-phase/role/score-situation
densities, sensitivity analyses, pronoun counts, slot tables, other contexts in the thrift test, cross-stream sharing.
Exploratory p-values are reported unadjusted and labelled exploratory.

## 8. Sensitivity analyses (exploratory)

S1 `text_dedup` instead of `text_corrected`; S2 no stop-only filter; S3 m = 3; S4 in-sample counting only repeats in utterances at least
4 clips apart (ASR window overlap); S5 official-call tokens masked (umpire/Hawk-Eye/announcer patterns: `game <name>`, `<name> leads by ... to ...`,
`... games all`, `mr <name> is challenging`, `... challenges remaining`, `ball was called`, `new balls please`, `thank you please`/`please thank you`,
`time violation`, `players ready`; masked tokens are removed from numerator and denominator); S6 n_min = 3; S7, S8 split variants (section 4).

## 9. Outputs for Phase 3

`results/formulas_2019.tsv` (formula, n, utterance count, occurrences, coverage share, pool streams, example excerpt <= 15 words; excerpts only for
the 100 most frequent, to keep the committed text far below the full transcript), `results/systems_2019.tsv` (excerpts for the 50 most frequent),
`results/top10_for_brief.csv`: the ten most frequent formulas or systems by distinct utterances, after dropping n-grams contained in a longer
listed formula with the same utterance count; flagged `official_call` when matched by S5 patterns; given both with and without official calls;
"typical situational slot" = modal `clip_role`, modal score situation, median `time_after_s` and `dead_time_before_s` of the utterances containing it.

## 10. Kuiper

Relate to Kuiper and Haggo 1984, Kuiper 1996 (Smooth Talkers), Kuiper and Austin (race calling) only after fetching a catalogue or publisher record
for each; anything not confirmed by a fetched record is marked [unverified].

## 11. Reproducibility

`bash analysis/formulas/run_all.sh` runs everything (scripts with `python -I`). Master seed 20190714; each script derives its own seeds.
Replicate counts may be reduced only if a script exceeds 30 minutes; any such deviation is logged in `results/deviations.json` and the report.

## Addendum (2026-10-07, written AFTER the confirmatory results C1 and C2 were seen): post hoc exploratory analysis

C1 and C2 came out with TV commentary *less* formulaic than press answers and written live text. One alternative explanation is
ASR noise in the TV text, which breaks exact repetitions. `f04b_asr_noise.py` injects substitution noise (rate e in {0, the
corpus's hand-read lower bound, 0.05, 0.10, 0.15}; replacement tokens drawn from the TV-pool unigram distribution) into press answers,
Cornell text and, as extra noise, the TV corpora, and recomputes split-half density at matched size (R = 50) and held-out density
(R = 10). This is exploratory and post hoc; it changes no confirmatory result.
