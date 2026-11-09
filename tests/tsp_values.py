"""Exercise the original TSP queue's struct-by-value boundaries."""
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from python import tsp_astar, tsp_pq


def print_record(label, s):
    print(f"{label} cost={s.cost:.1f} n={s.n} p={s.p[1]},{s.p[2]},{s.p[3]}")


q = tsp_pq.priority_queue()
source = tsp_astar.tsp_solution()
source.cost, source.n = 8, 3
source.p[1:4] = [1, 2, 3]
tsp_pq.pq_init(q)
tsp_pq.pq_insert(q, source)
source.cost, source.n, source.p[1] = 80, 1, 9
print_record("insert-copy", q.q[1])
source.cost, source.n = 4, 3
source.p[1:4] = [3, 2, 1]
tsp_pq.pq_insert(q, source)
source.cost, source.p[1] = 40, 9
peek = tsp_pq.top_pq(q)
peek.cost, peek.n, peek.p[1] = -1, 1, 99
print_record("modified-top", peek)
print_record("top-copy", q.q[1])
print_record("heap-second", q.q[2])
extracted = tsp_pq.extract_min(q)
print_record("extracted", extracted)
extracted.cost, extracted.n, extracted.p[2] = -2, 1, 99
print_record("modified-extracted", extracted)
print_record("extract-copy", q.q[1])
extracted = tsp_pq.extract_min(q)
print_record("last", extracted)
print(f"empty size={q.n} flag={int(tsp_pq.empty_pq(q))}")
