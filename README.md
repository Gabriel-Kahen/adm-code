# Algorithm Design Manual programs

The corrected C programs and direct C++17, Java 17, and Python 3.10+ translations.
The reference is the current `c/` directory, including the fixes in [FIXES.md](FIXES.md).
This translation work does not change the C sources.

Each of the 66 C implementation files has a matching counterpart. Names follow
the C files, with Java class naming and Python underscores; `10055` becomes
`P10055`/`p10055`, and `8-queens` becomes `EightQueens`/`eight_queens`.

The translations retain the C algorithms, auxiliary structures, capacities,
indices, sentinels, loop order, tie breaking, and demonstrations. In particular:

- Graphs retain explicit edge nodes or adjacency arrays. Traversals use the
  original queue, stack, parent, discovery, and timestamp arrays.
- Dijkstra and Prim retain their array scans, rather than using a library heap.
- Queue/stack/heap/union-find routines retain their arrays and state fields.
  Union-find does not add path compression.
- Bignums retain the digit array, sign, and last-digit index. Dynamic programming
  retains its tables and reconstruction; backtracking retains its candidates
  and make/unmake steps.
- The hand-written sorting algorithms remain hand-written. Library sorting is
  used only at the C sources' own `qsort` call sites.

Language-required changes, such as references instead of C pointers, scalar
out-parameters, Java classes, and input/output adapters, do not replace the
teaching algorithms. The original comments and copyright notices remain.
Use native operators, initialization, math, and library calls when they express
the same operation directly. `java/C.java` and `python/_c.py` retain adapters
where C behavior needs translation, such as streaming input, NUL-terminated
buffers, output parameters, and struct value copies. Algorithms remain in their
matching files.

## Build and run

Use GNU Make, a C99 compiler, a C++17 compiler, JDK 17+, and Python 3.10+.
No third-party packages are needed.

```sh
make -j4 all
printf '3 2\n1 2 2\n2 3 2\n' | ./c/dijkstra
printf '3 2\n1 2 2\n2 3 2\n' | ./build/cpp/dijkstra
printf '3 2\n1 2 2\n2 3 2\n' | java -cp build/java Dijkstra
printf '3 2\n1 2 2\n2 3 2\n' | python3 python/dijkstra.py
```

The demos use the C input format and print its teaching traces, including the
one-based vertex labels. Shared library files have no standalone demo.
Traversal/edit examples install their matching callbacks in the demo entry
point; the shared routines expect those hooks, just as C expects them at link time.
Build just C++ with `make cpp`, Java with `make java`, or a single C++ demo
with `make -C cpp ../build/cpp/dijkstra`. Override `CC`, `CXX`, `CXXFLAGS`,
`JAVAC`, `JAVA`, or `PYTHON` to select tools. `make clean` removes builds.

## Verification and limits

`make test` compiles every implementation and compares all 53 demo programs with
C on identical inputs, including stdout, stderr, and exit status. A console
check verifies line-by-line input without waiting for EOF. Additional cases
exercise insertion/traversal order, ties, disconnected graphs, parallel
edges, self-loops, wide weights, signed arithmetic, edit reconstruction, and
other recorded fixes. Auxiliary-state tests inspect queue wraparound, stack
state, heap layout, union-find parent chains, linked graph deletion, and TSP
record copies at queue insertion, inspection, and extraction.

These are translations, not a new API or an opportunity to repair remaining C
limitations. Use the C input domains and preconditions. Python has unbounded
integers and different string semantics; Java uses fixed-width integers and
UTF-16 strings. ASCII and values representable in the corresponding C types
are the common comparison domain. Floating-point library rounding can vary.
The parity checks use Linux's 32-bit `int` and 64-bit `long` C build.
The random-number primitive is runtime-specific; sampling, permutation,
hill-climbing, and annealing retain the C algorithms. General stochastic traces
are not expected to be identical across runtimes.

## Permission

The original [COPYRIGHT](COPYRIGHT) and source notices are retained unchanged.
Permission is granted for use in non-commerical applications provided the
copyright notice remains intact and unchanged. This repository does not replace
that permission notice with a different license.
