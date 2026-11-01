#define main matrix_demo_main
#include "matrix.c"
#undef main

int main(void) {
    int cases;
    scanf("%d", &cases);
    while (cases--) {
        matrix first, second, product;
        read_matrix(&first);
        read_matrix(&second);
        multiply(&first, &second, &product);
        printf("RESULT");
        for (int row = 1; row <= product.rows; row++) {
            for (int column = 1; column <= product.columns; column++) {
                printf(" %d", product.m[row][column]);
            }
        }
        printf("\n");
    }
    return 0;
}
