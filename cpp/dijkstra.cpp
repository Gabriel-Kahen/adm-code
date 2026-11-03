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

#include "item.hpp"
#include "graph.hpp"
#include "wgraph.hpp"
#include "distance.hpp"

namespace adm {
Distances dijkstra(const Graph &graph, int source) {
    graph.validate_vertex(source);
    for (const auto &edge : graph.edges()) {
        require(edge.weight >= 0, "Dijkstra requires nonnegative edges");
    }
    Distances distance(graph.size());
    distance[source] = 0;
    using Choice = std::pair<Integer, int>;
    std::priority_queue<Choice, std::vector<Choice>, std::greater<Choice>> ready;
    ready.emplace(0, source);
    while (!ready.empty()) {
        auto [cost, vertex] = ready.top();
        ready.pop();
        if (cost != distance[vertex]) {
            continue;
        }
        for (const auto &edge : graph.neighbors(vertex)) {
            Integer candidate = add(cost, edge.weight);
            if (!distance[edge.to] || candidate < *distance[edge.to]) {
                distance[edge.to] = candidate;
                ready.emplace(candidate, edge.to);
            }
        }
    }
    return distance;
}
} // namespace adm

#ifdef ADM_DEMO
int main() {
    using namespace adm;
    try {
        auto graph = read_weighted_graph(std::cin);
        for (auto value : dijkstra(graph, 0)) {
            if (value) {
                std::cout << *value;
            } else {
                std::cout << "unreachable";
            }
            std::cout << " ";
        }
        std::cout << "\n";
    } catch (const std::exception &error) {
        std::cerr << error.what() << "\n";
        return 1;
    }
}
#endif
