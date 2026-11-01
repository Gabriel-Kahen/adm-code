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

#include <numeric>

namespace adm {
namespace {
void check(bool condition, const std::string &message) {
    require(condition, "selftest: " + message);
}
void near(double actual, double expected, const std::string &message) {
    check(std::abs(actual - expected) <= epsilon * std::max(1.0, std::abs(expected)), message);
}
template <class Function> void rejects(Function operation, const std::string &message) {
    bool rejected = false;
    try {
        operation();
    } catch (const std::exception &) {
        rejected = true;
    }
    check(rejected, message);
}
} // namespace
void selftest() {
    Queue<Integer> queue;
    Stack<Integer> stack;
    MinHeap heap;
    for (Integer i = 0; i < 1000; ++i) {
        queue.push(i);
        stack.push(i);
        heap.push(999 - i);
    }
    for (Integer i = 0; i < 1000; ++i) {
        check(queue.pop() == i, "FIFO order");
        check(stack.pop() == 999 - i, "LIFO order");
        check(heap.pop() == i, "heap order");
    }
    check(queue.empty() && stack.empty() && heap.empty(), "empty containers");
    rejects([&] { queue.pop(); }, "queue underflow");
    rejects([&] { stack.pop(); }, "stack underflow");
    rejects([&] { heap.pop(); }, "heap underflow");
    for (Integer value : {3, 1, 1, 2}) {
        heap.push(value);
    }
    check(heap.size() == 4 && heap.pop() == 1 && heap.pop() == 1, "heap duplicates");
    DisjointSet sets(5);
    check(sets.unite(0, 1) && sets.unite(2, 3) && sets.unite(0, 3), "union changes components");
    check(!sets.unite(1, 2) && sets.find(1) == sets.find(3) && sets.find(4) != sets.find(0),
          "union-find membership");
    rejects([&] { sets.find(5); }, "set bounds");
    LinkedList list;
    for (Integer value : {1, 2, 1, 3}) {
        list.insert(value);
    }
    check(list.values() == Integers({3, 1, 2, 1}), "list head insertion");
    check(list.erase(3) && list.erase(2) && list.erase(1) && list.values() == Integers({1}),
          "list erase head/middle/one duplicate");
    check(list.contains(1) && !list.contains(9) && !list.erase(9), "list membership");
    check(list.erase(1) && list.values().empty(), "list erase last");
    BinarySearchTree tree;
    for (Integer value : {5, 3, 8, 2, 4, 6, 9, 7, 5}) {
        tree.insert(value);
    }
    check(tree.values() == Integers({2, 3, 4, 5, 6, 7, 8, 9}), "BST set order");
    check(tree.erase(5) && tree.erase(2) && tree.erase(6) && tree.contains(7) &&
              !tree.contains(5) && !tree.erase(10),
          "BST root/leaf/one-child deletion");
    check(tree.values() == Integers({3, 4, 7, 8, 9}), "BST after deletion");
    const std::vector<std::string> methods{"insertion", "selection", "quick", "heap", "merge"};
    for (const auto &method : methods) {
        check(sort(method, {3, -1, 3, 0}) == Integers({-1, 0, 3, 3}), "sort " + method);
    }
    check(binary_search({1, 2, 2, 3}, 2) == 1 && binary_search({}, 2) == -1,
          "binary first occurrence");
    check(sentinel_insert({1, 2}, std::numeric_limits<Integer>::min()) ==
              Integers({std::numeric_limits<Integer>::min(), 1, 2}),
          "sentinel finite minimum");
    rejects([&] { binary_search({2, 1}, 1); }, "binary sorted contract");
    for (Integer a = -20; a <= 20; ++a) {
        for (Integer b = -20; b <= 20; ++b) {
            BigInteger x(a), y(b);
            check((x + y).str() == std::to_string(a + b), "bigint signed addition");
            check((x - y).str() == std::to_string(a - b), "bigint signed subtraction");
            check((x * y).str() == std::to_string(a * b), "bigint signed multiplication");
            if (b) {
                check((x / y).str() == std::to_string(a / b), "bigint truncating division");
            }
        }
    }
    check((BigInteger("999999999999999999999999") * BigInteger("999999999999999999999999")).str() ==
              "999999999999999999999998000000000000000000000001",
          "bigint unbounded product");
    check((BigInteger("-000") / BigInteger(3)).str() == "0", "bigint normalized zero");
    rejects([&] { (void)(BigInteger(1) / BigInteger(0)); }, "bigint zero divisor");
    for (const auto &method : {"recursive", "memo", "table", "constant"}) {
        check(fibonacci(method, 10).str() == "55", "Fibonacci variants");
    }
    check(binomial(100, 50).str() == "100891344545564193334812497256", "large binomial");
    auto gcd = extended_gcd(-240, 46);
    check(gcd[0] == 2 && -240 * gcd[1] + 46 * gcd[2] == 2, "signed Bezout");
    check(prime_factors(360) == Integers({2, 2, 2, 3, 3, 5}), "prime factors");
    near(distance({1, 2, 3}, {1, 2, 7}), 4, "N-D distance");
    check(matrix_multiply({{1, 2}}, {{3}, {4}}) == Matrix({{11}}), "matrix product");
    check(convolve({1, 2}, {3, 4}) == Integers({3, 10, 8}), "convolution");
    rejects([&] { add(std::numeric_limits<Integer>::max(), 1); }, "checked addition");
    Random random(42), same(42);
    for (int i = 0; i < 100; ++i) {
        Integer a = random.integer(-10, 10), b = same.integer(-10, 10);
        check(a == b && a >= -10 && a <= 10, "seeded integer RNG");
        double x = random.real(-2, 3), y = same.real(-2, 3);
        check(x == y && x >= -2 && x < 3, "seeded real RNG");
    }
    Integers permutation{0, 1, 2, 3, 4, 5};
    random.shuffle(permutation);
    std::sort(permutation.begin(), permutation.end());
    check(permutation == Integers({0, 1, 2, 3, 4, 5}), "Fisher-Yates permutation");
    Graph graph(5);
    graph.insert(0, 1);
    graph.insert(0, 1);
    graph.insert(1, 2);
    graph.insert(3, 4);
    check(graph.edges().size() == 4 && has_cycle(graph), "graph parallel edges");
    check(articulation_points(graph) == std::vector<int>({1}), "multigraph cut vertex");
    auto breadth = bfs(graph, 0);
    check(reconstruct_path(breadth.parent, 0, 2) == std::vector<int>({0, 1, 2}) &&
              reconstruct_path(breadth.parent, 0, 3).empty(),
          "path reconstruction reachable/unreachable");
    check(graph.erase(1, 0) && !has_cycle(graph), "delete one reverse-oriented undirected edge");
    check(graph.erase(0, 1) && !graph.erase(0, 1), "delete last edge");
    check(connected_components(graph) == Groups({{0}, {1, 2}, {3, 4}}),
          "components after mutation");
    check(dfs(graph, 1) == std::vector<int>({1, 2}) && bipartite_coloring(graph).has_value(),
          "DFS/coloring");
    Graph directed_graph(4, true);
    directed_graph.insert(0, 1, 2);
    directed_graph.insert(1, 0, 1);
    directed_graph.insert(1, 2, 4);
    for (const auto &method : {"tarjan", "kosaraju"}) {
        check(strongly_connected(directed_graph, method) == Groups({{0, 1}, {2}, {3}}),
              "SCC variants");
    }
    rejects([&] { topological_order(directed_graph, "kahn"); }, "toposort cycle");
    check(directed_graph.erase(1, 0), "directed deletion");
    for (const auto &method : {"kahn", "dfs"}) {
        auto order = topological_order(directed_graph, method);
        check(std::find(order.begin(), order.end(), 0) < std::find(order.begin(), order.end(), 1),
              "topological variants");
    }
    check(dijkstra(directed_graph, 0)[2] == 6 && !dijkstra(directed_graph, 0)[3], "shortest paths");
    check(floyd_warshall(directed_graph)[0][2] == 6, "Floyd paths");
    Graph weighted(4);
    weighted.insert(0, 1, 5);
    weighted.insert(1, 2, -2);
    weighted.insert(0, 2, 7);
    for (const auto &method : {"prim", "kruskal"}) {
        check(minimum_spanning_forest(weighted, method).cost == 3, "MST forest variants");
    }
    Graph network(4, true);
    network.insert(0, 1, 2);
    network.insert(0, 1, 3);
    network.insert(1, 0, 2);
    network.insert(1, 3, 4);
    network.insert(0, 2, 2);
    network.insert(2, 3, 3);
    check(maximum_flow(network, 0, 3) == 6, "parallel/antiparallel maximum flow");
    check(simple_paths(network, 0, 3) == Groups({{0, 1, 3}, {0, 2, 3}}), "unique simple paths");
    check(edit_distance("kitten", "sitting").cost == 3 && brute_edit_distance("a", "b") == 1,
          "edit variants");
    check(longest_common_subsequence("abc", "ac") == "ac" &&
              substring_edit_distance("abc", "xxabcxx") == 0,
          "string variants");
    auto partition = linear_partition({2, 3, 5}, 2);
    check(partition.cost == 5 && partition.groups.size() == 2, "linear partition");
    check(subset_sum({1, 3, 4}, 7) == std::optional<std::vector<int>>({{1, 2}}),
          "subset-sum witness");
    check(elevator_stops({2, 4}, 1, 4).cost == 2 && elevator_stops({2, 4}, 0, 4).cost == 6,
          "elevator budget");
    Point a{0, 0}, b{2, 0}, c{0, 2};
    check(orientation(a, b, c) == 1 && orientation(a, c, b) == -1 && orientation(a, b, {1, 0}) == 0,
          "orientation predicates");
    near(triangle_area(a, b, c), 2, "triangle area");
    Line horizontal = points_to_line(a, b), vertical = points_to_line(a, c);
    check(parallel(horizontal, point_slope_line({0, 1}, 0)) &&
              same_line(horizontal, points_to_line(b, a)),
          "line equivalence");
    auto crossing = intersection(horizontal, vertical);
    check(crossing.has_value(), "line unique intersection");
    near(crossing->x, 0, "intersection x");
    near(project({1, 3}, horizontal).y, 0, "projection");
    check(!intersection(horizontal, point_slope_line({0, 1}, 0)), "parallel line intersection");
    check(in_box({1, 0}, a, b) && segments_intersect(a, b, {1, 0}, {3, 0}),
          "box/collinear segment");
    const double nan = std::numeric_limits<double>::quiet_NaN();
    const double infinity = std::numeric_limits<double>::infinity();
    rejects([&] { cross({nan, 0}, a, b); }, "nonfinite cross-product input");
    rejects([&] { triangle_area({0, 0}, {1e308, 0}, {0, 1e308}); }, "triangle area overflow");
    rejects([&] { in_box({infinity, 0}, a, b); }, "nonfinite box input");
    for (double tolerance : {-1.0, infinity, nan}) {
        rejects([&] { orientation(a, b, a, tolerance); }, "orientation tolerance");
        rejects([&] { in_box(a, a, b, tolerance); }, "box tolerance");
        rejects([&] { parallel(horizontal, horizontal, tolerance); }, "parallel tolerance");
        rejects([&] { same_line(horizontal, horizontal, tolerance); }, "line equality tolerance");
        rejects([&] { intersection(horizontal, vertical, tolerance); }, "intersection tolerance");
    }
    rejects([&] { parallel({1e-320, 0, 1}, {1e-320, 0, 1}); }, "line normalization overflow");
    rejects([&] { hex_to_cartesian({1e308, 1e308}, 1); }, "Cartesian conversion overflow");
    rejects([&] { cartesian_to_hex({1e308, 1e308}, 1e-308); }, "hex conversion overflow");
    const std::vector<Point> square{{0, 0}, {1, 0}, {1, 1}, {0, 1}};
    check(convex_hull({{0, 0}, {1, 0}, {0.5, 0}, {0, 0}}).size() == 2, "collinear hull");
    check(triangulate(square).size() == 2, "ear triangulation");
    near(minimum_weight_triangulation(square), 4 + 2 * std::sqrt(2.0), "convex minimum weight");
    check(dense_layers(4, 4, 1) == 2 && plates_per_row(1, 4, 1) == 1 &&
              dense_plates(4, 4, 1) == 3 && grid_plates(4, 4, 1) == 4,
          "packing helpers");
    for (int row = -3; row <= 3; ++row) {
        for (int column = -3; column <= 3; ++column) {
            auto hex = array_to_hex(row, column);
            check(hex_to_array(hex.first, hex.second) == std::make_pair(row, column),
                  "array/hex inverse");
            Point original{static_cast<double>(row), static_cast<double>(column)};
            Point roundtrip = cartesian_to_hex(hex_to_cartesian(original, 1.2), 1.2);
            near(roundtrip.x, original.x, "hex Cartesian row");
            near(roundtrip.y, original.y, "hex Cartesian diagonal");
        }
    }
    check(plates_on_top(0, 0, 4, 4, 1) == 1, "plates supported above");
    auto flight = superman({-2, 0}, {2, 0}, {{{0, 0}, 1}});
    near(flight.first, 2, "Superman chord");
    near(flight.second, 2 + std::acos(-1.0), "Superman arc");
    std::vector<int> prefix;
    int balance = 0, visited = 0;
    auto complete = [](const auto &path) { return path.size() == 3; };
    auto candidates = [](const auto &) { return std::vector<int>{0, 1}; };
    check(backtrack(
              prefix, complete, candidates, [&](int) { ++balance; }, [&](int) { --balance; },
              [&](const auto &) {
                  ++visited;
                  return true;
              }),
          "generic early stop");
    check(balance == 0 && prefix.empty() && visited == 1, "balanced undo on stop");
    rejects(
        [&] {
            backtrack(
                prefix, complete, candidates, [&](int) { ++balance; }, [&](int) { --balance; },
                [&](const auto &) -> bool { throw std::runtime_error("visit"); });
        },
        "visitor exception propagates");
    check(balance == 0 && prefix.empty(), "balanced undo on exception");
    check(permutations(0) == Groups({{}}) && permutations(4).size() == 24 &&
              subsets(4).size() == 16 && queens(8) == 92 && queens(0) == 1,
          "search enumeration");
    auto solved =
        sudoku("530070000600195000098000060800060003400803001700020006060000280000419005000080079");
    check(solved && solved->find('0') == std::string::npos, "Sudoku solve");
    const std::string almost_solved =
        "034678912672195348198342567859761423426853791713924856961537284287419635345286179";
    for (bool smart : {false, true}) {
        for (bool fast : {false, true}) {
            auto solution = sudoku(almost_solved, smart, fast);
            check(solution && solution->front() == '5', "Sudoku heuristic combinations");
        }
    }
    for (int i = 0; i < 4; ++i) {
        for (int j = 0; j < 4; ++j) {
            std::vector<int> tour{0, 1, 2, 3}, changed = tour;
            std::swap(changed[i], changed[j]);
            near(swap_delta(square, tour, i, j),
                 tour_cost(square, changed) - tour_cost(square, tour),
                 "TSP swap delta adjacent/wrap/equal");
        }
    }
    for (const auto &method : {"exact", "best"}) {
        near(traveling_salesperson(square, method).cost, 4, "exact TSP variants");
    }
    for (const auto &method : {"sample", "hill", "anneal"}) {
        auto tour = traveling_salesperson(square, method, 7, 100);
        near(tour.cost, tour_cost(square, tour.vertices), "heuristic recomputed objective");
    }
    for (const auto &method : {"sample", "hill", "anneal"}) {
        auto first = traveling_salesperson(square, method, 12, 10);
        auto restarted = repeated_traveling_salesperson(square, method, 3, 12, 10);
        check(restarted.cost <= first.cost, "TSP restarts retain best");
    }
    rejects([&] { repeated_traveling_salesperson(square, "hill", 0); },
            "invalid TSP restart count");
    check(grid_order("diagonal", 2, 3).size() == 6, "rectangular traversal");
    check(find_match("", "abc") == 0 && replace_names("aaa", {{"a", "aa"}}) == "aaaaaa",
          "nonrecursive replacement");
    auto ranked = rank_suitors({{"B", "Z", 180, 80}, {"A", "Y", 180, 75}});
    check(ranked[0].first == "A", "suitor lexicographic priority");
    for (int card = 0; card < 52; ++card) {
        check(encode_card(decode_card(card)) == card, "card roundtrip");
    }
    check(war({48}, {0}, 10).winner == "a", "War winner");
    check(war({0}, {1}, 10).winner == "draw", "War tied exhaustion");
    check(war({48}, {0}, 0).steps == 0, "War step limit");
}
} // namespace adm
