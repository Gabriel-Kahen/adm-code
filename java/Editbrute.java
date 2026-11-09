/*	editbrute.c

	Compute string edit distance *without* dynamic programming!
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
or http://www.amazon.com/exec/obidos/ASIN/0387001638/thealgorithmrepo/
*/

public class Editbrute {
    public static final int MAXLEN = 101; /* longest possible string */
    public static final int MATCH = 0; /* enumerated type symbol for match */
    public static final int INSERT = 1; /* enumerated type symbol for insert */
    public static final int DELETE = 2; /* enumerated type symbol for delete */
    public static Editdistance.cell[][] m = new Editdistance.cell[(MAXLEN + 1)][(MAXLEN + 1)]; /* dynamic programming table */
    static {
        for (int _i0 = 0; _i0 < (MAXLEN + 1); _i0++) {
            for (int _i1 = 0; _i1 < (MAXLEN + 1); _i1++) {
                m[_i0][_i1] = new Editdistance.cell();
            }
        }
    }

    public static int read_edit_string(char[] s, int limit) {
        int c = 0;
        int length = 0;
        s[0] = ' ';
        do {
            c = C.getchar();
        } while (((c != -1) && Character.isWhitespace((char)c)));
        if ((c == -1)) {
            return 0;
        }
        do {
            if ((length == limit)) {
                return 0;
            }
            s[++length] = ((char)c);
            c = C.getchar();
        } while (((c != -1) && !(Character.isWhitespace((char)c))));
        s[(length + 1)] = '\000';
        return 1;
    }

    public static void goal_cell(char[] s, char[] t, int[] i, int[] j) {
        i[0] = (C.strlen(s) - 1);
        j[0] = (C.strlen(t) - 1);
    }

    public static int match(char c, char d) {
        if ((c == d)) {
            return 0;
        }
        return 1;
    }

    public static int indel(char c) {
        return 1;
    }

    public static void row_init(int i, Editdistance.cell[][] m) {
        m[0][i].cost = i;
        if ((i > 0)) {
            m[0][i].parent = INSERT;
        } else {
            m[0][i].parent = (-1);
        }
    }

    public static void column_init(int i, Editdistance.cell[][] m) {
        m[i][0].cost = i;
        if ((i > 0)) {
            m[i][0].parent = DELETE;
        } else {
            m[0][i].parent = (-1);
        }
    }

    public static void match_out(char[] s, char[] t, int i, int j) {
        if ((s[i] == t[j])) {
            C.printf("M");
        } else {
            C.printf("S");
        }
    }

    public static void insert_out(char[] t, int j) {
        C.printf("I");
    }

    public static void delete_out(char[] s, int i) {
        C.printf("D");
    }

    public static int string_compare2(char[] s, char[] t, int i, int j, Editdistance.cell[][] m) {
        int k = 0; /* counter */
        int[] opt = new int[3]; /* cost of the three options */
        int lowest_cost = 0; /* lowest cost */
        if ((i == 0)) { /* indel is the cost of an insertion or deletion  */
            m[i][j].cost = (j * indel(' '));
            m[i][j].parent = ((j != 0) ? INSERT : (-1));
            return m[i][j].cost;
        }
        if ((j == 0)) {
            m[i][j].cost = (i * indel(' '));
            m[i][j].parent = DELETE;
            return m[i][j].cost;
        }
        opt[MATCH] = (string_compare2(s, t, (i - 1), (j - 1), m) + match(s[i], t[j]));
        opt[INSERT] = (string_compare2(s, t, i, (j - 1), m) + indel(t[j]));
        opt[DELETE] = (string_compare2(s, t, (i - 1), j, m) + indel(s[i]));
        lowest_cost = opt[MATCH];
        m[i][j].parent = MATCH;
        for (k = INSERT; (k <= DELETE); k++) {
            if ((opt[k] < lowest_cost)) {
                lowest_cost = opt[k];
                m[i][j].parent = k;
            }
        }
        m[i][j].cost = lowest_cost; /* REMOVE FROM PRINTED VERSION */
        return lowest_cost;
    }

    public static int string_compare_r(char[] s, char[] t, int i, int j) {
        int k = 0; /* counter */
        int[] opt = new int[3]; /* cost of the three options */
        int lowest_cost = 0; /* lowest cost */
        if ((i == 0)) { /* indel is the cost of an insertion or deletion */
            m[i][j].cost = (j * indel(' '));
            m[i][j].parent = ((j != 0) ? INSERT : (-1));
            return m[i][j].cost;
        }
        if ((j == 0)) {
            m[i][j].cost = (i * indel(' '));
            m[i][j].parent = DELETE;
            return m[i][j].cost;
        }
        /* match is the cost of a match/substitution */
        opt[MATCH] = (string_compare_r(s, t, (i - 1), (j - 1)) + match(s[i], t[j]));
        opt[INSERT] = (string_compare_r(s, t, i, (j - 1)) + indel(t[j]));
        opt[DELETE] = (string_compare_r(s, t, (i - 1), j) + indel(s[i]));
        lowest_cost = opt[MATCH];
        m[i][j].parent = MATCH;
        for (k = INSERT; (k <= DELETE); k++) {
            if ((opt[k] < lowest_cost)) {
                lowest_cost = opt[k];
                m[i][j].parent = k;
            }
        }
        return lowest_cost;
    }

    public static void reconstruct_path(char[] s, char[] t, int i, int j, Editdistance.cell[][] m) {
        if ((m[i][j].parent == (-1))) {
            return;
        }
        if ((m[i][j].parent == MATCH)) {
            reconstruct_path(s, t, (i - 1), (j - 1), m);
            match_out(s, t, i, j);
            return;
        }
        if ((m[i][j].parent == INSERT)) {
            reconstruct_path(s, t, i, (j - 1), m);
            insert_out(t, j);
            return;
        }
        if ((m[i][j].parent == DELETE)) {
            reconstruct_path(s, t, (i - 1), j, m);
            delete_out(s, i);
            return;
        }
    }

    public static void print_matrix(char[] s, char[] t, boolean costQ, Editdistance.cell[][] m) {
        int i = 0; /* counters */
        int j = 0;
        int x = 0; /* string lengths */
        int y = 0;
        x = C.strlen(s);
        y = C.strlen(t);
        C.printf("   ");
        for (i = 0; (i < y); i++) {
            C.printf("  %c", t[i]);
        }
        C.printf("\n");
        for (i = 0; (i < x); i++) {
            C.printf("%c: ", s[i]);
            for (j = 0; (j < y); j++) {
                if (costQ) {
                    C.printf(" %2d", m[i][j].cost);
                } else {
                    C.printf(" %2d", m[i][j].parent);
                }
            }
            C.printf("\n");
        }
    }

    public static int main() {
        int[] i = new int[]{0};
        int[] j = new int[]{0};
        int cost1 = 0;
        int cost2 = 0;
        char[] s = new char[(MAXLEN + 2)]; /* input strings */
        char[] t = new char[(MAXLEN + 2)];
        s[0] = (t[0] = ' ');
        if ((!((read_edit_string(s, MAXLEN) != 0)) || !((read_edit_string(t, MAXLEN) != 0)))) {
            C.fprintf("expected two strings of at most %d characters\n", MAXLEN);
            return 1;
        }
        cost1 = string_compare_r(s, t, (C.strlen(s) - 1), (C.strlen(t) - 1));
        C.printf("matching cost = %d \n", (cost2 = string_compare2(s, t, (C.strlen(s) - 1), (C.strlen(t) - 1), m)));
        if ((cost1 != cost2)) {
            C.printf("Editbrutes do not agree: cost1=%d cost2=%d\n", cost1, cost2);
        }
        print_matrix(s, t, true, m);
        C.printf("\n");
        print_matrix(s, t, false, m);
        goal_cell(s, t, i, j);
        C.printf("%d %d\n", i[0], j[0]);
        reconstruct_path(s, t, i[0], j[0], m);
        C.printf("\n");
        return 0;
    }

    public static void main(String[] args) {
        int status = main();
        if (status != 0) System.exit(status);
    }
}
