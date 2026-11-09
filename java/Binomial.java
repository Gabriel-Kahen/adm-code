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

public class Binomial {
    public static final int MAXN = 100; /* largest n or k */

    /* Returns -1 with errno set for invalid arguments or an unrepresentable result. */
    public static long binomial_coefficient(int n, int k) {
        long[] bc = new long[MAXN + 1];
        int i = 0;
        int j = 0;
        int last = 0;
        C.errno = 0;
        if (((((n < 0) || (n > MAXN)) || (k < 0)) || (k > n))) {
            C.errno = 33;
            return (-1);
        }
        if ((k > (n - k))) {
            k = (n - k);
        }
        bc[0] = 1;
        for (i = 1; (i <= n); i++) {
            last = ((i < k) ? i : k);
            for (j = last; (j > 0); j--) {
                if ((bc[j] > (Long.MAX_VALUE - bc[(j - 1)]))) {
                    C.errno = 34;
                    return (-1);
                }
                bc[j] += bc[(j - 1)];
            }
        }
        return bc[k];
    }

    public static int main() {
        int a = 0;
        int b = 0;
        int n = 0;
        int i = 0;
        long coefficient = 0;
        int _read0 = C.scan("%d");
        if (_read0 > 0) n = C.scanInt(0);
        for (i = 0; (i < n); i++) {
            int _read1 = C.scan("%d %d");
            if (_read1 > 0) a = C.scanInt(0);
            if (_read1 > 1) b = C.scanInt(1);
            coefficient = binomial_coefficient(a, b);
            if ((coefficient < 0)) {
                C.perror("binomial coefficient");
                return 1;
            }
            C.printf("%d choose %d = %ld\n", a, b, coefficient);
        }
        return 0;
    }

    public static void main(String[] args) {
        int status = main();
        if (status != 0) System.exit(status);
    }
}
