"""Compose the pinviz charts into a single one-page infographic poster.

Inspired by the editorial technique of Simon Scarr's "Iraq's Bloody Toll":
a headline, an intro deck, one dominant annotated hero chart, and a row of
supporting charts, all in a single accent colour on one page.

Pinterest cues: the brand logo mark, and a light background with rounded
white "cards" behind each chart to echo Pinterest's masonry pin-board UI.

Writes ``examples/pinviz_poster.pdf`` and ``examples/pinviz_poster.png``.

Usage
-----
    python examples/pinviz_poster.py
"""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.patheffects as pe
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.gridspec import GridSpec
from matplotlib.patches import Annulus, Circle, FancyBboxPatch, Polygon

from pinviz.theme import GRID, INK, MUTED, PIN_RED, SUBTLE

plt.rcParams["text.parse_math"] = False

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
OUT = ROOT / "examples"

# Palette. A warm off-white page makes the white cards read as a pin-board.
PAGE = "#F3F1EF"
CARD = "#FFFFFF"
PIN_RED_FILL = "#F7C6CE"
GREYS = ["#8A8A8A", "#BDBDBD"]

# year, value, label, (dx, dy) offset in points, horizontal alignment.
# The last event is the focal point and gets a red chip; the rest are white.
EVENTS = [
    (2019, 335, "2019 · IPO at 335M users", (10, -36), "left"),
    (2020, 459, "2020 · Pandemic surge, +37% to 459M", (10, 34), "left"),
    (2021, 431, "2021 · Reopening dip to 431M", (10, -36), "left"),
    (2025, 619, "2025 · Record 619M users", (-12, 18), "right"),
]


def add_logo(fig, left, bottom, size):
    """Draw a Pinterest-style badge: the pin-shaped 'P' (a white ring flowing
    into a tapered needle) on a solid red circle with a soft shadow.

    A stylised mark drawn from scratch for editorial identification — it
    approximates the brand's pin/'P' glyph rather than copying an official
    asset or its custom typeface.
    """
    ax = fig.add_axes([left, bottom, size, size * (fig.get_figwidth() / fig.get_figheight())])
    ax.set_aspect("equal")
    ax.axis("off")

    badge = Circle((0.5, 0.5), 0.46, facecolor=PIN_RED, edgecolor="none", zorder=2)
    badge.set_path_effects(
        [pe.withSimplePatchShadow(offset=(2, -3), shadow_rgbFace="#9A9A9A", alpha=0.4)]
    )
    ax.add_patch(badge)

    # The needle first (behind the ring), tapering to a point at lower-left.
    ax.add_patch(Polygon(
        [(0.40, 0.54), (0.60, 0.54), (0.45, 0.17)], closed=True,
        facecolor="white", edgecolor="none", zorder=3,
    ))
    # The bowl of the P / head of the pin: a thick white ring.
    ax.add_patch(Annulus((0.545, 0.60), 0.185, 0.092,
                         facecolor="white", edgecolor="none", zorder=4))
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    return ax


def add_card(ax_bg, axes, pad_y=0.030, extra_top=0.0, x0=0.045, x1=0.955, pad_bottom=None):
    """Draw a full-width rounded white card with a soft shadow behind ``axes``.

    Cards are drawn into ``ax_bg`` — a full-canvas axes pinned behind
    everything (negative zorder) — so they never paint over the charts. The
    horizontal extent is fixed (``x0``/``x1``) so every card aligns and left-
    side axis labels always fall inside the card. ``pad_bottom`` overrides the
    bottom padding independently (e.g. to clear text that overflows an axis).
    """
    pad_bottom = pad_y if pad_bottom is None else pad_bottom
    boxes = [ax.get_position() for ax in axes]
    y0 = min(b.y0 for b in boxes) - pad_bottom
    y1 = max(b.y1 for b in boxes) + pad_y + extra_top
    card = FancyBboxPatch(
        (x0, y0), x1 - x0, y1 - y0,
        boxstyle="round,pad=0,rounding_size=0.012",
        transform=ax_bg.transAxes, facecolor=CARD, edgecolor="none",
    )
    card.set_path_effects([pe.withSimplePatchShadow(offset=(2, -3), shadow_rgbFace="#B9B4AF", alpha=0.35)])
    ax_bg.add_patch(card)


def draw_hero(ax, mau):
    x, y = mau["year"], mau["maus_millions"]
    ax.fill_between(x, y, color=PIN_RED_FILL, alpha=0.6, zorder=1)
    ax.plot(x, y, color=PIN_RED, linewidth=3, marker="o", markersize=6, zorder=3)
    ax.set_ylim(0, 700)
    ax.set_xlim(2018.6, 2025.7)
    ax.set_facecolor("none")
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
    for yr, val, label, (dx, dy), ha in EVENTS:
        focal = yr == 2025
        ann = ax.annotate(
            label, xy=(yr, val), xytext=(dx, dy), textcoords="offset points",
            fontsize=9.5, fontweight="bold", ha=ha, va="center",
            color="white" if focal else INK, zorder=6,
            bbox=dict(
                boxstyle="round,pad=0.5,rounding_size=0.9",
                facecolor=PIN_RED if focal else "white",
                edgecolor=PIN_RED if focal else "#E4E1DE", linewidth=1.2,
            ),
            arrowprops=dict(
                arrowstyle="-", color="#C9C4BF", linewidth=1.1,
                connectionstyle="arc3,rad=0.15", shrinkA=4, shrinkB=6,
            ),
        )
        # Soft shadow on the chip so it lifts off the card, like a UI pill.
        ann.get_bbox_patch().set_path_effects(
            [pe.withSimplePatchShadow(offset=(1.5, -1.5), shadow_rgbFace="#B9B4AF", alpha=0.25)]
        )
        # Emphasise the anchor point with a ringed dot.
        ax.plot([yr], [val], marker="o", markersize=8, markerfacecolor=PIN_RED,
                markeredgecolor="white", markeredgewidth=1.6, zorder=7)
    ax.set_title("A decade of growth", loc="left", fontsize=12,
                 fontweight="bold", color=INK, pad=18)


def draw_revenue(ax, rev):
    """Annual revenue as vertical bars — the 'dollars' half of the growth
    story, to sit alongside the users line."""
    x = list(rev["year"])
    y = list(rev["revenue_musd"])
    colors = [PIN_RED if yr == 2025 else MUTED for yr in x]
    bars = ax.bar(x, y, width=0.62, color=colors, edgecolor="#333333", linewidth=1.0)
    ax.set_ylim(0, max(y) * 1.22)
    ax.set_facecolor("none")
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    for side in ("left", "bottom"):
        ax.spines[side].set_color(MUTED)
    ax.set_yticks([])
    ax.set_xticks(x)
    ax.tick_params(length=0, colors=SUBTLE, labelsize=10)
    for bar, v in zip(bars, y):
        ax.text(bar.get_x() + bar.get_width() / 2, v + max(y) * 0.03,
                f"${v/1000:.1f}B", ha="center", va="bottom",
                fontsize=8.5, fontweight="bold", color=INK)
    ax.set_title("Revenue grew nearly 4x, to $4.2B", loc="left",
                 fontsize=12, fontweight="bold", color=INK, pad=18)


def draw_share_gap(ax, reg):
    cats = list(reg["region"])
    users, rev = reg["maus_millions"], reg["revenue_musd"]
    u_pct = [100 * v / users.sum() for v in users]
    r_pct = [100 * v / rev.sum() for v in rev]
    color_for, gi = {}, 0
    for c in cats:
        if c == "Rest of World":
            color_for[c] = PIN_RED
        else:
            color_for[c] = GREYS[gi % len(GREYS)]; gi += 1
    ax.set_facecolor("none")
    left_u = left_r = 0
    for i, c in enumerate(cats):
        ax.barh("Users", u_pct[i], left=left_u, height=0.55, color=color_for[c],
                edgecolor="white", linewidth=1.5)
        ax.barh("Revenue", r_pct[i], left=left_r, height=0.55, color=color_for[c],
                edgecolor="white", linewidth=1.5)
        if u_pct[i] > 6:
            ax.text(left_u + u_pct[i] / 2, 0, f"{u_pct[i]:.0f}%", ha="center", va="center",
                    fontsize=9, color="white" if c == "Rest of World" else INK, fontweight="bold")
        if r_pct[i] > 6:
            ax.text(left_r + r_pct[i] / 2, 1, f"{r_pct[i]:.0f}%", ha="center", va="center",
                    fontsize=9, color="white" if c == "Rest of World" else INK, fontweight="bold")
        left_u += u_pct[i]; left_r += r_pct[i]
    ax.set_xlim(0, 100); ax.set_xticks([])
    ax.tick_params(length=0, colors=INK, labelsize=10)
    ax.invert_yaxis()
    for side in ("top", "right", "left", "bottom"):
        ax.spines[side].set_visible(False)
    ax.set_title("Rest of World is 58% of users but 7% of revenue",
                 loc="left", fontsize=12, fontweight="bold", color=INK, pad=18)


def draw_hbar(ax, cats, vals, colors, fmt, title):
    ax.set_facecolor("none")
    bars = ax.barh(cats, vals, height=0.55, color=colors,
                   edgecolor="#333333", linewidth=1.0)
    ax.set_xticks([])
    pad = max(vals) * 0.02
    for bar, v in zip(bars, vals):
        ax.text(bar.get_width() + pad, bar.get_y() + bar.get_height() / 2,
                fmt.format(v), va="center", ha="left", fontsize=10, fontweight="bold", color=INK)
    ax.tick_params(length=0, colors=INK, labelsize=10)
    for side in ("top", "right", "bottom"):
        ax.spines[side].set_visible(False)
    ax.spines["left"].set_color(MUTED)
    ax.margins(x=0.18)
    ax.set_title(title, loc="left", fontsize=12, fontweight="bold", color=INK, pad=18)


def main() -> None:
    mau = pd.read_csv(DATA / "pinterest_mau.csv").sort_values("year")
    rev_ts = pd.read_csv(DATA / "pinterest_revenue.csv").sort_values("year")
    reg = pd.read_csv(DATA / "pinterest_regions_q4_2025.csv")
    reg_rev = reg.sort_values("revenue_musd")
    reg_arpu = reg.assign(arpu=reg["revenue_musd"] / reg["maus_millions"]).sort_values("arpu")

    fig = plt.figure(figsize=(8.6, 17.2), facecolor=PAGE)

    # Full-canvas background layer that holds the pin-board cards.
    ax_bg = fig.add_axes([0, 0, 1, 1]); ax_bg.set_zorder(-10)
    ax_bg.axis("off"); ax_bg.set_xlim(0, 1); ax_bg.set_ylim(0, 1)

    gs = GridSpec(
        8, 2, figure=fig,
        height_ratios=[0.55, 1.25, 2.7, 1.7, 1.45, 1.15, 1.15, 0.3],
        hspace=1.05, wspace=0.30,
        left=0.19, right=0.85, top=0.95, bottom=0.035,
    )

    # --- Header: serif editorial headline ---
    fig.text(0.11, 0.947, "Pinterest's split screen", fontsize=27,
             fontweight="bold", family="serif", color=INK, va="center")

    # --- Deck + big numbers ---
    ax_deck = fig.add_subplot(gs[1, 0]); ax_deck.axis("off")
    ax_deck.text(
        0, 1.0,
        "By the end of 2025, Pinterest hit a\n"
        "record 619M monthly users and\n"
        "$4.2B in revenue, but where users\n"
        "live is not where the money is made.",
        fontsize=10.5, color=INK, va="top", linespacing=1.6,
    )
    ax_big = fig.add_subplot(gs[1, 1]); ax_big.axis("off")
    ax_big.text(0.05, 0.86, "619M", fontsize=24, fontweight="bold", color=PIN_RED, va="center")
    ax_big.text(0.05, 0.62, "monthly active users (+12% YoY)", fontsize=9.5, color=SUBTLE, va="center")
    ax_big.text(0.05, 0.32, "$4.2B", fontsize=24, fontweight="bold", color=INK, va="center")
    ax_big.text(0.05, 0.08, "FY2025 revenue (+16% YoY)", fontsize=9.5, color=SUBTLE, va="center")

    # --- Charts (each a full-width panel) ---
    ax_hero = fig.add_subplot(gs[2, :]); draw_hero(ax_hero, mau)
    ax_revts = fig.add_subplot(gs[3, :]); draw_revenue(ax_revts, rev_ts)
    ax_split = fig.add_subplot(gs[4, :]); draw_share_gap(ax_split, reg)
    ax_rev = fig.add_subplot(gs[5, :])
    draw_hbar(ax_rev, list(reg_rev["region"]), list(reg_rev["revenue_musd"]),
              [PIN_RED if c == "US & Canada" else MUTED for c in reg_rev["region"]],
              "${:,.0f}M", "Q4 revenue by region")
    ax_arpu = fig.add_subplot(gs[6, :])
    draw_hbar(ax_arpu, list(reg_arpu["region"]), list(reg_arpu["arpu"]),
              [PIN_RED if c == "US & Canada" else MUTED for c in reg_arpu["region"]],
              "${:,.2f}", "Implied revenue per user")
    # --- Footer ---
    ax_foot = fig.add_subplot(gs[7, :]); ax_foot.axis("off")
    ax_foot.text(0, 0.5,
                 "Source: Pinterest Q4 & Full-Year 2025 earnings report (Feb 2026).  Built with pinviz.",
                 fontsize=9, color=SUBTLE, va="center")

    # --- Pin-board cards behind each panel (drawn after layout is known) ---
    fig.canvas.draw()
    add_card(ax_bg, [ax_deck, ax_big], pad_y=0.02, extra_top=0.015, pad_bottom=0.04)
    add_card(ax_bg, [ax_hero], extra_top=0.045)
    add_card(ax_bg, [ax_revts], extra_top=0.045)
    add_card(ax_bg, [ax_split], extra_top=0.045)
    add_card(ax_bg, [ax_rev], extra_top=0.045)
    add_card(ax_bg, [ax_arpu], extra_top=0.045)

    fig.savefig(OUT / "pinviz_poster.pdf", bbox_inches="tight", facecolor=fig.get_facecolor())
    fig.savefig(OUT / "pinviz_poster.png", dpi=150, bbox_inches="tight", facecolor=fig.get_facecolor())
    plt.close(fig)
    print("wrote examples/pinviz_poster.pdf")
    print("wrote examples/pinviz_poster.png")


if __name__ == "__main__":
    main()
