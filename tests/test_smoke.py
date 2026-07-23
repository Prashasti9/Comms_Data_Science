"""Smoke tests for the simple_viz package.

Builds a small pandas DataFrame and confirms each public plotting function
runs without error and returns a matplotlib Axes.
"""

import matplotlib

matplotlib.use("Agg")  # headless backend, no display needed

import pandas as pd
import pytest
from matplotlib.axes import Axes

import simple_viz as sv


@pytest.fixture
def df():
    """A small sample DataFrame used across the smoke tests."""
    return pd.DataFrame(
        {
            "x": [1, 2, 3, 4, 5],
            "y": [10, 14, 9, 17, 12],
            "category": ["a", "b", "c", "d", "e"],
            "values": [3, 7, 2, 5, 8],
        }
    )


def test_public_api():
    """__all__ exposes the expected names and a version string."""
    assert sv.__all__ == [
        "line_plot",
        "bar_plot",
        "scatter_plot",
        "histogram",
        "__version__",
    ]
    assert isinstance(sv.__version__, str)


def test_line_plot_returns_axes(df):
    ax = sv.line_plot(df["x"], df["y"], title="Line")
    assert isinstance(ax, Axes)


def test_bar_plot_returns_axes(df):
    ax = sv.bar_plot(df["category"], df["values"], title="Bar")
    assert isinstance(ax, Axes)


def test_scatter_plot_returns_axes(df):
    ax = sv.scatter_plot(df["x"], df["y"], title="Scatter")
    assert isinstance(ax, Axes)


def test_histogram_returns_axes(df):
    ax = sv.histogram(df["y"], bins=4, title="Histogram")
    assert isinstance(ax, Axes)


def test_mismatched_lengths_raise():
    """Helpers validate that paired sequences have equal length."""
    with pytest.raises(ValueError):
        sv.line_plot([1, 2], [1])
