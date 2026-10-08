#!/usr/bin/env bash
# Phase 2b (analysis/parry/plan.md, including addendum 1): reruns every number in analysis/parry/report.md (about 75 min on 4 idle CPUs;
# p01 ~17 min, p05 ~16 min, p08 ~15 min). Needs corpus/transcripts/*.jsonl and corpus/transcripts/samples/parry_sample_300.jsonl (gitignored;
# rebuilt by corpus/scripts/build_corpus.sh and analysis/parry/sample.py), corpus/raw/cornell_tennis/extracted/transcripts_matchinfo.json
# (press answers) and the Sackmann slam match files.
# Optional arguments: first and last step to run (0-11), e.g. `bash analysis/parry/run_all.sh 0 3` then `... 4 7` then `... 8 11`
# (each chunk stays under the 40-minute limit of one shell command on the project VM). No arguments = every step.
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$ROOT"
if [ -f .venv/bin/activate ]; then source .venv/bin/activate; fi
D=analysis/parry
mkdir -p $D/results $D/figures
START=${1:-0}
END=${2:-99}
step() { local k=$1 script=$2 log=$3; shift 3; if [ "$k" -ge "$START" ] && [ "$k" -le "$END" ]; then echo "step $k: $script $*"; python -I "$script" "$@" > "$log" 2>&1; fi; }
# ---- pre-registered pipeline (plan sections 0-12); outputs must reproduce byte for byte (checked in step 11)
step 0 $D/tests/test_lib.py $D/results/log_test_lib.txt          # unit tests of lib2b (synthetic)
step 0 $D/tests/test_calibrate.py $D/results/log_test_calibrate.txt  # calibrate.py on a synthetic example with hand-computed answers
step 0 $D/p00_players.py $D/results/log_p00.txt                   # hand/players.tsv (nationalities; 3 entered by hand, [unverified])
step 1 $D/p01_sharing.py $D/results/log_p01.txt                   # 2b.1 pairwise sharing, nulls, baselines; H1a H1b H2a H2b
step 2 $D/p02_core.py $D/results/log_p02.txt                      # 2b.1 genre core, stream-specific share by slot
step 3 $D/p03_clusters_targets.py $D/results/log_p03.txt          # 2b.1 hint/slam/year/gender clusters; pool -> target coverage
step 4 $D/p04_refexpr_pool.py $D/results/log_p04.txt              # 2b.3 referring expressions in all 20 streams (spaCy; +2 post hoc columns)
step 5 $D/p05_thrift.py $D/results/log_p05.txt                    # 2b.3 E1-E3 economy, H4a H4b H5, MDEs
step 5 $D/p05b_h4_declustered.py $D/results/log_p05b.txt          # POST HOC (first round): H4 with one reference per player per utterance
step 6 $D/calibrate.py $D/results/log_calibrate.txt               # 2b.2 (runs only if coding_A.jsonl and coding_B.jsonl exist)
step 7 $D/p06_primary.py $D/results/log_p06.txt                   # Holm over the seven 2b-primary tests
# ---- POST HOC, plan addendum 1 (after review/critic_parry_v1.md)
step 8 $D/p08_largeI.py $D/results/log_p08.txt                    # A1: 100k-token identification sets (TV / Cornell / press); TV-only n>=3 stock
step 8 $D/p09_h2_observed.py $D/results/log_p09.txt               # M1/M2: H2 on observed coverage; unigram concentration; H1 as a check
step 9 $D/calibrate_chance.py $D/results/log_calibrate_chance.txt # M3/M4: calibration at chance level; slot classifier in context mode
step 9 $D/p10_h4_robust.py $D/results/log_p10.txt                 # M5: H4a/H4b robustness and verdict rule; H5 on all 20 streams
step 9 $D/p11_e1_loso.py $D/results/log_p11.txt                   # minor: E1 with leave-one-stream-out inventory; E2 per-slot sums
step 10 $D/p07_figures.py $D/results/log_p07.txt                  # figures from results/
step 11 $D/p12_rerun_check.py $D/results/log_p12.txt              # pre-registered outputs vs commit 476a088
step 11 $D/make_report.py $D/results/log_report.txt               # report.md from results/
echo "Phase 2b rebuilt (steps $START-$END)"
