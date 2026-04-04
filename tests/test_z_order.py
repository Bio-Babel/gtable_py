"""Tests for z-ordering — ported from test-z-order.R."""

import pytest
from grid_py import Unit

from gtable_py import (
    Gtable,
    cbind_gtable,
    gtable_col,
    gtable_matrix,
    gtable_row,
    rbind_gtable,
)
from gtable_py._z import z_arrange_gtables, z_normalise


class TestZOrderLayouts:
    def test_column_default_z(self, grob1, grob2, grob3, grob4):
        gt = gtable_col("test", [grob1, grob2, grob3, grob4])
        layout = gt.layout
        # z for positions 1,2,3,4 should be 1,2,3,4
        z_by_pos = [layout["z"][i] for i in range(4)]
        # sorted by t position, z should be sequential
        pairs = sorted(zip(layout["t"], layout["z"]))
        assert [z for _, z in pairs] == [1, 2, 3, 4]

    def test_column_custom_z(self, grob1, grob2, grob3, grob4):
        zorder = [3, 1, 2, 4]
        gt = gtable_col("test", [grob1, grob2, grob3, grob4], z=zorder)
        layout = gt.layout
        pairs = sorted(zip(layout["t"], layout["z"]))
        assert [z for _, z in pairs] == zorder

    def test_row_default_z(self, grob1, grob2, grob3, grob4):
        gt = gtable_row("test", [grob1, grob2, grob3, grob4])
        layout = gt.layout
        pairs = sorted(zip(layout["l"], layout["z"]))
        assert [z for _, z in pairs] == [1, 2, 3, 4]

    def test_row_custom_z(self, grob1, grob2, grob3, grob4):
        zorder = [3, 1, 2, 4]
        gt = gtable_row("test", [grob1, grob2, grob3, grob4], z=zorder)
        layout = gt.layout
        pairs = sorted(zip(layout["l"], layout["z"]))
        assert [z for _, z in pairs] == zorder

    def test_matrix_default_z(self, grob1, grob2, grob3, grob4):
        gt = gtable_matrix(
            "test",
            [[grob1, grob3], [grob2, grob4]],
            Unit([1, 1], "null"),
            Unit([1, 1], "null"),
        )
        layout = gt.layout
        # Column-major: position = 2*(l-1) + t
        locs = [2 * (layout["l"][i] - 1) + layout["t"][i] for i in range(4)]
        z_by_loc = [layout["z"][locs.index(pos)] if pos in locs else 0 for pos in [1, 2, 3, 4]]
        # For default z (Inf), they should be sequential
        sorted_z = sorted(zip(locs, layout["z"]))
        assert [z for _, z in sorted_z] == [1, 2, 3, 4]

    def test_matrix_custom_z(self, grob1, grob2, grob3, grob4):
        zorder = [3, 1, 2, 4]
        gt = gtable_matrix(
            "test",
            [[grob1, grob3], [grob2, grob4]],
            Unit([1, 1], "null"),
            Unit([1, 1], "null"),
            z=[[3, 2], [1, 4]],
        )
        layout = gt.layout
        locs = [2 * (layout["l"][i] - 1) + layout["t"][i] for i in range(4)]
        sorted_z = sorted(zip(locs, layout["z"]))
        assert [z for _, z in sorted_z] == zorder


class TestZNormalise:
    def test_normalise(self, grob1, grob2, grob3, grob4):
        zorder = [0.001, -4, 0, 1e6]
        gt = gtable_col("test", [grob1, grob2, grob3, grob4], z=zorder)
        assert gt.layout["z"] == zorder
        gt1 = z_normalise(gt)
        assert sorted(gt1.layout["z"]) == [1, 2, 3, 4]

    def test_empty_layout(self):
        gt = Gtable(Unit([1, 2, 3], "cm"), Unit([2, 4], "cm"))
        gt1 = z_normalise(gt)
        assert len(gt1.layout["t"]) == 0


class TestZArrangeGtables:
    def test_arrange(self, grob1, grob2, grob3, grob4):
        gt = [
            gtable_col("test1", [grob1, grob2, grob3], z=[0.9, 0.3, 0.6]),
            gtable_col("test2", [grob4, grob1, grob2], z=[1, 3, 2]),
            gtable_col("test3", [grob3, grob4, grob1], z=[2, 3, 1]),
        ]

        gt1 = z_arrange_gtables(gt, [3, 2, 1])
        assert gt1[0].layout["z"] == [9, 7, 8]
        assert gt1[1].layout["z"] == [4, 6, 5]
        assert gt1[2].layout["z"] == [2, 3, 1]

    def test_with_cbind(self, grob1, grob2, grob3, grob4):
        gt = [
            gtable_col("test1", [grob1, grob2, grob3], z=[0.9, 0.3, 0.6]),
            gtable_col("test2", [grob4, grob1, grob2], z=[1, 3, 2]),
            gtable_col("test3", [grob3, grob4, grob1], z=[2, 3, 1]),
        ]

        gt1 = cbind_gtable(gt[0], gt[1], gt[2], z=[3, 2, 1])
        assert gt1.layout["z"] == [9, 7, 8, 4, 6, 5, 2, 3, 1]

    def test_with_rbind(self, grob1, grob2, grob3, grob4):
        gt = [
            gtable_col("test1", [grob1, grob2, grob3], z=[0.9, 0.3, 0.6]),
            gtable_col("test2", [grob4, grob1, grob2], z=[1, 3, 2]),
            gtable_col("test3", [grob3, grob4, grob1], z=[2, 3, 1]),
        ]

        gt1 = rbind_gtable(gt[0], gt[1], gt[2], z=[3, 2, 1])
        assert gt1.layout["z"] == [9, 7, 8, 4, 6, 5, 2, 3, 1]
