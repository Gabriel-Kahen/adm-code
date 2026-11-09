/*    war.c

    Simulation of the children's card game War

    cards with format value, suit, e.g. 4h ranked by orders 23456789TJQKA and cdhs
*/

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

import java.util.Locale;

public class War {
    public static final int QUEUESIZE = 1000;
    public static final int NGAMES = 50;
    public static final int MAXSTEPS = 100000;
    public static final int NCARDS = 52; /* number of cards */
    public static final int NSUITS = 4; /* number of suits */
    public static char[] values = "23456789TJQKA".toCharArray();
    public static char[] suits = "cdhs".toCharArray();

    /*    Return the suit and value of the given card.     */
    public static char suit(int card) {
        return suits[(card % NSUITS)];
    }

    public static char value(int card) {
        return values[(card / NSUITS)];
    }

    public static void print_card_queue(Queue.queue q) {
        int i = 0;
        i = q.first;
        while ((i != q.last)) {
            System.out.printf(Locale.US, "%c%c ", value(q.q[i]), suit(q.q[i]));
            i = ((i + 1) % QUEUESIZE);
        }
        System.out.printf(Locale.US, "%2d ", q.q[i]);
        System.out.print("\n");
    }

    /*     Rank the card with given value and suit.    */
    public static int rank_card(char value, char suit) {
        int i = 0; /* counters */
        int j = 0;
        for (i = 0; (i < (NCARDS / NSUITS)); i++) {
            if ((values[i] == value)) {
                for (j = 0; (j < NSUITS); j++) {
                    if ((suits[j] == suit)) {
                        return ((i * NSUITS) + j);
                    }
                }
            }
        }
        System.out.printf(Locale.US, "Warning: bad input value=%d, suit=%d\n", (int)value, (int)suit);
        return (-1);
    }

    public static void testcards() {
        int i = 0; /* counter */
        for (i = 0; (i < NCARDS); i++) {
            System.out.printf(Locale.US, " i=%d card[i]=%c%c rank=%d\n", i, value(i), suit(i), rank_card(value(i), suit(i)));
        }
    }

    public static void random_init_decks(Queue.queue a, Queue.queue b) {
        int i = 0; /* counter */
        int[] perm = new int[(NCARDS + 1)];
        for (i = 0; (i < NCARDS); i = (i + 1)) {
            perm[i] = i;
        }
        Random.random_permutation(perm, NCARDS);
        Queue.init_queue(a);
        Queue.init_queue(b);
        for (i = 0; (i < (NCARDS / 2)); i = (i + 1)) {
            Queue.enqueue(a, perm[(2 * i)]);
            Queue.enqueue(b, perm[((2 * i) + 1)]);
        }
        print_card_queue(a);
        print_card_queue(b);
    }

    public static void clear_queue(Queue.queue a, Queue.queue b) {
        while (Queue.empty_queue(a) == 0) {
            Queue.enqueue(b, Queue.dequeue(a));
        }
    }

    public static void war(Queue.queue a, Queue.queue b) {
        int steps = 0; /* step counter */
        int x = 0; /* top cards */
        int y = 0;
        Queue.queue c = new Queue.queue(); /* cards involved in the war */
        boolean inwar = false; /* are we involved in a war? */
        inwar = false;
        Queue.init_queue(c);
        while (((Queue.empty_queue(a) == 0) && ((Queue.empty_queue(b) == 0) && (steps < MAXSTEPS)))) {
            steps = (steps + 1);
            x = Queue.dequeue(a);
            y = Queue.dequeue(b);
            Queue.enqueue(c, x);
            Queue.enqueue(c, y);
            if (inwar) {
                inwar = false;
            } else {
                if (((x / NSUITS) > (y / NSUITS))) {
                    clear_queue(c, a);
                } else {
                    if (((x / NSUITS) < (y / NSUITS))) {
                        clear_queue(c, b);
                    } else {
                        if (((y / NSUITS) == (x / NSUITS))) {
                            inwar = true;
                        }
                    }
                }
            }
        }
        if (((Queue.empty_queue(a) == 0) && (Queue.empty_queue(b) != 0))) {
            System.out.printf(Locale.US, "a wins in %d steps \n", steps);
        } else {
            if (((Queue.empty_queue(a) != 0) && (Queue.empty_queue(b) == 0))) {
                System.out.printf(Locale.US, "b wins in %d steps \n", steps);
            } else {
                if (((Queue.empty_queue(a) == 0) && (Queue.empty_queue(b) == 0))) {
                    System.out.printf(Locale.US, "game tied after %d steps, |a|=%d |b|=%d \n", steps, a.count, b.count);
                } else {
                    System.out.printf(Locale.US, "a and b tie in %d steps \n", steps);
                }
            }
        }
    }

    public static int old_main() {
        Queue.queue a = new Queue.queue();
        Queue.queue b = new Queue.queue();
        int i = 0;
        for (i = 1; (i <= NGAMES); i++) {
            random_init_decks(a, b);
            war(a, b);
        }
        return 0;
    }

    public static int main() {
        Queue.queue[] decks = new Queue.queue[2]; /* player's decks */
        for (int _i0 = 0; _i0 < 2; _i0++) {
            decks[_i0] = new Queue.queue();
        }
        char value = '\000'; /* input characters */
        char suit = '\000';
        int c = 0;
        int i = 0; /* deck counter */
        while (true) {
            for (i = 0; (i <= 1); i++) {
                Queue.init_queue(decks[i]);
                while (((c = C.getchar()) != '\n')) {
                    if ((c == -1)) {
                        return (-1);
                    }
                    if ((c != ' ')) {
                        value = (char)c;
                        suit = (char)(C.getchar());
                        Queue.enqueue(decks[i], rank_card(value, suit));
                    }
                }
            }
            war(decks[0], decks[1]);
        }
    }

    public static void main(String[] args) {
        int status = main();
        if (status != 0) System.exit(status);
    }
}
