"""Tests for _layouts.py — cover missing lines."""

import pytest
from grid_py import Unit, null_grob, rect_grob

from gtable_py import (
    Gtable,
    gtable_col,
    gtable_col_spacer,
    gtable_matrix,
    gtable_row,
    gtable_row_spacer,
    gtable_show_layout,
)


class TestGtableCol:
    def test_default_width_computed(self):
        """width=None triggers width_cm fallback."""
        grobs = [null_grob(), null_grob()]
        g = gtable_col("test", grobs)
        assert g.ncol == 1
        assert g.nrow == 2

    def test_z_length_mismatch(self):
        with pytest.raises(ValueError, match="same length"):
            gtable_col("test", [rect_grob()], z=[1, 2])

    def test_explicit_z(self):
        g = gtable_col("test", [rect_grob(), rect_grob()],
                        width=Unit(1, "cm"), heights=Unit([1, 1], "cm"),
                        z=[10, 20])
        assert g.nrow == 2

    def test_dict_grobs(self):
        """Dict input gives rownames."""
        grobs = {"row_a": rect_grob(), "row_b": rect_grob()}
        g = gtable_col("test", grobs, width=Unit(1, "cm"),
                        heights=Unit([1, 1], "cm"))
        assert g.rownames == ["row_a", "row_b"]


class TestGtableRow:
    def test_default_height_computed(self):
        grobs = [null_grob(), null_grob()]
        g = gtable_row("test", grobs)
        assert g.nrow == 1
        assert g.ncol == 2

    def test_z_length_mismatch(self):
        with pytest.raises(ValueError, match="same length"):
            gtable_row("test", [rect_grob()], z=[1, 2])

    def test_explicit_z(self):
        g = gtable_row("test", [rect_grob(), rect_grob()],
                        height=Unit(1, "cm"), widths=Unit([1, 1], "cm"),
                        z=[10, 20])
        assert g.ncol == 2

    def test_dict_grobs(self):
        grobs = {"col_a": rect_grob(), "col_b": rect_grob()}
        g = gtable_row("test", grobs, height=Unit(1, "cm"),
                        widths=Unit([1, 1], "cm"))
        assert g.colnames == ["col_a", "col_b"]


class TestGtableMatrix:
    def test_basic_matrix(self):
        grobs = [
            [rect_grob(), rect_grob()],
            [rect_grob(), rect_grob()],
        ]
        g = gtable_matrix("test", grobs,
                          widths=Unit([1, 1], "cm"),
                          heights=Unit([1, 1], "cm"))
        assert g.shape == (2, 2)
        assert len(g) == 4

    def test_width_mismatch(self):
        grobs = [[rect_grob(), rect_grob()]]
        with pytest.raises(ValueError, match="widths"):
            gtable_matrix("test", grobs,
                          widths=Unit(1, "cm"),
                          heights=Unit(1, "cm"))

    def test_height_mismatch(self):
        grobs = [[rect_grob()], [rect_grob()]]
        with pytest.raises(ValueError, match="heights"):
            gtable_matrix("test", grobs,
                          widths=Unit(1, "cm"),
                          heights=Unit(1, "cm"))

    def test_z_dimension_mismatch(self):
        grobs = [[rect_grob()]]
        with pytest.raises(ValueError, match="z"):
            gtable_matrix("test", grobs,
                          widths=Unit(1, "cm"),
                          heights=Unit(1, "cm"),
                          z=[[1, 2]])

    def test_explicit_z(self):
        grobs = [[rect_grob(), rect_grob()]]
        g = gtable_matrix("test", grobs,
                          widths=Unit([1, 1], "cm"),
                          heights=Unit(1, "cm"),
                          z=[[10, 20]])
        assert len(g) == 2


class TestSpacers:
    def test_row_spacer(self):
        g = gtable_row_spacer(Unit([1, 2], "cm"))
        assert g.ncol == 2
        assert g.nrow == 0

    def test_col_spacer(self):
        g = gtable_col_spacer(Unit([1, 2], "cm"))
        assert g.nrow == 2
        assert g.ncol == 0


class TestShowLayout:
    def test_non_gtable_raises(self):
        with pytest.raises(TypeError):
            gtable_show_layout("not a gtable")
