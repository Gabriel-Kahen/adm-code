/*    set_union.c

    Implementation of a heap / priority queue abstract data type.
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

public class SetUnion {
    public static final int SET_SIZE = 1000;
    public static class union_find {
        int[] p = new int[(SET_SIZE + 1)]; /* parent element */
        int[] size = new int[(SET_SIZE + 1)]; /* number of elements in subtree i */
        int n = 0; /* number of elements in set */
    }

    public static void union_find_init(SetUnion.union_find s, int n) {
        int i = 0; /* counter */
        for (i = 1; (i <= n); i++) {
            s.p[i] = i;
            s.size[i] = 1;
        }
        s.n = n;
    }

    public static int find(SetUnion.union_find s, int x) {
        if ((s.p[x] == x)) {
            return x;
        }
        return find(s, s.p[x]);
    }

    public static void union_sets(SetUnion.union_find s, int s1, int s2) {
        int r1 = 0; /* roots of sets */
        int r2 = 0;
        r1 = find(s, s1);
        r2 = find(s, s2);
        if ((r1 == r2)) {
            return; /* already in same set */
        }
        if ((s.size[r1] >= s.size[r2])) {
            s.size[r1] = (s.size[r1] + s.size[r2]);
            s.p[r2] = r1;
        } else {
            s.size[r2] = (s.size[r1] + s.size[r2]);
            s.p[r1] = r2;
        }
    }

    public static boolean same_component(SetUnion.union_find s, int s1, int s2) {
        return (find(s, s1) == find(s, s2));
    }

    public static void print_union_find(SetUnion.union_find s) {
        int i = 0; /* counter */
        for (i = 1; (i <= s.n); i++) {
            C.printf("%i  set=%d size=%d \n", i, s.p[i], s.size[i]);
        }
        C.printf("\n");
    }

}
