
void setup() {
  pinMode(LED_BUILTIN, OUTPUT);      // set LED pin as output
  digitalWrite(LED_BUILTIN, LOW);    // switch off LED pin

  Serial.begin(115200);              // initialize serial communication at 9600 bits per second:
  Serial1.begin(115200);            // initialize UART with the first board with baud rate of 9600

}

void loop() {
  // check if there is any incoming byte to read from the Serial Monitor
  if (Serial.available() > 0){
    delay(2);
    char inByte = Serial.read();

    switch (inByte){
      // Send to receiver 1

      case '0':
      Serial1.println('0');
      Serial.println('0');
      break;
      
      case '1':
      Serial1.println('1');
      Serial.println('1');
      break;

      case '2':
      Serial1.println('2');
      Serial.println('2');
      break;

      case '3':
      Serial1.println('3');
      Serial.println('3');
      break;

      case '4':
      Serial1.println('4');
      Serial.println('4');
      break;

      case '5':
      Serial1.println('5');
      Serial.println('5');
      break;

      case '6':
      Serial1.println('6');
      Serial.println('6');
      break;

      case '7':
      Serial1.println('7');
      Serial.println('7');
      break;

      case '8':
      Serial1.println('8');
      Serial.println('8');
      break;
           
      default:
      break;
    }
  }

  if(Serial1.available() > 0) {
    delay(2);
    char outByte = Serial1.read();

    Serial.println(outByte);

    
  }
}
