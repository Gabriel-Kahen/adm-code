import unittest

from support import ROOT, run_c


class ExtendedGCD(unittest.TestCase):
    def test_large_exact_coefficients(self):
        for name in ("gcd.c", "original/gcd.c"):
            code = f'''#define main archived_main
#include "{ROOT / name}"
#undef main
int main(void) {{
    long p = 18014398509481987L, x, y;
    long g = gcd(p, 2, &x, &y);
    if (g != 1 || x != 1 || y != -9007199254740993L) return 1;
    return (__int128)p*x + (__int128)2*y != g;
}}
'''
            result = run_c(
                code,
                flags=("-std=gnu89", "-w", "-fsanitize=undefined", "-fno-sanitize-recover=all"),
            )
            self.assertEqual(result.returncode, 0, result.stderr)


if __name__ == "__main__":
    unittest.main()
