#!/usr/bin/env bash
# Regenerates every count quoted in corpus/SOURCES.md from the files fetched by fetch_phase0.sh.
# Outputs go to corpus/raw/derived_scratch/ (gitignored) and stdout.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
RAW="$ROOT/corpus/raw"; S="$ROOT/corpus/scripts"; OUT="$RAW/derived_scratch"
mkdir -p "$OUT"
TEST="$RAW/tennisexpert_repo/data/tennis_data_test_stats_.json"
echo "== TennisVL test_stats: keys";            python3 -I "$S/tennisvl_keys.py" "$TEST"
echo "== TennisVL tennis_vl_test: keys";        python3 -I "$S/tennisvl_keys.py" "$RAW/tennisexpert_repo/data/tennis_vl_test.json"
echo "== TennisVL per-match stats";             python3 -I "$S/tennisvl_match_stats.py" "$TEST" "$OUT/test_match_stats.tsv"
echo "== TennisVL duplication";                 python3 -I "$S/tennisvl_overlap.py" "$TEST" | tee "$OUT/test_overlap.tsv"
echo "== TennisVL language/totals";             python3 -I "$S/tennisvl_language_check.py" "$TEST"
echo "== TennisVL broadcaster hints";           python3 -I "$S/tennisvl_broadcaster_hints.py" "$TEST"
echo "== TennisVL ranking";                     python3 -I "$S/rank_tennisvl_matches.py" "$TEST" "$RAW/sackmann_mcp" "$RAW/sackmann_slam_pbp_hfmirror" "$OUT/tennisvl_test_ranking.tsv"
echo "== TennisVL train list";                  python3 -I "$S/tennisvl_train_list.py" "$RAW/tennisvl_train/tennis_data_train_stats_.json" "$OUT/train_matches.tsv"
echo "== Cornell";                              python3 -I "$S/cornell_stats.py" "$RAW/cornell_tennis/extracted/text_commentaries.json"
for pair in 2019-wimbledon:2019-wimbledon-1701 2023-wimbledon:2023-wimbledon-1701 2020-ausopen:2020-ausopen-1701 2021-frenchopen:2021-frenchopen-1701; do
  echo "== Slam PBP ${pair##*:}"; python3 -I "$S/pbp_match.py" "$RAW/sackmann_slam_pbp_hfmirror/${pair%%:*}-points.csv" "${pair##*:}" | head -3
done
echo "== 2019 Wimbledon final clips (match idx 18)"; python3 -I "$S/tennisvl_transcripts.py" "$TEST" 18 "$OUT/wim2019_clips.jsonl"; python3 -I "$S/check_clip_frames.py" "$OUT/wim2019_clips.jsonl"
echo "== Samples";                              python3 -I "$S/print_samples.py" "$RAW"
