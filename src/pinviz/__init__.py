"""pinviz: opinionated, communication-first charts for the Pinterest story.

A small visualization library where every function makes deliberate design
choices from the Evergreen Data Visualization Checklist and maps to a family
in the Quantitative Chart Chooser. Each returns a matplotlib ``Figure``.

Example
-------
>>> import pandas as pd, pinviz
>>> mau = pd.read_csv("data/pinterest_mau.csv")
>>> fig = pinviz.growth_line(mau, "year", "maus_millions",
...     title="Pinterest reached a record 619M users in 2025")
"""

from pinviz.core import arpu_bar, big_number, growth_line, revenue_bar, share_gap

__version__ = "0.1.0"

__all__ = [
    "big_number",
    "growth_line",
    "revenue_bar",
    "share_gap",
    "arpu_bar",
    "__version__",
]
