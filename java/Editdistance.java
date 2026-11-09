/*	editdistance.c

	A generic implementation of string comparison via dynamic programming
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

public class Editdistance {
    public interface Callbacks {
        void row_init(int i, cell[][] m);
        void column_init(int i, cell[][] m);
        int match(char c, char d);
        int indel(char c);
        void goal_cell(char[] s, char[] t, int[] i, int[] j);
        void match_out(char[] s, char[] t, int i, int j);
        void insert_out(char[] t, int j);
        void delete_out(char[] s, int i);
    }
    public static Callbacks callbacks;

    public static final int MAXLEN = 101; /* longest possible string */
    public static final int MATCH = 0; /* enumerated type symbol for match */
    public static final int INSERT = 1; /* enumerated type symbol for insert */
    public static final int DELETE = 2; /* enumerated type symbol for delete */
    public static class cell {
        int cost = 0; /* cost of reaching this cell */
        int parent = 0; /* parent cell */
    }

    public static int string_compare(char[] s, char[] t, Editdistance.cell[][] m) {
        int[] i = new int[]{0};
        int[] j = new int[]{0};
        int k = 0;
        int[] opt = new int[3]; /* cost of the three options */
        for (i[0] = 0; (i[0] <= MAXLEN); i[0]++) {
            callbacks.row_init(i[0], m);
            callbacks.column_init(i[0], m);
        }
        for (i[0] = 1; (i[0] < C.strlen(s)); i[0]++) {
            for (j[0] = 1; (j[0] < C.strlen(t)); j[0]++) {
                opt[MATCH] = (m[(i[0] - 1)][(j[0] - 1)].cost + callbacks.match(s[i[0]], t[j[0]]));
                opt[INSERT] = (m[i[0]][(j[0] - 1)].cost + callbacks.indel(t[j[0]]));
                opt[DELETE] = (m[(i[0] - 1)][j[0]].cost + callbacks.indel(s[i[0]]));
                m[i[0]][j[0]].cost = opt[MATCH];
                m[i[0]][j[0]].parent = MATCH;
                for (k = INSERT; (k <= DELETE); k++) {
                    if ((opt[k] < m[i[0]][j[0]].cost)) {
                        m[i[0]][j[0]].cost = opt[k];
                        m[i[0]][j[0]].parent = k; /* counters */
                    }
                }
            }
        }
        callbacks.goal_cell(s, t, i, j);
        return m[i[0]][j[0]].cost;
    }

    public static void reconstruct_path(char[] s, char[] t, int i, int j, Editdistance.cell[][] m) {
        if ((m[i][j].parent == (-1))) {
            return;
        }
        if ((m[i][j].parent == MATCH)) {
            reconstruct_path(s, t, (i - 1), (j - 1), m);
            callbacks.match_out(s, t, i, j);
            return;
        }
        if ((m[i][j].parent == INSERT)) {
            reconstruct_path(s, t, i, (j - 1), m);
            callbacks.insert_out(t, j);
            return;
        }
        if ((m[i][j].parent == DELETE)) {
            reconstruct_path(s, t, (i - 1), j, m);
            callbacks.delete_out(s, i);
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

}
