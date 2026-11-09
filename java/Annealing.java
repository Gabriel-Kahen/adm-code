/*	Simulated Annealing Implementation

	These routines provide a fairly generic implementation of
	simulated annealing, starting from my older code to optimize
	selective assembly.
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
or http://www.amazon.com/exec/obidos/ASIN/0387001638/thealgorithmrepo/
*/

public class Annealing {
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
    public static int solution_count = 0; /* how many solutions evaluated */

    public static void solution_count_update(Tsp.tsp_solution s, Tsp.tsp_instance t) {
        solution_count = (solution_count + 1);
        if (((solution_count == 1) || ((solution_count % PRINT_FREQUENCY) == 0))) {
            C.printf("%d %7.1f\n", solution_count, Tsp.solution_cost(s, t));
        }
    }

    /*  Use random sampling to provide a heuristic solution to a given
        optimization problem.
    */
    public static void random_sampling(Tsp.tsp_instance t, int nsamples, Tsp.tsp_solution s) {
        Tsp.tsp_solution s_now = new Tsp.tsp_solution(); /* current tsp solution */
        double best_cost = 0; /* best cost so far */
        double cost_now = 0; /* current cost */
        int i = 0; /* counter */
        Tsp.initialize_solution(t.n, s_now);
        best_cost = Tsp.solution_cost(s_now, t);
        Tsp.copy_solution(s_now, s);
        for (i = 1; (i <= nsamples); i++) {
            Tsp.random_solution(s_now);
            cost_now = Tsp.solution_cost(s_now, t);
            if ((cost_now < best_cost)) {
                best_cost = cost_now;
                Tsp.copy_solution(s_now, s);
            }
            solution_count_update(s_now, t);
        }
    }

    /*  Use hill climbing to provide a heuristic solution to a given
        optimization problem.
    */
    public static void hill_climbing(Tsp.tsp_instance t, Tsp.tsp_solution s) {
        double cost = 0; /* best cost so far */
        double candidate_cost = 0; /* cost after the proposed swap */
        int i = 0; /* counters */
        int j = 0;
        boolean stuck = false;
        Tsp.initialize_solution(t.n, s);
        Tsp.random_solution(s);
        cost = Tsp.solution_cost(s, t);
        /* Recompute the objective so every accepted tour strictly decreases
               the same deterministic cost, including small real improvements. */
        do {
            stuck = true;
            for (i = 1; (i < t.n); i++) {
                for (j = (i + 1); (j <= t.n); j++) {
                    Tsp.transition(s, t, i, j);
                    candidate_cost = Tsp.solution_cost(s, t);
                    if ((candidate_cost < cost)) {
                        stuck = false;
                        cost = candidate_cost;
                    } else {
                        Tsp.transition(s, t, j, i);
                    }
                    solution_count_update(s, t);
                }
            }
        } while (!(stuck)); /* did I get a better solution? */
    }

    public static void repeated_hill_climbing(Tsp.tsp_instance t, int nsamples, Tsp.tsp_solution bestsol) {
        Tsp.tsp_solution s = new Tsp.tsp_solution(); /* current tsp solution */
        double best_cost = 0; /* best cost so far */
        double cost_now = 0; /* current cost */
        int i = 0; /* counter */
        Tsp.initialize_solution(t.n, s);
        best_cost = Tsp.solution_cost(s, t);
        Tsp.copy_solution(s, bestsol);
        for (i = 1; (i <= nsamples); i++) {
            hill_climbing(t, s);
            cost_now = Tsp.solution_cost(s, t);
            if ((cost_now < best_cost)) {
                best_cost = cost_now;
                Tsp.copy_solution(s, bestsol);
            }
        }
    }

    /*	These routines implement simulated annealing.  Pairs of components
	of the same type will be swapped at random, and the new arrangment
	accepted either if (1) it is an improvement, or (2) the penalty is
	less than a random number, which is a function of the temperature
	of the system.

	We are seeking to *minimize* the current_value.
    */
    public static void anneal(Tsp.tsp_instance t, Tsp.tsp_solution s) {
        int x = 0; /* pair of items to swap */
        int y = 0;
        int i = 0; /* counters */
        int j = 0;
        boolean accept_win = false;
        boolean accept_loss = false;
        double temperature = 0; /* the current system temp */
        double current_value = 0; /* value of current state */
        double start_value = 0; /* value at start of loop */
        double delta = 0; /* value after swap */
        double exponent = 0; /* exponent for energy funct */
        temperature = INITIAL_TEMPERATURE;
        Tsp.initialize_solution(t.n, s);
        current_value = Tsp.solution_cost(s, t);
        for (i = 1; (i <= COOLING_STEPS); i++) {
            temperature *= COOLING_FRACTION;
            start_value = current_value;
            for (j = 1; (j <= STEPS_PER_TEMP); j++) {
                /* pick indices of elements to swap */
                x = Random.random_int(1, t.n);
                y = Random.random_int(1, t.n);
                delta = Tsp.transition(s, t, x, y);
                accept_win = (delta < 0); /* did swap reduce cost? */
                exponent = (((-delta) / current_value) / (K * temperature));
                accept_loss = (Math.exp(exponent) > Random.random_float(0, 1));
                if ((accept_win || accept_loss)) { /* conditions to accept transition */
                    current_value += delta;
                } else {
                    Tsp.transition(s, t, x, y); /* reverse transition */
                }
                solution_count_update(s, t);
            }
            if ((current_value < start_value)) { /* rerun at this temp */
                temperature /= COOLING_FRACTION;
            }
        }
    }

    public static void repeated_annealing(Tsp.tsp_instance t, int nsamples, Tsp.tsp_solution bestsol) {
        Tsp.tsp_solution s = new Tsp.tsp_solution(); /* current tsp solution */
        double best_cost = 0; /* best cost so far */
        double cost_now = 0; /* current cost */
        int i = 0; /* counter */
        Tsp.initialize_solution(t.n, s);
        best_cost = Tsp.solution_cost(s, t);
        Tsp.copy_solution(s, bestsol);
        for (i = 1; (i <= nsamples); i++) {
            anneal(t, s);
            cost_now = Tsp.solution_cost(s, t);
            if ((cost_now < best_cost)) {
                best_cost = cost_now;
                Tsp.copy_solution(s, bestsol);
            }
        }
    }

}
