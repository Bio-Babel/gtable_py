"""Tests for _utils.py — cover missing lines."""

import pytest
from grid_py import Unit, rect_grob, is_unit

from gtable_py import Gtable
from gtable_py._utils import (
    check_gtable,
    check_unit_arg,
    compare_unit,
    height_cm,
    insert_unit,
    neg_to_pos_vec,
    width_cm,
)


class TestCheckGtable:
    def test_valid_gtable(self):
        g = Gtable(widths=Unit(1, "cm"), heights=Unit(1, "cm"))
        check_gtable(g)  # should not raise

    def test_invalid_raises(self):
        with pytest.raises(TypeError, match="Gtable"):
            check_gtable("not a gtable")


class TestCheckUnitArg:
    def test_valid_unit(self):
        check_unit_arg(Unit(1, "cm"))  # no raise

    def test_invalid_raises(self):
        with pytest.raises(TypeError, match="Unit"):
            check_unit_arg(42, arg="width")


class TestNegToPosVec:
    def test_basic(self):
        result = neg_to_pos_vec([0, -1, 2], 5)
        assert result == [0, 5, 2]


class TestInsertUnit:
    def test_insert_middle(self):
        x = Unit([1, 2, 3], "cm")
        v = Unit(10, "cm")
        result = insert_unit(x, v, after=1)
        assert len(result) == 4

    def test_insert_empty_x(self):
        result = insert_unit(None, Unit(1, "cm"))
        assert len(result) == 1

    def test_insert_empty_values(self):
        x = Unit([1, 2], "cm")
        result = insert_unit(x, None)
        assert len(result) == 2

    def test_insert_at_start(self):
        x = Unit([1, 2], "cm")
        v = Unit(10, "cm")
        result = insert_unit(x, v, after=0)
        assert len(result) == 3

    def test_insert_at_end(self):
        x = Unit([1, 2], "cm")
        v = Unit(10, "cm")
        result = insert_unit(x, v, after=5)
        assert len(result) == 3


class TestCompareUnit:
    def test_min(self):
        x = Unit([1, 3], "cm")
        y = Unit([2, 1], "cm")
        result = compare_unit(x, y, "min")
        assert is_unit(result)

    def test_max(self):
        x = Unit([1, 3], "cm")
        y = Unit([2, 1], "cm")
        result = compare_unit(x, y, "max")
        assert is_unit(result)

    def test_empty_y(self):
        x = Unit([1, 2], "cm")
        result = compare_unit(x, None, "max")
        assert len(result) == 2

    def test_empty_x(self):
        y = Unit([1, 2], "cm")
        result = compare_unit(None, y, "max")
        assert len(result) == 2

    def test_invalid_comp(self):
        with pytest.raises(ValueError, match="comp"):
            compare_unit(Unit(1, "cm"), Unit(1, "cm"), "bad")


class TestWidthCm:
    def test_invalid_raises(self):
        with pytest.raises(TypeError, match="width_cm"):
            width_cm(42)


class TestHeightCm:
    def test_invalid_raises(self):
        with pytest.raises(TypeError, match="height_cm"):
            height_cm("bad")
