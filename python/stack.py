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

"""Direct translation of stack.c; data structures and indexing match C."""

if __name__ == "__main__" and not __package__:
    import sys
    from pathlib import Path
    sys.path[0] = str(Path(__file__).resolve().parent.parent)
    __package__ = "python"
    sys.modules[__package__ + "." + Path(__file__).stem] = sys.modules[__name__]

from ._c import *
from . import _c

class stack:
    def __init__(self):
        # s: body of queue
        self.s = [0 for _ in range((STACKSIZE + 1))]
        # top: position of top element
        self.top = 0
        # count: number of stack elements
        self.count = 0


STACKSIZE = 1000


def init_stack(s):
    s.top = (-1)
    s.count = 0


def push(s, x):
    if (s.count >= STACKSIZE):
        printf("Warning: stack overflow push x=%d\n", x)
    else:
        s.top = (s.top + 1)
        s.s[s.top] = x
        s.count = (s.count + 1)


def pop(s):
    if (s.count <= 0):
        printf("Warning: empty stack pop.\n")
    x = s.s[s.top]
    s.top = (s.top - 1)
    s.count = (s.count - 1)
    return x


def empty_stack(s):
    return (s.count <= 0)


def print_stack(s):
    # i: counter
    i = (s.count - 1)
    while (i >= 0):
        printf("%d ", s.s[i])
        i -= 1
    printf("\n")
