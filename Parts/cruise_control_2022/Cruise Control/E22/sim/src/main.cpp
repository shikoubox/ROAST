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
void setup(){
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



}

void loop() {
  // put your main code here, to run repeatedly:
}