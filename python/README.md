# Python algorithms

Readable, independently callable Python 3.10+ implementations of the C programs
and their shared libraries. The modules use zero-based indices and own their
search state. They require only the standard library. The original permission
notice is preserved in every source file and in [NOTICE](NOTICE).

From the repository root:

```sh
PYTHONPATH=python python3 -m adm sort merge 8 -1 3 3
PYTHONPATH=python python3 -m adm edit kitten sitting
PYTHONPATH=python python3 -m adm selftest
```

Each command prints one JSON value. Errors go to standard error and exit with
status 2. Shell quoting preserves empty strings and spaces:

```sh
PYTHONPATH=python python3 -m adm edit '' 'a b'
```

For normal use, import the library directly:

```python
from adm.graphs import Graph, dijkstra, reconstruct_path

network = Graph(4, directed=True)
network.add_edge(0, 1, 3)
network.add_edge(1, 2, 2)
distances, parents = dijkstra(network, 0)
assert distances == [0, 3, 5, None]
assert reconstruct_path(parents, 0, 2) == [0, 1, 2]
```

## Module and API map

| Module | Public algorithms and types |
| --- | --- |
| `adm.containers` | `Queue`, `Stack`, hand-written `MinHeap`, `DisjointSet`, `LinkedList`, `BinarySearchTree` |
| `adm.sorting` | `insertion_sort`, `selection_sort`, `quick_sort`, `heap_sort`, `merge_sort`, `binary_search`, `sentinel_insert` |
| `adm.numeric` | `absolute_difference`, `big_integer`, `fibonacci` (recursive/memo/table/constant), `binomial`, `extended_gcd`, `prime_factors`, `euclidean_distance`, `matrix_multiply`, `convolve`, `RandomSource` |
| `adm.graphs` | Mutable `Graph`, `breadth_first_search`, `depth_first_search`, `reconstruct_path`, `connected_components`, `bipartite_coloring`, `has_undirected_cycle`, `articulation_points`, `strongly_connected_components` (Tarjan/Kosaraju), `topological_sort` (Kahn/DFS), `minimum_spanning_forest` (Prim/Kruskal), `dijkstra`, `floyd_warshall`, `maximum_flow`, `simple_paths` |
| `adm.dynamic` | `edit_distance` with trace, `edit_distance_brute`, `longest_common_subsequence`, `substring_edit_distance`, `linear_partition`, `subset_sum`, `elevator_stops` |
| `adm.geometry` | `Line`, line construction/equivalence/intersection/projection, orientation, segment intersection, triangle/polygon areas, `convex_hull`, `triangulate`, `minimum_weight_triangulation`, grid/dense disk packing, hex/array/Cartesian conversions, `plates_on_top`, `superman` |
| `adm.search` | Generic callback `backtrack`, `permutations`, `subsets`, `queens`, `solve_sudoku`, `tour_cost`, `swap_delta`, `traveling_salesperson` (exact/best/sample/hill/anneal), `repeated_tsp` |
| `adm.demos` | `grid_order`, `find_match`, `replace_names`, `Suitor`, `rank_suitors`, card encoding/decoding, bounded `war` |

The graph stores parallel edges with stable IDs. `add_edge` returns the ID and
`delete_edge` removes that specific edge. `len(graph.edges)` counts each input
edge once. BFS and Dijkstra return both distances and parents; unreachable
entries are `None`. Maximum flow returns a `FlowResult` with the value, residual
matrix, and antisymmetric signed net-flow matrix. Reverse flows can be negative.

The linked list retains duplicates and deletes the first match. The binary
search tree is an unbalanced ordered set and ignores duplicate insertions.
Empty queue/stack/heap removal raises `IndexError`; invalid domains raise
`ValueError`. Sorting returns a new list. Binary search requires sorted input
and returns the first occurrence. Direct library callers supply that
precondition; the CLI checks it.

Python tuples represent points and segment endpoints. Native tuple assignment
replaces the C point-copy/swap helpers; printers are replaced by returned values.
There is no fixed-capacity C storage ceiling and no shared global search state.
Historical copies and unfinished interfaces are represented by the supported
algorithms, rather than by reproducing their accidental behavior.

## Numerical and computational contracts

Python integer arithmetic is exact, subject to available memory. Bignum division
truncates toward zero, matching the other ports. Fibonacci, binomial, absolute
difference, and bignum CLI results are decimal JSON strings to preserve exactness
for consumers. Integer graph weights, matrix entries, and DP costs also use
Python integers. The other ports document their finite integer limits.

Strings use Python Unicode code points. The common cross-language string domain
is ASCII; C++ byte indexing and Java UTF-16 indexing differ for non-ASCII input.
No locale-dependent normalization or case folding is performed.

Geometry uses finite binary floating-point coordinates and an absolute `1e-9`
predicate tolerance. Use moderately scaled coordinates; results near boundaries
are tolerance dependent. Hulls keep only collinear endpoints. Ear clipping
accepts either winding of a simple nondegenerate polygon and rejects invalid
boundaries. Minimum-weight triangulation requires strict convexity and minimizes
the sum of triangle perimeters. `superman` implements the book's chord/arc model
for disjoint circles with outside endpoints; it is not a general obstacle path
optimizer. Packing compares two row-based layouts and both box orientations;
it does not claim globally optimal packing.

Brute edit distance requires total string length at most 18. Recursive Fibonacci
requires index at most 30; memoized recursion allows at most 800. Exact DFS/best-first TSP allows at most 12 cities;
best-first search raises an explicit error if its frontier would exceed 1,000,000 states.
Permutation materialization allows at most 9 items, subset materialization at
most 20, and n-queens counting at most 15. These are resource bounds, not promises
that the largest allowed instance will finish quickly. Recursive graph searches,
backtracking, and geometric algorithms can also reach Python's recursion limit;
use suitably sized teaching examples. CLI recursion exhaustion is an explicit
error. Simple-path enumeration can have exponentially large output.

`RandomSource` uses an isolated seeded generator, inclusive integer bounds, and
Fisher-Yates shuffling. Repeated seeds reproduce a run within Python; random
sequences need not match the other languages. Hill climbing accepts only strict
full-cost decreases. Annealing and sampling return the best visited tour;
heuristic results do not establish optimality. `repeated_tsp` runs independent
seeded restarts and retains the best; `solve_sudoku` exposes `mrv` and `row`
strategies while sharing constraint checks.

## Verification

```sh
PYTHONPATH=python python3 -m adm selftest
PYTHONPATH=python python3 -m unittest adm.selftest -v
```

The native tests check container mutation, heap ordering, duplicate handling,
graph deletion and predecessor reconstruction, flow capacity/conservation,
geometry conversion round trips, generic backtracking undo under early stop and
exceptions, seeded randomness, and TSP costs against exhaustive permutations.
They run under `python -O` too; validation does not rely on removable `assert`
statements. The repository's shared conformance suite additionally uses
independent small-instance oracles and checks the same CLI contracts in all
three languages.
