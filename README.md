# simple_viz

**Opinionated, communication-first charts that tell one data story.**

`simple_viz` is a small Python visualization library built for a communication
course. Every function is the right chart for one specific question and makes
deliberate design decisions, so the whole set reads as one system. The running
example is **Pinterest's 2025 results** — a company with a huge global audience
but very unevenly distributed revenue.

Each function returns a matplotlib `Figure`, so you can `savefig` it in any
format (PNG, PDF, SVG).

## Why it looks the way it does

The design is the point, not an afterthought:

- **One highlight colour.** Pinterest red (`#E60023`) marks the one thing the
  reader should look at; everything else is muted grey. Colour directs
  attention instead of decorating.
- **Titles state the takeaway.** "Rest of World is 58% of users but just 7% of
  revenue" — not "Users and revenue by region." The chart answers *so what?*
  before you read the axes.
- **Honest axes.** Bars and lines start at zero; percentages are normalised to
  100% so composition is compared fairly.
- **No chartjunk.** Top/right spines removed, tick marks dropped, gridlines a
  single very light grey, values labelled directly on the marks so legends and
  busy axes disappear.

## Install

From PyPI:

```bash
pip install simple-viz-prashasti
```

Or from source (editable), run from the project root:

```bash
python -m pip install -e .
```

Either way, you then `import simple_viz`. Dependencies: `matplotlib`, `pandas`.

## Use

```python
import pandas as pd
import simple_viz

mau = pd.read_csv("data/pinterest_mau.csv")
fig = simple_viz.growth_line(
    mau, "year", "maus_millions",
    title="Pinterest's audience hit a record 619M in 2025",
    subtitle="Global monthly active users, Q4 of each year (millions)",
    annotate=(2021, "users fell as pandemic\nlockdowns eased"),
)
fig.savefig("mau.png", dpi=150, bbox_inches="tight")
```

Generate the whole gallery (5 charts + a combined PDF) at once:

```bash
python examples/simple_viz_gallery.py
```

## The library

| Function | Chart type | Answers |
| --- | --- | --- |
| `big_number(value, unit, label, ...)` | Single important number | How big is the headline? |
| `growth_line(df, x, y, ...)` | Change over time | Which way is the trend going? |
| `revenue_bar(df, category, value, ...)` | Comparison | Who contributes the most? |
| `share_gap(df, category, part_a, part_b, ...)` | Parts of a whole | Where do users and revenue diverge? |
| `revenue_per_user(df, category, revenue, users, ...)` | Comparison / ratio | How well is each region monetised? |

## Data

All figures are **real**, from Pinterest's Q4 & Full-Year 2025 earnings report
(released February 12, 2026). See [`data/SOURCES.md`](data/SOURCES.md) for the
exact numbers and citations.

## Tests

```bash
python -m pip install -e ".[dev]"
python -m pytest
```

## License

[MIT](LICENSE)
