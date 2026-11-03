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

#pragma once

#include "item.hpp"

namespace adm {
constexpr double epsilon = 1e-9;
struct Point {
    double x, y;
};
struct Line {
    double a, b, c;
};
struct Circle {
    Point center;
    double radius;
};
double cross(Point a, Point b, Point c);
int orientation(Point a, Point b, Point c, double tolerance = epsilon);
double triangle_area(Point a, Point b, Point c);
double point_distance(Point a, Point b);
Line points_to_line(Point a, Point b);
Line point_slope_line(Point p, double slope);
bool parallel(Line a, Line b, double tolerance = epsilon);
bool same_line(Line a, Line b, double tolerance = epsilon);
std::optional<Point> intersection(Line a, Line b, double tolerance = epsilon);
Point project(Point point, Line line);
bool in_box(Point p, Point a, Point b, double tolerance = epsilon);
bool segments_intersect(Point a, Point b, Point c, Point d, double tolerance = epsilon);
double polygon_area(const std::vector<Point> &points);
void finite_point(Point point);
void packing_domain(double width, double height, double radius);
void simple_polygon(const std::vector<Point> &polygon);
double signed_polygon_area(const std::vector<Point> &polygon);
} // namespace adm
