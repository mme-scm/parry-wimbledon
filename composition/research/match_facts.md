# Match facts: 2019 Wimbledon gentlemen's singles final, Novak Djokovic d. Roger Federer, 14 July 2019

Phase 3 research file for the composer. Every number in the tables T1-T18 below is printed by the script in the Appendix
(`match_facts.py`, run with `python -I`), which reads only the corpus files named here; nothing is typed in by hand. The
external facts in section E come from pages fetched on 2026-10-07 with the URLs given, or are marked **[unverified]**.
Commentary quotations are at most 15 words (the script truncates them), as CLAUDE.md requires.

## A. Sources on disk and how to read them

| key | file | what it is | player keys |
|---|---|---|---|
| **P** | `corpus/timing/points_2019wimF.csv` | one row per point (422), joining R, M and S by index; columns `pbp_*` (from R), `mcp_*` (from M), `tv_*` (from S/T) | `p1_name` = Djokovic, `p2_name` = Federer; `pts_before_p1/p2` are Djokovic-Federer |
| **R** | `corpus/raw/sackmann_slam_pbp_hfmirror/2019-wimbledon-points.csv`, `match_id 2019-wimbledon-1701` | Grand Slam point-by-point (Jeff Sackmann's archive, HF mirror; CC BY-NC-SA 4.0): 424 rows = 2 placeholder rows `0X`, `0Y` + 422 points; 65 columns | **P1 = Djokovic, P2 = Federer** |
| **M** | `corpus/raw/sackmann_mcp/charting-m-points-2010s.csv`, `match_id 20190714-M-Wimbledon-F-Roger_Federer-Novak_Djokovic` | Match Charting Project shot codes, 422 points, charter "Zindaras" (CC BY-NC-SA 4.0) | **player 1 = Federer, player 2 = Djokovic** (`Svr`, `PtWinner`) |
| **S** | `corpus/timing/shots_2019wimF.csv` | TennisVL per-shot parser output: hitter, stroke type, wing, direction, `hit_timestamp_second` (video seconds) | names in full |
| **T** | `corpus/transcripts/tv_2019wimF.jsonl` | TennisVL WhisperX ASR transcript of one TV commentary track, one record per clip (481 clips), fields `text_corrected`, `point_idx_pbp`, `score_before`, `clip_start_s`, `elapsed_this_point_s` | broadcaster unnamed, "probably BBC TV [unverified]" (hints: "Boris" 18x, "Tim" 7x, "the gentleman on my left, Tim Henman") |

Conventions used throughout:

* **Clock** = R `ElapsedTime`, the match clock at the **first serve** of each point, 1 s resolution, 0:00:00 at point 1.
  The last point starts at 4:56:59; the official duration (section E) is 4 h 57 min.
* **Scores** are written Djokovic-Federer unless stated; in R the `P1Score/P2Score` columns are the state *after* the point.
  `GameNo` in R restarts at 1 in every set (the 12-12 tie-break is set-5 game 25).
* **R's rally count** (`RallyCount`) counts in-play shots and excludes the final erring shot; M and S count the erring shot
  (corpus/README.md section 7.1).
* **M shot codes.** The point-ending symbol is reliable and cross-checked in corpus/README.md 7.1: `*` winner, `@` unforced
  error, `#` forced error; `mcp_ace` / `mcp_double_fault` are derived columns of P. The rest of the notation (digits 4/5/6 =
  serve wide/body/T; `f`/`b` forehand/backhand drive, `r`/`s` forehand/backhand slice, `v`/`z` volleys, `o` overhead, `u`/`y`
  drop shots, `l`/`m` lobs, `h`/`i` half-volleys; `+` approach shot; `-` at net; digits 1-3 the direction; `n`/`w`/`d`/`x` the
  error type net/wide/deep/wide-and-deep; `c` a let; `;` and `!` special annotations) follows the Match Charting Project's
  instructions tab, which is **not on disk** here: **[unverified]**, used below only descriptively. The hitter of the last shot
  is inferred from the parity of `mcp_n_shots` (odd = the server hit last).
* **Coverage limits.** S/T clips exist for 368 of the 422 points (points 3 to 413); 318 clips carry text. The clips are
  rally and serve clips only: **there is no footage or transcript of the walk-on, warm-up, coin toss, trophy presentation or
  speeches**, and the last nine points of the match (414-422, the rest of the 12-12 tie-break and the championship point)
  have no clip at all (P `tv_n_clips` empty). Section T15 says what the transcript does contain of the "typical scenes".

## B. Headline numbers (all from the tables below; R unless stated)

| fact | value | where |
|---|---|---|
| score | Djokovic d. Federer **7-6(5), 1-6, 7-6(4), 4-6, 13-12(3)** | T1 |
| clock at the first serve of the last point | **4:56:59** | T1 |
| points won | Federer **218**, Djokovic **204** (R, M and P agree) | T2 |
| games | 68 (13 + 7 + 13 + 10 + 25); fifth set 169 points from 3:00:13 to 4:56:59 | T9, T18 |
| aces | Federer 25, Djokovic 10 | T3 |
| double faults | Federer 6, Djokovic 9 | T3 |
| winners (R `Winner`, aces included) | Federer 94, Djokovic 54 | T3 |
| unforced errors (R `UnfErr`) | Federer 62, Djokovic 52 | T3 |
| break points | Federer 7 of 13 converted; Djokovic 3 of 8 | T4 |
| fastest serve | Federer 202 km/h (3:35:36), Djokovic 199 km/h (3:07:13) | T5 |
| longest rally | 35 shots (M; R RallyCount 35; TennisVL 34 shots, 43.4 s), point 242 at **2:47:12**, set 4 game 8, 40-30 Dj-Fe with Federer serving at 2-5; won by Federer | T6 |
| championship points | two, Federer serving at 8-7 in set 5: **4:10:58** (40-15) and **4:11:30** (40-30); both won by Djokovic | T10 |
| the break back | Djokovic breaks in that game at **4:12:40** (point 362, AD-40) for 8-8 | T10, T11 |
| 12-12 tie-break | **4:48:30 to 4:56:59**, Djokovic 7-3 | T12 |
| final point | 4:56:59, Federer second serve 143 km/h, 3 shots, Federer forehand unforced error (R `P2UnfErr`, M `5b38f!@`) | T13 |

## C. The tables (script output, verbatim)

## T1. Score set by set (R: last row of each SetNo; tie-break score = P1Score/P2Score after the penultimate point + the winner of the last point)
| set | games Djokovic-Federer | set winner | tie-break (Djokovic-Federer) | first point clock | last point clock | points in set | games in set |
|---|---|---|---|---|---|---|---|
| 1 | 7-6 | Djokovic | 7-5 | 0:00:00 | 0:57:50 | 87 | 13 |
| 2 | 1-6 | Federer | - | 1:00:23 | 1:22:54 | 38 | 7 |
| 3 | 7-6 | Djokovic | 7-4 | 1:27:28 | 2:15:24 | 73 | 13 |
| 4 | 4-6 | Federer | - | 2:20:29 | 2:55:08 | 55 | 10 |
| 5 | 13-12 | Djokovic | 7-3 | 3:00:13 | 4:56:59 | 169 | 25 |

Duration = last ElapsedTime (R) = **4:56:59** (first serve of the last point; the match clock starts 0:00:00 at point 1).
Sets: Djokovic 3, Federer 2.

## T2. Points won
R PointWinner counts: Djokovic 204, Federer 218 (total 422); R running columns at the last row: P1PointsWon=204 (Djokovic), P2PointsWon=218 (Federer).
M PtWinner counts: Federer 218, Djokovic 204.
Per set (R):
| set | Djokovic | Federer |
|---|---|---|
| 1 | 46 | 41 |
| 2 | 12 | 26 |
| 3 | 36 | 37 |
| 4 | 25 | 30 |
| 5 | 85 | 84 |

Service points (R: PointServer = server; won = PointWinner == PointServer):
| server | service points | won | % |
|---|---|---|---|
| Djokovic | 219 | 140 | 63.9 |
| Federer | 203 | 139 | 68.5 |

## T3. Aces, double faults, winners, unforced errors per player per set (R columns P1Ace/P2Ace, P1DoubleFault/P2DoubleFault, P1Winner/P2Winner, P1UnfErr/P2UnfErr; 1 = that point)
| set | aces Dj | aces Fe | DF Dj | DF Fe | winners Dj | winners Fe | UE Dj | UE Fe | net pts Dj (won) | net pts Fe (won) |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | 4 | 5 | 2 | 1 | 14 | 21 | 6 | 14 | 7 (5) | 10 (8) |
| 2 | 0 | 3 | 1 | 3 | 2 | 9 | 10 | 4 | 2 (0) | 4 (4) |
| 3 | 1 | 4 | 2 | 0 | 9 | 13 | 7 | 12 | 4 (3) | 8 (7) |
| 4 | 3 | 1 | 1 | 2 | 9 | 14 | 6 | 10 | 3 (1) | 8 (8) |
| 5 | 2 | 12 | 3 | 0 | 20 | 37 | 23 | 22 | 10 (9) | 23 (18) |
| all | 10 | 25 | 9 | 6 | 54 | 94 | 52 | 62 | 26 (18) | 53 (45) |

Aces counted also as winners in R (rows with Ace=1 and Winner=1 for the same player): 35 of 35 aces -> the Winner columns include aces.
R columns that are empty for every point of this match: Rally, P1FirstSrvIn, P2FirstSrvIn, P1FirstSrvWon, P2FirstSrvWon, P1SecondSrvIn, P2SecondSrvIn, P1SecondSrvWon, P2SecondSrvWon, P1ForcedError, P2ForcedError, Serve_Direction, Winner_FH, Winner_BH, ServingTo, P1TurningPoint, P2TurningPoint.
R columns filled: all others; WinnerType is 'S' for 8 points (serve winners), WinnerShotType F/B for 105 points; Rally is empty (RallyCount is filled).

Cross-check from M (Match Charting Project; ending symbol of the last shot code: `*` winner, `@` unforced error, `#` forced error; mcp_ace / mcp_double_fault from P):
| | Djokovic | Federer |
|---|---|---|
| ace | 10 | 25 |
| double fault | 9 | 6 |
| winner (non-ace) | 39 | 63 |
| unforced error (non-DF) | 57 | 70 |
| forced error | 64 | 78 |
(hitter of the last shot inferred from the parity of mcp_n_shots: odd = server hit last; the MCP charter's own @/# labels differ from the official R labels, see corpus/README.md section 7.1)

## T4. Break points (R: P1BreakPoint = Djokovic holds a break point (Federer serving), P1BreakPointWon = converted; P2* likewise for Federer)
Sanity: server on the points with P1BreakPoint=1: {'2': 8} (2 = Federer serving, as expected).
| set | BP for Djokovic (converted) | BP for Federer (converted) | breaks of serve in set (game winner != server) |
|---|---|---|---|
| 1 | 0 (0) | 1 (0) |  |
| 2 | 0 (0) | 4 (3) | s2 g1 by Federer; s2 g3 by Federer; s2 g7 by Federer |
| 3 | 0 (0) | 1 (0) |  |
| 4 | 2 (1) | 2 (2) | s4 g5 by Federer; s4 g7 by Federer; s4 g8 by Djokovic |
| 5 | 6 (2) | 5 (2) | s5 g6 by Djokovic; s5 g7 by Federer; s5 g15 by Federer; s5 g16 by Djokovic |
| all | 8 (3) | 13 (7) | 10 |
(a tie-break game is excluded from the break column.)

## T5. Serve speed (R: Speed_KMH of the serve that started the point, by PointServer and ServeNumber; 0 = not recorded)
| server | serves recorded | 1st-serve n | 1st max | 1st mean | 2nd n | 2nd max | 2nd mean | all max | all mean | all min |
|---|---|---|---|---|---|---|---|---|---|---|
| Djokovic | 210 | 136 | 199 | 189.2 | 74 | 181 | 158.3 | 199 | 178.3 | 128 |
| Federer | 197 | 127 | 202 | 187.2 | 70 | 173 | 153.7 | 202 | 175.3 | 136 |
Points with Speed_KMH = 0 (unrecorded): 15 of 422.
Fastest serve Djokovic: 199 km/h (124 mph) at 3:07:13, set 5 game 3, point 267, serve 1, ace=0; MCP `6s29f3s2n@` -> unforced error; commentary: (no transcribed clip)
Fastest serve Federer: 202 km/h (126 mph) at 3:35:36, set 5 game 8, point 307, serve 1, ace=0; MCP `6s28u+3b1*` -> winner; commentary: tv_2019wimF:0349 (rally, video 12961.2s): "Gone down the line. Had a big gap. Like that. Risky business by Rochaferro at …"

## T6. Longest rallies
Conventions (corpus/README.md 7.1): R RallyCount counts in-play shots (the erring final shot is not counted); M and TennisVL count the erring shot too.
| rank | point_idx | clock (R ElapsedTime) | set/game, score before (server first, PBP) | MCP shots | R RallyCount | TV n_shots | TV rally s | winner | ending (MCP) | commentary (TennisVL clip) |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | 242 | 2:47:12 | s4 g8, 40-30 (Dj-Fe), games 2-5, server Federer | 35 | 35 | 34 | 43.44 | Federer | 1st `4w` (fault), 2nd `4b28b3b3b3f2b3b2f2f1f1f1f2b3s3b3b3b2f3b3s3b2b3b2s2f3b3b2f1r2f1f1f1f2b1*` -> winner | tv_2019wimF:0268 (rally, video 10066.7s): "35 shots every one of them right out of the middle yes" |
| 2 | 183 | 2:03:53 | s3 g12, 0-0 (Dj-Fe), games 5-6, server Djokovic | 26 | 26 | 26 | 32.24 | Federer | `4f29f1f2b1f3b3b1f2f1f1f1f2s3b3s2f3s3b2b3b2b3f1r1f+3b1*` -> winner | tv_2019wimF:0201 (rally, video 7458.6s): "justifies logic 26 shots and at the end Federer able to come up with the …" |
| 3 | 193 | 2:11:04 | s3 g13 TB, 4-1 (Dj-Fe), games 6-6, server Djokovic | 24 | 23 | - | - | Djokovic | `5s29f3s2f2f2f3b2f1f1f2s1f1f1f2s3b3s2f1f3b3s3b3s3d#` -> forced error | (no transcribed clip) |
| 4 | 401 | 4:38:36 | s5 g23, 40-40 (Dj-Fe), games 11-11, server Djokovic | 24 | 24 | 20 | 25.84 | Federer | `4f38b2s3b3s3b3b3b3f3b3s2f1f;1r2f1f2f1f3s3s3s1r2f3*` -> winner | tv_2019wimF:0466 (rally, video 16742.1s): "How was it? He didn't out. Mr. Federer is challenging Nicole Lefarbo. Oh, it's called …" |
| 5 | 77 | 0:49:48 | s1 g13 TB, 0-1 (Dj-Fe), games 6-6, server Djokovic | 22 | 21 | - | - | Djokovic | 1st `c6n` (fault), 2nd `6f38b3s1f3s3b3b3b3s1f1f3b2s2f2b3s2f1f2f3b3f!@` -> unforced error | (no transcribed clip) |
| 6 | 144 | 1:38:46 | s3 g4, 30-15 (Dj-Fe), games 1-2, server Djokovic | 22 | 21 | 22 | 26.32 | Djokovic | 1st `6x` (fault), 2nd `6f37b2f2f2f2b2f2f2s3s3f1f1f2b3s3b3b3b3b3b3s3d#` -> forced error | tv_2019wimF:0160 (first_serve_fault, video 5952.1s): "Ball!" |

Longest by TennisVL shot count: point 242 (34 shots, 43.44 s, MCP 35, clock 2:47:12); point 183 (26 shots, 32.24 s, MCP 26, clock 2:03:53); point 144 (22 shots, 26.32 s, MCP 22, clock 1:38:46)
Longest by R RallyCount: point 242 (35 in-play shots, clock 2:47:12); point 183 (26 in-play shots, clock 2:03:53); point 401 (24 in-play shots, clock 4:38:36)
Longest by TennisVL rally duration (first hit to last hit): point 242 (43.44 s, 34 shots, clock 2:47:12); point 183 (32.24 s, 26 shots, clock 2:03:53); point 144 (26.32 s, 22 shots, clock 1:38:46)
R distance run on point 242: Djokovic 104.207 m, Federer 85.525 m (units as in the file; the column is unlabelled).
MCP shots per point: mean 5.00, median 4.0, points with >= 10 shots: 58, 1-shot points (aces/DF/unreturned serves counted as 1 or 2): 138.

## T7. First-set tie-break (R: SetNo 1, GameNo 13), point by point
| pt | clock | score before (Dj-Fe) | server | serve km/h (no.) | winner | R RallyCount | MCP shots | MCP code -> ending | R flags | commentary |
|---|---|---|---|---|---|---|---|---|---|---|
| 76 | 0:49:06 | 0-0 | Federer | 197 (1) | Federer | 1 | 2 | `6b2d#` -> forced error |  | tv_2019wimF:0086 (rally, video 2971.4s): "Federer gets the first point. I'm not a believer in these mini break situations. I …" |
| 77 | 0:49:48 | 0-1 | Djokovic | 172 (2) | Djokovic | 21 | 22 | 1st `c6n` (fault), 2nd `6f38b3s1f3s3b3b3b3s1f1f3b2s2f2b3s2f1f2f3b3f!@` -> unforced error | Fe:UnfErr | (no transcribed clip) |
| 78 | 0:51:05 | 1-1 | Djokovic | 152 (2) | Djokovic | 13 | 14 | 1st `6n` (fault), 2nd `5f28b3s3b3b2b3s3b1r1f+3b3z2f1d@` -> unforced error | Fe:UnfErr,Dj:NetPoint | (no transcribed clip) |
| 79 | 0:52:11 | 2-1 | Federer | 196 (1) | Djokovic | 6 | 7 | `4b38f3b1r2f3b1d#` -> forced error |  | (no transcribed clip) |
| 80 | 0:52:44 | 3-1 | Federer | 175 (1) | Federer | 1 | 1 | `4*` -> winner | Fe:Ace,Fe:Winner | (no transcribed clip) |
| 81 | 0:53:19 | 3-2 | Djokovic | 146 (2) | Federer | 10 | 10 | 1st `6w` (fault), 2nd `5s37b3f1f1f3b3s1f3b1*` -> winner | Fe:Winner | (no transcribed clip) |
| 82 | 0:55:01 | 3-3 | Djokovic | 180 (1) | Federer | 6 | 6 | `c4f;27f3s3f+1f3*` -> winner | Fe:Winner,Dj:NetPoint | (no transcribed clip) |
| 83 | 0:55:41 | 3-4 | Federer | 197 (1) | Federer | 1 | 2 | `4s#` -> forced error | Fe:Winner | (no transcribed clip) |
| 84 | 0:56:03 | 3-5 | Federer | 175 (1) | Djokovic | 2 | 3 | `4f28f1w@` -> unforced error | Fe:UnfErr | (no transcribed clip) |
| 85 | 0:56:39 | 4-5 | Djokovic | 197 (1) | Djokovic | 3 | 4 | `6f28f1f1w@` -> unforced error | Fe:UnfErr | (no transcribed clip) |
| 86 | 0:57:12 | 5-5 | Djokovic | 196 (1) | Djokovic | 7 | 8 | `5s29b3s3b3s3b+1f3n#` -> forced error | Dj:NetPoint | (no transcribed clip) |
| 87 | 0:57:50 | 6-5 | Federer | 196 (1) | Djokovic | 6 | 7 | `6f28f2b3f3b3b3w@` -> unforced error | Fe:UnfErr | (no transcribed clip) |
Tie-break first point 0:49:06, last point 0:57:50; 12 points; game winner Djokovic; set winner Djokovic.

## T8. Third-set tie-break (R: SetNo 3, GameNo 13), point by point
| pt | clock | score before (Dj-Fe) | server | serve km/h (no.) | winner | R RallyCount | MCP shots | MCP code -> ending | R flags | commentary |
|---|---|---|---|---|---|---|---|---|---|---|
| 188 | 2:07:34 | 0-0 | Federer | 188 (1) | Djokovic | 4 | 5 | `4f29f3b3b3w@` -> unforced error | Fe:UnfErr | tv_2019wimF:0208 (rally, video 7679.5s): "1-0. You've seen the first serve return by Djokovic and all of a sudden it's …" |
| 189 | 2:08:28 | 1-0 | Djokovic | 194 (1) | Djokovic | 1 | 2 | `c6f2d#` -> forced error |  | (no transcribed clip) |
| 190 | 2:08:58 | 2-0 | Djokovic | 196 (1) | Djokovic | 13 | 14 | `6s;27b3b3b3b3b2f2b2b3b2s3b3b3w@` -> unforced error | Fe:UnfErr | (no transcribed clip) |
| 191 | 2:09:46 | 3-0 | Federer | 197 (1) | Federer | 1 | 2 | `6f3n#` -> forced error |  | (no transcribed clip) |
| 192 | 2:10:17 | 3-1 | Federer | 149 (2) | Djokovic | 2 | 3 | 1st `c6n` (fault), 2nd `6b38b2n@` -> unforced error | Fe:UnfErr | (no transcribed clip) |
| 193 | 2:11:04 | 4-1 | Djokovic | 193 (1) | Djokovic | 23 | 24 | `5s29f3s2f2f2f3b2f1f1f2s1f1f1f2s3b3s2f1f3b3s3b3s3d#` -> forced error |  | (no transcribed clip) |
| 194 | 2:12:34 | 5-1 | Djokovic | 186 (1) | Federer | 6 | 7 | `4f19f3b3b1f1f1n#` -> forced error |  | (no transcribed clip) |
| 195 | 2:13:23 | 5-2 | Federer | 197 (1) | Federer | 3 | 3 | `c6f2j3*` -> winner | Fe:Winner,Fe:NetPoint | (no transcribed clip) |
| 196 | 2:13:50 | 5-3 | Federer | 197 (1) | Federer | 1 | 1 | `6*` -> winner | Fe:Ace,Fe:Winner | (no transcribed clip) |
| 197 | 2:14:28 | 5-4 | Djokovic | 128 (2) | Djokovic | 3 | 4 | 1st `4n` (fault), 2nd `5s29f3s1w@` -> unforced error | Fe:UnfErr | (no transcribed clip) |
| 198 | 2:15:24 | 6-4 | Djokovic | 196 (1) | Djokovic | 5 | 6 | `6s28b3s3b+1f2n#` -> forced error | Dj:NetPoint | (no transcribed clip) |
Tie-break first point 2:07:34, last point 2:15:24; 11 points; game winner Djokovic; set winner Djokovic.

## T9. Fifth set game by game (R: SetNo 5; clock = ElapsedTime of the first point of the game; games after = P1GamesWon-P2GamesWon at the game's last point)
| game (set) | R GameNo (restarts each set) | clock first point | clock last point | server | points (Dj-Fe) | game winner | break? | games after (Dj-Fe) | note (R flags) |
|---|---|---|---|---|---|---|---|---|---|
| 1 | 1 | 3:00:13 | 3:02:24 | Djokovic | 4-1 | Djokovic |  | 1-0 |  |
| 2 | 2 | 3:03:20 | 3:05:14 | Federer | 2-4 | Federer |  | 1-1 | 2 ace(s) |
| 3 | 3 | 3:05:57 | 3:10:39 | Djokovic | 5-3 | Djokovic |  | 2-1 | 1 ace(s); 1 DF |
| 4 | 4 | 3:12:15 | 3:16:32 | Federer | 4-6 | Federer |  | 2-2 | 3 BP for Djokovic; 1 ace(s) |
| 5 | 5 | 3:17:07 | 3:20:54 | Djokovic | 5-3 | Djokovic |  | 3-2 |  |
| 6 | 6 | 3:22:33 | 3:25:11 | Federer | 4-2 | Djokovic | BREAK | 4-2 | 2 BP for Djokovic |
| 7 | 7 | 3:26:14 | 3:31:55 | Djokovic | 3-5 | Federer | BREAK | 4-3 | 2 BP for Federer; 1 DF |
| 8 | 8 | 3:34:08 | 3:37:10 | Federer | 2-4 | Federer |  | 4-4 | 1 ace(s) |
| 9 | 9 | 3:37:57 | 3:41:32 | Djokovic | 4-2 | Djokovic |  | 5-4 |  |
| 10 | 10 | 3:43:05 | 3:45:28 | Federer | 2-4 | Federer |  | 5-5 | 1 ace(s) |
| 11 | 11 | 3:46:17 | 3:49:49 | Djokovic | 4-2 | Djokovic |  | 6-5 | 1 DF |
| 12 | 12 | 3:51:46 | 3:56:54 | Federer | 4-6 | Federer |  | 6-6 | 1 ace(s) |
| 13 | 13 | 3:57:35 | 4:00:00 | Djokovic | 4-1 | Djokovic |  | 7-6 |  |
| 14 | 14 | 4:01:34 | 4:02:57 | Federer | 1-4 | Federer |  | 7-7 | 2 ace(s) |
| 15 | 15 | 4:03:41 | 4:07:16 | Djokovic | 2-4 | Federer | BREAK | 7-8 | 1 BP for Federer |
| 16 | 16 | 4:08:51 | 4:12:40 | Federer | 5-3 | Djokovic | BREAK | 8-8 | 1 BP for Djokovic; 2 ace(s) |
| 17 | 17 | 4:13:27 | 4:17:15 | Djokovic | 4-2 | Djokovic |  | 9-8 |  |
| 18 | 18 | 4:18:51 | 4:21:04 | Federer | 1-4 | Federer |  | 9-9 |  |
| 19 | 19 | 4:22:01 | 4:24:26 | Djokovic | 4-1 | Djokovic |  | 10-9 |  |
| 20 | 20 | 4:26:01 | 4:27:58 | Federer | 1-4 | Federer |  | 10-10 | 1 ace(s) |
| 21 | 21 | 4:28:38 | 4:31:08 | Djokovic | 4-2 | Djokovic |  | 11-10 | 1 ace(s) |
| 22 | 22 | 4:32:38 | 4:34:32 | Federer | 1-4 | Federer |  | 11-11 |  |
| 23 | 23 | 4:35:09 | 4:44:50 | Djokovic | 8-6 | Djokovic |  | 12-11 | 2 BP for Federer |
| 24 | 24 | 4:46:31 | 4:47:47 | Federer | 0-4 | Federer |  | 12-12 | 1 ace(s) |
| 25 | 25 | 4:48:30 | 4:56:59 | Djokovic | 7-3 | Djokovic |  | 13-12 | TIE-BREAK at 12-12 (first ever at this score in a Wimbledon final: see external section) |

Fifth set: 169 points, from 3:00:13 to 4:56:59; points won Djokovic 85, Federer 84.

## T10. The two championship points: Federer serving at 8-7 (set 5, R: SetNo 5, GameNo 16; games 7-8 Dj-Fe before the game; PointServer=2), at 40-15 and 40-30
Whole game (every point):
| pt | clock | score before (Dj-Fe) | serve km/h (no.) | winner | R RallyCount | MCP code -> ending | R flags | TennisVL (n_shots, outcome, hit times) | commentary |
|---|---|---|---|---|---|---|---|---|---|
| 355 | 4:08:51 | 0-0 | 180 (1) | Djokovic | 2 | `4f28f+3d@` -> unforced error | Fe:UnfErr | 3, Roger Federer unforced-error, [14957.52, 14958.24, 14959.44] | tv_2019wimF:0409 (rally, video 14956.5s): "Thank you, players, already. Thank you, ladies and gentlemen. Please. Please. Thank you. He's just …" |
| 356 | 4:09:22 | 15-0 | 143 (2) | Federer | 9 | 1st `4w` (fault), 2nd `4b37b2f3b3s3f3b2f1f1w@` -> unforced error |  | 10, Novak Djokovic unforced-error, [15001.72, 15002.6, 15003.8, 15004.92, 15006.04, 15007.24, 15009.08, 15010.28, 15011.56, 15013.08] | tv_2019wimF:0410 (first_serve_fault, video 14987.3s): "Sorry, Paul." |
| 357 | 4:10:13 | 15-15 | 201 (1) | Federer | 1 | `6*` -> winner | Fe:Ace,Fe:Winner | 1, Roger Federer winner, [15039.36] | tv_2019wimF:0412 (ace, video 15038.3s): "The Federer's 56 aces coming into this match He's served 22 so far against possibly …" |
| 358 | 4:10:35 | 15-30 | 193 (1) | Federer | 1 | `6*` -> winner | Fe:Ace,Fe:Winner | 1, Roger Federer winner, [15061.8] | (no transcribed clip) |
| 359 | 4:10:58 | 15-40 | 151 (2) | Djokovic | 2 | 1st `6n` (fault), 2nd `4f28f3w@` -> unforced error | Fe:UnfErr | 3, Roger Federer unforced-error, [15093.8, 15094.68, 15095.72] | tv_2019wimF:0414 (first_serve_fault, video 15084.0s): "Please."; tv_2019wimF:0415 (rally, video 15092.8s): "Breathe in, breathe out. 40, 30." |
| 360 | 4:11:30 | 30-40 | 193 (1) | Djokovic | 4 | `6r28f+1f1*` -> winner | Dj:Winner,Fe:NetPoint | 4, Novak Djokovic winner, [15116.64, 15117.36, 15118.8, 15119.92] | tv_2019wimF:0416 (rally, video 15115.6s): "And just as Federer passed Djokovic to get the break in the previous game, Djokovic …" |
| 361 | 4:11:58 | 40-40 | 146 (2) | Djokovic | 6 | 1st `4w` (fault), 2nd `5b28b3b3b2f1r#` -> forced error |  | 7, Roger Federer forced-error, [15154.72, 15155.68, 15156.88, 15158.32, 15159.36, 15161.12, 15162.24] | tv_2019wimF:0417 (first_serve_fault, video 15143.5s): "Well done, Dave, to Gilmour Leeds." |
| 362 | 4:12:40 | AD-40 | 189 (1) | Djokovic | 4 | `6r18f1f1f2n@` -> unforced error | Dj:BreakPoint,Dj:BreakPointWon,Dj:BreakPointMissed | 5, Roger Federer unforced-error, [15186.84, 15187.56, 15188.92, 15190.44, 15191.56] | tv_2019wimF:0419 (rally, video 15185.8s): "Amazing, isn't it? That is guts from Djokovic. It almost reminds me of the semi-final, …" |

Full MCP shot codes and TennisVL shot lists of the two championship points and the two break points that followed:
* point 359 (4:10:58, 15-40 Dj-Fe): MCP 1st=`6n` 2nd=`4f28f3w@`; MCP winner Djokovic; R winner Djokovic; R ServeWidth=BW ServeDepth=NCTL ReturnDepth=ND; distance run Dj 11.668 Fe 8.033.
    - TV shot 0 Federer: first serve null  serve-T hit 15085.0s outcome unforced-error (clip 377099_377174.mp4)
    - TV shot 0 Federer: second serve null  serve-wide hit 15093.8s outcome in (clip 377319_377473.mp4)
    - TV shot 1 Djokovic: return forehand ground down the middle hit 15094.68s outcome in (clip 377319_377473.mp4)
    - TV shot 2 Federer: stroke forehand ground inside-out hit 15095.72s outcome unforced-error (clip 377319_377473.mp4)
    - transcript tv_2019wimF:0414 (first_serve_fault, video 15083.96s): "Please."  [full length 1 words]
    - transcript tv_2019wimF:0415 (rally, video 15092.76s): "Breathe in, breathe out. 40, 30."  [full length 6 words]
* point 360 (4:11:30, 30-40 Dj-Fe): MCP 1st=`6r28f+1f1*` 2nd=`-`; MCP winner Djokovic; R winner Djokovic; R ServeWidth=BC ServeDepth=NCTL ReturnDepth=ND; distance run Dj 10.986 Fe 12.436.
    - TV shot 0 Federer: first serve null  serve-T hit 15116.64s outcome in (clip 377890_378049.mp4)
    - TV shot 1 Djokovic: return forehand slice inside-out hit 15117.36s outcome in (clip 377890_378049.mp4)
    - TV shot 2 Federer: stroke forehand ground inside-in hit 15118.8s outcome in (clip 377890_378049.mp4)
    - TV shot 3 Djokovic: stroke forehand ground cross-court hit 15119.92s outcome winner (clip 377890_378049.mp4)
    - transcript tv_2019wimF:0416 (rally, video 15115.60s): "And just as Federer passed Djokovic to get the break in the previous game, Djokovic …"  [full length 24 words]
* point 361 (4:11:58, 40-40 Dj-Fe): MCP 1st=`4w` 2nd=`5b28b3b3b2f1r#`; MCP winner Djokovic; R winner Djokovic; R ServeWidth=B ServeDepth=NCTL ReturnDepth=D; distance run Dj 18.253 Fe 18.374.
    - TV shot 0 Federer: first serve null  serve-wide hit 15144.56s outcome unforced-error (clip 378588_378663.mp4)
    - TV shot 0 Federer: second serve null  serve-body hit 15154.72s outcome in (clip 378842_379104.mp4)
    - TV shot 1 Djokovic: return backhand ground down the middle hit 15155.68s outcome in (clip 378842_379104.mp4)
    - TV shot 2 Federer: stroke backhand ground cross-court hit 15156.88s outcome in (clip 378842_379104.mp4)
    - TV shot 3 Djokovic: stroke backhand ground cross-court hit 15158.32s outcome in (clip 378842_379104.mp4)
    - TV shot 4 Federer: stroke backhand ground down the middle hit 15159.36s outcome in (clip 378842_379104.mp4)
    - TV shot 5 Djokovic: stroke forehand ground cross-court hit 15161.12s outcome in (clip 378842_379104.mp4)
    - TV shot 6 Federer: stroke forehand slice down the line hit 15162.24s outcome forced-error (clip 378842_379104.mp4)
    - transcript tv_2019wimF:0417 (first_serve_fault, video 15143.52s): "Well done, Dave, to Gilmour Leeds."  [full length 6 words]
    - transcript tv_2019wimF:0418 (rally, video 15153.68s): ""  [full length 0 words]
* point 362 (4:12:40, AD-40 Dj-Fe): MCP 1st=`6r18f1f1f2n@` 2nd=`-`; MCP winner Djokovic; R winner Djokovic; R ServeWidth=C ServeDepth=NCTL ReturnDepth=ND; distance run Dj 12.656 Fe 12.465.
    - TV shot 0 Federer: first serve null  serve-T hit 15186.84s outcome in (clip 379645_379839.mp4)
    - TV shot 1 Djokovic: return forehand slice cross-court hit 15187.56s outcome in (clip 379645_379839.mp4)
    - TV shot 2 Federer: stroke forehand ground cross-court hit 15188.92s outcome in (clip 379645_379839.mp4)
    - TV shot 3 Djokovic: stroke forehand ground cross-court hit 15190.44s outcome in (clip 379645_379839.mp4)
    - TV shot 4 Federer: stroke forehand ground cross-court hit 15191.56s outcome unforced-error (clip 379645_379839.mp4)
    - transcript tv_2019wimF:0419 (rally, video 15185.80s): "Amazing, isn't it? That is guts from Djokovic. It almost reminds me of the semi-final, …"  [full length 49 words]

## T11. Breaks of serve in the fifth set (R: GameWinner != PointServer, non-tie-break games)
* Game 6 (set-5 game 6): Federer serving at 3-2 (Dj-Fe); broken by Djokovic; clock 3:22:33 to 3:25:11; games after 4-2.
    - pt 291 3:22:33 0-0 serve 165(2) -> Djokovic; MCP 1st `6d` (fault), 2nd `4f27b2d@` -> unforced error; tv_2019wimF:0323 (rally, video 12183.5s): "Love 15. Definitely a few more half chances flying around in this fifth set."
    - pt 292 3:23:01 15-0 serve 146(2) -> Djokovic; MCP 1st `6d` (fault), 2nd `4b37b1d@` -> unforced error; tv_2019wimF:0325 (rally, video 12218.3s): "Looks more like it."
    - pt 293 3:23:38 30-0 serve 178(1) -> Federer; MCP `4r27f-3m2o1l2d#` -> forced error; tv_2019wimF:0326 (rally, video 12243.7s): "15, 13. Federer boxers virtually on their feet after every point now."
    - pt 294 3:24:06 30-15 serve 146(2) -> Djokovic; MCP 1st `6n` (fault), 2nd `4b38b2d@` -> unforced error; (no transcribed clip)
    - pt 295 3:24:39 40-15 serve 152(2) -> Federer; MCP 1st `6d` (fault), 2nd `5f2n@` -> unforced error; tv_2019wimF:0329 (first_serve_fault, video 12304.5s): "Oh, that's very pushy. Second serve, middle of the box. 95 miles an hour isn't …"
    - pt 296 3:25:11 40-30 serve 156(2) -> Djokovic; MCP 1st `6d` (fault), 2nd `6f39s3b2f+3b3z#` -> forced error; tv_2019wimF:0332 (rally, video 12347.1s): "Federer was in hoping rather than forcing and Djokovic will hit that target this shot …"
* Game 7 (set-5 game 7): Djokovic serving at 4-2 (Dj-Fe); broken by Federer; clock 3:26:14 to 3:31:55; games after 4-3.
    - pt 297 3:26:14 0-0 serve 189(1) -> Federer; MCP `4f28b2b1f2b3b2d#` -> forced error; (no transcribed clip)
    - pt 298 3:26:47 0-15 serve 152(2) -> Djokovic; MCP 1st `6n` (fault), 2nd `4s37b2b1f1f1f2s3b3b3n@` -> unforced error; tv_2019wimF:0334 (first_serve_fault, video 12433.1s): "Oh!"; tv_2019wimF:0335 (rally, video 12446.6s): "She can hardly watch anymore. Who can blame her? Very tense situation now."
    - pt 299 3:27:40 15-15 serve 194(1) -> Federer; MCP `6s38b3n@` -> unforced error; tv_2019wimF:0336 (rally, video 12485.5s): "Oh, he was there."
    - pt 300 3:28:11 15-30 serve 191(1) -> Djokovic; MCP `4s38b3s2f1f3d@` -> unforced error; tv_2019wimF:0337 (rally, video 12517.0s): "It's the right shot, got the forehand to be aggressive. Couldn't quite find the target."
    - pt 301 3:28:48 30-30 serve 0(0) -> Federer; MCP 1st `4w` (fault), 2nd `5n` -> ?; (no transcribed clip)
    - pt 302 3:29:35 30-40 serve 144(2) -> Djokovic; MCP 1st `4d` (fault), 2nd `5s28b3b1f1f1f3b2f2f1d@` -> unforced error; tv_2019wimF:0340 (first_serve_fault, video 12601.2s): "Not easy after the previous second serve."; tv_2019wimF:0341 (rally, video 12618.1s): "Both players are feeling their arms getting heavy. Two of the greatest champions in our …"
    - pt 303 3:30:35 40-40 serve 162(2) -> Federer; MCP 1st `6n` (fault), 2nd `4f28b3s3b2f3b3s1f2f1f1f2f1f3b3s3b3f;3s1f+3*` -> winner; tv_2019wimF:0342 (first_serve_fault, video 12661.2s): "No first serves now for Novak."
    - pt 304 3:31:55 40-AD serve 180(2) -> Federer; MCP 1st `5d` (fault), 2nd `6f37b3s1f2f3b3s3b2f1f3d@` -> unforced error; tv_2019wimF:0345 (rally, video 12755.8s): "It's away! Game on again in the fifth set. That was... a collective holding of …"
* Game 15 (set-5 game 15): Djokovic serving at 7-7 (Dj-Fe); broken by Federer; clock 4:03:41 to 4:07:16; games after 7-8.
    - pt 349 4:03:41 0-0 serve 196(1) -> Djokovic; MCP `6s28f1f1n@` -> unforced error; tv_2019wimF:0401 (rally, video 14646.3s): "safety in love"
    - pt 350 4:04:05 15-0 serve 173(2) -> Djokovic; MCP 1st `4x` (fault), 2nd `5f28b3s3b3f3b3s3b2f3d@` -> unforced error; tv_2019wimF:0403 (rally, video 14683.4s): "What's he complaining about? The call? A little bit louder from the call on the …"
    - pt 351 4:04:54 30-0 serve 151(2) -> Federer; MCP 1st `4n` (fault), 2nd `6s28b2f3b3b1f2f+1f1f-3*` -> winner; tv_2019wimF:0405 (rally, video 14731.0s): "30 15"
    - pt 352 4:05:50 30-15 serve 188(1) -> Federer; MCP `5s28f3s3b3b3b3f2f3s2f3s1f1f1f2d@` -> unforced error; (no transcribed clip)
    - pt 353 4:06:42 30-30 serve 181(1) -> Federer; MCP `4f18f3w@` -> unforced error; tv_2019wimF:0407 (rally, video 14824.4s): "Federer soaking up the pressure changing the pace using the slice back and down the …"
    - pt 354 4:07:16 30-40 serve 194(1) -> Federer; MCP `4s27f+1f1*` -> winner; tv_2019wimF:0408 (rally, video 14861.4s): "Yeah, and that's the break."
* Game 16 (set-5 game 16): Federer serving at 7-8 (Dj-Fe); broken by Djokovic; clock 4:08:51 to 4:12:40; games after 8-8.
    - pt 355 4:08:51 0-0 serve 180(1) -> Djokovic; MCP `4f28f+3d@` -> unforced error; tv_2019wimF:0409 (rally, video 14956.5s): "Thank you, players, already. Thank you, ladies and gentlemen. Please. Please. Thank you. He's just …"
    - pt 356 4:09:22 15-0 serve 143(2) -> Federer; MCP 1st `4w` (fault), 2nd `4b37b2f3b3s3f3b2f1f1w@` -> unforced error; tv_2019wimF:0410 (first_serve_fault, video 14987.3s): "Sorry, Paul."
    - pt 357 4:10:13 15-15 serve 201(1) -> Federer; MCP `6*` -> winner; tv_2019wimF:0412 (ace, video 15038.3s): "The Federer's 56 aces coming into this match He's served 22 so far against possibly …"
    - pt 358 4:10:35 15-30 serve 193(1) -> Federer; MCP `6*` -> winner; (no transcribed clip)
    - pt 359 4:10:58 15-40 serve 151(2) -> Djokovic; MCP 1st `6n` (fault), 2nd `4f28f3w@` -> unforced error; tv_2019wimF:0414 (first_serve_fault, video 15084.0s): "Please."; tv_2019wimF:0415 (rally, video 15092.8s): "Breathe in, breathe out. 40, 30."
    - pt 360 4:11:30 30-40 serve 193(1) -> Djokovic; MCP `6r28f+1f1*` -> winner; tv_2019wimF:0416 (rally, video 15115.6s): "And just as Federer passed Djokovic to get the break in the previous game, Djokovic …"
    - pt 361 4:11:58 40-40 serve 146(2) -> Djokovic; MCP 1st `4w` (fault), 2nd `5b28b3b3b2f1r#` -> forced error; tv_2019wimF:0417 (first_serve_fault, video 15143.5s): "Well done, Dave, to Gilmour Leeds."
    - pt 362 4:12:40 AD-40 serve 189(1) -> Djokovic; MCP `6r18f1f1f2n@` -> unforced error; tv_2019wimF:0419 (rally, video 15185.8s): "Amazing, isn't it? That is guts from Djokovic. It almost reminds me of the semi-final, …"

## T12. The 12-12 tie-break (R: SetNo 5, GameNo 25), point by point with the clock
| pt | clock | score before (Dj-Fe) | server | serve km/h (no.) | winner | R RallyCount | MCP shots | MCP code -> ending | R flags | commentary |
|---|---|---|---|---|---|---|---|---|---|---|
| 413 | 4:48:30 | 0-0 | Djokovic | 168 (2) | Djokovic | 11 | 12 | 1st `6d` (fault), 2nd `4f28b2s3s2f3b3b2f3s2b3b2d@` -> unforced error | Fe:UnfErr | tv_2019wimF:0480 (rally, video 17349.3s): "1-0 Djokovic. Djokovic has won the two tie breaks that have been played between these …" |
| 414 | 4:49:29 | 1-0 | Federer | 193 (1) | Federer | 3 | 3 | `6f37f1*` -> winner | Fe:Winner | (no transcribed clip) |
| 415 | 4:50:01 | 1-1 | Federer | 180 (1) | Djokovic | 2 | 3 | `4+f27h1w#` -> forced error | Fe:NetPoint | (no transcribed clip) |
| 416 | 4:50:37 | 2-1 | Djokovic | 140 (2) | Djokovic | 3 | 4 | 1st `5d` (fault), 2nd `4s28f1f1w#` -> forced error |  | (no transcribed clip) |
| 417 | 4:51:25 | 3-1 | Djokovic | 180 (1) | Djokovic | 7 | 8 | `4f19f3s3b3b3b1f1w#` -> forced error |  | (no transcribed clip) |
| 418 | 4:52:04 | 4-1 | Federer | 156 (2) | Federer | 11 | 11 | 1st `4n` (fault), 2nd `6f38b3b;1f3b3b3b3b2f2u+3*` -> winner | Fe:Winner | (no transcribed clip) |
| 419 | 4:53:31 | 4-2 | Federer | 154 (2) | Federer | 1 | 2 | 1st `6w` (fault), 2nd `6b#` -> forced error |  | (no transcribed clip) |
| 420 | 4:54:18 | 4-3 | Djokovic | 194 (1) | Djokovic | 3 | 3 | `6f27f1*` -> winner | Dj:Winner | (no transcribed clip) |
| 421 | 4:54:48 | 5-3 | Djokovic | 151 (2) | Djokovic | 13 | 13 | 1st `5n` (fault), 2nd `4f38b3s3b3b3b3b3b3f3b3f3b1*` -> winner | Dj:Winner | (no transcribed clip) |
| 422 | 4:56:59 | 6-3 | Federer | 143 (2) | Djokovic | 2 | 3 | 1st `6d` (fault), 2nd `5b38f!@` -> unforced error | Fe:UnfErr | (no transcribed clip) |
Tie-break first point 4:48:30, last point 4:56:59; 10 points; game winner Djokovic; set winner Djokovic.

## T13. The final point
Point 422: clock 4:56:59; score before 6-3 (Dj-Fe) in the tie-break, games 12-12; server Federer, serve 143 km/h (89 mph), serve number 2 (ServeWidth BW, ServeDepth NCTL, ReturnDepth ND); winner Djokovic; R RallyCount 2; R flags: P2UnfErr=1 (Federer unforced error); MCP 1st=`6d` 2nd=`5b38f!@` -> 1st `6d` (fault), 2nd `5b38f!@` -> unforced error; MCP shots 3; distance run Dj 4.624 Fe 4.347.

## T14. Transcript coverage (T)
481 clip records; 318 with non-empty text_corrected; first clip starts at video 65.04 s (point 3), last clip at 17349.28 s. Words (text_corrected): 9693.
The clips are rally/serve clips only: there is no footage or transcript of the walk-on, warm-up, coin toss or trophy ceremony in this corpus (see search results below).

## T15. Keyword search in text_corrected (typical-scene material). Excerpt <= 15 words around the first hit; score_before and clock from the record.
### walk-on / warm-up / toss / umpire: 3 clip(s)
* tv_2019wimF:0017 clip_i 17 video 604.0s, PBP pt 17, clock 0:09:28, s1 1-2 0-15 (Dj-Fe) srv Djokovic: "nothing instant about the challenge but Damien Steiner in the chair is allowing it the …"
* tv_2019wimF:0124 clip_i 124 video 4754.4s, PBP pt 117, clock 1:18:38, s2 1-4 0-15 (Dj-Fe) srv Federer: "50 not. Sun came out just for that ball toss."
* tv_2019wimF:0278 clip_i 278 video 10839.0s, PBP pt 254, clock 3:00:13, s5 0-0 0-0 (Dj-Fe) srv Djokovic: "… serve on the wrong side before the umpire told him you finished on the other …"
### Royal Box / royalty / celebrities: 9 clip(s)
* tv_2019wimF:0099 clip_i 99 video 3980.3s, PBP pt 98, clock 1:05:55, s2 0-1 30-40 (Dj-Fe) srv Federer: "… they're on their feet in the Federer box, because losing the first set to Djokovic …"
* tv_2019wimF:0155 clip_i 155 video 5704.8s, PBP pt 140, clock 1:34:40, s3 1-1 0-40 (Dj-Fe) srv Federer: "… or 40 yards beyond that is the royal box and Philbrook the chairman who's in …"
* tv_2019wimF:0226 clip_i 226 video 8830.2s, PBP pt 211, clock 2:26:44, s4 1-1 15-0 (Dj-Fe) srv Djokovic: "Judging by the size of the player box up there for Roger Federer. With Leo …"
* tv_2019wimF:0237 clip_i 237 video 9138.4s, PBP pt 220, clock 2:31:53, s4 2-1 40-40 (Dj-Fe) srv Federer: "… Djokovic's reaction, he's looking up at his box and just saying, how's this guy do …"
* tv_2019wimF:0277 clip_i 277 video 10533.8s, PBP pt 253, clock 2:55:08, s4 4-5 0-40 (Dj-Fe) srv Federer: "… are here on an excellent ticket. The Royal Portrush Club is hosting the Open. That'll …"
* tv_2019wimF:0297 clip_i 297 video 11316.0s, PBP pt 268, clock 3:07:58, s5 1-1 30-15 (Dj-Fe) srv Djokovic: "… theatrical. He's becoming quite animated towards his box at the moment. He's reaching out. A …"
* tv_2019wimF:0329 clip_i 329 video 12304.5s, PBP pt 295, clock 3:24:39, s5 3-2 40-15 (Dj-Fe) srv Federer: "… very pushy. Second serve, middle of the box. 95 miles an hour isn't really... Sometimes …"
* tv_2019wimF:0345 clip_i 345 video 12755.8s, PBP pt 304, clock 3:31:55, s5 4-2 40-AD (Dj-Fe) srv Djokovic: "… errors at the end. I thought the Royal Box was meant to be impartial. Did …"
* tv_2019wimF:0387 clip_i 387 video 14240.1s, PBP pt 338, clock 3:56:54, s5 6-5 40-AD (Dj-Fe) srv Federer: "… she's supporting i don't speak for the duchess Halfway to a final set tiebreaker. 12-0. …"
### crowd: 10 clip(s)
* tv_2019wimF:0063 clip_i 63 video 2094.8s, PBP pt 55, clock 0:34:29, s1 4-4 30-40 (Dj-Fe) srv Federer: "… of the other stars. They're true tennis fans. I love to People really take a …"
* tv_2019wimF:0079 clip_i 79 video 2658.2s, PBP pt 68, clock 0:44:03, s1 5-5 30-30 (Dj-Fe) srv Federer: "… well is really not that easy. The crowd is really engaging in the match now."
* tv_2019wimF:0090 clip_i 90 video 3708.4s, PBP pt 90, clock 1:01:24, s2 0-0 15-15 (Dj-Fe) srv Djokovic: "… word of wisdom for all the Federer fans out there. He's playing great. He should …"
* tv_2019wimF:0196 clip_i 196 video 7252.3s, PBP pt 178, clock 2:00:17, s3 4-5 AD-40 (Dj-Fe) srv Djokovic: "… not reacting he'll feel baited by the crowd to a point for the first time …"
* tv_2019wimF:0248 clip_i 248 video 9511.7s, PBP pt 227, clock 2:38:06, s4 2-3 0-0 (Dj-Fe) srv Federer: "… number one, the defending champion, and everyone's cheering for the other guy always. To say …"
* tv_2019wimF:0277 clip_i 277 video 10533.8s, PBP pt 253, clock 2:55:08, s4 4-5 0-40 (Dj-Fe) srv Federer: "It's a whole to love the crowd rise and we have a fifth and deciding …"
* tv_2019wimF:0300 clip_i 300 video 11397.4s, PBP pt 270, clock 3:09:20, s5 1-1 40-30 (Dj-Fe) srv Djokovic: "… finds the angles. It's where again the crowd can play a part. Can really lift …"
* tv_2019wimF:0345 clip_i 345 video 12755.8s, PBP pt 304, clock 3:31:55, s5 4-2 40-AD (Dj-Fe) srv Djokovic: "… you. Back on, Sir. At first the crowd has to relax a little. Please, ladies …"
* tv_2019wimF:0427 clip_i 427 video 15556.4s, PBP pt 369, clock 4:18:51, s5 9-8 0-0 (Dj-Fe) srv Federer: "… cannot afford to be as deflated as the crowd seem to be at the moment."
* tv_2019wimF:0477 clip_i 477 video 17272.4s, PBP pt 411, clock 4:47:27, s5 12-11 0-30 (Dj-Fe) srv Federer: "… don't think this will come as news to the crowd but it might to some."
### weather / roof / sun / shadow / wind / heat: 4 clip(s)
* tv_2019wimF:0124 clip_i 124 video 4754.4s, PBP pt 117, clock 1:18:38, s2 1-4 0-15 (Dj-Fe) srv Federer: "50 not. Sun came out just for that ball toss."
* tv_2019wimF:0155 clip_i 155 video 5704.8s, PBP pt 140, clock 1:34:40, s3 1-1 0-40 (Dj-Fe) srv Federer: "… one court, which has had the new roof celebrated in the last couple of months. …"
* tv_2019wimF:0200 clip_i 200 video 7364.7s, PBP pt 182, clock 2:02:19, s3 5-5 0-40 (Dj-Fe) srv Federer: "… has been phenomenal no need for the roof during this championship apart from two finish …"
* tv_2019wimF:0373 clip_i 373 video 13789.2s, PBP pt 327, clock 3:49:23, s5 5-5 30-30 (Dj-Fe) srv Djokovic: "… of the court, southern end where the sun is getting lower. Not so easy to …"
### trophy / ceremony / presentation: 0 clip(s)
### history / records / titles: 12 clip(s)
* tv_2019wimF:0002 clip_i 2 video 100.1s, PBP pt 5, clock 0:01:14, s1 0-0 15-40 (Dj-Fe) srv Federer: "… Grand Slams earlier on. First player in history. We're back. First man to win 100 …"
* tv_2019wimF:0224 clip_i 224 video 8774.6s, PBP pt 209, clock 2:25:49, s4 1-0 30-40 (Dj-Fe) srv Federer: "… players, obviously well rewarded over the years, both at or over £100,000,000 in. Prize money."
* tv_2019wimF:0227 clip_i 227 video 8869.7s, PBP pt 212, clock 2:27:24, s4 1-1 30-0 (Dj-Fe) srv Djokovic: "After his semi final victory over Rafa Nadal. They were singing him happy birthday, the …"
* tv_2019wimF:0229 clip_i 229 video 8987.0s, PBP pt 214, clock 2:29:21, s4 2-1 0-0 (Dj-Fe) srv Djokovic: "… love to win. They love to add another Wimbledon title to their resume. 15 love."
* tv_2019wimF:0230 clip_i 230 video 8995.2s, PBP pt None, clock -, s4 2-1 0-0 (Dj-Fe) srv Federer: "… there's still a debate out there who will end up with most Grand Slam titles."
* tv_2019wimF:0270 clip_i 270 video 10178.2s, PBP pt 244, clock 2:49:12, s4 2-5 AD-40 (Dj-Fe) srv Djokovic: "… That is news. And after losing the longest rally of the match in such spectacular …"
* tv_2019wimF:0284 clip_i 284 video 10980.4s, PBP pt 258, clock 3:02:24, s5 0-0 40-15 (Dj-Fe) srv Djokovic: "… Serbian. First game, final second. Five set record in their careers. Djokovic has won 29 …"
* tv_2019wimF:0364 clip_i 364 video 13502.1s, PBP pt 320, clock 3:44:27, s5 5-4 15-30 (Dj-Fe) srv Federer: "… hours and 45 minutes later, we're tired watching it. Djokovic, two points from the title."
* tv_2019wimF:0430 clip_i 430 video 15632.0s, PBP pt 371, clock 4:19:56, s5 9-8 15-15 (Dj-Fe) srv Federer: "… of the championships 2019, it's also the longest. That's fitting. Seeds one and two going …"
* tv_2019wimF:0458 clip_i 458 video 16477.3s, PBP pt 393, clock 4:34:12, s5 11-10 15-30 (Dj-Fe) srv Federer: "Well, this is now brutal physically. 100 minutes mostly of excellence certainly of tension in …"
* tv_2019wimF:0474 clip_i 474 video 17115.3s, PBP pt 408, clock 4:44:50, s5 11-11 AD-40 (Dj-Fe) srv Djokovic: "… to the full. We're into the second longest Wimbledon final. enjoying every minute of it …"
* tv_2019wimF:0477 clip_i 477 video 17272.4s, PBP pt 411, clock 4:47:27, s5 12-11 0-30 (Dj-Fe) srv Federer: "… four hours and 48 minutes matching the longest final of all time, Federer serves an …"
### rituals: new balls, towel, ball kids, changeover, racket: 7 clip(s)
* tv_2019wimF:0050 clip_i 50 video 1734.0s, PBP pt None, clock -, s1 3-4 0-0 (Dj-Fe) srv Djokovic: "15 love. Novak serving with new balls. Going to speed up the serve a little …"
* tv_2019wimF:0215 clip_i 215 video 8565.9s, PBP pt 203, clock 2:22:20, s4 0-0 40-15 (Dj-Fe) srv Djokovic: "Djokovic, new balls please. First game, 4-7. Dangerous times now for Federer. Was it Michael …"
* tv_2019wimF:0360 clip_i 360 video 13410.8s, PBP pt 317, clock 3:43:05, s5 5-4 0-0 (Dj-Fe) srv Federer: "Another very quick point by Federer. Probably using the new balls there to come in …"
* tv_2019wimF:0361 clip_i 361 video 13448.5s, PBP pt 318, clock 3:43:43, s5 5-4 15-0 (Dj-Fe) srv Federer: "… line? Could have been a real unlucky bounce for Roger. Don't forget all the time …"
* tv_2019wimF:0383 clip_i 383 video 14134.6s, PBP pt 335, clock 3:54:44, s5 6-5 40-40 (Dj-Fe) srv Federer: "That was a very gutsy forehand on a difficult low bouncing ball."
* tv_2019wimF:0422 clip_i 422 video 15305.6s, PBP pt 365, clock 4:14:40, s5 8-8 30-0 (Dj-Fe) srv Djokovic: "… Boris. Well and what a time to string seven points in a row. Facing two …"
* tv_2019wimF:0435 clip_i 435 video 15757.1s, PBP pt 374, clock 4:22:01, s5 9-9 0-0 (Dj-Fe) srv Djokovic: "sometimes not always easy to control those new balls flying through the air a little …"
### line calls / challenge / Hawk-Eye / umpire calls: 22 clip(s)
* tv_2019wimF:0014 clip_i 14 video 443.5s, PBP pt 15, clock 0:06:58, s1 1-1 30-40 (Dj-Fe) srv Federer: "… well, serving consistently, and... These are the challenges. These baseline exchanges over a long period …"
* tv_2019wimF:0017 clip_i 17 video 604.0s, PBP pt 17, clock 0:09:28, s1 1-2 0-15 (Dj-Fe) srv Djokovic: "nothing instant about the challenge but Damien Steiner in the chair is allowing it the …"
* tv_2019wimF:0038 clip_i 38 video 1235.4s, PBP pt 35, clock 0:20:15, s1 2-2 30-40 (Dj-Fe) srv Federer: "… was in Johannesburg. I got a phone call. He just lost his number one ranking …"
* tv_2019wimF:0059 clip_i 59 video 2002.8s, PBP pt 52, clock 0:32:57, s1 4-4 0-30 (Dj-Fe) srv Federer: "Mr. Djokovic is charging the call-up service line. Ball was called in."
* tv_2019wimF:0073 clip_i 73 video 2509.2s, PBP pt 64, clock 0:41:23, s1 5-5 0-0 (Dj-Fe) srv Federer: "Please. Please. Mr. Djokovic is having a call right past the line. Ball was called. …"
* tv_2019wimF:0074 clip_i 74 video 2540.4s, PBP pt 65, clock 0:41:55, s1 5-5 0-15 (Dj-Fe) srv Federer: "Mr. Djokovic has one challenge remaining. Wait, please."
* tv_2019wimF:0121 clip_i 121 video 4614.1s, PBP pt 115, clock 1:16:32, s2 0-4 40-30 (Dj-Fe) srv Djokovic: "… is the day to show them, to let it all out. This blood was built …"
* tv_2019wimF:0139 clip_i 139 video 5327.5s, PBP pt 128, clock 1:28:22, s3 0-0 15-15 (Dj-Fe) srv Federer: "… a goal, left centre service line, ball was called out. There we go, one millimetre."
* tv_2019wimF:0140 clip_i 140 video 5353.2s, PBP pt 128, clock 1:28:22, s3 0-0 15-15 (Dj-Fe) srv Federer: "And up goes the statistics for Challenging. 13.15, Mr. Federer has two challenges remaining."
* tv_2019wimF:0245 clip_i 245 video 9331.1s, PBP pt 225, clock 2:35:05, s4 2-2 15-30 (Dj-Fe) srv Djokovic: "The call didn't come. What do you think, Boris? Awfully close. I'm taking the fifth. …"
* tv_2019wimF:0248 clip_i 248 video 9511.7s, PBP pt 227, clock 2:38:06, s4 2-3 0-0 (Dj-Fe) srv Federer: "… now. Novak. Put a chin chucker down it's. call for her. I find it boiling."
* tv_2019wimF:0263 clip_i 263 video 9962.7s, PBP pt 239, clock 2:45:27, s4 2-5 15-15 (Dj-Fe) srv Federer: "30 15 Mr. Federer has two challenges remaining"
* … 10 more
### Boris: 18 clip(s)
* tv_2019wimF:0014 clip_i 14 video 443.5s, PBP pt 15, clock 0:06:58, s1 1-1 30-40 (Dj-Fe) srv Federer: "… will be in favor of Djokovic. And Boris, we would, with each other, for the …"
* tv_2019wimF:0032 clip_i 32 video 1068.4s, PBP pt 28, clock 0:17:23, s1 1-2 40-40 (Dj-Fe) srv Djokovic: "I'll get Boris Becker to introduce the full Djokovic camp in a few minutes at …"
* tv_2019wimF:0038 clip_i 38 video 1235.4s, PBP pt 35, clock 0:20:15, s1 2-2 30-40 (Dj-Fe) srv Federer: "Boris, how long were you with Novak? Three and a half years. Three and a …"
* tv_2019wimF:0063 clip_i 63 video 2094.8s, PBP pt 55, clock 0:34:29, s1 4-4 30-40 (Dj-Fe) srv Federer: "… I mean he played Wimbledon last century Boris No, he's done everything there is to …"
* tv_2019wimF:0081 clip_i 81 video 2733.9s, PBP pt 70, clock 0:45:08, s1 5-5 40-40 (Dj-Fe) srv Federer: "… up opportunities where they can dictate Again, Boris mentioned it in the semifinals, Federer and …"
* tv_2019wimF:0121 clip_i 121 video 4614.1s, PBP pt 115, clock 1:16:32, s2 0-4 40-30 (Dj-Fe) srv Djokovic: "… differ from other matches in the tournament, Boris? Well, it's the last one there is. …"
* tv_2019wimF:0137 clip_i 137 video 5282.1s, PBP pt 126, clock 1:27:28, s3 0-0 0-0 (Dj-Fe) srv Federer: "… left it off. Are you slightly surprised, Boris, at the end of the second set …"
* tv_2019wimF:0166 clip_i 166 video 6156.0s, PBP pt 149, clock 1:42:10, s3 2-2 15-30 (Dj-Fe) srv Federer: "How do you know that, Boris? Because he's asking me all the time. What, where …"
* tv_2019wimF:0173 clip_i 173 video 6407.2s, PBP pt 155, clock 1:46:21, s3 2-3 40-15 (Dj-Fe) srv Djokovic: "… the first set. What do you think, Boris? Halfway, you think we're heading to another …"
* tv_2019wimF:0217 clip_i 217 video 8627.3s, PBP pt 204, clock 2:23:13, s4 1-0 0-0 (Dj-Fe) srv Federer: "… can say Michael stick just at the moment because Boris is taking a loop rope."
* tv_2019wimF:0227 clip_i 227 video 8869.7s, PBP pt 212, clock 2:27:24, s4 1-1 30-0 (Dj-Fe) srv Djokovic: "… sets. And by two sets to one. Boris, it may be a little bit vulgar …"
* tv_2019wimF:0242 clip_i 242 video 9258.1s, PBP pt 223, clock 2:33:40, s4 2-2 0-15 (Dj-Fe) srv Djokovic: "… a drop shot? Great shot from Djokovic. Boris quite rightly said Djokovic not so happy …"
* … 6 more
### Tim: 7 clip(s)
* tv_2019wimF:0014 clip_i 14 video 443.5s, PBP pt 15, clock 0:06:58, s1 1-1 30-40 (Dj-Fe) srv Federer: "… by two games to one per set. Tim, Federer is going to have to play. …"
* tv_2019wimF:0081 clip_i 81 video 2733.9s, PBP pt 70, clock 0:45:08, s1 5-5 40-40 (Dj-Fe) srv Federer: "… of it but this is more artistry tim than than just bludgeoning there's so much …"
* tv_2019wimF:0119 clip_i 119 video 4552.9s, PBP pt 113, clock 1:15:17, s2 0-4 30-15 (Dj-Fe) srv Djokovic: "… 2012. And that's the last of my research, Tim. Out! You know what? No. 40-30."
* tv_2019wimF:0167 clip_i 167 video 6177.8s, PBP pt 150, clock 1:42:32, s3 2-2 15-40 (Dj-Fe) srv Federer: "… don't see a Djokovic return today. Now, Tim, you have played Roger Federer. You've been …"
* tv_2019wimF:0200 clip_i 200 video 7364.7s, PBP pt 182, clock 2:02:19, s3 5-5 0-40 (Dj-Fe) srv Federer: "just to back up what Tim Henman was just saying there Federer's first percentage pretty …"
* tv_2019wimF:0275 clip_i 275 video 10352.0s, PBP pt 249, clock 2:52:06, s4 3-5 40-15 (Dj-Fe) srv Djokovic: "… Lost to the gentleman on my left, Tim Henman. And then 2003, of course, the …"
* tv_2019wimF:0426 clip_i 426 video 15460.8s, PBP pt 368, clock 4:17:15, s5 8-8 40-30 (Dj-Fe) srv Djokovic: "… this is why we love five sets Tim it's incredible I'm still in a slight …"
### grass / court / lines / net: 50 clip(s)
* tv_2019wimF:0009 clip_i 9 video 302.0s, PBP pt 10, clock 0:04:28, s1 1-1 0-0 (Dj-Fe) srv Federer: "… the great Swiss stays close to the baseline, plays a short point, tries to be …"
* tv_2019wimF:0014 clip_i 14 video 443.5s, PBP pt 15, clock 0:06:58, s1 1-1 30-40 (Dj-Fe) srv Federer: "… consistently, and... These are the challenges. These baseline exchanges over a long period of time, …"
* tv_2019wimF:0021 clip_i 21 video 739.9s, PBP pt 20, clock 0:11:54, s1 1-2 40-15 (Dj-Fe) srv Djokovic: "The Djokovic down the line backhand doesn't achieve the right length or it's too far …"
* tv_2019wimF:0025 clip_i 25 video 854.6s, PBP pt 23, clock 0:13:49, s1 1-2 AD-40 (Dj-Fe) srv Djokovic: "… no man's land in between the service line and he really was forced to come …"
* tv_2019wimF:0031 clip_i 31 video 1025.7s, PBP pt None, clock -, s1 1-2 40-AD (Dj-Fe) srv Federer: "… How interesting. It stays low on a grass court. It skids through, tempting him, tempting …"
* tv_2019wimF:0033 clip_i 33 video 1093.2s, PBP pt 29, clock 0:17:48, s1 1-2 AD-40 (Dj-Fe) srv Djokovic: "… the pace, trying to lure Djokovic in and Novak wants to rally from the baseline."
* tv_2019wimF:0047 clip_i 47 video 1561.3s, PBP pt 42, clock 0:25:36, s1 3-3 0-15 (Dj-Fe) srv Federer: "… at 79% of first serves in the court. Giving Djokovic very few looks at second …"
* tv_2019wimF:0053 clip_i 53 video 1794.6s, PBP pt 47, clock 0:29:29, s1 3-4 30-0 (Dj-Fe) srv Djokovic: "… chip in charge. I'm so underappreciated on grass these days. Everybody wants to stay back …"
* tv_2019wimF:0059 clip_i 59 video 2002.8s, PBP pt 52, clock 0:32:57, s1 4-4 0-30 (Dj-Fe) srv Federer: "Mr. Djokovic is charging the call-up service line. Ball was called in."
* tv_2019wimF:0063 clip_i 63 video 2094.8s, PBP pt 55, clock 0:34:29, s1 4-4 30-40 (Dj-Fe) srv Federer: "… to do in this sport Interesting clothing line here with a see even is a …"
* tv_2019wimF:0067 clip_i 67 video 2252.3s, PBP pt 57, clock 0:36:54, s1 4-5 0-15 (Dj-Fe) srv Djokovic: "… final touch the delicacy and then it hit the line which gave Djokovic no chance"
* tv_2019wimF:0072 clip_i 72 video 2459.0s, PBP pt 63, clock 0:40:33, s1 4-5 AD-40 (Dj-Fe) srv Djokovic: "… love 30 down the backhand down the line for the recovery to his backhand side …"
* … 38 more
### serve / ace / second serve: 52 clip(s)
* tv_2019wimF:0002 clip_i 2 video 100.1s, PBP pt 5, clock 0:01:14, s1 0-0 15-40 (Dj-Fe) srv Federer: "… by beating Kei Nishikori. Novak Djokovic to serve. We're settling into something that he's done …"
* tv_2019wimF:0014 clip_i 14 video 443.5s, PBP pt 15, clock 0:06:58, s1 1-1 30-40 (Dj-Fe) srv Federer: "… the ground running, timing the ball well, serving consistently, and... These are the challenges. These …"
* tv_2019wimF:0023 clip_i 23 video 798.2s, PBP pt 21, clock 0:12:39, s1 1-2 40-30 (Dj-Fe) srv Djokovic: "… to watch out for Federer on second serve whether he'll look to run round and …"
* tv_2019wimF:0026 clip_i 26 video 887.3s, PBP pt 24, clock 0:14:22, s1 1-2 40-40 (Dj-Fe) srv Djokovic: "Body serve. Into Roger. Djokovic needs to find a few more first serves only at …"
* tv_2019wimF:0036 clip_i 36 video 1201.6s, PBP pt 33, clock 0:19:36, s1 2-2 30-15 (Dj-Fe) srv Federer: "… love. That's what Roger does so well. Serve excellent under pressure. And that's three first …"
* tv_2019wimF:0047 clip_i 47 video 1561.3s, PBP pt 42, clock 0:25:36, s1 3-3 0-15 (Dj-Fe) srv Federer: "… to have an impact he needed to serve well, he's at 79% of first serves …"
* tv_2019wimF:0050 clip_i 50 video 1734.0s, PBP pt None, clock -, s1 3-4 0-0 (Dj-Fe) srv Djokovic: "15 love. Novak serving with new balls. Going to speed up the serve a little …"
* tv_2019wimF:0062 clip_i 62 video 2060.7s, PBP pt 54, clock 0:33:55, s1 4-4 15-40 (Dj-Fe) srv Federer: "… Roger doesn't put it enough on the serve. Novak steps right into it. And forces …"
* tv_2019wimF:0065 clip_i 65 video 2201.6s, PBP pt 56, clock 0:36:03, s1 4-5 0-0 (Dj-Fe) srv Djokovic: "… statement on the first point with Djokovic serving to stay in the first set at …"
* tv_2019wimF:0083 clip_i 83 video 2866.6s, PBP pt 72, clock 0:47:21, s1 5-6 0-0 (Dj-Fe) srv Djokovic: "Djokovic has picked up his serve a little."
* tv_2019wimF:0098 clip_i 98 video 3952.8s, PBP pt 97, clock 1:05:27, s2 0-1 30-30 (Dj-Fe) srv Federer: "… play from Federer, the one-two punch, good serve out wide, opens up the court to …"
* tv_2019wimF:0126 clip_i 126 video 4780.0s, PBP pt 118, clock 1:19:05, s2 1-4 15-15 (Dj-Fe) srv Federer: "… has established a foothold by winning his serve and you know if he can get …"
* … 40 more
### break / championship point / match point: 13 clip(s)
* tv_2019wimF:0029 clip_i 29 video 958.4s, PBP pt 26, clock 0:15:23, s1 1-2 40-40 (Dj-Fe) srv Djokovic: "Just over a quarter of an hour played and Federer with the first break point."
* tv_2019wimF:0071 clip_i 71 video 2425.3s, PBP pt 62, clock 0:40:03, s1 4-5 40-40 (Dj-Fe) srv Djokovic: "Djokovic had to work so hard to recover to his backhand side to retrieve the …"
* tv_2019wimF:0215 clip_i 215 video 8565.9s, PBP pt 203, clock 2:22:20, s4 0-0 40-15 (Dj-Fe) srv Djokovic: "Djokovic, new balls please. First game, 4-7. Dangerous times now for Federer. Was it Michael …"
* tv_2019wimF:0266 clip_i 266 video 10031.4s, PBP pt 241, clock 2:46:46, s4 2-5 30-30 (Dj-Fe) srv Federer: "2 hours and 47 minutes into this final approaching 5 o'clock local time in the …"
* tv_2019wimF:0319 clip_i 319 video 12017.2s, PBP pt 288, clock 3:19:52, s5 2-2 40-30 (Dj-Fe) srv Djokovic: "And now, from 41 cruising, Novak Djokovic. Suddenly under some pressure on his serve. Yes. …"
* tv_2019wimF:0328 clip_i 328 video 12280.8s, PBP pt None, clock -, s5 3-2 30-15 (Dj-Fe) srv Djokovic: "Well they're on their feet and Federer began to look like he's a bit out …"
* tv_2019wimF:0416 clip_i 416 video 15115.6s, PBP pt 360, clock 4:11:30, s5 7-8 30-40 (Dj-Fe) srv Federer: "And just as Federer passed Djokovic to get the break in the previous game, Djokovic …"
* tv_2019wimF:0420 clip_i 420 video 15232.6s, PBP pt 363, clock 4:13:27, s5 8-8 0-0 (Dj-Fe) srv Djokovic: "Five strike points for Djokovic. It's going to be difficult to erase the memory of …"
* tv_2019wimF:0422 clip_i 422 video 15305.6s, PBP pt 365, clock 4:14:40, s5 8-8 30-0 (Dj-Fe) srv Djokovic: "He's got to be so relieved Boris. Well and what a time to string seven …"
* tv_2019wimF:0426 clip_i 426 video 15460.8s, PBP pt 368, clock 4:17:15, s5 8-8 40-30 (Dj-Fe) srv Djokovic: "Djokovic finding the mark just when he needed to he takes the lead 9-8 he …"
* tv_2019wimF:0466 clip_i 466 video 16742.1s, PBP pt 401, clock 4:38:36, s5 11-11 40-40 (Dj-Fe) srv Djokovic: "How was it? He didn't out. Mr. Federer is challenging Nicole Lefarbo. Oh, it's called …"
* tv_2019wimF:0472 clip_i 472 video 17032.5s, PBP pt 406, clock 4:43:27, s5 11-11 40-AD (Dj-Fe) srv Federer: "If he's wrong, he loses the point. He is wrong. Federer has found the outside …"
* … 1 more
### time / clock / hours / length: 28 clip(s)
* tv_2019wimF:0014 clip_i 14 video 443.5s, PBP pt 15, clock 0:06:58, s1 1-1 30-40 (Dj-Fe) srv Federer: "… would it? It was 6-1 in 20 minutes, but again, what's amazing, even early in …"
* tv_2019wimF:0029 clip_i 29 video 958.4s, PBP pt 26, clock 0:15:23, s1 1-2 40-40 (Dj-Fe) srv Djokovic: "Just over a quarter of an hour played and Federer with the first break point."
* tv_2019wimF:0032 clip_i 32 video 1068.4s, PBP pt 28, clock 0:17:23, s1 1-2 40-40 (Dj-Fe) srv Djokovic: "… to introduce the full Djokovic camp in a few minutes at the next change event."
* tv_2019wimF:0077 clip_i 77 video 2582.3s, PBP pt 66, clock 0:42:28, s1 5-5 15-15 (Dj-Fe) srv Federer: "… a third time in the last 10 minutes and this one spotted by Djokovic spotted …"
* tv_2019wimF:0084 clip_i 84 video 2918.2s, PBP pt 74, clock 0:48:13, s1 5-6 30-0 (Dj-Fe) srv Djokovic: "… tennis with us here. This next 7, 8, 10 minutes is going to be superb."
* tv_2019wimF:0099 clip_i 99 video 3980.3s, PBP pt 98, clock 1:05:55, s2 0-1 30-40 (Dj-Fe) srv Federer: "… first set to Djokovic for over an hour in a major championship final when you …"
* tv_2019wimF:0108 clip_i 108 video 4285.7s, PBP pt 104, clock 1:10:51, s2 0-3 0-0 (Dj-Fe) srv Federer: "amazing how you have 58 minutes of the first set that's so intense such a …"
* tv_2019wimF:0146 clip_i 146 video 5528.0s, PBP pt 134, clock 1:31:46, s3 0-1 30-15 (Dj-Fe) srv Djokovic: "… we have one right here. Next 10 minutes, 15 minutes can change direction of the …"
* tv_2019wimF:0155 clip_i 155 video 5704.8s, PBP pt 140, clock 1:34:40, s3 1-1 0-40 (Dj-Fe) srv Federer: "… the afternoon thoroughly enjoyed just over an hour and a half of this men's singles …"
* tv_2019wimF:0176 clip_i 176 video 6526.1s, PBP pt 159, clock 1:48:20, s3 3-3 0-40 (Dj-Fe) srv Federer: "… guessing the whole time. Djokovic after an hour and 50 of this captivating men's singles …"
* tv_2019wimF:0231 clip_i 231 video 9013.4s, PBP pt 215, clock 2:29:48, s4 2-1 0-15 (Dj-Fe) srv Djokovic: "… and Novak has 16. 15, I'm sorry, 15. Ah, you're looking ahead half an hour."
* tv_2019wimF:0266 clip_i 266 video 10031.4s, PBP pt 241, clock 2:46:46, s4 2-5 30-30 (Dj-Fe) srv Federer: "2 hours and 47 minutes into this final approaching 5 o'clock local time in the …"
* … 16 more
### tiredness / legs / fatigue / cramp: 8 clip(s)
* tv_2019wimF:0014 clip_i 14 video 443.5s, PBP pt 15, clock 0:06:58, s1 1-1 30-40 (Dj-Fe) srv Federer: "… He's 37 years of age. No physical energy. Can't stay the same forever. You can't …"
* tv_2019wimF:0092 clip_i 92 video 3761.5s, PBP pt 91, clock 1:02:02, s2 0-0 15-30 (Dj-Fe) srv Djokovic: "… be a nasty one but absolutely fine legs stayed together now he comes from a …"
* tv_2019wimF:0100 clip_i 100 video 4025.8s, PBP pt 99, clock 1:06:40, s2 0-2 0-0 (Dj-Fe) srv Djokovic: "… know his age, he won't be around forever and he's really feeding off that energy."
* tv_2019wimF:0134 clip_i 134 video 4999.5s, PBP pt 125, clock 1:22:54, s2 1-5 0-40 (Dj-Fe) srv Djokovic: "Djokovic not looking to expend too much energy to stick around in this set. That's …"
* tv_2019wimF:0341 clip_i 341 video 12618.1s, PBP pt 302, clock 3:29:35, s5 4-2 30-40 (Dj-Fe) srv Djokovic: "Both players are feeling their arms getting heavy. Two of the greatest champions in our …"
* tv_2019wimF:0364 clip_i 364 video 13502.1s, PBP pt 320, clock 3:44:27, s5 5-4 15-30 (Dj-Fe) srv Federer: "… impression we'll do it with a little fatigue, Rochaferro, slowly. I mean, three hours and …"
* tv_2019wimF:0373 clip_i 373 video 13789.2s, PBP pt 327, clock 3:49:23, s5 5-5 30-30 (Dj-Fe) srv Djokovic: "… fruit, yeah. Gives you a lot of energy very quickly. On a natural basis. Yeah, …"
* tv_2019wimF:0444 clip_i 444 video 16103.5s, PBP pt 383, clock 4:27:58, s5 10-9 15-40 (Dj-Fe) srv Federer: "… a row or anything silly like that. His fatigue is cumulative. It's exhausting not watching."
### quiet / silence: 0 clip(s)

## T16. Address terms in the transcript (whole-word counts over text_corrected)
* Boris: 18
* Tim: 7
* Andrew: 0
* John: 1
* Henman: 3
* Becker: 1
* Castle: 0
* McEnroe: 0

## T17. The first five and last five transcribed clips (chronological), <= 15 words each
* tv_2019wimF:0000 video 65.0s PBP pt 3 clock 0:00:39: "30, 15. 40, 15."
* tv_2019wimF:0002 video 100.1s PBP pt 5 clock 0:01:14: "First game. 350 match wins in the Grand Slams earlier on. First player in history. …"
* tv_2019wimF:0003 video 162.4s PBP pt 6 clock 0:02:17: "15 love."
* tv_2019wimF:0005 video 203.0s PBP pt 7 clock 0:02:45: "30 love. 40 love."
* tv_2019wimF:0008 video 263.1s PBP pt 9 clock 0:03:47: "One game all. Much talk about the head-to-head between these two. Djokovic leading 25 to …"
* tv_2019wimF:0472 video 17032.5s PBP pt 406 clock 4:43:27: "If he's wrong, he loses the point. He is wrong. Federer has found the outside …"
* tv_2019wimF:0474 video 17115.3s PBP pt 408 clock 4:44:50: "And the game ends. A brutal game. 41 up, one second. Two break points down, …"
* tv_2019wimF:0476 video 17247.3s PBP pt 410 clock 4:47:02: "Just practising his volley against our microphone. I just, I don't think you give a …"
* tv_2019wimF:0477 video 17272.4s PBP pt 411 clock 4:47:27: "And as the match clock ticks over to four hours and 48 minutes matching the …"
* tv_2019wimF:0480 video 17349.3s PBP pt 413 clock 4:48:30: "1-0 Djokovic. Djokovic has won the two tie breaks that have been played between these …"

## T18. Miscellany
Games in match (R: distinct (SetNo, GameNo)): 68; tie-breaks: 3 (sets 1, 3, 5).
Points per set: set 1: 87, set 2: 38, set 3: 73, set 4: 55, set 5: 169.
Mean RallyCount (R, raw) 4.34; points with RallyCount 0 or 1 (serve not returned in play or DF): 135.
Net points (R): Djokovic 26 (won 18), Federer 53 (won 45).
Sum of DistanceRun (R, unit unlabelled, presumably metres): Djokovic 5630, Federer 5820.
Breaks of serve, whole match (R; set, match game no., server, broken by, clock of the game's last point):
* set 2 game 1: Djokovic serving, broken by Federer at 1:03:00; games after 0-1 (Dj-Fe); (no transcribed clip)
* set 2 game 3: Djokovic serving, broken by Federer at 1:08:46; games after 0-3 (Dj-Fe); tv_2019wimF:0106 (rally, video 4164.1s): "and that will do nicely probably for the set three loud two breaks"
* set 2 game 7: Djokovic serving, broken by Federer at 1:22:54; games after 1-6 (Dj-Fe); tv_2019wimF:0134 (first_serve_fault, video 4999.5s): "Djokovic not looking to expend too much energy to stick around in this set. That's …"
* set 4 game 5: Djokovic serving, broken by Federer at 2:36:11; games after 2-3 (Dj-Fe); tv_2019wimF:0246 (first_serve_fault, video 9396.2s): "Thank you. Thank you. Please. Please. Thank you. This is rubbing Novak up the wrong …"; tv_2019wimF:0247 (rally, video 9409.2s): "firm down the middle on the backhand side a miss from Djokovic and it's a …"
* set 4 game 7: Djokovic serving, broken by Federer at 2:42:40; games after 2-5 (Dj-Fe); tv_2019wimF:0259 (first_serve_fault, video 9785.3s): "Hold that, please."
* set 4 game 8: Federer serving, broken by Djokovic at 2:49:12; games after 3-5 (Dj-Fe); tv_2019wimF:0270 (rally, video 10178.2s): "And it's a break. Djokovic breaks the Federer Reserve. That is news. And after losing …"
* set 5 game 6: Federer serving, broken by Djokovic at 3:25:11; games after 4-2 (Dj-Fe); tv_2019wimF:0332 (rally, video 12347.1s): "Federer was in hoping rather than forcing and Djokovic will hit that target this shot …"
* set 5 game 7: Djokovic serving, broken by Federer at 3:31:55; games after 4-3 (Dj-Fe); tv_2019wimF:0345 (rally, video 12755.8s): "It's away! Game on again in the fifth set. That was... a collective holding of …"
* set 5 game 15: Djokovic serving, broken by Federer at 4:07:16; games after 7-8 (Dj-Fe); tv_2019wimF:0408 (rally, video 14861.4s): "Yeah, and that's the break."
* set 5 game 16: Federer serving, broken by Djokovic at 4:12:40; games after 8-8 (Dj-Fe); tv_2019wimF:0419 (rally, video 15185.8s): "Amazing, isn't it? That is guts from Djokovic. It almost reminds me of the semi-final, …"
MCP matches file: date 20190714, tournament Wimbledon, round F, time 14:10, court Centre, surface Grass, umpire Damian Steiner, best of 5, final TB T, charted by Zindaras; players Roger Federer (1) and Novak Djokovic (2), handedness R/R.

## E. External facts (pages fetched 2026-10-07 with WebFetch; quotations verbatim from the fetched text)

1. **Wikipedia, "2019 Wimbledon Championships – Men's singles final"**,
   https://en.wikipedia.org/wiki/2019_Wimbledon_Championships_%E2%80%93_Men%27s_singles_final :
   "After 4 hours and 57 minutes, first seed Novak Djokovic defeated second seed Roger Federer" in five sets, 7–6(5), 1–6,
   7–6(4), 4–6, 13–12(3). "It was the longest Wimbledon final in history" and (as of the fetch date) "the fourth longest
   major final in history behind the 2012 Australian Open final ... the 2022 Australian Open final and the 2025 French Open
   final". "This was the second Wimbledon match (and first in Gentlemen's Singles) in which a final set tie break rule was
   utilized. Upon reaching 12–all in the fifth set, a classic tie break would be played." Statistics given there: Djokovic 10
   aces, 52 unforced errors, 54 winners, 204 total points, 3 break points won; Federer 25 aces, 62 unforced errors, 94 winners,
   218 total points, 7 break points won — **identical to R (T2-T4)**. Championship points saved: "two when down 7−8 in the
   fifth set". Chair umpire "Damian Steiner of Argentina" (M matches file: Umpire = Damian Steiner; transcript tv_2019wimF:0017
   at 0:09:28: "Damien Steiner in the chair").
2. **Wikipedia, "2019 Wimbledon Championships – Men's singles"**,
   https://en.wikipedia.org/wiki/2019_Wimbledon_Championships_%E2%80%93_Men%27s_singles : "four hours and 57 minutes in
   length, it was the longest singles final in Wimbledon history"; 2019 was "the first edition of Wimbledon in which a
   final-set tiebreak rule was introduced. Upon reaching 12–12 in the final set, a classic tiebreak would be played", and the
   final was "the first singles match at Wimbledon in which the new rule came into effect, with Djokovic winning the tiebreak
   7–3". "It was Djokovic's fifth Wimbledon title and 16th major title overall." "Aged 37 years, 11 months and 6 days, Federer
   was the oldest man to reach a major final since Ken Rosewall in the 1974 US Open." "Federer reached his 31st and last men's
   singles major final, an all-time record." Seeds: Djokovic 1, Federer 2.
3. **Wikipedia, "2008 Wimbledon Championships – Men's singles final"**,
   https://en.wikipedia.org/wiki/2008_Wimbledon_Championships_%E2%80%93_Men%27s_singles_final : "After 4 hours and 48 minutes
   of play, Nadal defeated Federer 6–4, 6–4, 6–7(5–7), 6–7(8–10), 9–7." "At 4 hours and 48 minutes, the match at the time was
   the longest singles final at Wimbledon in terms of time played. It was overtaken by the 2019 men's singles final (4 hours
   and 57 minutes)". This is the record the commentators reach at 4:47:27 (T15/T17: "four hours and 48 minutes matching the
   longest final of all time").
4. **ATP Tour**, https://www.atptour.com/en/news/djokovic-federer-wimbledon-2019-final : "7-6(5), 1-6, 7-6(4), 4-6, 13-12(3)
   victory over second seed Roger Federer ... in four hours and 55 minutes" — **two minutes less than Wikipedia's 4:57**; R's
   clock stands at 4:56:59 at the first serve of the last point, so by the corpus the ATP figure is too low. "the fifth set
   that lasted two hours and two minutes" (R: first serves 3:00:13 to 4:56:59, i.e. 1:56:46 between first serves of the first
   and last points). "first men's singles 12-12 deciding set tie-break at The Championships". "Federer had two championship
   points at 8-7, 40/15 on serve, in the fifth set". Djokovic's "fifth crown at The Championships, Wimbledon" and "won 16 Grand
   Slam singles championship trophies". "The 37-year-old" (Federer). "extended his FedEx ATP Head2Head record to 26-22 against
   Federer". Set 1: Djokovic "won seven of 10 points at the net and tightened up his game to commit only six unforced errors"
   (R, T3: 6 unforced errors agrees; R counts 7 net points of which 5 won — a counting difference), Federer "hit 21 winners"
   (R, T3: 21). Set 3: Federer "hit 13 winners" (R: 13).
5. **Not obtainable here**: the wimbledon.com report (the fetch returned only the page header), BBC Sport and The Guardian
   (hosts not reachable from this session). Hence **[unverified]**: the names of the commentators (the transcript itself
   supports Boris Becker and Tim Henman as co-commentators — "Boris" 18 times, "Tim" 7, "Henman" 3, "Becker" 1, and
   tv_2019wimF:0275 at 2:52:06 "the gentleman on my left, Tim Henman" — and never names the lead commentator), attendance,
   prize money, and the Royal Box attendees (the transcript has "the royal box and Philbrook the chairman" at 1:34:40, ASR for
   Philip Brook [unverified], "I thought the Royal Box was meant to be impartial" at 3:31:55, and "i don't speak for the
   duchess" at 3:56:54). Federer's age 37 is also in the transcript: tv_2019wimF:0014 at 0:06:58, "He's 37 years of age".
6. **Start time and venue**: M matches file, `Time 14:10`, `Court Centre`, `Surface Grass`, `Best of 5`, `Final TB? T`; the
   transcript at 2:46:46 (tv_2019wimF:0266) has "2 hours and 47 minutes into this final approaching 5 o'clock local time",
   consistent with a 14:10 start.

## F. Narrative beats for the composer (every time and number from T1-T18; nothing added)

1. **Opening (0:00:00).** Federer serves the first point (R PointServer = 2 at point 1; T1). Set 1 has no break of serve
   (T4) and one break point, for Federer, at 0:15:23 (T15: "Just over a quarter of an hour played and Federer with the first
   break point."). The tie-break (T7) runs 0:49:06-0:57:50: Federer leads 5-3 after a 197 km/h serve winner and an ace, then
   loses four points in a row — three Federer unforced errors and one forced error (R flags, points 84-87) — 7-5 Djokovic.
2. **Set 2 (1:00:23-1:22:54).** Federer breaks in games 1, 3 and 7 (T4, T18), 6-1 in 22½ minutes; 38 points, Federer 26-12
   (T2). Commentary at the second break: "and that will do nicely probably for the set three loud two breaks" (T18).
3. **Set 3 (1:27:28-2:15:24).** No breaks (T4). The 26-shot rally at 2:03:53 (point 183, Djokovic serving at 5-6 0-0) goes
   to Federer (T6: "justifies logic 26 shots and at the end Federer able to come up with the …"). Tie-break (T8): Djokovic
   5-1 up (a 24-shot rally at 2:11:04 ends in a Federer forced error), Federer back to 5-4 with a volley winner and an ace,
   Djokovic 7-4 at 2:15:24.
4. **Set 4 (2:20:29-2:55:08).** Federer breaks in games 5 (2:36:11) and 7 (2:42:40) to lead 5-2 (T18). Serving at 5-2
   40-30 he wins the 35-shot rally of the match at 2:47:12 (T6; TennisVL 34 shots, 43.4 s; R distance run Djokovic 104.2,
   Federer 85.5; commentary "35 shots every one of them right out of the middle yes") but is broken in that same game at
   2:49:12 (T18: "And it's a break. Djokovic breaks the Federer Reserve. That is news. And after losing …", where
   "Reserve" is the ASR's hearing of "serve"). Federer
   holds for 6-4 at 2:55:08 ("… the crowd rise and we have a fifth and deciding set as I look at …").
5. **Set 5 (3:00:13-4:56:59, 169 points, Djokovic 85-84; T9).** Djokovic breaks game 6 at 3:25:11 (4-2); Federer breaks
   straight back in game 7 at 3:31:55 (T11: "It's away! Game on again in the fifth set. That was... a collective holding of
   …"). Holds to 7-7 (4:02:57). Federer breaks game 15 at 4:07:16 with a forehand pass ("Yeah, and that's the break"): 8-7.
6. **The championship game (T10; set-5 game 16, Federer serving at 7-8, 4:08:51-4:12:40).** 0-15 (Federer error; the
   umpire's "Thank you, players, already. Thank you, ladies and gentlemen. Please. Please. …"), 15-15, ace at 201 km/h
   (4:10:13), ace at 193 km/h (4:10:35): **40-15, two championship points.** CP1 at **4:10:58**: second serve 151 km/h wide,
   Djokovic forehand return down the middle, Federer forehand inside-out wide, unforced error (M `4f28f3w@`, S shots 0-2;
   commentary "Breathe in, breathe out. 40, 30."). CP2 at **4:11:30**: first serve 193 km/h to the T, Djokovic forehand slice
   return, Federer forehand approach inside-in, Djokovic forehand cross-court passing winner (M `6r28f+1f1*`, S shot 3
   "winner"; "And just as Federer passed Djokovic to get the break in the previous game, Djokovic …"). Deuce at 4:11:58: a
   seven-shot backhand exchange, Federer forehand slice forced error. Break point and **break at 4:12:40** (AD-40): first
   serve 189 km/h, Djokovic forehand slice return, Federer forehand into the net (M `6r18f1f1f2n@`, 5 shots, server hit last):
   8-8 ("Amazing, isn't it? That is guts from Djokovic. It almost reminds me of the semi-final, …").
7. **8-8 to 12-12 (4:13:27-4:47:47).** Djokovic holds for 9-8 at 4:17:15 ("Djokovic finding the mark just when he needed to
   he takes the lead 9-8 …"); the crowd "deflated" at 4:18:51 (T15). Game 23 (Djokovic serving at 11-11, 4:35:09-4:44:50,
   14 points) contains the second-longest rally of the set (24 shots at 4:38:36, Federer) and two break points saved
   ("And the game ends. A brutal game. 41 up, one second. Two break points down, …"). Federer holds to love for 12-12 at
   4:47:47 as the clock passes the 2008 record ("… four hours and 48 minutes matching the longest final of all time …").
8. **The 12-12 tie-break (T12; 4:48:30-4:56:59).** Djokovic wins the first point from a second serve after a 12-shot rally
   (Federer backhand error; the last transcribed clip: "1-0 Djokovic. Djokovic has won the two tie breaks that have been played
   between these …"); Federer 1-1 with a forehand winner; Djokovic 4-1 (a Federer half-volley error, two forced errors);
   Federer 4-3 (drop-shot winner, serve winner); Djokovic 5-3 with a 194 km/h serve and forehand winner, 6-3 after a 13-shot
   rally ending in a Djokovic forehand winner; **7-3 at 4:56:59**: Federer second serve 143 km/h, Djokovic backhand return,
   Federer forehand unforced error (T13). No clip or commentary exists for points 414-422.
9. **Scene inventory from the transcript (T15-T17).** Available: the umpire's calls and "Please" (0:09:28, 4:08:51), the sun
   on the ball toss (1:18:38), the new Court One roof and "no need for the roof" (1:34:40, 2:02:19), the sun getting lower at
   the southern end (3:49:23), the Royal Box, the chairman and "the duchess" (1:34:40, 3:31:55, 3:56:54), the player boxes
   (1:05:55, 2:26:44, 2:31:53, 3:07:58, 3:24:06), the crowd engaging, cheering "for the other guy", deflated (0:44:03,
   2:38:06, 4:18:51), new balls (0:28:xx clip 0050, 2:22:20, 3:43:05, 4:22:01), challenges and line calls (0:32:57, 0:41:23,
   1:28:22, 4:38:36, 4:43:27), fatigue ("Both players are feeling their arms getting heavy", 3:29:35; "His fatigue is
   cumulative", 4:27:58). Absent: walk-on, warm-up, coin toss, trophy, speeches, the final point.


## Appendix: the script that produced tables T1-T18 (`match_facts.py`; run with `python -I` from any directory; paths are absolute to the repository)

```python
#!/usr/bin/env python3
"""Compute every number used in composition/research/match_facts.md from the corpus files.

Sources (all on disk, none edited):
  P  corpus/timing/points_2019wimF.csv               merged per-point table (PBP x MCP x TennisVL)
  R  corpus/raw/sackmann_slam_pbp_hfmirror/2019-wimbledon-points.csv  (match_id 2019-wimbledon-1701; P1 = Djokovic, P2 = Federer)
  M  corpus/raw/sackmann_mcp/charting-m-points-2010s.csv (match_id 20190714-M-Wimbledon-F-Roger_Federer-Novak_Djokovic; player 1 = Federer)
  S  corpus/timing/shots_2019wimF.csv                 TennisVL per-shot timing
  T  corpus/transcripts/tv_2019wimF.jsonl             TennisVL WhisperX transcript, one record per clip
Run:  python -I match_facts.py > match_facts_out.md
"""
import csv, json, re, statistics, sys
from collections import Counter, defaultdict

ROOT = '/home/user/parry-wimbledon'
P = list(csv.DictReader(open(f'{ROOT}/corpus/timing/points_2019wimF.csv', encoding='utf-8')))
R = [r for r in csv.DictReader(open(f'{ROOT}/corpus/raw/sackmann_slam_pbp_hfmirror/2019-wimbledon-points.csv', encoding='utf-8'))
     if r['match_id'] == '2019-wimbledon-1701' and r['PointNumber'] not in ('0X', '0Y')]
M = [r for r in csv.DictReader(open(f'{ROOT}/corpus/raw/sackmann_mcp/charting-m-points-2010s.csv', encoding='utf-8'))
     if r['match_id'] == '20190714-M-Wimbledon-F-Roger_Federer-Novak_Djokovic']
M.sort(key=lambda r: int(r['Pt']))
S = list(csv.DictReader(open(f'{ROOT}/corpus/timing/shots_2019wimF.csv', encoding='utf-8')))
T = [json.loads(l) for l in open(f'{ROOT}/corpus/transcripts/tv_2019wimF.jsonl', encoding='utf-8')]

assert len(P) == 422 and len(R) == 422 and len(M) == 422, (len(P), len(R), len(M))
for i, (p, r, m) in enumerate(zip(P, R, M), 1):
    assert int(p['point_idx']) == i == int(r['PointNumber']) == int(m['Pt'])
    assert p['pbp_elapsed'] == r['ElapsedTime']
    assert p['mcp_1st'] == m['1st'] and p['mcp_2nd'] == m['2nd']

DJ, FE = 'Novak Djokovic', 'Roger Federer'
NAME = {'1': 'Djokovic', '2': 'Federer'}           # PBP P1/P2
MCPNAME = {'1': 'Federer', '2': 'Djokovic'}        # MCP player 1/2
by_point = defaultdict(list)
for t in T:
    if t.get('point_idx_pbp') is not None:
        by_point[int(t['point_idx_pbp'])].append(t)

def hms(s):
    s = int(s); return f'{s//3600}:{(s%3600)//60:02d}:{s%60:02d}'

def excerpt(text, kw=None, n=15):
    """At most n words; centred on the first match of kw if given."""
    words = text.split()
    if len(words) <= n:
        return ' '.join(words)
    if kw:
        for i, w in enumerate(words):
            if re.search(kw, w, re.I):
                lo = max(0, i - n // 2); hi = lo + n
                if hi > len(words):
                    hi = len(words); lo = hi - n
                return ('… ' if lo > 0 else '') + ' '.join(words[lo:hi]) + (' …' if hi < len(words) else '')
    return ' '.join(words[:n]) + ' …'

def clips_for(idx):
    """Transcript records for PBP point idx: (utt_id, clip_role, clip_start_s, text_corrected)."""
    out = []
    for t in by_point.get(idx, []):
        out.append((t['utt_id'], t['clip_role'], t['clip_start_s'], t['text_corrected'] or ''))
    return out

def commentary(idx, n=15):
    parts = []
    for u, role, cs, txt in clips_for(idx):
        if txt.strip():
            parts.append(f'{u} ({role}, video {cs:.1f}s): "{excerpt(txt, None, n)}"')
    return '; '.join(parts) if parts else '(no transcribed clip)'

def mcp_end(code):
    """Point-ending class from the last MCP shot code: * winner, @ unforced error, # forced error."""
    c = (code or '').strip()
    return {'*': 'winner', '@': 'unforced error', '#': 'forced error'}.get(c[-1:], '?')

def mcp_desc(p):
    first, second = p['mcp_1st'], p['mcp_2nd']
    if second:
        return f'1st `{first}` (fault), 2nd `{second}` -> {mcp_end(second)}'
    return f'`{first}` -> {mcp_end(first)}'

out = []
pr = out.append

# ---------------------------------------------------------------- 1. score set by set
pr('## T1. Score set by set (R: last row of each SetNo; tie-break score = P1Score/P2Score after the penultimate point + the winner of the last point)')
pr('| set | games Djokovic-Federer | set winner | tie-break (Djokovic-Federer) | first point clock | last point clock | points in set | games in set |')
pr('|---|---|---|---|---|---|---|---|')
set_rows = defaultdict(list)
for r in R:
    set_rows[r['SetNo']].append(r)
for s in sorted(set_rows):
    rows = set_rows[s]
    last = rows[-1]
    tb = [r for r in rows if r['GameNo'] == (str(max(int(x['GameNo']) for x in rows)) if int(last['P1GamesWon']) + int(last['P2GamesWon']) in (13, 25) else '-')]
    tbtxt = '-'
    if tb:
        # score before the last tb point, then add the winner's point
        # R's P1Score/P2Score are the state AFTER the point (the last row resets to 0-0):
        a, b = int(tb[-2]['P1Score']), int(tb[-2]['P2Score'])
        if tb[-1]['PointWinner'] == '1': a += 1
        else: b += 1
        tbtxt = f'{a}-{b}'
    pr(f"| {s} | {last['P1GamesWon']}-{last['P2GamesWon']} | {NAME[last['SetWinner']]} | {tbtxt} | {rows[0]['ElapsedTime']} | {last['ElapsedTime']} | {len(rows)} | {len(set(r['GameNo'] for r in rows))} |")
pr(f"\nDuration = last ElapsedTime (R) = **{R[-1]['ElapsedTime']}** (first serve of the last point; the match clock starts 0:00:00 at point 1).")
pr(f"Sets: Djokovic {sum(1 for s in set_rows if set_rows[s][-1]['SetWinner']=='1')}, Federer {sum(1 for s in set_rows if set_rows[s][-1]['SetWinner']=='2')}.")
pr('')

# ---------------------------------------------------------------- 2. points won
pr('## T2. Points won')
pw = Counter(r['PointWinner'] for r in R)
pr(f"R PointWinner counts: Djokovic {pw['1']}, Federer {pw['2']} (total {sum(pw.values())}); R running columns at the last row: P1PointsWon={R[-1]['P1PointsWon']} (Djokovic), P2PointsWon={R[-1]['P2PointsWon']} (Federer).")
pwm = Counter(m['PtWinner'] for m in M)
pr(f"M PtWinner counts: Federer {pwm['1']}, Djokovic {pwm['2']}.")
pr('Per set (R):')
pr('| set | Djokovic | Federer |')
pr('|---|---|---|')
for s in sorted(set_rows):
    c = Counter(r['PointWinner'] for r in set_rows[s])
    pr(f"| {s} | {c['1']} | {c['2']} |")
# service points won
pr('\nService points (R: PointServer = server; won = PointWinner == PointServer):')
pr('| server | service points | won | % |')
pr('|---|---|---|---|')
for sv in ('1', '2'):
    n = sum(1 for r in R if r['PointServer'] == sv); w = sum(1 for r in R if r['PointServer'] == sv and r['PointWinner'] == sv)
    pr(f"| {NAME[sv]} | {n} | {w} | {100*w/n:.1f} |")
pr('')

# ---------------------------------------------------------------- 3. aces, DFs, winners, UEs per set
pr('## T3. Aces, double faults, winners, unforced errors per player per set (R columns P1Ace/P2Ace, P1DoubleFault/P2DoubleFault, P1Winner/P2Winner, P1UnfErr/P2UnfErr; 1 = that point)')
pr('| set | aces Dj | aces Fe | DF Dj | DF Fe | winners Dj | winners Fe | UE Dj | UE Fe | net pts Dj (won) | net pts Fe (won) |')
pr('|---|---|---|---|---|---|---|---|---|---|---|')
tot = Counter()
for s in sorted(set_rows) + ['all']:
    rows = R if s == 'all' else set_rows[s]
    c = {k: sum(int(r[k]) for r in rows) for k in ('P1Ace','P2Ace','P1DoubleFault','P2DoubleFault','P1Winner','P2Winner','P1UnfErr','P2UnfErr','P1NetPoint','P2NetPoint','P1NetPointWon','P2NetPointWon')}
    pr(f"| {s} | {c['P1Ace']} | {c['P2Ace']} | {c['P1DoubleFault']} | {c['P2DoubleFault']} | {c['P1Winner']} | {c['P2Winner']} | {c['P1UnfErr']} | {c['P2UnfErr']} | {c['P1NetPoint']} ({c['P1NetPointWon']}) | {c['P2NetPoint']} ({c['P2NetPointWon']}) |")
# does P1Winner include aces?
both = sum(1 for r in R if r['P1Ace']=='1' and r['P1Winner']=='1') + sum(1 for r in R if r['P2Ace']=='1' and r['P2Winner']=='1')
pr(f"\nAces counted also as winners in R (rows with Ace=1 and Winner=1 for the same player): {both} of {sum(int(r['P1Ace'])+int(r['P2Ace']) for r in R)} aces -> the Winner columns {'include' if both else 'exclude'} aces.")
empty = [c for c in R[0] if all(r[c] == '' for r in R)]
pr(f"R columns that are empty for every point of this match: {', '.join(empty)}.")
pr("R columns filled: all others; WinnerType is 'S' for 8 points (serve winners), WinnerShotType F/B for 105 points; Rally is empty (RallyCount is filled).")
# MCP cross-check
pr('\nCross-check from M (Match Charting Project; ending symbol of the last shot code: `*` winner, `@` unforced error, `#` forced error; mcp_ace / mcp_double_fault from P):')
mc = Counter()
for p in P:
    code = p['mcp_2nd'] or p['mcp_1st']
    hitter_is_server = (p['mcp_n_shots'] and int(p['mcp_n_shots']) % 2 == 1)
    srv = MCPNAME[p['mcp_svr']]
    other = 'Djokovic' if srv == 'Federer' else 'Federer'
    hitter = srv if hitter_is_server else other
    end = mcp_end(code)
    if p['mcp_ace'] == '1': mc[(srv, 'ace')] += 1
    if p['mcp_double_fault'] == '1': mc[(srv, 'double fault')] += 1
    if end == 'winner' and p['mcp_ace'] != '1': mc[(hitter, 'winner (non-ace)')] += 1
    if end == 'unforced error' and p['mcp_double_fault'] != '1': mc[(hitter, 'unforced error (non-DF)')] += 1
    if end == 'forced error': mc[(hitter, 'forced error')] += 1
pr('| | Djokovic | Federer |')
pr('|---|---|---|')
for k in ('ace', 'double fault', 'winner (non-ace)', 'unforced error (non-DF)', 'forced error'):
    pr(f"| {k} | {mc[('Djokovic', k)]} | {mc[('Federer', k)]} |")
pr('(hitter of the last shot inferred from the parity of mcp_n_shots: odd = server hit last; the MCP charter\'s own @/# labels differ from the official R labels, see corpus/README.md section 7.1)')
pr('')

# ---------------------------------------------------------------- 4. break points
pr('## T4. Break points (R: P1BreakPoint = Djokovic holds a break point (Federer serving), P1BreakPointWon = converted; P2* likewise for Federer)')
chk = Counter((r['PointServer']) for r in R if r['P1BreakPoint'] == '1')
pr(f"Sanity: server on the points with P1BreakPoint=1: {dict(chk)} (2 = Federer serving, as expected).")
pr('| set | BP for Djokovic (converted) | BP for Federer (converted) | breaks of serve in set (game winner != server) |')
pr('|---|---|---|---|')
for s in sorted(set_rows) + ['all']:
    rows = R if s == 'all' else set_rows[s]
    b1 = sum(int(r['P1BreakPoint']) for r in rows); w1 = sum(int(r['P1BreakPointWon']) for r in rows)
    b2 = sum(int(r['P2BreakPoint']) for r in rows); w2 = sum(int(r['P2BreakPointWon']) for r in rows)
    brk = [(r['SetNo'], r['GameNo'], NAME[r['GameWinner']]) for r in rows if r['GameWinner'] != '0' and r['GameWinner'] != r['PointServer'] and not (int(r['P1GamesWon'])+int(r['P2GamesWon']) in (13,25) and r['SetWinner']!='0')]
    pr(f"| {s} | {b1} ({w1}) | {b2} ({w2}) | {'; '.join(f's{a} g{g} by {w}' for a,g,w in brk) if s!='all' else len(brk)} |")
pr('(a tie-break game is excluded from the break column.)')
pr('')

# ---------------------------------------------------------------- 5. serve speed
pr('## T5. Serve speed (R: Speed_KMH of the serve that started the point, by PointServer and ServeNumber; 0 = not recorded)')
pr('| server | serves recorded | 1st-serve n | 1st max | 1st mean | 2nd n | 2nd max | 2nd mean | all max | all mean | all min |')
pr('|---|---|---|---|---|---|---|---|---|---|---|')
for sv in ('1', '2'):
    sp = [(int(r['Speed_KMH']), r['ServeNumber']) for r in R if r['PointServer'] == sv and int(r['Speed_KMH']) > 0]
    s1 = [v for v, n in sp if n == '1']; s2 = [v for v, n in sp if n == '2']; sa = [v for v, n in sp]
    pr(f"| {NAME[sv]} | {len(sa)} | {len(s1)} | {max(s1)} | {statistics.mean(s1):.1f} | {len(s2)} | {max(s2)} | {statistics.mean(s2):.1f} | {max(sa)} | {statistics.mean(sa):.1f} | {min(sa)} |")
zero = sum(1 for r in R if int(r['Speed_KMH']) == 0)
pr(f"Points with Speed_KMH = 0 (unrecorded): {zero} of 422.")
for sv in ('1','2'):
    best = max((r for r in R if r['PointServer']==sv), key=lambda r:int(r['Speed_KMH']))
    pr(f"Fastest serve {NAME[sv]}: {best['Speed_KMH']} km/h ({best['Speed_MPH']} mph) at {best['ElapsedTime']}, set {best['SetNo']} game {best['GameNo']}, point {best['PointNumber']}, serve {best['ServeNumber']}, ace={best['P'+sv+'Ace']}; MCP {mcp_desc(P[int(best['PointNumber'])-1])}; commentary: {commentary(int(best['PointNumber']))}")
pr('')

# ---------------------------------------------------------------- 6. longest rally
pr('## T6. Longest rallies')
pr('Conventions (corpus/README.md 7.1): R RallyCount counts in-play shots (the erring final shot is not counted); M and TennisVL count the erring shot too.')
top_m = sorted(P, key=lambda p: -int(p['mcp_n_shots'] or 0))[:6]
pr('| rank | point_idx | clock (R ElapsedTime) | set/game, score before (server first, PBP) | MCP shots | R RallyCount | TV n_shots | TV rally s | winner | ending (MCP) | commentary (TennisVL clip) |')
pr('|---|---|---|---|---|---|---|---|---|---|---|')
for i, p in enumerate(top_m, 1):
    idx = int(p['point_idx']); r = R[idx-1]
    sc = f"s{p['set_no']} g{p['game_in_set']}{' TB' if p['tiebreak']=='True' else ''}, {p['pts_before_p1']}-{p['pts_before_p2']} (Dj-Fe), games {p['games_before_p1']}-{p['games_before_p2']}, server {p['server'].split()[-1]}"
    pr(f"| {i} | {idx} | {p['pbp_elapsed']} | {sc} | {p['mcp_n_shots']} | {r['RallyCount']} | {p['tv_n_shots'] or '-'} | {p['tv_rally_duration_s'] or '-'} | {p['point_winner'].split()[-1]} | {mcp_desc(p)} | {commentary(idx)} |")
top_tv = sorted([p for p in P if p['tv_n_shots']], key=lambda p: -int(p['tv_n_shots']))[:3]
pr('\nLongest by TennisVL shot count: ' + '; '.join(f"point {p['point_idx']} ({p['tv_n_shots']} shots, {p['tv_rally_duration_s']} s, MCP {p['mcp_n_shots']}, clock {p['pbp_elapsed']})" for p in top_tv))
top_r = sorted(R, key=lambda r: -int(r['RallyCount']))[:3]
pr('Longest by R RallyCount: ' + '; '.join(f"point {r['PointNumber']} ({r['RallyCount']} in-play shots, clock {r['ElapsedTime']})" for r in top_r))
# longest by TV duration
top_dur = sorted([p for p in P if p['tv_rally_duration_s']], key=lambda p: -float(p['tv_rally_duration_s']))[:3]
pr('Longest by TennisVL rally duration (first hit to last hit): ' + '; '.join(f"point {p['point_idx']} ({p['tv_rally_duration_s']} s, {p['tv_n_shots']} shots, clock {p['pbp_elapsed']})" for p in top_dur))
# distance run on the longest point
r = R[int(top_m[0]['point_idx'])-1]
pr(f"R distance run on point {r['PointNumber']}: Djokovic {r['P1DistanceRun']} m, Federer {r['P2DistanceRun']} m (units as in the file; the column is unlabelled).")
# rally length distribution
rc = [int(p['mcp_n_shots']) for p in P if p['mcp_n_shots']]
pr(f"MCP shots per point: mean {statistics.mean(rc):.2f}, median {statistics.median(rc)}, points with >= 10 shots: {sum(1 for x in rc if x>=10)}, 1-shot points (aces/DF/unreturned serves counted as 1 or 2): {sum(1 for x in rc if x<=2)}.")
pr('')

# ---------------------------------------------------------------- helper for tie-break tables
def tb_table(set_no, game_no, title):
    pr(f'## {title}')
    pr('| pt | clock | score before (Dj-Fe) | server | serve km/h (no.) | winner | R RallyCount | MCP shots | MCP code -> ending | R flags | commentary |')
    pr('|---|---|---|---|---|---|---|---|---|---|---|')
    rows = [(i, r) for i, r in enumerate(R, 1) if r['SetNo'] == set_no and r['GameNo'] == game_no]
    prev = None
    for i, r in rows:
        p = P[i-1]
        flags = [k for k in ('P1Ace','P2Ace','P1DoubleFault','P2DoubleFault','P1Winner','P2Winner','P1UnfErr','P2UnfErr','P1NetPoint','P2NetPoint') if r[k]=='1']
        flags = ','.join(f.replace('P1','Dj:').replace('P2','Fe:') for f in flags)
        pr(f"| {i} | {r['ElapsedTime']} | {p['pts_before_p1']}-{p['pts_before_p2']} | {NAME[r['PointServer']]} | {r['Speed_KMH']} ({r['ServeNumber']}) | {NAME[r['PointWinner']]} | {r['RallyCount']} | {p['mcp_n_shots']} | {mcp_desc(p)} | {flags} | {commentary(i)} |")
    last = rows[-1][1]
    pr(f"Tie-break first point {rows[0][1]['ElapsedTime']}, last point {last['ElapsedTime']}; {len(rows)} points; game winner {NAME[last['GameWinner']]}; set winner {NAME[last['SetWinner']]}.")
    pr('')

tb_table('1', '13', 'T7. First-set tie-break (R: SetNo 1, GameNo 13), point by point')
tb_table('3', '13', 'T8. Third-set tie-break (R: SetNo 3, GameNo 13), point by point')

# ---------------------------------------------------------------- fifth set game by game
pr('## T9. Fifth set game by game (R: SetNo 5; clock = ElapsedTime of the first point of the game; games after = P1GamesWon-P2GamesWon at the game\'s last point)')
pr('| game (set) | R GameNo (restarts each set) | clock first point | clock last point | server | points (Dj-Fe) | game winner | break? | games after (Dj-Fe) | note (R flags) |')
pr('|---|---|---|---|---|---|---|---|---|---|')
games = defaultdict(list)
for i, r in enumerate(R, 1):
    if r['SetNo'] == '5':
        games[int(r['GameNo'])].append((i, r))
g5first = min(games)
for g in sorted(games):
    rows = games[g]
    first, last = rows[0][1], rows[-1][1]
    c = Counter(r['PointWinner'] for _, r in rows)
    srv = NAME[first['PointServer']]
    win = NAME[last['GameWinner']]
    brk = 'BREAK' if (win != srv and g != 25) else ''
    notes = []
    bp1 = sum(int(r['P1BreakPoint']) for _, r in rows); bp2 = sum(int(r['P2BreakPoint']) for _, r in rows)
    if bp1: notes.append(f'{bp1} BP for Djokovic')
    if bp2: notes.append(f'{bp2} BP for Federer')
    aces = sum(int(r['P1Ace'])+int(r['P2Ace']) for _, r in rows); dfs = sum(int(r['P1DoubleFault'])+int(r['P2DoubleFault']) for _, r in rows)
    if aces: notes.append(f'{aces} ace(s)')
    if dfs: notes.append(f'{dfs} DF')
    if g == 25: notes.append('TIE-BREAK at 12-12 (first ever at this score in a Wimbledon final: see external section)')
    pr(f"| {g-g5first+1} | {g} | {first['ElapsedTime']} | {last['ElapsedTime']} | {srv} | {c['1']}-{c['2']} | {win} | {brk} | {last['P1GamesWon']}-{last['P2GamesWon']} | {'; '.join(notes)} |")
s5 = set_rows['5']
pr(f"\nFifth set: {len(s5)} points, from {s5[0]['ElapsedTime']} to {s5[-1]['ElapsedTime']}; points won Djokovic {sum(1 for r in s5 if r['PointWinner']=='1')}, Federer {sum(1 for r in s5 if r['PointWinner']=='2')}.")
pr('')

# ---------------------------------------------------------------- championship points
pr('## T10. The two championship points: Federer serving at 8-7 (set 5, R: SetNo 5, GameNo 16; games 7-8 Dj-Fe before the game; PointServer=2), at 40-15 and 40-30')
cp_game = [(i, r) for i, r in enumerate(R, 1) if r['SetNo']=='5' and r['GameNo']=='16']
assert all(r['PointServer']=='2' for _, r in cp_game) and cp_game[0][1]['P1GamesWon']=='7' and cp_game[0][1]['P2GamesWon']=='8'
pr('Whole game (every point):')
pr('| pt | clock | score before (Dj-Fe) | serve km/h (no.) | winner | R RallyCount | MCP code -> ending | R flags | TennisVL (n_shots, outcome, hit times) | commentary |')
pr('|---|---|---|---|---|---|---|---|---|---|')
for i, r in cp_game:
    p = P[i-1]
    flags = ','.join(k.replace('P1','Dj:').replace('P2','Fe:') for k in ('P1Ace','P2Ace','P1DoubleFault','P2DoubleFault','P1Winner','P2Winner','P1UnfErr','P2UnfErr','P1NetPoint','P2NetPoint','P1BreakPoint','P1BreakPointWon','P1BreakPointMissed') if r[k]=='1')
    tv = f"{p['tv_n_shots'] or '-'}, {p['tv_point_outcome'] or '-'}, {p['tv_hit_times'] or '-'}"
    pr(f"| {i} | {r['ElapsedTime']} | {p['pts_before_p1']}-{p['pts_before_p2']} | {r['Speed_KMH']} ({r['ServeNumber']}) | {NAME[r['PointWinner']]} | {r['RallyCount']} | {mcp_desc(p)} | {flags} | {tv} | {commentary(i, 15)} |")
pr('')
pr('Full MCP shot codes and TennisVL shot lists of the two championship points and the two break points that followed:')
for i, r in cp_game:
    p = P[i-1]
    if p['pts_before_p2'] == '40' or r['P1BreakPoint'] == '1':
        pr(f"* point {i} ({r['ElapsedTime']}, {p['pts_before_p1']}-{p['pts_before_p2']} Dj-Fe): MCP 1st=`{p['mcp_1st']}` 2nd=`{p['mcp_2nd'] or '-'}`; MCP winner {MCPNAME[M[i-1]['PtWinner']]}; R winner {NAME[r['PointWinner']]}; R ServeWidth={r['ServeWidth']} ServeDepth={r['ServeDepth']} ReturnDepth={r['ReturnDepth']}; distance run Dj {r['P1DistanceRun']} Fe {r['P2DistanceRun']}.")
        shots = [s for s in S if s['point_idx'] == str(i)]
        for s in shots:
            pr(f"    - TV shot {s['shot_index']} {s['hitter'].split()[-1]}: {s['type']} {s['wing'] or ''} {s['technique'] or ''} {s['direction_rough'] or ''} hit {s['hit_timestamp_second']}s outcome {s['shot_outcome']} (clip {s['clip'].split('_')[-2]}_{s['clip'].split('_')[-1]})")
        for u, role, cs, txt in clips_for(i):
            pr(f"    - transcript {u} ({role}, video {cs:.2f}s): \"{excerpt(txt, None, 15)}\"  [full length {len(txt.split())} words]")
pr('')

# ---------------------------------------------------------------- the break and the break back in set 5
pr('## T11. Breaks of serve in the fifth set (R: GameWinner != PointServer, non-tie-break games)')
for g in sorted(games):
    rows = games[g]; first, last = rows[0][1], rows[-1][1]
    if g != 25 and last['GameWinner'] != first['PointServer']:
        pr(f"* Game {g} (set-5 game {g-g5first+1}): {NAME[first['PointServer']]} serving at {first['P1GamesWon']}-{first['P2GamesWon']} (Dj-Fe); broken by {NAME[last['GameWinner']]}; clock {first['ElapsedTime']} to {last['ElapsedTime']}; games after {last['P1GamesWon']}-{last['P2GamesWon']}.")
        for i, r in rows:
            p = P[i-1]
            pr(f"    - pt {i} {r['ElapsedTime']} {p['pts_before_p1']}-{p['pts_before_p2']} serve {r['Speed_KMH']}({r['ServeNumber']}) -> {NAME[r['PointWinner']]}; MCP {mcp_desc(p)}; {commentary(i, 15)}")
pr('')

# ---------------------------------------------------------------- 12-12 tie-break
tb_table('5', '25', 'T12. The 12-12 tie-break (R: SetNo 5, GameNo 25), point by point with the clock')

# ---------------------------------------------------------------- final point
pr('## T13. The final point')
i = 422; r = R[-1]; p = P[-1]
pr(f"Point {i}: clock {r['ElapsedTime']}; score before {p['pts_before_p1']}-{p['pts_before_p2']} (Dj-Fe) in the tie-break, games 12-12; server {NAME[r['PointServer']]}, serve {r['Speed_KMH']} km/h ({r['Speed_MPH']} mph), serve number {r['ServeNumber']} (ServeWidth {r['ServeWidth']}, ServeDepth {r['ServeDepth']}, ReturnDepth {r['ReturnDepth']}); winner {NAME[r['PointWinner']]}; R RallyCount {r['RallyCount']}; R flags: P2UnfErr={r['P2UnfErr']} (Federer unforced error); MCP 1st=`{p['mcp_1st']}` 2nd=`{p['mcp_2nd']}` -> {mcp_desc(p)}; MCP shots {p['mcp_n_shots']}; distance run Dj {r['P1DistanceRun']} Fe {r['P2DistanceRun']}.")
for s in [s for s in S if s['point_idx'] == '422']:
    pr(f"    - TV shot {s['shot_index']} {s['hitter'].split()[-1]}: {s['type']} {s['wing'] or ''} {s['technique'] or ''} {s['direction_rough'] or ''} hit {s['hit_timestamp_second']}s outcome {s['shot_outcome']}")
for u, role, cs, txt in clips_for(422):
    pr(f"    - transcript {u} ({role}, video {cs:.2f}s): \"{excerpt(txt, None, 15)}\" [full length {len(txt.split())} words]")
pr('')

# ---------------------------------------------------------------- transcript coverage and typical-scene material
pr('## T14. Transcript coverage (T)')
n_txt = sum(1 for t in T if (t['text_corrected'] or '').strip())
pr(f"{len(T)} clip records; {n_txt} with non-empty text_corrected; first clip starts at video {min(t['clip_start_s'] for t in T):.2f} s (point {T[0]['point_idx_pbp']}), last clip at {max(t['clip_start_s'] for t in T):.2f} s. Words (text_corrected): {sum(len((t['text_corrected'] or '').split()) for t in T)}.")
pr('The clips are rally/serve clips only: there is no footage or transcript of the walk-on, warm-up, coin toss or trophy ceremony in this corpus (see search results below).')
pr('')
pr('## T15. Keyword search in text_corrected (typical-scene material). Excerpt <= 15 words around the first hit; score_before and clock from the record.')
KW = {
 'walk-on / warm-up / toss / umpire': r'\b(walk|warm[- ]?up|coin|toss|umpire|chair|steiner)\b',
 'Royal Box / royalty / celebrities': r'\b(royal|duchess|prince|princess|kate|meghan|box)\b',
 'crowd': r'\b(crowd|applause|cheer|cheering|roar|noise|chant|standing ovation|ovation|fans|centre court|centre-court)\b',
 'weather / roof / sun / shadow / wind / heat': r'\b(roof|sun|sunshine|shadow|shade|wind|breeze|hot|heat|warm|cloud|rain|weather|humid|temperature|light)\b',
 'trophy / ceremony / presentation': r'\b(trophy|trophies|ceremon\w*|presentation|speech|winner\'?s|runner-up|plate|cup)\b',
 'history / records / titles': r'\b(history|historic|record|longest|oldest|sixteenth|16th|fifth title|grand slam|grand slams|titles?|100)\b',
 'rituals: new balls, towel, ball kids, changeover, racket': r'\b(new balls|towel|ball ?(boy|girl|kid)s?|changeover|change of ends|bounces?|bouncing|racket|racquet|strings?|shoes|water|banana)\b',
 'line calls / challenge / Hawk-Eye / umpire calls': r'\b(challenge\w*|hawk-?eye|called|call|line judge|replay|overrule\w*|let\b|fault)\b',
 'Boris': r'\bboris\b',
 'Tim': r'\btim\b',
 'grass / court / lines / net': r'\b(grass|baseline|line|lines|net|court|chalk|tramline)\b',
 'serve / ace / second serve': r'\b(ace|aces|serve|serving|second serve|first serve)\b',
 'break / championship point / match point': r'\b(break point|break points|championship point|championship points|match point|set point)\b',
 'time / clock / hours / length': r'\b(hour|hours|minutes|clock|longest|four hours|five hours)\b',
 'tiredness / legs / fatigue / cramp': r'\b(tired|fatigue|legs|cramp|exhaust|energy|heavy)\b',
 'quiet / silence': r'\b(quiet|silence|silent|hush)\b',
}
for label, pat in KW.items():
    hits = [t for t in T if re.search(pat, t['text_corrected'] or '', re.I)]
    pr(f"### {label}: {len(hits)} clip(s)")
    for t in hits[:12]:
        sb = t['score_before']; pts = sb.get('points', {})
        sc = f"s{t['set_no']} {sb['games'].get('DJOKOVIC','?')}-{sb['games'].get('FEDERER','?')} {pts.get('DJOKOVIC','?')}-{pts.get('FEDERER','?')} (Dj-Fe) srv {str(sb.get('server','?')).split()[-1]}"
        clk = hms(t['elapsed_this_point_s']) if t.get('elapsed_this_point_s') is not None else '-'
        pr(f"* {t['utt_id']} clip_i {t['clip_i']} video {t['clip_start_s']:.1f}s, PBP pt {t['point_idx_pbp']}, clock {clk}, {sc}: \"{excerpt(t['text_corrected'], pat)}\"")
    if len(hits) > 12:
        pr(f"* … {len(hits)-12} more")
pr('')

# names of the commentators' addressees
pr('## T16. Address terms in the transcript (whole-word counts over text_corrected)')
for w in ['Boris', 'Tim', 'Andrew', 'John', 'Henman', 'Becker', 'Castle', 'McEnroe']:
    n = sum(len(re.findall(rf'\b{w}\b', t['text_corrected'] or '', re.I)) for t in T)
    pr(f"* {w}: {n}")
pr('')

# first and last transcribed clips
pr('## T17. The first five and last five transcribed clips (chronological), <= 15 words each')
tt = [t for t in T if (t['text_corrected'] or '').strip()]
for t in tt[:5] + tt[-5:]:
    pr(f"* {t['utt_id']} video {t['clip_start_s']:.1f}s PBP pt {t['point_idx_pbp']} clock {hms(t['elapsed_this_point_s']) if t.get('elapsed_this_point_s') is not None else '-'}: \"{excerpt(t['text_corrected'])}\"")
pr('')

# ---------------------------------------------------------------- game count, service games, match summary
pr('## T18. Miscellany')
pr(f"Games in match (R: distinct (SetNo, GameNo)): {len(set((r['SetNo'], r['GameNo']) for r in R))}; tie-breaks: 3 (sets 1, 3, 5).")
pr(f"Points per set: " + ', '.join(f"set {s}: {len(set_rows[s])}" for s in sorted(set_rows)) + '.')
rc_adj = [int(r['RallyCount']) + (1 if (r['P1UnfErr']=='1' or r['P2UnfErr']=='1' or r['P1DoubleFault']=='1' or r['P2DoubleFault']=='1') else 0) for r in R]
pr(f"Mean RallyCount (R, raw) {statistics.mean(int(r['RallyCount']) for r in R):.2f}; points with RallyCount 0 or 1 (serve not returned in play or DF): {sum(1 for r in R if int(r['RallyCount'])<=1)}.")
# serve-and-volley / net
pr(f"Net points (R): Djokovic {sum(int(r['P1NetPoint']) for r in R)} (won {sum(int(r['P1NetPointWon']) for r in R)}), Federer {sum(int(r['P2NetPoint']) for r in R)} (won {sum(int(r['P2NetPointWon']) for r in R)}).")
d1 = sum(float(r['P1DistanceRun']) for r in R); d2 = sum(float(r['P2DistanceRun']) for r in R)
pr(f"Sum of DistanceRun (R, unit unlabelled, presumably metres): Djokovic {d1:.0f}, Federer {d2:.0f}.")
# set 2 and 4 narrative: who broke when
pr('Breaks of serve, whole match (R; set, match game no., server, broken by, clock of the game\'s last point):')
for i, r in enumerate(R, 1):
    if r['GameWinner'] != '0' and r['GameWinner'] != r['PointServer'] and not (r['SetWinner'] != '0' and r['GameNo'] in ('13','25') and r['SetNo'] in ('1','3','5')):
        pr(f"* set {r['SetNo']} game {r['GameNo']}: {NAME[r['PointServer']]} serving, broken by {NAME[r['GameWinner']]} at {r['ElapsedTime']}; games after {r['P1GamesWon']}-{r['P2GamesWon']} (Dj-Fe); {commentary(i, 15)}")
# match metadata from MCP matches file
mm = [r for r in csv.DictReader(open(f'{ROOT}/corpus/raw/sackmann_mcp/charting-m-matches.csv', encoding='utf-8', errors='replace')) if r['match_id'] == '20190714-M-Wimbledon-F-Roger_Federer-Novak_Djokovic']
if mm:
    r = mm[0]
    pr(f"MCP matches file: date {r['Date']}, tournament {r['Tournament']}, round {r['Round']}, time {r['Time']}, court {r['Court']}, surface {r['Surface']}, umpire {r['Umpire']}, best of {r['Best of']}, final TB {r['Final TB?']}, charted by {r['Charted by']}; players {r['Player 1']} (1) and {r['Player 2']} (2), handedness {r['Pl 1 hand']}/{r['Pl 2 hand']}.")
print('\n'.join(out))
```
