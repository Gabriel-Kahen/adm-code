/*    plates.c

    Compute the number of circles in two different disk packings.
    Assuming we have an $w \times l$ box, how many unit disks
    can we pack in there assumming we have w disks on the bottom?
*/

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

public class Plates {

    /*
        how many triangular-lattice layers of radius r balls fit in height h?
    */
    public static int dense_layers(double w, double h, double r) {
        double gap = 0; /* distance between layers */
        if ((((2 * r) > h) || ((2 * r) > w))) {
            return 0;
        }
        gap = ((2.0 * r) * (Math.sqrt(3) / 2.0));
        return (int)((1 + Math.floor(((h - (2.0 * r)) / gap))));
    }

    public static int plates_per_row(int row, double w, double r) {
        int plates_per_full_row = 0; /* number of plates in full/even row */
        if ((w < (2 * r))) {
            return 0;
        }
        plates_per_full_row = (int)(Math.floor((w / (2 * r))));
        if (((row % 2) == 0)) {
            return plates_per_full_row;
        }
        if ((((w / (2 * r)) - plates_per_full_row) >= 0.5)) { /* odd row full, too */
            return plates_per_full_row;
        } else {
            return (plates_per_full_row - 1);
        }
    }

    /*
        How many radius r plates fit in a hexagonal-lattice packed w*h box?
    */
    public static int dense_plates(double w, double l, double r) {
        int layers = 0; /* number of layers of balls */
        layers = dense_layers(w, l, r);
        return (int)(((Math.ceil((layers / 2.0)) * plates_per_row(0, w, r)) + (Math.floor((layers / 2.0)) * plates_per_row(1, w, r))));
    }

    public static int grid_plates(double w, double h, double r) {
        int layers = 0; /* number of layers of balls */
        layers = (int)(Math.floor((h / (2 * r))));
        return (layers * plates_per_row(0, w, r));
    }

    /*  Hexagonal coordinates start with the center of disk (0,0) at
        geometric point (0,0).  The hexagonal coordinate $(xh,yh)$
        refers to the center of the disk on the horizontal row xh
        and positive-slope diagonal yh.   The geometric coordinate of
        such a point is a function of the radius of the disk $r$.
    */
    public static void hex_to_geo(int xh, int yh, double r, double[] xg, double[] yg) {
        yg[0] = (((2.0 * r) * xh) * (Math.sqrt(3) / 2.0));
        xg[0] = ((((2.0 * r) * xh) * (1.0 / 2.0)) + ((2.0 * r) * yh));
    }

    public static void geo_to_hex(double xg, double yg, double r, double[] xh, double[] yh) {
        xh[0] = (((2.0 / Math.sqrt(3)) * yg) / (2.0 * r));
        yh[0] = ((xg - (((2.0 * r) * xh[0]) * (1.0 / 2.0))) / (2.0 * r));
    }

    /*  Under the hexagonal coordinate system, the set of hexagons defined
        by coordinates (hx,hy), where $0 <= hx <= xmax$ and $0 <= hx <= ymax$
        forms a diamond-shaped patch, not a conventional axis-oriented
        rectangle.  To solve this problem, we define array coordinates
        so that (ax,ay) refers to the position in an axis-oriented
        rectangle with (0,0) as the lower righthand point in the matrix.
    */
    public static void array_to_hex(int xa, int ya, int[] xh, int[] yh) {
        xh[0] = xa;
        yh[0] = (int)(((ya - xa) + Math.ceil((xa / 2.0))));
    }

    public static void hex_to_array(int xh, int yh, int[] xa, int[] ya) {
        xa[0] = xh;
        ya[0] = (int)(((yh + xh) - Math.ceil((xh / 2.0))));
    }

    public static int plates_on_top(int xh, int yh, double w, double l, double r) {
        int number_on_top = 0; /* total plates on top */
        int layers = 0; /* number of rows in grid */
        int rowlength = 0; /* number of plates in row */
        int row = 0; /* counter */
        int[] xla = new int[]{0};
        int[] yla = new int[]{0};
        int[] xra = new int[]{0};
        int[] yra = new int[]{0};
        layers = dense_layers(w, l, r);
        for (row = (xh + 1); (row < layers); row++) {
            rowlength = (plates_per_row(row, w, r) - 1);
            hex_to_array(row, (yh - (row - xh)), xla, yla);
            if ((yla[0] < 0)) {
                yla[0] = 0; /* left boundary */
            }
            hex_to_array(row, yh, xra, yra);
            if ((yra[0] > rowlength)) {
                yra[0] = rowlength; /* right boundary */
            }
            number_on_top += ((yra[0] - yla[0]) + 1);
        }
        return number_on_top;
    }

    public static int main() {
        double w = 0; /* box width */
        double l = 0; /* box length */
        double r = 0; /* plate radius */
        int i = 0; /* counters */
        int xmax = 0;
        C.printf("input box width, box length, and plate radius:\n");
        int _read0 = C.scan("%lf %lf %lf");
        if (_read0 > 0) w = C.scanDouble(0);
        if (_read0 > 1) l = C.scanDouble(1);
        if (_read0 > 2) r = C.scanDouble(2);
        C.printf("box width=%lf, box length=%lf, and plate radius=%lf:\n", w, l, r);
        C.printf("dense packing = %d\n", dense_plates(w, l, r));
        C.printf("grid packing = %d\n", grid_plates(w, l, r));
        /* print all the possible hexes in the box */
        xmax = (int)(Math.floor((w / (2 * r))));
        for (i = 0; (i < xmax); i++) {
            C.printf("(0,%d) has %d on top.\n", i, plates_on_top(0, i, w, l, r));
        }
        return 0;
    }

    public static void main(String[] args) {
        int status = main();
        if (status != 0) System.exit(status);
    }
}
