# Algorithm and input guide

The root files are small programs as well as examples of reusable functions.
Read the relevant `main()` for the exact output: several demos print intermediate
tables, traversal events, or multiple runs. Headers and `#define` constants record
storage limits. Inputs must satisfy the mathematical preconditions below; the
programs do not all validate every malformed or out-of-range value.

## Conventions

- Graph vertices and most book/permutation sequences use indices **1 through n**.
  Geometry points and Sudoku cells use indices starting at **0** internally.
- Each root program has its own `main()`. Build its Makefile target instead of
  linking every C file together. A few files provide shared functions only.
- C `int` and `long` arithmetic has finite range. The checked Linux configuration
  uses 32-bit `int` and 64-bit `long`; do not infer unlimited arithmetic from a
  large array or a numeric result's return type.
- A header's maximum is a storage ceiling. Exhaustive search can become
  impractical far below that ceiling.

## Graphs

Unweighted graph readers expect:

```text
n m
x1 y1
x2 y2
... m edges
```

Weighted readers add a signed integer weight to each edge row:

```text
n m
x1 y1 weight1
x2 y2 weight2
... m edges
```

Use labels `1..n`, with `1 <= n <= MAXV` (`100` in the current graph examples).
The reader's `directed` argument determines orientation; it is not a field in the
input. The standalone programs choose it as follows:

| Programs | Input interpretation and result |
|---|---|
| `bfs-demo`, `dfs-demo` | Undirected; traverse from vertex 1 and print events/paths |
| `connected`, `bipartite`, `biconnected` | Undirected; components, coloring, or articulation vertices |
| `strong`, `strong1` | Directed; strongly connected components via two implementations |
| `topsort`, `topsort1` | Directed; use a DAG to obtain a topological order |
| `findcycle`, `countedges` | Undirected; inspect the component reachable from vertex 1 |
| `paths` | Undirected; enumerate simple paths between vertex 1 and each other vertex, in both directions |
| `prim` | Undirected weighted graph; tree for the component containing vertex 1 |
| `kruskal` | Undirected weighted graph; minimum spanning forest |
| `dijkstra` | Undirected weighted graph with **nonnegative** weights; paths from vertex 1 |
| `floyd` | Undirected weighted graph; all-pairs distances |

For a spanning tree covering the whole input, give Prim a connected graph.
Dijkstra's printed `Total SPST edgeweight` is the sum of the chosen tree edges,
not the sum of distances from the source. Unreachable path requests print
`No path`. Floyd's unreachable distances retain its numeric `MAXINT` sentinel;
its diagonal is zero. Negative edges in an undirected graph create a negative
walk cycle, so they do not define ordinary finite all-pairs shortest distances.

### Maximum flow

`netflow` takes a source/sink prefix, followed by a directed weighted graph:

```text
source sink
n m
x1 y1 capacity1
... m arcs
```

For example, two parallel unit-capacity arcs allow total flow 2:

```sh
printf '1 2\n2 2\n1 2 1\n1 2 1\n' | ./netflow
```

Capacities are nonnegative integers. Parallel arcs are coalesced; synthetic
reverse entries support rerouting. Printed edge triples are
`(capacity, flow, residual)`. Flow is **signed net flow**: the reverse entry has
opposite flow, and residual capacity is `capacity - flow`. A negative reverse
flow is expected after sending positive forward flow.

Graph storage and traversal support live in `graph.c`, `wgraph.c`, and
`bfs-dfs.c`. Their global search state and callback functions make these teaching
implementations unsuitable for concurrent searches without adaptation.

## Dynamic programming and strings

| Programs | Standard input | Preconditions and limits |
|---|---|---|
| `stringedit`, `lcs`, `substringedit`, `editbrute` | Two nonempty whitespace-separated strings | At most `MAXLEN=101` characters per token; APIs can also represent empty strings |
| `partition` | `n k`, then n book thicknesses | Nonnegative thicknesses; `1 <= k <= n <= 45`, `k <= 10`; groups are contiguous and nonempty |
| `subsetsum` | Case count, then `n target` and n values for each case | Nonnegative values; `0 <= n <= 100`, `0 <= target <= 10000` |
| `elevator` | Rider count and stop budget, then each rider's destination | At most 50 riders and a stop budget of 0..50; destination floors 0..25 |
| `binomial` | Case count, then `n k` per case | `0 <= k <= n <= 100`; each returned coefficient must fit `long` |
| `matrix` | First matrix's rows/columns and entries, then the second matrix in the same format | Dimensions 1..100; first column count equals second row count; products/sums fit `int` |
| `convolve` | First length and its coefficients, then second length and coefficients | Each length 1..100; products/sums fit `int` |

The string examples store a leading sentinel in slot zero; callers pass the
actual characters starting at slot one. Edit distance prints operation traces:
`M` match, `S` substitution, `I` insertion, and `D` deletion. LCS changes the
substitution cost; approximate substring matching changes the boundary/goal
conditions. `editbrute` uses recursive enumeration and is useful only for short
strings.

`partition` minimizes the largest group sum while preserving book order.
`subsetsum` prints one witness when the target is achievable. `elevator` minimizes
walking distance over the permitted building floors; zero elevator stops means
walking from the ground floor.

Binomial APIs return `-1` and set `errno` for an invalid domain (`EDOM`) or an
unrepresentable result (`ERANGE`). Its driver reports the error and exits
nonzero. Some requests with large n still fit, such as `100 choose 0`.

## Geometry

`convex-hull` and `triangulate` read a point count followed by pairs of real
coordinates:

```text
n
x1 y1
x2 y2
... n points
```

```sh
printf '4\n0 0\n1 0\n1 1\n0 1\n' | ./convex-hull
```

Geometry storage uses `MAXPOLY=200`. Convex hull accepts unordered points and
handles duplicates and collinear sets. Ear-clipping triangulation requires a
**simple, nondegenerate polygon in counterclockwise boundary order**, with at
least three vertices. Clockwise or invalid polygons are outside that routine's
contract and can prevent progress.

`geometry.c` provides point, line, segment, and orientation operations used by
`geotest`, `cgtest`, and the geometry demos. Floating predicates use an absolute
`EPSILON`; results near a geometric boundary can depend on coordinate scale and
floating-point rounding.

`plates` reads box width, box height, and disk radius, all positive; it compares
row-based grid and dense packing arrangements. `superman` reads start/end
coordinates, an obstacle count (at most 100), and circle center/radius rows. It
illustrates a chord/arc obstacle model; its assumptions about obstacle placement
must be respected. Neither example establishes a general optimal geometric
packing or arbitrary-obstacle shortest-path solver.

## Search and traveling salesperson

`8-queens`, `permutations`, and `subsets` run small fixed examples from their
drivers. The general backtracking hooks are solution detection, candidate
construction, and balanced make/unmake operations. The enumeration arrays hold
up to 100 entries, but the search spaces grow exponentially or factorially.

`sudoku` reads nine rows of nine digits, using `0` for an empty cell. It tries
four fast/smart heuristic combinations and prints their solutions and step
counts. Provide a valid puzzle; this demo is not a full invalid-board validator.

Both TSP programs first read city records:

```text
n
1 x1 y1
2 x2 y2
... n indexed integer-coordinate cities
```

Supply rows in city order; the reader uses their row positions rather than
reordering them by the first field.

- `tsp-astar` reads only those city records. It runs exact backtracking and
  branch-and-bound with lower-bound modes. Storage supports 1..20 cities; time
  and its 400,000-entry priority queue can become limiting much sooner. Queue
  exhaustion is an explicit error, not an optimality result.
- `tsp` additionally reads the reference tour's length and its permutation of
  city IDs. The heuristic demo then compares sampling, repeated hill climbing,
  and annealing. Use 2..1001 cities and a valid complete reference permutation.
  The driver's label `OPTIMAL SOLUTION COST` describes the supplied reference
  tour; it does not independently certify that tour's optimality.

Hill climbing accepts strict decreases in a recomputed tour objective, avoiding
cycles through equal-cost tours. Each proposed swap therefore costs O(n) to
evaluate. Annealing and sampling are heuristics; their results need not be
optimal. Seed and C-library random-number behavior affect their runs.

## Containers and remaining demos

| Files | Purpose |
|---|---|
| `queue`, `stack`, `priority_queue`, `set_union` | FIFO, LIFO, minimum heap, and disjoint-set operations |
| `list-demo`, `tree-demo` | Commands `i value`, `s value`, `d value`, and `p` for insert/search/delete/print |
| `sorting` | Insertion, selection, quick, heap, and merge sort; binary search |
| `bignum` | Signed decimal arithmetic with up to 100 digits; the CLI reads C `int` pairs |
| `gcd`, `primes` | GCD/Bézout coefficients for nonnegative operands, and factorization of positive integers |
| `fib` | Prints three Fibonacci implementations through index 92 on a 64-bit-`long` host |
| `10055` | Absolute differences of pairs of integers |
| `distance` | A fixed three-dimensional Euclidean-distance example |
| `name`, `polly` | String replacement and lexicographic sorting examples |
| `war` | Card-game simulation using ranks `23456789TJQKA` and suits `cdhs` |
| `order`, `sentinel` | Array traversal order and sentinel insertion examples |

Container operations have fixed capacities defined in their headers; use valid
push/pop, enqueue/dequeue, and heap operations. Bignum APIs report capacity
exhaustion explicitly and require a nonzero divisor for division. The bignum
driver prints `NaN` for a zero divisor. Historical variants may have different
interfaces and are covered only where a test names them explicitly.
