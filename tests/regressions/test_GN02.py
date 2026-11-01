import unittest

from support import ROOT, run_c


class SegmentIntersections(unittest.TestCase):
    def test_shared_endpoints_and_integer_oracle(self):
        for name in ("geometry.c", "original/geometry.c"):
            code = f'''#include <stdio.h>
#include "{ROOT / name}"
long cross(point a, point b, point c) {{
    return (long)(b[0]-a[0])*(long)(c[1]-a[1]) -
           (long)(b[1]-a[1])*(long)(c[0]-a[0]);
}}
int reference(segment a, segment b) {{
    long x=cross(a.p1,a.p2,b.p1), y=cross(a.p1,a.p2,b.p2);
    long z=cross(b.p1,b.p2,a.p1), w=cross(b.p1,b.p2,a.p2);
    if ((!x && point_in_box(b.p1,a.p1,a.p2)) ||
        (!y && point_in_box(b.p2,a.p1,a.p2)) ||
        (!z && point_in_box(a.p1,b.p1,b.p2)) ||
        (!w && point_in_box(a.p2,b.p1,b.p2))) return 1;
    return x*y < 0 && z*w < 0;
}}
int main(void) {{
    segment a={{{{-7,7}},{{-2,-7}}}}, b={{{{-2,-7}},{{2,-3}}}};
    int i,j,k,l;
    if (!segments_intersect(a,b)) return 1;
    for(i=0;i<9;i++) for(j=0;j<9;j++)
    for(k=0;k<9;k++) for(l=0;l<9;l++) {{
        a.p1[0]=i%3-1; a.p1[1]=i/3-1;
        a.p2[0]=j%3-1; a.p2[1]=j/3-1;
        b.p1[0]=k%3-1; b.p1[1]=k/3-1;
        b.p2[0]=l%3-1; b.p2[1]=l/3-1;
        if (segments_intersect(a,b) != reference(a,b)) return 2;
    }}
    return 0;
}}
'''
            result = run_c(
                code,
                flags=("-std=gnu89", "-w", "-fsanitize=undefined", "-fno-sanitize-recover=all"),
            )
            self.assertEqual(result.returncode, 0, result.stderr)


if __name__ == "__main__":
    unittest.main()
