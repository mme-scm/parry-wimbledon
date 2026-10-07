# FOR_HUMAN

These items need human judgment or human action. Agents keep working without waiting for answers.
Agents may append sections; do not delete other agents' entries.

## Corpus (Phase 0, corpus-scout, 2026-10-07)

### What the current corpus cannot give

No acceptable source has the same match from more than one broadcaster, or from both TV and radio. The usable
corpus (see `corpus/SOURCES.md`) is:
* one TV commentary track per match, as WhisperX ASR text from the TennisVL research release;
* timing from Sackmann's point-by-point data and the Match Charting Project;
* Cornell's written live text from different matches, as a contrast.

The routes below would add a second broadcaster or a radio track for the recommended match: the 2019 Wimbledon
men's final, 14 July 2019. Each one needs a licence, an institutional login or an agreement that only you can
provide. Agents have not used them and will not.

### Routes that would add broadcasters or media

1. **Box of Broadcasts (BoB), Learning on Screen.**
   * Access: through a UK university that holds an ERA licence and Learning on Screen membership.
   * Search results describe BoB as on-demand TV and radio, recorded from 75+ free-to-air channels, for teaching
     and research [unverified: the learningonscreen.ac.uk page returned 403 to the agent].
   * Would add: the BBC TV coverage of the 2019 final, and BBC Radio 5 Live or 5 Sports Extra commentary of the
     same match if BoB recorded it [unverified]. Full-length audio would allow our own faster-whisper transcript
     with word timestamps, and a real TV-against-radio comparison of one match.
   * Ask your library whether BoB holds both programmes, and whether its terms allow you to extract audio
     locally for transcription and analysis.
2. **BBC Archives / BBC Sport licensing.**
   * A research licence for the 2019 final from BBC One/Two, BBC Radio 5 Live and 5 Sports Extra.
   * Would add: an authoritative broadcaster label (TennisVL only implies BBC), radio commentary, and
     clean-provenance audio.
3. **Internet Archive radio collection (BBC Radio 5 Live, 2016 onwards).**
   * Items are `stream_only` and `access-restricted-item: true`. Each has machine ASR (`.asr.srt`) and audio.
   * There is **no recording for 13–15 July 2019**.
   * There are 3-hour items on dates of other TennisVL test matches: 11 Sep 2021, 21:00–24:00 BST (Raducanu v
     Fernandez, US Open final), and 30 Jan 2022 (Nadal v Medvedev, AO final). Whether 5 Live carried
     commentary in those hours is unverified.
   * Route: Internet Archive's researcher access. If granted, a TennisVL match could gain a radio track.
4. **Other rights holders for the same match.**
   * Candidates include ESPN (US), Nine/Stan (Australia), Eurosport, Amazon Prime Video and Tennis Channel.
     Which of them held rights to which match is unverified.
   * Archive licences from any of these would give a second or third broadcaster for one match. TennisVL's
     2022 AO final transcript names "Brad" 19 times, and the 2023 Wimbledon final names "Todd" 4 times. Both are
     hints of non-BBC broadcasters [unverified].
5. **The Guardian Open Platform** (free developer key; registration).
   * The Guardian's minute-by-minute live blog of the 2019 final would give a timestamped written live text of
     **the same match**, from a named outlet. That makes a better written contrast than Cornell, which covers
     other matches.
   * Third-party summaries say the free key covers non-commercial research and returns full body text
     [unverified: the agent could not fetch open-platform.theguardian.com].
   * Needs you to register and accept the terms.
6. **SCBench CommentarySet** (https://huggingface.co/datasets/SCBench/CommentarySet).
   * Gated: "available upon request and only for academic research".
   * Contents and sports are not inspected. Worth a request if you want another research-licensed sports
     commentary set.
7. **ICE-GB (UCL) and other ICE components.**
   * UCL's description lists a "spontaneous commentaries" category (20 texts in ICE-GB). What they cover, and
     whether any is tennis, is unverified.
   * Paid or registered licence.
   * Would add: human-transcribed spoken commentary, possibly useful for diachronic comparison [unverified].
8. **Troveo Sports Commentary** (https://www.troveo.ai/datasets/sports-commentary).
   * Commercial. The page claims 1.1M+ hours across 30+ sports including tennis. Terms are not published.
   * Only relevant if the project can buy a licence.
9. **Official data (AELTC / IBM).**
   * Licensed ball-by-ball data with wall-clock timestamps would make TV-time-to-match-time alignment exact.
     The current alignment needs an estimated offset.

### Decisions for you

1. **TennisVL terms scope.**
   * The paper says: "We mandate that this dataset be utilized strictly for academic research in sports video understanding".
     The full sentence continues "and automated commentary generation".
   * Our use is non-commercial academic linguistic analysis of the commentary transcripts. The agent marked it USE,
     under CLAUDE.md's rule for research datasets.
   * If you want certainty, email the authors (Zhaoyu Liu et al., arXiv:2603.13397) and ask:
     * (a) whether linguistic research is within scope;
     * (b) for the source YouTube URLs, which the paper says are provided but the released files lack, and which
       would identify each broadcaster;
     * (c) for raw WhisperX output with word timestamps and speaker turns;
     * (d) for transcripts of the 182 training matches. The released train file has none.
2. **ShareAlike.**
   * The Match Charting Project and Sackmann point-by-point data are CC BY-NC-SA 4.0.
   * Derived data committed to this repo, such as aligned point tables, must carry CC BY-NC-SA 4.0 with
     attribution to Jeff Sackmann / Tennis Abstract.
   * Decide the repository's licence for `corpus/` derived files accordingly.
3. **Mirror provenance.**
   * The original `JeffSackmann/tennis_slam_pointbypoint` repository was unreachable on 2026-10-07.
   * The agent used the Hugging Face archival mirror `Aneeshers/tennis-sackmann-archive`, revision 8ac86f7.
   * Its 2019 Wimbledon final agrees with the MCP point count (422 points), but the mirror is third-party.
4. **LLM-generated commentary as a contrast.**
   * TennisVL's `gpt` field holds Gemini 3 Pro "commentary" built from the ASR and shot data.
   * It is not oral composition and is marked DON'T USE as commentary.
   * Decide whether the paper should include it as an explicitly labelled LLM contrast.
5. **Wording in the paper.**
   * The paper must state that the spoken corpus is ASR text of a single TV commentary per match, with no audio
     and no word-level timing.
   * Treat the broadcaster label (probably BBC TV for the 2019 final) as an inference from names the commentators
     use, not a fact from the data.

## Formula analysis (Phase 2, formula-analyst, 2026-10-07)

1. **Press-conference transcripts used as a baseline.** `corpus/SOURCES.md` row O lists the Cornell press conferences as
   DON'T USE *as commentary*. At the orchestrator's request, the player answers in
   `corpus/raw/cornell_tennis/extracted/transcripts_matchinfo.json` (same Cornell release as the USE source G, same terms)
   are used only as a spoken, non-commentary baseline for formulaic density (test C1 and the per-medium table). Every row that
   depends on them is labelled `press_answers` in `analysis/formulas/results/`. If you do not accept this use, drop
   those rows and test C1; nothing else depends on them.
2. **Kuiper and Austin (race calling).** No fetched catalogue record lists a Kuiper and Austin chapter on New Zealand race
   callers (believed to be in Bell and Holmes, eds, *New Zealand Ways of Speaking English*, 1990; chapter title, co-author's first
   name and pages [unverified]); only the edited volume was confirmed (Open Library, Crossref review record). It is cited as
   [unverified] in `analysis/formulas/report.md`. A library catalogue lookup would settle it.
3. **Hand verdicts in `analysis/formulas/hand/`.** The referent of 25 descriptive epithets ("the champion", "the world
   number one", "the young man", ...) and the syntactic slot of a 40-expression validation sample were judged by the
   analyst. Please spot-check them.

## Composition decisions taken provisionally (Phase 4, round 1)
- **Greek renderings of "Djokovic".** The brief's Ζοκοβίδης needs a long ι that no Homeric -ίδης shows, and Νοβάκος a long non-Ionic ᾱ (review/philology_v1.md, lines 48, 50, 51). The orchestrator replaced them with Ζοκοβείδης (patronymic in -είδης from Ζοκοβεύς, as Πηλείδης from Πηλεύς; Đoković is itself a patronymic) and Νοβήκος (Ionic η for ᾱ). A Homerist may prefer another convention (e.g. keeping the Serbian vowel quantities and accepting a metre-only licence, or a different base name). Σέρβος and Ζοκοβεύς are unchanged; Ἑλβέτιος is a Latin-based coinage for "the Swiss", flagged as such in the brief.
- **Ῥογῆρος ἰσόθεος φώς** was rejected because ς + ϝ making position is unattested for ἰσόθεος; the composer must use the name elsewhere. If a human judges the licence acceptable (cf. the general treatment of digamma after a consonant), lines 27/49 of v1 could be restored.
- **ἐξεναρίζω for "won the game / broke serve"** is limited to the aristeia (two uses); a human may prefer to allow the metaphor throughout or to ban it.
- **δίς + verb** ("twice") is avoided as un-Homeric (only δὶς τόσσον Od. 9.491); a human may accept it as an extension.
