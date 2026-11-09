"""Same state observations as structures.c, through the translated routines."""
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from python import graph, priority_queue, queue, set_union, stack

q = queue.queue()
queue.init_queue(q)
for i in range(queue.QUEUESIZE):
    queue.enqueue(q, i)
for i in range(17):
    queue.dequeue(q)
for i in range(queue.QUEUESIZE, queue.QUEUESIZE + 17):
    queue.enqueue(q, i)
print(f"queue first={q.first} last={q.last} count={q.count} head={queue.headq(q)} tail={q.q[q.last]}")
total = 0
while not queue.empty_queue(q):
    total += queue.dequeue(q)
print(f"queue sum={total} count={q.count}")

s = stack.stack()
stack.init_stack(s)
for i in range(stack.STACKSIZE):
    stack.push(s, i)
stack.push(s, stack.STACKSIZE)
first, second = stack.pop(s), stack.pop(s)
print(f"stack first={first} second={second} top={s.top} count={s.count}")

h = priority_queue.priority_queue()
priority_queue.pq_init(h)
for value in [4, 1, 7, 1, -3, 9, 2]:
    priority_queue.pq_insert(h, value)
print("heap array: ", end="")
priority_queue.print_pq(h)
print(f"heap_compare={priority_queue.heap_compare(h, 1, 4, 3)}")
print("heap sorted: ", end="")
while not priority_queue.empty_pq(h):
    print(priority_queue.extract_min(h), end=" ")
print()

sets = set_union.union_find()
set_union.union_find_init(sets, 6)
set_union.union_sets(sets, 2, 3)
set_union.union_sets(sets, 4, 5)
set_union.union_sets(sets, 4, 6)
set_union.union_sets(sets, 2, 4)
print(f"union root={set_union.find(sets, 3)}")
set_union.print_union_find(sets)

g = graph.graph()
graph.initialize_graph(g, False)
g.nvertices = 4
graph.insert_edge(g, 1, 2, False)
graph.insert_edge(g, 1, 3, False)
graph.insert_edge(g, 1, 4, False)
graph.delete_edge(g, 1, 3, False)
graph.print_graph(g)
print(f"graph nedges={g.nedges} degree1={g.degree[1]}")
