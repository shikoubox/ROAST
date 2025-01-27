#include <SPI.h>
#include <mcp_can.h>
#include <Arduino.h>
#include <stdlib.h>
#include <stdio.h>
#include <stdint.h>
#include <string.h>
#include <inttypes.h>

// Define IO-pins names
#define speederAnalogeIn_PIN A0
#define speederPWMIn_PIN PA11
#define cruiseControlPlus_PIN PA8
#define cruiseControlMinus_PIN PB10
#define breakOnIn_PIN PC7
#define cruiseControlOnIn_PIN PA9
#define cruiseControlOnLED_PIN PB8
#define breakeOnLED_PIN PB9


// Choose the SPI pin and pass it to the CAN libary
const int spiCSPin = 10;
MCP_CAN CAN(spiCSPin);

void setup(){
  // Begin serial communication
  Serial.println("Setup 1");
  Serial.begin(115200);

  //Tjek the CAN bus is ready
  while (CAN_OK != CAN.begin(CAN_500KBPS)){
    Serial.println("CAN BUS init Failed");
    delay(100);
  }
  Serial.println("CAN BUS Shield Init OK!");


  // Set up IO-pins
  pinMode(speederAnalogeIn_PIN,INPUT);
  pinMode(cruiseControlOnLED_PIN, OUTPUT); 
  pinMode(breakeOnLED_PIN, OUTPUT); 
  pinMode(breakOnIn_PIN,INPUT);
  pinMode(cruiseControlOnIn_PIN,INPUT);
  pinMode(cruiseControlPlus_PIN,INPUT);
  pinMode(cruiseControlMinus_PIN,INPUT);
  pinMode(speederPWMIn_PIN,INPUT);
}

// Funtions to detect edges on the speeder PWM signal
void rising() ;
void falling() ;

// Funtions to send values over CAN:
void set16BitIntOnCAN(unsigned char a[], uint16_t n);
void setCruiseControlBreakPlusMinus(unsigned char a[], unsigned char cc_on, unsigned char b_on,unsigned char plus_on, unsigned char minus_on);

// Values used for the PWM input
volatile int pwm_value = 0;
volatile int prev_time = 0;
int pwm_mapped;

// Array that stores data before it is send
unsigned char stmp[8] = {0, 0, 0, 0, 0, 0, 0, 0};

// Sets the id for CAN messeges send by this MCU
int id = 41;

// Sets the defalt length for CAN messeges send by this MCU
unsigned char l = 3;

// len and buf will be filed with data form the CAN bus
unsigned char len = 0;
unsigned char buf[8] = {0,0,0,0,0,0,0,0};


// Values for input dectection
// Gets the curent input from the buttons 
unsigned char cc_in = 0;
unsigned char b_in = 0;
unsigned char plus_in = 0;
unsigned char minus_in = 0;

// Stores the last input and is used for rising edge detection
unsigned char cc_s= 0;
unsigned char b_s = 0;
unsigned char plus_s = 0;
unsigned char minus_s = 0;

// Logic values for cruise control and breake state
bool cc_on = false;
bool b_on = false;
bool plus_on = false;
bool minus_on = false;

// Used to save the time the last messege was send
unsigned long timeOfLastMessege = 0; 

// Time between CAN messages in ms
uint16_t msBetweenCANMessages = 50;

int analogSpeederIn = analogRead(speederAnalogeIn_PIN);


int v = 0;
uint16_t rpm = 0;
uint8_t analogThrottel = 0;
uint8_t PWMThrottel = 0;
float throttelOut = 0;
uint16_t throttelSend = 0;

void loop()
{ 
  analogSpeederIn = analogRead(speederAnalogeIn_PIN);
  analogThrottel = map(analogSpeederIn, 0, 1023, 0, 100); 
  PWMThrottel = pwm_mapped;

  b_s = b_in;
  b_in = digitalRead(breakOnIn_PIN);
  plus_in = digitalRead(cruiseControlPlus_PIN);
  minus_in = digitalRead(cruiseControlMinus_PIN);
  cc_in = digitalRead(cruiseControlOnIn_PIN);

  if(b_s && !b_in){
    b_on = false;
    //v = analogThrottel; 
    throttelOut = 0;
  }
 

  if(!b_in){
    digitalWrite(breakeOnLED_PIN, b_in);

    if(cc_in && !cc_s){
      if(!cc_on){
        cc_on = true;
        digitalWrite(cruiseControlOnLED_PIN, cc_on);
      }else{
        cc_on = false;
        digitalWrite(cruiseControlOnLED_PIN, cc_on);
      }
      
    }

    if(cc_in){
      cc_s = 1;
    } else{
      cc_s = 0;
    }
    
    if(cc_on){
      if(plus_in && !plus_s){
        //v += 5;
        plus_on = true;
      }

      if(plus_in){
        plus_s = 1;
      } else{
        plus_s = 0;
      }

      if(minus_in && !minus_s){
        //v -= 5;
        minus_on = true;
      }
  
      if(minus_in){
        minus_s = 1;
      } else{
        minus_s = 0;
      }
    }else{
      //v = analogeThrottel;
      throttelOut = (analogThrottel + PWMThrottel)/2;
    }
    
  } else {
    b_on = true;
    cc_on = false;
    digitalWrite(breakeOnLED_PIN, b_in);
    digitalWrite(cruiseControlOnLED_PIN, cc_on);
    //v = 0;
    throttelOut = 0;
  }

  /*
  if(v < 0){
    v = 0;
  }else if(v > 120){
    v = 120;
  }
  */
  if(throttelOut < 0){
    throttelOut = 0;
  } else if(throttelOut > 100){
    throttelOut = 100;
  }


  if((millis() - timeOfLastMessege) > msBetweenCANMessages){
    timeOfLastMessege = millis();
    //rpm = (uint16_t)(v*12.91490549);
    throttelSend =  (uint16_t) throttelOut;
    set16BitIntOnCAN(stmp,throttelSend);
    setCruiseControlBreakPlusMinus(stmp,cc_on,b_on,plus_on,minus_on);
    plus_on = false;
    minus_on = false;
    
    CAN.sendMsgBuf(id, 0, l, stmp);
  }
  
}

void rising(){
  attachInterrupt(speederPWMIn_PIN, falling, FALLING);
  prev_time = micros();
}
 
void falling(){
  attachInterrupt(speederPWMIn_PIN, rising, RISING);
  pwm_value = micros()-prev_time;

  // Limit values is set to match test done with the speeder, to encure the input to the maped function is not excited. 
  if(pwm_value<381){
    pwm_value = 381;
  } else if(pwm_value>2937){
    pwm_value = 2937;
  }
  pwm_mapped = map(pwm_value, 381, 2937, 0, 100); 
  
}

void set16BitIntOnCAN(unsigned char a[], uint16_t n) {
  a[1] = (n & 0x000000000000FF00U) >> 8;
  a[0] = (n & 0x00000000000000FFU);
}

void setCruiseControlBreakPlusMinus(unsigned char a[], unsigned char cc_on, unsigned char b_on,unsigned char plus_on, unsigned char minus_on){
  a[2] = ((cc_on << 3) & 0x08U) | ((plus_on << 2) & 0x04U) | ((cc_on << 1) & 0x02U) | (b_on & 0x01U);
}

