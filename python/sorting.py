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

"""sorting.c translated to Python; indices start at zero."""

if __name__ == "__main__" and not __package__:
    import sys
    from pathlib import Path

    sys.path[0] = str(Path(__file__).resolve().parent.parent)
    __package__ = "python"

from typing import TypeVar

from .priority_queue import MinHeap

T = TypeVar("T")


def insertion_sort(values: list[T]) -> list[T]:
    """Stable O(n²) insertion sort, O(n) on already sorted input."""
    result = list(values)
    for index in range(1, len(result)):
        value = result[index]
        hole = index
        while hole and value < result[hole - 1]:
            result[hole] = result[hole - 1]
            hole -= 1
        result[hole] = value
    return result


def selection_sort(values: list[T]) -> list[T]:
    """O(n²) selection sort; not stable."""
    result = list(values)
    for index in range(len(result)):
        smallest = index
        for candidate in range(index + 1, len(result)):
            if result[candidate] < result[smallest]:
                smallest = candidate
        result[index], result[smallest] = result[smallest], result[index]
    return result


def quick_sort(values: list[T]) -> list[T]:
    """Iterative three-way quicksort; average O(n log n), worst O(n²)."""
    result = list(values)
    pending = [(0, len(result))]
    while pending:
        low, high = pending.pop()
        if high - low < 2:
            continue
        pivot = result[(low + high) // 2]
        smaller, current, greater = low, low, high
        while current < greater:
            if result[current] < pivot:
                result[smaller], result[current] = result[current], result[smaller]
                smaller += 1
                current += 1
            elif pivot < result[current]:
                greater -= 1
                result[current], result[greater] = result[greater], result[current]
            else:
                current += 1
        pending.extend(((low, smaller), (greater, high)))
    return result


def heap_sort(values: list[T]) -> list[T]:
    """O(n log n) sorting through the hand-written binary minimum heap."""
    heap = MinHeap(values)
    return [heap.pop() for _ in range(len(heap))]


def merge_sort(values: list[T]) -> list[T]:
    """Stable O(n log n) bottom-up merge sort with O(n) scratch storage."""
    result = list(values)
    width = 1
    while width < len(result):
        merged = []
        for start in range(0, len(result), width * 2):
            middle, end = min(start + width, len(result)), min(start + 2 * width, len(result))
            left, right = start, middle
            while left < middle and right < end:
                if result[right] < result[left]:
                    merged.append(result[right])
                    right += 1
                else:
                    merged.append(result[left])
                    left += 1
            merged.extend(result[left:middle])
            merged.extend(result[right:end])
        result = merged
        width *= 2
    return result


SORTS = {
    "insertion": insertion_sort,
    "selection": selection_sort,
    "quick": quick_sort,
    "heap": heap_sort,
    "merge": merge_sort,
}


def binary_search(values: list[T], target: T) -> int:
    """Find first equal item in a nondecreasing array, or -1; O(log n)."""
    low, high = 0, len(values)
    while low < high:
        middle = (low + high) // 2
        if values[middle] < target:
            low = middle + 1
        else:
            high = middle
    return low if low < len(values) and values[low] == target else -1


if __name__ == "__main__":
    import sys

    values = list(map(int, sys.stdin.read().split())) or [3, 1, 2, 1]
    for name, algorithm in SORTS.items():
        print(name, algorithm(values))
