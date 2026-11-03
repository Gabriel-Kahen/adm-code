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

public final class Sudoku {
    /** First Sudoku solution, or null for an unsatisfiable valid board. Contradictory givens are errors. */
    public static String sudoku(String puzzle) {
        return sudoku(puzzle, true);
    }

    public static String sudoku(String puzzle, boolean mostConstrainedFirst) {
        if (puzzle.length() != 81) {
            throw new IllegalArgumentException("Sudoku requires 81 digits");
        }
        int[] board = new int[81];
        int[] rows = new int[9];
        int[] columns = new int[9];
        int[] boxes = new int[9];
        for (int cell = 0; cell < 81; cell++) {
            char character = puzzle.charAt(cell);
            if (character < '0' || character > '9') {
                throw new IllegalArgumentException("Sudoku requires digits 0..9");
            }
            board[cell] = character - '0';
            if (board[cell] == 0) {
                continue;
            }
            int row = cell / 9;
            int column = cell % 9;
            int box = row / 3 * 3 + column / 3;
            int mask = 1 << board[cell];
            if (((rows[row] | columns[column] | boxes[box]) & mask) != 0) {
                throw new IllegalArgumentException("contradictory Sudoku givens");
            }
            rows[row] |= mask;
            columns[column] |= mask;
            boxes[box] |= mask;
        }
        if (!sudokuVisit(board, rows, columns, boxes, mostConstrainedFirst)) {
            return null;
        }
        StringBuilder result = new StringBuilder();
        for (int value : board) {
            result.append(value);
        }
        return result.toString();
    }

    static boolean sudokuVisit(int[] board, int[] rows, int[] columns, int[] boxes, boolean smart) {
        int bestCell = -1;
        int bestMask = 0;
        int bestCount = 10;
        for (int cell = 0; cell < 81; cell++) {
            if (board[cell] != 0) {
                continue;
            }
            int row = cell / 9;
            int column = cell % 9;
            int mask = 0x3fe & ~(rows[row] | columns[column] | boxes[row / 3 * 3 + column / 3]);
            int count = Integer.bitCount(mask);
            if (count == 0) {
                return false;
            }
            if (count < bestCount) {
                bestCell = cell;
                bestMask = mask;
                bestCount = count;
            }
            if (!smart) {
                break;
            }
        }
        if (bestCell == -1) {
            return true;
        }
        int row = bestCell / 9;
        int column = bestCell % 9;
        int box = row / 3 * 3 + column / 3;
        for (int remaining = bestMask; remaining != 0; remaining &= remaining - 1) {
            int bit = Integer.lowestOneBit(remaining);
            board[bestCell] = Integer.numberOfTrailingZeros(bit);
            rows[row] |= bit;
            columns[column] |= bit;
            boxes[box] |= bit;
            if (sudokuVisit(board, rows, columns, boxes, smart)) {
                return true;
            }
            board[bestCell] = 0;
            rows[row] ^= bit;
            columns[column] ^= bit;
            boxes[box] ^= bit;
        }
        return false;
    }

    public static void main(String[] args) {
        java.util.Scanner in = new java.util.Scanner(System.in);
        String puzzle =
            in.hasNext()
                ? in.next()
                : "530070000600195000098000060800060003400803001700020006060000280000419005000080079";
        System.out.println(sudoku(puzzle));
    }
}
