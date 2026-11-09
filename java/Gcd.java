/*	gcd.c

	Compute the greatest common divisor of two integers
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
or https://www.amazon.com/exec/obidos/ASIN/0387001638/thealgorithmrepo/
*/

public class Gcd {

    /* integers to compute the GCD of */
    public static long gcd1(long p, long q) {
        if ((q > p)) {
            return gcd1(q, p);
        }
        if ((q == 0)) {
            return p;
        }
        C.printf(" gcd(%ld,%ld) &=& gcd(%ld \\mod %ld, %ld) = gcd(%ld,%ld) \n", p, q, p, q, q, q, (p % q));
        return gcd1(q, (p % q));
    }

    /*	Find the gcd(p,q) and x,y such that p*x + q*y = gcd(p,q)	*/
    public static long gcd(long p, long q, long[] x, long[] y) {
        long[] x1 = new long[]{0}; /* previous coefficients */
        long[] y1 = new long[]{0};
        long g = 0; /* value of gcd(p,q) */
        if ((q > p)) {
            return gcd(q, p, y, x);
        }
        if ((q == 0)) {
            x[0] = 1;
            y[0] = 0;
            return p;
        }
        g = gcd(q, (p % q), x1, y1);
        x[0] = y1[0];
        y[0] = (x1[0] - ((p / q) * y1[0]));
        return g;
    }

    public static int main() {
        long p = 0;
        long q = 0;
        long[] x = new long[]{0};
        long[] y = new long[]{0};
        long g1 = 0;
        long g2 = 0;
        while (true) {
            int _read0 = C.scan("%ld %ld");
            if (_read0 > 0) p = C.scanLong(0);
            if (_read0 > 1) q = C.scanLong(1);
            if (!((_read0 != -1))) break;
            g1 = gcd1(p, q);
            g2 = gcd(p, q, x, y);
            C.printf("gcd of p=%ld and q=%ld = %ld\n", p, q, g1);
            C.printf(" %ld*%ld + %ld*%ld = %ld\n", p, x[0], q, y[0], g2);
            if ((g1 != g2)) {
                C.printf("ERROR: GCD\n");
            }
            if ((((p * x[0]) + (q * y[0])) != g1)) {
                C.printf("ERROR: DIOPHONINE SOLUTION WRONG!\n");
            }
        }
        return 0;
    }

    public static void main(String[] args) {
        int status = main();
        if (status != 0) System.exit(status);
    }
}
