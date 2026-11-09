/** Same state observations as structures.c, through the translated routines. */
public class Structures {
    public static void main(String[] args) {
        Queue.queue q = new Queue.queue();
        Stack.stack s = new Stack.stack();
        PriorityQueue.priority_queue h = new PriorityQueue.priority_queue();
        SetUnion.union_find sets = new SetUnion.union_find();
        Graph.graph g = new Graph.graph();
        int[] values = {4, 1, 7, 1, -3, 9, 2};
        long sum = 0;

        Queue.init_queue(q);
        for (int i = 0; i < Queue.QUEUESIZE; i++) Queue.enqueue(q, i);
        for (int i = 0; i < 17; i++) Queue.dequeue(q);
        for (int i = Queue.QUEUESIZE; i < Queue.QUEUESIZE + 17; i++) Queue.enqueue(q, i);
        System.out.printf("queue first=%d last=%d count=%d head=%d tail=%d%n",
            q.first, q.last, q.count, Queue.headq(q), q.q[q.last]);
        while (Queue.empty_queue(q) == 0) sum += Queue.dequeue(q);
        System.out.printf("queue sum=%d count=%d%n", sum, q.count);

        Stack.init_stack(s);
        for (int i = 0; i < Stack.STACKSIZE; i++) Stack.push(s, i);
        Stack.push(s, Stack.STACKSIZE);
        int first = Stack.pop(s);
        int second = Stack.pop(s);
        System.out.printf("stack first=%d second=%d top=%d count=%d%n", first, second, s.top, s.count);

        PriorityQueue.pq_init(h);
        for (int value : values) PriorityQueue.pq_insert(h, value);
        System.out.print("heap array: ");
        PriorityQueue.print_pq(h);
        System.out.printf("heap_compare=%d%n", PriorityQueue.heap_compare(h, 1, 4, 3));
        System.out.print("heap sorted: ");
        while (!PriorityQueue.empty_pq(h)) System.out.printf("%d ", PriorityQueue.extract_min(h));
        System.out.println();

        SetUnion.union_find_init(sets, 6);
        SetUnion.union_sets(sets, 2, 3);
        SetUnion.union_sets(sets, 4, 5);
        SetUnion.union_sets(sets, 4, 6);
        SetUnion.union_sets(sets, 2, 4);
        System.out.printf("union root=%d%n", SetUnion.find(sets, 3));
        SetUnion.print_union_find(sets);

        Graph.initialize_graph(g, false);
        g.nvertices = 4;
        Graph.insert_edge(g, 1, 2, false);
        Graph.insert_edge(g, 1, 3, false);
        Graph.insert_edge(g, 1, 4, false);
        Graph.delete_edge(g, 1, 3, false);
        Graph.print_graph(g);
        System.out.printf("graph nedges=%d degree1=%d%n", g.nedges, g.degree[1]);
    }
}
