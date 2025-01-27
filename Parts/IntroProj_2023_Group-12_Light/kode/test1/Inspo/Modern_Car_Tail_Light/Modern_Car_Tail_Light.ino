// HAZI TECH
// Program by Hasitha Jayasundara
// Subscribe to my YouTube Channel - http://www.youtube.com/c/HAZITECH?sub_confirmation=1

#include "Arduino.h"
#include <FastLED.h>

#define LED_PIN 3 //LED Strip Signal Connection 
#define BrakeSignal 5 //Brake Signal Connection
#define LeftSignal 7 //Left Blinker Signal Connection
#define RightSignal 9 //Right Blinker Signal Connection
#define ReverseSignal 11 //Reverse Signal Connection

#define NUM_LEDS 60 //Total no of LEDs in the LED strip
#define BlinkerLEDs 15 //No of LEDs for Left/Right Blinker 

int BlinkerSpeed = 35; //Turn Signal Running LED Speed. Adjust this to match with your vehicle turn signal speed.
int BlinkerOffDelay = 250; //Turn Signal Off time. Adjust this to match with your vehicle turn signal speed.

int StartupSpeed = 25;

CRGB leds[NUM_LEDS];


void setup() 
{
FastLED.addLeds<WS2812, LED_PIN, GRB>(leds, NUM_LEDS);
pinMode(BrakeSignal, INPUT);
pinMode(LeftSignal, INPUT);
pinMode(RightSignal, INPUT);
pinMode(ReverseSignal, INPUT);


  for (int i = 0; i < (NUM_LEDS/2); i++)
  {
    leds[i] = CRGB(30, 0, 0);
    leds[i-1] = CRGB(0, 0, 0);
    leds[(NUM_LEDS-1)-i] = CRGB(30, 0, 0);
    leds[(NUM_LEDS)-i] = CRGB(0, 0, 0);
    FastLED.show();
    delay (StartupSpeed);    
  }
  
  for (int j = ((NUM_LEDS/2)-1); j >= 0; j--)
  {
    leds[j] = CRGB(30, 0, 0);
    leds[(NUM_LEDS/2-1)+((NUM_LEDS/2)-j)] = CRGB(30, 0, 0);
    FastLED.show();
    delay (StartupSpeed);    
  }

  for (int j = ((NUM_LEDS/2)-1); j >= 0; j--)
  {
    leds[j] = CRGB(255, 0, 0);
    leds[(NUM_LEDS/2-1)+((NUM_LEDS/2)-j)] = CRGB(255, 0, 0);
    FastLED.show();
    delay (StartupSpeed);    
  }

  for (int j = 255; j >= 60; j--)
  {  
    for (int i = 0; i < NUM_LEDS; i++)
    {
    leds[i] = CRGB(j, 0, 0);
    }
    FastLED.show();  
    delay (5);
  }
}


void loop() 
{
if((digitalRead(ReverseSignal)==1)&&(digitalRead(BrakeSignal)==0)) //Reverse Light
{   
Reverse();
}

if((digitalRead(ReverseSignal)==1)&&(digitalRead(BrakeSignal)==1)) //Brake Light
{   
BrakeFull();
}

if(digitalRead(ReverseSignal)==0)
{
if((digitalRead(LeftSignal)==0)&&(digitalRead(RightSignal)==0)&&(digitalRead(BrakeSignal)==0)) //Park Light
{   
ParkFull();
}

if((digitalRead(BrakeSignal)==1)&&(digitalRead(LeftSignal)==0)&&(digitalRead(RightSignal)==0)) //Brake Light
{
BrakeFull();
}
    
if((digitalRead(LeftSignal)==1)&&(digitalRead(RightSignal)==0)&&(digitalRead(BrakeSignal)==0)) //Left Blinker
{
LeftDim();
RightLit(); 
LeftBlinker();
LeftDim();
delay (BlinkerOffDelay);
}

if((digitalRead(RightSignal)==1)&&(digitalRead(LeftSignal)==0)&&(digitalRead(BrakeSignal)==0)) //Right Blinker
{
RightDim();
LeftLit();
RightBlinker();
RightDim();
delay (BlinkerOffDelay);
}

if((digitalRead(LeftSignal)==1)&&(digitalRead(RightSignal)==0)&&(digitalRead(BrakeSignal)==1)) //Left Blinker & Brake
{
LeftDim();
RightFull(); 
LeftBlinker();
LeftDim();
delay (BlinkerOffDelay);
}

if((digitalRead(RightSignal)==1)&&(digitalRead(LeftSignal)==0)&&(digitalRead(BrakeSignal)==1)) //Right Blinker & Brake
{
RightDim();
LeftFull();
RightBlinker();
RightDim();
delay (BlinkerOffDelay);
}

if((digitalRead(LeftSignal)==1)&&(digitalRead(RightSignal)==1)&&(digitalRead(BrakeSignal)==0)) //Dual Blinker / Hazard
{
LeftDim();
RightDim();
ParkMiddle();
DualBlinker();
LeftDim();
RightDim();
delay (BlinkerOffDelay);
}

if((digitalRead(LeftSignal)==1)&&(digitalRead(RightSignal)==1)&&(digitalRead(BrakeSignal)==1)) //Dual Blinker / Hazard + Brake
{
LeftDim();
RightDim();
BrakeMiddle();
DualBlinker();
LeftDim();
RightDim();
delay (BlinkerOffDelay);
}
}
}




























void Reverse()
{
  for (int i = 0; i < NUM_LEDS; i++)
  {
    leds[i] = CRGB(255, 255, 255);
  }
    FastLED.show();  
}

void BrakeFull()
{
  for (int i = 0; i < NUM_LEDS; i++)
  {
    leds[i] = CRGB(255, 0, 0);
  }
    FastLED.show();  
}

void BrakeMiddle()
{
  for (int i = BlinkerLEDs; i < (NUM_LEDS - BlinkerLEDs); i++)
  {
    leds[i] = CRGB(255, 0, 0);
  }
    FastLED.show();  
}

void ParkFull()
{
  for (int i = 0; i < NUM_LEDS; i++)
  {
    leds[i] = CRGB(60, 0, 0);
  }
    FastLED.show();
}

void ParkMiddle()
{
  for (int i = BlinkerLEDs; i < (NUM_LEDS - BlinkerLEDs); i++)
  {
    leds[i] = CRGB(60, 0, 0);
  }
    FastLED.show();  
}

void LeftBlinker()
{
  for (int i = (BlinkerLEDs-1); i >= 0; i--)
  {
    leds[i] = CRGB(255, 165, 0);
    FastLED.show();
    delay (BlinkerSpeed);    
  }
}

void LeftDim()
{
  for (int i = 0; i < BlinkerLEDs; i++)
  {
    leds[i] = CRGB(0, 0, 0);
  }
    FastLED.show();
}

void LeftLit()
{
  for (int i = 0; i < (NUM_LEDS - BlinkerLEDs); i++)
  {
    leds[i] = CRGB(75, 0, 0);
  }
    FastLED.show();
}

void LeftFull()
{
  for (int i = 0; i < (NUM_LEDS - BlinkerLEDs); i++)
  {
    leds[i] = CRGB(255, 0, 0);
  }
    FastLED.show();
}

void RightBlinker()
{
  for (int i = (NUM_LEDS - BlinkerLEDs); i < NUM_LEDS; i++)
  {
    leds[i] = CRGB(255, 165, 0);
    FastLED.show();
    delay (BlinkerSpeed);
  }
}

void RightDim()
{
   for (int i = (NUM_LEDS - BlinkerLEDs); i < NUM_LEDS; i++)
  {
    leds[i] = CRGB(0, 0, 0);
  }
    FastLED.show();
}

void RightLit()
{
  for (int i = BlinkerLEDs; i < NUM_LEDS; i++)
  {
    leds[i] = CRGB(75, 0, 0);
  }
    FastLED.show();
}

void RightFull()
{
  for (int i = BlinkerLEDs; i < NUM_LEDS; i++)
  {
    leds[i] = CRGB(255, 0, 0);
  }
    FastLED.show();
}

void DualBlinker()
{
  for (int i = (BlinkerLEDs-1); i >= 0; i--)
  {
    leds[i] = CRGB(255, 165, 0);
    leds[NUM_LEDS-1-i] = CRGB(255, 165, 0);
    FastLED.show();
    delay (BlinkerSpeed);
  }
}
