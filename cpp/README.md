# C++ algorithm library

The C++17 implementations use the `adm` namespace and zero-based indices. Include
`include/adm.hpp` to call them independently of the command-line driver. They are
derived from Steven S. Skiena's programs; the original permission notice is kept
in every derived source file. The parent repository's permission terms apply.

Build with GCC or Clang, without third-party libraries:

```sh
mkdir -p build/ports/cpp
g++ -std=c++17 -O2 -Wall -Wextra -Wpedantic -Werror \
    -I cpp/include cpp/src/*.cpp -o build/ports/cpp/adm
build/ports/cpp/adm selftest
build/ports/cpp/adm sort merge 9 -2 4 4
build/ports/cpp/adm binomial 100 50
build/ports/cpp/adm dijkstra 3 1 2 0 1 7 1 2 4 0
```

Run these commands from the repository root. The final example describes three
vertices, directed edges `0 -> 1` of weight 7 and `1 -> 2` of weight 4, and source
vertex 0. It returns `[0,7,11]`. Each invocation writes one JSON result, or a clear
error on standard error with a nonzero exit status. Arguments are already
separated by the shell: quote strings containing spaces or an empty string.
The shared operation reference is in [the language guide](../docs/LANGUAGES.md).

For your own executable, link the implementation files below and leave out
`src/main.cpp`. The tests in `src/selftest.cpp` can also be omitted.

```cpp
#include "adm.hpp"

int main() {
    adm::Graph network(4, true);
    network.insert(0, 1, 3);
    network.insert(1, 3, 2);
    const auto flow = adm::maximum_flow(network, 0, 3); // 2
    return flow == 2 ? 0 : 1;
}
```

## Source and API map

All public declarations and result types are in `include/adm.hpp`. Functions
return values and own their working state; they do not write global search state
or diagnostic tables. Invalid domains throw `std::invalid_argument`. Checked
integer overflow throws `std::overflow_error`.

| Source | Main public APIs | Time and auxiliary space |
|---|---|---|
| `src/containers.cpp` | `Queue<T>`, `Stack<T>`, `MinHeap`, `DisjointSet` | Queue/stack operations amortized O(1); heap O(log n); union-find amortized O(alpha(n)); O(n) storage |
| `src/containers.cpp` | `LinkedList`, `BinarySearchTree` | List insertion O(1), search/deletion O(n); unbalanced BST O(height) operations; O(n) storage |
| `src/containers.cpp` | `sort`, `binary_search`, `sentinel_insert` | Insertion/selection O(n²), quick average O(n log n) and worst O(n²), heap/merge O(n log n); merge/heap O(n) auxiliary space; quick O(log n) call stack |
| `src/numeric.cpp` | `BigInteger` exact signed arithmetic | Grade-school decimal addition O(d), multiplication/division O(d²) for comparable digit counts; dynamic storage |
| `src/numeric.cpp` | `fibonacci`, `binomial`, `extended_gcd`, `prime_factors` | Fibonacci recursive exponential, memo/table O(n) additions, constant O(n) additions with two big integers; Pascal-row binomial O(n * min(k,n-k)) big-integer additions; GCD O(log max(a,b)); trial division O(sqrt(n)) |
| `src/numeric.cpp` | `matrix_multiply`, `convolve`, `distance`, `Random` | Matrix O(rows * inner * columns), convolution O(nm), distance O(d), Fisher–Yates O(n); output-sized space |
| `src/graphs.cpp` | `Graph`, `bfs`, `dfs`, `reconstruct_path`, `connected_components`, `bipartite_coloring`, `has_cycle`, `articulation_points` | Traversals/cuts O(V+E); cycle check O(E alpha(V)); adjacency storage O(V+E); deletion rebuilds adjacency in O(V+E) |
| `src/graphs.cpp` | `strongly_connected`, `topological_order` | Tarjan/Kosaraju SCC and Kahn/DFS ordering O(V+E), plus canonical SCC sorting; O(V+E) storage |
| `src/graphs.cpp` | `minimum_spanning_forest`, `dijkstra`, `floyd_warshall`, `maximum_flow` | Kruskal O(E log E), Prim/Dijkstra O((V+E) log E), Floyd O(V³)/O(V²) space; matrix Edmonds–Karp O(V³E)/O(V²) space |
| `src/dynamic.cpp` | `edit_distance`, `brute_edit_distance`, `longest_common_subsequence`, `substring_edit_distance` | Table methods O(nm); edit/LCS O(nm) space, substring O(m); brute recursion exponential |
| `src/dynamic.cpp` | `linear_partition`, `subset_sum`, `elevator_stops` | Partition O(kn²)/O(kn); subset sum O(n * target)/O(target); elevator O(budget * floors² * riders)/O(budget * floors) |
| `src/geometry.cpp` | `Point`, `Line`, `Circle`; `orientation`, `triangle_area`, `points_to_line`, `point_slope_line`, `parallel`, `same_line`, `intersection`, `project`, `in_box`, `segments_intersect` | Constant-time finite-coordinate primitives |
| `src/geometry.cpp` | `polygon_area`, `convex_hull`, `triangulate`, `minimum_weight_triangulation` | Area O(n); monotone-chain hull O(n log n); ear clipping O(n³); convex minimum-weight triangulation O(n³)/O(n²) |
| `src/geometry.cpp` | `dense_layers`, `plates_per_row`, `dense_plates`, `grid_plates`, `hex_to_cartesian`, `cartesian_to_hex`, `array_to_hex`, `hex_to_array`, `plates_on_top`, `superman` | Packing/conversions O(1), plates above O(layers), chord/arc model O(circles²) including overlap validation |
| `src/search.cpp` | `backtrack`, `permutations`, `subsets`, `queens`, `sudoku` | Output-sensitive exponential search; Sudoku uses either MRV or row-first choice and either bitmasks or recomputed candidates |
| `src/search.cpp` | `tour_cost`, `swap_delta`, `traveling_salesperson`, `repeated_traveling_salesperson` | Tour cost and swap delta O(n); exact DFS/best-first factorial worst case; heuristics have explicit iteration budgets; restarts retain best result |
| `src/demos.cpp` | `grid_order`, `find_match`, `replace_names`, `rank_suitors`, `encode_card`, `decode_card`, `war` | Grid output O(rows * columns); naive matching O(nm); ranking O(n log n); War O(step limit * deck size) |

`binary_search` validates its sorted-input precondition in O(n) before its O(log n)
search. Returned canonical group sorting adds O(V log V). The BST intentionally remains
unbalanced: no logarithmic bound is implied for ordered inserts.

## Contracts that matter

- `BigInteger`, Fibonacci and binomial use exact decimal arithmetic without a
  fixed digit limit. `BigInteger` division truncates toward zero. The CLI emits
  these results as JSON strings. Other integer arithmetic uses checked signed
  64-bit values; intermediate values must fit. GCD rejects the minimum signed
  64-bit operand because its absolute magnitude exceeds the signed working
  representation, even when the final GCD would fit.
  The checked arithmetic helpers use GCC/Clang overflow builtins.
- Strings are `std::string` bytes; byte offsets and edit operations agree with
  the other language ports on ASCII. Unicode grapheme processing is not implied.
- `Graph` retains parallel input edges and self loops; deleting an edge removes
  one occurrence. Undirected cycle and articulation routines distinguish input
  edge IDs. Dijkstra rejects negative edges anywhere in its graph, and Floyd
  rejects negative cycles. Prim and Kruskal cover disconnected graphs as forests.
- `bipartite_coloring` returns `nullopt` for a non-bipartite graph. Distances use
  `std::optional<Integer>` for unreachable vertices, so no numeric value doubles
  as an infinity sentinel. `reconstruct_path` returns an empty list when the
  target's parent chain does not reach the source. `maximum_flow` coalesces
  parallel capacities and allows antiparallel arcs; source and sink must differ.
- `LinkedList` allows duplicates and erases the first matching node.
  `BinarySearchTree` has set semantics and ignores duplicate insertion.
- Partition groups are nonempty and preserve input order. Subset sum accepts
  nonnegative values and returns distinct input indices. Elevator optimization
  uses at most the requested number of stops, with floor zero always available.
- Geometry uses an absolute tolerance of `1e-9`, adjustable on primitive
  predicates. Inputs must be finite, and extreme coordinate scales can exceed
  floating-point precision or range. Polygon triangulation validates simplicity,
  accepts either winding, and rejects degeneracy rather than looping. `mwt`
  minimizes the **sum of triangle perimeters** for a strictly convex polygon.
- Packing helpers describe row-based layouts, not a globally optimal disk
  packing proof. The CLI compares both rectangle orientations. `superman`
  computes the original chord/arc model only for disjoint circles with endpoints
  outside them; overlapping obstacles and interior endpoints are rejected.
- Sudoku validates all givens before solving and returns `nullopt` if no solution
  exists. `sudoku(board, smart, fast)` exposes all four original heuristic
  combinations: MRV versus row-first cell selection, and bitmask versus scanned
  candidates. It returns one solution without claiming uniqueness.
- TSP exact DFS and best-first search use an admissible outgoing-edge lower
  bound. They accept at most 12 cities. Heuristics return valid tours with fully
  recomputed costs and make no optimality claim. `hill` accepts strict objective
  decreases; `anneal` may accept increases. Repeated runs derive seeds as
  `seed + run` modulo 2^64 and return the best tour found, including the first.
- `Random` uses `std::mt19937_64`. A seed reproduces a run on the same standard
  library implementation; sequences need not match other languages or C++
  standard libraries. Integer bounds are inclusive; real bounds are half open
  unless both endpoints are equal.
- `backtrack` balances every successful `make` with `undo`, including early stop
  and exceptions from recursive search or the solution visitor. Returning true
  from the visitor stops traversal. Candidate construction must return a finite
  list. Search results and recursion can exhaust time, memory or the call stack
  well before integer limits.

Explicit educational search limits are permutations `0..10`, subsets `0..20`,
queens `0..15`, brute edit combined length at most 16, recursive Fibonacci index
at most 35, and subset-sum target at most 10,000,000. These are practical guards,
not polynomial-time guarantees for exhaustive algorithms.

## Native checks

`adm selftest` exercises both CLI-backed algorithms and library-only operations:
container underflow and mutation, union-find, linked-list/BST deletion, seeded RNG
and shuffling, graph mutation and parent reconstruction, line equivalence and
coordinate round trips, supported packing cells, all Sudoku strategies, balanced
backtracking undo on stop/exception, adjacent/wraparound TSP swaps and repeated
heuristic runs. It also checks signed and large bigint arithmetic. Any failure
returns nonzero. The shared Python conformance suite independently checks
mathematical results and witnesses across all three languages.
