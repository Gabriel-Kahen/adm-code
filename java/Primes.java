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

import java.util.ArrayList;
import java.util.List;

public final class Primes {
    /** Trial division, O(sqrt(n)) worst case; repeated prime factors in ascending order. */
    public static List<Long> factors(long n) {
        if (n < 1) {
            throw new IllegalArgumentException("factorization requires a positive integer");
        }
        List<Long> result = new ArrayList<>();
        while (n % 2 == 0) {
            result.add(2L);
            n /= 2;
        }
        for (long divisor = 3; divisor <= n / divisor; divisor += 2) {
            while (n % divisor == 0) {
                result.add(divisor);
                n /= divisor;
            }
        }
        if (n > 1) {
            result.add(n);
        }
        return result;
    }

    public static void main(String[] args) {
        java.util.Scanner in = new java.util.Scanner(System.in);
        System.out.println(factors(in.hasNextLong() ? in.nextLong() : 360));
    }
}
