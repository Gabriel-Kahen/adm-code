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

"""Direct translation of bignum.c; data structures and indexing match C."""

if __name__ == "__main__" and not __package__:
    import sys
    from pathlib import Path
    sys.path[0] = str(Path(__file__).resolve().parent.parent)
    __package__ = "python"
    sys.modules[__package__ + "." + Path(__file__).stem] = sys.modules[__name__]

from ._c import *
from . import _c

# maximum length bignum
# positive sign bit
# negative sign bit
class bignum:
    def __init__(self):
        # digits: represent the number
        self.digits = [0 for _ in range(MAXDIGITS)]
        # signbit: 1 if positive, -1 if negative
        self.signbit = 0
        # lastdigit: index of high-order digit
        self.lastdigit = 0


MAXDIGITS = 100
PLUS = 1
MINUS = (-1)


def bignum_capacity_error():
    fprintf(stderr, "bignum capacity exceeded\n")
    exit(EXIT_FAILURE)


def print_bignum(n):
    if (n.signbit == MINUS):
        printf("- ")
    i = n.lastdigit
    while (i >= 0):
        printf("%c", (ord('0') + n.digits[i]))
        i -= 1
    printf("\n")


def zero_justify(n):
    while ((n.lastdigit > 0) and (n.digits[n.lastdigit] == 0)):
        n.lastdigit -= 1
    if ((n.lastdigit == 0) and (n.digits[0] == 0)):
        # zero has one canonical, nonnegative representation
        n.signbit = PLUS


def int_to_bignum(s, n):
    # i: counter
    # magnitude: int to work with
    if (s >= 0):
        n.signbit = PLUS
    else:
        n.signbit = MINUS
    i = 0
    while (i < MAXDIGITS):
        n.digits[i] = int(0)
        i += 1
    n.lastdigit = (-1)
    # Unsigned subtraction also handles INT_MIN, whose signed negation does not fit.
    magnitude = (unsigned(0 - unsigned(s)) if (s < 0) else unsigned(s))
    while (magnitude > 0):
        n.lastdigit += 1
        n.digits[n.lastdigit] = magnitude % 10
        magnitude = magnitude // 10
    if (s == 0):
        n.lastdigit = 0


def initialize_bignum(n):
    int_to_bignum(0, n)


def max(a, b):
    if (a > b):
        return a
    return b


# Historical convention: PLUS means a < b, MINUS means a > b, and 0 means equality.
def compare_bignum(a, b):
    # i: counter
    if ((a.signbit == MINUS) and (b.signbit == PLUS)):
        return PLUS
    if ((a.signbit == PLUS) and (b.signbit == MINUS)):
        return MINUS
    if (b.lastdigit > a.lastdigit):
        return (PLUS * a.signbit)
    if (a.lastdigit > b.lastdigit):
        return (MINUS * a.signbit)
    i = a.lastdigit
    while (i >= 0):
        if (a.digits[i] > b.digits[i]):
            return (MINUS * a.signbit)
        if (b.digits[i] > a.digits[i]):
            return (PLUS * a.signbit)
        i -= 1
    return 0


def subtract_bignum(a, b, c):
    # borrow: has anything been borrowed?
    # v: placeholder digit
    # i: counter
    initialize_bignum(c)
    if ((a.signbit == MINUS) or (b.signbit == MINUS)):
        b.signbit = ((-1) * b.signbit)
        add_bignum(a, b, c)
        b.signbit = ((-1) * b.signbit)
        return
    if (compare_bignum(a, b) == PLUS):
        subtract_bignum(b, a, c)
        c.signbit = MINUS
        return
    c.lastdigit = max(a.lastdigit, b.lastdigit)
    borrow = 0
    i = 0
    while (i <= c.lastdigit):
        v = ((a.digits[i] - borrow) - b.digits[i])
        if (a.digits[i] > 0):
            borrow = 0
        if (v < 0):
            v = (v + 10)
            borrow = 1
        c.digits[i] = int(v) % 10
        i += 1
    zero_justify(c)


# c = a +- b;
def add_bignum(a, b, c):
    # carry: carry digit
    # i: counter
    initialize_bignum(c)
    if (a.signbit == b.signbit):
        c.signbit = a.signbit
    else:
        if (a.signbit == MINUS):
            a.signbit = PLUS
            subtract_bignum(b, a, c)
            a.signbit = MINUS
        else:
            b.signbit = PLUS
            subtract_bignum(a, b, c)
            b.signbit = MINUS
        return
    c.lastdigit = max(a.lastdigit, b.lastdigit)
    carry = 0
    i = 0
    while (i <= c.lastdigit):
        left_digit = (a.digits[i] if (i <= a.lastdigit) else 0)
        right_digit = (b.digits[i] if (i <= b.lastdigit) else 0)
        sum = ((carry + left_digit) + right_digit)
        c.digits[i] = sum % 10
        carry = sum // 10
        i += 1
    # Reserve a new digit only when a carry actually needs it.
    if (carry != 0):
        if (c.lastdigit == (MAXDIGITS - 1)):
            bignum_capacity_error()
        c.lastdigit += 1
        c.digits[c.lastdigit] = carry
    zero_justify(c)


# multiply n by 10^d
def digit_shift(n, d):
    # i: counter
    if ((n.lastdigit == 0) and (n.digits[0] == 0)):
        return
    if ((d < 0) or (d > ((MAXDIGITS - 1) - n.lastdigit))):
        bignum_capacity_error()
    i = n.lastdigit
    while (i >= 0):
        n.digits[(i + d)] = n.digits[i]
        i -= 1
    i = 0
    while (i < d):
        n.digits[i] = 0
        i += 1
    n.lastdigit = (n.lastdigit + d)


def multiply_bignum(a, b, c):
    # row: represent shifted row
    row = bignum()
    # tmp: placeholder bignum
    tmp = bignum()
    # j: counters
    initialize_bignum(c)
    copy_struct(row, a)
    i = 0
    while (i <= b.lastdigit):
        j = 1
        while (j <= b.digits[i]):
            add_bignum(c, row, tmp)
            copy_struct(c, tmp)
            j += 1
        if (i < b.lastdigit):
            digit_shift(row, 1)
        i += 1
    c.signbit = (a.signbit * b.signbit)
    zero_justify(c)


def divide_bignum(a, b, c):
    # row: represent shifted row
    row = bignum()
    # tmp: placeholder bignum
    tmp = bignum()
    # bsign: temporary signs
    # i: counters
    initialize_bignum(c)
    c.signbit = (a.signbit * b.signbit)
    asign = a.signbit
    bsign = b.signbit
    a.signbit = PLUS
    b.signbit = PLUS
    initialize_bignum(row)
    initialize_bignum(tmp)
    c.lastdigit = a.lastdigit
    i = a.lastdigit
    while (i >= 0):
        digit_shift(row, 1)
        row.digits[0] = a.digits[i]
        c.digits[i] = 0
        while (compare_bignum(row, b) != PLUS):
            c.digits[i] += 1
            subtract_bignum(row, b, tmp)
            copy_struct(row, tmp)
        i -= 1
    zero_justify(c)
    a.signbit = asign
    b.signbit = bsign


def main():
    a = [0]
    b = [0]
    n1 = bignum()
    n2 = bignum()
    n3 = bignum()
    zero = bignum()
    while (scanf("%d %d\n", a, b) != EOF):
        printf("a = %d    b = %d\n", a[0], b[0])
        int_to_bignum(a[0], n1)
        int_to_bignum(b[0], n2)
        add_bignum(n1, n2, n3)
        printf("addition -- ")
        print_bignum(n3)
        printf("compare_bignum a ? b = %d\n", compare_bignum(n1, n2))
        subtract_bignum(n1, n2, n3)
        printf("subtraction -- ")
        print_bignum(n3)
        multiply_bignum(n1, n2, n3)
        printf("multiplication -- ")
        print_bignum(n3)
        int_to_bignum(0, zero)
        if (compare_bignum(zero, n2) == 0):
            printf("division -- NaN \n")
        else:
            divide_bignum(n1, n2, n3)
            printf("division -- ")
            print_bignum(n3)
        printf("--------------------------\n")


if __name__ == "__main__":
    exit(main())
