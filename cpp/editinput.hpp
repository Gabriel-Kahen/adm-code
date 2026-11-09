#pragma once

#ifndef EDITINPUT_H
#define EDITINPUT_H

#include <ctype.h>
#include <stdio.h>

/* Read a bounded token with the edit-distance sentinel in slot zero. */
static int read_edit_string(char *s, int limit) {
    int c, length = 0;

    s[0] = ' ';
    do {
        c = getchar();
    } while (c != EOF && isspace((unsigned char)c));
    if (c == EOF)
        return 0;
    do {
        if (length == limit)
            return 0;
        s[++length] = (char)c;
        c = getchar();
    } while (c != EOF && !isspace((unsigned char)c));
    s[length + 1] = '\0';
    return 1;
}

#endif
