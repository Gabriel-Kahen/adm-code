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

import java.util.Arrays;
import java.util.List;

public final class Superman {
    /** Original independent chord/arc model, not a general shortest-path solver. */
    public static double[] superman(Geometry.Point source, Geometry.Point target,
                                    List<Geometry.Circle> circles) {
        for (int i = 0; i < circles.size(); i++) {
            Geometry.Circle circle = circles.get(i);
            if (Geometry.distance(source, circle.center()) < circle.radius() - Geometry.EPSILON ||
                Geometry.distance(target, circle.center()) < circle.radius() - Geometry.EPSILON) {
                throw new IllegalArgumentException("endpoint inside obstacle");
            }
            for (int j = 0; j < i; j++) {
                Geometry.Circle other = circles.get(j);
                if (Geometry.distance(circle.center(), other.center()) <
                    circle.radius() + other.radius() - Geometry.EPSILON) {
                    throw new IllegalArgumentException(
                        "overlapping obstacles are outside this model");
                }
            }
        }
        double length = Geometry.distance(source, target);
        if (length == 0) {
            return new double[] {0, 0};
        }
        double dx = (target.x() - source.x()) / length;
        double dy = (target.y() - source.y()) / length;
        double through = 0;
        double around = 0;
        for (Geometry.Circle circle : circles) {
            double along =
                (circle.center().x() - source.x()) * dx + (circle.center().y() - source.y()) * dy;
            double perpendicular = Math.abs((circle.center().x() - source.x()) * dy -
                                            (circle.center().y() - source.y()) * dx);
            if (along < 0 || along > length || perpendicular >= circle.radius()) {
                continue;
            }
            double halfChord = Math.sqrt(
                Math.max(0, circle.radius() * circle.radius() - perpendicular * perpendicular));
            if (along - halfChord < -Geometry.EPSILON ||
                along + halfChord > length + Geometry.EPSILON) {
                throw new IllegalArgumentException("partial obstacle crossing outside this model");
            }
            through += 2 * halfChord;
            around += 2 * circle.radius() * Math.acos(Math.min(1, perpendicular / circle.radius()));
        }
        return new double[] {Geometry.finite(through), Geometry.finite(length - through + around)};
    }

    public static void main(String[] args) {
        System.out.println(
            Arrays.toString(superman(new Geometry.Point(-3, 0), new Geometry.Point(3, 0),
                                     List.of(new Geometry.Circle(new Geometry.Point(0, 0), 1)))));
    }
}
