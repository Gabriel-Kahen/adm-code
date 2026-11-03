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

"""priority_queue.c translated to Python; indices start at zero."""

if __name__ == "__main__" and not __package__:
    import sys
    from pathlib import Path

    sys.path[0] = str(Path(__file__).resolve().parent.parent)
    __package__ = "python"

from collections.abc import Iterable
from typing import Generic, TypeVar

T = TypeVar("T")


class MinHeap(Generic[T]):
    """Binary minimum heap: O(log n) insert/remove, O(n) construction."""

    def __init__(self, values: Iterable[T] = ()) -> None:
        self._values = list(values)
        for parent in range(len(self._values) // 2 - 1, -1, -1):
            self._sink(parent)

    def _sink(self, parent: int) -> None:
        values = self._values
        while 2 * parent + 1 < len(values):
            child = 2 * parent + 1
            if child + 1 < len(values) and values[child + 1] < values[child]:
                child += 1
            if not values[child] < values[parent]:
                break
            values[parent], values[child] = values[child], values[parent]
            parent = child

    def push(self, value: T) -> None:
        self._values.append(value)
        child = len(self._values) - 1
        while child:
            parent = (child - 1) // 2
            if not self._values[child] < self._values[parent]:
                break
            self._values[parent], self._values[child] = self._values[child], self._values[parent]
            child = parent

    def pop(self) -> T:
        if not self._values:
            raise IndexError("empty heap")
        smallest = self._values[0]
        last = self._values.pop()
        if self._values:
            self._values[0] = last
            self._sink(0)
        return smallest

    def peek(self) -> T:
        if not self._values:
            raise IndexError("empty heap")
        return self._values[0]

    def __len__(self) -> int:
        return len(self._values)
