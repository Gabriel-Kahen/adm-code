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

#pragma once

#include "item.hpp"

namespace adm {
struct Edge {
    int from, to;
    Integer weight;
};
struct Arc {
    int to;
    Integer weight;
    std::size_t id;
};
class Graph {
    int vertices_;
    bool directed_;
    std::vector<Edge> edges_;
    std::vector<std::vector<Arc>> adjacency_;
    void rebuild();

  public:
    explicit Graph(int vertices, bool directed = false);
    int size() const {
        return vertices_;
    }
    bool directed() const {
        return directed_;
    }
    const std::vector<Edge> &edges() const {
        return edges_;
    }
    const std::vector<Arc> &neighbors(int vertex) const;
    void validate_vertex(int vertex) const;
    void insert(int from, int to, Integer weight = 1);
    bool erase(int from, int to); // Remove one matching input edge.
};
using Distances = std::vector<std::optional<Integer>>;
using Groups = std::vector<std::vector<int>>;
Groups canonical(Groups groups);
void undirected(const Graph &graph);
void directed(const Graph &graph);
Graph read_graph(std::istream &input, bool directed = false, bool weighted = false);
} // namespace adm
