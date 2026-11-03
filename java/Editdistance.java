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

public final class Editdistance {
    public record Edit(int cost, String operations) {}

    /** Unit-cost Levenshtein distance and an executable M/S/I/D alignment. O(mn). */
    public static Edit edit(String source, String target) {
        int[][] cost = editTable(source, target, false);
        int i = source.length();
        int j = target.length();
        StringBuilder reversed = new StringBuilder();
        while (i > 0 || j > 0) {
            if (i > 0 && j > 0 &&
                cost[i][j] ==
                    cost[i - 1][j - 1] + (source.charAt(i - 1) == target.charAt(j - 1) ? 0 : 1)) {
                reversed.append(source.charAt(i - 1) == target.charAt(j - 1) ? 'M' : 'S');
                i--;
                j--;
            } else if (i > 0 && cost[i][j] == cost[i - 1][j] + 1) {
                reversed.append('D');
                i--;
            } else {
                reversed.append('I');
                j--;
            }
        }
        return new Edit(cost[source.length()][target.length()], reversed.reverse().toString());
    }

    static int[][] editTable(String source, String target, boolean freePrefix) {
        int[][] cost = new int[source.length() + 1][target.length() + 1];
        for (int i = 0; i <= source.length(); i++) {
            cost[i][0] = i;
        }
        for (int j = 0; j <= target.length(); j++) {
            cost[0][j] = freePrefix ? 0 : j;
        }
        for (int i = 1; i <= source.length(); i++) {
            for (int j = 1; j <= target.length(); j++) {
                int diagonal =
                    cost[i - 1][j - 1] + (source.charAt(i - 1) == target.charAt(j - 1) ? 0 : 1);
                cost[i][j] = Math.min(diagonal, 1 + Math.min(cost[i - 1][j], cost[i][j - 1]));
            }
        }
        return cost;
    }
}
