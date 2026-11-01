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

"""Dynamic programs with explicit witnesses and no fixed-size arrays."""

from dataclasses import dataclass


@dataclass(frozen=True)
class EditResult:
    cost: int
    operations: str


def edit_distance(first: str, second: str) -> EditResult:
    """Unit-cost Levenshtein distance and M/S/I/D transformation, O(mn) time/space."""
    rows, columns = len(first) + 1, len(second) + 1
    costs = [[0] * columns for _ in range(rows)]
    for row in range(rows):
        costs[row][0] = row
    for column in range(columns):
        costs[0][column] = column
    for row in range(1, rows):
        for column in range(1, columns):
            costs[row][column] = min(
                costs[row - 1][column - 1] + (first[row - 1] != second[column - 1]),
                costs[row][column - 1] + 1,
                costs[row - 1][column] + 1,
            )
    operations = []
    row, column = len(first), len(second)
    while row or column:
        if (
            row
            and column
            and costs[row][column]
            == (costs[row - 1][column - 1] + (first[row - 1] != second[column - 1]))
        ):
            operations.append("M" if first[row - 1] == second[column - 1] else "S")
            row -= 1
            column -= 1
        elif column and costs[row][column] == costs[row][column - 1] + 1:
            operations.append("I")
            column -= 1
        else:
            operations.append("D")
            row -= 1
    return EditResult(costs[-1][-1], "".join(reversed(operations)))


def edit_distance_brute(first: str, second: str) -> int:
    """Exponential recurrence without memoization; restricted to total length <= 18."""
    if len(first) + len(second) > 18:
        raise ValueError("brute edit distance requires combined length <= 18")

    def recurse(row: int, column: int) -> int:
        if row == 0 or column == 0:
            return max(row, column)
        return min(
            recurse(row - 1, column - 1) + (first[row - 1] != second[column - 1]),
            recurse(row - 1, column) + 1,
            recurse(row, column - 1) + 1,
        )

    return recurse(len(first), len(second))


def longest_common_subsequence(first: str, second: str) -> str:
    """One maximum-length common subsequence, O(mn) time and space."""
    lengths = [[0] * (len(second) + 1) for _ in range(len(first) + 1)]
    for row in range(1, len(first) + 1):
        for column in range(1, len(second) + 1):
            if first[row - 1] == second[column - 1]:
                lengths[row][column] = lengths[row - 1][column - 1] + 1
            else:
                lengths[row][column] = max(lengths[row - 1][column], lengths[row][column - 1])
    result = []
    row, column = len(first), len(second)
    while row and column:
        if first[row - 1] == second[column - 1]:
            result.append(first[row - 1])
            row -= 1
            column -= 1
        elif lengths[row - 1][column] >= lengths[row][column - 1]:
            row -= 1
        else:
            column -= 1
    return "".join(reversed(result))


def substring_edit_distance(pattern: str, text: str) -> int:
    """Minimum edit cost from pattern to any text substring (including empty), O(mn)."""
    previous = [0] * (len(text) + 1)
    for row, character in enumerate(pattern, 1):
        current = [row] + [0] * len(text)
        for column, other in enumerate(text, 1):
            current[column] = min(
                previous[column - 1] + (character != other),
                previous[column] + 1,
                current[column - 1] + 1,
            )
        previous = current
    return min(previous)


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


def elevator_stops(destinations: list[int], budget: int, maximum_floor: int) -> dict:
    """Minimize walking to ground or at most budget stops; O(F²(R+budget)) time.

    Riders may walk either direction from their nearest stop. Stops are integer
    floors 1..maximum_floor; ground floor 0 is always available at no budget cost.
    """
    if (
        budget < 0
        or maximum_floor < 0
        or any(not 0 <= value <= maximum_floor for value in destinations)
    ):
        raise ValueError("invalid stop budget, building, or destination")
    budget = min(budget, maximum_floor)
    tail = [
        sum(max(0, value - floor) for value in destinations) for floor in range(maximum_floor + 1)
    ]
    between = [[0] * (maximum_floor + 1) for _ in range(maximum_floor + 1)]
    for first in range(maximum_floor + 1):
        for second in range(first + 1, maximum_floor + 1):
            between[first][second] = sum(
                min(value - first, second - value)
                for value in destinations
                if first < value <= second
            )
    previous: list[int | None] = [tail[0]] + [None] * maximum_floor
    parent_tables = []
    best_cost, best_floor, best_count = tail[0], 0, 0
    for count in range(1, budget + 1):
        current: list[int | None] = [None] * (maximum_floor + 1)
        parents = [-1] * (maximum_floor + 1)
        for last in range(1, maximum_floor + 1):
            for earlier in range(last):
                if previous[earlier] is None:
                    continue
                candidate = previous[earlier] - tail[earlier] + between[earlier][last] + tail[last]
                if current[last] is None or candidate < current[last]:
                    current[last], parents[last] = candidate, earlier
            if current[last] is not None and current[last] < best_cost:
                best_cost, best_floor, best_count = current[last], last, count
        previous = current
        parent_tables.append(parents)
    stops = []
    for count in range(best_count, 0, -1):
        stops.append(best_floor)
        best_floor = parent_tables[count - 1][best_floor]
    return {"cost": best_cost, "stops": stops[::-1]}
