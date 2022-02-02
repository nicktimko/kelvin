# Feather M0 Express IO demo
# Welcome to CircuitPython 5 :)

import board
import gc
import time
from digitalio import DigitalInOut, Direction, Pull
from analogio import AnalogIn
import touchio
import neopixel

gc.collect()   # make some rooooom

# One pixel connected internally!
dot = neopixel.NeoPixel(board.NEOPIXEL, 1, brightness=0.25)

# Built in red LED
led = DigitalInOut(board.D13)
led.direction = Direction.OUTPUT

# Analog input on A1
analog1in = AnalogIn(board.A1)

# Digital input with pullup on D7, D9, and D10
buttons = []
for p in [board.D6, board.D9, board.D10]:
    button = DigitalInOut(p)
    button.direction = Direction.INPUT
    button.pull = Pull.UP
    buttons.append(button)

######################### HELPERS ##############################

# Helper to convert analog input to voltage
def getVoltage(pin):
    return (pin.value * 3.3) / 65536

# Helper to give us a nice color swirl
def wheel(pos):
    # Input a value 0 to 255 to get a color value.
    # The colours are a transition r - g - b - back to r.
    if (pos < 0):
        return [0, 0, 0]
    if (pos > 255):
        return [0, 0, 0]
    if (pos < 85):
        return [int(pos * 3), int(255 - (pos*3)), 0]
    elif (pos < 170):
        pos -= 85
        return [int(255 - pos*3), 0, int(pos*3)]
    else:
        pos -= 170
        return [0, int(pos*3), int(255 - pos*3)]

######################### MAIN LOOP ##############################

i = 0
while True:
  # spin internal LED around! autoshow is on
#   dot[0] = wheel(i & 255)

#   i = (i+1) % 256  # run from 0 to 255
#   time.sleep(0.01) # make bigger to slow down

    for i in range(256):
        dot[0] = [i,i,i]
        time.sleep(0.002)
    for i in range(255, -1, -1):
        dot[0] = [i,i,i]
        time.sleep(0.002)

    dot[0] = [0,0,0]
    time.sleep(4.9)
