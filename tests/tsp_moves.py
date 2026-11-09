"""Check pointer-offset shuffling and the original transition/undo steps."""
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from python import tsp

s = tsp.tsp_solution()
t = tsp.tsp_instance()
tsp.initialize_solution(4, s)
s.p[0], s.p[5] = -7, -9
tsp.random_solution(s)
prefix = sorted(s.p[1:4])
print(f"random prefix={prefix[0]},{prefix[1]},{prefix[2]} last={s.p[4]} left={s.p[0]} right={s.p[5]}")
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

# Five cities give the nonadjacent swap a genuine cost change.
t.n = 5
t.p[5].x, t.p[5].y = 8, 7
tsp.initialize_solution(5, s)
for i, j in [(1, 5), (5, 1), (1, 3), (3, 1), (2, 2), (2, 2)]:
    delta = tsp.transition(s, t, i, j)
    tour = " ".join(str(s.p[k]) for k in range(1, s.n + 1))
    print(f"move {i},{j} delta={delta:.1f} cost={tsp.solution_cost(s, t):.1f} tour {tour}")

# The C pointer starts at p[1]; its n-1 prefix can be empty.
for n in [1, 2]:
    tsp.initialize_solution(n, s)
    s.p[0], s.p[n + 1] = -7, -9
    tsp.random_solution(s)
    tour = " ".join(str(s.p[k]) for k in range(1, n + 1))
    print(f"small n={n} left={s.p[0]} tour {tour} right={s.p[n + 1]}")
