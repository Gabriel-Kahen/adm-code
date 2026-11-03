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

public final class Substringedit {
    /** Minimum edit distance from pattern to ANY substring of text, including empty. */
    public static int substring(String pattern, String text) {
        int[][] cost = Editdistance.editTable(pattern, text, true);
        int result = pattern.length();
        for (int value : cost[pattern.length()]) {
            result = Math.min(result, value);
        }
        return result;
    }

    public static void main(String[] args) {
        System.out.println(substring("cat", "xxcatyy"));
    }
}
