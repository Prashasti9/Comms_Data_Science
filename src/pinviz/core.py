"""Chart functions for :mod:`pinviz`.

Each function maps to one family in the *Quantitative Chart Chooser* and
returns a :class:`matplotlib.figure.Figure`, so callers can ``savefig`` it in
any format. Every function shares the theme in :mod:`pinviz.theme`, so the
whole library reads as one designed system.

Chart Chooser mapping
---------------------
=====================  =======================  ===========================
Function               Chart Chooser family     "So what?" it answers
=====================  =======================  ===========================
``big_number``         Single important number  How big is the headline?
``growth_line``        Change over time         Which way is the trend going?
``revenue_bar``        Comparison               Who contributes the most?
``share_gap``          Parts of a whole         Users vs. revenue mismatch
``arpu_bar``           Comparison / ratio       How well is each region paid?
=====================  =======================  ===========================
"""

from __future__ import annotations

import matplotlib.pyplot as plt

from pinviz.theme import (
    GRID,
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
    """A single big-number callout — the Chart Chooser's "one important number".

    Aesthetic choices: no axes, no gridlines, nothing to read but the number.
    When a single figure *is* the story, a chart would only bury it, so the
    value is set huge in the highlight colour with a quiet grey caption
    beneath it.
    """
    fig, ax = plt.subplots(figsize=(6, 3.5))
    ax.axis("off")
    ax.text(0.5, 0.60, f"{value}{unit}", ha="center", va="center",
            fontsize=64, fontweight="bold", color=color)
    ax.text(0.5, 0.24, label, ha="center", va="center",
            fontsize=15, color=INK)
    if footnote:
        ax.text(0.5, 0.07, footnote, ha="center", va="center",
                fontsize=11, color=SUBTLE)
    return fig


def growth_line(df, x, y, title, subtitle="", annotate=None, value_fmt="{:.0f}M"):
    """A line chart for change over time, with the last point labelled directly.

    Aesthetic choices: a zero-based y-axis (so the growth isn't visually
    exaggerated), a direct end-of-line label instead of forcing the reader to
    a y-axis, and an optional annotation to explain an anomaly in plain
    language rather than leaving the dip unexplained.

    ``annotate`` is an optional ``(x_value, "note text")`` pair.
    """
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
        ax.annotate(
            note, xy=(row[x], row[y]), xytext=(0, -46),
            textcoords="offset points", ha="center", fontsize=9, color=SUBTLE,
            arrowprops=dict(arrowstyle="->", color=MUTED),
        )

    ax.set_xticks(list(data[x]))
    ax.margins(x=0.08)
    titles(ax, title, subtitle)
    return fig


def revenue_bar(df, category, value, title, subtitle="", spotlight=None,
                value_fmt="${:,.0f}M"):
    """A horizontal bar chart for comparison, with one bar spotlighted.

    Aesthetic choices: horizontal bars so long category labels stay
    left-to-right readable; bars sorted by size so rank is obvious; and a
    single spotlighted bar in the highlight colour while the rest are muted
    grey, so the eye lands on the point being made. Values are labelled at the
    end of each bar, removing the need for a busy x-axis.
    """
    data = df.sort_values(value, ascending=True)
    cats = list(data[category])
    vals = list(data[value])
    colors = [PIN_RED if c == spotlight else MUTED for c in cats]

    fig, ax = new_axes(figsize=(8, 4.2))
    for side in ("top", "right", "bottom"):
        ax.spines[side].set_visible(False)
    ax.spines["left"].set_color(MUTED)
    ax.tick_params(length=0, colors=SUBTLE)

    bars = ax.barh(cats, vals, color=colors, zorder=3)
    ax.set_xticks([])
    pad = max(vals) * 0.01
    for bar, v in zip(bars, vals):
        ax.text(bar.get_width() + pad, bar.get_y() + bar.get_height() / 2,
                value_fmt.format(v), va="center", ha="left",
                fontsize=11, fontweight="bold",
                color=INK if bar.get_facecolor()[:3] != (1.0, 0.0, 0.0) else PIN_RED)
    ax.margins(x=0.12)
    titles(ax, title, subtitle)
    return fig


def share_gap(df, category, part_a, part_b, title, subtitle="",
              label_a="Share A", label_b="Share B", highlight=None):
    """Paired 100%-normalised bars comparing two parts-of-a-whole splits.

    This is the library's signature chart. Two stacked bars — one for each
    metric — are each normalised to 100%, so the reader compares *composition*
    directly and sees the mismatch (e.g. a region that is a big share of users
    but a tiny share of revenue).

    Aesthetic choices: the highlighted segment uses the brand colour across
    both bars so the eye tracks the same region between them; the other
    segments use graded greys; each segment is labelled with its percentage
    in-place, so no legend hunting is required.
    """
    cats = list(df[category])
    a = list(df[part_a])
    b = list(df[part_b])
    a_pct = [100 * v / sum(a) for v in a]
    b_pct = [100 * v / sum(b) for v in b]

    greys = ["#8A8A8A", "#BDBDBD", "#DADADA", "#EAEAEA"]
    color_for = {}
    gi = 0
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

    bar_labels = [label_a, label_b]
    left_a = left_b = 0
    for i, c in enumerate(cats):
        ax.barh(bar_labels[0], a_pct[i], left=left_a, color=color_for[c], zorder=3)
        ax.barh(bar_labels[1], b_pct[i], left=left_b, color=color_for[c], zorder=3)
        # in-place percentage labels (only when the segment is wide enough)
        if a_pct[i] > 6:
            ax.text(left_a + a_pct[i] / 2, 0, f"{a_pct[i]:.0f}%",
                    ha="center", va="center", fontsize=10,
                    color="white" if c == highlight else INK, fontweight="bold")
        if b_pct[i] > 6:
            ax.text(left_b + b_pct[i] / 2, 1, f"{b_pct[i]:.0f}%",
                    ha="center", va="center", fontsize=10,
                    color="white" if c == highlight else INK, fontweight="bold")
        left_a += a_pct[i]
        left_b += b_pct[i]

    ax.set_xlim(0, 100)
    ax.set_xticks([])
    ax.invert_yaxis()
    titles(ax, title, subtitle)
    return fig


def arpu_bar(df, category, revenue, users, title, subtitle="",
             spotlight=None):
    """Comparison bars of an implied ratio: revenue per user by category.

    Computes revenue-per-user = revenue / users directly from the source
    columns (so the ratio is never hand-entered) and draws it as a spotlighted
    bar chart. Aesthetic choices mirror :func:`revenue_bar`: sorted bars, one
    highlight colour, end-of-bar value labels, dollar formatting.
    """
    data = df.copy()
    data["_arpu"] = data[revenue] / data[users]
    data = data.sort_values("_arpu", ascending=True)
    cats = list(data[category])
    vals = list(data["_arpu"])
    colors = [PIN_RED if c == spotlight else MUTED for c in cats]

    fig, ax = new_axes(figsize=(8, 4.2))
    for side in ("top", "right", "bottom"):
        ax.spines[side].set_visible(False)
    ax.spines["left"].set_color(MUTED)
    ax.tick_params(length=0, colors=SUBTLE)

    bars = ax.barh(cats, vals, color=colors, zorder=3)
    ax.set_xticks([])
    pad = max(vals) * 0.01
    for bar, v in zip(bars, vals):
        ax.text(bar.get_width() + pad, bar.get_y() + bar.get_height() / 2,
                f"${v:,.2f}", va="center", ha="left",
                fontsize=11, fontweight="bold", color=INK)
    ax.margins(x=0.14)
    titles(ax, title, subtitle)
    return fig
