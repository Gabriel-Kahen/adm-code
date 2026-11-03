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

public final class Random {

    private final java.util.Random random;
    public Random(long seed) {
        random = new java.util.Random(seed);
    }
    public int integer(int low, int high) {
        if (low > high) {
            throw new IllegalArgumentException("empty integer interval");
        }
        return (int)((long)low + random.nextLong((long)high - low + 1));
    }
    public double real(double low, double high) {
        Geometry.finite(low);
        Geometry.finite(high);
        if (low > high) {
            throw new IllegalArgumentException("empty real interval");
        }
        if (low == high) {
            return low;
        }
        double fraction = random.nextDouble();
        double value = Geometry.finite((1 - fraction) * low + fraction * high);
        return value < high ? Math.max(low, value) : Math.nextDown(high);
    }
    public void shuffle(int[] values) {
        for (int i = values.length - 1; i > 0; i--) {
            int j = random.nextInt(i + 1);
            int value = values[i];
            values[i] = values[j];
            values[j] = value;
        }
    }
}
