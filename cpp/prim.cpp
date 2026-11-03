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

namespace adm {
SpanningForest prim(const Graph &graph) {
    undirected(graph);
    SpanningForest result;

    using Choice = std::tuple<Integer, int, int>;
    std::priority_queue<Choice, std::vector<Choice>, std::greater<Choice>> ready;
    std::vector<bool> seen(graph.size());
    for (int root = 0; root < graph.size(); ++root) {
        if (seen[root]) {
            continue;
        }
        ready.emplace(0, root, -1);
        while (!ready.empty()) {
            auto [weight, vertex, parent] = ready.top();
            ready.pop();
            if (seen[vertex]) {
                continue;
            }
            seen[vertex] = true;
            if (parent != -1) {
                result.edges.push_back({parent, vertex, weight});
                result.cost = add(result.cost, weight);
            }
            for (const auto &edge : graph.neighbors(vertex)) {
                if (!seen[edge.to]) {
                    ready.emplace(edge.weight, edge.to, vertex);
                }
            }
        }
    }

    return result;
}
} // namespace adm

#ifdef ADM_DEMO
int main() {
    using namespace adm;
    try {
        auto graph = read_weighted_graph(std::cin, false);
        std::cout << prim(graph).cost << "\n";
    } catch (const std::exception &error) {
        std::cerr << error.what() << "\n";
        return 1;
    }
}
#endif
