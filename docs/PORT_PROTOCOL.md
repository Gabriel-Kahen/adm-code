# Shared command-line adapter protocol

CLI accepts operation and remaining tokens as argv, prints one JSON value and
newline. No stdin parser required. Strings can be empty or contain spaces because
argv is already delimited. Integers below signed64 unless bignum/fib/binomial,
which output JSON STRINGS for consistent exactness. All operations validate arity.
Canonical list order for sets: sorted; SCC/components sorted each then lexical
outer sort. Graph neighbors in input order; avoid tests depending on tie path.

Protocol (tokens after operation):
- sort METHOD [integers...] => sorted integer array (methods insertion selection quick heap merge)
- binary TARGET [sorted integers...] => index of FIRST occurrence or -1
- insert VALUE [sorted integers...] => sorted array with value (sentinel demo)
- absdiff A B => decimal STRING
- bigint OP A B => decimal STRING (OP add sub mul div, division truncates to zero)
- fib METHOD N => decimal STRING (recursive/memo/table/constant; recursive small only)
- binomial N K => decimal STRING
- gcd A B => [g,x,y] with g>=0, a*x+b*y=g (signed inputs accepted)
- factors N => [prime factors...] for N>=1
- distance DIM [A coords...] [B coords...] => number
- matrix ROWS INNER COLS [A entries...] [B entries...] => nested rows
- convolve N M [A coefficients...] [B coefficients...] => coefficients
- edit A B => {"cost":int,"operations":string} M/S/I/D trace
- editbrute A B => int
- lcs A B => string
- substring PATTERN TEXT => minimum edit distance matching any contiguous substring, int
- partition K [nonnegative values...] => {"cost":int,"groups":[[values...],...]}
- subsetsum TARGET [nonnegative values...] => null or selected INDICES
- elevator STOPS MAXFLOOR [destinations...] => {"cost":int,"stops":[floors...]}, AT MOST budget; floor0 free

Graph CLI prefix for graph ops below: N DIRECTED M [U V W repeated M]
N>=0, DIRECTED=0/1, vertices0..N-1, integer weights; unweighted ops ignore W.
- bfs GRAPH SOURCE => distance array, null unreachable
- dfs GRAPH SOURCE => list of visited vertices (preorder)
- components GRAPH => canonical vertex groups (undirected only)
- scc METHOD GRAPH => canonical groups (tarjan/kosaraju, directed only)
- bipartite GRAPH => bool (undirected)
- cycle GRAPH => bool (undirected, self/parallel edges count as cycles)
- articulation GRAPH => sorted vertices (undirected, multi-edge safe)
- topo METHOD GRAPH => valid order (kahn/dfs, directed; cycles => error)
- mst METHOD GRAPH => {"cost":int,"edges":[[u,v,w]...]}, forest (prim/kruskal undirected)
- dijkstra GRAPH SOURCE => distances null unreachable; reject ANY negative edge
- floyd GRAPH => distance matrix null unreachable; reject negative cycles
- maxflow GRAPH SOURCE SINK => maxflow integer (directed, nonnegative; source!=sink)
- paths GRAPH SOURCE TARGET => sorted list of distinct simple vertex paths
- edgecount GRAPH => input-edge count (undirected edge once)

Geometry use double coordinates; tolerance explicit library default1e-9.
- hull N [x y pairs...] => CCW extremal points from lexicographic minimum, collinear endpoints
- area N [x y pairs...] => nonnegative polygon area
- triangulate N [x y pairs...] => list of vertex-index triples, accept either orientation;
  reject selfintersection/degeneracy rather than hanging
- mwt N [x y pairs...] => minimum sum of triangle perimeters for STRICT convex polygon
- segment ax ay bx by cx cy dx dy => bool closed-segment intersection
- project px py ax ay bx by => closest point on infinite line AB, reject A=B
- intersection ax ay bx by cx cy dx dy => point or null (parallel/coincident no unique point)
- packing W H R => [grid count, dense count] (max over both box orientations)
- superman sx sy tx ty N [cx cy r triples...] => [through, travel]; only disjoint circles
  fully crossing segment, endpoints outside. Reject unsupported overlapping circles/inside endpoints.

Search/demos:
- queens N => number solutions (N<=12 in tests), zero has one solution
- permutations N => arrays permutations0..N-1, zero => [[]]
- subsets N => arrays of subsets0..N-1, canonical lexical sorted, zero => [[]]
- sudoku STRING81 => solved 81-digit string or null; malformed/contradictory givens => error
- tsp METHOD N [x y pairs...] [SEED ITERATIONS for sample/hill/anneal]
  => {"cost":number,"tour":[indices...]}; methods exact/best/sample/hill/anneal.
  closed cycle; empty cost0; exact/best require practical explicit bound (e.g. <=12)
- grid METHOD ROWS COLS => pairs zero-based (row column snake diagonal)
- find PATTERN TEXT => first index/-1 (empty at0)
- replace TEXT N [OLD NEW pairs...] => text, sequential changes; replacements never recursively
  process inserted text for same rule; reject empty OLD
- suitors N [FIRST LAST HEIGHT WEIGHT repeated N] => [[first,last],...] sorted by
  (abs(height-180), weight>75?weight-75:-weight, last, first)
- card ENCODED => int0..51 (ranks23456789TJQKA suitscdhs)
- uncard N => 2char card
- war LIMIT NA NB [A card integers...] [B card integers...] => {"winner":"a"/"b"/"draw","steps":int}
  original: compare rank/4; tie triggers ONE facedown pair then comparison pair; pot in A,B order;
  steps counts pairs including facedown; exhausted together or limit => draw; validate no duplicate cards.

