import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path
from support import ROOT

MACHINE_MAGIC={bytes.fromhex(value) for value in [
    '7f454c46','feedface','cefaedfe','feedfacf','cffaedfe',
    'cafebabe','bebafeca','cafebabf','bfbafeca']}

class SourceOnlyCheckout(unittest.TestCase):
    def tracked_files(self):
        result=subprocess.run(['git','ls-files','-z'],cwd=ROOT,text=True,capture_output=True)
        if result.returncode:self.skipTest('tracked-file checks require a Git checkout')
        return result.stdout.rstrip('\0').split('\0')

    def test_no_tracked_compiled_artifacts(self):
        names=self.tracked_files()
        compiled=[]
        for name in names:
            with (ROOT/name).open('rb') as source:
                magic=source.read(4)
            if name.endswith('.o') or magic in MACHINE_MAGIC:compiled.append(name)
        self.assertEqual(compiled,[])
        self.assertIn('tmp/sudoku-v2',names)
        self.assertIn('datafiles/sudoku-examples/sudoku.v1',names)

    def test_normal_make_builds_fresh_checkout(self):
        with tempfile.TemporaryDirectory(prefix='adm-fresh-checkout-') as name:
            directory=Path(name)
            for path in self.tracked_files():
                destination=directory/path
                destination.parent.mkdir(parents=True,exist_ok=True)
                shutil.copy2(ROOT/path,destination)
            result=subprocess.run(['make','-j2','all'],cwd=directory,text=True,capture_output=True,timeout=120)
            self.assertEqual(result.returncode,0,result.stdout+'\n'+result.stderr)
            self.assertIn('gcc',result.stdout)
            self.assertTrue((directory/'dfs-demo').is_file())
            self.assertTrue((directory/'dijkstra').is_file())
if __name__=='__main__':unittest.main()
