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

"""name.c translated to Python; indices start at zero."""

if __name__ == "__main__" and not __package__:
    import sys
    from pathlib import Path

    sys.path[0] = str(Path(__file__).resolve().parent.parent)
    __package__ = "python"


def find_match(pattern: str, text: str) -> int:
    """Naive first substring match, O(mn); empty pattern matches at zero."""
    for start in range(len(text) - len(pattern) + 1):
        if all(text[start + offset] == character for offset, character in enumerate(pattern)):
            return start
    return -1


def replace_names(text: str, changes: list[tuple[str, str]]) -> str:
    """Apply rules sequentially, consuming original matches once per rule."""
    for old, new in changes:
        if old == "":
            raise ValueError("replacement pattern must not be empty")
        pieces = []
        cursor = 0
        while True:
            relative = find_match(old, text[cursor:])
            if relative < 0:
                pieces.append(text[cursor:])
                break
            position = cursor + relative
            pieces.extend((text[cursor:position], new))
            cursor = position + len(old)
        text = "".join(pieces)
    return text


if __name__ == "__main__":
    import sys

    print(replace_names("old old", [("old", "new")]))
