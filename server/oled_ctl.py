"""
Display some text on the OLED (or clear it)
"""
import argparse
import sys

import board

import adafruit_ssd1306 as ssd1306
import busio
from digitalio import DigitalInOut


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--text", type=str, required=False, default="")
    args = parser.parse_args()

    i2c = busio.I2C(board.SCL, board.SDA)

    # 128x32 OLED Display
    reset_pin = DigitalInOut(board.D4)
    display = ssd1306.SSD1306_I2C(128, 32, i2c, reset=reset_pin)

    display.fill(0)  # clear
    display.text(args.text, 0, 0, 1)
    display.show()


if __name__ == "__main__":
    sys.exit(main())
