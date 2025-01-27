#include <SPI.h>
#include <mcp_can.h>
#include <Arduino.h>
#include <stdlib.h>
#include <stdio.h>
#include <stdint.h>
#include <string.h>
#include <inttypes.h>
#define POTENTIOMETER_PIN A0


// Choose the SPI pin and pass it to the CAN libary
const int spiCSPin = 10;
MCP_CAN CAN(spiCSPin);

void setup()
{
  pinMode(POTENTIOMETER_PIN,INPUT);
  // Begin serial communication
  Serial.println("Setup 1");
  Serial.begin(115200);

  //Tjek the CAN bus is ready
  while (CAN_OK != CAN.begin(CAN_500KBPS)){
    Serial.println("CAN BUS init Failed");
    delay(100);
  }
  Serial.println("CAN BUS Shield Init OK!");


  // Set up pins
  pinMode(PB8, OUTPUT); 
  pinMode(PB9, OUTPUT); 
  pinMode(PC7,INPUT);
  pinMode(PA9,INPUT);
  pinMode(PA8,INPUT);
  pinMode(PB10,INPUT);
}

// Converts a 64 bit unsigned integer to an array of unsigned char (8 bit)
void int64ToChar(unsigned char a[], uint64_t n) {
  a[7] = (n & 0xFF00000000000000U) >> 56;
  a[6] = (n & 0x00FF000000000000U) >> 48;
  a[5] = (n & 0x0000FF0000000000U) >> 40;
  a[4] = (n & 0x000000FF00000000U) >> 32;
  a[3] = (n & 0x00000000FF000000U) >> 24;
  a[2] = (n & 0x0000000000FF0000U) >> 16;
  a[1] = (n & 0x000000000000FF00U) >> 8;
  a[0] = (n & 0x00000000000000FFU);
}

//Converts an array (length 8) of unsigned char into a unsigned 64 bit integer 
uint64_t charToInt64(unsigned char a[]) {
  uint64_t n = 0;
  n = (((uint64_t)a[7] << 56) & 0xFF00000000000000U)
    | (((uint64_t)a[6] << 48) & 0x00FF000000000000U)
    | (((uint64_t)a[5] << 40) & 0x0000FF0000000000U)
    | (((uint64_t)a[4] << 32) & 0x000000FF00000000U)
    | ((a[3] << 24) & 0x00000000FF000000U)
    | ((a[2] << 16) & 0x0000000000FF0000U)
    | ((a[1] <<  8) & 0x000000000000FF00U)
    | (a[0]         & 0x00000000000000FFU);
  return n;
}

void clearBuf(unsigned char buf[]){
  for(int i = 0; i<8; i++){
    buf[i] = 0;
  }
}

// Converts a 16 bit unsigned integer to an array of unsigned char (8 bit)
void setRpm(unsigned char a[], uint16_t n) {
  a[1] = (n & 0x000000000000FF00U) >> 8;
  a[0] = (n & 0x00000000000000FFU);
}

uint16_t getRPM(unsigned char buf[]){
  int rpm = 0;
  rpm = ((buf[1] <<  8) & 0x000000000000FF00U) | (buf[0] & 0x00000000000000FFU);
  return rpm;
}

void setCruiseControlAndBreak(unsigned char a[], unsigned char CC_s, unsigned char b){
  a[2] = ((CC_s << 1) & 0x02U) | (b & 0x01U);
}

int getCruiseControl(unsigned char buf[]){
  int cc = 0;
  cc = (buf[2] && 0x02U) >> 1;
  return cc;
}

unsigned char getBreak(unsigned char buf[]){
  unsigned char b = 0;
  b = (buf[2] && 0x01U);
  return b;
}

uint64_t getRpmFromMsg(int rpm){
  unsigned char len = 0;
  unsigned char buf[8] = {0,0,0,0,0,0,0,0};
  if(CAN_MSGAVAIL == CAN.checkReceive())
  {   
    clearBuf(buf);

    CAN.readMsgBuf(&len, buf);
    
    // Get Id from the CAN bus
    unsigned long canId = CAN.getCanId();

    if (canId == 43){
      // Copy and convert data to integer
      return getRPM(buf);
    } 
  }
  return rpm;
}




uint16_t rpm = 0;
uint16_t speederV = 0;






// Array that stores data before it is send
unsigned char stmp[8] = {0, 0, 0, 0, 0, 0, 0, 0};

// len and buf will be filed with data form the CAN bus
unsigned char len = 0;
int id = 41;
unsigned char l = 3;
unsigned char buf[8] = {0,0,0,0,0,0,0,0};

uint64_t n = 0;
int v = 0;
unsigned char cc_in = 0;
unsigned char cc_s= 0;
bool b_in = 0;
bool b_s = 0;
unsigned char plus_in = 0;
unsigned char minus_in = 0;
unsigned char plus_s = 0;
unsigned char minus_s = 0;
bool cc_on = false;
bool b_on = false;
unsigned long sendMillis = 0;

int analog = analogRead(POTENTIOMETER_PIN);
void loop()
{ 
  analog = analogRead(POTENTIOMETER_PIN);
  speederV = map(analog, 0, 1023, 0, 120); 
  //Serial.println(speederRpm);
  

  b_s = b_in;
  b_in = digitalRead(PC7);
  plus_in = digitalRead(PA8);
  minus_in = digitalRead(PB10);
  cc_in = digitalRead(PA9);

  if(b_s && !b_in){
    b_on = false;
    v = speederV;
  }

  
 

  if(!b_in){
    digitalWrite(PB9, b_in);

    if(cc_in && !cc_s){
      if(!cc_on){
        cc_on = true;
        digitalWrite(PB8, cc_on);
      }else{
        cc_on = false;
        digitalWrite(PB8, cc_on);
      }
      
    }

    if(cc_in){
      cc_s = 1;
    } else{
      cc_s = 0;
    }
    
    if(cc_on){
      if(plus_in && !plus_s){
        v += 5;
      }

      if(plus_in){
        plus_s = 1;
      } else{
        plus_s = 0;
      }

      if(minus_in && !minus_s){
        v -= 5;
      }
  
      if(minus_in){
        minus_s = 1;
      } else{
        minus_s = 0;
      }
    }else{
      v = speederV;
    }
    
  } else {
    b_on = true;
    cc_on = false;
    digitalWrite(PB9, b_in);
    digitalWrite(PB8, cc_on);
    v = 0;
  }

  if(v < 0){
    v = 0;
  }else if(v > 120){
    v = 120;
  }


  if((millis() - sendMillis) > 50){
    sendMillis = millis();

    rpm = (uint16_t)(v*12.91490549);
    setRpm(stmp,rpm);
    setCruiseControlAndBreak(stmp,cc_on,b_on);
    CAN.sendMsgBuf(id, 0, l, stmp);

    Serial.println(rpm/12.91490549);
  }
  

  
}