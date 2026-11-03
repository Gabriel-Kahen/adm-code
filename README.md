# Algorithm Design Manual programs

The corrected C programs and their direct C++, Java, and Python counterparts.
Each language folder follows the original source filenames. Shared algorithms
stay in their own matching files; each demonstration has a small local entry
point. There is no shared command router or application framework.

```text
c/dijkstra.c       cpp/dijkstra.cpp
java/Dijkstra.java python/dijkstra.py

c/graph.c          cpp/graph.cpp
java/Graph.java    python/graph.py
```

All **66 original C implementation files** have counterparts in the other three
languages. The 22 C headers are retained. C++ uses normal shared headers; Java
uses class names such as `BfsDfs`, and Python uses underscores such as `bfs_dfs`.
The two leading-number names become `P10055` / `p10055` and `EightQueens` /
`eight_queens` in Java / Python. The C sources retain the previous bug fixes, recorded in [FIXES.md](FIXES.md).

## Build and run

Use GNU Make, a C99 compiler, a C++17 compiler, JDK 17+, and Python 3.10+.
No third-party libraries or package installation are needed.

```sh
make -j2 all
printf '3 2\n1 2 2\n2 3 2\n' | ./c/dijkstra
printf '3 2\n1 2 2\n2 3 2\n' | ./build/cpp/dijkstra
printf '3 2\n1 2 2\n2 3 2\n' | java -cp build/java Dijkstra
printf '3 2\n1 2 2\n2 3 2\n' | python3 python/dijkstra.py
```

The ports report distances **0, 2, 4**. The C demo prints its teaching trace and
shortest-path tree. Graph readers accept the original vertex labels **1..n**;
the new algorithms use **0..n-1** internally. Native demonstrations have compact
output or fixed examples; they do not reproduce every C diagnostic or stdin
driver. Read the small `main()` / `if __name__` block for each example's input.
The functions in the same file can be called directly with custom data.

Build a single C program with `make -C c dijkstra`, or a C++ program with
`make build/cpp/dijkstra`. A minimal standalone C++ build is:

```sh
g++ -std=c++17 -DADM_DEMO cpp/dijkstra.cpp cpp/graph.cpp cpp/wgraph.cpp -o dijkstra
```

Use `make clean` to remove generated programs. Override `CC`, `CXX`, `CXXFLAGS`,
`JAVAC`, `JAVA`, or `PYTHON` to select tools. If a JDK is outside PATH, set `JAVAC`
and `JAVA` to its executable paths.

## Correctness

Run `make test` for native C++, Java, and Python invariant/oracle tests, a fresh C
build, per-file C++ compilation, and checks of the source correspondence. Tests
cover containers, graph mutation, flow conservation, sorting, DP witnesses,
backtracking undo, geometry boundaries, Sudoku, and exact TSP versus exhaustive
tours. Algorithms are in their matching source files, not inside the tests.

The ports preserve the documented mathematical contracts: invalid domains raise
errors; unreachable distances have no numeric sentinel; integer routines use
exact big integers or checked 64-bit intermediates in C++/Java. Python integers
are unbounded. Geometry uses finite floating-point values and an absolute 1e-9
tolerance, not exact predicates. Strings count bytes in C++, UTF-16 units in Java,
and code points in Python; ASCII is the common domain. Exact search is practical
only for small inputs. TSP heuristics, disk packing, and the Superman chord/arc
model do not promise general optimality. These limits are also noted beside the
implementations. Passing finite tests is not a proof for arbitrary inputs.

Archived duplicates, generated excerpts, plotting notebooks, audit reports, and
old infrastructure have been removed from this working tree. They remain in Git
history; commit `357b45c` is the complete pre-trim version.

## Permission

The original [COPYRIGHT](COPYRIGHT) and source notices are retained unchanged.
Permission is granted for use in non-commerical applications provided the
copyright notice remains intact and unchanged. This repository does not replace
that permission notice with a different license.
