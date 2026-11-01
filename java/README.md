# Java implementations

Independent Java 17 implementations of the algorithms in the C distribution.
The original copyright and permission notice remains in every derived source.
Use these classes directly as a library or run the shared demonstration interface.
There are no third-party Java dependencies.

From the repository root:

```sh
mkdir -p build/ports/java
javac --release 17 -Xlint:all -Werror -d build/ports/java java/src/adm/*.java
java -cp build/ports/java adm.Main sort merge 8 -1 3 3
java -cp build/ports/java adm.Main edit kitten sitting
java -cp build/ports/java adm.Main selftest
```

The commands print `[-1,3,3,8]`, an edit result with cost 3, and `true` respectively.
The native selftests use explicit checks and run without Java's `-ea` option.
See the repository's shared port guide for command arguments and cross-language
oracle tests. Each command prints one JSON result. Invalid domains, missing or
extra arguments, arithmetic overflow, and exhausted exact-search capacity produce
an error on stderr and a nonzero exit code.

## Library map

All classes are in package `adm`, with static algorithms and per-instance mutable
containers, graphs, and random generators. There is no shared search state.

| Class | Public entry points and behavior |
|---|---|
| `Containers` | `Queue<T>` and `Stack<T>`; hand-written `MinHeap`; union-by-size/path-compressed `DisjointSet`; `LinkedList`; `BinarySearchTree` |
| `Sorting` | `sort(method, array)` for insertion, selection, quick, heap, and merge; first-match `binarySearch`; sorted `insert` |
| `Numeric` | `absoluteDifference`, signed `bigint`, four `fibonacci` strategies, Pascal-row DP `binomial`, `extendedGcd`, `factors`, N-dimensional `distance`, checked `multiply` and `convolve`, seeded `Generator` |
| `Graphs` | Mutable `Graph`, `breadthFirst` with parent witness, `depthFirst`, `path`, `components`, `bipartiteColors`, `bipartite`, `hasCycle`, `articulation`, two `stronglyConnected` and `topological` strategies, Prim/Kruskal `minimumSpanningForest`, `dijkstra`/`dijkstraPaths`, `floyd`, `maximumFlow`, `simplePaths` |
| `Dynamic` | `edit` with operation witness, `editBrute`, `lcs`, `substring`, `partition`, `subsetSum`, `elevator` |
| `Geometry` | Immutable `Point`, normalized `Line`, `Circle`; line construction/equality/intersection/projection, orientation/area, closed segment intersection, `convexHull`, `triangulate`, `minimumWeightTriangulation`, disk packing, hex/array/Cartesian conversions, `platesOnTop`, `superman` |
| `Search` | Callback `backtrack`, `permutations`, `subsets`, `queens`, validated `sudoku`, `identityTour`, `tourCost`, `swapDelta`, exact/heuristic `tsp`, `repeatedTsp` |
| `Demos` | `grid`, naive substring `find`, sequential `replace`, `rankSuitors`, `card`/`uncard`, original-rules `war` |

For example:

```java
import adm.Dynamic;
import adm.Graphs;

Dynamic.Edit alignment = Dynamic.edit("kitten", "sitting");
Graphs.Graph graph = new Graphs.Graph(3, false);
graph.add(0, 1, 7);
graph.add(1, 2, 4);
Graphs.ShortestPaths paths = Graphs.dijkstraPaths(graph, 0);
System.out.println(Graphs.path(paths.parents(), 0, 2)); // [0, 1, 2]
```

## Contracts and limits

- Vertices, string positions, cells, and witness indices start at zero. Graphs
  accept parallel edges and self-loops. `Graph.delete(u,v)` removes the first
  matching input edge; either orientation matches an undirected edge.
- Containers grow dynamically. Empty pop/dequeue/heap-minimum throws
  `NoSuchElementException`. List insertion is at the head, duplicates are allowed,
  and deletion removes the first match. The unbalanced BST stores a **set**:
  duplicate insertion has no effect; deleting an absent value has no effect.
- Sorting returns a copy. Binary search assumes sorted input; the CLI checks this
  precondition. Insertion and selection are O(n²); merge and heap are O(n log n).
  Quicksort has O(n²) worst-case work but recurses only into the smaller partition,
  limiting call depth to O(log n).
- Exact scalar integer routines use `BigInteger`. Division truncates toward zero;
  a zero divisor is an error. Matrix, convolution, path, forest, and capacity
  arithmetic use signed 64-bit `long` with checked intermediates. An unrepresentable
  intermediate is an error, even when another evaluation order could fit.
  Unreachable graph distances are `null`, so `Long.MAX_VALUE` remains a valid
  distance. Matrix CLI dimensions must be positive.
- `fibonacci` supports `recursive`, `memo`, `table`, and `constant`. Recursion is
  intentionally limited to 35, memoized recursion to 1000, and iterative methods
  to 100000. Binomial DP stores the smaller requested Pascal-row prefix. Trial
  factorization is O(sqrt(n)) and requires n >= 1; it is unsuitable for huge primes.
- Edit operations are `M` match, `S` substitution, `I` insertion, and `D` deletion.
  String algorithms use Java UTF-16 code units. Shared cross-language string
  comparisons use ASCII, including empty strings and spaces. Brute edit distance
  is limited to combined input length 18. Subset sum accepts nonnegative values
  and target 0..1000000. Partition requires 1..n nonempty contiguous groups and
  nonnegative values. Elevator stops are an **at most** budget; floor 0 is free,
  destinations must be inside 0..maxFloor, and maxFloor is limited to 1000.
- BFS, DFS, components, coloring, cycle/articulation checks, SCC, and topological
  sorting are O(V+E). Tarjan/Kosaraju and Kahn/DFS are separate implementations.
  Topological methods reject cycles. Dijkstra rejects every negative input edge,
  including unreachable ones; Floyd rejects any negative cycle. Prim/Kruskal
  return spanning **forests**. Matrix Edmonds-Karp coalesces parallel capacities
  and exposes an antisymmetric signed net-flow matrix. Its matrix BFS gives a
  conservative O(V³E) worst-case time bound and O(V²) storage.
- Geometry inputs and intermediate results must be finite. Orientation and
  intersection use absolute tolerance 1e-9, which is sensitive to coordinate
  scale. A line needs two distinct points; parallel or coincident lines have no
  unique intersection and return `null`. Hulls exclude interior collinear points.
  Ear clipping accepts either orientation of a simple, nondegenerate polygon;
  invalid boundaries fail explicitly. Convex triangulation minimizes the sum of
  triangle perimeters and requires strict convexity. Packing compares only the
  demonstrated grid/hexagonal arrangements, checking both box orientations.
  Superman implements the original independent chord/arc calculation for
  disjoint circles with endpoints outside; it is not a general shortest-path
  solver and rejects unsupported overlapping/partial obstacles.
- `backtrack` gives callbacks immutable prefix snapshots. Candidate values must
  be nonnull. Every completed `makeMove` is paired with `unmakeMove`, including
  early stop and exceptions from descendants. `processSolution` returning false
  stops the whole traversal. DFS, SCC, BST, and recursive teaching variants use
  the Java call stack, so exceptionally deep inputs can exhaust it.
- Enumeration limits are 9 permutation elements, 20 subset elements, and 15 queens;
  runtime/output size still grows exponentially. Sudoku validates all givens;
  contradiction is an error, unsatisfiability returns `null`. Its default is
  most-constrained-first; `sudoku(puzzle, false)` demonstrates row-first search.
- Exact TSP supports 0..12 cities with DFS or best-first branch-and-bound and an
  admissible remaining-MST bound. Best-first frontier capacity is 1000000 and
  exhaustion is an explicit error. Heuristics retain the best complete tour;
  hill climbing accepts strict improvements in a recomputed objective, and
  annealing may temporarily accept worse tours. Each proposal is O(n).
  `repeatedTsp` returns the best among seeds `seed`, `seed+1`, …, with Java signed
  overflow wrapping the seed sequence. Heuristics provide no optimality guarantee.
- Seeded random results are reproducible within Java; random sequences are not
  required to match the C++ or Python generators. Integer intervals are inclusive;
  real intervals are [low, high), with equal endpoints returning that endpoint.
- War uses ranks `23456789TJQKA`, suits `cdhs`, distinct cards across both decks,
  and one face-down pair after every tied comparison. Steps count paired draws.
  An exhausted tie pot or a step limit with both decks nonempty yields a draw.
