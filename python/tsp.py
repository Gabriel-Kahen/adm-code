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

"""Direct translation of tsp.c; data structures and indexing match C."""

if __name__ == "__main__" and not __package__:
    import sys
    from pathlib import Path
    sys.path[0] = str(Path(__file__).resolve().parent.parent)
    __package__ = "python"
    sys.modules[__package__ + "." + Path(__file__).stem] = sys.modules[__name__]

import math

from ._c import address, offset, printf, scanf
from . import annealing
from . import random

# maximum number of points
class point:
    def __init__(self):
        # y: x and y coordinates of point
        self.x = 0
        self.y = 0


class tsp_instance:
    def __init__(self):
        # n: how many points in problem?
        self.n = 0
        # p: array of points
        self.p = [point() for _ in range((NMAX + 1))]


class tsp_solution:
    def __init__(self):
        # cost: lower bound on full cost solution
        self.cost = 0.0
        # n: how many elements in permutation?
        self.n = 0
        # p: array of indices
        self.p = [0 for _ in range((NMAX + 1))]


NMAX = 1001


def read_tsp(t):
    # j: counters
    j = [0]
    scanf("%d\n", address(t, 'n'))
    i = 1
    while (i <= t.n):
        scanf("%d %d %d\n", j, address(t.p[i], 'x'), address(t.p[i], 'y'))
        i += 1


def print_tsp(t):
    # i: counter
    i = 1
    while (i <= t.n):
        printf("%d %d %d\n", i, t.p[i].x, t.p[i].y)
        i += 1


def sq(x):
    return (x * x)


def distance(s, x, y, t):
    i = x
    j = y
    if (i == (t.n + 1)):
        i = 1
    if (j == (t.n + 1)):
        j = 1
    if (i == 0):
        i = t.n
    if (j == 0):
        j = t.n
    return math.hypot((float(t.p[s.p[i]].x) - t.p[s.p[j]].x), (float(t.p[s.p[i]].y) - t.p[s.p[j]].y))


def solution_cost(s, t):
    # i: counter
    # cost: cost of solution
    cost = distance(s, t.n, 1, t)
    i = 1
    while (i < t.n):
        cost = (cost + distance(s, i, (i + 1), t))
        i += 1
    return cost


def initialize_solution(n, s):
    # i: counter
    s.n = n
    i = 1
    while (i <= n):
        s.p[i] = i
        i += 1


def copy_solution(s, t):
    # i: counter
    t.n = s.n
    i = 1
    while (i <= s.n):
        t.p[i] = s.p[i]
        i += 1


def print_solution(s):
    # i: counter
    i = 1
    while (i <= s.n):
        printf(" %d", s.p[i])
        i += 1
    printf("\n------------------------------------------------------\n")


def read_solution(s):
    # i: counter
    scanf("%d\n", address(s, 'n'))
    i = 1
    while (i <= s.n):
        scanf("%d", address(s.p, i))
        i += 1


def random_solution(s):
    random.random_permutation(offset(s.p, 1), (s.n - 1))


def transition(s, t, i, j):
    # willbe: before and after costs
    # neighbors: i,j neighboring tour positions?
    neighbors = False
    if (i == j):
        return 0.0
    if (i > j):
        return transition(s, t, j, i)
    if (i == (j - 1)):
        neighbors = True
    if ((i == 1) and (j == s.n)):
        i, j = j, i
        neighbors = True
    if neighbors:
        was = (distance(s, (i - 1), i, t) + distance(s, j, (j + 1), t))
    else:
        was = (((distance(s, (i - 1), i, t) + distance(s, i, (i + 1), t)) + distance(s, (j - 1), j, t)) + distance(s, j, (j + 1), t))
    random.swap(s.p, i, j)
    if neighbors:
        willbe = (distance(s, (i - 1), i, t) + distance(s, j, (j + 1), t))
    else:
        willbe = (((distance(s, (i - 1), i, t) + distance(s, i, (i + 1), t)) + distance(s, (j - 1), j, t)) + distance(s, j, (j + 1), t))
    return (willbe - was)


def main():
    # Bind this application's callbacks to the shared C-style backend.
    annealing.solution_cost = solution_cost
    annealing.initialize_solution = initialize_solution
    annealing.copy_solution = copy_solution
    annealing.random_solution = random_solution
    annealing.transition = transition
    # t: tsp points
    t = tsp_instance()
    # s: tsp solution
    s = tsp_solution()
    read_tsp(t)
    read_solution(s)
    printf("OPTIMAL SOLUTION COST = %7.1f\n", solution_cost(s, t))
    print_solution(s)
    initialize_solution(t.n, s)
    printf("solution_cost = %7.1f\n", solution_cost(s, t))
    print_solution(s)
    annealing.solution_count = 0
    annealing.random_sampling(t, 10000, s)
    printf("random_sampling %d iterations, cost = %7.1f\n", annealing.solution_count, solution_cost(s, t))
    print_solution(s)
    initialize_solution(t.n, s)
    printf("solution_cost = %7.1f\n", solution_cost(s, t))
    print_solution(s)
    annealing.solution_count = 0
    annealing.repeated_hill_climbing(t, 40, s)
    printf("repeated hill_climbing %d iterations, cost = %7.1f\n", annealing.solution_count, solution_cost(s, t))
    print_solution(s)
    initialize_solution(t.n, s)
    printf("solution_cost = %7.1f\n", solution_cost(s, t))
    print_solution(s)
    annealing.solution_count = 0
    annealing.repeated_annealing(t, 3, s)
    printf("repeated annealing %d iterations, cost = %7.1f\n", annealing.solution_count, solution_cost(s, t))
    print_solution(s)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
