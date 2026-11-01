import unittest
from support import run_c

class DuplicateTree(unittest.TestCase):
    def test_multiset_deletions_preserve_nodes_and_parents(self):
        code=r'''#define main archived_main
#include "tree-demo.c"
#undef main
int seen[10];
int valid(tree*t,tree*parent,int lo,int hi){
    if(!t)return 1;
    if(t->parent!=parent||t->item<lo||t->item>hi)return 0;
    seen[t->item]++;
    return valid(t->left,t,lo,t->item-1)&&valid(t->right,t,t->item,hi);
}
int main(void){
    tree *root=NULL;int counts[10]={0};unsigned state=373;
    insert_tree(&root,1,NULL);insert_tree(&root,1,NULL);
    root=delete_tree(root,1);root=delete_tree(root,1);if(root)return 1;
    for(int step=0;step<2000;step++){
        state=state*1664525u+1013904223u;int key=(state>>8)%10;
        if((state&1)||!counts[key]){insert_tree(&root,key,NULL);counts[key]++;}
        else {root=delete_tree(root,key);counts[key]--;}
        for(int i=0;i<10;i++)seen[i]=0;
        if(!valid(root,NULL,0,9))return 2;
        for(int i=0;i<10;i++)if(counts[i]!=seen[i])return 3;
    }
    for(int key=0;key<10;key++)while(counts[key]--)root=delete_tree(root,key);
    return root!=NULL;
}'''
        result=run_c(code,flags=["-fsanitize=address,undefined","-fno-sanitize-recover=all","-no-pie"])
        self.assertEqual(result.returncode,0,result.stderr)

if __name__=="__main__":unittest.main()
