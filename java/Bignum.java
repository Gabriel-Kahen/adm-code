/*	bignum.c
	Large integer arithmetic: addition, subtraction, multiplication, and division.
*/

/* Copyright 2003-2020 by Steven S. Skiena; all rights reserved.
Permission is granted for use in non-commerical applications
provided this copyright notice remains intact and unchanged.

These programs appear in my books:

"The Algorithm Design Manual" by Steven Skiena, second edition, Springer,
London 2008.  See out website www.algorist.com for additional information
or https://www.amazon.com/exec/obidos/ASIN/1848000693/thealgorith01-20

"Programming Challenges: The Programming Contest Training Manual"
by Steven Skiena and Miguel Revilla, Springer-Verlag, New York 2003.
See our website www.programming-challenges.com for additional information,
or http://www.amazon.com/exec/obidos/ASIN/0387001638/thealgorithmrepo/
*/

public class Bignum {
    public static final int MAXDIGITS = 100; /* maximum length bignum */
    public static final int PLUS = 1; /* positive sign bit */
    public static final int MINUS = -1; /* negative sign bit */
    public static class bignum {
        char[] digits = new char[MAXDIGITS]; /* represent the number */
        int signbit = 0; /* 1 if positive, -1 if negative */
        int lastdigit = 0; /* index of high-order digit */
        public void set(bignum source) {
            for (int _j0 = 0; _j0 < MAXDIGITS; _j0++) {
                digits[_j0] = source.digits[_j0];
            }
            signbit = source.signbit;
            lastdigit = source.lastdigit;
        }
    }

    public static void bignum_capacity_error() {
        C.fprintf("bignum capacity exceeded\n");
        System.exit(1);
    }

    public static void print_bignum(Bignum.bignum n) {
        int i = 0;
        if ((n.signbit == MINUS)) {
            C.printf("- ");
        }
        for (i = n.lastdigit; (i >= 0); i--) {
            C.printf("%c", ('0' + n.digits[i]));
        }
        C.printf("\n");
    }

    public static void zero_justify(Bignum.bignum n) {
        while (((n.lastdigit > 0) && (n.digits[n.lastdigit] == 0))) {
            n.lastdigit--;
        }
        if (((n.lastdigit == 0) && (n.digits[0] == 0))) {
            n.signbit = PLUS; /* zero has one canonical, nonnegative representation */
        }
    }

    public static void int_to_bignum(int s, Bignum.bignum n) {
        int i = 0; /* counter */
        long magnitude = 0;
        if ((s >= 0)) {
            n.signbit = PLUS;
        } else {
            n.signbit = MINUS;
        }
        for (i = 0; (i < MAXDIGITS); i++) {
            n.digits[i] = ((char)0);
        }
        n.lastdigit = (-1);
        /* Unsigned subtraction also handles INT_MIN, whose signed negation does not fit. */
        magnitude = ((s < 0) ? (0L - ((long)s)) : ((long)s));
        while ((magnitude > 0)) {
            n.lastdigit++;
            n.digits[n.lastdigit] = (char)((magnitude % 10));
            magnitude = (magnitude / 10);
        }
        if ((s == 0)) {
            n.lastdigit = 0;
        }
    }

    public static void initialize_bignum(Bignum.bignum n) {
        int_to_bignum(0, n);
    }

    public static int max(int a, int b) {
        if ((a > b)) {
            return a;
        }
        return b;
    }

    /* Historical convention: PLUS means a < b, MINUS means a > b, and 0 means equality. */
    public static int compare_bignum(Bignum.bignum a, Bignum.bignum b) {
        int i = 0; /* counter */
        if (((a.signbit == MINUS) && (b.signbit == PLUS))) {
            return PLUS;
        }
        if (((a.signbit == PLUS) && (b.signbit == MINUS))) {
            return MINUS;
        }
        if ((b.lastdigit > a.lastdigit)) {
            return (PLUS * a.signbit);
        }
        if ((a.lastdigit > b.lastdigit)) {
            return (MINUS * a.signbit);
        }
        for (i = a.lastdigit; (i >= 0); i--) {
            if ((a.digits[i] > b.digits[i])) {
                return (MINUS * a.signbit);
            }
            if ((b.digits[i] > a.digits[i])) {
                return (PLUS * a.signbit);
            }
        }
        return 0;
    }

    public static void subtract_bignum(Bignum.bignum a, Bignum.bignum b, Bignum.bignum c) {
        int borrow = 0; /* has anything been borrowed? */
        int v = 0; /* placeholder digit */
        int i = 0; /* counter */
        initialize_bignum(c);
        if (((a.signbit == MINUS) || (b.signbit == MINUS))) {
            b.signbit = ((-1) * b.signbit);
            add_bignum(a, b, c);
            b.signbit = ((-1) * b.signbit);
            return;
        }
        if ((compare_bignum(a, b) == PLUS)) {
            subtract_bignum(b, a, c);
            c.signbit = MINUS;
            return;
        }
        c.lastdigit = max(a.lastdigit, b.lastdigit);
        borrow = 0;
        for (i = 0; (i <= c.lastdigit); i++) {
            v = ((a.digits[i] - borrow) - b.digits[i]);
            if ((a.digits[i] > 0)) {
                borrow = 0;
            }
            if ((v < 0)) {
                v = (v + 10);
                borrow = 1;
            }
            c.digits[i] = (char)((((char)v) % 10));
        }
        zero_justify(c);
    }

    /*	c = a +- b;	*/
    public static void add_bignum(Bignum.bignum a, Bignum.bignum b, Bignum.bignum c) {
        int carry = 0; /* carry digit */
        int sum = 0;
        int i = 0; /* counter */
        initialize_bignum(c);
        if ((a.signbit == b.signbit)) {
            c.signbit = a.signbit;
        } else {
            if ((a.signbit == MINUS)) {
                a.signbit = PLUS;
                subtract_bignum(b, a, c);
                a.signbit = MINUS;
            } else {
                b.signbit = PLUS;
                subtract_bignum(a, b, c);
                b.signbit = MINUS;
            }
            return;
        }
        c.lastdigit = max(a.lastdigit, b.lastdigit);
        carry = 0;
        for (i = 0; (i <= c.lastdigit); i++) {
            int left_digit = ((i <= a.lastdigit) ? a.digits[i] : 0);
            int right_digit = ((i <= b.lastdigit) ? b.digits[i] : 0);
            sum = ((carry + left_digit) + right_digit);
            c.digits[i] = (char)((sum % 10));
            carry = (sum / 10);
        }
        /* Reserve a new digit only when a carry actually needs it. */
        if ((carry != 0)) {
            if ((c.lastdigit == (MAXDIGITS - 1))) {
                bignum_capacity_error();
            }
            c.lastdigit++;
            c.digits[c.lastdigit] = (char)(carry);
        }
        zero_justify(c);
    }

    /* multiply n by 10^d */
    public static void digit_shift(Bignum.bignum n, int d) {
        int i = 0; /* counter */
        if (((n.lastdigit == 0) && (n.digits[0] == 0))) {
            return;
        }
        if (((d < 0) || (d > ((MAXDIGITS - 1) - n.lastdigit)))) {
            bignum_capacity_error();
        }
        for (i = n.lastdigit; (i >= 0); i--) {
            n.digits[(i + d)] = n.digits[i];
        }
        for (i = 0; (i < d); i++) {
            n.digits[i] = (char)(0);
        }
        n.lastdigit = (n.lastdigit + d);
    }

    public static void multiply_bignum(Bignum.bignum a, Bignum.bignum b, Bignum.bignum c) {
        Bignum.bignum row = new Bignum.bignum(); /* represent shifted row */
        Bignum.bignum tmp = new Bignum.bignum(); /* placeholder bignum */
        int i = 0; /* counters */
        int j = 0;
        initialize_bignum(c);
        row.set(a);
        for (i = 0; (i <= b.lastdigit); i++) {
            for (j = 1; (j <= b.digits[i]); j++) {
                add_bignum(c, row, tmp);
                c.set(tmp);
            }
            if ((i < b.lastdigit)) {
                digit_shift(row, 1);
            }
        }
        c.signbit = (a.signbit * b.signbit);
        zero_justify(c);
    }

    public static void divide_bignum(Bignum.bignum a, Bignum.bignum b, Bignum.bignum c) {
        Bignum.bignum row = new Bignum.bignum(); /* represent shifted row */
        Bignum.bignum tmp = new Bignum.bignum(); /* placeholder bignum */
        int asign = 0; /* temporary signs */
        int bsign = 0;
        int i = 0; /* counters */
        initialize_bignum(c);
        c.signbit = (a.signbit * b.signbit);
        asign = a.signbit;
        bsign = b.signbit;
        a.signbit = PLUS;
        b.signbit = PLUS;
        initialize_bignum(row);
        initialize_bignum(tmp);
        c.lastdigit = a.lastdigit;
        for (i = a.lastdigit; (i >= 0); i--) {
            digit_shift(row, 1);
            row.digits[0] = a.digits[i];
            c.digits[i] = (char)(0);
            while ((compare_bignum(row, b) != PLUS)) {
                c.digits[i]++;
                subtract_bignum(row, b, tmp);
                row.set(tmp);
            }
        }
        zero_justify(c);
        a.signbit = asign;
        b.signbit = bsign;
    }

    public static int main() {
        int a = 0;
        int b = 0;
        Bignum.bignum n1 = new Bignum.bignum();
        Bignum.bignum n2 = new Bignum.bignum();
        Bignum.bignum n3 = new Bignum.bignum();
        Bignum.bignum zero = new Bignum.bignum();
        while (true) {
            int _read0 = C.scan("%d %d\n");
            if (_read0 > 0) a = C.scanInt(0);
            if (_read0 > 1) b = C.scanInt(1);
            if (!((_read0 != -1))) break;
            C.printf("a = %d    b = %d\n", a, b);
            int_to_bignum(a, n1);
            int_to_bignum(b, n2);
            add_bignum(n1, n2, n3);
            C.printf("addition -- ");
            print_bignum(n3);
            C.printf("compare_bignum a ? b = %d\n", compare_bignum(n1, n2));
            subtract_bignum(n1, n2, n3);
            C.printf("subtraction -- ");
            print_bignum(n3);
            multiply_bignum(n1, n2, n3);
            C.printf("multiplication -- ");
            print_bignum(n3);
            int_to_bignum(0, zero);
            if ((compare_bignum(zero, n2) == 0)) {
                C.printf("division -- NaN \n");
            } else {
                divide_bignum(n1, n2, n3);
                C.printf("division -- ");
                print_bignum(n3);
            }
            C.printf("--------------------------\n");
        }
        return 0;
    }

    public static void main(String[] args) {
        int status = main();
        if (status != 0) System.exit(status);
    }
}
