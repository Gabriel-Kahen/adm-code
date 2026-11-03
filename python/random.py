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

"""random.c translated to Python; indices start at zero."""

if __name__ == "__main__" and not __package__:
    import sys
    from pathlib import Path

    sys.path[0] = str(Path(__file__).resolve().parent.parent)
    __package__ = "python"

import math
import random
from typing import TypeVar

T = TypeVar("T")


class RandomSource:
    """Seedable local RNG; deterministic within Python, no cross-language sequence promise."""

    def __init__(self, seed: int = 0) -> None:
        self._random = random.Random(seed)

    def integer(self, low: int, high: int) -> int:
        """Uniform inclusive integer interval."""
        if low > high:
            raise ValueError("inverted integer interval")
        return self._random.randrange(low, high + 1)

    def real(self, low: float, high: float) -> float:
        """Uniform [low,high), except a degenerate interval returns its endpoint."""
        if not math.isfinite(low) or not math.isfinite(high) or low > high:
            raise ValueError("invalid real interval")
        fraction = self._random.random()
        value = low * (1 - fraction) + high * fraction
        return min(value, math.nextafter(high, low)) if low < high else low

    def permutation(self, values: list[T]) -> list[T]:
        """Fisher-Yates shuffle of a copy, O(n)."""
        result = list(values)
        for index in range(len(result) - 1, 0, -1):
            other = self.integer(0, index)
            result[index], result[other] = result[other], result[index]
        return result
