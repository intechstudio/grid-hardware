/*
 Controlling a servo position using a potentiometer (variable resistor)
 by Michal Rinott <http://people.interaction-ivrea.it/m.rinott>

 modified on 8 Nov 2013
 by Scott Fitzgerald
 http://www.arduino.cc/en/Tutorial/Knob
*/

#include <Servo.h>

Servo myservo;  // create servo object to control a servo


void setup() {
  myservo.attach(11);  // attaches the servo on pin 11 to the servo object
  pinMode(3, INPUT_PULLUP);
  pinMode(13, OUTPUT);
}

void loop() {

  int pinState = digitalRead(3);

  if (pinState){
    
    myservo.write(65);
    digitalWrite(13, HIGH);
    
  }
  else{
    
    myservo.write(90);
    digitalWrite(13, LOW);
  }

  delay(5);                           // waits for the servo to get there
}
