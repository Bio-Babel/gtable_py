"""Z-order normalisation for gtable grob layouts."""

from __future__ import annotations

from typing import TYPE_CHECKING, List, Optional

from ._utils import new_layout

if TYPE_CHECKING:
    from ._gtable import Gtable

__all__: list[str] = []


def z_normalise(x: "Gtable", i: int = 1) -> "Gtable":
    """Normalise z values to sequential integers starting at *i*.

    Ties are broken by first occurrence (stable sort).

    Parameters
    ----------
    x : Gtable
        A gtable object.
    i : int
        Starting z value.

    Returns
    -------
    Gtable
        Gtable with normalised z values.
    """
    import copy
    x = copy.copy(x)
    layout = x._layout
    z_vals = layout["z"]
    if not z_vals:
        return x
    # rank with first-occurrence tie breaking
    ranked = _rank_first(z_vals)
    layout["z"] = [r + i - 1 for r in ranked]
    x._layout = layout
    return x


def z_arrange_gtables(
    gtables: List["Gtable"],
    z: List[float],
) -> List["Gtable"]:
    """Arrange z values across multiple gtables.

    Each gtable's z values are normalised to sequential integers,
    ordered according to *z*.

    Parameters
    ----------
    gtables : list of Gtable
        Gtable objects.
    z : list of float
        Relative z ordering.

    Returns
    -------
    list of Gtable
        Gtables with adjusted z values.
    """
    if len(gtables) != len(z):
        raise ValueError("`gtables` and `z` must be the same length")

    import copy
    gtables = [copy.copy(g) for g in gtables]
    zmax = 0
    # Process in z-order
    for idx in _argsort(z):
        layout = gtables[idx]._layout
        if len(layout["t"]) > 0:
            gtables[idx] = z_normalise(gtables[idx], zmax + 1)
            zmax = max(gtables[idx]._layout["z"])
    return gtables


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _rank_first(values: List[float]) -> List[int]:
    """Rank values with first-occurrence tie-breaking (1-based).

    Parameters
    ----------
    values : list of float
        Values to rank.

    Returns
    -------
    list of int
        1-based ranks.
    """
    indexed = sorted(range(len(values)), key=lambda i: (values[i], i))
    ranks = [0] * len(values)
    for rank, orig_idx in enumerate(indexed, start=1):
        ranks[orig_idx] = rank
    return ranks


def _argsort(values: List[float]) -> List[int]:
    """Return indices that would sort *values*.

    Parameters
    ----------
    values : list of float
        Values to sort.

    Returns
    -------
    list of int
        Indices.
    """
    return sorted(range(len(values)), key=lambda i: values[i])
