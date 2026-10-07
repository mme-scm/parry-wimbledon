# Composition brief: the 2019 Wimbledon final in about 50 Homeric hexameters (Phase 3, final; reviewed by the orchestrator after critic_analysis_v2)

For the composer agent. Every fact in section 1 carries its source (table id in `composition/research/match_facts.md` = MF, a corpus file, or a fetched URL) and its match clock (`pbp_elapsed`, the clock at the first serve of the point, 1 s resolution, 0:00:00 at point 1). Every Homeric line and count below was printed by `python homer/concordance.py` (queries given in backticks) on 2026-10-07; the 154 queries copied from `composition/research/homeric_models.md` (= HM, sections a-j) were rerun and all reproduce, with three count corrections noted in 2.0. Positions are the half-foot numbers of homer/README.md (1 = first longum, 5 = penthemimeral caesura, 5.5 = trochaic, 7 = hephthemimeral, 8 = bucolic diaeresis, 12 = last syllable). Greek is NFC polytonic; the Perseus text writes elision with ʼ (U+02BC), which the tools accept. Commentary excerpts are at most 15 words (CLAUDE.md); `tv_2019wimF:NNNN` is the clip id in `corpus/transcripts/tv_2019wimF.jsonl`. Scores are Djokovic-Federer unless marked. Scholarship: Parry 1929 and 1930 and Higbie 1990 are cited from Crossref records fetched on 2026-10-07 (DOIs in 2.7); everything else is **[unverified]**.

## 1. Match facts

### 1.1 Frame

| fact | value | source |
|---|---|---|
| date, start | Sunday 14 July 2019, 14:10 local | MF E6: MCP matches file `Time 14:10`; transcript tv_2019wimF:0266 at 2:46:46 "2 hours and 47 minutes into this final approaching 5 o'clock local time" |
| venue | Centre Court, Wimbledon, grass | MF T18: MCP matches file `Court Centre`, `Surface Grass` |
| players | Novak Djokovic (seed 1) v. Roger Federer (seed 2); both right-handed | MF E2 (Wikipedia, seeds); MCP matches file (handedness); tv_2019wimF:0430 at 4:19:56 "Seeds one and two going hit to hit" |
| ages | Federer 37: tv_2019wimF:0014 at 0:06:58 "He's 37 years of age"; MF E4 (ATP) "The 37-year-old"; MF E2 (Wikipedia) "Aged 37 years, 11 months and 6 days". Djokovic 32: tv_2019wimF:0045 at 0:24:21 "… 15th Wimbledon for Novak Djokovic 32 years of age the top seed …" | transcript; MF E2, E4 |
| umpire | Damian Steiner (chair) | MF T18 (MCP `Umpire`); tv_2019wimF:0017 at 0:09:28 "Damien Steiner in the chair" (ASR spelling) |
| first server | Federer serves point 1 (PointServer = 2) at 0:00:00 | MF F1 (R) |
| score | Djokovic d. Federer 7-6(5), 1-6, 7-6(4), 4-6, 13-12(3) | MF T1 |
| duration | clock 4:56:59 at the first serve of the last point; official 4 h 57 min | MF T1; MF E1-E2 (Wikipedia) "After 4 hours and 57 minutes"; ATP says 4 h 55 (MF E4, too low by the corpus) |
| points | Federer 218, Djokovic 204 (R, M and P agree) | MF T2 |
| games, sets | 68 games (13+7+13+10+25); sets 3-2 Djokovic; 3 tie-breaks | MF T1, T18 |
| records | longest Wimbledon singles final; first men's singles match under the 12-12 final-set tie-break rule; Djokovic's 5th Wimbledon, 16th major; Federer's 31st major final | MF E1, E2, E4 (Wikipedia, ATP) |

### 1.2 Per-player totals (MF T3-T5; R columns unless stated)

| | Federer | Djokovic |
|---|---|---|
| aces | 25 (12 in set 5) | 10 |
| double faults | 6 | 9 |
| winners (aces included) | 94 (37 in set 5) | 54 (20 in set 5) |
| unforced errors | 62 | 52 |
| net points won | 45 of 53 | 18 of 26 |
| break points converted | 7 of 13 | 3 of 8 |
| service points won | 139 of 203 (68.5%) | 140 of 219 (63.9%) |
| fastest serve | 202 km/h at 3:35:36 (s5 g8, point 307, winner; tv_2019wimF:0349 "Gone down the line. Had a big gap.") | 199 km/h at 3:07:13 (s5 g3, point 267; ended in a Djokovic unforced error) |
| distance run (R, unit unlabelled) | 5820 | 5630 |
| points won in set 5 | 84 | 85 |

### 1.3 Set by set (MF T1-T4, T18, F)

| set | games | clocks | points | what happened | commentary (≤15 words, clip, clock) |
|---|---|---|---|---|---|
| 1 | 7-6(5) Dj | 0:00:00-0:57:50 | 87 (Dj 46-41) | no break; Federer's only break point at 0:15:23; tie-break 1.4a | tv_2019wimF:0029 0:15:23 "Just over a quarter of an hour played and Federer with the first break point."; tv_2019wimF:0079 0:44:03 "The crowd is really engaging in the match now." |
| 2 | 1-6 Fe | 1:00:23-1:22:54 | 38 (Fe 26-12) | Federer breaks games 1 (1:03:00), 3 (1:08:46), 7 (1:22:54); winners Fe 9 / Dj 2, UE Fe 4 / Dj 10; 22½ min | tv_2019wimF:0106 1:08:46 "and that will do nicely probably for the set three loud two breaks"; tv_2019wimF:0129 1:20:36 "Game, Federer. Federer leads by five games to one. Second set." |
| 3 | 7-6(4) Dj | 1:27:28-2:15:24 | 73 (Fe 37-36) | no break; 26-shot rally at 2:03:53 (point 183, Dj serving 5-6 0-0) won by Federer; tie-break 1.4b | tv_2019wimF:0201 2:03:53 "justifies logic 26 shots and at the end Federer able to come up with the …" |
| 4 | 4-6 Fe | 2:20:29-2:55:08 | 55 (Fe 30-25) | Federer breaks games 5 (2:36:11) and 7 (2:42:40) for 5-2; wins the 35-shot rally (1.5) but is broken at 2:49:12 (3-5); holds for 6-4 at 2:55:08 | tv_2019wimF:0270 2:49:12 "And it's a break. Djokovic breaks the Federer Reserve. That is news."; tv_2019wimF:0277 2:55:08 "… the crowd rise and we have a fifth and deciding …" |
| 5 | 13-12(3) Dj | 3:00:13-4:56:59 | 169 (Dj 85-84) | see 1.6-1.9 | tv_2019wimF:0345 3:31:55 "It's away! Game on again in the fifth set." |

### 1.4 The three tie-breaks, point by point (MF T7, T8, T12; "ending" = last MCP shot code symbol: * winner, @ unforced error, # forced error; rally = MCP shot count including the erring shot)

(a) Set 1, 0:49:06-0:57:50, Djokovic 7-5. Federer led 5-3 and lost four points in a row (three Federer unforced errors, one forced).

| pt | clock | before | server | serve | rally | winner | ending |
|---|---|---|---|---|---|---|---|
| 76 | 0:49:06 | 0-0 | Fe | 197 (1st) | 2 | Fe | Dj forced error `6b2d#` |
| 77 | 0:49:48 | 0-1 | Dj | 172 (2nd) | 22 | Dj | Fe unforced error `...f3b3f!@` |
| 78 | 0:51:05 | 1-1 | Dj | 152 (2nd) | 14 | Dj | Fe unforced error (Dj at net) |
| 79 | 0:52:11 | 2-1 | Fe | 196 (1st) | 7 | Dj | Fe forced error |
| 80 | 0:52:44 | 3-1 | Fe | 175 (1st) | 1 | Fe | ace `4*` |
| 81 | 0:53:19 | 3-2 | Dj | 146 (2nd) | 10 | Fe | Fe winner `...f3b1*` |
| 82 | 0:55:01 | 3-3 | Dj | 180 (1st) | 6 | Fe | Fe winner at net `...f+1f3*` |
| 83 | 0:55:41 | 3-4 | Fe | 197 (1st) | 2 | Fe | serve winner, Dj forced error `4s#` |
| 84 | 0:56:03 | 3-5 | Fe | 175 (1st) | 3 | Dj | Fe unforced error `4f28f1w@` |
| 85 | 0:56:39 | 4-5 | Dj | 197 (1st) | 4 | Dj | Fe unforced error |
| 86 | 0:57:12 | 5-5 | Dj | 196 (1st) | 8 | Dj | Fe forced error (Dj at net) |
| 87 | 0:57:50 | 6-5 | Fe | 196 (1st) | 7 | Dj | Fe unforced error `...b3w@` |

Commentary: only point 76 has a transcribed clip: tv_2019wimF:0086 "Federer gets the first point. I'm not a believer in these mini break situations."

(b) Set 3, 2:07:34-2:15:24, Djokovic 7-4. Djokovic 5-1 up (24-shot rally at 2:11:04, Federer forced error), Federer back to 5-4 with a volley winner (2:13:23) and an ace (2:13:50).

| pt | clock | before | server | serve | rally | winner | ending |
|---|---|---|---|---|---|---|---|
| 188 | 2:07:34 | 0-0 | Fe | 188 | 5 | Dj | Fe unforced error |
| 189 | 2:08:28 | 1-0 | Dj | 194 | 2 | Dj | Fe forced error (let, `c6f2d#`) |
| 190 | 2:08:58 | 2-0 | Dj | 196 | 14 | Dj | Fe unforced error |
| 191 | 2:09:46 | 3-0 | Fe | 197 | 2 | Fe | Dj forced error |
| 192 | 2:10:17 | 3-1 | Fe | 149 (2nd) | 3 | Dj | Fe unforced error (backhand into net) |
| 193 | 2:11:04 | 4-1 | Dj | 193 | 24 | Dj | Fe forced error |
| 194 | 2:12:34 | 5-1 | Dj | 186 | 7 | Fe | Dj forced error |
| 195 | 2:13:23 | 5-2 | Fe | 197 | 3 | Fe | Fe volley winner `c6f2j3*` |
| 196 | 2:13:50 | 5-3 | Fe | 197 | 1 | Fe | ace `6*` |
| 197 | 2:14:28 | 5-4 | Dj | 128 (2nd) | 4 | Dj | Fe unforced error |
| 198 | 2:15:24 | 6-4 | Dj | 196 | 6 | Dj | Fe forced error (Dj at net) |

Commentary: tv_2019wimF:0208 at 2:07:34 "1-0. You've seen the first serve return by Djokovic and all of a sudden it's …"; no other clip of this tie-break is transcribed.

(c) Set 5 at 12-12, 4:48:30-4:56:59, Djokovic 7-3. Transcript ends at point 413; points 414-422 have no clip at all (MF A, T12).

| pt | clock | before | server | serve | rally | winner | ending |
|---|---|---|---|---|---|---|---|
| 413 | 4:48:30 | 0-0 | Dj | 168 (2nd) | 12 | Dj | Fe backhand unforced error `...b2d@` |
| 414 | 4:49:29 | 1-0 | Fe | 193 | 3 | Fe | Fe forehand winner `6f37f1*` |
| 415 | 4:50:01 | 1-1 | Fe | 180 | 3 | Dj | Fe half-volley forced error at net `4+f27h1w#` |
| 416 | 4:50:37 | 2-1 | Dj | 140 (2nd) | 4 | Dj | Fe forced error |
| 417 | 4:51:25 | 3-1 | Dj | 180 | 8 | Dj | Fe forced error |
| 418 | 4:52:04 | 4-1 | Fe | 156 (2nd) | 11 | Fe | Fe drop-shot winner `...f2u+3*` |
| 419 | 4:53:31 | 4-2 | Fe | 154 (2nd) | 2 | Fe | Dj forced error on the return `6b#` |
| 420 | 4:54:18 | 4-3 | Dj | 194 | 3 | Dj | Dj forehand winner `6f27f1*` |
| 421 | 4:54:48 | 5-3 | Dj | 151 (2nd) | 13 | Dj | Dj backhand winner `...f3b1*` |
| 422 | 4:56:59 | 6-3 | Fe | 143 (2nd) | 3 | Dj | Fe forehand unforced error `5b38f!@` |

Commentary: tv_2019wimF:0480 at 4:48:30 "1-0 Djokovic. Djokovic has won the two tie breaks that have been played between these …" (the last transcribed clip of the match).

### 1.5 The 35-shot rally (MF T6, F4)
Point 242 at **2:47:12**, set 4 game 8, Federer serving at 5-2 up, 40-30 Dj-Fe = break point down. First serve fault (`4w`), second serve; MCP 35 shots (R RallyCount 35; TennisVL 34 shots, 43.44 s); distance run Djokovic 104.2, Federer 85.5 (R units); **won by Federer** with a backhand winner (`...f1f1f1f2b1*`). Commentary tv_2019wimF:0268 (video 10066.7 s): "35 shots every one of them right out of the middle yes". Federer was nevertheless broken in the same game at 2:49:12 (point 244): tv_2019wimF:0270 "… after losing the longest rally of the match in such spectacular …".

### 1.6 Fifth set, game by game (MF T9; games after each game, Dj-Fe, with the clock of the game's last point; B = break)
1-0 Dj 3:02:24 · 1-1 3:05:14 · 2-1 3:10:39 · 2-2 3:16:32 (3 BP saved by Federer) · 3-2 3:20:54 · **4-2 B Dj 3:25:11** · **4-3 B Fe 3:31:55** · 4-4 3:37:10 · 5-4 3:41:32 · 5-5 3:45:28 · 6-5 3:49:49 · 6-6 3:56:54 · 7-6 4:00:00 · 7-7 4:02:57 · **7-8 B Fe 4:07:16** (point 354, forehand pass `4s27f+1f1*`; tv_2019wimF:0408 "Yeah, and that's the break.") · **8-8 B Dj 4:12:40** (1.7) · 9-8 4:17:15 · 9-9 4:21:04 · 10-9 4:24:26 · 10-10 4:27:58 · 11-10 4:31:08 · 11-11 4:34:32 · 12-11 4:44:50 (14-point game, 2 BP saved by Djokovic, 24-shot rally at 4:38:36 won by Federer) · 12-12 4:47:47 (Federer holds to love) · 13-12 tie-break 1.4c.
Commentary: tv_2019wimF:0364 3:44:27 "… 45 minutes later, we're tired watching it. Djokovic, two points from the title."; tv_2019wimF:0426 4:17:15 "Djokovic finding the mark just when he needed to he takes the lead 9-8 …"; tv_2019wimF:0474 4:44:50 "And the game ends. A brutal game. 41 up, one second. Two break points down, …"; tv_2019wimF:0477 4:47:27 "… four hours and 48 minutes matching the longest final of all time, Federer serves an …".

### 1.7 The championship game: Federer serving at 8-7, 4:08:51-4:12:40 (MF T10; TV = TennisVL shot parse)

| pt | clock | before (Dj-Fe) | serve | rally | winner | MCP ending | TV ending | commentary (clip) |
|---|---|---|---|---|---|---|---|---|
| 355 | 4:08:51 | 0-0 | 180 (1st) | 3 | Dj | Fe approach error `4f28f+3d@` | Federer unforced-error | tv_2019wimF:0409 "Thank you, players, already. Thank you, ladies and gentlemen. Please. Please. Thank you." (umpire) |
| 356 | 4:09:22 | 15-0 | 143 (2nd) | 10 | Fe | Dj error `...f1f1w@` | Djokovic unforced-error | tv_2019wimF:0410 "Sorry, Paul." |
| 357 | 4:10:13 | 15-15 | **201 (1st)** | 1 | Fe | ace `6*` | Federer winner | tv_2019wimF:0412 "The Federer's 56 aces coming into this match He's served 22 so far …" |
| 358 | 4:10:35 | 15-30 | 193 (1st) | 1 | Fe | ace `6*` | Federer winner | (none) |
| **359 CP1** | **4:10:58** | 15-40 | 1st fault `6n`; 2nd 151 km/h wide | 3 | Dj | Fe forehand inside-out wide `4f28f3w@` | serve-wide in; Djokovic forehand return down the middle; Federer forehand inside-out: unforced-error | tv_2019wimF:0414 "Please."; tv_2019wimF:0415 "Breathe in, breathe out. 40, 30." |
| **360 CP2** | **4:11:30** | 30-40 | 193 (1st) to the T | 4 | Dj | Dj forehand cross-court pass `6r28f+1f1*` | Djokovic forehand slice return; Federer forehand approach inside-in; Djokovic forehand cross-court: winner | tv_2019wimF:0416 "And just as Federer passed Djokovic to get the break in the previous game, Djokovic …" (full: "… Djokovic denies Federer in this. Two championship points.") |
| 361 | 4:11:58 | 40-40 | 1st fault; 2nd 146 body | 7 | Dj | Fe forehand slice forced error `5b28b3b3b2f1r#` | seven-shot backhand exchange, Federer forehand slice down the line: forced-error | tv_2019wimF:0417 "Well done, Dave, to Gilmour Leeds." (ASR) |
| **362 break** | **4:12:40** | AD-40 | 189 (1st) T | 5 | Dj | Fe forehand into the net `6r18f1f1f2n@` | Djokovic slice return cross-court, three cross-court forehands, Federer forehand: unforced-error | tv_2019wimF:0419 "Amazing, isn't it? That is guts from Djokovic. It almost reminds me of the semi-final, …" |

Afterwards: tv_2019wimF:0420 4:13:27 "Five strike points for Djokovic. It's going to be difficult to erase the memory of …"; tv_2019wimF:0422 4:14:40 "… what a time to string seven points in a row. Facing two championship points …" (points 359-365: Djokovic won the last four of game 16 and the first three of game 17); tv_2019wimF:0426 4:17:15 "… he has saved two championship points the clouds have parted for him the forehand …"; tv_2019wimF:0472 4:43:27 "It's now over half an hour since the first championship points."

### 1.8 The final point (MF T13)
Point 422, clock **4:56:59**, tie-break 6-3 Dj, Federer serving: first serve fault (`6d`), second serve 143 km/h (89 mph) wide, Djokovic backhand return, **Federer forehand unforced error** (R `P2UnfErr`; MCP `5b38f!@`, 3 shots). Distance run Dj 4.6, Fe 4.3. **No TennisVL clip and no commentary exist for this point**; the transcript's last clip is point 413 (1.4c). Nothing after the point (reaction, handshake, ceremony) is in the corpus.

### 1.9 The crowd (transcript; ≤15 words)
tv_2019wimF:0079 0:44:03 "The crowd is really engaging in the match now." · tv_2019wimF:0099 1:05:55 "And I can understand why they're on their feet in the Federer box, because losing …" · tv_2019wimF:0196 2:00:17 "… he'll feel baited by the crowd to a point for the first time …" · tv_2019wimF:0248 2:38:06 "… the world number one, the defending champion, and everyone's cheering for the other guy always." · tv_2019wimF:0277 2:55:08 "… the crowd rise and we have a fifth and deciding …" · tv_2019wimF:0300 3:09:20 "It's where again the crowd can play a part. Can really lift …" · tv_2019wimF:0326 3:23:38 "15, 13. Federer boxers virtually on their feet after every point now." · tv_2019wimF:0328 (video 12280.8 s, no PBP clock; s5 3-2) "Well they're on their feet and Federer began to look like he's a bit out …" · tv_2019wimF:0345 3:31:55 "… Standing ovations everywhere." and "At first the crowd has to relax a little. Please, ladies …" · tv_2019wimF:0427 4:18:51 "Love 15. Federer cannot afford to be as deflated as the crowd seem to be …" · tv_2019wimF:0332 3:25:11 "… the first time I hear the sounds of Nole going through the center court." The transcript never records silence as such (MF T15: 0 clips for quiet/silence).

### 1.10 Commentators, umpire, weather, time of day, rituals
* Co-commentators addressed as **Boris** (18x) and **Tim** (7x); tv_2019wimF:0275 2:52:06 "… the gentleman on my left, Tim Henman"; tv_2019wimF:0032 0:17:23 "I'll get Boris Becker to introduce the full Djokovic camp …". The lead commentator is never named; broadcaster "probably BBC TV" **[unverified]** (MF A, E5).
* Umpire's voice in the transcript: "Please" (0:09:28; 4:08:51; 4:10:58), challenge announcements "Mr. Djokovic is charging the call-up service line. Ball was called in." (tv_2019wimF:0059 0:32:57; ASR for "challenging"), "Mr. Federer has two challenges remaining" (tv_2019wimF:0140 1:28:22; 0263 2:45:27), "Mr. Federer is challenging …" (tv_2019wimF:0466 4:38:36), "Game, Federer. Federer leads by five games to one. Second set." (1:20:36), "Game Djokovic." (3:02:24).
* Weather and light: tv_2019wimF:0124 1:18:38 "Sun came out just for that ball toss."; tv_2019wimF:0200 2:02:19 "… no need for the roof during this championship apart from two …"; tv_2019wimF:0155 1:34:40 "… number one court, which has had the new roof celebrated …"; tv_2019wimF:0373 3:49:23 "… southern end where the sun is getting lower. Not so easy to …"; tv_2019wimF:0426 4:17:15 "the clouds have parted for him" (figurative). No rain, no roof closure, no wind is mentioned.
* Time of day: 14:10 start; "approaching 5 o'clock local time" at 2:46:46; tv_2019wimF:0394 4:00:00 "After six o'clock on the Sunday afternoon."; so the last point fell at about 19:07 local (14:10 + 4:57). **The sun had not set** (the composer must not end with a literal sunset; see 2.6).
* Royal Box and boxes: tv_2019wimF:0155 1:34:40 "… the royal box and Philbrook the chairman …" (ASR; Philip Brook **[unverified]**); tv_2019wimF:0345 3:31:55 "I thought the Royal Box was meant to be impartial."; tv_2019wimF:0387 3:56:54 "i don't speak for the duchess"; tv_2019wimF:0297 3:07:58 "He's becoming quite animated towards his box at the moment."
* New balls (tv_2019wimF:0050, video 1734 s "Novak serving with new balls"; 2:22:20; 3:43:05; 4:22:01), challenges and Hawk-Eye (0:32:57, 0:41:23, 1:28:22 "There we go, one millimetre.", 4:38:36, 4:43:27 "If he's wrong, he loses the point. He is wrong."), fatigue (tv_2019wimF:0341 3:29:35 "Both players are feeling their arms getting heavy."; tv_2019wimF:0444 4:27:58 "His fatigue is cumulative. It's exhausting not watching.").
* Epithets the commentators use (analysis/formulas/results/refexpr_inventory.csv, tokens): Federer — "the great Swiss" 3 (tv_2019wimF:0009 0:04:28; 0209 2:20:29; 0469 4:41:26), "the man from Basel" 1 (0101 1:07:02 "… something magical about the man from Basel in Switzerland."), "the Swiss" 1 (0393 3:59:09), "the older man" 1 (0444 4:27:58 "… both players, but particularly the older man, Boris, has not been extended …"), "Mr Federer" 6, "Roger" 17; Djokovic — "the world number one" 3 (0248 2:38:06; 0328), "the defending champion" 1 (0209 2:20:29), "the top seed" 1 (0045 0:24:21), "the number one seed" 1, "the Serbian" 1 (0284 3:02:24), "the young man" 1 (0162 1:39:58), "the younger man" 1 (0437 4:23:03 "Is it going to be the younger man?"), "Nole" 1 (0332 3:25:11), "Mr Djokovic" 5, "Novak" 29. The bare surname is 127 tokens each.

### 1.11 Ceremony, and what is NOT in the corpus
No clip, transcript or timing exists for: the walk-on, warm-up, **coin toss** (who won it, who chose), the players' kit at entry, the ceremony, trophy presentation, speeches, Djokovic eating grass, the handshake, the crowd's reaction to the last point, attendance, prize money, the Royal Box guests by name, the weather beyond the five mentions above (MF A, T14, T15: trophy/ceremony 0 clips). External pages add only: the duration 4:57, seeds, the records in 1.1, Federer's exact age, and the ATP's "Federer had two championship points at 8-7, 40/15 on serve" (MF E1-E4). Anything else about these scenes must be marked **[unverified]** or omitted. Do not invent: the toss, the order of the warm-up, what the trophy looks like, who presented it, what either player said, the time of sunset.

## 2. Plan for about 50 lines

### 2.0 Line budget (50 lines; the similes are counted inside the sections they interrupt)

| section | lines | content | models (quoted below) |
|---|---|---|---|
| proem | 4 | theme, the two names, "from the point where they first stood apart", Zeus's will | Il. 1.1-7, Od. 1.1-10 (2.1) |
| entry and arming | 7 | the two enter the measured ground; shoes, socks/wristband, racket, strings, towel/cap, the ball as the spear | arming scenes (2.2), Il. 3.315-344 (2.3) |
| set 1 | 4 | no break; tie-break: 5-3 Federer, four points lost | counting formula 3.1; the lot 2.3 |
| set 2 | 3 | three breaks, 6-1; **simile: the horse breaking its tether** (2 of the 3) | 2.5 D |
| set 3 | 3 | the 26-shot rally (2:03:53); tie-break 7-4 | duel formulae 2.3 |
| set 4 | 4 | two breaks, **the 35-shot rally expanded** (2:47:12, 2 lines), broken back, 6-4 | 2.3; simile 2.5 C (rock in the sea) |
| set 5 to 7-7 | 2 | break and break back (3:25:11, 3:31:55); fatigue | 2.5 F (ploughman) |
| the championship game | 4 | 8-7, two aces, **CP1 4:10:58, CP2 4:11:30 expanded**, the break back 4:12:40 | 2.3 cast / hit / miss; 2.4 aristeia opens |
| aristeia (Djokovic) | 4 | the seven points in a row (4:10:58-4:14:40), 9-8, the clouds part; **simile: the lion roused or the Dog Star** | 2.4 |
| 8-8 to 12-12 | 2 | the horses round the posts, the great prize lying there; 11-11 game | 2.5 E; heralds Il. 7.282 |
| the 12-12 tie-break | 4 | **expanded**: scales simile (2.5 A), 4-1, Federer's drop shot (2.5 B hawk and dove, optional), 6-3 | counting formula 3.1 |
| the final point | 1 | second serve, return, forehand error | 2.3; 2.6 |
| ending | 8 | the loser's hope falls, the crowd, the handshake, the prize, the hour of day | 2.6 |

Count corrections to HM found on rerun: HM(c) "οἳ δ᾽ ὅτε δὴ σχεδὸν ἦσαν ἐπ᾽ ἀλλήλοισιν ἰόντες 11x as a whole line" = 10 whole-line hits (each half-line 11x; Il. 6.121 has the dual); HM(d) "ὦκα δ᾽ ἔπειτα 3x" = 4 hits, all 9-12; HM(d) "ἐπειγόμενοι περὶ νίκης 3x" = 2 (Il. 23.437, 23.496; 23.639 has ἀγασσάμενοι περὶ νίκης). Everything else reproduced exactly.

### 2.1 Proem (3-4 lines). Models Il. 1.1-7 and Od. 1.1-10 (HM a; `--ngram` queries rerun):
```
Il. 1.1      μῆνιν ἄειδε θεὰ Πηληϊάδεω Ἀχιλῆος    [DDSDDS; 1-1.5 2-3.5 4-5 6-9 9.5-12]
Il. 1.6      ἐξ οὗ δὴ τὰ πρῶτα διαστήτην ἐρίσαντε    [SSDSDS; 1-1 2-2 3-3 4-4 5-5.5 6-9 9.5-12]
Il. 1.7      Ἀτρεΐδης τε ἄναξ ἀνδρῶν καὶ δῖος Ἀχιλλεύς.    [DDSSDS; 1-3 3.5-3.5 4-5 6-7 8-8 9-9.5 10-12]
Od. 1.1      ἄνδρα μοι ἔννεπε, μοῦσα, πολύτροπον, ὃς μάλα πολλὰ    [DDDDDS; 1-1.5 2-2 3-4 5-5.5 6-8 9-9 9.5-10 11-12]
Od. 1.10     τῶν ἁμόθεν γε, θεά, θύγατερ Διός, εἰπὲ καὶ ἡμῖν.    [DDDDDS; 1-1 1.5-3 3.5-3.5 4-5 5.5-7 7.5-8 9-9.5 10-10 11-12]
```
Invocation formulae with counts and positions: μῆνιν ἄειδε 1x (1-3.5); ἄνδρα μοι ἔννεπε 1x (1-4); ἔννεπε Μοῦσα 2x (Il. 2.761 at 9-12 `τίς τὰρ τῶν ὄχʼ ἄριστος ἔην σύ μοι ἔννεπε Μοῦσα`, Od. 1.1 at 3-5.5); ἔσπετε νῦν μοι Μοῦσαι Ὀλύμπια δώματʼ ἔχουσαι 4x whole line (Il. 2.484, 11.218, 14.508, 16.112), each time opening a catalogue or a "who first" question (Il. 11.219 `ὅς τις δὴ πρῶτος Ἀγαμέμνονος ἀντίον ἦλθεν`); θεὰ θύγατερ Διός 3x, always 4-8; εἰπὲ καὶ ἡμῖν 1x (9-12); Διὸς δʼ ἐτελείετο βουλή 2x (Il. 1.5, Od. 11.297; 6-12); ἐξ οὗ δὴ 2x (1-3; ἐξ οὗ 19x). Skeleton: line 1 = accusative theme at 1-2 (ἔριν? νίκην? — the composer chooses an attested noun) + ἄειδε θεά (2-5) + genitive name at 6-12 on the pattern Πηληϊάδεω Ἀχιλῆος (8x, always 6-12; the tested substitutes Πηληϊάδεω Φεδερῆος / Ζοκοβῆος in 4.1-4.2); line 2 = ἐξ οὗ δὴ τὰ πρῶτα διαστήτην ἐρίσαντε adapted (the two "stood apart in strife" = the first point at 0:00:00, Federer serving); line 3-4 = the theme (two sets each, the fifth to 12-12) closing on Διὸς δʼ ἐτελείετο βουλή. Il. 2.761's τίς τὰρ τῶν ὄχʼ ἄριστος ἔην (ὄχʼ ἄριστος 9x) may frame "which of the two was best" = the commentary's "who will end up with most Grand Slam titles" (tv_2019wimF:0230, 2:29:21).

### 2.2 Entry and arming as a typical scene (6-8 lines). The four arming scenes share these whole lines (HM b; all counts reconfirmed):
```
κνημῖδας μὲν πρῶτα περὶ κνήμῃσιν ἔθηκε        4x: Il. 3.330, 11.17, 16.131, 19.369   [SSDSDS; κνημῖδας LLL at 1-3; verb phrase 1-5.5 + object 6-12]
καλάς, ἀργυρέοισιν ἐπισφυρίοις ἀραρυίας        4x: Il. 3.331, 11.18, 16.132, 19.370   [the expansion line of the greaves]
δεύτερον αὖ θώρηκα περὶ στήθεσσιν ἔδυνε(ν)      4x: Il. 3.332, 11.19, 16.133, 19.371   [θώρηκα LLS at 4-5.5]
ἀμφὶ δʼ ἄρʼ ὤμοισιν βάλετο ξίφος ἀργυρόηλον      4x: Il. 2.45, 3.334, 16.135, 19.372    [ξίφος SS at 7.5-8; half-line 1-8 5x incl. 11.29]
χάλκεον, αὐτὰρ ἔπειτα σάκος μέγα τε στιβαρόν τε   3x: Il. 3.335, 16.136, 19.373
κρατὶ δʼ ἐπʼ ἰφθίμῳ κυνέην εὔτυκτον ἔθηκεν       4x: Il. 3.336, 15.480, 16.137, Od. 22.123   [κυνέην SSL at 5.5-7]
ἵππουριν· δεινὸν δὲ λόφος καθύπερθεν ἔνευεν      5x: Il. 3.337, 11.42, 15.481, 16.138, Od. 22.124
εἵλετο δʼ ἄλκιμον ἔγχος, ὅ οἱ παλάμηφιν ἀρήρει    first half 8x (1-5.5), second half 2x (Il. 3.338, Od. 17.4; 6-12); εἵλετο δʼ ἄλκιμα δοῦρε 3x (Il. 11.43, 16.139, Od. 1.99)
```
The scene is a fixed order greaves → corselet → sword → shield → helmet → spear(s); each item is one line [verb phrase 1-5.5] + [object and epithet 6-12], and expansions follow the item's line (Agamemnon's corselet Il. 11.20-28, his shield 11.32-40 `ἂν δʼ ἕλετʼ ἀμφιβρότην πολυδαίδαλον ἀσπίδα θοῦριν`; the beacon simile for Achilles' shield 19.374-383). Mapping for the tennis arming (the kit at entry is NOT in the corpus, so keep the items generic and brief; HM j lexicon in brackets):

| order | Homeric item, line | tennis object | Homeric word (verified) | status |
|---|---|---|---|---|
| 1 | greaves, κνημῖδας … περὶ κνήμῃσιν | shoes and socks | κνημῖδες (the only leg-wear in the scene) | use the whole line; "shoes" has no better word |
| 2 | corselet, θώρηκα περὶ στήθεσσιν | shirt | θώρηξ, or χιτών (Il. 7.253 `ἀντικρὺ δὲ παραὶ λαπάρην διάμησε χιτῶνα`) | χιτών is the honest word |
| 3 | sword at the shoulders, ξίφος ἀργυρόηλον | the towel over the shoulder, or the racket bag | ξίφος slot SS at 7.5-8 | no equivalent: paraphrase or skip |
| 4 | shield, σάκος μέγα τε στιβαρόν τε | the racket | σάκος / ἀσπίς (what parries the ball), or ῥόπαλον "club" (3x: Od. 9.319, 11.575, 17.195; SSL), κορύνη (Il. 7.141, 7.143) | **choose one and keep it**: the racket as shield (Parry's "defensive" slot) or as the spear's shaft; never both |
| 5 | helmet, κυνέην εὔτυκτον … ἵππουριν … λόφος | cap and headband; the sweatband as the λόφος | κυνέη | the horsehair crest line (5x) can become the cap's peak only if the composer accepts a joke; otherwise omit |
| 6 | spear(s), ἄλκιμον ἔγχος / ἄλκιμα δοῦρε | the serve: the balls in hand | ἔγχος / δόρυ metaphorically; the ball itself is σφαῖρα (σφαίρῃ Od. 6.100, 8.377; σφαῖραν Od. 6.115, 8.372; σφαιρηδόν Il. 13.204) | the cast formulae of 2.3 then narrate the serve; "strings" and "wristband" have no equivalent: omit |

Close the scene with the Patroclus/Ajax line `ὣς ἄρʼ ἔφαν, Αἴας δὲ κορύσσετο νώροπι χαλκῷ` (Il. 7.206; κορύσσετο νώροπι χαλκῷ 2x at 6-12, 7.206 and 16.130), and the entry into the measured ground: Il. 3.315 `χῶρον μὲν πρῶτον διεμέτρεον, αὐτὰρ ἔπειτα` (1x; 1-8) and 3.344 `καί ῥʼ ἐγγὺς στήτην διαμετρητῷ ἐνὶ χώρῳ` (διαμετρητῷ ἐνὶ χώρῳ 1x, 5.5-12; the only Homeric "measured court"). The lot for the serve (coin toss) is in Homer `κλήρους ἐν κυνέῃ χαλκήρεϊ πάλλον ἑλόντες` (Il. 3.316 = 23.861 with δʼ); **but the toss is not in the corpus (1.11): state only that Federer served first (0:00:00).**

### 2.3 The duel set by set (sets 1-4 about 14 lines; set 5 about 10). Formulae of the duel typical scene (HM c) and of the games (HM d), reconfirmed:
* Approach: `οἳ δʼ ὅτε δὴ σχεδὸν ἦσαν ἐπʼ ἀλλήλοισιν ἰόντες` (10x whole line, e.g. Il. 3.15, 5.14, 22.248; first half 11x at 1-5.5, second 11x at 6-12). Spectators' awe: `θάμβος δʼ ἔχεν εἰσορόωντας` (Il. 3.342 = 4.79; 6-12).
* **The serve = the cast**: `ἦ ῥα, καὶ ἀμπεπαλὼν προΐει δολιχόσκιον ἔγχος` (7x whole: Il. 3.355, 5.280, 7.244, 11.349, 17.516, 22.273, 22.289; ἦ ῥα καὶ ἀμπεπαλὼν 8x at 1-5; προΐει δολιχόσκιον ἔγχος 13x at 5.5-12; δολιχόσκιον ἔγχος 25x, 24 at 7.5-12). Second server: `δεύτερος αὖτʼ Ἀχιλεὺς προΐει δολιχόσκιον ἔγχος` (Il. 20.273; δεύτερος αὖτʼ 6x at 1-3). Also `στῆ δὲ μάλʼ ἐγγὺς ἰὼν καὶ ἀκόντισε δουρὶ φαεινῷ` (Il. 4.496, 5.611; ἀκόντισε δουρὶ φαεινῷ 14x at 6-12).
* **The hit**: `καὶ βάλεν` 11x, always 1-2 (Il. 3.347 `καὶ βάλεν Ἀτρεΐδαο κατʼ ἀσπίδα πάντοσε ἴσην`); `καὶ βάλε` 6x (Il. 22.290 `καὶ βάλε Πηλεΐδαο μέσον σάκος οὐδʼ ἀφάμαρτε`). **The winner / ace**: `οὐδʼ ἀφάμαρτε` 4x (Il. 11.350, 13.160 at 3-5.5; 2x at 9-12) and `οὐδʼ ἀφάμαρτεν` 2x (Il. 16.322, 21.591 at 9-12); the ace past every mark `ὁ δʼ ὑπέρπτατο σήματα πάντων` (Od. 8.192; ὑπέρπτατο 4x at 6-8). **The fault**: `ἤμβροτες οὐδʼ ἔτυχες` (Il. 5.287, 1-5; ἤμβροτ- 10x). **The ball through the defence**: the block Il. 3.357-360 = 7.251-254 (`διὰ μὲν ἀσπίδος ἦλθε φαεινῆς ὄβριμον ἔγχος` 3x incl. 11.435; `ἔγχος· ὃ δʼ ἐκλίνθη καὶ ἀλεύατο κῆρα μέλαιναν` for the ball that is just reached). **The retreat / the lob** `ὣς φάτο, Τυδεΐδης δʼ ἀνεχάζετο τυτθὸν ὀπίσσω` (Il. 5.443; τυτθὸν ὀπίσσω 1x, 9-12). **Forehand and backhand**: `οἶδʼ ἐπὶ δεξιά, οἶδʼ ἐπʼ ἀριστερὰ νωμῆσαι βῶν` (Il. 7.238; ἐπʼ ἀριστερά 14x, 10 at 5.5-8; ἐπὶ δεξιά 1x) — the nearest Homeric statement of two-sided skill (Hector's boast).
* **Games**: the start `τοῖσι δʼ ἀπὸ νύσσης τέτατο δρόμος· ὦκα δʼ ἔπειτα` (Il. 23.758 = Od. 8.121, 1-8; ὦκα δʼ ἔπειτα 4x at 9-12), the marking of the course and the umpire `στὰν δὲ μεταστοιχί, σήμηνε δὲ τέρματʼ Ἀχιλλεὺς` (23.358 = 23.757; σήμηνε δὲ τέρματʼ Ἀχιλλεύς 2x at 6-12), `παρὰ δὲ σκοπὸν εἷσεν` (23.359, 7.5-12) … `ὡς μεμνέῳτο δρόμους καὶ ἀληθείην ἀποείποι` (23.361 — the line judge and the challenge); the spectators `Ἀργεῖοι δʼ ἐν ἀγῶνι καθήμενοι εἰσορόωντο` (23.448), `κάππεσε· λαοὶ δʼ αὖ θηεῦντό τε θάμβησάν τε` (23.728 = 23.881), `τοὶ δὲ βόησαν` (17.607, 23.847; 9-12), `ἀτὰρ κελάδησαν Ἀχαιοί` (23.869); both set on victory `νίκης ἱέσθην τρίποδος πέρι ποιητοῖο` (23.718), `ἐπειγόμενοι περὶ νίκης` (23.437, 23.496); the draw/deuce `νίκη δʼ ἀμφοτέροισιν· ἀέθλια δʼ ἶσʼ ἀνελόντες` (23.736), `ὣς μὲν τῶν ἐπὶ ἶσα μάχη τέτατο πτόλεμός τε` (Il. 12.436 = 15.413); divine interference (net cord, bad bounce) `ἔνθʼ Αἴας μὲν ὄλισθε θέων, βλάψεν γὰρ Ἀθήνη` (23.774); the discus/serve `τόν ῥα περιστρέψας ἧκε στιβαρῆς ἀπὸ χειρός, / βόμβησεν δὲ λίθος` (Od. 8.189-190); the handshake at the net Il. 7.299-305 (`δῶρα δʼ ἄγʼ ἀλλήλοισι περικλυτὰ δώομεν ἄμφω`; `ἠμὲν ἐμαρνάσθην ἔριδος πέρι θυμοβόροιο, / ἠδʼ αὖτʼ ἐν φιλότητι διέτμαγεν ἀρθμήσαντε`) and `ἔν τʼ ἄρα οἱ φῦ χειρὶ ἔπος τʼ ἔφατʼ ἔκ τʼ ὀνόμαζε` (first half 10x at 1-5.5, e.g. Il. 6.253, 6.406, 14.232, 18.384).
* **The 12-12 rule** = the heralds stopping Hector and Ajax at nightfall, Il. 7.274-282: `μηκέτι παῖδε φίλω πολεμίζετε μηδὲ μάχεσθον· / … / νὺξ δʼ ἤδη τελέθει· ἀγαθὸν καὶ νυκτὶ πιθέσθαι` (7.282 = 7.293, 2x whole line) and the Achaeans stopping the armed duel `παυσαμένους ἐκέλευσαν ἀέθλια ἶσʼ ἀνελέσθαι` (23.823). Use it for the tie-break at 12-12 as a **simile or as the heralds' decree**, not as a statement that night fell (1.10).

**The three expanded points** (facts and clock in section 1):
1. The 35-shot rally, 2:47:12 (1.5): Federer serving at 5-2, break point down, second serve; 35 shots, 43 s; Federer's backhand winner; then broken at 2:49:12. Two lines: the exchange (ἐπὶ ἶσα … τέτατο; the τρὶς μὲν … τρὶς δὲ counting of 3.1 for the shots) and the ending (οὐδʼ ἀφάμαρτε at 9-12). Commentary "35 shots every one of them right out of the middle yes".
2. The two championship points, 4:10:58 and 4:11:30 (1.7): CP1 = second serve wide, forehand return down the middle, Federer's inside-out forehand wide (the fault/miss formula ἤμβροτες οὐδʼ ἔτυχες or ἐτώσιον ἔκφυγε χειρός, Il. 22.292 = 14.407 `ὅττί ῥά οἱ βέλος ὠκὺ ἐτώσιον ἔκφυγε χειρός`); CP2 = first serve to the T, slice return, Federer's forehand approach, Djokovic's cross-court passing winner (καὶ βάλε … οὐδʼ ἀφάμαρτε; Il. 22.274-275 for the shot that flies past: `καὶ τὸ μὲν ἄντα ἰδὼν ἠλεύατο φαίδιμος Ἕκτωρ· / ἕζετο γὰρ προϊδών, τὸ δʼ ὑπέρπτατο χάλκεον ἔγχος`). Frame both with the "would have … had not" construction `καί νύ κεν … εἰ μὴ` (καί νύ κεν 16x, 1-2; εἰ μὴ 65x; e.g. Il. 3.373-374 `καί νύ κεν εἴρυσσέν τε καὶ ἄσπετον ἤρατο κῦδος, / εἰ μὴ ἄρʼ ὀξὺ νόησε Διὸς θυγάτηρ Ἀφροδίτη`; ἄσπετον ἤρατο κῦδος 2x). Then the break back at 4:12:40: forehand into the net (ἐν … ἕρκεϊ? ἕρκος 21x, 16 at 9-9.5: the net is ἕρκος, HM j).
3. The 12-12 tie-break, 4:48:30-4:56:59 (1.4c): open with the scales (2.5 A), count the points with τρὶς μὲν … / ἀλλʼ ὅτε δὴ τὸ τέταρτον (3.1), give Federer's drop-shot winner at 4:52:04 (hawk and dove, 2.5 B, optional) and Djokovic's two winners at 4:54:18 and 4:54:48, then the last point (2.6).

### 2.4 Aristeia: Djokovic, from the first championship point to 9-8 (4:10:58-4:17:15), with the 12-12 tie-break as its second wave.
Justification from the facts: Djokovic won all three tie-breaks (7-5, 7-4, 7-3; 1.4), saved both championship points and won seven points in a row (points 359-365; tv_2019wimF:0422 4:14:40 "what a time to string seven points in a row"), broke back at 4:12:40 and led 9-8 at 4:17:15 ("the clouds have parted for him"); he won the fifth set 85-84 on points. Federer's aristeia is the earlier one of the loser (Patroclus, Hector): set 2 at 1:00:23-1:22:54 (three breaks, 26-12 on points, winners 9-2) and the break for 8-7 at 4:07:16 — give it two lines with the horse simile (2.5 D) and let it be remembered at the end. Markers (HM f, reconfirmed):
```
Il. 5.1      ἔνθʼ αὖ Τυδεΐδῃ Διομήδεϊ Παλλὰς Ἀθήνη
Il. 5.2      δῶκε μένος καὶ θάρσος, ἵνʼ ἔκδηλος μετὰ πᾶσιν        μένος καὶ θάρσος 2x (= Od. 1.321), 2-5.5
Il. 5.4      δαῖέ οἱ ἐκ κόρυθός τε καὶ ἀσπίδος ἀκάματον πῦρ        ἀκάματον πῦρ 9x, always 9-12
Il. 5.5      ἀστέρʼ ὀπωρινῷ ἐναλίγκιον, ὅς τε μάλιστα              1x, 1-8 (the autumn star returns for Achilles, Il. 22.26-32)
Il. 5.7      τοῖόν οἱ πῦρ δαῖεν ἀπὸ κρατός τε καὶ ὤμων            1x
Il. 16.130   ὣς φάτο, Πάτροκλος δὲ κορύσσετο νώροπι χαλκῷ.
Il. 18.206   χρύσεον, ἐκ δʼ αὐτοῦ δαῖε φλόγα παμφανόωσαν.
Il. 2.451    ὀτρύνουσʼ ἰέναι· ἐν δὲ σθένος ὦρσεν ἑκάστῳ            ἐν δὲ σθένος ὦρσεν ἑκάστῳ 1x, 6-12
```
The catalogue opener for a run of points: `ἔνθα τίνα πρῶτον τίνα δʼ ὕστατον ἐξενάριξαν` (Il. 5.703; the 1-8 frame 3x: 5.703, 11.299 -εν, 16.692 -ας; ἔνθα τίνα πρῶτον 4x at 1-5; ἐξενάριξε 15x). A test adaptation passed check_line with no flags: `ἔνθα τίνα πρῶτον τίνα δ᾽ ὕστατον ἐξενάριξε` (DSDDDS). The "fourth onset" line is the aristeia's climax formula: `ἀλλʼ ὅτε δὴ τὸ τέταρτον ἐπέσσυτο δαίμονι ἶσος` (Il. 5.438 = 16.705 = 16.786 = 20.447; δαίμονι ἶσος 9x at 9-12) — use it for the fourth point of the championship game (the break, 4:12:40) or for the fourth game of the run.

### 2.5 Similes: at least two extended ones in the poem; six candidates, each quoted in full (HM e; all reconfirmed by `--ngram` on the first line and on the key phrases). Openers ὡς δʼ ὅτε 29x and ὡς δʼ ὅτε τις 10x (1-3), ἠΰτε 31x (20 at 9-10); closers ὣς οἳ μὲν 50x (1-3), ὣς τοῦ 9x.

**A. The golden scales of Zeus → the 12-12 tie-break at 4:48:30** (two whole lines shared by Il. 8.69-70 and 22.209-210):
```
Il. 22.209   καὶ τότε δὴ χρύσεια πατὴρ ἐτίταινε τάλαντα,    [DSDDDS]   = Il. 8.69
Il. 22.210   ἐν δʼ ἐτίθει δύο κῆρε τανηλεγέος θανάτοιο,     [DDDDDS]   = Il. 8.70
Il. 22.211   τὴν μὲν Ἀχιλλῆος, τὴν δʼ Ἕκτορος ἱπποδάμοιο,
Il. 22.212   ἕλκε δὲ μέσσα λαβών· ῥέπε δʼ Ἕκτορος αἴσιμον ἦμαρ,    (ἕλκε δὲ μέσσα λαβών 2x, 1-5)
Il. 22.213   ᾤχετο δʼ εἰς Ἀΐδαο, λίπεν δέ ἑ Φοῖβος Ἀπόλλων.
```
Replace κῆρε … θανάτοιο by the two νίκαι or ἄεθλα (the composer must find an attested genitive of the same shape: τανηλεγέος θανάτοιο is SLSSL SSLX); the genitives Φεδερῆος / Ζοκοβῆος do NOT fit the slot of Ἀχιλλῆος at 3-5.5 (check_line fails: `τὴν μὲν Φεδερῆος, τὴν δʼ Ἕκτορος ἱπποδάμοιο` needs two unattested licences), so name the two by epithet or ethnic there (Σέρβου, Ἑλβετίου: verify the shape).

**B. Hawk and dove → the chase to a drop shot** (Federer's drop-shot winner at 4:52:04, point 418; or Djokovic's drop shot at 2:33:40, tv_2019wimF:0242 "a drop shot? Great shot from Djokovic"):
```
Il. 22.139   ἠΰτε κίρκος ὄρεσφιν ἐλαφρότατος πετεηνῶν
Il. 22.140   ῥηϊδίως οἴμησε μετὰ τρήρωνα πέλειαν,
Il. 22.141   ἣ δέ θʼ ὕπαιθα φοβεῖται, ὃ δʼ ἐγγύθεν ὀξὺ λεληκὼς
Il. 22.142   ταρφέʼ ἐπαΐσσει, ἑλέειν τέ ἑ θυμὸς ἀνώγει·
```
**C. The rock in the sea / the wave on the shore → Federer's attack on Djokovic's defence** (Federer 23 net points in set 5, 18 won; Djokovic the rock):
```
Il. 15.618   ἴσχον γὰρ πυργηδὸν ἀρηρότες, ἠΰτε πέτρη        (ἠΰτε πέτρη 2x, 9-12)
Il. 15.619   ἠλίβατος μεγάλη πολιῆς ἁλὸς ἐγγὺς ἐοῦσα,
Il. 15.620   ἥ τε μένει λιγέων ἀνέμων λαιψηρὰ κέλευθα
Il. 15.621   κύματά τε τροφόεντα, τά τε προσερεύγεται αὐτήν·
Il. 4.422    ὡς δʼ ὅτʼ ἐν αἰγιαλῷ πολυηχέϊ κῦμα θαλάσσης
Il. 4.423    ὄρνυτʼ ἐπασσύτερον Ζεφύρου ὕπο κινήσαντος·
Il. 4.424    πόντῳ μέν τε πρῶτα κορύσσεται, αὐτὰρ ἔπειτα
Il. 4.425    χέρσῳ ῥηγνύμενον μεγάλα βρέμει, ἀμφὶ δέ τʼ ἄκρας
Il. 4.426    κυρτὸν ἐὸν κορυφοῦται, ἀποπτύει δʼ ἁλὸς ἄχνην·
```
**D. The stalled horse breaking its tether → Federer's second set** (six lines identical at Il. 6.506-511 = 15.263-268):
```
Il. 6.506    ὡς δʼ ὅτε τις στατὸς ἵππος ἀκοστήσας ἐπὶ φάτνῃ
Il. 6.507    δεσμὸν ἀπορρήξας θείῃ πεδίοιο κροαίνων
Il. 6.508    εἰωθὼς λούεσθαι ἐϋρρεῖος ποταμοῖο
Il. 6.509    κυδιόων· ὑψοῦ δὲ κάρη ἔχει, ἀμφὶ δὲ χαῖται
Il. 6.510    ὤμοις ἀΐσσονται· ὃ δʼ ἀγλαΐηφι πεποιθὼς
Il. 6.511    ῥίμφά ἑ γοῦνα φέρει μετά τʼ ἤθεα καὶ νομὸν ἵππων·
```
**E. The prize-winning horses round the turning posts, the great prize lying there → the fifth set from 8-8 to 12-12** (and 2.3 for the τέρματα):
```
Il. 22.162   ὡς δʼ ὅτʼ ἀεθλοφόροι περὶ τέρματα μώνυχες ἵπποι
Il. 22.163   ῥίμφα μάλα τρωχῶσι· τὸ δὲ μέγα κεῖται ἄεθλον        (τὸ δὲ μέγα κεῖται ἄεθλον 1x, 6-12)
Il. 22.164   ἢ τρίπος ἠὲ γυνὴ ἀνδρὸς κατατεθνηῶτος·
Il. 22.165   ὣς τὼ τρὶς Πριάμοιο πόλιν πέρι δινηθήτην
Il. 22.166   καρπαλίμοισι πόδεσσι· θεοὶ δʼ ἐς πάντες ὁρῶντο·
```
**F. The ploughman longing for sunset → the fatigue of the fifth set** (tv_2019wimF:0341 3:29:35 "Both players are feeling their arms getting heavy."; tv_2019wimF:0444 4:27:58 "His fatigue is cumulative."):
```
Od. 13.31    ὡς δʼ ὅτʼ ἀνὴρ δόρποιο λιλαίεται, ᾧ τε πανῆμαρ
Od. 13.32    νειὸν ἀνʼ ἕλκητον βόε οἴνοπε πηκτὸν ἄροτρον·
Od. 13.33    ἀσπασίως δʼ ἄρα τῷ κατέδυ φάος ἠελίοιο
Od. 13.34    δόρπον ἐποίχεσθαι, βλάβεται δέ τε γούνατʼ ἰόντι·
Od. 13.35    ὣς Ὀδυσῆʼ ἀσπαστὸν ἔδυ φάος ἠελίοιο.
```
Further candidates with the moment each fits: the two men with measuring rods disputing a boundary → deuce and the 14-point game at 11-11 (Il. 12.421-423 `ἀλλʼ ὥς τʼ ἀμφʼ οὔροισι δύʼ ἀνέρε δηριάασθον / μέτρʼ ἐν χερσὶν ἔχοντες ἐπιξύνῳ ἐν ἀρούρῃ, / ὥ τʼ ὀλίγῳ ἐνὶ χώρῳ ἐρίζητον περὶ ἴσης`); the lion roused, lashing its flanks → the aristeia's opening (Il. 20.164-173 `Πηλεΐδης δʼ ἑτέρωθεν ἐναντίον ὦρτο λέων ὣς`; ἐναντίον ὦρτο 3x, λέων ὣς 4x; the tested `Σέρβος δ᾽ αὖθ᾽ ἑτέρωθεν ἐναντίον ὦρτο λέων ὣς` passes with no flags, 4.2); the lion and boar at one spring → two men, one trophy (Il. 16.823-826 `… πίδακος ἀμφʼ ὀλίγης· ἐθέλουσι δὲ πιέμεν ἄμφω`); the Dog Star → the winner's shining (Il. 22.26-32). Fatigue vocabulary (reconfirmed): κάματος 7x nom. (3.5-5 or 5.5-7), καμάτῳ 14x, `φίλα γυῖα λέλυνται` 2x at 7.5-12 (Od. 8.233, 18.242), `λῦσε δὲ γυῖα` 7x at 9-12, ἱδρώς 11x nom. (`κατὰ δὲ νότιος ῥέεν ἱδρώς` Il. 11.811 = 23.715), `πολὺς δʼ ἀνεκήκιεν ἱδρὼς` (23.507 — the winning driver stepping down).

### 2.6 The ending (8 lines)
1. The final point (1.8): second serve (δεύτερον αὖτʼ … προΐει), the return (καὶ βάλε), the forehand that misses: `ἤμβροτες οὐδʼ ἔτυχες` (Il. 5.287) or `ἐτώσιον ἔκφυγε χειρός` (Il. 14.407 = 22.292). No commentary exists: the poem's own voice carries it.
2. The fall of the loser's hope: `ἔλπετο θυμῷ` 3x at 9-12 (Il. 17.404 `… τό μιν οὔ ποτε ἔλπετο θυμῷ`, 17.603, Od. 3.275), `μάλα δέ σφισιν ἔλπετο θυμὸς` 3x (Il. 17.234, 17.395, 17.495), `ἐέλπετο νίκην` (Il. 13.609), `νήπιος, οὐδὲ …` 6x at 1-3.5 (Il. 2.38 `νήπιος, οὐδὲ τὰ ᾔδη ἅ ῥα Ζεὺς μήδετο ἔργα`; 20.466 `… ὃ οὐ πείσεσθαι ἔμελλεν`), `οὐδʼ ἄρʼ ἔμελλε` 2x; the scales' `ῥέπε δʼ … αἴσιμον ἦμαρ` (2.5 A). Keep the loser alive: no ψυχή-leaving formula.
3. The crowd: `ἐπὶ δὲ στενάχοντο` 6x (5.5-9.5; Il. 19.301 `… ἐπὶ δὲ στενάχοντο γυναῖκες`), `ἀκὴν ἐγένοντο σιωπῇ` 16x (6-12; the whole line ὣς ἔφαθʼ, οἳ δʼ ἄρα πάντες ἀκὴν ἐγένοντο σιωπῇ 15x), `ἐπίαχον` 5x (6-8; `ὣς ἔφαθʼ, οἳ δʼ ἄρα πάντες ἐπίαχον υἷες Ἀχαιῶν` Il. 7.403 = 9.50), `Ἀργεῖοι δὲ μέγʼ ἴαχον` 2x, `χεῖρας ἀνέσχον` 4x at 9-12 (`λαοὶ δʼ ἠρήσαντο, θεοῖσι δὲ χεῖρας ἀνέσχον` Il. 3.318 = 7.177 — the crowd's hands up), `θηεῦντό τε θάμβησάν τε` (23.728 = 23.881). The corpus has no reaction to the last point (1.11): use the generic lines, not a described gesture.
4. The handshake: `ἔν τʼ ἄρα οἱ φῦ χειρὶ ἔπος τʼ ἔφατʼ ἔκ τʼ ὀνόμαζε` (10x) and Il. 7.301-302 (2.3); nothing said by either player may be quoted (none exists in the corpus).
5. The prize: `ἴφθιμος Σθένελος, ἀλλʼ ἐσσυμένως λάβʼ ἄεθλον` (Il. 23.511; λάβʼ ἄεθλον 1x, 9.5-12); `ὣς εἰπὼν ἐν χερσὶ τίθει, ὃ δʼ ἐδέξατο χαίρων` (Il. 23.797 = 23.624; Od. 15.130 with εἰποῦσʼ; ἐδέξατο χαίρων 3x at 7.5-12; Il. 1.446 ὃ δὲ δέξατο χαίρων); `δέπας ἀμφικύπελλον` 11x at 7.5-12 (`χρύσεον δέπας ἀμφικύπελλον` Il. 6.220) for the gold trophy; ἄεθλον 22x at 10-12; `Ζεὺς κῦδος ἔδωκε` (κῦδος ἔδωκε 3x at 9-12: Il. 8.216, 18.456, 19.414); `ὅτε οἱ Ζεὺς κῦδος ἔδωκε` is the second half of `Ἕκτωρ Πριαμίδης, ὅτε οἱ Ζεὺς κῦδος ἔδωκε` (Il. 8.216 = 11.300), whose first half takes Σέρβος (4.2). Note Il. 23.785-797 (Antilochus' prize, "the gods honour older men", `Αἴας μὲν γὰρ ἐμεῖʼ ὀλίγον προγενέστερός ἐστιν`) for the older man's consolation.
6. The hour. The match began at 14:10 and ended about 19:07 in July; the transcript has "sun is getting lower" at 3:49:23 and "after six o'clock" at 4:00:00 (1.10). Homer has no hours (ὥρη 18x = season, never 'hour'), so the clock 4:56:59 goes into the jsonl record of the last line, and the verse marks time by the sun's station: start `ἦμος δʼ Ἠέλιος μέσον οὐρανὸν ἀμφιβεβήκει` (Il. 8.68 = Od. 4.400; the phrase 3x with 16.777), the long afternoon `ὄφρα μὲν ἠὼς ἦν καὶ ἀέξετο ἱερὸν ἦμαρ` (3x: Il. 8.66, 11.84, Od. 9.56) → `ἦμος δʼ Ἠέλιος μετενίσετο βουλυτὸν δέ` (Il. 16.779; Od. 9.58 βουλυτόνδε), the low sun `δείελον ἦμαρ` (Od. 17.606, 9-12), `ὀψὲ δὲ δὴ` 12x (1-3) for "late at last". **Do not use** `δύσετό τʼ ἠέλιος σκιόωντό τε πᾶσαι ἀγυιαί` (7x) or `ἐν δʼ ἔπεσʼ Ὠκεανῷ λαμπρὸν φάος ἠελίοιο` (Il. 8.485) as a statement: the sun had not set. They may appear inside a simile (2.5 F) or as the loser's "day" (`ῥέπε δʼ Ἕκτορος αἴσιμον ἦμαρ`).
7-8. Close with a "so they …" line (ὣς οἳ μὲν 50x) and the longest-final fact as a numberless superlative (δηρόν 47x; `δηρὸν` for the length; the record itself, 1.1, belongs to the jsonl note).

### 2.7 Enjambment
Vary Parry's three types across the poem and record each line's type in the jsonl: no enjambment (sentence ends with the verse), unperiodic (the sense is complete at verse end but the sentence continues, e.g. Il. 1.1-2, 2.2 lines ending on an adjective + expansion), necessary (the verse ends inside a syntactic unit, e.g. Il. 22.211-212). Source for the classification: Parry, M. 1929. "The Distinctive Character of Enjambement in Homeric Verse", TAPA 60: 200-220, DOI 10.2307/282817 (Crossref record fetched 2026-10-07; the three-type summary above is from memory of that paper and is **[unverified against its text]**); the later typology: Higbie, C. 1990. Measure and Music: Enjambement and Sentence Structure in the Iliad, Oxford, DOI 10.1093/oso/9780198143871.001.0001 (Crossref record fetched; contents **[unverified]**); Kirk 1966 **[unverified, no record found]**. Target: roughly a third of the 50 lines with necessary enjambment, the proem and the arming scene mostly end-stopped (as their models), the rallies and the championship game run-on.

## 3. The ten most frequent commentary formulae or systems, paired with Homeric functional equivalents

Sources: `analysis/formulas/results/top10_for_brief_n3.csv` (formulas of n ≥ 3 and systems with ≥ 2 fixed tokens; counts = distinct utterances / occurrences in the 2019 transcript), `top10_for_brief.csv` and `systems_2019.tsv` (the n ≥ 2 lists, dominated by score calls), `analysis/formulas/report.md` section 7. "pool" = number of the 18 other TV streams in which the item is also attested. Every Homeric item was found with `homer/concordance.py` (query in backticks). **Rule for the composer: use the Homeric equivalent wherever the commentators used theirs** — every score change inside a narrated point gets a counting formula (3.1), every game or set won gets a prize/victory formula (3.2), every "leads by" a race-position line (3.3), and so on; record the pairing in the jsonl `commentary_equivalent` field.

**3.1 The score-call frame `<NUM> 15` / `15 <NUM>` / `40 <NUM>` / `30 <NUM>` / `<NUM> love`** — 40/36, 30/29, 28/22, 19/19, 19/15 occurrences/utterances; fillers 40, 30, love, 0 (and ASR 13, 14 for 30, 40); pool 16-17; spoken in the dead time after a point (median 25-30 s to the next serve), pressure share 0-14%; the systems are the umpire's calls repeated by the commentator. ↔ **The counting formula** `τρὶς μὲν … τρὶς δὲ …` and **the fourth-time climax** (`--ngram "τρὶς μὲν"` 15x, all 1-2; `--ngram "τρὶς δὲ"` 8x; `--ngram "τρὶς δ᾽"` 9x; `--ngram "ἀλλ᾽ ὅτε δὴ τὸ τέταρτον"` 5x, all 1-5.5; `--ngram "τὸ δὲ τέτρατον"` 2x at 5.5-8; `πέμπτον` 2x):
```
Il. 5.436    τρὶς μὲν ἔπειτʼ ἐπόρουσε κατακτάμεναι μενεαίνων,      (τρὶς μὲν ἔπειτʼ ἐπόρουσε 3x: 5.436, 16.784, 20.445)
Il. 5.437    τρὶς δέ οἱ ἐστυφέλιξε φαεινὴν ἀσπίδʼ Ἀπόλλων·
Il. 5.438    ἀλλʼ ὅτε δὴ τὸ τέταρτον ἐπέσσυτο δαίμονι ἶσος,         = 16.705, 16.786, 20.447; 22.208 … ἐπὶ κρουνοὺς ἀφίκοντο
Il. 13.20    τρὶς μὲν ὀρέξατʼ ἰών, τὸ δὲ τέτρατον ἵκετο τέκμωρ
Il. 21.176   τρὶς μέν μιν πελέμιξεν ἐρύσσασθαι μενεαίνων,          = Od. 21.125
Il. 21.177   τρὶς δὲ μεθῆκε βίης· τὸ δὲ τέτρατον ἤθελε θυμῷ
Il. 23.817   τρὶς μὲν ἐπήϊξαν, τρὶς δὲ σχεδὸν ὁρμήθησαν.           (the armed duel of the games: both counts in one line)
Od. 9.361    τρὶς μὲν ἔδωκα φέρων, τρὶς δʼ ἔκπιεν ἀφραδίῃσιν.
Od. 12.105   τρὶς μὲν γάρ τʼ ἀνίησιν ἐπʼ ἤματι, τρὶς δʼ ἀναροιβδεῖ
Il. 23.615   τέτρατος, ὡς ἔλασεν. πέμπτον δʼ ὑπελείπετʼ ἄεθλον,     (πέμπτον δʼ ὑπελείπετʼ ἄεθλον 1x, 6-12: "the fifth prize was left")
```
Use: a game is four points, so τρὶς μὲν … τρὶς δὲ … ἀλλʼ ὅτε δὴ τὸ τέταρτον is the natural scansion of 40-x; the 12-12 tie-break (7-3) and the first tie-break (Federer 5-3 then 7-5) take τρὶς … τρὶς … and the fourth-time line for the decisive point. A note on arithmetic honesty: the numbers in the formula must match the point sequence in 1.4 and 1.7 (e.g. CP1 came at 40-15 after two aces: "twice he cast and twice he did not miss" is the correct count).

**3.2 `game <NAME>`** — 9/9 (djokovic 7, federer 2; pool 9), the umpire's announcement at the end of a game, e.g. tv_2019wimF:0129 1:20:36 "Game, Federer. Federer leads by five games to one. Second set."; tv_2019wimF:0284 3:02:24 "Game Djokovic. Important hole for the Serbian." ↔ **The prize-award and victory announcements of Il. 23** (HM d): `θῆκεν ἄεθλα` 2x at 9-12 (`Πηλεΐδης δʼ αἶψʼ ἄλλα κατὰ τρίτα θῆκεν ἄεθλα` 23.700); `λάβʼ ἄεθλον` (23.511, 9.5-12); `δῶκε δʼ ἄγειν` 2x at 1-3 (23.512); `ὣς εἰπὼν ἐν χερσὶ τίθει, ὃ δʼ ἐδέξατο χαίρων` (23.624, 23.797); `νίκη δʼ ἀμφοτέροισιν` (23.736, 1-5.5) for deuce; `κῦδος ἔδωκε` 3x at 9-12; `ἄσπετον ἤρατο κῦδος` 2x (Il. 3.373 = 18.165, 7-12); `ἐξενάριξε` 15x (9-12 or 3-5.5) for "broke". Every game won in the narrated stretches = one of these at line end; a break of serve = ἐξενάριξε or ἤρατο κῦδος.

**3.3 `<NAME> leads by` / `by <_> games to` / `by <_> games`** — 7/7, 9/9, 9/9 (fillers two 3, four 2, six, five, three; pool 4-7; 78% of the "by <_> games to" occurrences fall inside the umpire's official call pattern), e.g. tv_2019wimF:0321 3:20:54 "Djokovic leads by three games to two, final set."; tv_2019wimF:0474 4:44:50 "Djokovic leads by 12, gains to 11. Fifth set." ↔ **The race-position lines of the chariot race and footrace** (`--ngram "ἀλλ᾽ ὅτε δὴ πύματον τέλεον δρόμον"` 2x at 1-8; `--ngram "ὄπιθεν δὲ"` 5x, all 3.5-5.5; `--loose "παρελα"` 3x; `--ngram "λείπετ᾽"` 3x; `ἔκφερ᾽` 3x; `ἔκφερον ὠκέες ἵπποι` Il. 16.383 = 16.866 at 7-12):
```
Il. 23.373   ἀλλʼ ὅτε δὴ πύματον τέλεον δρόμον ὠκέες ἵπποι          = 23.768 … δρόμον, αὐτίκʼ Ὀδυσσεὺς (the footrace)
Il. 23.374   ἂψ ἐφʼ ἁλὸς πολιῆς, τότε δὴ ἀρετή γε ἑκάστου
Il. 23.375   φαίνετʼ, ἄφαρ δʼ ἵπποισι τάθη δρόμος· ὦκα δʼ ἔπειτα
Il. 23.379   αἰεὶ γὰρ δίφρου ἐπιβησομένοισιν ἐΐκτην,                 (the pursuer "always seemed about to mount the car in front")
Il. 23.382   καί νύ κεν ἢ παρέλασσʼ ἢ ἀμφήριστον ἔθηκεν,             (= 23.527 τώ κέν μιν παρέλασσʼ οὐδʼ ἀμφήριστον ἔθηκεν: "he would have passed him or made it a dead heat")
Il. 23.499   ὣς φάτο, Τυδεΐδης δὲ μάλα σχεδὸν ἦλθε διώκων,
Il. 23.504   ἵπποις ὠκυπόδεσσιν ἐπέτρεχον· οὐδέ τι πολλὴ
Il. 23.505   γίγνετʼ ἐπισσώτρων ἁρματροχιὴ κατόπισθεν                 (the gap behind the leader)
Il. 23.523   λείπετʼ· ἀτὰρ τὰ πρῶτα καὶ ἐς δίσκουρα λέλειπτο,          (23.529 λείπετʼ ἀγακλῆος Μενελάου δουρὸς ἐρωήν: "a spear-cast behind")
Il. 23.759   ἔκφερʼ Ὀϊλιάδης· ἐπὶ δʼ ὄρνυτο δῖος Ὀδυσσεὺς
Il. 23.785   Ἀντίλοχος δʼ ἄρα δὴ λοισθήϊον ἔκφερʼ ἄεθλον
Il. 6.181    πρόσθε λέων, ὄπιθεν δὲ δράκων, μέσση δὲ χίμαιρα,          (πρόσθε 25x; ὄπισθεν 22x)
Il. 5.443    ὣς φάτο, Τυδεΐδης δʼ ἀνεχάζετο τυτθὸν ὀπίσσω             (a game behind = τυτθὸν ὀπίσσω)
```
Use: a lead of one game = λείπετʼ … δουρὸς ἐρωήν / τυτθὸν ὀπίσσω; a level score = ἀμφήριστον ἔθηκεν or ἐπὶ ἶσα … τέτατο (2.3); the last game before a set = ἀλλʼ ὅτε δὴ πύματον τέλεον δρόμον.

**3.4 `the <_> set` / `in the <_> set` / `the first set`** — 27/21 (first 10, fifth 7, second 6, fourth 2, third 1, final 1; pool 17), 9/9, 10/8. ↔ **Ordinal-slot formulae**: `πρῶτος` 55x (`πρῶτος δʼ` 5x at 1-3, e.g. Il. 23.450 `πρῶτος δʼ Ἰδομενεὺς Κρητῶν ἀγὸς ἐφράσαθʼ ἵππους`; `τὰ πρῶτα` as in Il. 1.6 and 23.538 `δεύτερʼ· ἀτὰρ τὰ πρῶτα φερέσθω Τυδέος υἱός`); `δεύτερος` 12x (`δεύτερος αὖτʼ` 6x at 1-3; `δεύτερος αὖτε` 23.248 at 9-12); `τρίτος` 5x, `τρίτατος` 3x (5.5-7 or 3.5-5: `τοῖσι δʼ ἅμʼ Εὐρύαλος τρίτατος κίεν ἰσόθεος φὼς` Il. 2.565), `τὸ τρίτον αὖτʼ` (Il. 3.225, 23.842); `τέταρτος` 1x (Il. 23.301 `Ἀντίλοχος δὲ τέταρτος ἐΰτριχας ὁπλίσαθʼ ἵππους`), `τὸ τέταρτον` 6x; `πέμπτος` 2x (Il. 23.351 `Μηριόνης δʼ ἄρα πέμπτος ἐΰτριχας ὁπλίσαθʼ ἵππους`; Od. 9.335), `πέμπτον` 2x (Il. 23.615; Od. 24.309 `αὐτὰρ Ὀδυσσῆϊ τόδε δὴ πέμπτον ἔτος ἐστίν`); `ὕστατος` 3x (Il. 23.356 `… ὕστατος αὖτε`, 9-10), `ὕστατον` 7x (7-8), and the catalogue question `ἔνθα τίνα πρῶτον τίνα δʼ ὕστατον ἐξενάριξαν` (3x; 2.4). Use: each set opens with its ordinal in the Il. 23.301/23.351 pattern (the drivers harnessing in order) and the fifth with Od. 24.309 / Il. 23.615; the set the commentators call "final" (fifth 7 + final 1) takes πύματον or ὕστατον.

**3.5 `in <_> fifth`** — 9/9 (the 6, this 3; pool 4; 44% at pressure points, the highest of the ten), e.g. "good hold every hold a good hold in the fifth" (systems_2019.tsv row 19). ↔ `πέμπτον δʼ ὑπελείπετʼ ἄεθλον` (Il. 23.615), `τόδε δὴ πέμπτον ἔτος ἐστίν` (Od. 24.309), and for the fifth set's endlessness the heralds' night, `νὺξ δʼ ἤδη τελέθει· ἀγαθὸν καὶ νυκτὶ πιθέσθαι` (Il. 7.282 = 7.293) and `τὸ δὲ μέγα κεῖται ἄεθλον` (Il. 22.163). Use once at 3:00:13 (the set's first point) and once at the 12-12 rule.

**3.6 `a little bit` / `a little`** — 15/14 and 24/22 (pool 18 of 18: the most widely shared formula), the commentators' hedge in evaluations: tv_2019wimF:0294 3:06:34 "… a little bit more proactive, a little bit more aggressive on the baseline."; tv_2019wimF:0403 4:04:05 "A little bit louder from the call on the baseline there."; tv_2019wimF:0227 2:27:24 "Boris, it may be a little bit vulgar …". ↔ **τυτθόν / ὀλίγον / οὐδʼ ἠβαιόν** (`--loose "τυτθον" --word` 29x, 9-9.5 the commonest slot, e.g. Il. 1.354 `… νῦν δʼ οὐδέ με τυτθὸν ἔτισεν`, 5.443 `τυτθὸν ὀπίσσω`; also 1-1.5 Il. 7.334, 10.345; `--loose "ολιγον" --word` 20x, e.g. Il. 11.391 `… καὶ εἴ κʼ ὀλίγον περ ἐπαύρῃ`, 23.789 `Αἴας μὲν γὰρ ἐμεῖʼ ὀλίγον προγενέστερός ἐστιν`; `--ngram "οὐδ᾽ ἠβαιόν"` 6x, all 9-12, e.g. Il. 2.380 `Τρωσὶν ἀνάβλησις κακοῦ ἔσσεται οὐδʼ ἠβαιόν`; ἠβαιόν 7x at 10-12). Use τυτθόν at 9-9.5 for the "little" margins (the ball out by one millimetre at 1:28:22; the break of serve "a little behind"), οὐδʼ ἠβαιόν at line end for "not a bit" (Federer "cannot afford to be as deflated", 4:18:51).

**3.7 `the <_> serve` / `the <_> shot`** — 8/8 (first 3, great, federer, body, previous, second; pool 17) and 8/8 (drop 3, right 2, second, approach, passing; pool 15), e.g. tv_2019wimF:0026 0:14:22 "Body serve. Into Roger."; tv_2019wimF:0329 3:24:39 "Second serve, middle of the box. 95 miles an hour isn't …". ↔ **The spear-cast lines** (2.3): `ἦ ῥα, καὶ ἀμπεπαλὼν προΐει δολιχόσκιον ἔγχος` (7x whole; 13x second half at 5.5-12), `δεύτερος αὖτʼ Ἀχιλεὺς προΐει δολιχόσκιον ἔγχος` (Il. 20.273; "second serve" = δεύτερος αὖτʼ … προΐει), `καὶ βάλεν` 11x at 1-2, `οὐδʼ ἀφάμαρτε(ν)` 4x + 2x, `ἀκόντισε δουρὶ φαεινῷ` 14x at 6-12, `ἔγχεϊ χαλκείῳ` 7x at 1-5, the fault `ἤμβροτες οὐδʼ ἔτυχες` (Il. 5.287), the serve speed by the discus `τόν ῥα περιστρέψας ἧκε στιβαρῆς ἀπὸ χειρός, / βόμβησεν δὲ λίθος` (Od. 8.189-190), the shot types by direction `ἐπὶ δεξιά … ἐπʼ ἀριστερά` (Il. 7.238), the drop shot by the hawk (2.5 B), the passing shot by `τὸ δʼ ὑπέρπτατο χάλκεον ἔγχος` (Il. 22.275 = 13.408), the approach shot by `ὁ δʼ ἐγγύθεν` (ἐγγύθεν 42x; `στῆ δὲ μάλʼ ἐγγὺς ἰὼν` Il. 4.496). Use: every serve in a narrated point is a προΐει line or its half-line; each named shot type in 1.4/1.7 maps to one of these.

**3.8 Name + verb frames `djokovic <_> the` / `federer <_> to` / `djokovic <_> to` / `federer <_> the`** — 11/11 (finding 2, had 2, down, certainly, perhaps, in, breaks, flashed), 10/10 (looking 3, going, trying, able, yet, began, likes, again), 8/8, 8/8; pool 0-4 (these are match-specific, 20-38% at pressure points), e.g. tv_2019wimF:0021 0:11:54 "The Djokovic down the line backhand doesn't achieve the right length …"; systems row 14 "proactive from federer looking to dictate"; tv_2019wimF:0426 4:17:15 "Djokovic finding the mark just when he needed to". ↔ **The name-epithet + verb speech and action frames** (HM h; `--ngram` counts): `τὸν δʼ ἀπαμειβόμενος προσέφη …` 55x (1-7, name-epithet at 7.5-12: πόδας ὠκὺς Ἀχιλλεύς, κρείων Ἀγαμέμνων, κορυθαίολος Ἕκτωρ, πολύμητις Ὀδυσσεύς); `τὸν δʼ ἠμείβετʼ ἔπειτα …` 55x (1-5.5, name-epithet at 6-12: ποδάρκης δῖος Ἀχιλλεύς, βοῶπις πότνια Ἥρη); `τὸν δʼ αὖτε προσέειπε …` 68x; `ὣς φάτο, τὸν δʼ οὔ τι προσέφη κρατερὸς Διομήδης` (Il. 4.401); action frames `Πηλεΐδης δʼ ἑτέρωθεν ἐναντίον ὦρτο λέων ὣς` (Il. 20.164), `ὣς φάτο, Τυδεΐδης δʼ ἀνεχάζετο τυτθὸν ὀπίσσω` (5.443), `ὣς μεμαὼς Τρώεσσι μίγη κρατερὸς Διομήδης` (5.143), `ἀλλά σφεας κρατερὸς Διομήδης ἐξενάριξε` (5.151, name at 3.5-8), `δεύτερος αὖθʼ ὡρμᾶτο βοὴν ἀγαθὸς Διομήδης` (5.855). Use: the commentary's surname-first sentence = a name-epithet formula of section 4 in the line-end slot with the verb before it; the players never speak in the poem (no speech is in the corpus), so the speech frames serve only for the umpire's calls (3.10) or are avoided.

**3.9 `<NUM> minutes` / `the match`** — 14/12 (10 3, 48 2, 20, 58, 13, 15, 47, 24; pool 15) and 17/17; time-of-match statements: tv_2019wimF:0014 0:06:58 "It was 6-1 in 20 minutes"; tv_2019wimF:0108 1:10:51 "58 minutes of the first set"; tv_2019wimF:0266 2:46:46 "2 hours and 47 minutes into this final"; tv_2019wimF:0477 4:47:27 "four hours and 48 minutes matching the longest final of all time". ↔ **Time formulae** (2.6): `ἦμος δʼ` 36x (35 at 1-3); `ὄφρα μὲν ἠὼς ἦν καὶ ἀέξετο ἱερὸν ἦμαρ` 3x; `ἦμος δʼ Ἠέλιος μέσον οὐρανὸν ἀμφιβεβήκει` 2x; `ἦμος δʼ Ἠέλιος μετενίσετο βουλυτὸν δέ` 1x; `δείελον ἦμαρ` 1x; `ὀψὲ δὲ δὴ` 12x; `δηρόν` 47x, `δηθά` 16x; `τόφρα` 54x / `εἰς ὅ κε` 34x for "until"; `ἐπὶ δηρὸν δέ μοι αἰὼν` (Il. 9.415). Use: at each point where the commentators give the clock (0:06:58, 1:10:51, 2:46:46, 3:44:27, 3:56:54, 4:47:27) the poem gives the sun's station or a δηρόν/δηθά; "the match" = ἀγών (ἐν ἀγῶνι 13x; εὐρὺν ἀγῶνα 23.258) or ἄεθλος/ἄεθλον (88 stem hits; 22x ἄεθλον at 10-12).

**3.10 `mr <NAME>`** — 11/11 (federer 6, djokovic 5; pool 2), exclusively the umpire's formal announcements relayed through the broadcast: tv_2019wimF:0059 0:32:57 "Mr. Djokovic is charging the call-up service line. Ball was called in." (ASR for "challenging"); tv_2019wimF:0074 0:41:55 "Mr. Djokovic has one challenge remaining. Wait, please."; tv_2019wimF:0140 1:28:22 "… Mr. Federer has two challenges remaining."; tv_2019wimF:0466 4:38:36 "Mr. Federer is challenging …". ↔ **The vocative address formulae** (`--ngram` counts): `διογενὲς Λαερτιάδη πολυμήχανʼ Ὀδυσσεῦ` 21x whole line (Il. 2.173, 4.358, 8.93, 9.308 …); `Ἀτρεΐδη κύδιστε ἄναξ ἀνδρῶν Ἀγάμεμνον` 10x whole line (Il. 2.434, 9.96 …; Ἀτρεΐδη κύδιστε 12x at 1-5.5); `Αἶαν διογενὲς Τελαμώνιε κοίρανε λαῶν` 3x (Il. 7.234, 9.644, 11.465); `Μενέλαε διοτρεφές` 15x (3.5-8); `Τυδεΐδη Διόμηδες` 3x (1-5.5); `ὦ φίλοι` 42x, `Ζεῦ πάτερ` 32x, `ὦ γέρον` 19x, `ὦ πέπον` 8x (all 1-2). The umpire himself: `ἴστορι` / `ἴστορα` (Il. 18.501, 23.486; nominative ἴστωρ unattested), `σκοπὸν` (23.359), `ἐπίσκοπος` 3x; his "Please" = `κήρυκες δʼ ἄρα λαὸν ἐρήτυον` (Il. 18.503); the challenge verdict = `ἀληθείην ἀποείποι` (23.361) and Il. 23.485-487 (`ἴστορα δʼ Ἀτρεΐδην Ἀγαμέμνονα θείομεν ἄμφω`). Use: the one umpire moment worth a line is the challenge at 4:38:36 or 4:43:27 ("He is wrong."): address the player with a full-line vocative built on the 4.x renderings (e.g. the tested `Ῥογῆρε`/`Ζοκοβίδη` shapes must be checked), then the herald's verdict.

## 4. Name-epithet formulae

Method (HM h-i): each rendering is placed in an attested line in the slot of a Homeric name of the same shape and run through `homer/check_line.py`; the status lines below are copied from HM (i) or from the tests run for this brief on 2026-10-07 (marked *new*). "metre only" = the vowel quantity is a free choice for an invented word and check_line warns `quantity_unattested`; **the composer must flag every such line in the jsonl (`quantity: metre-only`) and the philologist will query it.** Both players share Diomedes' shape SSLX/SSLL at 9.5-12, so the epithets must keep them apart (ἀγαθός v. κρατερός is not enough on its own: use the ethnics and the craft/endurance epithets).

### 4.1 Federer (commentary: "Federer" 127, "Roger" 17, "Mr Federer" 6, "the great Swiss" 3, "the man from Basel", "the Swiss", "the older man" 1 each)

| rendering, declension | shape | position | model formula (count) | test line and verdict |
|---|---|---|---|---|
| **Φεδερῆρος**, -ήρου, -ήρῳ, -ῆρον, voc. -ῆρε (2nd decl.) | SSLX (gen./dat. SSLL) | 9.5-12 only (position 1 needs a long) | βοὴν ἀγαθὸς Διομήδης 21x at 6-12; κρατερὸς Διομήδης 20x at 7.5-12; βοὴν ἀγαθὸς 43x | `ὣς φάτο, τὸν δ᾽ οὔ τι προσέφη κρατερὸς Φεδερῆρος` status=unique tier=0 flags=[] warnings=[]; `τὸν δ᾽ ἠμείβετ᾽ ἔπειτα βοὴν ἀγαθὸς Φεδερῆρος` status=unique tier=0 flags=[] warnings=[]; `δὴ τότ᾽ ἔπειτ᾽ ἠρᾶτο βοὴν ἀγαθὸς Φεδερῆρος` (Il. 5.114 frame) status=unique tier=0 flags=[] warnings=[] (*new*, reconfirmed); `Φεδερῆρος δ᾽ ἑτέρωθεν ἀνίστατο ἰσόθεος φώς` status=fail (cannot open a line; *new* `Φεδερῆρος δ᾽ ἑτέρωθεν ἐναντίον ὦρτο λέων ὣς` also fails) |
| **Φεδερεύς**, gen. Φεδερῆος, dat. Φεδερῆϊ, acc. Φεδερῆα, voc. Φεδερεῦ (3rd decl. in -εύς like Ὀδυσσεύς, Ἀχιλλεύς) | nom. SSL; gen. SSLX | nom. 3.5-5 and 1.5-3; gen. 9.5-12 | Ὀδυσεὺς πολύμητις 3x at 1.5-5.5 (Il. 3.268, 23.709, 23.755); διογενὴς Ὀδυσεύς 6x at 1-5; Πηληϊάδεω Ἀχιλῆος 8x at 6-12 | `διογενὴς Φεδερεύς, Διομήδεα δὲ προσέειπεν` status=unique tier=0 flags=[] (warning on Διομήδεα only); `ἂν δʼ Φεδερεὺς πολύμητις ἀνίστατο κέρδεα εἰδώς.` status=unique tier=0 flags=[]; `μῆνιν ἄειδε θεὰ Πηληϊάδεω Φεδερῆος` status=unique tier=1 flags=[] (the licence is Πηληϊάδεω's attested synizesis); fails at 10-12 after πολύμητις (SSL cannot end a line) and *new* at 3-5.5 in the scales line (`τὴν μὲν Φεδερῆος …` needs two unattested licences) |
| **Ῥογῆρος**, -ήρου, -ήρῳ, -ῆρον, voc. Ῥογῆρε | SLX (gen./dat. SLL) | 6-8 after a vowel-final word; 10-12 only after a vowel; never after a word ending in a consonant whose syllable must stay short (ς + ῥ makes position) | Ὀδυσσεὺς at 6-8 before ἰσόθεος φώς (ἰσόθεος φώς 14x at 9-12; `Εὐρύαλος δέ οἱ οἶος ἀνίστατο ἰσόθεος φὼς` Il. 23.677); acc. Ὀδυσῆα δαΐφρονα ποικιλομήτην (Od. 22.115, 7.168; ποικιλομήτην 5x at 9-12) | `τὸν δ᾽ ἠμείβετ᾽ ἔπειτα Ῥογῆρος ἰσόθεος φώς` status=unique tier=0 flags=[] warnings=[]; `ὣς φάτο, μείδησεν δὲ Ῥογῆρος, ἰσόθεος φώς` status=unique tier=0 flags=[]; *new* `ἔσταν δ᾽ ἀμφὶ Ῥογῆρα δαΐφρονα ποικιλομήτην` (Od. 22.115 frame) status=unique tier=0 flags=[] (warning: α of -ῆρα taken short); fails: after πολύμητις, after πόδας ὠκύς, after πολύτλας δῖος (*new*), and `εἰ μὴ Ῥογῆρος αὐτὸς ἀνίστατο` |
| **Ἑλβέτιος** "the Swiss", -ίου, -ίῳ, -ιον (ι short, metre only; post-Homeric word, Latin Helvetii **[unverified]**) | LSSL | 1-3 | Ἀτρεΐδης/Τυδεΐδης/Πηλεΐδης LSSL at 1-3 (Ἀτρεΐδ- 210x, 101 at 1-3); `Πηλεΐδης δʼ ἑτέρωθεν ἐναντίον ὦρτο λέων ὣς` (Il. 20.164) | `Ἑλβέτιος δὲ πρῶτος ἀκόντισε δουρὶ φαεινῷ` status=unique tier=0 flags=[] (warning: ι metre only); `Ἑλβέτιος δʼ ἑτέρωθεν ἐναντίον ὦρτο λέων ὣς` status=unique tier=0 flags=[] (same warning; reconfirmed *new*); at 7-9 after ἔπειτα it is flagged (hiatus); Ἑλουήτιος fails |

Commentary epithets rendered: "the great Swiss" → μέγας + Ἑλβέτιος (μέγας as in μέγας Τελαμώνιος Αἴας 12x, μέγας κορυθαίολος Ἕκτωρ 12x — the composer must find the slot and test it); "the older man" / "37 years of age" → `πρεσβύτερος` 1x (Il. 11.787 `πρεσβύτερος δὲ σύ ἐσσι· βίῃ δʼ ὅ γε πολλὸν ἀμείνων`, 1-3), `ὀλίγον προγενέστερός ἐστιν` (Il. 23.789 — the race-winner's own words about the older man), `γεραιός` 13x (all 10-12 as ὁ γεραιός: of Priam and Nestor, too old for a 37-year-old), `γέρων` 93x (avoid), `παλαιοτέρους` (23.788 `ἀθάνατοι τιμῶσι παλαιοτέρους ἀνθρώπους`); "the man from Basel" → no Homeric rendering: omit or paraphrase with νήσῳ-type periphrasis (5.3). Homeric epithets of craft (reconfirmed): `πολύμητις` 86x (80 as πολύμητις Ὀδυσσεύς at 7.5-12; 3x at 3.5-5.5 after Ὀδυσεύς: this is the slot that takes Φεδερεύς), `ποικιλομήτην` 5x acc. at 9-12 (nom. unattested; voc. ποικιλομῆτα Od. 13.293 `σχέτλιε, ποικιλομῆτα, δόλων ἆτʼ`), `δαΐφρων` 5x nom. (10-12 or 6-8; δαΐφρονος 28x, δαΐφρονι 13x, δαΐφρονα 11x, all 6-8), `κέρδεα εἰδώς` (Il. 23.709), `μείδησεν` for the smile.

### 4.2 Djokovic (commentary: "Djokovic" 127, "Novak" 29, "Mr Djokovic" 5, "the world number one" 3, "the defending champion", "the top seed", "the Serbian", "the young(er) man", "Nole" 1 each)

| rendering, declension | shape | position | model formula (count) | test line and verdict |
|---|---|---|---|---|
| **Ζοκοβίδης** (patronymic of Đoko), gen. Ζοκοβίδαο / -εω, dat. -ίδῃ, acc. -ίδην, voc. -ίδη; ῑ long **metre only** (as Κρονίδης, 26x nom., SSL; with the short ι of Πηλεΐδης it would be SSSL and unmetrical) | SSLL | 9.5-12 only; ζ counts double, so the syllable before it is lengthened: harmless at 9 (longum), fatal after a short that must stay short | βοὴν ἀγαθὸς Διομήδης 21x at 6-12; κρατερὸς Διομήδης 20x at 7.5-12 | `ὣς φάτο, τὸν δ᾽ οὔ τι προσέφη κρατερὸς Ζοκοβίδης` status=unique tier=0 flags=[] warnings=[quantity_unattested ί … (metre only)]; `τὸν δ᾽ ἠμείβετ᾽ ἔπειτα βοὴν ἀγαθὸς Ζοκοβίδης` same; `δὴ τότʼ ἔπειτʼ ἠρᾶτο βοὴν ἀγαθὸς Ζοκοβίδης` same; *new* fails/flags: line-initial `Ζοκοβίδης δ᾽ ἑτέρωθεν …` (needs lengthening), `ὣς φάτο, Ζοκοβίδης δ᾽ ἀνεχάζετο …` (ζ after -το), `πολύτλας Ζοκοβίδης` at 9-12 (SLL + SSLL does not fit) |
| **Ζοκοβεύς**, gen. Ζοκοβῆος, dat. Ζοκοβῆϊ, acc. Ζοκοβῆα, voc. Ζοκοβεῦ | nom. SSL; gen. SSLX | nom. 3.5-5, 1.5-3; gen. 9.5-12 | as Φεδερεύς | `διογενὴς Ζοκοβεύς, Διομήδεα δὲ προσέειπεν` status=unique tier=0 flags=[]; `ἂν δʼ Ζοκοβεὺς πολύμητις ἀνίστατο κέρδεα εἰδώς.` status=unique tier=0 flags=[]; `μῆνιν ἄειδε θεὰ Πηληϊάδεω Ζοκοβῆος` status=unique tier=1 flags=[] warnings=[]; fails after πολύμητις at 10-12 and *new* `τὸν δ᾽ ἠμείβετ᾽ ἔπειτα πολύτλας Ζοκοβεὺς ἥρως` |
| **Σέρβος** "the Serb", -ου, -ῳ, -ον (coinage, post-Homeric ethnic **[unverified]**) | LX | 1-2; 11-12 after a vowel (σ after -ος makes position: fails after κορυθαίολος) | Ἕκτωρ Πριαμίδης 7x at 1-5 (Il. 8.216 `Ἕκτωρ Πριαμίδης, ὅτε οἱ Ζεὺς κῦδος ἔδωκε`) | `Σέρβος Πριαμίδης, ὅτε οἱ Ζεὺς κῦδος ἔδωκε` status=unique tier=0 flags=[] warnings=[]; `ὣς ἔφατ᾽, οὐδ᾽ ἀπίθησε βοὴν ἀγαθὸς μέγα Σέρβος` status=unique tier=0 flags=[]; *new* `Σέρβος δ᾽ αὖθ᾽ ἑτέρωθεν ἐναντίον ὦρτο λέων ὣς` status=unique tier=0 flags=[] warnings=[] |
| **Σέρβιος**, -ίου (ι metre only) | LSS before a vowel (LSL before a consonant: impossible) | 1-2 as a dactyl; 7-8 | Αἰγύπτιος LLSS at 6-8 (Od. 2.15); Δαρδάνιος | `Σέρβιος ἀντίθεος, μέγα δὲ φρεσὶ θάρσος ἔχει μοι` status=unique tier=0 flags=[] (warnings metre only); `τοῖσι δ᾽ ἔπειθ᾽ ἥρως μὲν Σέρβιος ἦρχ᾽ ἀγορεύειν` passes with caesura warnings; `Σέρβιος δʼ ἑτέρωθεν …` passes with ι taken long |
| **Νοβάκος** (ᾱ long, metre only) | SLX | 10-12 after a vowel-final word only (ν after -ς makes position: fails after πολύμητις, κορυθαίολος, ἀμύμων) | Ὀδυσσεύς / Ἀχιλλεύς SLL at 10-12 | `ὣς ἔφατ᾽, οὐδ᾽ ἀπίθησε περικλυτὸς αὖτε Νοβάκος` status=unique tier=0 flags=[] (warning ά metre only); Νόβακος with short α has no line-end slot (both tests fail); *new* gen. `Νοβάκου ἐκ χειρῶν …` at 1-2 is flagged (two unattested licences): keep Νοβάκος at 10-12 only |

Commentary epithets rendered: "the world number one" → `ὃς μέγʼ ἄριστος` 4x (Il. 2.82 at 3-5.5 `νῦν δʼ ἴδεν ὃς μέγʼ ἄριστος Ἀχαιῶν εὔχεται εἶναι`; 16.271, 17.164, Od. 22.29 at 9-12), `μέγʼ ἄριστος` 5x, `ὄχʼ ἄριστος` 9x; **correction to the task's hint**: Il. 1.91 reads `ὃς νῦν πολλὸν ἄριστος Ἀχαιῶν εὔχεται εἶναι` (πολλὸν, not μέγ᾽) — it gives the same claim with Ἀχαιῶν εὔχεται εἶναι at 6-12, usable as "who boasts to be far the best of all"; "the defending champion" → no word: paraphrase "who held the prize before" with ἄεθλον (Il. 22.163 `τὸ δὲ μέγα κεῖται ἄεθλον`) or omit; "the top seed" / "seeds one and two" → πρῶτος … δεύτερος (3.4); "the young(er) man" → `ὁπλότερος` 3x (Il. 2.707 = Od. 19.184 `ὁπλότερος γενεῇ· ὁ δʼ ἅμα πρότερος καὶ ἀρείων` — "younger by birth; the other was elder and better": note the irony if used), `νεώτερος` 6x (6-8; Il. 21.439 `… σὺ γὰρ γενεῆφι νεώτερος`), `ὁπλότατος γενεῆφιν` (Il. 9.58); "the Serbian" → Σέρβος (coinage); "Nole" → Homer has no hypocoristics; the single-sigma Ὀδυσεύς / Ἀχιλεύς is the metrical analogue of a shortened name, and Ζοκοβεύς plays that part. Homeric epithets of endurance (reconfirmed): `πολύτλας` 42x, all as πολύτλας δῖος Ὀδυσσεύς at 6-8 (SLL: usable before a LS SLL name only, so not before Ζοκοβίδης; test fails); `ταλασίφρονος` 12x gen. at 5.5-8 (`Ὀδυσσῆος ταλασίφρονος`; nominative ταλασίφρων unattested); `ἀμύμων` 19x nom. (mostly 10-12: `Τεῦκρος ἀμύμων` Il. 8.273), `ἀμύμονος` 41x, `ἀμύμονα` 42x (6-8: `ἀμύμονά τε κρατερόν τε` Il. 4.89 = 5.169); `τλήμων` was not queried; `κρατερός` 38x (κρατερὸς Διομήδης 20x) — give κρατερός to Djokovic and ἀγαθός (βοὴν ἀγαθός) to Federer, or the reverse, but **one assignment, kept throughout** (Parry's economy, HM h).

### 4.3 Summary of economical systems (each player: three shapes, one formula per shape)
Federer: (1) line-end SSLX `βοὴν ἀγαθὸς Φεδερῆρος` / `… κρατερὸς Φεδερῆρος` at 6-12 / 7.5-12; (2) line-initial LSSL `Ἑλβέτιος δ(έ) …` at 1-3; (3) mid-line SLX `… Ῥογῆρος ἰσόθεος φώς` at 6-8 (+ 9-12), and the genitive `Πηληϊάδεω Φεδερῆος` / nominative `διογενὴς Φεδερεύς` for the proem and the 3.5-5 slot. Djokovic: (1) line-end SSLL `βοὴν ἀγαθὸς Ζοκοβίδης` / `κρατερὸς Ζοκοβίδης`; (2) line-initial LX `Σέρβος Πριαμίδης …`-type (Σέρβος + a patronymic-shaped epithet of LSSL, e.g. ἀντίθεος, checked) and `Σέρβος δ᾽ αὖθ᾽ ἑτέρωθεν …`; (3) SLX `αὖτε Νοβάκος` at 10-12 after a vowel, and `διογενὴς Ζοκοβεύς` / `Πηληϊάδεω Ζοκοβῆος`. Each player must receive each of his three shapes at least once (5.1).

## 5. Constraints for the composer

### 5.1 Form
* About 50 lines (45-55), numbered; every line passes `python homer/check_line.py` with no flags (warnings allowed only for the invented names' quantities, each flagged `metre-only` in the jsonl); run `--file` on the whole draft before returning it.
* Homeric Kunstsprache only: Ionic-epic forms as in homer/lines.tsv; no post-Homeric words (no γραμμή, στέγη, ὄχλος, ἀθλητής beyond ἀθλητήρ Od. 8.164, no ὥρα 'hour', no σφαιριστ-, no ἡττ-); prefer attested formulae, and for every formula or half-line record in `poem.jsonl`: `source` (citation + position, from a concordance query you ran), `status` (ATTESTED-EXACT / ATTESTED-ADAPTED / MODELLED / FREE), `count`, and the `commentary_equivalent` of section 3 where one applies.
* Name-epithet formulae of section 4: each player gets each of his three metrical shapes at least once; one epithet assignment kept throughout (economy); no name in a slot that section 4 marks as failing (Φεδερῆρος/Ζοκοβίδης never line-initial; Ῥογῆρος never after -ς; Ζοκοβ- never after a short that must stay short; Νοβάκος only after a vowel at 10-12).
* Enjambment varied and recorded per line (2.7); at least two extended similes (≥ 3 lines each) from 2.5, with the Homeric model cited in the jsonl; the arming scene in the attested order (2.2); the counting formula at every score change inside a narrated point and a prize/victory formula at every game or set won (3.1-3.2).
* Match facts only from section 1, with the clock of each narrated point in the jsonl (`clock`); nothing from 1.11's "not available" list; commentary excerpts, if any are echoed, ≤ 15 words and cited by clip id.

### 5.2 Lexicon (HM j, reconfirmed; counts from `--loose`/`--ngram`)
| thing | use | do not use |
|---|---|---|
| racket | σάκος/ἀσπίς (what parries) or ῥόπαλον (3x), κορύνη (2x); the spear formulae for the stroke (ἔγχος, δόρυ) | ῥάβδος (a wand or fishing rod) |
| ball | σφαῖρα: σφαίρῃ (Od. 6.100, 8.377), σφαῖραν (Od. 6.115, 8.372), σφαιρηδόν (Il. 13.204); Od. 8.374-376 for a volley; metaphorically ἔγχος/βέλος | — |
| net | ἕρκος 21x (16 at 9-9.5), ἕρκεϊ; λίνον for the cord | δίκτυον (once, Od. 22.386, of fish) |
| court, baseline, lines | ἀγών (ἐν ἀγῶνι 13x; εὐρὺν ἀγῶνα), χῶρος (διαμετρητῷ ἐνὶ χώρῳ Il. 3.344), αὐλή (38x) for the enclosure, πεδίον; lines = τέρματα (8x), νύσσα (ἐν νύσσῃ 2x), σῆμα/σήματα (Od. 8.192) | γραμμή (0 hits) |
| grass | ποίη (Il. 14.347 νεοθηλέα ποίην), λειμών (16x) | χλόη (0 hits), χόρτος (2x, a yard) |
| serve | προΐει / προέηκε (29 + 32), ἧκε (38x), ἀφέηκε (Il. 23.841), ἔρριψε (6x: Od. 6.115 of the ball, Il. 23.842-845 of the shot), ἀκόντισε (18x) | — |
| ace, winner, error, fault | οὐδʼ ἀφάμαρτε(ν); ὑπέρπτατο σήματα πάντων; ἤμβροτες οὐδʼ ἔτυχες; ἐτώσιον ἔκφυγε χειρός; double fault = δίς … ἥμαρτε (the composer builds it from δίς and ἁμαρτ-, attested separately) | — |
| umpire, line judge, challenge | ἴστορι / ἴστορα (nom. unattested), σκοπόν (23.359), ἐπίσκοπος (3x), δικασπόλος (2x); κήρυκες for "Please"; ἀληθείην ἀποείποι | δικαστής (0 hits) |
| crowd | λαοί 47x, λαός, ὅμιλος (ὅμιλον 54x), πληθύς, δῆμος; the shouts and the hush of 2.6 | ὄχλος (0 hits) |
| prize, trophy | ἄεθλον (22x at 10-12), ἄεθλα, δέπας (30x; δέπας ἀμφικύπελλον 11x), γέρας 39x, τρίπους / λέβης, κρητήρ | — |
| roof, rain, sun, shade, heat | ὄροφος (Il. 24.451, of reeds), ὀροφή, μέλαθρον; ὄμβρος 8x, ὗε δʼ ἄρα Ζεύς 2x (no rain fell: do not use); ἠέλιος (135 stem hits), σκιόωντο; καῦμα (Il. 5.865) | στέγη (0) |
| time, length | ἦμαρ 82x, δηρόν 47x, δηθά 16x, δείελον; the sun's stations (2.6) | ὥρη 'hour' (18x, always a season) |
| fatigue | κάματος, καμάτῳ, ἱδρώς, φίλα γυῖα λέλυνται, κεκμηώς (7x), ἀσθμαίνων (9x) | — |
| forehand / backhand | ἐπὶ δεξιά / ἐπʼ ἀριστερά (Il. 7.238); δεξι- 64x, ἀριστερ- 25x | — |
| no equivalent (paraphrase or drop) | deuce/advantage (ἶσα, ἐπὶ ἶσα, ἰσάζουσʼ, ἐρίζητον περὶ ἴσης, ἀμφήριστον), tie-break and the 12-12 rule (the heralds, Il. 7.282), set/game (no word: ἄεθλος, δρόμος at most), love/15/30/40 (the counting formula), let, volley, slice/topspin, break of serve (ἐξενάριξε, ἤρατο κῦδος), Hawk-Eye, ball kids, the chair (θρόνος), scoreboard, new balls, towel, changeover (the turn at the τέρμα), the roof, the Royal Box (Il. 23.448-451 `ἧστο γὰρ ἐκτὸς ἀγῶνος ὑπέρτατος ἐν περιωπῇ`), km/h, the record books | — |

### 5.3 Wimbledon and other proper names
No modern proper name except the two players' renderings. For Wimbledon use no name: the attested periphrasis `νήσῳ ἐν ἀμφιρύτῃ` (3x, all 1-5: Od. 1.50, 1.198, 12.283; ἀμφιρύτ- 4x) "on a sea-girt island", with `πρὸς ζόφον` (Od. 9.26, 12.81, 1-2) "toward the west" if the location is wanted, plus ἀγών/λειμών/ποίη for the grass court. There is no Homeric ethnic for Britain; Βρεττανοί or "the grass of the Britons" would be a post-Homeric coinage and must be marked `coinage` in the jsonl if used (not recommended). Ἑλβέτιος and Σέρβος are likewise coinages (marked). Basel, Serbia, Switzerland, London, the BBC, Boris, Tim, Damian Steiner, the Duchess, Nadal (tv_2019wimF:0227 2:27:24 mentions "his semi final victory over Rafa Nadal"): none may appear by name.

### 5.4 What not to do
* No post-Homeric vocabulary, no Attic contractions, no Latin-based words; no numerals for minutes or km/h; no "hour".
* No fact outside section 1; in particular no coin toss, no walk-on description, no ceremony, no speeches, no sunset at the end, no grass-eating, no named spectator, no weather beyond 1.10, no rain, no roof closing.
* No speech by either player (none is in the corpus); the umpire's and the heralds' words may be rendered only as the generic calls of 3.10.
* Do not give both players the same epithet; do not put a name in a failing slot (4.1-4.2); do not quote a Homeric line that you have not re-run through the concordance yourself (write the query into the jsonl).
* Do not exceed 15 words of any commentary excerpt; do not commit corpus media or full transcripts.

### 5.5 Deliverables
`composition/drafts/v1.txt` (one line per verse, numbered) and `composition/drafts/v1.jsonl` (one record per verse: `n`, `text`, `scansion` from check_line, `enjambment`, `section` of 2.0, `clock` and `facts` from section 1, `sources` [{citation, position, count, status, query}], `name_formula`, `commentary_equivalent`, `quantity` flags, `notes`), plus a 10-line summary of what was attempted and which lines are weakest. Verification pipeline (PHASES.md Phase 4): scansion-verifier, provenance-verifier, philologist; a line passes only if all three pass it.

## Addendum A1 (after round 1, orchestrator)
1. Name slots: §4's slot lists were tests, not an exhaustive licence. Any slot where `check_line.py` passes with no flags and no unattested licence is allowed; record the slot in the jsonl.
2. Djokovic renderings replaced (review/round_1.md R3): **Ζοκοβείδης** (SSLL; patronymic in -είδης from Ζοκοβεύς, model Πηλείδης: verify) for the Διομήδης slot; **Νοβήκος** (SLX, Ionic η for ᾱ) for the Ὀδυσσεύς/Ἀχιλλεύς slot after a vowel-final word; Σέρβος and Ζοκοβεύς unchanged. Ζοκοβίδης and Νοβάκος are withdrawn.
3. Ῥογῆρος must not stand before ἰσόθεος φώς (R2). δίς + verb is not allowed (R4); ἐξενάριξε at most twice, inside the aristeia (R5); πάλιν only as "back" (R6).

## Addendum A2 (after round 2, orchestrator)
1. The Ionic form of Novak is **Νοβῆκος** (circumflex), replacing Νοβήκος in A1.
2. Ζοκοβεύς denotes the eponym (Đoko), never Novak Djokovic himself; Djokovic's forms are Ζοκοβείδης (gen. Ζοκοβείδαο / Ζοκοβείδεω, to be verified against Πηλεΐδαο / Πηληϊάδεω), Σέρβος, Νοβῆκος. Models for -είδης: Ἀμαρυγκείδην Il. 4.517, Ἀτρείδης Od. 15.52, Πηλείδη Il. 1.277.
3. Counting must match the facts: δεύτερον αὖτις narrates one repeated action.
