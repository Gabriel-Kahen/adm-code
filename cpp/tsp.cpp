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
#include "annealing.hpp"

namespace adm {
double tour_cost(const std::vector<Point> &points, const std::vector<int> &tour) {
    require(tour.size() == points.size(), "tour must include every city");
    std::vector<bool> seen(points.size());
    double cost = 0;
    for (std::size_t i = 0; i < tour.size(); ++i) {
        int vertex = tour[i];
        require(vertex >= 0 && static_cast<std::size_t>(vertex) < points.size() && !seen[vertex],
                "invalid tour permutation");
        seen[vertex] = true;
        int next = tour[(i + 1) % tour.size()];
        require(next >= 0 && static_cast<std::size_t>(next) < points.size(), "invalid tour city");
        cost += point_distance(points[vertex], points[next]);
    }
    require(std::isfinite(cost), "tour cost overflow");
    return cost;
}

double swap_delta(const std::vector<Point> &points, const std::vector<int> &tour, int a, int b) {
    require(a >= 0 && b >= 0 && static_cast<std::size_t>(a) < tour.size() &&
                static_cast<std::size_t>(b) < tour.size(),
            "swap index outside tour");
    auto changed = tour;
    std::swap(changed[a], changed[b]);
    return tour_cost(points, changed) - tour_cost(points, tour);
}
} // namespace adm

#ifdef ADM_DEMO
int main() {
    using namespace adm;
    try {
        std::cout << traveling_salesperson({{0, 0}, {1, 0}, {1, 1}, {0, 1}}, "hill").cost << "\n";
    } catch (const std::exception &error) {
        std::cerr << error.what() << "\n";
        return 1;
    }
}
#endif
