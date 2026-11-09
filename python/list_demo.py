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

"""Direct translation of list-demo.c; data structures and indexing match C."""

if __name__ == "__main__" and not __package__:
    import sys
    from pathlib import Path
    sys.path[0] = str(Path(__file__).resolve().parent.parent)
    __package__ = "python"
    sys.modules[__package__ + "." + Path(__file__).stem] = sys.modules[__name__]

from ._c import *
from . import _c

class list:
    def __init__(self):
        # item: data item
        self.item = 0
        # next: point to successor
        self.next = None




def init_list():
    return None


def empty_list(l):
    if (l == None):
        return True
    else:
        return False


def search_list(l, x):
    if (l == None):
        return None
    if (l.item == x):
        return l
    else:
        return search_list(l.next, x)


def item_ahead(l, x):
    if ((l == None) or (l.next == None)):
        return None
    if (l.next == x):
        return l
    else:
        return item_ahead(l.next, x)


def insert_list(l, x):
    # p: temporary pointer
    p = list()
    p.item = x
    p.next = l[0]
    l[0] = p


def print_list(l):
    while (l != None):
        printf("%d ", l.item)
        l = l.next
    printf("\n")


def delete_list(l, x):
    # p: item pointer
    # pred: predecessor pointer
    p = l[0]
    pred = item_ahead(l[0], x[0])
    # splice out of list
    if (pred == None):
        l[0] = p.next
    else:
        pred.next = x[0].next
    # free memory used by node
    # Python releases this node when its references disappear.


def main():
    # c: input character
    c = [0]
    # d: input item
    d = [0]
    # l: list under construction
    l = [None]
    # tmp: returned list from search
    tmp = [None]
    l[0] = init_list()
    while (scanf("%c", c) != EOF):
        if (tolower(c[0]) == ord('p')):
            print_list(l[0])
        if (tolower(c[0]) == ord('i')):
            scanf("%d", d)
            printf("new item: %d\n", d[0])
            insert_list(l, d[0])
        if (tolower(c[0]) == ord('s')):
            scanf("%d", d)
            tmp[0] = search_list(l[0], d[0])
            if (tmp[0] == None):
                printf("item %d not found\n", d[0])
            else:
                printf("item %d found\n", d[0])
        if (tolower(c[0]) == ord('d')):
            scanf("%d", d)
            tmp[0] = search_list(l[0], d[0])
            if (tmp[0] == None):
                printf("item to delete %d not found\n", d[0])
            else:
                delete_list(l, tmp)
                printf("item %d deleted\n", d[0])
    return 0


if __name__ == "__main__":
    exit(main())
