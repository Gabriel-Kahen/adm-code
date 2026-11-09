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

"""Direct translation of permutations.c; data structures and indexing match C."""

if __name__ == "__main__" and not __package__:
    import sys
    from pathlib import Path
    sys.path[0] = str(Path(__file__).resolve().parent.parent)
    __package__ = "python"
    sys.modules[__package__ + "." + Path(__file__).stem] = sys.modules[__name__]

from ._c import printf

# max possible next extensions
MAXCANDIDATES = 100
# maximum solution size
NMAX = 100
finished = False


def process_solution(a, k, input):
    # i: counter
    i = 1
    while (i <= k):
        printf(" %d", a[i])
        i += 1
    printf("\n")


def is_a_solution(a, k, n):
    return (k == n)


def make_move(a, k, n):
    pass


def unmake_move(a, k, n):
    pass


# What are possible elements of the next slot in the permutation?
def construct_candidates(a, k, n, c):
    # i: counter
    # in_perm: what is now in the permutation?
    in_perm = [0 for _ in range((NMAX + 1))]
    i = 1
    while (i <= NMAX):
        in_perm[i] = False
        i += 1
    i = 1
    while (i < k):
        in_perm[a[i]] = True
        i += 1
    nc = 0
    i = 1
    while (i <= n):
        if (not in_perm[i]):
            c[nc] = i
            nc = (nc + 1)
        i += 1
    return nc


def backtrack(a, k, input):
    # c: candidates for next position
    c = [0 for _ in range(MAXCANDIDATES)]
    # i: counter
    if is_a_solution(a, k, input):
        process_solution(a, k, input)
    else:
        k = (k + 1)
        # ncandidates: next position candidate count
        ncandidates = construct_candidates(a, k, input, c)
        i = 0
        while (i < ncandidates):
            a[k] = c[i]
            make_move(a, k, input)
            backtrack(a, k, input)
            unmake_move(a, k, input)
            if finished:
                # return: terminate early
                return
            i += 1


def generate_permutations(n):
    # a: solution vector
    a = [0 for _ in range((NMAX + 1))]
    backtrack(a, 0, n)


def main():
    generate_permutations(0)
    generate_permutations(1)
    generate_permutations(2)
    generate_permutations(3)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
