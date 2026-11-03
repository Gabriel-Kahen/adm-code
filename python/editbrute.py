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

"""editbrute.c translated to Python; indices start at zero."""

if __name__ == "__main__" and not __package__:
    import sys
    from pathlib import Path

    sys.path[0] = str(Path(__file__).resolve().parent.parent)
    __package__ = "python"


def edit_distance_brute(first: str, second: str) -> int:
    """Exponential recurrence without memoization; restricted to total length <= 18."""
    if len(first) + len(second) > 18:
        raise ValueError("brute edit distance requires combined length <= 18")

    def recurse(row: int, column: int) -> int:
        if row == 0 or column == 0:
            return max(row, column)
        return min(
            recurse(row - 1, column - 1) + (first[row - 1] != second[column - 1]),
            recurse(row - 1, column) + 1,
            recurse(row, column - 1) + 1,
        )

    return recurse(len(first), len(second))


if __name__ == "__main__":
    import sys

    first, second = sys.stdin.read().split() or ["cat", "cut"]
    print(edit_distance_brute(first, second))
