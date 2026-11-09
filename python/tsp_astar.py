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

"""Direct translation of tsp-astar.c; data structures and indexing match C."""

if __name__ == "__main__" and not __package__:
    import sys
    from pathlib import Path
    sys.path[0] = str(Path(__file__).resolve().parent.parent)
    __package__ = "python"
    sys.modules[__package__ + "." + Path(__file__).stem] = sys.modules[__name__]

import math

from ._c import DBL_EPSILON, address, copy_struct, printf, scanf
from . import tsp_pq

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


NMAX = 20
# max possible next extensions
MAXCANDIDATES = 100
# largest possible distance
MAXD = 100000.0
# best_solution: store the current best solution
best_solution = tsp_solution()
# best_cost: cost of current best solution
best_cost = 0.0
# lb: vertex lower bounds
lb = [0.0 for _ in range((NMAX + 1))]
# minlb: global edge lower bound
minlb = 0.0
# evaluations: how many of (n-1!) evaluations were done?
evaluations = 0
# constructions: how many intermediate nodes were calculated
constructions = 0
# maxqueuesize: largest size of queue realized
maxqueuesize = 0
# q: priority queue for branch & bound search
q = tsp_pq.priority_queue()
# use  lower bound to speed branch & bound
lb_flag = True
finished = False


# declarations to clean up branch_and_bound for the book
def process_solution(s, k, input):
    global best_cost, evaluations
    s.cost = solution_cost(s, input)
    if (s.cost < best_cost):
        best_cost = s.cost
        copy_solution(s, best_solution)
    evaluations += 1


def is_a_solution(s, k, t):
    return (k == t.n)


def make_move(s, k, t):
    pass


def unmake_move(s, k, t):
    pass


# What are possible elements of the next slot in the permutation?
def construct_candidates(s, k, t, c, ncandidates):
    global constructions
    # i: counter
    # in_perm: what is now in the permutation?
    in_perm = [0 for _ in range((NMAX + 1))]
    constructions += 1
    if (partial_solution_lb(s, t) > best_cost):
        ncandidates[0] = 0
        return
    if (k == 1):
        c[0] = 1
        ncandidates[0] = 1
        return
    i = 1
    while (i <= NMAX):
        in_perm[i] = False
        i += 1
    i = 1
    while (i < k):
        in_perm[s.p[i]] = True
        i += 1
    ncandidates[0] = 0
    i = 1
    while (i <= t.n):
        if (not in_perm[i]):
            c[ncandidates[0]] = i
            ncandidates[0] = (ncandidates[0] + 1)
        i += 1


# customize backtrack to TSP solutions
def backtrack(s, k, input):
    # c: candidates for next position
    c = [0 for _ in range(MAXCANDIDATES)]
    # ncandidates: next position candidate count
    ncandidates = [0]
    # i: counter
    if is_a_solution(s, k, input):
        process_solution(s, k, input)
    else:
        k = (k + 1)
        construct_candidates(s, k, input, c, ncandidates)
        i = 0
        while (i < ncandidates[0]):
            s.p[k] = c[i]
            s.n = k
            make_move(s, k, input)
            backtrack(s, k, input)
            unmake_move(s, k, input)
            if finished:
                # return: terminate early
                return
            i += 1


def solve_tsp(t, s):
    global best_cost
    first_solution(best_solution, t)
    best_cost = solution_cost(best_solution, t)
    # Fix the first city: rotations describe the same closed tour.
    initialize_solution(s, t)
    extend_solution(s, t, 1)
    backtrack(s, 1, t)


# customize branch and bound  to TSP solutions
def branch_and_bound(s, t):
    global best_cost
    # c: candidates for next position
    c = [0 for _ in range(MAXCANDIDATES)]
    # nc: next position candidate count
    nc = [0]
    # i: counter
    first_solution(best_solution, t)
    best_cost = solution_cost(best_solution, t)
    initialize_solution(s, t)
    extend_solution(s, t, 1)
    tsp_pq.pq_init(q)
    tsp_pq.pq_insert(q, s)
    # Queue keys are conservative lower bounds, not complete-tour costs.
    while ((not tsp_pq.empty_pq(q)) and (tsp_pq.top_pq(q).cost < best_cost)):
        copy_struct(s, tsp_pq.extract_min(q))
        if is_a_solution(s, s.n, t):
            process_solution(s, s.n, t)
        else:
            construct_candidates(s, (s.n + 1), t, c, nc)
            i = 0
            while (i < nc[0]):
                extend_solution(s, t, c[i])
                tsp_pq.pq_insert(q, s)
                contract_solution(s, t)
                i += 1


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


def d(x1, y1, x2, y2):
    return math.hypot((float(x1) - x2), (float(y1) - y2))


def d1(i, j, t):
    return d(t.p[i].x, t.p[i].y, t.p[j].x, t.p[j].y)


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
    return d1(s.p[i], s.p[j], t)


def solution_cost(s, t):
    # i: counter
    # cost: cost of solution
    cost = distance(s, t.n, 1, t)
    i = 1
    while (i < t.n):
        cost = (cost + distance(s, i, (i + 1), t))
        i += 1
    s.cost = cost
    return cost


def partial_solution_cost(s, t):
    # i: counter
    # cost of solution
    cost = 0.0
    i = 1
    while (i < s.n):
        cost = (cost + distance(s, i, (i + 1), t))
        i += 1
    return cost


def partial_solution_lb(s, t):
    remaining = ((t.n - s.n) + (s.n > 0))
    bound = partial_solution_cost(s, t)
    if lb_flag:
        bound += (remaining * minlb)
    # Round conservatively: a lower bound must not round above a tour.
    return max(0.0, (bound - ((64 * DBL_EPSILON) * (abs(bound) + 1))))


def initialize_solution(s, t):
    s.n = 0
    s.cost = 0


def extend_solution(s, t, v):
    s.n += 1
    s.p[s.n] = v
    s.cost = partial_solution_lb(s, t)


def contract_solution(s, t):
    s.n -= 1
    s.cost = partial_solution_lb(s, t)


def first_solution(s, t):
    # i: counter
    s.n = t.n
    i = 1
    while (i <= t.n):
        s.p[i] = i
        i += 1
    s.cost = solution_cost(s, t)


def copy_solution(s, t):
    # i: counter
    t.cost = s.cost
    t.n = s.n
    i = 1
    while (i <= s.n):
        t.p[i] = s.p[i]
        i += 1


def print_solution(s):
    # i: counter
    printf(" n = %d   ", s.n)
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


# Compute lower bounds on edge costs for all vertices
def find_vertex_lower_bounds(t, lb):
    # j: counters
    # minweight: min weight edge in graph
    minweight = MAXD
    i = 1
    while (i <= t.n):
        lb[i] = MAXD
        j = 1
        while (j <= t.n):
            if ((i != j) and (lb[i] > d1(i, j, t))):
                lb[i] = d1(i, j, t)
            j += 1
        if (minweight > lb[i]):
            minweight = lb[i]
        i += 1
    return minweight


def main():
    # Bind this application's callbacks to the shared C-style backend.
    tsp_pq.solution_cost = solution_cost
    tsp_pq.initialize_solution = initialize_solution
    tsp_pq.copy_solution = copy_solution
    global best_cost, constructions, evaluations, lb_flag, maxqueuesize, minlb
    # s: solution vector
    s = tsp_solution()
    # t: tsp points
    t = tsp_instance()
    # i: counter
    read_tsp(t)
    print_tsp(t)
    # first_solution(&s,&t);
    # best_cost = solution_cost(&s, &t);
    #
    # print_solution(&s);
    # printf("INITIAL SOLUTION COST = %7.1f\n",best_cost);
    minlb = find_vertex_lower_bounds(t, lb)
    # printf("minlb = %7.1f\n",minlb);
    #
    # for (i=1; i<=t.n; i++) {
    # printf(" lb[%d] = %7.1f\n", i, lb[i]);
    # }
    i = False
    while (i <= True):
        first_solution(s, t)
        best_cost = solution_cost(s, t)
        # print_solution(&s);
        # printf("INITIAL SOLUTION COST = %7.1f\n",best_cost);
        lb_flag = i
        evaluations = 0
        constructions = evaluations
        solve_tsp(t, s)
        printf(" evaluations = %ld backtracking lb_flag=%d \n", evaluations, lb_flag)
        printf(" constructions = %ld \n", constructions)
        print_solution(best_solution)
        printf("OPTIMAL SOLUTION COST = %7.1f\n", best_cost)
        # Branch and Bound Search *************
        first_solution(s, t)
        best_cost = solution_cost(s, t)
        # print_solution(&s);
        # printf("INITIAL SOLUTION COST = %7.1f\n",best_cost);
        evaluations = 0
        constructions = evaluations
        maxqueuesize = constructions
        branch_and_bound(s, t)
        printf(" evaluations = %ld  branch-and-bound lb_flag=%d \n", evaluations, lb_flag)
        printf(" constructions = %ld  maxqueuesize = %ld \n", constructions, maxqueuesize)
        print_solution(best_solution)
        printf("OPTIMAL B-AND-B SOLUTION COST = %7.1f\n", best_cost)
        i += 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
