#define VBATPIN A7

#include <SPI.h>
#include <RH_RF95.h>

#define RFM95_CS 6
#define RFM95_RST 5
#define RFM95_INT 10

#define MAX31855_CS 12

#define BLINKY 13

#define RF95_FREQ 915.0
RH_RF95 rf95(RFM95_CS, RFM95_INT);

int32_t message_num;
uint8_t radiobuf[20];

PROGMEM static const RH_RF95::ModemConfig MODEM_CONF = {
  RH_RF95_SPREADING_FACTOR_128CPS,  // SF7 (2**7 = 128)
  RH_RF95_BW_125KHZ,
  RH_RF95_CODING_RATE_4_5
};

void setup() {
  message_num = 0;

  pinMode(13, OUTPUT); // blinkenlight

  Serial.begin(115200);

  pinMode(RFM95_RST, OUTPUT);
  pinMode(MAX31855_CS, OUTPUT);

  // manual reset
  digitalWrite(RFM95_RST, LOW);
  delay(10);
  digitalWrite(RFM95_RST, HIGH);
  delay(10);

  while (!rf95.init()) {
    Serial.println("LoRa radio init failed");
    Serial.println("Uncomment '#define SERIAL_DEBUG' in RH_RF95.cpp for detailed debug info");
    while (1);
  }

  if (!rf95.setFrequency(RF95_FREQ)) {
    Serial.println("setFrequency failed");
    while (1);
  }

  analogReadResolution(12);
//  rf95.setModemRegisters(&MODEM_CONF);

//  Serial.print("Set Freq to: "); Serial.println(RF95_FREQ);

//  rf95.sleep();
}

void loop() {
  // put your main code here, to run repeatedly:
  digitalWrite(BLINKY, LOW);
  delay(1920);

  digitalWrite(BLINKY, HIGH);
//  delay(100);

  float vbatmv = analogRead(VBATPIN)
    * 2           // 1:1 voltage divider
    * 3.3         // 3.3 V reference
    * 1000        // millivolts
    / 4096        // 12 bit counts
    * 4189/4194;  // 'calibration'
  uint16_t vbatmvi = (uint16_t)vbatmv;

  digitalWrite(RFM95_CS, HIGH);

  SPI.beginTransaction(SPISettings(1000000, MSBFIRST, SPI_MODE0));
  digitalWrite(MAX31855_CS, LOW);

  radiobuf[6] = SPI.transfer(0);
  radiobuf[7] = SPI.transfer(0);
  radiobuf[8] = SPI.transfer(0);
  radiobuf[9] = SPI.transfer(0);

  digitalWrite(MAX31855_CS, HIGH);
  SPI.endTransaction();


//  Serial.print("VBat: " ); Serial.println(measuredvbat);

//  message_num++;
//  std::copy(static_cast<const char*>(static_cast<const void*>(&message_num)),
//            static_cast<const char*>(static_cast<const void*>(&message_num)) + sizeof message_num,
//            radiobuf);

  // 0-3 = message serial number
  for (uint8_t i = 0; i < 4; i++) {
    radiobuf[i]++;
    if (radiobuf[i] == 0) {
      radiobuf[i+1]++;
    } else {
      break;
    }
  }

  // 4-5 vbat_mv
  radiobuf[4] = vbatmvi >> 8;
  radiobuf[5] = vbatmvi % 256;

  // 6-9 temp data (raw max dump)


  rf95.setModeTx();
  rf95.send(
//    reinterpret_cast<const uint8_t*>(reinterpret_cast<const void*>(&message_num)),
//    sizeof message_num
    (uint8_t *)radiobuf, 10
  );
  rf95.waitPacketSent();
  rf95.setModeIdle();

}
