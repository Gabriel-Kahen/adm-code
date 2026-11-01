# Algorithm Design Manual programs

Small, standalone implementations from Steven S. Skiena's *The Algorithm Design
Manual* and *Programming Challenges*. Use them to study an algorithm, inspect its
invariants, and experiment with small inputs.

Start with the C programs in the repository root. Historical implementations and
unfinished experiments are kept separately for reference.

## Build and run

You need a C99 compiler and GNU Make. GCC is the default; Clang is also checked in CI.

```sh
make -j2 all
printf '3 2\n1 2 1\n2 3 1\n' | ./dijkstra
printf '3 3\n10 1 1\n' | ./partition
printf 'kitten\nsitting\n' | ./stringedit
```

The Dijkstra example prints a shortest-path tree with total edge weight **2**.
The partition example produces three nonempty singleton groups. The edit-distance
example reports cost **3**, followed by its tables and operation trace.

Build one program with `make dijkstra`. To switch compilers, rebuild the objects:

```sh
make clean
make -j2 all CC=clang
```

These are instructional command-line demos: most read whitespace-separated input
from standard input and print explanatory output. See the [algorithm and input
guide](docs/ALGORITHMS.md) before choosing an input, especially for graph
orientation, geometry, and fixed-size arrays.

## Find an algorithm

| Topic | Good starting points |
|---|---|
| Graph traversal and structure | [BFS/DFS](bfs-dfs.c), [components](connected.c), [strong components](strong.c), [articulation vertices](biconnected.c) |
| Weighted graphs | [Dijkstra](dijkstra.c), [Prim](prim.c), [Kruskal](kruskal.c), [Floyd–Warshall](floyd.c), [maximum flow](netflow.c) |
| Dynamic programming | [edit distance](editdistance.c), [partitioning](partition.c), [subset sum](subsetsum.c), [elevator stops](elevator.c) |
| Backtracking | [queens](8-queens.c), [permutations](permutations.c), [paths](paths.c), [Sudoku](sudoku.c) |
| Sorting and containers | [sorting](sorting.c), [heap](priority_queue.c), [list](list-demo.c), [tree](tree-demo.c), [union-find](set_union.c) |
| Geometry | [primitives](geometry.c), [convex hull](convex-hull.c), [triangulation](triangulate.c), [disk packing](plates.c) |
| Numbers and sequences | [bignums](bignum.c), [binomial coefficients](binomial.c), [GCD](gcd.c), [convolution](convolve.c), [Fibonacci](fib.c) |
| Traveling salesperson | [exact search](tsp-astar.c), [sampling/hill climbing/annealing](annealing.c) |

The [guide](docs/ALGORITHMS.md) lists the other demos and their shared conventions.

## Tests and maintenance

```sh
make test
# The historical entry point runs the same supported suite:
./test-script.sh
```

The suite needs Python 3.10 or newer, GCC, Clang, and their sanitizer runtimes. It compiles the
actual C implementations and checks counterexamples, boundaries, invariants, and
independent reference results. [Testing](docs/TESTING.md) explains how to select a
suite, understand sanitizer output, and add a useful regression.

[Contributing](CONTRIBUTING.md) covers the readability conventions, pinned formatters,
and generated excerpts. Run `make check` before submitting a change. Fix provenance
and upstream issue links are recorded in [AUDIT_FIXES.md](AUDIT_FIXES.md).

## Repository layout

| Location | Purpose |
|---|---|
| Root `*.c` and `*.h` | Current educational programs and shared implementations |
| `tests/` | Supported automated tests and their C compilation helpers |
| `datafiles/` | Sample inputs and archived outputs; some historical source examples |
| `code-fragments/` | Saved book excerpts, mostly generated from marked source blocks |
| `original/` | Earlier implementations, including legacy C interfaces |
| `tmp/`, `plot/` | Historical experiments, debug material, and plotting notebooks |
| `docs/` | Input/contracts guide, testing guide, and preserved distribution notes |

`make all` builds the root C demos. It does not build every historical draft or the
C++, Java, Pascal, Wolfram, and notebook examples. Historical output snapshots are
reference material; corrected tests use explicit mathematical expectations and
invariants rather than treating those snapshots as a correctness oracle.

Generated objects and executables are excluded from Git. The imported archive is
recoverable from commit `f74a015406c0821aa23390e3983d2c385712e3f4`. The previous
README and file catalog are preserved [verbatim](docs/ARCHIVE_README.txt).

## Permission notice

The original notice is retained without changing its wording:

```text
Copyright 2003-2020 by Steven S. Skiena; all rights reserved. 
Permission is granted for use in non-commerical applications
provided this copyright notice remains intact and unchanged.
```

This repository does not replace that notice with a different license. Preserve
copyright and permission text in source files when making changes.
