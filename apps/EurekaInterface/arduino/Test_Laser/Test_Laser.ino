
#include <Servo.h>
Servo s1;
Servo s2;

int pinSwitch   = 3;
int switchS = 0;

int muse1 = 0;
int motorPin1 = 10;
int motorSpeed1 = 0;
int Laser1      = 13;
int Detector1   = 12;
int servo1      = 5;

int muse2 = 0;
int motorPin2 = 11;
int motorSpeed2 = 0;
int Laser2      = 5;
int Detector2   = 9;
int servo2      = 6;


void setup() { 
  s1.attach(servo1);
  s2.attach(servo2); 
  pinMode(Laser1, OUTPUT);
  pinMode(Detector1, INPUT);
  pinMode(Laser2, OUTPUT);
  pinMode(Detector2, INPUT);
  Serial.begin(9600);
  Serial.print("Hello Computer");
}

void loop() { 
  digitalWrite(Laser1, HIGH);
//  digitalWrite(Laser2, HIGH);
  s1.write(0);
//  s2.write(0);

  int win1 = digitalRead(Detector1);
  int win2 = digitalRead(Detector2);
  Serial.print(win2);
  Serial.print('\n');
  
  
  if ( win1 == 0 ){
    analogWrite(motorPin1, 0);
    analogWrite(motorPin2, 0);
    //s1.write(180);   
    //delay(2000);
   // s1.write(0);
   // delay(1000);
//    while (1) {
//    }
  }

//  if ( win2 == 0 ){
//    analogWrite(motorPin1, 0);
//    analogWrite(motorPin2, 0);
//    s2.write(180);
//    delay(2000);
//    s2.write(0);
//  }

//  if (Serial.available()) {
//    //Serial.println("RECEIVED");
//    String data = Serial.readString();
//    String dataP1 = data.substring(0,3);
//    String dataP2 = data.substring(3,6);
//    int museDataP1 = dataP1.toInt();
//    int museDataP2 = dataP2.toInt();
//    if (museDataP1 >= 100 and museDataP2 >= 100) {
//      motorSpeed1 = museDataP1 - 50;
//      Serial.println("Muse 1");
//      Serial.println(motorSpeed1);
//      motorSpeed2 = museDataP2 - 50;
//      Serial.println("Muse 2");
//      Serial.println(motorSpeed2);
//        }
//    }
    
    switchS = digitalRead(pinSwitch);
    
    if (switchS == HIGH) {
      analogWrite(motorPin1, 0);
      analogWrite(motorPin2, 0);
      delay(100);
      }
       else {
      analogWrite(motorPin1, motorSpeed1);
      analogWrite(motorPin2, motorSpeed2);
      delay(100);
     }
    //Serial.println("Ready");
}
