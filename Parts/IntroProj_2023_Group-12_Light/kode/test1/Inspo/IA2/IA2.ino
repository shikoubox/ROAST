//Gruppe 5 IA2 Simon Voss
const int pwmPin = 6; //PWM pin output
const int aSeenPin = 2; //sensor A
const int bSeenPin = 3; //sensor B
const int voltageReadPin = 0; //analog Voltage input
const double gearRatio = 7.2; //Gear ratio til motoren


const double voltageMin = 1.3; //Min limit for inputspændingen
const double voltageMax = 3.95; //Max limit for inputspændingen
static double voltage;                //Pladsholder til avgVoltage
static double avgVoltage = 2.5;       //avgVoltage baceret på samples
static int voltageCounter = 0;        //Tæller for avgVoltage
int voltageSamples = 10;       //Antal ønskede samples
static double inputVoltage;           //Aktuel ingangsspæning

static double targetDutyCycle = 0.5;        //ønskede dutycycle i %
static double dutyCycle = 0.5;              //Angivet i %
static  double pwmDuty;                      //Tal imellem 0 til 255
double dutyCycleIncrement = 0.000001; //Increment af dutyCycle, skal være et meget lille tal

static int previusCounter = 0;     //Tidligere position
static int currentCounter = 0;     // currentCounter af position 0 til 675
static int targetCounter ;      // Ønskede counter position
static double cmPosition = 0;      //Position i cm

static int stepBlocker = 0;      //Blokerer anden step funktion til nedsætning af hastighed
static double command;           // Input fra brugeren position 0 til 90, kald 91: Start,92: Stop,93: Nulstil punkt
int retning = 1;              // Enten 1 eller 0
static int positionsPrint = 0;   //Variable så der ikke printes konstant

int menuInput;

void setup() {
//Set correct pwm frequency (ca. 32 kHz)
  TCB0_CTRLA = (TCB_CLKSEL_CLKDIV2_gc) | (TCB_ENABLE_bm);
  TCB1_CTRLA = (TCB_CLKSEL_CLKDIV2_gc) | (TCB_ENABLE_bm);
  TCB2_CTRLA = (TCB_CLKSEL_CLKDIV2_gc) | (TCB_ENABLE_bm);
  
//Pin modes:
  pinMode(pwmPin, OUTPUT);
  pinMode(voltageReadPin, INPUT);
  pinMode(aSeenPin, INPUT_PULLUP);
  pinMode(bSeenPin, INPUT_PULLUP);
  
//Interrupt for counting distance
  attachInterrupt(digitalPinToInterrupt(aSeenPin), sensor, RISING);
  
//Open serial port writing:
  Serial.begin(115200);
  
//Skriver PWM til output
  pwmDuty = dutyCycle * 255;
  analogWrite(pwmPin, pwmDuty);
}

void loop() {
  getCommand(); //Input fra brugeren
  positionCounter(); //Udrening af position  
  //sensor();   //Interrupt funktion
  //stepToDuty(dutyCycle); //Incrementerende step af dutyCycle
  threashold(); //Udregning af overforbrug
  if(threashold() == 1){
    //stop!
    dutyCycle = 0.5;
    pwmDuty = dutyCycle * 255;
    analogWrite(pwmPin, pwmDuty);
    Serial.println("Noedstop!");
    if(Serial.parseInt() == 92){
      return;
    }
  }
  pwmDuty = dutyCycle * 255;
  analogWrite(pwmPin, pwmDuty);
}

void sensor(){            //Interrupt funktion sensor a fungerer som Clock og aktiverer funktion
    if(digitalRead(bSeenPin) == true){ //Hvis sensor b er blokeret køres der den ene vej
      currentCounter++;
    }else{                //Hvis sensor b er åben køres der den anden vej
      currentCounter--;
  }
}


void positionCounter(){
  while(currentCounter < 0 || currentCounter > 651){ //Tjekker for om motoren er ude for banen hvis ja stoppes motoren.
    //stop!
    dutyCycle = 0.5;
    pwmDuty = dutyCycle * 255;    
    analogWrite(pwmPin, pwmDuty);    
    Serial.print("Ude af banen");
    Serial.print(currentCounter);
    Serial.println();
    Serial.println("Skriv 800 for at retunere og nulpunktet sættes");
      if(Serial.parseInt() == 800){
         currentCounter = 0;
         return;
      }
  } 

    //Bestemmer retning baceret på currentCounter til targetCounter
    if (targetCounter - currentCounter > 0) {
       retning = 1;
       Serial.println(targetCounter - currentCounter);
    }
    if (targetCounter - currentCounter < 0) {
       retning = 0;
       Serial.println(targetCounter - currentCounter);
    }

/*
    //Sætter hastigheden ned omkring ønsket punkt
    if(abs(targetCounter - currentCounter) < 30){ 
      if(retning){
        stepBlocker = 1;
        dutyCycle = 0.44;
      }else
        stepBlocker = 1;
        dutyCycle = 0.56;
    }
*/
  
    //Stopper motoren når punktet er nået
    if(abs(targetCounter - currentCounter) < 1){  
      //stop!
      dutyCycle = 0.5;
      pwmDuty = dutyCycle * 255;    
      analogWrite(pwmPin, pwmDuty);
      stepBlocker = 0;
      positionsPrint++;
      if(positionsPrint == 1000){
        Serial.print("Du er nået til punkt: ");
        Serial.print(currentCounter/gearRatio);
        Serial.println();
        positionsPrint = 0;
      }
    }else if(retning == 1) { //stepblocker
        dutyCycle = 0.40;
        //stepToDuty(0.40);
     }else if(retning == 0){ //stepblocker
        dutyCycle = 0.60;
       // stepToDuty(0.60);
     }       
}

void getCommand() {
  if (Serial.available() > 0) {
    command = Serial.parseInt();
     if (command < 651 && command >= 0) {        //Tal fra 0 til 90 er placering 
      targetCounter = command;
      //command = 1000;                            //For at command ikke kontinuerligt skriver det samme ind
      Serial.read();
      Serial.print("Ønsket position: ");
      Serial.print(targetCounter/gearRatio);
      Serial.println();
      Serial.print("Retning: ");
      Serial.print(retning);
      Serial.println();
    }
    if (command == 700) {                         //Motoren stopper og nulstilles
        Serial.println("Stop");
        dutyCycle = 0.5;
    }

    if (command == 800) {
        Serial.print("Udgangspunkt sat til: ");
        currentCounter = 0;     
        Serial.print(currentCounter); 
         
    }
    if(command == 900){
      retning = 0;
    }
    if(command == 901){
      retning = 1;
    }
    
  }
}

void stepToDuty(double targetDutyCycle){
  if(dutyCycle == targetDutyCycle){
    return;
  }
  if(dutyCycle < targetDutyCycle){
     dutyCycle += dutyCycleIncrement;
     
  }
  if(dutyCycle > targetDutyCycle){
     dutyCycle -= dutyCycleIncrement;  
  }
}
  
int threashold(){
  inputVoltage = analogRead(voltageReadPin)*0.004882812500; //Læser input
  voltage += inputVoltage; 
  voltageCounter++;
  
  if(voltageCounter == voltageSamples){
     voltageCounter = 0;    
     avgVoltage = voltage/voltageSamples-0.43;
     voltage = 2.5;   
  }
  
  
  if(avgVoltage > voltageMax){ //Spændingen har opnået max
    return 1;
  }else if(avgVoltage < voltageMin){ //Spændingen har opnået min
    return 1;
  }else
  avgVoltage = 2.5;
  return 0;
}
