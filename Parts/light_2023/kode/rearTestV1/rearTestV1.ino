#include <FastLED.h>

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

//pins og states er pt sat til modulet foran
int pinO[] = {2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13}; //define output pins
int pinI[] = {A0, A1, A2, A3, A4, A5, A6, A7}; // define input pins

int alive = 1; // to check that the arduino has not broken, should be send as a message out everyonce in a while. Probably dont need an int
int lightStates[9] = {}; // states of the lights, allows for simply changing state compared to turning on or off.
int canbusOut = 0;
byte canbusOutBus[2] = {};


unsigned long blinkInterval = 25;
unsigned long blinkTimeLast = 0;
unsigned long blinkTimeCurrent = 0;

unsigned int blinkStateR = 0;
unsigned int blinkStateL = 0;

int analogPin[] = {"A0", "A1", "A2", "A3", "A4", "A5", "A6", "A7"};
int analogStates[10] = {};

unsigned int test;


void setup() {
  Serial.begin(115200); // init UART with baud rate of 9600
  for(int i = 0; i < 12; i++) { //set pins for output
    pinMode(pinO[i], OUTPUT);
  };
  for(int i = 0; i < 8; i++) { //set pins for input
    pinMode(pinI[i], INPUT);
  };
  for(int i = 0; i < 9; i++) {
    Serial.print("Light state ");
    Serial.print(i);
    Serial.print(": ");
    Serial.println(lightStates[i]);
  }

  // Serial pins
  // RX = pin 0, TX = pin 1
  // Digital States = light = pin
  // state 0 = Rear R = pin 2, 1 = Stop R = pin 3, 2 = Blink R = pin 12, 
  // state 3 = Rear L = pin 13, 4 = Stop L = pin 6, 5 = Blink L = pin 7, 
  // state 6 = Middle stop = pin 8, 7 = Reverse = pin 11, 8 = Fog = pin 10,
  // ekstra output 
  // Muxs1 = pin 4, Muxs2 = pin 5, Reserce = pin 13
  // Analog states = light = pin
  // state 0 = Rear R = A0, 1 = Stop R = A1, 2 = Blink R = A2, 
  // state 3 = Rear L = A3, 4 = Stop L = A4, 5 = Blink L = A5
  // 6 = Middle Stop = A6, 
  // Mux = A7
  // state 7 = Reverse = AMux1 00, 8 = Fog = AMux2 01, 9 = Temp = AMux3 10, 10 = Reserve = AMux4 11


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
}

void loop() {
  // put your main code here, to run repeatedly:

  //Serial.println("test");

  if (Serial.available() > 0) {

    char light = Serial.read();

    switch (light) { // switch for choosing which light should change state
      case '0': //Rear R
        if (lightStates[0] == 0) {
          // turn on the light
          lightStates[0] = 1; 
        } else {
          // turn off the light
          lightStates[0] = 0;
        }
        Serial.print("State 0: ");
        Serial.println(lightStates[0]);
        rightRest(lightStates[0]);
        break;
      case '1': //Stop R
        if (lightStates[1] == 0) {
          // turn on the light
          lightStates[1] = 1;
        } else {
          // turn off the light
          lightStates[1] = 0;
        }
        Serial.print("State 1: ");
        Serial.println(lightStates[1]);
        rightStop(lightStates[1]);
        break;
      case '2': //Blink R
        if (lightStates[2] == 0) {
          // turn on the light
          lightStates[2] = 1;
        } else if(lightStates[2] == 1) {
          // turn off the light
          lightStates[2] = 0;
          blinkStateR = 0;
          for (int i = 0; i < NUM_LEDS_BLINK; i++) {
            ledsBlinkR[i] = CRGB(0, 0, 0);
          }
          FastLED.show(); 
        }
        Serial.print("State 2: ");
        Serial.println(lightStates[2]);
        break;
      case '3': //Rear L
        if (lightStates[3] == 0) {
          // turn on the light
          lightStates[3] = 1;
        } else {
          // turn off the light
          lightStates[3] = 0;
        }
        Serial.print("State 3: ");
        Serial.println(lightStates[3]);
        leftRest(lightStates[3]);
        break;
      case '4': //Stop L
        if (lightStates[4] == 0) {
          // turn on the light
          lightStates[4] = 1;
        } else {
          // turn off the light
          lightStates[4] = 0;
        }
        Serial.print("State 4: ");
        Serial.println(lightStates[4]);
        leftStop(lightStates[4]);
        break;
      case '5': //Blink L
        if (lightStates[5] == 0) {
          // turn on the light
          lightStates[5] = 1;
        } else if(lightStates[5] == 1) {
          // turn off the light
          lightStates[5] = 0;
          blinkStateL = 0;
          for (int i = 0; i < NUM_LEDS_BLINK; i++) {
            ledsBlinkL[i] = CRGB(0, 0, 0);
          } 
          FastLED.show();
        }
        Serial.print("State 5: ");
        Serial.println(lightStates[5]);
        break;
      case '6': //Middle stop
        if (lightStates[6] == 0) {
          // turn on the light
          lightStates[6] = 1;
        } else {
          // turn off the light
          lightStates[6] = 0;
        }
        Serial.print("State 6: ");
        Serial.println(lightStates[6]);
        middleStop(lightStates[6]);
        break;
      case '7': //Reverse
        if (lightStates[7] == 0) {
          // turn on the light
          lightStates[7] = 1;
        } else {
          // turn off the light
          lightStates[7] = 0;
        }
        Serial.print("State 7: ");
        Serial.println(lightStates[7]);
        reverse(lightStates[7]);
        break;
      case '8': //Fog
        if (lightStates[8] == 0) {
          // turn on the light
          digitalWrite(7, HIGH);
          lightStates[8] = 1;
        } else {
          // turn off the light
          digitalWrite(7, LOW);
          lightStates[8] = 0;
        }
        Serial.print("State 8: ");
        Serial.println(lightStates[8]);
        break;
      default:
        Serial.println("Default");
        // something something default??
        break;        
      }
    
  }
  
  // something something things that work  at a pulse

  blinkTimeCurrent = millis();

  if(lightStates[2] == 1 || lightStates[5] == 1) {
    if(blinkTimeCurrent - blinkTimeLast >= blinkInterval) {
      blinkTimeLast = blinkTimeCurrent;
      if(lightStates[2] == 1) {
        blinkRight();
        blinkStateR++;
      }
      if(lightStates[5] == 1) {
        blinkLeft();
        blinkStateL++;
      } 
      if(blinkStateR >= 20) {
        blinkStateR = 0;
      }
      if(blinkStateL >= 20) {
        blinkStateL = 0;
      }
    }
  }


  // check the analog inputs
  

  
  if(test == 50000) {
    lightCheck();
    signalOut();
    test = 0;
  }
  test++;
  
}

void middleStop(int state){
  if(state == 1) {
    for (int i = 0; i < NUM_LEDS_MID; i++) {
      ledsMid[i] = CRGB(255, 0, 0);
    } 
  } else {
    for (int i = 0; i < NUM_LEDS_MID; i++) {
      ledsMid[i] = CRGB(0, 0, 0);
    } 
  }
  FastLED.show();
}

void rightStop(int state){
  if(state == 1) {
    for (int i = 0; i < NUM_LEDS_STOP; i++) {
      ledsStopR[i] = CRGB(255, 0, 0);
    } 
  } else {
    for (int i = 0; i < NUM_LEDS_STOP; i++) {
      ledsStopR[i] = CRGB(0, 0, 0);
    } 
  }
  FastLED.show();
}

void leftStop(int state){
  if(state == 1) {
    for (int i = 0; i < NUM_LEDS_STOP; i++) {
      ledsStopL[i] = CRGB(255, 0, 0);
    } 
  } else {
    for (int i = 0; i < NUM_LEDS_STOP; i++) {
      ledsStopL[i] = CRGB(0, 0, 0);
    } 
  }
  FastLED.show();
}

void leftRest(int state) {
  if(state == 1) {
    for (int i = 0; i < NUM_LEDS_REST; i++) {
      ledsRestL[i] = CRGB(255, 0, 0);
    } 
  } else {
    for (int i = 0; i < NUM_LEDS_REST; i++) {
      ledsRestL[i] = CRGB(0, 0, 0);
    } 
  }
  FastLED.show();
}

void rightRest(int state) {
  if(state == 1) {
    for (int i = 0; i < NUM_LEDS_REST; i++) {
      ledsRestR[i] = CRGB(255, 0, 0);
    } 
  } else {
    for (int i = 0; i < NUM_LEDS_REST; i++) {
      ledsRestR[i] = CRGB(0, 0, 0);
    } 
  }
  FastLED.show();
}


void reverse(int state) {
  if(state == 1) {
    for (int i = 0; i < NUM_LEDS_REV; i++) {
      ledsRev[i] = CRGB(255, 0, 0);
    } 
  } else {
    for (int i = 0; i < NUM_LEDS_REV; i++) {
      ledsRev[i] = CRGB(0, 0, 0);
    } 
  }
  FastLED.show();
}

void blinkRight() {
  if(blinkStateR == 0) {
    for (int i = 0; i < NUM_LEDS_BLINK; i++) {
      ledsBlinkR[i] = CRGB(0, 0, 0);
    }
  } else if(blinkStateR <= 18) {
    ledsBlinkR[blinkStateR-1] = CRGB(100, 25, 0);
    ledsBlinkR[NUM_LEDS_BLINK-blinkStateR] = CRGB(100, 25, 0);
  } else if(blinkStateR == 19) {
    ledsBlinkR[18] = CRGB(100, 25, 0);
  }
  FastLED.show();
}

void blinkLeft() {
  if(blinkStateL == 0) {
    for (int i = 0; i < NUM_LEDS_BLINK; i++) {
      ledsBlinkL[i] = CRGB(0, 0, 0);
    }   
  } else if(blinkStateL <= 18) {
    ledsBlinkL[blinkStateL-1] = CRGB(100, 25, 0);
    ledsBlinkL[NUM_LEDS_BLINK-blinkStateL] = CRGB(100, 25, 0);
  } else if(blinkStateL == 19) {
    ledsBlinkL[18] = CRGB(100, 25, 0);
  }
  FastLED.show();
}


//a


void lightCheck() {
  int minimumRead = 400;
  int value;
  for(int i = 0; i <= 6; i++) {
    value = analogRead(analogPin[i]);
    if(value > minimumRead) {
      analogStates[i] = 1;
    } else {
      analogStates[i] = 0;
    }
  }
  digitalWrite(4, LOW);
  digitalWrite(5, LOW);
  value = analogRead(analogPin[7]);
  if(value > minimumRead) {
    analogStates[7] = 1;
  } else {
    analogStates[7] = 0;
  }
  digitalWrite(4, HIGH);
  digitalWrite(5, LOW);
  value = analogRead(analogPin[7]);
  if(value > minimumRead) {
    analogStates[8] = 1;
  } else {
    analogStates[8] = 0;
  }
  digitalWrite(4, LOW);
  digitalWrite(5, HIGH);
  value = analogRead(analogPin[7]);
  if(value > minimumRead) {
    analogStates[9] = 1;
  } else {
    analogStates[9] = 0;
  }
}

void signalOut() {
  canbusOut = 0;
  for(int i = 0; i < 9; i++) {
    if(lightStates[i] == analogStates[i]) {
      canbusOut = canbusOut | (1 << i);
    }
  }
  //if(analogStates[9] == 1) {
  //  canbusOut++;
  //}
  byte array_new[] = {'N', 'e', 'x', 't'};

  canbusOutBus[1] = canbusOut & 255;
  canbusOutBus[2] = canbusOut >> 8;
  //Serial.write(canbusOutBus[1]);
  //Serial.println("");
  //Serial.write(canbusOutBus[2]);
  //Serial.println("");

  
  //Serial.write(canbusOutBus, 2);
} 
