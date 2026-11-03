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

#include "graph.hpp"

namespace adm {
// Generic backtracking calls undo after EVERY make, even when visit stops early.
// Returning true from visit requests early termination. State is held by callbacks.
using Candidates = std::function<std::vector<int>(const std::vector<int> &)>;
bool backtrack(std::vector<int> &prefix,
               const std::function<bool(const std::vector<int> &)> &complete,
               const Candidates &candidates, const std::function<void(int)> &make,
               const std::function<void(int)> &undo,
               const std::function<bool(const std::vector<int> &)> &visit);
} // namespace adm
