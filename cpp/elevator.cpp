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

namespace adm {
struct Elevator {
    Integer cost;
    std::vector<int> stops;
};

Elevator elevator_stops(const std::vector<int> &destinations, int budget, int max_floor) {
    require(budget >= 0 && max_floor >= 0, "negative elevator dimension");
    for (int destination : destinations) {
        require(destination >= 0 && destination <= max_floor, "destination outside building");
    }
    budget = std::min(budget, max_floor);
    auto after = [&](int floor) {
        Integer cost = 0;
        for (int destination : destinations) {
            if (destination > floor) {
                cost = add(cost, destination - floor);
            }
        }
        return cost;
    };
    auto between = [&](int low, int high) {
        Integer cost = 0;
        for (int destination : destinations) {
            if (destination > low && destination <= high) {
                cost = add(cost, std::min(destination - low, high - destination));
            }
        }
        return cost;
    };
    std::vector<std::vector<std::optional<Integer>>> cost(
        budget + 1, std::vector<std::optional<Integer>>(max_floor + 1));
    std::vector<std::vector<int>> parent(budget + 1, std::vector<int>(max_floor + 1, -1));
    cost[0][0] = after(0);
    Elevator result{*cost[0][0], {}};
    int best_count = 0, best_floor = 0;
    for (int count = 1; count <= budget; ++count) {
        for (int high = 1; high <= max_floor; ++high) {
            for (int low = 0; low < high; ++low) {
                if (!cost[count - 1][low]) {
                    continue;
                }
                Integer candidate =
                    add(add(*cost[count - 1][low] - after(low), between(low, high)), after(high));
                if (!cost[count][high] || candidate < *cost[count][high]) {
                    cost[count][high] = candidate;
                    parent[count][high] = low;
                }
            }
            if (cost[count][high] && *cost[count][high] < result.cost) {
                result.cost = *cost[count][high];
                best_count = count;
                best_floor = high;
            }
        }
    }
    for (int count = best_count, floor = best_floor; count > 0; --count) {
        result.stops.push_back(floor);
        floor = parent[count][floor];
    }
    std::reverse(result.stops.begin(), result.stops.end());
    return result;
}
} // namespace adm

#ifdef ADM_DEMO
int main() {
    using namespace adm;
    try {
        std::cout << elevator_stops({1, 3, 6}, 2, 6).cost << "\n";
    } catch (const std::exception &error) {
        std::cerr << error.what() << "\n";
        return 1;
    }
}
#endif
