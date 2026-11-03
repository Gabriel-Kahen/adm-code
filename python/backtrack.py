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

"""backtrack.c translated to Python; indices start at zero."""

if __name__ == "__main__" and not __package__:
    import sys
    from pathlib import Path

    sys.path[0] = str(Path(__file__).resolve().parent.parent)
    __package__ = "python"

from collections.abc import Callable, Iterable
from typing import TypeVar

T = TypeVar("T")


def backtrack(
    prefix: list[T],
    is_solution: Callable[[list[T]], bool],
    candidates: Callable[[list[T]], Iterable[T]],
    process: Callable[[list[T]], bool],
    make_move: Callable[[list[T]], None] = lambda _: None,
    unmake_move: Callable[[list[T]], None] = lambda _: None,
) -> bool:
    """Generic DFS: process returns False to stop; every made move is undone.

    Callbacks see the current prefix including its latest move. The caller's
    prefix is copied. Undo runs even when recursive callbacks raise exceptions.
    Returns True on exhaustive completion and False on requested early stop.
    """
    current = list(prefix)

    def visit() -> bool:
        if is_solution(current):
            return process(current)
        for candidate in candidates(current):
            current.append(candidate)
            make_move(current)
            try:
                if not visit():
                    return False
            finally:
                unmake_move(current)
                current.pop()
        return True

    return visit()
