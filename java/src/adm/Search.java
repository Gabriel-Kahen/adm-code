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

package adm;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.Comparator;
import java.util.List;
import java.util.PriorityQueue;

/** Exhaustive and heuristic search. Exponential algorithms have explicit practical limits. */
public final class Search {
    private Search() {}

    /** Callbacks see a read-only prefix; make/unmake must balance for every completed move. */
    public interface Problem<T> {
        boolean isSolution(List<T> prefix);
        List<T> candidates(List<T> prefix);
        default void makeMove(List<T> prefix) {}
        default void unmakeMove(List<T> prefix) {}
        /** Return false to stop the entire search after this solution. */
        boolean processSolution(List<T> prefix);
    }
    public static <T> void backtrack(Problem<T> problem) {
        enumerate(problem, new ArrayList<>());
    }
    private static <T> boolean enumerate(Problem<T> problem, List<T> prefix) {
        if (problem.isSolution(List.copyOf(prefix))) {
            return problem.processSolution(List.copyOf(prefix));
        }
        for (T candidate : problem.candidates(List.copyOf(prefix))) {
            prefix.add(candidate);
            try {
                problem.makeMove(List.copyOf(prefix));
                try {
                    if (!enumerate(problem, prefix)) {
                        return false;
                    }
                } finally {
                    problem.unmakeMove(List.copyOf(prefix));
                }
            } finally {
                prefix.remove(prefix.size() - 1);
            }
        }
        return true;
    }

    public static List<List<Integer>> permutations(int n) {
        if (n < 0 || n > 9) {
            throw new IllegalArgumentException("permutation size outside 0..9");
        }
        List<List<Integer>> result = new ArrayList<>();
        permutationsVisit(n, new boolean[n], new ArrayList<>(), result);
        return result;
    }
    private static void permutationsVisit(int n, boolean[] used, List<Integer> prefix,
                                          List<List<Integer>> result) {
        if (prefix.size() == n) {
            result.add(new ArrayList<>(prefix));
            return;
        }
        for (int value = 0; value < n; value++) {
            if (used[value]) {
                continue;
            }
            used[value] = true;
            prefix.add(value);
            permutationsVisit(n, used, prefix, result);
            prefix.remove(prefix.size() - 1);
            used[value] = false;
        }
    }
    public static List<List<Integer>> subsets(int n) {
        if (n < 0 || n > 20) {
            throw new IllegalArgumentException("subset size outside 0..20");
        }
        List<List<Integer>> result = new ArrayList<>();
        subsetsVisit(n, 0, new ArrayList<>(), result);
        result.sort(Graphs::compareLists);
        return result;
    }
    private static void subsetsVisit(int n, int next, List<Integer> prefix,
                                     List<List<Integer>> result) {
        result.add(new ArrayList<>(prefix));
        for (int value = next; value < n; value++) {
            prefix.add(value);
            subsetsVisit(n, value + 1, prefix, result);
            prefix.remove(prefix.size() - 1);
        }
    }

    /** Number of nonattacking queen placements, O(n!) search and O(n) auxiliary storage. */
    public static long queens(int n) {
        if (n < 0 || n > 15) {
            throw new IllegalArgumentException("queen size outside 0..15");
        }
        return queensVisit(0, n, new boolean[n], new boolean[2 * n + 1], new boolean[2 * n + 1]);
    }
    private static long queensVisit(int row, int n, boolean[] columns, boolean[] rising,
                                    boolean[] falling) {
        if (row == n) {
            return 1;
        }
        long count = 0;
        for (int column = 0; column < n; column++) {
            int up = row + column;
            int down = row - column + n;
            if (columns[column] || rising[up] || falling[down]) {
                continue;
            }
            columns[column] = rising[up] = falling[down] = true;
            count += queensVisit(row + 1, n, columns, rising, falling);
            columns[column] = rising[up] = falling[down] = false;
        }
        return count;
    }

    /** First Sudoku solution, or null for an unsatisfiable valid board. Contradictory givens are errors. */
    public static String sudoku(String puzzle) {
        return sudoku(puzzle, true);
    }
    public static String sudoku(String puzzle, boolean mostConstrainedFirst) {
        if (puzzle.length() != 81) {
            throw new IllegalArgumentException("Sudoku requires 81 digits");
        }
        int[] board = new int[81];
        int[] rows = new int[9];
        int[] columns = new int[9];
        int[] boxes = new int[9];
        for (int cell = 0; cell < 81; cell++) {
            char character = puzzle.charAt(cell);
            if (character < '0' || character > '9') {
                throw new IllegalArgumentException("Sudoku requires digits 0..9");
            }
            board[cell] = character - '0';
            if (board[cell] == 0) {
                continue;
            }
            int row = cell / 9;
            int column = cell % 9;
            int box = row / 3 * 3 + column / 3;
            int mask = 1 << board[cell];
            if (((rows[row] | columns[column] | boxes[box]) & mask) != 0) {
                throw new IllegalArgumentException("contradictory Sudoku givens");
            }
            rows[row] |= mask;
            columns[column] |= mask;
            boxes[box] |= mask;
        }
        if (!sudokuVisit(board, rows, columns, boxes, mostConstrainedFirst)) {
            return null;
        }
        StringBuilder result = new StringBuilder();
        for (int value : board) {
            result.append(value);
        }
        return result.toString();
    }
    private static boolean sudokuVisit(int[] board, int[] rows, int[] columns, int[] boxes,
                                       boolean smart) {
        int bestCell = -1;
        int bestMask = 0;
        int bestCount = 10;
        for (int cell = 0; cell < 81; cell++) {
            if (board[cell] != 0) {
                continue;
            }
            int row = cell / 9;
            int column = cell % 9;
            int mask = 0x3fe & ~(rows[row] | columns[column] | boxes[row / 3 * 3 + column / 3]);
            int count = Integer.bitCount(mask);
            if (count == 0) {
                return false;
            }
            if (count < bestCount) {
                bestCell = cell;
                bestMask = mask;
                bestCount = count;
            }
            if (!smart) {
                break;
            }
        }
        if (bestCell == -1) {
            return true;
        }
        int row = bestCell / 9;
        int column = bestCell % 9;
        int box = row / 3 * 3 + column / 3;
        for (int remaining = bestMask; remaining != 0; remaining &= remaining - 1) {
            int bit = Integer.lowestOneBit(remaining);
            board[bestCell] = Integer.numberOfTrailingZeros(bit);
            rows[row] |= bit;
            columns[column] |= bit;
            boxes[box] |= bit;
            if (sudokuVisit(board, rows, columns, boxes, smart)) {
                return true;
            }
            board[bestCell] = 0;
            rows[row] ^= bit;
            columns[column] ^= bit;
            boxes[box] ^= bit;
        }
        return false;
    }

    public record Tour(double cost, int[] tour) {}
    public static int[] identityTour(int n) {
        if (n < 0) {
            throw new IllegalArgumentException("negative tour size");
        }
        int[] result = new int[n];
        for (int i = 0; i < n; i++) {
            result[i] = i;
        }
        return result;
    }
    public static double tourCost(List<Geometry.Point> points, int[] tour) {
        validateTour(points, tour);
        return cost(points, tour);
    }
    private static void validateTour(List<Geometry.Point> points, int[] tour) {
        if (tour.length != points.size()) {
            throw new IllegalArgumentException("tour must visit every city");
        }
        boolean[] seen = new boolean[tour.length];
        for (int city : tour) {
            if (city < 0 || city >= tour.length || seen[city]) {
                throw new IllegalArgumentException("invalid tour permutation");
            }
            seen[city] = true;
        }
    }
    private static double cost(List<Geometry.Point> points, int[] tour) {
        double result = 0;
        for (int i = 0; i < tour.length; i++) {
            result =
                Numeric.finite(result + Geometry.distance(points.get(tour[i]),
                                                          points.get(tour[(i + 1) % tour.length])));
        }
        return result;
    }
    /** Recomputed O(n) swap delta handles neighbors, closing edge and very small tours. */
    public static double swapDelta(List<Geometry.Point> points, int[] tour, int i, int j) {
        validateTour(points, tour);
        if (i < 0 || j < 0 || i >= tour.length || j >= tour.length) {
            throw new IllegalArgumentException("invalid swap position");
        }
        double before = cost(points, tour);
        int[] changed = tour.clone();
        swap(changed, i, j);
        return cost(points, changed) - before;
    }
    private static void swap(int[] a, int i, int j) {
        int value = a[i];
        a[i] = a[j];
        a[j] = value;
    }

    public static Tour tsp(List<Geometry.Point> points, String method, long seed, int iterations) {
        if (iterations < 0) {
            throw new IllegalArgumentException("negative search budget");
        }
        return switch (method) {
            case "exact" -> exactTsp(points, false);
            case "best" -> exactTsp(points, true);
            case "sample", "hill", "anneal" -> heuristicTsp(points, method, seed, iterations);
            default -> throw new IllegalArgumentException("unknown TSP method");
        };
    }

    /** Repeated independent heuristic runs; returns the best of the documented seed sequence. */
    public static Tour repeatedTsp(List<Geometry.Point> points, String method, long seed,
                                   int iterations, int runs) {
        if (runs < 1) {
            throw new IllegalArgumentException("restart count must be positive");
        }
        if (!method.equals("sample") && !method.equals("hill") && !method.equals("anneal")) {
            throw new IllegalArgumentException("restarts require a heuristic TSP method");
        }
        Tour best = tsp(points, method, seed, iterations);
        for (int run = 1; run < runs; run++) {
            Tour candidate = tsp(points, method, seed + run, iterations);
            if (candidate.cost < best.cost) {
                best = candidate;
            }
        }
        return best;
    }

    private static double[][] distances(List<Geometry.Point> points) {
        double[][] distance = new double[points.size()][points.size()];
        for (int i = 0; i < points.size(); i++) {
            for (int j = 0; j < points.size(); j++) {
                distance[i][j] = Geometry.distance(points.get(i), points.get(j));
            }
        }
        return distance;
    }
    private record Partial(int[] path, boolean[] used, double cost, double bound) {}
    private static Tour exactTsp(List<Geometry.Point> points, boolean bestFirst) {
        int n = points.size();
        if (n > 12) {
            throw new IllegalArgumentException("exact TSP limited to 12 cities");
        }
        int[] incumbent = identityTour(n);
        double upperBound = cost(points, incumbent);
        if (n <= 1) {
            return new Tour(upperBound, incumbent);
        }
        double[][] distance = distances(points);
        boolean[] used = new boolean[n];
        used[0] = true;
        Partial root = new Partial(new int[] {0}, used, 0, lowerBound(distance, used, 0, 0));
        if (!bestFirst) {
            Best best = new Best(upperBound, incumbent);
            exactVisit(distance, root, best);
            return new Tour(best.cost, best.tour);
        }
        PriorityQueue<Partial> frontier =
            new PriorityQueue<>(Comparator.comparingDouble(Partial::bound)
                                    .thenComparingInt(partial -> - partial.path.length));
        frontier.add(root);
        while (!frontier.isEmpty()) {
            Partial partial = frontier.remove();
            if (partial.bound >= upperBound) {
                continue;
            }
            if (partial.path.length == n) {
                double complete = partial.cost + distance[partial.path[n - 1]][0];
                if (complete < upperBound) {
                    upperBound = complete;
                    incumbent = partial.path;
                }
                continue;
            }
            for (Partial child : children(distance, partial)) {
                if (child.bound < upperBound) {
                    if (frontier.size() >= 1000000) {
                        throw new IllegalStateException("exact TSP frontier exhausted");
                    }
                    frontier.add(child);
                }
            }
        }
        return new Tour(upperBound, incumbent);
    }
    private static final class Best {
        double cost;
        int[] tour;
        Best(double cost, int[] tour) {
            this.cost = cost;
            this.tour = tour;
        }
    }
    private static void exactVisit(double[][] distance, Partial partial, Best best) {
        if (partial.bound >= best.cost) {
            return;
        }
        if (partial.path.length == distance.length) {
            double complete = partial.cost + distance[partial.path[partial.path.length - 1]][0];
            if (complete < best.cost) {
                best.cost = complete;
                best.tour = partial.path;
            }
            return;
        }
        List<Partial> children = children(distance, partial);
        children.sort(Comparator.comparingDouble(Partial::bound));
        for (Partial child : children) {
            exactVisit(distance, child, best);
        }
    }
    private static List<Partial> children(double[][] distance, Partial parent) {
        List<Partial> result = new ArrayList<>();
        int last = parent.path[parent.path.length - 1];
        for (int next = 0; next < distance.length; next++) {
            if (parent.used[next]) {
                continue;
            }
            int[] path = Arrays.copyOf(parent.path, parent.path.length + 1);
            path[path.length - 1] = next;
            boolean[] used = parent.used.clone();
            used[next] = true;
            double accumulated = Numeric.finite(parent.cost + distance[last][next]);
            result.add(new Partial(path, used, accumulated,
                                   lowerBound(distance, used, next, accumulated)));
        }
        return result;
    }
    // Any completion contains a tree on remaining vertices and one link to each endpoint.
    private static double lowerBound(double[][] distance, boolean[] used, int last,
                                     double accumulated) {
        int n = used.length;
        int firstRemaining = -1;
        double fromLast = Double.POSITIVE_INFINITY;
        double fromStart = Double.POSITIVE_INFINITY;
        for (int v = 0; v < n; v++) {
            if (!used[v]) {
                firstRemaining = v;
                fromLast = Math.min(fromLast, distance[last][v]);
                fromStart = Math.min(fromStart, distance[0][v]);
            }
        }
        if (firstRemaining == -1) {
            return accumulated + distance[last][0];
        }
        boolean[] included = used.clone();
        double[] key = new double[n];
        Arrays.fill(key, Double.POSITIVE_INFINITY);
        key[firstRemaining] = 0;
        double tree = 0;
        while (true) {
            int next = -1;
            for (int v = 0; v < n; v++) {
                if (!included[v] && (next == -1 || key[v] < key[next])) {
                    next = v;
                }
            }
            if (next == -1) {
                break;
            }
            included[next] = true;
            tree += key[next];
            for (int v = 0; v < n; v++) {
                if (!included[v]) {
                    key[v] = Math.min(key[v], distance[next][v]);
                }
            }
        }
        return Numeric.finite(accumulated + tree + fromLast + fromStart);
    }

    private static Tour heuristicTsp(List<Geometry.Point> points, String method, long seed,
                                     int iterations) {
        int[] current = identityTour(points.size());
        int[] best = current.clone();
        double currentCost = cost(points, current);
        double bestCost = currentCost;
        if (points.size() < 2) {
            return new Tour(bestCost, best);
        }
        Numeric.Generator random = new Numeric.Generator(seed);
        double initialTemperature = Math.max(1, currentCost / points.size());
        for (int iteration = 0; iteration < iterations; iteration++) {
            if (method.equals("sample")) {
                random.shuffle(current);
                currentCost = cost(points, current);
            } else {
                int i = random.integer(0, current.length - 1);
                int j = random.integer(0, current.length - 1);
                swap(current, i, j);
                double candidate = cost(points, current);
                double temperature = initialTemperature *
                                     Math.pow(0.001, (double)iteration / Math.max(1, iterations));
                boolean accept = candidate < currentCost;
                if (method.equals("anneal") && !accept) {
                    accept = random.real(0, 1) < Math.exp((currentCost - candidate) / temperature);
                }
                if (accept) {
                    currentCost = candidate;
                } else {
                    swap(current, i, j);
                }
            }
            if (currentCost < bestCost) {
                bestCost = currentCost;
                best = current.clone();
            }
        }
        return new Tour(bestCost, best);
    }
}
