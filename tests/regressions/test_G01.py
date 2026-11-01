import unittest
from support import run_c

class StrongRoots(unittest.TestCase):
    def test_roots_and_components(self):
        p = run_c(sources=['strong.c','bfs-dfs.c','queue.c','graph.c','stack.c'],
                  data='4 3\n1 2\n2 1\n3 4\n',
                  flags=['-fsanitize=undefined','-fno-sanitize-recover=all'])
        self.assertEqual(p.returncode, 0, p.stderr)
        groups = {}
        for line in p.stdout.splitlines():
            if ' is in component ' in line:
                v, _, _, _, c = line.split()
                groups.setdefault(c,set()).add(int(v))
        self.assertEqual({frozenset(s) for s in groups.values()},
                         {frozenset([1,2]),frozenset([3]),frozenset([4])})

if __name__ == '__main__': unittest.main()
