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
Groups tarjan(const Graph &graph) {
    directed(graph);
    Groups groups;

    std::vector<int> entered(graph.size(), -1), low(graph.size()), stack;
    std::vector<bool> active(graph.size());
    int clock = 0;
    std::function<void(int)> visit = [&](int vertex) {
        entered[vertex] = low[vertex] = clock++;
        stack.push_back(vertex);
        active[vertex] = true;
        for (const auto &edge : graph.neighbors(vertex)) {
            if (entered[edge.to] == -1) {
                visit(edge.to);
                low[vertex] = std::min(low[vertex], low[edge.to]);
            } else if (active[edge.to]) {
                low[vertex] = std::min(low[vertex], entered[edge.to]);
            }
        }
        if (low[vertex] == entered[vertex]) {
            std::vector<int> component;
            while (true) {
                int member = stack.back();
                stack.pop_back();
                active[member] = false;
                component.push_back(member);
                if (member == vertex) {
                    break;
                }
            }
            groups.push_back(std::move(component));
        }
    };
    for (int vertex = 0; vertex < graph.size(); ++vertex) {
        if (entered[vertex] == -1) {
            visit(vertex);
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
        for (auto row : tarjan(graph)) {
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
