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
#include "backtrack.hpp"

namespace adm {
bool backtrack(std::vector<int> &prefix,
               const std::function<bool(const std::vector<int> &)> &complete,
               const Candidates &candidates, const std::function<void(int)> &make,
               const std::function<void(int)> &undo,
               const std::function<bool(const std::vector<int> &)> &visit) {
    if (complete(prefix)) {
        return visit(prefix);
    }
    for (int candidate : candidates(prefix)) {
        make(candidate);
        prefix.push_back(candidate);
        bool stop;
        try {
            stop = backtrack(prefix, complete, candidates, make, undo, visit);
        } catch (...) {
            prefix.pop_back();
            undo(candidate);
            throw;
        }
        prefix.pop_back();
        undo(candidate);
        if (stop) {
            return true;
        }
    }
    return false;
}
} // namespace adm
