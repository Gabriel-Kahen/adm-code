"""Small adapters for the C examples' I/O and value/reference semantics."""

import copy
import os
import re
import sys

LONG_MAX = LLONG_MAX = 9223372036854775807
LONG_MIN = -9223372036854775808
INT_MAX = 2147483647
DBL_MAX = sys.float_info.max
DBL_EPSILON = sys.float_info.epsilon
RAND_MAX = 2147483647
EOF = -1
EDOM, ERANGE = 33, 34
EXIT_SUCCESS, EXIT_FAILURE = 0, 1
errno = 0
stdin, stdout, stderr = sys.stdin, sys.stdout, sys.stderr


class offset:
    """A C array pointer advanced by a fixed number of elements."""

    def __init__(self, array, start):
        self.array, self.start = array, start

    def __getitem__(self, index):
        return self.array[self.start + index]

    def __setitem__(self, index, value):
        self.array[self.start + index] = value

    def __len__(self):
        return len(self.array) - self.start


def copy_struct(destination, source):
    destination.__dict__.update(copy.deepcopy(source.__dict__))


def string(value):
    if isinstance(value, str):
        return value.split('\0', 1)[0]
    result = []
    for i in range(len(value)):
        if value[i] == 0:
            break
        result.append(chr(value[i]))
    return ''.join(result)


def strlen(value):
    return len(string(value))


def strcmp(a, b):
    a, b = string(a), string(b)
    return (a > b) - (a < b)


def strcpy(destination, source):
    values = [ord(c) for c in string(source)] + [0]
    for i, value in enumerate(values):
        destination[i] = value
    return destination


_lookahead = None


def _peek():
    global _lookahead
    if _lookahead is None:
        _lookahead = sys.stdin.read(1)
    return _lookahead


def getchar():
    global _lookahead
    value = _peek()
    _lookahead = None
    return ord(value) if value else EOF


def scanf(fmt, *defaults):
    """Return (conversion_count, *values), retaining defaults on EOF/partial input.

    Scalars are returned normally; %s still fills its original fixed char buffer.
    """
    values = list(defaults)
    assigned = 0
    fi = 0
    while fi < len(fmt):
        if fmt[fi].isspace():
            while _peek() and _peek().isspace():
                getchar()
            fi += 1
            continue
        if fmt[fi] != '%':
            if not _peek():
                return (assigned if assigned else EOF, *values)
            if _peek() != fmt[fi]:
                return (assigned, *values)
            getchar()
            fi += 1
            continue
        match = re.match(r'%(\d*)(?:ll|l|h)?([diufsc])', fmt[fi:])
        if not match:
            raise ValueError('unsupported scanf conversion: ' + fmt[fi:])
        width, conversion = match.groups()
        width = int(width) if width else 0
        fi += len(match[0])
        if conversion != 'c':
            while _peek() and _peek().isspace():
                getchar()
        if not _peek():
            return (assigned if assigned else EOF, *values)
        if conversion == 'c':
            text = chr(getchar())
        elif conversion == 's':
            chars = []
            while (not width or len(chars) < width) and _peek() and not _peek().isspace():
                chars.append(chr(getchar()))
            text = ''.join(chars)
        else:
            chars = []
            if _peek() in ('+', '-'):
                chars.append(chr(getchar()))
            digits = False
            while (not width or len(chars) < width) and _peek() and _peek().isdigit():
                chars.append(chr(getchar()))
                digits = True
            if conversion == 'f' and (not width or len(chars) < width) and _peek() == '.':
                chars.append(chr(getchar()))
                while (not width or len(chars) < width) and _peek() and _peek().isdigit():
                    chars.append(chr(getchar()))
                    digits = True
            if not digits:
                return (assigned, *values)
            if conversion == 'f' and (not width or len(chars) < width) and _peek() in ('e', 'E'):
                chars.append(chr(getchar()))
                if (not width or len(chars) < width) and _peek() in ('+', '-'):
                    chars.append(chr(getchar()))
                while (not width or len(chars) < width) and _peek() and _peek().isdigit():
                    chars.append(chr(getchar()))
            text = ''.join(chars)
        destination = values[assigned]
        if conversion == 's':
            strcpy(destination, text)
        else:
            values[assigned] = ord(text) if conversion == 'c' else float(text) if conversion == 'f' else int(text)
        assigned += 1
    return (assigned, *values)


def _format(fmt, values):
    conversions = list(re.finditer(r'%(?!%)[-+ #0]*\d*(?:\.\d+)?(?:ll|l|h)?[diufFeEgGcs]', fmt))
    prepared = list(values)
    for i, match in enumerate(conversions):
        if match[0].endswith('s'):
            prepared[i] = string(prepared[i])
    fmt = re.sub(r'(%[-+ #0]*\d*(?:\.\d+)?)(?:ll|l|h)([diufFeEgGcs])', r'\1\2', fmt)
    fmt = fmt.replace('%u', '%d')
    return fmt % tuple(prepared)


def printf(fmt, *values):
    text = _format(fmt, values)
    sys.stdout.write(text)
    return len(text)


def fprintf(stream, fmt, *values):
    text = _format(fmt, values)
    stream.write(text)
    return len(text)


def perror(prefix):
    sys.stderr.write(prefix + ": " + os.strerror(errno) + "\n")
