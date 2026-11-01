import unittest

from support import run_c


class BruteEditParents(unittest.TestCase):
    def test_modern_and_intermediate_drivers(self):
        for source in ["editbrute.c", "tmp/editbrute-previous.c"]:
            for a, b, path in [
                ("a", "b", "S"),
                ("a", "a", "M"),
                ("a", "ab", "MI"),
                ("ab", "a", "MD"),
            ]:
                with self.subTest(source=source, a=a, b=b):
                    r = run_c(
                        sources=[source],
                        data=a + "\n" + b + "\n",
                        flags=["-fsanitize=address,undefined", "-DTRUE=1", "-DFALSE=0"],
                    )
                    self.assertEqual(r.returncode, 0, r.stderr)
                    self.assertEqual(r.stdout.splitlines()[-1], path)

    def test_original_parent_chain(self):
        code = r"""
#include <stdio.h>
int match(char a, char b) {
    return a != b;
}
int indel(char a) {
    return 1;
}
void match_out(char *s, char *t, int i, int j) {
    putchar(s[i] == t[j] ? 'M' : 'S');
}
void insert_out(char *t, int j) {
    putchar('I');
}
void delete_out(char *s, int i) {
    putchar('D');
}
#include "original/editbrute.c"
int main(void) {
    char s[] = " a", t[] = " ab";
    if (string_compare(s, t, 1, 2) != 1)
        return 1;
    reconstruct_path(s, t, 1, 2);
    return 0;
}
"""
        r = run_c(code, flags=["-std=gnu89", "-w", "-fsanitize=address,undefined"])
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertEqual(r.stdout, "MI")


if __name__ == "__main__":
    unittest.main()
