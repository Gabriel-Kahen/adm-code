/** Check pointer-offset shuffling and the original transition/undo steps. */
public class TspMoves {
    public static void main(String[] args) {
        Tsp.tsp_solution s = new Tsp.tsp_solution();
        Tsp.tsp_instance t = new Tsp.tsp_instance();
        Tsp.initialize_solution(4, s);
        s.p[0] = -7;
        s.p[5] = -9;
        Tsp.random_solution(s);
        int[] prefix = java.util.Arrays.copyOfRange(s.p, 1, 4);
        java.util.Arrays.sort(prefix);
        System.out.printf("random prefix=%d,%d,%d last=%d left=%d right=%d%n",
                          prefix[0], prefix[1], prefix[2], s.p[4], s.p[0], s.p[5]);

        t.n = 4;
        int[][] points = {{0, 0}, {3, 0}, {3, 4}, {0, 4}};
        for (int i = 1; i <= 4; i++) {
            t.p[i].x = points[i - 1][0];
            t.p[i].y = points[i - 1][1];
        }
        Tsp.initialize_solution(4, s);
        System.out.printf("initial cost=%.1f%n", Tsp.solution_cost(s, t));
        double delta = Tsp.transition(s, t, 1, 2);
        System.out.printf("forward delta=%.1f cost=%.1f%n", delta, Tsp.solution_cost(s, t));
        delta = Tsp.transition(s, t, 2, 1);
        System.out.printf("reverse delta=%.1f cost=%.1f%n", delta, Tsp.solution_cost(s, t));
        System.out.printf("tour %d %d %d %d%n", s.p[1], s.p[2], s.p[3], s.p[4]);

        // Five cities give the nonadjacent swap a genuine cost change.
        t.n = 5;
        t.p[5].x = 8;
        t.p[5].y = 7;
        Tsp.initialize_solution(5, s);
        int[][] moves = {{1, 5}, {5, 1}, {1, 3}, {3, 1}, {2, 2}, {2, 2}};
        for (int[] move : moves) {
            delta = Tsp.transition(s, t, move[0], move[1]);
            System.out.printf("move %d,%d delta=%.1f cost=%.1f tour",
                              move[0], move[1], delta, Tsp.solution_cost(s, t));
            for (int j = 1; j <= s.n; j++) {
                System.out.printf(" %d", s.p[j]);
            }
            System.out.println();
        }

        // The C pointer starts at p[1]; its n-1 prefix can be empty.
        for (int n = 1; n <= 2; n++) {
            Tsp.initialize_solution(n, s);
            s.p[0] = -7;
            s.p[n + 1] = -9;
            Tsp.random_solution(s);
            System.out.printf("small n=%d left=%d tour", n, s.p[0]);
            for (int j = 1; j <= n; j++) {
                System.out.printf(" %d", s.p[j]);
            }
            System.out.printf(" right=%d%n", s.p[n + 1]);
        }
    }
}
