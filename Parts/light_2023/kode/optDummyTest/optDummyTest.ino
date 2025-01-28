/////////////////////////////////////////Initialising/////////////////////////////////////////////////
#include <FastLED.h>
#include "Arduino.h"


#define NUM_LEDS 10
#define BRAKE_PIN 2
#define REAR_PIN 3
#define BLINK_PIN 7
#define REVERSE_PIN 8


CRGB leds[NUM_LEDS];

//unsigned long LastTimeLedBlinked = millis();
//unsigned long LastTimeLedBlinked = 25;



/////////////////////////////////////////Config/////////////////////////////////////////////////

void setup() {
  FastLED.addLeds<WS2812, BRAKE_PIN, GRB>(leds, NUM_LEDS);
  FastLED.addLeds<WS2812, REAR_PIN, GRB>(leds, NUM_LEDS);
  FastLED.addLeds<WS2812, BLINK_PIN, GRB>(leds, NUM_LEDS);
  FastLED.addLeds<WS2812, REVERSE_PIN, GRB>(leds, NUM_LEDS);
  FastLED.setMaxPowerInVoltsAndMilliamps(5, 1500);                   // Set power limit of LED strip to 5V, 1500mA
  for (int i = 0; i < NUM_LEDS/2; i++)
  {
    leds[i] = CRGB(0, 0, 0);
  }
  FastLED.show();  
  //FastLED.clear(); FastLED.show();                                   // Initialize all LEDs to "OFF"
  //attachInterrupt(digitalPinToInterrupt(aSeenPin), sensor, RISING);  //Interrupt for whatever
  Serial.begin(115200);                                              //Open serial port writing:
  pinMode(BRAKE_PIN, OUTPUT);
  pinMode(REAR_PIN, OUTPUT);
  pinMode(BLINK_PIN, OUTPUT);  
  pinMode(REVERSE_PIN, OUTPUT);
}


/////////////////////////////////////////Setup/////////////////////////////////////////////////


void loop() {


  //Blink5V();
  Rear5V();
  //Brake5V();
  //Reverse5V();
  //Test12V();
  int TempValue = analogRead(A1);
  Serial.print("Temp Value: ");
  Serial.println(TempValue);
  
  
}


/////////////////////////////////////////Funktions/////////////////////////////////////////////////

void Test12V(){
  Serial.println("12V vises");    
  digitalWrite(BRAKE_PIN, HIGH);
  delay(500);
  
  int sensorValue = analogRead(A0); 
  float voltage= sensorValue * (5.0 / 1023.0);
  Serial.print("Voltage: ");
  Serial.print(voltage);
  Serial.println("");

  delay(4500);
  digitalWrite(BRAKE_PIN, LOW);
  delay(3000);
}


void Blink5V(){ 
  for (int i = 0; i < NUM_LEDS; i++)
  {
    leds[i] = CRGB(100, 30, 0);
  }
    FastLED.show();  
    delay(500);

  int sensorValue = analogRead(A0); 
  //float voltage = sensorValue * (5.0 / 1023.0);
  double voltage = map(sensorValue, 0, 1023, 0, 5);
  Serial.print("Voltage ON: ");
  Serial.print(sensorValue);
  Serial.println("");


    delay(5000);

    FastLED.clear();                                    // Initialize all LEDs to "OFF"
    FastLED.show();
    sensorValue = analogRead(A0); 
    voltage = map(sensorValue, 0, 1023, 0, 5);
    Serial.print("Voltage OFF: ");
    Serial.print(sensorValue);
    Serial.println("");
    delay(3000);
}

void Brake5V(){ 
  for (int i = 0; i < NUM_LEDS/2; i++)
  {
    leds[i] = CRGB(100, 0, 0);
  }
    FastLED.show();  
  
  for (int i = NUM_LEDS/2; i < NUM_LEDS; i++)
  {
    leds[i] = CRGB(10, 0, 0);
  }
    FastLED.show();  

  int sensorValue = analogRead(A0); 
  //float voltage = sensorValue * (5.0 / 1023.0);
  double voltage = map(sensorValue, 0, 1023, 0, 5);
  Serial.print("Voltage ON: ");
  Serial.print(sensorValue);
  Serial.println("");


    delay(5000);

    FastLED.clear();                                    // Initialize all LEDs to "OFF"
    FastLED.show();
    sensorValue = analogRead(A0); 
    voltage = map(sensorValue, 0, 1023, 0, 5);
    Serial.print("Voltage OFF: ");
    Serial.print(sensorValue);
    Serial.println("");
    delay(3000);
}

void Reverse5V(){ 
  for (int i = 0; i < NUM_LEDS/2; i++)
  {
    leds[i] = CRGB(255, 255, 255);
  }
    FastLED.show();  
  
  for (int i = NUM_LEDS/2; i < NUM_LEDS; i++)
  {
    leds[i] = CRGB(255, 255, 255);
  }
    FastLED.show();  

  int sensorValue = analogRead(A0); 
  //float voltage = sensorValue * (5.0 / 1023.0);
  double voltage = map(sensorValue, 0, 1023, 0, 5);
  Serial.print("Voltage ON: ");
  Serial.print(sensorValue);
  Serial.println("");


    delay(5000);

    FastLED.clear();                                    // Initialize all LEDs to "OFF"
    FastLED.show();
    sensorValue = analogRead(A0); 
    voltage = map(sensorValue, 0, 1023, 0, 5);
    Serial.print("Voltage OFF: ");
    Serial.print(sensorValue);
    Serial.println("");
    delay(3000);
}

void Rear5V(){ 
  for (int i = 0; i < NUM_LEDS/2; i++)
  {
    leds[i] = CRGB(100, 0, 0);
  }
    FastLED.show();  
  
  for (int i = NUM_LEDS/2; i < NUM_LEDS; i++)
  {
    leds[i] = CRGB(100, 0, 0);
  }
    FastLED.show();  

  int sensorValue = analogRead(A0); 
  //float voltage = sensorValue * (5.0 / 1023.0);
  double voltage = map(sensorValue, 0, 1023, 0, 5);
  Serial.print("Voltage ON: ");
  Serial.print(sensorValue);
  Serial.println("");


    delay(5000);

    FastLED.clear();                                    // Initialize all LEDs to "OFF"
    FastLED.show();
    sensorValue = analogRead(A0); 
    voltage = map(sensorValue, 0, 1023, 0, 5);
    Serial.print("Voltage OFF: ");
    Serial.print(sensorValue);
    Serial.println("");
    delay(3000);
}