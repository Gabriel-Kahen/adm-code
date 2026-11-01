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

import java.math.BigInteger;
import java.util.Arrays;
import java.util.List;
import java.util.NoSuchElementException;
import java.util.PriorityQueue;
import java.util.Random;

/** Native API invariants not visible through the shared command-line protocol. */
public final class SelfTest {
    private SelfTest() {}
    private static void check(boolean condition, String description) {
        if (!condition) {
            throw new IllegalStateException("selftest failed: " + description);
        }
    }
    private static void rejects(Runnable action) {
        try {
            action.run();
        } catch (IllegalArgumentException | ArithmeticException | NoSuchElementException expected) {
            return;
        }
        throw new IllegalStateException("selftest failed: invalid input was accepted");
    }
    public static boolean run() {
        containers();
        sortingAndNumbers();
        graphs();
        dynamic();
        geometry();
        search();
        demos();
        return true;
    }
    private static void containers() {
        Containers.Queue<Integer> queue = new Containers.Queue<>();
        Containers.Stack<Integer> stack = new Containers.Stack<>();
        for (int i = 0; i < 2000; i++) {
            queue.add(i);
            stack.push(i);
        }
        for (int i = 0; i < 2000; i++) {
            check(queue.remove() == i, "FIFO");
            check(stack.pop() == 1999 - i, "LIFO");
        }
        rejects(queue::remove);
        rejects(stack::pop);
        queue.add(7);
        check(queue.size() == 1 && queue.remove() == 7 && queue.isEmpty(),
              "queue reuse after drain");
        Containers.MinHeap heap = new Containers.MinHeap();
        PriorityQueue<Long> reference = new PriorityQueue<>();
        Random random = new Random(317);
        for (int i = 0; i < 2000; i++) {
            if (reference.isEmpty() || random.nextBoolean()) {
                long value = random.nextLong();
                heap.add(value);
                reference.add(value);
            } else {
                check(heap.remove() == reference.remove(), "interleaved heap removal");
            }
            check(heap.size() == reference.size(), "heap size");
            if (!reference.isEmpty()) {
                check(heap.minimum() == reference.element(), "heap minimum");
            }
        }
        while (!reference.isEmpty()) {
            check(heap.remove() == reference.remove(), "heap final drain");
        }
        rejects(heap::remove);
        Containers.DisjointSet sets = new Containers.DisjointSet(7);
        check(sets.union(1, 2) && sets.union(2, 3) && !sets.union(3, 1), "union idempotence");
        check(sets.size(3) == 3 && sets.find(0) != sets.find(1), "union sizes and separation");
        rejects(() -> sets.find(-1));
        Containers.LinkedList list = new Containers.LinkedList();
        list.insert(1);
        list.insert(2);
        list.insert(1);
        check(list.delete(1) && list.values().equals(List.of(2L, 1L)),
              "list deletes first occurrence");
        check(list.delete(1) && !list.contains(1) && !list.delete(9), "list tail/absent deletion");
        check(list.delete(2) && list.values().isEmpty(), "list singleton deletion");
        Containers.BinarySearchTree tree = new Containers.BinarySearchTree();
        for (long value : new long[] {5, 3, 8, 7, 9, 6, 5}) {
            tree.insert(value);
        }
        tree.delete(5); // Root with two children; successor is below right child's left child.
        check(tree.values().equals(List.of(3L, 6L, 7L, 8L, 9L)),
              "BST successor replacement and set duplicates");
        for (long value : new long[] {6, 9, 8, 3, 7}) {
            tree.delete(value);
        }
        tree.delete(100);
        check(tree.values().isEmpty() && !tree.contains(6), "BST repeated root deletion");
    }
    private static void sortingAndNumbers() {
        long[] input = {Long.MAX_VALUE, 0, -3, Long.MIN_VALUE, 4, 4};
        long[] expected = input.clone();
        Arrays.sort(expected);
        for (String method : List.of("insertion", "selection", "quick", "heap", "merge")) {
            check(Arrays.equals(Sorting.sort(method, input), expected), "sort " + method);
        }
        check(input[0] == Long.MAX_VALUE && Sorting.binarySearch(expected, 4) == 3,
              "copying and lower bound");
        for (String method : List.of("recursive", "memo", "table", "constant")) {
            check(Numeric.fibonacci(method, 20).equals(BigInteger.valueOf(6765)),
                  "Fibonacci " + method);
        }
        check(Numeric.binomial(100, 50).toString().equals("100891344545564193334812497256"),
              "unbounded binomial");
        BigInteger a = BigInteger.valueOf(Long.MIN_VALUE);
        BigInteger b = BigInteger.valueOf(-15);
        BigInteger[] gcd = Numeric.extendedGcd(a, b);
        check(a.multiply(gcd[1]).add(b.multiply(gcd[2])).equals(gcd[0]),
              "signed Bezout coefficients");
        rejects(() -> Numeric.multiply(new long[][] {{Long.MAX_VALUE}}, new long[][] {{2}}));
        Numeric.Generator first = new Numeric.Generator(892);
        Numeric.Generator second = new Numeric.Generator(892);
        int[] permutation = Search.identityTour(50);
        int[] repeated = permutation.clone();
        first.shuffle(permutation);
        second.shuffle(repeated);
        check(Arrays.equals(permutation, repeated), "seeded shuffle reproducibility");
        Arrays.sort(permutation);
        check(Arrays.equals(permutation, Search.identityTour(50)),
              "Fisher-Yates preserves permutation");
        for (int i = 0; i < 2000; i++) {
            int integer = first.integer(Integer.MIN_VALUE, Integer.MAX_VALUE);
            check(integer >= Integer.MIN_VALUE && integer <= Integer.MAX_VALUE,
                  "inclusive integer interval");
            double real = first.real(-12, 17);
            check(real >= -12 && real < 17, "real interval");
        }
        check(first.integer(3, 3) == 3 && first.real(2, 2) == 2, "singleton random intervals");
        rejects(() -> first.integer(2, 1));
        rejects(() -> first.real(Double.NaN, 1));
    }
    private static void graphs() {
        Graphs.Graph graph = new Graphs.Graph(5, false);
        graph.add(0, 1, 2);
        graph.add(0, 1, 3);
        graph.add(1, 2, 4);
        graph.add(3, 3, 0);
        check(Graphs.hasCycle(graph) && graph.edges().size() == 4, "multigraph cycles");
        check(Graphs.articulation(graph).equals(List.of(1)), "multigraph articulation");
        check(graph.delete(1, 0) && graph.edges().size() == 3, "undirected edge deletion");
        check(graph.delete(3, 3) && !Graphs.hasCycle(graph), "self-loop deletion");
        int[] colors = Graphs.bipartiteColors(graph);
        check(colors != null, "bipartite witness exists");
        for (Graphs.Edge edge : graph.edges()) {
            check(colors[edge.from()] == -colors[edge.to()],
                  "bipartite witness separates endpoints");
        }
        Graphs.ShortestPaths shortest = Graphs.dijkstraPaths(graph, 0);
        check(shortest.distances()[2] == 7 &&
                  Graphs.path(shortest.parents(), 0, 2).equals(List.of(0, 1, 2)),
              "Dijkstra parent witness");
        Graphs.BreadthFirst bfs = Graphs.breadthFirst(graph, 0);
        check(Graphs.path(bfs.parents(), 0, 2).equals(List.of(0, 1, 2)), "path reconstruction");
        check(Graphs.path(bfs.parents(), 0, 4).isEmpty(), "unreachable path");
        rejects(() -> Graphs.path(new int[] {1, 0}, 0, 1 + 1));
        rejects(() -> Graphs.path(new int[] {-1, 2, 1}, 0, 1));
        Graphs.Graph directed = new Graphs.Graph(4, true);
        directed.add(0, 1, 2);
        directed.add(0, 1, 1);
        directed.add(1, 0, 5);
        directed.add(1, 2, 3);
        directed.add(2, 3, 3);
        directed.add(1, 1, 100);
        Graphs.Flow flow = Graphs.maximumFlow(directed, 0, 3);
        check(flow.value() == 3, "parallel/antiparallel capacities");
        for (int v = 0; v < 4; v++) {
            long net = 0;
            for (int w = 0; w < 4; w++) {
                check(flow.net()[v][w] == -flow.net()[w][v], "flow antisymmetry");
                net += flow.net()[v][w];
            }
            check(net == (v == 0 ? 3 : v == 3 ? -3 : 0), "flow conservation");
        }
        check(directed.delete(1, 0) && !directed.delete(1, 0), "directed deletion orientation");
        for (String method : List.of("tarjan", "kosaraju")) {
            check(Graphs.stronglyConnected(directed, method)
                      .equals(List.of(List.of(0), List.of(1), List.of(2), List.of(3))),
                  "SCC " + method);
        }
    }
    private static void dynamic() {
        check(Dynamic.edit("", "abc").operations().equals("III"), "empty edit trace");
        check(Dynamic.editBrute("ab", "ba") == 2, "brute edit distance");
        check(Dynamic.substring("abc", "zzabczz") == 0, "free substring boundaries");
        Dynamic.Partition partition = Dynamic.partition(new long[] {10, 0, 20, 3}, 2);
        check(partition.cost() == 23 && partition.groups().size() == 2, "partition witness");
        check(Dynamic.subsetSum(new long[] {0, 3, 3}, 6).equals(List.of(1, 2)),
              "subset items used once");
        check(Dynamic.subsetSum(new long[] {0}, 0).isEmpty(), "empty subset witness");
        check(Dynamic.elevator(new int[] {2, 4}, 0, 4).cost() == 6, "zero elevator stops");
        check(Dynamic.elevator(new int[] {2, 4}, 7, 4).cost() == 0, "unused elevator budget");
        rejects(() -> Dynamic.partition(new long[] {1}, 2));
        rejects(() -> Dynamic.subsetSum(new long[] {-1}, 0));
    }
    private static Geometry.Point p(double x, double y) {
        return new Geometry.Point(x, y);
    }
    private static void close(double actual, double expected, String message) {
        check(Math.abs(actual - expected) <= 1e-8 * Math.max(1, Math.abs(expected)), message);
    }
    private static void geometry() {
        Geometry.Line horizontal = Geometry.line(p(0, 2), p(5, 2));
        check(Geometry.sameLine(horizontal, Geometry.line(p(8, 2), p(-1, 2))),
              "normalized same line");
        check(Geometry.parallel(horizontal, Geometry.line(p(0, 3), p(7, 3))), "parallel lines");
        check(Geometry.intersection(horizontal, Geometry.pointAndSlope(p(0, 0), 1)).equals(p(2, 2)),
              "line intersection");
        check(Geometry.projection(p(4, 7), horizontal).equals(p(4, 2)), "orthogonal projection");
        Geometry.Point translatedEndpoint = p(100000000, 100000001);
        Geometry.Line translatedLine = Geometry.line(translatedEndpoint, p(100000001, 100000002));
        close(Geometry.distance(Geometry.projection(translatedEndpoint, translatedLine),
                                translatedEndpoint),
              0, "translated line preserves its endpoint under projection");
        check(Geometry.orientation(p(0, 0), p(2, 0), p(1, 1)) == 1, "orientation");
        check(Geometry.pointInBox(p(1, 0), p(2, 0), p(0, 0)), "reversed box corners");
        check(Geometry.segmentsIntersect(p(0, 0), p(1, 0), p(1, 0), p(2, 0)),
              "closed segment endpoint");
        List<Geometry.Point> concave = List.of(p(0, 0), p(3, 0), p(3, 3), p(1, 1), p(0, 3));
        List<int[]> triangles = Geometry.triangulate(concave);
        double total = 0;
        for (int[] triangle : triangles) {
            total += Geometry.triangleArea(concave.get(triangle[0]), concave.get(triangle[1]),
                                           concave.get(triangle[2]));
        }
        close(total, Geometry.area(concave), "triangulation area conservation");
        check(triangles.size() == 3, "n-2 triangles");
        close(Geometry.minimumWeightTriangulation(List.of(p(0, 0), p(1, 0), p(1, 1), p(0, 1))),
              4 + 2 * Math.sqrt(2), "convex triangulation perimeter");
        for (int row = -5; row <= 5; row++) {
            for (int column = -5; column <= 5; column++) {
                int[] hex = Geometry.arrayToHex(row, column);
                check(Arrays.equals(Geometry.hexToArray(hex[0], hex[1]), new int[] {row, column}),
                      "array/hex inverse");
                Geometry.Point geo = Geometry.hexToGeo(row, column, 1.5);
                Geometry.Point recovered = Geometry.geoToHex(geo, 1.5);
                close(recovered.x(), row, "hex/Cartesian row inverse");
                close(recovered.y(), column, "hex/Cartesian diagonal inverse");
            }
        }
        check(Geometry.denseLayers(10, 10, 1) == 5 && Geometry.platesPerRow(1, 10, 1) == 4,
              "hexagonal layers and shifted rows");
        check(Geometry.platesOnTop(0, 0, 2, 2, 1) == 0, "no plates above singleton");
        rejects(() -> Geometry.projection(p(1, 1), Geometry.line(p(0, 0), p(0, 0))));
        rejects(() -> Geometry.triangulate(List.of(p(0, 0), p(2, 2), p(0, 2), p(2, 0))));
        rejects(() -> Geometry.minimumWeightTriangulation(concave));
    }
    private static void search() {
        int[] balance = {0};
        int[] moves = {0};
        int[] undone = {0};
        int[] solutions = {0};
        Search.backtrack(new Search.Problem<Integer>() {
            @Override
            public boolean isSolution(List<Integer> prefix) {
                return prefix.size() == 3;
            }
            @Override
            public List<Integer> candidates(List<Integer> prefix) {
                return List.of(0, 1);
            }
            @Override
            public void makeMove(List<Integer> prefix) {
                balance[0]++;
                moves[0]++;
            }
            @Override
            public void unmakeMove(List<Integer> prefix) {
                balance[0]--;
                undone[0]++;
            }
            @Override
            public boolean processSolution(List<Integer> prefix) {
                solutions[0]++;
                return false;
            }
        });
        check(balance[0] == 0 && moves[0] == 3 && undone[0] == 3 && solutions[0] == 1,
              "generic backtracking balanced undo and global early stop");
        rejects(() -> Search.backtrack(new Search.Problem<Integer>() {
            @Override
            public boolean isSolution(List<Integer> prefix) {
                return prefix.size() == 2;
            }
            @Override
            public List<Integer> candidates(List<Integer> prefix) {
                return List.of(0);
            }
            @Override
            public void makeMove(List<Integer> prefix) {
                balance[0]++;
            }
            @Override
            public void unmakeMove(List<Integer> prefix) {
                balance[0]--;
            }
            @Override
            public boolean processSolution(List<Integer> prefix) {
                throw new IllegalArgumentException("intentional callback failure");
            }
        }));
        check(balance[0] == 0, "generic undo also runs on callback exceptions");
        check(Search.queens(0) == 1 && Search.queens(8) == 92, "queen boundaries");
        String solved =
            "534678912672195348198342567859761423426853791713924856961537284287419635345286179";
        String puzzle = "0" + solved.substring(1);
        check(solved.equals(Search.sudoku(puzzle, false)) &&
                  solved.equals(Search.sudoku(puzzle, true)),
              "Sudoku row-first and most-constrained search");
        List<Geometry.Point> points = List.of(p(0, 0), p(2, 2), p(0, 2), p(2, 0), p(1, 3));
        int[] tour = Search.identityTour(points.size());
        for (int i = 0; i < tour.length; i++) {
            for (int j = 0; j < tour.length; j++) {
                int[] swapped = tour.clone();
                int old = swapped[i];
                swapped[i] = swapped[j];
                swapped[j] = old;
                close(Search.tourCost(points, swapped) - Search.tourCost(points, tour),
                      Search.swapDelta(points, tour, i, j), "swap delta includes closing edge");
            }
        }
        double reference = Double.POSITIVE_INFINITY;
        for (List<Integer> permutation : Search.permutations(points.size())) {
            int[] candidate = new int[permutation.size()];
            for (int i = 0; i < candidate.length; i++) {
                candidate[i] = permutation.get(i);
            }
            reference = Math.min(reference, Search.tourCost(points, candidate));
        }
        close(Search.tsp(points, "exact", 0, 0).cost(), reference,
              "DFS TSP versus exhaustive tours");
        close(Search.tsp(points, "best", 0, 0).cost(), reference,
              "best-first TSP versus exhaustive tours");
        for (String method : List.of("sample", "hill", "anneal")) {
            Search.Tour first = Search.tsp(points, method, 73, 100);
            Search.Tour repeated = Search.tsp(points, method, 73, 100);
            check(Arrays.equals(first.tour(), repeated.tour()), "seeded TSP reproducibility");
            check(first.cost() <= Search.tourCost(points, tour), "heuristics retain incumbent");
            Search.Tour restarts = Search.repeatedTsp(points, method, 73, 100, 3);
            check(restarts.cost() <= first.cost(), "restarts retain best tour");
        }
        rejects(() -> Search.repeatedTsp(points, "hill", 1, 10, 0));
    }
    private static void demos() {
        check(Demos.find("", "abc") == 0 && Demos.find("x", "abc") == -1,
              "naive substring boundaries");
        check(Demos.replace("a a", List.of(new Demos.Change("a", "aa"))).equals("aa aa"),
              "nonrecursive replacement");
        check(Demos.grid("diagonal", 2, 3).size() == 6 && Demos.grid("snake", 0, 2).isEmpty(),
              "rectangular grids");
        for (int card = 0; card < 52; card++) {
            check(Demos.card(Demos.uncard(card)) == card, "card round trip");
        }
        check(Demos.war(100, new int[] {48}, new int[] {0}).winner().equals("a"), "War winner");
        check(Demos.war(100, new int[] {0}, new int[] {1}).winner().equals("draw"),
              "War exhausted tied pot");
    }
}
