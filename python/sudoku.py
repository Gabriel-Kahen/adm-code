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

"""sudoku.c translated to Python; indices start at zero."""

if __name__ == "__main__" and not __package__:
    import sys
    from pathlib import Path

    sys.path[0] = str(Path(__file__).resolve().parent.parent)
    __package__ = "python"


def solve_sudoku(encoded: str, strategy: str = "mrv") -> str | None:
    """MRV or row-order backtracking; reject malformed or conflicting givens."""
    if strategy not in ("mrv", "row"):
        raise ValueError("unknown Sudoku strategy")
    if len(encoded) != 81 or any(character not in "0123456789" for character in encoded):
        raise ValueError("Sudoku must contain exactly 81 ASCII digits")
    board = [int(character) for character in encoded]
    rows, columns, boxes = [0] * 9, [0] * 9, [0] * 9
    empty = []
    for index, value in enumerate(board):
        row, column = divmod(index, 9)
        box = row // 3 * 3 + column // 3
        if value == 0:
            empty.append(index)
            continue
        bit = 1 << value
        if (rows[row] | columns[column] | boxes[box]) & bit:
            raise ValueError("conflicting Sudoku givens")
        rows[row] |= bit
        columns[column] |= bit
        boxes[box] |= bit

    def solve(position: int) -> bool:
        if position == len(empty):
            return True
        best, best_mask, best_count = position, 0, 10
        candidates = range(position, len(empty)) if strategy == "mrv" else (position,)
        for candidate in candidates:
            row, column = divmod(empty[candidate], 9)
            mask = 0x3FE & ~(rows[row] | columns[column] | boxes[row // 3 * 3 + column // 3])
            count = mask.bit_count()
            if count < best_count:
                best, best_mask, best_count = candidate, mask, count
        if best_count == 0:
            return False
        empty[position], empty[best] = empty[best], empty[position]
        index = empty[position]
        row, column = divmod(index, 9)
        box = row // 3 * 3 + column // 3
        mask = best_mask
        while mask:
            bit = mask & -mask
            mask -= bit
            board[index] = bit.bit_length() - 1
            rows[row] |= bit
            columns[column] |= bit
            boxes[box] |= bit
            if solve(position + 1):
                return True
            rows[row] ^= bit
            columns[column] ^= bit
            boxes[box] ^= bit
        board[index] = 0
        empty[position], empty[best] = empty[best], empty[position]
        return False

    return "".join(map(str, board)) if solve(0) else None


if __name__ == "__main__":
    import sys

    puzzle = (
        "".join(sys.stdin.read().split())
        or "530070000600195000098000060800060003400803001700020006060000280000419005000080079"
    )
    print(solve_sudoku(puzzle))
