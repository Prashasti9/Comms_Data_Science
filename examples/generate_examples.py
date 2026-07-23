"""Generate example plots for each public simple_viz function.

Running this script writes one PDF per plot into the same directory as the
script (``examples/``):

    line.pdf, bar.pdf, scatter.pdf, histogram.pdf

and a combined ``all_plots.pdf`` with all four on a single 2x2 grid.

Usage
-----
    python examples/generate_examples.py
"""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")  # headless backend, writes files without a display

import matplotlib.pyplot as plt
import pandas as pd

import simple_viz as sv

OUT_DIR = Path(__file__).resolve().parent


def sample_data() -> pd.DataFrame:
    """A small, deterministic sample DataFrame for the examples."""
    return pd.DataFrame(
        {
            "month": ["Jan", "Feb", "Mar", "Apr", "May", "Jun"],
            "revenue": [10, 14, 9, 17, 12, 21],
            "spend": [4, 6, 5, 8, 7, 9],
        }
    )


def sample_scores() -> pd.Series:
    """A standalone series of scores for the histogram example."""
    return pd.Series([72, 85, 63, 91, 78, 88, 69, 95, 81, 74], name="score")


def save(ax, name: str) -> Path:
    """Save the figure that owns ``ax`` to ``examples/<name>.pdf``."""
    path = OUT_DIR / f"{name}.pdf"
    ax.figure.savefig(path, format="pdf", bbox_inches="tight")
    plt.close(ax.figure)
    return path


def main() -> None:
    df = sample_data()
    scores = sample_scores()
    written = []

    # Line plot: revenue over the months.
    ax = sv.line_plot(
        range(len(df)), df["revenue"],
        title="Monthly Revenue", xlabel="Month index", ylabel="Revenue ($k)",
        marker="o",
    )
    written.append(save(ax, "line"))

    # Bar chart: revenue by month.
    ax = sv.bar_plot(
        df["month"], df["revenue"],
        title="Revenue by Month", xlabel="Month", ylabel="Revenue ($k)",
        color="steelblue",
    )
    written.append(save(ax, "bar"))

    # Scatter plot: spend vs revenue.
    ax = sv.scatter_plot(
        df["spend"], df["revenue"],
        title="Spend vs Revenue", xlabel="Spend ($k)", ylabel="Revenue ($k)",
        color="darkorange",
    )
    written.append(save(ax, "scatter"))

    # Histogram: distribution of scores.
    ax = sv.histogram(
        scores, bins=5,
        title="Score Distribution", xlabel="Score",
        color="mediumseagreen", edgecolor="white",
    )
    written.append(save(ax, "histogram"))

    # Combined 2x2 grid using the shared `ax` argument.
    fig, axes = plt.subplots(2, 2, figsize=(11, 8))
    sv.line_plot(range(len(df)), df["revenue"], title="Line", ax=axes[0, 0], marker="o")
    sv.bar_plot(df["month"], df["revenue"], title="Bar", ax=axes[0, 1], color="steelblue")
    sv.scatter_plot(df["spend"], df["revenue"], title="Scatter", ax=axes[1, 0], color="darkorange")
    sv.histogram(scores, bins=5, title="Histogram", ax=axes[1, 1], color="mediumseagreen", edgecolor="white")
    fig.suptitle("simple_viz — all plot types", fontsize=14)
    fig.tight_layout()
    combined = OUT_DIR / "all_plots.pdf"
    fig.savefig(combined, format="pdf", bbox_inches="tight")
    plt.close(fig)
    written.append(combined)

    for path in written:
        print(f"wrote {path.relative_to(OUT_DIR.parent)}")


if __name__ == "__main__":
    main()
