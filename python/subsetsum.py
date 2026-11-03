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

"""subsetsum.c translated to Python; indices start at zero."""

if __name__ == "__main__" and not __package__:
    import sys
    from pathlib import Path

    sys.path[0] = str(Path(__file__).resolve().parent.parent)
    __package__ = "python"


def subset_sum(values: list[int], target: int) -> list[int] | None:
    """Return selected indices, or None; nonnegative inputs, O(n*target) time/space bound."""
    if target < 0 or any(value < 0 for value in values):
        raise ValueError("subset sum requires nonnegative values and target")
    witnesses: dict[int, tuple[int, ...]] = {0: ()}
    for index, value in enumerate(values):
        for total, witness in list(witnesses.items()):
            candidate = total + value
            if candidate <= target and candidate not in witnesses:
                witnesses[candidate] = (*witness, index)
        if target in witnesses:
            return list(witnesses[target])
    return list(witnesses[target]) if target in witnesses else None


if __name__ == "__main__":
    import sys

    print(subset_sum([1, 3, 4], 7))
