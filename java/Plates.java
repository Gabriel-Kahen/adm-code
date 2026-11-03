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

public final class Plates {
    static void packingDomain(double width, double height, double radius) {
        Geometry.finite(width);
        Geometry.finite(height);
        Geometry.finite(radius);
        if (width <= 0 || height <= 0 || radius <= 0 || !Double.isFinite(2 * radius)) {
            throw new IllegalArgumentException(
                "positive finite box dimensions and radius required");
        }
    }

    static long count(double value) {
        if (!Double.isFinite(value) || value < 0 || value >= 0x1.0p63) {
            throw new ArithmeticException("packing count overflows long");
        }
        return (long)Math.floor(value);
    }

    public static long denseLayers(double width, double height, double radius) {
        packingDomain(width, height, radius);
        if (width < 2 * radius || height < 2 * radius) {
            return 0;
        }
        return Math.addExact(1, count((height - 2 * radius) / (Math.sqrt(3) * radius)));
    }

    public static long platesPerRow(long row, double width, double radius) {
        packingDomain(width, width, radius);
        if (row < 0) {
            throw new IllegalArgumentException("negative row");
        }
        if (width < 2 * radius) {
            return 0;
        }
        return count((width - (row % 2 == 0 ? 0 : radius)) / (2 * radius));
    }

    public static long densePlates(double width, double height, double radius) {
        long layers = denseLayers(width, height, radius);
        long even = Math.multiplyExact(layers / 2 + layers % 2, platesPerRow(0, width, radius));
        long odd = Math.multiplyExact(layers / 2, platesPerRow(1, width, radius));
        return Math.addExact(even, odd);
    }

    public static long gridPlates(double width, double height, double radius) {
        packingDomain(width, height, radius);
        return Math.multiplyExact(count(width / (2 * radius)), count(height / (2 * radius)));
    }

    public static long[] packing(double width, double height, double radius) {
        return new long[] {
            gridPlates(width, height, radius),
            Math.max(densePlates(width, height, radius), densePlates(height, width, radius))};
    }

    public static Geometry.Point hexToGeo(double xh, double yh, double radius) {
        packingDomain(1, 1, radius);
        return new Geometry.Point(radius * xh + 2 * radius * yh, Math.sqrt(3) * radius * xh);
    }

    public static Geometry.Point geoToHex(Geometry.Point point, double radius) {
        packingDomain(1, 1, radius);
        double xh = point.y() / (Math.sqrt(3) * radius);
        return new Geometry.Point(xh, (point.x() - radius * xh) / (2 * radius));
    }

    public static int[] arrayToHex(int row, int column) {
        return new int[] {row, Math.subtractExact(column, Math.floorDiv(row, 2))};
    }

    public static int[] hexToArray(int row, int diagonal) {
        return new int[] {row, Math.addExact(diagonal, Math.floorDiv(row, 2))};
    }

    public static long platesOnTop(int row, int diagonal, double width, double height,
                                   double radius) {
        long layers = denseLayers(width, height, radius);
        int[] array = hexToArray(row, diagonal);
        if (row < 0 || row >= layers || array[1] < 0 ||
            array[1] >= platesPerRow(row, width, radius)) {
            throw new IllegalArgumentException("plate outside packing");
        }
        long total = 0;
        for (long current = row + 1L; current < layers; current++) {
            long left = Math.max(0, diagonal - (current - row) + Math.floorDiv(current, 2));
            long right = Math.min(platesPerRow(current, width, radius) - 1,
                                  diagonal + Math.floorDiv(current, 2));
            total = Math.addExact(total, Math.max(0, right - left + 1));
        }
        return total;
    }

    public static void main(String[] args) {
        java.util.Scanner in = new java.util.Scanner(System.in);
        double w = in.hasNextDouble() ? in.nextDouble() : 4;
        double h = in.hasNextDouble() ? in.nextDouble() : 4;
        double r = in.hasNextDouble() ? in.nextDouble() : 1;
        System.out.println(Arrays.toString(packing(w, h, r)));
    }
}
