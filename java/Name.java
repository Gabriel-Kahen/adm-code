/*    name.c

      Corporate name changing program -- string example
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

public class Name {
    public static final int MAXLEN = 1001; /* longest possible string */
    public static final int MAXCHANGES = 101; /* maximum number of name changes */
    public static char[][][] mergers = new char[MAXCHANGES][2][MAXLEN]; /* store before/after corporate names */
    public static int nmergers = 0; /* the number of different name changes */

    public static void read_quoted_string(char[] s) {
        int i = 0; /* counter */
        char c = '\000'; /* latest character */
        while (((c = (char)(C.getchar())) != '\"')) {
            ;
        }
        while (((c = (char)(C.getchar())) != '\"')) {
            s[i] = c;
            i = (i + 1);
        }
        s[i] = '\000';
    }

    public static void read_changes() {
        int i = 0; /* counter */
        int _read0 = C.scan("%d\n");
        if (_read0 > 0) nmergers = C.scanInt(0);
        for (i = 0; (i < nmergers); i++) {
            read_quoted_string(mergers[i][0]);
            read_quoted_string(mergers[i][1]);
        }
    }

    /*    Replace the substring of length xlen starting at position pos in
          string s with the contents of string y.
    */
    public static void replace_x_with_y(char[] s, int pos, int xlen, char[] y) {
        int i = 0; /* counter */
        int slen = 0; /* lengths of relevant strings */
        int ylen = 0;
        slen = C.strlen(s);
        ylen = C.strlen(y);
        if ((xlen >= ylen)) {
            for (i = (pos + xlen); (i <= slen); i++) {
                s[(i + (ylen - xlen))] = s[i];
            }
        } else {
            for (i = slen; (i >= (pos + xlen)); i--) {
                s[(i + (ylen - xlen))] = s[i];
            }
        }
        for (i = 0; (i < ylen); i++) {
            s[(pos + i)] = y[i];
        }
    }

    /*    Return the position of the first occurrence of the pattern p
          in the text t, and -1 if it does not occur.
    */
    public static int findmatch(char[] p, char[] t) {
        return findmatch(p, t, 0);
    }

    public static int findmatch(char[] p, char[] t, int offset) {
        int i = 0; /* counters */
        int j = 0;
        int plen = 0; /* string lengths */
        int tlen = 0;
        plen = C.strlen(p);
        tlen = C.strlen(t, offset);
        for (i = 0; (i <= (tlen - plen)); i = (i + 1)) {
            j = 0;
            while (((j < plen) && (t[(offset + i + j)] == p[j]))) {
                j = (j + 1);
            }
            if ((j == plen)) {
                return i; /* location of the first match */
            }
        }
        return (-1); /* there is no match */
    }

    public static int main() {
        char[] s = new char[MAXLEN];
        char c = '\000'; /* input character */
        int nlines = 0; /* number of lines in text */
        int i = 0; /* counters */
        int j = 0;
        int pos = 0; /* position of pattern in string */
        read_changes();
        int _read1 = C.scan("%d\n");
        if (_read1 > 0) nlines = C.scanInt(0);
        for (i = 1; (i <= nlines); i = (i + 1)) {
            /* read text line */
            j = 0;
            while (((c = (char)(C.getchar())) != '\n')) {
                s[j] = c;
                j = (j + 1);
            }
            s[j] = '\000';
            for (j = 0; (j < nmergers); j++) {
                int cursor = 0;
                int oldlen = C.strlen(mergers[j][0]);
                int newlen = C.strlen(mergers[j][1]);
                if ((oldlen == 0)) {
                    System.err.print("A name to replace must not be empty.\n");
                    return 1;
                }
                while (((pos = findmatch(mergers[j][0], s, cursor)) != (-1))) {
                    pos += cursor;
                    if ((((C.strlen(s) - oldlen) + newlen) >= MAXLEN)) {
                        System.err.print("Renamed text exceeds the line capacity.\n");
                        return 1;
                    }
                    replace_x_with_y(s, pos, oldlen, mergers[j][1]);
                    cursor = (pos + newlen);
                }
            }
            C.printf("%s\n", s);
        }
        return 0;
    }

    public static void main(String[] args) {
        int status = main();
        if (status != 0) System.exit(status);
    }
}
