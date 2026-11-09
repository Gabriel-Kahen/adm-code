"""Small adapters for the C examples' I/O and value/reference semantics."""

import copy
import math
import os
import re
import sys
import random as _random
from functools import cmp_to_key

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


class address:
    """An address of an array slot or object field, for C output parameters."""

    def __init__(self, obj, key):
        self.obj, self.key = obj, key

    def __getitem__(self, index):
        assert index == 0
        return getattr(self.obj, self.key) if isinstance(self.key, str) and not isinstance(self.obj, dict) else self.obj[self.key]

    def __setitem__(self, index, value):
        assert index == 0
        if isinstance(self.key, str) and not isinstance(self.obj, dict):
            setattr(self.obj, self.key, value)
        else:
            self.obj[self.key] = value


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


def unsigned(value):
    return value & 0xffffffff


def assign(destination, value):
    destination[0] = value
    return value


def increment(destination, amount, postfix):
    old = destination[0]
    destination[0] += amount
    return old if postfix else destination[0]


def copy_struct(destination, source):
    destination.__dict__.update(copy.deepcopy(source.__dict__))


def struct_init(destination, values):
    for name, value in zip(destination.__dict__, values):
        setattr(destination, name, value)
    return destination


def array_init(destination, values):
    for i, value in enumerate(values):
        if isinstance(destination[i], list) and isinstance(value, list):
            array_init(destination[i], value)
        else:
            destination[i] = value
    return destination


def char_array(text, size):
    result = [0] * size
    for i, char in enumerate(text[:size]):
        result[i] = ord(char)
    return result


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


def strncpy(destination, source, n):
    values = [ord(c) for c in string(source)]
    for i in range(n):
        destination[i] = values[i] if i < len(values) else 0
    return destination


def memcpy(destination, source, n):
    for i in range(n):
        destination[i] = copy.deepcopy(source[i])
    return destination


def memmove(destination, source, n):
    values = [copy.deepcopy(source[i]) for i in range(n)]
    return memcpy(destination, values, n)


def memset(destination, value, n):
    for i in range(min(n, len(destination))):
        destination[i] = value
    return destination


def qsort(array, n, compare, start=0):
    # qsort is the C library call; the book's sorting algorithms stay handwritten.
    array[start:start + n] = sorted(array[start:start + n], key=cmp_to_key(compare))


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


def scanf(fmt, *destinations):
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
                return assigned if assigned else EOF
            if _peek() != fmt[fi]:
                return assigned
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
            return assigned if assigned else EOF
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
                return assigned
            if conversion == 'f' and (not width or len(chars) < width) and _peek() in ('e', 'E'):
                chars.append(chr(getchar()))
                if (not width or len(chars) < width) and _peek() in ('+', '-'):
                    chars.append(chr(getchar()))
                while (not width or len(chars) < width) and _peek() and _peek().isdigit():
                    chars.append(chr(getchar()))
            text = ''.join(chars)
        destination = destinations[assigned]
        if conversion == 's':
            strcpy(destination, text)
        else:
            destination[0] = ord(text) if conversion == 'c' else float(text) if conversion == 'f' else int(text)
        assigned += 1
    return assigned


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


def putchar(c):
    sys.stdout.write(chr(c))
    return c


def tolower(c):
    return ord(chr(c).lower()) if 0 <= c < 128 else c


def toupper(c):
    return ord(chr(c).upper()) if 0 <= c < 128 else c


def isspace(c):
    return 0 <= c < 128 and chr(c).isspace()


def isalpha(c):
    return 0 <= c < 128 and chr(c).isalpha()


def isdigit(c):
    return ord('0') <= c <= ord('9')


# rand() is a primitive supplied by the language runtime, as in the C program.
_rng = _random.Random(1)

def rand():
    return _rng.getrandbits(31)


def srand(seed):
    _rng.seed(seed)


def exit(code=0):
    raise SystemExit(code)


def free(value):
    pass


sqrt, pow, acos, sin, cos, fabs, floor, ceil = math.sqrt, math.pow, math.acos, math.sin, math.cos, math.fabs, math.floor, math.ceil
fmin, fmax = min, max

def exp(value):
    try:
        return math.exp(value)
    except OverflowError:
        return math.inf

labs = abs


def perror(prefix):
    sys.stderr.write(prefix + ": " + os.strerror(errno) + "\n")


def fputs(text, stream):
    return stream.write(string(text))


hypot = math.hypot
