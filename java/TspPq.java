/*    TSP priority_queue.c

    Implementation of a heap / priority queue abstract data type,
    adjusted for complete records with key and data fields.
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

public class TspPq {
    public static final int NMAX = 20;
    public static final int PQ_SIZE = 400000;
    public static class priority_queue {
        TspAstar.tsp_solution[] q = new TspAstar.tsp_solution[(PQ_SIZE + 1)]; /* body of queue */
        {
            for (int _i0 = 0; _i0 < (PQ_SIZE + 1); _i0++) {
                q[_i0] = new TspAstar.tsp_solution();
            }
        }
        int n = 0; /* number of queue elements */
    }

    public static void pq_init(TspPq.priority_queue q) {
        q.n = 0;
    }

    public static int pq_parent(int n) {
        if ((n == 1)) {
            return (-1);
        }
        return (n / 2); /* implicitly take floor(n/2) */
    }

    public static int pq_young_child(int n) {
        return (2 * n);
    }

    public static void pq_swap(TspPq.priority_queue q, int i, int j) {
        TspAstar.tsp_solution temp = new TspAstar.tsp_solution(); /* placeholder */
        temp.set(q.q[i]);
        q.q[i].set(q.q[j]);
        q.q[j].set(temp);
    }

    public static void bubble_up(TspPq.priority_queue q, int p) {
        if ((pq_parent(p) == (-1))) {
            return; /* at root of heap, no parent */
        }
        if ((q.q[pq_parent(p)].cost > q.q[p].cost)) {
            pq_swap(q, p, pq_parent(p));
            bubble_up(q, pq_parent(p));
        }
    }

    public static void bubble_down(TspPq.priority_queue q, int p) {
        int c = 0; /* child index */
        int i = 0; /* counter */
        int min_index = 0; /* index of lightest child */
        c = pq_young_child(p);
        min_index = p;
        for (i = 0; (i <= 1); i++) {
            if (((c + i) <= q.n)) {
                if ((q.q[min_index].cost > q.q[(c + i)].cost)) {
                    min_index = (c + i);
                }
            }
        }
        if ((min_index != p)) {
            pq_swap(q, p, min_index);
            bubble_down(q, min_index);
        }
    }

    public static void pq_insert(TspPq.priority_queue q, TspAstar.tsp_solution x) {
        if ((q.n >= PQ_SIZE)) {
            System.err.print("TSP priority queue capacity exceeded\n");
            System.exit(1);
        } else {
            q.n = (q.n + 1);
            q.q[q.n].set(x);
            bubble_up(q, q.n);
        }
    }

    public static TspAstar.tsp_solution extract_min(TspPq.priority_queue q) {
        TspAstar.tsp_solution min = new TspAstar.tsp_solution(); /* minimum value */
        if ((q.n <= 0)) {
            System.err.print("Cannot extract from an empty priority queue.\n");
            System.exit(1);
        }
        min.set(q.q[1]);
        q.q[1].set(q.q[q.n]);
        q.n = (q.n - 1);
        bubble_down(q, 1);
        return min;
    }

    public static TspAstar.tsp_solution top_pq(TspPq.priority_queue q) {
        if ((q.n <= 0)) {
            System.err.print("Cannot inspect an empty priority queue.\n");
            System.exit(1);
        }
        return q.q[1].copy();
    }

    public static int empty_pq(TspPq.priority_queue q) {
        return ((q.n <= 0) ? 1 : 0);
    }

    public static void print_pq(TspPq.priority_queue q) {
        int i = 0; /* counter */
        for (i = 1; (i <= q.n); i++) {
            System.out.printf(Locale.US, "%7.1f ", q.q[i].cost);
        }
        System.out.print("\n");
    }

    public static void make_heap_fast(TspPq.priority_queue q, TspAstar.tsp_solution[] s, int n) {
        int i = 0; /* counter */
        q.n = n;
        for (i = 0; (i < n); i++) {
            q.q[(i + 1)].set(s[i]);
        }
        for (i = (q.n / 2); (i >= 1); i--) {
            bubble_down(q, i);
        }
    }

    public static void make_heap(TspPq.priority_queue q, TspAstar.tsp_solution[] s, int n) {
        int i = 0; /* counter */
        pq_init(q);
        for (i = 0; (i < n); i++) {
            pq_insert(q, s[i]);
        }
    }

    public static int heap_compare(TspPq.priority_queue q, int i, int count, int x) {
        if (((count <= 0) || (i > q.n))) {
            return count;
        }
        if ((q.q[i].cost < x)) {
            count = heap_compare(q, pq_young_child(i), (count - 1), x);
            count = heap_compare(q, (pq_young_child(i) + 1), count, x);
        }
        return count;
    }

}
