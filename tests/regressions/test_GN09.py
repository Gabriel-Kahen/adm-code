import unittest
from support import ROOT, run_c

class NonnegativeDiskPacking(unittest.TestCase):
    def test_narrow_boxes_and_row_boundaries(self):
        for name in ("plates.c", "original/plates.c"):
            code = f'''#define main archived_main
#include "{ROOT/name}"
#undef main
int main(void) {{
    int row;
    for(row=0;row<4;row++) if(plates_per_row(row,0.5,1)!=0) return 1;
    if(dense_layers(0.5,4,1)!=0 || dense_plates(0.5,4,1)!=0) return 2;
    if(dense_plates(1.5,4,1)!=0 || grid_plates(0.5,4,1)!=0) return 3;
    if(dense_plates(2,4,1)!=1 || dense_plates(3,4,1)!=2) return 4;
    return dense_plates(4,4,1)!=3 || grid_plates(4,4,1)!=4;
}}
'''
            result = run_c(code, flags=("-std=gnu89", "-w", "-fsanitize=undefined", "-fno-sanitize-recover=all"))
            self.assertEqual(result.returncode, 0, result.stderr)

if __name__ == "__main__": unittest.main()
