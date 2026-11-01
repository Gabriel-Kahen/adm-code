#include <stdbool.h>
#include <stdio.h>
#include "queue.h"
#include "stack.h"
#include "priority_queue.h"

int main(void) {
    queue fifo;
    stack lifo;
    priority_queue heap;
    char operation;
    int value;
    init_queue(&fifo);
    init_stack(&lifo);
    pq_init(&heap);
    while (scanf(" %c %d", &operation, &value) == 2) {
        switch (operation) {
        case 'q':
            enqueue(&fifo, value);
            break;
        case 'Q':
            printf("%d\n", dequeue(&fifo));
            break;
        case 's':
            push(&lifo, value);
            break;
        case 'S':
            printf("%d\n", pop(&lifo));
            break;
        case 'p':
            pq_insert(&heap, value);
            break;
        case 'P':
            printf("%d\n", extract_min(&heap));
            break;
        default:
            return 1;
        }
    }
    return 0;
}
