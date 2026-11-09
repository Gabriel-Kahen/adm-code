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

"""Direct translation of name.c; data structures and indexing match C."""

if __name__ == "__main__" and not __package__:
    import sys
    from pathlib import Path
    sys.path[0] = str(Path(__file__).resolve().parent.parent)
    __package__ = "python"
    sys.modules[__package__ + "." + Path(__file__).stem] = sys.modules[__name__]

from ._c import address, getchar, offset, printf, scanf, stderr, strlen

# longest possible string
MAXLEN = 1001
# maximum number of name changes
MAXCHANGES = 101
# mergers: store before/after corporate names
mergers = [[[0 for _ in range(MAXLEN)] for _ in range(2)] for _ in range(MAXCHANGES)]
# nmergers: the number of different name changes
nmergers = 0


def read_quoted_string(s):
    # counter
    i = 0
    # c: latest character
    while ((c := getchar()) != ord('\"')):
        pass
    while ((c := getchar()) != ord('\"')):
        s[i] = c
        i = (i + 1)
    s[i] = ord('\0')


def read_changes():
    # i: counter
    scanf("%d\n", address(globals(), 'nmergers'))
    i = 0
    while (i < nmergers):
        read_quoted_string(mergers[i][0])
        read_quoted_string(mergers[i][1])
        i += 1


# Replace the substring of length xlen starting at position pos in
# string s with the contents of string y.
def replace_x_with_y(s, pos, xlen, y):
    # i: counter
    # ylen: lengths of relevant strings
    slen = strlen(s)
    ylen = strlen(y)
    if (xlen >= ylen):
        i = (pos + xlen)
        while (i <= slen):
            s[(i + (ylen - xlen))] = s[i]
            i += 1
    else:
        i = slen
        while (i >= (pos + xlen)):
            s[(i + (ylen - xlen))] = s[i]
            i -= 1
    i = 0
    while (i < ylen):
        s[(pos + i)] = y[i]
        i += 1


# Return the position of the first occurrence of the pattern p
# in the text t, and -1 if it does not occur.
def findmatch(p, t):
    # j: counters
    # tlen: string lengths
    plen = strlen(p)
    tlen = strlen(t)
    i = 0
    while (i <= (tlen - plen)):
        j = 0
        while ((j < plen) and (t[(i + j)] == p[j])):
            j = (j + 1)
        if (j == plen):
            # location of the first match
            return i
        i = (i + 1)
    # there is no match
    return (-1)


def main():
    # s: input string
    s = [0 for _ in range(MAXLEN)]
    # c: input character
    # nlines: number of lines in text
    nlines = [0]
    # j: counters
    # pos: position of pattern in string
    read_changes()
    scanf("%d\n", nlines)
    i = 1
    while (i <= nlines[0]):
        # read text line
        j = 0
        while ((c := getchar()) != ord('\n')):
            s[j] = c
            j = (j + 1)
        s[j] = ord('\0')
        j = 0
        while (j < nmergers):
            cursor = 0
            oldlen = strlen(mergers[j][0])
            newlen = strlen(mergers[j][1])
            if (oldlen == 0):
                stderr.write("A name to replace must not be empty.\n")
                return 1
            while ((pos := findmatch(mergers[j][0], offset(s, cursor))) != (-1)):
                pos += cursor
                if (((strlen(s) - oldlen) + newlen) >= MAXLEN):
                    stderr.write("Renamed text exceeds the line capacity.\n")
                    return 1
                replace_x_with_y(s, pos, oldlen, mergers[j][1])
                cursor = (pos + newlen)
            j += 1
        printf("%s\n", s)
        i = (i + 1)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
