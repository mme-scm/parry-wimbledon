#!/usr/bin/env bash
# Phase 2 formula analysis: reruns every number in analysis/formulas/report.md (about 30 min on 4 idle CPUs after revision 1;
# per-stage runtimes of f04 and f09 are written to results/density_medium_meta.json and results/mde_summary.json).
# Needs corpus/transcripts/*.jsonl (gitignored; rebuilt by corpus/scripts/build_corpus.sh) and, for the press baseline,
# corpus/raw/cornell_tennis/extracted/transcripts_matchinfo.json.
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$ROOT"
if [ -f .venv/bin/activate ]; then source .venv/bin/activate; fi
D=analysis/formulas
mkdir -p $D/results
# Optional argument: first step to run (1-10), e.g. `bash analysis/formulas/run_all.sh 5` to resume after f04
# (f04 alone takes about 20 min on 4 CPUs; run it in the background if commands are time-limited).
START=${1:-1}
step() { local k=$1 script=$2 log=$3; if [ "$k" -ge "$START" ]; then echo "step $k: $script"; python -I "$script" > "$log"; fi; }
step 1 $D/f01_formulas.py $D/results/log_f01.txt   # (a) inventory, per-n, maximal match, cross-stream
step 2 $D/f02_systems.py $D/results/log_f02.txt   # (b) systems
step 3 $D/f03_density_main.py $D/results/log_f03.txt   # D1-D3, D6, D7, S1-S8, C3/R3; revision 1: coverage family, S5b
step 4 $D/f04_density_streams_media.py $D/results/log_f04.txt   # D4 per stream, D5 per corpus + press baseline; D5(ii-b)
step 4 $D/f04b_asr_noise.py $D/results/log_f04b.txt   # POST HOC exploratory: injected ASR-like noise, crossing points
step 5 $D/f05_refexpr.py $D/results/log_f05.txt   # referring expressions (uses hand/*.tsv); umpire-pattern flags
step 6 $D/f06_thrift.py $D/results/log_f06.txt   # thrift / extension, C4/C5, R4/R5 (commentary-only and all tokens)
step 7 $D/f09_power.py $D/results/log_f09.txt   # revision 1: minimum detectable effects, circular-shift nulls
step 8 $D/f07_confirmatory.py $D/results/log_f07.txt   # C1-C5, R1-R5, Holm, corpus contrasts
step 9 $D/f08_top10.py $D/results/log_f08.txt   # top-10 for the composition brief
step 10 $D/make_report.py $D/results/log_report.txt   # report.md from results/
echo "formulas analysis rebuilt"
