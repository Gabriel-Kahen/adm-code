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
std::vector<int> topological_dfs(const Graph &graph) {
    directed(graph);
    std::vector<int> result;

    std::vector<int> color(graph.size());
    std::function<void(int)> visit = [&](int vertex) {
        require(color[vertex] != 1, "topological order requires acyclic graph");
        if (color[vertex] == 2) {
            return;
        }
        color[vertex] = 1;
        for (const auto &edge : graph.neighbors(vertex)) {
            visit(edge.to);
        }
        color[vertex] = 2;
        result.push_back(vertex);
    };
    for (int vertex = 0; vertex < graph.size(); ++vertex) {
        if (!color[vertex]) {
            visit(vertex);
        }
    }
    std::reverse(result.begin(), result.end());

    return result;
}
} // namespace adm

#ifdef ADM_DEMO
int main() {
    using namespace adm;
    try {
        auto graph = read_graph(std::cin, true);
        for (auto vertex : topological_dfs(graph)) {
            std::cout << vertex << " ";
        }
        std::cout << "\n";
    } catch (const std::exception &error) {
        std::cerr << error.what() << "\n";
        return 1;
    }
}
#endif
