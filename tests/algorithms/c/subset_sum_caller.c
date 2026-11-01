#define main subset_demo_main
#include "subsetsum.c"
#undef main

int main(void) {
    int cases;
    scanf("%d", &cases);
    while (cases--) {
        int values[MAXN], count, target;
        scanf("%d %d", &count, &target);
        for (int i = 0; i < count; i++)
            scanf("%d", &values[i]);
        bool found = subset_sum(values, count, target);
        if (found) {
            int remaining = target;
            for (int row = count; row > 0; row--) {
                int previous = parent[row][remaining];
                if (previous != NIL) {
                    if (remaining - previous != values[row - 1])
                        return 1;
                    remaining = previous;
                }
            }
            if (remaining != 0)
                return 2;
        }
        printf("%d\n", found);
    }
    return 0;
}
