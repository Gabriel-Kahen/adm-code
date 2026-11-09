/*    suduku.c

    A backtracking program to solve Seduku
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

import java.util.Locale;

public class Sudoku {
    public static final int BASED = 3; /* base dimension, 3*3 blocks */
    public static final int DIMENSION = 9; /* 9*9 board */
    public static final int NCELLS = DIMENSION *DIMENSION; /* 81 cells in 9-by-9-board */
    public static final int MAXCANDIDATES = DIMENSION + 1; /* max digit choices per cell */
    public static class point {
        int x = 0; /* row and column coordinates of square */
        int y = 0; /* row and column coordinates of square */
    }
    public static class boardtype {
        int[][] m = new int[(DIMENSION + 1)][(DIMENSION + 1)]; /* board contents */
        int freecount = 0; /* open square count */
        Sudoku.point[] move = new Sudoku.point[(NCELLS + 1)]; /* which cells have we filled? */
        {
            for (int _i0 = 0; _i0 < (NCELLS + 1); _i0++) {
                move[_i0] = new Sudoku.point();
            }
        }
    }
    public static boolean finished = false;
    public static int steps = 0; /* how many total move insertions? */
    public static boolean fast = false; /* fast or slow nextmove algorithm? */
    public static boolean smart = false; /* quickly test for unfillable squares? */

    public static void possible_values(Sudoku.point p, Sudoku.boardtype board, boolean[] possible) {
        int x = 0; /* square to fill */
        int y = 0;
        int i = 0; /* counters */
        int j = 0;
        int xlow = 0; /* origin of box with (x,y) */
        int ylow = 0;
        boolean init = false;
        x = p.x;
        y = p.y;
        if (((board.m[x][y] != 0) || ((x < 0) || (y < 0)))) {
            init = false;
        } else {
            init = true;
        }
        possible[0] = false;
        for (i = 1; (i <= DIMENSION); i++) {
            possible[i] = init;
        }
        for (i = 0; (i < DIMENSION); i++) {
            if ((board.m[x][i] != 0)) {
                possible[board.m[x][i]] = false;
            }
        }
        for (i = 0; (i < DIMENSION); i++) {
            if ((board.m[i][y] != 0)) {
                possible[board.m[i][y]] = false;
            }
        }
        xlow = (BASED * (x / BASED));
        ylow = (BASED * (y / BASED));
        for (i = xlow; (i < (xlow + BASED)); i++) {
            for (j = ylow; (j < (ylow + BASED)); j++) {
                if ((board.m[i][j] != 0)) {
                    possible[board.m[i][j]] = false;
                }
            }
        }
    }

    public static void print_possible(boolean[] possible) {
        int i = 0; /* counter */
        for (i = 1; (i <= DIMENSION); i++) {
            if (possible[i]) {
                System.out.printf(Locale.US, " %d", i);
            }
            System.out.print("\n");
        }
    }

    public static int possible_count(int x, int y, Sudoku.boardtype board) {
        int i = 0; /* counter */
        int cnt = 0; /* number of open squares */
        boolean[] possible = new boolean[(DIMENSION + 1)]; /* what is possible for the square */
        Sudoku.point p = new Sudoku.point();
        p.x = x;
        p.y = y;
        possible_values(p, board, possible);
        cnt = 0;
        for (i = 1; (i <= DIMENSION); i++) {
            if (possible[i]) {
                cnt++;
            }
        }
        return cnt;
    }

    public static void fill_square(Sudoku.point p, int v, Sudoku.boardtype board) {
        if ((board.m[p.x][p.y] == 0)) {
            board.freecount = (board.freecount - 1);
        } else {
            System.out.printf(Locale.US, "Warning: filling already filled square (%d,%d)\n", p.x, p.y);
        }
        board.m[p.x][p.y] = v;
    }

    public static void free_square(Sudoku.point p, Sudoku.boardtype board) {
        if ((board.m[p.x][p.y] != 0)) {
            board.freecount = (board.freecount + 1);
        } else {
            System.out.printf(Locale.US, "Warning: freeing already empty square (%d,%d)\n", p.x, p.y);
        }
        board.m[p.x][p.y] = 0;
    }

    public static void next_square(Sudoku.point p, Sudoku.boardtype board) {
        int i = 0; /* counters */
        int j = 0;
        int bestcnt = 0; /* the best and latest square counts */
        int newcnt = 0;
        boolean doomed = false;
        bestcnt = (DIMENSION + 1);
        doomed = false;
        p.x = (p.y = (-1)); /* initialize to non-position */
        for (i = 0; (i < DIMENSION); i++) {
            for (j = 0; (j < DIMENSION); j++) {
                newcnt = possible_count(i, j, board);
                if (((newcnt == 0) && (board.m[i][j] == 0))) {
                    doomed = true;
                }
                if (fast) {
                    if ((((board.m[i][j] == 0) && (newcnt < bestcnt)) && (newcnt >= 1))) {
                        bestcnt = newcnt;
                        p.x = i;
                        p.y = j;
                    }
                } else {
                    if (((newcnt >= 1) && (board.m[i][j] == 0))) {
                        p.x = i;
                        p.y = j;
                    }
                }
            }
        }
        if ((doomed && smart)) {
            p.x = (p.y = (-1));
        }
    }

    public static void print_board(Sudoku.boardtype board) {
        int i = 0; /* counters */
        int j = 0;
        System.out.printf(Locale.US, "\nThere are %d free board positions.\n", board.freecount);
        for (i = 0; (i < DIMENSION); i++) {
            for (j = 0; (j < DIMENSION); j++) {
                if ((board.m[i][j] == 0)) {
                    System.out.print(" ");
                } else {
                    System.out.printf(Locale.US, "%c", ('0' + board.m[i][j]));
                }
                if ((((j + 1) % BASED) == 0)) {
                    System.out.print("|");
                }
            }
            System.out.print("\n");
            if ((((i + 1) % BASED) == 0)) {
                for (j = 0; (j < ((DIMENSION + BASED) - 1)); j++) {
                    System.out.print("-");
                }
                System.out.print("\n");
            }
        }
    }

    public static void init_board(Sudoku.boardtype board) {
        int i = 0; /* counters */
        int j = 0;
        for (i = 0; (i < DIMENSION); i++) {
            for (j = 0; (j < DIMENSION); j++) {
                board.m[i][j] = 0;
            }
            board.freecount = (DIMENSION * DIMENSION);
        }
    }

    public static void read_board(Sudoku.boardtype board) {
        int i = 0; /* counters */
        int j = 0;
        char c = '\000';
        int value = 0;
        Sudoku.point p = new Sudoku.point();
        init_board(board);
        for (i = 0; (i < DIMENSION); i++) {
            for (j = 0; (j < DIMENSION); j++) {
                int _read0 = C.scan("%c");
                if (_read0 > 0) c = (char)C.scanInt(0);
                value = (c - '0');
                if ((value != 0)) {
                    p.x = i;
                    p.y = j;
                    fill_square(p, value, board);
                }
            }
            int _read1 = C.scan("\n");
        }
    }

    public static void copy_board(Sudoku.boardtype a, Sudoku.boardtype b) {
        int i = 0;
        int j = 0;
        b.freecount = a.freecount;
        for (i = 0; (i < DIMENSION); i++) {
            for (j = 0; (j < DIMENSION); j++) {
                b.m[i][j] = a.m[i][j];
            }
        }
    }

    public static void process_solution(int[] a, int k, Sudoku.boardtype board) {
        finished = true;
        System.out.print("process solution\n");
        print_board(board);
    }

    public static boolean is_a_solution(int[] a, int k, Sudoku.boardtype board) {
        steps = (steps + 1); /* count steps for results table */
        return (board.freecount == 0);
    }

    public static void make_move(int[] a, int k, Sudoku.boardtype board) {
        fill_square(board.move[k], a[k], board);
    }

    public static void unmake_move(int[] a, int k, Sudoku.boardtype board) {
        free_square(board.move[k], board);
    }

    public static int construct_candidates(int[] a, int k, Sudoku.boardtype board, int[] c) {
        int i = 0; /* counter */
        boolean[] possible = new boolean[(DIMENSION + 1)]; /* which digits fit in this square */
        next_square(board.move[k], board); /* pick square to fill next */
        int nc = 0;
        if (((board.move[k].x < 0) && (board.move[k].y < 0))) {
            return nc; /* error condition, no moves possible */
        }
        possible_values(board.move[k], board, possible);
        for (i = 1; (i <= DIMENSION); i++) {
            if (possible[i]) {
                c[nc] = i;
                nc = (nc + 1);
            }
        }
        return nc;
    }

    public static void backtrack(int[] a, int k, Sudoku.boardtype input) {
        int[] c = new int[MAXCANDIDATES]; /* candidates for next position */
        int i = 0; /* counter */
        if (is_a_solution(a, k, input)) {
            process_solution(a, k, input);
        } else {
            k = (k + 1);
            int ncandidates = construct_candidates(a, k, input, c); /* next position candidate count */
            for (i = 0; (i < ncandidates); i++) {
                a[k] = c[i];
                make_move(a, k, input);
                backtrack(a, k, input);
                unmake_move(a, k, input);
                if (finished) {
                    return; /* terminate early */
                }
            }
        }
    }

    public static void solve_problem(Sudoku.boardtype board) {
        int[] a = new int[((DIMENSION * DIMENSION) + 1)];
        Sudoku.boardtype temp = new Sudoku.boardtype();
        System.out.print("----------------------------------\n");
        steps = 0;
        copy_board(board, temp);
        finished = false;
        backtrack(a, 0, temp);
        System.out.printf(Locale.US, "It took %d steps to find this solution ", steps);
        C.printf("for fast=%d  smart=%d\n", fast, smart);
    }

    public static int main() {
        Sudoku.boardtype board = new Sudoku.boardtype(); /* Sudoku board structure */
        read_board(board);
        print_board(board);
        fast = true;
        smart = true;
        solve_problem(board);
        fast = true;
        smart = false;
        solve_problem(board);
        fast = false;
        smart = true;
        solve_problem(board);
        fast = false;
        smart = false;
        solve_problem(board);
        return 0;
    }

    public static void main(String[] args) {
        int status = main();
        if (status != 0) System.exit(status);
    }
}
