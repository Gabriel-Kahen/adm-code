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

namespace adm {
bool backtrack(std::vector<int> &prefix,
               const std::function<bool(const std::vector<int> &)> &complete,
               const Candidates &candidates, const std::function<void(int)> &make,
               const std::function<void(int)> &undo,
               const std::function<bool(const std::vector<int> &)> &visit) {
    if (complete(prefix)) {
        return visit(prefix);
    }
    for (int candidate : candidates(prefix)) {
        make(candidate);
        prefix.push_back(candidate);
        bool stop;
        try {
            stop = backtrack(prefix, complete, candidates, make, undo, visit);
        } catch (...) {
            prefix.pop_back();
            undo(candidate);
            throw;
        }
        prefix.pop_back();
        undo(candidate);
        if (stop) {
            return true;
        }
    }
    return false;
}
Groups permutations(int n) {
    require(n >= 0 && n <= 10, "permutation enumeration requires 0 <= n <= 10");
    Groups result;
    std::vector<int> prefix;
    std::vector<bool> used(n);
    backtrack(
        prefix, [n](const auto &path) { return static_cast<int>(path.size()) == n; },
        [&](const auto &) {
            std::vector<int> choices;
            for (int i = 0; i < n; ++i) {
                if (!used[i]) {
                    choices.push_back(i);
                }
            }
            return choices;
        },
        [&](int value) { used[value] = true; }, [&](int value) { used[value] = false; },
        [&](const auto &path) {
            result.push_back(path);
            return false;
        });
    return result;
}
Groups subsets(int n) {
    require(n >= 0 && n <= 20, "subset enumeration requires 0 <= n <= 20");
    Groups result{{}};
    for (int value = 0; value < n; ++value) {
        auto size = result.size();
        for (std::size_t i = 0; i < size; ++i) {
            auto next = result[i];
            next.push_back(value);
            result.push_back(std::move(next));
        }
    }
    std::sort(result.begin(), result.end());
    return result;
}
Integer queens(int n) {
    require(n >= 0 && n <= 15, "queens count requires 0 <= n <= 15");
    using Mask = std::uint64_t;
    Mask all = (Mask(1) << n) - 1;
    std::function<Integer(Mask, Mask, Mask)> visit = [&](Mask columns, Mask left,
                                                         Mask right) -> Integer {
        if (columns == all) {
            return 1;
        }
        Mask choices = all & ~(columns | left | right);
        Integer count = 0;
        while (choices) {
            Mask next = choices & (~choices + 1);
            choices -= next;
            count = add(count, visit(columns | next, (left | next) << 1, (right | next) >> 1));
        }
        return count;
    };
    return visit(0, 0, 0);
}
std::optional<std::string> sudoku(const std::string &input, bool smart, bool fast) {
    require(input.size() == 81 && std::all_of(input.begin(), input.end(),
                                              [](char c) { return c >= '0' && c <= '9'; }),
            "Sudoku requires 81 decimal digits");
    std::string board = input;
    std::array<int, 9> rows{}, columns{}, boxes{};
    auto box = [](int cell) { return (cell / 27) * 3 + (cell % 9) / 3; };
    for (int cell = 0; cell < 81; ++cell) {
        int digit = board[cell] - '0';
        if (!digit) {
            continue;
        }
        int bit = 1 << digit, row = cell / 9, column = cell % 9, block = box(cell);
        require(((rows[row] | columns[column] | boxes[block]) & bit) == 0,
                "contradictory Sudoku givens");
        rows[row] |= bit;
        columns[column] |= bit;
        boxes[block] |= bit;
    }
    auto candidate_mask = [&](int cell) {
        if (fast) {
            return 0x3fe & ~(rows[cell / 9] | columns[cell % 9] | boxes[box(cell)]);
        }
        int blocked = 0;
        for (int other = 0; other < 81; ++other) {
            if (other / 9 == cell / 9 || other % 9 == cell % 9 || box(other) == box(cell)) {
                blocked |= 1 << (board[other] - '0');
            }
        }
        return 0x3fe & ~blocked;
    };
    std::function<bool()> solve = [&]() {
        int best_cell = -1, best_mask = 0, best_count = 10;
        for (int cell = 0; cell < 81; ++cell) {
            if (board[cell] != '0') {
                continue;
            }
            int mask = candidate_mask(cell);
            int count = 0;
            for (int bits = mask; bits; bits &= bits - 1) {
                ++count;
            }
            if (count < best_count) {
                best_count = count;
                best_cell = cell;
                best_mask = mask;
            }
            if (!smart) {
                break;
            }
        }
        if (best_cell == -1) {
            return true;
        }
        if (best_count == 0) {
            return false;
        }
        int row = best_cell / 9, column = best_cell % 9, block = box(best_cell);
        for (int digit = 1; digit <= 9; ++digit) {
            int bit = 1 << digit;
            if (!(best_mask & bit)) {
                continue;
            }
            board[best_cell] = static_cast<char>('0' + digit);
            rows[row] |= bit;
            columns[column] |= bit;
            boxes[block] |= bit;
            if (solve()) {
                return true;
            }
            rows[row] ^= bit;
            columns[column] ^= bit;
            boxes[block] ^= bit;
            board[best_cell] = '0';
        }
        return false;
    };
    if (solve()) {
        return board;
    }
    return std::nullopt;
}
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
            std::priority_queue<State, std::vector<State>, decltype(later)> ready(later);
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
                        require(ready.size() < 1000000, "TSP best-first frontier exhausted");
                        ready.push(extend(state, vertex));
                    }
                }
            }
        }
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
