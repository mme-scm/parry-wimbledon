#!/usr/bin/env bash
# Regenerates every figure (PNG + SVG), every script-generated table of paper/paper.md and the poem's
# record statistics (results/poem_stats.json) from analysis/formulas/results/, analysis/metre/results/,
# composition/final/poem.jsonl and review/poem_density_v4.json. Run from the repository root:
#   source .venv/bin/activate && bash paper/figures/make_all.sh
set -euo pipefail
cd "$(dirname "$0")"
for s in fig1_coverage.py fig2_noise.py fig3_refexpr.py fig4_metre.py tables.py poem_stats.py fig5_poem.py; do
  echo "== $s"
  python -I "$s"
done
