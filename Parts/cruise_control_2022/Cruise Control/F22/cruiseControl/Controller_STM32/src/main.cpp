#include <SPI.h>
#include <mcp_can.h>
#include <Arduino.h>
#include <stdlib.h>
#include <stdio.h>
#include <stdint.h>
#include <string.h>
#include <inttypes.h>


const int spiCSPin = 10;
MCP_CAN CAN(spiCSPin);

void setup()
{
  // Begin serial communication
  Serial.begin(115200);
  Serial.println("point 1");

  //Tjek the CAN bus is ready
  while (CAN_OK != CAN.begin(CAN_500KBPS))
  {
        Serial.println("CAN BUS Init Failed");
        delay(100);
  }
  Serial.println("CAN BUS  Init OK!");

  pinMode(PB1, OUTPUT); 
  pinMode(PB15, OUTPUT);
  pinMode(PB14, OUTPUT); 
  pinMode(PB13, OUTPUT);
  pinMode(PA12, OUTPUT);
  pinMode(PA11, OUTPUT);
  pinMode(PB12, OUTPUT);
  pinMode(PB11, OUTPUT);
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
    | (((uint64_t)a[3] << 24) & 0x00000000FF000000U)
    | (((uint64_t)a[2] << 16) & 0x0000000000FF0000U)
    | ((a[1] <<  8) & 0x000000000000FF00U)
    | (a[0]         & 0x00000000000000FFU);

  return n;
 
  
}

// Converts a 16 bit unsigned integer to an array of unsigned char (8 bit)
void setRpm(unsigned char a[], uint16_t n) {
  a[1] = (n & 0x000000000000FF00U) >> 8;
  a[0] = (n & 0x00000000000000FFU);
}

int getRPM(unsigned char buf[]){
  int rpm = 0;
  rpm = ((buf[1] <<  8) & 0x000000000000FF00U) | (buf[0] & 0x00000000000000FFU);
  return rpm;
}

void setCruiseControlAndBreak(unsigned char a[], unsigned char CC_s, unsigned char b){
  a[2] = ((CC_s << 1) & 0x02U) | (b & 0x01U);
}

bool getCruiseControl(unsigned char buf[]){
  unsigned char cc = 0;
  bool cc_on = false;
  cc = (buf[2] && 0x02U) >> 1;
  if(cc){
    cc_on = true;
  } else{
    cc_on = false;
  }
  return cc_on;
}

bool getBreak(unsigned char buf[]){
  unsigned char b = 0;
  bool b_on = false;
  b = (buf[2] & 0x01U);
  if(b){
    b_on = true;
  } else{
    b_on = false;
  }
  return b_on;
}

void clearBuf(unsigned char buf[]){
  for(int i = 0; i<8; i++){
    buf[i] = 0;
  }
}

void voltageOut(float voltage){
  float k = voltage* 255*0.2;
  int j = (int) k;
  int binaryNum[8];
  int i = 0;

  for (int m = 0; m < 8; m++){
    binaryNum[m]=0;
  }

  while (j > 0) {
    binaryNum[i] = j % 2;
    j = j / 2;
    i++;
  }
  
  digitalWrite(PA12, binaryNum[0]);
  digitalWrite(PA11, binaryNum[1]);
  digitalWrite(PB12, binaryNum[2]);
  digitalWrite(PB11, binaryNum[3]);

  digitalWrite(PB1, binaryNum[4]);
  digitalWrite(PB15, binaryNum[5]);
  digitalWrite(PB14, binaryNum[6]);
  digitalWrite(PB13, binaryNum[7]); 
}


float e = 0;
float upi = 0;
float up = 0;
float ui[2] = {0,0};
float uidiff = 0;
float uisum[2] = {0,0};
float rpmFilter[2] = {0,0};
float rpmRef[2] = {0,0};

float GpiAW(float rpmIn, float rpm, float T){
  //float T = time;
  float K__P =  0.1125;
  float tau__i = 9.3624;
  float w = 1;
  float voltage = 0;

  rpmRef[0] = rpmIn;
  rpmFilter[0] = -(T*w - 2)*rpmFilter[1]/(T*w + 2) + w*T*rpmRef[0]/(T*w + 2) + w*T*rpmRef[1]/(T*w + 2);

  rpmRef[1] = rpmRef[0];
  rpmFilter[1] = rpmFilter[0];


  e = rpmFilter[0] - rpm;

  
  up = e *K__P;

  //6.371742305
  uisum[0] = up/tau__i - uidiff/tau__i; 

  ui[0] = ui[1] + 0.5*T*uisum[0] + 0.5*T*uisum[1];

  upi = up + ui[0];

  voltage = upi;

  if(voltage < 0){
        voltage = 0;
  } else if (voltage > 5){
      voltage = 5;
  }

  uidiff = upi- voltage;

  ui[1] = ui[0];
  uisum[1] = uisum[0];


  return voltage;
}



uint64_t n = 0;
uint16_t rpmIn = 900;
uint16_t rpm = 0;
int cnt = 0;
bool cc_on = false;
bool b_on = false;
// len and buf will be filed with data form the CAN bus



float voltage = 0;
float T = 0;

unsigned char len = 0;
unsigned char buf[8] = {0,0,0,0,0,0,0,0};

unsigned long rpmRefMillis = 0;
unsigned long rpmMillis = 0;
unsigned long regBeginMillis = 0;
unsigned long regMillis = 0;

void loop(){

  //Tjek if a message is received
  
  if(CAN_MSGAVAIL == CAN.checkReceive())
  {
    clearBuf(buf);

    // Get data and length from the CAN bus
    CAN.readMsgBuf(&len, buf);
    
    // Get Id from the CAN bus
    unsigned long canId = CAN.getCanId();
    
    
    if (canId == 41){
      // Copy and convert data to integer
      rpmIn = getRPM(buf);
      b_on = getBreak(buf);
      cc_on = getCruiseControl(buf);
      rpmRefMillis = millis();
      //Serial.println("ID = 41");

    } else if(canId == 43){
      // Copy and convert data to integer
      rpm = getRPM(buf);

      //Serial.println("ID = 43");

      rpmMillis = millis();
      regBeginMillis = rpmMillis;

    }
    
  }
  

  if((millis() - rpmRefMillis) > 1000 || (millis() - rpmMillis) > 1000){
    voltage = 0;
    
    voltageOut(voltage);
  } else if(regBeginMillis == rpmMillis){
    T = ((float)(millis() - regMillis))/1000; 
    regMillis =  millis();

    voltage = GpiAW(rpmIn, rpm, T);
    if(!b_on){
      voltageOut(voltage);
    } else if(b_on){
      voltage = 0;
      voltageOut(voltage);

      e = 0;
      upi = 0;
      up = 0;
      uidiff = 0;
      ui[0] = 0;
      ui[1] = 0;
      uisum[0] = 0;
      uisum[1] = 0;
    }

      
    Serial.println("");
    Serial.println("");
    Serial.println("");
    Serial.println("");
    Serial.println("");
    Serial.println("");
    Serial.println("");
    Serial.println("");

    Serial.print(rpmFilter[0]/12.91491);
    Serial.print("\t");

    Serial.print(rpm/12.91491);
    Serial.print("\t");

    Serial.print(e);
    Serial.print("\t");

    Serial.print(voltage);
    Serial.print("\t");


    Serial.print(upi);
    Serial.print("\t");


    Serial.print(T,3);
    Serial.print("\t");

    Serial.print("");
    Serial.print("\t");
    Serial.print("");
    Serial.print("\t");

      
    Serial.println("");
    Serial.println("");
    Serial.println("");
    Serial.println("");
    Serial.println("");
    Serial.println("");
    Serial.println("");
      regBeginMillis = 0;
    
  }

  
  
}
