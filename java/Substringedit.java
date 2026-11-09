/*    substringedit.c

    Approximately match one string as a substring of another, where is s in t?
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

public class Substringedit {
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

    /*    For normal edit distance computation  */
    public static void goal_cell(char[] s, char[] t, int[] i, int[] j) {
        int k = 0; /* counter */
        i[0] = (C.strlen(s) - 1);
        j[0] = 0;
        for (k = 1; (k < C.strlen(t)); k++) {
            if ((m[i[0]][k].cost < m[i[0]][j[0]].cost)) {
                j[0] = k;
            }
        }
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
        m[0][i].cost = 0; /* NOTE CHANGE */
        m[0][i].parent = (-1); /* NOTE CHANGE */
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

    public static int main() {
        Editdistance.callbacks = new Editdistance.Callbacks() {
            public void row_init(int i, Editdistance.cell[][] m) { Substringedit.row_init(i, m); }
            public void column_init(int i, Editdistance.cell[][] m) { Substringedit.column_init(i, m); }
            public int match(char c, char d) { return Substringedit.match(c, d); }
            public int indel(char c) { return Substringedit.indel(c); }
            public void goal_cell(char[] s, char[] t, int[] i, int[] j) { Substringedit.goal_cell(s, t, i, j); }
            public void match_out(char[] s, char[] t, int i, int j) { Substringedit.match_out(s, t, i, j); }
            public void insert_out(char[] t, int j) { Substringedit.insert_out(t, j); }
            public void delete_out(char[] s, int i) { Substringedit.delete_out(s, i); }
        };
        int[] i = new int[]{0};
        int[] j = new int[]{0};
        char[] s = new char[(MAXLEN + 2)]; /* input strings */
        char[] t = new char[(MAXLEN + 2)];
        s[0] = (t[0] = ' ');
        if ((!((read_edit_string(s, MAXLEN) != 0)) || !((read_edit_string(t, MAXLEN) != 0)))) {
            C.fprintf("expected two strings of at most %d characters\n", MAXLEN);
            return 1;
        }
        C.printf("matching cost = %d \n", Editdistance.string_compare(s, t, m));
        Editdistance.print_matrix(s, t, true, m);
        C.printf("\n");
        Editdistance.print_matrix(s, t, false, m);
        goal_cell(s, t, i, j);
        C.printf("%d %d\n", i[0], j[0]);
        Editdistance.reconstruct_path(s, t, i[0], j[0], m);
        C.printf("\n");
        return 0;
    }

    public static void main(String[] args) {
        int status = main();
        if (status != 0) System.exit(status);
    }
}
