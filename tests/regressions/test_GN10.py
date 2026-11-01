import unittest
from support import ROOT, run_c

class CircleCapacity(unittest.TestCase):
    def test_maximum_and_rejected_extra_circle(self):
        for name, geometry in (("superman.c", "geometry.c"), ("original/superman.c", "original/geometry.c")):
            flags=("-std=gnu89", "-w", "-include", "stdio.h", "-fsanitize=address,undefined", "-fno-sanitize-recover=all", "-no-pie")
            data="0 0\n1000 0\n100\n"+"".join(f"{2*i} 100 1\n" for i in range(100))
            result=run_c(sources=(name,geometry),data=data,flags=flags)
            self.assertEqual(result.returncode,0,result.stderr)
            self.assertIn("flies 1000.000 units",result.stdout)
            result=run_c(sources=(name,geometry),data="0 0\n1 0\n101\n",flags=flags)
            self.assertNotEqual(result.returncode,0)
            self.assertIn("circle count exceeds capacity",result.stderr)
            self.assertNotIn("AddressSanitizer",result.stderr)

if __name__ == "__main__": unittest.main()
