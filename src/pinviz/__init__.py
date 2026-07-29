"""pinviz: communication-first charts for the Pinterest 2025 data story.

Every function follows the Evergreen Data Visualization Checklist, maps to a
Quantitative Chart Chooser family, and returns a matplotlib ``Figure``.
"""

from pinviz.core import arpu_bar, big_number, growth_line, revenue_bar, share_gap

__version__ = "0.1.0"
__all__ = ["big_number", "growth_line", "revenue_bar", "share_gap", "arpu_bar", "__version__"]
