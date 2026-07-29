"""Shared visual theme for :mod:`pinviz`.

The whole point of this library is that every chart makes the *same*
deliberate design decisions, so the palette, fonts, and "clean up the frame"
helper live here and are reused by every function in :mod:`pinviz.core`.

Design decisions (from the Evergreen Data Visualization Checklist):

* **One highlight colour, everything else muted.** Colour is used to direct
  attention, not to decorate. ``PIN_RED`` marks the thing the reader should
  look at; ``MUTED``/``GRID`` recede into the background.
* **No chartjunk.** Top and right spines are removed, tick marks are dropped,
  and gridlines are a single very-light grey so they guide the eye without
  competing with the data.
* **Text does the work.** Titles state the takeaway ("the so-what"), not just
  the variable name, and a lighter subtitle carries the context.
"""

import matplotlib.pyplot as plt

# Render dollar signs and other symbols literally. Matplotlib treats a pair
# of ``$`` as LaTeX math mode, which would mangle titles like "$9 ... $0.27";
# disabling math parsing keeps currency labels readable.
plt.rcParams["text.parse_math"] = False

# Pinterest brand red — the single highlight colour used across the library.
PIN_RED = "#E60023"
# Neutral greys for context marks, de-emphasised bars, and gridlines.
MUTED = "#BDBDBD"
INK = "#2B2B2B"
SUBTLE = "#666666"
GRID = "#ECECEC"


def apply_base_style(ax):
    """Strip chartjunk from ``ax`` so the data stands on its own.

    Removes the top and right spines, softens the remaining spines, drops
    tick marks (keeping the labels), and lightens the horizontal gridlines.
    """
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    for side in ("left", "bottom"):
        ax.spines[side].set_color(MUTED)
    ax.tick_params(length=0, colors=SUBTLE)
    ax.grid(axis="y", color=GRID, linewidth=1, zorder=0)
    ax.set_axisbelow(True)
    return ax


def titles(ax, title, subtitle=""):
    """Add a bold takeaway ``title`` and a lighter ``subtitle`` above ``ax``.

    Titles are left-aligned to the plot area (not centred) so they read like
    a sentence the viewer starts from, following the checklist's guidance to
    lead with the message rather than the variable name.
    """
    ax.text(
        0, 1.14, title, transform=ax.transAxes,
        fontsize=15, fontweight="bold", color=INK, ha="left", va="bottom",
    )
    if subtitle:
        ax.text(
            0, 1.045, subtitle, transform=ax.transAxes,
            fontsize=10, color=SUBTLE, ha="left", va="bottom",
        )
    return ax


def new_axes(figsize=(8, 4.5)):
    """Create a figure/axes pair with room reserved above for the titles."""
    fig, ax = plt.subplots(figsize=figsize)
    fig.subplots_adjust(top=0.80)
    return fig, ax
