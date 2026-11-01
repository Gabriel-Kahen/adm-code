import unittest

from support import ROOT, run_c


class DegenerateHull(unittest.TestCase):
    def test_extremes_and_small_inputs(self):
        code = f'''#define main archived_main
#include "{ROOT / "convex-hull.c"}"
#undef main
int main(void) {{
    point p[MAXPOLY+1] = {{{{3,0}},{{1,0}},{{0,0}},{{2,0}}}};
    polygon h;
    convex_hull(p,4,&h);
    if(h.n!=2 || h.p[0][0]!=0 || h.p[1][0]!=3) return 1;
    convex_hull(p,0,&h); if(h.n!=0) return 2;
    p[0][0]=5; p[0][1]=2; convex_hull(p,1,&h);
    if(h.n!=1 || h.p[0][0]!=5) return 3;
    p[1][0]=5;p[1][1]=2;p[2][0]=5;p[2][1]=2;
    convex_hull(p,3,&h); if(h.n!=1) return 4;
    p[0][0]=3;p[0][1]=0;p[1][0]=1;p[1][1]=0;
    p[2][0]=0;p[2][1]=0;
    convex_hull(p,3,&h);
    return h.n!=2 || h.p[0][0]!=0 || h.p[1][0]!=3;
}}
'''
        result = run_c(
            code,
            sources=("geometry.c",),
            flags=("-fsanitize=address,undefined", "-fno-sanitize-recover=all", "-no-pie"),
        )
        self.assertEqual(result.returncode, 0, result.stderr)


if __name__ == "__main__":
    unittest.main()
