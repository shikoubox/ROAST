#include <Arduino.h>
#include <SPI.h>
#include <nRF24L01.h>
#include <RF24.h>
#define nRF24_IQR PA8
#define PIPE 0xE8E8F0F0E1LL
#define CE_PIN PB10
#define CSN_PIN PA9
#define PKG_L 32
#define BAUD 9600
char buffer[100];

RF24 radio(CE_PIN,CSN_PIN);
uint8_t data[PKG_L];

void setup()
{ 
  Serial.begin(BAUD);
  radio.begin();
  radio.setDataRate(RF24_2MBPS);
  radio.setPALevel(RF24_PA_MAX,0);
  radio.setAddressWidth(3);
  radio.setCRCLength(RF24_CRC_8);
  radio.openReadingPipe(1,PIPE);
  radio.startListening();
  radio.printDetails();
}

unsigned long lastReportTime = 0;
int count = 0;

void loop()
{
  while ( radio.available() ) {        
    radio.read(&(data[0]), PKG_L);
    count++;
  }
  
  unsigned long now = millis();
  if ( now - lastReportTime > 1000 ) {
    sprintf(buffer,"%03d",count/4);
    Serial.print(buffer);
    Serial.print(" KBPS ");
    int i;
    for(i=0;i<30;i++){
      if(i==0 || i==10 || i==20)
      Serial.print(" |");
      if(i==2 || i==12 || i==22)
      Serial.print(" |");
      Serial.print(" ");
      sprintf(buffer,"%02x",(int)(data[i]));
      Serial.print(buffer);
    }
    Serial.print(" | ");
    Serial.print((int)(data[30]),DEC);
    Serial.print(":");
    Serial.print((int)(data[31]),DEC);
    Serial.println(" ");
    lastReportTime = now;
    count = 0;
  }
}