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

"""substringedit.c translated to Python; indices start at zero."""

if __name__ == "__main__" and not __package__:
    import sys
    from pathlib import Path

    sys.path[0] = str(Path(__file__).resolve().parent.parent)
    __package__ = "python"


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


if __name__ == "__main__":
    import sys

    first, second = sys.stdin.read().split() or ["cat", "xxcatyy"]
    print(substring_edit_distance(first, second))
