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

package adm;

import java.math.BigInteger;
import java.util.ArrayDeque;
import java.util.ArrayList;
import java.util.Comparator;
import java.util.List;

/** Small demonstrations with reusable results instead of hard-coded console output. */
public final class Demos {
    private Demos() {}

    /** Traversal coordinates for any nonnegative rectangular dimensions. O(rows*columns). */
    public static List<int[]> grid(String method, int rows, int columns) {
        if (rows < 0 || columns < 0 || (long)rows * columns > Integer.MAX_VALUE) {
            throw new IllegalArgumentException("invalid grid dimensions");
        }
        List<int[]> result = new ArrayList<>();
        switch (method) {
        case "row" -> {
            for (int row = 0; row < rows; row++) {
                for (int column = 0; column < columns; column++) {
                    result.add(new int[] {row, column});
                }
            }
        }
        case "column" -> {
            for (int column = 0; column < columns; column++) {
                for (int row = 0; row < rows; row++) {
                    result.add(new int[] {row, column});
                }
            }
        }
        case "snake" -> {
            for (int row = 0; row < rows; row++) {
                for (int i = 0; i < columns; i++) {
                    result.add(new int[] {row, row % 2 == 0 ? i : columns - 1 - i});
                }
            }
        }
        case "diagonal" -> {
            for (long diagonal = 0; diagonal < (long)rows + columns - 1; diagonal++) {
                int first = (int)Math.max(0, diagonal - columns + 1);
                int last = (int)Math.min(rows - 1L, diagonal);
                for (int row = first; row <= last; row++) {
                    result.add(new int[] {row, (int)(diagonal - row)});
                }
            }
        }
        default -> throw new IllegalArgumentException("unknown grid traversal");
        }
        return result;
    }

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

    public record Suitor(String first, String last, long height, long weight) {}
    private static BigInteger heightKey(Suitor suitor) {
        return BigInteger.valueOf(suitor.height).subtract(BigInteger.valueOf(180)).abs();
    }
    private static BigInteger weightKey(Suitor suitor) {
        BigInteger weight = BigInteger.valueOf(suitor.weight);
        return suitor.weight > 75 ? weight.subtract(BigInteger.valueOf(75)) : weight.negate();
    }
    public static List<Suitor> rankSuitors(List<Suitor> input) {
        List<Suitor> result = new ArrayList<>(input);
        result.sort(Comparator.comparing(Demos::heightKey)
                        .thenComparing(Demos::weightKey)
                        .thenComparing(Suitor::last)
                        .thenComparing(Suitor::first));
        return result;
    }

    private static final String RANKS = "23456789TJQKA";
    private static final String SUITS = "cdhs";
    public static int card(String encoded) {
        if (encoded.length() != 2) {
            throw new IllegalArgumentException("card must have rank and suit");
        }
        int rank = RANKS.indexOf(encoded.charAt(0));
        int suit = SUITS.indexOf(encoded.charAt(1));
        if (rank == -1 || suit == -1) {
            throw new IllegalArgumentException("unknown card rank or suit");
        }
        return 4 * rank + suit;
    }
    public static String uncard(int card) {
        if (card < 0 || card >= 52) {
            throw new IllegalArgumentException("card number outside 0..51");
        }
        return "" + RANKS.charAt(card / 4) + SUITS.charAt(card % 4);
    }
    public record War(String winner, int steps) {}

    /** Original War: each tied comparison is followed by one face-down pair, then another comparison. */
    public static War war(int limit, int[] first, int[] second) {
        if (limit < 0) {
            throw new IllegalArgumentException("negative game step limit");
        }
        boolean[] used = new boolean[52];
        ArrayDeque<Integer> a = deck(first, used);
        ArrayDeque<Integer> b = deck(second, used);
        ArrayDeque<Integer> pot = new ArrayDeque<>();
        int steps = 0;
        boolean faceDown = false;
        while (!a.isEmpty() && !b.isEmpty() && steps < limit) {
            int x = a.remove();
            int y = b.remove();
            pot.add(x);
            pot.add(y);
            steps++;
            if (faceDown) {
                faceDown = false;
            } else if (x / 4 == y / 4) {
                faceDown = true;
            } else {
                ArrayDeque<Integer> winner = x / 4 > y / 4 ? a : b;
                while (!pot.isEmpty()) {
                    winner.add(pot.remove());
                }
            }
        }
        if (!a.isEmpty() && b.isEmpty()) {
            return new War("a", steps);
        }
        if (a.isEmpty() && !b.isEmpty()) {
            return new War("b", steps);
        }
        return new War("draw", steps);
    }
    private static ArrayDeque<Integer> deck(int[] cards, boolean[] used) {
        ArrayDeque<Integer> result = new ArrayDeque<>();
        for (int card : cards) {
            if (card < 0 || card >= 52 || used[card]) {
                throw new IllegalArgumentException("invalid or duplicate card");
            }
            used[card] = true;
            result.add(card);
        }
        return result;
    }
}
