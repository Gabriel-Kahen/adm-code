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

"""editdistance.c translated to Python; indices start at zero."""

if __name__ == "__main__" and not __package__:
    import sys
    from pathlib import Path

    sys.path[0] = str(Path(__file__).resolve().parent.parent)
    __package__ = "python"

from dataclasses import dataclass


@dataclass(frozen=True)
class EditResult:
    cost: int
    operations: str


def edit_distance(first: str, second: str) -> EditResult:
    """Unit-cost Levenshtein distance and M/S/I/D transformation, O(mn) time/space."""
    rows, columns = len(first) + 1, len(second) + 1
    costs = [[0] * columns for _ in range(rows)]
    for row in range(rows):
        costs[row][0] = row
    for column in range(columns):
        costs[0][column] = column
    for row in range(1, rows):
        for column in range(1, columns):
            costs[row][column] = min(
                costs[row - 1][column - 1] + (first[row - 1] != second[column - 1]),
                costs[row][column - 1] + 1,
                costs[row - 1][column] + 1,
            )
    operations = []
    row, column = len(first), len(second)
    while row or column:
        if (
            row
            and column
            and costs[row][column]
            == (costs[row - 1][column - 1] + (first[row - 1] != second[column - 1]))
        ):
            operations.append("M" if first[row - 1] == second[column - 1] else "S")
            row -= 1
            column -= 1
        elif column and costs[row][column] == costs[row][column - 1] + 1:
            operations.append("I")
            column -= 1
        else:
            operations.append("D")
            row -= 1
    return EditResult(costs[-1][-1], "".join(reversed(operations)))
