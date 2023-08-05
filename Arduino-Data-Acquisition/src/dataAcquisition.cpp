// Arduino based 1 channel DAQ system
// This sketch will read the data from the A0 channel

#include <Arduino.h>

int AnalogPin_AN1 = A0;    // select the input pin

void setup() 
{
   Serial.begin(9600); //Data will be sent to PC @9600bps
}

void loop() 
{
   int data1 = 0;

   data1 = analogRead(AnalogPin_AN1);
   
   Serial.println(data1);
   delay(1000); // delay to ensure we sample once every second
}