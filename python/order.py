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

"""Direct translation of order.c; data structures and indexing match C."""

if __name__ == "__main__" and not __package__:
    import sys
    from pathlib import Path
    sys.path[0] = str(Path(__file__).resolve().parent.parent)
    __package__ = "python"
    sys.modules[__package__ + "." + Path(__file__).stem] = sys.modules[__name__]

from ._c import printf


def process(i, j):
    printf("(%d,%d)\n", i, j)


def row_major(n, m):
    # j: counters
    i = 1
    while (i <= n):
        j = 1
        while (j <= m):
            process(i, j)
            j += 1
        i += 1


def column_major(n, m):
    # j: counters
    j = 1
    while (j <= m):
        i = 1
        while (i <= n):
            process(i, j)
            i += 1
        j += 1


def snake_order(n, m):
    # j: counters
    i = 1
    while (i <= n):
        j = 1
        while (j <= m):
            process(i, j + (m + 1 - 2 * j) * ((i + 1) % 2))
            j += 1
        i += 1


def diagonal_order(n, m):
    d = 1
    while (d <= ((n + m) - 1)):
        first = max(1, ((d + 1) - m))
        last = min(n, d)
        row = first
        while (row <= last):
            process(row, ((d + 1) - row))
            row += 1
        d += 1


def main():
    printf("row_major\n")
    row_major(5, 5)
    printf("\ncolumn_major\n")
    column_major(3, 3)
    printf("\nsnake_order\n")
    snake_order(5, 5)
    printf("\ndiagonal_order\n")
    diagonal_order(3, 4)
    printf("\ndiagonal_order\n")
    diagonal_order(4, 3)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
