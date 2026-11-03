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
#include "bfs-dfs.hpp"
#include "distance.hpp"

namespace adm {
BreadthFirst bfs(const Graph &graph, int source) {
    graph.validate_vertex(source);
    BreadthFirst result{Distances(graph.size()), std::vector<int>(graph.size(), -1)};
    std::deque<int> pending{source};
    result.distance[source] = 0;
    while (!pending.empty()) {
        int vertex = pending.front();
        pending.pop_front();
        for (const auto &edge : graph.neighbors(vertex)) {
            if (!result.distance[edge.to]) {
                result.distance[edge.to] = *result.distance[vertex] + 1;
                result.parent[edge.to] = vertex;
                pending.push_back(edge.to);
            }
        }
    }
    return result;
}

std::vector<int> reconstruct_path(const std::vector<int> &parent, int source, int target) {
    require(source >= 0 && target >= 0 && static_cast<std::size_t>(source) < parent.size() &&
                static_cast<std::size_t>(target) < parent.size(),
            "invalid path endpoint");
    std::vector<int> result;
    for (int current = target; current != -1;) {
        require(current >= 0 && static_cast<std::size_t>(current) < parent.size() &&
                    result.size() <= parent.size(),
                "invalid parent chain");
        result.push_back(current);
        if (current == source) {
            std::reverse(result.begin(), result.end());
            return result;
        }
        current = parent[current];
    }
    return {};
}

std::vector<int> dfs(const Graph &graph, int source) {
    graph.validate_vertex(source);
    std::vector<bool> seen(graph.size());
    std::vector<int> order;
    std::function<void(int)> visit = [&](int vertex) {
        seen[vertex] = true;
        order.push_back(vertex);
        for (const auto &edge : graph.neighbors(vertex)) {
            if (!seen[edge.to]) {
                visit(edge.to);
            }
        }
    };
    visit(source);
    return order;
}
} // namespace adm
