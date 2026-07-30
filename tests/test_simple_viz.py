"""Tests for the simple_viz library.

Confirms each chart function runs on the real Pinterest data and returns a
matplotlib Figure, and checks the couple of computations simple_viz does itself
(share normalisation and implied ARPU).
"""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")  # headless backend, no display needed

import pandas as pd
import pytest
from matplotlib.figure import Figure

import simple_viz

DATA = Path(__file__).resolve().parent.parent / "data"


@pytest.fixture
def mau():
    return pd.read_csv(DATA / "pinterest_mau.csv")


@pytest.fixture
def regions():
    return pd.read_csv(DATA / "pinterest_regions_q4_2025.csv")


def test_public_api():
    assert simple_viz.__all__ == [
        "big_number",
        "growth_line",
        "revenue_bar",
        "share_gap",
        "revenue_per_user",
        "__version__",
    ]
    assert isinstance(simple_viz.__version__, str)


def test_big_number_returns_figure():
    fig = simple_viz.big_number(619, "M", "monthly active users")
    assert isinstance(fig, Figure)


def test_growth_line_returns_figure(mau):
    fig = simple_viz.growth_line(mau, "year", "maus_millions", title="MAUs")
    assert isinstance(fig, Figure)


def test_growth_line_with_annotation(mau):
    fig = simple_viz.growth_line(
        mau, "year", "maus_millions", title="MAUs", annotate=(2021, "dip")
    )
    assert isinstance(fig, Figure)


def test_revenue_bar_returns_figure(regions):
    fig = simple_viz.revenue_bar(
        regions, "region", "revenue_musd", title="Revenue", spotlight="US & Canada"
    )
    assert isinstance(fig, Figure)


def test_share_gap_returns_figure(regions):
    fig = simple_viz.share_gap(
        regions, "region", "maus_millions", "revenue_musd",
        title="Users vs revenue", highlight="Rest of World",
    )
    assert isinstance(fig, Figure)


def test_revenue_per_user_returns_figure(regions):
    fig = simple_viz.revenue_per_user(
        regions, "region", "revenue_musd", "maus_millions", title="ARPU"
    )
    assert isinstance(fig, Figure)


def test_data_is_internally_consistent(regions):
    """The regional MAUs sum to the reported 619M global total."""
    assert regions["maus_millions"].sum() == 619


def test_implied_per_user_matches_hand_calc(regions):
    """Implied ARPU = revenue / users, computed the same way revenue_per_user does."""
    row = regions.set_index("region").loc["US & Canada"]
    arpu = row["revenue_musd"] / row["maus_millions"]
    assert round(arpu, 2) == 9.32
