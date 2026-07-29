"""Compose the pinviz charts into a single one-page infographic poster.

Inspired by the editorial technique of Simon Scarr's "Iraq's Bloody Toll":
a serif headline, an intro deck, one dominant annotated hero chart, and a
row of supporting charts, all in a single accent colour on one page.

Writes ``examples/pinviz_poster.pdf`` and ``examples/pinviz_poster.png``.

Usage
-----
    python examples/pinviz_poster.py
"""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.gridspec import GridSpec

from pinviz.theme import GRID, INK, MUTED, PIN_RED, SUBTLE

plt.rcParams["text.parse_math"] = False

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
OUT = ROOT / "examples"

# Light tint of the brand red for area fills.
PIN_RED_FILL = "#F7C6CE"
GREYS = ["#8A8A8A", "#BDBDBD"]

# Dated events for the hero chart (year, y-value, label, text offset).
EVENTS = [
    (2019, 335, "2019  IPO at 335M users", (14, 8)),
    (2020, 459, "2020  Pandemic surge: +37% to 459M", (14, 8)),
    (2021, 431, "2021  Reopening dip to 431M", (10, -34)),
    (2025, 619, "2025  Record 619M users", (-6, 14)),
]


def draw_hero(ax, mau):
    """Large annotated MAU growth line — the poster's centrepiece."""
    x, y = mau["year"], mau["maus_millions"]
    ax.fill_between(x, y, color=PIN_RED_FILL, alpha=0.6, zorder=1)
    ax.plot(x, y, color=PIN_RED, linewidth=3, marker="o", markersize=6, zorder=3)
    ax.set_ylim(0, 700)
    ax.set_xlim(2018.6, 2025.7)

    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    for side in ("left", "bottom"):
        ax.spines[side].set_color(MUTED)
    ax.tick_params(length=0, colors=SUBTLE, labelsize=10)
    ax.grid(axis="y", color=GRID, linewidth=1)
    ax.set_axisbelow(True)
    ax.set_xticks(list(x))
    ax.set_yticks([0, 200, 400, 600])
    ax.set_ylabel("Monthly active users (millions)", color=SUBTLE, fontsize=10)

    for yr, val, label, (dx, dy) in EVENTS:
        ax.annotate(
            label, xy=(yr, val), xytext=(dx, dy), textcoords="offset points",
            fontsize=9.5, color=INK, fontweight="bold",
            ha="left" if dx >= 0 else "right",
            arrowprops=dict(arrowstyle="-", color=MUTED, linewidth=1),
        )
    ax.set_title("A decade of growth, in monthly active users",
                 loc="left", fontsize=13, fontweight="bold", color=INK, pad=10)


def draw_share_gap(ax, reg):
    """100%-normalised paired bars: user share vs revenue share."""
    cats = list(reg["region"])
    users = reg["maus_millions"]
    rev = reg["revenue_musd"]
    u_pct = [100 * v / users.sum() for v in users]
    r_pct = [100 * v / rev.sum() for v in rev]

    color_for = {}
    gi = 0
    for c in cats:
        if c == "Rest of World":
            color_for[c] = PIN_RED
        else:
            color_for[c] = GREYS[gi % len(GREYS)]
            gi += 1

    left_u = left_r = 0
    for i, c in enumerate(cats):
        ax.barh("Users", u_pct[i], left=left_u, color=color_for[c])
        ax.barh("Revenue", r_pct[i], left=left_r, color=color_for[c])
        if u_pct[i] > 6:
            ax.text(left_u + u_pct[i] / 2, 0, f"{u_pct[i]:.0f}%", ha="center",
                    va="center", fontsize=9,
                    color="white" if c == "Rest of World" else INK, fontweight="bold")
        if r_pct[i] > 6:
            ax.text(left_r + r_pct[i] / 2, 1, f"{r_pct[i]:.0f}%", ha="center",
                    va="center", fontsize=9,
                    color="white" if c == "Rest of World" else INK, fontweight="bold")
        left_u += u_pct[i]
        left_r += r_pct[i]

    ax.set_xlim(0, 100)
    ax.set_xticks([])
    ax.tick_params(length=0, colors=INK, labelsize=10)
    ax.invert_yaxis()
    for side in ("top", "right", "left", "bottom"):
        ax.spines[side].set_visible(False)
    ax.set_title("Rest of World is 58% of users but 7% of revenue",
                 loc="left", fontsize=12, fontweight="bold", color=INK, pad=8)


def draw_hbar(ax, cats, vals, colors, fmt, title):
    """Generic spotlighted horizontal bar with end labels."""
    bars = ax.barh(cats, vals, color=colors)
    ax.set_xticks([])
    pad = max(vals) * 0.02
    for bar, v in zip(bars, vals):
        ax.text(bar.get_width() + pad, bar.get_y() + bar.get_height() / 2,
                fmt.format(v), va="center", ha="left", fontsize=10,
                fontweight="bold", color=INK)
    ax.tick_params(length=0, colors=INK, labelsize=10)
    for side in ("top", "right", "bottom"):
        ax.spines[side].set_visible(False)
    ax.spines["left"].set_color(MUTED)
    ax.margins(x=0.18)
    ax.set_title(title, loc="left", fontsize=12, fontweight="bold", color=INK, pad=8)


def main() -> None:
    mau = pd.read_csv(DATA / "pinterest_mau.csv").sort_values("year")
    reg = pd.read_csv(DATA / "pinterest_regions_q4_2025.csv")
    reg_rev = reg.sort_values("revenue_musd")
    reg_arpu = reg.assign(arpu=reg["revenue_musd"] / reg["maus_millions"]).sort_values("arpu")

    fig = plt.figure(figsize=(11, 15.5), facecolor="white")
    gs = GridSpec(
        6, 2, figure=fig,
        height_ratios=[0.55, 1.05, 2.9, 1.5, 1.6, 0.3],
        hspace=0.55, wspace=0.28,
        left=0.08, right=0.94, top=0.96, bottom=0.03,
    )

    # --- Title band ---
    ax_title = fig.add_subplot(gs[0, :]); ax_title.axis("off")
    ax_title.text(0, 0.5, "Pinterest's split screen", fontsize=40,
                  fontweight="bold", family="serif", color=INK, va="center")

    # --- Deck + big numbers ---
    ax_deck = fig.add_subplot(gs[1, 0]); ax_deck.axis("off")
    ax_deck.text(
        0, 1.0,
        "By the end of 2025, Pinterest had grown to a\n"
        "record 619 million monthly users and $4.2\n"
        "billion in annual revenue. But where those\n"
        "users live looks nothing like where the money\n"
        "comes from — the gap that defines its next decade.",
        fontsize=12, color=INK, va="top", linespacing=1.55,
    )

    ax_big = fig.add_subplot(gs[1, 1]); ax_big.axis("off")
    ax_big.text(0.0, 0.90, "619M", fontsize=30, fontweight="bold", color=PIN_RED, va="center")
    ax_big.text(0.0, 0.66, "monthly active users  (+12% YoY)", fontsize=11, color=SUBTLE, va="center")
    ax_big.text(0.0, 0.36, "$4.2B", fontsize=30, fontweight="bold", color=INK, va="center")
    ax_big.text(0.0, 0.12, "FY2025 revenue  (+16% YoY)", fontsize=11, color=SUBTLE, va="center")

    # --- Hero chart ---
    draw_hero(fig.add_subplot(gs[2, :]), mau)

    # --- Signature share-gap ---
    draw_share_gap(fig.add_subplot(gs[3, :]), reg)

    # --- Supporting bars ---
    draw_hbar(
        fig.add_subplot(gs[4, 0]),
        list(reg_rev["region"]), list(reg_rev["revenue_musd"]),
        [PIN_RED if c == "US & Canada" else MUTED for c in reg_rev["region"]],
        "${:,.0f}M", "Q4 revenue by region",
    )
    draw_hbar(
        fig.add_subplot(gs[4, 1]),
        list(reg_arpu["region"]), list(reg_arpu["arpu"]),
        [PIN_RED if c == "US & Canada" else MUTED for c in reg_arpu["region"]],
        "${:,.2f}", "Implied revenue per user",
    )

    # --- Footer ---
    ax_foot = fig.add_subplot(gs[5, :]); ax_foot.axis("off")
    ax_foot.text(0, 0.5,
                 "Source: Pinterest Q4 & Full-Year 2025 earnings report (Feb 2026).  "
                 "Built with pinviz.",
                 fontsize=9, color=SUBTLE, va="center")

    fig.savefig(OUT / "pinviz_poster.pdf", bbox_inches="tight")
    fig.savefig(OUT / "pinviz_poster.png", dpi=150, bbox_inches="tight")
    plt.close(fig)
    print("wrote examples/pinviz_poster.pdf")
    print("wrote examples/pinviz_poster.png")


if __name__ == "__main__":
    main()
