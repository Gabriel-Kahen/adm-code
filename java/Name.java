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

import java.util.List;

public final class Name {
    /** Naive first substring match, O(pattern.length*text.length), empty pattern at zero. */
    public static int find(String pattern, String text) {
        for (int start = 0; start <= text.length() - pattern.length(); start++) {
            int matched = 0;
            while (matched < pattern.length() &&
                   pattern.charAt(matched) == text.charAt(start + matched)) {
                matched++;
            }
            if (matched == pattern.length()) {
                return start;
            }
        }
        return -1;
    }

    public record Change(String before, String after) {}

    /** Apply each rule to original occurrences in that stage, never to its newly inserted text. */
    public static String replace(String text, List<Change> changes) {
        for (Change change : changes) {
            if (change.before.isEmpty()) {
                throw new IllegalArgumentException("empty replacement pattern");
            }
            StringBuilder result = new StringBuilder();
            int cursor = 0;
            int position;
            while ((position = text.indexOf(change.before, cursor)) != -1) {
                result.append(text, cursor, position).append(change.after);
                cursor = position + change.before.length();
            }
            result.append(text, cursor, text.length());
            text = result.toString();
        }
        return text;
    }

    public static void main(String[] args) {
        System.out.println(replace("old old", List.of(new Change("old", "new"))));
    }
}
