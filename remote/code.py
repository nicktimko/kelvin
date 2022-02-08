import board

import colorsys
import gc
import time

# from digitalio import DigitalInOut, Direction, Pull
from analogio import AnalogIn
# import touchio
import neopixel

gc.collect()   # make some rooooom

# One pixel connected internally!
dot = neopixel.NeoPixel(board.NEOPIXEL, 1, brightness=0.25)

# Built in red LED
# led = DigitalInOut(board.D13)
# led.direction = Direction.OUTPUT

# Digital input with pullup on D7, D9, and D10
# buttons = []
# for p in [board.D6, board.D9, board.D10]:
#     button = DigitalInOut(p)
#     button.direction = Direction.INPUT
#     button.pull = Pull.UP
#     buttons.append(button)

battery_in = AnalogIn(board.D9)

def getVoltage(pin):
    return (pin.value * 3.3) / 65536

max_voltage = 4.2
min_voltage = 3.5

def lipo_voltage_to_soc(volts):
    # https://electronics.stackexchange.com/a/551667
    return 123 - 123 / (1 + (volts/3.7)**80) ** 0.165

steps = 64

i = 0
while True:
    vbat = getVoltage(battery_in) * 2  # vbat is behind 50/50 divider
    vbat *= 4.017/3.95  # rough calibration from multimeter measurements

    soc = lipo_voltage_to_soc(vbat) / 100
    # soc = 0.5

    print("Vbat: {:3.2f}, SOC: {:2.0f}%".format(vbat, 100*soc))

    hue = soc * 0.666  # soc = 1 --> blue, soc = 0 --> red

    for value in ((steps - abs(x))/steps for x in range(-steps, steps+1)):
        dot[0] = [int(255 * comp) for comp in colorsys.hsv_to_rgb(hue, 1, value)]
        time.sleep(0.002)

    dot[0] = [0,0,0]
    time.sleep(4.9)
