/*    tsp.c

    Heuristics for solving TSP
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

public class Tsp {
    public static final int NMAX = 1001;
    public static final boolean TRACE_OUTPUT = false; /* print the swaps as they happen */
    public static final int PRINT_FREQUENCY = 10000; /* how often we report progress */
    public static final int REPEAT_COUNT = 1;
    public static final int INITIAL_TEMPERATURE = 1;
    public static final double COOLING_FRACTION = 0.998;
    public static final int COOLING_STEPS = 1000;
    public static final int STEPS_PER_TEMP = 1000;
    public static final double E = 2.718; /* approximation retained for historical examples */
    public static final double K = 0.01;
    public static final String ERROR = "ERROR"; /* string denoting error id */
    public static final double ERROR_VALUE = 0.0; /* float denoting error value */
    public static class point {
        int x = 0; /* x and y coordinates of point */
        int y = 0; /* x and y coordinates of point */
    }
    public static class tsp_instance {
        int n = 0; /* how many points in problem? */
        Tsp.point[] p = new Tsp.point[(NMAX + 1)]; /* array of points */
        {
            for (int _i0 = 0; _i0 < (NMAX + 1); _i0++) {
                p[_i0] = new Tsp.point();
            }
        }
    }
    public static class tsp_solution {
        double cost = 0; /* lower bound on full cost solution */
        int n = 0; /* how many elements in permutation? */
        int[] p = new int[(NMAX + 1)]; /* array of indices */
    }

    public static void read_tsp(Tsp.tsp_instance t) {
        int i = 0; /* counters */
        int j = 0;
        int _read0 = C.scan("%d\n");
        if (_read0 > 0) t.n = C.scanInt(0);
        for (i = 1; (i <= t.n); i++) {
            int _read1 = C.scan("%d %d %d\n");
            if (_read1 > 0) j = C.scanInt(0);
            if (_read1 > 1) t.p[i].x = C.scanInt(1);
            if (_read1 > 2) t.p[i].y = C.scanInt(2);
        }
    }

    public static void print_tsp(Tsp.tsp_instance t) {
        int i = 0; /* counter */
        for (i = 1; (i <= t.n); i++) {
            System.out.printf(Locale.US, "%d %d %d\n", i, t.p[i].x, t.p[i].y);
        }
    }

    public static int sq(int x) {
        return (x * x);
    }

    public static double distance(Tsp.tsp_solution s, int x, int y, Tsp.tsp_instance t) {
        int i = 0;
        int j = 0;
        i = x;
        j = y;
        if ((i == (t.n + 1))) {
            i = 1;
        }
        if ((j == (t.n + 1))) {
            j = 1;
        }
        if ((i == 0)) {
            i = t.n;
        }
        if ((j == 0)) {
            j = t.n;
        }
        return Math.hypot((((double)t.p[s.p[i]].x) - t.p[s.p[j]].x), (((double)t.p[s.p[i]].y) - t.p[s.p[j]].y));
    }

    public static double solution_cost(Tsp.tsp_solution s, Tsp.tsp_instance t) {
        int i = 0; /* counter */
        double cost = 0; /* cost of solution */
        cost = distance(s, t.n, 1, t);
        for (i = 1; (i < t.n); i++) {
            cost = (cost + distance(s, i, (i + 1), t));
        }
        return cost;
    }

    public static void initialize_solution(int n, Tsp.tsp_solution s) {
        int i = 0; /* counter */
        s.n = n;
        for (i = 1; (i <= n); i++) {
            s.p[i] = i;
        }
    }

    public static void copy_solution(Tsp.tsp_solution s, Tsp.tsp_solution t) {
        int i = 0; /* counter */
        t.n = s.n;
        for (i = 1; (i <= s.n); i++) {
            t.p[i] = s.p[i];
        }
    }

    public static void print_solution(Tsp.tsp_solution s) {
        int i = 0; /* counter */
        for (i = 1; (i <= s.n); i++) {
            System.out.printf(Locale.US, " %d", s.p[i]);
        }
        System.out.print("\n------------------------------------------------------\n");
    }

    public static void read_solution(Tsp.tsp_solution s) {
        int i = 0; /* counter */
        int _read2 = C.scan("%d\n");
        if (_read2 > 0) s.n = C.scanInt(0);
        for (i = 1; (i <= s.n); i++) {
            int _read3 = C.scan("%d");
            if (_read3 > 0) s.p[i] = C.scanInt(0);
        }
    }

    public static void random_solution(Tsp.tsp_solution s) {
        Random.random_permutation(s.p, 1, (s.n - 1));
    }

    public static double transition(Tsp.tsp_solution s, Tsp.tsp_instance t, int i, int j) {
        double was = 0; /* before and after costs */
        double willbe = 0;
        boolean neighbors = false;
        neighbors = false;
        if ((i == j)) {
            return 0.0;
        }
        if ((i > j)) {
            return transition(s, t, j, i);
        }
        if ((i == (j - 1))) {
            neighbors = true;
        }
        if (((i == 1) && (j == s.n))) {
            int temporary = i;
            i = j;
            j = temporary;
            neighbors = true;
        }
        if (neighbors) { /* i,j neighboring tour positions? */
            was = (distance(s, (i - 1), i, t) + distance(s, j, (j + 1), t));
        } else {
            was = (((distance(s, (i - 1), i, t) + distance(s, i, (i + 1), t)) + distance(s, (j - 1), j, t)) + distance(s, j, (j + 1), t));
        }
        Random.swap(s.p, i, s.p, j);
        if (neighbors) {
            willbe = (distance(s, (i - 1), i, t) + distance(s, j, (j + 1), t));
        } else {
            willbe = (((distance(s, (i - 1), i, t) + distance(s, i, (i + 1), t)) + distance(s, (j - 1), j, t)) + distance(s, j, (j + 1), t));
        }
        return (willbe - was);
    }

    public static int main() {
        Tsp.tsp_instance t = new Tsp.tsp_instance(); /* tsp points */
        Tsp.tsp_solution s = new Tsp.tsp_solution(); /* tsp solution */
        read_tsp(t);
        read_solution(s);
        System.out.printf(Locale.US, "OPTIMAL SOLUTION COST = %7.1f\n", solution_cost(s, t));
        print_solution(s);
        initialize_solution(t.n, s);
        System.out.printf(Locale.US, "solution_cost = %7.1f\n", solution_cost(s, t));
        print_solution(s);
        Annealing.solution_count = 0;
        Annealing.random_sampling(t, 10000, s);
        System.out.printf(Locale.US, "random_sampling %d iterations, cost = %7.1f\n", Annealing.solution_count, solution_cost(s, t));
        print_solution(s);
        initialize_solution(t.n, s);
        System.out.printf(Locale.US, "solution_cost = %7.1f\n", solution_cost(s, t));
        print_solution(s);
        Annealing.solution_count = 0;
        Annealing.repeated_hill_climbing(t, 40, s);
        System.out.printf(Locale.US, "repeated hill_climbing %d iterations, cost = %7.1f\n", Annealing.solution_count, solution_cost(s, t));
        print_solution(s);
        initialize_solution(t.n, s);
        System.out.printf(Locale.US, "solution_cost = %7.1f\n", solution_cost(s, t));
        print_solution(s);
        Annealing.solution_count = 0;
        Annealing.repeated_annealing(t, 3, s);
        System.out.printf(Locale.US, "repeated annealing %d iterations, cost = %7.1f\n", Annealing.solution_count, solution_cost(s, t));
        print_solution(s);
        return 0;
    }

    public static void main(String[] args) {
        int status = main();
        if (status != 0) System.exit(status);
    }
}
