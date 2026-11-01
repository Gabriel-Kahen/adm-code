#include <stdio.h>
#include "set_union.h"

int main(void) {
    union_find sets;
    char operation;
    int first, second;
    while (scanf(" %c %d %d", &operation, &first, &second) == 3) {
        switch (operation) {
        case 'I':
            union_find_init(&sets, first);
            break;
        case 'U':
            union_sets(&sets, first, second);
            break;
        case 'F':
            printf("%d\n", same_component(&sets, first, second));
            break;
        default:
            return 1;
        }
    }
    return 0;
}
