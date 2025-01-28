// Tx Code
#include <Arduino.h>
#include <SPI.h>
#include <SDFat.h>
#include <RF24.h>
#include <eXoCAN.h>
#include <STM32RTC.h>
#define nRF24_IQR PA8
#define PIPE 0xE8E8F0F0E1LL
#define CE_PIN PB10
#define CSN_PIN PA9
#define CS_PIN PA4
#define BLK_L 512          // Block size (Bytes)
#define BLK_BUF_L 1        // Number of blocks in block buffer
#define PKG_L 32           // Pacakge size (Bytes)
#define PKG_BUF_L 1        // Number of packages in package buffer
#define MSG_L 8            // CAN message length (Bytes)
#define ID_L 2             // CAN id length (Bytes)
#define FRM_L MSG_L + ID_L // Frame length (Bytes)
#define TIME_L 2           // Time stamp length (Bytes)
#define BAUD 9600

/* RTC declarations */
STM32RTC &rtc = STM32RTC::getInstance(); // Get the rtc object
uint8_t seconds;
uint8_t minutes;
uint8_t hours;

/* SD declarations */
SdFat sd;
SdFile myFile;

/* RF declarations */
RF24 radio(CE_PIN, CSN_PIN); // Radio object (CE,CSN)

/* CAN declarations */
eXoCAN can(STD_ID_LEN, BR500K, PORTB_8_9_WIRE_PULLUP);

/*Buffer declarations */
uint8_t block[BLK_BUF_L][BLK_L];
uint8_t package[PKG_BUF_L][PKG_L]; // RF payload data
uint32_t idx = 0;
uint32_t pkgIdx = 0;
uint32_t blkIdx = 0;

void nRF24_ISR();
bool radioWritePayload(uint8_t *data, uint8_t data_len);
void rtcTimeToInt(const char *str);
void sdWrite();
void canISR();

void setup()
{
  /* RTC config */
  rtc.setClockSource(STM32RTC::LSE_CLOCK);
  rtc.begin(0);
  rtcTimeToInt(__TIME__);
  if (
      (rtc.getHours() < hours) ||
      (rtc.getHours() == hours && rtc.getMinutes() < minutes) ||
      (rtc.getHours() == hours && rtc.getMinutes() == minutes && rtc.getSeconds() < seconds))
  {
    rtc.setTime(hours, minutes, seconds);
  }

  /* Serial config */

  /* LED config */
  pinMode(LED_BUILTIN, OUTPUT);

  /* SD config */
  sd.begin(CS_PIN, 18e6); // SPI speed = 18MHz
  myFile.open("datalog.txt", FILE_WRITE);

  /* Radio config */
  SPI.begin();
  radio.begin();
  radio.setAddressWidth(3);
  radio.setCRCLength(RF24_CRC_8);
  radio.setDataRate(RF24_2MBPS); // Options: RF24_1MBPS, RF24_2MBPS, RF24_250KBPS
  radio.setPALevel(RF24_PA_LOW, 0);
  radio.openWritingPipe(PIPE);
  radio.stopListening();
  radioWritePayload(package[pkgIdx], PKG_L); // Fill Tx buffer
  radioWritePayload(package[pkgIdx], PKG_L); // Fill Tx buffer
  radioWritePayload(package[pkgIdx], PKG_L); // Fill Tx buffer

  /* Interrupt config */
  radio.maskIRQ(0, 0, 1);
  pinMode(nRF24_IQR, INPUT);
  attachInterrupt(digitalPinToInterrupt(nRF24_IQR), nRF24_ISR, FALLING);
  can.attachInterrupt(canISR);
}

void loop()
{
  if (!(millis() % 8)){ // write to sd card every 8ms
    sdWrite();
  }
}

void canISR() // get CAN bus frame passed by a filter into fifo0
{
  digitalWrite(LED_BUILTIN, LOW);
  int id;
  int fltIdx;
  uint8_t msg[MSG_L];
  can.receive(id, fltIdx, msg); // Empties CAN FIFO
  uint8_t i;
  for (i = 0; i < ID_L; i++){ // Write id to package
    package[pkgIdx][idx] = (id >> (8 * (ID_L - i - 1))) & 0x00FF;
    idx++;
  }
  for (i = ID_L; i < FRM_L; i++){ // Write msg to package
    package[pkgIdx][idx] = msg[i - ID_L];
    idx++;
  }
  if (idx >= 3 * FRM_L){ // A package contains 3 frames.
    idx = 0;
    pkgIdx++;
  }
  if (pkgIdx >= PKG_BUF_L){
    pkgIdx = 0;
  }
  digitalWrite(LED_BUILTIN, HIGH);
}

void nRF24_ISR() // This runs when nRF24 module interupts the MCU
{
  package[pkgIdx][PKG_L - 1] = rtc.getSeconds();
  package[pkgIdx][PKG_L - 2] = rtc.getMinutes();
  if (radioWritePayload(package[pkgIdx], PKG_L)){ // Upload data via SPI
    // digitalWrite(LED_BUILTIN,HIGH);
  }
  else{
    // digitalWrite(LED_BUILTIN,LOW);
  }
}

bool radioWritePayload(uint8_t *data, uint8_t data_len)
{
  digitalWrite(CE_PIN, HIGH);
  SPI.beginTransaction(CSN_PIN, SPISettings(RF24_SPI_SPEED, MSBFIRST, SPI_MODE0));
  uint8_t status = SPI.transfer(CSN_PIN, 0x27, SPI_CONTINUE); // 0x27 is a write register command. Returns status register.
  SPI.transfer(CSN_PIN, 0x77, SPI_LAST);                      // 0x77 resets satus register (rst exti).
  SPI.transfer(CSN_PIN, 0xA0, SPI_CONTINUE);                  // 0xA0 is a wirte Tx buffer command.
  SPI.transfer(CSN_PIN, data, data_len, SPI_LAST);            // writing data over SPI
  SPI.endTransaction(CSN_PIN);
  digitalWrite(CE_PIN, LOW);
  return (bool)(status >> (5)) & 1; // 5th bit in status reg tells us if data transfered succesfully
}

void sdWrite()
{
  detachInterrupt(digitalPinToInterrupt(nRF24_IQR));
  myFile.write(block[0], BLK_L); // Log data to sd
  if (!(millis() % 3000)){ // Save sd card file every 3s
    myFile.close();
    myFile.open("datalog.txt", FILE_WRITE);
  }
  radioWritePayload(package[pkgIdx], PKG_L); // Resume RF transmission.
  attachInterrupt(digitalPinToInterrupt(nRF24_IQR), nRF24_ISR, FALLING);
}

void rtcTimeToInt(const char *str)
{
  seconds = 0;
  minutes = 0;
  hours = 0;
  int32_t hms = 0, multiplier = 1, strIdx;
  for (strIdx = 0; str[strIdx]; strIdx++){}
  strIdx--;
  for (; strIdx >= 0; strIdx--){
    if (str[strIdx] == ':'){
      hms++;
      multiplier = 1;
    }
    else if (str[strIdx] >= '0' && str[strIdx] <= '9'){
      if (hms == 0){
        seconds += (str[strIdx] - '0') * multiplier;
      }
      if (hms == 1){
        minutes += (str[strIdx] - '0') * multiplier;
      }
      if (hms == 2){
        hours += (str[strIdx] - '0') * multiplier;
      }
      multiplier *= 10;
    }
  }
}
