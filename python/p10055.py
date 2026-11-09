
"""Direct translation of 10055.c; data structures and indexing match C."""

if __name__ == "__main__" and not __package__:
    import sys
    from pathlib import Path
    sys.path[0] = str(Path(__file__).resolve().parent.parent)
    __package__ = "python"
    sys.modules[__package__ + "." + Path(__file__).stem] = sys.modules[__name__]

from ._c import EOF, printf, scanf


def main():
    p = 0
    q = 0
    while True:
        nread, p, q = scanf("%ld %ld", p, q)
        if nread == EOF:
            break
        if (q > p):
            r = (q - p)
        else:
            r = (p - q)
        printf("%ld\n", r)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
