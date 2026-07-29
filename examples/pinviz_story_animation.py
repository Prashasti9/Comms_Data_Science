"""Animated 'story' — the key panels build in sequence (growth line ->
revenue bars -> user/revenue split -> takeaway), exported as a GIF. A
motion-first companion to the static poster; identical data, revealed over
time. Play it as a short flourish alongside the static poster.

Usage
-----
    python examples/pinviz_story_animation.py   ->  examples/pinviz_story.gif
"""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.animation import FuncAnimation, PillowWriter
from matplotlib.gridspec import GridSpec
from matplotlib.patches import FancyBboxPatch

from pinviz.theme import GRID, INK, MUTED, PIN_RED, SUBTLE

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
OUT = ROOT / "examples"
PAGE = "#F3F1EF"
PIN_RED_FILL = "#F7C6CE"
GREYS = ["#8A8A8A", "#BDBDBD"]


def _clamp(v):
    return max(0.0, min(1.0, v))


def _seg(frame, start, end):
    return _clamp((frame - start) / (end - start))


def draw_growth(ax, frac, x, y):
    ax.cla()
    ax.set_xlim(2018.85, 2025.95)
    ax.set_ylim(0, 700)
    ax.set_xticks(range(2019, 2026))
    ax.set_yticks([0, 200, 400, 600])
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    for side in ("left", "bottom"):
        ax.spines[side].set_color(MUTED)
    ax.tick_params(length=0, colors=SUBTLE, labelsize=9)
    ax.grid(axis="y", color=GRID, linewidth=1)
    ax.set_axisbelow(True)
    ax.set_ylabel("Monthly active users (M)", color=SUBTLE, fontsize=9)
    ax.set_title("A decade of growth", loc="left", fontsize=12,
                 fontweight="bold", color=INK, pad=8)
    if frac <= 0:
        return
    k = min(len(x), max(2, round(frac * len(x))))
    xi, yi = x[:k], y[:k]
    ax.fill_between(xi, yi, color=PIN_RED_FILL, alpha=0.6, zorder=1)
    ax.plot(xi, yi, color=PIN_RED, linewidth=2.5, zorder=3)
    ax.plot([xi[-1]], [yi[-1]], marker="o", markersize=7, markerfacecolor=PIN_RED,
            markeredgecolor="white", markeredgewidth=1.5, zorder=5)
    ax.text(xi[-1] + 0.06, yi[-1], f"{yi[-1]:.0f}M", va="center", ha="left",
            fontsize=11, fontweight="bold", color=PIN_RED)


def draw_revenue(ax, frac, years, rev):
    ax.cla()
    ax.set_ylim(0, max(rev) * 1.22)
    ax.set_xlim(min(years) - 0.6, max(years) + 0.6)
    ax.set_xticks(years)
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    for side in ("left", "bottom"):
        ax.spines[side].set_color(MUTED)
    ax.set_yticks([])
    ax.tick_params(length=0, colors=SUBTLE, labelsize=9)
    ax.set_title("Revenue grew nearly 4x, to $4.2B", loc="left", fontsize=12,
                 fontweight="bold", color=INK, pad=8)
    if frac <= 0:
        return
    heights = [v * frac for v in rev]
    colors = [PIN_RED if yr == 2025 else MUTED for yr in years]
    bars = ax.bar(years, heights, width=0.62, color=colors,
                  edgecolor="#333333", linewidth=1.0)
    if frac > 0.98:
        for bar, v in zip(bars, rev):
            ax.text(bar.get_x() + bar.get_width() / 2, v + max(rev) * 0.03,
                    f"${v/1000:.1f}B", ha="center", va="bottom",
                    fontsize=8, fontweight="bold", color=INK)


def draw_split(ax, frac, cats, u_pct, r_pct):
    ax.cla()
    ax.set_xlim(0, 100)
    ax.set_ylim(-0.6, 1.6)
    ax.set_xticks([])
    ax.set_yticks([0, 1])
    ax.set_yticklabels(["Users", "Revenue"], fontsize=9, color=INK)
    for side in ("top", "right", "left", "bottom"):
        ax.spines[side].set_visible(False)
    ax.tick_params(length=0)
    ax.invert_yaxis()
    ax.set_title("Rest of World: 58% of users, 7% of revenue", loc="left",
                 fontsize=12, fontweight="bold", color=INK, pad=8)
    if frac <= 0:
        return
    color_for, gi = {}, 0
    for c in cats:
        if c == "Rest of World":
            color_for[c] = PIN_RED
        else:
            color_for[c] = GREYS[gi % len(GREYS)]
            gi += 1
    left_u = left_r = 0
    for c, up, rp in zip(cats, u_pct, r_pct):
        ax.barh(0, up * frac, left=left_u, height=0.5, color=color_for[c],
                edgecolor="white", linewidth=1.3)
        ax.barh(1, rp * frac, left=left_r, height=0.5, color=color_for[c],
                edgecolor="white", linewidth=1.3)
        if frac > 0.98:
            tc = "white" if c == "Rest of World" else INK
            if up > 6:
                ax.text(left_u + up / 2, 0, f"{up:.0f}%", ha="center",
                        va="center", fontsize=8, color=tc, fontweight="bold")
            if rp > 6:
                ax.text(left_r + rp / 2, 1, f"{rp:.0f}%", ha="center",
                        va="center", fontsize=8, color=tc, fontweight="bold")
        left_u += up * frac
        left_r += rp * frac


def draw_callout(ax, alpha):
    ax.cla()
    ax.axis("off")
    if alpha <= 0:
        return
    band = FancyBboxPatch((0.02, 0.2), 0.96, 0.6,
                          boxstyle="round,pad=0,rounding_size=0.06",
                          transform=ax.transAxes, facecolor=PIN_RED,
                          edgecolor="none", alpha=alpha)
    ax.add_patch(band)
    ax.text(0.5, 0.5, "A US & Canada user is worth about 35x a Rest-of-World user.",
            transform=ax.transAxes, ha="center", va="center", color="white",
            fontsize=11.5, fontweight="bold", alpha=alpha)


def main() -> None:
    mau = pd.read_csv(DATA / "pinterest_mau_quarterly.csv").sort_values(["year", "quarter"])
    x = (mau["year"] + (mau["quarter"] - 1) * 0.25).tolist()
    y = mau["maus_millions"].tolist()
    rev_df = pd.read_csv(DATA / "pinterest_revenue.csv").sort_values("year")
    years = rev_df["year"].tolist()
    rev = rev_df["revenue_musd"].tolist()
    reg = pd.read_csv(DATA / "pinterest_regions_q4_2025.csv")
    cats = list(reg["region"])
    u_pct = [100 * v / reg["maus_millions"].sum() for v in reg["maus_millions"]]
    r_pct = [100 * v / reg["revenue_musd"].sum() for v in reg["revenue_musd"]]

    fig = plt.figure(figsize=(8, 11), facecolor=PAGE)
    gs = GridSpec(4, 1, figure=fig, height_ratios=[3, 2.2, 1.8, 0.8],
                  hspace=0.55, left=0.12, right=0.94, top=0.90, bottom=0.05)
    ax_g = fig.add_subplot(gs[0]); ax_r = fig.add_subplot(gs[1])
    ax_s = fig.add_subplot(gs[2]); ax_c = fig.add_subplot(gs[3])
    for a in (ax_g, ax_r, ax_s, ax_c):
        a.set_facecolor(PAGE)
    fig.text(0.12, 0.955, "PINTEREST  ·  FULL-YEAR 2025", fontsize=9,
             fontweight="bold", color=PIN_RED)
    fig.text(0.12, 0.925, "Pinterest's split screen", fontsize=22,
             fontweight="bold", family="serif", color=INK)

    # Phase boundaries (frames): growth, revenue, split, callout, hold.
    G, R, S, C, END = 16, 28, 40, 49, 62

    def update(frame):
        draw_growth(ax_g, _seg(frame, 0, G), x, y)
        draw_revenue(ax_r, _seg(frame, G, R), years, rev)
        draw_split(ax_s, _seg(frame, R, S), cats, u_pct, r_pct)
        draw_callout(ax_c, _seg(frame, S, C))

    anim = FuncAnimation(fig, update, frames=END, interval=90, blit=False)
    out = OUT / "pinviz_story.gif"
    anim.save(out, writer=PillowWriter(fps=11))
    plt.close(fig)
    print(f"wrote {out.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
