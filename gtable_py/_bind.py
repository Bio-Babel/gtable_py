"""Row- and column-binding for gtables."""

from __future__ import annotations

import copy
import functools
from typing import List, Optional, Union

from grid_py import Unit

from ._gtable import Gtable
from ._utils import check_gtable, compare_unit, insert_unit, layout_nrow, new_layout
from ._z import z_arrange_gtables

__all__ = ["rbind_gtable", "cbind_gtable"]


def rbind_gtable(
    *args: Gtable,
    size: str = "max",
    z: Optional[List[float]] = None,
) -> Gtable:
    """Row-bind multiple gtables.

    Parameters
    ----------
    *args : Gtable
        Tables to bind vertically.
    size : str
        How to reconcile widths: ``"first"``, ``"last"``,
        ``"min"``, or ``"max"``.
    z : list of float or None
        Relative z-ordering of the input tables.

    Returns
    -------
    Gtable
        Combined table.
    """
    gtables = list(args)
    if z is not None:
        gtables = z_arrange_gtables(gtables, z)
    return functools.reduce(lambda x, y: _rbind_two(x, y, size=size), gtables)


def cbind_gtable(
    *args: Gtable,
    size: str = "max",
    z: Optional[List[float]] = None,
) -> Gtable:
    """Column-bind multiple gtables.

    Parameters
    ----------
    *args : Gtable
        Tables to bind horizontally.
    size : str
        How to reconcile heights: ``"first"``, ``"last"``,
        ``"min"``, or ``"max"``.
    z : list of float or None
        Relative z-ordering of the input tables.

    Returns
    -------
    Gtable
        Combined table.
    """
    gtables = list(args)
    if z is not None:
        gtables = z_arrange_gtables(gtables, z)
    return functools.reduce(lambda x, y: _cbind_two(x, y, size=size), gtables)


# ---------------------------------------------------------------------------
# Internal two-table operations
# ---------------------------------------------------------------------------


def _rbind_two(x: Gtable, y: Gtable, size: str = "max") -> Gtable:
    """Row-bind two gtables.

    Parameters
    ----------
    x, y : Gtable
        Tables to bind.
    size : str
        Width reconciliation strategy.

    Returns
    -------
    Gtable
        Combined table.
    """
    x_ncol = x.ncol
    y_ncol = y.ncol
    if x_ncol != y_ncol:
        raise ValueError("`x` and `y` must have the same number of columns")

    x_row = x.nrow
    y_row = y.nrow
    if x_row == 0:
        return copy.copy(y)
    if y_row == 0:
        return copy.copy(x)

    result = copy.copy(x)
    lay_x = x._layout
    lay_y = y._layout

    result._layout = {
        "t": lay_x["t"] + [v + x_row for v in lay_y["t"]],
        "l": lay_x["l"] + lay_y["l"],
        "b": lay_x["b"] + [v + x_row for v in lay_y["b"]],
        "r": lay_x["r"] + lay_y["r"],
        "z": lay_x["z"] + lay_y["z"],
        "clip": lay_x["clip"] + lay_y["clip"],
        "name": lay_x["name"] + lay_y["name"],
    }

    result._heights = insert_unit(x.heights, y.heights)
    result._rownames = _concat_names(x.rownames, y.rownames)

    if size not in ("first", "last", "min", "max"):
        raise ValueError(f"`size` must be 'first', 'last', 'min', or 'max', got {size!r}")
    if size == "first":
        result._widths = copy.copy(x.widths) if x.widths is not None else None
    elif size == "last":
        result._widths = copy.copy(y.widths) if y.widths is not None else None
    elif size == "min":
        result._widths = compare_unit(x.widths, y.widths, "min")
    else:
        result._widths = compare_unit(x.widths, y.widths, "max")

    result._grobs = list(x._grobs) + list(y._grobs)
    return result


def _cbind_two(x: Gtable, y: Gtable, size: str = "max") -> Gtable:
    """Column-bind two gtables.

    Parameters
    ----------
    x, y : Gtable
        Tables to bind.
    size : str
        Height reconciliation strategy.

    Returns
    -------
    Gtable
        Combined table.
    """
    x_nrow = x.nrow
    y_nrow = y.nrow
    if x_nrow != y_nrow:
        raise ValueError("`x` and `y` must have the same number of rows")

    x_col = x.ncol
    y_col = y.ncol
    if x_col == 0:
        return copy.copy(y)
    if y_col == 0:
        return copy.copy(x)

    result = copy.copy(x)
    lay_x = x._layout
    lay_y = y._layout

    result._layout = {
        "t": lay_x["t"] + lay_y["t"],
        "l": lay_x["l"] + [v + x_col for v in lay_y["l"]],
        "b": lay_x["b"] + lay_y["b"],
        "r": lay_x["r"] + [v + x_col for v in lay_y["r"]],
        "z": lay_x["z"] + lay_y["z"],
        "clip": lay_x["clip"] + lay_y["clip"],
        "name": lay_x["name"] + lay_y["name"],
    }

    result._widths = insert_unit(x.widths, y.widths)
    result._colnames = _concat_names(x.colnames, y.colnames)

    if size not in ("first", "last", "min", "max"):
        raise ValueError(f"`size` must be 'first', 'last', 'min', or 'max', got {size!r}")
    if size == "first":
        result._heights = copy.copy(x.heights) if x.heights is not None else None
    elif size == "last":
        result._heights = copy.copy(y.heights) if y.heights is not None else None
    elif size == "min":
        result._heights = compare_unit(x.heights, y.heights, "min")
    else:
        result._heights = compare_unit(x.heights, y.heights, "max")

    result._grobs = list(x._grobs) + list(y._grobs)
    return result


def _concat_names(
    a: Optional[List[str]],
    b: Optional[List[str]],
) -> Optional[List[str]]:
    """Concatenate two optional name lists.

    Parameters
    ----------
    a, b : list of str or None
        Name lists.

    Returns
    -------
    list of str or None
        Concatenated list, or None if both are None.
    """
    if a is None and b is None:
        return None
    return (a or []) + (b or [])
