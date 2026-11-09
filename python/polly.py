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

"""Direct translation of polly.c; data structures and indexing match C."""

if __name__ == "__main__" and not __package__:
    import sys
    from pathlib import Path
    sys.path[0] = str(Path(__file__).resolve().parent.parent)
    __package__ = "python"
    sys.modules[__package__ + "." + Path(__file__).stem] = sys.modules[__name__]

from functools import cmp_to_key

from ._c import EOF, printf, scanf, strcmp

# maximum length of name
# maximum number of suitors
# best height in centimeters
# best weight in kilograms
class suitor:
    def __init__(self):
        # first: suitor's first name
        self.first = [0 for _ in range(NAMELENGTH)]
        # last: suitor's last name
        self.last = [0 for _ in range(NAMELENGTH)]
        # height: suitor's height
        self.height = 0
        # weight: suitor's weight
        self.weight = 0


NAMELENGTH = 30
NSUITORS = 100
BESTHEIGHT = 180
BESTWEIGHT = 75
# suitors: database of suitors
suitors = [suitor() for _ in range(NSUITORS)]
# nsuitors: number of suitors
nsuitors = 0


def read_suitors():
    global nsuitors
    height = 0
    weight = 0
    nsuitors = 0
    while True:
        nread, suitors[nsuitors].first, suitors[nsuitors].last, height, weight = scanf("%s %s %d %d\n", suitors[nsuitors].first, suitors[nsuitors].last, height, weight)
        if nread == EOF:
            break
        suitors[nsuitors].height = abs((height - BESTHEIGHT))
        if (weight > BESTWEIGHT):
            suitors[nsuitors].weight = (weight - BESTWEIGHT)
        else:
            suitors[nsuitors].weight = (-weight)
        nsuitors += 1


def main():
    # i: counter
    read_suitors()
    suitors[:nsuitors] = sorted(suitors[:nsuitors], key=cmp_to_key(suitor_compare))
    i = 0
    while (i < nsuitors):
        printf("%s, %s\n", suitors[i].last, suitors[i].first)
        i += 1
    return 0


def suitor_compare(left, right):
    a = left
    b = right
    # result: result of comparsion
    if (a.height < b.height):
        return (-1)
    if (a.height > b.height):
        return 1
    if (a.weight < b.weight):
        return (-1)
    if (a.weight > b.weight):
        return 1
    if ((result := strcmp(a.last, b.last)) != 0):
        return result
    return strcmp(a.first, b.first)


if __name__ == "__main__":
    raise SystemExit(main())
