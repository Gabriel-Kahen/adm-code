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

"""distance.c translated to Python; indices start at zero."""

if __name__ == "__main__" and not __package__:
    import sys
    from pathlib import Path

    sys.path[0] = str(Path(__file__).resolve().parent.parent)
    __package__ = "python"

import math


def euclidean_distance(first: list[float], second: list[float]) -> float:
    if len(first) != len(second):
        raise ValueError("coordinate dimensions differ")
    if not all(math.isfinite(value) for value in [*first, *second]):
        raise ValueError("coordinates must be finite")
    result = math.hypot(*(a - b for a, b in zip(first, second)))
    if not math.isfinite(result):
        raise ValueError("distance exceeds floating-point range")
    return result


if __name__ == "__main__":
    import sys

    print(euclidean_distance([0, 0, 0], [3, 4, 0]))
