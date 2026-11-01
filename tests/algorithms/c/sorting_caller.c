/* The driver is replaced so each sorting routine sees the same supplied data. */
#define main sorting_demo_main
#include "sorting.c"
#undef main

int main(void) {
    int cases;
    if (scanf("%d", &cases) != 1)
        return 1;
    while (cases--) {
        int count, input[1000], sorted[1000];
        scanf("%d", &count);
        for (int i = 0; i < count; i++)
            scanf("%d", &input[i]);
        for (int algorithm = 0; algorithm < 5; algorithm++) {
            for (int i = 0; i < count; i++)
                sorted[i] = input[i];
            switch (algorithm) {
            case 0:
                insertion_sort(sorted, count);
                break;
            case 1:
                selection_sort(sorted, count);
                break;
            case 2:
                quicksort(sorted, 0, count - 1);
                break;
            case 3:
                heapsort_(sorted, count);
                break;
            case 4:
                merge_sort(sorted, 0, count - 1);
                break;
            }
            printf("SORT");
            for (int i = 0; i < count; i++)
                printf(" %d", sorted[i]);
            printf("\n");
        }
        for (int key = -4; key <= 4; key++) {
            int index = binary_search(sorted, key, 0, count - 1);
            if (index >= 0 && sorted[index] != key)
                return 2;
            printf("%d ", index >= 0);
        }
        printf("\n");
    }
    return 0;
}
