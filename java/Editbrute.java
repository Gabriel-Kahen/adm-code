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

public final class Editbrute {
    /** Deliberately exponential recursive reference for source.length+target.length <= 18. */
    public static int editBrute(String source, String target) {
        if (source.length() + target.length() > 18) {
            throw new IllegalArgumentException("brute edit input too long");
        }
        return brute(source, target, source.length(), target.length());
    }

    static int brute(String source, String target, int i, int j) {
        if (i == 0) {
            return j;
        }
        if (j == 0) {
            return i;
        }
        return Math.min(
            brute(source, target, i - 1, j - 1) +
                (source.charAt(i - 1) == target.charAt(j - 1) ? 0 : 1),
            1 + Math.min(brute(source, target, i - 1, j), brute(source, target, i, j - 1)));
    }

    public static void main(String[] args) {
        System.out.println(editBrute("cat", "cut"));
    }
}
