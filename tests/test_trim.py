"""Tests for gtable_trim — ported from test-trim.R."""

import pytest
from grid_py import Unit, rect_grob

from gtable_py import Gtable, gtable_add_grob, gtable_trim


class TestTrim:
    def test_trim_to_grob(self):
        gt_empty = Gtable(
            widths=Unit([1, 1, 1, 1], "null"),
            heights=Unit([1, 1, 1, 1], "null"),
        )
        gt = gtable_add_grob(gt_empty, rect_grob(), 1, 1)
        assert gtable_trim(gt).shape == (1, 1)

    def test_trim_empty(self):
        gt_empty = Gtable(
            widths=Unit([1, 1, 1, 1], "null"),
            heights=Unit([1, 1, 1, 1], "null"),
        )
        assert gtable_trim(gt_empty).shape == (0, 0)
