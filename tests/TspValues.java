/** Exercise the original TSP queue's struct-by-value boundaries. */
public class TspValues {
    static void printRecord(String label, TspAstar.tsp_solution s) {
        System.out.printf("%s cost=%.1f n=%d p=%d,%d,%d%n", label, s.cost, s.n, s.p[1], s.p[2], s.p[3]);
    }

    public static void main(String[] args) {
        TspPq.priority_queue q = new TspPq.priority_queue();
        TspAstar.tsp_solution source = new TspAstar.tsp_solution();
        source.cost = 8;
        source.n = 3;
        source.p[1] = 1;
        source.p[2] = 2;
        source.p[3] = 3;
        TspPq.pq_init(q);
        TspPq.pq_insert(q, source);
        source.cost = 80;
        source.n = 1;
        source.p[1] = 9;
        printRecord("insert-copy", q.q[1]);
        source.cost = 4;
        source.n = 3;
        source.p[1] = 3;
        source.p[2] = 2;
        source.p[3] = 1;
        TspPq.pq_insert(q, source);
        source.cost = 40;
        source.p[1] = 9;
        TspAstar.tsp_solution peek = TspPq.top_pq(q);
        peek.cost = -1;
        peek.n = 1;
        peek.p[1] = 99;
        printRecord("modified-top", peek);
        printRecord("top-copy", q.q[1]);
        printRecord("heap-second", q.q[2]);
        TspAstar.tsp_solution extracted = TspPq.extract_min(q);
        printRecord("extracted", extracted);
        extracted.cost = -2;
        extracted.n = 1;
        extracted.p[2] = 99;
        printRecord("modified-extracted", extracted);
        printRecord("extract-copy", q.q[1]);
        extracted = TspPq.extract_min(q);
        printRecord("last", extracted);
        System.out.printf("empty size=%d flag=%d%n", q.n, TspPq.empty_pq(q));
    }
}
