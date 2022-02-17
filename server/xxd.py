import argparse
import base64
import builtins
import itertools
import string
import sys

TEXTABLE = set(string.punctuation + string.ascii_letters + string.digits + " ")

def generate(bs, cols=16, uppercase=False, group=2):
    index = 0
    linefmt = "{index:08x}: {hexed:{hexlen:}s}  {text:}"
    ibs = iter(bs)
    hexlen = 2 * cols + (cols // group - 1)
    while True:
        line = bytes(itertools.islice(ibs, cols))
        iline = iter(line)
        if not line:
            break
        hexed = " ".join(base64.b16encode(bytes(itertools.islice(iline, group))).decode() for g in line)
        if not uppercase:
            hexed = hexed.lower()
        text = "".join(c if c in TEXTABLE else "." for c in (chr(c) for c in line))
        print(hexlen)
        yield linefmt.format(index=index, hexlen=hexlen, hexed=hexed, text=text)


def format(bs, **kwargs):
    return "\n".join(generate(bs))


def print(bs, **kwargs):
    builtins.print(bs, **kwargs)


def _main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--cols", type=int, help="Format <cols> octets per line. Default 16 (-i: 12, -ps: 30)")
    parser.add_argument("-u", "--uppercase", action="store_true", help="use upper case hex letters")
    parser.add_argument("-g", "--group", type=int, help="number of octets per group in normal output. Default 2 (-e: 4).")
    parser.add_argument("input")
    args = parser.parse_args()

    cols = args.cols or 16
    group = args.group or 2

    infile = args.input
    if infile == "-":
        print(format(sys.stdin.buffer.read(), cols=cols, uppercase=args.uppercase, group=group))
    else:
        with open(args.input, mode="rb") as f:
            print(format(f.read(), cols=cols, uppercase=args.uppercase, group=group))


if __name__ == "__main__":
    sys.exit(_main())
