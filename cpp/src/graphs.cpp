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

#include "adm.hpp"

#include <numeric>
#include <queue>
#include <set>

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
namespace {
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
} // namespace
Groups connected_components(const Graph &graph) {
    undirected(graph);
    Groups groups;
    std::vector<bool> seen(graph.size());
    std::function<void(int, std::vector<int> &)> visit = [&](int vertex, std::vector<int> &group) {
        seen[vertex] = true;
        group.push_back(vertex);
        for (const auto &edge : graph.neighbors(vertex)) {
            if (!seen[edge.to]) {
                visit(edge.to, group);
            }
        }
    };
    for (int root = 0; root < graph.size(); ++root) {
        if (!seen[root]) {
            groups.emplace_back();
            visit(root, groups.back());
        }
    }
    return canonical(std::move(groups));
}
std::optional<std::vector<int>> bipartite_coloring(const Graph &graph) {
    undirected(graph);
    std::vector<int> color(graph.size(), -1);
    for (int root = 0; root < graph.size(); ++root) {
        if (color[root] != -1) {
            continue;
        }
        std::deque<int> pending{root};
        color[root] = 0;
        while (!pending.empty()) {
            int vertex = pending.front();
            pending.pop_front();
            for (const auto &edge : graph.neighbors(vertex)) {
                if (color[edge.to] == color[vertex]) {
                    return std::nullopt;
                }
                if (color[edge.to] == -1) {
                    color[edge.to] = 1 - color[vertex];
                    pending.push_back(edge.to);
                }
            }
        }
    }
    return color;
}
bool has_cycle(const Graph &graph) {
    undirected(graph);
    DisjointSet sets(graph.size());
    for (const auto &edge : graph.edges()) {
        if (!sets.unite(edge.from, edge.to)) {
            return true;
        }
    }
    return false;
}
std::vector<int> articulation_points(const Graph &graph) {
    undirected(graph);
    std::vector<int> entered(graph.size(), -1), low(graph.size());
    std::vector<bool> cut(graph.size());
    int clock = 0;
    std::function<void(int, std::size_t)> visit = [&](int vertex, std::size_t parent_edge) {
        entered[vertex] = low[vertex] = clock++;
        int children = 0;
        for (const auto &edge : graph.neighbors(vertex)) {
            if (edge.id == parent_edge) {
                continue;
            }
            if (entered[edge.to] == -1) {
                ++children;
                visit(edge.to, edge.id);
                low[vertex] = std::min(low[vertex], low[edge.to]);
                if (parent_edge != std::numeric_limits<std::size_t>::max() &&
                    low[edge.to] >= entered[vertex]) {
                    cut[vertex] = true;
                }
            } else {
                low[vertex] = std::min(low[vertex], entered[edge.to]);
            }
        }
        if (parent_edge == std::numeric_limits<std::size_t>::max() && children > 1) {
            cut[vertex] = true;
        }
    };
    for (int vertex = 0; vertex < graph.size(); ++vertex) {
        if (entered[vertex] == -1) {
            visit(vertex, std::numeric_limits<std::size_t>::max());
        }
    }
    std::vector<int> result;
    for (int vertex = 0; vertex < graph.size(); ++vertex) {
        if (cut[vertex]) {
            result.push_back(vertex);
        }
    }
    return result;
}
Groups strongly_connected(const Graph &graph, const std::string &method) {
    directed(graph);
    Groups groups;
    if (method == "tarjan") {
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
    } else {
        require(method == "kosaraju", "unknown SCC method");
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
        std::function<void(int, std::vector<int> &)> second = [&](int vertex,
                                                                  std::vector<int> &group) {
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
    }
    return canonical(std::move(groups));
}
std::vector<int> topological_order(const Graph &graph, const std::string &method) {
    directed(graph);
    std::vector<int> result;
    if (method == "kahn") {
        std::vector<int> indegree(graph.size());
        for (const auto &edge : graph.edges()) {
            ++indegree[edge.to];
        }
        std::deque<int> ready;
        for (int vertex = 0; vertex < graph.size(); ++vertex) {
            if (indegree[vertex] == 0) {
                ready.push_back(vertex);
            }
        }
        while (!ready.empty()) {
            int vertex = ready.front();
            ready.pop_front();
            result.push_back(vertex);
            for (const auto &edge : graph.neighbors(vertex)) {
                if (--indegree[edge.to] == 0) {
                    ready.push_back(edge.to);
                }
            }
        }
        require(static_cast<int>(result.size()) == graph.size(),
                "topological order requires acyclic graph");
    } else {
        require(method == "dfs", "unknown topological method");
        std::vector<int> color(graph.size());
        std::function<void(int)> visit = [&](int vertex) {
            require(color[vertex] != 1, "topological order requires acyclic graph");
            if (color[vertex] == 2) {
                return;
            }
            color[vertex] = 1;
            for (const auto &edge : graph.neighbors(vertex)) {
                visit(edge.to);
            }
            color[vertex] = 2;
            result.push_back(vertex);
        };
        for (int vertex = 0; vertex < graph.size(); ++vertex) {
            if (!color[vertex]) {
                visit(vertex);
            }
        }
        std::reverse(result.begin(), result.end());
    }
    return result;
}
SpanningForest minimum_spanning_forest(const Graph &graph, const std::string &method) {
    undirected(graph);
    SpanningForest result;
    if (method == "kruskal") {
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
    } else {
        require(method == "prim", "unknown spanning forest method");
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
    }
    return result;
}
Distances dijkstra(const Graph &graph, int source) {
    graph.validate_vertex(source);
    for (const auto &edge : graph.edges()) {
        require(edge.weight >= 0, "Dijkstra requires nonnegative edges");
    }
    Distances distance(graph.size());
    distance[source] = 0;
    using Choice = std::pair<Integer, int>;
    std::priority_queue<Choice, std::vector<Choice>, std::greater<Choice>> ready;
    ready.emplace(0, source);
    while (!ready.empty()) {
        auto [cost, vertex] = ready.top();
        ready.pop();
        if (cost != distance[vertex]) {
            continue;
        }
        for (const auto &edge : graph.neighbors(vertex)) {
            Integer candidate = add(cost, edge.weight);
            if (!distance[edge.to] || candidate < *distance[edge.to]) {
                distance[edge.to] = candidate;
                ready.emplace(candidate, edge.to);
            }
        }
    }
    return distance;
}
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
