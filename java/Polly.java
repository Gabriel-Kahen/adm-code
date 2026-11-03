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
import java.util.ArrayList;
import java.util.Comparator;
import java.util.List;

public final class Polly {
    public record Suitor(String first, String last, long height, long weight) {}

    static BigInteger heightKey(Suitor suitor) {
        return BigInteger.valueOf(suitor.height).subtract(BigInteger.valueOf(180)).abs();
    }

    static BigInteger weightKey(Suitor suitor) {
        BigInteger weight = BigInteger.valueOf(suitor.weight);
        return suitor.weight > 75 ? weight.subtract(BigInteger.valueOf(75)) : weight.negate();
    }

    public static List<Suitor> rankSuitors(List<Suitor> input) {
        List<Suitor> result = new ArrayList<>(input);
        result.sort(Comparator.comparing(Polly::heightKey)
                        .thenComparing(Polly::weightKey)
                        .thenComparing(Suitor::last)
                        .thenComparing(Suitor::first));
        return result;
    }

    public static void main(String[] args) {
        System.out.println(
            rankSuitors(List.of(new Suitor("Amy", "A", 180, 75), new Suitor("Bob", "B", 181, 80))));
    }
}
