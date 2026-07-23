"""simple_viz: a small, friendly wrapper around matplotlib for quick plots.

Example
-------
>>> import simple_viz as sv
>>> sv.line_plot([1, 2, 3], [4, 5, 6], title="Demo")
"""

from simple_viz.core import bar_plot, histogram, line_plot, scatter_plot

__version__ = "0.1.0"

__all__ = [
    "line_plot",
    "bar_plot",
    "scatter_plot",
    "histogram",
    "__version__",
]
