import unittest

from support import ROOT, run_c


class BignumCapacity(unittest.TestCase):
    def test_full_precision_and_explicit_overflow(self):
        for name in ("bignum.c", "original/bignum.c"):
            preamble = f'''#define main archived_main
#include "{ROOT / name}"
#undef main
'''
            code = (
                preamble
                + r"""
int main(void) {
    bignum a, b, c;
    initialize_bignum(&a);
    int_to_bignum(1, &b);
    a.lastdigit = 99;
    a.digits[99] = 1;
    add_bignum(&a, &b, &c);
    if (c.lastdigit != 99 || c.signbit != PLUS || c.digits[99] != 1 || c.digits[0] != 1)
        return 1;
    multiply_bignum(&a, &b, &c);
    if (c.lastdigit != 99 || c.signbit != PLUS || c.digits[99] != 1 || c.digits[0] != 0)
        return 2;
    int_to_bignum(0, &b);
    multiply_bignum(&a, &b, &c);
    return c.lastdigit != 0 || c.signbit != PLUS || c.digits[0] != 0;
}
"""
            )
            flags = (
                "-std=gnu89",
                "-w",
                "-fsanitize=address,undefined",
                "-fno-sanitize-recover=all",
                "-no-pie",
            )
            result = run_c(code, flags=flags)
            self.assertEqual(result.returncode, 0, result.stderr)
            code = (
                preamble
                + r"""
int main(void) {
    bignum a, b, c;
    int i;
    initialize_bignum(&a);
    int_to_bignum(1, &b);
    a.lastdigit = 99;
    for (i = 0; i < 100; i++)
        a.digits[i] = 9;
    add_bignum(&a, &b, &c);
    return 0;
}
"""
            )
            result = run_c(code, flags=flags)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("bignum capacity exceeded", result.stderr)
            self.assertNotIn("runtime error", result.stderr)
            self.assertNotIn("AddressSanitizer", result.stderr)


if __name__ == "__main__":
    unittest.main()
