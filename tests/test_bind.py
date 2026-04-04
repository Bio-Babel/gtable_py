"""Tests for rbind/cbind — ported from test-bind.R."""

import pytest
from grid_py import Unit

from gtable_py import (
    Gtable,
    cbind_gtable,
    gtable_add_cols,
    gtable_add_rows,
    gtable_col,
    rbind_gtable,
)


class TestRbind:
    def test_rows_grow(self, cm):
        lay1 = gtable_add_rows(Gtable(), cm)
        lay2 = gtable_add_rows(Gtable(), Unit([1, 1], "cm"))

        assert rbind_gtable(lay1, lay2).nrow == 3
        assert rbind_gtable(lay2, lay1).nrow == 3


class TestCbind:
    def test_cols_grow(self, cm):
        lay1 = gtable_add_cols(Gtable(), cm)
        lay2 = gtable_add_cols(Gtable(), Unit([1, 1], "cm"))

        assert cbind_gtable(lay1, lay2).ncol == 3
        assert cbind_gtable(lay2, lay1).ncol == 3


class TestSizeParameter:
    def test_cbind_heights(self, grob1, cm, cm2):
        col1 = gtable_col("col1", [grob1], cm, cm)
        col2 = gtable_col("col1", [grob1], cm2, cm2)

        result = cbind_gtable(col1, col2, size="first")
        assert len(result.heights) == 1

        result = cbind_gtable(col1, col2, size="last")
        assert len(result.heights) == 1

    def test_rbind_widths(self, grob1, cm, cm2):
        col1 = gtable_col("col1", [grob1], cm, cm)
        col2 = gtable_col("col1", [grob1], cm2, cm2)

        result = rbind_gtable(col1, col2, size="first")
        assert len(result.widths) == 1

        result = rbind_gtable(col1, col2, size="last")
        assert len(result.widths) == 1

    def test_dimension_mismatch(self, grob1, cm, cm2):
        col1 = gtable_col("c1", [grob1], cm, cm)
        # row1 has 2 rows, col1 has 1 row -> cbind should fail
        row1 = Gtable(Unit(1, "cm"), Unit([1, 1], "cm"))
        with pytest.raises(ValueError):
            cbind_gtable(col1, row1)
