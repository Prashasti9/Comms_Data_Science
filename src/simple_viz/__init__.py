"""simple_viz: communication-first charts for the Pinterest 2025 data story.

Every function is the right chart for one specific question, makes deliberate
design choices, and returns a matplotlib ``Figure``.
"""

from simple_viz.core import revenue_per_user, big_number, growth_line, revenue_bar, share_gap

__version__ = "0.1.0"
__all__ = ["big_number", "growth_line", "revenue_bar", "share_gap", "revenue_per_user", "__version__"]
