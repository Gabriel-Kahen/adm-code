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

"""list-demo.c translated to Python; indices start at zero."""

if __name__ == "__main__" and not __package__:
    import sys
    from pathlib import Path

    sys.path[0] = str(Path(__file__).resolve().parent.parent)
    __package__ = "python"

from collections.abc import Iterator
from dataclasses import dataclass
from typing import Generic, TypeVar

T = TypeVar("T")


@dataclass
class ListNode(Generic[T]):
    value: T
    next: "ListNode[T] | None" = None


class LinkedList(Generic[T]):
    """Head insertion, first-match deletion; duplicates are retained. Search O(n)."""

    def __init__(self) -> None:
        self.head: ListNode[T] | None = None

    def insert(self, value: T) -> None:
        self.head = ListNode(value, self.head)

    def search(self, value: T) -> ListNode[T] | None:
        node = self.head
        while node is not None and node.value != value:
            node = node.next
        return node

    def delete(self, value: T) -> bool:
        previous = None
        node = self.head
        while node is not None:
            if node.value == value:
                if previous is None:
                    self.head = node.next
                else:
                    previous.next = node.next
                return True
            previous, node = node, node.next
        return False

    def __iter__(self) -> Iterator[T]:
        node = self.head
        while node is not None:
            yield node.value
            node = node.next


if __name__ == "__main__":
    import sys

    linked = LinkedList()
    for value in (2, 1, 2):
        linked.insert(value)
    linked.delete(2)
    print(list(linked))
