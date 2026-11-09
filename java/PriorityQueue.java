/*    priority_queue.c

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

public class PriorityQueue {
    public static final int PQ_SIZE = 1000;
    public static class priority_queue {
        int[] q = new int[(PQ_SIZE + 1)]; /* body of queue */
        int n = 0; /* number of queue elements */
    }

    public static void pq_init(PriorityQueue.priority_queue q) {
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

    public static void pq_swap(PriorityQueue.priority_queue q, int i, int j) {
        int temp = 0; /* placeholder */
        temp = q.q[i];
        q.q[i] = q.q[j];
        q.q[j] = temp;
    }

    public static void bubble_up(PriorityQueue.priority_queue q, int p) {
        if ((pq_parent(p) == (-1))) {
            return; /* at root of heap, no parent */
        }
        if ((q.q[pq_parent(p)] > q.q[p])) {
            pq_swap(q, p, pq_parent(p));
            bubble_up(q, pq_parent(p));
        }
    }

    public static void bubble_down(PriorityQueue.priority_queue q, int p) {
        int c = 0; /* child index */
        int i = 0; /* counter */
        int min_index = 0; /* index of lightest child */
        c = pq_young_child(p);
        min_index = p;
        for (i = 0; (i <= 1); i++) {
            if (((c + i) <= q.n)) {
                if ((q.q[min_index] > q.q[(c + i)])) {
                    min_index = (c + i);
                }
            }
        }
        if ((min_index != p)) {
            pq_swap(q, p, min_index);
            bubble_down(q, min_index);
        }
    }

    public static void pq_insert(PriorityQueue.priority_queue q, int x) {
        if ((q.n >= PQ_SIZE)) {
            C.printf("Warning: priority queue overflow! \n");
        } else {
            q.n = (q.n + 1);
            q.q[q.n] = x;
            bubble_up(q, q.n);
        }
    }

    public static int extract_min(PriorityQueue.priority_queue q) {
        int min = (-1); /* minimum value */
        if ((q.n <= 0)) {
            C.printf("Warning: empty priority queue.\n");
        } else {
            min = q.q[1];
            q.q[1] = q.q[q.n];
            q.n = (q.n - 1);
            bubble_down(q, 1);
        }
        return min;
    }

    public static boolean empty_pq(PriorityQueue.priority_queue q) {
        return (q.n <= 0);
    }

    public static void print_pq(PriorityQueue.priority_queue q) {
        int i = 0; /* counter */
        for (i = 1; (i <= q.n); i++) {
            C.printf("%d ", q.q[i]);
        }
        C.printf("\n");
    }

    public static void make_heap_fast(PriorityQueue.priority_queue q, int[] s, int n) {
        int i = 0; /* counter */
        q.n = n;
        for (i = 0; (i < n); i++) {
            q.q[(i + 1)] = s[i];
        }
        for (i = (q.n / 2); (i >= 1); i--) {
            bubble_down(q, i);
        }
    }

    public static void make_heap(PriorityQueue.priority_queue q, int[] s, int n) {
        int i = 0; /* counter */
        pq_init(q);
        for (i = 0; (i < n); i++) {
            pq_insert(q, s[i]);
        }
    }

    public static int heap_compare(PriorityQueue.priority_queue q, int i, int count, int x) {
        if (((count <= 0) || (i > q.n))) {
            return count;
        }
        if ((q.q[i] < x)) {
            count = heap_compare(q, pq_young_child(i), (count - 1), x);
            count = heap_compare(q, (pq_young_child(i) + 1), count, x);
        }
        return count;
    }

}
