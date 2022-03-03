import board
import gc
import time
from analogio import AnalogIn
import busio
import digitalio as dio
gc.collect()
import adafruit_rfm9x as rfm9x
gc.collect()
import neopixel

dot = neopixel.NeoPixel(board.NEOPIXEL, 1, brightness=0.1)

FREQ = 915.0

reset = dio.DigitalInOut(board.D5)
reset.direction = dio.Direction.OUTPUT
reset.value = True
cs = dio.DigitalInOut(board.D6)
cs.direction = dio.Direction.OUTPUT
cs.value = True  # active low
# irq = dio.DigitalInOut(board.D10)
# irq.direction = dio.Direction.INPUT
spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)

def hv_to_rgb(h, v):
    i = int(h*6.0) # XXX assume int() truncates!
    f = (h*6.0) - i
    q = v*(1.0 - f)
    t = v*f
    i = i%6
    if i == 0:
        return v, t, 0
    if i == 1:
        return q, v, 0
    if i == 2:
        return 0, v, t
    if i == 3:
        return 0, q, v
    if i == 4:
        return t, 0, v
    if i == 5:
        return v, 0, q

gc.collect()

radio = rfm9x.RFM9x(spi=spi, cs=cs, reset=reset, frequency=FREQ, baudrate=1_000_000)

battery_in = AnalogIn(board.D9)

def getVoltage(pin):
    return (pin.value * 3.3) / 65536

max_voltage = 4.2
min_voltage = 3.5

def lipo_voltage_to_soc(volts):
    return 123 - 123 / (1 + (volts/3.7)**80) ** 0.165

steps = 64

i = 0
while True:
    vbat = getVoltage(battery_in) * 2  # vbat is behind 50/50 divider
    vbat *= 4.017/3.95  # rough calibration from multimeter measurements

    soc = lipo_voltage_to_soc(vbat) / 100
    # soc = 0.5
    radio.send("vbat={:3.2f}".format(vbat).encode("ascii"))

    print("Vbat: {:3.2f}, SOC: {:2.0f}%".format(vbat, 100*soc))

    hue = soc * 0.666  # soc = 1 --> blue, soc = 0 --> red
    for value in ((steps - abs(x))/steps for x in range(-steps, steps+1)):
        dot[0] = [int(255 * comp) for comp in hv_to_rgb(hue, value)]
        time.sleep(0.002)
    dot[0] = [0,0,0]
    time.sleep(4.9)
