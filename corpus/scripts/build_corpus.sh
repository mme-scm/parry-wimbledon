#!/usr/bin/env bash
# Rebuild everything in corpus/ (except the raw downloads) from corpus/raw/.
# Usage: bash corpus/scripts/build_corpus.sh      (from the repository root, with .venv present)
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$ROOT"
if [ -f .venv/bin/activate ]; then source .venv/bin/activate; fi
S=corpus/scripts
python -I $S/build_timing.py        > corpus/reports/log_build_timing.txt      # 1. join TennisVL x PBP x MCP; points_*.csv, shots_*.csv
python -I $S/validate_timing.py     > corpus/reports/log_validate_timing.txt   # 2. timing validation vs MCP / PBP
python -I $S/build_transcripts.py   > corpus/reports/log_build_transcripts.txt  # 3. streams jsonl (raw + dedup), alignment
python -I $S/detect_fps.py          > corpus/reports/log_detect_fps.txt        # 3a. per-stream video fps from raw TennisVL (fps_by_stream.json)
python -I $S/apply_fps_correction.py > corpus/reports/log_apply_fps_correction.txt # 3a'. recompute frame-derived times at detected fps; timing_corrections.log
python -I $S/correction_candidates.py > corpus/reports/log_correction_candidates.txt  # 3b. candidate tokens for the hand-curated rules
python -I $S/apply_corrections.py   > corpus/reports/log_apply_corrections.txt  # 4. corrections list + log (separate step)
python -I $S/tag_phase.py           > corpus/reports/log_tag_phase.txt         # 5. heuristic phase / umpire cues
python -I $S/make_manifest.py       > corpus/reports/log_make_manifest.txt     # 6. manifest.json, meta_<stream>.csv
python -I $S/asr_sample.py          > corpus/reports/log_asr_sample.txt        # 7. 500-word sample (gitignored scratch)
python -I $S/asr_proxy.py           > corpus/reports/log_asr_proxy.txt         # 8. ASR proxies (uses corpus/validation/asr_sample_errors.tsv)
python -I $S/align_validation.py    > corpus/reports/log_align_validation.txt  # 9. alignment sample + stats (uses hand verdicts)
python -I $S/make_readme.py         > corpus/reports/log_make_readme.txt       # 10. corpus/README.md
echo "corpus rebuilt"
