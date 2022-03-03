#!/bin/bash

TARGET="/media/nick/CIRCUITPY"

rm -rf "$TARGET/lib"
mkdir -p "$TARGET/lib"
# cp -r extlibs/Adafruit_CircuitPython_BusDevice/adafruit_bus_device "$TARGET/lib/"
# cp extlibs/Adafruit_CircuitPython_RFM9x/adafruit_rfm9x.py "$TARGET/lib/"
# cp -r lib "$TARGET"
# cp lib/colorsys.py "$TARGET/lib/"
cp lib/neopixel.mpy "$TARGET/lib/"
cp -r lib/adafruit_bus_device "$TARGET/lib/"
cp lib/adafruit_rfm9x.mpy "$TARGET/lib/"

cp code.py $TARGET/code.py
