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

namespace adm {
EditResult edit_distance(const std::string &a, const std::string &b) {
    const std::size_t rows = a.size() + 1, columns = b.size() + 1;
    Matrix cost(rows, Integers(columns));
    std::vector<std::string> parent(rows, std::string(columns, 'M'));
    for (std::size_t i = 1; i < rows; ++i) {
        cost[i][0] = static_cast<Integer>(i);
        parent[i][0] = 'D';
    }
    for (std::size_t j = 1; j < columns; ++j) {
        cost[0][j] = static_cast<Integer>(j);
        parent[0][j] = 'I';
    }
    for (std::size_t i = 1; i < rows; ++i) {
        for (std::size_t j = 1; j < columns; ++j) {
            cost[i][j] = cost[i - 1][j - 1] + (a[i - 1] != b[j - 1]);
            parent[i][j] = a[i - 1] == b[j - 1] ? 'M' : 'S';
            if (cost[i][j - 1] + 1 < cost[i][j]) {
                cost[i][j] = cost[i][j - 1] + 1;
                parent[i][j] = 'I';
            }
            if (cost[i - 1][j] + 1 < cost[i][j]) {
                cost[i][j] = cost[i - 1][j] + 1;
                parent[i][j] = 'D';
            }
        }
    }
    std::string operations;
    std::size_t i = a.size(), j = b.size();
    while (i || j) {
        char operation = parent[i][j];
        operations.push_back(operation);
        if (operation != 'I') {
            --i;
        }
        if (operation != 'D') {
            --j;
        }
    }
    std::reverse(operations.begin(), operations.end());
    return {cost.back().back(), operations};
}
Integer brute_edit_distance(const std::string &a, const std::string &b) {
    require(a.size() + b.size() <= 16, "brute-force edit distance limited to combined length 16");
    std::function<Integer(std::size_t, std::size_t)> solve = [&](std::size_t i,
                                                                 std::size_t j) -> Integer {
        if (i == 0) {
            return static_cast<Integer>(j);
        }
        if (j == 0) {
            return static_cast<Integer>(i);
        }
        return std::min({solve(i - 1, j - 1) + (a[i - 1] != b[j - 1]), solve(i - 1, j) + 1,
                         solve(i, j - 1) + 1});
    };
    return solve(a.size(), b.size());
}
std::string longest_common_subsequence(const std::string &a, const std::string &b) {
    Matrix length(a.size() + 1, Integers(b.size() + 1));
    for (std::size_t i = 1; i <= a.size(); ++i) {
        for (std::size_t j = 1; j <= b.size(); ++j) {
            length[i][j] = a[i - 1] == b[j - 1] ? length[i - 1][j - 1] + 1
                                                : std::max(length[i - 1][j], length[i][j - 1]);
        }
    }
    std::string result;
    std::size_t i = a.size(), j = b.size();
    while (i && j) {
        if (a[i - 1] == b[j - 1]) {
            result.push_back(a[--i]);
            --j;
        } else if (length[i - 1][j] >= length[i][j - 1]) {
            --i;
        } else {
            --j;
        }
    }
    std::reverse(result.begin(), result.end());
    return result;
}
Integer substring_edit_distance(const std::string &pattern, const std::string &text) {
    // Every text prefix is free: the first row represents all possible starts.
    Integers previous(text.size() + 1), current(text.size() + 1);
    for (std::size_t i = 1; i <= pattern.size(); ++i) {
        current[0] = static_cast<Integer>(i);
        for (std::size_t j = 1; j <= text.size(); ++j) {
            current[j] = std::min({previous[j - 1] + (pattern[i - 1] != text[j - 1]),
                                   previous[j] + 1, current[j - 1] + 1});
        }
        previous.swap(current);
    }
    return *std::min_element(previous.begin(), previous.end());
}
Partition linear_partition(const Integers &values, int groups) {
    require(groups >= 1 && static_cast<std::size_t>(groups) <= values.size(),
            "partition requires 1 <= groups <= item count");
    Integers prefix(values.size() + 1);
    for (std::size_t i = 0; i < values.size(); ++i) {
        require(values[i] >= 0, "negative partition value");
        prefix[i + 1] = add(prefix[i], values[i]);
    }
    std::vector<std::vector<std::optional<Integer>>> cost(
        groups + 1, std::vector<std::optional<Integer>>(values.size() + 1));
    std::vector<std::vector<std::size_t>> split(groups + 1,
                                                std::vector<std::size_t>(values.size() + 1));
    cost[0][0] = 0;
    for (int count = 1; count <= groups; ++count) {
        for (std::size_t end = static_cast<std::size_t>(count); end <= values.size(); ++end) {
            for (std::size_t begin = static_cast<std::size_t>(count - 1); begin < end; ++begin) {
                if (!cost[count - 1][begin]) {
                    continue;
                }
                Integer candidate = std::max(*cost[count - 1][begin], prefix[end] - prefix[begin]);
                if (!cost[count][end] || candidate < *cost[count][end]) {
                    cost[count][end] = candidate;
                    split[count][end] = begin;
                }
            }
        }
    }
    Matrix parts;
    std::size_t end = values.size();
    for (int count = groups; count > 0; --count) {
        std::size_t begin = split[count][end];
        parts.emplace_back(values.begin() + static_cast<std::ptrdiff_t>(begin),
                           values.begin() + static_cast<std::ptrdiff_t>(end));
        end = begin;
    }
    std::reverse(parts.begin(), parts.end());
    return {*cost[groups][values.size()], parts};
}
std::optional<std::vector<int>> subset_sum(const Integers &values, Integer target) {
    require(target >= 0, "negative subset-sum target");
    // Pseudopolynomial storage; explicitly reject requests beyond practical memory.
    require(target <= 10000000, "subset-sum target exceeds memory budget 10000000");
    std::vector<int> chosen(static_cast<std::size_t>(target) + 1, -1);
    chosen[0] = -2;
    for (std::size_t i = 0; i < values.size(); ++i) {
        require(values[i] >= 0, "negative subset-sum value");
        if (values[i] == 0 || values[i] > target) {
            continue;
        }
        for (Integer sum = target; sum >= values[i]; --sum) {
            if (chosen[sum] == -1 && chosen[sum - values[i]] != -1) {
                chosen[sum] = static_cast<int>(i);
            }
        }
    }
    if (chosen[target] == -1) {
        return std::nullopt;
    }
    std::vector<int> indices;
    for (Integer sum = target; sum > 0;) {
        int index = chosen[sum];
        indices.push_back(index);
        sum -= values[index];
    }
    std::sort(indices.begin(), indices.end());
    return indices;
}
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
