# Fixes and counterexamples

Each row gives a concrete input/state, the previous failure, and the corrected
result. Indices are one-based unless stated otherwise; `×k` means repeat k times.
ASan/UBSan/MSan reports below are observed invalid accesses, arithmetic, or
uninitialized reads—not promises of a particular result after undefined behavior.
Numeric examples use Linux 32-bit `int` and 64-bit `long`. Command sequences use
`;` for newline; point lists describe API instances rather than literal stdin.

“Original” means import [`f74a015`](https://github.com/Gabriel-Kahen/adm-code/tree/f74a015406c0821aa23390e3983d2c385712e3f4).
Historical paths refer to that tree; retained sources now live under `c/`.
Follow-up/tooling cases identify their own earlier version. Fix PRs and regression
callers remain in the [audit index](https://github.com/Gabriel-Kahen/adm-code/blob/357b45cd6c1dd48e9ca2b5bd23a7390c6b0e234d/AUDIT_FIXES.md)
and [tests](https://github.com/Gabriel-Kahen/adm-code/tree/357b45cd6c1dd48e9ca2b5bd23a7390c6b0e234d/tests/regressions).

## Search, trees, and strings

| ID | Counterexample | Before → correct result |
|---|---|---|
| C01 | Exact TSP: cities `(2,8),(8,10),(7,6),(1,9)` in that order. | Returns **18.570078440826883** without exploring a tour → **17.993551806990734**, e.g. tour `1,4,2,3` (checked against all six anchored tours). |
| C02 | TSP branch-and-bound: `(0,9),(4,5),(6,7),(5,0)`. | The frontier empties, but another extraction reads queue index **−1** (UBSan) → terminate normally with cost **24.1514968952874**. |
| C03 | Exact TSP: triangle `(0,0),(1,0),(0,1)`; initial tour is already optimal. | Reports cost **3.414213562373095** with saved-tour length **0** → retain a valid **3-city tour**, including when no strict improvement exists. |
| C04 | 20 cities `(i,0)`, `i=1..20`; initialize lower bounds, then request candidates after city 1. | Writes `lb[20]` and reads `in_perm[20]` in length-20 arrays (ASan/UBSan) → both maps include index 20 and return 19 candidates. |
| C05 | Hill climbing: `(29,76),(40,84),(18,19),(8,23)`, `srand(0)` on the checked Linux C library. | Cycles through equal-edge tours with reported delta **−2.8421709430404007e−14** → recomputed strict descent terminates. The repeated cycle is shown below. |
| C06 | Tree commands: `i 1; i 1; d 1; p`. | Deleting one duplicate recurses into the same root until stack overflow (ASan) → exactly one `1` remains. |
| C07 | War: deck A=`Ah`, deck B=`Kh`. | Prints **b wins**, because ASCII `A<K` → **a wins**, because ace outranks king. |
| C08 | Rename `"ACME" → "ACME Corp"`; input line `ACME`. | Repeatedly matches `ACME` inside its own replacement and overflows the buffer (ASan) → **`ACME Corp`** once. The no-op rename `ACME → ACME` instead loops without growth. |
| C09 | Archived `datafiles/tsp-examples/annealing.c`: two coincident cities `(0,0),(0,0)`; every swap has delta 0. | `stuck` stays true, so the reversed loop repeats the unchanged pass → return after **one pair evaluation**. The saved hill-climbing fragment has the same defect. |
| C10 | Call `sorting.c` comparator on `(1,2)`, `(2,1)`, `(1,1)`. | Returns **1,1,0** because its `bool` return converts −1 to 1 → three-way signs **−1,1,0**. This helper was unused by the sorting demos. |

C05's observed cycle (closed tours) was:

```text
4 1 2 3 → 2 1 4 3 → 2 3 4 1 → 4 3 2 1 → 4 1 2 3
```

Every tour uses exactly the same undirected edges `{1–2,2–3,3–4,4–1}`;
accepting these rounded negative deltas does not establish a real improvement.
The observation wrapper recorded the cycle without changing `transition`.

## Graphs

| ID | Counterexample | Before → correct result |
|---|---|---|
| G01 | `strong.c`: one vertex, no edges (`1 0`). | DFS root has `parent[1]=-1`; UBSan reports `low[-1]`. After: SCC `{1}`, no invalid access. |
| G02 | `kruskal.c`: complete undirected graph on 15 vertices, all 105 edges weight 1. | ASan reports overflowing the 101-entry edge array. After: MST weight 14. |
| G03 | `paths.c`: edge 1–2, source 1, target 2; initialize the unused slot `a[0]=2`. | Prints `{ }` as a solution. After: `{ 1 2 }`. Unused slot zero is outside the 1-based solution and must not determine whether it is complete. |
| G04 | `paths.c` driver: chain 1–2–…–100. | ASan reports writing past the driver's 100-entry solution array at `a[100]`. After: full 100-vertex path, no overflow. The replay zero-initializes automatic variables in both builds so G03 cannot mask this defect. |
| G05 | `netflow.c`: fill a `flow_graph` with byte `0x55`, then call `initialize_graph`. | `degree[100]` remains 1431655765. After: it is 0 and `edges[100]=NULL`, like every other vertex slot. |
| G06 | `netflow.c`: source 1, sink 2; two arcs `(1,2,1)`. | Reports total flow 1. After: 2, matching the capacity of the only source/sink cut. |
| G07 | `floyd.c`: one vertex, no edges (`1 0`). | `d(1,1)=100007`. After: 0, the cost of the empty path. |
| G08 | Directed `floyd.c`: 3 vertices; only arc `(2,3,-5)`. | Says 1 reaches 3 (`100007-5` became a finite distance). After: 1→3 remains unreachable; 2→3 costs −5. |
| G09 | Dijkstra: 2 vertices, edge `(1,2,100007)`. Also test Prim/Floyd/Kruskal on chain `(1,2,2147483647),(2,3,2147483647)`. | Dijkstra leaves `parent[2]=-1`; Prim leaves both parents unset; Floyd/Kruskal trigger signed-int-overflow UBSan. After: vertex 2 is reachable, both forest edges are selected, and the chain/MST cost is 4294967294. |
| G10 | `graph.c`: insert 1→2, 1→3, 1→4 (list `[4,3,2]`), then delete 1→3. | Remaining list is `[2]`, losing 1→4. After: `[4,2]`. |
| G11 | `netflow.c`, source 1, sink 6: unit arcs `1→3,1→2,2→5,2→4,3→4,4→6,5→6` in that order. | After rerouting, both stored `flow(2,4)` and `flow(4,2)` equal 1; forward residual is also 1 with capacity 1, violating `residual=capacity-flow` and antisymmetry. After: both net flows are 0; residual(2,4)=1. |
| G12 | Directed `floyd.c`: arcs `(1,2,1)` then `(1,2,9)`. | `d(1,2)=9`. After: 1, the cheaper available edge. |
| G13 | `wgraph.c`: parents `[-1,-1,1,-1]`; call `find_path(1,3,parents)`. | Prints fabricated path `1 3`, despite vertex 3 having no parent. After: `No path`. |
| G14 | `dijkstra.c`: unit-weight chain 1–2–3. | Labels 3 as the tree-edge total (summing distances 1+2). After: 2, the sum of its two unit edges. |
| G15 | `bipartite.c`: one vertex with self-loop (`1 1`, edge `1 1`). | Reports bipartite=true. After: false; a vertex cannot have a color different from itself. |
| G16 | `countedges.c`: two vertices joined by two parallel edges. | Reports `nedges=1`. After: 2. |
| G17 | Legacy `original/`: run BFS, Dijkstra, Prim and topological sort on chain 1–2–…–100 (unit weighted where required); run max flow on `(1,100,1)`. Also send unit arcs `i→52` for `i=1..51`. | UBSan/ASan finds index 100 in length-100 traversal/weighted/flow/topological arrays. The 52-vertex case separately overflows the 50-entry residual-neighbor row when 51 reverse arcs are inserted. After: `parent[100]=99`, topological order 1..100, unit flow to vertex 100, and sink 52 has 51 residual neighbors without overflow. |
| G18 | Legacy `original/netflow.c`: source 1, sink 2; 51 vertices, no arcs (`1 2`, then `51 0`). | Final summation loops over 51 vertices rather than 0 source adjacencies; UBSan reports reading `edges[1][50]` beyond the 50-entry row. After: total flow 0. |

## Geometry and arithmetic

| ID | Counterexample | Before → correct result |
|---|---|---|
| GN01 (`gcd.c`) | `gcd(18014398509481987, 2, &x, &y)` | Returns `g=1,x=1,y=-9007199254740992`; `p*x+2*y=3`, contradicting Bézout's identity. → `x=1,y=-9007199254740993`, giving `p*x+2*y=1`. |
| GN02 (`geometry.c`) | Closed segments `(-7,7)–(-2,-7)` and `(-2,-7)–(2,-3)` | `segments_intersect` returns false. → True: both contain the endpoint `(-2,-7)`. |
| GN03 (`convex-hull.c`) | Points `(3,0),(1,0),(0,0),(2,0)` | Hull contains only `(0,0)`. → Two extremal points `(0,0),(3,0)`; otherwise the hull fails to contain the input. |
| GN04 (`convex-hull.c`) | `point p[200]`; fill `p[i]=(i,i²)` for `0≤i<200`, then hull of all 200. | ASan reports a write beyond `p`: the implementation uses `p[200]`, but the last valid index is 199. → 200 hull vertices, without an invalid access. |
| GN05 (`convolve.c`) | Two length-51 sequences, every coefficient 1. | UBSan reports `c[100]` outside `int c[100]`. → 101 coefficients `1,2,…,51,…,2,1`; lengths 51 are within the advertised 100-element limits. |
| GN06 (`bignum.c`) | Representable 100-digit `10^99 + 1`. | Sets `lastdigit=100`, then UBSan catches `digits[100]` outside the 100-digit arrays. → `lastdigit=99`, positive sign, leading digit 1 and units digit 1. |
| GN07 (`distance.c`; TSP helpers) | Distance from `(0,0,0)` to `(50000,0,0)`; also TSP x-coordinates `INT_MIN,INT_MAX`. | UBSan catches integer overflow in `50000²`; the TSP helper also overflows `INT_MIN-INT_MAX` before conversion. → Distances `50000` and `4294967295`, respectively. |
| GN08 (`bignum.c`) | `int_to_bignum(INT_MIN, &n)` with `INT_MIN=-2147483648`. | UBSan catches `abs(INT_MIN)`: positive 2147483648 does not fit `int`. → Negative bignum with magnitude 2147483648, `lastdigit=9`. |
| GN09 (`plates.c`) | Width `0.5`, height `4`, disk radius `1`. | `dense_plates` returns `-1`; odd-row count is also `-1`. → Zero: a diameter-2 disk cannot fit in a width-0.5 box. |
| GN10 (`superman.c`) | Start `(0,0)`, target `(1000,0)`; 100 circles `(2i,100,r=1)`, `0≤i<100`. | UBSan catches `c[100]` outside `circle c[100]` while reading the last valid circle. → All 100 circles fit storage; through-length 0 and travel distance 1000. |
| GN11 (`original/convex-hull.c`) | Collinear points `(0,0),(1,0),(2,0),(3,0)` in `point p[MAXPOLY]`. | The non-left-turn loop decrements `top` to 0 without advancing; next it reads `hull.p[-1]`. ASan confirms an access before `hull`. → Hull endpoints `(0,0),(3,0)`. |
| GN12 (`original/binomial.c`) | `binomial_coefficient(100,0)` with `MAXN=100`. | ASan catches initialization of `bc[100][0]` in `long bc[100][100]`. → 1; this answer is representable regardless of central binomial coefficients. |
| GN13 (`binomial.c`) | `C(67,0)` and `C(67,33)` on signed 64-bit `long`. | Even the first request overflows while computing unused central columns: UBSan reports `4472995859186094240 + 5516694892996182896`. → `C(67,0)=1`; `C(67,33)=14226520737620288370` exceeds `LONG_MAX`, so return `-1` with `errno=ERANGE`, never silent overflow. |

## Dynamic programming and backtracking

| ID | Counterexample | Before → correct result |
|---|---|---|
| DP-01 | `editbrute`: strings `a`, `b`. | Cost is 1, but missing parent initialization makes reconstruction read index **−1** (UBSan) → cost **1**, trace **S**, normal termination. |
| DP-02 | Partition `[10,1,1]` into **3** nonempty contiguous groups. | Reconstruction enters impossible state `(1 item,2 groups)` and reads an uninitialized divider (MSan) → **`{10},{1},{1}`**. |
| DP-03 | Initialize an empty Sudoku board; call `possible_count(0,0,&board)`. | Counts uninitialized `possible[0]` (MSan), although only digits 1..9 exist → exactly **9** candidates. This is not a claim that every puzzle produces a wrong grid. |
| DP-04 | Call `diagonal_order(1,2)`. | Emits **`(1,1),(2,1)`**, including an invalid row → **`(1,1),(1,2)`**, each valid cell once. |
| DP-05 | Partition `[100000,100000]` into **2** groups. | True cost equals old finite infinity `100000`; strict comparison never assigns a divider (MSan) → **`{100000},{100000}`**, cost **100000**. |
| DP-06 | Elevator input: **50 riders, 1 stop**, all destinations **1**. | The last input writes `stops[50]` outside length-50 storage (ASan) → serve all 50 at floor **1**, walking cost **0**. |
| DP-07 | `stringedit`: first token **100 `a` characters**, second token `a`. | Leading sentinel plus token plus terminator needs 102 bytes; the 101-byte buffer overflows (ASan) → normal execution, distance **99**. |
| DP-08 | Permutations: `construct_candidates(a,1,100,c,&nc)`; subsets: begin `generate_subsets(100)`. | Permutation membership reads `in_perm[100]`; the first subset branch writes `a[100]` beyond length-100 arrays (UBSan/ASan) → 100 candidates / a full first subset without invalid access. No full exponential enumeration is needed. |
| DP-09 | Link legacy `original/substringedit.c` with `original/editdistance.c`; strings `a`, `a`. | The engine calls `row_init(i)`, but the driver dereferences a nonexistent second matrix argument (sanitizer failure) → matching cost **0**, trace **M**. |
| DP-10 | `tmp/subsetsum.c`: one item `[1]`, target **1**. | The final trace prints uninitialized `s[1]` although input only filled `s[0]` (MSan) → base row has no item; final row labels the actual item **1**. Reachability itself remains true. |

## Follow-up, build, and maintenance fixes

| ID | Counterexample | Before → correct result |
|---|---|---|
| C02QUEUE | A valid min-heap already has `PQ_SIZE=400000` entries, all bound 100; insert a candidate of bound 0. | Old `pq_insert` prints a warning, returns success normally, and leaves minimum **100**, discarding the better search state. Fixed code exits 1 with `TSP priority queue capacity exceeded`. This is a precise full-frontier state witness, not a fabricated complete TSP answer. Predecessor: `dc49b1f^`. |
| C05-STRICT | Points `(0,0),(10000000,1),(10000000,0),(0,1)` with `srand(2)`. | The first roundoff fix returns tour `[3,2,1,4]` costing **20000002.000000101**, although a perimeter tour costs **20000002**. Its global tolerance (~`2.84e-7`) rejects the real ~`1e-7` decrease. Recomputed strict descent reaches **20000002**. This regression belongs to our initial epsilon fix, **not** the imported version; use `8f682a7^` (already has safe coordinate arithmetic). |
| BUILD01 | On original sources: `make -B dfs-demo CC=gcc`. Separately, make every invoked demo exit 7 while `diff` accepts empty output (exit 0). | Original build fails with duplicate definitions of `entry_time`, `exit_time`, and `time`; corrected build exits 0. Original test script exits **0** despite every demo failing; corrected delegated test entry preserves **7**. The second case is a controlled shell failure-injection witness. |
| BUILD02 | Extract the imported root tree and run `make dfs-demo`, then `./dfs-demo` on Linux. | `make` says **`'dfs-demo' is up to date`**; execution fails **`Exec format error`** (exit 126), because the tracked executable is Mach-O arm64 (`cffaedfe`), not a Linux binary. The clean source build runs the `1 0` graph input successfully. |
| FRAGMENTS01 | Compile saved `string_compare_cut` with its then-current `editbrute.c`; compare `"a"` to `"b"`, then reconstruct. | Distance is **1**, but the saved recursion never initialized reconstruction parents: UBSan reports **index -1 out of bounds for `cell[102]`**. Synchronized fragment prints **`S`** and exits 0. Predecessor: `7d651ac^`. |
| CICOMPAT | Actual [failed hosted-Clang run](https://github.com/Gabriel-Kahen/adm-code/actions/runs/41257081330): legacy `original/sudoku.c:277` and `original/backtrack.c:51` have value-less returns from implicit-int functions. | Suppressing only `-Wreturn-mismatch` still fails with **`non-void function ... should return a value [-Wreturn-type]`**; adding the legacy-only `-Wno-return-type` makes the [same suite pass](https://github.com/Gabriel-Kahen/adm-code/actions/runs/41257293891). This is compiler compatibility, not a bad mathematical answer. |
| CI02 | Actual [run 41257401626](https://github.com/Gabriel-Kahen/adm-code/actions/runs/41257401626) retries `azure.archive.ubuntu.com` at 00:35:47 UTC, then is canceled at 00:42:10 before checks. The same `bfede2e` head also launched both [push](https://github.com/Gabriel-Kahen/adm-code/actions/runs/41257080532) and [PR](https://github.com/Gabriel-Kahen/adm-code/actions/runs/41257081330) runs. | Reusing installed tools removes that package-mirror dependency; push-only-on-main and concurrency cancellation remove duplicate/superseded work. This is an observed reliability/duplication problem; it cannot honestly be presented as an algorithmic counterexample or proof that every network update fails. |

## Reproducing a witness

Use the original inputs/callers from the preserved regression directory linked
above. To materialize both source layouts without changing your checkout:

```sh
mkdir -p /tmp/adm-original /tmp/adm-corrected
git archive f74a015406c0821aa23390e3983d2c385712e3f4 | tar -x -C /tmp/adm-original
git archive 357b45cd6c1dd48e9ca2b5bd23a7390c6b0e234d | tar -x -C /tmp/adm-corrected
```

For command-line cases, compile the named source and its shared dependencies,
then supply the listed tokens on stdin. API cases use the regression callers as setup; adapt assertions when an old
signature differs (e.g. old `find_path` returns `void`, so inspect its output).
Do not change the algorithm body. Add `-fsanitize=address,undefined` for bounds and
arithmetic witnesses, or Clang `-fsanitize=memory -fPIE -pie` for uninitialized
reads. Historical files may need GNU89 syntax, standard-header preincludes, or
`-fcommon`; these accommodate interfaces without repairing algorithm logic.
For G04, both runs use `-ftrivial-auto-var-init=zero` so G03 cannot hide the bounds
failure. C05's exact seed-to-tour sequence depends on the C library.

The 88 retained C source/header blobs are byte-identical between `357b45c` and
the `c/` directory after the repository trim. Retired copies, fragments, and old
CI files remain in history. C05-STRICT and the CI fixes concern later patches or
tooling, not new counterexamples to the original algorithms. C02QUEUE proves
silent frontier-state loss; it is not a claimed complete-instance TSP optimum
counterexample. The CI rows document observed failures, not mathematical proofs.
