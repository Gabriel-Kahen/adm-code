import unittest

from support import run_c


class CardRanks(unittest.TestCase):
    def test_all_rank_pairs_in_both_games(self):
        for prefix in ["", "original/"]:
            code = (
                '#define main archived_main\n#include "'
                + prefix
                + 'war.c"\n#undef main\n'
                + r"""
int main(void) {
    int x, y;
    for (x = 0; x < 13; x++)
        for (y = 0; y < 13; y++) {
            queue a, b;
            init_queue(&a);
            init_queue(&b);
            enqueue(&a, x * 4);
            enqueue(&b, y * 4 + 1);
            war(&a, &b);
        }
    return 0;
}
"""
            )
            flags = ["-std=gnu89", "-include", "stdlib.h"] if prefix else []
            result = run_c(code, sources=[prefix + "queue.c", prefix + "random.c"], flags=flags)
            self.assertEqual(result.returncode, 0, result.stderr)
            lines = result.stdout.splitlines()
            self.assertEqual(len(lines), 169)
            for (x, y), line in zip(((x, y) for x in range(13) for y in range(13)), lines):
                self.assertIn("a wins" if x > y else "b wins" if y > x else "tie", line)


if __name__ == "__main__":
    unittest.main()
