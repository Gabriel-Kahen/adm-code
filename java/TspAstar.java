/*    tsp-astar.c

    Solve TSP to optimality via backtracking and later A* search.
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

public class TspAstar {
    public static final int NMAX = 20;
    public static final int PQ_SIZE = 400000;
    public static final int MAXCANDIDATES = 100; /* max possible next extensions */
    public static final double MAXD = 100000.0; /* largest possible distance */
    public static class point {
        int x = 0; /* x and y coordinates of point */
        int y = 0; /* x and y coordinates of point */
    }
    public static class tsp_instance {
        int n = 0; /* how many points in problem? */
        TspAstar.point[] p = new TspAstar.point[(NMAX + 1)]; /* array of points */
        {
            for (int _i0 = 0; _i0 < (NMAX + 1); _i0++) {
                p[_i0] = new TspAstar.point();
            }
        }
    }
    public static class tsp_solution {
        double cost = 0; /* lower bound on full cost solution */
        int n = 0; /* how many elements in permutation? */
        int[] p = new int[(NMAX + 1)]; /* array of indices */
        public void set(tsp_solution source) {
            cost = source.cost;
            n = source.n;
            for (int _j0 = 0; _j0 < (NMAX + 1); _j0++) {
                p[_j0] = source.p[_j0];
            }
        }
        public tsp_solution copy() { tsp_solution result = new tsp_solution(); result.set(this); return result; }
    }
    public static TspAstar.tsp_solution best_solution = new TspAstar.tsp_solution(); /* store the current best solution */
    public static double best_cost = 0; /* cost of current best solution */
    public static double[] lb = new double[(NMAX + 1)]; /* vertex lower bounds */
    public static double minlb = 0; /* global edge lower bound */
    public static long evaluations = 0; /* how many of (n-1!) evaluations were done? */
    public static long constructions = 0; /* how many intermediate nodes were calculated */
    public static long maxqueuesize = 0; /* largest size of queue realized */
    public static TspPq.priority_queue q = new TspPq.priority_queue(); /* priority queue for branch & bound search */
    public static boolean lb_flag = true; /* use  lower bound to speed branch & bound */
    public static boolean finished = false;

    public static void process_solution(TspAstar.tsp_solution s, int k, TspAstar.tsp_instance input) {
        s.cost = solution_cost(s, input);
        if ((s.cost < best_cost)) {
            best_cost = s.cost;
            copy_solution(s, best_solution);
        }
        evaluations++;
    }

    public static int is_a_solution(TspAstar.tsp_solution s, int k, TspAstar.tsp_instance t) {
        return ((k == t.n) ? 1 : 0);
    }

    public static void make_move(TspAstar.tsp_solution s, int k, TspAstar.tsp_instance t) {
    }

    public static void unmake_move(TspAstar.tsp_solution s, int k, TspAstar.tsp_instance t) {
    }

    /*    What are possible elements of the next slot in the permutation?  */
    public static void construct_candidates(TspAstar.tsp_solution s, int k, TspAstar.tsp_instance t, int[] c, int[] ncandidates) {
        int i = 0; /* counter */
        boolean[] in_perm = new boolean[(NMAX + 1)]; /* what is now in the permutation? */
        constructions++;
        if ((partial_solution_lb(s, t) > best_cost)) {
            ncandidates[0] = 0;
            return;
        }
        if ((k == 1)) {
            c[0] = 1;
            ncandidates[0] = 1;
            return;
        }
        for (i = 1; (i <= NMAX); i++) {
            in_perm[i] = false;
        }
        for (i = 1; (i < k); i++) {
            in_perm[s.p[i]] = true;
        }
        ncandidates[0] = 0;
        for (i = 1; (i <= t.n); i++) {
            if (!(in_perm[i])) {
                c[ncandidates[0]] = i;
                ncandidates[0] = (ncandidates[0] + 1);
            }
        }
    }

    /* customize backtrack to TSP solutions */
    public static void backtrack(TspAstar.tsp_solution s, int k, TspAstar.tsp_instance input) {
        int[] c = new int[MAXCANDIDATES]; /* candidates for next position */
        int[] ncandidates = new int[]{0}; /* next position candidate count */
        int i = 0; /* counter */
        if ((is_a_solution(s, k, input) != 0)) {
            process_solution(s, k, input);
        } else {
            k = (k + 1);
            construct_candidates(s, k, input, c, ncandidates);
            for (i = 0; (i < ncandidates[0]); i++) {
                s.p[k] = c[i];
                s.n = k;
                make_move(s, k, input);
                backtrack(s, k, input);
                unmake_move(s, k, input);
                if (finished) {
                    return; /* terminate early */
                }
            }
        }
    }

    public static void solve_tsp(TspAstar.tsp_instance t, TspAstar.tsp_solution s) {
        first_solution(best_solution, t);
        best_cost = solution_cost(best_solution, t);
        /* Fix the first city: rotations describe the same closed tour. */
        initialize_solution(s, t);
        extend_solution(s, t, 1);
        backtrack(s, 1, t);
    }

    /* customize branch and bound  to TSP solutions */
    public static void branch_and_bound(TspAstar.tsp_solution s, TspAstar.tsp_instance t) {
        int[] c = new int[MAXCANDIDATES]; /* candidates for next position */
        int[] nc = new int[]{0}; /* next position candidate count */
        int i = 0; /* counter */
        first_solution(best_solution, t);
        best_cost = solution_cost(best_solution, t);
        initialize_solution(s, t);
        extend_solution(s, t, 1);
        TspPq.pq_init(q);
        TspPq.pq_insert(q, s);
        /* Queue keys are conservative lower bounds, not complete-tour costs. */
        while ((!((TspPq.empty_pq(q) != 0)) && (TspPq.top_pq(q).cost < best_cost))) {
            s.set(TspPq.extract_min(q));
            if ((is_a_solution(s, s.n, t) != 0)) {
                process_solution(s, s.n, t);
            } else {
                construct_candidates(s, (s.n + 1), t, c, nc);
                for (i = 0; (i < nc[0]); i++) {
                    extend_solution(s, t, c[i]);
                    TspPq.pq_insert(q, s);
                    contract_solution(s, t);
                }
            }
        }
    }

    public static void read_tsp(TspAstar.tsp_instance t) {
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

    public static void print_tsp(TspAstar.tsp_instance t) {
        int i = 0; /* counter */
        for (i = 1; (i <= t.n); i++) {
            C.printf("%d %d %d\n", i, t.p[i].x, t.p[i].y);
        }
    }

    public static int sq(int x) {
        return (x * x);
    }

    public static double d(int x1, int y1, int x2, int y2) {
        return Math.hypot((((double)x1) - x2), (((double)y1) - y2));
    }

    public static double d1(int i, int j, TspAstar.tsp_instance t) {
        return d(t.p[i].x, t.p[i].y, t.p[j].x, t.p[j].y);
    }

    public static double distance(TspAstar.tsp_solution s, int x, int y, TspAstar.tsp_instance t) {
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
        return d1(s.p[i], s.p[j], t);
    }

    public static double solution_cost(TspAstar.tsp_solution s, TspAstar.tsp_instance t) {
        int i = 0; /* counter */
        double cost = 0; /* cost of solution */
        cost = distance(s, t.n, 1, t);
        for (i = 1; (i < t.n); i++) {
            cost = (cost + distance(s, i, (i + 1), t));
        }
        s.cost = cost;
        return cost;
    }

    public static double partial_solution_cost(TspAstar.tsp_solution s, TspAstar.tsp_instance t) {
        int i = 0; /* counter */
        double cost = 0.0; /* cost of solution */
        for (i = 1; (i < s.n); i++) {
            cost = (cost + distance(s, i, (i + 1), t));
        }
        return cost;
    }

    public static double partial_solution_lb(TspAstar.tsp_solution s, TspAstar.tsp_instance t) {
        int remaining = ((t.n - s.n) + ((s.n > 0) ? 1 : 0));
        double bound = partial_solution_cost(s, t);
        if (lb_flag) {
            bound += (remaining * minlb);
        }
        /* Round conservatively: a lower bound must not round above a tour. */
        return Math.max(0.0, (bound - ((64 * Math.ulp(1.0)) * (Math.abs(bound) + 1))));
    }

    public static void initialize_solution(TspAstar.tsp_solution s, TspAstar.tsp_instance t) {
        s.n = 0;
        s.cost = 0;
    }

    public static void extend_solution(TspAstar.tsp_solution s, TspAstar.tsp_instance t, int v) {
        s.n++;
        s.p[s.n] = v;
        s.cost = partial_solution_lb(s, t);
    }

    public static void contract_solution(TspAstar.tsp_solution s, TspAstar.tsp_instance t) {
        s.n--;
        s.cost = partial_solution_lb(s, t);
    }

    public static void first_solution(TspAstar.tsp_solution s, TspAstar.tsp_instance t) {
        int i = 0; /* counter */
        s.n = t.n;
        for (i = 1; (i <= t.n); i++) {
            s.p[i] = i;
        }
        s.cost = solution_cost(s, t);
    }

    public static void copy_solution(TspAstar.tsp_solution s, TspAstar.tsp_solution t) {
        int i = 0; /* counter */
        t.cost = s.cost;
        t.n = s.n;
        for (i = 1; (i <= s.n); i++) {
            t.p[i] = s.p[i];
        }
    }

    public static void print_solution(TspAstar.tsp_solution s) {
        int i = 0; /* counter */
        C.printf(" n = %d   ", s.n);
        for (i = 1; (i <= s.n); i++) {
            C.printf(" %d", s.p[i]);
        }
        C.printf("\n------------------------------------------------------\n");
    }

    public static void read_solution(TspAstar.tsp_solution s) {
        int i = 0; /* counter */
        int _read2 = C.scan("%d\n");
        if (_read2 > 0) s.n = C.scanInt(0);
        for (i = 1; (i <= s.n); i++) {
            int _read3 = C.scan("%d");
            if (_read3 > 0) s.p[i] = C.scanInt(0);
        }
    }

    /* Compute lower bounds on edge costs for all vertices */
    public static double find_vertex_lower_bounds(TspAstar.tsp_instance t, double[] lb) {
        int i = 0; /* counters */
        int j = 0;
        double minweight = 0; /* min weight edge in graph */
        minweight = MAXD;
        for (i = 1; (i <= t.n); i++) {
            lb[i] = MAXD;
            for (j = 1; (j <= t.n); j++) {
                if (((i != j) && (lb[i] > d1(i, j, t)))) {
                    lb[i] = d1(i, j, t);
                }
            }
            if ((minweight > lb[i])) {
                minweight = lb[i];
            }
        }
        return minweight;
    }

    public static int main() {
        TspAstar.tsp_solution s = new TspAstar.tsp_solution(); /* solution vector */
        TspAstar.tsp_instance t = new TspAstar.tsp_instance(); /* tsp points */
        int i = 0; /* counter */
        read_tsp(t);
        print_tsp(t);
        /*
            first_solution(&s,&t);
            best_cost = solution_cost(&s, &t);

            print_solution(&s);
            printf("INITIAL SOLUTION COST = %7.1f\n",best_cost);
        */
        minlb = find_vertex_lower_bounds(t, lb);
        /*
            printf("minlb = %7.1f\n",minlb);

            for (i=1; i<=t.n; i++) {
	printf(" lb[%d] = %7.1f\n", i, lb[i]);
            }
        */
        for (i = 0; (i <= 1); i++) {
            /********* Branch and Bound Search **************/
            first_solution(s, t);
            best_cost = solution_cost(s, t);
            /*
                print_solution(&s);
                printf("INITIAL SOLUTION COST = %7.1f\n",best_cost);
            */
            lb_flag = (i != 0);
            constructions = (evaluations = 0);
            solve_tsp(t, s);
            C.printf(" evaluations = %ld backtracking lb_flag=%d \n", evaluations, lb_flag);
            C.printf(" constructions = %ld \n", constructions);
            print_solution(best_solution);
            C.printf("OPTIMAL SOLUTION COST = %7.1f\n", best_cost);
            first_solution(s, t);
            best_cost = solution_cost(s, t);
            /*
                print_solution(&s);
                printf("INITIAL SOLUTION COST = %7.1f\n",best_cost);
            */
            maxqueuesize = (constructions = (evaluations = 0));
            branch_and_bound(s, t);
            C.printf(" evaluations = %ld  branch-and-bound lb_flag=%d \n", evaluations, lb_flag);
            C.printf(" constructions = %ld  maxqueuesize = %ld \n", constructions, maxqueuesize);
            print_solution(best_solution);
            C.printf("OPTIMAL B-AND-B SOLUTION COST = %7.1f\n", best_cost);
        }
        return 0;
    }

    public static void main(String[] args) {
        int status = main();
        if (status != 0) System.exit(status);
    }
}
