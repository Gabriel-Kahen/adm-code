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

import java.lang.reflect.Array;
import java.math.BigInteger;
import java.util.ArrayList;
import java.util.List;
import java.util.Map;

/** Common argv-in/JSON-out demonstration interface. See docs/PORTS.md. */
public final class Main {
    private Main() {}

    public static void main(String[] arguments) {
        try {
            Arguments input = new Arguments(arguments);
            String operation = input.next();
            Object result = execute(operation, input);
            input.end();
            System.out.println(json(result));
        } catch (IllegalArgumentException | ArithmeticException | IllegalStateException exception) {
            System.err.println("error: " + exception.getMessage());
            System.exit(1);
        }
    }

    private static Object execute(String operation, Arguments input) {
        return switch (operation) {
            case "selftest" -> SelfTest.run();
            case "sort" -> Sorting.sort(input.next(), input.remainingLongs());
            case "binary" -> {
                long target = input.longValue();
                long[] sorted = input.remainingLongs();
                requireSorted(sorted);
                yield Sorting.binarySearch(sorted, target);
            }
            case "insert" -> {
                long value = input.longValue();
                yield Sorting.insert(input.remainingLongs(), value);
            }
            case "absdiff" ->
                Numeric.absoluteDifference(input.bigInteger(), input.bigInteger()).toString();
            case "bigint" ->
                Numeric.bigint(input.next(), input.bigInteger(), input.bigInteger()).toString();
            case "fib" -> Numeric.fibonacci(input.next(), input.integer()).toString();
            case "binomial" -> Numeric.binomial(input.integer(), input.integer()).toString();
            case "gcd" -> Numeric.extendedGcd(input.bigInteger(), input.bigInteger());
            case "factors" -> Numeric.factors(input.longValue());
            case "distance" -> {
                int dimension = input.count();
                yield Numeric.distance(input.doubles(dimension), input.doubles(dimension));
            }
            case "matrix" -> {
                int rows = input.count();
                int inner = input.count();
                int columns = input.count();
                if (rows == 0 || inner == 0 || columns == 0) {
                    throw new IllegalArgumentException("matrix dimensions must be positive");
                }
                long[][] a = new long[rows][inner];
                long[][] b = new long[inner][columns];
                for (int row = 0; row < rows; row++) {
                    a[row] = input.longs(inner);
                }
                for (int row = 0; row < inner; row++) {
                    b[row] = input.longs(columns);
                }
                yield Numeric.multiply(a, b);
            }
            case "convolve" -> {
                int firstLength = input.count();
                int secondLength = input.count();
                yield Numeric.convolve(input.longs(firstLength), input.longs(secondLength));
            }
            case "edit" -> {
                Dynamic.Edit edit = Dynamic.edit(input.next(), input.next());
                yield Map.of("cost", edit.cost(), "operations", edit.operations());
            }
            case "editbrute" -> Dynamic.editBrute(input.next(), input.next());
            case "lcs" -> Dynamic.lcs(input.next(), input.next());
            case "substring" -> Dynamic.substring(input.next(), input.next());
            case "partition" -> {
                int groups = input.integer();
                Dynamic.Partition result = Dynamic.partition(input.remainingLongs(), groups);
                yield Map.of("cost", result.cost(), "groups", result.groups());
            }
            case "subsetsum" -> {
                int target = input.integer();
                yield Dynamic.subsetSum(input.remainingLongs(), target);
            }
            case "elevator" -> {
                int stops = input.integer();
                int maximum = input.integer();
                Dynamic.Elevator result =
                    Dynamic.elevator(input.remainingIntegers(), stops, maximum);
                yield Map.of("cost", result.cost(), "stops", result.stops());
            }
            case "bfs" -> {
                Graphs.Graph graph = input.graph();
                yield Graphs.breadthFirst(graph, input.integer()).distances();
            }
            case "dfs" -> Graphs.depthFirst(input.graph(), input.integer());
            case "components" -> Graphs.components(input.graph());
            case "scc" -> {
                String method = input.next();
                yield Graphs.stronglyConnected(input.graph(), method);
            }
            case "bipartite" -> Graphs.bipartite(input.graph());
            case "cycle" -> Graphs.hasCycle(input.graph());
            case "articulation" -> Graphs.articulation(input.graph());
            case "topo" -> {
                String method = input.next();
                yield Graphs.topological(input.graph(), method);
            }
            case "mst" -> {
                String method = input.next();
                Graphs.Forest result = Graphs.minimumSpanningForest(input.graph(), method);
                yield Map.of("cost", result.cost(), "edges", result.edges());
            }
            case "dijkstra" -> Graphs.dijkstra(input.graph(), input.integer());
            case "floyd" -> Graphs.floyd(input.graph());
            case "maxflow" ->
                Graphs.maximumFlow(input.graph(), input.integer(), input.integer()).value();
            case "paths" -> Graphs.simplePaths(input.graph(), input.integer(), input.integer());
            case "edgecount" -> input.graph().edges().size();
            case "hull" -> Geometry.convexHull(input.points());
            case "area" -> Geometry.area(input.points());
            case "triangulate" -> Geometry.triangulate(input.points());
            case "mwt" -> Geometry.minimumWeightTriangulation(input.points());
            case "segment" ->
                Geometry.segmentsIntersect(input.point(), input.point(), input.point(),
                                           input.point());
            case "project" ->
                Geometry.projection(input.point(), Geometry.line(input.point(), input.point()));
            case "intersection" ->
                Geometry.intersection(Geometry.line(input.point(), input.point()),
                                      Geometry.line(input.point(), input.point()));
            case "packing" -> Geometry.packing(input.real(), input.real(), input.real());
            case "superman" -> {
                Geometry.Point source = input.point();
                Geometry.Point target = input.point();
                int count = input.count();
                List<Geometry.Circle> circles = new ArrayList<>();
                for (int i = 0; i < count; i++) {
                    circles.add(new Geometry.Circle(input.point(), input.real()));
                }
                yield Geometry.superman(source, target, circles);
            }
            case "queens" -> Search.queens(input.integer());
            case "permutations" -> Search.permutations(input.integer());
            case "subsets" -> Search.subsets(input.integer());
            case "sudoku" -> Search.sudoku(input.next());
            case "tsp" -> {
                String method = input.next();
                List<Geometry.Point> points = input.points();
                long seed = 0;
                int iterations = 0;
                if (method.equals("sample") || method.equals("hill") || method.equals("anneal")) {
                    seed = input.longValue();
                    iterations = input.integer();
                }
                Search.Tour result = Search.tsp(points, method, seed, iterations);
                yield Map.of("cost", result.cost(), "tour", result.tour());
            }
            case "grid" -> Demos.grid(input.next(), input.integer(), input.integer());
            case "find" -> Demos.find(input.next(), input.next());
            case "replace" -> {
                String text = input.next();
                int count = input.count();
                List<Demos.Change> changes = new ArrayList<>();
                for (int i = 0; i < count; i++) {
                    changes.add(new Demos.Change(input.next(), input.next()));
                }
                yield Demos.replace(text, changes);
            }
            case "suitors" -> {
                int count = input.count();
                List<Demos.Suitor> suitors = new ArrayList<>();
                for (int i = 0; i < count; i++) {
                    suitors.add(new Demos.Suitor(input.next(), input.next(), input.longValue(),
                                                 input.longValue()));
                }
                List<String[]> result = new ArrayList<>();
                for (Demos.Suitor suitor : Demos.rankSuitors(suitors)) {
                    result.add(new String[] {suitor.first(), suitor.last()});
                }
                yield result;
            }
            case "card" -> Demos.card(input.next());
            case "uncard" -> Demos.uncard(input.integer());
            case "war" -> {
                int limit = input.integer();
                int firstCount = input.count();
                int secondCount = input.count();
                Demos.War result =
                    Demos.war(limit, input.integers(firstCount), input.integers(secondCount));
                yield Map.of("winner", result.winner(), "steps", result.steps());
            }
            default -> throw new IllegalArgumentException("unknown operation: " + operation);
        };
    }

    private static void requireSorted(long[] values) {
        for (int i = 1; i < values.length; i++) {
            if (values[i] < values[i - 1]) {
                throw new IllegalArgumentException("array must be sorted");
            }
        }
    }
    private static final class Arguments {
        private final String[] values;
        private int position;
        Arguments(String[] values) {
            this.values = values;
        }
        String next() {
            if (position == values.length) {
                throw new IllegalArgumentException("missing argument");
            }
            return values[position++];
        }
        int integer() {
            return Integer.parseInt(next());
        }
        long longValue() {
            return Long.parseLong(next());
        }
        BigInteger bigInteger() {
            return new BigInteger(next());
        }
        double real() {
            return Numeric.finite(Double.parseDouble(next()));
        }
        int count() {
            int value = integer();
            if (value < 0) {
                throw new IllegalArgumentException("negative count");
            }
            return value;
        }
        int[] integers(int count) {
            int[] result = new int[count];
            for (int i = 0; i < count; i++) {
                result[i] = integer();
            }
            return result;
        }
        long[] longs(int count) {
            long[] result = new long[count];
            for (int i = 0; i < count; i++) {
                result[i] = longValue();
            }
            return result;
        }
        double[] doubles(int count) {
            double[] result = new double[count];
            for (int i = 0; i < count; i++) {
                result[i] = real();
            }
            return result;
        }
        long[] remainingLongs() {
            return longs(values.length - position);
        }
        int[] remainingIntegers() {
            return integers(values.length - position);
        }
        Geometry.Point point() {
            return new Geometry.Point(real(), real());
        }
        List<Geometry.Point> points() {
            int count = count();
            List<Geometry.Point> points = new ArrayList<>();
            for (int i = 0; i < count; i++) {
                points.add(point());
            }
            return points;
        }
        Graphs.Graph graph() {
            int vertices = count();
            int directed = integer();
            if (directed != 0 && directed != 1) {
                throw new IllegalArgumentException("direction flag must be 0 or 1");
            }
            int count = count();
            Graphs.Graph graph = new Graphs.Graph(vertices, directed == 1);
            for (int i = 0; i < count; i++) {
                graph.add(integer(), integer(), longValue());
            }
            return graph;
        }
        void end() {
            if (position != values.length) {
                throw new IllegalArgumentException("unexpected extra argument");
            }
        }
    }

    /** Minimal JSON writer: the command interface produces data only, never source expressions. */
    private static String json(Object value) {
        if (value == null) {
            return "null";
        }
        if (value instanceof String string) {
            return quote(string);
        }
        if (value instanceof Geometry.Point point) {
            return json(new double[] {point.x(), point.y()});
        }
        if (value instanceof Boolean || value instanceof Number) {
            return value.toString();
        }
        StringBuilder result = new StringBuilder();
        if (value instanceof Map<?, ?> map) {
            result.append('{');
            boolean first = true;
            for (Map.Entry<?, ?> entry : map.entrySet()) {
                if (!first) {
                    result.append(',');
                }
                first = false;
                result.append(quote(entry.getKey().toString()))
                    .append(':')
                    .append(json(entry.getValue()));
            }
            return result.append('}').toString();
        }
        result.append('[');
        if (value instanceof Iterable<?> items) {
            boolean first = true;
            for (Object item : items) {
                if (!first) {
                    result.append(',');
                }
                first = false;
                result.append(json(item));
            }
        } else if (value.getClass().isArray()) {
            for (int i = 0; i < Array.getLength(value); i++) {
                if (i != 0) {
                    result.append(',');
                }
                result.append(json(Array.get(value, i)));
            }
        } else {
            throw new IllegalArgumentException("unsupported JSON value");
        }
        return result.append(']').toString();
    }
    private static String quote(String text) {
        StringBuilder result = new StringBuilder("\"");
        for (int i = 0; i < text.length(); i++) {
            char character = text.charAt(i);
            switch (character) {
            case '"' -> result.append("\\\"");
            case '\\' -> result.append("\\\\");
            case '\b' -> result.append("\\b");
            case '\f' -> result.append("\\f");
            case '\n' -> result.append("\\n");
            case '\r' -> result.append("\\r");
            case '\t' -> result.append("\\t");
            default -> {
                if (character < 32 || Character.isSurrogate(character)) {
                    result.append(String.format("\\u%04x", (int)character));
                } else {
                    result.append(character);
                }
            }
            }
        }
        return result.append('"').toString();
    }
}
