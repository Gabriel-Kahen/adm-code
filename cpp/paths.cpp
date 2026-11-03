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
Groups simple_paths(const Graph &graph, int source, int target) {
    graph.validate_vertex(source);
    graph.validate_vertex(target);
    Groups result;
    std::vector<int> path{source};
    std::vector<bool> used(graph.size());
    used[source] = true;
    std::function<void(int)> visit = [&](int vertex) {
        if (vertex == target) {
            result.push_back(path);
            return;
        }
        std::set<int> unique_neighbors;
        for (const auto &edge : graph.neighbors(vertex)) {
            unique_neighbors.insert(edge.to);
        }
        for (int next : unique_neighbors) {
            if (!used[next]) {
                used[next] = true;
                path.push_back(next);
                visit(next);
                path.pop_back();
                used[next] = false;
            }
        }
    };
    visit(source);
    std::sort(result.begin(), result.end());
    return result;
}
} // namespace adm

#ifdef ADM_DEMO
int main() {
    using namespace adm;
    try {
        auto graph = read_graph(std::cin, false);
        for (auto row : simple_paths(graph, 0, graph.size() - 1)) {
            for (auto vertex : row) {
                std::cout << vertex << " ";
            }
            std::cout << "\n";
        }
    } catch (const std::exception &error) {
        std::cerr << error.what() << "\n";
        return 1;
    }
}
#endif
