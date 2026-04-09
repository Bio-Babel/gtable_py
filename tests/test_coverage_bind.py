"""Tests for _bind.py — cover missing lines."""

import pytest
from grid_py import Unit, rect_grob

from gtable_py import Gtable, cbind_gtable, gtable_add_grob, gtable_col, rbind_gtable


class TestRbindEdgeCases:
    def test_rbind_empty_x(self):
        """x has 0 rows -> returns copy of y (line 102)."""
        from gtable_py._add_rows_cols import gtable_add_cols
        # Build a 0-row, 1-col table
        x = gtable_add_cols(Gtable(), Unit(1, "cm"))
        y = Gtable(widths=Unit(1, "cm"), heights=Unit(1, "cm"))
        result = rbind_gtable(x, y)
        assert result.nrow == 1

    def test_rbind_empty_y(self):
        """y has 0 rows -> returns copy of x (line 104)."""
        from gtable_py._add_rows_cols import gtable_add_cols
        x = Gtable(widths=Unit(1, "cm"), heights=Unit(1, "cm"))
        y = gtable_add_cols(Gtable(), Unit(1, "cm"))
        result = rbind_gtable(x, y)
        assert result.nrow == 1

    def test_rbind_invalid_size(self):
        g1 = gtable_col("a", [rect_grob()], width=Unit(1, "cm"), heights=Unit(1, "cm"))
        g2 = gtable_col("b", [rect_grob()], width=Unit(1, "cm"), heights=Unit(1, "cm"))
        with pytest.raises(ValueError, match="size"):
            rbind_gtable(g1, g2, size="bad")

    def test_rbind_size_min(self):
        g1 = gtable_col("a", [rect_grob()], width=Unit(1, "cm"), heights=Unit(1, "cm"))
        g2 = gtable_col("b", [rect_grob()], width=Unit(2, "cm"), heights=Unit(1, "cm"))
        result = rbind_gtable(g1, g2, size="min")
        assert result.nrow == 2

    def test_rbind_ncol_mismatch(self):
        g1 = Gtable(widths=Unit(1, "cm"), heights=Unit(1, "cm"))
        g2 = Gtable(widths=Unit([1, 2], "cm"), heights=Unit(1, "cm"))
        with pytest.raises(ValueError, match="same number of columns"):
            rbind_gtable(g1, g2)

    def test_rbind_with_z(self):
        g1 = gtable_col("a", [rect_grob()], width=Unit(1, "cm"), heights=Unit(1, "cm"))
        g2 = gtable_col("b", [rect_grob()], width=Unit(1, "cm"), heights=Unit(1, "cm"))
        result = rbind_gtable(g1, g2, z=[2, 1])
        assert result.nrow == 2


class TestCbindEdgeCases:
    def test_cbind_empty_x(self):
        """x has 0 cols -> returns copy of y."""
        from gtable_py._add_rows_cols import gtable_add_rows
        x = gtable_add_rows(Gtable(), Unit(1, "cm"))
        y = Gtable(widths=Unit(1, "cm"), heights=Unit(1, "cm"))
        result = cbind_gtable(x, y)
        assert result.ncol == 1

    def test_cbind_empty_y(self):
        x = Gtable(widths=Unit(1, "cm"), heights=Unit(1, "cm"))
        from gtable_py._add_rows_cols import gtable_add_rows
        y = gtable_add_rows(Gtable(), Unit(1, "cm"))
        result = cbind_gtable(x, y)
        assert result.ncol == 1

    def test_cbind_invalid_size(self):
        from gtable_py import gtable_row
        g1 = gtable_row("a", [rect_grob()], height=Unit(1, "cm"), widths=Unit(1, "cm"))
        g2 = gtable_row("b", [rect_grob()], height=Unit(1, "cm"), widths=Unit(1, "cm"))
        with pytest.raises(ValueError, match="size"):
            cbind_gtable(g1, g2, size="bad")

    def test_cbind_size_min(self):
        from gtable_py import gtable_row
        g1 = gtable_row("a", [rect_grob()], height=Unit(1, "cm"), widths=Unit(1, "cm"))
        g2 = gtable_row("b", [rect_grob()], height=Unit(2, "cm"), widths=Unit(1, "cm"))
        result = cbind_gtable(g1, g2, size="min")
        assert result.ncol == 2

    def test_cbind_nrow_mismatch(self):
        g1 = Gtable(widths=Unit(1, "cm"), heights=Unit(1, "cm"))
        g2 = Gtable(widths=Unit(1, "cm"), heights=Unit([1, 2], "cm"))
        with pytest.raises(ValueError, match="same number of rows"):
            cbind_gtable(g1, g2)

    def test_cbind_with_z(self):
        from gtable_py import gtable_row
        g1 = gtable_row("a", [rect_grob()], height=Unit(1, "cm"), widths=Unit(1, "cm"))
        g2 = gtable_row("b", [rect_grob()], height=Unit(1, "cm"), widths=Unit(1, "cm"))
        result = cbind_gtable(g1, g2, z=[2, 1])
        assert result.ncol == 2


class TestConcatNames:
    def test_both_none(self):
        from gtable_py._bind import _concat_names
        assert _concat_names(None, None) is None

    def test_one_none(self):
        from gtable_py._bind import _concat_names
        assert _concat_names(["a"], None) == ["a"]
        assert _concat_names(None, ["b"]) == ["b"]
