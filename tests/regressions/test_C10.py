import unittest

from support import run_c


class Comparator(unittest.TestCase):
    def test_three_way_sign_is_preserved(self):
        code = r"""
#define main sorting_demo_main
#include "sorting.c"
#undef main
#include <limits.h>
int main(void) {
    int a[] = {INT_MIN, -1, 0, 1, INT_MAX};
    for (int i = 0; i < 5; i++)
        for (int j = 0; j < 5; j++) {
            int expected = (a[i] > a[j]) - (a[i] < a[j]);
            if (compare(a[i], a[j]) != expected)
                return 1;
        }
    return 0;
}
"""
        result = run_c(
            code,
            sources=["random.c", "queue.c", "priority_queue.c"],
            flags=["-fsanitize=undefined", "-fno-sanitize-recover=all"],
        )
        self.assertEqual(result.returncode, 0, result.stderr)


if __name__ == "__main__":
    unittest.main()
