# Coding manual: formula spans in tennis commentary (Phase 2b.2)

Purpose: mark, by judgement, the word groups that a Parryan analysis would call formulas, so that the automatic repeated-n-gram inventory can be scored against them. You never see that inventory. Code from the sample alone.

Definition (Parry 1930, adapted): a formula is "a group of words which is regularly employed under the same [situational] conditions to express a given essential idea". "Situational conditions" replaces Parry's metrical conditions: the slot in the point cycle in which the words are spoken. A formulaic system is a frame with one open slot that is filled by alternatives of the same kind ("⟨NUM⟩ 15", "game ⟨NAME⟩", "the ⟨ordinal⟩ set").

Slots (choose one per span):
- SCORE: calling the score after a point (15-30, deuce, advantage, game X, X leads by N games to M, set/match announcements).
- OFFICIAL: umpire, line judge or Hawk-Eye speech relayed by the broadcast (Mr X is challenging, ball was called in, please, new balls please, time violation).
- SHOT: describing a stroke or rally during or just after play (down the line, into the net, big serve out wide, drop shot, forehand cross-court).
- JUDGE: evaluation or explanation (a little bit, that's what he does so well, he needs to, under pressure).
- STAT: statistics, history, background (first serve percentage, 20 Grand Slam titles, back in 2015).
- CROWD: crowd, atmosphere, box, royal box, weather.
- OTHER.

Type: FIXED (the whole string is conventional and invariant) or FRAME (a conventional frame with one open slot; write the frame with ⟨…⟩ for the slot, e.g. "game ⟨NAME⟩").

Confidence: HIGH (a ready-made expression you recognise as conventional in English tennis commentary, used as a unit), MEDIUM (a conventional pattern, but the wording here may be free), LOW (possibly formulaic). Mark LOW sparingly.

Rules:
1. A span is a contiguous group of two or more words inside one utterance. Single words are never spans.
2. Mark a span when the words express one essential idea in a conventional form that commentators reuse, not merely when they are grammatical collocations of English ("of the", "in the", "he has"). Function-word-only groups are never spans.
3. ASR errors: if the intended conventional expression is clear (e.g. "15 left" for "15 love"), mark it and note the error in `note`.
4. Overlapping spans are allowed only when a FIXED span sits inside a FRAME span.
5. Do not code names alone; code a name only inside a frame ("game ⟨NAME⟩", "⟨NAME⟩ leads by").
6. Code every utterance in the sample, including those with no spans (empty list).

Output: one JSON object per line in your output file, in sample order:
{"utt_id": "...", "spans": [{"start_char": int, "end_char": int, "text": "...", "essential_idea": "short phrase", "slot": "SCORE|OFFICIAL|SHOT|JUDGE|STAT|CROWD|OTHER", "type": "FIXED|FRAME", "frame": "game ⟨NAME⟩" or null, "confidence": "HIGH|MEDIUM|LOW", "note": "" }]}
`start_char`/`end_char` are 0-based character offsets into the utterance's `text` field exactly as given (end exclusive); `text` must equal the slice. Spans are at most 15 words.
