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

"""Direct translation of sudoku.c; data structures and indexing match C."""

if __name__ == "__main__" and not __package__:
    import sys
    from pathlib import Path
    sys.path[0] = str(Path(__file__).resolve().parent.parent)
    __package__ = "python"
    sys.modules[__package__ + "." + Path(__file__).stem] = sys.modules[__name__]

from ._c import printf, scanf

# base dimension, 3*3 blocks
# 9*9 board
# 81 cells in 9-by-9-board
# max digit choices per cell
class point:
    def __init__(self):
        # y: row and column coordinates of square
        self.x = 0
        self.y = 0


class boardtype:
    def __init__(self):
        # m: board contents
        self.m = [[0 for _ in range((DIMENSION + 1))] for _ in range((DIMENSION + 1))]
        # freecount: open square count
        self.freecount = 0
        # move: which cells have we filled?
        self.move = [point() for _ in range((NCELLS + 1))]


BASED = 3
DIMENSION = 9
NCELLS = (DIMENSION * DIMENSION)
MAXCANDIDATES = (DIMENSION + 1)
finished = False
# finished: solution found, stop search
# steps: how many total move insertions?
steps = 0
# fast: fast or slow nextmove algorithm?
fast = 0
# smart: quickly test for unfillable squares?
smart = 0


def possible_values(p, board, possible):
    # y: square to fill
    # j: counters
    # ylow: origin of box with (x,y)
    # init: is anything/everthing possible?
    x = p.x
    y = p.y
    if ((board.m[x][y] != 0) or ((x < 0) or (y < 0))):
        init = False
    else:
        init = True
    possible[0] = False
    i = 1
    while (i <= DIMENSION):
        possible[i] = init
        i += 1
    i = 0
    while (i < DIMENSION):
        if (board.m[x][i] != 0):
            possible[board.m[x][i]] = False
        i += 1
    i = 0
    while (i < DIMENSION):
        if (board.m[i][y] != 0):
            possible[board.m[i][y]] = False
        i += 1
    xlow = (BASED * int(x // BASED))
    ylow = (BASED * int(y // BASED))
    i = xlow
    while (i < (xlow + BASED)):
        j = ylow
        while (j < (ylow + BASED)):
            if (board.m[i][j] != 0):
                possible[board.m[i][j]] = False
            j += 1
        i += 1


def print_possible(possible):
    # i: counter
    i = 1
    while (i <= DIMENSION):
        if possible[i]:
            printf(" %d", i)
        printf("\n")
        i += 1


def possible_count(x, y, board):
    # i: counter
    # cnt: number of open squares
    # possible: what is possible for the square
    possible = [0 for _ in range((DIMENSION + 1))]
    p = point()
    p.x = x
    p.y = y
    possible_values(p, board, possible)
    cnt = 0
    i = 1
    while (i <= DIMENSION):
        if possible[i]:
            cnt += 1
        i += 1
    return cnt


def fill_square(p, v, board):
    if (board.m[p.x][p.y] == 0):
        board.freecount = (board.freecount - 1)
    else:
        printf("Warning: filling already filled square (%d,%d)\n", p.x, p.y)
    board.m[p.x][p.y] = v


def free_square(p, board):
    if (board.m[p.x][p.y] != 0):
        board.freecount = (board.freecount + 1)
    else:
        printf("Warning: freeing already empty square (%d,%d)\n", p.x, p.y)
    board.m[p.x][p.y] = 0


def next_square(p, board):
    # j: counters
    # newcnt: the best and latest square counts
    # doomed: some empty square without moves?
    bestcnt = (DIMENSION + 1)
    doomed = False
    p.y = (-1)
    p.x = p.y
    i = 0
    while (i < DIMENSION):
        j = 0
        while (j < DIMENSION):
            newcnt = possible_count(i, j, board)
            if ((newcnt == 0) and (board.m[i][j] == 0)):
                doomed = True
            if fast:
                if (((board.m[i][j] == 0) and (newcnt < bestcnt)) and (newcnt >= 1)):
                    bestcnt = newcnt
                    p.x = i
                    p.y = j
            else:
                if ((newcnt >= 1) and (board.m[i][j] == 0)):
                    p.x = i
                    p.y = j
            j += 1
        i += 1
    if (doomed and smart):
        # initialize to non-position
        p.y = (-1)
        p.x = p.y


def print_board(board):
    # j: counters
    printf("\nThere are %d free board positions.\n", board.freecount)
    i = 0
    while (i < DIMENSION):
        j = 0
        while (j < DIMENSION):
            if (board.m[i][j] == 0):
                printf(" ")
            else:
                printf("%c", (int(ord('0')) + board.m[i][j]))
            if ((j + 1) % BASED == 0):
                printf("|")
            j += 1
        printf("\n")
        if ((i + 1) % BASED == 0):
            j = 0
            while (j < ((DIMENSION + BASED) - 1)):
                printf("-")
                j += 1
            printf("\n")
        i += 1


def init_board(board):
    # j: counters
    i = 0
    while (i < DIMENSION):
        j = 0
        while (j < DIMENSION):
            board.m[i][j] = 0
            j += 1
        board.freecount = (DIMENSION * DIMENSION)
        i += 1


def read_board(board):
    # j: counters
    c = [0]
    p = point()
    init_board(board)
    i = 0
    while (i < DIMENSION):
        j = 0
        while (j < DIMENSION):
            scanf("%c", c)
            value = int((c[0] - ord('0')))
            if (value != 0):
                p.x = i
                p.y = j
                fill_square(p, value, board)
            j += 1
        # newline
        scanf("\n")
        i += 1


def copy_board(a, b):
    b.freecount = a.freecount
    i = 0
    while (i < DIMENSION):
        j = 0
        while (j < DIMENSION):
            b.m[i][j] = a.m[i][j]
            j += 1
        i += 1


def process_solution(a, k, board):
    global finished
    finished = True
    printf("process solution\n")
    print_board(board)


def is_a_solution(a, k, board):
    global steps
    # count steps for results table
    steps = (steps + 1)
    return (board.freecount == 0)


def make_move(a, k, board):
    fill_square(board.move[k], a[k], board)


def unmake_move(a, k, board):
    free_square(board.move[k], board)


def construct_candidates(a, k, board, c, nc):
    # i: counter
    # possible: which digits fit in this square
    possible = [0 for _ in range((DIMENSION + 1))]
    # pick square to fill next
    next_square(board.move[k], board)
    nc[0] = 0
    if ((board.move[k].x < 0) and (board.move[k].y < 0)):
        # return: error condition, no moves possible
        return
    possible_values(board.move[k], board, possible)
    i = 1
    while (i <= DIMENSION):
        if possible[i]:
            c[nc[0]] = i
            nc[0] = (nc[0] + 1)
        i += 1


def backtrack(a, k, input):
    # c: candidates for next position
    c = [0 for _ in range(MAXCANDIDATES)]
    # ncandidates: next position candidate count
    ncandidates = [0]
    # i: counter
    if is_a_solution(a, k, input):
        process_solution(a, k, input)
    else:
        k = (k + 1)
        construct_candidates(a, k, input, c, ncandidates)
        i = 0
        while (i < ncandidates[0]):
            a[k] = c[i]
            make_move(a, k, input)
            backtrack(a, k, input)
            unmake_move(a, k, input)
            if finished:
                # return: terminate early
                return
            i += 1


def solve_problem(board):
    global finished, steps
    a = [0 for _ in range(((DIMENSION * DIMENSION) + 1))]
    temp = boardtype()
    printf("----------------------------------\n")
    steps = 0
    copy_board(board, temp)
    finished = False
    backtrack(a, 0, temp)
    printf("It took %d steps to find this solution ", steps)
    printf("for fast=%d  smart=%d\n", fast, smart)


def main():
    global fast, smart
    # board: Sudoku board structure
    board = boardtype()
    read_board(board)
    print_board(board)
    fast = True
    smart = True
    solve_problem(board)
    fast = True
    smart = False
    solve_problem(board)
    fast = False
    smart = True
    solve_problem(board)
    fast = False
    smart = False
    solve_problem(board)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
