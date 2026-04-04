"""Tests for Gtable.__getitem__ — ported from test-subsetting.R."""

import pytest
from grid_py import Unit, circle_grob, lines_grob, polygon_grob, rect_grob

from gtable_py import Gtable, gtable_add_grob, gtable_matrix


def make_gt(grobmat, rows, cols):
    """Create a gtable from a matrix using specific rows/cols.

    Parameters
    ----------
    grobmat : list of list
        Matrix of grobs.
    rows : list of int
        Row indices (0-based).
    cols : list of int
        Column indices (0-based).
    """
    sub_grobs = [[grobmat[r][c] for c in cols] for r in rows]
    # Heights/widths use 1-based values from R (the row/col number + 1)
    return gtable_matrix(
        "test",
        sub_grobs,
        widths=Unit([c + 1 for c in cols], "cm"),
        heights=Unit([r + 1 for r in rows], "cm"),
    )


@pytest.fixture
def base():
    b = Gtable(
        Unit([1, 1, 1], "null"),
        Unit([1, 1, 1], "null"),
    )
    b.dimnames = (["A", "B", "C"], ["a", "b", "c"])
    return b


class TestDimensionsAfterSubset:
    def test_full_range(self, base):
        assert base[:, :].shape == (3, 3)
        assert base[0:3, 0:3].shape == (3, 3)

    def test_single_cell(self, base):
        assert base[0, 0].shape == (1, 1)

    def test_subrange(self, base):
        assert base[0:2, 1:3].shape == (2, 2)


class TestGrobMovement:
    def test_grob_moved_to_correct_location(self, base):
        rect = rect_grob()
        mid = gtable_add_grob(base, rect, 2, 2)

        def tlbr(gt):
            layout = gt.layout
            return [layout["t"][0], layout["l"][0], layout["b"][0], layout["r"][0]]

        # Subsetting [2,2] (0-based: [1,1]) should place grob at (1,1,1,1)
        assert tlbr(mid[1, 1]) == [1, 1, 1, 1]
        assert tlbr(mid[1:3, 1:3]) == [1, 1, 1, 1]

        # Subsetting [1:2, 1:2] (0-based: [0:2, 0:2]) keeps grob at relative pos
        assert tlbr(mid[0:2, 0:2]) == [2, 2, 2, 2]
        assert tlbr(mid[0:3, 0:3]) == [2, 2, 2, 2]


class TestSpanningGrobsKept:
    def test_spanning_row_grob(self, base):
        rect = rect_grob()
        # row spanning: grob at row 2, cols 1-3
        row = gtable_add_grob(base, rect, t=2, l=1, r=3)

        # Remove col 2 (0-based: drop index 1)
        # In R: row[, -2] — keep cols 1,3
        sub = row[[0, 2], slice(None)]  # all rows, cols 0 and 2
        # Actually we need to keep all rows and just drop col index 1
        sub2 = row[:, [0, 2]]
        assert len(sub2) == 1

    def test_spanning_col_grob(self, base):
        rect = rect_grob()
        # col spanning: grob at col 2, rows 1-3
        col = gtable_add_grob(base, rect, t=1, l=2, b=3)

        # Remove row 2 (0-based: drop index 1)
        sub = col[[0, 2], :]
        assert len(sub) == 1


class TestSingleCellGrobs:
    def test_contiguous(self):
        g1, g2, g3, g4, g5, g6 = (
            rect_grob(),
            circle_grob(),
            polygon_grob(),
            lines_grob(),
            circle_grob(),
            rect_grob(),
        )
        # 2x3 matrix: [[g1,g3,g5],[g2,g4,g6]] (column-major like R)
        grobmat = [[g1, g3, g5], [g2, g4, g6]]
        gt = make_gt(grobmat, [0, 1], [0, 1, 2])

        # Full indexing should preserve
        assert gt[:, :].shape == (2, 3)
        assert gt[0:2, 0:3].shape == (2, 3)
        assert len(gt[:, :]) == 6

        # Single cell
        sub = gt[0, 0]
        assert sub.shape == (1, 1)
        assert len(sub) == 1

    def test_non_contiguous(self):
        g1, g2, g3, g4, g5, g6 = (
            rect_grob(),
            circle_grob(),
            polygon_grob(),
            lines_grob(),
            circle_grob(),
            rect_grob(),
        )
        grobmat = [[g1, g3, g5], [g2, g4, g6]]
        gt = make_gt(grobmat, [0, 1], [0, 1, 2])

        # Non-contiguous columns: keep cols 0 and 2
        sub = gt[0, [0, 2]]
        assert sub.shape == (1, 2)
        assert len(sub) == 2


class TestIndexingWithNames:
    def test_name_based(self):
        g1, g2, g3, g4, g5, g6 = (
            rect_grob(),
            circle_grob(),
            polygon_grob(),
            lines_grob(),
            circle_grob(),
            rect_grob(),
        )
        grobmat = [[g1, g3, g5], [g2, g4, g6]]
        gt = make_gt(grobmat, [0, 1], [0, 1, 2])
        gt.dimnames = (["a", "b"], ["x", "y", "z"])

        # Name-based indexing should work
        sub_name = gt[["a"], ["x", "y"]]
        sub_idx = gt[0, 0:2]
        assert sub_name.shape == sub_idx.shape
        assert len(sub_name) == len(sub_idx)


class TestIndexingErrors:
    def test_non_increasing(self, base):
        with pytest.raises(IndexError):
            base[[1, 0], :]
        with pytest.raises(IndexError):
            base[:, [1, 0]]
        with pytest.raises(IndexError):
            base[[1, 1], :]

    def test_valid_passes(self, base):
        # Should not raise
        base[0:2, 0:2]
