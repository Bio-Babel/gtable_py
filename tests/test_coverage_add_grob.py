"""Tests for _add_grob.py — cover missing lines."""

import math

import pytest
from grid_py import Unit, rect_grob

from gtable_py import Gtable, gtable_add_grob


class TestGtableAddGrobEdgeCases:
    def test_non_grob_in_list_raises(self):
        g = Gtable(widths=Unit(1, "cm"), heights=Unit(1, "cm"))
        with pytest.raises(TypeError, match="Grob"):
            gtable_add_grob(g, [42], t=1, l=1)

    def test_non_grob_not_list_raises(self):
        g = Gtable(widths=Unit(1, "cm"), heights=Unit(1, "cm"))
        with pytest.raises(TypeError, match="Grob"):
            gtable_add_grob(g, 42, t=1, l=1)

    def test_boolean_clip(self):
        g = Gtable(widths=Unit(1, "cm"), heights=Unit(1, "cm"))
        result = gtable_add_grob(g, rect_grob(), t=1, l=1, clip=True)
        assert result._layout["clip"][-1] == "on"

    def test_boolean_clip_false(self):
        g = Gtable(widths=Unit(1, "cm"), heights=Unit(1, "cm"))
        result = gtable_add_grob(g, rect_grob(), t=1, l=1, clip=False)
        assert result._layout["clip"][-1] == "off"

    def test_boolean_clip_list(self):
        g = Gtable(widths=Unit([1, 2], "cm"), heights=Unit(1, "cm"))
        result = gtable_add_grob(
            g, [rect_grob(), rect_grob()], t=1, l=[1, 2], clip=[True, False]
        )
        assert result._layout["clip"][-2] == "on"
        assert result._layout["clip"][-1] == "off"

    def test_neg_inf_z(self):
        g = Gtable(widths=Unit(1, "cm"), heights=Unit(1, "cm"))
        g = gtable_add_grob(g, rect_grob(), t=1, l=1, z=1)
        result = gtable_add_grob(g, rect_grob(), t=1, l=1, z=-math.inf)
        assert result._layout["z"][-1] < 1

    def test_length_mismatch_raises(self):
        g = Gtable(widths=Unit([1, 2], "cm"), heights=Unit(1, "cm"))
        with pytest.raises(ValueError, match="same length"):
            gtable_add_grob(
                g, [rect_grob(), rect_grob()], t=[1, 1], l=[1, 2],
                clip=["on", "off", "on"],  # length 3 != 2
            )
