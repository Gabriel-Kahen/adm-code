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

"""partition.c translated to Python; indices start at zero."""

if __name__ == "__main__" and not __package__:
    import sys
    from pathlib import Path

    sys.path[0] = str(Path(__file__).resolve().parent.parent)
    __package__ = "python"


def linear_partition(values: list[int], groups: int) -> dict:
    """Split into exactly k nonempty contiguous groups, minimizing largest sum; O(kn²)."""
    if not 1 <= groups <= len(values) or any(value < 0 for value in values):
        raise ValueError("partition requires nonnegative values and 1 <= k <= n")
    prefix = [0]
    for value in values:
        prefix.append(prefix[-1] + value)
    costs: list[list[int | None]] = [[None] * (len(values) + 1) for _ in range(groups + 1)]
    parents = [[-1] * (len(values) + 1) for _ in range(groups + 1)]
    costs[0][0] = 0
    for count in range(1, groups + 1):
        for end in range(count, len(values) + 1):
            for split in range(count - 1, end):
                previous = costs[count - 1][split]
                if previous is None:
                    continue
                candidate = max(previous, prefix[end] - prefix[split])
                if costs[count][end] is None or candidate < costs[count][end]:
                    costs[count][end] = candidate
                    parents[count][end] = split
    result = []
    end = len(values)
    for count in range(groups, 0, -1):
        split = parents[count][end]
        result.append(values[split:end])
        end = split
    return {"cost": costs[groups][-1], "groups": result[::-1]}


if __name__ == "__main__":
    import sys

    values = list(map(int, sys.stdin.read().split())) or [3, 2, 1, 2, 3]
    size, count, *items = values
    if len(items) != size:
        raise ValueError("incorrect item count")
    print(linear_partition(items, count))
