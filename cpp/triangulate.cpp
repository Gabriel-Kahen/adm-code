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

namespace adm {
std::vector<std::array<int, 3>> triangulate(const std::vector<Point> &polygon) {
    simple_polygon(polygon);
    std::vector<int> remaining(polygon.size());
    std::iota(remaining.begin(), remaining.end(), 0);
    if (signed_polygon_area(polygon) < 0) {
        std::reverse(remaining.begin(), remaining.end());
    }
    std::vector<std::array<int, 3>> result;
    while (remaining.size() > 3) {
        bool found = false;
        for (std::size_t i = 0; i < remaining.size(); ++i) {
            int a = remaining[(i + remaining.size() - 1) % remaining.size()], b = remaining[i],
                c = remaining[(i + 1) % remaining.size()];
            if (orientation(polygon[a], polygon[b], polygon[c]) <= 0) {
                continue;
            }
            bool blocked = false;
            for (int vertex : remaining) {
                if (vertex == a || vertex == b || vertex == c) {
                    continue;
                }
                if (orientation(polygon[a], polygon[b], polygon[vertex]) >= 0 &&
                    orientation(polygon[b], polygon[c], polygon[vertex]) >= 0 &&
                    orientation(polygon[c], polygon[a], polygon[vertex]) >= 0) {
                    blocked = true;
                    break;
                }
            }
            if (!blocked) {
                result.push_back({a, b, c});
                remaining.erase(remaining.begin() + static_cast<std::ptrdiff_t>(i));
                found = true;
                break;
            }
        }
        require(found, "polygon has no nondegenerate ear at tolerance");
    }
    require(triangle_area(polygon[remaining[0]], polygon[remaining[1]], polygon[remaining[2]]) >
                epsilon,
            "degenerate final triangle");
    result.push_back({remaining[0], remaining[1], remaining[2]});
    return result;
}

double minimum_weight_triangulation(const std::vector<Point> &polygon) {
    simple_polygon(polygon);
    const std::size_t n = polygon.size();
    int direction = orientation(polygon[0], polygon[1], polygon[2]);
    require(direction != 0, "minimum-weight triangulation requires strict convexity");
    for (std::size_t i = 0; i < n; ++i) {
        require(orientation(polygon[i], polygon[(i + 1) % n], polygon[(i + 2) % n]) == direction,
                "minimum-weight triangulation requires strict convexity");
    }
    std::vector<std::vector<double>> cost(n, std::vector<double>(n));
    for (std::size_t gap = 2; gap < n; ++gap) {
        for (std::size_t begin = 0; begin + gap < n; ++begin) {
            std::size_t end = begin + gap;
            cost[begin][end] = std::numeric_limits<double>::infinity();
            for (std::size_t middle = begin + 1; middle < end; ++middle) {
                double perimeter = point_distance(polygon[begin], polygon[middle]) +
                                   point_distance(polygon[middle], polygon[end]) +
                                   point_distance(polygon[end], polygon[begin]);
                cost[begin][end] =
                    std::min(cost[begin][end], cost[begin][middle] + cost[middle][end] + perimeter);
            }
        }
    }
    require(std::isfinite(cost[0][n - 1]), "triangulation cost overflow");
    return cost[0][n - 1];
}
} // namespace adm

#ifdef ADM_DEMO
int main() {
    using namespace adm;
    try {
        for (auto triangle : triangulate({{0, 0}, {1, 0}, {1, 1}, {0, 1}})) {
            std::cout << triangle[0] << " " << triangle[1] << " " << triangle[2] << "\n";
        }
    } catch (const std::exception &error) {
        std::cerr << error.what() << "\n";
        return 1;
    }
}
#endif
