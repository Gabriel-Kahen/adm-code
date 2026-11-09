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
# or http://www.amazon.com/exec/obidos/ASIN/0387001638/thealgorithmrepo/

"""Direct translation of annealing.c; data structures and indexing match C."""

if __name__ == "__main__" and not __package__:
    import sys
    from pathlib import Path
    sys.path[0] = str(Path(__file__).resolve().parent.parent)
    __package__ = "python"
    sys.modules[__package__ + "." + Path(__file__).stem] = sys.modules[__name__]

from ._c import *
from . import _c
from . import random
from . import tsp

# print the swaps as they happen
TRACE_OUTPUT = False
# how often we report progress
PRINT_FREQUENCY = 10000
# Simulated Annealing Constants *************************
# Repeated attempts let the caller compare independent heuristic runs.
REPEAT_COUNT = 1
# Initial temperature and cooling rate control how readily uphill moves are accepted.
INITIAL_TEMPERATURE = 1
COOLING_FRACTION = 0.998
# Tune these together: more temperatures or proposals increase the search effort.
COOLING_STEPS = 1000
STEPS_PER_TEMP = 1000
# approximation retained for historical examples
E = 2.718
# Problem-specific Boltzmann constant: tune the acceptance of uphill moves.
K = 0.01
# =========================================================================
# The stuff below is less likely to change in adapting to new
# problems, but look for yourself before leaping.
# string denoting error id
ERROR = "ERROR"
# float denoting error value
ERROR_VALUE = 0.0
# type declarations for SA
# solution_count: how many solutions evaluated
solution_count = 0


def solution_count_update(s, t):
    global solution_count
    solution_count = (solution_count + 1)
    if ((solution_count == 1) or (c_mod(solution_count, PRINT_FREQUENCY) == 0)):
        printf("%d %7.1f\n", solution_count, tsp.solution_cost(s, t))


# Use random sampling to provide a heuristic solution to a given
# optimization problem.
def random_sampling(t, nsamples, s):
    # s_now: current tsp solution
    s_now = tsp.tsp_solution()
    # best_cost: best cost so far
    # cost_now: current cost
    # i: counter
    tsp.initialize_solution(t.n, s_now)
    best_cost = tsp.solution_cost(s_now, t)
    tsp.copy_solution(s_now, s)
    i = 1
    while (i <= nsamples):
        tsp.random_solution(s_now)
        cost_now = tsp.solution_cost(s_now, t)
        if (cost_now < best_cost):
            best_cost = cost_now
            tsp.copy_solution(s_now, s)
        solution_count_update(s_now, t)
        i += 1


# Use hill climbing to provide a heuristic solution to a given
# optimization problem.
def hill_climbing(t, s):
    # cost: best cost so far
    # candidate_cost: cost after the proposed swap
    # j: counters
    # stuck: did I get a better solution?
    tsp.initialize_solution(t.n, s)
    tsp.random_solution(s)
    cost = tsp.solution_cost(s, t)
    # Recompute the objective so every accepted tour strictly decreases
    # the same deterministic cost, including small real improvements.
    while True:
        stuck = True
        i = 1
        while (i < t.n):
            j = (i + 1)
            while (j <= t.n):
                tsp.transition(s, t, i, j)
                candidate_cost = tsp.solution_cost(s, t)
                if (candidate_cost < cost):
                    stuck = False
                    cost = candidate_cost
                else:
                    tsp.transition(s, t, j, i)
                solution_count_update(s, t)
                j += 1
            i += 1
        if not ((not stuck)):
            break


def repeated_hill_climbing(t, nsamples, bestsol):
    # s: current tsp solution
    s = tsp.tsp_solution()
    # best_cost: best cost so far
    # cost_now: current cost
    # i: counter
    tsp.initialize_solution(t.n, s)
    best_cost = tsp.solution_cost(s, t)
    tsp.copy_solution(s, bestsol)
    i = 1
    while (i <= nsamples):
        hill_climbing(t, s)
        cost_now = tsp.solution_cost(s, t)
        if (cost_now < best_cost):
            best_cost = cost_now
            tsp.copy_solution(s, bestsol)
        i += 1


# These routines implement simulated annealing.  Pairs of components
# of the same type will be swapped at random, and the new arrangment
# accepted either if (1) it is an improvement, or (2) the penalty is
# less than a random number, which is a function of the temperature
# of the system.
#
# We are seeking to *minimize* the current_value.
def anneal(t, s):
    # y: pair of items to swap
    # j: counters
    # accept_loss: conditions to accept transition
    # temperature: the current system temp
    # current_value: value of current state
    # start_value: value at start of loop
    # delta: value after swap
    # exponent: exponent for energy funct
    temperature = INITIAL_TEMPERATURE
    tsp.initialize_solution(t.n, s)
    current_value = tsp.solution_cost(s, t)
    i = 1
    while (i <= COOLING_STEPS):
        temperature *= COOLING_FRACTION
        start_value = current_value
        j = 1
        while (j <= STEPS_PER_TEMP):
            # pick indices of elements to swap
            x = random.random_int(1, t.n)
            y = random.random_int(1, t.n)
            delta = tsp.transition(s, t, x, y)
            # did swap reduce cost?
            accept_win = (delta < 0)
            exponent = (float_div(-delta, current_value) / (K * temperature))
            accept_loss = (exp(exponent) > random.random_float(0, 1))
            if (accept_win or accept_loss):
                current_value += delta
            else:
                # reverse transition
                tsp.transition(s, t, x, y)
            solution_count_update(s, t)
            j += 1
        # rerun at this temp
        if (current_value < start_value):
            temperature /= COOLING_FRACTION
        i += 1


def repeated_annealing(t, nsamples, bestsol):
    # s: current tsp solution
    s = tsp.tsp_solution()
    # best_cost: best cost so far
    # cost_now: current cost
    # i: counter
    tsp.initialize_solution(t.n, s)
    best_cost = tsp.solution_cost(s, t)
    tsp.copy_solution(s, bestsol)
    i = 1
    while (i <= nsamples):
        anneal(t, s)
        cost_now = tsp.solution_cost(s, t)
        if (cost_now < best_cost):
            best_cost = cost_now
            tsp.copy_solution(s, bestsol)
        i += 1
