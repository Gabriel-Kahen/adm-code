/*	elevator.c

	Elevator stop optimization via dynamic programming.
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

public class Elevator {
    public static final int NFLOORS = 25; /* the height of the building in floors */
    public static final int MAX_RIDERS = 50; /* what is the capacity of the elevator? */
    public static final int MAXINT = 100007;
    public static int[] stops = new int[(MAX_RIDERS + 1)]; /* what floor does everyone get off at? */
    public static int nriders = 0; /* number of riders */
    public static int nstops = 0; /* number of allowable stops */
    public static int[][] m = new int[(NFLOORS + 1)][(MAX_RIDERS + 1)]; /* dynamic programming cost table */
    public static int[][] p = new int[(NFLOORS + 1)][(MAX_RIDERS + 1)]; /* dynamic programming parent table */

    public static int min(int a, int b) {
        if ((a < b)) {
            return a;
        }
        return b;
    }

    public static int floors_walked(int previous, int current) {
        int nsteps = 0; /* total distance traveled */
        int i = 0; /* counter */
        for (i = 1; (i <= nriders); i++) {
            if (((stops[i] > previous) && (stops[i] <= current))) {
                nsteps += min((stops[i] - previous), (current - stops[i]));
            }
        }
        return nsteps;
    }

    /*	m[i][j] denotes the cost of serving all the riders using j stops,
	the last of which is at floor i.  Zero is the originating floor.
    */
    public static int optimize_floors() {
        int i = 0;
        int j = 0;
        int k = 0;
        int cost = 0; /* costs placeholder */
        int laststop = 0; /* the elevator's last stop */
        if (((((nriders < 0) || (nriders > MAX_RIDERS)) || (nstops < 0)) || (nstops > MAX_RIDERS))) {
            return (-1);
        }
        for (i = 0; (i <= NFLOORS); i++) {
            m[i][0] = floors_walked(0, MAXINT);
            p[i][0] = (-1);
        }
        for (j = 1; (j <= nstops); j++) {
            for (i = 0; (i <= NFLOORS); i++) {
                m[i][j] = MAXINT;
                for (k = 0; (k <= i); k++) {
                    cost = (((m[k][(j - 1)] - floors_walked(k, MAXINT)) + floors_walked(k, i)) + floors_walked(i, MAXINT));
                    if ((cost < m[i][j])) {
                        m[i][j] = cost;
                        p[i][j] = k; /* counters */
                    }
                }
            }
        }
        laststop = 0;
        for (i = 1; (i <= NFLOORS); i++) {
            if ((m[i][nstops] < m[laststop][nstops])) {
                laststop = i;
            }
        }
        return laststop;
    }

    public static void reconstruct_path(int lastfloor, int stops_to_go) {
        if ((stops_to_go > 1)) {
            reconstruct_path(p[lastfloor][stops_to_go], (stops_to_go - 1));
        }
        C.printf("%d\n", lastfloor);
    }

    public static void print_matrix(int[][] m) {
        int i = 0; /* counters */
        int j = 0;
        for (j = 0; (j <= nstops); j++) {
            for (i = 0; (i <= NFLOORS); i++) {
                C.printf("%3d", m[i][j]);
            }
            C.printf("\n");
        }
    }

    public static int main() {
        int i = 0; /* counter */
        int laststop = 0;
        int _read0 = C.scan("%d %d");
        if (_read0 > 0) nriders = C.scanInt(0);
        if (_read0 > 1) nstops = C.scanInt(1);
        if ((((((_read0 != 2) || (nriders < 0)) || (nriders > MAX_RIDERS)) || (nstops < 0)) || (nstops > MAX_RIDERS))) {
            C.fprintf("invalid elevator dimensions\n");
            return 1;
        }
        for (i = 1; (i <= nriders); i++) {
            int _read1 = C.scan("%d");
            if (_read1 > 0) stops[i] = C.scanInt(0);
            if ((((_read1 != 1) || (stops[i] < 0)) || (stops[i] > NFLOORS))) {
                C.fprintf("invalid destination floor\n");
                return 1;
            }
        }
        for (i = 1; (i <= nriders); i++) {
            C.printf("%d\n", stops[i]);
        }
        laststop = optimize_floors();
        print_matrix(m);
        C.printf("\n");
        print_matrix(p);
        C.printf("cost = %d\n", m[laststop][nstops]);
        reconstruct_path(laststop, nstops);
        return 0;
    }

    public static void main(String[] args) {
        int status = main();
        if (status != 0) System.exit(status);
    }
}
