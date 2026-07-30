"""Shared visual theme for simple_viz: one highlight colour, no chartjunk, and
takeaway titles — the design choices every chart in :mod:`simple_viz.core`
reuses so the library reads as one designed system."""

import matplotlib.pyplot as plt

# A pair of "$" is LaTeX math mode in matplotlib; disable it so currency
# labels like "$9" / "$0.27" render literally.
plt.rcParams["text.parse_math"] = False

PIN_RED = "#E60023"   # the single highlight colour
MUTED = "#BDBDBD"     # de-emphasised bars and spines
INK = "#2B2B2B"       # primary text
SUBTLE = "#666666"    # captions
GRID = "#ECECEC"      # gridlines


def apply_base_style(ax):
    """Strip chartjunk: drop top/right spines, soften the rest, light y-grid."""
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    for side in ("left", "bottom"):
        ax.spines[side].set_color(MUTED)
    ax.tick_params(length=0, colors=SUBTLE)
    ax.grid(axis="y", color=GRID, linewidth=1, zorder=0)
    ax.set_axisbelow(True)
    return ax


def titles(ax, title, subtitle=""):
    """Left-aligned bold takeaway title, with an optional lighter subtitle."""
    ax.text(0, 1.14, title, transform=ax.transAxes, fontsize=15,
            fontweight="bold", color=INK, ha="left", va="bottom")
    if subtitle:
        ax.text(0, 1.045, subtitle, transform=ax.transAxes, fontsize=10,
                color=SUBTLE, ha="left", va="bottom")
    return ax


def new_axes(figsize=(8, 4.5)):
    """Figure/axes pair with headroom reserved above for the titles."""
    fig, ax = plt.subplots(figsize=figsize)
    fig.subplots_adjust(top=0.80)
    return fig, ax
