import unittest

from support import ROOT, run_c


class HistoricalBinomialCapacity(unittest.TestCase):
    def test_inclusive_maximum_index_fits_table(self):
        # AddressSanitizer isolates this ID's indexing defect. GN13 separately
        # checks the full recurrence's arithmetic range under UBSan.
        for name in ("original/binomial.c", "tmp/binomial.v1", "fib.c", "original/fib.c"):
            code = f'''#include <stdio.h>
#define main archived_main
#include "{ROOT / name}"
#undef main
int main(void) {{
    return binomial_coefficient(MAXN,0)!=1 || binomial_coefficient(MAXN,MAXN)!=1;
}}
'''
            result = run_c(code, flags=("-std=gnu89", "-w", "-fsanitize=address", "-no-pie"))
            self.assertEqual(result.returncode, 0, result.stderr)


if __name__ == "__main__":
    unittest.main()
