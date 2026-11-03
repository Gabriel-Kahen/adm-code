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

if __name__ == "__main__" and not __package__:
    import sys
    from pathlib import Path

    sys.path[0] = str(Path(__file__).resolve().parent.parent)
    __package__ = "python"

"""tsp-pq.c translated to Python; indices start at zero."""


import heapq
import itertools


class TourQueue:
    """Minimum-bound frontier with stable ties and an explicit memory guard."""

    def __init__(self, capacity=1_000_000):
        if capacity < 1:
            raise ValueError("capacity must be positive")
        self.capacity = capacity
        self.values = []
        self.sequence = itertools.count()

    def push(self, bound, state):
        if len(self.values) >= self.capacity:
            raise ValueError("TSP best-first frontier exhausted")
        heapq.heappush(self.values, (bound, next(self.sequence), state))

    def pop(self):
        bound, _, state = heapq.heappop(self.values)
        return bound, state

    def __bool__(self):
        return bool(self.values)
