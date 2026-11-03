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
import java.util.List;

public final class Backtrack {
    /** Callbacks see a read-only prefix; make/unmake must balance for every completed move. */
    public interface Problem<T> {
        boolean isSolution(List<T> prefix);
        List<T> candidates(List<T> prefix);
        default void makeMove(List<T> prefix) {}
        default void unmakeMove(List<T> prefix) {}
        /** Return false to stop the entire search after this solution. */
        boolean processSolution(List<T> prefix);
    }

    public static <T> void backtrack(Problem<T> problem) {
        enumerate(problem, new ArrayList<>());
    }

    static <T> boolean enumerate(Problem<T> problem, List<T> prefix) {
        if (problem.isSolution(List.copyOf(prefix))) {
            return problem.processSolution(List.copyOf(prefix));
        }
        for (T candidate : problem.candidates(List.copyOf(prefix))) {
            prefix.add(candidate);
            try {
                problem.makeMove(List.copyOf(prefix));
                try {
                    if (!enumerate(problem, prefix)) {
                        return false;
                    }
                } finally {
                    problem.unmakeMove(List.copyOf(prefix));
                }
            } finally {
                prefix.remove(prefix.size() - 1);
            }
        }
        return true;
    }
}
