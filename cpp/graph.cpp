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
Graph::Graph(int vertices, bool directed) : vertices_(vertices), directed_(directed) {
    require(vertices >= 0, "negative vertex count");
    adjacency_.resize(vertices);
}

void Graph::validate_vertex(int vertex) const {
    require(vertex >= 0 && vertex < vertices_, "vertex outside graph");
}

const std::vector<Arc> &Graph::neighbors(int vertex) const {
    validate_vertex(vertex);
    return adjacency_[vertex];
}

void Graph::insert(int from, int to, Integer weight) {
    validate_vertex(from);
    validate_vertex(to);
    std::size_t id = edges_.size();
    edges_.push_back({from, to, weight});
    adjacency_[from].push_back({to, weight, id});
    if (!directed_) {
        adjacency_[to].push_back({from, weight, id});
    }
}

void Graph::rebuild() {
    adjacency_.assign(vertices_, {});
    auto old = std::move(edges_);
    edges_.clear();
    for (const auto &edge : old) {
        insert(edge.from, edge.to, edge.weight);
    }
}

bool Graph::erase(int from, int to) {
    validate_vertex(from);
    validate_vertex(to);
    auto match = std::find_if(edges_.begin(), edges_.end(), [&](const Edge &edge) {
        return (edge.from == from && edge.to == to) ||
               (!directed_ && edge.from == to && edge.to == from);
    });
    if (match == edges_.end()) {
        return false;
    }
    edges_.erase(match);
    rebuild();
    return true;
}

Groups canonical(Groups groups) {
    for (auto &group : groups) {
        std::sort(group.begin(), group.end());
    }
    std::sort(groups.begin(), groups.end());
    return groups;
}

void undirected(const Graph &graph) {
    require(!graph.directed(), "operation requires undirected graph");
}

void directed(const Graph &graph) {
    require(graph.directed(), "operation requires directed graph");
}

Graph read_graph(std::istream &input, bool is_directed, bool weighted) {
    int size, count;
    require(bool(input >> size >> count) && count >= 0, "expected vertex and edge counts");
    Graph graph(size, is_directed);
    for (int i = 0; i < count; ++i) {
        int source, target;
        Integer weight = 1;
        require(bool(input >> source >> target), "missing graph edge");
        if (weighted) {
            require(bool(input >> weight), "missing edge weight");
        }
        graph.insert(source - 1, target - 1, weight);
    }
    return graph;
}
} // namespace adm
