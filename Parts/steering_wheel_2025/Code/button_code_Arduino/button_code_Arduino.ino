//Define button/light pins (GPIO)
int button_1_1_Push = 7; // First GPIO for button 1 - always push button
int button_1_2_R = 4; // Second GPIO for button 1 - ether red light or push button
int button_1_3_G = 3; // Third GPIO for button 1 - ether green light or push button
int button_1_4_B = 2; // Fourth GPIO for button 1 - ether blue light or push button

// Define light intensity PWM
int button_1_light = 6; // PWM pin for button light control

// Define debounce delay
int Delay = 100;

byte colorCode = 0b111;

/*
void setRGBColor(byte colorCode) {
  // Extract bits for each color using bitwise AND
  // Red is the least significant bit (LSB)
  digitalWrite(button_1_2_R, (colorCode & 0b001) ? HIGH : LOW);

  // Green is the middle bit
  digitalWrite(button_1_3_G, (colorCode & 0b010) ? HIGH : LOW);

  // Blue is the most significant bit (MSB)
  digitalWrite(button_1_4_B, (colorCode & 0b100) ? HIGH : LOW);
}
*/
void setup() {
  Serial.begin(9600);

  // Depending on the usecase set theese GPIO as follows:

  // For RGB-buttons 
  pinMode(button_1_1_Push, INPUT);
  pinMode(button_1_2_R, OUTPUT);
  pinMode(button_1_3_G, OUTPUT);
  pinMode(button_1_4_B, OUTPUT);
  // For buttons like d-pad
  /*
  pinMode(button_1_1_Push, INPUT);
  pinMode(button_1_2_R, INPUT);
  pinMode(button_1_3_G, INPUT);
  pinMode(button_1_4_B, INPUT);
  */

  // Set button light pin as output
  pinMode(button_1_light, OUTPUT);

  // Initialize light brightness from 0-255
  analogWrite(button_1_light, 180); // Set light to half (128)

  // Set colour of RGB light
  //0b000 (0): All OFF
  //0b001 (1): Red ON
  //0b010 (2): Green ON
  //0b011 (3): Red + Green ON (Yellow)
  //0b100 (4): Blue ON
  //0b101 (5): Red + Blue ON (Magenta)
  //0b110 (6): Green + Blue ON (Cyan)
  //0b111 (7): All ON (White)
  setRGBColor(colorCode);
}

void setRGBColor(byte colorCode) {
  // Extract bits for each color using bitwise AND
  // Red is the least significant bit (LSB)
  digitalWrite(button_1_2_R, (colorCode >> 0) & 1);

  // Green is the middle bit
  digitalWrite(button_1_3_G, (colorCode >> 1) & 1);

  // Blue is the most significant bit (MSB)
  digitalWrite(button_1_4_B, (colorCode >> 2) & 1);
}

void loop() {
  // Read button(s) state
  int But = digitalRead(button_1_1_Push);

  // Debugging: print button states
  if (But == HIGH) {
    Serial.println("uh. Tryk på mig din frækkert");
  }
  else{
   // Serial.println("...");
  }
  Serial.print("R");
  Serial.print((colorCode >> 0) & 1);
  Serial.print(", G");
  Serial.print((colorCode >> 1) & 1);
  Serial.print(", B");
  Serial.println((colorCode >> 2) & 1 );

  /*
  for (int i = 0; i <= 7; i++) {
    setRGBColor(i); // Test all colors from 0 to 7
    delay(1000);    // Wait 1 second for each color
  }
  */
}