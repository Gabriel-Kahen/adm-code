# Audit fixes and upstream tracking

All **50 numbered findings** from the source audit of import `f74a015406c0821aa23390e3983d2c385712e3f4` have a separate merged fix PR in this private repository. Affected current, historical, and fragment copies are included where applicable. Each finding has an actual-C regression and a receipt under `audit/fixes/`.

The upstream issue inventory includes all open and closed issues checked on October 31, 2026. Matching or overlapping upstream reports exist for **C09 (#9), G10 (#8), and G14 (#6)**. No matching upstream issue was found for the other **47 numbered findings**. The Dijkstra issue is a related discussion of its returned weight; our fix specifically makes the displayed shortest-path-tree edge total match the chosen parent edges. This status describes upstream tracking, not whether an upstream fix has merged.

## Numbered findings

| Audit ID | Finding | Merged private fix PR | Upstream issue |
|---|---|---|---|
| C01 | TSP floating-point pruning can discard the entire exact search | [#9](https://github.com/Gabriel-Kahen/adm-code/pull/9) | None found |
| C02 | TSP branch-and-bound extracts from an empty queue | [#14](https://github.com/Gabriel-Kahen/adm-code/pull/14); capacity guard [#52](https://github.com/Gabriel-Kahen/adm-code/pull/52) | None found |
| C03 | Exact TSP can print an empty or stale incumbent tour | [#15](https://github.com/Gabriel-Kahen/adm-code/pull/15) | None found |
| C04 | Exact TSP overruns two arrays at its advertised 20-city limit | [#16](https://github.com/Gabriel-Kahen/adm-code/pull/16) | None found |
| C05 | Corrected hill climbing can still cycle forever through roundoff | [#25](https://github.com/Gabriel-Kahen/adm-code/pull/25); strict-descent follow-up [#51](https://github.com/Gabriel-Kahen/adm-code/pull/51) | None found |
| C06 | Deleting a duplicate tree key recurses into the same node indefinitely | [#26](https://github.com/Gabriel-Kahen/adm-code/pull/26) | None found |
| C07 | War compares ASCII characters instead of card ranks | [#36](https://github.com/Gabriel-Kahen/adm-code/pull/36) | None found |
| C08 | Name replacement reprocesses its own inserted text | [#37](https://github.com/Gabriel-Kahen/adm-code/pull/37) | None found |
| C09 | The archive still distributes the originally reported reversed hill loop | [#1](https://github.com/Gabriel-Kahen/adm-code/pull/1) | [#9](https://github.com/SkienaBook/Algorithm-Design-Manual-Programs-V3/issues/9) |
| G01 | Tarjan SCC reads before `low[]` on every DFS root (high) | [#2](https://github.com/Gabriel-Kahen/adm-code/pull/2) | None found |
| G02 | Kruskal's edge array is sized by vertices, not edges (high) | [#3](https://github.com/Gabriel-Kahen/adm-code/pull/3) | None found |
| G03 | Path enumeration consults the nonexistent element `a[0]` (high) | [#10](https://github.com/Gabriel-Kahen/adm-code/pull/10) | None found |
| G04 | Path enumeration overflows its solution vector at the advertised maximum (high) | [#11](https://github.com/Gabriel-Kahen/adm-code/pull/11) | None found |
| G05 | Max-flow initialization skips vertex 100 (high) | [#12](https://github.com/Gabriel-Kahen/adm-code/pull/12) | None found |
| G06 | Max flow undercounts parallel edges (high) | [#13](https://github.com/Gabriel-Kahen/adm-code/pull/13) | None found |
| G07 | Floyd–Warshall computes positive self-distances (medium) | [#20](https://github.com/Gabriel-Kahen/adm-code/pull/20) | None found |
| G08 | Floyd–Warshall invents reachability with negative edges (medium) | [#21](https://github.com/Gabriel-Kahen/adm-code/pull/21) | None found |
| G09 | Finite "infinity" silently clips valid weighted inputs (medium) | [#30](https://github.com/Gabriel-Kahen/adm-code/pull/30) | None found |
| G10 | Deleting a non-head adjacency entry discards preceding edges (medium; already upstream issue #8) | [#31](https://github.com/Gabriel-Kahen/adm-code/pull/31) | [#8](https://github.com/SkienaBook/Algorithm-Design-Manual-Programs-V3/issues/8) |
| G11 | Reverse augmentations do not cancel stored edge flow (medium) | [#32](https://github.com/Gabriel-Kahen/adm-code/pull/32) | None found |
| G12 | Floyd matrix input overwrites cheaper parallel edges (medium; multigraph input) | [#33](https://github.com/Gabriel-Kahen/adm-code/pull/33) | None found |
| G13 | Path reconstruction fabricates a path to unreachable vertices (medium) | [#45](https://github.com/Gabriel-Kahen/adm-code/pull/45) | None found |
| G14 | Dijkstra labels sum of distances as SPST edge weight (medium; already upstream issue #6) | [#46](https://github.com/Gabriel-Kahen/adm-code/pull/46) | [#6](https://github.com/SkienaBook/Algorithm-Design-Manual-Programs-V3/issues/6) |
| G15 | Bipartiteness misses self-loops (medium; graphs with loops) | [#47](https://github.com/Gabriel-Kahen/adm-code/pull/47) | None found |
| G16 | DFS-based edge count loses parallel parent edges (medium; multigraph input) | [#48](https://github.com/Gabriel-Kahen/adm-code/pull/48) | None found |
| G17 | Historical traversal/weighted/topological arrays are one entry too small (high at MAXV) | [#49](https://github.com/Gabriel-Kahen/adm-code/pull/49) | None found |
| G18 | Historical max-flow sums the wrong adjacency bound (high) | [#50](https://github.com/Gabriel-Kahen/adm-code/pull/50) | None found |
| GN01 | Extended GCD loses exact integer arithmetic [P2] | [#4](https://github.com/Gabriel-Kahen/adm-code/pull/4) | None found |
| GN02 | Segment intersection rejects shared endpoints [P2] | [#5](https://github.com/Gabriel-Kahen/adm-code/pull/5) | None found |
| GN03 | Convex hull loses the far endpoint of collinear sets [P2] | [#6](https://github.com/Gabriel-Kahen/adm-code/pull/6) | None found |
| GN04 | Convex hull exceeds its documented maximum-size buffer [P2, capacity] | [#17](https://github.com/Gabriel-Kahen/adm-code/pull/17) | None found |
| GN05 | Convolution output is undersized for allowed inputs [P2, capacity] | [#18](https://github.com/Gabriel-Kahen/adm-code/pull/18) | None found |
| GN06 | Bignum addition corrupts a representable 100-digit result [P2, capacity] | [#19](https://github.com/Gabriel-Kahen/adm-code/pull/19) | None found |
| GN07 | Distance squares overflow before conversion to double [P2, numeric range] | [#38](https://github.com/Gabriel-Kahen/adm-code/pull/38) | None found |
| GN08 | Bignum conversion cannot handle INT_MIN [P2, numeric range] | [#27](https://github.com/Gabriel-Kahen/adm-code/pull/27) | None found |
| GN09 | Disk packing can return a negative number of disks [P2] | [#28](https://github.com/Gabriel-Kahen/adm-code/pull/28) | None found |
| GN10 | Superman's circle array is off by one [P2, capacity] | [#29](https://github.com/Gabriel-Kahen/adm-code/pull/29) | None found |
| GN11 | Legacy convex hull can pop below an empty stack [P2, legacy only] | [#39](https://github.com/Gabriel-Kahen/adm-code/pull/39) | None found |
| GN12 | Legacy binomial table's inclusive loop overruns its dimensions [P2, legacy/capacity] | [#40](https://github.com/Gabriel-Kahen/adm-code/pull/40) | None found |
| GN13 | Binomial's declared n<=100 range exceeds its computation's arithmetic range [P2, numeric range] | [#41](https://github.com/Gabriel-Kahen/adm-code/pull/41) | None found |
| DP-01 | P1: brute-force edit-distance executable reconstructs nonexistent parent pointers | [#7](https://github.com/Gabriel-Kahen/adm-code/pull/7) | None found |
| DP-02 | P2: partition reconstruction can enter an impossible state on small valid inputs | [#8](https://github.com/Gabriel-Kahen/adm-code/pull/8) | None found |
| DP-03 | P2: Sudoku candidate counting reads an uninitialized boolean | [#23](https://github.com/Gabriel-Kahen/adm-code/pull/23) | None found |
| DP-04 | P2: diagonal grid traversal emits extra and out-of-range cells | [#22](https://github.com/Gabriel-Kahen/adm-code/pull/22) | None found |
| DP-05 | P2: finite “infinity” leaves partition dividers unset for valid integer weights | [#24](https://github.com/Gabriel-Kahen/adm-code/pull/24) | None found |
| DP-06 | P2: the advertised 50-rider elevator capacity overflows its stop array | [#34](https://github.com/Gabriel-Kahen/adm-code/pull/34) | None found |
| DP-07 | P2: string comparison drivers overflow below the documented maximum length | [#35](https://github.com/Gabriel-Kahen/adm-code/pull/35) | None found |
| DP-08 | P2: backtracking examples cannot hold the declared maximum solution size | [#42](https://github.com/Gabriel-Kahen/adm-code/pull/42) | None found |
| DP-09 | P2, legacy only: original approximate substring implementation has incompatible callbacks | [#43](https://github.com/Gabriel-Kahen/adm-code/pull/43) | None found |
| DP-10 | P3, debug files only: subset-sum traces print an uninitialized element | [#44](https://github.com/Gabriel-Kahen/adm-code/pull/44) | None found |

## Supporting corrections

- [C05-STRICT: Preserve strict hill-climbing improvements without roundoff cycles](https://github.com/Gabriel-Kahen/adm-code/pull/51).
- [C02QUEUE: Fail explicitly when exact TSP exhausts its queue capacity](https://github.com/Gabriel-Kahen/adm-code/pull/52).
- [C10: Preserve signed three-way sorting comparator results](https://github.com/Gabriel-Kahen/adm-code/pull/53).
- [BUILD01: Build with modern GCC/Clang and propagate regression failures](https://github.com/Gabriel-Kahen/adm-code/pull/54).
- [CICOMPAT: Compile legacy regression callers on both Clang 18 and Clang 22](https://github.com/Gabriel-Kahen/adm-code/pull/55).

The source-only checkout cleanup accompanying this index removes 118 obsolete compiled files from the archive. They remain recoverable from the original import commit. Source, data, images, notebooks, and copyright notices are retained. Generated program/object files are ignored so a fresh build uses the corrected source.

## Build and verify

```sh
make -j2 all
make test
# To build every current program with Clang instead:
make clean
make CC=clang -j2 all
```

`make test` and `./test-script.sh` run the corrected invariant/oracle and sanitizer regressions. Historical golden-output data is retained as archive material; it is not blindly regenerated from changed program output. GitHub Actions builds current sources with both GCC and Clang and runs the regression suite.

Hill climbing now recomputes the tour objective after a proposed swap and accepts strict decreases. This costs O(n) per proposed swap, provides finite-state descent, and preserves real small improvements that a global epsilon threshold discarded. Exact TSP reports queue-capacity exhaustion explicitly rather than silently losing search states and claiming optimality. Numeric operations that exceed their fixed representation fail explicitly where the audit identified silent corruption.

Finite regression/oracle checks establish the documented cases and domains. Historical incomplete drafts received fixes for their listed defects; the audit did not supply missing specifications for unfinished algorithms.
