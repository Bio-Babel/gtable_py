"""Tests for _add_space.py — cover missing lines."""

import pytest
from grid_py import Unit

from gtable_py import Gtable, gtable_add_col_space, gtable_add_row_space


class TestGtableAddColSpace:
    def test_single_col_no_space(self):
        """n=0 path: single column table returns unchanged."""
        g = Gtable(widths=Unit(1, "cm"), heights=Unit(1, "cm"))
        result = gtable_add_col_space(g, Unit(1, "cm"))
        assert result.ncol == 1

    def test_wrong_length_raises(self):
        g = Gtable(widths=Unit([1, 2, 3], "cm"), heights=Unit(1, "cm"))
        with pytest.raises(ValueError, match="length 1 or ncol - 1"):
            gtable_add_col_space(g, Unit([1, 2, 3], "cm"))  # needs 1 or 2

    def test_multi_width(self):
        """Multiple widths (length n-1) path."""
        g = Gtable(widths=Unit([1, 2, 3], "cm"), heights=Unit(1, "cm"))
        result = gtable_add_col_space(g, Unit([0.5, 0.5], "cm"))
        assert result.ncol == 5  # 3 original + 2 spacers


class TestGtableAddRowSpace:
    def test_single_row_no_space(self):
        """n=0 path: single row table returns unchanged."""
        g = Gtable(widths=Unit(1, "cm"), heights=Unit(1, "cm"))
        result = gtable_add_row_space(g, Unit(1, "cm"))
        assert result.nrow == 1

    def test_wrong_length_raises(self):
        g = Gtable(widths=Unit(1, "cm"), heights=Unit([1, 2, 3], "cm"))
        with pytest.raises(ValueError, match="length 1 or nrow - 1"):
            gtable_add_row_space(g, Unit([1, 2, 3], "cm"))

    def test_multi_height(self):
        """Multiple heights (length n-1) path."""
        g = Gtable(widths=Unit(1, "cm"), heights=Unit([1, 2, 3], "cm"))
        result = gtable_add_row_space(g, Unit([0.5, 0.5], "cm"))
        assert result.nrow == 5
