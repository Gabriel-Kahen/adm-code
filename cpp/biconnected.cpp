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

namespace adm {
std::vector<int> articulation_points(const Graph &graph) {
    undirected(graph);
    std::vector<int> entered(graph.size(), -1), low(graph.size());
    std::vector<bool> cut(graph.size());
    int clock = 0;
    std::function<void(int, std::size_t)> visit = [&](int vertex, std::size_t parent_edge) {
        entered[vertex] = low[vertex] = clock++;
        int children = 0;
        for (const auto &edge : graph.neighbors(vertex)) {
            if (edge.id == parent_edge) {
                continue;
            }
            if (entered[edge.to] == -1) {
                ++children;
                visit(edge.to, edge.id);
                low[vertex] = std::min(low[vertex], low[edge.to]);
                if (parent_edge != std::numeric_limits<std::size_t>::max() &&
                    low[edge.to] >= entered[vertex]) {
                    cut[vertex] = true;
                }
            } else {
                low[vertex] = std::min(low[vertex], entered[edge.to]);
            }
        }
        if (parent_edge == std::numeric_limits<std::size_t>::max() && children > 1) {
            cut[vertex] = true;
        }
    };
    for (int vertex = 0; vertex < graph.size(); ++vertex) {
        if (entered[vertex] == -1) {
            visit(vertex, std::numeric_limits<std::size_t>::max());
        }
    }
    std::vector<int> result;
    for (int vertex = 0; vertex < graph.size(); ++vertex) {
        if (cut[vertex]) {
            result.push_back(vertex);
        }
    }
    return result;
}
} // namespace adm

#ifdef ADM_DEMO
int main() {
    using namespace adm;
    try {
        auto graph = read_graph(std::cin, false);
        for (auto vertex : articulation_points(graph)) {
            std::cout << vertex << " ";
        }
        std::cout << "\n";
    } catch (const std::exception &error) {
        std::cerr << error.what() << "\n";
        return 1;
    }
}
#endif
