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

"""8-queens.c translated to Python; indices start at zero."""

if __name__ == "__main__" and not __package__:
    import sys
    from pathlib import Path

    sys.path[0] = str(Path(__file__).resolve().parent.parent)
    __package__ = "python"


def queens(size: int) -> int:
    """Count n-queens solutions by bitmask backtracking; restricted to n<=15."""
    if not 0 <= size <= 15:
        raise ValueError("queens requires 0 <= n <= 15")
    full = (1 << size) - 1

    def count(columns: int, down: int, up: int) -> int:
        if columns == full:
            return 1
        available = full & ~(columns | down | up)
        result = 0
        while available:
            bit = available & -available
            available -= bit
            result += count(columns | bit, ((down | bit) << 1) & full, (up | bit) >> 1)
        return result

    return count(0, 0, 0)


if __name__ == "__main__":
    import sys

    print(queens(int(sys.stdin.read().strip() or "8")))
