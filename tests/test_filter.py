"""Tests for gtable_filter — ported from test-filter.R."""

import pytest
from grid_py import Unit, circle_grob, lines_grob, polygon_grob, rect_grob

from gtable_py import Gtable, gtable_add_grob, gtable_filter


@pytest.fixture
def gt():
    """Create a 4-row gtable with named grobs."""
    g = Gtable(widths=Unit(1, "null"), heights=Unit([1, 1, 1, 1], "null"))
    g = gtable_add_grob(
        g,
        [circle_grob(), rect_grob(), polygon_grob(), lines_grob()],
        t=[1, 2, 3, 4],
        l=1,
        name=["circle", "rect", "polygon", "lines"],
    )
    return g


class TestFilter:
    def test_filter_single(self, gt):
        result = gtable_filter(gt, "circle")
        assert result.layout["name"] == ["circle"]

    def test_filter_invert(self, gt):
        result = gtable_filter(gt, "circle", invert=True)
        assert result.layout["name"] == ["rect", "polygon", "lines"]

    def test_filter_regex(self, gt):
        result = gtable_filter(gt, "(circle)|(rect)")
        assert result.layout["name"] == ["circle", "rect"]

    def test_filter_fixed_no_match(self, gt):
        result = gtable_filter(gt, "(circle)|(rect)", fixed=True, trim=False)
        assert len(result) == 0
