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

"""queue.c translated to Python; indices start at zero."""

if __name__ == "__main__" and not __package__:
    import sys
    from pathlib import Path

    sys.path[0] = str(Path(__file__).resolve().parent.parent)
    __package__ = "python"

from collections import deque
from collections.abc import Iterable
from typing import Generic, TypeVar

T = TypeVar("T")


class Queue(Generic[T]):
    """FIFO queue with O(1) enqueue/dequeue."""

    def __init__(self, values: Iterable[T] = ()) -> None:
        self._values = deque(values)

    def enqueue(self, value: T) -> None:
        self._values.append(value)

    def dequeue(self) -> T:
        return self._values.popleft()

    def __len__(self) -> int:
        return len(self._values)
