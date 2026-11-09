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
or https://www.amazon.com/exec/obidos/ASIN/0387001638/thealgorithmrepo/
*/

import java.util.Locale;

public class Fib {
    public static final int MAXN = 92; /* largest n for which F(n) fits in a long */
    public static final int UNKNOWN = -1; /* contents denote an empty cell */
    public static long[] f = new long[(MAXN + 1)]; /* array for caching fib values */

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

    public static long fib_r(int n) {
        if ((n == 0)) {
            return 0;
        }
        if ((n == 1)) {
            return 1;
        }
        return (fib_r((n - 1)) + fib_r((n - 2)));
    }

    public static long fib_c(int n) {
        if ((f[n] == UNKNOWN)) {
            f[n] = (fib_c((n - 1)) + fib_c((n - 2)));
        }
        return f[n];
    }

    public static long fib_c_driver(int n) {
        int i = 0; /* counter */
        f[0] = 0;
        f[1] = 1;
        for (i = 2; (i <= n); i++) {
            f[i] = UNKNOWN;
        }
        return fib_c(n);
    }

    public static long fib_dp(int n) {
        int i = 0; /* counter */
        long[] f = new long[(MAXN + 1)]; /* array for caching values */
        f[0] = 0;
        f[1] = 1;
        for (i = 2; (i <= n); i++) {
            f[i] = (f[(i - 1)] + f[(i - 2)]);
        }
        return f[n];
    }

    public static long fib_ultimate(int n) {
        int i = 0; /* counter */
        long back2 = 0; /* last two values of f[n] */
        long back1 = 1;
        long next = 0; /* placeholder for sum */
        if ((n == 0)) {
            return 0;
        }
        for (i = 2; (i < n); i++) {
            next = (back1 + back2);
            back2 = back1;
            back1 = next;
        }
        return (back1 + back2);
    }

    public static int main() {
        int i = 0;
        int ntest = 92;
        for (i = 0; (i <= ntest); i++) {
            System.out.printf(Locale.US, "fib_c(%d) = %d\n", i, fib_c_driver(i));
        }
        for (i = 0; (i <= ntest); i++) {
            System.out.printf(Locale.US, "fib_dp(%d) = %d\n", i, fib_dp(i));
        }
        for (i = 0; (i <= ntest); i++) {
            System.out.printf(Locale.US, "fib_dp2(%d) = %d\n", i, fib_ultimate(i));
        }
        /*
            for (i = 0; i <= ntest; i++) {
                printf("fib(%d) = %ld\n",i, fib_r(i));
            }
        */
        return 0;
    }

    public static void main(String[] args) {
        int status = main();
        if (status != 0) System.exit(status);
    }
}
