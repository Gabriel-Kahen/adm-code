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

import java.util.ArrayDeque;

public final class War {
    static final String RANKS = "23456789TJQKA";

    static final String SUITS = "cdhs";

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

    public record Result(String winner, int steps) {}

    /** Original Result: each tied comparison is followed by one face-down pair, then another comparison. */
    public static Result war(int limit, int[] first, int[] second) {
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
            return new Result("a", steps);
        }
        if (a.isEmpty() && !b.isEmpty()) {
            return new Result("b", steps);
        }
        return new Result("draw", steps);
    }

    static ArrayDeque<Integer> deck(int[] cards, boolean[] used) {
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

    public static void main(String[] args) {
        System.out.println(war(100, new int[] {48}, new int[] {0}));
    }
}
