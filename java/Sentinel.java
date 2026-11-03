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

public final class Sentinel {
    /** Sentinel insertion expressed without an out-of-domain numeric sentinel. O(n). */
    public static long[] insert(long[] sorted, long value) {
        for (int i = 1; i < sorted.length; i++) {
            if (sorted[i] < sorted[i - 1]) {
                throw new IllegalArgumentException("array must be sorted");
            }
        }
        long[] result = Arrays.copyOf(sorted, sorted.length + 1);
        int i = sorted.length;
        while (i > 0 && result[i - 1] > value) {
            result[i] = result[i - 1];
            i--;
        }
        result[i] = value;
        return result;
    }

    public static void main(String[] args) {
        System.out.println(Arrays.toString(insert(new long[] {1, 2, 3}, -1)));
    }
}
