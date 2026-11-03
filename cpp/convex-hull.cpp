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
std::vector<Point> convex_hull(std::vector<Point> points) {
    for (Point point : points) {
        finite_point(point);
    }
    std::sort(points.begin(), points.end(),
              [](Point a, Point b) { return std::tie(a.x, a.y) < std::tie(b.x, b.y); });
    points.erase(std::unique(points.begin(), points.end(),
                             [](Point a, Point b) { return a.x == b.x && a.y == b.y; }),
                 points.end());
    if (points.size() <= 2) {
        return points;
    }
    std::vector<Point> lower, upper;
    for (Point point : points) {
        while (lower.size() >= 2 &&
               orientation(lower[lower.size() - 2], lower.back(), point) <= 0) {
            lower.pop_back();
        }
        lower.push_back(point);
    }
    for (auto it = points.rbegin(); it != points.rend(); ++it) {
        while (upper.size() >= 2 && orientation(upper[upper.size() - 2], upper.back(), *it) <= 0) {
            upper.pop_back();
        }
        upper.push_back(*it);
    }
    lower.pop_back();
    upper.pop_back();
    lower.insert(lower.end(), upper.begin(), upper.end());
    return lower;
}
} // namespace adm

#ifdef ADM_DEMO
int main() {
    using namespace adm;
    try {
        std::vector<Point> points;
        int n;
        if (std::cin >> n) {
            require(n >= 0, "negative point count");
            for (int i = 0; i < n; ++i) {
                Point p;
                require(bool(std::cin >> p.x >> p.y), "missing point");
                points.push_back(p);
            }
        } else {
            points = {{0, 0}, {1, 0}, {1, 1}, {0, 1}};
        }
        for (auto p : convex_hull(points)) {
            std::cout << p.x << " " << p.y << "\n";
        }
    } catch (const std::exception &error) {
        std::cerr << error.what() << "\n";
        return 1;
    }
}
#endif
