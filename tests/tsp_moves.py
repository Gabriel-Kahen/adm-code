"""Check pointer-offset shuffling and the original transition/undo steps."""
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from python import tsp

s = tsp.tsp_solution()
t = tsp.tsp_instance()
tsp.initialize_solution(4, s)
tsp.random_solution(s)
prefix = sorted(s.p[1:4])
print(f"random prefix={prefix[0]},{prefix[1]},{prefix[2]} last={s.p[4]}")
t.n = 4
for i, (x, y) in enumerate([(0, 0), (3, 0), (3, 4), (0, 4)], 1):
    t.p[i].x, t.p[i].y = x, y
tsp.initialize_solution(4, s)
print(f"initial cost={tsp.solution_cost(s, t):.1f}")
delta = tsp.transition(s, t, 1, 2)
print(f"forward delta={delta:.1f} cost={tsp.solution_cost(s, t):.1f}")
delta = tsp.transition(s, t, 2, 1)
print(f"reverse delta={delta:.1f} cost={tsp.solution_cost(s, t):.1f}")
print(f"tour {s.p[1]} {s.p[2]} {s.p[3]} {s.p[4]}")
