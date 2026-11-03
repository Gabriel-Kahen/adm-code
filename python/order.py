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

"""order.c translated to Python; indices start at zero."""

if __name__ == "__main__" and not __package__:
    import sys
    from pathlib import Path

    sys.path[0] = str(Path(__file__).resolve().parent.parent)
    __package__ = "python"


def grid_order(method: str, rows: int, columns: int) -> list[list[int]]:
    """Visit every cell once, with row/column/snake/diagonal order; O(rows*columns)."""
    if rows < 0 or columns < 0:
        raise ValueError("negative grid dimensions")
    if method == "row":
        return [[row, column] for row in range(rows) for column in range(columns)]
    if method == "column":
        return [[row, column] for column in range(columns) for row in range(rows)]
    if method == "snake":
        return [
            [row, column if row % 2 == 0 else columns - 1 - column]
            for row in range(rows)
            for column in range(columns)
        ]
    if method == "diagonal":
        return [
            [row, diagonal - row]
            for diagonal in range(rows + columns - 1)
            for row in range(max(0, diagonal - columns + 1), min(rows - 1, diagonal) + 1)
        ]
    raise ValueError("unknown grid order")


if __name__ == "__main__":
    import sys

    for method in ("row", "column", "snake", "diagonal"):
        print(method, grid_order(method, 3, 4))
