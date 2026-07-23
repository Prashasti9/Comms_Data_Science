"""Core plotting helpers for :mod:`simple_viz`.

Each function is a thin convenience wrapper around matplotlib. They share a
common set of keyword arguments (``title``, ``xlabel``, ``ylabel``, ``ax``)
and always return the :class:`matplotlib.axes.Axes` used for the plot so the
result can be customised further by the caller.
"""

from __future__ import annotations

from typing import Optional, Sequence

import matplotlib.pyplot as plt
from matplotlib.axes import Axes

__all__ = ["line_plot", "bar_plot", "scatter_plot", "histogram"]


def _get_ax(ax: Optional[Axes]) -> Axes:
    """Return ``ax`` if provided, otherwise create a new Axes."""
    if ax is None:
        _, ax = plt.subplots()
    return ax


def _apply_labels(
    ax: Axes,
    title: Optional[str],
    xlabel: Optional[str],
    ylabel: Optional[str],
) -> None:
    """Apply optional title and axis labels to ``ax``."""
    if title:
        ax.set_title(title)
    if xlabel:
        ax.set_xlabel(xlabel)
    if ylabel:
        ax.set_ylabel(ylabel)


def line_plot(
    x: Sequence[float],
    y: Sequence[float],
    *,
    title: Optional[str] = None,
    xlabel: Optional[str] = None,
    ylabel: Optional[str] = None,
    ax: Optional[Axes] = None,
    **kwargs,
) -> Axes:
    """Draw a line plot of ``y`` against ``x``.

    Extra keyword arguments are forwarded to
    :meth:`matplotlib.axes.Axes.plot`.
    """
    if len(x) != len(y):
        raise ValueError(f"x and y must have equal length ({len(x)} != {len(y)})")
    ax = _get_ax(ax)
    ax.plot(x, y, **kwargs)
    _apply_labels(ax, title, xlabel, ylabel)
    return ax


def bar_plot(
    categories: Sequence[str],
    values: Sequence[float],
    *,
    title: Optional[str] = None,
    xlabel: Optional[str] = None,
    ylabel: Optional[str] = None,
    ax: Optional[Axes] = None,
    **kwargs,
) -> Axes:
    """Draw a vertical bar chart of ``values`` labelled by ``categories``.

    Extra keyword arguments are forwarded to
    :meth:`matplotlib.axes.Axes.bar`.
    """
    if len(categories) != len(values):
        raise ValueError(
            f"categories and values must have equal length "
            f"({len(categories)} != {len(values)})"
        )
    ax = _get_ax(ax)
    ax.bar(categories, values, **kwargs)
    _apply_labels(ax, title, xlabel, ylabel)
    return ax


def scatter_plot(
    x: Sequence[float],
    y: Sequence[float],
    *,
    title: Optional[str] = None,
    xlabel: Optional[str] = None,
    ylabel: Optional[str] = None,
    ax: Optional[Axes] = None,
    **kwargs,
) -> Axes:
    """Draw a scatter plot of ``y`` against ``x``.

    Extra keyword arguments are forwarded to
    :meth:`matplotlib.axes.Axes.scatter`.
    """
    if len(x) != len(y):
        raise ValueError(f"x and y must have equal length ({len(x)} != {len(y)})")
    ax = _get_ax(ax)
    ax.scatter(x, y, **kwargs)
    _apply_labels(ax, title, xlabel, ylabel)
    return ax


def histogram(
    data: Sequence[float],
    *,
    bins: int = 10,
    title: Optional[str] = None,
    xlabel: Optional[str] = None,
    ylabel: Optional[str] = "Frequency",
    ax: Optional[Axes] = None,
    **kwargs,
) -> Axes:
    """Draw a histogram of ``data`` using ``bins`` buckets.

    Extra keyword arguments are forwarded to
    :meth:`matplotlib.axes.Axes.hist`.
    """
    ax = _get_ax(ax)
    ax.hist(data, bins=bins, **kwargs)
    _apply_labels(ax, title, xlabel, ylabel)
    return ax
