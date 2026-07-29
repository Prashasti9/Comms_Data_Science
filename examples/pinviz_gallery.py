"""Generate the full pinviz chart gallery from the verified Pinterest data.

Writes one PNG per chart into ``examples/`` and a combined ``pinviz_gallery.pdf``.

Usage
-----
    python examples/pinviz_gallery.py
"""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")  # headless: render straight to files, no display

import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.backends.backend_pdf import PdfPages

import pinviz

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
OUT = ROOT / "examples"


def main() -> None:
    mau = pd.read_csv(DATA / "pinterest_mau.csv")
    reg = pd.read_csv(DATA / "pinterest_regions_q4_2025.csv")

    figs = {}

    # 1. Big number — the headline figure.
    figs["01_big_number"] = pinviz.big_number(
        619, "M", "monthly active users in 2025",
        footnote="a record high, up 12% year over year",
    )

    # 2. Growth line — change over time, with the 2021 dip explained.
    figs["02_growth_line"] = pinviz.growth_line(
        mau, "year", "maus_millions",
        title="Pinterest's audience hit a record 619M in 2025",
        subtitle="Global monthly active users, Q4 of each year (millions)",
        annotate=(2021, "users fell as pandemic\nlockdowns eased"),
    )

    # 3. Revenue bar — who brings in the money (spotlight US & Canada).
    figs["03_revenue_bar"] = pinviz.revenue_bar(
        reg, "region", "revenue_musd",
        title="US & Canada earns $979M — 74% of Q4 revenue",
        subtitle="Q4 2025 revenue by region",
        spotlight="US & Canada",
    )

    # 4. Share gap — the signature chart: users vs revenue mismatch.
    figs["04_share_gap"] = pinviz.share_gap(
        reg, "region", "maus_millions", "revenue_musd",
        title="Rest of World is 58% of users but just 7% of revenue",
        subtitle="Share of Q4 2025 monthly active users vs. share of revenue",
        label_a="Users", label_b="Revenue",
        highlight="Rest of World",
    )

    # 5. ARPU bar — implied revenue per user, spotlight the gap.
    figs["05_arpu_bar"] = pinviz.arpu_bar(
        reg, "region", "revenue_musd", "maus_millions",
        title="Each US & Canada user is worth ~$9; Rest of World ~$0.27",
        subtitle="Implied Q4 2025 revenue per monthly active user",
        spotlight="US & Canada",
    )

    # Save individual PNGs.
    for name, fig in figs.items():
        path = OUT / f"pinviz_{name}.png"
        fig.savefig(path, dpi=150, bbox_inches="tight")
        print(f"wrote {path.relative_to(ROOT)}")

    # Save a combined multi-page PDF.
    pdf_path = OUT / "pinviz_gallery.pdf"
    with PdfPages(pdf_path) as pdf:
        for fig in figs.values():
            pdf.savefig(fig, bbox_inches="tight")
    print(f"wrote {pdf_path.relative_to(ROOT)}")

    for fig in figs.values():
        plt.close(fig)


if __name__ == "__main__":
    main()
