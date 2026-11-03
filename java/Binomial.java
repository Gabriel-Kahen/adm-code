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

import java.math.BigInteger;
import java.util.Arrays;

public final class Binomial {
    /** Pascal-row dynamic programming, O(n min(k,n-k)) additions and O(min(k,n-k)) space. */
    public static BigInteger binomial(int n, int k) {
        if (n < 0 || k < 0 || k > n) {
            throw new IllegalArgumentException("require 0 <= k <= n");
        }
        k = Math.min(k, n - k);
        if (k == 0) {
            return BigInteger.ONE;
        }
        BigInteger[] row = new BigInteger[k + 1];
        java.util.Arrays.fill(row, BigInteger.ZERO);
        row[0] = BigInteger.ONE;
        for (long i = 1; i <= n; i++) {
            for (int column = (int)Math.min(i, k); column > 0; column--) {
                row[column] = row[column].add(row[column - 1]);
            }
        }
        return row[k];
    }

    public static void main(String[] args) {
        java.util.Scanner in = new java.util.Scanner(System.in);
        int n = in.hasNextInt() ? in.nextInt() : 10;
        int k = in.hasNextInt() ? in.nextInt() : 5;
        System.out.println(binomial(n, k));
    }
}
