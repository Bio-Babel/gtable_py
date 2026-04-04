"""Filter grobs in a gtable by name."""

from __future__ import annotations

import copy
import re
from typing import Optional

from ._gtable import Gtable
from ._trim import gtable_trim
from ._utils import layout_nrow, layout_subset

__all__ = ["gtable_filter"]


def gtable_filter(
    x: Gtable,
    pattern: str,
    fixed: bool = False,
    trim: bool = True,
    invert: bool = False,
) -> Gtable:
    """Filter cells by name.

    Parameters
    ----------
    x : Gtable
        Target table.
    pattern : str
        Pattern to match against grob names.
    fixed : bool
        If True, use literal string matching instead of regex.
    trim : bool
        If True, trim empty rows/columns after filtering.
    invert : bool
        If True, remove matching grobs instead of keeping them.

    Returns
    -------
    Gtable
        Filtered table.
    """
    layout = x._layout
    names = layout["name"]

    if fixed:
        matches = [pattern in n for n in names]
    else:
        matches = [bool(re.search(pattern, n)) for n in names]

    if invert:
        matches = [not m for m in matches]

    result = copy.copy(x)
    result._layout = layout_subset(copy.deepcopy(x._layout), matches)
    result._grobs = [g for g, m in zip(x._grobs, matches) if m]

    if trim:
        result = gtable_trim(result)

    return result
