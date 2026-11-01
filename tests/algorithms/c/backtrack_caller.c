/* The generic engine is linked as its own translation unit. */
#include <stdbool.h>
#include "backtrack.h"
#include "backtrack.h" /* The public header must also be safe to include twice. */
#include <stdio.h>
#include <string.h>

typedef struct {
    int length;
    int stop_after;
    int solutions;
    int moves;
    int unmoves;
    int depth;
    int prefix_sum;
    int error;
    unsigned char seen[1 << 12];
} search_state;

int is_a_solution(int a[], int k, data input) {
    search_state *state = (search_state *)input;
    (void)a;
    if (k > state->length)
        state->error = 1;
    return k >= state->length;
}

void process_solution(int a[], int k, data input) {
    search_state *state = (search_state *)input;
    int mask = 0, sum = 0;
    if (k != state->length || state->depth != k)
        state->error = 1;
    for (int i = 1; i <= k; i++) {
        if (a[i] != 0 && a[i] != 1)
            state->error = 1;
        mask = (mask << 1) | a[i];
        sum += a[i];
    }
    if (state->seen[mask] || sum != state->prefix_sum)
        state->error = 1;
    state->seen[mask] = 1;
    state->solutions++;
    if (state->stop_after && state->solutions == state->stop_after)
        finished = true;
}

void construct_candidates(int a[], int k, data input, int c[], int *nc) {
    search_state *state = (search_state *)input;
    (void)a;
    if (state->depth != k - 1)
        state->error = 1;
    c[0] = 0;
    c[1] = 1;
    *nc = 2;
}

void make_move(int a[], int k, data input) {
    search_state *state = (search_state *)input;
    if (state->depth != k - 1)
        state->error = 1;
    state->depth++;
    state->moves++;
    state->prefix_sum += a[k];
}

void unmake_move(int a[], int k, data input) {
    search_state *state = (search_state *)input;
    if (state->depth != k)
        state->error = 1;
    state->depth--;
    state->unmoves++;
    state->prefix_sum -= a[k];
}

int main(void) {
    int cases;
    scanf("%d", &cases);
    while (cases--) {
        int solution[NMAX + 1] = {0};
        search_state state;
        memset(&state, 0, sizeof(state));
        scanf("%d %d", &state.length, &state.stop_after);
        if (state.length < 0 || state.length > 12)
            return 1;
        finished = false;
        backtrack(solution, 0, (data)&state);
        if (state.error || state.depth || state.prefix_sum)
            return 2;
        if (state.moves != state.unmoves)
            return 3;
        printf("%d %d %d\n", state.solutions, state.moves, finished);
    }
    return 0;
}
