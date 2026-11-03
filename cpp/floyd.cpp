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
std::vector<Distances> floyd_warshall(const Graph &graph) {
    std::vector<Distances> distance(graph.size(), Distances(graph.size()));
    for (int vertex = 0; vertex < graph.size(); ++vertex) {
        distance[vertex][vertex] = 0;
        for (const auto &edge : graph.neighbors(vertex)) {
            auto &entry = distance[vertex][edge.to];
            if (!entry || edge.weight < *entry) {
                entry = edge.weight;
            }
        }
    }
    for (int via = 0; via < graph.size(); ++via) {
        for (int from = 0; from < graph.size(); ++from) {
            if (!distance[from][via]) {
                continue;
            }
            for (int to = 0; to < graph.size(); ++to) {
                if (!distance[via][to]) {
                    continue;
                }
                Integer candidate = add(*distance[from][via], *distance[via][to]);
                if (!distance[from][to] || candidate < *distance[from][to]) {
                    distance[from][to] = candidate;
                }
            }
        }
    }
    for (int vertex = 0; vertex < graph.size(); ++vertex) {
        require(*distance[vertex][vertex] >= 0, "negative cycle");
    }
    return distance;
}
} // namespace adm

#ifdef ADM_DEMO
int main() {
    using namespace adm;
    try {
        auto graph = read_weighted_graph(std::cin, false);
        for (auto row : floyd_warshall(graph)) {
            for (auto value : row) {
                if (value) {
                    std::cout << *value;
                } else {
                    std::cout << "unreachable";
                }
                std::cout << " ";
            }
            std::cout << "\n";
        }
    } catch (const std::exception &error) {
        std::cerr << error.what() << "\n";
        return 1;
    }
}
#endif
