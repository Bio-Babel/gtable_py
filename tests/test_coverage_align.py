"""Tests for _align.py — gtable alignment functions (0% -> ~100%)."""

import pytest
from grid_py import Unit, rect_grob

from gtable_py import Gtable, gtable_add_grob
from gtable_py._align import gtable_align, gtable_join, gtable_reindex


@pytest.fixture
def gt_a():
    """2-row, 2-col table with rownames a,b and colnames x,y."""
    g = Gtable(
        widths=Unit([1, 2], "cm"),
        heights=Unit([1, 2], "cm"),
        rownames=["a", "b"],
        colnames=["x", "y"],
    )
    g = gtable_add_grob(g, rect_grob(), t=1, l=1)
    return g


@pytest.fixture
def gt_b():
    """2-row, 2-col table with rownames b,c and colnames x,y."""
    g = Gtable(
        widths=Unit([4, 5], "cm"),
        heights=Unit([6, 7], "cm"),
        rownames=["b", "c"],
        colnames=["x", "y"],
    )
    g = gtable_add_grob(g, rect_grob(), t=1, l=1)
    return g


class TestGtableJoin:
    def test_join_along_1_cbind(self):
        """Inner join along=1 then cbind."""
        g1 = Gtable(widths=Unit(1, "cm"), heights=Unit([1, 2], "cm"),
                     rownames=["a", "b"], colnames=["x"])
        g2 = Gtable(widths=Unit(2, "cm"), heights=Unit([1, 2], "cm"),
                     rownames=["a", "b"], colnames=["y"])
        result = gtable_join(g1, g2, along=1, join="inner")
        assert result.ncol == 2
        assert result.nrow == 2

    def test_join_along_2_rbind(self):
        """Inner join along=2 then rbind."""
        g1 = Gtable(widths=Unit([1, 2], "cm"), heights=Unit(1, "cm"),
                     rownames=["r1"], colnames=["x", "y"])
        g2 = Gtable(widths=Unit([1, 2], "cm"), heights=Unit(1, "cm"),
                     rownames=["r2"], colnames=["x", "y"])
        result = gtable_join(g1, g2, along=2, join="inner")
        assert result.nrow == 2

    def test_join_along_invalid(self):
        """along > 2 raises ValueError in gtable_join."""
        # Use simple matching tables for the along=1 cbind path
        g1 = Gtable(widths=Unit(1, "cm"), heights=Unit(1, "cm"),
                     rownames=["a"], colnames=["x"])
        g2 = Gtable(widths=Unit(1, "cm"), heights=Unit(1, "cm"),
                     rownames=["a"], colnames=["x"])
        # gtable_join calls gtable_align first which does dimnames[along-1]
        # along=3 -> dimnames[2] -> IndexError from tuple
        with pytest.raises((ValueError, IndexError)):
            gtable_join(g1, g2, along=3)


class TestGtableAlign:
    def test_invalid_join(self, gt_a, gt_b):
        with pytest.raises(ValueError, match="join"):
            gtable_align(gt_a, gt_b, join="bad")

    def test_right_join(self, gt_a, gt_b):
        xa, ya = gtable_align(gt_a, gt_b, along=1, join="right")
        assert xa.rownames == ["b", "c"]
        assert ya.rownames == ["b", "c"]

    def test_inner_join(self, gt_a, gt_b):
        xa, ya = gtable_align(gt_a, gt_b, along=1, join="inner")
        # only "b" is common
        assert xa.rownames == ["b"]
        assert ya.rownames == ["b"]

    def test_left_join_same_names(self):
        """Left join where both have same names (no reordering needed)."""
        g1 = Gtable(widths=Unit(1, "cm"), heights=Unit([1, 2], "cm"),
                     rownames=["a", "b"], colnames=["x"])
        g2 = Gtable(widths=Unit(1, "cm"), heights=Unit([1, 2], "cm"),
                     rownames=["a", "b"], colnames=["x"])
        xa, ya = gtable_align(g1, g2, along=1, join="left")
        assert xa.rownames == ["a", "b"]

    def test_outer_join_same_names(self):
        """Outer join where both have same names."""
        g1 = Gtable(widths=Unit(1, "cm"), heights=Unit([1, 2], "cm"),
                     rownames=["a", "b"], colnames=["x"])
        g2 = Gtable(widths=Unit(1, "cm"), heights=Unit([1, 2], "cm"),
                     rownames=["a", "b"], colnames=["x"])
        xa, ya = gtable_align(g1, g2, along=1, join="outer")
        assert xa.rownames == ["a", "b"]

    def test_align_no_names_raises(self, gt_a):
        gt_no_names = Gtable(widths=Unit([1, 2], "cm"), heights=Unit(1, "cm"))
        with pytest.raises(ValueError, match="names"):
            gtable_align(gt_a, gt_no_names, along=1)

    def test_align_along_2(self, gt_a, gt_b):
        xa, ya = gtable_align(gt_a, gt_b, along=2, join="inner")
        assert xa.colnames == ["x", "y"]
        assert ya.colnames == ["x", "y"]


class TestGtableReindex:
    def test_identity_reindex(self, gt_a):
        result = gtable_reindex(gt_a, ["a", "b"], along=1)
        assert result.rownames == ["a", "b"]

    def test_reindex_subset(self, gt_a):
        result = gtable_reindex(gt_a, ["b"], along=1)
        assert result.rownames == ["b"]

    def test_reindex_with_missing_cols(self, gt_a):
        # Adding missing col at end -> names order is preserved
        result = gtable_reindex(gt_a, ["x", "y", "z_new"], along=2)
        assert "z_new" in result.colnames

    def test_reindex_with_missing_rows(self, gt_a):
        # Add missing row at end
        result = gtable_reindex(gt_a, ["a", "b", "c_new"], along=1)
        assert "c_new" in result.rownames

    def test_reindex_invalid_along(self, gt_a):
        with pytest.raises(ValueError, match="2d"):
            gtable_reindex(gt_a, ["a"], along=3)

    def test_reindex_no_names_raises(self):
        g = Gtable(widths=Unit(1, "cm"), heights=Unit(1, "cm"))
        with pytest.raises(ValueError, match="None"):
            gtable_reindex(g, ["a"], along=1)

    def test_reindex_cols_subset(self, gt_a):
        result = gtable_reindex(gt_a, ["y"], along=2)
        assert result.colnames == ["y"]
