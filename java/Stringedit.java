/*    stringedit.c

    Compute the optimal alignment matching two strings
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

public class Stringedit {
    public static final int MAXLEN = 101; /* longest possible string */
    public static final int MATCH = 0; /* enumerated type symbol for match */
    public static final int INSERT = 1; /* enumerated type symbol for insert */
    public static final int DELETE = 2; /* enumerated type symbol for delete */
    public static Editdistance.cell[][] m = new Editdistance.cell[(MAXLEN + 1)][(MAXLEN + 1)];
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

    public static void row_init(int i, Editdistance.cell[][] m) { /* what is m[0][i]? */
        m[0][i].cost = i;
        if ((i > 0)) {
            m[0][i].parent = INSERT;
        } else {
            m[0][i].parent = (-1);
        }
    }

    public static void column_init(int i, Editdistance.cell[][] m) { /* what is m[i][0]? */
        m[i][0].cost = i;
        if ((i > 0)) {
            m[i][0].parent = DELETE;
        } else {
            m[0][i].parent = (-1);
        }
    }

    public static void match_out(char[] s, char[] t, int i, int j) {
        if ((s[i] == t[j])) {
            System.out.print("M");
        } else {
            System.out.print("S");
        }
    }

    public static void insert_out(char[] t, int j) {
        System.out.print("I");
    }

    public static void delete_out(char[] s, int i) {
        System.out.print("D");
    }

    public static int main() {
        Editdistance.callbacks = new Editdistance.Callbacks() {
            public void row_init(int i, Editdistance.cell[][] m) { Stringedit.row_init(i, m); }
            public void column_init(int i, Editdistance.cell[][] m) { Stringedit.column_init(i, m); }
            public int match(char c, char d) { return Stringedit.match(c, d); }
            public int indel(char c) { return Stringedit.indel(c); }
            public void goal_cell(char[] s, char[] t, int[] i, int[] j) { Stringedit.goal_cell(s, t, i, j); }
            public void match_out(char[] s, char[] t, int i, int j) { Stringedit.match_out(s, t, i, j); }
            public void insert_out(char[] t, int j) { Stringedit.insert_out(t, j); }
            public void delete_out(char[] s, int i) { Stringedit.delete_out(s, i); }
        };
        int[] i = new int[]{0};
        int[] j = new int[]{0};
        char[] s = new char[(MAXLEN + 2)]; /* input strings */
        char[] t = new char[(MAXLEN + 2)];
        s[0] = (t[0] = ' ');
        if (((read_edit_string(s, MAXLEN) == 0) || (read_edit_string(t, MAXLEN) == 0))) {
            System.err.printf(Locale.US, "expected two strings of at most %d characters\n", MAXLEN);
            return 1;
        }
        System.out.printf(Locale.US, "matching cost = %d \n", Editdistance.string_compare(s, t, m));
        Editdistance.print_matrix(s, t, true, m);
        System.out.print("\n");
        Editdistance.print_matrix(s, t, false, m);
        goal_cell(s, t, i, j);
        System.out.printf(Locale.US, "%d %d\n", i[0], j[0]);
        Editdistance.reconstruct_path(s, t, i[0], j[0], m);
        System.out.print("\n");
        return 0;
    }

    public static void main(String[] args) {
        int status = main();
        if (status != 0) System.exit(status);
    }
}
