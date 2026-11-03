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

"""tree-demo.c translated to Python; indices start at zero."""

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


if __name__ == "__main__":
    import sys

    tree = BinarySearchTree()
    for value in (3, 1, 2):
        tree.insert(value)
    tree.delete(3)
    print(list(tree))
