"""Trim empty rows and columns from a gtable."""

from __future__ import annotations

import copy

from grid_py import Unit

from ._gtable import Gtable
from ._utils import check_gtable, layout_nrow

__all__ = ["gtable_trim"]


def gtable_trim(x: Gtable) -> Gtable:
    """Remove empty rows and columns.

    Parameters
    ----------
    x : Gtable
        Target table.

    Returns
    -------
    Gtable
        Trimmed table.
    """
    check_gtable(x)
    if len(x) == 0:
        return Gtable(respect=x.respect, name=x.name, vp=x.vp)

    layout = x._layout

    # Find used row/col range (1-based)
    all_l = layout["l"]
    all_r = layout["r"]
    all_t = layout["t"]
    all_b = layout["b"]

    w_min = min(min(all_l), min(all_r))
    w_max = max(max(all_l), max(all_r))
    h_min = min(min(all_t), min(all_b))
    h_max = max(max(all_t), max(all_b))

    result = copy.copy(x)

    # Subset widths and heights (1-based range → 0-based slicing)
    from ._gtable import _unit_subset
    result._widths = x.widths[w_min - 1:w_max]
    result._heights = x.heights[h_min - 1:h_max]

    # Adjust layout positions
    new_layout = copy.deepcopy(x._layout)
    for i in range(layout_nrow(new_layout)):
        new_layout["l"][i] = new_layout["l"][i] - w_min + 1
        new_layout["r"][i] = new_layout["r"][i] - w_min + 1
        new_layout["t"][i] = new_layout["t"][i] - h_min + 1
        new_layout["b"][i] = new_layout["b"][i] - h_min + 1

    result._layout = new_layout
    result._grobs = list(x._grobs)

    return result
