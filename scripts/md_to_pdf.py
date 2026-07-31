"""Render a Markdown file to a clean, paginated PDF using matplotlib only.

Usage:
    python scripts/md_to_pdf.py CUE_CARD.md CUE_CARD.pdf
    python scripts/md_to_pdf.py HANDOFF.md HANDOFF.pdf

No external dependencies beyond matplotlib. It is not a full Markdown engine:
it lays out the source as readable text (headings larger/bold, code blocks and
tables in monospace, bullets preserved) and paginates onto US-Letter pages.
"""

import sys
import textwrap

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

plt.rcParams["text.parse_math"] = False

INK = "#2B2B2B"
RED = "#E60023"
SUBTLE = "#666666"

# US Letter, generous margins.
PAGE_W, PAGE_H = 8.5, 11.0
TOP, BOTTOM, LEFT = 0.94, 0.06, 0.09
LINE = 0.019          # vertical step per line (figure fraction)
WRAP_PROSE = 92       # wrap width for normal prose
WRAP_MONO = 96        # wrap width inside code/table blocks


def _emit(lines):
    """Turn raw markdown lines into (text, size, weight, color, mono) tuples."""
    out = []
    in_code = False
    for raw in lines:
        line = raw.rstrip("\n")

        if line.strip().startswith("```"):
            in_code = not in_code
            out.append((None, 0, "normal", INK, False))  # spacer
            continue

        if in_code:
            for seg in textwrap.wrap(line, WRAP_MONO) or [""]:
                out.append(("    " + seg, 8.5, "normal", SUBTLE, True))
            continue

        stripped = line.strip()
        if not stripped:
            out.append((None, 0, "normal", INK, False))
            continue

        # Tables (keep monospace, strip nothing).
        if stripped.startswith("|"):
            for seg in textwrap.wrap(line, WRAP_MONO) or [""]:
                out.append((seg, 8.0, "normal", INK, True))
            continue

        # Headings.
        if stripped.startswith("#"):
            level = len(stripped) - len(stripped.lstrip("#"))
            text = stripped[level:].strip()
            size = {1: 17, 2: 14, 3: 12}.get(level, 11)
            color = RED if level == 1 else INK
            out.append((None, 0, "normal", INK, False))
            out.append((text, size, "bold", color, False))
            continue

        # Horizontal rule.
        if stripped in ("---", "***", "___"):
            out.append(("─" * 60, 8, "normal", "#CCCCCC", True))
            continue

        # Bullets / numbered list — preserve leading indent + marker.
        indent = len(line) - len(line.lstrip(" "))
        prefix = " " * indent
        wrapped = textwrap.wrap(stripped, WRAP_PROSE) or [""]
        # de-emphasise markdown bold/inline markers lightly for readability
        for i, seg in enumerate(wrapped):
            lead = prefix if i == 0 else prefix + "  "
            out.append((lead + seg, 10.5, "normal", INK, False))
    return out


def render(md_path, pdf_path):
    with open(md_path, encoding="utf-8") as fh:
        items = _emit(fh.readlines())

    with PdfPages(pdf_path) as pdf:
        fig = plt.figure(figsize=(PAGE_W, PAGE_H))
        y = TOP
        for text, size, weight, color, mono in items:
            if text is None:
                y -= LINE * 0.6
            else:
                if y < BOTTOM:
                    pdf.savefig(fig)
                    plt.close(fig)
                    fig = plt.figure(figsize=(PAGE_W, PAGE_H))
                    y = TOP
                fig.text(
                    LEFT, y, text,
                    fontsize=size, fontweight=weight, color=color,
                    family="monospace" if mono else "sans-serif",
                    va="top", ha="left",
                )
                y -= LINE * (1.0 + max(0, size - 10.5) * 0.06)
        pdf.savefig(fig)
        plt.close(fig)
    print(f"wrote {pdf_path}")


if __name__ == "__main__":
    render(sys.argv[1], sys.argv[2])
