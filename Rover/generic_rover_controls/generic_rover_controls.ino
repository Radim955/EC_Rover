#include <Servo.h>

#define MOTOR_A1 11
#define MOTOR_A2 10
#define MOTOR_B1 9
#define MOTOR_B2 8
#define PIN_SERVO_X 5
#define PIN_SERVO_Y 6

#define IMPULSE 4

//Motor A
short motorAtime = 0;
boolean motorAfwd = true;
byte motorApower = 0;
byte motorApowerT = 0;

//Motor B
short motorBtime = 0;
boolean motorBfwd = true;
byte motorBpower = 0;
byte motorBpowerT = 0;

//Servos
short servoXval = 90;
short servoYval = 90;
Servo servoX;
Servo servoY;

//-- Serial
#define MAX_PARAMS 8
int paramIndex = 0;
String params[MAX_PARAMS];

void setup() {
  Serial.begin(115200);
  pinMode(MOTOR_A1, OUTPUT);
  pinMode(MOTOR_A2, OUTPUT);
  pinMode(MOTOR_B1, OUTPUT);
  pinMode(MOTOR_B2, OUTPUT);
  
  for(int i=0; i < MAX_PARAMS; i++){
    params[i] = "";
  }
  
  //Set PWM frequency on pins 9 and 10
  TCCR1B = (TCCR1B & 0b11111000) | 0x05;
  
  servoX.attach(PIN_SERVO_X);
  servoY.attach(PIN_SERVO_Y);
}

int bbpwmt = 0;

void loop(){
  
  //"Manual" PWM generation for smoother motor controls
  bbpwmt++;
  if(bbpwmt >= 255){
    bbpwmt = 0;
    motorAtime--;
    motorBtime--;
    if(motorApower > motorApowerT){
      if(motorApowerT >= 244){
        motorApowerT = 254;
      } else {
        motorApowerT += 1;
      }
    } else if(motorApower < motorApowerT){
      motorApowerT--;
    }
  
    if(motorBpower > motorBpowerT){
      if(motorBpowerT >= 244){
        motorBpowerT = 254;
      } else {
        motorBpowerT += 1;
      }
    } else if(motorBpower < motorBpowerT){
      motorBpowerT--;
    }
  }
  
  //Motor powers update
  if(bbpwmt < motorApowerT && motorAtime > 0){
    if(motorAfwd){
      digitalWrite(MOTOR_A1, HIGH);
      digitalWrite(MOTOR_A2, LOW);    
    } else {
      digitalWrite(MOTOR_A1, LOW);
      digitalWrite(MOTOR_A2, HIGH);
    }
  } else {
    digitalWrite(MOTOR_A1, LOW);
    digitalWrite(MOTOR_A2, LOW);
  }
  
  if(bbpwmt < motorBpowerT && motorBtime > 0){
    if(motorBfwd){
      digitalWrite(MOTOR_B1, HIGH);
      digitalWrite(MOTOR_B2, LOW);
    } else {
      digitalWrite(MOTOR_B1, LOW);
      digitalWrite(MOTOR_B2, HIGH);
    }
  } else {
    digitalWrite(MOTOR_B1, LOW);
    digitalWrite(MOTOR_B2, LOW);
  }
  
  //servoX.write(servoXval);
  //servoY.write(servoYval);

}

void serialEvent() {
  while (Serial.available()) {
    char inChar = (char)Serial.read();
    if (inChar == '\n' || inChar == '\0') {
      params[paramIndex] += "\0";
      //Handle commands referring to motors M F 255 9999 B 0 0
      if(params[0] == "M" && paramIndex >= 6){
        motorAfwd = (params[1] == "F" ? true : false);
        motorApower = params[2].toInt();
        motorAtime = params[3].toInt();
        motorBfwd = (params[4] == "F" ? true : false);
        motorBpower = params[5].toInt();
        motorBtime = params[6].toInt();
        if(motorApower > 127) motorApower = 127;
        if(motorApower < 0) motorApower = 0;
        if(motorBpower > 127) motorBpower = 127;
        if(motorBpower < 0) motorBpower = 0;
        Serial.println("OK");
      } else if(params[0] == "C" && paramIndex == 2){
        servoXval = params[1].toInt();
        servoYval = params[2].toInt();
        if(servoXval > 180) servoXval = 180;
        if(servoXval < 0) servoXval = 0;
        if(servoYval > 180) servoYval = 180;
        if(servoYval < 0) servoYval = 0;
        Serial.println("OK");
      }
      paramIndex = 0;
      for(int i=0; i < MAX_PARAMS; i++){
        params[i] = "";      
      }
    } else if(inChar == ' '){
      params[paramIndex] += "\0";
      paramIndex++;
      if(paramIndex >= MAX_PARAMS) paramIndex = 0;
    } else {
      params[paramIndex] += inChar;
    }
  }
}
