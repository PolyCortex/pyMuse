

int motorSpeed1 = 0;
int motorPin1 = 9;
int motorSpeed2 = 0;
int motorPin2 = 10;

int muse1 = 0;
int muse2 = 0;

void setup() {
    Serial.begin(9600);
    Serial.println("Hello Computer");
}

void loop() {
  
    // communication pyserial
    // read from port 0, send to port 1:
    if (Serial.available()) {
        int museData = Serial.parseInt();
        //Serial.write(museData);
        if (museData >= 100 and museData <= 355) {
            motorSpeed1 = museData - 100;
            Serial.println("Muse 1");
            Serial.println(motorSpeed1);
        } else if (museData >= 400 and museData <= 655){
            motorSpeed2 = museData - 400;
            Serial.println("Muse 2");
            Serial.println(motorSpeed2);
        }
    }

    analogWrite(motorPin1, motorSpeed1);
    analogWrite(motorPin2, motorSpeed2);
    delay(100);
}
