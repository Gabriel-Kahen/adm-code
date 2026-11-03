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

import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

public final class Order {
    /** Traversal coordinates for any nonnegative rectangular dimensions. O(rows*columns). */
    public static List<int[]> grid(String method, int rows, int columns) {
        if (rows < 0 || columns < 0 || (long)rows * columns > Integer.MAX_VALUE) {
            throw new IllegalArgumentException("invalid grid dimensions");
        }
        List<int[]> result = new ArrayList<>();
        switch (method) {
        case "row" -> {
            for (int row = 0; row < rows; row++) {
                for (int column = 0; column < columns; column++) {
                    result.add(new int[] {row, column});
                }
            }
        }
        case "column" -> {
            for (int column = 0; column < columns; column++) {
                for (int row = 0; row < rows; row++) {
                    result.add(new int[] {row, column});
                }
            }
        }
        case "snake" -> {
            for (int row = 0; row < rows; row++) {
                for (int i = 0; i < columns; i++) {
                    result.add(new int[] {row, row % 2 == 0 ? i : columns - 1 - i});
                }
            }
        }
        case "diagonal" -> {
            for (long diagonal = 0; diagonal < (long)rows + columns - 1; diagonal++) {
                int first = (int)Math.max(0, diagonal - columns + 1);
                int last = (int)Math.min(rows - 1L, diagonal);
                for (int row = first; row <= last; row++) {
                    result.add(new int[] {row, (int)(diagonal - row)});
                }
            }
        }
        default -> throw new IllegalArgumentException("unknown grid traversal");
        }
        return result;
    }

    public static void main(String[] args) {
        for (int[] cell : grid("diagonal", 3, 4)) {
            System.out.println(Arrays.toString(cell));
        }
    }
}
