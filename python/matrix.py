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

"""matrix.c translated to Python; indices start at zero."""

if __name__ == "__main__" and not __package__:
    import sys
    from pathlib import Path

    sys.path[0] = str(Path(__file__).resolve().parent.parent)
    __package__ = "python"


def matrix_multiply(first: list[list[int]], second: list[list[int]]) -> list[list[int]]:
    """Dense rectangular multiplication in O(rows*inner*columns)."""
    if not first or not second or not first[0] or not second[0]:
        raise ValueError("matrices must have positive dimensions")
    inner, columns = len(second), len(second[0])
    if any(len(row) != inner for row in first) or any(len(row) != columns for row in second):
        raise ValueError("incompatible or ragged matrix dimensions")
    result = [[0] * columns for _ in first]
    for row in range(len(first)):
        for shared in range(inner):
            for column in range(columns):
                result[row][column] += first[row][shared] * second[shared][column]
    return result


if __name__ == "__main__":
    import sys

    print(matrix_multiply([[1, 2]], [[3], [4]]))
