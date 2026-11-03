# Copyright 2003-2020 by Steven S. Skiena; all rights reserved.
# Permission is granted for use in non-commerical applications
# provided this copyright notice remains intact and unchanged.
#
# These programs appear in my books:
#
# "The Algorithm Design Manual" by Steven Skiena, second edition, Springer,
# London 2008.  See out website www.algorist.com for additional information
# or https://www.amazon.com/exec/obidos/ASIN/1848000693/thealgorith01-20
#
# "Programming Challenges: The Programming Contest Training Manual"
# by Steven Skiena and Miguel Revilla, Springer-Verlag, New York 2003.
# See our website www.programming-challenges.com for additional information,
# or https://www.amazon.com/exec/obidos/ASIN/0387001638/thealgorithmrepo/

"""plates.c translated to Python; indices start at zero."""

if __name__ == "__main__" and not __package__:
    import sys
    from pathlib import Path

    sys.path[0] = str(Path(__file__).resolve().parent.parent)
    __package__ = "python"

import math

from .geometry import Point, _finite


def _packing_dimensions(width: float, height: float, radius: float) -> None:
    _finite(width, height, radius)
    if width <= 0 or height <= 0 or radius <= 0:
        raise ValueError("packing dimensions and radius must be positive")


def dense_layers(width: float, height: float, radius: float) -> int:
    _packing_dimensions(width, height, radius)
    if width < 2 * radius or height < 2 * radius:
        return 0
    return 1 + math.floor((height - 2 * radius) / (math.sqrt(3) * radius))


def plates_per_row(row: int, width: float, radius: float) -> int:
    _finite(width, radius)
    if row < 0 or width <= 0 or radius <= 0:
        raise ValueError("invalid packing row")
    full = math.floor(width / (2 * radius))
    if full == 0:
        return 0
    return full if row % 2 == 0 or width / (2 * radius) - full >= 0.5 else full - 1


def grid_plates(width: float, height: float, radius: float) -> int:
    _packing_dimensions(width, height, radius)
    return math.floor(height / (2 * radius)) * plates_per_row(0, width, radius)


def dense_plates(width: float, height: float, radius: float) -> int:
    layers = dense_layers(width, height, radius)
    return (layers + 1) // 2 * plates_per_row(0, width, radius) + layers // 2 * plates_per_row(
        1, width, radius
    )


def packing(width: float, height: float, radius: float) -> tuple[int, int]:
    """Best row-based grid and triangular-lattice counts across both box orientations."""
    return max(grid_plates(width, height, radius), grid_plates(height, width, radius)), max(
        dense_plates(width, height, radius), dense_plates(height, width, radius)
    )


def hex_to_cartesian(row: float, diagonal: float, radius: float) -> Point:
    _finite(row, diagonal, radius)
    if radius <= 0:
        raise ValueError("radius must be positive")
    result = radius * row + 2 * radius * diagonal, math.sqrt(3) * radius * row
    _finite(*result)
    return result


def cartesian_to_hex(x: float, y: float, radius: float) -> Point:
    _finite(x, y, radius)
    if radius <= 0:
        raise ValueError("radius must be positive")
    row = y / (math.sqrt(3) * radius)
    result = row, (x - radius * row) / (2 * radius)
    _finite(*result)
    return result


def array_to_hex(row: int, column: int) -> tuple[int, int]:
    return row, column - row // 2


def hex_to_array(row: int, diagonal: int) -> tuple[int, int]:
    return row, diagonal + row // 2


def plates_on_top(row: int, diagonal: int, width: float, height: float, radius: float) -> int:
    """Count the triangular dependency cone above one plate in a fixed packing."""
    layers = dense_layers(width, height, radius)
    _, column = hex_to_array(row, diagonal)
    if not 0 <= row < layers or not 0 <= column < plates_per_row(row, width, radius):
        raise ValueError("plate lies outside packing")
    result = 0
    for higher in range(row + 1, layers):
        left = max(0, hex_to_array(higher, diagonal - (higher - row))[1])
        right = min(plates_per_row(higher, width, radius) - 1, hex_to_array(higher, diagonal)[1])
        result += max(0, right - left + 1)
    return result


if __name__ == "__main__":
    import sys

    width, height, radius = map(float, sys.stdin.read().split() or ["4", "4", "1"])
    print(packing(width, height, radius))
