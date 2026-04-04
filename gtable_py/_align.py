"""Internal alignment utilities for gtables (not exported)."""

from __future__ import annotations

from typing import Any, Dict, List, Optional, Tuple

from grid_py import Unit

from ._bind import cbind_gtable, rbind_gtable
from ._gtable import Gtable

__all__: list[str] = []


def gtable_join(
    x: Gtable,
    y: Gtable,
    along: int = 1,
    join: str = "left",
) -> Gtable:
    """Join two gtables based on row/column names.

    Parameters
    ----------
    x, y : Gtable
        Tables to join.
    along : int
        1 = align rows (then cbind), 2 = align columns (then rbind).
    join : str
        ``"left"``, ``"right"``, ``"inner"``, or ``"outer"``.

    Returns
    -------
    Gtable
        Combined table.
    """
    aligned = gtable_align(x, y, along=along, join=join)
    if along == 1:
        return cbind_gtable(aligned[0], aligned[1])
    elif along == 2:
        return rbind_gtable(aligned[0], aligned[1])
    else:
        raise ValueError("`along` > 2 not implemented")


def gtable_align(
    x: Gtable,
    y: Gtable,
    along: int = 1,
    join: str = "left",
) -> Tuple[Gtable, Gtable]:
    """Align two gtables by dimension names.

    Parameters
    ----------
    x, y : Gtable
        Tables to align.
    along : int
        1 = rows, 2 = columns.
    join : str
        ``"left"``, ``"right"``, ``"inner"``, or ``"outer"``.

    Returns
    -------
    tuple of Gtable
        Aligned (x, y).
    """
    if join not in ("left", "right", "inner", "outer"):
        raise ValueError(f"`join` must be 'left', 'right', 'inner', or 'outer', got {join!r}")

    dn_x = x.dimnames[along - 1]
    dn_y = y.dimnames[along - 1]

    if dn_x is None or dn_y is None:
        raise ValueError("Both gtables must have names along the alignment dimension")

    if join == "left":
        idx = list(dn_x)
    elif join == "right":
        idx = list(dn_y)
    elif join == "inner":
        idx = [n for n in dn_x if n in set(dn_y)]
    else:  # outer
        seen = set()
        idx = []
        for n in list(dn_x) + list(dn_y):
            if n not in seen:
                idx.append(n)
                seen.add(n)

    return (
        gtable_reindex(x, idx, along),
        gtable_reindex(y, idx, along),
    )


def gtable_reindex(x: Gtable, index: List[str], along: int = 1) -> Gtable:
    """Reindex a gtable along a dimension.

    Parameters
    ----------
    x : Gtable
        Input table.
    index : list of str
        Target dimension names.
    along : int
        1 = rows, 2 = columns.

    Returns
    -------
    Gtable
        Reindexed table.
    """
    if along == 1:
        old_index = x.rownames
    elif along == 2:
        old_index = x.colnames
    else:
        raise ValueError("only 2d objects can be reindexed")

    if old_index is None:
        raise ValueError("`index` is None in the given dimension")

    if index == old_index:
        return x

    old_set = set(old_index)
    missing = [n for n in index if n not in old_set]

    if missing:
        if along == 1:
            spacer = Gtable(
                widths=Unit([0] * len(x.widths), "cm"),
                heights=Unit([0] * len(missing), "cm"),
                rownames=missing,
            )
            x = rbind_gtable(x, spacer, size="first")
        else:
            spacer = Gtable(
                heights=Unit([0] * len(x.heights), "cm"),
                widths=Unit([0] * len(missing), "cm"),
                colnames=missing,
            )
            x = cbind_gtable(x, spacer, size="first")

    # Reorder & subset
    if along == 1:
        return x[
            [x.rownames.index(n) for n in index],
            slice(None),
        ]
    else:
        return x[
            slice(None),
            [x.colnames.index(n) for n in index],
        ]
