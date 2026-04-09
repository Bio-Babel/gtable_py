"""Tests for _gtable.py — cover missing lines in main Gtable class."""

import copy

import pytest
from grid_py import Unit, Viewport, rect_grob, circle_grob

from gtable_py import (
    Gtable,
    gtable_add_grob,
    gtable_height,
    gtable_width,
)


class TestGtableConstructorWithVp:
    def test_vp_passed(self):
        vp = Viewport(
            name="test_vp",
            width=Unit(1, "npc"),
            height=Unit(1, "npc"),
            just="centre",
        )
        # Add justification attribute that Gtable constructor expects
        vp.justification = vp.just
        g = Gtable(widths=Unit(1, "cm"), heights=Unit(1, "cm"), vp=vp)
        assert g is not None

    def test_respect_property(self):
        g = Gtable(widths=Unit(1, "cm"), heights=Unit(1, "cm"), respect=True)
        assert g.respect is True
        g.respect = False
        assert g.respect is False


class TestPropertySetters:
    def test_grobs_setter(self):
        g = Gtable(widths=Unit(1, "cm"), heights=Unit(1, "cm"))
        g.grobs = [rect_grob()]
        assert len(g.grobs) == 1

    def test_layout_setter(self):
        g = Gtable(widths=Unit(1, "cm"), heights=Unit(1, "cm"))
        g.layout = {"t": [1], "l": [1], "b": [1], "r": [1], "z": [1], "clip": ["on"], "name": ["test"]}
        assert g.layout["t"] == [1]

    def test_widths_setter(self):
        g = Gtable()
        g.widths = Unit([1, 2], "cm")
        assert g.ncol == 2

    def test_heights_setter(self):
        g = Gtable()
        g.heights = Unit([1, 2, 3], "cm")
        assert g.nrow == 3

    def test_rownames_setter(self):
        g = Gtable(widths=Unit(1, "cm"), heights=Unit([1, 2], "cm"))
        g.rownames = ["a", "b"]
        assert g.rownames == ["a", "b"]
        g.rownames = None
        assert g.rownames is None

    def test_colnames_setter(self):
        g = Gtable(widths=Unit([1, 2], "cm"), heights=Unit(1, "cm"))
        g.colnames = ["x", "y"]
        assert g.colnames == ["x", "y"]
        g.colnames = None
        assert g.colnames is None


class TestDimnames:
    def test_duplicate_colnames_raises(self):
        g = Gtable(widths=Unit([1, 2], "cm"), heights=Unit([1, 2], "cm"))
        with pytest.raises(ValueError, match="colnames must be distinct"):
            g.dimnames = (["r1", "r2"], ["c", "c"])

    def test_none_dimnames(self):
        g = Gtable(widths=Unit(1, "cm"), heights=Unit(1, "cm"))
        g.dimnames = (None, None)
        assert g.rownames is None
        assert g.colnames is None


class TestReprWithGrobs:
    def test_repr_with_grobs(self):
        g = Gtable(widths=Unit(1, "cm"), heights=Unit(1, "cm"))
        g = gtable_add_grob(g, rect_grob(), t=1, l=1)
        r = repr(g)
        assert "1 grobs" in r
        assert "z=" in r


class TestGetitem:
    def test_basic_subset(self):
        g = Gtable(widths=Unit([1, 2], "cm"), heights=Unit([1, 2, 3], "cm"))
        g = gtable_add_grob(g, rect_grob(), t=1, l=1)
        g = gtable_add_grob(g, rect_grob(), t=2, l=2)
        sub = g[0:2, 0:1]
        assert sub.nrow == 2
        assert sub.ncol == 1

    def test_invalid_key(self):
        g = Gtable(widths=Unit(1, "cm"), heights=Unit(1, "cm"))
        with pytest.raises(IndexError):
            g[0]

    def test_name_based_indexing(self):
        g = Gtable(
            widths=Unit([1, 2], "cm"),
            heights=Unit([1, 2], "cm"),
            rownames=["r1", "r2"],
            colnames=["c1", "c2"],
        )
        g = gtable_add_grob(g, rect_grob(), t=1, l=1)
        sub = g[["r1"], ["c1"]]
        assert sub.nrow == 1
        assert sub.ncol == 1

    def test_missing_name_adds_zero_row(self):
        g = Gtable(
            widths=Unit([1, 2], "cm"),
            heights=Unit([1, 2], "cm"),
            rownames=["r1", "r2"],
            colnames=["c1", "c2"],
        )
        g = gtable_add_grob(g, rect_grob(), t=1, l=1)
        sub = g[["r1", "missing"], ["c1"]]
        assert sub.nrow == 2

    def test_negative_int_index(self):
        g = Gtable(widths=Unit([1, 2], "cm"), heights=Unit([1, 2], "cm"))
        g = gtable_add_grob(g, rect_grob(), t=1, l=1)
        sub = g[[-1], [-1]]
        assert sub.nrow == 1
        assert sub.ncol == 1

    def test_single_int_index(self):
        g = Gtable(widths=Unit([1, 2], "cm"), heights=Unit([1, 2], "cm"))
        g = gtable_add_grob(g, rect_grob(), t=1, l=1)
        sub = g[0, 0]
        assert sub.nrow == 1
        assert sub.ncol == 1

    def test_invalid_index_type_raises(self):
        g = Gtable(widths=Unit(1, "cm"), heights=Unit(1, "cm"))
        with pytest.raises(IndexError, match="Invalid selector"):
            g[{}, 0]

    def test_invalid_item_type_in_list(self):
        g = Gtable(widths=Unit(1, "cm"), heights=Unit(1, "cm"))
        with pytest.raises(IndexError, match="Invalid index type"):
            g[[1.5], 0]

    def test_non_increasing_raises(self):
        g = Gtable(widths=Unit([1, 2, 3], "cm"), heights=Unit([1, 2, 3], "cm"))
        with pytest.raises(IndexError, match="increasing"):
            g[[2, 1, 0], slice(None)]

    def test_cols_non_increasing_raises(self):
        g = Gtable(widths=Unit([1, 2, 3], "cm"), heights=Unit([1, 2, 3], "cm"))
        with pytest.raises(IndexError, match="increasing"):
            g[slice(None), [2, 1, 0]]

    def test_missing_col_name(self):
        g = Gtable(
            widths=Unit([1, 2], "cm"),
            heights=Unit([1, 2], "cm"),
            rownames=["r1", "r2"],
            colnames=["c1", "c2"],
        )
        sub = g[["r1"], ["c1", "missing_col"]]
        assert sub.ncol == 2


class TestGtableHeightWidth:
    def test_height_empty(self):
        g = Gtable()
        h = gtable_height(g)
        assert h is not None

    def test_width_empty(self):
        g = Gtable()
        w = gtable_width(g)
        assert w is not None

    def test_height_with_data(self):
        g = Gtable(widths=Unit(1, "cm"), heights=Unit([1, 2], "cm"))
        h = gtable_height(g)
        assert h is not None

    def test_width_with_data(self):
        g = Gtable(widths=Unit([1, 2], "cm"), heights=Unit(1, "cm"))
        w = gtable_width(g)
        assert w is not None


class TestMakeContextAndContent:
    def test_make_context_no_vp(self):
        g = Gtable(widths=Unit(1, "cm"), heights=Unit(1, "cm"))
        result = g.make_context()
        assert result.vp is not None

    def test_make_context_with_vp(self):
        vp = Viewport(name="outer", width=Unit(1, "npc"), height=Unit(1, "npc"), just="centre")
        vp.justification = vp.just
        g = Gtable(widths=Unit(1, "cm"), heights=Unit(1, "cm"), vp=vp)
        result = g.make_context()
        assert result.vp is not None

    def test_make_content(self):
        g = Gtable(widths=Unit(1, "cm"), heights=Unit(1, "cm"))
        g = gtable_add_grob(g, rect_grob(), t=1, l=1)
        result = g.make_content()
        assert result is not None


class TestWidthHeightDetails:
    def test_width_details(self):
        g = Gtable(widths=Unit(1, "cm"), heights=Unit(1, "cm"))
        w = g.width_details()
        assert w is not None

    def test_height_details(self):
        g = Gtable(widths=Unit(1, "cm"), heights=Unit(1, "cm"))
        h = g.height_details()
        assert h is not None


class TestGtableLayout:
    def test_gtable_layout_no_widths(self):
        from gtable_py._gtable import _gtable_layout
        g = Gtable()
        layout = _gtable_layout(g)
        assert layout is not None


class TestCopy:
    def test_copy(self):
        g = Gtable(
            widths=Unit(1, "cm"),
            heights=Unit(1, "cm"),
            rownames=["r1"],
            colnames=["c1"],
        )
        g = gtable_add_grob(g, rect_grob(), t=1, l=1)
        g2 = copy.copy(g)
        assert g2.nrow == g.nrow
        assert g2.ncol == g.ncol
        assert len(g2) == len(g)


class TestUnitSubset:
    def test_single_index(self):
        from gtable_py._gtable import _unit_subset
        result = _unit_subset(Unit([1, 2, 3], "cm"), [2])
        assert len(result) == 1

    def test_multiple_indices(self):
        from gtable_py._gtable import _unit_subset
        result = _unit_subset(Unit([1, 2, 3], "cm"), [1, 3])
        assert len(result) == 2
