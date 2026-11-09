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

"""Direct translation of priority_queue.c; data structures and indexing match C."""

if __name__ == "__main__" and not __package__:
    import sys
    from pathlib import Path
    sys.path[0] = str(Path(__file__).resolve().parent.parent)
    __package__ = "python"
    sys.modules[__package__ + "." + Path(__file__).stem] = sys.modules[__name__]


from ._c import printf

class priority_queue:
    def __init__(self):
        # q: body of queue
        self.q = [0 for _ in range((PQ_SIZE + 1))]
        # n: number of queue elements
        self.n = 0


PQ_SIZE = 1000


def pq_init(q):
    q.n = 0


def pq_parent(n):
    if (n == 1):
        return (-1)
    # implicitly take floor(n/2)
    return int(n) // 2


def pq_young_child(n):
    return (2 * n)


def pq_swap(q, i, j):
    # temp: placeholder
    temp = q.q[i]
    q.q[i] = q.q[j]
    q.q[j] = temp


def bubble_up(q, p):
    if (pq_parent(p) == (-1)):
        # return: at root of heap, no parent
        return
    if (q.q[pq_parent(p)] > q.q[p]):
        pq_swap(q, p, pq_parent(p))
        bubble_up(q, pq_parent(p))


def bubble_down(q, p):
    # c: child index
    # i: counter
    # min_index: index of lightest child
    c = pq_young_child(p)
    min_index = p
    i = 0
    while (i <= 1):
        if ((c + i) <= q.n):
            if (q.q[min_index] > q.q[(c + i)]):
                min_index = (c + i)
        i += 1
    if (min_index != p):
        pq_swap(q, p, min_index)
        bubble_down(q, min_index)


def pq_insert(q, x):
    if (q.n >= PQ_SIZE):
        printf("Warning: priority queue overflow! \n")
    else:
        q.n = (q.n + 1)
        q.q[q.n] = x
        bubble_up(q, q.n)


def extract_min(q):
    # minimum value
    min = (-1)
    if (q.n <= 0):
        printf("Warning: empty priority queue.\n")
    else:
        min = q.q[1]
        q.q[1] = q.q[q.n]
        q.n = (q.n - 1)
        bubble_down(q, 1)
    return min


def empty_pq(q):
    return (q.n <= 0)


def print_pq(q):
    # i: counter
    i = 1
    while (i <= q.n):
        printf("%d ", q.q[i])
        i += 1
    printf("\n")


def make_heap_fast(q, s, n):
    # i: counter
    q.n = n
    i = 0
    while (i < n):
        q.q[(i + 1)] = s[i]
        i += 1
    i = q.n // 2
    while (i >= 1):
        bubble_down(q, i)
        i -= 1


def make_heap(q, s, n):
    # i: counter
    pq_init(q)
    i = 0
    while (i < n):
        pq_insert(q, s[i])
        i += 1


def heap_compare(q, i, count, x):
    if ((count <= 0) or (i > q.n)):
        return count
    if (q.q[i] < x):
        count = heap_compare(q, pq_young_child(i), (count - 1), x)
        count = heap_compare(q, (pq_young_child(i) + 1), count, x)
    return count
