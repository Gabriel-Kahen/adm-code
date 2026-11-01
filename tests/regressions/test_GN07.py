import unittest

from support import ROOT, run_c


class IntegerPointDistance(unittest.TestCase):
    def test_large_coordinates(self):
        for name in ("distance.c", "original/distance.c"):
            code = f'''#include <stdio.h>
#include <limits.h>
#define main archived_main
#include "{ROOT / name}"
#undef main
int main(void) {{
    point a={{0,0,0}}, b={{50000,0,0}};
    double expected;
    if(distance(a,b)!=50000.0) return 1;
    a[0]=INT_MIN;b[0]=INT_MAX;
    expected=(double)INT_MAX-(double)INT_MIN;
    return distance(a,b)!=expected;
}}
'''
            result = run_c(
                code,
                flags=("-std=gnu89", "-w", "-fsanitize=undefined", "-fno-sanitize-recover=all"),
            )
            self.assertEqual(result.returncode, 0, result.stderr)


if __name__ == "__main__":
    unittest.main()
