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

public final class Permutations {
    public static List<List<Integer>> permutations(int n) {
        if (n < 0 || n > 9) {
            throw new IllegalArgumentException("permutation size outside 0..9");
        }
        List<List<Integer>> result = new ArrayList<>();
        permutationsVisit(n, new boolean[n], new ArrayList<>(), result);
        return result;
    }

    static void permutationsVisit(int n, boolean[] used, List<Integer> prefix,
                                  List<List<Integer>> result) {
        if (prefix.size() == n) {
            result.add(new ArrayList<>(prefix));
            return;
        }
        for (int value = 0; value < n; value++) {
            if (used[value]) {
                continue;
            }
            used[value] = true;
            prefix.add(value);
            permutationsVisit(n, used, prefix, result);
            prefix.remove(prefix.size() - 1);
            used[value] = false;
        }
    }

    public static void main(String[] args) {
        java.util.Scanner in = new java.util.Scanner(System.in);
        System.out.println(permutations(in.hasNextInt() ? in.nextInt() : 3));
    }
}
