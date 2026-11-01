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

#include "adm.hpp"

#include <iomanip>
#include <iostream>
#include <sstream>

namespace {
using namespace adm;
std::string json(const std::string &value) {
    std::ostringstream output;
    output << '"';
    for (unsigned char byte : value) {
        switch (byte) {
        case '"':
            output << "\\\"";
            break;
        case '\\':
            output << "\\\\";
            break;
        case '\n':
            output << "\\n";
            break;
        case '\r':
            output << "\\r";
            break;
        case '\t':
            output << "\\t";
            break;
        default:
            if (byte < 0x20) {
                output << "\\u" << std::hex << std::setw(4) << std::setfill('0')
                       << static_cast<int>(byte) << std::dec;
            } else {
                output << static_cast<char>(byte);
            }
        }
    }
    output << '"';
    return output.str();
}
std::string json(bool value) {
    return value ? "true" : "false";
}
std::string json(Integer value) {
    return std::to_string(value);
}
std::string json(int value) {
    return std::to_string(value);
}
std::string json(double value) {
    require(std::isfinite(value), "nonfinite result");
    std::ostringstream output;
    output << std::setprecision(17) << value;
    return output.str();
}
std::string json(Point point) {
    return "[" + json(point.x) + "," + json(point.y) + "]";
}
std::string json(Edge edge) {
    return "[" + json(edge.from) + "," + json(edge.to) + "," + json(edge.weight) + "]";
}
template <class T> std::string json(const std::vector<T> &values);
template <class T> std::string json(const std::optional<T> &value) {
    return value ? json(*value) : "null";
}
template <class A, class B> std::string json(const std::pair<A, B> &value) {
    return "[" + json(value.first) + "," + json(value.second) + "]";
}
template <class T, std::size_t N> std::string json(const std::array<T, N> &values) {
    std::string result = "[";
    for (std::size_t i = 0; i < N; ++i) {
        if (i) {
            result += ',';
        }
        result += json(values[i]);
    }
    return result + "]";
}
template <class T> std::string json(const std::vector<T> &values) {
    std::string result = "[";
    for (std::size_t i = 0; i < values.size(); ++i) {
        if (i) {
            result += ',';
        }
        result += json(values[i]);
    }
    return result + "]";
}
std::string object(std::initializer_list<std::pair<std::string, std::string>> members) {
    std::string result = "{";
    bool first = true;
    for (const auto &[name, value] : members) {
        if (!first) {
            result += ',';
        }
        first = false;
        result += json(name) + ":" + value;
    }
    return result + "}";
}
class Arguments {
    int count_, position_ = 1;
    char **values_;

  public:
    Arguments(int count, char **values) : count_(count), values_(values) {}
    bool empty() const {
        return position_ == count_;
    }
    std::string string() {
        require(position_ < count_, "missing argument");
        return values_[position_++];
    }
    Integer integer() {
        auto text = string();
        std::size_t end;
        Integer value = std::stoll(text, &end);
        require(end == text.size(), "invalid integer argument");
        return value;
    }
    int small() {
        auto value = integer();
        require(value >= std::numeric_limits<int>::min() &&
                    value <= std::numeric_limits<int>::max(),
                "argument outside int range");
        return static_cast<int>(value);
    }
    int count() {
        int value = small();
        require(value >= 0, "negative count");
        return value;
    }
    double number() {
        auto text = string();
        std::size_t end;
        double value = std::stod(text, &end);
        require(end == text.size() && std::isfinite(value), "invalid finite number");
        return value;
    }
    Integers integers(std::size_t size) {
        Integers result;
        for (std::size_t i = 0; i < size; ++i) {
            result.push_back(integer());
        }
        return result;
    }
    Integers remaining_integers() {
        Integers result;
        while (!empty()) {
            result.push_back(integer());
        }
        return result;
    }
    Point point() {
        double x = number();
        double y = number();
        return {x, y};
    }
    std::vector<Point> points(int size) {
        std::vector<Point> result;
        for (int i = 0; i < size; ++i) {
            result.push_back(point());
        }
        return result;
    }
    Graph graph() {
        int vertices = count();
        int directed = small();
        int edges = count();
        require(directed == 0 || directed == 1, "directed flag must be 0 or 1");
        Graph graph(vertices, directed == 1);
        for (int i = 0; i < edges; ++i) {
            int from = small();
            int to = small();
            Integer weight = integer();
            graph.insert(from, to, weight);
        }
        return graph;
    }
};
std::string run(const std::string &operation, Arguments &args) {
    if (operation == "selftest") {
        selftest();
        return "true";
    }
    if (operation == "sort") {
        auto method = args.string();
        return json(sort(method, args.remaining_integers()));
    }
    if (operation == "binary" || operation == "insert") {
        Integer value = args.integer();
        auto values = args.remaining_integers();
        return operation == "binary" ? json(binary_search(values, value))
                                     : json(sentinel_insert(values, value));
    }
    if (operation == "absdiff") {
        BigInteger a(args.string());
        BigInteger b(args.string());
        auto result = (a - b).str();
        if (result.front() == '-') {
            result.erase(result.begin());
        }
        return json(result);
    }
    if (operation == "bigint") {
        auto method = args.string();
        BigInteger a(args.string());
        BigInteger b(args.string());
        if (method == "add") {
            return json((a + b).str());
        }
        if (method == "sub") {
            return json((a - b).str());
        }
        if (method == "mul") {
            return json((a * b).str());
        }
        require(method == "div", "unknown bigint operation");
        return json((a / b).str());
    }
    if (operation == "fib") {
        auto method = args.string();
        int n = args.small();
        return json(fibonacci(method, n).str());
    }
    if (operation == "binomial") {
        int n = args.small();
        int k = args.small();
        return json(binomial(n, k).str());
    }
    if (operation == "gcd") {
        Integer a = args.integer();
        Integer b = args.integer();
        return json(extended_gcd(a, b));
    }
    if (operation == "factors") {
        return json(prime_factors(args.integer()));
    }
    if (operation == "distance") {
        int dimension = args.count();
        std::vector<double> a, b;
        for (int i = 0; i < dimension; ++i) {
            a.push_back(args.number());
        }
        for (int i = 0; i < dimension; ++i) {
            b.push_back(args.number());
        }
        return json(distance(a, b));
    }
    if (operation == "matrix") {
        int rows = args.count();
        int inner = args.count();
        int columns = args.count();
        require(rows > 0 && inner > 0 && columns > 0, "empty matrix dimension");
        Matrix a, b;
        for (int i = 0; i < rows; ++i) {
            a.push_back(args.integers(inner));
        }
        for (int i = 0; i < inner; ++i) {
            b.push_back(args.integers(columns));
        }
        return json(matrix_multiply(a, b));
    }
    if (operation == "convolve") {
        int n = args.count();
        int m = args.count();
        auto a = args.integers(n);
        auto b = args.integers(m);
        return json(convolve(a, b));
    }
    if (operation == "edit" || operation == "editbrute" || operation == "lcs" ||
        operation == "substring") {
        auto a = args.string();
        auto b = args.string();
        if (operation == "edit") {
            auto result = edit_distance(a, b);
            return object({{"cost", json(result.cost)}, {"operations", json(result.operations)}});
        }
        if (operation == "editbrute") {
            return json(brute_edit_distance(a, b));
        }
        if (operation == "lcs") {
            return json(longest_common_subsequence(a, b));
        }
        return json(substring_edit_distance(a, b));
    }
    if (operation == "partition") {
        int count = args.small();
        auto result = linear_partition(args.remaining_integers(), count);
        return object({{"cost", json(result.cost)}, {"groups", json(result.groups)}});
    }
    if (operation == "subsetsum") {
        Integer target = args.integer();
        auto values = args.remaining_integers();
        return json(subset_sum(values, target));
    }
    if (operation == "elevator") {
        int budget = args.small();
        int max_floor = args.small();
        std::vector<int> destinations;
        while (!args.empty()) {
            destinations.push_back(args.small());
        }
        auto result = elevator_stops(destinations, budget, max_floor);
        return object({{"cost", json(result.cost)}, {"stops", json(result.stops)}});
    }
    const std::vector<std::string> graph_operations{
        "bfs",  "dfs", "components", "scc",   "bipartite", "cycle", "articulation",
        "topo", "mst", "dijkstra",   "floyd", "maxflow",   "paths", "edgecount"};
    if (std::find(graph_operations.begin(), graph_operations.end(), operation) !=
        graph_operations.end()) {
        std::string method;
        if (operation == "scc" || operation == "topo" || operation == "mst") {
            method = args.string();
        }
        Graph graph = args.graph();
        if (operation == "bfs") {
            return json(bfs(graph, args.small()).distance);
        }
        if (operation == "dfs") {
            return json(dfs(graph, args.small()));
        }
        if (operation == "components") {
            return json(connected_components(graph));
        }
        if (operation == "scc") {
            return json(strongly_connected(graph, method));
        }
        if (operation == "bipartite") {
            return json(bipartite_coloring(graph).has_value());
        }
        if (operation == "cycle") {
            return json(has_cycle(graph));
        }
        if (operation == "articulation") {
            return json(articulation_points(graph));
        }
        if (operation == "topo") {
            return json(topological_order(graph, method));
        }
        if (operation == "mst") {
            auto result = minimum_spanning_forest(graph, method);
            return object({{"cost", json(result.cost)}, {"edges", json(result.edges)}});
        }
        if (operation == "dijkstra") {
            return json(dijkstra(graph, args.small()));
        }
        if (operation == "floyd") {
            return json(floyd_warshall(graph));
        }
        if (operation == "maxflow") {
            int source = args.small();
            int sink = args.small();
            return json(maximum_flow(graph, source, sink));
        }
        if (operation == "paths") {
            int source = args.small();
            int target = args.small();
            return json(simple_paths(graph, source, target));
        }
        require(graph.edges().size() <=
                    static_cast<std::size_t>(std::numeric_limits<Integer>::max()),
                "edge count overflow");
        return json(static_cast<Integer>(graph.edges().size()));
    }
    if (operation == "hull" || operation == "area" || operation == "triangulate" ||
        operation == "mwt") {
        int n = args.count();
        auto points = args.points(n);
        if (operation == "hull") {
            return json(convex_hull(points));
        }
        if (operation == "area") {
            return json(polygon_area(points));
        }
        if (operation == "triangulate") {
            return json(triangulate(points));
        }
        return json(minimum_weight_triangulation(points));
    }
    if (operation == "segment" || operation == "intersection") {
        auto points = args.points(4);
        if (operation == "segment") {
            return json(segments_intersect(points[0], points[1], points[2], points[3]));
        }
        return json(intersection(points_to_line(points[0], points[1]),
                                 points_to_line(points[2], points[3])));
    }
    if (operation == "project") {
        auto points = args.points(3);
        return json(project(points[0], points_to_line(points[1], points[2])));
    }
    if (operation == "packing") {
        double width = args.number();
        double height = args.number();
        double radius = args.number();
        return json(std::array<Integer, 2>{
            std::max(grid_plates(width, height, radius), grid_plates(height, width, radius)),
            std::max(dense_plates(width, height, radius), dense_plates(height, width, radius))});
    }
    if (operation == "superman") {
        Point start = args.point();
        Point end = args.point();
        int count = args.count();
        std::vector<Circle> circles;
        for (int i = 0; i < count; ++i) {
            Point center = args.point();
            double radius = args.number();
            circles.push_back({center, radius});
        }
        return json(superman(start, end, circles));
    }
    if (operation == "queens") {
        return json(queens(args.small()));
    }
    if (operation == "permutations") {
        return json(permutations(args.small()));
    }
    if (operation == "subsets") {
        return json(subsets(args.small()));
    }
    if (operation == "sudoku") {
        return json(sudoku(args.string()));
    }
    if (operation == "tsp") {
        auto method = args.string();
        int n = args.count();
        auto points = args.points(n);
        std::uint64_t seed = 0;
        int iterations = 1000;
        if (method == "sample" || method == "hill" || method == "anneal") {
            Integer signed_seed = args.integer();
            require(signed_seed >= 0, "negative random seed");
            seed = static_cast<std::uint64_t>(signed_seed);
            iterations = args.small();
        }
        auto result = traveling_salesperson(points, method, seed, iterations);
        return object({{"cost", json(result.cost)}, {"tour", json(result.vertices)}});
    }
    if (operation == "grid") {
        auto method = args.string();
        int rows = args.small();
        int columns = args.small();
        return json(grid_order(method, rows, columns));
    }
    if (operation == "find") {
        auto pattern = args.string();
        auto text = args.string();
        return json(find_match(pattern, text));
    }
    if (operation == "replace") {
        auto text = args.string();
        int count = args.count();
        std::vector<std::pair<std::string, std::string>> rules;
        for (int i = 0; i < count; ++i) {
            auto old_name = args.string();
            auto new_name = args.string();
            rules.emplace_back(old_name, new_name);
        }
        return json(replace_names(text, rules));
    }
    if (operation == "suitors") {
        int n = args.count();
        std::vector<Suitor> suitors;
        for (int i = 0; i < n; ++i) {
            auto first = args.string();
            auto last = args.string();
            Integer height = args.integer();
            Integer weight = args.integer();
            suitors.push_back({first, last, height, weight});
        }
        std::vector<std::pair<std::string, std::string>> result;
        for (const auto &suitor : rank_suitors(suitors)) {
            result.emplace_back(suitor.first, suitor.last);
        }
        return json(result);
    }
    if (operation == "card") {
        return json(encode_card(args.string()));
    }
    if (operation == "uncard") {
        return json(decode_card(args.small()));
    }
    if (operation == "war") {
        int limit = args.small();
        int na = args.count();
        int nb = args.count();
        std::vector<int> a, b;
        for (int i = 0; i < na; ++i) {
            a.push_back(args.small());
        }
        for (int i = 0; i < nb; ++i) {
            b.push_back(args.small());
        }
        auto result = war(a, b, limit);
        return object({{"winner", json(result.winner)}, {"steps", json(result.steps)}});
    }
    throw std::invalid_argument("unknown operation: " + operation);
}
} // namespace
int main(int argc, char **argv) {
    try {
        Arguments args(argc, argv);
        auto operation = args.string();
        auto result = run(operation, args);
        adm::require(args.empty(), "unexpected trailing arguments");
        std::cout << result << '\n';
        return 0;
    } catch (const std::exception &error) {
        std::cerr << error.what() << '\n';
        return 1;
    }
}
