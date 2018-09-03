#include "./PinChangeInt.h"

#define PIN_COUNT 4

//RANGES (Min, Mid, Max):
//Throttle (Ch3, 9): 1096,

const int pinMap[4] = {7, 8, 16, 17};
const int bPinMap[20] = { 0, 0, 0, 0, 0,
                          0, 0, 0, 1, 2,
                          3, 0, 0, 0, 0,
                          0, 2, 3, 2, 3,
                        };
volatile unsigned long pwm_value[PIN_COUNT] = {0, 0, 0, 0};
volatile unsigned long prev_time[PIN_COUNT] = {0, 0, 0, 0};
volatile uint8_t lastPin;

void rising()
{
  lastPin = PCintPort::arduinoPin;
  //Serial.println(lastPin);
  PCintPort::attachInterrupt(lastPin, &falling, FALLING);
  prev_time[bPinMap[lastPin]] = micros();
}

void falling() {
  lastPin = PCintPort::arduinoPin;
  //Serial.print(lastPin);
  PCintPort::attachInterrupt(lastPin, &rising, RISING);
  pwm_value[bPinMap[lastPin]] = micros() - prev_time[bPinMap[lastPin]];
}

void setup() {
  Serial.begin(115200);
  Serial.println("Serial initialized!");
  for (int i = 0; i < PIN_COUNT; ++i)
  {
    pinMode(pinMap[i], INPUT); digitalWrite(pinMap[i], HIGH);
    PCintPort::attachInterrupt(pinMap[i], &rising, RISING);
  }
}
long lastMillis = 0;
void loop() {
  long currentMillis = millis();
  if (currentMillis - lastMillis > 50) {
    Serial.print(pwm_value[0]);
    Serial.flush();
    Serial.print("x");
    Serial.print(pwm_value[1]);
    Serial.flush();
    Serial.print("x");
    Serial.print(pwm_value[2]);
    Serial.flush();
    Serial.print("x");
    Serial.println(pwm_value[3]);
    Serial.flush();
    lastMillis = currentMillis;
  }
}
