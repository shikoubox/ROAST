#include <FastLED.h>


void setup() {
  Serial.begin(115200);
  pinMode(8,OUTPUT);
  // put your setup code here, to run once:
  FastLED.setMaxPowerInVoltsAndMilliamps(5, 1500);  
}

void loop() {
  // put your main code here, to run repeatedly:
  digitalWrite(8, HIGH);
  delay(5000);
  digitalWrite(8, LOW);
  delay(5000);
}
