import unittest
from support import run_c

class ElevatorCapacity(unittest.TestCase):
    def test_fifty_riders_and_stop_limit(self):
        for source in ['elevator.c','original/elevator.c']:
            for count in [1,50]:
                r=run_c(sources=[source],data='50 %d\n'%count+' '.join(['1']*50)+'\n',flags=['-std=gnu89','-w','-fsanitize=address,undefined'])
                self.assertEqual(r.returncode,0,r.stderr)
                self.assertEqual(r.stderr,'')
                self.assertIn('cost = 0\n',r.stdout)
    def test_reject_dimensions_before_reading_into_array(self):
        for source in ['elevator.c','original/elevator.c']:
            r=run_c(sources=[source],data='51 1\n',flags=['-std=gnu89','-w','-fsanitize=address,undefined'])
            self.assertEqual(r.returncode,1,r.stderr)
            self.assertIn('invalid elevator dimensions',r.stderr)
if __name__=='__main__':unittest.main()
