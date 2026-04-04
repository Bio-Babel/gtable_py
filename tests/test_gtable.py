"""Tests for core Gtable class — ported from test-gtable.R."""

import pytest
from grid_py import Unit, circle_grob

from gtable_py import Gtable, as_gtable, gtable_height, gtable_width, is_gtable


class TestAsGtable:
    def test_gtable_identity(self):
        g1 = Gtable(Unit(1, "npc"), Unit(1, "npc"))
        assert as_gtable(g1) is g1

    def test_grob_conversion(self):
        g2 = circle_grob(r=Unit(1, "cm"))
        test = as_gtable(g2)
        assert is_gtable(test)

    def test_widths_truncation(self):
        g2 = circle_grob(r=Unit(1, "cm"))
        with pytest.warns(UserWarning):
            as_gtable(g2, widths=Unit([1, 1], "cm"))

    def test_heights_truncation(self):
        g2 = circle_grob(r=Unit(1, "cm"))
        with pytest.warns(UserWarning):
            as_gtable(g2, heights=Unit([1, 1], "cm"))

    def test_invalid_type(self):
        with pytest.raises(TypeError):
            as_gtable([1, 2, 3, 4, 5])


class TestIsGtable:
    def test_is_gtable(self):
        g = Gtable(Unit(1, "cm"), Unit(1, "cm"))
        assert is_gtable(g)
        assert not is_gtable("not a gtable")
        assert not is_gtable(42)


class TestDimensions:
    def test_shape(self):
        g = Gtable(Unit([1, 2], "cm"), Unit([3, 4, 5], "cm"))
        assert g.shape == (3, 2)
        assert g.nrow == 3
        assert g.ncol == 2

    def test_empty(self):
        g = Gtable()
        assert g.shape == (0, 0)
        assert len(g) == 0


class TestDimnames:
    def test_set_get(self):
        g = Gtable(Unit([1, 2, 3], "cm"), Unit([1, 2, 3], "cm"))
        g.dimnames = (["r1", "r2", "r3"], ["c1", "c2", "c3"])
        assert g.dimnames == (["r1", "r2", "r3"], ["c1", "c2", "c3"])

    def test_duplicate_raises(self):
        g = Gtable(Unit([1, 2], "cm"), Unit([1, 2], "cm"))
        with pytest.raises(ValueError, match="distinct"):
            g.dimnames = (["a", "a"], ["b", "c"])


class TestTranspose:
    def test_transpose(self):
        g = Gtable(Unit([1, 2], "cm"), Unit([3, 4, 5], "cm"))
        t = g.transpose()
        assert t.shape == (2, 3)


class TestRepr:
    def test_empty_repr(self):
        g = Gtable(Unit([1, 2], "cm"), Unit([3, 4], "cm"))
        r = repr(g)
        assert "TableGrob" in r
        assert "0 grobs" in r
