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

"""set_union.c translated to Python; indices start at zero."""

if __name__ == "__main__" and not __package__:
    import sys
    from pathlib import Path

    sys.path[0] = str(Path(__file__).resolve().parent.parent)
    __package__ = "python"


class DisjointSet:
    """Union by size and path compression; amortized inverse-Ackermann operations."""

    def __init__(self, size: int) -> None:
        if size < 0:
            raise ValueError("negative set size")
        self.parent = list(range(size))
        self.size = [1] * size

    def find(self, value: int) -> int:
        if not 0 <= value < len(self.parent):
            raise ValueError("set index out of range")
        root = value
        while root != self.parent[root]:
            root = self.parent[root]
        while value != root:
            previous_parent = self.parent[value]
            self.parent[value] = root
            value = previous_parent
        return root

    def union(self, first: int, second: int) -> bool:
        first, second = self.find(first), self.find(second)
        if first == second:
            return False
        if self.size[first] < self.size[second]:
            first, second = second, first
        self.parent[second] = first
        self.size[first] += self.size[second]
        return True
