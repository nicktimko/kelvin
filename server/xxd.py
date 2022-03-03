import argparse
import base64
import builtins
import itertools
import string
import sys

_print = builtins.print
_format = builtins.format
# del print
# del format

TEXTABLE = set(string.punctuation + string.ascii_letters + string.digits + " ")

def generate(bs, cols=16, uppercase=False, group=2):
    if isinstance(bs, str):
        raise TypeError("bs should be a bytestring, not string")
    index = 0
    hexlen = 2 * cols + (cols // group - 1)
    linefmt = "{index:08x}: {hexed:<{hexlen:}s}  {text:}".replace("{hexlen:}", str(hexlen))
    ibs = iter(bs)
    while True:
        line = bytes(itertools.islice(ibs, cols))
        iline = iter(line)
        if not line:
            break
        hexed = " ".join(base64.b16encode(bytes(itertools.islice(iline, group))).decode() for g in line)
        if not uppercase:
            hexed = hexed.lower()
        text = "".join(c if c in TEXTABLE else "." for c in (chr(c) for c in line))
        yield linefmt.format(index=index, hexed=hexed, text=text)
        index += cols


def format(bs, **kwargs):
    return "\n".join(generate(bs))


def print(bs, **kwargs):
    _print(format(bs, **kwargs))


def _main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--cols", type=int, help="Format <cols> octets per line. Default 16 (-i: 12, -ps: 30)")
    parser.add_argument("-u", "--uppercase", action="store_true", help="use upper case hex letters")
    parser.add_argument("-g", "--group", type=int, help="number of octets per group in normal output. Default 2 (-e: 4).")
    parser.add_argument("input")
    args = parser.parse_args()

    cols = 16
    group = 2

    infile = args.input
    if infile == "-":
        print(sys.stdin.buffer.read(), cols=cols, uppercase=args.uppercase, group=group)
    else:
        with open(args.input, mode="rb") as f:
            print(f.read(), cols=cols, uppercase=args.uppercase, group=group)


if __name__ == "__main__":
    sys.exit(_main())
