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
Integer maximum_flow(const Graph &graph, int source, int sink) {
    directed(graph);
    graph.validate_vertex(source);
    graph.validate_vertex(sink);
    require(source != sink, "flow endpoints must differ");
    Matrix residual(graph.size(), Integers(graph.size()));
    for (const auto &edge : graph.edges()) {
        require(edge.weight >= 0, "negative flow capacity");
        residual[edge.from][edge.to] = add(residual[edge.from][edge.to], edge.weight);
    }
    Integer total = 0;
    while (true) {
        std::vector<int> parent(graph.size(), -1);
        parent[source] = source;
        std::deque<int> pending{source};
        while (!pending.empty() && parent[sink] == -1) {
            int vertex = pending.front();
            pending.pop_front();
            for (int next = 0; next < graph.size(); ++next) {
                if (parent[next] == -1 && residual[vertex][next] > 0) {
                    parent[next] = vertex;
                    pending.push_back(next);
                }
            }
        }
        if (parent[sink] == -1) {
            return total;
        }
        Integer amount = std::numeric_limits<Integer>::max();
        for (int vertex = sink; vertex != source; vertex = parent[vertex]) {
            amount = std::min(amount, residual[parent[vertex]][vertex]);
        }
        for (int vertex = sink; vertex != source; vertex = parent[vertex]) {
            residual[parent[vertex]][vertex] -= amount;
            residual[vertex][parent[vertex]] = add(residual[vertex][parent[vertex]], amount);
        }
        total = add(total, amount);
    }
}
} // namespace adm

#ifdef ADM_DEMO
int main() {
    using namespace adm;
    try {
        int source, sink;
        require(bool(std::cin >> source >> sink), "missing source and sink");
        auto graph = read_weighted_graph(std::cin, true);
        std::cout << maximum_flow(graph, source - 1, sink - 1) << "\n";
    } catch (const std::exception &error) {
        std::cerr << error.what() << "\n";
        return 1;
    }
}
#endif
