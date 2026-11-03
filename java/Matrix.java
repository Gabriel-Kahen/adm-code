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

public final class Matrix {
    public static long[][] multiply(long[][] a, long[][] b) {
        int inner = a.length == 0 ? 0 : a[0].length;
        int columns = b.length == 0 ? 0 : b[0].length;
        for (long[] row : a) {
            if (row.length != inner) {
                throw new IllegalArgumentException("ragged matrix");
            }
        }
        for (long[] row : b) {
            if (row.length != columns) {
                throw new IllegalArgumentException("ragged matrix");
            }
        }
        if (inner != b.length) {
            throw new IllegalArgumentException("matrix dimensions do not match");
        }
        long[][] result = new long[a.length][columns];
        for (int i = 0; i < a.length; i++) {
            for (int j = 0; j < columns; j++) {
                for (int k = 0; k < inner; k++) {
                    result[i][j] =
                        Math.addExact(result[i][j], Math.multiplyExact(a[i][k], b[k][j]));
                }
            }
        }
        return result;
    }

    public static void main(String[] args) {
        System.out.println(
            Arrays.deepToString(multiply(new long[][] {{1, 2}}, new long[][] {{3}, {4}})));
    }
}
