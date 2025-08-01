#include <Arduino.h>
#include <SPI.h>
#include <mcp_can.h>
#include <stdlib.h>
#include <stdio.h>
#include <stdint.h>
#include <string.h>
#include <inttypes.h>

#define POTENTIOMETER_PIN A0
#define VOLTAGE_PIN A1

// https://x-engineer.org/vehicle-acceleration-maximum-speed-modeling-simulation/

int count = 0;
bool print = true;          // used to print to csv file by using programm downloaded from https://circuitjournal.com/arduino-serial-to-spreadsheet

float voltage;              // control voltage ranging form 0V to 5V
float input_voltage = 0;    // measured volatage in a range from 0 to 1023
int refrence_voltage = 5;   // constant for calcualting the voltage
int input_alpha = 0;        // measured elevation in a range from 0 to 1023
float alpha = 0;            // angle of road elevation

float F_t, F_S, F_a, F_r;   // Forces which will be defined in the while loop

float a;                    // Vehicle acceleration
float v = 60/3.6;           // Vehicle velocity
float v_old = 0;            // will be used to save the last iterations calculated speed
float rpm = 0;
unsigned int t_s = 5;       // sample intervall in ms
unsigned int t_c = 440;      // time preriod between CAN transmission

int i_x = 1;                // Transmission gear ratio, assuming only one gear
float i_0 = 1.67;           // Final drive ratio
float eta_d = 0.98;         // Driveline efficieny (guesstimated)
float r_wd = 0.343;         // Dynamic wheel radius 0.98*wheel radius = 0.98*0.35
int m = 800;                // Car mass (guesstimated)

float g = 9.816;            // Gravity
float rho = 1.3;            // Air density at sea level at 288.15 K
float c_d = 0.25;           // Air drag coefficient of a prius 0.19
float A = 2.4;              // Vehicle frontal area of a prius 1.5
float c_r = 0.015;          // road load coefficent of a prius  -- rullemodstand
float T_e;                  // Engine torque

unsigned long startMillis;
unsigned long refMillis;
unsigned long lapMillis;
unsigned long currentMillis;

// Choose the SPI pin and pass it to the CAN libary
const int spiCSPin = 10;
MCP_CAN CAN(spiCSPin);

// Set id and length of meseges (Be aware that "charToInt64" and "int64ToChar" requires a length of 8)
int id = 43;
int l = 2;

// Array that stores data before it is sendt
unsigned char stmp[8] = {0, 0, 0, 0, 0, 0, 0, 0};



void setup(){
  // Begin serial communication
  Serial.println("Setup 1");
  Serial.begin(115200);

  //Check the CAN bus is ready
  while (CAN_OK != CAN.begin(CAN_500KBPS)){
    if(!print){
      Serial.println("CAN BUS init Failed");
    }
    delay(100);
  }
    if (!print){
      Serial.println("CAN BUS Shield Init OK!");
    }
  
  pinMode(POTENTIOMETER_PIN,INPUT);
  pinMode(VOLTAGE_PIN,INPUT);

  startMillis = millis();
  refMillis = millis();
  lapMillis =millis();
  
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

void loop(){

  input_alpha = analogRead(POTENTIOMETER_PIN);
  alpha = map(input_alpha, 0, 1023, -5, 11);           // read angle -5 to 5 degrees
  alpha = alpha*0.01745329252;                          // alpha in radians

  input_voltage = analogRead(VOLTAGE_PIN);
  voltage = (input_voltage/1023.0)*refrence_voltage;  // read volatge 0V to 5V
  
//////////////////////////////////////////// Model calculations starts /////////////////////////////////////////////////////

  if (rpm <= 1064.6){                                 // the limit of 1064 RPM is derived from P = P/((60/(2*Pi))*T_e)=(14.5*10^3)/((60/(2*Pi))*130)=1064
  T_e = (130 / 5) * voltage;                          //Torque when power is below rated power if 14.5 kW
  }else{
    T_e = ((14500*9.5488) / rpm) *(voltage / 5);      //Torque when restricted by rated power. 9.5448 is a ratio between RPM and rad/s (60s/2*Pi)
  }

  F_t = (T_e * i_x * i_0 * eta_d) / r_wd;             // Traction force
 
  F_S = m * g * sin(alpha);                           // Road slope force
 
  F_a = (rho * c_d * A * v*v)/2;                      // Aerodynamic drag force
 
  if(voltage == 0 && alpha == 0 && v_old <= 0){
    F_r = 0;                                          // Road load force when no (attempted) movement
  }else{
    F_r = m * g * c_r * cos(alpha);                   // Road load force
  }
  
  
  a = -(F_S + F_a + F_r - F_t) / m;                   // acceleration in m/s^2

  v_old = v;                                          // saves old speed
  
  v = v_old + a * t_s/1000;                           // in m/s

  if (v < 0){
    v = 0;                                            // restricts velocity to not be negative. Prevents oveflow on CAN
  }

  rpm = ((v / (2* PI * r_wd)) * 60) * i_0 * i_x;     // motor rpm    
   
  //////////////////////////////////////////// Model calculations done /////////////////////////////////////////////////////
  
  // print data to serial monitor
  if(count > 100 && !print){
    Serial.print("Acceleration at ");
    Serial.println(a);
 
    Serial.print("Speed in km/h ");
    Serial.println(v*3.6);
    
    Serial.print("Angel at ");
    Serial.println(alpha*57.29577951);
   
    Serial.print("Motor RPM at ");
    Serial.println(rpm);

    Serial.print("Voltage at ");
    Serial.println(voltage);

    Serial.println("");
    // Print data as DEC integer and BIN array with respective Id.
    Serial.println("-----------------------------");
    Serial.print("Data from ID: 0x");
    Serial.println(id, DEC);
    Serial.println(rpm);
    
    for(int i = l-1; i>=0; i--){   
        if(stmp[i]<2) Serial.print("0");
        if(stmp[i]<4) Serial.print("0");
        if(stmp[i]<8) Serial.print("0");
        if(stmp[i]<16) Serial.print("0");
        if(stmp[i]<32) Serial.print("0");
        if(stmp[i]<64) Serial.print("0");
        if(stmp[i]<128) Serial.print("0");
      
        Serial.print(stmp[i], BIN);
        Serial.print("\t");
    }
    Serial.println("");
  
    count = 0;

  } else if (print){
    
    Serial.print(currentMillis-refMillis);
    Serial.print('\t');
    Serial.print(voltage);
    Serial.print('\t');
    Serial.print(rpm);
    Serial.print('\t');
    Serial.print(v*3.6);      // km/h
    Serial.print('\t');
    Serial.print(alpha*57.29577951);      // angle
    Serial.print('\t');

    Serial.println();
  }

  currentMillis = millis();
  if((currentMillis - startMillis) >= t_c){
  // Send data of length l, stored in stmp[] identified with id (The 0 choose the std CAN protocol)
  int64ToChar(stmp,rpm);
  CAN.sendMsgBuf(id, 0, l, stmp);
  startMillis = currentMillis;

  }
  
  count++;

  //currentMillis = millis();
  //Serial.print(currentMillis-startMillis);
  //Serial.println();
  //startMillis = currentMillis;
  currentMillis = millis();

  while((currentMillis - lapMillis) < t_s){
    currentMillis = millis();
  }
  lapMillis = currentMillis;
}

