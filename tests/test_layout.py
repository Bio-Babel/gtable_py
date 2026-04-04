"""Tests for adding rows, columns, grobs, and spacing — ported from test-layout.R."""

import math

import pytest
from grid_py import Unit, rect_grob

from gtable_py import (
    Gtable,
    gtable_add_col_space,
    gtable_add_cols,
    gtable_add_grob,
    gtable_add_row_space,
    gtable_add_rows,
)


def gtable_find(x, grob):
    """Find the layout row for a specific grob (by identity)."""
    layout = x.layout
    for i, g in enumerate(x.grobs):
        if g is grob:
            return {k: layout[k][i] for k in layout}
    return None


class TestAddRows:
    def test_rows_grow(self, cm):
        layout = Gtable()
        assert layout.nrow == 0

        layout = gtable_add_rows(layout, Unit(1, "cm"))
        assert layout.nrow == 1

        layout = gtable_add_rows(layout, Unit(1, "cm"))
        layout = gtable_add_rows(layout, Unit(1, "cm"))
        assert layout.nrow == 3

        layout = gtable_add_rows(layout, Unit([1, 2], "cm"))
        assert layout.nrow == 5


class TestAddCols:
    def test_cols_grow(self, cm):
        layout = Gtable()
        assert layout.ncol == 0

        layout = gtable_add_cols(layout, Unit(1, "cm"))
        assert layout.ncol == 1

        layout = gtable_add_cols(layout, Unit([1, 1], "cm"))
        assert layout.ncol == 3

        layout = gtable_add_cols(layout, Unit([1, 2], "cm"))
        assert layout.ncol == 5


class TestSettingGetting:
    def test_setting_getting(self, cm, grob1):
        layout = gtable_add_cols(gtable_add_rows(Gtable(), cm), cm)
        layout = gtable_add_grob(layout, grob1, 1, 1)
        loc = gtable_find(layout, grob1)
        assert loc is not None
        assert loc["t"] == 1
        assert loc["r"] == 1
        assert loc["b"] == 1
        assert loc["l"] == 1


class TestSpanningGrobsAfterInsertion:
    def test_spanning_within(self, cm, grob1):
        layout = gtable_add_cols(
            gtable_add_rows(Gtable(), Unit([1, 1, 1], "cm")),
            Unit([1, 1, 1], "cm"),
        )
        layout = gtable_add_grob(layout, grob1, 1, 1, 3, 3)

        within = gtable_add_rows(
            gtable_add_cols(layout, cm, pos=2), cm, pos=2
        )
        loc = gtable_find(within, grob1)
        assert loc["t"] == 1
        assert loc["l"] == 1
        assert loc["b"] == 4
        assert loc["r"] == 4

    def test_spanning_top_left(self, cm, grob1):
        layout = gtable_add_cols(
            gtable_add_rows(Gtable(), Unit([1, 1, 1], "cm")),
            Unit([1, 1, 1], "cm"),
        )
        layout = gtable_add_grob(layout, grob1, 1, 1, 3, 3)

        top_left = gtable_add_cols(layout, cm, pos=0)
        top_left = gtable_add_rows(top_left, cm, pos=0)
        loc = gtable_find(top_left, grob1)
        assert loc["t"] == 2
        assert loc["l"] == 2
        assert loc["b"] == 4
        assert loc["r"] == 4

    def test_spanning_bottom_right(self, cm, grob1):
        layout = gtable_add_cols(
            gtable_add_rows(Gtable(), Unit([1, 1, 1], "cm")),
            Unit([1, 1, 1], "cm"),
        )
        layout = gtable_add_grob(layout, grob1, 1, 1, 3, 3)

        bottom_right = gtable_add_cols(layout, cm)
        bottom_right = gtable_add_rows(bottom_right, cm)
        loc = gtable_find(bottom_right, grob1)
        assert loc["t"] == 1
        assert loc["l"] == 1
        assert loc["b"] == 3
        assert loc["r"] == 3


class TestSpacing:
    def test_n_plus_1_after_spacing(self, cm):
        layout = Gtable()
        layout = gtable_add_rows(layout, Unit([1, 1, 1], "cm"))
        layout = gtable_add_cols(layout, Unit([1, 1, 1], "cm"))

        layout = gtable_add_col_space(layout, cm)
        assert layout.ncol == 5

        layout = gtable_add_row_space(layout, cm)
        # ncol stays 5
        assert layout.ncol == 5


class TestNegativePositions:
    def test_negative_positions(self, cm, grob1):
        layout = Gtable()
        layout = gtable_add_rows(layout, Unit([1, 1, 1], "cm"))
        layout = gtable_add_cols(layout, Unit([1, 1, 1], "cm"))

        col_span = gtable_add_grob(layout, grob1, t=1, l=1, r=-1)
        loc = gtable_find(col_span, grob1)
        assert loc["t"] == 1
        assert loc["l"] == 1
        assert loc["b"] == 1
        assert loc["r"] == 3

        row_span = gtable_add_grob(layout, grob1, t=1, l=1, b=-1)
        loc = gtable_find(row_span, grob1)
        assert loc["t"] == 1
        assert loc["l"] == 1
        assert loc["b"] == 3
        assert loc["r"] == 1


class TestMultipleGrobs:
    def test_z_inf(self, cm, grob1):
        grobs = [grob1] * 8
        tval = [1, 2, 3, 1, 2, 3, 1, 2]
        layout = gtable_add_cols(
            gtable_add_rows(Gtable(), Unit([1, 1, 1], "cm")),
            Unit([1, 1, 1], "cm"),
        )
        layout = gtable_add_grob(layout, grobs, tval, 1, 3, 3, z=math.inf)
        assert layout.layout["t"] == tval
        assert layout.layout["z"] == list(range(1, 9))

    def test_z_neg_inf(self, cm, grob1):
        grobs = [grob1] * 8
        layout = gtable_add_cols(
            gtable_add_rows(Gtable(), Unit([1, 1, 1], "cm")),
            Unit([1, 1, 1], "cm"),
        )
        layout = gtable_add_grob(layout, grobs, 1, 1, 3, 3, z=-math.inf)
        assert layout.layout["z"] == list(range(-7, 1))

    def test_z_mixed(self, cm, grob1):
        grobs = [grob1] * 8
        zval = [math.inf, math.inf, 6, 0, -math.inf, math.inf, -2, -math.inf]
        layout = gtable_add_cols(
            gtable_add_rows(Gtable(), Unit([1, 1, 1], "cm")),
            Unit([1, 1, 1], "cm"),
        )
        layout = gtable_add_grob(layout, grobs, 1, 1, 3, 3, z=zval)
        assert layout.layout["z"] == [7, 8, 6, 0, -4, 9, -2, -3]

    def test_length_mismatch_errors(self, cm, grob1):
        grobs = [grob1] * 8
        tval = [1, 2, 3, 1, 2, 3, 1, 2]
        layout = gtable_add_cols(
            gtable_add_rows(Gtable(), Unit([1, 1, 1], "cm")),
            Unit([1, 1, 1], "cm"),
        )
        with pytest.raises(ValueError):
            gtable_add_grob(layout, grobs, [1, 2, 3], 1, 3, 3)
        with pytest.raises(ValueError):
            gtable_add_grob(layout, grobs, tval, [1, 2], 3, 3)
