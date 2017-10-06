

int motorSpeed1 = 0;
int motorPin1 = 9;
int motorSpeed2 = 0;
int motorPin2 = 10;
int pinSwitch = 2;

int muse1 = 0;
int muse2 = 0;
int switchS = 0;

void setup() {
    Serial.begin(9600);
    //Serial.println("Hello Computer");
}

void loop() {
    // communication with pyserial
    if (Serial.available()) {
        //Serial.println("RECEIVED");
        String data = Serial.readString();
        String dataP1 = data.substring(0,3);
        String dataP2 = data.substring(3,6);
        int museDataP1 = dataP1.toInt();
        int museDataP2 = dataP2.toInt();
        if (museDataP1 >= 100 and museDataP2 >= 100) {
          motorSpeed1 = museDataP1 - 100;
          Serial.println("Muse 1");
          Serial.println(motorSpeed1);
          motorSpeed2 = museDataP2 - 100;
          Serial.println("Muse 2");
          Serial.println(motorSpeed2);
        }
    }
    
    switchS = digitalRead(pinSwitch);
    
    if (switchS == HIGH) {
      analogWrite(motorPin1, 0);
      analogWrite(motorPin2, 0);
      delay(100);
      }
     else {
      analogWrite(motorPin1, 0);
      analogWrite(motorPin2, 0);
      delay(100);
     }
    //Serial.println("Ready");
}
