/*	convolve.c
	Compute the convolution function of two sequences
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

public class Convolve {
    public static final int MAXN = 100; /* largest n or m */

    /* largest n or m */
    public static int max(int x, int y) {
        if ((x > y)) {
            return x;
        } else {
            return y;
        }
    }

    public static int min(int x, int y) {
        if ((x < y)) {
            return x;
        } else {
            return y;
        }
    }

    public static int main() {
        int i = 0; /* counters */
        int j = 0;
        int[] a = new int[MAXN];
        int[] b = new int[MAXN];
        int[] c = new int[((2 * MAXN) - 1)]; /* sequences */
        int n = 0; /* sequence lengths */
        int m = 0;
        for (i = 0; (i < MAXN); i++) {
            a[i] = (b[i] = 0);
        }
        for (i = 0; (i < ((2 * MAXN) - 1)); i++) {
            c[i] = 0;
        }
        int _read0 = C.scan("%d");
        if (_read0 > 0) m = C.scanInt(0);
        if ((((_read0 != 1) || (m < 1)) || (m > MAXN))) {
            return 1;
        }
        for (i = 0; (i < m); i++) {
            int _read1 = C.scan("%d");
            if (_read1 > 0) a[i] = C.scanInt(0);
        }
        int _read2 = C.scan("%d");
        if (_read2 > 0) n = C.scanInt(0);
        if ((((_read2 != 1) || (n < 1)) || (n > MAXN))) {
            return 1;
        }
        for (i = 0; (i < n); i++) {
            int _read3 = C.scan("%d");
            if (_read3 > 0) b[i] = C.scanInt(0);
        }
        for (i = 0; (i < ((n + m) - 1)); i++) {
            for (j = max(0, (i - (n - 1))); (j <= min((m - 1), i)); j++) {
                c[i] = (c[i] + (a[j] * b[(i - j)]));
            }
        }
        for (i = 0; (i < ((m + n) - 1)); i++) {
            C.printf("%d ", c[i]);
        }
        C.printf("\n");
        return 0;
    }

    public static void main(String[] args) {
        int status = main();
        if (status != 0) System.exit(status);
    }
}
