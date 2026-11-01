# C++, Java, and Python implementations

The three libraries cover the algorithms in all 53 current C demos and their
shared modules. They also complete the minimum-weight convex-polygon triangulation
outlined in the archived `mwt.c` draft. Readable modules replace the C demos' global
state and fixed-size buffers. Each language implements the algorithms itself;
none invokes the C executables or another language at runtime.

## Start here

Install a C++17 compiler, JDK 17 or newer, and Python 3.10 or newer. No library or
package installation is required.

```sh
make ports
python3 tools/ports.py run cpp edit kitten sitting
python3 tools/ports.py run java edit kitten sitting
python3 tools/ports.py run python edit kitten sitting
make test-ports
```

Each edit command prints a JSON object with cost **3** and an operation trace.
The adapters accept arguments rather than the old demos' stdin formats. This
keeps the examples small and lets one test suite exercise all three libraries.
Libraries can also be imported/called directly; see the native API guides:

- [C++](../cpp/README.md), with declarations in `cpp/include/adm.hpp`.
- [Java](../java/README.md), with classes in package `adm`.
- [Python](../python/README.md), with modules in package `adm`.

Compiler outputs go to ignored `build/ports/` directories. Set `CXX`, `JAVAC`,
`JAVA`, or `JAVA_HOME` to select installed tools. `CXXFLAGS` and `PORTS_LDFLAGS`
control C++ compilation and linking. C++ and Java builds treat warnings as errors.

```sh
CXX=clang++ make test-ports
# Select languages during development; CI always checks all three.
PORT_LANGUAGES="java python" make test-ports
```

## Find an implementation

| Family | Includes |
|---|---|
| Containers | Queue, stack, binary min heap, union-find, singly linked list, binary search tree |
| Sorting | Insertion, selection, quick, heap, merge; first-occurrence binary search; sorted insertion |
| Numeric | Exact bignum arithmetic, four Fibonacci versions, binomial DP, extended GCD, factors, distance, matrices, convolution, seeded randomness |
| Graphs | Mutable multigraph, BFS/DFS, paths, components, coloring, cycles, articulation points, both SCC and topological algorithms, both spanning forests, shortest paths, maximum flow |
| Dynamic programming | Edit distance and trace, brute recurrence, LCS, substring matching, partition and subset-sum witnesses, elevator stops |
| Geometry | Lines, segments, predicates, projections, areas, hull, ear clipping, convex triangulation DP, disk packings and coordinate conversions, chord/arc obstacle model |
| Search | Callback backtracking, subsets, permutations, queens, simple paths, Sudoku, exact TSP with DFS and best-first bounds, sampling, hill climbing, annealing |
| Demos | Grid traversal orders, substring search/replacement, suitor ordering, card conversion and War |

The machine-readable [coverage inventory](PORT_COVERAGE.json) maps each of the 88
current C sources and headers to its implementations. The inventory test prevents
new C sources from silently missing a port entry. It establishes the documented
mapping; mathematical tests establish behavior on their tested inputs.

`original/`, `tmp/`, and generated book excerpts often repeat the same algorithm.
Their algorithms map to the corresponding maintained family, including different
sorting, SCC, topological, Fibonacci, and TSP methods. Archived broken interfaces,
debug traces, and unfinished representations are preserved as historical sources.
Build/excerpt tools and plotting notebooks keep their original languages; they
are maintenance and visualization material rather than additional algorithm ports.

## Common contracts

- Vertices, array positions, tour entries, witness indices, and grid coordinates
  are **zero-based**. This differs from many original C interfaces.
- Invalid mathematical domains raise a native exception. The adapters print a
  diagnostic to stderr and exit nonzero. Unreachable shortest-path distances and
  absent witnesses use JSON `null`, without numeric infinity sentinels.
- Bignums, Fibonacci, and binomial coefficients have arbitrary precision. Their
  adapter results are decimal **strings**, including small values. C++ supplies
  a decimal big-integer implementation; Java uses `BigInteger`; Python uses `int`.
- Other integral arithmetic uses checked signed 64-bit values in C++ and Java.
  Python integers remain unbounded. Cross-language equivalence for these APIs
  requires intermediate and final values within signed 64-bit range. A native
  library may document a narrower index or practical search bound.
- Floating-point coordinates must be finite. Predicates use a documented absolute
  tolerance, generally `1e-9`; they are not exact geometric predicates. Tests use
  well-separated coordinates and numerical tolerances.
- Cross-language string examples use ASCII, including spaces and empty strings.
  Outside ASCII, C++ counts bytes, Java UTF-16 code units, and Python Unicode code
  points. Character indices and edit costs can therefore differ.
- Ties may produce different valid paths, partitions, or edit traces. Tests check
  the objective and witness. A random seed reproduces a run within one language;
  random generators are not synchronized across languages.

Read [the adapter protocol](PORT_PROTOCOL.md) for every operation and the native
guides for callable functions. Heuristics return feasible tours and their measured
costs; only exact TSP methods claim optimality. Disk packing compares specified
lattice arrangements. Superman retains the book's restricted chord/arc model.

## Correctness checks

`make test-ports` compiles both compiled languages, runs each library's native
invariant checks, and executes shared deterministic tests against independent
reference calculations. It checks all five sorts, exact large integers, edit
traces, exhaustive DP optima, graph structure with parallel/self edges, both SCC,
topological and forest variants, shortest paths against Bellman–Ford, flows
against all cuts, and exact TSP against all tours. Geometry checks include invalid
polygons, triangle coverage and exhaustive convex triangulation splits. Search
tests validate Sudoku rows/columns/boxes and known queens counts.

Native tests cover containers, mutation, random generators, backtracking undo,
and other APIs without a shared adapter operation. These checks provide useful
evidence, not a proof for arbitrary inputs. Exhaustive algorithms remain practical
only for small instances; recursive implementations also use the language stack.

`make test` includes the existing C regression and algorithm suites as well as the
new ports. `make test-c` runs the original maintained suites alone. CI checks C
with GCC and Clang, all three libraries together, and C++ again with Clang's
address and undefined-behavior sanitizers, including leak detection.
