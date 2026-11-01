import ctypes
import errno
import math
import unittest
from support import ROOT, run_c

class CheckedBinomial(unittest.TestCase):
    def test_all_representable_requests_and_reported_overflow(self):
        limit=(1 << (8*ctypes.sizeof(ctypes.c_long)-1))-1
        for name in ("binomial.c","original/binomial.c","tmp/binomial.v1","fib.c","original/fib.c","code-fragments/binomial_coeff_cut"):
            if name.startswith("code-fragments/"):
                prefix="#include <stdio.h>\n#include <errno.h>\n#include <limits.h>\n#define MAXN 100\n"+(ROOT/name).read_text()
            else:
                prefix=f'#include <stdio.h>\n#define main archived_main\n#include "{ROOT/name}"\n#undef main\n'
            code=prefix+'''int main(void) {
    int n,k;long value;
    printf("%d\\n",MAXN);
    for(n=0;n<=MAXN;n++) for(k=0;k<=n;k++) {
        value=binomial_coefficient(n,k);printf("%ld %d\\n",value,errno);
    }
    if(binomial_coefficient(-1,0)!=-1 || errno!=EDOM) return 1;
    if(binomial_coefficient(1,2)!=-1 || errno!=EDOM) return 2;
    return binomial_coefficient(MAXN+1,0)!=-1 || errno!=EDOM;
}
'''
            result=run_c(code,flags=("-std=gnu89","-w","-fsanitize=address,undefined","-fno-sanitize-recover=all","-no-pie"))
            self.assertEqual(result.returncode,0,result.stderr)
            lines=result.stdout.splitlines();maximum=int(lines[0]);values=iter(lines[1:])
            for n in range(maximum+1):
                for k in range(n+1):
                    value,error=map(int,next(values).split());expected=math.comb(n,k)
                    self.assertEqual((value,error),(expected,0) if expected<=limit else (-1,errno.ERANGE),(name,n,k))

    def test_demo_reports_unrepresentable_result(self):
        result=run_c(sources=("binomial.c",),data="1\n67 33\n",flags=("-fsanitize=undefined","-fno-sanitize-recover=all"))
        self.assertNotEqual(result.returncode,0)
        self.assertIn("binomial coefficient",result.stderr)
        self.assertNotIn("runtime error",result.stderr)

if __name__ == "__main__": unittest.main()
