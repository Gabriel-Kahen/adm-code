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
std::pair<double, double> superman(Point start, Point end, const std::vector<Circle> &circles) {
    finite_point(start);
    finite_point(end);
    for (std::size_t i = 0; i < circles.size(); ++i) {
        const auto &circle = circles[i];
        finite_point(circle.center);
        require(std::isfinite(circle.radius) && circle.radius > 0, "invalid obstacle radius");
        require(point_distance(start, circle.center) >= circle.radius - epsilon &&
                    point_distance(end, circle.center) >= circle.radius - epsilon,
                "endpoint inside obstacle");
        for (std::size_t j = 0; j < i; ++j) {
            require(point_distance(circle.center, circles[j].center) >=
                        circle.radius + circles[j].radius - epsilon,
                    "overlapping circles outside model");
        }
    }
    double direct = point_distance(start, end), through = 0, around = 0;
    if (direct == 0) {
        return {0, 0};
    }
    Line path = points_to_line(start, end);
    for (const auto &circle : circles) {
        Point closest = project(circle.center, path);
        double away = point_distance(circle.center, closest);
        if (away < circle.radius && in_box(closest, start, end)) {
            through += 2 * std::sqrt(std::max(0.0, circle.radius * circle.radius - away * away));
            around += 2 * circle.radius * std::acos(std::clamp(away / circle.radius, -1.0, 1.0));
        }
    }
    return {through, direct - through + around};
}
} // namespace adm

#ifdef ADM_DEMO
int main() {
    using namespace adm;
    try {
        auto result = superman({-3, 0}, {3, 0}, {{{0, 0}, 1}});
        std::cout << result.first << " " << result.second << "\n";
    } catch (const std::exception &error) {
        std::cerr << error.what() << "\n";
        return 1;
    }
}
#endif
