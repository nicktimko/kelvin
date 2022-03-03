import argparse
import base64
import datetime
import struct
import sys


def parse_line(line: str):
    """
    Examples:
    0c52 0200 1049 00b8 1900
    0d52 0200 104d 00b4 1910
    ---------
    msg_num   ----
              vbatmv
                   ---------
                   tc_data
    """
    now = datetime.datetime.now()
    raw = base64.b64decode(line)

    msg_num, = struct.unpack("<i", raw[:4])
    vbat_mv, tc_hi, tc_lo = struct.unpack(">hhh", raw[4:])

    vbat = vbat_mv / 1000
    tc_temp = (tc_hi >> 2) / 2**2
    tc_temp /= 2
    tc_cjc = (tc_lo >> 4) / 2**4

    fmt_line = "#{:07d}, {:0.2f} V, {:4.2f} \N{DEGREE SIGN}C, cj: {:2.2f} \N{DEGREE SIGN}C".format(msg_num, vbat, tc_temp, tc_cjc)

    print(now.isoformat(), fmt_line)


def main():
    for line in sys.stdin:
        parse_line(line)


if __name__ == "__main__":
    sys.exit(main())
