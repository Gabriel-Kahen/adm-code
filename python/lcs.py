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

"""lcs.c translated to Python; indices start at zero."""

if __name__ == "__main__" and not __package__:
    import sys
    from pathlib import Path

    sys.path[0] = str(Path(__file__).resolve().parent.parent)
    __package__ = "python"


def longest_common_subsequence(first: str, second: str) -> str:
    """One maximum-length common subsequence, O(mn) time and space."""
    lengths = [[0] * (len(second) + 1) for _ in range(len(first) + 1)]
    for row in range(1, len(first) + 1):
        for column in range(1, len(second) + 1):
            if first[row - 1] == second[column - 1]:
                lengths[row][column] = lengths[row - 1][column - 1] + 1
            else:
                lengths[row][column] = max(lengths[row - 1][column], lengths[row][column - 1])
    result = []
    row, column = len(first), len(second)
    while row and column:
        if first[row - 1] == second[column - 1]:
            result.append(first[row - 1])
            row -= 1
            column -= 1
        elif lengths[row - 1][column] >= lengths[row][column - 1]:
            row -= 1
        else:
            column -= 1
    return "".join(reversed(result))


if __name__ == "__main__":
    import sys

    first, second = sys.stdin.read().split() or ["banana", "ananas"]
    print(longest_common_subsequence(first, second))
