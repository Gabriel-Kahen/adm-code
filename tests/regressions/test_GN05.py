import unittest

from support import run_c


class ConvolutionCapacity(unittest.TestCase):
    def test_full_output_length(self):
        for m, n in ((60, 60), (100, 100), (1, 100)):
            a = list(range(m))
            b = [1] * n
            data = f"{m}\n" + " ".join(map(str, a)) + f"\n{n}\n" + " ".join(map(str, b)) + "\n"
            result = run_c(
                sources=("convolve.c",),
                data=data,
                flags=("-fsanitize=address,undefined", "-fno-sanitize-recover=all", "-no-pie"),
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            expected = [
                sum(a[j] * b[k - j] for j in range(m) if 0 <= k - j < n) for k in range(m + n - 1)
            ]
            self.assertEqual(list(map(int, result.stdout.split())), expected)


if __name__ == "__main__":
    unittest.main()
