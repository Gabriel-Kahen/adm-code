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

"""fib.c translated to Python; indices start at zero."""

if __name__ == "__main__" and not __package__:
    import sys
    from pathlib import Path

    sys.path[0] = str(Path(__file__).resolve().parent.parent)
    __package__ = "python"


def fibonacci(index: int, method: str = "constant") -> int:
    """F(0)=0, F(1)=1; recursion, memoized recursion, table, or constant space."""
    if index < 0:
        raise ValueError("negative Fibonacci index")
    if method == "recursive":
        if index > 30:
            raise ValueError("recursive Fibonacci requires index <= 30")

        def recurse(n: int) -> int:
            return n if n < 2 else recurse(n - 1) + recurse(n - 2)

        return recurse(index)
    if method == "memo":
        if index > 800:
            raise ValueError("memoized Fibonacci requires index <= 800")
        cache = {0: 0, 1: 1}

        def memoized(n: int) -> int:
            if n not in cache:
                cache[n] = memoized(n - 1) + memoized(n - 2)
            return cache[n]

        return memoized(index)
    if method == "table":
        values = [0, 1]
        for current in range(2, index + 1):
            values.append(values[current - 1] + values[current - 2])
        return values[index]
    if method == "constant":
        previous, current = 0, 1
        for _ in range(index):
            previous, current = current, previous + current
        return previous
    raise ValueError("unknown Fibonacci method")


if __name__ == "__main__":
    import sys

    print(fibonacci(int(sys.stdin.read().strip() or "10")))
