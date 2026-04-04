"""Add padding around a gtable."""

from __future__ import annotations

from grid_py import Unit

from ._add_rows_cols import gtable_add_cols, gtable_add_rows
from ._gtable import Gtable

__all__ = ["gtable_add_padding"]


def gtable_add_padding(x: Gtable, padding: Unit) -> Gtable:
    """Add padding around the table edges.

    Parameters
    ----------
    x : Gtable
        Target table.
    padding : Unit
        Padding amounts. Recycled to length 4: top, right, bottom, left.

    Returns
    -------
    Gtable
        Table with padding added.
    """
    # Recycle to length 4
    p_len = len(padding)
    if p_len == 0:
        return x

    # Get individual padding values (top, right, bottom, left)
    indices = [i % p_len for i in range(4)]
    pad = [padding[idx:idx + 1] for idx in indices]

    x = gtable_add_rows(x, pad[0], pos=0)     # top
    x = gtable_add_cols(x, pad[1], pos=-1)     # right
    x = gtable_add_rows(x, pad[2], pos=-1)     # bottom
    x = gtable_add_cols(x, pad[3], pos=0)      # left
    return x
