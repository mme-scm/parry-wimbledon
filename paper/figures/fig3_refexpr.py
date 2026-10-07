"""Figure 3: the referring-expression inventory by player (every form with its token count; the part of
each bar that falls inside an umpire/Hawk-Eye pattern is shown separately). Reads
analysis/formulas/results/refexpr_tokens_tv_{2019wimF,2023wimF}.csv and refexpr_inventory.csv only."""
import pandas as pd

import sys as _sys
from pathlib import Path as _Path

_sys.path.insert(0, str(_Path(__file__).resolve().parent))  # python -I does not add the script dir
from common import BLUE, INK, INK2, MUTED, RES_F, plt, save

tok = pd.concat([pd.read_csv(RES_F / f"refexpr_tokens_tv_{m}.csv") for m in ("2019wimF", "2023wimF")])
tok["umpire"] = tok.umpire_pattern.notna() & (tok.umpire_pattern.astype(str).str.len() > 0)
inv = pd.read_csv(RES_F / "refexpr_inventory.csv")

PANELS = [("tv_2019wimF", "federer", "2019 final: Federer"), ("tv_2019wimF", "djokovic", "2019 final: Djokovic"),
          ("tv_2023wimF", "djokovic", "2023 final: Djokovic"), ("tv_2023wimF", "alcaraz", "2023 final: Alcaraz")]
CAT = {"surname": "surname", "first_name": "first name", "full_name": "full name", "title_surname": "title + surname",
       "epithet": "epithet", "hypocoristic": "hypocoristic"}

fig, axes = plt.subplots(2, 2, figsize=(6.6, 5.6))
for ax, (stream, player, title) in zip(axes.ravel(), PANELS):
    sub = tok[(tok.stream == stream) & (tok.player == player)]
    g = sub.groupby(["expression", "category"]).agg(total=("umpire", "size"), ump=("umpire", "sum")).reset_index()
    # check against the committed inventory table
    chk = inv[(inv.stream == stream) & (inv.player == player)].set_index("expression").tokens
    for _, r in g.iterrows():
        assert int(chk[r.expression]) == int(r.total), (stream, player, r.expression, int(chk[r.expression]), int(r.total))
    g = g.sort_values("total", ascending=True)
    y = range(len(g))
    comm = g.total - g.ump
    ax.barh(y, comm, color=BLUE, height=0.7, linewidth=0, label="commentary (tests C4/C5)")
    ax.barh(y, g.ump, left=comm, color=MUTED, height=0.7, linewidth=0, label="inside an umpire/Hawk-Eye pattern")
    ax.set_yticks(list(y))
    ax.set_yticklabels([f"{e}  ({CAT[c]})" for e, c in zip(g.expression, g.category)], fontsize=7.2)
    for yy, t in zip(y, g.total):
        ax.annotate(str(int(t)), (t, yy), xytext=(3, 0), textcoords="offset points", va="center", fontsize=7, color=INK2)
    ax.set_xlim(0, max(g.total) * 1.14)
    ax.set_title(f"{title} (n = {int(g.total.sum())} references)", loc="left", color=INK)
    ax.grid(axis="y", visible=False)
    ax.tick_params(axis="y", length=0)
for ax in axes[1]:
    ax.set_xlabel("tokens")
h, l = axes[0, 0].get_legend_handles_labels()
fig.legend(h, l, loc="lower center", ncol=2, bbox_to_anchor=(0.5, 0.0))
fig.tight_layout(rect=(0, 0.035, 1, 1))
save(fig, "fig3_refexpr")
