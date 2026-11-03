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

public final class Distance {
    public static double distance(double[] a, double[] b) {
        if (a.length != b.length) {
            throw new IllegalArgumentException("dimension mismatch");
        }
        double result = 0;
        for (int i = 0; i < a.length; i++) {
            Geometry.finite(a[i]);
            Geometry.finite(b[i]);
            result = Math.hypot(result, a[i] - b[i]);
        }
        return Geometry.finite(result);
    }

    public static void main(String[] args) {
        System.out.println(distance(new double[] {0, 0, 0}, new double[] {3, 4, 0}));
    }
}
