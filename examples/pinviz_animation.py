"""Animated growth line — the quarterly MAU series drawing in over time,
exported as a GIF. A creative, motion-first take for a visual platform; the
data is identical to the static charts, just revealed progressively.

Usage
-----
    python examples/pinviz_animation.py   ->  examples/pinviz_growth.gif
"""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.animation import FuncAnimation, PillowWriter

from pinviz.theme import GRID, INK, MUTED, PIN_RED, SUBTLE

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
OUT = ROOT / "examples"
PIN_RED_FILL = "#F7C6CE"


def main() -> None:
    data = pd.read_csv(DATA / "pinterest_mau_quarterly.csv").sort_values(["year", "quarter"])
    x = (data["year"] + (data["quarter"] - 1) * 0.25).tolist()
    y = data["maus_millions"].tolist()
    n = len(x)

    fig, ax = plt.subplots(figsize=(9, 5), facecolor="white")
    ax.set_facecolor("white")
    ax.set_xlim(2018.85, 2025.95)
    ax.set_ylim(0, 700)
    ax.set_xticks(range(2019, 2026))
    ax.set_yticks([0, 200, 400, 600])
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    for side in ("left", "bottom"):
        ax.spines[side].set_color(MUTED)
    ax.tick_params(length=0, colors=SUBTLE, labelsize=11)
    ax.grid(axis="y", color=GRID, linewidth=1)
    ax.set_axisbelow(True)
    ax.set_ylabel("Monthly active users (millions)", color=SUBTLE, fontsize=11)
    ax.set_title("Pinterest's audience hit a record 619M in 2025", loc="left",
                 fontsize=15, fontweight="bold", color=INK, pad=12)

    (line,) = ax.plot([], [], color=PIN_RED, linewidth=3, zorder=3)
    (dot,) = ax.plot([], [], marker="o", markersize=9, markerfacecolor=PIN_RED,
                     markeredgecolor="white", markeredgewidth=1.8, zorder=5)
    label = ax.text(0, 0, "", va="center", ha="left", fontsize=13,
                    fontweight="bold", color=PIN_RED, zorder=6)
    state = {"fill": None}

    reveal, hold = n, 14  # draw in, then hold the final frame

    def update(frame):
        i = min(frame + 2, n)
        xi, yi = x[:i], y[:i]
        line.set_data(xi, yi)
        if state["fill"] is not None:
            state["fill"].remove()
        state["fill"] = ax.fill_between(xi, yi, color=PIN_RED_FILL, alpha=0.6, zorder=1)
        dot.set_data([xi[-1]], [yi[-1]])
        label.set_position((xi[-1] + 0.06, yi[-1]))
        label.set_text(f"{yi[-1]:.0f}M")
        return line, dot, label

    anim = FuncAnimation(fig, update, frames=reveal + hold, interval=90, blit=False)
    out = OUT / "pinviz_growth.gif"
    anim.save(out, writer=PillowWriter(fps=12))
    plt.close(fig)
    print(f"wrote {out.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
