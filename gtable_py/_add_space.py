"""Add spacing between rows/columns in a gtable."""

from __future__ import annotations

from grid_py import Unit

from ._add_rows_cols import gtable_add_cols, gtable_add_rows
from ._gtable import Gtable
from ._utils import check_gtable

__all__ = ["gtable_add_col_space", "gtable_add_row_space"]


def gtable_add_col_space(x: Gtable, width: Unit) -> Gtable:
    """Add spacing between columns.

    Parameters
    ----------
    x : Gtable
        Target table.
    width : Unit
        Width(s) of spacing. Length 1 or ``ncol - 1``.

    Returns
    -------
    Gtable
        Table with column spacing added.
    """
    check_gtable(x)
    n = (len(x.widths) if x.widths is not None else 0) - 1
    if n == 0:
        return x

    w_len = len(width)
    if w_len != 1 and w_len != n:
        raise ValueError("`width` must be of length 1 or ncol - 1")

    # Replicate if length 1
    if w_len == 1:
        widths = [width] * n
    else:
        widths = [width[i:i + 1] for i in range(n)]

    for i in reversed(range(n)):
        x = gtable_add_cols(x, widths[i], pos=i + 1)

    return x


def gtable_add_row_space(x: Gtable, height: Unit) -> Gtable:
    """Add spacing between rows.

    Parameters
    ----------
    x : Gtable
        Target table.
    height : Unit
        Height(s) of spacing. Length 1 or ``nrow - 1``.

    Returns
    -------
    Gtable
        Table with row spacing added.
    """
    check_gtable(x)
    n = (len(x.heights) if x.heights is not None else 0) - 1
    if n == 0:
        return x

    h_len = len(height)
    if h_len != 1 and h_len != n:
        raise ValueError("`height` must be of length 1 or nrow - 1")

    if h_len == 1:
        heights = [height] * n
    else:
        heights = [height[i:i + 1] for i in range(n)]

    for i in reversed(range(n)):
        x = gtable_add_rows(x, heights[i], pos=i + 1)

    return x
