#!/usr/bin/env bash
# Phase 0 (corpus-scout) downloads: annotation/metadata files only, no media.
# Reproduces everything under corpus/raw/ that corpus/SOURCES.md describes.
# Total transferred is about 400 MB. corpus/raw/ is gitignored and must never be committed.
# Run from anywhere: bash corpus/scripts/fetch_phase0.sh
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
RAW="$ROOT/corpus/raw"
mkdir -p "$RAW"

# 1. TennisVL / TennisExpert repository (blobless clone, then check out data/ only). Pinned commit.
if [ ! -d "$RAW/tennisexpert_repo/.git" ]; then
  git clone -q --filter=blob:none --no-checkout https://github.com/LZYAndy/TennisExpert.git "$RAW/tennisexpert_repo"
fi
git -C "$RAW/tennisexpert_repo" checkout -q 8b778bc1321229639a2cc56c281589a51ff46dfd -- data/ README.md

# 1b. TennisVL training JSON (Google Drive link given in data/README.md of the repo; 118 MB; no transcripts inside).
mkdir -p "$RAW/tennisvl_train"
[ -s "$RAW/tennisvl_train/tennis_data_train_stats_.json" ] || \
  curl -sS -L --max-filesize 200000000 -o "$RAW/tennisvl_train/tennis_data_train_stats_.json" \
    "https://drive.usercontent.google.com/download?id=1raeJJoyGxDyZxNeAo7uk2ngsvlwMQ9SI&export=download&confirm=t"

# 1c. TennisVL paper (arXiv HTML, for the data-construction description and usage terms).
mkdir -p "$RAW/tennisvl_paper"
curl -sS -o "$RAW/tennisvl_paper/arxiv_2603.13397v2.html" https://arxiv.org/html/2603.13397v2

# 2. Cornell tennis dataset (Fu, Danescu-Niculescu-Mizil & Lee 2016).
mkdir -p "$RAW/cornell_tennis/extracted"
curl -sS -o "$RAW/cornell_tennis/tennis_README.txt" https://www.cs.cornell.edu/~liye/tennis_README.txt
curl -sS -o "$RAW/cornell_tennis/tennis.html" https://www.cs.cornell.edu/~liye/tennis.html
[ -s "$RAW/cornell_tennis/tennis_data.zip" ] || curl -sS -o "$RAW/cornell_tennis/tennis_data.zip" https://www.cs.cornell.edu/~liye/tennis_data.zip
unzip -o -q "$RAW/cornell_tennis/tennis_data.zip" -d "$RAW/cornell_tennis/extracted" -x '__MACOSX/*'

# 3. Match Charting Project (Jeff Sackmann / Tennis Abstract), CC BY-NC-SA 4.0. Pinned commit.
mkdir -p "$RAW/sackmann_mcp"
B=https://raw.githubusercontent.com/JeffSackmann/tennis_MatchChartingProject/1813a1309b7ed7ebf1c7e884b32bf675d00e4edf
for f in README.md charting-m-matches.csv charting-w-matches.csv charting-m-points-2010s.csv \
         charting-m-points-2020s.csv charting-w-points-2010s.csv charting-w-points-2020s.csv; do
  [ -s "$RAW/sackmann_mcp/$f" ] || curl -sS -o "$RAW/sackmann_mcp/$f" "$B/$f"
done

# 4. Grand Slam point-by-point (Sackmann), via the Hugging Face archival mirror (the original GitHub
#    repo JeffSackmann/tennis_slam_pointbypoint returned 404 / no access on 2026-10-07). Pinned revision.
mkdir -p "$RAW/sackmann_slam_pbp_hfmirror"
B=https://huggingface.co/datasets/Aneeshers/tennis-sackmann-archive/resolve/8ac86f7c62889b5d5c4cfec4c6403edcb8c5d993
for f in LICENSE README.md slam_pointbypoint/UPSTREAM_README.md; do
  curl -sS -L -o "$RAW/sackmann_slam_pbp_hfmirror/$(basename "$f")" "$B/$f"
done
for s in 2019-wimbledon 2020-ausopen 2021-frenchopen 2023-wimbledon; do
  [ -s "$RAW/sackmann_slam_pbp_hfmirror/$s-points.csv" ] || \
    curl -sS -L -o "$RAW/sackmann_slam_pbp_hfmirror/$s-points.csv" "$B/slam_pointbypoint/$s-points.csv"
done
for s in 2019-ausopen 2019-wimbledon 2020-ausopen 2020-frenchopen 2021-ausopen 2021-frenchopen 2021-usopen \
         2022-usopen 2023-usopen 2023-wimbledon 2024-usopen 2024-wimbledon; do
  curl -sS -L -o "$RAW/sackmann_slam_pbp_hfmirror/$s-matches.csv" "$B/slam_pointbypoint/$s-matches.csv"
done

# 5. TenniSet (Faulkner & Dick 2017): README, licence, three small annotation files (checked, not used).
mkdir -p "$RAW/tenniset/annotations"
curl -sS -o "$RAW/tenniset/README_master.md" https://raw.githubusercontent.com/HaydenFaulkner/Tennis/master/README.md
for pair in 1Zl2dpzlW1iWVXBzhQbPF1WCgZxQfWup1:captions.txt 1BG6v6OcGaIOfduGPCulpP71fR2-OAIj6:points.txt \
            1kc7UGmyb97Jzgqkd3rjzlcqafoSOyi-R:V006.json; do
  id=${pair%%:*}; n=${pair##*:}
  curl -sS -L --max-filesize 20000000 -o "$RAW/tenniset/annotations/$n" \
    "https://drive.usercontent.google.com/download?id=$id&export=download&confirm=t"
done

# 6. Small metadata/preview files of datasets that were checked and rejected.
mkdir -p "$RAW/livecc" "$RAW/hf_misc" "$RAW/f3set"
B=https://huggingface.co/datasets/chenjoya/Live-WhisperX-526K/resolve/main
curl -sS -L -o "$RAW/livecc/README.md" "$B/README.md"
curl -sS -L -o "$RAW/livecc/live_whisperx_100_for_preview.json" "$B/live_whisperx_100_for_preview.json"
curl -sS -L -o "$RAW/hf_misc/SCBench_CommentarySet_README.md" https://huggingface.co/datasets/SCBench/CommentarySet/resolve/main/README.md
curl -sS -L -o "$RAW/hf_misc/TennisNLData_sample.json" \
  "https://huggingface.co/datasets/ramizheman/TennisNLData/resolve/main/1981-07-01_Wimbledon_Pam_Shriver_vs_Chris_Evert.json"
curl -sS -o "$RAW/f3set/README_main.md" https://raw.githubusercontent.com/F3Set/F3Set/main/README.md

# Checksums observed on 2026-10-07 (first 16 hex digits of sha256):
#   tennisexpert_repo/data/tennis_data_test_stats_.json  49faad1351c811cc
#   tennisexpert_repo/data/tennis_vl_test.json           c9c2c22d1f1d29bd
#   tennisvl_train/tennis_data_train_stats_.json         dd14027989b93b8e
#   cornell_tennis/tennis_data.zip                       0e1c147dd5b4e151
#   sackmann_slam_pbp_hfmirror/2019-wimbledon-points.csv 7e894b03d277547a
#   sackmann_mcp/charting-m-points-2010s.csv             2719cdc136b64698
echo "done; du -sh $RAW:"; du -sh "$RAW"
