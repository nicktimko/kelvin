import base64
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
        baudrate=1_000_000, spi=None, cs=None, reset=None
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

    def recv(self, **kwargs):
        return self.radio.receive(**kwargs)

    def send(self, **kwargs):
        return self.radio.send(**kwargs)


def _main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--frequency", default=915)
    parser.add_argument("-s", "--sf", default=7)
    parser.add_argument("-b", "--bw", default=125)
    parser.add_argument("-t", "--timeout", default=60)
    args = parser.parse_args()

    radio = Radio(frequency=args.frequency, bw=args.bw, sf=args.sf)

    data = radio.recv(timeout=args.timeout)

    xxd.print(base64.b16encode(data).encode))


if __name__ == "__main__":
    import argparse
    import sys
    sys.exit(_main())
