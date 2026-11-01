import unittest
from support import ROOT, run_c

class MinimumIntegerBignum(unittest.TestCase):
    def test_entire_int_magnitude_range(self):
        for name in ("bignum.c", "original/bignum.c"):
            code = f'''#include <limits.h>
#define main archived_main
#include "{ROOT/name}"
#undef main
int main(void) {{
    int values[5]={{INT_MIN,INT_MIN+1,INT_MAX,-1,0}},i,j;
    for(i=0;i<5;i++) {{
        bignum n; unsigned int magnitude=0, expected;
        int_to_bignum(values[i],&n);
        for(j=n.lastdigit;j>=0;j--) magnitude=magnitude*10+n.digits[j];
        expected=values[i]<0 ? 0u-(unsigned int)values[i] : (unsigned int)values[i];
        if(magnitude!=expected || n.lastdigit<0 ||
           n.signbit!=(values[i]<0 ? MINUS : PLUS)) return 1;
    }}
    return 0;
}}
'''
            result = run_c(code, flags=("-std=gnu89", "-w", "-fsanitize=undefined", "-fno-sanitize-recover=all"))
            self.assertEqual(result.returncode, 0, result.stderr)

if __name__ == "__main__": unittest.main()
