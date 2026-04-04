"""Add grobs to a gtable."""

from __future__ import annotations

import copy
import math
from typing import List, Optional, Union

from grid_py import Grob, is_grob

from ._gtable import Gtable
from ._utils import check_gtable, len_same_or_1, neg_to_pos

__all__ = ["gtable_add_grob"]


def gtable_add_grob(
    x: Gtable,
    grobs: Union[Grob, List[Grob]],
    t: Union[int, List[int]],
    l: Union[int, List[int]],
    b: Optional[Union[int, List[int]]] = None,
    r: Optional[Union[int, List[int]]] = None,
    z: Union[float, List[float]] = math.inf,
    clip: Union[str, List[str]] = "on",
    name: Optional[Union[str, List[str]]] = None,
) -> Gtable:
    """Add grobs to a gtable.

    Positions are **1-based** (matching R semantics).

    Parameters
    ----------
    x : Gtable
        Target table.
    grobs : Grob or list of Grob
        Grob(s) to add.
    t : int or list of int
        Top row(s), 1-based.
    l : int or list of int
        Left column(s), 1-based.
    b : int or list of int or None
        Bottom row(s), 1-based. Defaults to *t*.
    r : int or list of int or None
        Right column(s), 1-based. Defaults to *l*.
    z : float or list of float
        Z-order. ``inf`` places above existing; ``-inf`` below.
    clip : str or list of str
        Clipping: ``"on"``, ``"off"``, or ``"inherit"``.
    name : str or list of str or None
        Grob name(s). Defaults to table name.

    Returns
    -------
    Gtable
        Table with grobs added.
    """
    check_gtable(x)
    if is_grob(grobs):
        grobs = [grobs]
    if not isinstance(grobs, (list, tuple)):
        raise TypeError("`grobs` must be a Grob or list of Grobs")
    for g in grobs:
        if not is_grob(g):
            raise TypeError("`grobs` must be a Grob or list of Grobs")

    n_grobs = len(grobs)
    if b is None:
        b = t
    if r is None:
        r = l
    if name is None:
        name = x.name

    # Handle boolean clip
    if isinstance(clip, bool):
        clip = "on" if clip else "off"
    if isinstance(clip, list):
        clip = ["on" if c else "off" if isinstance(c, bool) else c for c in clip]

    # Ensure lists
    def _to_list(v, n):
        if isinstance(v, (list, tuple)):
            return list(v)
        return [v] * n

    t_list = _to_list(t, n_grobs)
    l_list = _to_list(l, n_grobs)
    b_list = _to_list(b, n_grobs)
    r_list = _to_list(r, n_grobs)
    z_list = _to_list(z, n_grobs)
    clip_list = _to_list(clip, n_grobs)
    name_list = _to_list(name, n_grobs)

    # Validate lengths
    for lst, lbl in [
        (t_list, "t"), (l_list, "l"), (b_list, "b"),
        (r_list, "r"), (z_list, "z"), (clip_list, "clip"),
        (name_list, "name"),
    ]:
        if not len_same_or_1(lst, n_grobs):
            raise ValueError(
                f"All inputs must have length 1 or same length as grobs, "
                f"but `{lbl}` has length {len(lst)}"
            )
        # Replicate length-1 to n_grobs
        if len(lst) == 1 and n_grobs > 1:
            lst *= n_grobs

    # Ensure lists are the right length after replication
    z_list = (z_list * n_grobs)[:n_grobs]

    # Compute z values
    layout = x._layout
    existing_z = layout["z"]
    finite_new_z = [zv for zv in z_list if not math.isinf(zv)]
    all_z = existing_z + finite_new_z

    if not all_z:
        zmin, zmax = 1, 0
    else:
        zmin = min(all_z)
        zmax = max(all_z)

    neg_inf_count = sum(1 for zv in z_list if zv == -math.inf)
    pos_inf_count = sum(1 for zv in z_list if zv == math.inf)

    neg_inf_idx = 0
    pos_inf_idx = 0
    for i in range(len(z_list)):
        if z_list[i] == -math.inf:
            z_list[i] = zmin - (neg_inf_count - neg_inf_idx)
            neg_inf_idx += 1
        elif z_list[i] == math.inf:
            pos_inf_idx += 1
            z_list[i] = zmax + pos_inf_idx

    x_row = x.nrow
    x_col = x.ncol

    t_list = [neg_to_pos(v, x_row) for v in t_list]
    b_list = [neg_to_pos(v, x_row) for v in b_list]
    l_list = [neg_to_pos(v, x_col) for v in l_list]
    r_list = [neg_to_pos(v, x_col) for v in r_list]

    result = copy.copy(x)
    result._grobs = list(x._grobs) + list(grobs)
    result._layout = {
        "t": layout["t"] + t_list,
        "l": layout["l"] + l_list,
        "b": layout["b"] + b_list,
        "r": layout["r"] + r_list,
        "z": layout["z"] + z_list,
        "clip": layout["clip"] + clip_list,
        "name": layout["name"] + name_list,
    }

    return result
