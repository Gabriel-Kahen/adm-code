/*    primes.c

    Compute the prime factorization of an integer.
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

import java.util.Locale;

public class Primes {

    public static void prime_factorization(long x) {
        long i = 0; /* counter */
        long c = 0; /* remaining product to factor */
        c = x;
        while (((c % 2) == 0)) {
            System.out.printf(Locale.US, "%d\n", 2);
            c = (c / 2);
        }
        i = 3;
        while ((i <= (Math.sqrt(c) + 1))) {
            if (((c % i) == 0)) {
                System.out.printf(Locale.US, "%d\n", i);
                c = (c / i);
            } else {
                i = (i + 2);
            }
        }
        if ((c > 1)) {
            System.out.printf(Locale.US, "%d\n", c);
        }
    }

    public static int main() {
        long p = 0;
        while (true) {
            int _read0 = C.scan("%ld");
            if (_read0 > 0) p = C.scanLong(0);
            if (!((_read0 != -1))) break;
            System.out.printf(Locale.US, "prime factorization of p=%d \n", p);
            prime_factorization(p);
        }
        return 0;
    }

    public static void main(String[] args) {
        int status = main();
        if (status != 0) System.exit(status);
    }
}
