
"""Direct translation of editinput.c; data structures and indexing match C."""

if __name__ == "__main__" and not __package__:
    import sys
    from pathlib import Path
    sys.path[0] = str(Path(__file__).resolve().parent.parent)
    __package__ = "python"
    sys.modules[__package__ + "." + Path(__file__).stem] = sys.modules[__name__]

from ._c import *
from . import _c



# Read a bounded token with the edit-distance sentinel in slot zero.
def read_edit_string(s, limit):
    length = 0
    s[0] = ord(' ')
    while True:
        c = getchar()
        if not (((c != EOF) and isspace(unsigned(c)))):
            break
    if (c == EOF):
        return 0
    while True:
        if (length == limit):
            return 0
        length += 1
        s[length] = int(c)
        c = getchar()
        if not (((c != EOF) and (not isspace(unsigned(c))))):
            break
    s[(length + 1)] = ord('\0')
    return 1
