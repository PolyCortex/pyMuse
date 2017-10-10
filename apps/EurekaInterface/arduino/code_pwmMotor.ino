#define DC_MOTOR_PIN1 9
#define DC_MOTOR_PIN2 10
#define ONOFF 3
int mode=1;
int i=150;

void setup() {
  /* Initialize DC motor control pin as digital output */
  pinMode( DC_MOTOR_PIN1, OUTPUT );
  pinMode( DC_MOTOR_PIN2, OUTPUT );
  pinMode( ONOFF, INPUT );
  attachInterrupt(digitalPinToInterrupt(ONOFF),TRIGGER,RISING);
}

void TRIGGER()
{
  if(mode==0)
  {
    mode=1;
  }
  else
  {
    mode=0;
  }
}
void loop() 
{ 
  while(1)
  {
    if(mode==1)
    {
    analogWrite( DC_MOTOR_PIN1, i );
    analogWrite( DC_MOTOR_PIN2, i );
    }
    if(mode==0)
    {
    analogWrite( DC_MOTOR_PIN1, 0 ); 
    analogWrite( DC_MOTOR_PIN2, 0 );
   }
  }
}
