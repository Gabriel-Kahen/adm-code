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

"""permutations.c translated to Python; indices start at zero."""

if __name__ == "__main__" and not __package__:
    import sys
    from pathlib import Path

    sys.path[0] = str(Path(__file__).resolve().parent.parent)
    __package__ = "python"

from .backtrack import backtrack


def permutations(size: int) -> list[list[int]]:
    """All permutations of 0..n-1, O(n*n!) output; restricted to n<=9."""
    if not 0 <= size <= 9:
        raise ValueError("permutations require 0 <= n <= 9")
    result = []
    backtrack(
        [],
        lambda prefix: len(prefix) == size,
        lambda prefix: (value for value in range(size) if value not in prefix),
        lambda prefix: result.append(list(prefix)) is None,
    )
    return result


if __name__ == "__main__":
    import sys

    print(permutations(int(sys.stdin.read().strip() or "3")))
