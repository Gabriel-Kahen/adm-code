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

"""Unbounded containers; empty removal raises IndexError, lookup uses equality."""

from collections import deque
from dataclasses import dataclass
from typing import Generic, Iterable, Iterator, TypeVar

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


class Stack(Generic[T]):
    """LIFO stack with amortized O(1) push/pop."""

    def __init__(self, values: Iterable[T] = ()) -> None:
        self._values = list(values)

    def push(self, value: T) -> None:
        self._values.append(value)

    def pop(self) -> T:
        return self._values.pop()

    def __len__(self) -> int:
        return len(self._values)


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


@dataclass
class TreeNode(Generic[T]):
    value: T
    left: "TreeNode[T] | None" = None
    right: "TreeNode[T] | None" = None


class BinarySearchTree(Generic[T]):
    """Unbalanced ordered set; duplicate insertions do nothing. Operations O(height)."""

    def __init__(self) -> None:
        self.root: TreeNode[T] | None = None

    def search(self, value: T) -> TreeNode[T] | None:
        node = self.root
        while node is not None and node.value != value:
            node = node.left if value < node.value else node.right
        return node

    def insert(self, value: T) -> None:
        if self.root is None:
            self.root = TreeNode(value)
            return
        node = self.root
        while node.value != value:
            attribute = "left" if value < node.value else "right"
            child = getattr(node, attribute)
            if child is None:
                setattr(node, attribute, TreeNode(value))
                return
            node = child

    def delete(self, value: T) -> bool:
        parent = None
        node = self.root
        while node is not None and node.value != value:
            parent, node = node, node.left if value < node.value else node.right
        if node is None:
            return False
        if node.left is not None and node.right is not None:
            successor_parent, successor = node, node.right
            while successor.left is not None:
                successor_parent, successor = successor, successor.left
            node.value = successor.value
            parent, node = successor_parent, successor
        child = node.left if node.left is not None else node.right
        if parent is None:
            self.root = child
        elif parent.left is node:
            parent.left = child
        else:
            parent.right = child
        return True

    def __iter__(self) -> Iterator[T]:
        stack = []
        node = self.root
        while node is not None or stack:
            while node is not None:
                stack.append(node)
                node = node.left
            node = stack.pop()
            yield node.value
            node = node.right
