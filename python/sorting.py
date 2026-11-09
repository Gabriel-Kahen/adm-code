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

"""Direct translation of sorting.c; data structures and indexing match C."""

if __name__ == "__main__" and not __package__:
    import sys
    from pathlib import Path
    sys.path[0] = str(Path(__file__).resolve().parent.parent)
    __package__ = "python"
    sys.modules[__package__ + "." + Path(__file__).stem] = sys.modules[__name__]

from ._c import *
from . import _c
from . import priority_queue
from . import queue
from . import random

# size of test arrays
NELEM = 100
LESS_THAN = (-1)
EQUAL_TO = 0
GREATER_THAN = 1


def compare(a, b):
    if (a < b):
        return LESS_THAN
    if (a > b):
        return GREATER_THAN
    return EQUAL_TO


# Swap the ith and jth elements of array s.
def newswap(s, i, j):
    # tmp: placeholder
    tmp = s[i]
    s[i] = s[j]
    s[j] = tmp


def insertion_sort(s, n):
    # j: counters
    i = 1
    while (i < n):
        j = i
        while ((j > 0) and (s[j] < s[(j - 1)])):
            random.swap(address(s, j), address(s, (j - 1)))
            j = (j - 1)
        i += 1


def selection_sort(s, n):
    # j: counters
    # min: index of minimum
    i = 0
    while (i < n):
        min = i
        j = (i + 1)
        while (j < n):
            if (s[j] < s[min]):
                min = j
            j += 1
        random.swap(address(s, i), address(s, min))
        i += 1


def partition(s, l, h):
    # i: counter
    # p: pivot element index
    # firsthigh: divider position for pivot element
    # select last element as pivot
    p = h
    firsthigh = l
    i = l
    while (i < h):
        if (s[i] < s[p]):
            random.swap(address(s, i), address(s, firsthigh))
            firsthigh += 1
        i += 1
    random.swap(address(s, p), address(s, firsthigh))
    return firsthigh


# quicksort array s from the index l to index h.
def quicksort(s, l, h):
    # p: index of partition
    if (l < h):
        p = partition(s, l, h)
        quicksort(s, l, (p - 1))
        quicksort(s, (p + 1), h)


def heapsort_(s, n):
    # i: counters
    # q: heap for heapsort
    q = priority_queue.priority_queue()
    priority_queue.make_heap(q, s, n)
    i = 0
    while (i < n):
        s[i] = priority_queue.extract_min(q)
        i += 1


def binary_search(s, key, low, high):
    # middle: index of middle element
    if (low > high):
        # key not found
        return (-1)
    middle = c_div((low + high), 2)
    if (s[middle] == key):
        return middle
    if (s[middle] > key):
        return binary_search(s, key, low, (middle - 1))
    else:
        return binary_search(s, key, (middle + 1), high)


def merge(s, low, middle, high):
    # i: counter
    # buffer2: buffers to hold elements for merging
    buffer1 = queue.queue()
    buffer2 = queue.queue()
    queue.init_queue(buffer1)
    queue.init_queue(buffer2)
    i = low
    while (i <= middle):
        queue.enqueue(buffer1, s[i])
        i += 1
    i = (middle + 1)
    while (i <= high):
        queue.enqueue(buffer2, s[i])
        i += 1
    i = low
    while (not (queue.empty_queue(buffer1) or queue.empty_queue(buffer2))):
        if (queue.headq(buffer1) <= queue.headq(buffer2)):
            s[i] = queue.dequeue(buffer1)
            i += 1
        else:
            s[i] = queue.dequeue(buffer2)
            i += 1
    while (not queue.empty_queue(buffer1)):
        s[i] = queue.dequeue(buffer1)
        i += 1
    while (not queue.empty_queue(buffer2)):
        s[i] = queue.dequeue(buffer2)
        i += 1


def merge_sort(s, low, high):
    # middle: index of middle element
    if (low < high):
        middle = c_div((low + high), 2)
        merge_sort(s, low, middle)
        merge_sort(s, (middle + 1), high)
        merge(s, low, middle, high)


def main():
    s = [0 for _ in range((NELEM + 2))]
    # i: counter
    i = 0
    while (i < NELEM):
        s[i] = (NELEM - i)
        i += 1
    random.random_permutation(s, NELEM)
    insertion_sort(s, NELEM)
    printf("\n\nInsertion sort: \n")
    i = 0
    while (i < NELEM):
        printf("%d ", s[i])
        i += 1
    i = 0
    while (i < NELEM):
        s[i] = (NELEM - i)
        i += 1
    random.random_permutation(s, NELEM)
    selection_sort(s, NELEM)
    printf("\n\nSelection sort: \n")
    i = 0
    while (i < NELEM):
        printf("%d ", s[i])
        i += 1
    i = 0
    while (i < NELEM):
        s[i] = (NELEM - i)
        i += 1
    random.random_permutation(s, NELEM)
    quicksort(s, 0, (NELEM - 1))
    printf("\n\nQuicksort: \n")
    i = 0
    while (i < NELEM):
        printf("%d ", s[i])
        i += 1
    i = 0
    while (i < NELEM):
        s[i] = (NELEM - i)
        i += 1
    random.random_permutation(s, NELEM)
    heapsort_(s, NELEM)
    printf("\n\nHeapsort sort: \n")
    i = 0
    while (i < NELEM):
        printf("%d ", s[i])
        i += 1
    i = 0
    while (i < NELEM):
        s[i] = (NELEM - i)
        i += 1
    random.random_permutation(s, NELEM)
    merge_sort(s, 0, (NELEM - 1))
    printf("\n\nMergesort: \n")
    i = 0
    while (i < NELEM):
        printf("%d ", s[i])
        i += 1
    printf("\n")
    printf("\n")
    # test binary search
    printf("Binary Search: \n")
    i = 0
    while (i < NELEM):
        s[i] = (2 * (NELEM - i))
        i += 1
    random.random_permutation(s, NELEM)
    heapsort_(s, NELEM)
    i = 2
    while (i < ((2 * NELEM) + 1)):
        printf("%d found in %d\n", i, binary_search(s, i, 0, (NELEM - 1)))
        i += 2
    return 0


if __name__ == "__main__":
    exit(main())
