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

"""Direct translation of queue.c; data structures and indexing match C."""

if __name__ == "__main__" and not __package__:
    import sys
    from pathlib import Path
    sys.path[0] = str(Path(__file__).resolve().parent.parent)
    __package__ = "python"
    sys.modules[__package__ + "." + Path(__file__).stem] = sys.modules[__name__]

from ._c import *
from . import _c

class queue:
    def __init__(self):
        # q: body of queue
        self.q = [0 for _ in range((QUEUESIZE + 1))]
        # first: position of first element
        self.first = 0
        # last: position of last element
        self.last = 0
        # count: number of queue elements
        self.count = 0


QUEUESIZE = 1000


def init_queue(q):
    q.first = 0
    q.last = (QUEUESIZE - 1)
    q.count = 0


def enqueue(q, x):
    if (q.count >= QUEUESIZE):
        printf("Warning: queue overflow enqueue x=%d\n", x)
    else:
        q.last = (q.last + 1) % QUEUESIZE
        q.q[q.last] = x
        q.count = (q.count + 1)


def dequeue(q):
    if (q.count <= 0):
        printf("Warning: empty queue dequeue.\n")
    x = q.q[q.first]
    q.first = (q.first + 1) % QUEUESIZE
    q.count = (q.count - 1)
    return x


def headq(q):
    return q.q[q.first]


def empty_queue(q):
    if (q.count <= 0):
        return True
    return False


def print_queue(q):
    i = q.first
    while (i != q.last):
        printf("%d ", q.q[i])
        i = (i + 1) % QUEUESIZE
    printf("%2d ", q.q[i])
    printf("\n")
