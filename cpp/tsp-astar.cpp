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
#include "geometry.hpp"
#include "tsp.hpp"
#include "tsp-astar.hpp"
#include "tsp-pq.hpp"

namespace adm {
Tour exact_tsp(const std::vector<Point> &points, const std::string &method) {
    const int n = static_cast<int>(points.size());

    require(method == "exact" || method == "best", "unknown exact TSP method");
    if (method == "exact" || method == "best") {
        require(n <= 12, "exact TSP limited to 12 cities");
    }
    std::vector<int> initial(points.size());
    std::iota(initial.begin(), initial.end(), 0);
    Tour best{tour_cost(points, initial), initial};
    // Euclidean distances are nonnegative: a validated zero-cost tour is optimal.
    if (n < 2 || best.cost == 0) {
        return best;
    }
    std::vector<std::vector<double>> distances(n, std::vector<double>(n));
    std::vector<double> minimum(n, std::numeric_limits<double>::infinity());
    for (int i = 0; i < n; ++i) {
        for (int j = 0; j < n; ++j) {
            distances[i][j] = point_distance(points[i], points[j]);
            if (i != j) {
                minimum[i] = std::min(minimum[i], distances[i][j]);
            }
        }
    }
    struct State {
        double cost, bound;
        std::vector<int> path;
        std::uint32_t used;
    };
    auto bound = [&](const State &state) {
        double estimate = state.cost + minimum[state.path.back()];
        for (int vertex = 0; vertex < n; ++vertex) {
            if (!(state.used & (std::uint32_t(1) << vertex))) {
                estimate += minimum[vertex];
            }
        }
        return estimate;
    };
    if (method == "exact" || method == "best") {
        // Each still-unassigned outgoing tour edge is at least that vertex's
        // cheapest edge. This lower bound is admissible even with duplicate cities.
        auto extend = [&](const State &state, int vertex) {
            State next = state;
            next.cost += distances[state.path.back()][vertex];
            next.path.push_back(vertex);
            next.used |= std::uint32_t(1) << vertex;
            next.bound = bound(next);
            return next;
        };
        auto finish = [&](const State &state) {
            double cost = tour_cost(points, state.path);
            if (cost < best.cost) {
                best = {cost, state.path};
            }
        };
        State first{0, 0, {0}, 1};
        first.bound = bound(first);
        if (method == "exact") {
            std::function<void(const State &)> visit = [&](const State &state) {
                if (static_cast<int>(state.path.size()) == n) {
                    finish(state);
                    return;
                }
                // Roundoff slack prevents pruning a slightly underestimated best.
                if (state.bound > best.cost + epsilon * std::max(1.0, best.cost)) {
                    return;
                }
                for (int vertex = 1; vertex < n; ++vertex) {
                    if (!(state.used & (std::uint32_t(1) << vertex))) {
                        visit(extend(state, vertex));
                    }
                }
            };
            visit(first);
        } else {
            auto later = [](const State &a, const State &b) { return a.bound > b.bound; };
            TourQueue<State, decltype(later)> ready(later);
            ready.push(first);
            while (!ready.empty()) {
                State state = ready.top();
                ready.pop();
                if (state.bound > best.cost + epsilon * std::max(1.0, best.cost)) {
                    continue;
                }
                if (static_cast<int>(state.path.size()) == n) {
                    finish(state);
                    continue;
                }
                for (int vertex = 1; vertex < n; ++vertex) {
                    if (!(state.used & (std::uint32_t(1) << vertex))) {
                        ready.push(extend(state, vertex));
                    }
                }
            }
        }
        return best;
    }
    return best;
}
} // namespace adm

#ifdef ADM_DEMO
int main() {
    using namespace adm;
    try {
        std::cout << exact_tsp({{0, 0}, {1, 0}, {1, 1}, {0, 1}}, "best").cost << "\n";
    } catch (const std::exception &error) {
        std::cerr << error.what() << "\n";
        return 1;
    }
}
#endif
