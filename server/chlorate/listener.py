import base64
import datetime
import sys

import board

import adafruit_rfm9x as rfm9x
import busio
import digitalio as dio

import xxd


class Radio:
    def __init__(self, *,
        frequency=915.0,
        sf=7,
        bw=125,
        cr=5,
        baudrate=1_000_000,
        spi=None, cs=None, reset=None
    ):
        if spi is None:
            spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)
        if cs is None:
            cs = dio.DigitalInOut(board.CE1)
        if reset is None:
            reset = dio.DigitalInOut(board.D25)
        self.radio = rfm9x.RFM9x(
            spi=spi,
            cs=cs,
            reset=reset,
            frequency=frequency,
            baudrate=baudrate,
        )
        self.radio.coding_rate = cr

    def recv(self, **kwargs):
        return self.radio.receive(**kwargs)

    def send(self, **kwargs):
        return self.radio.send(**kwargs)


def _main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--frequency", default=915, type=float)
    parser.add_argument("-s", "--sf", default=7, type=int)
    parser.add_argument("-b", "--bw", default=125, type=float)
    parser.add_argument("-c", "--cr", default=5, type=int)
    parser.add_argument("-t", "--timeout", default=60, help="Only used if in one-shot mode")
    parser.add_argument("-1", "--oneshot", action="store_true", help="Receive one packet and exit")
    parser.add_argument("-a", "--ascii", action="store_true", help="For each packet received, print it on a line in base64 format, no timestamp")
    args = parser.parse_args()

    radio = Radio(frequency=args.frequency, bw=args.bw, sf=args.sf, cr=args.cr)

    while True:
        try:
            data = radio.recv(timeout=args.timeout)
        except KeyboardInterrupt:
            break

        if data is None:  # means a timeout happened
            if args.oneshot:
                print("Timeout", file=sys.stderr)
                return 1
            continue

        if args.ascii:
            print(base64.b64encode(data).decode("ascii"))
        else:
            print(datetime.datetime.now().isoformat())
            xxd.print(data)
        sys.stdout.flush()

        if args.oneshot:
            break


if __name__ == "__main__":
    import argparse
    import sys
    sys.exit(_main())
