/***********************************
   Firmware for Arduino, team Alpha
   Author: Radim Lipka
   Date:   19.4.2019
 ***********************************/
// =================== LIBS ===================
#include <Servo.h>

// ================= IMPORTANT ================
// #define MOTORS_USING_PWM

// =================== PINS ===================
// Motors
#define PIN_MOTOR_A_BRAKE       9
#define PIN_MOTOR_B_BRAKE       8
#define PIN_MOTOR_A_DIRECTION   12
#define PIN_MOTOR_B_DIRECTION   13
#define PIN_MOTOR_A_SPEED       3
#define PIN_MOTOR_B_SPEED       11

// Control LEDs
#define PIN_LED_ALIVE     6
#define PIN_LED_COMMAND   7

// Servo motors
#define PIN_SERVO_A     4
#define PIN_SERVO_B     5

// ================== TIMERS ==================
// LED diods
#define DELAY_TIMER_ALIVE   250
#define DELAY_TIMER_COMMAND 100

unsigned long timerAlive   = 0;
unsigned long timerCommand = 0;

// ================== MOTORS ==================

#define MOTOR_FORWARD  true
#define MOTOR_BACKWARD false

#define MOTOR_BREAK_ON  true
#define MOTOR_BREAK_OFF false

#define MOTOR_ZERO_SPEED 0

unsigned long int motorAtime  = 0;
unsigned long int motorBtime  = 0;
unsigned int motorApower = 0;
unsigned int motorBpower = 0;

bool motorAdirection = MOTOR_FORWARD;
bool motorBdirection = MOTOR_FORWARD;

#define MOTOR_PERIOD            10
#define MOTOR_WORKING_PERIOD    10
#define MOTOR_NON_WORKING_PERIOD (MOTOR_PERIOD - MOTOR_WORKING_PERIOD)

#if MOTOR_WORKING_PERIOD != MOTOR_PERIOD
#warning "You are using PWM!"
#endif

unsigned long motorTimer = 0;
bool motorARunning       = true;
bool motorBRunning       = true;

// ================== SERVOS ==================

#define SERVO_DEGREES_0    13
#define SERVO_DEGREES_90   90
#define SERVO_DEGREES_180  170

#define SERVO_FIX_INACCURACY(VALUE, LOWEST, HIGHEST) (LOWEST + (VALUE * (HIGHEST - LOWEST) / 90))

short unsigned int servoAdegrees = 0;
short unsigned int servoBdegrees = 0;

unsigned short servoAval = 90;
unsigned short servoBval = 90;

Servo servoA;
Servo servoB;

// ================== SERIAL ==================
#define SERIAL_BAUD_RATE 115200
#define MAX_PARAMS 8
String serialInputBuffer[MAX_PARAMS];
unsigned char serialInputBufferPtr = 0;

// =================== LEDS ===================

bool stateAliveLed   = false;
bool stateCommandLed = false;

// =============== DEFINITIONS ================
void processLeds();
void arrayInit(String * inArray, unsigned int stringSize);
void processServos();
void processMotor();

// ********************************************
// === THE CODE   =============================
// ********************************************

void setup()
{
  Serial.begin(115200);

  pinMode(PIN_MOTOR_A_BRAKE, OUTPUT);
  pinMode(PIN_MOTOR_B_BRAKE, OUTPUT);
  pinMode(PIN_MOTOR_A_DIRECTION, OUTPUT);
  pinMode(PIN_MOTOR_B_DIRECTION, OUTPUT);
  pinMode(PIN_MOTOR_A_SPEED, OUTPUT);
  pinMode(PIN_MOTOR_B_SPEED, OUTPUT);

  digitalWrite(PIN_MOTOR_A_BRAKE, MOTOR_BREAK_OFF);
  digitalWrite(PIN_MOTOR_B_BRAKE, MOTOR_BREAK_OFF);
  digitalWrite(PIN_MOTOR_A_DIRECTION, motorAdirection);
  digitalWrite(PIN_MOTOR_B_DIRECTION, motorBdirection);
  analogWrite(PIN_MOTOR_A_SPEED, MOTOR_ZERO_SPEED);
  analogWrite(PIN_MOTOR_B_SPEED, MOTOR_ZERO_SPEED);

  pinMode(PIN_LED_ALIVE,   OUTPUT);
  pinMode(PIN_LED_COMMAND, OUTPUT);

  servoA.attach(PIN_SERVO_A);
  servoB.attach(PIN_SERVO_B);
}

void loop()
{
  processLeds();
  processServos();
  processMotors();
}

void processServos()
{
  servoA.write(servoAval);
  servoB.write(servoBval);
}

void processMotors()
{
  digitalWrite(PIN_MOTOR_A_DIRECTION, motorAdirection);
  digitalWrite(PIN_MOTOR_B_DIRECTION, motorBdirection);

  if ((motorAtime > millis()))
  {
    analogWrite(PIN_MOTOR_A_SPEED, motorApower);
    motorARunning = true;
  } else
  {
    analogWrite(PIN_MOTOR_A_SPEED, MOTOR_ZERO_SPEED);
    motorARunning = false;
  }

  if ((motorBtime > millis()))
  {
    analogWrite(PIN_MOTOR_B_SPEED, motorBpower);
    motorBRunning = true;
  } else
  {
    analogWrite(PIN_MOTOR_B_SPEED, MOTOR_ZERO_SPEED);
    motorBRunning = false;
  }
}

void processLeds()
{
  if (timerAlive < millis())
  {
    timerAlive = millis() + DELAY_TIMER_ALIVE;
    stateAliveLed = stateAliveLed ? false : true; // Toggle boolean value
    digitalWrite(PIN_LED_ALIVE, stateAliveLed);
  }

  if ((timerCommand < millis()) && stateCommandLed)
  {
    stateCommandLed = false;
    digitalWrite(PIN_LED_COMMAND, stateCommandLed);
  }
}

void everythingStop()
{
  motorApower = MOTOR_ZERO_SPEED;
  motorBpower = MOTOR_ZERO_SPEED;
  analogWrite(PIN_MOTOR_A_SPEED, MOTOR_ZERO_SPEED);
  analogWrite(PIN_MOTOR_B_SPEED, MOTOR_ZERO_SPEED);
}

void arrayInit(String * inArray, unsigned int stringSize)
{
  for (int i = 0; i != stringSize; i++)
    inArray[i] = "";
}

// ********************************************
// === INTERRUPTS   ===========================
// ********************************************

void serialEvent()
{
  while (Serial.available())
  {
    timerCommand = millis() + DELAY_TIMER_COMMAND;
    stateCommandLed = true;
    digitalWrite(PIN_LED_COMMAND, stateCommandLed);

    char inChar = (char)Serial.read();
    if (inChar == '\n' || inChar == '\0')
    {
      serialInputBuffer[serialInputBufferPtr] += '\0';

      // Handle commands referring to motors M F 255 9999 B 0 0
      if (serialInputBuffer[0] == "M" && serialInputBufferPtr >= 6)
      {
        motorAdirection = (serialInputBuffer[1] == "F" ? MOTOR_FORWARD : MOTOR_BACKWARD);
        motorApower = serialInputBuffer[2].toInt();
        motorAtime = millis() + serialInputBuffer[3].toInt();
        motorBdirection = (serialInputBuffer[4] == "F" ? MOTOR_FORWARD : MOTOR_BACKWARD);
        motorBpower = serialInputBuffer[5].toInt();
        motorBtime = millis() + serialInputBuffer[6].toInt();
        if (motorApower > 254) motorApower = 255;
        if (motorApower < 0) motorApower = 0;
        if (motorBpower > 254) motorBpower = 255;
        if (motorBpower < 0) motorBpower = 0;

        Serial.println(motorAdirection);
        Serial.println(motorBdirection);
        Serial.println("OK - Motor CMD");

        // Handle commands referring to servos S 90 90
      } else if (serialInputBuffer[0] == "S" && serialInputBufferPtr == 2)
      {
        servoAval = serialInputBuffer[1].toInt();
        servoBval = serialInputBuffer[2].toInt();
        if (servoAval > 180) servoAval = 180;
        if (servoAval < 0) servoAval = 0;
        if (servoBval > 180) servoBval = 180;
        if (servoBval < 0) servoBval = 0;

        // Fixing inaccuracy of servo motors
        if (servoAval < 90)
          servoAval = SERVO_FIX_INACCURACY(servoAval, SERVO_DEGREES_0, SERVO_DEGREES_90);
        else
          servoAval = SERVO_FIX_INACCURACY(servoAval - 90, SERVO_DEGREES_90, SERVO_DEGREES_180);

        if (servoBval < 90)
          servoBval = SERVO_FIX_INACCURACY(servoBval, SERVO_DEGREES_0, SERVO_DEGREES_90);
        else
          servoBval = SERVO_FIX_INACCURACY(servoBval - 90, SERVO_DEGREES_90, SERVO_DEGREES_180);

        Serial.println("OK - Servo CMD");

        // Handle commands referring to controll C STOP
      } else if (serialInputBuffer[0] == "C" && serialInputBufferPtr == 1)
      {
        if (serialInputBuffer[1] == "STOP")
        {
          everythingStop();
          Serial.println("OK - Control CMD STOP");
        } else
        {
          Serial.println("FAIL - Control CMD unrecognized");
        }
      } else
      {
        Serial.print("ERR - Unrecognized command: ");
        for (int i = 0; i != MAX_PARAMS; i++)
          Serial.print(serialInputBuffer[i]);
        Serial.println(" ");
      }

      serialInputBufferPtr = 0;
      arrayInit(serialInputBuffer, MAX_PARAMS);
    } else if (inChar == ' ')
    {
      serialInputBuffer[serialInputBufferPtr] += '\0';
      serialInputBufferPtr++;
      if (serialInputBufferPtr >= MAX_PARAMS)
      {
        Serial.println("ERR - Serial Input buffer OVERFLOW!");
        serialInputBufferPtr = 0;
      }
    } else
    {
      serialInputBuffer[serialInputBufferPtr] += inChar;
    }
  }
}
