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

"""war.c translated to Python; indices start at zero."""

if __name__ == "__main__" and not __package__:
    import sys
    from pathlib import Path

    sys.path[0] = str(Path(__file__).resolve().parent.parent)
    __package__ = "python"

from collections import deque

RANKS = "23456789TJQKA"

SUITS = "cdhs"


def card_rank(encoded: str) -> int:
    if len(encoded) != 2 or encoded[0] not in RANKS or encoded[1] not in SUITS:
        raise ValueError("invalid card")
    return RANKS.index(encoded[0]) * 4 + SUITS.index(encoded[1])


def card_name(card: int) -> str:
    if not 0 <= card < 52:
        raise ValueError("invalid card rank")
    return RANKS[card // 4] + SUITS[card % 4]


def war(first: list[int], second: list[int], limit: int = 100000) -> dict:
    """Bounded War simulation; tie means one facedown pair before next comparison.

    Pot order is alternating first/second cards. A pair drawn counts as one step,
    including a facedown pair. Exhaustion together or the step limit means draw.
    """
    cards = first + second
    if limit < 0 or any(not 0 <= card < 52 for card in cards) or len(set(cards)) != len(cards):
        raise ValueError("invalid step limit or repeated/invalid card")
    first_queue, second_queue = deque(first), deque(second)
    pot = []
    facedown = False
    steps = 0
    while first_queue and second_queue and steps < limit:
        steps += 1
        a, b = first_queue.popleft(), second_queue.popleft()
        pot.extend((a, b))
        if facedown:
            facedown = False
        elif a // 4 > b // 4:
            first_queue.extend(pot)
            pot.clear()
        elif a // 4 < b // 4:
            second_queue.extend(pot)
            pot.clear()
        else:
            facedown = True
    winner = (
        "a"
        if first_queue and not second_queue
        else "b"
        if second_queue and not first_queue
        else "draw"
    )
    return {"winner": winner, "steps": steps}


if __name__ == "__main__":
    import sys

    print(war([48], [0]))
