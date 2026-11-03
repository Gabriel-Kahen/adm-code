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

"""bignum.c translated to Python; indices start at zero."""

if __name__ == "__main__" and not __package__:
    import sys
    from pathlib import Path

    sys.path[0] = str(Path(__file__).resolve().parent.parent)
    __package__ = "python"


def big_integer(operation: str, first: int, second: int) -> int:
    """Signed integer arithmetic; division truncates toward zero."""
    if operation == "add":
        return first + second
    if operation == "sub":
        return first - second
    if operation == "mul":
        return first * second
    if operation == "div":
        if second == 0:
            raise ValueError("division by zero")
        quotient = abs(first) // abs(second)
        return -quotient if (first < 0) != (second < 0) else quotient
    raise ValueError("unknown bigint operation")


if __name__ == "__main__":
    import sys

    first, second = map(int, (sys.stdin.read().split() or ["123", "17"]))
    for operation in ("add", "sub", "mul", "div"):
        print(operation, big_integer(operation, first, second))
