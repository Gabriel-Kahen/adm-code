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
#include "set_union.hpp"
#include "graph.hpp"
#include "wgraph.hpp"

namespace adm {
SpanningForest kruskal(const Graph &graph) {
    undirected(graph);
    SpanningForest result;

    auto edges = graph.edges();
    std::stable_sort(edges.begin(), edges.end(),
                     [](const Edge &a, const Edge &b) { return a.weight < b.weight; });
    DisjointSet sets(graph.size());
    for (const auto &edge : edges) {
        if (sets.unite(edge.from, edge.to)) {
            result.edges.push_back(edge);
            result.cost = add(result.cost, edge.weight);
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
        std::cout << kruskal(graph).cost << "\n";
    } catch (const std::exception &error) {
        std::cerr << error.what() << "\n";
        return 1;
    }
}
#endif
