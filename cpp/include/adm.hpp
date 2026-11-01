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

#ifndef ADM_HPP
#define ADM_HPP

#include <algorithm>
#include <array>
#include <cmath>
#include <cstdint>
#include <deque>
#include <functional>
#include <limits>
#include <memory>
#include <optional>
#include <random>
#include <stdexcept>
#include <string>
#include <tuple>
#include <utility>
#include <vector>

// Independent, zero-based teaching implementations. See cpp/README.md.
namespace adm {
using Integer = long long;
using Integers = std::vector<Integer>;
using Matrix = std::vector<Integers>;
Integer add(Integer a, Integer b);
Integer subtract(Integer a, Integer b);
Integer multiply(Integer a, Integer b);
void require(bool condition, const std::string &message);

// Exact signed decimal integers. No fixed digit capacity.
class BigInteger {
    std::string digits_; // Magnitude, most significant digit first.
    bool negative_ = false;
    static int compare_magnitude(const std::string &, const std::string &);
    static std::string add_magnitude(const std::string &, const std::string &);
    static std::string subtract_magnitude(const std::string &, const std::string &);
    void normalize();

  public:
    explicit BigInteger(const std::string &value = "0");
    explicit BigInteger(Integer value);
    std::string str() const;
    BigInteger operator-() const;
    friend BigInteger operator+(const BigInteger &, const BigInteger &);
    friend BigInteger operator-(const BigInteger &, const BigInteger &);
    friend BigInteger operator*(const BigInteger &, const BigInteger &);
    friend BigInteger operator/(const BigInteger &, const BigInteger &);
};
BigInteger fibonacci(const std::string &method, int n);
BigInteger binomial(int n, int k);
std::array<Integer, 3> extended_gcd(Integer a, Integer b);
Integers prime_factors(Integer n);
double distance(const std::vector<double> &a, const std::vector<double> &b);
Matrix matrix_multiply(const Matrix &a, const Matrix &b);
Integers convolve(const Integers &a, const Integers &b);
class Random {
    std::mt19937_64 engine_;

  public:
    explicit Random(std::uint64_t seed) : engine_(seed) {}
    Integer integer(Integer low, Integer high);
    double real(double low, double high);
    template <class T> void shuffle(std::vector<T> &values) {
        for (std::size_t remaining = values.size(); remaining > 1; --remaining) {
            auto choice = static_cast<std::size_t>(integer(0, static_cast<Integer>(remaining - 1)));
            std::swap(values[remaining - 1], values[choice]);
        }
    }
};

template <class T> class Queue {
    std::deque<T> values_;

  public:
    void push(T value) {
        values_.push_back(std::move(value));
    }
    T pop() {
        require(!empty(), "empty queue");
        T value = std::move(values_.front());
        values_.pop_front();
        return value;
    }
    bool empty() const {
        return values_.empty();
    }
    std::size_t size() const {
        return values_.size();
    }
};
template <class T> class Stack {
    std::vector<T> values_;

  public:
    void push(T value) {
        values_.push_back(std::move(value));
    }
    T pop() {
        require(!empty(), "empty stack");
        T value = std::move(values_.back());
        values_.pop_back();
        return value;
    }
    bool empty() const {
        return values_.empty();
    }
    std::size_t size() const {
        return values_.size();
    }
};
class MinHeap {
    Integers values_;

  public:
    void push(Integer value);
    Integer pop();
    bool empty() const {
        return values_.empty();
    }
    std::size_t size() const {
        return values_.size();
    }
};
class DisjointSet {
    std::vector<int> parent_, size_;

  public:
    explicit DisjointSet(int n);
    int find(int vertex);
    bool unite(int a, int b);
};
class LinkedList {
    struct Node {
        Integer value;
        std::unique_ptr<Node> next;
        explicit Node(Integer value) : value(value) {}
    };
    std::unique_ptr<Node> head_;

  public:
    // Insert at head; duplicates allowed. Erase removes the first occurrence.
    void insert(Integer value);
    bool contains(Integer value) const;
    bool erase(Integer value);
    Integers values() const;
};
class BinarySearchTree {
    struct Node {
        Integer value;
        std::unique_ptr<Node> left, right;
        explicit Node(Integer value) : value(value) {}
    };
    std::unique_ptr<Node> root_;
    static bool erase_node(std::unique_ptr<Node> &node, Integer value);

  public:
    // Set semantics: duplicate inserts do nothing.
    void insert(Integer value);
    bool contains(Integer value) const;
    bool erase(Integer value);
    Integers values() const;
};
Integers sort(const std::string &method, Integers values);
int binary_search(const Integers &values, Integer target);
Integers sentinel_insert(Integers sorted, Integer value);

struct Edge {
    int from, to;
    Integer weight;
};
struct Arc {
    int to;
    Integer weight;
    std::size_t id;
};
class Graph {
    int vertices_;
    bool directed_;
    std::vector<Edge> edges_;
    std::vector<std::vector<Arc>> adjacency_;
    void rebuild();

  public:
    explicit Graph(int vertices, bool directed = false);
    int size() const {
        return vertices_;
    }
    bool directed() const {
        return directed_;
    }
    const std::vector<Edge> &edges() const {
        return edges_;
    }
    const std::vector<Arc> &neighbors(int vertex) const;
    void validate_vertex(int vertex) const;
    void insert(int from, int to, Integer weight = 1);
    bool erase(int from, int to); // Remove one matching input edge.
};
using Distances = std::vector<std::optional<Integer>>;
using Groups = std::vector<std::vector<int>>;
struct BreadthFirst {
    Distances distance;
    std::vector<int> parent;
};
BreadthFirst bfs(const Graph &graph, int source);
std::vector<int> reconstruct_path(const std::vector<int> &parent, int source, int target);
std::vector<int> dfs(const Graph &graph, int source);
Groups connected_components(const Graph &graph);
std::optional<std::vector<int>> bipartite_coloring(const Graph &graph);
bool has_cycle(const Graph &graph);
std::vector<int> articulation_points(const Graph &graph);
Groups strongly_connected(const Graph &graph, const std::string &method);
std::vector<int> topological_order(const Graph &graph, const std::string &method);
struct SpanningForest {
    Integer cost = 0;
    std::vector<Edge> edges;
};
SpanningForest minimum_spanning_forest(const Graph &graph, const std::string &method);
Distances dijkstra(const Graph &graph, int source);
std::vector<Distances> floyd_warshall(const Graph &graph);
Integer maximum_flow(const Graph &graph, int source, int sink);
Groups simple_paths(const Graph &graph, int source, int target);

struct EditResult {
    Integer cost;
    std::string operations;
};
EditResult edit_distance(const std::string &a, const std::string &b);
Integer brute_edit_distance(const std::string &a, const std::string &b);
std::string longest_common_subsequence(const std::string &a, const std::string &b);
Integer substring_edit_distance(const std::string &pattern, const std::string &text);
struct Partition {
    Integer cost;
    Matrix groups;
};
Partition linear_partition(const Integers &values, int groups);
std::optional<std::vector<int>> subset_sum(const Integers &values, Integer target);
struct Elevator {
    Integer cost;
    std::vector<int> stops;
};
Elevator elevator_stops(const std::vector<int> &destinations, int budget, int max_floor);

constexpr double epsilon = 1e-9;
struct Point {
    double x, y;
};
struct Line {
    double a, b, c;
};
struct Circle {
    Point center;
    double radius;
};
double cross(Point a, Point b, Point c);
int orientation(Point a, Point b, Point c, double tolerance = epsilon);
double triangle_area(Point a, Point b, Point c);
double point_distance(Point a, Point b);
Line points_to_line(Point a, Point b);
Line point_slope_line(Point p, double slope);
bool parallel(Line a, Line b, double tolerance = epsilon);
bool same_line(Line a, Line b, double tolerance = epsilon);
std::optional<Point> intersection(Line a, Line b, double tolerance = epsilon);
Point project(Point point, Line line);
bool in_box(Point p, Point a, Point b, double tolerance = epsilon);
bool segments_intersect(Point a, Point b, Point c, Point d, double tolerance = epsilon);
double polygon_area(const std::vector<Point> &points);
std::vector<Point> convex_hull(std::vector<Point> points);
std::vector<std::array<int, 3>> triangulate(const std::vector<Point> &polygon);
double minimum_weight_triangulation(const std::vector<Point> &polygon);
Integer dense_layers(double width, double height, double radius);
Integer plates_per_row(Integer row, double width, double radius);
Integer dense_plates(double width, double height, double radius);
Integer grid_plates(double width, double height, double radius);
Point hex_to_cartesian(Point hex, double radius);
Point cartesian_to_hex(Point point, double radius);
std::pair<int, int> array_to_hex(int row, int column);
std::pair<int, int> hex_to_array(int row, int column);
Integer plates_on_top(int row, int diagonal, double width, double height, double radius);
std::pair<double, double> superman(Point start, Point end, const std::vector<Circle> &circles);

// Generic backtracking calls undo after EVERY make, even when visit stops early.
// Returning true from visit requests early termination. State is held by callbacks.
using Candidates = std::function<std::vector<int>(const std::vector<int> &)>;
bool backtrack(std::vector<int> &prefix,
               const std::function<bool(const std::vector<int> &)> &complete,
               const Candidates &candidates, const std::function<void(int)> &make,
               const std::function<void(int)> &undo,
               const std::function<bool(const std::vector<int> &)> &visit);
Groups permutations(int n);
Groups subsets(int n);
Integer queens(int n);
std::optional<std::string> sudoku(const std::string &board, bool smart = true, bool fast = true);
struct Tour {
    double cost;
    std::vector<int> vertices;
};
double tour_cost(const std::vector<Point> &points, const std::vector<int> &tour);
double swap_delta(const std::vector<Point> &points, const std::vector<int> &tour, int a, int b);
Tour traveling_salesperson(const std::vector<Point> &points, const std::string &method,
                           std::uint64_t seed = 0, int iterations = 1000);

Tour repeated_traveling_salesperson(const std::vector<Point> &points, const std::string &method,
                                    int runs, std::uint64_t seed = 0, int iterations = 1000);

std::vector<std::pair<int, int>> grid_order(const std::string &method, int rows, int columns);
int find_match(const std::string &pattern, const std::string &text);
std::string replace_names(std::string text,
                          const std::vector<std::pair<std::string, std::string>> &rules);
struct Suitor {
    std::string first, last;
    Integer height, weight;
};
std::vector<Suitor> rank_suitors(std::vector<Suitor> suitors);
int encode_card(const std::string &card);
std::string decode_card(int card);
struct WarResult {
    std::string winner;
    int steps;
};
WarResult war(const std::vector<int> &a, const std::vector<int> &b, int limit);
void selftest();
} // namespace adm
#endif
