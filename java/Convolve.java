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

import java.util.Arrays;

public final class Convolve {
    public static long[] convolve(long[] a, long[] b) {
        if (a.length == 0 || b.length == 0) {
            return new long[0];
        }
        long[] result = new long[Math.addExact(a.length, b.length) - 1];
        for (int i = 0; i < a.length; i++) {
            for (int j = 0; j < b.length; j++) {
                result[i + j] = Math.addExact(result[i + j], Math.multiplyExact(a[i], b[j]));
            }
        }
        return result;
    }

    public static void main(String[] args) {
        System.out.println(Arrays.toString(convolve(new long[] {1, 2}, new long[] {3, 4})));
    }
}
