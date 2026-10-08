# Phase 2b analysis plan: the tradition across broadcasts (shared stock, calibration, thrift per slot)

Written and committed before any Phase 2b test script was written or run. **All of Phase 2b is exploratory relative to
the pre-registered Phase 2** (analysis/formulas/plan.md, committed before the Phase 2 results): it was added by the human
after Phase 2 closed and after every Phase 2 result had been seen. Within 2b, a small family of tests is designated
"2b-primary" below (section 7) so that the reader can see which analyses were fixed in advance and corrected for
multiplicity; they are not confirmatory in the Phase 2 sense, because their design was chosen with knowledge of the
Phase 2 results on the same corpus.

What was looked at before this commit (no sharing, coverage, kappa, thrift or extension figure of 2b was computed):
1. every Phase 2 report, result file and critic review (analysis/formulas/, analysis/metre/, review/critic_analysis_v1.md, v2.md);
2. stream token counts (Phase 2 Table 3.4: smallest TV stream 1,597 tokens, 2020 Roland Garros women's final; 17 streams have >= 3,000);
3. press-conference answer tokens per interviewee (358 interviewees; the four largest are Federer, Djokovic, Murray, Nadal, each > 280,000 tokens);
4. clip timing fields per stream. **Finding:** in 6 streams (2021, 2022, 2023, 2024, 2025 US Open; 2025 AO semi-final) the video runs at
   about 29.97 frames per second but `clip_start_s`/`clip_end_s` are frames/25, so `t_to_next_first_hit_s` and `t_since_prev_last_hit_s`
   mix two clocks and are negative for most clips (down to -1,857 s). The hit times (`first_hit_s`, `last_hit_s`) are on one clock in every
   stream; the hit-clock gap "next clip's first hit minus this clip's last hit" is positive in all 20 streams (minimum 6.8 s, medians
   20.6-43.1 s). `dead_time_before_s` exists only for the two finals (PBP clock). This is a corpus defect to report (FOR_HUMAN via the orchestrator); 2b does not edit corpus/;
5. broadcaster hints: only four streams carry any (2019 'Boris', 'Tim'; 2023 'Tim', 'Todd'; 2021 US Open women's 'Kim', 'Amazon', 'Prime';
   2022 AO men's 'Brad'); all [unverified];
6. player nationalities available in the Sackmann slam `*-matches.csv` files (`nation1`, `nation2`): found for 19 of the 22 distinct players;
   missing for Alcaraz, Raducanu, Shelton;
7. the fields of the Cornell records (`players` = the two surnames of the scoreline) and of the 300-utterance coding sample.

Seeds: master seed 20261007; each script derives its own (documented in the script). Everything reruns with
`bash analysis/parry/run_all.sh`; scripts run with `python -I`; results in analysis/parry/results/, figures in analysis/parry/figures/
(drawn from results files only), the report analysis/parry/report.md is generated from results by a script. No number in the report is typed by hand.

## 0. Data and units

| team | text | utterance | use |
|---|---|---|---|
| 20 TV streams (`tv_2019wimF`, `tv_2023wimF`, 18 `tv_pool_*`) | `text_corrected` (the corpus's corrections.tsv rules applied), raw WhisperX ASR | one rally clip | the "teams" whose stock is compared; one stream = one match x one unnamed broadcaster/commentary team |
| `cornell` | Cornell / Sports Mole written live text | one update | further team, written baseline (medium = text; never pooled with speech) |
| `press_pooled` | Cornell press-conference player answers, all interviewees | one answer | further team, spoken non-commentary baseline |
| `press_<speaker>` (Federer, Djokovic, Murray, Nadal) | answers of one interviewee | one answer | exploratory single-speaker baselines (idiolect of one speaker in a non-commentary genre) |

Utterances with no tokens are dropped (as Phase 2). Nothing is pooled across media: the Cornell and press teams are only ever sources or
targets in pairwise comparisons, never merged with TV text.

## 1. Tokens and normalisation

* Tokeniser, STOP list (182 words), n-gram machinery: analysis/formulas/common.py, imported unchanged.
* **Primary normalisation (2b):** after tokenisation, (i) every token for which `common.is_num` is true (digit strings and
  `love fifteen thirty forty deuce`, Phase 2's `<NUM>` slot type) becomes `<num>`; (ii) every player-name token becomes `<name>`
  (`<name>'s` for a possessive), where the name set is Phase 2's lexicon (first names and surnames of the players of the 20 TV matches,
  `common.player_name_lexicon`) plus, for a Cornell update, the tokens of its `players` field, and, for a press answer, the tokens of the
  interviewee's name. Rationale: player names are match content, not stock; without (ii) two streams share n-grams only because they share a
  player. `<num>` and `<name>` are not STOP words.
* **Sensitivity "raw":** no normalisation (exactly Phase 2's tokens).

## 2. Inventories (2b.1)

* **Formula of a team** (= used as a formula by that team): an n-gram, 2 <= n <= 12, occurring in >= 2 distinct utterances of the team's
  text, not made only of STOP words (Phase 2 "base" filter; `common.formula_set_fast`). Variants: **n >= 3** (the same inventory restricted to n >= 3),
  and **content** (excluding n-grams made only of STOP words, numerals (`common.NUMERAL_WORDS`) and `<num>`).
* **Coverage** of a text M by an inventory F: share of M's tokens inside at least one occurrence in M of an n-gram of F (n >= 2 for base and content,
  n >= 3 for n3).
* Per-stream inventory table: types (n >= 2, n >= 3) and types per 1,000 tokens, at full size and at matched size.

## 3. Pairwise sharing at matched size (2b.1)

* Matched size **S = 1,500 tokens** (primary; below the smallest stream, so all 20 TV streams enter); sensitivity **S = 3,000** (the 17 TV streams
  with >= 3,000 tokens and all baselines). Subsample = random utterance order without replacement, whole utterances until >= S tokens (`common.subsample`).
* Replicates: **R = 500** at S = 1,500, **R = 200** at S = 3,000. In each replicate every team is subsampled independently once; the inventory F_i
  is identified on i's subsample; for every ordered pair (i, j), i != j: **coverage C_ij** = coverage of j's subsample by F_i; **Jaccard J_ij** =
  |F_i intersect F_j| / |F_i union F_j| (symmetric). Computed for base, n3 and content (Jaccard for base and n3).
* **Null (a), unigram-preserving shuffle:** in the same replicate, each team's subsample has its tokens permuted over all its positions (utterance lengths kept;
  the multiset of tokens, i.e. lexicon and topic, is identical; multiword units are destroyed); identification and coverage are repeated on the
  shuffled texts. **Excess** E_ij = mean_r C_ij(observed) - mean_r C_ij(shuffled). Per pair: mean, null mean, excess, and the 2.5-97.5% range of the
  replicate differences (a spread over subsamples, not a CI).
* **Baselines (b):** `cornell`, `press_pooled` and the four `press_<speaker>` teams go through the same procedure; their rows and columns of the
  pair matrices are reported.
* **Aggregates and CIs:** mean over ordered TV pairs; per target j, mean over TV sources i != j; TV->TV minus Cornell->TV and minus press->TV.
  Uncertainty: **vertex bootstrap over the 20 TV streams** (resample streams with replacement; average over ordered pairs of resampled positions whose
  original streams differ; B = 2,000 for CIs, B = 10,000 for the p-values of section 7). The bootstrap covers the sampling of broadcasts, holding each
  pair's replicate mean fixed. Baseline teams are fixed (not resampled).

## 4. Genre core and idiolect (2b.1)

* K(g) = number of the 20 TV streams whose inventory contains g. Core_k = {g : K(g) >= k}, k = 2..20. Sizes reported (base and n3) at full size
  (each stream's whole text; primary for the core-size curve) and at matched size S = 1,500 (mean over R = 200 replicates).
* For each TV stream s, the tokens covered by its own inventory F_s ("formula tokens"); each such token gets a(t) = max K(g) over the g in F_s that cover it.
  **Idiolect share** = share of s's formula tokens with a(t) = 1 (every covering formula is found in no other stream's inventory); **core-k share** = share
  with a(t) >= k, for k = 2, 5, 10, 15, 20. Primary for these per-stream shares: matched size S = 1,500 (K counted over the 20 subsampled inventories
  of the same replicate; R = 200; mean and 2.5-97.5% range); full size as sensitivity. Correlation of idiolect share with stream size reported.
* **By situational slot:** each formula token takes the slot of the longest own-inventory occurrence covering it (ties: leftmost), classified by the slot
  classifier (section 5) on that occurrence's span.
* Baseline comparison (exploratory): share of Core_k types (full size) that are in the inventory of a Cornell, and of a press_pooled, random subsample of the
  same total size as the 20 TV streams together (R = 20).

## 5. Situational slot classifier (used in 2b.1, 2b.2, 2b.3; frozen here)

Input: the token list of one utterance (Phase 2 tokens, lower case) and a span [a, b). Output: one of SCORE, OFFICIAL, SHOT, JUDGE, STAT, CROWD, OTHER.
NAME = a token of the player-name set of section 1 (possessive stripped); SC = `0 15 30 40 love fifteen thirty forty 13 14 50` (13/14/50 are the
documented ASR confusions of thirty/forty/fifteen).

1. **OFFICIAL patterns** (regex over the space-joined utterance; a span is OFFICIAL if any of its tokens lies inside a match):
   `(mr|miss|ms|mrs) NAME`; `(NAME )+(is )?(challenging|charging|having a call)( the call)?`; `(\w+ )?has \w+ challenges? (remaining|left)`;
   `challenges? remaining`; `((service )?line )?ball was called( out| in| wide| long)?`; `new balls( please)?`; `thank you( players| please| all)*`;
   `quiet please`; `time violation( warning)?`; `code violation`; `players ready`; `hawk ?eye`; `overrule[sd]?|overruled`.
2. **SCORE patterns** (same rule): `SC (SC|all)`; `deuce`; `advantage (NAME|server|receiver)`; `game (and )?((\w+ )?set( and match)? )?NAME`;
   `game set and match`; `NAME leads? (by )?\w+ (games?|sets?) to \w+`; `\w+ games? all`; `\w+ sets? (to|all) \w+`;
   `(break|set|match|championship|game) points?`; `tie ?break(er)?s?`.
3. **Keyword lexicons** (counts of matching unigrams/bigrams inside the span; the slot with most hits wins; ties broken in the order
   OFFICIAL > SCORE > CROWD > STAT > SHOT > JUDGE):
   * OFFICIAL: challenge, challenges, challenged, umpire, umpire's, referee, supervisor, linesman, lineswoman, "line judge", "the call".
   * SCORE: love, advantage, deuce, tiebreak, tiebreaker, "games all", "all square", "hold serve", "holds serve", "held serve", broken,
     "break back", "breaks back", "double break", consolidate, consolidates, consolidated.
   * SHOT: forehand(s), backhand(s), serve(s), served, serving, volley(s), volleyed, smash, smashed, overhead, lob, lobs, lobbed, dropshot, "drop shot",
     "drop volley", slice, sliced, topspin, return, returns, returned, returner, rally, rallies, groundstroke(s), "passing shot", net, nets, netted, tape,
     "net cord", line, lines, baseline, sideline, tramline(s), wide, long, crosscourt, "cross court", "down the line", "inside out", "down the t",
     "down the middle", "out wide", "the body", ace, aces, winner, winners, error, errors, unforced, mishit, framed, shot, shots, swing, struck, strike,
     hit, hits, hitting, angle, angled, approach, kick, kicker, spin, pace, deep, short, racket, racquet, footwork, slide, sliding, chase, chased,
     retrieve, retrieved, defend, defends, defended, defending, defence, defense, scramble, scrambled, "double fault", fault, faults, stroke(s), "first serve",
     "second serve".
   * STAT: percent, percentage, "per cent", statistics, stats, statistic, record, records, title, titles, slam, slams, "grand slam", major, majors, ranking,
     rankings, ranked, seed, seeded, seeds, career, history, historic, year, years, season, seasons, times, minutes, hours, hour, mph, miles, kilometres,
     kilometers, km, kph, average, averaging, h2h, "head to head", trophy, trophies, debut, age, aged, born, prize, money, million, olympic, olympics,
     weeks, consecutive, streak, "in a row", tournament, tournaments, championships, finals, semifinal, semifinals, "semi final", quarterfinal,
     quarterfinals, "quarter final", "number one", "world number", "first time", "last year".
   * CROWD: crowd, crowds, fans, fan, spectators, spectator, audience, applause, applauding, applaud, clapping, cheer, cheers, cheering, cheered, chant,
     chanting, ovation, atmosphere, noise, roar, roars, royal, box, stands, stadium, arena, roof, rain, weather, wind, windy, breeze, sun, sunshine, heat,
     hot, cold, temperature, shade, lights, seats, celebrity, celebrities, supporters, flag, flags, "centre court", "center court", "arthur ashe", "rod laver",
     chatrier, wife, family, parents.
   * JUDGE: good, great, brilliant, superb, lovely, beautiful, beautifully, fantastic, incredible, incredibly, unbelievable, amazing, terrific, wonderful,
     excellent, magnificent, sensational, spectacular, extraordinary, remarkable, impressive, poor, bad, terrible, awful, sloppy, loose, careless, tough,
     difficult, easy, hard, important, crucial, vital, big, huge, key, pressure, nerves, nervous, confidence, confident, tension, tense, tight, mental,
     mentally, physical, physically, tired, fatigue, energy, momentum, rhythm, focus, focused, aggressive, aggression, passive, defensive, attacking,
     tactics, tactical, tactically, plan, strategy, needs, need, needed, must, should, "has to", "have to", "got to", think, thinks, thought, feel, feels,
     felt, believe, believes, know, knows, "little bit", maybe, perhaps, probably, really, quite, "well played", mistake, mistakes, smart, clever, brave,
     courage, composure, calm, frustrated, frustration, angry, upset, emotion, emotions, emotional, happy, disappointed, relief, character, belief,
     "what a", best, better, worse, worst, nice, nicely, perfect, perfectly, quality, class, outstanding, typical, special, genius, wow.
4. If steps 1-3 give nothing for the span, they are repeated on the window [a - 4, b + 4) clipped to the utterance.
5. Otherwise OTHER.

Token-level slot (every token t): the classifier on the span [t, t + 1). Reference-level slot (2b.3): the classifier on the window of 4 tokens on
either side of the reference, excluding the reference's own tokens (steps 1-2 still use pattern matches over the whole utterance).
The lexicons were written from the coders' manual definitions and general knowledge of tennis English; they were not tuned on the coding sample or on
any 2b output. Agreement with the blind coders' slot labels (section 6) is the only validation; changes after that would be labelled post hoc.

## 6. Calibration against hand coding (2b.2): `analysis/parry/calibrate.py`

Inputs: `analysis/parry/coding_A.jsonl`, `coding_B.jsonl` (format in manual.md), the sample `corpus/transcripts/samples/parry_sample_300.jsonl`
(gitignored), `sample_ids.json`. The coders are **two LLM agents**, blind to the automatic inventory; kappa measures their mutual reliability,
not the validity of either against Parry's concept or against human experts.

* Spans to tokens: Phase 2 tokens with character offsets in the utterance's `text`; a token is inside a span if their character intervals overlap.
  A span whose `text` differs from the slice is re-located at the occurrence of `text` in the utterance nearest to `start_char`; if absent it is dropped;
  counts of relocated and dropped spans are reported. Utterances missing from a coder's file are excluded from every statistic that needs both coders (counted).
* **Coder-positive tokens:** inside a HIGH or MEDIUM span (primary); inside any span (sensitivity, includes LOW).
* **Inter-coder agreement:** token-level Cohen's kappa (primary positive set; also with LOW); span-level F1 with exact matching (identical token interval)
  and overlap matching (one-to-one, greedy by token Jaccard among overlapping pairs); for overlap-matched spans, % agreement and Cohen's kappa on slot and on
  type (FIXED/FRAME). CIs: percentile bootstrap over utterances, B = 2,000.
* **Automatic measures** (token-level positive sets), each evaluated against coder A, coder B, their intersection and their union:
  (1) pool exact n >= 2, (2) pool exact n >= 3, (3) pool systems only, (3b) pool exact n >= 2 or systems, (4) in-sample exact n >= 2, (5) in-sample n >= 3;
  exploratory: (6) pool exact n >= 2 under the 2b normalisation, (7) content n >= 2 (pool), (8) genre core, K(g) >= 5 at full size.
  "Pool" = the 18 `tv_pool_*` streams minus the utterance's own stream (for 2019 and 2023 utterances, all 18), raw Phase 2 tokens and Phase 2 criteria for
  (a) formulas and (b) systems; "in-sample" = the utterance's own full stream (n-gram in >= 2 distinct utterances of the stream, the utterance itself included).
* Precision, recall, F1 (micro over the tokens of all coded utterances), bootstrap CI over utterances (B = 2,000). Recall stratified by the coder's slot and by
  confidence (HIGH / MEDIUM / LOW); precision stratified by the classifier's token-level slot; both also split 2019 vs other streams.
* **Slot classifier agreement:** for every coder span, classifier(span) vs the coder's slot: % agreement, Cohen's kappa, confusion matrix, per coder.
* The script is first tested on a synthetic example with hand-computable answers (`tests/test_calibrate.py`); it runs on the real files only if both exist.

## 7. 2b-primary tests (fixed now; Holm-Bonferroni over these seven p-values, alpha = 0.05)

| id | claim tested | statistic | null and p-value |
|---|---|---|---|
| H1a | TV teams share multiword stock beyond lexicon | mean over the 380 ordered TV pairs of E_ij (base, S = 1,500) | vertex bootstrap (B = 10,000); two-sided p = 2 min(P*(T <= 0), P*(T >= 0)), floor 2/(B + 1) |
| H1b | same for longer units | as H1a with n >= 3 | as H1a |
| H2a | TV teams share more with each other than written live text shares with them | mean over TV targets j of [mean over TV sources i != j of E_ij - E_cornell,j] (base) | as H1a |
| H2b | same against press answers | as H2a with `press_pooled` | as H1a |
| H4a | naming habits are team-specific (team-level economy) | D_a = sum over TV team x situational slot cells of the number of distinct reference categories (surname, first name, full name, hypocoristic, epithet), commentary-only references | team labels permuted among reference tokens within each slot (10,000 permutations); one-sided p for D_a below the null |
| H4b | form choice is slot-bound within a team (Parryan thrift) | D_b = sum over team x player x situational slot cells of the number of distinct expression forms | slot labels permuted among tokens within each team x player (10,000 permutations); one-sided (fewer) |
| H5 | extension: longer referring expressions where more time is available | weighted mean (by tokens) of within-stream Spearman rho between syllables and A_after (section 9) | A_after permuted among utterances within stream (tokens of an utterance keep one value; 10,000 permutations); two-sided |

The null hypotheses, stated exactly: H1: the expected matched-size coverage of a TV stream by another TV stream's inventory equals that of their
unigram-shuffled texts. H2: that excess is no larger for TV sources than for the Cornell (H2a) / press (H2b) source. H4a: given the slot, the reference
category is independent of the team. H4b: within team x player, the expression form is independent of the situational slot. H5: within stream, the
syllable count of a reference is independent of the time available after its clip. The bootstrap p-values (H1, H2) are percentile-bootstrap
approximations for a population of broadcasts from which the 20 streams are treated as exchangeable draws; they are reported with their floor.
Everything else in 2b is exploratory and labelled so; exploratory p-values are unadjusted, and the report states how many exploratory tests were run.

## 8. Clusters and per-target coverage (2b.1, exploratory)

* Pair similarity for clusters: symmetric excess sharing (E_ij + E_ji)/2 (base, S = 1,500) and observed Jaccard (base).
* Labels: hint cluster ('Tim' = {2019, 2023 finals}; 'Brad' and 'Kim' single streams; streams without hints are singletons, never "same team"), slam
  (AO / RG / Wimbledon / US Open), year, gender (M/W). Statistic: mean within-cluster pair similarity minus mean between-cluster. Null: cluster labels
  permuted over the 20 streams, 10,000 permutations; for the hint cluster the null is enumerated exactly (any 2 of 20 streams; 190 pairs), so p = rank of the
  2019-2023 pair among all pairs. The hint pair is confounded with slam (Wimbledon), player (Djokovic) and round (final).
* Shared players: Mantel-type correlation between pair similarity and the number of shared players (0/1/2), and between pair similarity and |year difference|,
  node-label permutation (10,000); a QAP regression of similarity on same slam, same gender, shared players, |year difference| and same hint, with node-permutation
  p-values. The 2019-2023 pair is reported separately (value, rank among 190).
* **Pool -> target coverage for every TV stream as target**: I = the other 19 TV streams pooled, M = the target; raw Phase 2 tokens (base and n3) and 2b
  normalisation; 95% bootstrap CI over M's utterances (B = 2,000, I fixed, as in Phase 2); and an I-size-matched version (I = random 100,000-token subsample of
  the other 19 streams, R = 20, mean and range). Check: for 2019 with I = the 18 pool streams and raw tokens the Phase 2 value (55.0%) must be reproduced.

## 9. Thrift and extension per situational slot (2b.3)

* **Available time** A_after = `first_hit_s` of the next clip minus `last_hit_s` of this clip (hit clock; the clip's text runs into the following dead time,
  so this is the apt interval; the stored `t_to_next_first_hit_s` is invalid in 6 streams, section "looked at", item 4); missing for a stream's last clip or a
  clip without hits. Sensitivity: `t_to_next_first_hit_s` on the 14 streams where it is valid; A_before (this first hit minus previous last hit).
* **E3, referring expressions (primary for H4, H5):** for each TV stream, the two players of the match. Forms (longest match first, possessive stripped):
  full name; title + surname (`mr|miss|ms|mrs`); surname; first name; hypocoristic (`nole`, `rog`, `rafa`, `carlitos`); nationality epithet
  `the (young |younger |great |big )?<demonym>` with demonyms from `hand/players.tsv` (nationality from the Sackmann slam match files, three players entered by hand
  and marked [unverified]); resolved to the player of that nationality (no match has two players of one nationality). Other descriptive epithets (Phase 2's regex
  family: champion, world number one, seeds, young/older man, N-time champion, N-year-old, plus `the young|younger|older woman`, `the teenager`, `the qualifier`,
  `the maestro`) are resolved by Phase 2's hand verdicts (`analysis/formulas/hand/epithet_referents.tsv`) in the two finals and are otherwise counted as
  "epithet, referent unresolved" (excluded from per-player cells; their count bounds the epithet share). Commentary-only = references not inside umpire patterns
  (Phase 2 `refexpr.umpire_rule`, extended to `miss|ms|mrs`); all references as sensitivity. Syntactic slot (spaCy, Phase 2 mapping), syllables (Phase 2 counter),
  situational slot (section 5, reference window).
  Tables: per team, shares of surname / first name / full name / title / hypocoristic / epithet (resolved; and with unresolved as an upper bound); per team x player x
  slot (situational and syntactic): tokens, distinct forms, modal-form share, distinct forms per 100 references and per 100 tokens of the slot.
  **Parryan one-form-per-slot pattern:** a team shows it if, for each player, every situational-slot cell with >= 5 commentary references has a modal-form share
  >= 0.9 and at least two such cells have different modal forms (complementary distribution); a team whose cells all share one modal form at >= 0.9 is reported
  as "one form throughout" (economy without slot conditioning). The same is reported for syntactic slots.
* **E1, formula expressions (exploratory):** genre inventory = 2b-normalised formulas (base) and OPEN-slot systems (Phase 2 criteria) identified on the 20 TV streams
  pooled. Each stream is segmented left to right, greedy longest item first; each occurrence has a type (n-gram or frame with `<_>`) and a slot (classifier on its span).
  Per stream x slot: slot tokens (token-level classifier), occurrences, distinct types, distinct types per 100 slot tokens, modal-type share. Null across teams: team
  labels permuted among occurrences within slot (10,000; one-sided, fewer distinct types = team-specific stock). No cross-slot null for E1: the slot is computed from
  the expression's own words, so permuting it would be circular.
* **E2, functional-equivalence classes (exploratory; the classes and forms below are frozen here; spelling variants unified first:
  `crosscourt` -> `cross court`, `hawkeye` -> `hawk eye`, `tiebreak|tiebreaker` -> `tie break`, `per cent` -> `percent`, `centre`/`center` unified):**
  SCORE: tied at forty {`deuce`, `40 all`, `forty all`, `40 40`}; match point {`match point(s)`, `championship point(s)`}; break chance {`break point(s)`,
  `break back point(s)`, `chance(s) to break`, `break chance(s)`, `break opportunit(y|ies)`}. OFFICIAL: challenge {`is challenging`, `challenge from`,
  `going to challenge`, `has challenged`, `challenges the call`}. SHOT: net error {`into the net`, `in the net`, `into the tape`, `finds|found the net`,
  `hits|hit the net`, `into the bottom of the net`}; along the line {`down the line`, `up the line`}; serve to the centre {`down the t`, `down the middle`,
  `down the centre`, `up the t`, `up the middle`}; serve to the body {`into the body`, `at the body`, `body serve`, `to the body`}; serve wide {`out wide`,
  `wide serve`, `serve wide`, `swinging wide`}. JUDGE: small degree {`a little bit`, `a little`, `a bit`, `slightly`, `a touch`}; praise of a stroke
  {form = `what a | great | good | lovely | brilliant | superb | fantastic | beautiful | terrific | wonderful | unbelievable | incredible | amazing | magnificent |
  sensational | excellent`, followed by one of `shot point rally return forehand backhand serve volley winner get`}; well played {`well played`, `nicely played`,
  `beautifully played`, `brilliantly played`, `superbly played`, `well done`}; obligation {`need(s) to` -> need to, `has|have to` -> have to,
  `('s|has|have) got to|got to` -> got to, `must`}; opinion hedge {`i think`, `i feel`, `i believe`, `i reckon`, `i suspect`, `i'd say|i would say`, `i guess`}.
  STAT: speed unit {`<num> miles an hour`, `<num> miles per hour`, `<num> mph`, `<num> kilometres|kilometers an hour|per hour`, `<num> km h`, `<num> kph`};
  major titles {`grand slam titles`, `slam titles`, `major titles`, `grand slams`, `majors`, `slams`}. CROWD: audience {`crowd`, `fans`, `spectators`,
  `audience`, `supporters`}. Longest form first, no overlaps. Per team x class: occurrences, distinct forms, modal share (Cornell and press reported beside the TV teams);
  null across TV teams as for E1, per class and summed per slot. Extension (exploratory): syllables of the form vs A_after within stream x class.
* **Nulls for E3:** across teams (H4a, on categories, because players differ between teams) and across slots within team x player (H4b, on forms). Per-team
  versions of H4b and the syntactic-slot versions are exploratory.
* **Economy index** reported everywhere as (i) modal-form share and (ii) distinct forms per 100 tokens of the slot (as the brief asks) and per 100 occurrences.
* **Extension (H5):** tokens = commentary-only resolved references with A_after; y = syllables. Primary statistic and null in section 7. Also: stream-cluster
  bootstrap CI of the weighted rho (B = 2,000); a linear mixed model syllables ~ log(A_after) + (1 | stream) (statsmodels MixedLM; exploratory);
  **minimum detectable effect** at the pooled N: rho_MDE = (z_0.975 + z_0.80) x SD of the permutation null = 2.80 SD (normal approximation), and for H4b a
  simulation as in Phase 2 f09 (with probability theta a reference takes a designated form of its team x player x slot cell; 200 simulated data sets per theta,
  499 permutations each; theta at 80% power interpolated).

## 10. Exclusion rules (summary)

Empty utterances dropped; streams with fewer than S tokens excluded at that S (none at 1,500; three at 3,000); umpire-pattern references excluded from
commentary-only thrift/extension (sensitivity with all); unresolved epithets excluded from per-player cells; references or occurrences without A_after
excluded from extension only; coder spans that cannot be located excluded and counted; nothing else is removed.

## 11. Limits stated in advance

ASR noise breaks exact repeats in TV text (sources and targets), so TV-TV sharing and the TV inventories are attenuated, while Cornell and press texts are
edited; this biases H2 towards 0. Clip-level text: slots and times are clip or window properties. Hints, broadcasters and commentators are unverified; a
stream is one match with one unnamed broadcaster, so team, match and broadcaster are confounded. The slot classifier and the E2 equivalence classes are
my own specification; their validity is checked only against two LLM coders. All of 2b is exploratory relative to Phase 2.

## 12. Files

lib2b.py (normalisation, inventories, coverage, slot classifier, vertex bootstrap); p01_sharing.py (sections 3, 7 H1-H2); p02_core.py (section 4);
p03_clusters_targets.py (section 8); p04_refexpr_pool.py (E3 inventory); p05_thrift.py (E1-E3, H4, H5, MDE); calibrate.py (section 6);
p06_primary.py (Holm); p07_figures.py; make_report.py; run_all.sh; tests/; hand/players.tsv.

---

## Addendum 1 (2026-10-08): revisions after review/critic_parry_v1.md. ALL OF THIS ADDENDUM IS POST HOC.

Written after the 2b results and the critic's review (1 critical, 6 major, 12 minor) had been read, including the critic's own
reruns (its large-identification-set numbers, its observed-difference bootstrap, its kappa table and its H4b variants). Nothing
below is pre-registered. The seven 2b-primary tests of section 7, their statistics, nulls, seeds and permutation counts are
unchanged and are rerun exactly as before (their outputs must reproduce byte for byte; a script checks this against commit 476a088,
the last full 2b rerun). Every new analysis writes new files; no pre-registered output file is overwritten with different content,
except that `refexpr_pool_tokens.csv` gains two columns (its existing columns are unchanged and are checked).

### A1. Cross-corpus comparison with a large identification set (new primary cross-corpus design; `p08_largeI.py`)
Reason: at S = 1,500 an n >= 3 inventory has 17-49 types and covers about 1% of a target, so the n >= 3 rows of Table 2.3 compare
near-empty inventories. The design below is the pooled design of section 8 / Phase 2, applied to three kinds of source.
* Targets: each of the 20 TV streams, whole text. Sources, each subsampled to I = 100,000 tokens (whole utterances, random order,
  `common.subsample`): (a) the other 19 TV streams pooled; (b) Cornell live text; (c) press answers pooled. R = 5 subsamples per source and
  target; seed `[SEED, 108, target index, r, token variant]`, sources drawn in the order TV, Cornell, press.
* Tokens: 2b normalisation (primary) and raw Phase 2 tokens (sensitivity). Inventory = `common.formula_set_fast(subsample, m = 2)` (n-grams
  2..12 in >= 2 utterances, not stop-only). Coverage of the target at n >= 2 and n >= 3 (token share).
* Null: in each replicate the target is unigram-shuffled once (utterance lengths kept) and each source subsample once; identification and
  coverage repeated. Excess = observed - shuffled. Reported beside the observed values; **claims rest on the observed differences**.
* Commentary-only variant: target tokens inside `common.official_mask_v2` patterns (computed on raw tokens; umpire calls, Hawk-Eye announcements
  and point-score calls) are dropped from numerator and denominator.
* Statistics: per target, mean over R of each coverage; TV minus Cornell and TV minus press, per target; mean over the 20 targets; 95%
  percentile bootstrap over targets (B = 10,000, seed `[SEED, 109]`); number of targets with a positive difference. The targets' TV sources
  overlap (18 of 19 streams in common), so the bootstrap treats targets as exchangeable and understates between-broadcast uncertainty; the
  per-target signs are reported for that reason.
* Verdict rule (generated, not typed): a TV-minus-baseline difference is reported as "TV sources cover TV targets more than <baseline>
  sources of the same size" if its 95% CI lies above 0, "less" if below 0, "no difference detected" otherwise.
* **TV-only n >= 3 stock.** For target M and replicate r with inventories F_TV, F_C, F_P (2b-normalised): an occurrence in M of an n-gram
  g in F_TV with n >= 3 is *shared* if g is in F_C or F_P, else *TV-only*. A target token covered by some n >= 3 F_TV occurrence is *shared* if
  any covering occurrence is shared, else *TV-only*. Reported: share of M's tokens that are shared / TV-only (mean over R), all tokens and
  commentary-only. Two stricter readings of TV-only, as robustness: (i) *strict*: every covering TV-only n-gram is also not a formula
  (>= 2 utterances) of the **whole** Cornell text (178,770 tokens) nor of the **whole** press corpus (5.4 million tokens); (ii)
  *cross-broadcast*: every covering TV-only n-gram occurs in >= 2 of the other 19 TV streams (so it is not repeated inside one broadcast only).
* Composition of the TV-only tokens: each TV-only token takes the slot of the longest TV-only occurrence covering it (ties: leftmost),
  classified by `SlotClassifier.classify(span)` on raw tokens (the mode validated against the coders in section 6); also the share of TV-only
  tokens inside `official_mask_v2` patterns. Per target, pooled over the 20 targets, and for the two finals. Type lists: n-grams that are TV-only
  in at least 3 of the 5 replicates, with their occurrences in the target, modal slot, number of other TV streams attesting them and their
  utterance counts in the whole Cornell and press texts.
* The S = 1,500 / 3,000 rows of Tables 2.2-2.3 are kept as the secondary, matched-small-size design. Rule for their n >= 3 rows: if the mean
  TV -> TV n >= 3 coverage at that S is below 2% of tokens they are printed with the label "near-empty inventories (not informative)".

### M1/M2. H1 and H2 at their real strength (`p09_h2_observed.py`)
* The H2-type statistic of section 7 recomputed on observed coverage, on shuffled coverage and on excess, for S = 1,500 and 3,000, base, n3 and
  content, normalised and raw tokens, from `sharing_pairs.csv`, with the same vertex bootstrap (`lib2b.vertex_boot_vs_baseline`, B = 10,000,
  seed `[SEED, 110]`) and the number of targets > 0. The H2a/H2b rows of the 2b-primary table stay as pre-registered (excess); the report states
  the observed difference beside them and bases the H2 claim on the observed difference and its CI.
* Why the Cornell shuffled null is larger: per corpus, unigram concentration (share of `<name>` and `<num>` tokens, Simpson index sum p^2,
  share of the 10 commonest types), and, over 50 shuffled 1,500-token subsamples per team (seed `[SEED, 111, team]`), the size of the shuffled
  inventory and the share of its types containing `<name>` or `<num>`.
* H1 is reported as a check that the pipeline detects collocation: the share of the TV -> TV excess reached by press -> TV and Cornell -> TV
  (Table 2.2 numbers, computed by the generator) and the press-speaker yardstick.

### M3/M4. Calibration at chance level; the slot classifier in the mode used (`calibrate_chance.py`)
* For every automatic measure x reference (A, B, A and B, A or B; HIGH + MEDIUM): auto share a, coder share c; chance precision = c, chance
  recall = a (labels placed at random with the same shares), precision ceiling = min(1, c / a); precision - c, recall - a; Cohen's kappa
  (automatic vs coder), 95% bootstrap CI over utterances (B = 2,000, seed `[SEED, 112]`). The same by sample group (2019 / other), with the
  groups' median utterance length and token weighting stated. Span level: share of HIGH spans of each coder fully inside / touching the automatic
  positive set, against a chance level from 200 random circular shifts of the automatic labels within each utterance.
* Rule for the report: an automatic measure is called a "weak proxy" for the coders' judgement if its kappa against every reference set is
  below 0.40 (about half the coders' mutual kappa).
* Slot classifier, context mode (the mode that assigns the situational slot of a reference in H4): (i) `classify_context(span)` on every coder
  span vs the coder's slot; (ii) the referring expressions of the 300 sampled utterances (p04's extraction) that lie inside a coder span, with
  `classify_context` and `classify(span)` slots vs that span's coder slot (longest covering span). Agreement and kappa per coder.
* H4a/H4b rerun with the span-mode slot of each reference (`classify(span)` on the reference; new column `slot_sit_span` written by p04) as a
  sensitivity (`p10_h4_robust.py`).

### M5. Robustness of H4a and H4b (`p10_h4_robust.py`)
* The pre-registered statistics with 100,000 permutations at three seeds (`[SEED, 113, k]`, k = 0, 1, 2), Monte Carlo SE of p.
* Variants (20,000 permutations each, seed `[SEED, 114, variant]`): without hypocoristic and epithet forms; surname and first name only;
  first reference per player per utterance; span-mode slot; without the two streams that carry hypocoristics; leave-one-stream-out
  (20 runs, 5,000 permutations each; range of p and count of p < 0.05).
* Holm under substitution: each variant's p replaces the primary p in the seven-test family and Holm is recomputed.
* **Verdict rule:** a thrift test is reported as "rejected (robust)" if the pre-registered run is Holm-rejected and every variant above
  (three 100,000-permutation seeds, each listed variant; leave-one-stream-out excluded because it changes the population) is Holm-rejected under
  substitution; "not robust / inconclusive" if the pre-registered run is rejected but at least one variant is not; "not rejected" otherwise.
  The speaker-role confound (no speaker labels: a play-by-play voice and an analyst voice that differ in naming and in typical slot produce the
  same deficit) cannot be tested and is stated beside the verdict.
* H5 sensitivity with the stored `t_to_next_first_hit_s` on all 20 streams (valid after the corpus frame-rate correction of 3.3 in
  corpus/README.md; new column `t_next_stored_all` written by p04), beside the pre-registered 14-stream row.

### Minor items
* E1 economy: the pooled-inventory null rejects by construction (a type repeated inside one stream only is in the inventory and belongs to one
  team). Added: E1 with the inventory identified leave-one-stream-out (each stream segmented with the formulas and open systems of the other 19
  streams pooled), same null (`p11_e1_loso.py`, 10,000 permutations, seed `[SEED, 115]`). E2 nulls summed per slot (plan section 9 promised them):
  per slot, the sum of D over the slot's classes, null = sum of independent within-class permutations (10,000, seed `[SEED, 116]`).
* Exploratory p-values are counted per p-value, not per row, by the generator from the results files; E2's are also given with a Bonferroni
  bound over the E2 p-values.
* `p12_rerun_check.py`: sha256 of every pre-registered results file against the version in commit 476a088 (for `refexpr_pool_tokens.csv`,
  the original columns only).
* The report generator contains no verdict literal: every verdict sentence is chosen by a rule from the results (rules above and in
  make_report.py), and every number is read from results/.

### Addendum 1, implementation notes (2026-10-08; POST HOC, written while implementing addendum 1 and after its first outputs)
* A1 type tables: besides the planned columns, each TV-only string carries its rate per 100,000 tokens in the TV streams, the whole Cornell text
  and the whole press corpus (descriptive; added because 'not a formula of a 100,000-token sample' and 'never repeated in 5.4 million tokens' are
  far apart, and the rates show where a string lies between them).
* A1 composition: the umpire/score-call share is tallied for the strict and cross-broadcast classes too (the first quick test tallied it only for
  the main TV-only class).
* M5 variant 'without the streams that carry hypocoristics' removes three streams: the two Nadal streams and the 2019 final, which has one
  hypocoristic token. The rule was applied as written.
* M5: H5 with the stored time field uses seed [SEED, 117]. The first run of p10_h4_robust.py wrote h4_robust.csv with the column list of its first
  row, which dropped the null-distribution columns; fixed (explicit columns) and rerun with the same seeds before any report was written from it.
* M3: calibrate.py writes calibration_auto_labels.json (the automatic token labels it already computed) so that calibrate_chance.py need not
  recompute them; no other calibrate.py output changes.
* Report rules (in make_report.py's docstring): ci_verdict, share_word, near-empty, weak-proxy, the thrift verdict file, the composition rule
  (OFFICIAL + SCORE + STAT >= 50% of TV-only tokens = 'majority', otherwise 'minority'), and the base-rate rule for the 2019-vs-other precision
  difference (attributed 'mostly' to the base rate if the groups' precision-minus-chance values differ by less than half their raw precisions).
