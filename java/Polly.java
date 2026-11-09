/*    polly.c

    Rank the desirability of suitors -- sorting example.
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

public class Polly {
    public static final int NAMELENGTH = 30; /* maximum length of name */
    public static final int NSUITORS = 100; /* maximum number of suitors */
    public static final int BESTHEIGHT = 180; /* best height in centimeters */
    public static final int BESTWEIGHT = 75; /* best weight in kilograms */
    public static class suitor {
        char[] first = new char[NAMELENGTH]; /* suitor's first name */
        char[] last = new char[NAMELENGTH]; /* suitor's last name */
        int height = 0; /* suitor's height */
        int weight = 0; /* suitor's weight */
    }
    public static Polly.suitor[] suitors = new Polly.suitor[NSUITORS]; /* database of suitors */
    static {
        for (int _i0 = 0; _i0 < NSUITORS; _i0++) {
            suitors[_i0] = new Polly.suitor();
        }
    }
    public static int nsuitors = 0; /* number of suitors */

    public static void read_suitors() {
        int height = 0;
        int weight = 0;
        nsuitors = 0;
        while (true) {
            int _read0 = C.scan("%s %s %d %d\n");
            if (_read0 > 0) C.strcpy(suitors[nsuitors].first, C.scanString(0));
            if (_read0 > 1) C.strcpy(suitors[nsuitors].last, C.scanString(1));
            if (_read0 > 2) height = C.scanInt(2);
            if (_read0 > 3) weight = C.scanInt(3);
            if (_read0 == -1) break;
            suitors[nsuitors].height = Math.abs((height - BESTHEIGHT));
            if ((weight > BESTWEIGHT)) {
                suitors[nsuitors].weight = (weight - BESTWEIGHT);
            } else {
                suitors[nsuitors].weight = (-weight);
            }
            nsuitors++;
        }
    }

    public static int main() {
        int i = 0; /* counter */
        read_suitors();
        java.util.Arrays.sort(suitors, 0, nsuitors, Polly::suitor_compare);
        for (i = 0; (i < nsuitors); i++) {
            C.printf("%s, %s\n", suitors[i].last, suitors[i].first);
        }
        return 0;
    }

    public static int suitor_compare(Object left, Object right) {
        Polly.suitor a = ((Polly.suitor)left);
        Polly.suitor b = ((Polly.suitor)right);
        int result = 0; /* result of comparsion */
        if ((a.height < b.height)) {
            return (-1);
        }
        if ((a.height > b.height)) {
            return 1;
        }
        if ((a.weight < b.weight)) {
            return (-1);
        }
        if ((a.weight > b.weight)) {
            return 1;
        }
        if (((result = C.strcmp(a.last, b.last)) != 0)) {
            return result;
        }
        return C.strcmp(a.first, b.first);
    }

    public static void main(String[] args) {
        int status = main();
        if (status != 0) System.exit(status);
    }
}
