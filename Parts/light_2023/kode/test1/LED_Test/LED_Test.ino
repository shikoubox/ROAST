/////////////////////////////////////////Initialising/////////////////////////////////////////////////
#include <FastLED.h>
#include "Arduino.h"



#define NUM_LEDS_MID 84 //sat for midter stoplygten bagpå
#define NUM_LEDS_STOP 75 //bremselyset til siden
#define NUM_LEDS_REST 34 //hvilelys
#define NUM_LEDS_REV 85 //baklys
#define NUM_LEDS_BLINK 37 //blinklys

CRGB ledsMid[NUM_LEDS_MID];
CRGB ledsStopR[NUM_LEDS_STOP];
CRGB ledsStopL[NUM_LEDS_STOP];
CRGB ledsRestR[NUM_LEDS_REST];
CRGB ledsRestL[NUM_LEDS_REST];
CRGB ledsRev[NUM_LEDS_REV];
CRGB ledsBlinkR[NUM_LEDS_BLINK];
CRGB ledsBlinkL[NUM_LEDS_BLINK];

int pinO[] = {2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13};


int BlinkerSpeed = 25;
int StartupSpeed = 25;
int command = 0;


//unsigned long LastTimeLedBlinked = millis();
//unsigned long LastTimeLedBlinked = 25;



/////////////////////////////////////////Config/////////////////////////////////////////////////

void setup() {
  FastLED.addLeds<WS2812, 8, GRB>(ledsMid, NUM_LEDS_MID);
  FastLED.addLeds<WS2812, 3, GRB>(ledsStopR, NUM_LEDS_STOP);
  FastLED.addLeds<WS2812, 6, GRB>(ledsStopL, NUM_LEDS_STOP);
  FastLED.addLeds<WS2812, 2, GRB>(ledsRestR, NUM_LEDS_REST);
  FastLED.addLeds<WS2812, 13, GRB>(ledsRestL, NUM_LEDS_REST);
  FastLED.addLeds<WS2812, 11, GRB>(ledsRev, NUM_LEDS_REV);
  FastLED.addLeds<WS2812, 12, GRB>(ledsBlinkR, NUM_LEDS_BLINK);
  FastLED.addLeds<WS2812, 7, GRB>(ledsBlinkL, NUM_LEDS_BLINK);
  FastLED.setMaxPowerInVoltsAndMilliamps(5, 1500);                   // Set power limit of LED strip to 5V, 1500mA
  FastLED.clear(); FastLED.show();                                   // Initialize all LEDs to "OFF"
  //attachInterrupt(digitalPinToInterrupt(aSeenPin), sensor, RISING);  //Interrupt for whatever
  Serial.begin(115200);                                              //Open serial port writing:
    
  for(int i = 0; i < 12; i++) { //set pins for output
  pinMode(pinO[i], OUTPUT);
  };
}


/////////////////////////////////////////Setup/////////////////////////////////////////////////


void loop() {
  getCommand(); //Input fra brugeren
}


/////////////////////////////////////////Funktions/////////////////////////////////////////////////


//void Delay(current, wait, funktion){
//  if(timeNow - current > wait){
//    current = timeNow;
//  }
//}

void getCommand() {
  if (Serial.available() > 0) {
    command = Serial.parseInt();
  }
    if (command == 1){
      LEDS_OFF();
   }
   if (command == 2){
     StartUpAnimation();
   }
}

void LEDS_OFF(){
    FastLED.clear();                                    // Initialize all LEDs to "OFF"
    FastLED.show();
    Serial.println("LED slukkes");
}

void StartUpAnimation(){
  Serial.println("Startop animation vises");
  for (int i = 0; i < (NUM_LEDS_MID/2); i++)
  {
    ledsMid[i] = CRGB(30, 0, 0);
    ledsMid[i-1] = CRGB(0, 0, 0);
    ledsMid[(NUM_LEDS_MID-1)-i] = CRGB(30, 0, 0);
    ledsMid[(NUM_LEDS_MID)-i] = CRGB(0, 0, 0);
    FastLED.show();
    delay (StartupSpeed);    
  }
  
  for (int j = ((NUM_LEDS_MID/2)-1); j >= 0; j--)
  {
    ledsMid[j] = CRGB(30, 0, 0);
    ledsMid[(NUM_LEDS_MID/2-1)+((NUM_LEDS_MID/2)-j)] = CRGB(30, 0, 0);
    FastLED.show();
    delay (StartupSpeed);    
  }

  for (int j = ((NUM_LEDS_MID/2)-1); j >= 0; j--)
  {
    ledsMid[j] = CRGB(255, 0, 0);
    ledsMid[(NUM_LEDS_MID/2-1)+((NUM_LEDS_MID/2)-j)] = CRGB(255, 0, 0);
    FastLED.show();
    delay (StartupSpeed);    
  }

  for (int j = 255; j >= 60; j--)
  {  
    for (int i = 0; i < NUM_LEDS_MID; i++)
    {
    ledsMid[i] = CRGB(j, 0, 0);
    }
    FastLED.show();  
    delay (5);
  }
}

void Reverse(){
  Serial.println("Reverse animation vises");
  for (int i = 0; i < NUM_LEDS_MID; i++)
  {
    ledsMid[i] = CRGB(255, 255, 255);
  }
    FastLED.show();  
}

void BrakeFull(){
  Serial.println("BrakeFull animation vises");  
  for (int i = 0; i < NUM_LEDS_MID; i++)
  {
    ledsMid[i] = CRGB(255, 0, 0);
  }
    FastLED.show();  
}

void ParkFull(){
  Serial.println("ParkFull animation vises");  
  for (int i = 0; i < NUM_LEDS_MID; i++)
  {
    ledsMid[i] = CRGB(255, 80, 0);
  }
    FastLED.show();
}







