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

"""Small examples: grid traversal, text changes, ranking, and the original War rules."""

from collections import deque
from dataclasses import dataclass


def grid_order(method: str, rows: int, columns: int) -> list[list[int]]:
    """Visit every cell once, with row/column/snake/diagonal order; O(rows*columns)."""
    if rows < 0 or columns < 0:
        raise ValueError("negative grid dimensions")
    if method == "row":
        return [[row, column] for row in range(rows) for column in range(columns)]
    if method == "column":
        return [[row, column] for column in range(columns) for row in range(rows)]
    if method == "snake":
        return [
            [row, column if row % 2 == 0 else columns - 1 - column]
            for row in range(rows)
            for column in range(columns)
        ]
    if method == "diagonal":
        return [
            [row, diagonal - row]
            for diagonal in range(rows + columns - 1)
            for row in range(max(0, diagonal - columns + 1), min(rows - 1, diagonal) + 1)
        ]
    raise ValueError("unknown grid order")


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
