#!/usr/bin/env bash
# Rerun the metre analysis end to end (about 10 minutes on 4 CPUs; s04b_posthoc is the POST HOC addendum-1 step). Needs corpus/transcripts/*.jsonl (gitignored, built by
# corpus/scripts/build_corpus.sh) and corpus/timing/*.csv. Outputs: analysis/metre/results/, analysis/metre/figures/, report.md.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
source "$ROOT/.venv/bin/activate"
cd "$ROOT"
for s in s01_syllable_check s02_build s03_confirmatory s04_exploratory s04b_posthoc s05_figures s06_make_report; do
  echo "== $s"
  python -I "analysis/metre/$s.py" > "analysis/metre/results/log_$s.txt" 2>&1 || { cat "analysis/metre/results/log_$s.txt"; exit 1; }
  tail -n 3 "analysis/metre/results/log_$s.txt"
done
