// PinChangeIntExample
// This only works for ATMega328-compatibles; ie, Leonardo is not covered here.
// See the Arduino and the chip documentation for more details.
// See the Wiki at http://code.google.com/p/arduino-pinchangeint/wiki for more information.

// for vim editing: :set et ts=2 sts=2 sw=2

// This example demonstrates a configuration of 3 interrupting pins and 2 interrupt functions.
// The functions set the values of some global variables. All interrupts are serviced immediately,
// and the sketch can then query the values at our leisure. This makes loop timing non-critical.

// The interrupt functions are a simple count of the number of times the pin was brought high.
// For 2 of the pins, the values are stored and retrieved from an array and they are reset after
// every read. For one of the pins ("MYPIN3"), there is a monotonically increasing count; that is,
// until the 8-bit value reaches 255. Then it will go back to 0.

// For a more introductory sketch, see the SimpleExample328.ino sketch in the PinChangeInt
// library distribution.

#include "./PinChangeInt.h"

// Modify these at your leisure.
#define MY_PIN  A3
#define MY_PIN1 A4
#define MY_PIN2 A5
#define MY_PIN2 A6
///

 
volatile int pwm_value = 0;
volatile int pwm_value1 = 0;
volatile int pwm_value2 = 0;
volatile int pwm_value3 = 0;
volatile int prev_time = 0;
volatile int prev_time1 = 0;
volatile int prev_time2 = 0;
volatile int prev_time3 = 0;
uint8_t latest_interrupted_pin;
uint8_t latest_interrupted_pin1;
uint8_t latest_interrupted_pin2;
uint8_t latest_interrupted_pin3;
void rising()
{
  latest_interrupted_pin=PCintPort::arduinoPin;
  PCintPort::attachInterrupt(latest_interrupted_pin, &falling, FALLING);
  prev_time = micros();
}
void rising1()
{
  latest_interrupted_pin1=PCintPort::arduinoPin;
  PCintPort::attachInterrupt(latest_interrupted_pin1, &falling1, FALLING);
  prev_time1 = micros();
}
void rising2()
{
  latest_interrupted_pin2=PCintPort::arduinoPin;
  PCintPort::attachInterrupt(latest_interrupted_pin2, &falling2, FALLING);
  prev_time2 = micros();
}
void rising3()
{
  latest_interrupted_pin3=PCintPort::arduinoPin;
  PCintPort::attachInterrupt(latest_interrupted_pin3, &falling3, FALLING);
  prev_time3 = micros();
}
 
void falling() {
  latest_interrupted_pin=PCintPort::arduinoPin;
  PCintPort::attachInterrupt(latest_interrupted_pin, &rising, RISING);
  pwm_value = micros()-prev_time;

}
void falling1() {
  latest_interrupted_pin1=PCintPort::arduinoPin;
  PCintPort::attachInterrupt(latest_interrupted_pin1, &rising1, RISING);
  pwm_value1 = micros()-prev_time1;
}
void falling2() {
  latest_interrupted_pin2=PCintPort::arduinoPin;
  PCintPort::attachInterrupt(latest_interrupted_pin2, &rising2, RISING);
  pwm_value2 = micros()-prev_time2;
}
void falling3() {
  latest_interrupted_pin3=PCintPort::arduinoPin;
  PCintPort::attachInterrupt(latest_interrupted_pin3, &rising3, RISING);
  pwm_value2 = micros()-prev_time3;
}
 
 
void setup() {
  pinMode(MY_PIN, INPUT); digitalWrite(MY_PIN, HIGH);
  pinMode(MY_PIN1, INPUT); digitalWrite(MY_PIN1, HIGH);
  pinMode(MY_PIN2, INPUT); digitalWrite(MY_PIN2, HIGH);
  Serial.begin(115200);
  PCintPort::attachInterrupt(MY_PIN, &rising, RISING);
  PCintPort::attachInterrupt(MY_PIN1, &rising1, RISING);
  PCintPort::attachInterrupt(MY_PIN2, &rising2, RISING);
}
 
void loop() { 

  Serial.print(pwm_value, DEC);
  Serial.print("\t");   
  Serial.print(pwm_value1, DEC);
  Serial.print("\t");   
  Serial.print(pwm_value2, DEC);
  Serial.print("\t");   
  Serial.println(pwm_value3, DEC);
  delay(100);


  }

