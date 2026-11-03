# Fixes to the original code

Concise index of the 50 audit findings and supporting corrections, including
historical copies. [Audit details](https://github.com/Gabriel-Kahen/adm-code/blob/357b45cd6c1dd48e9ca2b5bd23a7390c6b0e234d/AUDIT_FIXES.md) contain PRs, upstream links,
and tests; [receipts](https://github.com/Gabriel-Kahen/adm-code/tree/357b45cd6c1dd48e9ca2b5bd23a7390c6b0e234d/audit/fixes) retain individual records.

## Search, trees, and strings

- C01: Prevent floating-point pruning from discarding exact TSP searches.
- C02/C02QUEUE: Guard empty/full TSP queues; report incomplete searches explicitly.
- C03: Initialize and retain a valid incumbent TSP tour.
- C04: Fix TSP array overruns at 20 cities.
- C05/C05-STRICT: Prevent hill-climbing roundoff cycles using strict, recomputed descent.
- C06: Stop duplicate-key tree deletion from recursing indefinitely.
- C07: Compare War cards by rank, not ASCII value.
- C08: Stop name replacement from reprocessing its inserted text.
- C09: Correct reversed hill-climbing loop conditions in archived copies.
- C10: Preserve negative/zero/positive sorting comparator results.

## Graphs

- G01: Stop Tarjan SCC from indexing before `low[]` at DFS roots.
- G02: Size Kruskal's storage by edges, not vertices.
- G03: Stop path enumeration from reading uninitialized `a[0]`.
- G04: Size path solution vectors for their advertised maximum.
- G05: Initialize max-flow state for vertex 100.
- G06: Accumulate parallel-arc capacities in max flow.
- G07: Set Floyd–Warshall self-distances to zero.
- G08: Never add unreachable-distance sentinels to negative edge weights.
- G09: Stop finite infinity sentinels from clipping valid weighted inputs.
- G10: Preserve preceding adjacency entries when deleting an edge.
- G11: Cancel stored flow during reverse augmentations.
- G12: Retain the cheapest parallel edge in Floyd input.
- G13: Report unreachable vertices instead of fabricating paths.
- G14: Report Dijkstra tree-edge weight, not summed source distances.
- G15: Reject self-loops when checking bipartiteness.
- G16: Count parallel parent edges correctly during DFS.
- G17: Fix legacy traversal, weighted, and topological arrays at `MAXV`.
- G18: Use the correct legacy max-flow adjacency bound.

## Geometry and arithmetic

- GN01: Keep extended GCD calculations in exact integer arithmetic.
- GN02: Recognize shared endpoints in segment intersection.
- GN03: Retain the far endpoint of collinear convex hulls.
- GN04: Prevent maximum-size convex-hull buffer overruns.
- GN05: Allocate enough convolution output coefficients.
- GN06: Preserve representable 100-digit bignum sums.
- GN07: Convert coordinates before squaring to prevent integer overflow.
- GN08: Handle `INT_MIN` in bignum conversion.
- GN09: Return zero, never negative counts, for undersized disk packings.
- GN10: Fix Superman's circle-array capacity.
- GN11: Prevent legacy hull stack underflow.
- GN12: Fix inclusive-loop bounds in legacy binomial tables.
- GN13: Check binomial arithmetic overflow without rejecting representable results.

## Dynamic programming and backtracking

- DP-01: Populate parent pointers for brute-force edit-distance reconstruction.
- DP-02: Keep partition reconstruction in valid, nonempty states.
- DP-03: Initialize Sudoku candidate-counting state.
- DP-04: Emit each valid diagonal-grid cell exactly once.
- DP-05: Initialize partition dividers for large valid weights.
- DP-06: Support the advertised 50-rider elevator capacity.
- DP-07: Fit maximum-length strings and their sentinels/terminators.
- DP-08: Fit maximum-size backtracking solutions in their arrays.
- DP-09: Repair incompatible legacy substring-matching callbacks.
- DP-10: Stop subset-sum debug traces from printing uninitialized elements.

## Build and maintenance

- BUILD01: Modernize C declarations/linkage and propagate build/test failures.
- BUILD02: Remove 118 stale binaries/objects that could bypass corrected sources.
- FRAGMENTS01: Synchronize saved edit-distance reconstruction excerpts.
- CICOMPAT: Support legacy regression callers across Clang versions.
- CI02: Avoid package-mirror stalls and duplicate/superseded CI runs.
