#define main string_demo_main
#if defined(TEST_LCS)
#include "lcs.c"
#elif defined(TEST_SUBSTRING)
#include "substringedit.c"
#else
#include "stringedit.c"
#endif
#undef main

int main(void) {
    int cases;
    scanf("%d", &cases);
    while (cases--) {
        char first[MAXLEN + 2] = " ", second[MAXLEN + 2] = " ";
        scanf("%101s %101s", first + 1, second + 1);
        /* A dash encodes the empty string; generated test strings use a/b only. */
        if (first[1] == '-')
            first[1] = '\0';
        if (second[1] == '-')
            second[1] = '\0';
        int cost = string_compare(first, second, m);
        int row, column, path_cost = 0, steps = 0;
        goal_cell(first, second, &row, &column);
        while (m[row][column].parent != -1) {
            if (++steps > 2 * MAXLEN)
                return 1;
            switch (m[row][column].parent) {
            case MATCH:
                if (!row || !column)
                    return 2;
                path_cost += match(first[row], second[column]);
                row--;
                column--;
                break;
            case INSERT:
                if (!column)
                    return 3;
                path_cost += indel(second[column--]);
                break;
            case DELETE:
                if (!row)
                    return 4;
                path_cost += indel(first[row--]);
                break;
            default:
                return 5;
            }
        }
        if (path_cost != cost)
            return 6;
        printf("%d\n", cost);
    }
    return 0;
}
