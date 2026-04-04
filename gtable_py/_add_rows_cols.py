"""Add rows and columns to a gtable."""

from __future__ import annotations

import copy
from typing import Union

from grid_py import Unit

from ._gtable import Gtable
from ._utils import check_gtable, insert_unit, neg_to_pos

__all__ = ["gtable_add_rows", "gtable_add_cols"]


def gtable_add_rows(
    x: Gtable,
    heights: Unit,
    pos: int = -1,
) -> Gtable:
    """Insert new rows at a given position.

    If rows are added in the middle of a spanning grob, the grob
    continues to span. If added above or below, it does not.

    Parameters
    ----------
    x : Gtable
        Target table.
    heights : Unit
        Heights for the new rows.
    pos : int
        Insert after this position (1-based). ``0`` adds at top,
        ``-1`` adds at bottom.

    Returns
    -------
    Gtable
        Table with new rows.
    """
    check_gtable(x)
    if not isinstance(pos, (int, float)):
        raise TypeError("`pos` must be an integer")
    pos = int(pos)
    n = len(heights)
    h_len = len(x.heights) if x.heights is not None else 0
    pos = neg_to_pos(pos, h_len)

    result = copy.copy(x)
    result._heights = insert_unit(x.heights, heights, pos)
    layout = copy.deepcopy(x._layout)
    for i in range(len(layout["t"])):
        if layout["t"][i] > pos:
            layout["t"][i] += n
        if layout["b"][i] > pos:
            layout["b"][i] += n
    result._layout = layout
    return result


def gtable_add_cols(
    x: Gtable,
    widths: Unit,
    pos: int = -1,
) -> Gtable:
    """Insert new columns at a given position.

    If columns are added in the middle of a spanning grob, the grob
    continues to span. If added left or right, it does not.

    Parameters
    ----------
    x : Gtable
        Target table.
    widths : Unit
        Widths for the new columns.
    pos : int
        Insert after this position (1-based). ``0`` adds at left,
        ``-1`` adds at right.

    Returns
    -------
    Gtable
        Table with new columns.
    """
    check_gtable(x)
    if not isinstance(pos, (int, float)):
        raise TypeError("`pos` must be an integer")
    pos = int(pos)
    n = len(widths)
    w_len = len(x.widths) if x.widths is not None else 0
    pos = neg_to_pos(pos, w_len)

    result = copy.copy(x)
    result._widths = insert_unit(x.widths, widths, pos)
    layout = copy.deepcopy(x._layout)
    for i in range(len(layout["l"])):
        if layout["l"][i] > pos:
            layout["l"][i] += n
        if layout["r"][i] > pos:
            layout["r"][i] += n
    result._layout = layout
    return result
