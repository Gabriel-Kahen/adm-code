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

"""Exact integer arithmetic and basic numeric algorithms (Python integers are unbounded)."""

import math
import random
from typing import TypeVar

T = TypeVar("T")


def absolute_difference(first: int, second: int) -> int:
    return abs(first - second)


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


def extended_gcd(first: int, second: int) -> tuple[int, int, int]:
    """Return (g,x,y), g>=0 and first*x + second*y=g; Euclid O(log min(a,b))."""
    old_r, remainder = abs(first), abs(second)
    old_x, x, old_y, y = 1, 0, 0, 1
    while remainder:
        quotient = old_r // remainder
        old_r, remainder = remainder, old_r - quotient * remainder
        old_x, x = x, old_x - quotient * x
        old_y, y = y, old_y - quotient * y
    return old_r, -old_x if first < 0 else old_x, -old_y if second < 0 else old_y


def prime_factors(value: int) -> list[int]:
    """Trial division in O(sqrt(n)); 1 has an empty factorization."""
    if value < 1:
        raise ValueError("factorization requires a positive integer")
    factors = []
    divisor = 2
    while divisor <= value // divisor:
        while value % divisor == 0:
            factors.append(divisor)
            value //= divisor
        divisor = 3 if divisor == 2 else divisor + 2
    if value > 1:
        factors.append(value)
    return factors


def euclidean_distance(first: list[float], second: list[float]) -> float:
    if len(first) != len(second):
        raise ValueError("coordinate dimensions differ")
    if not all(math.isfinite(value) for value in [*first, *second]):
        raise ValueError("coordinates must be finite")
    result = math.hypot(*(a - b for a, b in zip(first, second)))
    if not math.isfinite(result):
        raise ValueError("distance exceeds floating-point range")
    return result


def matrix_multiply(first: list[list[int]], second: list[list[int]]) -> list[list[int]]:
    """Dense rectangular multiplication in O(rows*inner*columns)."""
    if not first or not second or not first[0] or not second[0]:
        raise ValueError("matrices must have positive dimensions")
    inner, columns = len(second), len(second[0])
    if any(len(row) != inner for row in first) or any(len(row) != columns for row in second):
        raise ValueError("incompatible or ragged matrix dimensions")
    result = [[0] * columns for _ in first]
    for row in range(len(first)):
        for shared in range(inner):
            for column in range(columns):
                result[row][column] += first[row][shared] * second[shared][column]
    return result


def convolve(first: list[int], second: list[int]) -> list[int]:
    """Polynomial coefficients in ascending degree order; O(n*m)."""
    if not first or not second:
        return []
    result = [0] * (len(first) + len(second) - 1)
    for i, a in enumerate(first):
        for j, b in enumerate(second):
            result[i + j] += a * b
    return result


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
        value = low * (1 - (fraction := self._random.random())) + high * fraction
        return min(value, math.nextafter(high, low)) if low < high else low

    def permutation(self, values: list[T]) -> list[T]:
        """Fisher-Yates shuffle of a copy, O(n)."""
        result = list(values)
        for index in range(len(result) - 1, 0, -1):
            other = self.integer(0, index)
            result[index], result[other] = result[other], result[index]
        return result
