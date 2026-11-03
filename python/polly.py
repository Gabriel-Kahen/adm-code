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

"""polly.c translated to Python; indices start at zero."""

if __name__ == "__main__" and not __package__:
    import sys
    from pathlib import Path

    sys.path[0] = str(Path(__file__).resolve().parent.parent)
    __package__ = "python"

from dataclasses import dataclass


@dataclass(frozen=True)
class Suitor:
    first: str
    last: str
    height: int
    weight: int


def rank_suitors(suitors: list[Suitor]) -> list[Suitor]:
    """Sort by the book's (height deviation, weight category, last, first) key."""
    return sorted(
        suitors,
        key=lambda person: (
            abs(person.height - 180),
            person.weight - 75 if person.weight > 75 else -person.weight,
            person.last,
            person.first,
        ),
    )


if __name__ == "__main__":
    import sys

    print(rank_suitors([Suitor("Amy", "A", 180, 75), Suitor("Bob", "B", 181, 80)]))
