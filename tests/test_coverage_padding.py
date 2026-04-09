"""Tests for _padding.py — gtable_add_padding (38% -> ~100%)."""

import pytest
from grid_py import Unit

from gtable_py import Gtable, gtable_add_padding


class TestGtableAddPadding:
    def test_basic_padding(self):
        g = Gtable(widths=Unit(1, "cm"), heights=Unit(1, "cm"))
        padded = gtable_add_padding(g, Unit([0.5, 0.5, 0.5, 0.5], "cm"))
        # 1 original row + 2 padding rows (top, bottom)
        assert padded.nrow == 3
        # 1 original col + 2 padding cols (left, right)
        assert padded.ncol == 3

    def test_padding_preserves_grobs(self):
        """Padding with 4 values preserves original structure."""
        from gtable_py import gtable_add_grob
        from grid_py import rect_grob
        g = Gtable(widths=Unit(1, "cm"), heights=Unit(1, "cm"))
        g = gtable_add_grob(g, rect_grob(), t=1, l=1)
        padded = gtable_add_padding(g, Unit([1, 1, 1, 1], "cm"))
        assert len(padded) == 1  # grob preserved

    def test_single_value_recycled(self):
        g = Gtable(widths=Unit(1, "cm"), heights=Unit(1, "cm"))
        padded = gtable_add_padding(g, Unit(1, "cm"))
        assert padded.nrow == 3
        assert padded.ncol == 3

    def test_two_values_recycled(self):
        g = Gtable(widths=Unit(1, "cm"), heights=Unit(1, "cm"))
        padded = gtable_add_padding(g, Unit([1, 2], "cm"))
        assert padded.nrow == 3
        assert padded.ncol == 3
