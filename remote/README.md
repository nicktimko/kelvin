# Remote Device

* Feather M0 Express (shoulda bought the M4...)
* FeatherWing RFM95W (LoRa 900 MHz)
* 400 mAh battery

## Wiring

Wiring to make the Feather M0 and LoRa Wing act like the LoRa Feather-ish

### Feather to LoRa
* Power
    * GND, black
    * 3V, red
* SPI
    * SCK, green, LoRa: SCK, Feather: CK (M0 pin )
    * MOSI, blue, LoRa: MOSI, Feather: MO (M0 pin )
    * MISO, purple, LoRa: MISO, Feather: MI (M0 pin )
* Control
    * IRQ, yellow, LoRa: IRQ, Feather: D10 (M0 pin 12, PA07)
    * RST, orange, LoRa: RST, Feather: D6 (M0 pin 29, PA20)
    * CS, gray, LoRa: CS, Feather: D5 (M0 pin 24, PA15)
