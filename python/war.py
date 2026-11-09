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

"""Direct translation of war.c; data structures and indexing match C."""

if __name__ == "__main__" and not __package__:
    import sys
    from pathlib import Path
    sys.path[0] = str(Path(__file__).resolve().parent.parent)
    __package__ = "python"
    sys.modules[__package__ + "." + Path(__file__).stem] = sys.modules[__name__]

from ._c import *
from . import _c
from . import queue
from . import random

NGAMES = 50
MAXSTEPS = 100000
# number of cards
NCARDS = 52
# number of suits
NSUITS = 4
values = char_array("23456789TJQKA", len("23456789TJQKA") + 1)
suits = char_array("cdhs", len("cdhs") + 1)


# Return the suit and value of the given card.
def suit(card):
    return suits[card % NSUITS]


def value(card):
    return values[card // NSUITS]


def print_card_queue(q):
    i = q.first
    while (i != q.last):
        printf("%c%c ", value(q.q[i]), suit(q.q[i]))
        i = (i + 1) % queue.QUEUESIZE
    printf("%2d ", q.q[i])
    printf("\n")


# Rank the card with given value and suit.
def rank_card(value, suit):
    # j: counters
    i = 0
    while (i < NCARDS // NSUITS):
        if (values[i] == value):
            j = 0
            while (j < NSUITS):
                if (suits[j] == suit):
                    return ((i * NSUITS) + j)
                j += 1
        i += 1
    printf("Warning: bad input value=%d, suit=%d\n", value, suit)
    return (-1)


def testcards():
    # i: counter
    i = 0
    while (i < NCARDS):
        printf(" i=%d card[i]=%c%c rank=%d\n", i, value(i), suit(i), rank_card(value(i), suit(i)))
        i += 1


def random_init_decks(a, b):
    # i: counter
    perm = [0 for _ in range((NCARDS + 1))]
    i = 0
    while (i < NCARDS):
        perm[i] = i
        i = (i + 1)
    random.random_permutation(perm, NCARDS)
    queue.init_queue(a)
    queue.init_queue(b)
    i = 0
    while (i < NCARDS // 2):
        queue.enqueue(a, perm[(2 * i)])
        queue.enqueue(b, perm[((2 * i) + 1)])
        i = (i + 1)
    print_card_queue(a)
    print_card_queue(b)


def clear_queue(a, b):
    while (not queue.empty_queue(a)):
        queue.enqueue(b, queue.dequeue(a))


def war(a, b):
    # step counter
    steps = 0
    # y: top cards
    # c: cards involved in the war
    c = queue.queue()
    # inwar: are we involved in a war?
    inwar = False
    queue.init_queue(c)
    while ((not queue.empty_queue(a)) and ((not queue.empty_queue(b)) and (steps < MAXSTEPS))):
        steps = (steps + 1)
        x = queue.dequeue(a)
        y = queue.dequeue(b)
        queue.enqueue(c, x)
        queue.enqueue(c, y)
        if inwar:
            inwar = False
        else:
            if (x // NSUITS > y // NSUITS):
                clear_queue(c, a)
            else:
                if (x // NSUITS < y // NSUITS):
                    clear_queue(c, b)
                else:
                    if (y // NSUITS == x // NSUITS):
                        inwar = True
    if ((not queue.empty_queue(a)) and queue.empty_queue(b)):
        printf("a wins in %d steps \n", steps)
    else:
        if (queue.empty_queue(a) and (not queue.empty_queue(b))):
            printf("b wins in %d steps \n", steps)
        else:
            if ((not queue.empty_queue(a)) and (not queue.empty_queue(b))):
                printf("game tied after %d steps, |a|=%d |b|=%d \n", steps, a.count, b.count)
            else:
                printf("a and b tie in %d steps \n", steps)


def old_main():
    a = queue.queue()
    b = queue.queue()
    i = 1
    while (i <= NGAMES):
        random_init_decks(a, b)
        war(a, b)
        i += 1
    return 0


def main():
    # decks: player's decks
    decks = [queue.queue() for _ in range(2)]
    # c: input characters
    # i: deck counter
    while True:
        i = 0
        while (i <= 1):
            queue.init_queue(decks[i])
            while ((c := getchar()) != ord('\n')):
                if (c == EOF):
                    return (-1)
                if (c != ord(' ')):
                    value = c
                    suit = getchar()
                    queue.enqueue(decks[i], rank_card(value, suit))
            i += 1
        war(decks[0], decks[1])
    return 0


if __name__ == "__main__":
    exit(main())
