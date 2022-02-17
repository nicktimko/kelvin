import itertools
import time
import struct
import sys

import board

import adafruit_rfm9x as rfm9x
import busio
from digitalio import DigitalInOut


def main():
    radio = rfm9x.RFM9x(
        spi=busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO),
        cs=DigitalInOut(board.CE1),
        reset=DigitalInOut(board.D25),
        frequency=915.0,
        baudrate=1_000_000,
    )

    radio.signal_bandwidth = 62500
    radio.coding_rate = 6
    radio.spreading_factor = 8
    radio.enable_crc = True
    # radio.tx_power = 15

    for i in itertools.count():
        print(i)
        radio.send(struct.pack("=i", i))
        time.sleep(5)


if __name__ == "__main__":
    sys.exit(main())
