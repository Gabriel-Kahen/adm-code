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

"""sentinel.c translated to Python; indices start at zero."""

if __name__ == "__main__" and not __package__:
    import sys
    from pathlib import Path

    sys.path[0] = str(Path(__file__).resolve().parent.parent)
    __package__ = "python"

from typing import TypeVar

T = TypeVar("T")


def sentinel_insert(values: list[T], value: T) -> list[T]:
    """Insert into a sorted array using value itself as a sentinel."""
    result = [value, *values, value]
    hole = len(result) - 1
    while value < result[hole - 1]:
        result[hole] = result[hole - 1]
        hole -= 1
    result[hole] = value
    return result[1:]


if __name__ == "__main__":
    import sys

    print(sentinel_insert([1, 2, 3], -1))
