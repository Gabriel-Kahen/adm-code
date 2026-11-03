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

public final class Subsets {
    public static List<List<Integer>> subsets(int n) {
        if (n < 0 || n > 20) {
            throw new IllegalArgumentException("subset size outside 0..20");
        }
        List<List<Integer>> result = new ArrayList<>();
        subsetsVisit(n, 0, new ArrayList<>(), result);
        result.sort(Graph::compareLists);
        return result;
    }

    static void subsetsVisit(int n, int next, List<Integer> prefix, List<List<Integer>> result) {
        result.add(new ArrayList<>(prefix));
        for (int value = next; value < n; value++) {
            prefix.add(value);
            subsetsVisit(n, value + 1, prefix, result);
            prefix.remove(prefix.size() - 1);
        }
    }

    public static void main(String[] args) {
        java.util.Scanner in = new java.util.Scanner(System.in);
        System.out.println(subsets(in.hasNextInt() ? in.nextInt() : 3));
    }
}
