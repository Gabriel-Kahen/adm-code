/*    queue.c

    Implementation of a FIFO queue abstract data type.
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

public class Queue {
    public static final int QUEUESIZE = 1000;
    public static class queue {
        int[] q = new int[(QUEUESIZE + 1)]; /* body of queue */
        int first = 0; /* position of first element */
        int last = 0; /* position of last element */
        int count = 0; /* number of queue elements */
    }

    public static void init_queue(Queue.queue q) {
        q.first = 0;
        q.last = (QUEUESIZE - 1);
        q.count = 0;
    }

    public static void enqueue(Queue.queue q, int x) {
        if ((q.count >= QUEUESIZE)) {
            C.printf("Warning: queue overflow enqueue x=%d\n", x);
        } else {
            q.last = ((q.last + 1) % QUEUESIZE);
            q.q[q.last] = x;
            q.count = (q.count + 1);
        }
    }

    public static int dequeue(Queue.queue q) {
        int x = 0;
        if ((q.count <= 0)) {
            C.printf("Warning: empty queue dequeue.\n");
        }
        x = q.q[q.first];
        q.first = ((q.first + 1) % QUEUESIZE);
        q.count = (q.count - 1);
        return x;
    }

    public static int headq(Queue.queue q) {
        return q.q[q.first];
    }

    public static int empty_queue(Queue.queue q) {
        if ((q.count <= 0)) {
            return 1;
        }
        return 0;
    }

    public static void print_queue(Queue.queue q) {
        int i = 0;
        i = q.first;
        while ((i != q.last)) {
            C.printf("%d ", q.q[i]);
            i = ((i + 1) % QUEUESIZE);
        }
        C.printf("%2d ", q.q[i]);
        C.printf("\n");
    }

}
