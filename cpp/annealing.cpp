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
#include "random.hpp"
#include "geometry.hpp"
#include "tsp.hpp"
#include "annealing.hpp"
#include "tsp-astar.hpp"

namespace adm {
Tour traveling_salesperson(const std::vector<Point> &points, const std::string &method,
                           std::uint64_t seed, int iterations) {
    const int n = static_cast<int>(points.size());
    require(iterations >= 0, "negative TSP iteration budget");
    require(method == "exact" || method == "best" || method == "sample" || method == "hill" ||
                method == "anneal",
            "unknown TSP method");
    if (method == "exact" || method == "best") {
        require(n <= 12, "exact TSP limited to 12 cities");
    }
    if (method == "exact" || method == "best") {
        return exact_tsp(points, method);
    }
    std::vector<int> initial(points.size());
    std::iota(initial.begin(), initial.end(), 0);
    Tour best{tour_cost(points, initial), initial};
    // Euclidean distances are nonnegative: a validated zero-cost tour is optimal.
    if (n < 2 || best.cost == 0) {
        return best;
    }
    Random random(seed);
    if (method == "sample") {
        for (int iteration = 0; iteration < iterations; ++iteration) {
            auto candidate = initial;
            random.shuffle(candidate);
            double cost = tour_cost(points, candidate);
            if (cost < best.cost) {
                best = {cost, std::move(candidate)};
            }
        }
        return best;
    }
    auto current = initial;
    random.shuffle(current);
    double current_cost = tour_cost(points, current);
    if (current_cost < best.cost) {
        best = {current_cost, current};
    }
    if (method == "hill") {
        for (int pass = 0; pass < iterations; ++pass) {
            bool improved = false;
            for (int a = 0; a < n && !improved; ++a) {
                for (int b = a + 1; b < n; ++b) {
                    std::swap(current[a], current[b]);
                    double candidate_cost = tour_cost(points, current);
                    if (candidate_cost < current_cost) {
                        current_cost = candidate_cost;
                        improved = true;
                        break;
                    }
                    std::swap(current[a], current[b]);
                }
            }
            if (current_cost < best.cost) {
                best = {current_cost, current};
            }
            if (!improved) {
                break;
            }
        }
    } else {
        double initial_temperature = std::max(1.0, current_cost);
        for (int iteration = 0; iteration < iterations; ++iteration) {
            int a = static_cast<int>(random.integer(0, n - 1)),
                b = static_cast<int>(random.integer(0, n - 1));
            std::swap(current[a], current[b]);
            double candidate_cost = tour_cost(points, current);
            double temperature =
                initial_temperature *
                std::pow(0.001, static_cast<double>(iteration) / std::max(1, iterations));
            if (candidate_cost <= current_cost ||
                random.real(0, 1) < std::exp((current_cost - candidate_cost) / temperature)) {
                current_cost = candidate_cost;
            } else {
                std::swap(current[a], current[b]);
            }
            if (current_cost < best.cost) {
                best = {current_cost, current};
            }
        }
    }
    return best;
}

Tour repeated_traveling_salesperson(const std::vector<Point> &points, const std::string &method,
                                    int runs, std::uint64_t seed, int iterations) {
    require(runs > 0, "TSP restart count must be positive");
    require(method == "sample" || method == "hill" || method == "anneal",
            "restarts require a heuristic TSP method");
    Tour best = traveling_salesperson(points, method, seed, iterations);
    for (int run = 1; run < runs; ++run) {
        Tour candidate = traveling_salesperson(points, method,
                                               seed + static_cast<std::uint64_t>(run), iterations);
        if (candidate.cost < best.cost) {
            best = std::move(candidate);
        }
    }
    return best;
}
} // namespace adm
