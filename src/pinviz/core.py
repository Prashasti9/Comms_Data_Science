"""Chart functions for :mod:`pinviz`.

Each function maps to one family in the *Quantitative Chart Chooser* and
returns a :class:`matplotlib.figure.Figure`. They all share the theme in
:mod:`pinviz.theme`, so the library reads as one designed system.

    Function       Chart Chooser family     "So what?" it answers
    -----------    ----------------------   ---------------------------
    big_number     Single important number  How big is the headline?
    growth_line    Change over time         Which way is the trend going?
    revenue_bar    Comparison               Who contributes the most?
    share_gap      Parts of a whole         Users vs. revenue mismatch
    arpu_bar       Comparison / ratio       How well is each region paid?
"""

from __future__ import annotations

import matplotlib.pyplot as plt

from pinviz.theme import (
    INK,
    MUTED,
    PIN_RED,
    SUBTLE,
    apply_base_style,
    new_axes,
    titles,
)

__all__ = ["big_number", "growth_line", "revenue_bar", "share_gap", "arpu_bar"]


def big_number(value, unit, label, footnote="", color=PIN_RED):
    """One big-number callout. Aesthetic: no axes or gridlines — when a single
    figure *is* the story, the number is set huge in the highlight colour with
    a quiet grey caption, so nothing competes with it."""
    fig, ax = plt.subplots(figsize=(6, 3.5))
    ax.axis("off")
    ax.text(0.5, 0.60, f"{value}{unit}", ha="center", va="center",
            fontsize=64, fontweight="bold", color=color)
    ax.text(0.5, 0.24, label, ha="center", va="center", fontsize=15, color=INK)
    if footnote:
        ax.text(0.5, 0.07, footnote, ha="center", va="center",
                fontsize=11, color=SUBTLE)
    return fig


def growth_line(df, x, y, title, subtitle="", annotate=None, value_fmt="{:.0f}M"):
    """Line chart for change over time. Aesthetic: zero-based y-axis (growth
    isn't exaggerated), the last point labelled directly (no y-axis hunting),
    and an optional ``(x_value, "note")`` annotation to explain an anomaly."""
    data = df.sort_values(x)
    fig, ax = new_axes()
    apply_base_style(ax)

    ax.plot(data[x], data[y], color=PIN_RED, linewidth=2.5,
            marker="o", markersize=5, zorder=3)
    ax.set_ylim(bottom=0)

    # Label the final point directly, next to the line.
    xl, yl = data[x].iloc[-1], data[y].iloc[-1]
    ax.text(xl, yl, "  " + value_fmt.format(yl), va="center", ha="left",
            fontsize=11, fontweight="bold", color=PIN_RED)

    if annotate is not None:
        ax_x, note = annotate
        row = data[data[x] == ax_x].iloc[0]
        ax.annotate(note, xy=(row[x], row[y]), xytext=(0, -46),
                    textcoords="offset points", ha="center", fontsize=9,
                    color=SUBTLE, arrowprops=dict(arrowstyle="->", color=MUTED))

    ax.set_xticks(list(data[x]))
    ax.margins(x=0.08)
    titles(ax, title, subtitle)
    return fig


def _spotlight_barh(cats, vals, spotlight, value_fmt, title, subtitle, figsize):
    """Shared horizontal-bar drawing for revenue_bar and arpu_bar. Aesthetic:
    bars sorted by size, one spotlighted bar in the highlight colour while the
    rest are grey, and end-of-bar value labels so no x-axis is needed."""
    colors = [PIN_RED if c == spotlight else MUTED for c in cats]
    fig, ax = new_axes(figsize=figsize)
    for side in ("top", "right", "bottom"):
        ax.spines[side].set_visible(False)
    ax.spines["left"].set_color(MUTED)
    ax.tick_params(length=0, colors=SUBTLE)

    ax.barh(cats, vals, color=colors, zorder=3)
    ax.set_xticks([])
    pad = max(vals) * 0.01
    for c, v in zip(cats, vals):
        ax.text(v + pad, c, value_fmt.format(v), va="center", ha="left",
                fontsize=11, fontweight="bold",
                color=PIN_RED if c == spotlight else INK)
    ax.margins(x=0.14)
    titles(ax, title, subtitle)
    return fig


def revenue_bar(df, category, value, title, subtitle="", spotlight=None,
                value_fmt="${:,.0f}M"):
    """Horizontal bar chart for comparison, with one bar spotlighted."""
    data = df.sort_values(value, ascending=True)
    return _spotlight_barh(list(data[category]), list(data[value]), spotlight,
                           value_fmt, title, subtitle, figsize=(8, 4.2))


def arpu_bar(df, category, revenue, users, title, subtitle="", spotlight=None):
    """Comparison bars of an implied ratio: revenue per user by category.
    The ratio is computed here (revenue / users), never hand-entered."""
    data = df.copy()
    data["_arpu"] = data[revenue] / data[users]
    data = data.sort_values("_arpu", ascending=True)
    return _spotlight_barh(list(data[category]), list(data["_arpu"]), spotlight,
                           "${:,.2f}", title, subtitle, figsize=(8, 4.2))


def share_gap(df, category, part_a, part_b, title, subtitle="",
              label_a="Share A", label_b="Share B", highlight=None):
    """Paired 100%-normalised bars comparing two parts-of-a-whole splits — the
    library's signature chart. Aesthetic: each bar is normalised to 100% so
    the reader compares composition directly; the highlighted region uses the
    brand colour across both bars so the eye tracks it; percentages are
    labelled in-place, so there's no legend to hunt through."""
    cats = list(df[category])
    a_pct = [100 * v / df[part_a].sum() for v in df[part_a]]
    b_pct = [100 * v / df[part_b].sum() for v in df[part_b]]

    greys = ["#8A8A8A", "#BDBDBD", "#DADADA", "#EAEAEA"]
    color_for, gi = {}, 0
    for c in cats:
        if c == highlight:
            color_for[c] = PIN_RED
        else:
            color_for[c] = greys[gi % len(greys)]
            gi += 1

    fig, ax = new_axes(figsize=(8, 4.6))
    for side in ("top", "right", "left", "bottom"):
        ax.spines[side].set_visible(False)
    ax.tick_params(length=0, colors=SUBTLE)

    left_a = left_b = 0
    for c, ap, bp in zip(cats, a_pct, b_pct):
        ax.barh(label_a, ap, left=left_a, color=color_for[c], zorder=3)
        ax.barh(label_b, bp, left=left_b, color=color_for[c], zorder=3)
        text_color = "white" if c == highlight else INK
        if ap > 6:
            ax.text(left_a + ap / 2, 0, f"{ap:.0f}%", ha="center", va="center",
                    fontsize=10, color=text_color, fontweight="bold")
        if bp > 6:
            ax.text(left_b + bp / 2, 1, f"{bp:.0f}%", ha="center", va="center",
                    fontsize=10, color=text_color, fontweight="bold")
        left_a += ap
        left_b += bp

    ax.set_xlim(0, 100)
    ax.set_xticks([])
    ax.invert_yaxis()
    titles(ax, title, subtitle)
    return fig
