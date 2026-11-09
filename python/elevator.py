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

"""Direct translation of elevator.c; data structures and indexing match C."""

if __name__ == "__main__" and not __package__:
    import sys
    from pathlib import Path
    sys.path[0] = str(Path(__file__).resolve().parent.parent)
    __package__ = "python"
    sys.modules[__package__ + "." + Path(__file__).stem] = sys.modules[__name__]

from ._c import address, fprintf, printf, scanf, stderr

# the height of the building in floors
NFLOORS = 25
# what is the capacity of the elevator?
MAX_RIDERS = 50
MAXINT = 100007
# stops: what floor does everyone get off at?
stops = [0 for _ in range((MAX_RIDERS + 1))]
# nriders: number of riders
nriders = 0
# nstops: number of allowable stops
nstops = 0
# m: dynamic programming cost table
m = [[0 for _ in range((MAX_RIDERS + 1))] for _ in range((NFLOORS + 1))]
# p: dynamic programming parent table
p = [[0 for _ in range((MAX_RIDERS + 1))] for _ in range((NFLOORS + 1))]


def min(a, b):
    if (a < b):
        return a
    return b


def floors_walked(previous, current):
    # total distance traveled
    nsteps = 0
    # i: counter
    i = 1
    while (i <= nriders):
        if ((stops[i] > previous) and (stops[i] <= current)):
            nsteps += min((stops[i] - previous), (current - stops[i]))
        i += 1
    return nsteps


# m[i][j] denotes the cost of serving all the riders using j stops,
# the last of which is at floor i.  Zero is the originating floor.
def optimize_floors():
    # k: counters
    # cost: costs placeholder
    # laststop: the elevator's last stop
    if ((((nriders < 0) or (nriders > MAX_RIDERS)) or (nstops < 0)) or (nstops > MAX_RIDERS)):
        return (-1)
    i = 0
    while (i <= NFLOORS):
        m[i][0] = floors_walked(0, MAXINT)
        p[i][0] = (-1)
        i += 1
    j = 1
    while (j <= nstops):
        i = 0
        while (i <= NFLOORS):
            m[i][j] = MAXINT
            k = 0
            while (k <= i):
                cost = (((m[k][(j - 1)] - floors_walked(k, MAXINT)) + floors_walked(k, i)) + floors_walked(i, MAXINT))
                if (cost < m[i][j]):
                    m[i][j] = cost
                    p[i][j] = k
                k += 1
            i += 1
        j += 1
    laststop = 0
    i = 1
    while (i <= NFLOORS):
        if (m[i][nstops] < m[laststop][nstops]):
            laststop = i
        i += 1
    return laststop


def reconstruct_path(lastfloor, stops_to_go):
    if (stops_to_go > 1):
        reconstruct_path(p[lastfloor][stops_to_go], (stops_to_go - 1))
    printf("%d\n", lastfloor)


def print_matrix(m):
    # j: counters
    j = 0
    while (j <= nstops):
        i = 0
        while (i <= NFLOORS):
            printf("%3d", m[i][j])
            i += 1
        printf("\n")
        j += 1


def main():
    # i: counter
    if (((((scanf("%d %d", address(globals(), 'nriders'), address(globals(), 'nstops')) != 2) or (nriders < 0)) or (nriders > MAX_RIDERS)) or (nstops < 0)) or (nstops > MAX_RIDERS)):
        fprintf(stderr, "invalid elevator dimensions\n")
        return 1
    i = 1
    while (i <= nriders):
        if (((scanf("%d", address(stops, i)) != 1) or (stops[i] < 0)) or (stops[i] > NFLOORS)):
            fprintf(stderr, "invalid destination floor\n")
            return 1
        i += 1
    i = 1
    while (i <= nriders):
        printf("%d\n", stops[i])
        i += 1
    laststop = optimize_floors()
    print_matrix(m)
    printf("\n")
    print_matrix(p)
    printf("cost = %d\n", m[laststop][nstops])
    reconstruct_path(laststop, nstops)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
