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
Groups kosaraju(const Graph &graph) {
    directed(graph);
    Groups groups;

    Graph reverse(graph.size(), true);
    for (const auto &edge : graph.edges()) {
        reverse.insert(edge.to, edge.from, edge.weight);
    }
    std::vector<bool> seen(graph.size());
    std::vector<int> finish;
    std::function<void(int)> first = [&](int vertex) {
        seen[vertex] = true;
        for (const auto &edge : graph.neighbors(vertex)) {
            if (!seen[edge.to]) {
                first(edge.to);
            }
        }
        finish.push_back(vertex);
    };
    for (int vertex = 0; vertex < graph.size(); ++vertex) {
        if (!seen[vertex]) {
            first(vertex);
        }
    }
    std::fill(seen.begin(), seen.end(), false);
    std::function<void(int, std::vector<int> &)> second = [&](int vertex, std::vector<int> &group) {
        seen[vertex] = true;
        group.push_back(vertex);
        for (const auto &edge : reverse.neighbors(vertex)) {
            if (!seen[edge.to]) {
                second(edge.to, group);
            }
        }
    };
    for (auto it = finish.rbegin(); it != finish.rend(); ++it) {
        if (!seen[*it]) {
            groups.emplace_back();
            second(*it, groups.back());
        }
    }

    return canonical(std::move(groups));
}
} // namespace adm

#ifdef ADM_DEMO
int main() {
    using namespace adm;
    try {
        auto graph = read_graph(std::cin, true);
        for (auto row : kosaraju(graph)) {
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
