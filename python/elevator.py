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

"""elevator.c translated to Python; indices start at zero."""

if __name__ == "__main__" and not __package__:
    import sys
    from pathlib import Path

    sys.path[0] = str(Path(__file__).resolve().parent.parent)
    __package__ = "python"


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


if __name__ == "__main__":
    import sys

    print(elevator_stops([1, 3, 6], 2, 6))
