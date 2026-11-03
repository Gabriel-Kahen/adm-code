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

"""binomial.c translated to Python; indices start at zero."""

if __name__ == "__main__" and not __package__:
    import sys
    from pathlib import Path

    sys.path[0] = str(Path(__file__).resolve().parent.parent)
    __package__ = "python"


def binomial(n: int, k: int) -> int:
    """Pascal-row DP, O(n min(k,n-k)) integer operations and O(min(k,n-k)) space."""
    if n < 0 or not 0 <= k <= n:
        raise ValueError("require 0 <= k <= n")
    k = min(k, n - k)
    row = [1] + [0] * k
    for size in range(1, n + 1):
        for column in range(min(size, k), 0, -1):
            row[column] += row[column - 1]
    return row[k]


if __name__ == "__main__":
    import sys

    n, k = map(int, (sys.stdin.read().split() or ["10", "5"]))
    print(binomial(n, k))
