import unittest
from support import ROOT, run_c

class HullCapacity(unittest.TestCase):
    def test_maximum_input_and_output_capacity(self):
        for name, geometry in (("convex-hull.c", "geometry.c"), ("original/convex-hull.c", "original/geometry.c")):
            code = f'''#include <stdio.h>
#include <stdlib.h>
#define main archived_main
#include "{ROOT/name}"
#undef main
int main(void) {{
    point p[MAXPOLY]; polygon h; int i;
    for (i=0;i<MAXPOLY;i++) {{ p[i][0]=i; p[i][1]=i*i; }}
    convex_hull(p,MAXPOLY,&h);
    return h.n != MAXPOLY;
}}
'''
            result = run_c(code, sources=(geometry,), flags=("-std=gnu89", "-w", "-include", "stdio.h", "-include", "stdlib.h", "-fsanitize=address,undefined", "-fno-sanitize-recover=all", "-no-pie"))
            self.assertEqual(result.returncode, 0, result.stderr)

if __name__ == "__main__": unittest.main()
