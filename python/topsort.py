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

"""Direct translation of topsort.c; data structures and indexing match C."""

if __name__ == "__main__" and not __package__:
    import sys
    from pathlib import Path
    sys.path[0] = str(Path(__file__).resolve().parent.parent)
    __package__ = "python"
    sys.modules[__package__ + "." + Path(__file__).stem] = sys.modules[__name__]

from ._c import printf
from . import graph
from . import queue


def compute_indegrees(g, in_):
    # i: counter
    # p: temporary pointer
    i = 1
    while (i <= g.nvertices):
        in_[i] = 0
        i += 1
    i = 1
    while (i <= g.nvertices):
        p = g.edges[i]
        while (p != None):
            in_[p.y] += 1
            p = p.next
        i += 1


def topsort(g, sorted):
    # indegree: indegree of each vertex
    indegree = [0 for _ in range((graph.MAXV + 1))]
    # zeroin: vertices of indegree 0
    zeroin = queue.queue()
    # y: current and next vertex
    # j: counters
    # p: temporary pointer
    compute_indegrees(g, indegree)
    queue.init_queue(zeroin)
    i = 1
    while (i <= g.nvertices):
        if (indegree[i] == 0):
            queue.enqueue(zeroin, i)
        i += 1
    j = 0
    while (not queue.empty_queue(zeroin)):
        j = (j + 1)
        x = queue.dequeue(zeroin)
        sorted[j] = x
        p = g.edges[x]
        while (p != None):
            y = p.y
            indegree[y] -= 1
            if (indegree[y] == 0):
                queue.enqueue(zeroin, y)
            p = p.next
    if (j != g.nvertices):
        printf("Not a DAG -- only %d vertices found\n", j)


def main():
    g = graph.graph()
    out = [0 for _ in range((graph.MAXV + 1))]
    graph.read_graph(g, True)
    graph.print_graph(g)
    topsort(g, out)
    i = 1
    while (i <= g.nvertices):
        printf(" %d", out[i])
        i += 1
    printf("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
