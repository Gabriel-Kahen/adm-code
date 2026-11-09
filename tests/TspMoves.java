/** Check pointer-offset shuffling and the original transition/undo steps. */
public class TspMoves {
    public static void main(String[] args) {
        Tsp.tsp_solution s = new Tsp.tsp_solution();
        Tsp.tsp_instance t = new Tsp.tsp_instance();
        Tsp.initialize_solution(4, s);
        Tsp.random_solution(s);
        int[] prefix = java.util.Arrays.copyOfRange(s.p, 1, 4);
        java.util.Arrays.sort(prefix);
        System.out.printf("random prefix=%d,%d,%d last=%d%n", prefix[0], prefix[1], prefix[2], s.p[4]);

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
    }
}
