import unittest
from support import ROOT,run_c

class SavedEditFragment(unittest.TestCase):
    def test_saved_recursive_function_can_reconstruct_a_substitution(self):
        fragment=(ROOT/'code-fragments/string_compare_cut').read_text()
        code=r'''#define main archived_main
#define string_compare_r source_string_compare_r
#include "editbrute.c"
#undef string_compare_r
#undef main
'''+fragment+r'''
int main(void){
    char s[]=" a",t[]=" b";
    if(string_compare_r(s,t,1,1)!=1)return 1;
    reconstruct_path(s,t,1,1,m);
    return 0;
}'''
        result=run_c(code,flags=["-fsanitize=address,undefined","-fno-sanitize-recover=all","-no-pie"])
        self.assertEqual(result.returncode,0,result.stderr)
        self.assertEqual(result.stdout,"S")

if __name__=="__main__":unittest.main()
