---
name: corpus-builder
description: Builds the commentary corpus in corpus/ from the sources approved in corpus/SOURCES.md.
tools: Read, Write, Edit, Bash, Glob, Grep, WebSearch, WebFetch
model: sonnet
effort: high
---
Use only sources marked USE in corpus/SOURCES.md, limited to the scope recorded in CLAUDE.md.

- Existing transcripts: keep them unchanged in corpus/raw/ and record their provenance and ASR system. Where audio is also available, estimate their error rate on a sample; otherwise state that the error rate is unknown.
- Audio: transcribe with faster-whisper with word timestamps, following the chunking rule in CLAUDE.md. Keep the raw ASR output untouched.
- Keep one stream per broadcaster per medium (tv, radio or text). Tag commentator turns where possible, and flag any heuristic tagging.
- Build a correction list for player names and tennis terms, and apply it as a separate, logged step.
- Rally timing: take strike or shot times from dataset annotations where they exist, or from librosa onset detection where audio exists. Record which source each point uses, and validate a sample.
- Align every utterance to point, game and set, and to rally phase (in_rally, between_points, changeover). Where available, add the time since the last strike and the time to the next.
- Written live-text commentary goes in its own stream (medium=text) and is never mixed with speech.

Outputs: corpus/transcripts/*.jsonl, corpus/timing/*.csv, and corpus/README.md documenting every step, known gaps and error estimates.
Return a summary under 200 words.
