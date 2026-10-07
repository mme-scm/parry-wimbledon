# Oral-formulaic tennis commentary and a Homeric match narrative

Goal: (1) test Parry–Lord oral-formulaic theory on live tennis commentary of one match; (2) compose ~50 Homeric hexameters narrating the match, built from attested formulae, every line scanned and sourced; (3) translation and a short paper. The reader is a specialist in Homeric and Indo-European studies who will check the Greek and the statistics.

Match: 2019 Wimbledon men's final, Djokovic d. Federer, 14 July 2019 (TennisVL id 20190714-M-Wimbledon-F-Roger_Federer-Novak_Djokovic; Sackmann 2019-wimbledon-1701). Held-out match: 2023 Wimbledon men's final, Alcaraz d. Djokovic. See corpus/SOURCES.md
Corpus scope: (1) MAIN, in-sample: WhisperX ASR transcripts of the single TV commentary track of the 2019 final from the TennisVL test split (broadcaster unnamed in the files; probably BBC TV [unverified]), with TennisVL per-shot hit times, Sackmann slam point-by-point ElapsedTime, and Match Charting Project shot sequences. (2) HELD-OUT: the same layers for the 2023 final. (3) REFERENCE POOL, exploratory and for cross-match formula identification only: the other 18 TennisVL test-split matches' transcripts. (4) WRITTEN CONTRAST (medium=text, never pooled with speech): Cornell/Sports Mole live-text commentary, different matches. No radio, no second broadcaster, no audio, no speaker labels, no word timings: see STATUS.md Phase 0.

## Rules for every agent
- Files are the interface. Write outputs to the paths given; return short summaries.
- Never assert Homeric text, lexicon entries, or scholarship from memory. Homeric claims must be backed by homer/concordance.py output; scholarship must be verified by fetching a source or marked [unverified].
- Greek: Unicode NFC, polytonic. Citations: Il. 6.146, Od. 9.1.
- Every number comes from a script under analysis/ (or paper/) that reruns end to end. No hand-entered results.
- Separate in-sample from held-out, confirmatory from exploratory.
- Never overwrite raw data. Log every correction step.
- Python in .venv; dependencies in requirements.txt.
- The orchestrator keeps STATUS.md: phases, decisions, validation figures, open issues.

## Cloud-session rules
- This runs on a cloud VM: 4 CPUs, 16 GB RAM, 30 GB disk, no GPU. A single shell command can run at most about 40 minutes.
- The human supplies no data. corpus-scout finds the corpus in Phase 0 and records it in corpus/SOURCES.md. Use only sources marked USE there.
- Never download from YouTube or other streaming sites, or from broadcasters' players. Never circumvent access controls or paywalls.
- Datasets that researchers have publicly released for research use may be used for this non-commercial research, with citation. Commit only derived data and excerpts of at most 15 words; never commit the source media or full source texts.
- Downloads go to corpus/raw/ and are never committed. Keep total downloads under 20 GB, and prefer annotation files to media.
- Split any audio into chunks of at most 10 minutes and process each chunk in its own command. Use the most accurate faster-whisper model that transcribes one chunk in under 8 minutes on this machine; record the choice in corpus/README.md.
- Commit and push after every completed step. The VM can be reclaimed, and anything unpushed is lost.
- Never wait for the human. Put anything needing human judgment in FOR_HUMAN.md and continue.
