#!/usr/bin/env bash
# Regenerates every figure (PNG + SVG) and every script-generated table of paper/paper.md
# from analysis/formulas/results/ and analysis/metre/results/. Run from the repository root:
#   source .venv/bin/activate && bash paper/figures/make_all.sh
set -euo pipefail
cd "$(dirname "$0")"
for s in fig1_coverage.py fig2_noise.py fig3_refexpr.py fig4_metre.py tables.py; do
  echo "== $s"
  python -I "$s"
done
